import json
import socket
import xmlrpc.client
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import duckdb
import pandas as pd

from app.services.file_import import _safe_identifier, _upsert_catalog
from app.services.workspace import ensure_workspace, workspace_paths

BATCH_SIZE = 500
UNSUPPORTED_FIELD_TYPES = {"binary", "one2many", "many2many"}


def test_connection(payload: dict[str, str]) -> dict[str, Any]:
    normalized = _normalized_connection(payload)
    try:
        common = _common_proxy(normalized["odooUrl"])
        version_info = common.version()
        uid = common.authenticate(
            normalized["dbName"],
            normalized["username"],
            normalized["apiKey"],
            {},
        )
    except socket.gaierror:
        return _error("unreachable", f"Cannot reach {normalized['odooUrl']}. Check the URL and your network connection.")
    except TimeoutError:
        return _error("unreachable", f"Cannot reach {normalized['odooUrl']}. Check the URL and your network connection.")
    except xmlrpc.client.Fault as exc:
        message = str(exc)
        if "database" in message.lower() or "db" in message.lower():
            return _error("invalid-db", f"Database '{normalized['dbName']}' not found on this Odoo instance.")
        return _error("auth-failed", "Authentication failed. Check your username and API key.")
    except OSError:
        return _error("unreachable", f"Cannot reach {normalized['odooUrl']}. Check the URL and your network connection.")

    if not uid:
        return _error("auth-failed", "Authentication failed. Check your username and API key.")

    return {
        "status": "success",
        "message": f"Connected successfully to {normalized['odooUrl']} (Odoo {version_info.get('server_version', 'unknown')}).",
        "odooUrl": normalized["odooUrl"],
        "version": version_info.get("server_version", "unknown"),
        "serverInfo": version_info,
        "uid": uid,
    }


