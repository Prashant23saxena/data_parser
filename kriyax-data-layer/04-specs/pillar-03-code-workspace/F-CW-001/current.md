# Spec — F-CW-001: Python code editor

**Version:** v2  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-001  
**Dependencies:** none

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Single-file Python/pandas editor with syntax highlighting, line numbers, Run action, and sandboxed execution context.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| code | string | yes | empty | valid Python checked on run |
| timeout_seconds | int | no | 60 | 5-300 |

## States

### empty
Observable user/system state for this feature.

### editing
Observable user/system state for this feature.

### dirty/unsaved
Successful/usable state with the expected data, controls, or result visible.

### running
In-flight state with spinner/progress text and duplicate action prevention.

### completed
Observable user/system state for this feature.

### error:syntax
Error state with explicit message, recoverable by retry or input correction.

### error:runtime
Error state with explicit message, recoverable by retry or input correction.

### error:timeout
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Run disabled for empty code.
- Editor becomes read-only during execution to avoid racing state.
- Syntax errors are reported in output without losing code.
- Long-running scripts are killed at timeout.
- Only approved packages are available in the sandbox.

## Side effects on success

- Creates an execution request.
- Output is shown via F-CW-005.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Write pandas code and run it successfully.
- [ ] Syntax error shows line-linked traceback.
- [ ] Infinite loop times out and returns control.
- [ ] Code remains in editor after failure.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
