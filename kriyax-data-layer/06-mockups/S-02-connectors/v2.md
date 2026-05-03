# Mockup — S-02: Connectors

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — primary configured state

## Purpose

Give users a clear place to start file imports, open Odoo ingestion, and manage saved Odoo connections.

## Primary layout elements

- Connector entry cards for File upload and Odoo.
- Saved Odoo connection table with health/status actions.
- Recent imports table linking into table details.
- Explicit connector rules: new-table-only import, duplicate-column rename, saved connection management.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-DC-001 | File upload entry card and recent file imports. |
| F-DC-004 | Odoo entry card, connection test action, saved connection status. |
| F-DC-008 | Saved Odoo connections table with open/fix actions. |

## Flow notes

- `Start file import` opens S-03.
- `Open Odoo workspace` opens S-04.
- `Table detail` opens S-06.

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
