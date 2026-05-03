---
name: sps-feature-detailer
description: Layer 4 of the top-down app-design workflow. For one feature at a time, defines every state, edge case, validation rule, error case, empty state, loading state, success/failure transitions — the smallest details so a developer (or your future self) can build it without ambiguity. Loops once per feature across all pillars. Use after L3 is fully frozen, when sps-app-architect routes here for the next pending feature, or when the user says "let's spec out feature {ID}", "detail the {feature} feature", "I want to define every state and edge case for X". Generates a state diagram per feature.
---

# Feature Detailer (Layer 4)

The fourth vertical layer. **Loops once per feature** (across every pillar). This is the layer where vague specs die — every state and edge case is named.

## Preconditions

- L3 must be fully `FROZEN` (every pillar in the loop table FROZEN).
- The target feature must be in the L4 loop table with status `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`
- **Loop target: pillar slug + feature ID** (e.g. `pillar-01-onboarding` / `F-ON-001`)


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-feature-detailer`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Identify the feature

If no target was passed, read freeze-status.md L4 loop table. Default to the first PENDING. Show the user the next 3 pending and confirm.

### Step 2 — Load context

- Read the feature's full entry from `03-features/{pillar}/current.md`. Show the user:
  - Feature name + description
  - Definition of done
  - Dependencies
  - Cross-pillar links

> "Detailing **F-ON-001: Sign up with email**. Definition of done: user can enter email + password, receive confirmation email, log in. Dependencies: none. Cross-pillar: links to F-CO-001 in content pillar (creates default workspace on signup)."

### Step 3 — Domain research

Do **2-4 searches** specific to the feature's domain:
- "Edge cases for {feature type}"
- "Common errors in {feature type}"
- "UX states for {feature type}"
- For UI features: "What states does {feature} typically have"

Examples for "Sign up with email":
- "Email signup edge cases"
- "Email validation rules"
- "Common signup errors"

Use this to populate a starter list of states and edge cases.

### Step 4 — Structured interview

**Q1. States.** "Walk me through every state this feature can be in."
Suggest from research: empty, loading, loaded, success, error, partial. Push for completeness:
- Initial / empty state — what's shown before any user input?
- Loading / in-flight state — when waiting for backend?
- Success state — what does the user see when it works?
- Error states — list every error type (validation, network, server, conflict, rate limit, etc.)
- Edge states — what about: very long input, slow connection, offline, conflict with another user, expired session, etc.?

**Q2. Inputs and validation.** For every input field/parameter:
- Field name, type
- Required? Default?
- Validation rules (format, length, range, allowed values)
- Validation error messages (the exact text)

**Q3. Transitions.** For each state pair, what triggers the transition?
- empty → loading: user clicks submit
- loading → success: server returns 200
- loading → error: server returns 4xx/5xx
- error → empty: user clicks retry / closes modal

**Q4. Edge cases (push hard here).** Ask domain-aware questions from research:
- "What if {edge case from research}?"
- "What if the user does X then Y in sequence?"
- "What if this happens twice quickly?"
- "What about accessibility — screen reader behavior?"
- "What about really small / really large screens?"

**Q5. Side effects.** "When this feature succeeds, what else changes?"
- Data written somewhere?
- Notification sent?
- Other features triggered? (cross-pillar)
- Logging / analytics events?

**Q6. Failure recovery.** "If this feature fails midway, what's the recovery? Idempotent retry? Manual cleanup? Surface an error and abandon?"

**Q7. Acceptance.** "How do you verify this feature works? List 3-5 specific test scenarios you'd run." This becomes the test checklist.

Allow "park this" — call `sps-idea-parker` with `scope: 04-specs/{pillar}/{feature}/backlog.md` (create if not exist).

### Step 5 — Synthesize draft

Write `04-specs/{pillar}/{feature}/v{N}.md`:

```markdown
# Spec — {Feature ID}: {Feature Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Pillar:** {pillar slug}
**Feature ref:** `03-features/{pillar}/current.md` → {Feature ID}
**Dependencies:** {list}

## Summary

{description from L3}

## Inputs

| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| email | string | yes | — | RFC 5322 format, max 254 chars |
| password | string | yes | — | min 12, requires letter+number |

## States

### empty
What the user sees before any action.

### loading
Triggered by: ...
Visual: ...

### success
...

### error: validation
Triggered by: invalid input
Visual: inline error messages, exact text:
- Empty email: "Email is required"
- Bad format: "That doesn't look like an email"
- ...

### error: network
...

### error: conflict
Triggered by: account exists with this email
Visual: ...

### {other states}
...

## Transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| empty | loading | user clicks Submit (after passing client validation) | none |
| loading | success | server returns 200 | account created, confirmation email sent |
| loading | error:network | request fails | retry button shown |
| ... | ... | ... | ... |

## Edge cases

- {edge case 1 + handling}
- {edge case 2 + handling}
- ...

## Side effects on success

- {effect 1}
- {effect 2 — cross-pillar to F-XX-YYY}

## Failure recovery

{strategy}

## Acceptance checklist

- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test scenario 3
- ...

---

*Frozen on: {date when frozen}*
```

Show the draft. Iterate.

### Step 6 — Visual

Call `sps-visual-maker`:
- type: `state-diagram`
- format: ask (default ASCII; HTML or image if many states)
- content: feature name + states + transitions
- output_path: `visuals/04-state-{pillar}-{feature-id}-v{N}.{ext}`

### Step 7 — Generate test scenarios (NEW — before freeze gate)

Before freezing this feature spec, invoke `sps-test-writer` in embedded mode:
- feature_ref: `{pillar}/{feature ID}`
- mode: embedded

The test writer reads this draft spec and produces a sibling `v{N}-tests.md` with test scenarios covering happy path, validation, errors, edge cases, state transitions, side effects, and negatives. The test file is version-locked to this spec.

If the test writer flags spec gaps (e.g. "this state has no observable trigger"), it raises a revision flag. Address those before freezing.

After tests are generated, show the user a summary count: "Generated {N} test scenarios across {M} categories. Coverage map confirms every spec section is tested."

### Step 8 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L4 Spec / {feature ID}
=================================================

  ✓ Spec locked for {Feature Name}

    States: {count}
    Edge cases: {count}
    Inputs: {count}
    Acceptance tests: {count}

  → Next: next feature in L4, or advance to L5 when all
    features are spec'd.

=================================================
```

Ask: "Freeze L4/{feature ID} at v{N}? (freeze / revise / backlog)"

### Step 9 — On freeze

1. Write `04-specs/{pillar}/{feature}/v{N}.md` with FROZEN status.
2. Also mark the sibling `v{N}-tests.md` as FROZEN (status copied from spec).
3. Update both `current.md` and `current-tests.md` (or equivalent pointer).
4. Update freeze-status.md:
   - This feature's row in L4 loop table → `FROZEN`, v{N}.
   - **If this is the last pending feature:**
     - L4 → `FROZEN`.
     - L5 → `PENDING`.
   - Otherwise L4 stays `IN PROGRESS`.
5. Call `sps-memory-keeper log-activity` with the freeze event.
6. Tell user what's next:
   - More features pending → "Next feature: {ID}. Run **sps-app-architect** or **sps-feature-detailer**."
   - L4 done → "All features spec'd (with tests). Run **sps-screen-planner** for L5."

## Backlog hook

Common parking moments at L4:
- Edge cases that are low-priority or out-of-scope for v1
- Questions about implementation ("should this use OAuth?") — park, decide at L7
- "What if we added X to this feature later" — park as a future enhancement

## Revision cascade

Revising L4 may invalidate L5/L6 (if states changed, screens may need new states; if inputs changed, mockups may need new fields). Mark downstream as `NEEDS_REVISION`.

## Critical rules

- **Be relentless about edge cases.** This is the layer that prevents "we forgot to handle X" pain later.
- **Exact error messages matter.** Don't accept "show an error" — get the actual text.
- **Acceptance checklist is mandatory.** It doubles as your test plan.
- **Cross-pillar side effects must be explicit.** They become integration tests.
- **One feature per run.** Don't merge multiple features.
- **Visual is mandatory** per feature.
