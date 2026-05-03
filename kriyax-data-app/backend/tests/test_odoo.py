import importlib
import json

import duckdb


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


class FakeCommonProxy:
    def __init__(self, version=None, uid=7, auth_error=None):
        self._version = version or {"server_version": "17.0"}
        self._uid = uid
        self._auth_error = auth_error

    def version(self):
        return self._version

    def authenticate(self, db_name, username, api_key, context):
        if self._auth_error:
            raise self._auth_error
        return self._uid


class FakeObjectProxy:
    def execute_kw(self, db_name, uid, api_key, model, method, args, kwargs=None):
        kwargs = kwargs or {}
        if model == "ir.model" and method == "search_read":
            return [
                {"model": "res.partner", "name": "Contacts", "field_id": [1, 2, 3]},
                {"model": "sale.order", "name": "Sales Order", "field_id": [4, 5]},
            ]
        if model == "res.partner" and method == "fields_get":
            return {
                "name": {"string": "Name", "type": "char", "required": True, "readonly": False},
                "company_id": {
                    "string": "Company",
                    "type": "many2one",
                    "relation": "res.company",
                    "required": False,
                    "readonly": False,
                },
                "image_1920": {"string": "Image", "type": "binary", "required": False, "readonly": True},
            }
        if model == "res.partner" and method == "search_read":
            return [
                {"id": 10, "name": "Acme", "company_id": [1, "Acme Holding"]},
                {"id": 11, "name": "Bravo", "company_id": False},
            ]
        raise AssertionError(f"Unexpected Odoo call: {model}.{method} args={args} kwargs={kwargs}")


class IncrementalObjectProxy:
    def __init__(self):
        self.records = [
            {"id": 10, "name": "Acme", "write_date": "2026-05-02T00:00:00"},
            {"id": 11, "name": "Bravo", "write_date": "2026-05-02T01:00:00"},
        ]

    def execute_kw(self, db_name, uid, api_key, model, method, args, kwargs=None):
        kwargs = kwargs or {}
        if model == "res.partner" and method == "fields_get":
            return {
                "id": {"string": "ID", "type": "integer", "required": False, "readonly": True},
                "name": {"string": "Name", "type": "char", "required": False, "readonly": False},
                "write_date": {"string": "Last Updated", "type": "datetime", "required": False, "readonly": True},
            }
        if model == "res.partner" and method == "search_read":
            fields = kwargs.get("fields") or []
            domain = args[0] if args else []
            records = self.records
            for clause in domain:
                if len(clause) == 3 and clause[1] == ">":
                    records = [record for record in records if record.get(clause[0]) > clause[2]]
            return [{field: record.get(field) for field in fields} for record in records]
        raise AssertionError(f"Unexpected Odoo call: {model}.{method} args={args} kwargs={kwargs}")


def test_test_connection_normalizes_url_and_returns_success(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())

    result = odoo.test_connection(
        {
            "connectionName": "Client Odoo",
            "odooUrl": "client.odoo.com/",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": " key ",
        }
    )

    assert result["status"] == "success"
    assert result["odooUrl"] == "https://client.odoo.com"
    assert result["version"] == "17.0"
    assert result["uid"] == 7


def test_test_connection_reports_auth_failure(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy(uid=False))

    result = odoo.test_connection(
        {
            "connectionName": "Bad Odoo",
            "odooUrl": "https://bad.example.com",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": "wrong",
        }
    )

    assert result["status"] == "error"
    assert result["code"] == "auth-failed"
    assert "Authentication failed" in result["message"]


def test_save_connection_persists_masked_connection(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)

    from app.services.odoo import list_connections, save_connection

    saved = save_connection(
        {
            "connectionName": "Client Odoo",
            "odooUrl": "client.odoo.com/",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": "secret-key",
        }
    )

    assert saved["connectionName"] == "Client Odoo"
    assert saved["apiKey"] == "********"
    assert list_connections()[0]["apiKey"] == "********"

    raw = json.loads(workspace.workspace_paths()["connections"].read_text(encoding="utf-8"))
    assert raw[0]["apiKey"] == "secret-key"


def test_list_models_returns_searchable_model_metadata(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())
    monkeypatch.setattr(odoo, "_object_proxy", lambda url: FakeObjectProxy())

    models = odoo.list_models(
        {
            "connectionName": "Client Odoo",
            "odooUrl": "client.odoo.com",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": "secret-key",
        },
        search_query="sale",
    )

    assert models == [{"model": "sale.order", "name": "Sales Order", "fieldCount": 2}]


