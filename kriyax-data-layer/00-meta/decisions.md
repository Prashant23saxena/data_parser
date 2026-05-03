# Decisions Log

> Decisions made during design that should be remembered. Append new decisions; do not edit old ones.

## D-001: Python-only code workspace
Layer: L3
Date: 2026-05-02
Reason: User prefers Python/pandas scripts over SQL or notebook approach. Simpler to build, pandas handles all transformation needs.
Affects: Pillar 3, Pillar 4 (agent generates Python only)

## D-002: No Jupyter — plain Python editor
Layer: L3
Date: 2026-05-02
Reason: Full Jupyter is overkill for a bridge tool. A simple Python code editor with run/output is sufficient.
Affects: Pillar 3 (Code Workspace)

## D-003: Schema confirmation before table creation
Layer: L3
Date: 2026-05-02
Reason: User wants auto-detected schema to be reviewed and confirmed before committing to DB. Prevents silent wrong-type tables.
Affects: Pillar 6 (Data Storage), Pillar 1 (Data Connectors)

## D-004: Agent generates Python only, no SQL
Layer: L3
Date: 2026-05-02
Reason: Since Pillar 3 is Python-only, agent output must also be Python/pandas code using load_table()/save_table() helpers.
Affects: Pillar 4 (Agentic Layer)

## D-005: Self-correction is core agentic behavior
Layer: L3
Date: 2026-05-02
Reason: User identified agentic error recovery as very important and requiring dedicated research before implementation.
Affects: Pillar 4 (Agentic Layer), L4 feature specs, L7 build planning

## D-006: Data Connector features are all must-have
Layer: L3/L4
Date: 2026-05-02
Reason: User clarified this is a full feature list; if a connector feature is kept, it is must-have rather than should-have.
Affects: Pillar 1 (Data Connectors), L4 connector specs

## D-007: Connector imports create new tables only in v1
Layer: L4
Date: 2026-05-02
Reason: User chose new-table import behavior and removed overwrite from the connector import flow.
Affects: F-DC-003, F-DC-006, Data Storage

## D-008: Duplicate file columns require user rename
Layer: L4
Date: 2026-05-02
Reason: User chose an explicit rename flow for duplicate columns instead of silent auto-suffixing or generic schema overrides.
Affects: F-DC-002, F-DC-003

## D-009: Bare-bones Python scripts run through local Python execution wrapper
Layer: L6
Date: 2026-05-02
Reason: User wants the backend model to stay understandable: save transformations as real Python files and execute them with the laptop's configured Python. The app should only wrap that call to provide workspace context, helpers, logs, errors, and scheduling, avoiding a custom Python engine, heavy notebook, or hidden transform system.
Affects: Code Workspace, Saved Scripts, Pipelines, Pipeline Run Detail, Storage Settings, L7 build planning

## D-010: File import uses user-selected target schema and column mapping
Layer: L6
Date: 2026-05-02
Reason: User clarified that import should not imply blind auto-detected schema creation. The user should choose an available target schema/storage area and be able to edit both column names and column types before import.
Affects: File Import Wizard, F-DC-002, F-DC-003, F-DS-002, L4 revision wording

## D-011: Generated page images are visual references, not pixel-perfect specs
Layer: L6
Date: 2026-05-02
Reason: User approved the generated page images as good design-language references while noting they may not be 100% accurate. Frozen specs and v2 wireframes remain the implementation source of truth.
Affects: L6 visual references, L7 build planning, frontend implementation

## D-012: Keep KriyaX Data Layer as a modular monolith
Layer: L8.2
Date: 2026-05-03
Reason: The app is an internal bridge tool with a local workspace, one FastAPI backend, one React frontend, and one DuckDB warehouse. Component boundaries should guide ownership and contracts, not introduce deployable microservices.
Affects: L8.2 components, L8.3 contracts, implementation sequencing

## D-013: Backend routers stay thin; services own domain behavior
Layer: L8.2
Date: 2026-05-03
Reason: The existing build already separates `backend/app/api/*` from `backend/app/services/*`. Keeping routers focused on HTTP parsing/error mapping and services focused on behavior makes the remaining work easier to package and test.
Affects: backend API contracts, service ownership, work packages

## D-014: Pipelines orchestrate but delegate execution and connector sync
Layer: L8.2
Date: 2026-05-03
Reason: Pipeline scheduling owns definitions, schedules, run records, and failure state. Python execution remains owned by the execution service; Odoo incremental sync remains owned by the Odoo service.
Affects: Pipeline scheduling, Odoo sync pre-step, execution service contracts
