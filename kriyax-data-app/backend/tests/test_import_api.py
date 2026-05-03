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
    assert inspection["draftId"]
    assert inspection["columns"][0]["targetName"] == "customer"

    drafts_response = client.get("/api/imports/drafts")
    assert drafts_response.status_code == 200
    assert drafts_response.json()["drafts"][0]["id"] == inspection["draftId"]

    resume_response = client.get(f"/api/imports/drafts/{inspection['draftId']}")
    assert resume_response.status_code == 200
    assert resume_response.json()["filePath"] == inspection["filePath"]

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

    assert client.get("/api/imports/drafts").json()["drafts"] == []


def test_schema_api_create_and_list(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    create_response = client.post("/api/catalog/schemas", json={"schemaName": "Sandbox Tests"})

    assert create_response.status_code == 200
    assert create_response.json()["schema"] == "sandbox_tests"

    list_response = client.get("/api/catalog/schemas")
    assert list_response.status_code == 200
    assert "sandbox_tests" in list_response.json()["schemas"]
