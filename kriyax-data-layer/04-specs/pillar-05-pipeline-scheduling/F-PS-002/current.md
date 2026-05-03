# Spec — F-PS-002: Schedule pipeline

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-05-pipeline-scheduling  
**Feature ref:** `03-features/pillar-05-pipeline-scheduling/current.md` → F-PS-002  
**Dependencies:** F-PS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Attach recurring schedule to a pipeline using simple presets and/or cron-style timing.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| pipeline_id | string | yes | — | existing pipeline |
| schedule_type | enum | yes | preset | hourly/daily/weekly/cron |
| cron_expression | string | conditional | — | valid if schedule_type=cron |
| timezone | string | no | local | valid timezone |

## States

### unscheduled
Observable user/system state for this feature.

### editing schedule
Observable user/system state for this feature.

### scheduled
Observable user/system state for this feature.

### error:invalid-cron
Error state with explicit message, recoverable by retry or input correction.

### error:scheduler-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Show next run time before save.
- Timezone must be explicit.
- Invalid cron cannot save.
- Disabled pipeline stores schedule but skips automatic runs.

## Side effects on success

- Creates/updates scheduler job.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Daily 6am schedule saves and shows next run.
- [ ] Cron schedule validates.
- [ ] Invalid cron shows error.
- [ ] Schedule persists across restart.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
