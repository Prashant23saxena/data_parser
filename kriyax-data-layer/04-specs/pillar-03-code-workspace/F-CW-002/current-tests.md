# Test Scenarios — F-CW-002: Show available tables

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 10  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-002/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Show available tables primary success path
**Given:** The app is configured and dependencies for F-CW-002 are available.
**When:** The user completes the main Show available tables action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Show available tables rejects invalid or missing required input
**Given:** The user is on the Show available tables surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-002 handles error:catalog-unavailable
**Given:** The feature can be forced into error:catalog-unavailable.
**When:** The triggering failure occurs.
**Then:** The error:catalog-unavailable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-CW-002 edge case: 100+ tables require search and scroll.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 100+ tables require search and scroll.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-CW-002 edge case: Refresh pulls latest catalog state.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Refresh pulls latest catalog state.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-CW-002 edge case: Clicking a table can insert load_table("table_name") into the editor.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Clicking a table can insert load_table("table_name") into the editor.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-007: Catalog tables appear in editor sidebar.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Catalog tables appear in editor sidebar.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Search by table name works.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Search by table name works.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Click table inserts load_table helper.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Click table inserts load_table helper.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Empty catalog message points user to connectors.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Empty catalog message points user to connectors.
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
