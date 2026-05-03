# Work Packages Index

**Version:** v1
**Status:** FROZEN
**Last updated:** 2026-05-03
**Scope:** remaining implementation only; Phase 1, Phase 2, and initial Phase 3 are baseline.

Total: 11 packages across 6 remaining streams.

## Stream B: Pipeline Scheduling and Failures

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-B01 | Pipeline schedule model and API | PENDING | M | existing pipeline service | C-007 |
| WP-B02 | Scheduler restore and automatic execution | PENDING | M | WP-B01 | C-007 |
| WP-B03 | Failure notifications and run filtering | PENDING | M | existing run history | C-007 |

## Stream C: Odoo Incremental Sync and Pre-Step

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-C01 | Odoo sync cursor and incremental upsert | PENDING | L | existing Odoo full fetch | C-006 |
| WP-C02 | Pipeline Odoo pre-step orchestration | PENDING | M | WP-C01, existing pipeline run | C-006, C-007 |

## Stream D: Storage Management and Export

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-D01 | Table rename, truncate, drop | PENDING | M | existing DuckDB/catalog | C-002, C-003 |
| WP-D02 | CSV table export | PENDING | S | existing DuckDB/catalog | C-002 |

## Stream E: Agentic Layer

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-E01 | Agent backend generate/correct API | PENDING | L | catalog + execution baseline | C-003, C-005, C-008 |
| WP-E02 | Agent panel frontend and editor insert | PENDING | M | frontend code workspace | C-008 |

## Stream F: Frontend Integration

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-F01 | Home, pipeline, connector, catalog UI polish | PENDING | M | frontend baseline | C-002, C-003, C-006, C-007 |

## Stream G: Integration and Regression

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-G01 | Contract, integration, Playwright regression pass | PENDING | L | B/C/D/E/F stream outputs | all contracts |

## Critical Path

WP-B01 -> WP-B02 -> WP-C01 -> WP-C02 -> WP-F01 -> WP-G01.

## Coverage Check

- Every frozen L8.3 contract has a producer-side WP or existing baseline.
- Every remaining L8.2 component depth gap has at least one WP.
- Every unbuilt feature group from the activity log is covered.
- Existing completed slices are treated as dependencies, not rework packages.
