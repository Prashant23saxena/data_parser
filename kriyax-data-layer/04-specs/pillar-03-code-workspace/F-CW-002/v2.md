# Spec — F-CW-002: Show available tables

**Version:** v2  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-002  
**Dependencies:** F-SC-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Sidebar/panel listing catalog tables and useful metadata beside the editor.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| search_query | string | no | empty | matches table/column names |
| source_filter | enum | no | all | all/csv/odoo/derived/external |

## States

### loading tables
In-flight state with spinner/progress text and duplicate action prevention.

### table list loaded
Successful/usable state with the expected data, controls, or result visible.

### empty catalog
Observable user/system state for this feature.

### filtered no-results
Observable user/system state for this feature.

### error:catalog-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- 100+ tables require search and scroll.
- Refresh pulls latest catalog state.
- Clicking a table can insert load_table("table_name") into the editor.

## Side effects on success

- Reads Schema & Catalog only.
- May insert helper code into editor at cursor.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Catalog tables appear in editor sidebar.
- [ ] Search by table name works.
- [ ] Click table inserts load_table helper.
- [ ] Empty catalog message points user to connectors.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
