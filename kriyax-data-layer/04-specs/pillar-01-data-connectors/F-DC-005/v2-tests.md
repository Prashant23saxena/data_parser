# Test Scenarios — F-DC-005: Browse Odoo models & fields

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 14  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Browse Odoo models & fields primary success path
**Given:** The app is configured and dependencies for F-DC-005 are available.
**When:** The user completes the main Browse Odoo models & fields action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Browse Odoo models & fields rejects invalid or missing required input
**Given:** The user is on the Browse Odoo models & fields surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-005 handles error:connection-lost
**Given:** The feature can be forced into error:connection-lost.
**When:** The triggering failure occurs.
**Then:** The error:connection-lost state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-DC-005 edge case: Odoo instance with 500+ models → paginated/virtual-scroll list, search
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Odoo instance with 500+ models → paginated/virtual-scroll list, search is essential
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-DC-005 edge case: Model with 100+ fields → scrollable field list
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Model with 100+ fields → scrollable field list
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DC-005 edge case: Relational fields (many2one, one2many, many2many) → show related model
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Relational fields (many2one, one2many, many2many) → show related model name and clearly mark how each relation can be fetched/imported
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-005 edge case: Computed/read-only fields → show when Odoo metadata exposes this
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Computed/read-only fields → show when Odoo metadata exposes this
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DC-005 edge case: Required fields and field labels → show alongside technical names so b
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Required fields and field labels → show alongside technical names so both humans and the agent can understand the model
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Connect to Odoo → model list loads
**Given:** The feature and dependencies are available.
**When:** Tester performs: Connect to Odoo → model list loads
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Search "sale" → filters to sale.order, sale.order.line, etc.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Search "sale" → filters to sale.order, sale.order.line, etc.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Click model → fields displayed with types
**Given:** The feature and dependencies are available.
**When:** Tester performs: Click model → fields displayed with types
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Relational fields show target model information
**Given:** The feature and dependencies are available.
**When:** Tester performs: Relational fields show target model information
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Field labels, technical names, required flags, and available read-only/computed hints are visible
**Given:** The feature and dependencies are available.
**When:** Tester performs: Field labels, technical names, required flags, and available read-only/computed hints are visible
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Select fields and click Fetch → hands off to F-DC-006
**Given:** The feature and dependencies are available.
**When:** Tester performs: Select fields and click Fetch → hands off to F-DC-006
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
