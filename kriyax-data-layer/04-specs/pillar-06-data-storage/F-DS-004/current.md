# Spec — F-DS-004: Basic table management

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-06-data-storage  
**Feature ref:** `03-features/pillar-06-data-storage/current.md` → F-DS-004  
**Dependencies:** F-DS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

UI operations for drop, truncate, and rename tables with strong confirmation for destructive actions.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| table_name | string | yes | — | existing table |
| operation | enum | yes | — | drop/truncate/rename |
| new_name | string | conditional | — | required for rename |

## States

### table selected
Observable user/system state for this feature.

### confirm destructive
Observable user/system state for this feature.

### processing
In-flight state with spinner/progress text and duplicate action prevention.

### success
Successful/usable state with the expected data, controls, or result visible.

### error:operation-failed
Error state with explicit message, recoverable by retry or input correction.

### error:dependency-warning
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Drop/truncate require typed confirmation or strong modal.
- Rename validates uniqueness.
- Protected internal metadata tables cannot be modified.
- Pipelines/scripts referencing a table should warn before destructive action.

## Side effects on success

- Mutates database table.
- Updates catalog metadata.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Rename table updates catalog.
- [ ] Truncate clears rows keeps schema.
- [ ] Drop removes table after confirmation.
- [ ] Protected tables cannot be dropped.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
