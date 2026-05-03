# Features — Data Connectors

**Version:** v3
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors, from `02-pillars/current.md`

## Feature index

| ID | Name | Priority | Depends on |
|---|---|---|---|
| F-DC-001 | Upload CSV/Excel file | must | — |
| F-DC-002 | Auto-detect columns & types | must | F-DC-001 |
| F-DC-003 | Preview before import | must | F-DC-002 |
| F-DC-004 | Configure Odoo connection | must | — |
| F-DC-005 | Browse Odoo models & fields | must | F-DC-004 |
| F-DC-006 | Fetch Odoo records to table | must | F-DC-005 |
| F-DC-007 | Incremental/delta sync | must | F-DC-006 |
| F-DC-008 | Manage saved connections | must | F-DC-004 |

## Features

### F-DC-001: Upload CSV/Excel file

**Description:** User uploads a local CSV or Excel file via drag-and-drop or file picker. Supports .csv, .xlsx, .xls formats. Handles multiple sheets in Excel (user picks which sheet to import).

**Priority:** must

**Dependencies:** none

**Definition of done:** User can select or drag a CSV/Excel file, the system accepts it and stores it temporarily for parsing. Multiple Excel sheets are listed for selection.

**Cross-pillar links:** none

---

### F-DC-002: Auto-detect columns & types

**Description:** After file upload, the system parses headers and sample rows to infer column names and data types (string, integer, float, date, boolean). Handles common CSV quirks (delimiters, encoding, quoted fields).

**Priority:** must

**Dependencies:** F-DC-001

**Definition of done:** System produces a column list with inferred types from any uploaded CSV/Excel file. If duplicate column names are detected, user is asked to rename the duplicates before continuing.

**Cross-pillar links:** Pillar 2 (Schema & Catalog) — detected schema is registered in the catalog after import.

---

### F-DC-003: Preview before import

**Description:** Before committing data to the database, show the user the first 50-100 rows along with the detected schema (column names + types). User confirms the schema and chooses a new table name before proceeding.

**Priority:** must

**Dependencies:** F-DC-002

**Definition of done:** User sees a table preview with correct columns and types, chooses a new unique table name, and clicks "Import" to commit. Can cancel without side effects.

**Cross-pillar links:** none

---

### F-DC-004: Configure Odoo connection

**Description:** User enters Odoo instance URL, database name, and API key (or username/password). System tests the connection via XML-RPC and reports success/failure with clear error messages.

**Priority:** must

**Dependencies:** none

**Definition of done:** User can enter Odoo credentials, click "Test Connection", and see a success confirmation (with Odoo version info) or a clear error message. Credentials are saved for reuse.

**Cross-pillar links:** Pillar 5 (Pipeline & Scheduling) — saved connections are used in scheduled pipeline steps.

---

### F-DC-005: Browse Odoo models & fields

**Description:** After connecting to Odoo, the user can browse available models (e.g., res.partner, sale.order, product.product) and see their fields with types. Uses Odoo's `fields_get` API method.

**Priority:** must

**Dependencies:** F-DC-004

**Definition of done:** User sees a searchable list of Odoo models. Clicking a model shows its fields (name, type, required, description). User can select which model and fields to fetch.

**Cross-pillar links:** Pillar 2 (Schema & Catalog) — Odoo model structure feeds into the schema catalog as a source schema.

---

### F-DC-006: Fetch Odoo records to table

**Description:** User selects an Odoo model and fields, clicks fetch, and the system pulls records via XML-RPC `search_read` and loads them into a local database table. Supports domain filters to limit records.

**Priority:** must

**Dependencies:** F-DC-005

**Definition of done:** Records from selected Odoo model are loaded into a named database table. User can specify a table name and optional domain filters. Row count is reported on completion.

**Cross-pillar links:** Pillar 6 (Data Storage) — creates tables in the backing database. Pillar 2 (Schema & Catalog) — new table is registered in catalog.

---

### F-DC-007: Incremental/delta sync

**Description:** For Odoo connections, support fetching only new or modified records since the last sync. Uses a cursor field (e.g., `write_date`) to detect changes. Appends or upserts into the existing table.

**Priority:** must

**Dependencies:** F-DC-006

**Definition of done:** System tracks last sync timestamp per connection+model. Subsequent syncs only pull records where cursor field > last sync. Existing rows are updated (upsert), new rows are appended.

**Cross-pillar links:** Pillar 5 (Pipeline & Scheduling) — incremental sync is the primary mode for scheduled pipelines.

---

### F-DC-008: Manage saved connections

**Description:** List all saved connection configurations (Odoo instances, file upload history). Edit credentials, rename connections, delete unused ones. Simple CRUD interface.

**Priority:** must

**Dependencies:** F-DC-004

**Definition of done:** User sees a list of saved connections with name, type (Odoo/file), and last-used date. Can edit, rename, or delete any connection.

**Cross-pillar links:** none

---

## Coverage map

| Pillar in-scope item | Covered by |
|---|---|
| CSV/Excel file upload | F-DC-001, F-DC-002, F-DC-003 |
| Odoo ERP API connector | F-DC-004, F-DC-005, F-DC-006 |
| Connection configuration and credential storage | F-DC-004, F-DC-008 |
| Schema discovery at source | F-DC-002 (CSV), F-DC-005 (Odoo) |
| Full refresh and incremental/delta sync modes | F-DC-006 (full), F-DC-007 (incremental) |

---

*Frozen on: 2026-05-02*
