# Test Scenarios — F-DS-005: Export table data

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-06-data-storage/F-DS-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Export table data primary success path
**Given:** The app is configured and dependencies for F-DS-005 are available.
**When:** The user completes the main Export table data action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Export table data rejects invalid or missing required input
**Given:** The user is on the Export table data surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DS-005 handles error:table-not-found
**Given:** The feature can be forced into error:table-not-found.
**When:** The triggering failure occurs.
**Then:** The error:table-not-found state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DS-005 handles error:export-failed
**Given:** The feature can be forced into error:export-failed.
**When:** The triggering failure occurs.
**Then:** The error:export-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-DS-005 edge case: Large exports stream/chunk rather than loading all into memory.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Large exports stream/chunk rather than loading all into memory.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DS-005 edge case: 0-row table exports headers.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 0-row table exports headers.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DS-005 edge case: File name uses table name plus timestamp.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: File name uses table name plus timestamp.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Export small table downloads CSV.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Export small table downloads CSV.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Export 0-row table downloads headers.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Export 0-row table downloads headers.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Export large table completes without memory crash.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Export large table completes without memory crash.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Missing table shows error.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Missing table shows error.
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
