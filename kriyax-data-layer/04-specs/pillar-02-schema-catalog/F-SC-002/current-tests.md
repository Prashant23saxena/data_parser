# Test Scenarios — F-SC-002: Column metadata viewer

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 8  
**Spec file:** 04-specs/pillar-02-schema-catalog/F-SC-002/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Column metadata viewer primary success path
**Given:** The app is configured and dependencies for F-SC-002 are available.
**When:** The user completes the main Column metadata viewer action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Error states

### TS-002: F-SC-002 handles error:table-gone
**Given:** The feature can be forced into error:table-gone.
**When:** The triggering failure occurs.
**Then:** The error:table-gone state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-003: F-SC-002 edge case: Table with 200+ columns → scrollable, no limit
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Table with 200+ columns → scrollable, no limit
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-SC-002 edge case: Column with unknown nullable status → show "unknown"
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Column with unknown nullable status → show "unknown"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-SC-002 edge case: Binary/blob columns → show type and description only; values are not s
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Binary/blob columns → show type and description only; values are not shown here
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-006: Click table → columns displayed with correct types
**Given:** The feature and dependencies are available.
**When:** Tester performs: Click table → columns displayed with correct types
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-007: Column descriptions are shown when available
**Given:** The feature and dependencies are available.
**When:** Tester performs: Column descriptions are shown when available
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: No sample row values are shown in this metadata view
**Given:** The feature and dependencies are available.
**When:** Tester performs: No sample row values are shown in this metadata view
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
