from fastapi.testclient import TestClient

from app.main import app


def test_file_import_api_upload_commit_catalog_and_preview(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    upload_response = client.post(
        "/api/imports/upload",
        files={"file": ("orders.csv", b"Customer,Amount\nAcme,12.50\nBravo,20.00\n", "text/csv")},
    )

    assert upload_response.status_code == 200
    inspection = upload_response.json()
    assert inspection["fileName"] == "orders.csv"
    assert inspection["columns"][0]["targetName"] == "customer"

    commit_response = client.post(
        "/api/imports/commit",
        json={
            "filePath": inspection["filePath"],
            "targetSchema": "raw_files",
            "tableName": "sales_orders_raw",
            "columns": inspection["columns"],
        },
    )

    assert commit_response.status_code == 200
    assert commit_response.json()["qualifiedName"] == "raw_files.sales_orders_raw"
    assert commit_response.json()["source"]["fileName"] == "orders.csv"

    catalog_response = client.get("/api/catalog/tables")
    assert catalog_response.status_code == 200
    assert catalog_response.json()["tables"][0]["qualifiedName"] == "raw_files.sales_orders_raw"

    preview_response = client.get("/api/catalog/tables/raw_files/sales_orders_raw/preview")
    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["columns"] == ["customer", "amount"]
    assert preview["rows"][0]["customer"] == "Acme"
