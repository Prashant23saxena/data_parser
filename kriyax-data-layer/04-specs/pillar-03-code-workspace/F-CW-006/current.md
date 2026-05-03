# Spec — F-CW-006: Save & re-run scripts

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-006  
**Dependencies:** F-CW-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Save Python scripts with names so users can reopen, edit, manually re-run, and attach them to pipelines.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| script_name | string | yes | — | unique, 1-80 chars |
| code | string | yes | current editor | non-empty |
| description | string | no | empty | optional notes |

## States

### unsaved
Successful/usable state with the expected data, controls, or result visible.

### saving
In-flight state with spinner/progress text and duplicate action prevention.

### saved
Successful/usable state with the expected data, controls, or result visible.

### script list
Observable user/system state for this feature.

### loading script
In-flight state with spinner/progress text and duplicate action prevention.

### error:name-conflict
Error state with explicit message, recoverable by retry or input correction.

### error:save-failed
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Renaming existing script requires unique name.
- Saved script persists across sessions.
- Manual re-run uses current saved content.
- Pipeline references stable script id, not just name.

## Side effects on success

- Creates/updates saved script record.
- Enables Pipeline & Scheduling.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Save current code as named script.
- [ ] Open saved script into editor.
- [ ] Re-run saved script manually.
- [ ] Saved script appears as pipeline candidate.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
