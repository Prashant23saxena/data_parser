import importlib

import duckdb


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_workspace_bootstrap_creates_required_paths() -> None:
    from app.services.workspace import ensure_workspace, workspace_paths

    paths = ensure_workspace()

    assert paths["root"]
    assert workspace_paths()["metadata"].exists()
    assert workspace_paths()["warehouse"].exists()


def test_table_rename_truncate_drop_and_export(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)

    from app.services import file_import

    paths = workspace.workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute('create schema raw_files')
        conn.execute('create table raw_files.orders as select 1 as id, \'A\' as name')
    file_import._upsert_catalog(
        {
            "qualifiedName": "raw_files.orders",
            "schema": "raw_files",
            "tableName": "orders",
            "rowCount": 1,
            "columnCount": 2,
            "source": {"kind": "test"},
            "createdAt": "2026-05-02T00:00:00+00:00",
            "columns": [
                {"name": "id", "sourceName": "id", "type": "integer"},
                {"name": "name", "sourceName": "name", "type": "text"},
            ],
        }
    )

    renamed = file_import.rename_table("raw_files", "orders", "orders_renamed")
    assert renamed["qualifiedName"] == "raw_files.orders_renamed"

    filename, csv_text = file_import.export_table_csv("raw_files", "orders_renamed")
    assert filename == "raw_files_orders_renamed.csv"
    assert "id,name" in csv_text
    assert "1,A" in csv_text

    truncated = file_import.truncate_table("raw_files", "orders_renamed", "raw_files.orders_renamed")
    assert truncated["rowCount"] == 0
    _, empty_csv = file_import.export_table_csv("raw_files", "orders_renamed")
    assert empty_csv.strip() == "id,name"

    dropped = file_import.drop_table("raw_files", "orders_renamed", "raw_files.orders_renamed")
    assert dropped["dropped"] is True
    assert file_import.list_catalog_tables() == []


def test_table_actions_require_confirmation_and_protect_system_tables(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import file_import

    try:
        file_import.truncate_table("raw_files", "orders", "wrong")
    except ValueError as exc:
        assert str(exc) == "Confirmation must match the qualified table name."
    else:
        raise AssertionError("Expected confirmation failure")

    try:
        file_import.drop_table("information_schema", "tables", "information_schema.tables")
    except ValueError as exc:
        assert str(exc) == "System or internal tables cannot be modified."
    else:
        raise AssertionError("Expected protected table failure")


def test_export_missing_table_reports_error(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import file_import

    try:
        file_import.export_table_csv("raw_files", "missing")
    except ValueError as exc:
        assert str(exc) == "Table not found."
    else:
        raise AssertionError("Expected missing table failure")
