import json
import time
from datetime import datetime, timedelta, timezone
from calendar import monthrange
from uuid import uuid4
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.services import odoo
from app.services.execution import get_script, run_script
from app.services.workspace import ensure_workspace, workspace_paths


def create_pipeline(
    *,
    pipeline_name: str,
    script_id: str,
    connector_sync_id: str | None = None,
) -> dict[str, Any]:
    ensure_workspace()
    name = pipeline_name.strip()
    script_name = script_id.strip()
    if not name:
        raise ValueError("Pipeline name is required.")
    if len(name) > 80:
        raise ValueError("Pipeline name must be 80 characters or fewer.")
    if not script_name:
        raise ValueError("Saved script is required.")

    try:
        get_script(script_name)
    except FileNotFoundError as exc:
        raise ValueError(f"Saved script does not exist: {script_name}") from exc

    pipelines = _read_pipelines()
    if any(item["name"] == name for item in pipelines):
        raise ValueError("A pipeline with this name already exists.")

    now = _now()
    pipeline = {
        "id": uuid4().hex,
        "name": name,
        "scriptId": script_name,
        "connectorSyncId": connector_sync_id,
        "enabled": True,
        "schedule": None,
        "createdAt": now,
        "updatedAt": now,
    }
    pipelines.append(pipeline)
    _write_pipelines(pipelines)
    return _with_last_run(pipeline)


def list_pipelines() -> list[dict[str, Any]]:
    ensure_workspace()
    return [_with_last_run(pipeline) for pipeline in _read_pipelines()]


def set_pipeline_enabled(pipeline_id: str, enabled: bool) -> dict[str, Any]:
    pipelines = _read_pipelines()
    for pipeline in pipelines:
        if pipeline["id"] == pipeline_id:
            pipeline["enabled"] = enabled
            pipeline["updatedAt"] = _now()
            _write_pipelines(pipelines)
            return _with_last_run(pipeline)
    raise ValueError("Pipeline not found.")


