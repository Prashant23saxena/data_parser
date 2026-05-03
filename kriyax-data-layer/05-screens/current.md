# Screens — KriyaX Data Layer

**Version:** v1
**Status:** FROZEN
**Last updated:** 2026-05-02

## Research anchors

- Databricks workspace UI uses a sidebar/workspace model with Catalog and Jobs & Pipelines as first-class destinations.
- ETL/data integration tools commonly separate connectors, catalog/data assets, transformation workspace, schedules, and run monitoring.
- For this internal bridge tool, desktop-first sidebar navigation is preferred over a marketing or mobile-first layout.

## Platform

Desktop-first responsive web app for internal Kriya users. Mobile responsiveness is acceptable for viewing status, but authoring code, browsing schemas, and configuring pipelines are desktop workflows.

## Top-level navigation

**Pattern:** Left sidebar control plane.

**Destinations:**
1. Home → operations overview and recent work
2. Connectors → CSV/Excel and Odoo ingestion
3. Catalog → tables, metadata, preview, export, table actions
4. Code Workspace → Python/pandas authoring and output
5. Agent → docked inside Code Workspace, not separate top-level route
6. Pipelines → schedules, manual runs, history, alerts
7. Storage Settings → backing database health

## Screen index

| ID | Name | Purpose | Pillar(s) | Features | Type |
|---|---|---|---|---|---|
| S-01 | Home / Operations Overview | Entry screen with shortcuts, recent tables/scripts/pipelines, and current pipeline health. | Cross-cutting | F-PS-004, F-PS-005 | full screen |
| S-02 | Connectors | Choose file upload or Odoo connection workflows and view saved connector entry points. | Data Connectors | F-DC-001, F-DC-004, F-DC-008 | full screen |
| S-03 | File Import Wizard | Upload CSV/Excel, detect schema, preview rows, and create a new table. | Data Connectors, Data Storage, Schema & Catalog | F-DC-001, F-DC-002, F-DC-003, F-DS-002, F-SC-003 | full screen wizard |
| S-04 | Odoo Import Workspace | Configure/test Odoo, browse models/fields, fetch records, and configure delta sync. | Data Connectors, Data Storage, Schema & Catalog | F-DC-004, F-DC-005, F-DC-006, F-DC-007, F-DC-008, F-DS-002, F-SC-003 | full screen workspace |
| S-05 | Catalog | Browse/search all tables and open table details. | Schema & Catalog | F-SC-001, F-SC-004, F-SC-005, F-DS-005 | full screen |
| S-06 | Table Detail | View table metadata, columns, sample rows, export, and management actions. | Schema & Catalog, Data Storage | F-SC-002, F-SC-005, F-DS-004, F-DS-005 | full screen detail |
| S-07 | Table Management Confirmation | Confirm rename, truncate, or drop actions with strong destructive-action safeguards. | Data Storage | F-DS-004 | modal |
| S-08 | Export Table Modal | Export a selected table as CSV. | Data Storage | F-DS-005 | modal |
| S-09 | Code Workspace | Write/run Python transformations, inspect available tables, load/save DataFrames, see output, and save scripts. | Code Workspace, Schema & Catalog, Data Storage | F-CW-001, F-CW-002, F-CW-003, F-CW-004, F-CW-005, F-CW-006, F-SC-001, F-SC-002, F-SC-005, F-DS-003 | full screen workspace |
| S-10 | Agent Panel | Chat with the agent, load schema-aware context, generate Python code, insert code, self-correct errors, and continue follow-ups. | Agentic Layer, Code Workspace | F-AL-001, F-AL-002, F-AL-003, F-AL-004, F-AL-005, F-AL-006, F-CW-005 | dockable panel within Code Workspace |
| S-11 | Saved Scripts | Browse saved Python scripts, open them in editor, and select them for pipelines. | Code Workspace, Pipeline & Scheduling | F-CW-006, F-PS-001 | full screen or side panel |
| S-12 | Pipelines | Create, schedule, enable/disable, manually trigger, and monitor pipelines. | Pipeline & Scheduling | F-PS-001, F-PS-002, F-PS-003, F-PS-004, F-PS-005, F-PS-006, F-CW-006, F-DC-007 | full screen |
| S-13 | Pipeline Run Detail | Inspect one pipeline run, logs, traceback, status, duration, and related script/sync step. | Pipeline & Scheduling, Agentic Layer | F-PS-004, F-PS-005, F-AL-005 | full screen detail |
| S-14 | Storage Settings | Show backing database status and storage configuration health. | Data Storage | F-DS-001 | settings screen |

