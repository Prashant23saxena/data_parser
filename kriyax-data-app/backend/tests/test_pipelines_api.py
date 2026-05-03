from fastapi.testclient import TestClient

from app.main import app


def test_pipeline_api_create_run_history_and_toggle(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    client.post(
        "/api/execution/scripts",
        json={"scriptName": "hello_pipeline.py", "code": 'print("pipeline hello")\n'},
    )

    create_response = client.post(
        "/api/pipelines",
        json={"pipelineName": "Daily refresh", "scriptId": "hello_pipeline.py"},
    )
    assert create_response.status_code == 200
    pipeline = create_response.json()
    assert pipeline["name"] == "Daily refresh"
    assert pipeline["enabled"] is True

    list_response = client.get("/api/pipelines")
    assert list_response.status_code == 200
    assert list_response.json()["pipelines"][0]["id"] == pipeline["id"]

    toggle_response = client.patch(f"/api/pipelines/{pipeline['id']}/enabled", json={"enabled": False})
    assert toggle_response.status_code == 200
    assert toggle_response.json()["enabled"] is False

    schedule_response = client.patch(
        f"/api/pipelines/{pipeline['id']}/schedule",
        json={"type": "daily", "timeOfDay": "06:00", "timezone": "Asia/Kolkata"},
    )
    assert schedule_response.status_code == 200
    schedule = schedule_response.json()["schedule"]
    assert schedule["type"] == "daily"
    assert schedule["timeOfDay"] == "06:00"
    assert schedule["timezone"] == "Asia/Kolkata"
    assert schedule["nextRunAt"]

    run_response = client.post(f"/api/pipelines/{pipeline['id']}/run")
    assert run_response.status_code == 200
    run = run_response.json()
    assert run["status"] == "success"
    assert run["trigger"] == "manual"
    assert "pipeline hello" in run["stdout"]

    history_response = client.get(f"/api/pipelines/{pipeline['id']}/runs")
    assert history_response.status_code == 200
    assert history_response.json()["runs"][0]["id"] == run["id"]

    detail_response = client.get(f"/api/pipelines/runs/{run['id']}")
    assert detail_response.status_code == 200
    assert detail_response.json()["pipelineName"] == "Daily refresh"


def test_pipeline_api_rejects_invalid_cron(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    client.post(
        "/api/execution/scripts",
        json={"scriptName": "cron_pipeline.py", "code": 'print("cron")\n'},
    )
    create_response = client.post(
        "/api/pipelines",
        json={"pipelineName": "Cron refresh", "scriptId": "cron_pipeline.py"},
    )
    pipeline = create_response.json()

    schedule_response = client.patch(
        f"/api/pipelines/{pipeline['id']}/schedule",
        json={"type": "cron", "cronExpression": "0 6 *"},
    )

    assert schedule_response.status_code == 400
    assert schedule_response.json()["detail"] == "Cron expression must have five fields."


def test_pipeline_api_lists_and_acknowledges_failures(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    client.post(
        "/api/execution/scripts",
        json={"scriptName": "failing_pipeline.py", "code": 'raise RuntimeError("api boom")\n'},
    )
    create_response = client.post(
        "/api/pipelines",
        json={"pipelineName": "Failing refresh", "scriptId": "failing_pipeline.py"},
    )
    pipeline = create_response.json()
    run_response = client.post(f"/api/pipelines/{pipeline['id']}/run")
    run = run_response.json()
    assert run["status"] == "error"

    error_runs_response = client.get("/api/pipelines/runs?status=error")
    assert error_runs_response.status_code == 200
    assert error_runs_response.json()["runs"][0]["id"] == run["id"]

    failures_response = client.get("/api/pipelines/failures")
    assert failures_response.status_code == 200
    assert failures_response.json()["failures"][0]["runId"] == run["id"]

    ack_response = client.post(f"/api/pipelines/failures/{run['id']}/ack")
    assert ack_response.status_code == 200
    assert ack_response.json() == {"acknowledged": True, "runId": run["id"]}
    assert client.get("/api/pipelines/failures").json()["failures"] == []


def test_pipeline_api_run_includes_odoo_pre_step(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services import pipelines

    monkeypatch.setattr(
        pipelines.odoo,
        "sync_cursor",
        lambda sync_cursor_id: {
            "status": "success",
            "targetQualifiedName": "raw_odoo.partners",
            "inserted": 1,
            "updated": 0,
            "lastCursorValue": "2026-05-02T04:00:00",
        },
    )
    client = TestClient(app)

    client.post(
        "/api/execution/scripts",
        json={"scriptName": "sync_pipeline.py", "code": 'print("after sync")\n'},
    )
    create_response = client.post(
        "/api/pipelines",
        json={"pipelineName": "Sync pipeline", "scriptId": "sync_pipeline.py", "connectorSyncId": "cursor-1"},
    )
    pipeline = create_response.json()
    run_response = client.post(f"/api/pipelines/{pipeline['id']}/run")

    assert run_response.status_code == 200
    run = run_response.json()
    assert run["status"] == "success"
    assert run["preStep"]["syncCursorId"] == "cursor-1"
    assert run["preStep"]["inserted"] == 1
    assert "after sync" in run["stdout"]
