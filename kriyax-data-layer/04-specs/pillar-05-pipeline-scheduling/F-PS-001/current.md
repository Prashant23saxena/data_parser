# Spec — F-PS-001: Create pipeline

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-05-pipeline-scheduling  
**Feature ref:** `03-features/pillar-05-pipeline-scheduling/current.md` → F-PS-001  
**Dependencies:** F-CW-006

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Create a named pipeline from a saved Python script, optionally with a connector sync pre-step.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| pipeline_name | string | yes | — | unique, 1-80 chars |
| script_id | string | yes | — | saved script exists |
| connector_sync_id | string | no | none | saved connector/sync config if provided |

## States

### form empty
Observable user/system state for this feature.

### configuring
Observable user/system state for this feature.

### validating
Observable user/system state for this feature.

### saved
Successful/usable state with the expected data, controls, or result visible.

### error:name-conflict
Error state with explicit message, recoverable by retry or input correction.

### error:invalid-step
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Script is required.
- Connector pre-step is optional.
- Pipeline stores references to script/connection ids.
- No schedule required at creation.

## Side effects on success

- Creates pipeline definition.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Create pipeline with script only.
- [ ] Create pipeline with Odoo sync pre-step.
- [ ] Duplicate name rejected.
- [ ] Pipeline appears in list.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
