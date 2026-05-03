# Spec — F-PS-004: Run history & status

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-05-pipeline-scheduling  
**Feature ref:** `03-features/pillar-05-pipeline-scheduling/current.md` → F-PS-004  
**Dependencies:** F-PS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Show pipeline runs with start/end time, duration, status, logs, and error details.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| pipeline_id | string | yes | — | existing pipeline |
| status_filter | enum | no | all | all/success/failure/running |

## States

### loading history
In-flight state with spinner/progress text and duplicate action prevention.

### history list
Observable user/system state for this feature.

### run detail
Observable user/system state for this feature.

### empty history
Observable user/system state for this feature.

### error:history-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Newest runs first.
- Failed run shows traceback/log.
- Running run updates status.
- Long history paginated.

## Side effects on success

- Reads run records/logs.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Manual run appears in history.
- [ ] Failed run shows error.
- [ ] Running status updates to success/failure.
- [ ] History persists across sessions.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
