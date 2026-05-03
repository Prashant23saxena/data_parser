# Test Scenarios — F-DS-003: Persist derived tables

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-06-data-storage/F-DS-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Persist derived tables primary success path
**Given:** The app is configured and dependencies for F-DS-003 are available.
**When:** The user completes the main Persist derived tables action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Persist derived tables rejects invalid or missing required input
**Given:** The user is on the Persist derived tables surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DS-003 handles error:invalid-dataframe
**Given:** The feature can be forced into error:invalid-dataframe.
**When:** The triggering failure occurs.
**Then:** The error:invalid-dataframe state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DS-003 handles error:write-failed
**Given:** The feature can be forced into error:write-failed.
**When:** The triggering failure occurs.
**Then:** The error:write-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-DS-003 handles error:catalog-sync
**Given:** The feature can be forced into error:catalog-sync.
**When:** The triggering failure occurs.
**Then:** The error:catalog-sync state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-006: F-DS-003 edge case: Derived table replace is separate from connector import behavior.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Derived table replace is separate from connector import behavior.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DS-003 edge case: Rollback previous table where supported if replace fails.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Rollback previous table where supported if replace fails.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DS-003 edge case: Catalog sync failure is surfaced but table can remain saved.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Catalog sync failure is surfaced but table can remain saved.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Save derived DataFrame creates table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Save derived DataFrame creates table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Replace derived table updates rows/schema.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Replace derived table updates rows/schema.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Failure does not corrupt old table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Failure does not corrupt old table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Catalog reflects derived source.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Catalog reflects derived source.
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