def set_pipeline_schedule(pipeline_id: str, schedule: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_schedule(schedule)
    pipelines = _read_pipelines()
    for pipeline in pipelines:
        if pipeline["id"] == pipeline_id:
            pipeline["schedule"] = validated
            pipeline["updatedAt"] = validated["updatedAt"]
            _write_pipelines(pipelines)
            return _with_last_run(pipeline)
    raise ValueError("Pipeline not found.")


def run_pipeline_now(pipeline_id: str, trigger: str = "manual") -> dict[str, Any]:
    pipeline = _pipeline_by_id(pipeline_id)
    script = get_script(pipeline["scriptId"])
    run_id = uuid4().hex
    started = time.perf_counter()
    started_at = _now()
    pre_step = _run_connector_pre_step(pipeline.get("connectorSyncId"))
    if pre_step and pre_step["status"] == "error":
        ended_at = _now()
        run = {
            "id": run_id,
            "pipelineId": pipeline["id"],
            "pipelineName": pipeline["name"],
            "scriptId": pipeline["scriptId"],
            "trigger": trigger,
            "status": "error",
            "startedAt": started_at,
            "endedAt": ended_at,
            "durationMs": int((time.perf_counter() - started) * 1000),
            "stdout": "",
            "stderr": pre_step["message"],
            "returnCode": 1,
            "savedTables": [],
            "preStep": pre_step,
        }
        _write_run(run)
        return run

    result = run_script(script_name=script["name"], code=script["code"])
    ended_at = _now()
    duration_ms = int((time.perf_counter() - started) * 1000)

    run = {
        "id": run_id,
        "pipelineId": pipeline["id"],
        "pipelineName": pipeline["name"],
        "scriptId": pipeline["scriptId"],
        "trigger": trigger,
        "status": result["status"],
        "startedAt": started_at,
        "endedAt": ended_at,
        "durationMs": duration_ms,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "returnCode": result["returnCode"],
        "savedTables": result["savedTables"],
        "preStep": pre_step,
    }
    _write_run(run)
    return run


def process_due_schedules(now: datetime | None = None) -> list[dict[str, Any]]:
    ensure_workspace()
    now_utc = now or datetime.now(timezone.utc)
    due_runs: list[dict[str, Any]] = []
    pipelines = _read_pipelines()
    changed = False

    for pipeline in pipelines:
        schedule = pipeline.get("schedule")
        if not pipeline.get("enabled", True) or not schedule:
            continue
        next_run_at = datetime.fromisoformat(schedule["nextRunAt"])
        if next_run_at <= now_utc:
            run = run_pipeline_now(pipeline["id"], trigger="schedule")
            due_runs.append(run)
            if run["status"] == "success":
                refreshed_schedule = _validate_schedule(schedule, now=now_utc)
                pipeline["schedule"] = refreshed_schedule
                pipeline["updatedAt"] = refreshed_schedule["updatedAt"]
                changed = True

    if changed:
        _write_pipelines(pipelines)
    return due_runs


def list_runs(pipeline_id: str | None = None, status_filter: str = "all") -> list[dict[str, Any]]:
    ensure_workspace()
    runs = []
    for path in workspace_paths()["runs"].glob("pipeline-*.json"):
        runs.append(json.loads(path.read_text(encoding="utf-8")))
    if pipeline_id:
        runs = [run for run in runs if run["pipelineId"] == pipeline_id]
    if status_filter != "all":
        runs = [run for run in runs if run["status"] == status_filter]
    return sorted(runs, key=lambda run: run["startedAt"], reverse=True)


def list_failures(active_only: bool = True) -> list[dict[str, Any]]:
    acknowledgements = _read_failure_acknowledgements()
    failures = []
    for run in list_runs(status_filter="error"):
        acknowledged_at = acknowledgements.get(run["id"])
        status = "acknowledged" if acknowledged_at else "active"
        if active_only and status != "active":
            continue
        failures.append(
            {
                "pipelineId": run["pipelineId"],
                "pipelineName": run["pipelineName"],
                "runId": run["id"],
                "status": status,
                "createdAt": run["endedAt"] or run["startedAt"],
                "acknowledgedAt": acknowledged_at,
                "message": run["stderr"].splitlines()[-1] if run.get("stderr") else "Pipeline run failed.",
            }
        )
    return failures


def acknowledge_failure(run_id: str) -> dict[str, Any]:
    run = get_run(run_id)
    if run["status"] != "error":
        raise ValueError("Only failed pipeline runs can be acknowledged.")
    acknowledgements = _read_failure_acknowledgements()
    acknowledgements[run_id] = _now()
    _write_failure_acknowledgements(acknowledgements)
    return {"acknowledged": True, "runId": run_id}


def _run_connector_pre_step(connector_sync_id: str | None) -> dict[str, Any] | None:
    if not connector_sync_id:
        return None
    try:
        result = odoo.sync_cursor(connector_sync_id)
    except ValueError as exc:
        return {
            "type": "odoo_sync",
            "syncCursorId": connector_sync_id,
            "status": "error",
            "message": str(exc),
        }
    return {
        "type": "odoo_sync",
        "syncCursorId": connector_sync_id,
        "status": result["status"],
        "targetQualifiedName": result["targetQualifiedName"],
        "inserted": result["inserted"],
        "updated": result["updated"],
        "lastCursorValue": result["lastCursorValue"],
        "message": f"Odoo sync {result['status']}: {result['inserted']} inserted, {result['updated']} updated.",
    }


def get_run(run_id: str) -> dict[str, Any]:
    path = _run_path(run_id)
    if not path.exists():
        raise ValueError("Pipeline run not found.")
    return json.loads(path.read_text(encoding="utf-8"))


def _pipeline_by_id(pipeline_id: str) -> dict[str, Any]:
    for pipeline in _read_pipelines():
        if pipeline["id"] == pipeline_id:
            return pipeline
    raise ValueError("Pipeline not found.")


def _with_last_run(pipeline: dict[str, Any]) -> dict[str, Any]:
    runs = list_runs(pipeline["id"])
    return {**pipeline, "lastRun": runs[0] if runs else None}


def _read_pipelines() -> list[dict[str, Any]]:
    ensure_workspace()
    return json.loads(workspace_paths()["pipelines"].read_text(encoding="utf-8"))


def _write_pipelines(pipelines: list[dict[str, Any]]) -> None:
    workspace_paths()["pipelines"].write_text(json.dumps(pipelines, indent=2) + "\n", encoding="utf-8")


def _write_run(run: dict[str, Any]) -> None:
    _run_path(run["id"]).write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")


def _read_failure_acknowledgements() -> dict[str, str]:
    ensure_workspace()
    return json.loads(workspace_paths()["pipeline_failures"].read_text(encoding="utf-8"))


def _write_failure_acknowledgements(acknowledgements: dict[str, str]) -> None:
    workspace_paths()["pipeline_failures"].write_text(
        json.dumps(acknowledgements, indent=2) + "\n",
        encoding="utf-8",
    )


def _run_path(run_id: str):
    return workspace_paths()["runs"] / f"pipeline-{run_id}.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_schedule(schedule: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    schedule_type = str(schedule.get("type", "")).strip().lower()
    if schedule_type not in {"hourly", "daily", "weekly", "cron"}:
        raise ValueError("Schedule type must be hourly, daily, weekly, or cron.")

    timezone_name = str(schedule.get("timezone") or "Asia/Kolkata").strip()
    try:
        tz = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("Invalid timezone.") from exc

    now_utc = now or datetime.now(timezone.utc)
    updated_at = now_utc.isoformat()
    validated: dict[str, Any] = {
        "type": schedule_type,
        "timezone": timezone_name,
        "updatedAt": updated_at,
    }

    if schedule_type == "hourly":
        next_run_at = (now_utc + timedelta(hours=1)).replace(second=0, microsecond=0)
    elif schedule_type == "daily":
        time_of_day = str(schedule.get("timeOfDay") or "06:00").strip()
        hour, minute = _parse_time_of_day(time_of_day)
        next_run_at = _next_daily(now_utc, tz, hour, minute)
        validated["timeOfDay"] = time_of_day
    elif schedule_type == "weekly":
        time_of_day = str(schedule.get("timeOfDay") or "06:00").strip()
        hour, minute = _parse_time_of_day(time_of_day)
        weekday = str(schedule.get("weekday") or "monday").strip().lower()
        next_run_at = _next_weekly(now_utc, tz, weekday, hour, minute)
        validated["timeOfDay"] = time_of_day
        validated["weekday"] = weekday
    else:
        cron_expression = str(schedule.get("cronExpression") or "").strip()
        next_run_at = _next_cron(now_utc, cron_expression)
        validated["cronExpression"] = cron_expression

    validated["nextRunAt"] = next_run_at.astimezone(timezone.utc).isoformat()
    return validated


def _parse_time_of_day(value: str) -> tuple[int, int]:
    parts = value.split(":")
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError("Time of day must use HH:MM format.")
    hour = int(parts[0])
    minute = int(parts[1])
    if hour > 23 or minute > 59:
        raise ValueError("Time of day must use HH:MM format.")
    return hour, minute


def _next_daily(now: datetime, tz: ZoneInfo, hour: int, minute: int) -> datetime:
    local_now = now.astimezone(tz)
    candidate = local_now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= local_now:
        candidate += timedelta(days=1)
    return candidate


WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def _next_weekly(now: datetime, tz: ZoneInfo, weekday: str, hour: int, minute: int) -> datetime:
    if weekday not in WEEKDAYS:
        raise ValueError("Weekday must be a full lowercase weekday name.")
    local_now = now.astimezone(tz)
    days_ahead = (WEEKDAYS[weekday] - local_now.weekday()) % 7
    candidate = (local_now + timedelta(days=days_ahead)).replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )
    if candidate <= local_now:
        candidate += timedelta(days=7)
    return candidate


