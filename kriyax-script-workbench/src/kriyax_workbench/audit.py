from __future__ import annotations

import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from kriyax_workbench.workspace import ensure_workspace, workspace_paths


SECRET_KEYS = {"api_key", "apikey", "password", "token", "secret", "authorization"}


def audit_event(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_workspace()
    record = {
        "eventId": uuid4().hex,
        "eventType": event_type,
        "createdAt": _now(),
        "actor": os.environ.get("KRIYAX_ACTOR", "cli"),
        "workspaceRoot": str(workspace_paths()["root"]),
        **_redact(payload or {}),
    }
    _append(record)
    return record


def start_action(action: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return audit_event(f"{action}.started", {"startedAt": _now(), **(payload or {})})


def finish_action(start_record: dict[str, Any], status: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    action = str(start_record["eventType"]).removesuffix(".started")
    return audit_event(
        f"{action}.finished",
        {
            "parentEventId": start_record["eventId"],
            "startedAt": start_record.get("startedAt"),
            "finishedAt": _now(),
            "status": status,
            **(payload or {}),
        },
    )


def snapshot_script(script_path: Path, event_id: str) -> dict[str, str]:
    ensure_workspace()
    digest = sha256_file(script_path)
    snapshot_path = workspace_paths()["audit_snapshots"] / f"{event_id}-{script_path.name}"
    shutil.copyfile(script_path, snapshot_path)
    return {"scriptSha256": digest, "snapshotPath": str(snapshot_path)}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_events(limit: int = 50) -> list[dict[str, Any]]:
    ensure_workspace()
    lines = workspace_paths()["audit_log"].read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines[-limit:]]


def get_event(event_id: str) -> dict[str, Any]:
    for event in read_events(limit=100000):
        if event.get("eventId") == event_id:
            return event
    raise FileNotFoundError(f"Audit event not found: {event_id}")


def verify_snapshot(event_id: str) -> dict[str, Any]:
    event = get_event(event_id)
    snapshot_path = Path(event.get("snapshotPath", ""))
    expected = event.get("scriptSha256")
    if not expected or not snapshot_path.exists():
        return {"eventId": event_id, "verified": False, "reason": "snapshot missing"}
    actual = sha256_file(snapshot_path)
    return {"eventId": event_id, "verified": actual == expected, "expected": expected, "actual": actual}


def _append(record: dict[str, Any]) -> None:
    with workspace_paths()["audit_log"].open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, default=str) + "\n")


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "***REDACTED***" if key.lower() in SECRET_KEYS else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
