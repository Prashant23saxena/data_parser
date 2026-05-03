# Feature Availability Audit v1

**Date:** 2026-05-03
**Scope:** Frozen SPS feature set plus the new LLM provider setup requirement.
**Reference visuals:**
- `visuals/sleek-ui-reference-board.png`
- `visuals/sleek-catalog-agent-reference.png`
- `visuals/current-ui-screenshots/`

## Summary

The current build covers the main local data-layer loop: file import, catalog registration, Python execution, saved scripts, Odoo fetch, pipelines, table management/export, storage status, and deterministic agent code generation. The latest pass added a more professional shell treatment, catalog filtering, improved Code Workspace table picking, live Home metrics, and Fernet-encrypted OpenAI/Anthropic LLM provider setup under Storage.

## Available Now

| Feature | Status | Evidence |
|---|---|---|
| F-DC-001 Upload CSV/Excel | Available | File Import accepts CSV/XLSX and uploads to backend. |
| F-DC-002 Auto-detect columns | Available | Import inspection infers column names/types. |
| F-DC-003 Preview before import | Available | Preview rows render before table creation. |
| F-DC-004 Configure Odoo connection | Available | Odoo workspace tests and saves connection payloads. |
| F-DC-005 Browse Odoo models | Available | Model search/load and field browse are wired. |
| F-DC-006 Fetch Odoo records | Available | Selected fields fetch into DuckDB and catalog. |
| F-DC-007 Incremental/delta sync | Partial | Backend sync cursor/upsert and pipeline pre-step exist; UI selection/management is still thin. |
| F-DC-008 Manage saved connections | Partial | Connections are saved; list/edit/delete UI is not first-class yet. |
| F-SC-001 Table registry | Available | Catalog lists registered tables. |
| F-SC-002 Column metadata viewer | Available | Table detail and inline catalog expansion show columns. |
| F-SC-003 Auto-register on ingest | Available | File/Odoo/Python writes register catalog entries. |
| F-SC-004 Browse & search catalog | Available | Catalog now has search and schema filter. |
| F-SC-005 Preview table rows | Available | Table detail preview endpoint/UI are wired. |
| F-CW-001 Python code editor | Available | Editor saves/runs local Python scripts. |
| F-CW-002 Show available tables | Available | Code Workspace has a table picker list. |
| F-CW-003 Load tables as DataFrames | Available | `load_table()` helper and insert-load actions exist. |
| F-CW-004 Save DataFrame as table | Available | `save_table()` persists derived DuckDB tables. |
| F-CW-005 View execution output | Available | Run Output shows stdout/stderr/return code. |
| F-CW-006 Save & re-run scripts | Available | Saved Scripts opens scripts back into Code Workspace. |
| F-AL-001 Chat interface | Partial | Docked prompt/follow-up panel exists; persistent conversational thread is not built. |
| F-AL-002 Schema-aware context | Available | Agent backend reads catalog context for generated code. |
| F-AL-003 Generate Python code | Available | Agent generate endpoint/UI returns Python. |
| F-AL-004 Insert code into editor | Available | Generated code inserts into Code Workspace. |
| F-AL-005 Self-correction on error | Available | Correction endpoint/UI accepts traceback and code. |
| F-AL-006 Conversational follow-ups | Partial | Follow-up action exists, but not persistent multi-turn chat history. |
| F-PS-001 Create pipeline | Available | Pipeline create UI/API exist. |
| F-PS-002 Schedule pipeline | Available | Hourly/daily/weekly/cron scheduling exists. |
| F-PS-003 Manual trigger | Available | Run-now action exists. |
| F-PS-004 Run history & status | Available | Run history and run detail exist. |
| F-PS-005 Error notifications | Available | Active failures and acknowledge flow exist. |
| F-PS-006 Enable/disable pipeline | Available | Toggle action exists. |
| F-DS-001 Backing database setup | Available | Workspace bootstrap creates DuckDB storage. |
| F-DS-002 Auto-create tables on import | Available | Import and Odoo fetch create tables. |
| F-DS-003 Persist derived tables | Available | Python saved tables persist. |
| F-DS-004 Basic table management | Available | Rename/truncate/drop exist. |
| F-DS-005 Export table data | Available | CSV export endpoint/UI preview exists. |
| New: OpenAI/Anthropic key setup | Available | Storage has encrypted local provider setup and `/api/llm` settings endpoints. |

## Missing Or Thin Items

1. **Odoo saved connection manager**
   - Need a saved connection list with masked status, edit, delete, and use-for-browse actions.
   - Existing backend storage can be extended instead of replaced.

2. **Odoo sync cursor UI**
   - Need a visible sync cursor list and a pipeline selector for saved cursor IDs.
   - This completes the gap between backend delta sync and user-facing scheduling.

3. **Real LLM gateway**
   - OpenAI/Anthropic keys can now be saved encrypted.
   - The Agent still uses deterministic code generation until the provider gateway is wired into `app/services/agent.py`.

4. **Persistent agent conversation**
   - Current Agent supports generate/follow-up/correct actions.
   - It does not yet preserve a named conversation thread across restarts.

5. **Edge UAT completion**
   - UAT-010 empty workspace, UAT-011 large-ish local data, and UAT-012 local-only privacy defaults remain open in `08-architecture/checklist.md`.

## Implementation Plan

### Phase 1 — Finish LLM Runtime Wiring

- Add `app/services/llm_gateway.py` to load the active encrypted provider profile and call OpenAI/Anthropic through a single internal interface.
- Update `app/services/agent.py` so generate/follow-up/correct use the real provider when a key is saved, with deterministic fallback when no key is configured.
- Add backend tests that monkeypatch the gateway client and prove no raw keys appear in API responses or logs.
- Add UI status in the Agent dock: deterministic fallback vs active provider.

### Phase 2 — Odoo Connection Manager

- Add list/update/delete connection endpoints if the current Odoo service does not expose them fully.
- Update S-04 Odoo Import Workspace with saved connection cards and one-click load.
- Add masked-key handling so saved Odoo keys are never echoed raw.

### Phase 3 — Sync Cursor Selection

- Add Sync Cursor panel in Odoo workspace for cursor field, target table, last cursor value, and manual sync.
- Replace free-text `connectorSyncId` in Pipeline create with a dropdown of saved sync cursors.
- Add Playwright coverage for Odoo sync cursor -> pipeline pre-step selection.

### Phase 4 — UAT Hardening

- Run empty workspace and large-ish catalog scenarios.
- Add privacy verification for local storage paths and encrypted vault files.
- Update `08-architecture/checklist.md` when UAT-010 through UAT-012 pass.
