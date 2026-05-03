# Spec — F-DS-002: Auto-create tables on import

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-06-data-storage  
**Feature ref:** `03-features/pillar-06-data-storage/current.md` → F-DS-002  
**Dependencies:** F-DS-001, F-DC-003, F-DC-006

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Create physical database tables after connector preview/schema confirmation using new table names only.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| table_name | string | yes | — | unique, valid identifier |
| schema | array | yes | — | columns/types confirmed |
| rows | dataset | yes | — | parsed connector data |

## States

### ready
Successful/usable state with the expected data, controls, or result visible.

### creating
Observable user/system state for this feature.

### success
Successful/usable state with the expected data, controls, or result visible.

### error:name-conflict
Error state with explicit message, recoverable by retry or input correction.

### error:schema-invalid
Error state with explicit message, recoverable by retry or input correction.

### error:write-failed
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Connector imports do not overwrite existing tables.
- 0-row table with columns is allowed.
- Duplicate columns must already be resolved before this feature.
- Type conversion failures surface clear column-specific errors where possible.

## Side effects on success

- Creates database table.
- Triggers catalog registration.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] CSV import creates new table.
- [ ] Odoo fetch creates new table.
- [ ] Existing name is rejected.
- [ ] 0-row confirmed import creates empty table.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
