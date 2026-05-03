# Test Scenarios — F-DC-006: Fetch Odoo records to table

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 15  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-006/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Fetch Odoo records to table primary success path
**Given:** The app is configured and dependencies for F-DC-006 are available.
**When:** The user completes the main Fetch Odoo records to table action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Fetch Odoo records to table rejects invalid or missing required input
**Given:** The user is on the Fetch Odoo records to table surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-006 handles error:fetch-failed
**Given:** The feature can be forced into error:fetch-failed.
**When:** The triggering failure occurs.
**Then:** The error:fetch-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DC-006 handles error:import-failed
**Given:** The feature can be forced into error:import-failed.
**When:** The triggering failure occurs.
**Then:** The error:import-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-DC-006 edge case: Model with 0 records → success with warning: "0 records found matching
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Model with 0 records → success with warning: "0 records found matching your filter"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DC-006 edge case: Model with 100k+ records → batched fetch with progress, may take minut
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Model with 100k+ records → batched fetch with progress, may take minutes
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-006 edge case: Odoo session timeout mid-fetch → retry with re-auth
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Odoo session timeout mid-fetch → retry with re-auth
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DC-006 edge case: Relational fields (many2one) → import as ID value + display_name (two 
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Relational fields (many2one) → import as ID value + display_name (two columns)
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-DC-006 edge case: Relational fields (one2many/many2many) → do not flatten deeply in v1; 
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Relational fields (one2many/many2many) → do not flatten deeply in v1; show warning and skip unless explicitly supported later
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-010: Fetch res.partner with all fields → table created with correct data
**Given:** The feature and dependencies are available.
**When:** Tester performs: Fetch res.partner with all fields → table created with correct data
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Fetch selected fields from a large Odoo model → only selected fields are imported
**Given:** The feature and dependencies are available.
**When:** Tester performs: Fetch selected fields from a large Odoo model → only selected fields are imported
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Fetch with domain filter [["customer","=",true]] → only matching records
**Given:** The feature and dependencies are available.
**When:** Tester performs: Fetch with domain filter [["customer","=",true]] → only matching records
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Fetch model with 0 records → success with warning
**Given:** The feature and dependencies are available.
**When:** Tester performs: Fetch model with 0 records → success with warning
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Table name conflict → error requires a new unique table name
**Given:** The feature and dependencies are available.
**When:** Tester performs: Table name conflict → error requires a new unique table name
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-015: Large fetch (10k+ records) → progress shown, completes successfully
**Given:** The feature and dependencies are available.
**When:** Tester performs: Large fetch (10k+ records) → progress shown, completes successfully
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
