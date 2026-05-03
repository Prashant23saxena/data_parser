import csv
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from app.services.workspace import ensure_workspace, workspace_paths

SUPPORTED_SUFFIXES = {".csv", ".xlsx"}
TYPE_ALIASES = {
    "text": "VARCHAR",
    "integer": "BIGINT",
    "decimal": "DOUBLE",
    "date": "DATE",
    "datetime": "TIMESTAMP",
    "boolean": "BOOLEAN",
}


def inspect_file(file_path: Path, preview_limit: int = 20, display_name: str | None = None) -> dict[str, Any]:
    source_columns = _source_columns(file_path)
    frame = _read_file(file_path, source_columns=source_columns)
    preview = frame.head(preview_limit)
    inferred_types = _infer_types(frame)
    duplicate_names = _duplicates(source_columns)

    used_targets: set[str] = set()
    columns = []
    for index, source_name in enumerate(source_columns):
        target_name = _safe_column_name(source_name)
        status = "ready"
        if source_name in duplicate_names:
            status = "needs_rename"
        elif target_name in used_targets:
            status = "needs_rename"
        used_targets.add(target_name)
        columns.append(
            {
                "sourceIndex": index,
                "sourceName": source_name,
                "targetName": target_name,
                "inferredType": inferred_types[index],
                "selectedType": inferred_types[index],
                "status": status,
            }
        )

    return {
        "fileName": display_name or file_path.name,
        "filePath": str(file_path),
        "rowCount": int(len(frame.index)),
        "columns": columns,
        "requiresRename": any(column["status"] == "needs_rename" for column in columns),
        "previewRows": _records_for_json(preview, source_columns),
    }


def commit_import(
    *,
    file_path: Path,
    target_schema: str,
    table_name: str,
    columns: list[dict[str, Any]],
) -> dict[str, Any]:
    ensure_workspace()
    source_columns = _source_columns(file_path)
    frame = _read_file(file_path, source_columns=source_columns)
    target_columns = _validated_columns(columns)
    schema = _safe_identifier(target_schema)
    table = _safe_identifier(table_name)

    if len(target_columns) != len(frame.columns):
        raise ValueError("Column mapping does not match uploaded file.")

    frame = frame.copy()
    frame.columns = [column["targetName"] for column in target_columns]
    frame = _apply_selected_types(frame, target_columns)

    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute(f'create schema if not exists "{schema}"')
        conn.register("import_frame", frame)
        conn.execute(f'create or replace table "{schema}"."{table}" as select * from import_frame')
        conn.unregister("import_frame")

    entry = _catalog_entry(
        schema=schema,
        table=table,
        source_path=file_path,
        row_count=len(frame.index),
        columns=target_columns,
    )
    _upsert_catalog(entry)
    return entry


def list_catalog_tables() -> list[dict[str, Any]]:
    ensure_workspace()
    path = workspace_paths()["catalog"]
    return json.loads(path.read_text(encoding="utf-8"))


def preview_table(schema: str, table_name: str, limit: int = 20) -> dict[str, Any]:
    paths = workspace_paths()
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(table_name)
    with duckdb.connect(str(paths["database"])) as conn:
        frame = conn.execute(
            f'select * from "{safe_schema}"."{safe_table}" limit ?',
            [limit],
        ).fetchdf()
    return {
        "schema": safe_schema,
        "tableName": safe_table,
        "columns": list(frame.columns),
        "rows": _records_for_json(frame, list(frame.columns)),
    }