## Sitemap

```
Home / Operations Overview (S-01)
├── Connectors (S-02)
│   ├── File Import Wizard (S-03)
│   └── Odoo Import Workspace (S-04)
├── Catalog (S-05)
│   ├── Table Detail (S-06)
│   │   ├── Table Management Confirmation (S-07 modal)
│   │   └── Export Table Modal (S-08 modal)
│   └── Code Workspace (S-09)
│       └── Agent Panel (S-10 docked)
├── Saved Scripts (S-11)
├── Pipelines (S-12)
│   └── Pipeline Run Detail (S-13)
└── Storage Settings (S-14)
```

## Screens

### S-01: Home / Operations Overview
**Purpose:** Entry screen with shortcuts, recent tables/scripts/pipelines, and current pipeline health.
**Pillar(s):** Cross-cutting
**Features:** F-PS-004, F-PS-005
**States shown:** loading / healthy / failures / empty workspace
**Type:** full screen
**Reachable from:** entry, sidebar
**Goes to:** S-02, S-05, S-09, S-12

### S-02: Connectors
**Purpose:** Choose file upload or Odoo connection workflows and view saved connector entry points.
**Pillar(s):** Data Connectors
**Features:** F-DC-001, F-DC-004, F-DC-008
**States shown:** empty / configured / connection errors
**Type:** full screen
**Reachable from:** sidebar, S-01
**Goes to:** S-03, S-04

### S-03: File Import Wizard
**Purpose:** Upload CSV/Excel, detect schema, preview rows, and create a new table.
**Pillar(s):** Data Connectors, Data Storage, Schema & Catalog
**Features:** F-DC-001, F-DC-002, F-DC-003, F-DS-002, F-SC-003
**States shown:** upload / detecting / duplicate column rename / preview / importing / success / error
**Type:** full screen wizard
**Reachable from:** S-02
**Goes to:** S-05

### S-04: Odoo Import Workspace
**Purpose:** Configure/test Odoo, browse models/fields, fetch records, and configure delta sync.
**Pillar(s):** Data Connectors, Data Storage, Schema & Catalog
**Features:** F-DC-004, F-DC-005, F-DC-006, F-DC-007, F-DC-008, F-DS-002, F-SC-003
**States shown:** connection form / model list / field detail / fetch configure / syncing / success / errors
**Type:** full screen workspace
**Reachable from:** S-02
**Goes to:** S-05, S-13

### S-05: Catalog
**Purpose:** Browse/search all tables and open table details.
**Pillar(s):** Schema & Catalog
**Features:** F-SC-001, F-SC-004, F-SC-005, F-DS-005
**States shown:** loading / populated / empty / no results / error
**Type:** full screen
**Reachable from:** sidebar, S-01, import success
**Goes to:** S-06, S-07, S-08, S-09

### S-06: Table Detail
**Purpose:** View table metadata, columns, sample rows, export, and management actions.
**Pillar(s):** Schema & Catalog, Data Storage
**Features:** F-SC-002, F-SC-005, F-DS-004, F-DS-005
**States shown:** metadata / preview / empty table / management confirm / error
**Type:** full screen detail
**Reachable from:** S-05
**Goes to:** S-08, S-09

