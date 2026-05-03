# Spec — F-SC-004: Browse & search catalog

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-02-schema-catalog
**Feature ref:** F-SC-004
**Dependencies:** F-SC-001

## Summary
Search/filter the catalog by table name, column name, source type, or date. Find tables quickly in a growing catalog.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| search_query | string | no | — | free text, matches table name or column name |
| source_filter | enum | no | all | all / csv / odoo / derived / external |
| sort_by | enum | no | name | name / created / updated / rows |

## States

### filtered
Catalog list with active filters applied. Shows matching tables.

### no-results
Search/filter returns 0 results. Message: "No tables match '{{query}}'."

## Edge cases
- Search is case-insensitive
- Partial matches work ("ord" matches "sale_orders")
- Column search works ("partner_id" matches tables that contain a `partner_id` column)
- Filters combine: source=odoo AND query="partner" → only Odoo tables with "partner" in name

## Acceptance checklist
- [ ] Search "order" → matching tables shown
- [ ] Search a column name → tables containing that column are shown
- [ ] Filter by source "csv" → only CSV-imported tables shown
- [ ] Clear filters → all tables visible
- [ ] No matches → "No tables match" message

---
*Frozen on: 2026-05-02*
