# Spec — F-DC-001: Upload CSV/Excel file

**Version:** v1
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** `03-features/pillar-01-data-connectors/current.md` → F-DC-001
**Dependencies:** none

## Summary

User uploads a local CSV or Excel file via a "Browse" button (opens OS file explorer), drag-and-drop, or file picker. Supports .csv, .xlsx, .xls formats. Handles multiple sheets in Excel (user picks which sheet to import).

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| file | File | yes | — | .csv, .xlsx, .xls only; max 100MB |
| sheet_name | string | only for multi-sheet Excel | first sheet | must match an existing sheet name |

## States

### empty
Upload area with drag-and-drop zone and a **"Browse Files"** button. Text: "Drag a CSV or Excel file here, or click Browse to select from your computer." No file selected yet.

### file-selected
File chosen via browse dialog or drag-drop. System validates file extension before proceeding. Shows filename, size, and type. Brief validation spinner.

### sheet-picker
Excel file has multiple sheets. Show a dropdown/list of sheet names. User selects which sheet to import. Default: first sheet. "Continue" button to proceed.

### uploading
File is being read and parsed server-side. Show progress bar or spinner with text: "Reading file…"

### success
File accepted and parsed. Hand off to F-DC-002 (auto-detect columns & types). Text: "File loaded successfully. Detecting columns…"

### error:invalid-format
Triggered by: user selects a file that is not .csv, .xlsx, or .xls (e.g., .pdf, .json, .txt).
Visual: red banner — "Unsupported file format. Please upload a .csv, .xlsx, or .xls file."
Recovery: user can select a different file. Upload area remains active.

### error:too-large
Triggered by: file exceeds 100MB.
Visual: red banner — "File too large ({{size}}MB). Maximum allowed: 100MB."
Recovery: user can select a smaller file.

### error:corrupt
Triggered by: file can't be parsed (broken encoding, corrupt Excel, binary garbage).
Visual: red banner — "Unable to read this file. It may be corrupted or in an unsupported encoding. Try re-exporting from the source."
Recovery: user can select a different file.

### error:empty-file
Triggered by: file has 0 bytes or no parseable content.
Visual: red banner — "This file appears to be empty."
Recovery: select a different file.

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| empty | file-selected | user clicks Browse and selects file, OR drags file onto drop zone | file reference stored temporarily |
| file-selected | error:invalid-format | file extension not in (.csv, .xlsx, .xls) | none |
| file-selected | error:too-large | file size > 100MB | none |
| file-selected | sheet-picker | file is .xlsx/.xls AND has multiple sheets | sheet list extracted |
| file-selected | uploading | file is .csv OR single-sheet Excel | parsing begins |
| sheet-picker | uploading | user selects sheet and clicks Continue | selected sheet stored |
| uploading | success | parsing completes without error | hand off to F-DC-002 |
| uploading | error:corrupt | parsing fails | none |
| uploading | error:empty-file | file parsed but 0 rows/columns found | none |
| error:* | empty | user clicks "Try another file" | previous file reference cleared |

## Edge cases

- **Empty CSV (headers only, no rows):** Accept it — 0-row table is valid. Show warning: "File has column headers but no data rows."
- **CSV with no headers:** Detect heuristically (first row looks like data, not headers). Show toggle: "First row is headers / First row is data." Default to headers.
- **Excel with 20+ sheets:** Show scrollable sheet list. No limit on sheet count.
- **File with special characters in name:** Accept any filename. Sanitize for display only, never use filename as table name (user chooses table name later in F-DC-003).
- **Duplicate upload of same filename:** Allow it — treat as a new upload. No conflict with previous imports.
- **Very large file (50-100MB):** Show progress indicator during parsing. Consider chunked reading.
- **CSV with mixed delimiters:** Auto-detect delimiter (comma, semicolon, tab, pipe). If ambiguous, default to comma.
- **Excel with formulas:** Read computed values, not formulas. If cell has error (#REF, #N/A), import as null.
- **File encoding:** Auto-detect UTF-8, Latin-1, Windows-1252. If unreadable, show error:corrupt.

## Side effects on success

- File content stored temporarily for F-DC-002 (column detection) and F-DC-003 (preview).
- No database table created yet — that happens after preview confirmation (F-DC-003 → F-DS-002).

## Failure recovery

All errors are recoverable — user selects a different file. No partial state to clean up. Upload area resets to empty state on "Try another file."

## Acceptance checklist

- [ ] Upload a valid .csv file via Browse button (OS file explorer opens) → success
- [ ] Upload a valid .xlsx file via drag-and-drop → success
- [ ] Upload a multi-sheet .xlsx → sheet picker appears, select sheet → success
- [ ] Upload a .pdf → error:invalid-format shown
- [ ] Upload a 150MB file → error:too-large shown
- [ ] Upload a corrupt Excel file → error:corrupt shown
- [ ] Upload an empty .csv (0 bytes) → error:empty-file shown
- [ ] Upload a CSV with semicolon delimiter → auto-detected, success
- [ ] Upload a CSV with headers-only (0 rows) → success with warning

---

*Frozen on: 2026-05-02*
