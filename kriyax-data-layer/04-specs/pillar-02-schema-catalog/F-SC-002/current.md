# Spec — F-SC-002: Column metadata viewer

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-02-schema-catalog
**Feature ref:** F-SC-002
**Dependencies:** F-SC-001

## Summary
Click any table in the registry to view its column metadata: column name, data type, nullable status, and description when available. Actual row values are handled by F-SC-005 Preview table rows.

## States

### loading
Fetching column metadata. Spinner: "Loading columns…"

### detail-view
Column table displayed: name, type, nullable status, and description when available. Table name as header.

### error:table-gone
Table was deleted between listing and detail view.
Message: "Table '{{name}}' no longer exists."

## Edge cases
- Table with 200+ columns → scrollable, no limit
- Column with unknown nullable status → show "unknown"
- Binary/blob columns → show type and description only; values are not shown here

## Acceptance checklist
- [ ] Click table → columns displayed with correct types
- [ ] Column descriptions are shown when available
- [ ] No sample row values are shown in this metadata view

---
*Frozen on: 2026-05-02*
