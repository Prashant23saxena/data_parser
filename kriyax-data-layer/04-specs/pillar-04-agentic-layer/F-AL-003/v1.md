# Spec — F-AL-003: Generate Python/pandas code

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-003  
**Dependencies:** F-AL-001, F-AL-002, F-CW-003, F-CW-004

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Generate runnable Python/pandas code using load_table() and save_table() helpers from a natural-language data request.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| user_request | string | yes | — | clear data intent |
| schema_context | object | yes | — | from F-AL-002 |

## States

### drafting
Observable user/system state for this feature.

### code generated
Observable user/system state for this feature.

### needs clarification
Observable user/system state for this feature.

### error:generation-failed
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Ambiguous requests produce a clarification question.
- Generated code must not include secrets or raw DB credentials.
- No SQL generation in v1.
- Persisting results is suggested but not automatic unless user asked.

## Side effects on success

- Creates code response.
- Can feed Insert code into editor.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Request for join produces pandas merge code.
- [ ] Request for cleaning produces pandas transformation code.
- [ ] Unknown column asks clarification.
- [ ] Generated code uses load_table/save_table helpers.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
