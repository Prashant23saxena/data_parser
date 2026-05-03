# Test Scenarios — F-SC-004: Browse & search catalog

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-02-schema-catalog/F-SC-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Browse & search catalog primary success path
**Given:** The app is configured and dependencies for F-SC-004 are available.
**When:** The user completes the main Browse & search catalog action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Browse & search catalog rejects invalid or missing required input
**Given:** The user is on the Browse & search catalog surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Edge cases

### TS-003: F-SC-004 edge case: Search is case-insensitive
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Search is case-insensitive
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-SC-004 edge case: Partial matches work ("ord" matches "sale_orders")
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Partial matches work ("ord" matches "sale_orders")
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-SC-004 edge case: Column search works ("partner_id" matches tables that contain a `partn
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Column search works ("partner_id" matches tables that contain a `partner_id` column)
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-SC-004 edge case: Filters combine: source=odoo AND query="partner" → only Odoo tables wi
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Filters combine: source=odoo AND query="partner" → only Odoo tables with "partner" in name
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-007: Search "order" → matching tables shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Search "order" → matching tables shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Search a column name → tables containing that column are shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Search a column name → tables containing that column are shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Filter by source "csv" → only CSV-imported tables shown
**Given:** The feature and dependencies are available.
**When:** Tester performs: Filter by source "csv" → only CSV-imported tables shown
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Clear filters → all tables visible
**Given:** The feature and dependencies are available.
**When:** Tester performs: Clear filters → all tables visible
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: No matches → "No tables match" message
**Given:** The feature and dependencies are available.
**When:** Tester performs: No matches → "No tables match" message
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
