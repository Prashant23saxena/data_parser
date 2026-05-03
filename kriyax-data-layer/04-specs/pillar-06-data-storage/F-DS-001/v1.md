# Spec — F-DS-001: Backing database setup

**Version:** v1  
**Status:** FROZEN  
**Last updated:** 2026-05-02  
**Pillar:** pillar-06-data-storage  
**Feature ref:** `03-features/pillar-06-data-storage/current.md` → F-DS-001  
**Dependencies:** none

## Research anchors

- Odoo External API docs: search_read supports fields and domains; fields_get exposes model field metadata.
- pandas I/O docs: DataFrame-oriented read/write flows and CSV handling patterns.
- DuckDB Python docs: Python client integrates with pandas DataFrames and table storage.
- APScheduler docs: cron and interval triggers support recurring scheduled execution.

## Summary

Provision and configure the single backing database used by connectors, catalog, code workspace, pipelines, and storage features.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| db_type | enum | yes | duckdb or postgres | approved supported value |
| database_path_or_url | string | yes | project default | valid local path or connection URL |

## States

### not configured
Observable user/system state for this feature.

### checking
Observable user/system state for this feature.

### ready
Successful/usable state with the expected data, controls, or result visible.

### error:connection
Error state with explicit message, recoverable by retry or input correction.

### error:migration
Error state with explicit message, recoverable by retry or input correction.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| initial/ready | processing/loading | user starts the feature action | request or local operation begins |
| processing/loading | success/loaded | operation completes | result is displayed or persisted as defined |
| processing/loading | error state | validation/backend/external service failure | no partial user-visible success is claimed |
| error state | initial/ready | user fixes input or retries | prior error is cleared or preserved in history |

## Edge cases

- DuckDB is simplest local default; Postgres remains option if multi-process/server needs demand it.
- Database must be available whenever app is running.
- Schema migrations are idempotent.

## Side effects on success

- Creates metadata tables.
- Provides shared connection service.

## Failure recovery

Validation failures stop before mutation. External/API/database failures surface a clear error, preserve user input/configuration where practical, and allow retry. Mutating operations must either complete fully or report exactly what did and did not change.

## Acceptance checklist

- [ ] App starts with DB ready.
- [ ] Catalog can read metadata.
- [ ] Connector can create table.
- [ ] Failure shows actionable setup error.

## Notes for validation

Approved in one-pass validation and frozen for L5 screen planning.

---
*Frozen on: 2026-05-02*
