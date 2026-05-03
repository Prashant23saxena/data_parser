# Build Backlog

> Ideas, questions, and notes parked during the build-planning process.
> Items here may be promoted into the active build plan or deferred.

**Layer:** L7 — Build
**Last updated:** 2026-05-02

## Parked Items

- [ ] **Unity Catalog (open source)** — Consider for Pillar 2 (Schema & Catalog). Open-sourced by Databricks in June 2024 under Apache 2.0. Provides centralized governance, metadata, and table registry. — *parked from L2 discussion* — 2026-05-02
- [ ] **Jupyter Notebook (open source)** — Consider for Pillar 3 (Code Workspace). BSD-licensed, provides cell-by-cell execution with inline output, supports SQL + Python. Could be embedded as the notebook engine. — *parked from L2 discussion* — 2026-05-02
- [ ] **Vanna.ai (open source)** — Consider for Pillar 4 (Agentic Layer). RAG-based text-to-SQL framework, schema-aware, supports self-correction. v2.0 has agentic architecture. — *parked from L2 discussion* — 2026-05-02
- [ ] **Delta Lake (open source)** — Consider for Pillar 6 (Data Storage). ACID transactions on data lakes, schema evolution, time travel. May be overkill for current scale. — *parked from L2 discussion* — 2026-05-02
- [ ] **Airbyte (open source)** — Consider for Pillar 1 (Data Connectors). 300+ pre-built connectors, incremental sync, schema discovery. Could replace custom connector code. — *parked from L2 discussion* — 2026-05-02
- [ ] **PostgreSQL or DuckDB** — Backing database decision for Pillar 6. PostgreSQL for production use, DuckDB for lightweight analytical queries. — *parked from L2 discussion* — 2026-05-02
- [ ] **Dagster or simple cron** — Orchestration engine for Pillar 5 (Pipelines). Dagster is modern but may be overkill; simple cron + custom scheduler might suffice for bridge tool. — *parked from L2 discussion* — 2026-05-02
