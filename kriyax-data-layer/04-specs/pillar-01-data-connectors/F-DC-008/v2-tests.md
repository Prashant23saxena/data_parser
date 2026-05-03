# Test Scenarios — F-DC-008: Manage saved connections

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 9  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-008/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Manage saved connections primary success path
**Given:** The app is configured and dependencies for F-DC-008 are available.
**When:** The user completes the main Manage saved connections action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Manage saved connections rejects invalid or missing required input
**Given:** The user is on the Manage saved connections surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Edge cases

### TS-003: F-DC-008 edge case: Delete a connection used by a pipeline → warn: "This connection is use
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Delete a connection used by a pipeline → warn: "This connection is used by pipeline '{{pipeline_name}}'. Deleting will break it."
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-DC-008 edge case: Edit URL and re-test → must pass test before save
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Edit URL and re-test → must pass test before save
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-DC-008 edge case: No connections → show empty-list state with link to add
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: No connections → show empty-list state with link to add
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-006: View list of saved connections → shows all with correct details
**Given:** The feature and dependencies are available.
**When:** Tester performs: View list of saved connections → shows all with correct details
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-007: Edit a connection's API key → save works, re-test passes
**Given:** The feature and dependencies are available.
**When:** Tester performs: Edit a connection's API key → save works, re-test passes
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Delete a connection → removed from list
**Given:** The feature and dependencies are available.
**When:** Tester performs: Delete a connection → removed from list
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Delete connection used by pipeline → warning shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Delete connection used by pipeline → warning shown
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
