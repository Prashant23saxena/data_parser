# Build Checklist — KriyaX Data Layer

**Generated:** 2026-05-03
**Source of truth for status:** `00-meta/agent-claims.md` latest line per WP wins.

## Summary

- Work packages total: 11
- WPs complete: 11 / 11
- Streams: 6 remaining streams
- Critical path: WP-B01 -> WP-B02 -> WP-C01 -> WP-C02 -> WP-F01 -> WP-G01
- Integration scenarios: 8
- Critical UAT scenarios: 7

## Stream B: Pipeline Scheduling and Failures

- [x] WP-B01: Pipeline schedule model and API — DONE
- [x] WP-B02: Scheduler restore and automatic execution — DONE
- [x] WP-B03: Failure notifications and run filtering — DONE

## Stream C: Odoo Incremental Sync and Pre-Step

- [x] WP-C01: Odoo sync cursor and incremental upsert — DONE
- [x] WP-C02: Pipeline Odoo pre-step orchestration — DONE

## Stream D: Storage Management and Export

- [x] WP-D01: Table rename, truncate, drop — DONE
- [x] WP-D02: CSV table export — DONE

## Stream E: Agentic Layer

- [x] WP-E01: Agent backend generate/correct API — DONE
- [x] WP-E02: Agent panel frontend and editor insert — DONE

## Stream F: Frontend Integration

- [x] WP-F01: Home, pipeline, connector, catalog UI polish — DONE

## Stream G: Integration and Regression

- [x] WP-G01: Contract, integration, Playwright regression pass — DONE

## Integration Tests

- [x] INT-001: File Import Registers Catalog Table
- [x] INT-002: Python Execution Creates Derived Catalog Table
- [x] INT-003: Odoo Fetch Registers Odoo Table
- [x] INT-004: Scheduled Pipeline Runs and Records History
- [x] INT-005: Failed Pipeline Surfaces Notification
- [x] INT-006: Odoo Sync Pre-Step Runs Before Script
- [x] INT-007: Table Management Updates Catalog
- [x] INT-008: Agent Generates and Corrects Code

## UAT Scenarios

- [x] UAT-001: Import CSV and Inspect It in Catalog
- [x] UAT-002: Fetch Odoo Records Into a Local Table
- [x] UAT-003: Transform Data With Python and Save a Derived Table
- [x] UAT-004: Create, Schedule, and Monitor a Pipeline
- [x] UAT-005: Recover From a Pipeline Failure
- [x] UAT-006: Run Odoo Sync Before Pipeline Script
- [x] UAT-007: Use Agent to Generate and Correct Python Code
- [ ] UAT-010: Empty Workspace Is Understandable
- [ ] UAT-011: Large-ish Local Data Does Not Break the UI
- [ ] UAT-012: Local-Only Privacy Defaults
