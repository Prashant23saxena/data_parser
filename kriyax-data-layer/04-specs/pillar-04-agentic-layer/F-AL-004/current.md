# Spec — F-AL-004: Insert code into editor

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-004  
**Dependencies:** F-AL-003, F-CW-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Let user insert generated code into the Python editor with one explicit click for review and execution.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| generated_code | string | yes | — | from agent response |
| insert_mode | enum | no | replace | replace/append at cursor if later enabled |

## States

### code available
Observable user/system state for this feature.

### inserting
Observable user/system state for this feature.

### inserted
Observable user/system state for this feature.

### error:editor-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Never auto-execute inserted code.
- If editor has unsaved edits, confirm replace/append behavior.
- Preserve generated code block formatting.

## Side effects on success

- Updates editor content.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Insert generated code into empty editor.
- [ ] Warn before replacing unsaved editor content.
- [ ] Inserted code remains editable.
- [ ] Run still requires user click.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
