# Test Scenarios — F-DC-001: Upload CSV/Excel file

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 17  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Upload CSV/Excel file primary success path
**Given:** The app is configured and dependencies for F-DC-001 are available.
**When:** The user completes the main Upload CSV/Excel file action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Upload CSV/Excel file rejects invalid or missing required input
**Given:** The user is on the Upload CSV/Excel file surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-001 handles error:invalid-format
**Given:** The feature can be forced into error:invalid-format.
**When:** The triggering failure occurs.
**Then:** The error:invalid-format state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DC-001 handles error:too-large
**Given:** The feature can be forced into error:too-large.
**When:** The triggering failure occurs.
**Then:** The error:too-large state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-DC-001 handles error:corrupt
**Given:** The feature can be forced into error:corrupt.
**When:** The triggering failure occurs.
**Then:** The error:corrupt state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-006: F-DC-001 handles error:empty-file
**Given:** The feature can be forced into error:empty-file.
**When:** The triggering failure occurs.
**Then:** The error:empty-file state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-007: F-DC-001 edge case: **Empty CSV (headers only, no rows):** Accept it — 0-row table is vali
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: **Empty CSV (headers only, no rows):** Accept it — 0-row table is valid. Show warning: "File has column headers but no data rows."
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DC-001 edge case: **CSV with no headers:** Detect heuristically (first row looks like da
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: **CSV with no headers:** Detect heuristically (first row looks like data, not headers). Show toggle: "First row is headers / First row is data." Default to headers.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-DC-001 edge case: **Excel with 20+ sheets:** Show scrollable sheet list. No limit on she
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: **Excel with 20+ sheets:** Show scrollable sheet list. No limit on sheet count.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-010: F-DC-001 edge case: **File with special characters in name:** Accept any filename. Sanitiz
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: **File with special characters in name:** Accept any filename. Sanitize for display only, never use filename as table name (user chooses table name later in F-DC-003).
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-011: F-DC-001 edge case: **Duplicate upload of same filename:** Allow it — treat as a new uploa
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: **Duplicate upload of same filename:** Allow it — treat as a new upload. No conflict with previous imports.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-012: Upload a valid .csv file via Browse button (OS file explorer opens) → success
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a valid .csv file via Browse button (OS file explorer opens) → success
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Upload a valid .xlsx file via drag-and-drop → success
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a valid .xlsx file via drag-and-drop → success
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Upload a multi-sheet .xlsx → sheet picker appears, select sheet → success
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a multi-sheet .xlsx → sheet picker appears, select sheet → success
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-015: Upload a .pdf → error:invalid-format shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a .pdf → error:invalid-format shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-016: Upload a 150MB file → error:too-large shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a 150MB file → error:too-large shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-017: Upload a corrupt Excel file → error:corrupt shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Upload a corrupt Excel file → error:corrupt shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

## Coverage map

| Spec area | Covered by scenarios |
|---|---|
| Inputs and validation | Validation scenarios plus acceptance scenarios |
| States and transitions | Happy path, error state, and acceptance scenarios |
| Edge cases | Edge case scenarios |
| Side effects and recovery | Happy path, negative, and error state scenarios |

## Gaps

- None identified at draft-test generation time. User validation may add more scenarios.

---
*Frozen on: 2026-05-02*
