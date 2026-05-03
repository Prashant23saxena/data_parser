# Spec — F-CW-004: Save DataFrame as table

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-004  
**Dependencies:** F-CW-003, F-DS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Helper function save_table(df, "name") persists a pandas DataFrame as a derived table in the backing database.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| df | pandas.DataFrame | yes | — | must be DataFrame with at least one column |
| table_name | string | yes | — | lowercase letters/numbers/underscores, starts with letter |
| mode | enum | no | replace | replace only unless later changed |

## States

### ready
Successful/usable state with the expected data, controls, or result visible.

### validating
Observable user/system state for this feature.

### saving
In-flight state with spinner/progress text and duplicate action prevention.

### success:create
Successful/usable state with the expected data, controls, or result visible.

### success:replace
Successful/usable state with the expected data, controls, or result visible.

### error:invalid-dataframe
Error state with explicit message, recoverable by retry or input correction.

### error:invalid-table-name
Error state with explicit message, recoverable by retry or input correction.

### error:db-write
Error state with explicit message, recoverable by retry or input correction.

### error:catalog-sync
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Empty DataFrame with columns creates 0-row table.
- Duplicate columns are rejected.
- Unsupported nested object columns are rejected with offending column where possible.
- Catalog sync failure does not roll back successful DB write.

## Side effects on success

- Creates/replaces derived table.
- Triggers catalog registration.
- Makes table available to load_table and table list.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Save valid DataFrame creates table.
- [ ] Save same name replaces derived table if mode stays approved.
- [ ] Invalid table name fails before DB write.
- [ ] Catalog updates after save.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
