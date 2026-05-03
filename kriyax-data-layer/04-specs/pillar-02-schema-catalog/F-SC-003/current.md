# Spec — F-SC-003: Auto-register on ingest

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-02-schema-catalog
**Feature ref:** F-SC-003
**Dependencies:** F-SC-001, F-DC-003, F-DS-002

## Summary
When a new table is created (from CSV import, Odoo fetch, or save_table()), it is automatically registered in the catalog with source, timestamp, and schema metadata. No manual step needed.

## States
This is a **background process** — no UI states. It fires as a side effect of table creation.

### trigger:new-table
Event: New table created in DB from connector import, Odoo fetch, or save_table().
Action: Read table's information_schema, create catalog entry with: table_name, source, created_at, column_count, row_count.

### trigger:derived-replace
Event: A derived table is replaced later by Code Workspace behavior, if approved in F-CW-004/F-DS-003.
Action: Update the existing catalog entry; do not create a duplicate.

### error:registration-failed
Catalog write failed (should be very rare — DB is already up since table was just created).
Action: Log error. Table still exists in DB. User can see it but catalog may be stale. Catalog refreshes on next page load.

## Edge cases
- Connector imports are new-table-only in v1 → create a new catalog entry only after the new table is created
- Derived table replacement from save_table(), if approved later, → update catalog entry, don't create duplicate
- Table created by external tool (direct SQL) → not auto-registered. Discovered on next catalog page load via information_schema scan.

## Acceptance checklist
- [ ] Import CSV → table appears in catalog automatically
- [ ] save_table() from code → table appears in catalog
- [ ] Connector import creates a new table → new catalog entry created
- [ ] Derived table replacement, if approved later → catalog entry updated, not duplicated

---
*Frozen on: 2026-05-02*
