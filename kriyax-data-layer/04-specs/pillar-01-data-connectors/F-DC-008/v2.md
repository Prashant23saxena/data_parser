# Spec — F-DC-008: Manage saved connections

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-008
**Dependencies:** F-DC-004

## Summary
List all saved connection configurations. Edit credentials, rename, delete. Simple CRUD interface.

This feature is must-have because saved connections are reused by Odoo browsing, record fetch, incremental sync, and scheduled pipelines.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| (none for list view) | — | — | — | — |
| connection_id | string | yes (for edit/delete) | — | must exist |

## States

### list
Table of saved connections: name, type (Odoo), URL, last used date, status (active/error). Action buttons: Edit, Delete, Test.

### empty-list
No saved connections. Message: "No connections saved yet. Add one from the Connectors page."

### editing
Edit form pre-filled with connection details. Same fields as F-DC-004. "Save" and "Cancel" buttons.

### confirm-delete
User clicked Delete. Confirmation dialog: "Delete connection '{{name}}'? This cannot be undone. Pipelines using this connection will break."

### deleted
Connection removed. Message: "Connection '{{name}}' deleted." List refreshes.

## Transitions
| From | To | Trigger | Side effects |
|---|---|---|---|
| list | editing | user clicks Edit on a connection | form populated |
| list | confirm-delete | user clicks Delete | none |
| editing | list | user clicks Save (validation passes) | connection updated |
| editing | list | user clicks Cancel | no changes |
| confirm-delete | deleted | user confirms | connection removed from DB |
| confirm-delete | list | user cancels | none |

## Edge cases
- Delete a connection used by a pipeline → warn: "This connection is used by pipeline '{{pipeline_name}}'. Deleting will break it."
- Edit URL and re-test → must pass test before save
- No connections → show empty-list state with link to add

## Acceptance checklist
- [ ] View list of saved connections → shows all with correct details
- [ ] Edit a connection's API key → save works, re-test passes
- [ ] Delete a connection → removed from list
- [ ] Delete connection used by pipeline → warning shown

---
*Frozen on: 2026-05-02*