def rename_table(schema: str, table_name: str, new_table_name: str) -> dict[str, Any]:
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(table_name)
    safe_new_table = _safe_identifier(new_table_name)
    _guard_table(safe_schema, safe_table)
    if not safe_new_table:
        raise ValueError("New table name is required.")
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute(f'alter table "{safe_schema}"."{safe_table}" rename to "{safe_new_table}"')
    catalog = _read_catalog()
    for entry in catalog:
        if entry.get("qualifiedName") == f"{safe_schema}.{safe_table}":
            entry["tableName"] = safe_new_table
            entry["qualifiedName"] = f"{safe_schema}.{safe_new_table}"
            entry["updatedAt"] = datetime.now(timezone.utc).isoformat()
            _write_catalog(catalog)
            return entry
    raise ValueError("Catalog entry not found.")


def truncate_table(schema: str, table_name: str, confirmation: str) -> dict[str, Any]:
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(table_name)
    _guard_table(safe_schema, safe_table)
    _require_confirmation(safe_schema, safe_table, confirmation)
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute(f'delete from "{safe_schema}"."{safe_table}"')
    catalog = _read_catalog()
    for entry in catalog:
        if entry.get("qualifiedName") == f"{safe_schema}.{safe_table}":
            entry["rowCount"] = 0
            entry["updatedAt"] = datetime.now(timezone.utc).isoformat()
            _write_catalog(catalog)
            return entry
    raise ValueError("Catalog entry not found.")


def drop_table(schema: str, table_name: str, confirmation: str) -> dict[str, Any]:
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(table_name)
    _guard_table(safe_schema, safe_table)
    _require_confirmation(safe_schema, safe_table, confirmation)
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute(f'drop table "{safe_schema}"."{safe_table}"')
    catalog = [entry for entry in _read_catalog() if entry.get("qualifiedName") != f"{safe_schema}.{safe_table}"]
    _write_catalog(catalog)
    return {"dropped": True, "qualifiedName": f"{safe_schema}.{safe_table}"}


def export_table_csv(schema: str, table_name: str) -> tuple[str, str]:
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(table_name)
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        try:
            frame = conn.execute(f'select * from "{safe_schema}"."{safe_table}"').fetchdf()
        except duckdb.CatalogException as exc:
            raise ValueError("Table not found.") from exc
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(list(frame.columns))
    for row in frame.itertuples(index=False, name=None):
        writer.writerow(row)
    return f"{safe_schema}_{safe_table}.csv", buffer.getvalue()


def _source_columns(file_path: Path) -> list[str]:
    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError("Only CSV and XLSX files are supported.")

    if suffix == ".csv":
        with file_path.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
        if not header:
            raise ValueError("Uploaded CSV must include a header row.")
        return [column.strip() or f"column_{index + 1}" for index, column in enumerate(header)]

    excel = pd.ExcelFile(file_path)
    frame = pd.read_excel(excel, sheet_name=excel.sheet_names[0], nrows=0)
    return [_restore_pandas_duplicate_name(column) for column in frame.columns.astype(str)]


def _read_file(file_path: Path, source_columns: list[str]) -> pd.DataFrame:
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(file_path, header=0, names=[f"source_{index}" for index in range(len(source_columns))])
    elif suffix == ".xlsx":
        frame = pd.read_excel(file_path)
        frame.columns = [f"source_{index}" for index in range(len(frame.columns))]
    else:
        raise ValueError("Only CSV and XLSX files are supported.")
    return frame


def _infer_types(frame: pd.DataFrame) -> list[str]:
    inferred = []
    for column in frame.columns:
        series = frame[column].dropna()
        if series.empty:
            inferred.append("text")
            continue
        if pd.api.types.is_bool_dtype(series):
            inferred.append("boolean")
        elif pd.api.types.is_integer_dtype(series):
            inferred.append("integer")
        elif pd.api.types.is_float_dtype(series):
            inferred.append("decimal")
        elif pd.api.types.is_datetime64_any_dtype(series):
            inferred.append("datetime")
        else:
            parsed_dates = pd.to_datetime(series, errors="coerce", format="mixed")
            if parsed_dates.notna().mean() == 1:
                inferred.append("date")
            else:
                inferred.append("text")
    return inferred


