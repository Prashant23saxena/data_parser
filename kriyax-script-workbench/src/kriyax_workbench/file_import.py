from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from kriyax_workbench.audit import finish_action, start_action
from kriyax_workbench.catalog import records, register_dataframe_table, safe_identifier
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


SUPPORTED_SUFFIXES = {".csv", ".xlsx", ".xls"}


def inspect_file(file_path: Path, preview_limit: int = 20, sheet: str | None = None) -> dict[str, Any]:
    file_path = file_path.expanduser().resolve()
    frame = _read_file(file_path, sheet=sheet)
    source_columns = [str(column) for column in frame.columns]
    duplicates = _duplicates([_safe_column_name(column) for column in source_columns])
    columns = []
    for column in source_columns:
        target_name = _safe_column_name(column)
        columns.append(
            {
                "sourceName": column,
                "targetName": target_name,
                "inferredType": _infer_type(frame[column]),
                "selectedType": _infer_type(frame[column]),
                "status": "needs_rename" if target_name in duplicates else "ready",
            }
        )
    return {
        "fileName": file_path.name,
        "filePath": str(file_path),
        "rowCount": int(len(frame)),
        "sheetNames": _sheet_names(file_path),
        "columns": columns,
        "requiresRename": any(column["status"] == "needs_rename" for column in columns),
        "previewRows": records(frame.head(preview_limit)),
    }


def commit_import(
    file_path: Path,
    target_schema: str,
    table_name: str,
    columns: list[dict[str, Any]] | None = None,
    sheet: str | None = None,
) -> dict[str, Any]:
    ensure_workspace()
    file_path = file_path.expanduser().resolve()
    stored_file_path = _store_source_file(file_path)
    frame = _read_file(file_path, sheet=sheet)
    inspection = inspect_file(file_path, sheet=sheet)
    mapping = columns or inspection["columns"]
    if any(column.get("status") == "needs_rename" for column in mapping):
        raise ValueError("Column mapping contains duplicate target names. Rename them before import.")
    target_names = [safe_identifier(column["targetName"]) for column in mapping]
    if len(target_names) != len(set(target_names)):
        raise ValueError("Target column names must be unique.")
    frame = frame.copy()
    frame.columns = target_names
    frame = _apply_types(frame, mapping)
    schema = safe_identifier(target_schema)
    table = safe_identifier(table_name)
    audit = start_action(
        "file.import",
        {"filePath": str(file_path), "storedFilePath": str(stored_file_path), "targetTable": f"{schema}.{table}"},
    )
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'create schema if not exists "{schema}"')
        conn.register("import_frame", frame)
        conn.execute(f'create or replace table "{schema}"."{table}" as select * from import_frame')
        conn.unregister("import_frame")
    qualified = register_dataframe_table(
        schema,
        table,
        frame,
        {
            "kind": "file",
            "filePath": str(stored_file_path),
            "originalFilePath": str(file_path),
            "fileName": stored_file_path.name,
            "originalFileName": file_path.name,
            "importedAt": datetime.now(timezone.utc).isoformat(),
        },
    )
    result = {
        "qualifiedName": qualified,
        "rowCount": int(len(frame)),
        "columnCount": int(len(frame.columns)),
        "storedFilePath": str(stored_file_path),
    }
    finish_action(audit, "success", result)
    return result


def _read_file(file_path: Path, sheet: str | None = None) -> pd.DataFrame:
    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError("Only CSV, XLSX, and XLS files are supported.")
    if suffix == ".csv":
        return pd.read_csv(file_path)
    return pd.read_excel(file_path, sheet_name=sheet or 0)


def _store_source_file(file_path: Path) -> Path:
    uploads = workspace_paths()["uploads"]
    uploads.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    target = uploads / f"{timestamp}-{safe_identifier(file_path.stem)}{file_path.suffix.lower()}"
    shutil.copy2(file_path, target)
    return target


def _sheet_names(file_path: Path) -> list[str]:
    if file_path.suffix.lower() not in {".xlsx", ".xls"}:
        return []
    return list(pd.ExcelFile(file_path).sheet_names)


def _infer_type(series: pd.Series) -> str:
    clean = series.dropna()
    if clean.empty:
        return "text"
    if pd.api.types.is_bool_dtype(clean):
        return "boolean"
    if pd.api.types.is_integer_dtype(clean):
        return "integer"
    if pd.api.types.is_float_dtype(clean):
        return "decimal"
    parsed = pd.to_datetime(clean, errors="coerce", format="mixed")
    if parsed.notna().mean() == 1:
        return "date"
    return "text"


def _apply_types(frame: pd.DataFrame, columns: list[dict[str, Any]]) -> pd.DataFrame:
    result = frame.copy()
    for column in columns:
        name = safe_identifier(column["targetName"])
        selected = column.get("selectedType", "text")
        if selected in {"integer", "decimal"}:
            result[name] = pd.to_numeric(result[name], errors="coerce")
        elif selected in {"date", "datetime"}:
            result[name] = pd.to_datetime(result[name], errors="coerce")
        elif selected == "boolean":
            result[name] = result[name].astype("boolean")
    return result


def _safe_column_name(value: str) -> str:
    return safe_identifier(value or "column")


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates
