# Test Scenarios — F-SC-005: Preview table rows

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-02-schema-catalog/F-SC-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Preview table rows primary success path
**Given:** The app is configured and dependencies for F-SC-005 are available.
**When:** The user completes the main Preview table rows action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Preview table rows rejects invalid or missing required input
**Given:** The user is on the Preview table rows surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-SC-005 handles error:table-not-found
**Given:** The feature can be forced into error:table-not-found.
**When:** The triggering failure occurs.
**Then:** The error:table-not-found state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-SC-005 handles error:preview-failed
**Given:** The feature can be forced into error:preview-failed.
**When:** The triggering failure occurs.
**Then:** The error:preview-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-SC-005 edge case: Very wide tables use horizontal scroll and sticky first column where p
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Very wide tables use horizontal scroll and sticky first column where practical.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-SC-005 edge case: Binary/blob columns show a placeholder rather than raw bytes.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Binary/blob columns show a placeholder rather than raw bytes.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-SC-005 edge case: Large text values are truncated in cells with expand-on-click later if
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Large text values are truncated in cells with expand-on-click later if needed.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-SC-005 edge case: Preview is read-only; no edits from this surface.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Preview is read-only; no edits from this surface.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Open an ingested CSV table and see first 50 rows.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Open an ingested CSV table and see first 50 rows.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Open a derived table and see first 50 rows.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Open a derived table and see first 50 rows.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Open a 0-row table and see an empty-table message with headers.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Open a 0-row table and see an empty-table message with headers.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Preview a wide table without layout breakage.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Preview a wide table without layout breakage.
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
