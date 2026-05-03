# Test Scenarios — F-DC-002: Auto-detect columns & types

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 13  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-002/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Auto-detect columns & types primary success path
**Given:** The app is configured and dependencies for F-DC-002 are available.
**When:** The user completes the main Auto-detect columns & types action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Auto-detect columns & types rejects invalid or missing required input
**Given:** The user is on the Auto-detect columns & types surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-002 handles error:no-columns
**Given:** The feature can be forced into error:no-columns.
**When:** The triggering failure occurs.
**Then:** The error:no-columns state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-DC-002 edge case: Column names with spaces/special chars → preserve as-is, sanitize only
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Column names with spaces/special chars → preserve as-is, sanitize only for DB column names later
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-DC-002 edge case: Duplicate column names → ask user to rename duplicates before continui
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Duplicate column names → ask user to rename duplicates before continuing; do not auto-suffix silently
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DC-002 edge case: Mixed types in column (some rows int, some string) → default to string
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Mixed types in column (some rows int, some string) → default to string
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-002 edge case: Date format ambiguity (01/02/2024 = Jan 2 or Feb 1?) → default to loca
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Date format ambiguity (01/02/2024 = Jan 2 or Feb 1?) → default to locale-aware and show detected format for review
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DC-002 edge case: Very wide files (100+ columns) → show scrollable table, no limit
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Very wide files (100+ columns) → show scrollable table, no limit
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: CSV with clear headers and types → types detected correctly
**Given:** The feature and dependencies are available.
**When:** Tester performs: CSV with clear headers and types → types detected correctly
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: CSV with mixed int/string column → defaults to string
**Given:** The feature and dependencies are available.
**When:** Tester performs: CSV with mixed int/string column → defaults to string
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Excel with dates → date type detected
**Given:** The feature and dependencies are available.
**When:** Tester performs: Excel with dates → date type detected
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Detected types are shown for review without manual override controls
**Given:** The feature and dependencies are available.
**When:** Tester performs: Detected types are shown for review without manual override controls
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: File with duplicate column names → user is asked to rename duplicates before continuing
**Given:** The feature and dependencies are available.
**When:** Tester performs: File with duplicate column names → user is asked to rename duplicates before continuing
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
