---
name: sps-feature-lister
description: Layer 3 of the top-down app-design workflow. For one pillar at a time, lists every feature inside that pillar with ID, name, description, dependencies, priority (must/should/could), and definition-of-done. This skill loops — once per pillar from L2. Use after L2 is frozen, when sps-app-architect routes here for the next pending pillar, or when the user says "let's list features for {pillar}", "break down the {pillar} pillar", "what features go inside {pillar}". Does domain research per pillar, runs an interview, generates a feature dependency graph, and freezes one pillar's features at a time. Seeds the L4 specs loop on freeze.
---

# Feature Lister (Layer 3)

The third vertical layer. **Loops once per pillar.** Each run defines all features inside one pillar. After all pillars are processed, L3 is fully frozen and L4 can begin.

## Preconditions

- L2 must be `FROZEN`.
- The target pillar must be in the L3 loop table with status `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`
- **Loop target: pillar slug** (e.g. `pillar-01-onboarding`) — passed by `sps-app-architect` or asked from user


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-feature-lister`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Identify the pillar

If no target was passed, read freeze-status.md and offer the user the list of pending pillars. Default to the first pending one.

> "L3 has these pillars pending: onboarding, discovery, settings. Default is **onboarding**. Continue, or pick another?"

### Step 2 — Load context

- Read `01-vision/current.md` (one-line summary).
- Read `02-pillars/current.md`, focus on the target pillar's section.
- Read existing features for previously-frozen pillars (briefly, just names) — useful to spot cross-pillar dependencies.

Show the user the pillar's purpose and in-scope/out-of-scope from L2 to anchor:

> "Pillar **onboarding**. Purpose: get a new user from zero to first useful action. In scope: signup, profile setup, tutorial. Out of scope: ongoing settings (those are in pillar settings)."

### Step 3 — Domain research

Do **3-5 searches** specific to this pillar's domain. Examples for an onboarding pillar of a habit tracker:
- "Onboarding flows in habit tracker apps"
- "Best practices for habit tracker first-run experience"
- "Common features in habit tracker signup"

Use this to suggest a candidate feature list. Don't dump search results.

### Step 4 — Structured interview

**Q1. Candidate list.** "Based on common patterns, I'm thinking these features for **{pillar}**: A, B, C, D, E. Which are right? Wrong? Missing?"

**Q2. For each accepted feature:**
- **Name:** short, action-oriented ("Sign up with email", not "Authentication")
- **Description:** 1-2 sentences. What it does, who triggers it.
- **Dependencies:** does this depend on another feature in this or another pillar? (Cross-pillar deps are fine, just note them with the pillar.)
- **Priority:** must / should / could
- **Definition of done:** when do we say this feature is "built"? One concrete sentence. (e.g. "User can enter email + password, receive confirmation email, and log in.")

**Q3. Coverage check against pillar in-scope.** Walk through L2's in-scope list for this pillar and verify each is covered by at least one feature.

**Q4. Out-of-scope drift.** Walk through L2's out-of-scope list for this pillar and verify no feature crosses into those.

**Q5. Cross-pillar links.** Any feature here that another pillar will need to know about? Note explicitly — this prevents L3 silos.

**Q6. Count check.** Pillars typically have 3-12 features. If 1-2, the pillar might be too small. If 15+, the pillar might be doing too much (consider revising L2).

Allow "park this" — call `sps-idea-parker` with `scope: 03-features/{pillar}/backlog.md` (create file if it doesn't exist).

### Step 5 — Synthesize draft

Write `03-features/{pillar}/v{N}.md`:

```markdown
# Features — {Pillar Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Pillar:** {pillar slug}, from `02-pillars/current.md`

## Feature index

| ID | Name | Priority | Depends on |
|---|---|---|---|
| F-{pillar-prefix}-001 | ... | must | — |
| F-{pillar-prefix}-002 | ... | must | F-...001 |
| ... | ... | ... | ... |

## Features

### F-{prefix}-001: {Name}

**Description:** ...

**Priority:** must / should / could

**Dependencies:** F-..., or "none"

**Definition of done:** ...

**Cross-pillar links:** {pillar} → {feature in another pillar}, if any

---

### F-{prefix}-002: {Name}
...

## Coverage map

| Pillar in-scope item | Covered by |
|---|---|
| signup | F-001, F-002 |
| ... | ... |

---

*Frozen on: {date when frozen}*
```

**Feature ID convention:** `F-{pillar-2-letter-prefix}-{3-digit-counter}`. Example: F-ON-001 (onboarding), F-CO-001 (content). The 2-letter prefix should be derivable from the pillar slug.

Show the draft. Iterate.

### Step 6 — Visual

Call `sps-visual-maker`:
- type: `feature-dep-graph`
- format: ask (default ASCII; HTML if more than 8 features)
- content: pillar name + features with deps
- output_path: `visuals/03-feature-dep-{pillar}-v{N}.{ext}`

### Step 7 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L3 Features / {pillar}
=================================================

  ✓ {N} features defined in pillar "{pillar}"

    Must-have: {count}
    Should-have: {count}
    Could-have: {count}

    Dependencies mapped, cross-pillar links noted.

  → Next: continue L3 with next pillar, or advance to L4
    when all pillars are done.

=================================================
```

Ask: "Freeze L3/{pillar} at v{N}? (freeze / revise / backlog)"

### Step 8 — On freeze

1. Write `03-features/{pillar}/v{N}.md` with status FROZEN.
2. Update `03-features/{pillar}/current.md`.
3. Update freeze-status.md:
   - This pillar's row in the L3 loop table → `FROZEN`, version `v{N}`.
   - **If this is the last pending pillar in L3:**
     - L3 overall → `FROZEN`.
     - L4 → `PENDING` (was BLOCKED).
     - **Seed the L4 loop table** — one row per (pillar, feature) pair across ALL pillars, all `PENDING`:
       ```
       | Pillar | Feature | Status | Version |
       |---|---|---|---|
       | onboarding | F-ON-001 | PENDING | — |
       | onboarding | F-ON-002 | PENDING | — |
       | content | F-CO-001 | PENDING | — |
       ...
       ```
   - Otherwise L3 stays `IN PROGRESS`.
4. Confirm to user. Tell them what's next:
   - If more pillars pending: "Run **sps-app-architect** or **sps-feature-lister** for next pillar: {next pillar}."
   - If L3 done: "All pillars frozen. {total features} features seeded into L4. Run **sps-feature-detailer** to begin Layer 4."

## Backlog hook

Most common parking moment in L3: "ooh, what about feature X" — but feature X is out of scope for this pillar or this version. Park to that pillar's backlog. If it's actually a different pillar's feature, park to *that* pillar's backlog.

## Revision cascade

Revising L3/{pillar} means dependent L4 specs may need updating. Mark them `NEEDS_REVISION` in the L4 loop table.

## Critical rules

- **One pillar per run.** Don't try to define multiple pillars' features in one session.
- **Every feature must have a definition of done.** Vague features are the failure mode.
- **Dependencies are mandatory.** Even "none" must be explicit.
- **Cross-pillar links are gold.** They prevent silos and surface integration points.
- **Don't go down to states/edge cases.** That's L4. Anything that looks like a state → park to backlog.
- **Always seed L4 loop table** on the last pillar's freeze.
- **Visual is mandatory** per pillar.
