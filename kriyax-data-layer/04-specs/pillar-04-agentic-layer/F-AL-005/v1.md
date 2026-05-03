# Spec — F-AL-005: Self-correction on error

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-005  
**Dependencies:** F-AL-003, F-CW-005

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

When generated code fails, send code, traceback, and relevant schema context back to the agent to propose a corrected version under user control.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| failed_code | string | yes | — | code that ran |
| traceback | string | yes | — | execution error |
| schema_context | object | yes | fresh | current metadata |

## States

### error captured
Error state with explicit message, recoverable by retry or input correction.

### analyzing
Observable user/system state for this feature.

### fix proposed
Observable user/system state for this feature.

### needs user approval
Observable user/system state for this feature.

### error:fix-failed
Error state with explicit message, recoverable by retry or input correction.

### max-attempts-reached
Observable user/system state for this feature.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Limit automatic correction attempts, recommended max 2 before asking user.
- Fix proposal never auto-runs.
- Tracebacks are included; secrets are redacted.
- If error indicates missing table/column, refresh schema context.

## Side effects on success

- Creates corrected code candidate.
- May append agent explanation.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] KeyError triggers corrected column reference or clarification.
- [ ] Syntax error returns valid corrected code.
- [ ] Second failed fix stops with clear message.
- [ ] User must approve insert/run.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
