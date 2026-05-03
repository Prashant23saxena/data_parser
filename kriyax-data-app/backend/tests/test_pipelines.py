import importlib
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_pipeline_create_manual_run_history_and_disable(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "hello_pipeline.py"
    script_path.write_text('print("pipeline hello")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Daily refresh",
        script_id="hello_pipeline.py",
        connector_sync_id=None,
    )

    assert pipeline["name"] == "Daily refresh"
    assert pipeline["scriptId"] == "hello_pipeline.py"
    assert pipeline["enabled"] is True
    assert pipeline["schedule"] is None

    duplicate = None
    try:
        pipelines.create_pipeline(
            pipeline_name="Daily refresh",
            script_id="hello_pipeline.py",
            connector_sync_id=None,
        )
    except ValueError as exc:
        duplicate = str(exc)
    assert duplicate == "A pipeline with this name already exists."

    disabled = pipelines.set_pipeline_enabled(pipeline["id"], False)
    assert disabled["enabled"] is False

    run = pipelines.run_pipeline_now(pipeline["id"])
    assert run["pipelineId"] == pipeline["id"]
    assert run["trigger"] == "manual"
    assert run["status"] == "success"
    assert "pipeline hello" in run["stdout"]
    assert run["durationMs"] >= 0

    history = pipelines.list_runs(pipeline["id"])
    assert history[0]["id"] == run["id"]
    assert history[0]["status"] == "success"

    listed = pipelines.list_pipelines()
    assert listed[0]["lastRun"]["id"] == run["id"]
    assert listed[0]["enabled"] is False


def test_pipeline_daily_schedule_saves_next_run(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "scheduled.py"
    script_path.write_text('print("scheduled")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Daily scheduled refresh",
        script_id="scheduled.py",
        connector_sync_id=None,
    )
    updated = pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "daily", "timeOfDay": "06:00", "timezone": "Asia/Kolkata"},
    )

    schedule = updated["schedule"]
    next_run_at = datetime.fromisoformat(schedule["nextRunAt"]).astimezone(ZoneInfo("Asia/Kolkata"))
    assert schedule["type"] == "daily"
    assert schedule["timeOfDay"] == "06:00"
    assert schedule["timezone"] == "Asia/Kolkata"
    assert next_run_at.hour == 6
    assert next_run_at.minute == 0


def test_pipeline_cron_schedule_validates(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "cron.py"
    script_path.write_text('print("cron")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Cron refresh",
        script_id="cron.py",
        connector_sync_id=None,
    )
    updated = pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "cron", "cronExpression": "0 6 * * *", "timezone": "Asia/Kolkata"},
    )

    assert updated["schedule"]["type"] == "cron"
    assert updated["schedule"]["cronExpression"] == "0 6 * * *"
    assert datetime.fromisoformat(updated["schedule"]["nextRunAt"])


def test_pipeline_rejects_invalid_cron(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "bad_cron.py"
    script_path.write_text('print("bad")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Bad cron refresh",
        script_id="bad_cron.py",
        connector_sync_id=None,
    )

    try:
        pipelines.set_pipeline_schedule(
            pipeline["id"],
            {"type": "cron", "cronExpression": "0 6 *", "timezone": "Asia/Kolkata"},
        )
    except ValueError as exc:
        assert str(exc) == "Cron expression must have five fields."
    else:
        raise AssertionError("Expected invalid cron to be rejected")


def test_disabled_pipeline_keeps_schedule(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "paused.py"
    script_path.write_text('print("paused")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Paused scheduled refresh",
        script_id="paused.py",
        connector_sync_id=None,
    )
    pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "daily", "timeOfDay": "06:00", "timezone": "Asia/Kolkata"},
    )
    updated = pipelines.set_pipeline_enabled(pipeline["id"], False)

    assert updated["enabled"] is False
    assert updated["schedule"]["type"] == "daily"
    assert updated["schedule"]["timeOfDay"] == "06:00"


def test_due_enabled_schedule_runs_and_recalculates_next_run(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "due.py"
    script_path.write_text('print("due schedule")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Due scheduled refresh",
        script_id="due.py",
        connector_sync_id=None,
    )
    pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "hourly", "timezone": "Asia/Kolkata"},
    )
    due_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    _force_schedule_next_run(workspace, pipeline["id"], due_at.isoformat())

    due_runs = pipelines.process_due_schedules(now=datetime.now(timezone.utc))

    assert len(due_runs) == 1
    assert due_runs[0]["pipelineId"] == pipeline["id"]
    assert due_runs[0]["trigger"] == "schedule"
    assert "due schedule" in due_runs[0]["stdout"]
    listed = pipelines.list_pipelines()[0]
    assert datetime.fromisoformat(listed["schedule"]["nextRunAt"]) > datetime.now(timezone.utc)


def test_due_disabled_schedule_is_skipped(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "disabled_due.py"
    script_path.write_text('print("disabled due")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Disabled due refresh",
        script_id="disabled_due.py",
        connector_sync_id=None,
    )
    pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "hourly", "timezone": "Asia/Kolkata"},
    )
    pipelines.set_pipeline_enabled(pipeline["id"], False)
    due_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    _force_schedule_next_run(workspace, pipeline["id"], due_at.isoformat())

    due_runs = pipelines.process_due_schedules(now=datetime.now(timezone.utc))

    assert due_runs == []
    assert pipelines.list_runs(pipeline["id"]) == []


