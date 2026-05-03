# Mockup — S-05: Catalog

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — populated catalog with preview drawer

## Purpose

Let users browse, search, preview, export, and open tables without needing to enter the code workspace first.

## Primary layout elements

- Search and source filters.
- Table registry with source, rows, columns, updated time, and explicit actions.
- Preview drawer for selected table rows.
- Empty/no-result guidance.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-SC-001 | Table registry list. |
| F-SC-004 | Search and filters. |
| F-SC-005 | Inline preview drawer. |
| F-DS-005 | Export action. |

## Action language

- **Details** opens S-06 Table Detail.
- **Preview rows** opens the inline row-preview drawer only.
- **Use in Python** opens S-09 Code Workspace and inserts/loads the table using `load_table("table_name")`.
- **Export CSV** opens S-08 Export Table Modal.

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
