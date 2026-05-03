# Spec — F-DS-005: Export table data

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-06-data-storage  
**Feature ref:** `03-features/pillar-06-data-storage/current.md` → F-DS-005  
**Dependencies:** F-DS-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Export any table as CSV for sharing, backup, or downstream manual use.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| table_name | string | yes | — | existing table |
| format | enum | no | csv | csv only in v1 |

## States

### ready
Successful/usable state with the expected data, controls, or result visible.

### exporting
Observable user/system state for this feature.

### download-ready
Successful/usable state with the expected data, controls, or result visible.

### error:table-not-found
Error state with explicit message, recoverable by retry or input correction.

### error:export-failed
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Large exports stream/chunk rather than loading all into memory.
- 0-row table exports headers.
- File name uses table name plus timestamp.

## Side effects on success

- Reads table data.
- Creates downloadable file/stream.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Export small table downloads CSV.
- [ ] Export 0-row table downloads headers.
- [ ] Export large table completes without memory crash.
- [ ] Missing table shows error.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
