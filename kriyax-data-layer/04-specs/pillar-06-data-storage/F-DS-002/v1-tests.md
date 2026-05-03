# Test Scenarios — F-DS-002: Auto-create tables on import

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 13  
**Spec file:** 04-specs/pillar-06-data-storage/F-DS-002/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Auto-create tables on import primary success path
**Given:** The app is configured and dependencies for F-DS-002 are available.
**When:** The user completes the main Auto-create tables on import action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Auto-create tables on import rejects invalid or missing required input
**Given:** The user is on the Auto-create tables on import surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DS-002 handles error:name-conflict
**Given:** The feature can be forced into error:name-conflict.
**When:** The triggering failure occurs.
**Then:** The error:name-conflict state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DS-002 handles error:schema-invalid
**Given:** The feature can be forced into error:schema-invalid.
**When:** The triggering failure occurs.
**Then:** The error:schema-invalid state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-DS-002 handles error:write-failed
**Given:** The feature can be forced into error:write-failed.
**When:** The triggering failure occurs.
**Then:** The error:write-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-006: F-DS-002 edge case: Connector imports do not overwrite existing tables.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Connector imports do not overwrite existing tables.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DS-002 edge case: 0-row table with columns is allowed.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 0-row table with columns is allowed.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DS-002 edge case: Duplicate columns must already be resolved before this feature.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Duplicate columns must already be resolved before this feature.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-DS-002 edge case: Type conversion failures surface clear column-specific errors where po
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Type conversion failures surface clear column-specific errors where possible.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-010: CSV import creates new table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: CSV import creates new table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Odoo fetch creates new table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Odoo fetch creates new table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Existing name is rejected.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Existing name is rejected.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: 0-row confirmed import creates empty table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: 0-row confirmed import creates empty table.
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
