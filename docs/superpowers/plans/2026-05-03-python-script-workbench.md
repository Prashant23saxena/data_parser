# Python Script Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **2026-05-03 branch update:** This plan is now superseded for implementation by the standalone application plan at `kriyax-script-workbench/docs/IMPLEMENTATION_PLAN.md`. Do not add the script tools into `kriyax-data-app/backend` unless the user explicitly asks to merge the standalone app back into the existing UI/backend app.

**Goal:** Build a barebones Python-script-first operating layer that exposes every KriyaX Data Layer capability without requiring the React UI.

**Architecture:** Keep the existing FastAPI service modules as the source of truth. Add a thin `backend/tools/` script layer that calls those services, prints human-readable tables or JSON, and writes real files into `workspace/`. User transformation logic stays in normal `.py` files under `workspace/scripts/`; scripts are run through the existing execution wrapper so `load_table()`, `save_table()`, and `show()` work consistently.

**Tech Stack:** Python 3, argparse, pandas, DuckDB, existing `app.services.*`, pytest, existing workspace folder contract.

---

## Core Answers

### Where Tables Are Stored

All ingested and derived tables are stored inside one local DuckDB database file:

```text
kriyax-data-app/workspace/warehouse/kriyax.duckdb
```

Each table has a schema-qualified name:

```text
raw_files.orders
odoo.sale_order
curated.revenue_by_region
```

The actual rows live in DuckDB. The catalog metadata lives separately in:

```text
kriyax-data-app/workspace/metadata/catalog.json
```

The catalog stores table name, schema, source type, row count, column list, and source metadata. It is not the table storage; it is the table index.

### How Join Results Are Saved

A user or agent writes a normal Python file:

```python
orders = load_table("raw_files.orders")
customers = load_table("raw_files.customers")

joined = orders.merge(customers, on="customer_id", how="left")
region_revenue = joined.groupby("region", as_index=False)["amount"].sum()

show(region_revenue, name="region_revenue_preview")
save_table(region_revenue, "region_revenue", schema="curated")
```

When run through `tools/script_run.py`, `save_table()` creates or replaces:

```text
curated.region_revenue
```

That new table is persisted in DuckDB and auto-registered in `metadata/catalog.json`.

### How Tables Are Viewed Without UI

Use scripts:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
python tools/catalog_list.py
python tools/table_describe.py curated.region_revenue
python tools/table_view.py curated.region_revenue --limit 20
python tools/table_export.py curated.region_revenue --output ../workspace/data/exports/region_revenue.csv
```

For unsaved intermediate DataFrames, use `show(df, name="preview_name")` inside the transformation script. `tools/script_run.py` prints the preview from the run result without saving it as a table.

### Agent Skill Requirement

The script workbench needs a dedicated agent skill so Codex, Antigravity, or another coding agent knows the exact operating contract. This is not business logic. It is the instruction layer for the agent.

Create a repo-local skill:

```text
kriyax-data-app/agent-skill/
  SKILL.md
  references/
    script-workbench-contract.md