def test_get_model_fields_returns_field_details(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())
    monkeypatch.setattr(odoo, "_object_proxy", lambda url: FakeObjectProxy())

    fields = odoo.get_model_fields(
        {
            "connectionName": "Client Odoo",
            "odooUrl": "client.odoo.com",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": "secret-key",
        },
        "res.partner",
    )

    assert fields[0] == {
        "name": "company_id",
        "label": "Company",
        "type": "many2one",
        "required": False,
        "readonly": False,
        "relation": "res.company",
        "supported": True,
    }
    binary_field = next(field for field in fields if field["name"] == "image_1920")
    assert binary_field["supported"] is False
    assert binary_field["warning"] == "Binary fields excluded from import"


def test_fetch_records_creates_duckdb_table_and_catalog_entry(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)

    from app.services import odoo
    from app.services.file_import import list_catalog_tables, preview_table

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())
    monkeypatch.setattr(odoo, "_object_proxy", lambda url: FakeObjectProxy())

    result = odoo.fetch_records_to_table(
        {
            "connectionName": "Client Odoo",
            "odooUrl": "client.odoo.com",
            "dbName": "client-db",
            "username": "admin",
            "apiKey": "secret-key",
        },
        model_name="res.partner",
        fields=["id", "name", "company_id", "image_1920"],
        target_schema="raw_odoo",
        table_name="partners",
        domain_filter=[],
        record_limit=0,
    )

    assert result["qualifiedName"] == "raw_odoo.partners"
    assert result["rowCount"] == 2
    assert "Binary fields excluded from import: image_1920" in result["warnings"]
    assert "company_id_id" in [column["name"] for column in result["columns"]]
    assert "company_id_display_name" in [column["name"] for column in result["columns"]]

    catalog = list_catalog_tables()
    assert catalog[0]["source"] == {"kind": "odoo", "connectionName": "Client Odoo", "model": "res.partner"}

    preview = preview_table("raw_odoo", "partners")
    assert preview["rows"][0]["name"] == "Acme"
    assert preview["rows"][0]["company_id_display_name"] == "Acme Holding"
    assert workspace.workspace_paths()["database"].exists()


def test_incremental_sync_inserts_updates_and_reports_no_changes(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    proxy = IncrementalObjectProxy()
    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())
    monkeypatch.setattr(odoo, "_object_proxy", lambda url: proxy)
    connection = {
        "connectionName": "Client Odoo",
        "odooUrl": "client.odoo.com",
        "dbName": "client-db",
        "username": "admin",
        "apiKey": "secret-key",
    }

    initial = odoo.fetch_records_to_table(
        connection,
        model_name="res.partner",
        fields=["id", "name"],
        target_schema="raw_odoo",
        table_name="partners",
        domain_filter=[],
        record_limit=0,
        cursor_field="write_date",
    )
    assert initial["syncCursorId"]
    assert initial["lastCursorValue"] == "2026-05-02T01:00:00"

    proxy.records = [
        {"id": 10, "name": "Acme Updated", "write_date": "2026-05-02T03:00:00"},
        {"id": 11, "name": "Bravo", "write_date": "2026-05-02T01:00:00"},
        {"id": 12, "name": "Charlie", "write_date": "2026-05-02T04:00:00"},
    ]
    result = odoo.sync_cursor(initial["syncCursorId"])

    assert result == {
        "status": "success",
        "targetQualifiedName": "raw_odoo.partners",
        "inserted": 1,
        "updated": 1,
        "lastCursorValue": "2026-05-02T04:00:00",
    }
    with duckdb.connect(str(workspace.workspace_paths()["database"])) as conn:
        rows = conn.execute('select id, name from "raw_odoo"."partners" order by id').fetchall()
    assert rows == [(10, "Acme Updated"), (11, "Bravo"), (12, "Charlie")]

    no_changes = odoo.sync_cursor(initial["syncCursorId"])
    assert no_changes["status"] == "no-changes"
    assert no_changes["inserted"] == 0
    assert no_changes["updated"] == 0


def test_incremental_sync_rejects_missing_cursor_field(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import odoo

    monkeypatch.setattr(odoo, "_common_proxy", lambda url: FakeCommonProxy())
    monkeypatch.setattr(odoo, "_object_proxy", lambda url: FakeObjectProxy())

    try:
        odoo.create_sync_cursor(
            {
                "connectionName": "Client Odoo",
                "odooUrl": "client.odoo.com",
                "dbName": "client-db",
                "username": "admin",
                "apiKey": "secret-key",
            },
            model_name="res.partner",
            fields=["id", "name"],
            target_schema="raw_odoo",
            table_name="partners",
            cursor_field="write_date",
            domain_filter=[],
            record_limit=0,
        )
    except ValueError as exc:
        assert str(exc) == "Field 'write_date' not found"
    else:
        raise AssertionError("Expected missing cursor field to be rejected")
