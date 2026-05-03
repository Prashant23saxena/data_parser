from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from kriyax_workbench.audit import finish_action, start_action
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def list_tables() -> list[dict[str, Any]]:
    ensure_workspace()
    return json.loads(workspace_paths()["catalog"].read_text(encoding="utf-8"))


def upsert_table(entry: dict[str, Any]) -> None:
    catalog = [item for item in list_tables() if item.get("qualifiedName") != entry["qualifiedName"]]
    catalog.append(entry)
    workspace_paths()["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


def preview_table(qualified_name: str, limit: int = 20) -> dict[str, Any]:
    schema, table = split_qualified_name(qualified_name)
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        frame = conn.execute(f'select * from "{schema}"."{table}" limit ?', [limit]).fetchdf()
    return {"qualifiedName": f"{schema}.{table}", "columns": list(frame.columns), "rows": records(frame)}


def search_tables(query: str) -> list[dict[str, Any]]:
    needle = query.lower()
    matches = []
    for table in list_tables():
        haystack = [table.get("qualifiedName", ""), table.get("schema", ""), table.get("tableName", "")]
        source = table.get("source", {})
        if isinstance(source, dict):
            haystack.append(source.get("kind", ""))
        haystack.extend(column.get("name", "") for column in table.get("columns", []))
        if any(needle in str(value).lower() for value in haystack):
            matches.append(table)
    return matches


def describe_table(qualified_name: str) -> dict[str, Any]:
    schema, table = split_qualified_name(qualified_name)
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        columns = conn.execute(f'describe "{schema}"."{table}"').fetchall()
        row_count = conn.execute(f'select count(*) from "{schema}"."{table}"').fetchone()[0]
    return {
        "qualifiedName": f"{schema}.{table}",
        "rowCount": int(row_count),
        "columns": [{"name": column[0], "type": str(column[1])} for column in columns],
    }


def register_dataframe_table(schema: str, table: str, frame: pd.DataFrame, source: dict[str, Any]) -> str:
    safe_schema = safe_identifier(schema)
    safe_table = safe_identifier(table)
    qualified_name = f"{safe_schema}.{safe_table}"
    entry = {
        "qualifiedName": qualified_name,
        "schema": safe_schema,
        "tableName": safe_table,
        "source": source,
        "rowCount": int(len(frame)),
        "columnCount": int(len(frame.columns)),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "columns": [{"name": str(column), "type": str(dtype)} for column, dtype in frame.dtypes.items()],
    }
    upsert_table(entry)
    return qualified_name


def rename_table(qualified_name: str, new_qualified_name: str) -> dict[str, Any]:
    schema, table = split_qualified_name(qualified_name)
    new_schema, new_table = split_qualified_name(new_qualified_name)
    if schema != new_schema:
        raise ValueError("Rename keeps the same schema in v1.")
    audit = start_action("table.rename", {"from": f"{schema}.{table}", "to": f"{new_schema}.{new_table}"})
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'alter table "{schema}"."{table}" rename to "{new_table}"')
    catalog = list_tables()
    updated = None
    for entry in catalog:
        if entry.get("qualifiedName") == f"{schema}.{table}":
            entry["qualifiedName"] = f"{new_schema}.{new_table}"
            entry["schema"] = new_schema
            entry["tableName"] = new_table
            entry["updatedAt"] = datetime.now(timezone.utc).isoformat()
            updated = entry
            break
    if updated is None:
        updated = describe_table(f"{new_schema}.{new_table}")
        updated["source"] = {"kind": "unknown"}
    workspace_paths()["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    finish_action(audit, "success", {"qualifiedName": updated["qualifiedName"]})
    return updated


def truncate_table(qualified_name: str, confirmation: str) -> dict[str, Any]:
    schema, table = split_qualified_name(qualified_name)
    expected = f"{schema}.{table}"
    if confirmation != expected:
        raise ValueError(f"Confirmation must exactly match {expected}")
    audit = start_action("table.truncate", {"qualifiedName": expected})
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'delete from "{schema}"."{table}"')
    catalog = list_tables()
    for entry in catalog:
        if entry.get("qualifiedName") == expected:
            entry["rowCount"] = 0
            entry["updatedAt"] = datetime.now(timezone.utc).isoformat()
    workspace_paths()["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    finish_action(audit, "success", {"qualifiedName": expected})
    return {"qualifiedName": expected, "rowCount": 0}


def drop_table(qualified_name: str, confirmation: str) -> dict[str, Any]:
    schema, table = split_qualified_name(qualified_name)
    expected = f"{schema}.{table}"
    if confirmation != expected:
        raise ValueError(f"Confirmation must exactly match {expected}")
    audit = start_action("table.drop", {"qualifiedName": expected})
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'drop table "{schema}"."{table}"')
    catalog = [entry for entry in list_tables() if entry.get("qualifiedName") != expected]
    workspace_paths()["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    finish_action(audit, "success", {"qualifiedName": expected})
    return {"dropped": True, "qualifiedName": expected}


def export_table(qualified_name: str, output_path: str | None = None) -> str:
    schema, table = split_qualified_name(qualified_name)
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        frame = conn.execute(f'select * from "{schema}"."{table}"').fetchdf()
    path = workspace_paths()["exports"] / f"{schema}_{table}.csv" if output_path is None else Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return str(path)


def export_table_html(qualified_name: str, output_path: str | None = None, limit: int = 100) -> str:
    schema, table = split_qualified_name(qualified_name)
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        frame = conn.execute(f'select * from "{schema}"."{table}" limit ?', [limit]).fetchdf()
    path = workspace_paths()["exports"] / f"{schema}_{table}.html" if output_path is None else Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{schema}.{table}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 24px; color: #172033; }}
    h1 {{ font-size: 20px; margin-bottom: 4px; }}
    p {{ color: #5f6b7a; margin-top: 0; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
    th, td {{ border: 1px solid #d8dee8; padding: 8px 10px; text-align: left; vertical-align: top; }}
    th {{ background: #f5f7fa; position: sticky; top: 0; }}
    tr:nth-child(even) td {{ background: #fbfcfe; }}
  </style>
</head>
<body>
  <h1>{schema}.{table}</h1>
  <p>Showing up to {limit} rows from the local DuckDB workspace.</p>
  {frame.to_html(index=False, border=0)}
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
    return str(path)


def split_qualified_name(value: str) -> tuple[str, str]:
    if "." not in value:
        raise ValueError("Use schema-qualified table names like raw.orders")
    schema, table = value.split(".", 1)
    return safe_identifier(schema), safe_identifier(table)


def safe_identifier(value: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", value.strip().lower()).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    if not cleaned:
        raise ValueError("Identifier cannot be empty")
    return cleaned


def records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return json.loads(frame.where(pd.notnull(frame), None).to_json(orient="records", date_format="iso"))
