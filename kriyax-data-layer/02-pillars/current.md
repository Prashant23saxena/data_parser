# Pillars — KriyaX Data Layer

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Vision:** linked to `01-vision/current.md` (v2)

## Pillar 1: Data Connectors

**Purpose:** Get data into the system from external sources — files and third-party systems — reliably and repeatably.

**In scope:**
- CSV/Excel file upload (drag-and-drop or file picker)
- Odoo ERP API connector (read models, fetch records)
- Connection configuration and credential storage
- Schema discovery at source (auto-detect columns/types from CSV headers, Odoo model fields)
- Full refresh and incremental/delta sync modes

**Out of scope:**
- Real-time streaming connectors (Kafka, webhooks)
- Connectors beyond CSV/Excel and Odoo (future backlog)
- Data transformation during ingestion (that's Pillar 3)

---

## Pillar 2: Schema & Catalog

**Purpose:** Provide a central registry of all tables, their columns, data types, and relationships — the single source of truth that humans and the AI agent both use to understand available data.

**In scope:**
- Table registry (list of all ingested and derived tables)
- Column metadata (name, type, nullable, description)
- Schema evolution tracking (when columns are added/removed/changed)
- Browsable catalog UI (or CLI) to explore what data exists
- Metadata API for the agentic layer to read programmatically

**Out of scope:**
- Data governance / access control (RBAC, row-level security)
- Data lineage tracking (nice-to-have, not MVP)
- Business glossary / semantic layer definitions

---

## Pillar 3: Code Workspace

**Purpose:** Let the team write, run, and see results of Python/pandas transformation scripts against the platform data layer.

**In scope:**
- Plain Python code editor with run/output flow
- Python/pandas transformation support only
- Visible execution output for stdout, errors, and DataFrame previews
- Load tables from different sources (Odoo + CSV) as DataFrames and join them in pandas
- Save Python scripts as named transformations
- Create derived/refined tables from code results

**Out of scope:**
- R / Scala / other language support
- SQL authoring surface for v1
- Visualization / charting of results (future backlog)
- Collaborative editing (multi-user live cursors)
- Full Jupyter/JupyterHub deployment

---

## Pillar 4: Agentic Layer

**Purpose:** Let team members describe data needs in plain English and get working Python/pandas code back — powered by an LLM that understands the available schemas, tables, and metadata.

**In scope:**
- Natural language → Python/pandas code generation
- Schema-aware context (agent reads catalog metadata before generating)
- Code validation (check generated code against actual schema/data)
- Self-correction (if code fails, agent analyzes error and retries)
- Conversational follow-ups ("now filter this by date", "add a column for X")
- Output inserted directly into the Python code editor (Pillar 3 integration)

**Out of scope:**
- Autonomous pipeline creation (agent doesn't create scheduled jobs by itself)
- ML model training or predictions
- Multi-modal input (voice, images)
- Fine-tuning custom models (uses existing LLM APIs)

---

## Pillar 5: Pipeline & Scheduling

**Purpose:** Automate recurring data work — define ETL jobs that run on a schedule, with incremental/delta support, so data stays fresh without manual intervention.

**In scope:**
- Define pipeline steps (connector sync → transform → save to table)
- Schedule runs (cron expressions, interval-based)
- Incremental/delta update support
- Run history and status (success/failure/duration)
- Manual trigger option ("run now")
- Basic error notification (log failures, surface in UI)

**Out of scope:**
- Complex DAG orchestration (Airflow-style dependency graphs)
- Event-driven triggers (file arrival, webhook)
- Pipeline versioning and rollback
- Distributed execution across multiple workers

---

## Pillar 6: Data Storage

**Purpose:** Persist all ingested and refined data in a queryable database — and expose it so other KriyaX layers can pull cleaned data models.

**In scope:**
- Backing database for all tables (PostgreSQL or DuckDB)
- Table creation from ingested data (CSV → table, Odoo → table)
- Refined/derived table persistence (Python transformation results saved as new tables)
- Data export capability (other KriyaX layers can read from the same DB)
- Basic table management (drop, truncate, rename)

**Out of scope:**
- Multi-database federation (querying across Postgres + MySQL + etc.)
- Data lake / object storage (S3, parquet files)
- Backup and disaster recovery automation
- Horizontal scaling / sharding

---

## Coverage Map

| Vision element | Covered by pillar(s) |
|---|---|
| Ingest from CSV/Excel | Pillar 1 (Data Connectors) |
| Ingest from Odoo | Pillar 1 (Data Connectors) |
| Load into queryable tables | Pillar 1 + Pillar 6 (Connectors → Storage) |
| Schema management / view schemas | Pillar 2 (Schema & Catalog) |
| Python/pandas joins / clean data | Pillar 3 (Code Workspace) |
| English → Python/pandas code (agentic) | Pillar 4 (Agentic Layer) |
| Agent reads metadata | Pillar 4 + Pillar 2 (Agent reads Catalog) |
| Schedule pipelines | Pillar 5 (Pipeline & Scheduling) |
| Delta/incremental updates | Pillar 1 + Pillar 5 (Connectors + Pipelines) |
| Expose refined data to other layers | Pillar 6 (Data Storage) |
| Self-hosted / open-source | Cross-cutting (all pillars) |

---

*Frozen on: 2026-05-02*
