# Test Scenarios — F-CW-004: Save DataFrame as table

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 14  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Save DataFrame as table primary success path
**Given:** The app is configured and dependencies for F-CW-004 are available.
**When:** The user completes the main Save DataFrame as table action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Save DataFrame as table rejects invalid or missing required input
**Given:** The user is on the Save DataFrame as table surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-004 handles error:invalid-dataframe
**Given:** The feature can be forced into error:invalid-dataframe.
**When:** The triggering failure occurs.
**Then:** The error:invalid-dataframe state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-CW-004 handles error:invalid-table-name
**Given:** The feature can be forced into error:invalid-table-name.
**When:** The triggering failure occurs.
**Then:** The error:invalid-table-name state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-CW-004 handles error:db-write
**Given:** The feature can be forced into error:db-write.
**When:** The triggering failure occurs.
**Then:** The error:db-write state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-006: F-CW-004 handles error:catalog-sync
**Given:** The feature can be forced into error:catalog-sync.
**When:** The triggering failure occurs.
**Then:** The error:catalog-sync state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-007: F-CW-004 edge case: Empty DataFrame with columns creates 0-row table.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Empty DataFrame with columns creates 0-row table.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-CW-004 edge case: Duplicate columns are rejected.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Duplicate columns are rejected.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-CW-004 edge case: Unsupported nested object columns are rejected with offending column w
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Unsupported nested object columns are rejected with offending column where possible.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-010: F-CW-004 edge case: Catalog sync failure does not roll back successful DB write.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Catalog sync failure does not roll back successful DB write.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-011: Save valid DataFrame creates table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Save valid DataFrame creates table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Save same name replaces derived table if mode stays approved.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Save same name replaces derived table if mode stays approved.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Invalid table name fails before DB write.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Invalid table name fails before DB write.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Catalog updates after save.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Catalog updates after save.
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
