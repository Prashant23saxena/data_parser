# Spec — F-DS-003: Persist derived tables

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-06-data-storage  
**Feature ref:** `03-features/pillar-06-data-storage/current.md` → F-DS-003  
**Dependencies:** F-DS-001, F-CW-004

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Persist DataFrames produced in Code Workspace as derived database tables, with catalog update.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| df | pandas.DataFrame | yes | — | valid DataFrame |
| table_name | string | yes | — | valid identifier |
| mode | enum | no | replace | replace if approved by F-CW-004 |

## States

### validating
Observable user/system state for this feature.

### writing
Observable user/system state for this feature.

### success:create
Successful/usable state with the expected data, controls, or result visible.

### success:replace
Successful/usable state with the expected data, controls, or result visible.

### error:invalid-dataframe
Error state with explicit message, recoverable by retry or input correction.

### error:write-failed
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

- Derived table replace is separate from connector import behavior.
- Rollback previous table where supported if replace fails.
- Catalog sync failure is surfaced but table can remain saved.

## Side effects on success

- Creates/replaces derived table.
- Triggers catalog registration/update.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Save derived DataFrame creates table.
- [ ] Replace derived table updates rows/schema.
- [ ] Failure does not corrupt old table.
- [ ] Catalog reflects derived source.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
