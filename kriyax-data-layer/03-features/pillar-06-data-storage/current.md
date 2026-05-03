# Features — Data Storage

**Version:** v1
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-06-data-storage, from `02-pillars/current.md`

## Feature index

| ID | Name | Priority | Depends on |
|---|---|---|---|
| F-DS-001 | Backing database setup | must | — |
| F-DS-002 | Auto-create tables on import | must | F-DS-001, F-DC-003 |
| F-DS-003 | Persist derived tables | must | F-DS-001, F-CW-004 |
| F-DS-004 | Basic table management | must | F-DS-001 |
| F-DS-005 | Export table data | should | F-DS-001 |

## Features

### F-DS-001: Backing database setup

**Description:** A single backing database (PostgreSQL or DuckDB) that stores all ingested and derived tables. Pre-configured and ready to use — no manual database setup by the user. All other pillars read/write to this database.

**Priority:** must

**Dependencies:** none

**Definition of done:** Database is provisioned and accessible. All platform components (connectors, code workspace, catalog) can connect to it. Tables can be created, queried, and dropped via standard DB operations.

**Cross-pillar links:** All pillars depend on this — it's the foundation.

---

### F-DS-002: Auto-create tables on import

**Description:** When data is ingested via connectors (CSV upload or Odoo fetch), the system auto-detects the schema (column names + data types) and proposes it to the user for confirmation before creating the table. User can adjust column names/types before committing.

**Priority:** must

**Dependencies:** F-DS-001, F-DC-003 (Data Connectors: Preview before import)

**Definition of done:** After import, system proposes a table name and auto-detected schema (columns + types). User reviews and confirms (or adjusts column names/types). Only after confirmation does the table get created in the database. No silent table creation.

**Cross-pillar links:** Pillar 1 (Data Connectors) — triggered by import flow. Pillar 2 (Schema & Catalog) — new table auto-registers via F-SC-003.

---

### F-DS-003: Persist derived tables

**Description:** When a user calls `save_table(df, "name")` from the Code Workspace (Pillar 3), the pandas DataFrame is written to the backing database as a real table. Creates the table if it doesn't exist, replaces data if it does.

**Priority:** must

**Dependencies:** F-DS-001, F-CW-004 (Code Workspace: Save DataFrame as table)

**Definition of done:** `save_table()` creates or replaces a database table with the DataFrame's data and schema. Table is queryable immediately after save. Appears in the catalog (Pillar 2) via auto-registration.

**Cross-pillar links:** Pillar 3 (Code Workspace) — called from Python scripts. Pillar 2 (Schema & Catalog) — new/updated table auto-registers.

---

### F-DS-004: Basic table management

**Description:** Simple table operations accessible from the UI — drop a table, truncate (clear all rows but keep schema), or rename a table. Confirmation dialog before destructive actions.

**Priority:** must

**Dependencies:** F-DS-001

**Definition of done:** User can select a table and perform drop, truncate, or rename. Destructive actions (drop, truncate) require confirmation. Changes are reflected in the catalog immediately.

**Cross-pillar links:** Pillar 2 (Schema & Catalog) — catalog updates on table changes.

---

### F-DS-005: Export table data

**Description:** Download any table's data as a CSV file for use outside the platform — e.g., sharing with someone, importing into another tool, or backing up manually.

**Priority:** should

**Dependencies:** F-DS-001

**Definition of done:** User can click "Export" on any table and download a .csv file containing all rows and columns. File downloads to the browser/local machine.

**Cross-pillar links:** none

---

## Coverage map

| Pillar in-scope item | Covered by |
|---|---|
| Backing database for all tables (PostgreSQL or DuckDB) | F-DS-001 |
| Table creation from ingested data | F-DS-002 |
| Refined/derived table persistence | F-DS-003 |
| Data export capability | F-DS-005 |
| Basic table management (drop, truncate, rename) | F-DS-004 |

---

*Frozen on: 2026-05-02*
