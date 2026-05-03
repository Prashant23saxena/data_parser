from __future__ import annotations

import xmlrpc.client
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import duckdb
import pandas as pd

from kriyax_workbench.audit import finish_action, start_action
from kriyax_workbench.catalog import register_dataframe_table, safe_identifier
from kriyax_workbench.json_store import read_json, write_json
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def test_connection(payload: dict[str, str]) -> dict[str, Any]:
    normalized = _normalize_connection(payload)
    audit = start_action("odoo.connection.test", {"url": normalized["url"], "database": normalized["database"], "username": normalized["username"]})
    uid = _authenticate(normalized)
    result = {"status": "success", "uid": uid, "url": normalized["url"], "database": normalized["database"]}
    finish_action(audit, "success", result)
    return result


def save_connection(payload: dict[str, str]) -> dict[str, Any]:
    normalized = _normalize_connection(payload)
    name = normalized.get("name") or "default"
    connections = [item for item in list_connections(mask=False) if item.get("name") != name]
    record = {**normalized, "name": name, "updatedAt": _now()}
    connections.append(record)
    write_json(workspace_paths()["connections"], connections)
    return _mask(record)


def list_connections(mask: bool = True) -> list[dict[str, Any]]:
    ensure_workspace()
    connections = read_json(workspace_paths()["connections"], [])
    return [_mask(item) for item in connections] if mask else connections


def get_connection(name: str) -> dict[str, str]:
    for connection in list_connections(mask=False):
        if connection.get("name") == name:
            return connection
    raise FileNotFoundError(f"Odoo connection not found: {name}")


def list_models(connection_name: str, search: str | None = None) -> list[dict[str, Any]]:
    conn = get_connection(connection_name)
    uid = _authenticate(conn)
    domain = []
    if search:
        domain = [["model", "ilike", search]]
    records = _object(conn).execute_kw(conn["database"], uid, conn["api_key"], "ir.model", "search_read", [domain], {"fields": ["model", "name"], "limit": 200})
    return [{"model": row["model"], "name": row.get("name", row["model"])} for row in records]


def model_fields(connection_name: str, model: str) -> list[dict[str, Any]]:
    conn = get_connection(connection_name)
    uid = _authenticate(conn)
    fields = _object(conn).execute_kw(conn["database"], uid, conn["api_key"], model, "fields_get", [], {"attributes": ["string", "type", "required", "relation"]})
    return [{"name": name, "label": details.get("string", name), "type": details.get("type"), "required": bool(details.get("required")), "relation": details.get("relation")} for name, details in sorted(fields.items())]


def fetch_records(
    connection_name: str,
    model: str,
    fields: list[str],
    schema: str,
    table: str,
    domain: list[Any] | None = None,
    limit: int = 1000,
) -> dict[str, Any]:
    conn = get_connection(connection_name)
    uid = _authenticate(conn)
    safe_schema = safe_identifier(schema)
    safe_table = safe_identifier(table)
    audit = start_action("odoo.fetch", {"connection": connection_name, "model": model, "fields": fields, "targetTable": f"{safe_schema}.{safe_table}"})
    rows = _object(conn).execute_kw(conn["database"], uid, conn["api_key"], model, "search_read", [domain or []], {"fields": fields, "limit": limit})
    frame = pd.DataFrame(rows)
    _write_frame(safe_schema, safe_table, frame)
    qualified = register_dataframe_table(safe_schema, safe_table, frame, {"kind": "odoo", "connection": connection_name, "model": model, "fields": fields})
    result = {"qualifiedName": qualified, "rowCount": int(len(frame)), "columnCount": int(len(frame.columns))}
    finish_action(audit, "success", result)
    return result


def create_cursor(connection_name: str, model: str, fields: list[str], schema: str, table: str, cursor_field: str = "write_date") -> dict[str, Any]:
    cursor = {
        "id": uuid4().hex,
        "connection": connection_name,
        "model": model,
        "fields": sorted(set(fields + ["id", cursor_field])),
        "schema": safe_identifier(schema),
        "table": safe_identifier(table),
        "cursorField": cursor_field,
        "lastValue": None,
        "updatedAt": _now(),
    }
    cursors = read_json(workspace_paths()["odoo_cursors"], [])
    cursors.append(cursor)
    write_json(workspace_paths()["odoo_cursors"], cursors)
    return cursor


def sync_cursor(cursor_id: str, limit: int = 1000) -> dict[str, Any]:
    cursors = read_json(workspace_paths()["odoo_cursors"], [])
    cursor = next((item for item in cursors if item["id"] == cursor_id), None)
    if not cursor:
        raise FileNotFoundError(f"Odoo cursor not found: {cursor_id}")
    domain = []
    if cursor.get("lastValue"):
        domain = [[cursor["cursorField"], ">", cursor["lastValue"]]]
    result = fetch_records(cursor["connection"], cursor["model"], cursor["fields"], cursor["schema"], cursor["table"], domain=domain, limit=limit)
    if result["rowCount"] > 0:
        with duckdb.connect(str(workspace_paths()["database"])) as conn:
            max_value = conn.execute(f'select max("{cursor["cursorField"]}") from "{cursor["schema"]}"."{cursor["table"]}"').fetchone()[0]
        cursor["lastValue"] = str(max_value) if max_value is not None else cursor.get("lastValue")
    cursor["updatedAt"] = _now()
    write_json(workspace_paths()["odoo_cursors"], cursors)
    return {**result, "cursorId": cursor_id, "lastValue": cursor.get("lastValue")}


def _write_frame(schema: str, table: str, frame: pd.DataFrame) -> None:
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'create schema if not exists "{schema}"')
        conn.register("odoo_frame", frame)
        conn.execute(f'create or replace table "{schema}"."{table}" as select * from odoo_frame')
        conn.unregister("odoo_frame")


def _normalize_connection(payload: dict[str, str]) -> dict[str, str]:
    return {
        "name": payload.get("name", "default"),
        "url": payload["url"].rstrip("/"),
        "database": payload["database"],
        "username": payload["username"],
        "api_key": payload.get("api_key") or payload.get("password") or "",
    }


def _authenticate(conn: dict[str, str]) -> int:
    uid = _common(conn).authenticate(conn["database"], conn["username"], conn["api_key"], {})
    if not uid:
        raise RuntimeError("Odoo authentication failed.")
    return int(uid)


def _common(conn: dict[str, str]):
    return xmlrpc.client.ServerProxy(f"{conn['url']}/xmlrpc/2/common")


def _object(conn: dict[str, str]):
    return xmlrpc.client.ServerProxy(f"{conn['url']}/xmlrpc/2/object")


def _mask(conn: dict[str, Any]) -> dict[str, Any]:
    masked = dict(conn)
    if "api_key" in masked:
        masked["api_key"] = "***REDACTED***"
    return masked


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
