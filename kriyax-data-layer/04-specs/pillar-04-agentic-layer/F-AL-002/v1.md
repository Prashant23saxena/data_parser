# Spec — F-AL-002: Schema-aware context loading

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-04-agentic-layer  
**Feature ref:** `03-features/pillar-04-agentic-layer/current.md` → F-AL-002  
**Dependencies:** F-SC-001, F-SC-002

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Load current table and column metadata into the agent prompt so generated code references real tables and columns.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| request_text | string | yes | — | current user request |
| max_tables | int | no | relevance-based | bounded for prompt size |

## States

### collecting metadata
Observable user/system state for this feature.

### context built
Observable user/system state for this feature.

### context too large
Observable user/system state for this feature.

### error:catalog-unavailable
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- Large catalogs require relevance selection and summaries.
- Missing table names trigger clarification instead of guessing.
- Metadata refreshed per request or explicit refresh.
- Sample row context remains gated by F-SC-005 policy.

## Side effects on success

- Builds agent prompt context.
- No database mutation.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] Prompt context includes table names and columns.
- [ ] Unavailable catalog returns clear error.
- [ ] Large catalog is summarized without exceeding limits.
- [ ] Agent avoids hallucinated table names.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
