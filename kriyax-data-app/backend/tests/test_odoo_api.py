from fastapi.testclient import TestClient

from app.main import app


def test_odoo_api_tests_saves_and_lists_connection(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services import odoo

    monkeypatch.setattr(
        odoo,
        "test_connection",
        lambda payload: {
            "status": "success",
            "message": "Connected successfully to https://client.odoo.com (Odoo 17.0).",
            "odooUrl": "https://client.odoo.com",
            "version": "17.0",
            "uid": 7,
        },
    )

    client = TestClient(app)
    payload = {
        "connectionName": "Client Odoo",
        "odooUrl": "client.odoo.com/",
        "dbName": "client-db",
        "username": "admin",
        "apiKey": "secret-key",
    }

    test_response = client.post("/api/odoo/test-connection", json=payload)
    assert test_response.status_code == 200
    assert test_response.json()["status"] == "success"

    save_response = client.post("/api/odoo/connections", json=payload)
    assert save_response.status_code == 200
    assert save_response.json()["apiKey"] == "********"

    list_response = client.get("/api/odoo/connections")
    assert list_response.status_code == 200
    assert list_response.json()["connections"][0]["connectionName"] == "Client Odoo"


def test_odoo_api_browses_fields_and_fetches_records(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services import odoo

    connection = {
        "connectionName": "Client Odoo",
        "odooUrl": "client.odoo.com/",
        "dbName": "client-db",
        "username": "admin",
        "apiKey": "secret-key",
    }
    monkeypatch.setattr(
        odoo,
        "list_models",
        lambda payload, search_query=None: [{"model": "res.partner", "name": "Contacts", "fieldCount": 4}],
    )
    monkeypatch.setattr(
        odoo,
        "get_model_fields",
        lambda payload, model_name: [
            {"name": "id", "label": "ID", "type": "integer", "required": False, "readonly": True, "relation": None, "supported": True},
            {"name": "name", "label": "Name", "type": "char", "required": True, "readonly": False, "relation": None, "supported": True},
        ],
    )
    monkeypatch.setattr(
        odoo,
        "fetch_records_to_table",
        lambda payload, **kwargs: {
            "qualifiedName": "raw_odoo.partners",
            "schema": "raw_odoo",
            "tableName": "partners",
            "rowCount": 2,
            "columnCount": 2,
            "warnings": [],
        },
    )

    client = TestClient(app)

    models_response = client.post("/api/odoo/models?search=sale", json=connection)
    assert models_response.status_code == 200
    assert models_response.json()["models"][0]["model"] == "res.partner"

    fields_response = client.post("/api/odoo/models/res.partner/fields", json=connection)
    assert fields_response.status_code == 200
    assert fields_response.json()["fields"][1]["name"] == "name"

    fetch_response = client.post(
        "/api/odoo/fetch",
        json={
            "connection": connection,
            "modelName": "res.partner",
            "fields": ["id", "name"],
            "targetSchema": "raw_odoo",
            "tableName": "partners",
            "domainFilter": [],
            "recordLimit": 0,
        },
    )
    assert fetch_response.status_code == 200
    assert fetch_response.json()["qualifiedName"] == "raw_odoo.partners"


def test_odoo_api_creates_and_runs_sync_cursor(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services import odoo

    connection = {
        "connectionName": "Client Odoo",
        "odooUrl": "client.odoo.com/",
        "dbName": "client-db",
        "username": "admin",
        "apiKey": "secret-key",
    }
    monkeypatch.setattr(
        odoo,
        "create_sync_cursor",
        lambda payload, **kwargs: {
            "id": "cursor-1",
            "modelName": "res.partner",
            "targetSchema": "raw_odoo",
            "tableName": "partners",
            "cursorField": "write_date",
            "lastCursorValue": "2026-05-02T00:00:00",
        },
    )
    monkeypatch.setattr(
        odoo,
        "sync_cursor",
        lambda sync_cursor_id: {
            "status": "success",
            "targetQualifiedName": "raw_odoo.partners",
            "inserted": 1,
            "updated": 1,
            "lastCursorValue": "2026-05-02T01:00:00",
        },
    )

    client = TestClient(app)
    create_response = client.post(
        "/api/odoo/sync-cursors",
        json={
            "connection": connection,
            "modelName": "res.partner",
            "fields": ["id", "name", "write_date"],
            "targetSchema": "raw_odoo",
            "tableName": "partners",
            "cursorField": "write_date",
            "domainFilter": [],
            "recordLimit": 0,
        },
    )
    assert create_response.status_code == 200
    assert create_response.json()["id"] == "cursor-1"

    sync_response = client.post("/api/odoo/sync/cursor-1")
    assert sync_response.status_code == 200
    assert sync_response.json()["inserted"] == 1
    assert sync_response.json()["updated"] == 1
