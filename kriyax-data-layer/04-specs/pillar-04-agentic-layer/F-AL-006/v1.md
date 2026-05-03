# Spec — F-AL-006: Conversational follow-ups

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-006  
**Dependencies:** F-AL-001, F-AL-003

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Support follow-up requests that modify prior generated code or intent within the same chat/session.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| followup_message | string | yes | — | non-empty |
| prior_context | object | yes | current chat | previous request/code/result |

## States

### context available
Observable user/system state for this feature.

### generating revision
Observable user/system state for this feature.

### revised code ready
Successful/usable state with the expected data, controls, or result visible.

### context missing
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

- New chat resets context.
- Follow-up should preserve prior code unless user asks to start over.
- If previous code was edited manually, user may need to include latest editor content.

## Side effects on success

- Creates revised code response.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Follow-up filter modifies previous code.
- [ ] Follow-up aggregation builds on prior load_table calls.
- [ ] Context reset starts fresh.
- [ ] Ambiguous follow-up asks clarification.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
