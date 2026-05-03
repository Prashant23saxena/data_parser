import importlib
import json

import duckdb


def _reload_workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_csv_inspection_returns_mapping_preview_and_requires_duplicate_renames(monkeypatch, tmp_path):
    workspace = _reload_workspace(monkeypatch, tmp_path)
    csv_path = workspace.workspace_paths()["uploads"] / "orders.csv"
    csv_path.write_text(
        "Customer,Customer,Order Date,Amount\n"
        "Acme,A-001,2026-05-01,12.50\n"
        "Bravo,B-002,2026-05-02,20.00\n",
        encoding="utf-8",
    )

    from app.services.file_import import inspect_file

    inspection = inspect_file(csv_path)

    assert inspection["fileName"] == "orders.csv"
    assert inspection["requiresRename"] is True
    assert [column["sourceName"] for column in inspection["columns"]] == [
        "Customer",
        "Customer",
        "Order Date",
        "Amount",
    ]
    assert inspection["columns"][0]["targetName"] == "customer"
    assert inspection["columns"][1]["status"] == "needs_rename"
    assert inspection["columns"][2]["inferredType"] == "date"
    assert inspection["columns"][3]["inferredType"] == "decimal"
    assert inspection["previewRows"][0]["Customer"] == "Acme"


def test_commit_import_creates_duckdb_table_and_catalog_entry(monkeypatch, tmp_path):
    workspace = _reload_workspace(monkeypatch, tmp_path)
    csv_path = workspace.workspace_paths()["uploads"] / "orders.csv"
    csv_path.write_text(
        "Customer,Order Date,Amount\n"
        "Acme,2026-05-01,12.50\n"
        "Bravo,2026-05-02,20.00\n",
        encoding="utf-8",
    )

    from app.services.file_import import commit_import, inspect_file

    inspection = inspect_file(csv_path)
    result = commit_import(
        file_path=csv_path,
        target_schema="raw_files",
        table_name="sales_orders_raw",
        columns=[
            {**column, "selectedType": column["inferredType"]}
            for column in inspection["columns"]
        ],
    )

    assert result["qualifiedName"] == "raw_files.sales_orders_raw"
    assert result["rowCount"] == 2
    assert result["columnCount"] == 3

    with duckdb.connect(str(workspace.workspace_paths()["database"])) as conn:
        rows = conn.execute(
            'select customer, amount from raw_files.sales_orders_raw order by customer'
        ).fetchall()

    assert rows == [("Acme", 12.5), ("Bravo", 20.0)]

    catalog = json.loads(workspace.workspace_paths()["catalog"].read_text(encoding="utf-8"))
    assert catalog[0]["qualifiedName"] == "raw_files.sales_orders_raw"
    assert catalog[0]["source"]["kind"] == "file"
    assert [column["name"] for column in catalog[0]["columns"]] == [
        "customer",
        "order_date",
        "amount",
    ]
