# Test Scenarios — F-DS-004: Basic table management

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-06-data-storage/F-DS-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Basic table management primary success path
**Given:** The app is configured and dependencies for F-DS-004 are available.
**When:** The user completes the main Basic table management action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Basic table management rejects invalid or missing required input
**Given:** The user is on the Basic table management surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DS-004 handles error:operation-failed
**Given:** The feature can be forced into error:operation-failed.
**When:** The triggering failure occurs.
**Then:** The error:operation-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DS-004 handles error:dependency-warning
**Given:** The feature can be forced into error:dependency-warning.
**When:** The triggering failure occurs.
**Then:** The error:dependency-warning state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-DS-004 edge case: Drop/truncate require typed confirmation or strong modal.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Drop/truncate require typed confirmation or strong modal.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DS-004 edge case: Rename validates uniqueness.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Rename validates uniqueness.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DS-004 edge case: Protected internal metadata tables cannot be modified.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Protected internal metadata tables cannot be modified.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DS-004 edge case: Pipelines/scripts referencing a table should warn before destructive a
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Pipelines/scripts referencing a table should warn before destructive action.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Rename table updates catalog.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Rename table updates catalog.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Truncate clears rows keeps schema.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Truncate clears rows keeps schema.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Drop removes table after confirmation.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Drop removes table after confirmation.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Protected tables cannot be dropped.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Protected tables cannot be dropped.
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