### S-07: Table Management Confirmation
**Purpose:** Confirm rename, truncate, or drop actions with strong destructive-action safeguards.
**Pillar(s):** Data Storage
**Features:** F-DS-004
**States shown:** confirm rename / confirm truncate / confirm drop / blocked internal table
**Type:** modal
**Reachable from:** S-06
**Goes to:** S-06

### S-08: Export Table Modal
**Purpose:** Export a selected table as CSV.
**Pillar(s):** Data Storage
**Features:** F-DS-005
**States shown:** ready / exporting / download ready / error
**Type:** modal
**Reachable from:** S-05, S-06
**Goes to:** S-05, S-06

### S-09: Code Workspace
**Purpose:** Write/run Python transformations, inspect available tables, load/save DataFrames, see output, and save scripts.
**Pillar(s):** Code Workspace, Schema & Catalog, Data Storage
**Features:** F-CW-001, F-CW-002, F-CW-003, F-CW-004, F-CW-005, F-CW-006, F-SC-001, F-SC-002, F-SC-005, F-DS-003
**States shown:** empty editor / editing / running / output success / traceback / saved script
**Type:** full screen workspace
**Reachable from:** sidebar, S-01, S-05, S-06, S-10
**Goes to:** S-05, S-10, S-12

### S-10: Agent Panel
**Purpose:** Chat with the agent, load schema-aware context, generate Python code, insert code, self-correct errors, and continue follow-ups.
**Pillar(s):** Agentic Layer, Code Workspace
**Features:** F-AL-001, F-AL-002, F-AL-003, F-AL-004, F-AL-005, F-AL-006, F-CW-005
**States shown:** empty chat / thinking / code generated / fix proposed / max attempts / LLM error
**Type:** dockable panel within Code Workspace
**Reachable from:** S-09
**Goes to:** S-09

### S-11: Saved Scripts
**Purpose:** Browse saved Python scripts, open them in editor, and select them for pipelines.
**Pillar(s):** Code Workspace, Pipeline & Scheduling
**Features:** F-CW-006, F-PS-001
**States shown:** list / empty / script detail / rename conflict
**Type:** full screen or side panel
**Reachable from:** sidebar, S-09, S-12
**Goes to:** S-09, S-12

### S-12: Pipelines
**Purpose:** Create, schedule, enable/disable, manually trigger, and monitor pipelines.
**Pillar(s):** Pipeline & Scheduling
**Features:** F-PS-001, F-PS-002, F-PS-003, F-PS-004, F-PS-005, F-PS-006, F-CW-006, F-DC-007
**States shown:** list / empty / configuring / scheduled / disabled / failure badge / running
**Type:** full screen
**Reachable from:** sidebar, S-01, S-11
**Goes to:** S-13

### S-13: Pipeline Run Detail
**Purpose:** Inspect one pipeline run, logs, traceback, status, duration, and related script/sync step.
**Pillar(s):** Pipeline & Scheduling, Agentic Layer
**Features:** F-PS-004, F-PS-005, F-AL-005
**States shown:** running / success / failed / logs unavailable
**Type:** full screen detail
**Reachable from:** S-12, S-01
**Goes to:** S-09, S-10, S-12

### S-14: Storage Settings
**Purpose:** Show backing database status and storage configuration health.
**Pillar(s):** Data Storage
**Features:** F-DS-001
**States shown:** ready / checking / db unreachable / migration error
**Type:** settings screen
**Reachable from:** sidebar/settings
**Goes to:** S-01, S-05

## Critical user flows

### Flow 1: File import to transformation
S-01 → S-02 → S-03 → S-05 → S-06 → S-09

### Flow 2: Odoo ingest to scheduled pipeline
S-01 → S-02 → S-04 → S-05 → S-09 → S-11 → S-12

### Flow 3: Agent-assisted transformation
S-09 → S-10 → S-09 → S-10 if correction needed → S-09 → S-05