def _apply_selected_types(frame: pd.DataFrame, columns: list[dict[str, Any]]) -> pd.DataFrame:
    converted = frame.copy()
    for column in columns:
        name = column["targetName"]
        selected_type = column["selectedType"]
        if selected_type in {"integer", "decimal"}:
            converted[name] = pd.to_numeric(converted[name], errors="coerce")
        elif selected_type in {"date", "datetime"}:
            converted[name] = pd.to_datetime(converted[name], errors="coerce")
            if selected_type == "date":
                converted[name] = converted[name].dt.date
        elif selected_type == "boolean":
            converted[name] = converted[name].astype("boolean")
        else:
            converted[name] = converted[name].astype("string")
    return converted


def _validated_columns(columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    validated = []
    for index, column in enumerate(columns):
        target_name = _safe_column_name(str(column.get("targetName") or ""))
        selected_type = str(column.get("selectedType") or column.get("inferredType") or "text")
        if selected_type not in TYPE_ALIASES:
            selected_type = "text"
        if not target_name:
            raise ValueError(f"Column {index + 1} needs a target name.")
        if target_name in seen:
            raise ValueError(f"Column name '{target_name}' is duplicated. Rename it before import.")
        seen.add(target_name)
        validated.append({**column, "targetName": target_name, "selectedType": selected_type})
    return validated


def _catalog_entry(
    *,
    schema: str,
    table: str,
    source_path: Path,
    row_count: int,
    columns: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "qualifiedName": f"{schema}.{table}",
        "schema": schema,
        "tableName": table,
        "source": {"kind": "file", "fileName": _display_file_name(source_path), "filePath": str(source_path)},
        "rowCount": int(row_count),
        "columnCount": len(columns),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "columns": [
            {
                "name": column["targetName"],
                "sourceName": column["sourceName"],
                "type": column["selectedType"],
            }
            for column in columns
        ],
    }


def _upsert_catalog(entry: dict[str, Any]) -> None:
    catalog = _read_catalog()
    remaining = [item for item in catalog if item.get("qualifiedName") != entry["qualifiedName"]]
    remaining.append(entry)
    _write_catalog(remaining)


def _read_catalog() -> list[dict[str, Any]]:
    return json.loads(workspace_paths()["catalog"].read_text(encoding="utf-8"))


def _write_catalog(catalog: list[dict[str, Any]]) -> None:
    workspace_paths()["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


def _guard_table(schema: str, table_name: str) -> None:
    if schema in {"information_schema", "pg_catalog"} or table_name.startswith("_"):
        raise ValueError("System or internal tables cannot be modified.")


def _require_confirmation(schema: str, table_name: str, confirmation: str) -> None:
    if confirmation != f"{schema}.{table_name}":
        raise ValueError("Confirmation must match the qualified table name.")


def _records_for_json(frame: pd.DataFrame, source_columns: list[str]) -> list[dict[str, Any]]:
    rows = []
    for _, row in frame.iterrows():
        record: dict[str, Any] = {}
        for index, value in enumerate(row.tolist()):
            key = source_columns[index] if index < len(source_columns) else str(frame.columns[index])
            json_value = None if pd.isna(value) else value
            if hasattr(json_value, "isoformat"):
                json_value = json_value.isoformat()
            if key in record:
                key = f"{key} ({index + 1})"
            record[key] = json_value
        rows.append(record)
    return rows


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicated: set[str] = set()
    for value in values:
        if value in seen:
            duplicated.add(value)
        seen.add(value)
    return duplicated


def _safe_column_name(value: str) -> str:
    return _safe_identifier(value)


def _safe_identifier(value: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", value.strip().lower()).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    return cleaned


def _restore_pandas_duplicate_name(value: str) -> str:
    return re.sub(r"\.\d+$", "", value)


def _display_file_name(file_path: Path) -> str:
    return re.sub(r"^[0-9a-f]{32}-", "", file_path.name)
