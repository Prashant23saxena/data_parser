from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from kriyax_workbench.catalog import list_tables
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def connection_info() -> dict[str, Any]:
    paths = ensure_workspace()
    tables = list_tables()
    payload = {
        "viewer": "DBCode or any DuckDB-compatible database viewer",
        "driver": "DuckDB",
        "databasePath": paths["database"],
        "schemas": sorted({table.get("schema", "") for table in tables if table.get("schema")}),
        "tables": [table["qualifiedName"] for table in tables],
        "recommendedUse": "Use DBCode for visual inspection. Use workbench tools for audited imports, scripts, and writes.",
        "lockingNote": "DuckDB is file-based. If a write fails due to a lock, disconnect the DB viewer and rerun the workbench command.",
        "sampleQueries": _sample_queries(tables),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path = workspace_paths()["metadata"] / "db-viewer.json"
    metadata_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["metadataPath"] = str(metadata_path)
    return payload


def render_text(info: dict[str, Any]) -> str:
    lines = [
        "DB viewer connection",
        "--------------------",
        f"Driver: {info['driver']}",
        f"Database file: {info['databasePath']}",
        f"Metadata file: {info['metadataPath']}",
        "",
        "Schemas:",
    ]
    lines.extend(f"- {schema}" for schema in info["schemas"] or ["none yet"])
    lines.extend(["", "Tables:"])
    lines.extend(f"- {table}" for table in info["tables"] or ["none yet"])
    lines.extend(["", "Suggested SQL:"])
    lines.extend(info["sampleQueries"] or ["-- Import or save a table first."])
    lines.extend(["", f"Note: {info['lockingNote']}"])
    return "\n".join(lines) + "\n"


def _sample_queries(tables: list[dict[str, Any]]) -> list[str]:
    if not tables:
        return []
    first = tables[0]["qualifiedName"]
    queries = [f"select * from {first} limit 100;"]
    if len(tables) >= 2:
        left = tables[0]["qualifiedName"]
        right = tables[1]["qualifiedName"]
        queries.append(f"-- Example join shape; replace key columns as needed\nselect * from {left} l join {right} r on l.id = r.id limit 100;")
    return queries
