# Spec — F-SC-001: Table registry

**Version:** v1
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-02-schema-catalog
**Feature ref:** F-SC-001
**Dependencies:** F-DS-001

## Summary
Central registry of all tables in the backing database. Shows table name, row count, column count, source (CSV import / Odoo sync / derived), created date, last updated date.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| (none — reads from DB metadata) | — | — | — | — |

## States

### loading
Fetching table metadata from database. Spinner: "Loading table registry…"

### populated
Table list displayed: name, source, rows, columns, created, last updated. Sortable by any column. Search/filter bar.

### empty
No tables exist yet. Message: "No tables yet. Import data from the Connectors tab to get started."

### error:db-unreachable
Cannot connect to backing database.
Message: "Cannot connect to database. Check your setup."

## Transitions
| From | To | Trigger | Side effects |
|---|---|---|---|
| loading | populated | metadata fetched | none |
| loading | empty | 0 tables found | none |
| loading | error:db-unreachable | DB connection fails | none |

## Edge cases
- 100+ tables → paginated list (25 per page) with search
- Table with 0 rows → show normally, row count = 0
- Table source unknown (created outside platform) → source = "external"
- Registry refresh after import → auto-refresh when navigating to catalog page

## Acceptance checklist
- [ ] Import a CSV → table appears in registry with correct metadata
- [ ] Fetch from Odoo → table appears with source "odoo"
- [ ] Save from code workspace → table appears with source "derived"
- [ ] No tables → empty state shown
- [ ] Search by table name → filters correctly

---
*Frozen on: 2026-05-02*
