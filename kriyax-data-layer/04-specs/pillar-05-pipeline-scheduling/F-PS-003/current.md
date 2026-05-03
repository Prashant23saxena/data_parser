# Spec — F-PS-003: Manual trigger

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-05-pipeline-scheduling  
**Feature ref:** `03-features/pillar-05-pipeline-scheduling/current.md` → F-PS-003  
**Dependencies:** F-PS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Run any pipeline immediately on demand for testing or one-off refresh.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| pipeline_id | string | yes | — | existing pipeline |

## States

### ready
Successful/usable state with the expected data, controls, or result visible.

### queued
Observable user/system state for this feature.

### running
In-flight state with spinner/progress text and duplicate action prevention.

### success
Successful/usable state with the expected data, controls, or result visible.

### failed
Observable user/system state for this feature.

### blocked:already-running
Successful/usable state with the expected data, controls, or result visible.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Manual run allowed even if schedule disabled.
- Prevent duplicate concurrent runs for same pipeline.
- Run appears in history.

## Side effects on success

- Creates run record.
- Executes connector pre-step and script.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Click Run now executes pipeline.
- [ ] Disabled scheduled pipeline can still run manually.
- [ ] Concurrent run is blocked.
- [ ] Run history updates.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