def save_connection(payload: dict[str, str]) -> dict[str, Any]:
    ensure_workspace()
    normalized = _normalized_connection(payload)
    connections = _read_connections()
    if any(item["connectionName"] == normalized["connectionName"] for item in connections):
        raise ValueError("A connection with this name already exists")

    record = {
        **normalized,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    connections.append(record)
    workspace_paths()["connections"].write_text(json.dumps(connections, indent=2) + "\n", encoding="utf-8")
    return _masked_connection(record)


def list_connections() -> list[dict[str, Any]]:
    ensure_workspace()
    return [_masked_connection(record) for record in _read_connections()]


def list_models(payload: dict[str, str], search_query: str | None = None) -> list[dict[str, Any]]:
    normalized = _normalized_connection(payload)
    uid = _authenticate(normalized)
    records = _execute_object_kw(
        normalized,
        uid,
        "ir.model",
        "search_read",
        [[]],
        {"fields": ["model", "name", "field_id"], "order": "model asc"},
    )
    query = (search_query or "").strip().lower()
    models = []
    for record in records:
        technical_name = str(record.get("model") or "")
        display_name = str(record.get("name") or technical_name)
        if query and query not in technical_name.lower() and query not in display_name.lower():
            continue
        field_ids = record.get("field_id") or []
        models.append(
            {
                "model": technical_name,
                "name": display_name,
                "fieldCount": len(field_ids) if isinstance(field_ids, list) else 0,
            }
        )
    return models


def get_model_fields(payload: dict[str, str], model_name: str) -> list[dict[str, Any]]:
    normalized = _normalized_connection(payload)
    uid = _authenticate(normalized)
    metadata = _execute_object_kw(
        normalized,
        uid,
        model_name,
        "fields_get",
        [],
        {
            "attributes": [
                "string",
                "type",
                "required",
                "readonly",
                "relation",
                "compute",
            ]
        },
    )
    return [_field_detail(name, detail) for name, detail in sorted(metadata.items())]


def fetch_records_to_table(
    payload: dict[str, str],
    *,
    model_name: str,
    fields: list[str],
    target_schema: str,
    table_name: str,
    domain_filter: list[Any] | None = None,
    record_limit: int = 0,
    cursor_field: str | None = None,
) -> dict[str, Any]:
    ensure_workspace()
    normalized = _normalized_connection(payload)
    schema = _safe_identifier(target_schema)
    table = _safe_identifier(table_name)
    if not schema or not table:
        raise ValueError("Target schema and table name are required.")

    selected_fields = [field.strip() for field in fields if field.strip()]
    if not selected_fields:
        raise ValueError("Select at least one Odoo field to fetch.")

    field_details = {field["name"]: field for field in get_model_fields(normalized, model_name)}
    cursor_name = cursor_field.strip() if cursor_field else None
    if cursor_name:
        _validate_cursor_field(field_details, cursor_name)
        selected_fields = _ensure_required_sync_fields(selected_fields, cursor_name)

    supported_fields = []
    warnings = []
    for field in selected_fields:
        detail = field_details.get(field)
        if detail and not detail["supported"]:
            warnings.append(f"{detail['warning']}: {field}")
            continue
        supported_fields.append(field)

    if not supported_fields:
        raise ValueError("No supported Odoo fields selected for import.")

    _raise_if_table_exists(schema, table)

    uid = _authenticate(normalized)
    records = _fetch_records(
        normalized,
        uid=uid,
        model_name=model_name,
        fields=supported_fields,
        domain_filter=domain_filter or [],
        record_limit=record_limit,
    )
    frame, columns = _records_to_frame(records, supported_fields, field_details)

    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute(f'create schema if not exists "{schema}"')
        conn.register("odoo_frame", frame)
        conn.execute(f'create table "{schema}"."{table}" as select * from odoo_frame')
        conn.unregister("odoo_frame")

    if not records:
        warnings.append("0 records found matching your filter")

    entry = {
        "qualifiedName": f"{schema}.{table}",
        "schema": schema,
        "tableName": table,
        "source": {
            "kind": "odoo",
            "connectionName": normalized["connectionName"],
            "model": model_name,
        },
        "rowCount": int(len(frame.index)),
        "columnCount": len(columns),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
        "warnings": warnings,
    }
    if cursor_name:
        cursor = _save_sync_cursor(
            {
                "id": uuid4().hex,
                "connection": normalized,
                "modelName": model_name,
                "targetSchema": schema,
                "tableName": table,
                "fields": supported_fields,
                "domainFilter": domain_filter or [],
                "recordLimit": record_limit,
                "cursorField": cursor_name,
                "lastCursorValue": _max_cursor_value(records, cursor_name),
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            }
        )
        entry["syncCursorId"] = cursor["id"]
        entry["lastCursorValue"] = cursor["lastCursorValue"]
    _upsert_catalog(entry)
    return entry


def create_sync_cursor(
    payload: dict[str, str],
    *,
    model_name: str,
    fields: list[str],
    target_schema: str,
    table_name: str,
    cursor_field: str = "write_date",
    domain_filter: list[Any] | None = None,
    record_limit: int = 0,
) -> dict[str, Any]:
    ensure_workspace()
    normalized = _normalized_connection(payload)
    schema = _safe_identifier(target_schema)
    table = _safe_identifier(table_name)
    if not schema or not table:
        raise ValueError("Target schema and table name are required.")

    field_details = {field["name"]: field for field in get_model_fields(normalized, model_name)}
    _validate_cursor_field(field_details, cursor_field)
    selected_fields = _ensure_required_sync_fields([field.strip() for field in fields if field.strip()], cursor_field)
    _validate_existing_table_for_sync(schema, table, cursor_field)

    last_cursor_value = _current_table_cursor(schema, table, cursor_field)
    cursor = {
        "id": uuid4().hex,
        "connection": normalized,
        "modelName": model_name,
        "targetSchema": schema,
        "tableName": table,
        "fields": selected_fields,
        "domainFilter": domain_filter or [],
        "recordLimit": record_limit,
        "cursorField": cursor_field,
        "lastCursorValue": last_cursor_value,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    return _save_sync_cursor(cursor)


def sync_cursor(sync_cursor_id: str) -> dict[str, Any]:
    ensure_workspace()
    cursor = _sync_cursor_by_id(sync_cursor_id)
    normalized = _normalized_connection(cursor["connection"])
    field_details = {field["name"]: field for field in get_model_fields(normalized, cursor["modelName"])}
    cursor_field = cursor["cursorField"]
    _validate_cursor_field(field_details, cursor_field)

    uid = _authenticate(normalized)
    domain_filter = list(cursor.get("domainFilter") or [])
    if cursor.get("lastCursorValue") is not None:
        domain_filter.append([cursor_field, ">", cursor["lastCursorValue"]])

    records = _fetch_records(
        normalized,
        uid=uid,
        model_name=cursor["modelName"],
        fields=_ensure_required_sync_fields(cursor["fields"], cursor_field),
        domain_filter=domain_filter,
        record_limit=int(cursor.get("recordLimit") or 0),
    )
    if not records:
        return {
            "status": "no-changes",
            "targetQualifiedName": f"{cursor['targetSchema']}.{cursor['tableName']}",
            "inserted": 0,
            "updated": 0,
            "lastCursorValue": cursor.get("lastCursorValue"),
        }

    frame, _ = _records_to_frame(records, _ensure_required_sync_fields(cursor["fields"], cursor_field), field_details)
    inserted, updated = _upsert_frame(cursor["targetSchema"], cursor["tableName"], frame)
    last_cursor_value = _max_cursor_value(records, cursor_field)
    cursor["lastCursorValue"] = last_cursor_value
    cursor["updatedAt"] = datetime.now(timezone.utc).isoformat()
    _save_sync_cursor(cursor)
    _refresh_catalog_count(cursor["targetSchema"], cursor["tableName"])

    return {
        "status": "success",
        "targetQualifiedName": f"{cursor['targetSchema']}.{cursor['tableName']}",
        "inserted": inserted,
        "updated": updated,
        "lastCursorValue": last_cursor_value,
    }


def _validate_cursor_field(field_details: dict[str, dict[str, Any]], cursor_field: str) -> None:
    detail = field_details.get(cursor_field)
    if not detail:
        raise ValueError(f"Field '{cursor_field}' not found")
    if detail.get("type") not in {"date", "datetime"}:
        raise ValueError("Cursor field must be a date or datetime field.")


def _ensure_required_sync_fields(fields: list[str], cursor_field: str) -> list[str]:
    result = list(dict.fromkeys([field for field in fields if field]))
    if "id" not in result:
        result.insert(0, "id")
    if cursor_field not in result:
        result.append(cursor_field)
    return result


def _max_cursor_value(records: list[dict[str, Any]], cursor_field: str) -> Any:
    values = [record.get(cursor_field) for record in records if record.get(cursor_field) not in {None, False}]
    return max(values) if values else None


def _validate_existing_table_for_sync(schema: str, table: str, cursor_field: str) -> None:
    paths = workspace_paths()
    try:
        with duckdb.connect(str(paths["database"])) as conn:
            frame = conn.execute(f'select * from "{schema}"."{table}" limit 0').fetchdf()
    except duckdb.CatalogException as exc:
        raise ValueError(f"Target table does not exist: {schema}.{table}") from exc
    columns = set(frame.columns)
    if "id" not in columns:
        raise ValueError("Target table must include Odoo id for incremental sync.")
    if _safe_identifier(cursor_field) not in columns:
        raise ValueError(f"Target table must include cursor field '{cursor_field}'.")


def _current_table_cursor(schema: str, table: str, cursor_field: str) -> Any:
    paths = workspace_paths()
    cursor_column = _safe_identifier(cursor_field)
    with duckdb.connect(str(paths["database"])) as conn:
        return conn.execute(f'select max("{cursor_column}") from "{schema}"."{table}"').fetchone()[0]


def _upsert_frame(schema: str, table: str, frame: pd.DataFrame) -> tuple[int, int]:
    if "id" not in frame.columns:
        raise ValueError("Odoo sync records must include id.")
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.register("odoo_sync_frame", frame)
        updated = conn.execute(
            f'select count(*) from "{schema}"."{table}" target join odoo_sync_frame source on target.id = source.id'
        ).fetchone()[0]
        conn.execute(f'delete from "{schema}"."{table}" where id in (select id from odoo_sync_frame)')
        conn.execute(f'insert into "{schema}"."{table}" select * from odoo_sync_frame')
        conn.unregister("odoo_sync_frame")
    inserted = int(len(frame.index) - updated)
    return inserted, int(updated)


def _read_sync_cursors() -> list[dict[str, Any]]:
    ensure_workspace()
    return json.loads(workspace_paths()["odoo_sync_cursors"].read_text(encoding="utf-8"))


def _save_sync_cursor(cursor: dict[str, Any]) -> dict[str, Any]:
    cursors = _read_sync_cursors()
    remaining = [item for item in cursors if item["id"] != cursor["id"]]
    remaining.append(cursor)
    workspace_paths()["odoo_sync_cursors"].write_text(json.dumps(remaining, indent=2) + "\n", encoding="utf-8")
    return cursor


def _sync_cursor_by_id(sync_cursor_id: str) -> dict[str, Any]:
    for cursor in _read_sync_cursors():
        if cursor["id"] == sync_cursor_id:
            return cursor
    raise ValueError("Sync cursor not found.")


def _refresh_catalog_count(schema: str, table: str) -> None:
    paths = workspace_paths()
    qualified_name = f"{schema}.{table}"
    with duckdb.connect(str(paths["database"])) as conn:
        row_count = conn.execute(f'select count(*) from "{schema}"."{table}"').fetchone()[0]
    catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
    for entry in catalog:
        if entry.get("qualifiedName") == qualified_name:
            entry["rowCount"] = int(row_count)
            break
    paths["catalog"].write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


def _normalized_connection(payload: dict[str, str]) -> dict[str, str]:
    name = (payload.get("connectionName") or "").strip()
    url = (payload.get("odooUrl") or "").strip().rstrip("/")
    db_name = (payload.get("dbName") or "").strip()
    username = (payload.get("username") or "").strip()
    api_key = (payload.get("apiKey") or "").strip()

    if url and not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    if not all([name, url, db_name, username, api_key]):
        raise ValueError("Connection name, URL, database, username, and API key are required.")
    if len(name) > 64:
        raise ValueError("Connection name must be 64 characters or fewer.")

    return {
        "connectionName": name,
        "odooUrl": url,
        "dbName": db_name,
        "username": username,
        "apiKey": api_key,
    }


def _authenticate(normalized: dict[str, str]) -> int:
    common = _common_proxy(normalized["odooUrl"])
    uid = common.authenticate(
        normalized["dbName"],
        normalized["username"],
        normalized["apiKey"],
        {},
    )
    if not uid:
        raise ValueError("Authentication failed. Check your username and API key.")
    return int(uid)


def _fetch_records(
    normalized: dict[str, str],
    *,
    uid: int,
    model_name: str,
    fields: list[str],
    domain_filter: list[Any],
    record_limit: int,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    offset = 0
    while True:
        remaining = record_limit - len(records) if record_limit else BATCH_SIZE
        if record_limit and remaining <= 0:
            break
        batch_limit = min(BATCH_SIZE, remaining) if record_limit else BATCH_SIZE
        batch = _execute_object_kw(
            normalized,
            uid,
            model_name,
            "search_read",
            [domain_filter],
            {"fields": fields, "limit": batch_limit, "offset": offset},
        )
        records.extend(batch)
        if len(batch) < batch_limit:
            break
        offset += batch_limit
    return records


def _records_to_frame(
    records: list[dict[str, Any]],
    selected_fields: list[str],
    field_details: dict[str, dict[str, Any]],
) -> tuple[pd.DataFrame, list[dict[str, str]]]:
    normalized_rows = []
    column_specs = _column_specs(selected_fields, field_details)
    for record in records:
        row: dict[str, Any] = {}
        for field in selected_fields:
            detail = field_details.get(field, {"type": "text"})
            value = record.get(field)
            if detail.get("type") == "many2one":
                safe = _safe_identifier(field)
                if isinstance(value, list) and len(value) >= 2:
                    row[f"{safe}_id"] = value[0]
                    row[f"{safe}_display_name"] = value[1]
                else:
                    row[f"{safe}_id"] = None
                    row[f"{safe}_display_name"] = None
            else:
                row[_safe_identifier(field)] = value if value is not False else None
        normalized_rows.append(row)
    frame = pd.DataFrame(normalized_rows, columns=[column["name"] for column in column_specs])
    return frame, column_specs


def _column_specs(selected_fields: list[str], field_details: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    columns = []
    for field in selected_fields:
        detail = field_details.get(field, {"type": "text"})
        safe = _safe_identifier(field)
        if detail.get("type") == "many2one":
            columns.append({"name": f"{safe}_id", "sourceName": field, "type": "integer"})
            columns.append({"name": f"{safe}_display_name", "sourceName": field, "type": "text"})
        else:
            columns.append({"name": safe, "sourceName": field, "type": _odoo_type_to_catalog_type(str(detail.get("type", "text")))})
    return columns


def _field_detail(name: str, detail: dict[str, Any]) -> dict[str, Any]:
    field_type = str(detail.get("type") or "unknown")
    supported = field_type not in UNSUPPORTED_FIELD_TYPES
    result = {
        "name": name,
        "label": str(detail.get("string") or name),
        "type": field_type,
        "required": bool(detail.get("required", False)),
        "readonly": bool(detail.get("readonly", False)),
        "relation": detail.get("relation"),
        "supported": supported,
    }
    if not supported:
        if field_type == "binary":
            result["warning"] = "Binary fields excluded from import"
        else:
            result["warning"] = f"{field_type} fields are not flattened in v1"
    if detail.get("compute"):
        result["computed"] = True
    return result


def _odoo_type_to_catalog_type(field_type: str) -> str:
    if field_type in {"integer", "many2one"}:
        return "integer"
    if field_type in {"float", "monetary"}:
        return "decimal"
    if field_type == "boolean":
        return "boolean"
    if field_type in {"date", "datetime"}:
        return field_type
    return "text"


def _raise_if_table_exists(schema: str, table: str) -> None:
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        exists = conn.execute(
            """
            select count(*)
            from information_schema.tables
            where table_schema = ? and table_name = ?
            """,
            [schema, table],
        ).fetchone()[0]
    if exists:
        raise ValueError(f"Table '{schema}.{table}' already exists. Choose a new table name.")


def _execute_object_kw(
    normalized: dict[str, str],
    uid: int,
    model_name: str,
    method: str,
    args: list[Any],
    kwargs: dict[str, Any] | None = None,
) -> Any:
    try:
        return _object_proxy(normalized["odooUrl"]).execute_kw(
            normalized["dbName"],
            uid,
            normalized["apiKey"],
            model_name,
            method,
            args,
            kwargs or {},
        )
    except (socket.gaierror, TimeoutError, OSError) as exc:
        raise ValueError("Lost connection to Odoo. Reconnect and try again.") from exc
    except xmlrpc.client.Fault as exc:
        raise ValueError(f"Odoo API error: {exc.faultString}") from exc


def _read_connections() -> list[dict[str, Any]]:
    path = workspace_paths()["connections"]
    return json.loads(path.read_text(encoding="utf-8"))


def _masked_connection(record: dict[str, Any]) -> dict[str, Any]:
    return {**record, "apiKey": "********"}


def _common_proxy(odoo_url: str):
    return xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common", allow_none=True)


def _object_proxy(odoo_url: str):
    return xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object", allow_none=True)


def _error(code: str, message: str) -> dict[str, str]:
    return {"status": "error", "code": code, "message": message}
