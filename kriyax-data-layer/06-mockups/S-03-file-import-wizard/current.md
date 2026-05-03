# Mockup — S-03: File Import Wizard

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — target-schema and column-mapping state

## Purpose

Guide a user from CSV/Excel upload to a new registered table, with explicit target schema selection, column-name/type review, duplicate-column renaming, preview rows, and safe create-table behavior.

## Primary layout elements

- Wizard progress indicator.
- Uploaded file summary.
- Target schema dropdown and new table name input.
- Duplicate column review panel.
- Column mapping and type review table.
- Row preview.
- Back, preview more rows, and create table actions.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-DC-001 | Upload file state and uploaded file summary. |
| F-DC-002 | User chooses target schema/storage area and reviews system-suggested column names/types. |
| F-DC-003 | Row preview before import. |
| F-DS-002 | New table creation action. |
| F-SC-003 | Success state links to registered table. |

## Revision flags raised

- L4 wording should be revised later from "detected schema" to "target schema selection plus column mapping/type review" so the implementation contract is not ambiguous.

---
*Frozen on: 2026-05-02*
