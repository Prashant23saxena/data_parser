# Spec — F-DC-003: Preview and target schema before import

**Version:** v3
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-003
**Dependencies:** F-DC-002

## Summary

Before committing data to the database, the user chooses the target schema/storage area, enters a new table name, reviews the confirmed column mapping from F-DC-002, previews rows, and imports into a new table only.

The preview step is the final confirmation point before a table is created.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| target_schema | enum/string | yes | raw_files | must be an available schema/storage area |
| table_name | string | yes | filename sanitized | alphanumeric + underscores, max 64 chars, unique within target schema |
| column_mapping | array | yes | from F-DC-002 | at least 1 column; all names/types valid |
| preview_rows | int | no | 50 | 10-100 |

## States

### previewing
Preview page is visible. User sees target schema dropdown, new table name input, column mapping/type summary, and first 50 rows.

### conversion-warning
One or more selected column types may not cleanly convert all previewed values. Message: "Some values may not match the selected type. Review before importing."

### importing
User clicked Create table. Data is being written to the selected target schema. Spinner: "Creating table..."

### success
Table created. Message: "Table '{{target_schema}}.{{table_name}}' created with {{row_count}} rows and {{col_count}} columns." Links to Catalog, Table Detail, and Code Workspace.

### error:schema-required
Target schema is missing or unavailable.
Message: "Choose a target schema before creating the table."

### error:name-conflict
Table name already exists in the selected schema.
Message: "Table '{{target_schema}}.{{table_name}}' already exists. Choose a new table name."

### error:import-failed
Database write failed.
Message: "Import failed: {{error}}. Try again."

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| previewing | conversion-warning | selected types conflict with previewed values | warning displayed; import may be blocked or require explicit confirmation |
| previewing | importing | user clicks Create table with valid schema/table/mapping | begin DB write |
| previewing | error:schema-required | target schema missing/unavailable | none |
| importing | success | DB write completes | table created and auto-registered in catalog |
| importing | error:name-conflict | table exists in selected schema | no table created |
| importing | error:import-failed | DB error | no successful import claimed |
| error:name-conflict | previewing | user enters unique table name | error clears |
| conversion-warning | previewing | user changes type or accepts warning | preview updates or import allowed |

## Edge cases

- Target schema dropdown unavailable → block import and link to storage settings.
- Table name with spaces → suggest underscore version, but show final name before import.
- Same table name in another schema → allowed if unique in selected schema.
- Very wide preview (100+ columns) → horizontal scroll.
- 0-row import (headers only) → allow with warning: "Table will be empty (0 rows)."
- User changes schema after preview → revalidate table-name conflict in the newly selected schema.

## Side effects on success

- Creates a new table in selected target schema/storage area.
- Registers table in catalog with source=file upload and mapping metadata.
- Clears temporary upload state after success.

## Failure recovery

Validation failures stop before database write. Database failures preserve target schema, table name, mapping, and preview so user can retry. No overwrite or partial-success claim is allowed.

## Acceptance checklist

- [ ] User must choose/confirm target schema before import.
- [ ] User enters unique new table name and creates table.
- [ ] Existing table name in same schema blocks import and asks for a different name.
- [ ] Same table name in different schema is allowed if storage supports it.
- [ ] Preview shows final column names and selected types.
- [ ] Import creates a new table and links to Catalog/Table Detail/Code Workspace.
- [ ] Cancel clears temporary import state and creates no table.

---
*Frozen on: 2026-05-02*
