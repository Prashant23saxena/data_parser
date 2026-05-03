# Spec — F-PS-005: Error notifications

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-05-pipeline-scheduling  
**Feature ref:** `03-features/pillar-05-pipeline-scheduling/current.md` → F-PS-005  
**Dependencies:** F-PS-004

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Surface failed scheduled pipeline runs clearly in the UI through badges, alerts, and failure indicators.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| run_status | internal | yes | — | from run history |
| acknowledged | boolean | no | false | user acknowledgement |

## States

### no failures
Observable user/system state for this feature.

### failure badge
Observable user/system state for this feature.

### failure detail
Observable user/system state for this feature.

### acknowledged
Observable user/system state for this feature.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- UI notification only in v1; no email/Slack.
- Acknowledging does not delete run history.
- New failure reopens badge.

## Side effects on success

- Updates notification/ack state.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Failed scheduled run shows badge.
- [ ] Opening detail shows error.
- [ ] Acknowledge hides active alert but keeps history.
- [ ] New failure returns alert.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
