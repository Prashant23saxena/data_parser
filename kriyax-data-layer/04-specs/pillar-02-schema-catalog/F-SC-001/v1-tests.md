# Test Scenarios — F-SC-001: Table registry

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-02-schema-catalog/F-SC-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Table registry primary success path
**Given:** The app is configured and dependencies for F-SC-001 are available.
**When:** The user completes the main Table registry action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Table registry rejects invalid or missing required input
**Given:** The user is on the Table registry surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-SC-001 handles error:db-unreachable
**Given:** The feature can be forced into error:db-unreachable.
**When:** The triggering failure occurs.
**Then:** The error:db-unreachable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-SC-001 edge case: 100+ tables → paginated list (25 per page) with search
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: 100+ tables → paginated list (25 per page) with search
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-SC-001 edge case: Table with 0 rows → show normally, row count = 0
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Table with 0 rows → show normally, row count = 0
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-SC-001 edge case: Table source unknown (created outside platform) → source = "external"
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Table source unknown (created outside platform) → source = "external"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-SC-001 edge case: Registry refresh after import → auto-refresh when navigating to catalo
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Registry refresh after import → auto-refresh when navigating to catalog page
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Import a CSV → table appears in registry with correct metadata
**Given:** The feature and dependencies are available.
**When:** Tester performs: Import a CSV → table appears in registry with correct metadata
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Fetch from Odoo → table appears with source "odoo"
**Given:** The feature and dependencies are available.
**When:** Tester performs: Fetch from Odoo → table appears with source "odoo"
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Save from code workspace → table appears with source "derived"
**Given:** The feature and dependencies are available.
**When:** Tester performs: Save from code workspace → table appears with source "derived"
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: No tables → empty state shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: No tables → empty state shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Search by table name → filters correctly
**Given:** The feature and dependencies are available.
**When:** Tester performs: Search by table name → filters correctly
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
