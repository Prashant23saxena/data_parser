from fastapi.testclient import TestClient

from app.main import app


def test_run_script_api_returns_output_and_saved_table(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    upload = client.post(
        "/api/imports/upload",
        files={"file": ("orders.csv", b"Customer,Amount\nAcme,12.50\nBravo,20.00\n", "text/csv")},
    ).json()
    client.post(
        "/api/imports/commit",
        json={
            "filePath": upload["filePath"],
            "targetSchema": "raw_files",
            "tableName": "orders",
            "columns": upload["columns"],
        },
    )

    response = client.post(
        "/api/execution/run",
        json={
            "scriptName": "make_big_orders.py",
            "code": (
                'df = load_table("raw_files.orders")\n'
                'print(f"rows={len(df)}")\n'
                'save_table(df[df["amount"] > 15], "big_orders", schema="curated")\n'
            ),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["persistedScript"] is False
    assert payload["scriptPath"] is None
    assert "rows=2" in payload["stdout"]
    assert payload["savedTables"] == ["curated.big_orders"]
    assert payload["preview"]["rows"] == [{"customer": "Bravo", "amount": 20.0}]
    assert payload["resultTables"][0]["qualifiedName"] == "curated.big_orders"


def test_run_script_api_returns_show_preview(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    upload = client.post(
        "/api/imports/upload",
        files={"file": ("orders.csv", b"Customer,Amount\nAcme,12.50\nBravo,20.00\n", "text/csv")},
    ).json()
    client.post(
        "/api/imports/commit",
        json={
            "filePath": upload["filePath"],
            "targetSchema": "raw_files",
            "tableName": "orders",
            "columns": upload["columns"],
        },
    )

    response = client.post(
        "/api/execution/run",
        json={
            "scriptName": "show_orders.py",
            "code": 'df = load_table("raw_files.orders")\nshow(df[df["amount"] > 15], name="large_orders")\n',
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["displayFrames"][0]["name"] == "large_orders"
    assert payload["preview"]["rows"] == [{"customer": "Bravo", "amount": 20.0}]


def test_run_does_not_save_and_saved_script_api_lists_and_loads_explicit_saves(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    client.post(
        "/api/execution/run",
        json={
            "scriptName": "hello_script.py",
            "code": 'print("hello saved script")\n',
        },
    )

    assert client.get("/api/execution/scripts").json()["scripts"] == []

    save_response = client.post(
        "/api/execution/scripts",
        json={
            "scriptName": "hello_script.py",
            "code": 'print("hello saved script")\n',
        },
    )
    assert save_response.status_code == 200
    assert save_response.json()["name"] == "hello_script.py"

    list_response = client.get("/api/execution/scripts")
    assert list_response.status_code == 200
    assert list_response.json()["scripts"][0]["name"] == "hello_script.py"

    get_response = client.get("/api/execution/scripts/hello_script.py")
    assert get_response.status_code == 200
    assert get_response.json()["code"] == 'print("hello saved script")\n'
