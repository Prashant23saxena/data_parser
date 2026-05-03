# Spec — F-AL-001: Chat interface

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-001  
**Dependencies:** none

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Chat panel where the user asks for Python/pandas transformations in natural language and receives agent responses.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| message | string | yes | — | non-empty |
| chat_id | string | no | current/new | valid existing chat if provided |

## States

### empty chat
Observable user/system state for this feature.

### composing
Observable user/system state for this feature.

### sending
Observable user/system state for this feature.

### agent thinking
Observable user/system state for this feature.

### response ready
Successful/usable state with the expected data, controls, or result visible.

### error:llm-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Disable send on empty message.
- Preserve chat history within session.
- Show model/provider error without losing user input.
- Do not auto-run code from chat.

## Side effects on success

- Creates chat messages.
- Feeds later code generation workflow.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Send a plain-English request.
- [ ] See agent response in history.
- [ ] LLM error is recoverable.
- [ ] Starting new chat clears context.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
