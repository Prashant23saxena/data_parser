# Test Scenarios — F-PS-001: Create pipeline

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-05-pipeline-scheduling/F-PS-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Create pipeline primary success path
**Given:** The app is configured and dependencies for F-PS-001 are available.
**When:** The user completes the main Create pipeline action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Create pipeline rejects invalid or missing required input
**Given:** The user is on the Create pipeline surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-PS-001 handles error:name-conflict
**Given:** The feature can be forced into error:name-conflict.
**When:** The triggering failure occurs.
**Then:** The error:name-conflict state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-PS-001 handles error:invalid-step
**Given:** The feature can be forced into error:invalid-step.
**When:** The triggering failure occurs.
**Then:** The error:invalid-step state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-PS-001 edge case: Script is required.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Script is required.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-PS-001 edge case: Connector pre-step is optional.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Connector pre-step is optional.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-PS-001 edge case: Pipeline stores references to script/connection ids.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Pipeline stores references to script/connection ids.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-PS-001 edge case: No schedule required at creation.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: No schedule required at creation.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Create pipeline with script only.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Create pipeline with script only.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Create pipeline with Odoo sync pre-step.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Create pipeline with Odoo sync pre-step.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Duplicate name rejected.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Duplicate name rejected.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Pipeline appears in list.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Pipeline appears in list.
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
