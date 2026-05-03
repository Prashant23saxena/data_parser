# Test Scenarios — F-DC-002: Column detection and editable mapping

**Spec version:** v3
**Generated:** 2026-05-02
**Status:** FROZEN
**Total scenarios:** 12
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-002/v3.md

## Happy path

### TS-001: Suggest columns and types from uploaded file
**Given:** A CSV/Excel file has been uploaded successfully.
**When:** The system scans headers and sample rows.
**Then:** The mapping table shows source column, final column name, suggested type, null count, and sample values.

### TS-002: Confirm mapping and continue
**Given:** All final column names and types are valid.
**When:** The user continues.
**Then:** The confirmed mapping is passed to F-DC-003 and no table is created yet.

## Validation

### TS-003: Duplicate final column names block continue
**Given:** Two columns normalize to the same final name.
**When:** The mapping table is shown.
**Then:** The duplicate names are highlighted and continue is disabled until the user renames them.

### TS-004: Blank or invalid final column name blocks continue
**Given:** A final column name is blank or invalid.
**When:** The user attempts to continue.
**Then:** The action is blocked with a clear inline error.

### TS-005: User can edit any column name
**Given:** The mapping table is visible.
**When:** The user changes a final column name.
**Then:** The updated name is validated and saved into the draft mapping.

### TS-006: User can change any column type
**Given:** The mapping table is visible.
**When:** The user changes a column type.
**Then:** The selected type is saved into the draft mapping.

## Error states

### TS-007: No parseable columns
**Given:** The uploaded file has no parseable columns.
**When:** Detection runs.
**Then:** The user sees "Could not detect any columns. Check the file format."

## Edge cases

### TS-008: Mixed-type column suggests text
**Given:** A column contains both numeric and text values.
**When:** Detection runs.
**Then:** The suggested type is text, and the user can override it.

### TS-009: Ambiguous date format is visible
**Given:** A date column includes ambiguous values.
**When:** Detection runs.
**Then:** The suggested type/format note is visible, and the user can change the type.

### TS-010: Very wide file remains usable
**Given:** A file has more than 100 columns.
**When:** The mapping table is shown.
**Then:** The table can be scrolled and all columns can be reviewed.

### TS-011: Blank source headers receive suggested names
**Given:** One or more source headers are blank.
**When:** Detection runs.
**Then:** Suggested names like `column_1` are shown and require validation.

## Side effects

### TS-012: No permanent mutation before preview/import
**Given:** The user completes mapping.
**When:** The feature hands off to preview.
**Then:** No database table or catalog entry has been created yet.

---
*Frozen on: 2026-05-02*
