# KriyaX Script Workbench Implementation Plan

## Goal

Create a separate Python-script-first application that can perform the same core data-layer capabilities without requiring the React UI:

- file import
- Odoo import and sync
- catalog search and table preview
- Python/pandas transformations
- joined/derived table persistence
- agent code generation/fix flow
- pipelines and scheduled runs
- deterministic auditability

## Application Boundary

This is a new app under:

```text
kriyax-script-workbench/
```

It should not modify the existing React/FastAPI app except when deliberately porting proven logic.

## Phases

### Phase 1: Core Workspace, Storage, Audit, Script Runner

Status: implemented.

- workspace bootstrap
- DuckDB storage
- catalog metadata
- audit service
- script runner with `load_table()`, `save_table()`, `show()`
- table viewing utilities

Done when:

- a script can join two tables
- `save_table()` persists a derived table
- `table_view.py` can show saved rows
- `audit_tail.py` shows the exact script run
- code snapshot exists in `workspace/audit/snapshots/`

### Phase 2: File Import

Status: implemented.

- `file_inspect.py`
- `file_import.py`
- duplicate-column checks
- type inference
- catalog registration

### Phase 3: Agent Skill and Agent Utilities

Status: implemented.

- repo-local `agent-skill/SKILL.md`
- `agent_generate.py`
- `agent_fix.py`
- `agent_follow_up.py`
- deterministic audit records for generated code hashes

### Phase 4: Odoo Utilities

Status: implemented.

- connection test/save/list
- model browse
- fields browse
- fetch records to DuckDB
- cursor-based incremental sync

### Phase 5: Pipelines

Status: implemented.

- create pipeline from saved script
- manual run
- schedule metadata
- due-run processor
- failure list and acknowledgement

## Verification Status

Current automated coverage:

- script run joins two tables, saves a derived table, and writes audit evidence
- file import creates a DuckDB table and catalog entry
- file import preserves the original source file under `workspace/data/uploads`
- table search, preview, export, rename, truncate, and drop work through services
- table HTML export creates visual previews for agent-driven inspection
- DB viewer integration writes `workspace/metadata/db-viewer.json` and `tools/db_viewer_info.py` so DBCode can inspect the DuckDB database directly
- pipeline create, schedule, disable, manual run, run history, and failure tracking work
- agent code generation saves code and writes prompt/code hashes to audit without storing raw prompt text
- real LLM runtime can reuse the sibling `kriyax-data-app` encrypted LLM vault when no local environment key is set
- `tools/agent_context.py` creates a deterministic context pack for Codex/Antigravity without requiring the optional in-app LLM layer

Current verification commands:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-script-workbench
PYTHONPATH=src ../kriyax-data-app/backend/.venv/bin/python -m pytest tests -v
PYTHONPATH=src ../kriyax-data-app/backend/.venv/bin/python -m compileall src tools tests
```

## Non-Negotiables

- Script execution must always go through the workbench runner.
- Audit must be written by deterministic Python services.
- LLM output is never the system of record.
- Every table write must be traceable to a script, import, Odoo fetch, or pipeline run.
- Secrets must be redacted from audit logs.
