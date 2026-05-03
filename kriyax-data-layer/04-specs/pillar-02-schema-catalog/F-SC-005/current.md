# Spec — F-SC-005: Preview table rows

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-02-schema-catalog  
**Feature ref:** `03-features/pillar-02-schema-catalog/current.md` → F-SC-005  
**Dependencies:** F-SC-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Read-only preview of a small sample of rows for any catalog table so users can inspect real values before writing Python/pandas transformations.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| table_name | string | yes | — | must exist in table registry |
| row_limit | int | no | 50 | 10-200 |
| offset | int | no | 0 | >= 0 for paging |

## States

### loading preview data
In-flight state with spinner/progress text and duplicate action prevention.

### preview loaded
Successful/usable state with the expected data, controls, or result visible.

### empty table
Observable user/system state for this feature.

### error:table-not-found
Error state with explicit message, recoverable by retry or input correction.

### error:preview-failed
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Very wide tables use horizontal scroll and sticky first column where practical.
- Binary/blob columns show a placeholder rather than raw bytes.
- Large text values are truncated in cells with expand-on-click later if needed.
- Preview is read-only; no edits from this surface.

## Side effects on success

- No data mutation.
- Supports Code Workspace table selection.
- May later provide safe sample rows to agent context if approved.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Open an ingested CSV table and see first 50 rows.
- [ ] Open a derived table and see first 50 rows.
- [ ] Open a 0-row table and see an empty-table message with headers.
- [ ] Preview a wide table without layout breakage.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