### Flow 4: Pipeline failure recovery
S-01 → S-12 → S-13 → S-09/S-10 → S-12 manual rerun

### Flow 5: Table maintenance/export
S-05 → S-06 → S-08 export OR S-07 destructive confirmation → S-05

## Modal vs Screen Rule

Use full screens for multi-step, stateful workspaces: import, Odoo, catalog, code, pipelines. Use modals only for short confirmations or one-action tasks: table management confirmation and CSV export.

## Coverage check

| Feature | On screen(s) |
|---|---|
| F-DC-001 Upload CSV/Excel file | S-02 Connectors; S-03 File Import Wizard |
| F-DC-002 Auto-detect columns & types | S-03 File Import Wizard |
| F-DC-003 Preview before import | S-03 File Import Wizard |
| F-DC-004 Configure Odoo connection | S-02 Connectors; S-04 Odoo Import Workspace |
| F-DC-005 Browse Odoo models & fields | S-04 Odoo Import Workspace |
| F-DC-006 Fetch Odoo records to table | S-04 Odoo Import Workspace |
| F-DC-007 Incremental/delta sync | S-04 Odoo Import Workspace; S-12 Pipelines |
| F-DC-008 Manage saved connections | S-02 Connectors; S-04 Odoo Import Workspace |
| F-SC-001 Table registry | S-05 Catalog; S-09 Code Workspace |
| F-SC-002 Column metadata viewer | S-06 Table Detail; S-09 Code Workspace |
| F-SC-003 Auto-register on ingest | S-03 File Import Wizard; S-04 Odoo Import Workspace |
| F-SC-004 Browse & search catalog | S-05 Catalog |
| F-SC-005 Preview table rows | S-05 Catalog; S-06 Table Detail; S-09 Code Workspace |
| F-CW-001 Python code editor | S-09 Code Workspace |
| F-CW-002 Show available tables | S-09 Code Workspace |
| F-CW-003 Load tables as DataFrames | S-09 Code Workspace |
| F-CW-004 Save DataFrame as table | S-09 Code Workspace |
| F-CW-005 View execution output | S-09 Code Workspace; S-10 Agent Panel |
| F-CW-006 Save & re-run scripts | S-09 Code Workspace; S-11 Saved Scripts; S-12 Pipelines |
| F-AL-001 Chat interface | S-10 Agent Panel |
| F-AL-002 Schema-aware context loading | S-10 Agent Panel |
| F-AL-003 Generate Python/pandas code | S-10 Agent Panel |
| F-AL-004 Insert code into editor | S-10 Agent Panel |
| F-AL-005 Self-correction on error | S-10 Agent Panel; S-13 Pipeline Run Detail |
| F-AL-006 Conversational follow-ups | S-10 Agent Panel |
| F-PS-001 Create pipeline | S-11 Saved Scripts; S-12 Pipelines |
| F-PS-002 Schedule pipeline | S-12 Pipelines |
| F-PS-003 Manual trigger | S-12 Pipelines |
| F-PS-004 Run history & status | S-01 Home / Operations Overview; S-12 Pipelines; S-13 Pipeline Run Detail |
| F-PS-005 Error notifications | S-01 Home / Operations Overview; S-12 Pipelines; S-13 Pipeline Run Detail |
| F-PS-006 Enable/disable pipeline | S-12 Pipelines |
| F-DS-001 Backing database setup | S-14 Storage Settings |
| F-DS-002 Auto-create tables on import | S-03 File Import Wizard; S-04 Odoo Import Workspace |
| F-DS-003 Persist derived tables | S-09 Code Workspace |
| F-DS-004 Basic table management | S-06 Table Detail; S-07 Table Management Confirmation |
| F-DS-005 Export table data | S-05 Catalog; S-06 Table Detail; S-08 Export Table Modal |

---
*Drafted on: 2026-05-02*

---
*Frozen on: 2026-05-02*