```

The skill must tell the agent:

- Work from `kriyax-data-app/backend`.
- Use `python tools/*.py` commands for all product actions.
- Do not run `workspace/scripts/*.py` directly with `python`; use `tools/script_run.py` so helpers and audit are applied.
- Use `load_table("schema.table")`, `show(df, name="preview")`, and `save_table(df, "name", schema="curated")`.
- After any write action, verify with `tools/catalog_list.py`, `tools/table_view.py`, or `tools/audit_tail.py`.
- Treat `workspace/audit/` as system-owned evidence. Do not edit it manually.

This can later be installed into `~/.codex/skills/kriyax-data-workbench/`, but the repo-local version is enough for the implementation contract.

### Forced Auditability Requirement

Auditability must be enforced by deterministic Python code, not by the LLM remembering to write notes.

Add an audit service:

```text
kriyax-data-app/backend/app/services/audit.py
```

Audit records are stored in two places:

```text
kriyax-data-app/workspace/audit/audit.jsonl
kriyax-data-app/workspace/audit/snapshots/
```

`audit.jsonl` is append-only evidence. Each record includes:

```json
{
  "eventId": "uuid",
  "eventType": "script.run.finished",
  "actor": "cli",
  "toolName": "tools/script_run.py",
  "workspaceRoot": ".../workspace",
  "scriptName": "revenue_by_region.py",
  "scriptPath": ".../workspace/scripts/revenue_by_region.py",
  "scriptSha256": "hash of exact code that ran",
  "snapshotPath": ".../workspace/audit/snapshots/event-id.py",
  "startedAt": "timestamp",
  "finishedAt": "timestamp",
  "status": "success",
  "returnCode": 0,
  "savedTables": ["curated.region_revenue"],
  "displayFrames": ["preview"],
  "stdoutPath": ".../workspace/runs/event-id.stdout.txt",
  "stderrPath": ".../workspace/runs/event-id.stderr.txt"
}
```

For import, Odoo fetch, table management, pipeline run, and agent generation, the audit service records the action name, inputs with secrets redacted, output table names, status, and error message. Script execution additionally snapshots the exact `.py` code that ran so later edits cannot erase history.

The enforcement point is the service layer:

- `app.services.execution.run_script()` must always write audit start/finish records.
- `app.services.file_import.commit_import()` must audit imported table creation.
- `app.services.odoo.fetch_records_to_table()` and `sync_cursor()` must audit Odoo writes.
- `app.services.pipelines.run_pipeline_now()` must audit pipeline execution.
- `app.services.agent.generate_code()`, `correct_code()`, and `follow_up()` must audit generated code metadata and destination script path when saved through tools.

The CLI tools can add friendly labels, but audit must not depend on the LLM or the CLI alone.

---

## File Structure

Create:

```text
kriyax-data-app/backend/tools/
  __init__.py
  _cli.py
  audit_tail.py
  audit_show.py
  audit_verify.py
  workspace_status.py
  file_inspect.py
  file_import.py
  catalog_list.py
  catalog_search.py
  table_describe.py
  table_view.py
  table_rename.py
  table_truncate.py
  table_drop.py
  table_export.py
  script_create.py
  script_list.py
  script_show.py
  script_run.py
  agent_generate.py
  agent_fix.py
  agent_follow_up.py
  llm_status.py
  llm_test.py
  odoo_test_connection.py
  odoo_save_connection.py
  odoo_list_connections.py
  odoo_models.py
  odoo_fields.py
  odoo_fetch.py
  odoo_cursor_create.py
  odoo_sync.py
  pipeline_create.py
  pipeline_list.py
  pipeline_schedule.py
  pipeline_enable.py
  pipeline_run.py
  pipeline_runs.py
  pipeline_failures.py
  pipeline_ack_failure.py
  pipeline_process_due.py
```

Create tests:

```text
kriyax-data-app/backend/tests/test_tools_cli.py
kriyax-data-app/backend/tests/test_audit.py
```

Modify:

```text
kriyax-data-app/backend/app/services/workspace.py
kriyax-data-app/backend/app/services/execution.py
kriyax-data-app/backend/app/services/file_import.py
kriyax-data-app/backend/app/services/odoo.py
kriyax-data-app/backend/app/services/pipelines.py
kriyax-data-app/backend/app/services/agent.py
kriyax-data-app/README.md
```

Do not duplicate business logic in tools. Each tool should import and call `app.services.*`.

---

## Feature Coverage Matrix

| Feature | Python-script interface |
| --- | --- |
| F-DC-001 Upload CSV/Excel | `tools/file_inspect.py <file>` copies or references local path for parsing |
| F-DC-002 Auto-detect columns/types | `tools/file_inspect.py <file> --json` |
| F-DC-003 Preview before import | `tools/file_inspect.py <file> --limit 50` |
| F-DC-004 Configure Odoo connection | `tools/odoo_test_connection.py`, `tools/odoo_save_connection.py` |
| F-DC-005 Browse Odoo models/fields | `tools/odoo_models.py`, `tools/odoo_fields.py` |
| F-DC-006 Fetch Odoo records to table | `tools/odoo_fetch.py` |
| F-DC-007 Incremental/delta sync | `tools/odoo_cursor_create.py`, `tools/odoo_sync.py` |
| F-DC-008 Manage saved connections | `tools/odoo_list_connections.py`, later edit/delete scripts if service support is added |
| F-SC-001 Table registry | `tools/catalog_list.py` |
| F-SC-002 Column metadata viewer | `tools/table_describe.py <schema.table>` |
| F-SC-003 Auto-register on ingest | handled by services called from `file_import.py`, `odoo_fetch.py`, `script_run.py` |
| F-SC-004 Browse/search catalog | `tools/catalog_search.py <query>` |
| F-SC-005 Preview table rows | `tools/table_view.py <schema.table> --limit 20` |
| F-CW-001 Python code editor | real files in `workspace/scripts/*.py`, edited in Codex/Antigravity |
| F-CW-002 Show available tables | `tools/catalog_list.py`, `tools/table_describe.py` |
| F-CW-003 Load tables as DataFrames | `load_table("schema.table")` inside scripts |
| F-CW-004 Save DataFrame as table | `save_table(df, "table", schema="curated")` inside scripts |
| F-CW-005 View execution output | `tools/script_run.py <script.py>` |
| F-CW-006 Save and rerun scripts | `tools/script_create.py`, `tools/script_list.py`, `tools/script_run.py` |
| F-AL-001 Chat interface | external LLM/Codex prompt plus `tools/agent_generate.py` |
| F-AL-002 Schema-aware context | existing `app.services.agent.generate_code()` reads catalog |
| F-AL-003 Generate Python/pandas code | `tools/agent_generate.py "request"` |
| F-AL-004 Insert code into editor | `tools/agent_generate.py --save workspace/scripts/name.py` |
| F-AL-005 Self-correction on error | `tools/agent_fix.py --script <script> --run latest` |
| F-AL-006 Conversational follow-ups | `tools/agent_follow_up.py --script <script> "change request"` |
| F-PS-001 Create pipeline | `tools/pipeline_create.py` |
| F-PS-002 Schedule pipeline | `tools/pipeline_schedule.py` |
| F-PS-003 Manual trigger | `tools/pipeline_run.py` |
| F-PS-004 Run history/status | `tools/pipeline_runs.py` |
| F-PS-005 Error notifications | `tools/pipeline_failures.py` |
| F-PS-006 Enable/disable pipeline | `tools/pipeline_enable.py` |
| F-DS-001 Backing database setup | `tools/workspace_status.py` |
| F-DS-002 Auto-create tables on import | `tools/file_import.py`, `tools/odoo_fetch.py` |
| F-DS-003 Persist derived tables | `save_table()` through `tools/script_run.py` |
| F-DS-004 Basic table management | `tools/table_rename.py`, `tools/table_truncate.py`, `tools/table_drop.py` |
| F-DS-005 Export table data | `tools/table_export.py` |

---

## Task 0: Deterministic Audit Layer and Agent Skill

**Files:**
- Create: `kriyax-data-app/backend/app/services/audit.py`
- Modify: `kriyax-data-app/backend/app/services/workspace.py`
- Modify: `kriyax-data-app/backend/app/services/execution.py`
- Create: `kriyax-data-app/backend/tools/audit_tail.py`
- Create: `kriyax-data-app/backend/tools/audit_show.py`
- Create: `kriyax-data-app/backend/tools/audit_verify.py`
- Create: `kriyax-data-app/agent-skill/SKILL.md`
- Create: `kriyax-data-app/agent-skill/references/script-workbench-contract.md`
- Test: `kriyax-data-app/backend/tests/test_audit.py`

- [ ] **Step 1: Write failing audit tests**

Create `tests/test_audit.py`:

```python
import importlib
import json
from pathlib import Path

import duckdb


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_run_script_writes_audit_record_and_code_snapshot(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    with duckdb.connect(str(workspace.workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw")
        conn.execute("create or replace table raw.orders as select 1 as id, 10.0 as amount")

    from app.services.execution import run_script

    result = run_script(
        script_name="audit_probe.py",
        code=(
            'df = load_table("raw.orders")\n'
            'show(df, name="orders_preview")\n'
            'save_table(df, "orders_copy", schema="curated")\n'
        ),
    )

    assert result["status"] == "success"

    audit_path = workspace.workspace_paths()["audit_log"]
    records = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]
    finished = [record for record in records if record["eventType"] == "script.run.finished"]

    assert len(finished) == 1
    record = finished[0]
    assert record["scriptName"] == "audit_probe.py"
    assert record["status"] == "success"
    assert record["savedTables"] == ["curated.orders_copy"]
    assert record["scriptSha256"]
    assert Path(record["snapshotPath"]).exists()
    assert Path(record["snapshotPath"]).read_text(encoding="utf-8").startswith('df = load_table("raw.orders")')


def test_audit_redacts_secret_values(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)

    from app.services.audit import audit_event

    audit_event(
        "odoo.connection.tested",
        payload={"username": "user@example.com", "api_key": "secret-value", "password": "hidden"},
    )

    text = workspace.workspace_paths()["audit_log"].read_text(encoding="utf-8")
    assert "secret-value" not in text
    assert "hidden" not in text
    assert "***REDACTED***" in text
```

- [ ] **Step 2: Run failing audit tests**

Run:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest tests/test_audit.py -v
```

Expected: FAIL because audit paths and service do not exist.

- [ ] **Step 3: Add audit paths to workspace**

Modify `app/services/workspace.py`:

```python
def workspace_paths() -> dict[str, Path]:
    root = workspace_root()
    return {
        "root": root,
        "uploads": root / "data" / "uploads",
        "exports": root / "data" / "exports",
        "scripts": root / "scripts",
        "runs": root / "runs",
        "warehouse": root / "warehouse",
        "metadata": root / "metadata",
        "audit": root / "audit",
        "audit_snapshots": root / "audit" / "snapshots",
        "audit_log": root / "audit" / "audit.jsonl",
        "database": root / "warehouse" / "kriyax.duckdb",
        "catalog": root / "metadata" / "catalog.json",
        "connections": root / "metadata" / "connections.json",
        "llm_settings": root / "metadata" / "llm-settings.vault",
        "llm_master_key": root / "metadata" / "llm-master.key",
        "pipelines": root / "metadata" / "pipelines.json",
        "pipeline_failures": root / "metadata" / "pipeline-failures.json",
        "odoo_sync_cursors": root / "metadata" / "odoo-sync-cursors.json",
    }
```

Update `ensure_workspace()`:

```python
for key in ["uploads", "exports", "scripts", "runs", "warehouse", "metadata", "audit", "audit_snapshots"]:
    paths[key].mkdir(parents=True, exist_ok=True)

if not paths["audit_log"].exists():
    paths["audit_log"].write_text("", encoding="utf-8")
```

- [ ] **Step 4: Implement audit service**

Create `app/services/audit.py`:

```python
from __future__ import annotations

import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.services.workspace import ensure_workspace, workspace_paths

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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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
    if not snapshot_path.exists() or not expected:
        return {"eventId": event_id, "verified": False, "reason": "snapshot missing"}
    actual = sha256_file(snapshot_path)
    return {"eventId": event_id, "verified": actual == expected, "expected": expected, "actual": actual}


def _append(record: dict[str, Any]) -> None:
    path = workspace_paths()["audit_log"]
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, default=str) + "\n")


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            if key.lower() in SECRET_KEYS:
                redacted[key] = "***REDACTED***"
            else:
                redacted[key] = _redact(item)
        return redacted
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
```

- [ ] **Step 5: Wire script execution audit at service layer**

Modify `app/services/execution.py`:

```python
from app.services.audit import finish_action, snapshot_script, start_action
```

At the start of `run_script()` after `script_path` is resolved:

```python
audit_start = start_action(
    "script.run",
    {
        "scriptName": script_path.name,
        "scriptPath": str(script_path),
        "toolName": "app.services.execution.run_script",
    },
)
```

After `script_path.write_text(code, encoding="utf-8")`:

```python
script_snapshot = snapshot_script(script_path, audit_start["eventId"])
```

Before returning the result dictionary:

```python
result = {
    "status": status,
    "scriptName": script_path.name,
    "scriptPath": str(script_path),
    "stdout": stdout_buffer.getvalue(),
    "stderr": stderr,
    "returnCode": return_code,
    "savedTables": saved_tables,
    "resultTables": result_tables,
    "displayFrames": display_frames,
    "preview": preview,
}
finish_action(
    audit_start,
    status,
    {
        "scriptName": script_path.name,
        "scriptPath": str(script_path),
        **script_snapshot,
        "returnCode": return_code,
        "savedTables": saved_tables,
        "displayFrames": [frame["name"] for frame in display_frames],
    },
)
return result
```

- [ ] **Step 6: Wire write-action audit at service layer**

Modify `app/services/file_import.py`:

```python
from app.services.audit import finish_action, start_action
```

At the start of `commit_import()` after `schema` and `table` are resolved:

```python
audit_start = start_action(
    "file.import",
    {
        "filePath": str(file_path),
        "targetTable": f"{schema}.{table}",
        "columnCount": len(columns),
    },
)
```

Before returning the catalog entry:

```python
finish_action(
    audit_start,
    "success",
    {
        "qualifiedName": entry["qualifiedName"],
        "rowCount": entry["rowCount"],
        "columnCount": entry["columnCount"],
    },
)
return entry
```

Modify `app/services/odoo.py`:

```python
from app.services.audit import finish_action, start_action
```

Wrap `fetch_records_to_table()` after payload normalization:

```python
audit_start = start_action(
    "odoo.fetch",
    {
        "connectionName": payload.get("name"),
        "model": model_name,
        "targetTable": f"{target_schema}.{table_name}",
        "fields": selected_fields,
    },
)
```

Before returning success:

```python
finish_action(
    audit_start,
    "success",
    {
        "qualifiedName": entry["qualifiedName"],
        "rowCount": entry["rowCount"],
    },
)
```

Wrap `sync_cursor()` the same way with action name `odoo.sync` and payload containing `syncCursorId`, `model`, `targetTable`, `insertedRows`, and `updatedRows`.

Modify `app/services/pipelines.py`:

```python
from app.services.audit import finish_action, start_action
```

At the start of `run_pipeline_now()`:

```python
audit_start = start_action(
    "pipeline.run",
    {
        "pipelineId": pipeline_id,
        "trigger": trigger,
    },
)
```

Before returning the run record:

```python
finish_action(
    audit_start,
    run["status"],
    {
        "runId": run["id"],
        "pipelineId": run["pipelineId"],
        "scriptId": run["scriptId"],
        "savedTables": run.get("savedTables", []),
        "durationMs": run.get("durationMs"),
    },
)
```

Modify `app/services/agent.py`:

```python
from app.services.audit import audit_event, sha256_text
```

After successful generation/correction/follow-up, record metadata only:

```python
audit_event(
    "agent.code.generated",
    {
        "promptSha256": sha256_text(prompt),
        "codeSha256": sha256_text(llm_code),
        "schemaTableCount": len(context.get("tables", [])),
    },
)
```

Do not store raw prompts by default in audit records because they may contain business-sensitive text. Store hashes and the saved script snapshot when code is actually run.

- [ ] **Step 7: Implement audit utility scripts**

`tools/audit_tail.py`:

```python
import argparse

from app.services.audit import read_events
from tools._cli import print_payload


parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=20)
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

print_payload(read_events(limit=args.limit), as_json=args.json)
```

`tools/audit_show.py`:

```python
import argparse

from app.services.audit import get_event
from tools._cli import print_payload


parser = argparse.ArgumentParser()
parser.add_argument("event_id")
args = parser.parse_args()

print_payload(get_event(args.event_id), as_json=True)
```

`tools/audit_verify.py`:

```python
import argparse

from app.services.audit import verify_snapshot
from tools._cli import print_payload


parser = argparse.ArgumentParser()
parser.add_argument("event_id")
args = parser.parse_args()

print_payload(verify_snapshot(args.event_id), as_json=True)
```

- [ ] **Step 8: Create the repo-local agent skill**

Create `agent-skill/SKILL.md`:

```markdown
---
name: kriyax-data-workbench
description: Use when operating the KriyaX DataParser barebones Python workbench through scripts, including imports, catalog inspection, table viewing, Python transformations, agent code generation, pipelines, and audit verification.
---

# KriyaX Data Workbench

Work from:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
```

Use `python tools/*.py` for product actions. Do not run `../workspace/scripts/*.py` directly. Script execution must go through `python tools/script_run.py <script>` so `load_table()`, `save_table()`, `show()`, and deterministic audit logging are applied.

Before writing transformation code, inspect available tables:

```bash
python tools/catalog_list.py
python tools/table_describe.py schema.table
python tools/table_view.py schema.table --limit 20
```

Write transformation scripts in `../workspace/scripts/*.py` using:

```python
df = load_table("schema.table")
show(df, name="preview")
save_table(df, "new_table", schema="curated")
```

After any action that writes data or runs code, verify:

```bash
python tools/catalog_list.py
python tools/audit_tail.py --limit 10
```

Never manually edit `../workspace/audit/*`. Treat it as system-owned evidence.

For more detail, read `references/script-workbench-contract.md`.
```

Create `agent-skill/references/script-workbench-contract.md`:

```markdown
# Script Workbench Contract

Tables live in `../workspace/warehouse/kriyax.duckdb`.
Catalog metadata lives in `../workspace/metadata/catalog.json`.
User scripts live in `../workspace/scripts`.
Run and pipeline outputs live in `../workspace/runs`.
Audit evidence lives in `../workspace/audit/audit.jsonl` and `../workspace/audit/snapshots`.

Every product action should be traceable through audit records. If a script run succeeds or fails, inspect audit before reporting completion.
```

- [ ] **Step 9: Run audit tests**

Run:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest tests/test_audit.py -v
```

Expected: PASS.

---

## Task 1: Shared CLI Utilities

**Files:**
- Create: `kriyax-data-app/backend/tools/__init__.py`
- Create: `kriyax-data-app/backend/tools/_cli.py`
- Test: `kriyax-data-app/backend/tests/test_tools_cli.py`

- [ ] **Step 1: Write failing tests for shared output helpers**

Add to `tests/test_tools_cli.py`:

```python
from tools._cli import parse_qualified_name, render_rows


def test_parse_qualified_name_requires_schema_and_table():
    assert parse_qualified_name("raw.orders") == ("raw", "orders")

    try:
        parse_qualified_name("orders")
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected invalid table name to exit")


def test_render_rows_outputs_headers_and_values():
    text = render_rows(
        [{"qualifiedName": "raw.orders", "rowCount": 2}],
        columns=["qualifiedName", "rowCount"],
    )

    assert "qualifiedName" in text
    assert "raw.orders" in text
    assert "2" in text
```

- [ ] **Step 2: Run failing test**

Run:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest tests/test_tools_cli.py -v
```

Expected: FAIL because `tools._cli` does not exist.

- [ ] **Step 3: Implement shared CLI helpers**

Create `tools/__init__.py`:

```python
"""Command-line tools for the barebones KriyaX data workbench."""
```

Create `tools/_cli.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_qualified_name(value: str) -> tuple[str, str]:
    if "." not in value:
        raise SystemExit("Use a schema-qualified table name like raw.orders")
    schema, table = value.split(".", 1)
    if not schema.strip() or not table.strip():
        raise SystemExit("Use a schema-qualified table name like raw.orders")
    return schema.strip(), table.strip()


def print_payload(payload: Any, *, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, default=str))
        return
    if isinstance(payload, list):
        print(render_rows(payload))
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                print(f"{key}: {json.dumps(value, default=str)}")
            else:
                print(f"{key}: {value}")
        return
    print(payload)


def render_rows(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "No rows."
    selected = columns or list(rows[0].keys())
    widths = {
        column: max(len(column), *(len(str(row.get(column, ""))) for row in rows))
        for column in selected
    }
    header = "  ".join(column.ljust(widths[column]) for column in selected)
    rule = "  ".join("-" * widths[column] for column in selected)
    body = [
        "  ".join(str(row.get(column, "")).ljust(widths[column]) for column in selected)
        for row in rows
    ]
    return "\n".join([header, rule, *body])


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File does not exist: {path}")
    return path
```

- [ ] **Step 4: Run test**

Run:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest tests/test_tools_cli.py -v
```

Expected: PASS.

---

## Task 2: Workspace, Catalog, Table Viewing, and Export Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/workspace_status.py`
- Create: `kriyax-data-app/backend/tools/catalog_list.py`
- Create: `kriyax-data-app/backend/tools/catalog_search.py`
- Create: `kriyax-data-app/backend/tools/table_describe.py`
- Create: `kriyax-data-app/backend/tools/table_view.py`
- Create: `kriyax-data-app/backend/tools/table_export.py`
- Test: `kriyax-data-app/backend/tests/test_tools_cli.py`

- [ ] **Step 1: Add CLI smoke test for table viewing**

Append:

```python
import json
import subprocess
import sys

import duckdb


def test_table_view_script_reads_duckdb_table(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services.workspace import ensure_workspace, workspace_paths

    ensure_workspace()
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw")
        conn.execute("create or replace table raw.orders as select 1 as id, 'Acme' as customer")

    catalog_entry = {
        "qualifiedName": "raw.orders",
        "schema": "raw",
        "tableName": "orders",
        "source": {"kind": "test"},
        "rowCount": 1,
        "columnCount": 2,
        "columns": [{"name": "id", "type": "integer"}, {"name": "customer", "type": "text"}],
    }
    workspace_paths()["catalog"].write_text(json.dumps([catalog_entry]) + "\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "tools/table_view.py", "raw.orders", "--limit", "5"],
        cwd="/Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend",
        text=True,
        capture_output=True,
        check=True,
    )

    assert "customer" in result.stdout
    assert "Acme" in result.stdout
```

- [ ] **Step 2: Implement scripts**

`tools/workspace_status.py`:

```python
from app.services.storage import storage_status
from tools._cli import print_payload


if __name__ == "__main__":
    print_payload(storage_status())
```

`tools/catalog_list.py`:

```python
import argparse

from app.services.file_import import list_catalog_tables
from tools._cli import print_payload, render_rows


parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

tables = list_catalog_tables()
if args.json:
    print_payload(tables, as_json=True)
else:
    print(render_rows(tables, columns=["qualifiedName", "rowCount", "columnCount"]))
```

`tools/catalog_search.py`:

```python
import argparse

from app.services.file_import import list_catalog_tables
from tools._cli import render_rows


parser = argparse.ArgumentParser()
parser.add_argument("query")
args = parser.parse_args()

query = args.query.lower()
matches = []
for table in list_catalog_tables():
    haystack = [table.get("qualifiedName", ""), table.get("source", {}).get("kind", "")]
    haystack.extend(column.get("name", "") for column in table.get("columns", []))
    if any(query in str(value).lower() for value in haystack):
        matches.append(table)

print(render_rows(matches, columns=["qualifiedName", "rowCount", "columnCount"]))
```

`tools/table_describe.py`:

```python
import argparse

from app.services.file_import import list_catalog_tables
from tools._cli import parse_qualified_name, render_rows


parser = argparse.ArgumentParser()
parser.add_argument("table")
args = parser.parse_args()

schema, table = parse_qualified_name(args.table)
qualified = f"{schema}.{table}"
for entry in list_catalog_tables():
    if entry.get("qualifiedName") == qualified:
        print(f"Table: {qualified}")
        print(f"Rows: {entry.get('rowCount', 0)}")
        print(render_rows(entry.get("columns", []), columns=["name", "type"]))
        break
else:
    raise SystemExit(f"Table not found in catalog: {qualified}")
```

`tools/table_view.py`:

```python
import argparse

from app.services.file_import import preview_table
from tools._cli import parse_qualified_name, render_rows


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--limit", type=int, default=20)
args = parser.parse_args()

schema, table = parse_qualified_name(args.table)
preview = preview_table(schema, table, limit=args.limit)
print(render_rows(preview["rows"], columns=preview["columns"]))
```

`tools/table_export.py`:

```python
import argparse
from pathlib import Path

from app.services.file_import import export_table_csv
from app.services.workspace import workspace_paths
from tools._cli import parse_qualified_name


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--output")
args = parser.parse_args()

schema, table = parse_qualified_name(args.table)
file_name, csv_text = export_table_csv(schema, table)
output = Path(args.output).expanduser().resolve() if args.output else workspace_paths()["exports"] / file_name
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(csv_text, encoding="utf-8")
print(f"Exported {schema}.{table} to {output}")
```

- [ ] **Step 3: Run tests**

Run:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest tests/test_tools_cli.py -v
```

Expected: PASS.

---

## Task 3: File Import Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/file_inspect.py`
- Create: `kriyax-data-app/backend/tools/file_import.py`
- Test: `kriyax-data-app/backend/tests/test_tools_cli.py`

Scripts:

```bash
python tools/file_inspect.py /path/orders.csv --limit 20
python tools/file_inspect.py /path/orders.csv --json > /tmp/orders-inspection.json
python tools/file_import.py /path/orders.csv --schema raw_files --table orders --auto
python tools/file_import.py /path/orders.csv --schema raw_files --table orders --columns /tmp/orders-columns.json
```

Implementation notes:

- `file_inspect.py` calls `app.services.file_import.inspect_file()`.
- `file_import.py` calls `inspect_file()` first when `--auto` is used, then passes inferred columns into `commit_import()`.
- If `requiresRename` is true and no `--columns` file is provided, exit with a clear message telling the user to edit the JSON mapping.
- After import, `commit_import()` persists rows to DuckDB and writes catalog metadata automatically.

Test:

```python
def test_file_import_script_creates_catalog_entry(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("customer,amount\nAcme,12.5\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "tools/file_import.py",
            str(csv_path),
            "--schema",
            "raw_files",
            "--table",
            "orders",
            "--auto",
        ],
        cwd="/Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend",
        text=True,
        capture_output=True,
        check=True,
    )

    assert "raw_files.orders" in result.stdout
```

---

## Task 4: Script Workspace and Join/Transform Execution

**Files:**
- Create: `kriyax-data-app/backend/tools/script_create.py`
- Create: `kriyax-data-app/backend/tools/script_list.py`
- Create: `kriyax-data-app/backend/tools/script_show.py`
- Create: `kriyax-data-app/backend/tools/script_run.py`
- Test: `kriyax-data-app/backend/tests/test_tools_cli.py`

Scripts:

```bash
python tools/script_create.py revenue_by_region.py --template join
python tools/script_list.py
python tools/script_show.py revenue_by_region.py
python tools/script_run.py revenue_by_region.py
```

`script_create.py --template join` should create:

```python
orders = load_table("raw_files.orders")
customers = load_table("raw_files.customers")

joined = orders.merge(customers, on="customer_id", how="left")
result = joined.groupby("region", as_index=False)["amount"].sum()

show(result, name="region_revenue_preview")
save_table(result, "region_revenue", schema="curated")
```

`script_run.py` calls `app.services.execution.run_script(script_name=name, code=code)`.

Expected behavior:

- stdout/stderr prints in terminal.
- `displayFrames` prints when `show()` is used.
- `savedTables` prints when `save_table()` is used.
- Saved tables are queryable with `tools/table_view.py`.

Test:

```python
def test_script_run_saves_join_result(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    from app.services.workspace import ensure_workspace, workspace_paths

    ensure_workspace()
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw_files")
        conn.execute("create or replace table raw_files.orders as select 1 as customer_id, 10.0 as amount")
        conn.execute("create or replace table raw_files.customers as select 1 as customer_id, 'West' as region")

    script = workspace_paths()["scripts"] / "join_orders.py"
    script.write_text(
        'orders = load_table("raw_files.orders")\n'
        'customers = load_table("raw_files.customers")\n'
        'joined = orders.merge(customers, on="customer_id", how="left")\n'
        'result = joined.groupby("region", as_index=False)["amount"].sum()\n'
        'show(result, name="preview")\n'
        'save_table(result, "region_revenue", schema="curated")\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "tools/script_run.py", "join_orders.py"],
        cwd="/Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend",
        text=True,
        capture_output=True,
        check=True,
    )

    assert "curated.region_revenue" in result.stdout
```

---

## Task 5: Agent Code Generation and Correction Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/agent_generate.py`
- Create: `kriyax-data-app/backend/tools/agent_fix.py`
- Create: `kriyax-data-app/backend/tools/agent_follow_up.py`
- Create: `kriyax-data-app/backend/tools/llm_status.py`
- Create: `kriyax-data-app/backend/tools/llm_test.py`

Scripts:

```bash
python tools/llm_status.py
python tools/llm_test.py "Say ready"
python tools/agent_generate.py "join orders and customers and save revenue by region" --save revenue_by_region.py
python tools/script_run.py revenue_by_region.py
python tools/agent_fix.py --script revenue_by_region.py --traceback-file /tmp/traceback.txt --save
python tools/agent_follow_up.py --script revenue_by_region.py "filter to 2026 orders only" --save
```

Implementation notes:

- Use `app.services.agent.generate_code()`, `correct_code()`, and `follow_up()`.
- `--save` writes generated code into `workspace/scripts/<name>.py`.
- `agent_fix.py --run latest` can be added after a helper exists to locate the latest failed run JSON. Initial implementation can accept `--traceback-file`.
- Never auto-run generated or corrected code. The user/agent must call `script_run.py`.

---

## Task 6: Odoo Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/odoo_test_connection.py`
- Create: `kriyax-data-app/backend/tools/odoo_save_connection.py`
- Create: `kriyax-data-app/backend/tools/odoo_list_connections.py`
- Create: `kriyax-data-app/backend/tools/odoo_models.py`
- Create: `kriyax-data-app/backend/tools/odoo_fields.py`
- Create: `kriyax-data-app/backend/tools/odoo_fetch.py`
- Create: `kriyax-data-app/backend/tools/odoo_cursor_create.py`
- Create: `kriyax-data-app/backend/tools/odoo_sync.py`

Scripts:

```bash
python tools/odoo_test_connection.py --url https://example.odoo.com --database db --username user --api-key key
python tools/odoo_save_connection.py --name production --url https://example.odoo.com --database db --username user --api-key key
python tools/odoo_list_connections.py
python tools/odoo_models.py --connection production --search sale
python tools/odoo_fields.py --connection production --model sale.order
python tools/odoo_fetch.py --connection production --model sale.order --fields id,name,amount_total,write_date --schema odoo --table sale_order
python tools/odoo_cursor_create.py --connection production --model sale.order --fields id,name,amount_total,write_date --schema odoo --table sale_order --cursor-field write_date
python tools/odoo_sync.py <cursor-id>
```

Implementation notes:

- Reuse `app.services.odoo`.
- Resolve `--connection production` from `workspace/metadata/connections.json`.
- `odoo_fetch.py` persists records to DuckDB and catalog through the service.
- `odoo_sync.py` updates existing Odoo tables incrementally using cursor metadata.

---

## Task 7: Pipeline Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/pipeline_create.py`
- Create: `kriyax-data-app/backend/tools/pipeline_list.py`
- Create: `kriyax-data-app/backend/tools/pipeline_schedule.py`
- Create: `kriyax-data-app/backend/tools/pipeline_enable.py`
- Create: `kriyax-data-app/backend/tools/pipeline_run.py`
- Create: `kriyax-data-app/backend/tools/pipeline_runs.py`
- Create: `kriyax-data-app/backend/tools/pipeline_failures.py`
- Create: `kriyax-data-app/backend/tools/pipeline_ack_failure.py`
- Create: `kriyax-data-app/backend/tools/pipeline_process_due.py`

Scripts:

```bash
python tools/pipeline_create.py "Daily revenue refresh" --script revenue_by_region.py
python tools/pipeline_schedule.py <pipeline-id> --daily 06:00 --timezone Asia/Kolkata
python tools/pipeline_enable.py <pipeline-id> false
python tools/pipeline_run.py <pipeline-id>
python tools/pipeline_runs.py --pipeline <pipeline-id>
python tools/pipeline_failures.py
python tools/pipeline_ack_failure.py <run-id>
python tools/pipeline_process_due.py
```

Implementation notes:

- Use `app.services.pipelines`.
- Manual runs should work even if a pipeline is disabled.
- Failures are already persisted under `workspace/runs/` and `workspace/metadata/pipeline-failures.json`.
- `pipeline_process_due.py` is the barebones scheduler loop entry for cron/launchd/manual invocation.

---

## Task 8: Table Management Scripts

**Files:**
- Create: `kriyax-data-app/backend/tools/table_rename.py`
- Create: `kriyax-data-app/backend/tools/table_truncate.py`
- Create: `kriyax-data-app/backend/tools/table_drop.py`

Scripts:

```bash
python tools/table_rename.py curated.region_revenue curated.region_revenue_v2
python tools/table_truncate.py curated.region_revenue --confirm curated.region_revenue
python tools/table_drop.py curated.region_revenue --confirm curated.region_revenue
```

Implementation notes:

- Use `app.services.file_import.rename_table()`, `truncate_table()`, and `drop_table()`.
- Require exact `--confirm schema.table` for destructive actions.
- Print updated catalog result after success.

---

## Task 9: README and Agent Instructions

**Files:**
- Modify: `kriyax-data-app/README.md`
- Create: `kriyax-data-app/backend/AGENTS.md`

README must include:

```markdown
## Barebones Python Workbench

Run every product capability through scripts from `backend/tools`.

Tables are stored in `workspace/warehouse/kriyax.duckdb`.
Catalog metadata is stored in `workspace/metadata/catalog.json`.
User transformations are stored as real Python files in `workspace/scripts`.
Run output and tracebacks are stored in `workspace/runs`.

Common commands:

python tools/workspace_status.py
python tools/file_inspect.py ../sample.csv
python tools/file_import.py ../sample.csv --schema raw_files --table sample --auto
python tools/catalog_list.py
python tools/table_view.py raw_files.sample --limit 20
python tools/script_run.py clean_sample.py
python tools/table_export.py curated.clean_sample
```

AGENTS.md must tell Codex/Antigravity:

```markdown
# KriyaX Data Workbench Agent Instructions

- Work from `kriyax-data-app/backend`.
- Use `python tools/*.py` for product actions.
- Store transformation code in `../workspace/scripts/*.py`.
- Use `load_table("schema.table")`, `show(df, name="preview")`, and `save_table(df, "table", schema="curated")`.
- Do not edit `workspace/metadata/*.json` manually unless repairing metadata.
- After any import, fetch, or save, verify with `python tools/catalog_list.py` and `python tools/table_view.py schema.table`.
- Run `.venv/bin/python -m pytest` before claiming the script workbench is complete.
```

---

## Verification Plan

Run backend tests:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest
```

Manual no-UI scenario:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
python tools/workspace_status.py
python tools/file_inspect.py /tmp/orders.csv --json
python tools/file_import.py /tmp/orders.csv --schema raw_files --table orders --auto
python tools/catalog_list.py
python tools/table_view.py raw_files.orders --limit 10
python tools/script_create.py revenue_by_region.py --template join
python tools/script_run.py revenue_by_region.py
python tools/catalog_search.py revenue
python tools/table_view.py curated.region_revenue --limit 20
python tools/table_export.py curated.region_revenue
python tools/pipeline_create.py "Revenue refresh" --script revenue_by_region.py
python tools/pipeline_list.py
```

Success means:

- CSV rows are stored in DuckDB.
- Imported table appears in catalog.
- Script can load tables with `load_table()`.
- Join result can be previewed with `show()`.
- Join result can be persisted with `save_table()`.
- Persisted result appears as a new catalog table.
- Table can be viewed and exported from terminal.
- Pipeline can reference and run the saved script.

---

## Self-Review

Spec coverage:

- Data Connectors: covered by file and Odoo scripts.
- Schema & Catalog: covered by catalog and table scripts.
- Code Workspace: covered by real files in `workspace/scripts` and script run/list/show scripts.
- Agentic Layer: covered by agent generate/fix/follow-up scripts using existing LLM service.
- Pipeline & Scheduling: covered by pipeline scripts using existing pipeline service.
- Data Storage: covered by workspace status, DuckDB persistence, table management, and export scripts.

Known limitation:

- Saved Odoo connection edit/delete is only partially covered because current service exposes save/list, not explicit edit/delete. If exact edit/delete is required, add `app.services.odoo.update_connection()` and `delete_connection()` before wiring `odoo_edit_connection.py` and `odoo_delete_connection.py`.
