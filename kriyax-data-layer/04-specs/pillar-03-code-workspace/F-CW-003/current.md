# Spec — F-CW-003: Load tables as DataFrames

**Version:** v2  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-003  
**Dependencies:** F-CW-001, F-DS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Helper function load_table("name") returns a pandas DataFrame from the backing database with no user-managed credentials.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| table_name | string | yes | — | must exist in catalog/backing DB |
| columns | array[string] | no | all | must be valid columns if provided |
| limit | int | no | none | positive integer if provided |

## States

### ready
Successful/usable state with the expected data, controls, or result visible.

### loading
In-flight state with spinner/progress text and duplicate action prevention.

### success
Successful/usable state with the expected data, controls, or result visible.

### error:table-not-found
Error state with explicit message, recoverable by retry or input correction.

### error:column-not-found
Error state with explicit message, recoverable by retry or input correction.

### error:db-connection
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- 0-row table returns empty DataFrame with columns.
- Very large tables warn when loading all rows.
- Column names with spaces are still accessible through DataFrame bracket syntax.

## Side effects on success

- Reads database only.
- May emit output warning for large loads.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] load_table on existing table returns DataFrame.
- [ ] Missing table returns clear error with available tables.
- [ ] Optional column subset loads only those columns.
- [ ] 0-row table returns columns.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
