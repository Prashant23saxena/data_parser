# Test Scenarios — F-DC-003: Preview and target schema before import

**Spec version:** v3
**Generated:** 2026-05-02
**Status:** FROZEN
**Total scenarios:** 13
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-003/v3.md

## Happy path

### TS-001: Preview with target schema and table name
**Given:** A confirmed column mapping exists from F-DC-002.
**When:** The preview screen opens.
**Then:** The user sees target schema dropdown, table name input, mapping summary, and row preview.

### TS-002: Create table in selected schema
**Given:** The selected schema, table name, and mapping are valid.
**When:** The user clicks Create table.
**Then:** A new table is created in the selected schema and links to Catalog/Table Detail/Code Workspace are shown.

## Validation

### TS-003: Missing target schema blocks import
**Given:** No target schema is selected.
**When:** The user clicks Create table.
**Then:** The user sees "Choose a target schema before creating the table." and no table is created.

### TS-004: Existing table name in same schema blocks import
**Given:** A table with the same name exists in the selected schema.
**When:** The user clicks Create table.
**Then:** The user sees a name-conflict message and must choose a different table name.

### TS-005: Same table name in different schema is allowed
**Given:** A table name exists in `raw_odoo` but the user selects `raw_files`.
**When:** The user validates the name.
**Then:** The name is allowed if it is unique in `raw_files`.

### TS-006: Table name with spaces suggests underscore version
**Given:** The user enters a table name with spaces.
**When:** The field validates.
**Then:** The app suggests an underscore version and shows the final name before import.

## Error states

### TS-007: Database import failure preserves user choices
**Given:** The DB write fails.
**When:** The import attempt errors.
**Then:** Target schema, table name, mapping, and preview remain available for retry.

### TS-008: Target schema unavailable
**Given:** The selected schema/storage area is no longer available.
**When:** The user attempts import.
**Then:** Import is blocked and the user is linked to Storage Settings.

## Edge cases

### TS-009: Conversion warning is shown
**Given:** User-selected types conflict with previewed values.
**When:** Preview validates the mapping.
**Then:** A conversion warning is shown before import.

### TS-010: Very wide preview scrolls
**Given:** The mapping has more than 100 columns.
**When:** Preview is shown.
**Then:** The row preview remains usable with horizontal scroll.

### TS-011: Empty table import is allowed with warning
**Given:** The file has headers but 0 data rows.
**When:** Preview is shown.
**Then:** The app warns "Table will be empty (0 rows)" and allows import.

### TS-012: Changing schema revalidates table name
**Given:** The user has entered a valid table name in one schema.
**When:** The user changes target schema.
**Then:** The table name is rechecked in the new schema.

## Side effects

### TS-013: Cancel creates no table
**Given:** The user is on preview.
**When:** The user cancels.
**Then:** Temporary import state is cleared and no table/catalog entry is created.

---
*Frozen on: 2026-05-02*
