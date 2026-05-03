# Spec — F-DC-002: Column detection and editable mapping

**Version:** v3
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-002
**Dependencies:** F-DC-001

## Summary

After file upload, parse headers and sample rows to suggest source columns, final column names, and data types. The system may infer defaults, but the user must be able to review and edit the final column name and final column type for every column before import continues.

This feature does **not** silently create a final schema. It produces a user-confirmed column mapping that F-DC-003 uses during preview and import.

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| parsed_file | internal | yes | — | from F-DC-001 success |
| sample_rows | int | no | 100 | 10-1000 |
| column_mapping | array | yes | system-suggested from file | at least 1 column; final names unique and valid |
| final_column_name | string | yes | source header sanitized for display | not blank; unique after normalization; max 64 chars |
| final_column_type | enum | yes | system-suggested type | text/integer/decimal/date/datetime/boolean |

## States

### detecting
System scans headers and sample rows. Spinner: "Reading file and suggesting columns..."

### mapping-ready
Column mapping table is visible. Each row shows source column, suggested final column name, suggested type, null count, sample values, and actions to edit name or change type.

### needs-rename
Duplicate or invalid final column names are detected. User must fix highlighted names before continuing. Message: "Some column names need attention. Rename highlighted columns to continue."

### type-review
User changes one or more suggested types. The mapping table updates and preview/import will use the user-selected type.

### error:no-columns
File has no parseable columns.
Message: "Could not detect any columns. Check the file format."

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| detecting | mapping-ready | parsing completes with at least one column | suggested mapping stored as draft |
| detecting | needs-rename | duplicate/invalid names found | problem columns highlighted |
| detecting | error:no-columns | 0 columns found | none |
| mapping-ready | type-review | user changes a column type | draft mapping updates |
| mapping-ready | needs-rename | user creates duplicate/blank/invalid name | continue disabled |
| needs-rename | mapping-ready | user fixes names | continue enabled if all validation passes |
| mapping-ready/type-review | F-DC-003 | user continues to preview | confirmed mapping passed forward |

## Edge cases

- Column names with spaces/special chars → show friendly name, validate final DB-safe name before import.
- Duplicate column names → user must rename; do not auto-suffix silently.
- Mixed types in a column → suggest text, but user can change type.
- Date ambiguity → suggest date/datetime with detected format note; user can change to text/date/datetime.
- Very wide files (100+ columns) → mapping table scrolls horizontally and vertically.
- Blank source header → suggest `column_1`, `column_2`, etc., and require user review.
- User changes type that conflicts with preview values → F-DC-003 should show conversion warnings before import.

## Side effects on success

- Stores a confirmed column mapping in temporary import state.
- Does not create a database table yet.
- Does not register anything in catalog yet.

## Failure recovery

No permanent mutation occurs in this feature. User can fix names/types and continue, or cancel to clear temporary import state.

## Acceptance checklist

- [ ] CSV with clear headers and types → mapping table shows suggested names/types.
- [ ] User can edit any column name.
- [ ] User can change any column type.
- [ ] Duplicate column names → user is asked to rename before continuing.
- [ ] Mixed int/string column → system suggests text, user can override.
- [ ] Blank/invalid column name → continue disabled until fixed.
- [ ] Confirmed mapping is passed to preview/import.

---
*Frozen on: 2026-05-02*
