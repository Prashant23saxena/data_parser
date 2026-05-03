# Test Scenarios — F-CW-003: Load tables as DataFrames

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Load tables as DataFrames primary success path
**Given:** The app is configured and dependencies for F-CW-003 are available.
**When:** The user completes the main Load tables as DataFrames action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Load tables as DataFrames rejects invalid or missing required input
**Given:** The user is on the Load tables as DataFrames surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-003 handles error:table-not-found
**Given:** The feature can be forced into error:table-not-found.
**When:** The triggering failure occurs.
**Then:** The error:table-not-found state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-CW-003 handles error:column-not-found
**Given:** The feature can be forced into error:column-not-found.
**When:** The triggering failure occurs.
**Then:** The error:column-not-found state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-CW-003 handles error:db-connection
**Given:** The feature can be forced into error:db-connection.
**When:** The triggering failure occurs.
**Then:** The error:db-connection state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-006: F-CW-003 edge case: 0-row table returns empty DataFrame with columns.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 0-row table returns empty DataFrame with columns.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-CW-003 edge case: Very large tables warn when loading all rows.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Very large tables warn when loading all rows.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-CW-003 edge case: Column names with spaces are still accessible through DataFrame bracke
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Column names with spaces are still accessible through DataFrame bracket syntax.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: load_table on existing table returns DataFrame.
**Given:** The feature and dependencies are available.
**When:** Tester performs: load_table on existing table returns DataFrame.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Missing table returns clear error with available tables.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Missing table returns clear error with available tables.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Optional column subset loads only those columns.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Optional column subset loads only those columns.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: 0-row table returns columns.
**Given:** The feature and dependencies are available.
**When:** Tester performs: 0-row table returns columns.
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
