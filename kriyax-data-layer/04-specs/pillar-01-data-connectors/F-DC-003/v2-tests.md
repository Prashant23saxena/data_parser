# Test Scenarios — F-DC-003: Preview before import

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Preview before import primary success path
**Given:** The app is configured and dependencies for F-DC-003 are available.
**When:** The user completes the main Preview before import action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Preview before import rejects invalid or missing required input
**Given:** The user is on the Preview before import surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-003 handles error:name-conflict
**Given:** The feature can be forced into error:name-conflict.
**When:** The triggering failure occurs.
**Then:** The error:name-conflict state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DC-003 handles error:import-failed
**Given:** The feature can be forced into error:import-failed.
**When:** The triggering failure occurs.
**Then:** The error:import-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-DC-003 edge case: Table name with spaces → auto-replace with underscores
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Table name with spaces → auto-replace with underscores
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DC-003 edge case: Very wide preview (100+ columns) → horizontal scroll
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Very wide preview (100+ columns) → horizontal scroll
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-003 edge case: 0-row import (headers only) → allow, show warning: "Table will be empt
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 0-row import (headers only) → allow, show warning: "Table will be empty (0 rows)"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Preview shows correct data and types → user clicks Import → table created
**Given:** The feature and dependencies are available.
**When:** Tester performs: Preview shows correct data and types → user clicks Import → table created
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: User changes table name → new name used
**Given:** The feature and dependencies are available.
**When:** Tester performs: User changes table name → new name used
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Existing table name → error:name-conflict, user must choose a new table name
**Given:** The feature and dependencies are available.
**When:** Tester performs: Existing table name → error:name-conflict, user must choose a new table name
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Cancel → returns to upload area, no table created
**Given:** The feature and dependencies are available.
**When:** Tester performs: Cancel → returns to upload area, no table created
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