def _next_cron(now: datetime, expression: str) -> datetime:
    fields = expression.split()
    if len(fields) != 5:
        raise ValueError("Cron expression must have five fields.")

    minutes = _parse_cron_field(fields[0], 0, 59, "minute")
    hours = _parse_cron_field(fields[1], 0, 23, "hour")
    days = _parse_cron_field(fields[2], 1, 31, "day")
    months = _parse_cron_field(fields[3], 1, 12, "month")
    weekdays = {0 if item == 7 else item for item in _parse_cron_field(fields[4], 0, 7, "weekday")}

    candidate = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    for _ in range(366 * 24 * 60):
        _, max_day = monthrange(candidate.year, candidate.month)
        cron_weekday = (candidate.weekday() + 1) % 7
        if (
            candidate.minute in minutes
            and candidate.hour in hours
            and candidate.day <= max_day
            and candidate.day in days
            and candidate.month in months
            and cron_weekday in weekdays
        ):
            return candidate
        candidate += timedelta(minutes=1)
    raise ValueError("Cron expression has no matching run in the next year.")


def _parse_cron_field(field: str, minimum: int, maximum: int, label: str) -> set[int]:
    values: set[int] = set()
    for token in field.split(","):
        token = token.strip()
        if not token:
            raise ValueError(f"Invalid cron {label} field.")
        if token == "*":
            values.update(range(minimum, maximum + 1))
            continue
        if token.startswith("*/"):
            step = _parse_positive_int(token[2:], label)
            values.update(range(minimum, maximum + 1, step))
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = _parse_positive_int(start_text, label)
            end = _parse_positive_int(end_text, label)
            if start > end:
                raise ValueError(f"Invalid cron {label} range.")
            _assert_cron_bounds(start, minimum, maximum, label)
            _assert_cron_bounds(end, minimum, maximum, label)
            values.update(range(start, end + 1))
            continue
        value = _parse_positive_int(token, label)
        _assert_cron_bounds(value, minimum, maximum, label)
        values.add(value)
    return values


def _parse_positive_int(value: str, label: str) -> int:
    if not value.isdigit():
        raise ValueError(f"Invalid cron {label} field.")
    parsed = int(value)
    if parsed < 0:
        raise ValueError(f"Invalid cron {label} field.")
    return parsed


def _assert_cron_bounds(value: int, minimum: int, maximum: int, label: str) -> None:
    if value < minimum or value > maximum:
        raise ValueError(f"Cron {label} field is out of range.")
