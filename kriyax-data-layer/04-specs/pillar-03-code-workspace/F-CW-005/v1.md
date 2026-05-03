# Spec — F-CW-005: View execution output

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-03-code-workspace  
**Feature ref:** `03-features/pillar-03-code-workspace/current.md` → F-CW-005  
**Dependencies:** F-CW-001

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Output panel for stdout, stderr, tracebacks, run status, duration, and DataFrame previews from Python execution.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| run_id | string | yes | — | must match execution run |
| output_stream | internal | yes | — | stdout/stderr/results/errors |

## States

### empty
Observable user/system state for this feature.

### running stream
In-flight state with spinner/progress text and duplicate action prevention.

### success output
Successful/usable state with the expected data, controls, or result visible.

### error output
Error state with explicit message, recoverable by retry or input correction.

### truncated output
Observable user/system state for this feature.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Large output truncates with explicit message and retained downloadable log later if needed.
- DataFrame result preview shows head rows and shape.
- Tracebacks preserve line numbers.
- Re-run clears old output only after new run starts.

## Side effects on success

- Stores recent run output for self-correction and run history.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] print output appears.
- [ ] DataFrame preview appears with shape.
- [ ] Runtime traceback appears clearly.
- [ ] Large output is truncated safely.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
