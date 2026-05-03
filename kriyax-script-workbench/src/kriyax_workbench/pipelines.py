from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from kriyax_workbench.audit import finish_action, start_action
from kriyax_workbench.execution import run_script, script_file
from kriyax_workbench.json_store import read_json, write_json
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def create_pipeline(name: str, script: str, connector_sync_id: str | None = None) -> dict[str, Any]:
    ensure_workspace()
    if not script_file(script).exists():
        raise FileNotFoundError(f"Script not found: {script}")
    pipelines = _read_pipelines()
    if any(item["name"] == name for item in pipelines):
        raise ValueError("A pipeline with this name already exists.")
    pipeline = {
        "id": uuid4().hex,
        "name": name,
        "script": script_file(script).name,
        "connectorSyncId": connector_sync_id,
        "enabled": True,
        "schedule": None,
        "createdAt": _now(),
        "updatedAt": _now(),
    }
    pipelines.append(pipeline)
    _write_pipelines(pipelines)
    return pipeline


def list_pipelines() -> list[dict[str, Any]]:
    runs = list_runs()
    result = []
    for pipeline in _read_pipelines():
        latest = next((run for run in runs if run["pipelineId"] == pipeline["id"]), None)
        result.append({**pipeline, "lastRun": latest})
    return result


def set_enabled(pipeline_id: str, enabled: bool) -> dict[str, Any]:
    pipelines = _read_pipelines()
    for pipeline in pipelines:
        if pipeline["id"] == pipeline_id:
            pipeline["enabled"] = enabled
            pipeline["updatedAt"] = _now()
            _write_pipelines(pipelines)
            return pipeline
    raise FileNotFoundError(f"Pipeline not found: {pipeline_id}")


def set_schedule(pipeline_id: str, schedule: dict[str, Any]) -> dict[str, Any]:
    pipelines = _read_pipelines()
    for pipeline in pipelines:
        if pipeline["id"] == pipeline_id:
            pipeline["schedule"] = _normalize_schedule(schedule)
            pipeline["updatedAt"] = _now()
            _write_pipelines(pipelines)
            return pipeline
    raise FileNotFoundError(f"Pipeline not found: {pipeline_id}")


def run_pipeline(pipeline_id: str, trigger: str = "manual") -> dict[str, Any]:
    pipeline = _pipeline(pipeline_id)
    audit = start_action("pipeline.run", {"pipelineId": pipeline_id, "trigger": trigger, "script": pipeline["script"]})
    started = datetime.now(timezone.utc)
    result = run_script(pipeline["script"])
    finished = datetime.now(timezone.utc)
    run = {
        "id": uuid4().hex,
        "pipelineId": pipeline_id,
        "pipelineName": pipeline["name"],
        "script": pipeline["script"],
        "trigger": trigger,
        "status": result["status"],
        "startedAt": started.isoformat(),
        "finishedAt": finished.isoformat(),
        "durationMs": round((finished - started).total_seconds() * 1000),
        "savedTables": result["savedTables"],
        "stdoutPath": result["stdoutPath"],
        "stderrPath": result["stderrPath"],
    }
    _write_run(run)
    if run["status"] != "success":
        failures = read_json(workspace_paths()["pipeline_failures"], {})
        failures[run["id"]] = {"pipelineId": pipeline_id, "pipelineName": pipeline["name"], "runId": run["id"], "status": "open", "createdAt": _now()}
        write_json(workspace_paths()["pipeline_failures"], failures)
    finish_action(audit, run["status"], {"runId": run["id"], "savedTables": run["savedTables"], "durationMs": run["durationMs"]})
    return run


def list_runs(pipeline_id: str | None = None, status: str = "all") -> list[dict[str, Any]]:
    ensure_workspace()
    runs = []
    for path in sorted(workspace_paths()["runs"].glob("pipeline-*.json"), reverse=True):
        run = read_json(path, {})
        if pipeline_id and run.get("pipelineId") != pipeline_id:
            continue
        if status != "all" and run.get("status") != status:
            continue
        runs.append(run)
    return runs


def list_failures(active_only: bool = True) -> list[dict[str, Any]]:
    failures = list(read_json(workspace_paths()["pipeline_failures"], {}).values())
    if active_only:
        failures = [failure for failure in failures if failure.get("status") == "open"]
    return failures


def acknowledge_failure(run_id: str) -> dict[str, Any]:
    failures = read_json(workspace_paths()["pipeline_failures"], {})
    if run_id not in failures:
        raise FileNotFoundError(f"Failure not found: {run_id}")
    failures[run_id]["status"] = "acknowledged"
    failures[run_id]["acknowledgedAt"] = _now()
    write_json(workspace_paths()["pipeline_failures"], failures)
    return failures[run_id]


def process_due(now: datetime | None = None) -> list[dict[str, Any]]:
    current = now or datetime.now(timezone.utc)
    processed = []
    pipelines = _read_pipelines()
    for pipeline in pipelines:
        schedule = pipeline.get("schedule")
        if not pipeline.get("enabled") or not schedule:
            continue
        next_run = datetime.fromisoformat(schedule["nextRunAt"])
        if next_run <= current:
            processed.append(run_pipeline(pipeline["id"], trigger="schedule"))
            schedule["nextRunAt"] = _next_run(schedule, current).isoformat()
            pipeline["updatedAt"] = _now()
    _write_pipelines(pipelines)
    return processed


def _normalize_schedule(schedule: dict[str, Any]) -> dict[str, Any]:
    schedule_type = schedule.get("type", "hourly")
    now = datetime.now(timezone.utc)
    normalized = {"type": schedule_type}
    if schedule_type == "hourly":
        normalized["nextRunAt"] = (now + timedelta(hours=1)).isoformat()
    elif schedule_type == "daily":
        time_of_day = schedule.get("timeOfDay", "06:00")
        hour, minute = [int(part) for part in time_of_day.split(":", 1)]
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        normalized["timeOfDay"] = time_of_day
        normalized["nextRunAt"] = candidate.isoformat()
    else:
        raise ValueError("Only hourly and daily schedules are supported in the script workbench.")
    return normalized


def _next_run(schedule: dict[str, Any], now: datetime) -> datetime:
    if schedule["type"] == "hourly":
        return now + timedelta(hours=1)
    hour, minute = [int(part) for part in schedule["timeOfDay"].split(":", 1)]
    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate


def _pipeline(pipeline_id: str) -> dict[str, Any]:
    for pipeline in _read_pipelines():
        if pipeline["id"] == pipeline_id:
            return pipeline
    raise FileNotFoundError(f"Pipeline not found: {pipeline_id}")


def _read_pipelines() -> list[dict[str, Any]]:
    ensure_workspace()
    return read_json(workspace_paths()["pipelines"], [])


def _write_pipelines(pipelines: list[dict[str, Any]]) -> None:
    write_json(workspace_paths()["pipelines"], pipelines)


def _write_run(run: dict[str, Any]) -> None:
    write_json(workspace_paths()["runs"] / f"pipeline-{run['id']}.json", run)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