def test_failed_scheduled_run_ack_and_new_failure_reopens_alert(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "fails.py"
    script_path.write_text('raise RuntimeError("scheduled boom")\n', encoding="utf-8")

    from app.services import pipelines

    pipeline = pipelines.create_pipeline(
        pipeline_name="Failing scheduled refresh",
        script_id="fails.py",
        connector_sync_id=None,
    )
    pipelines.set_pipeline_schedule(
        pipeline["id"],
        {"type": "hourly", "timezone": "Asia/Kolkata"},
    )
    _force_schedule_next_run(workspace, pipeline["id"], (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat())

    due_runs = pipelines.process_due_schedules(now=datetime.now(timezone.utc))

    assert len(due_runs) == 1
    first_run = due_runs[0]
    assert first_run["status"] == "error"
    assert first_run["trigger"] == "schedule"
    failures = pipelines.list_failures()
    assert len(failures) == 1
    assert failures[0]["status"] == "active"
    assert failures[0]["runId"] == first_run["id"]

    ack = pipelines.acknowledge_failure(first_run["id"])
    assert ack == {"acknowledged": True, "runId": first_run["id"]}
    assert pipelines.list_failures() == []
    assert pipelines.list_runs(pipeline["id"], status_filter="error")[0]["id"] == first_run["id"]

    _force_schedule_next_run(workspace, pipeline["id"], (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat())
    second_run = pipelines.process_due_schedules(now=datetime.now(timezone.utc))[0]

    assert second_run["id"] != first_run["id"]
    failures = pipelines.list_failures()
    assert len(failures) == 1
    assert failures[0]["runId"] == second_run["id"]


def test_pipeline_runs_odoo_sync_pre_step_before_script(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "with_sync.py"
    script_path.write_text('print("script after sync")\n', encoding="utf-8")

    from app.services import pipelines

    sync_calls = []
    monkeypatch.setattr(
        pipelines.odoo,
        "sync_cursor",
        lambda sync_cursor_id: sync_calls.append(sync_cursor_id) or {
            "status": "success",
            "targetQualifiedName": "raw_odoo.partners",
            "inserted": 1,
            "updated": 2,
            "lastCursorValue": "2026-05-02T04:00:00",
        },
    )
    pipeline = pipelines.create_pipeline(
        pipeline_name="Sync then script",
        script_id="with_sync.py",
        connector_sync_id="cursor-1",
    )

    run = pipelines.run_pipeline_now(pipeline["id"])

    assert sync_calls == ["cursor-1"]
    assert run["status"] == "success"
    assert "script after sync" in run["stdout"]
    assert run["preStep"]["status"] == "success"
    assert run["preStep"]["inserted"] == 1
    assert run["preStep"]["updated"] == 2


def test_pipeline_blocks_script_when_odoo_sync_pre_step_fails(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    script_path = workspace.workspace_paths()["scripts"] / "blocked.py"
    script_path.write_text('print("should not run")\n', encoding="utf-8")

    from app.services import pipelines

    monkeypatch.setattr(pipelines.odoo, "sync_cursor", lambda sync_cursor_id: (_ for _ in ()).throw(ValueError("Sync cursor not found.")))
    script_ran = {"value": False}

    def fake_run_script(script_name, code):
        script_ran["value"] = True
        return {"status": "success", "stdout": "", "stderr": "", "returnCode": 0, "savedTables": []}

    monkeypatch.setattr(pipelines, "run_script", fake_run_script)
    pipeline = pipelines.create_pipeline(
        pipeline_name="Blocked sync",
        script_id="blocked.py",
        connector_sync_id="missing-cursor",
    )

    run = pipelines.run_pipeline_now(pipeline["id"])

    assert script_ran["value"] is False
    assert run["status"] == "error"
    assert run["stderr"] == "Sync cursor not found."
    assert run["preStep"] == {
        "type": "odoo_sync",
        "syncCursorId": "missing-cursor",
        "status": "error",
        "message": "Sync cursor not found.",
    }


def test_pipeline_rejects_missing_script(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import pipelines

    try:
        pipelines.create_pipeline(
            pipeline_name="Broken pipeline",
            script_id="missing.py",
            connector_sync_id=None,
        )
    except ValueError as exc:
        assert str(exc) == "Saved script does not exist: missing.py"
    else:
        raise AssertionError("Expected missing script to be rejected")


def _force_schedule_next_run(workspace, pipeline_id: str, next_run_at: str) -> None:
    path = workspace.workspace_paths()["pipelines"]
    pipelines = json.loads(path.read_text(encoding="utf-8"))
    for pipeline in pipelines:
        if pipeline["id"] == pipeline_id:
            pipeline["schedule"]["nextRunAt"] = next_run_at
    path.write_text(json.dumps(pipelines, indent=2) + "\n", encoding="utf-8")
