---
name: sps-pillar-mapper
description: Layer 2 of the top-down app-design workflow. Defines the 4-7 high-level pillars (capability areas) that the app delivers. Each pillar gets a name, a one-sentence purpose, in-scope items, and out-of-scope items. Use after L1 (vision) is frozen, when sps-app-architect routes here, or when the user says "let's define the pillars", "what are the main capability areas", "break this into top-level chunks". Searches the domain for typical pillar patterns, runs a structured interview, generates a pillar-tree visual, and freezes the layer — also seeding the L3 loop progress table in freeze-status.md.
---

# Pillar Mapper (Layer 2)

The second vertical layer. Produces the high-level capability tree — the "first split" of the app into 4-7 pillars. Every feature in L3 must belong to a pillar.

## Preconditions

- L1 must be `FROZEN` in `freeze-status.md`.
- L2 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

If L1 isn't frozen, route the user to `sps-vision-definer`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-pillar-mapper`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Greet and load context

Read `01-vision/current.md`. Summarize the vision back to the user in 2 lines so the conversation is anchored:

> "From L1: this app is for **{user}**, promises **{promise}**, and is explicitly NOT **{non_goals[:2]}**. Now we define the pillars."

If `revise` mode: read existing `02-pillars/current.md`, show it, ask what's changing.

### Step 2 — Domain research

Do **2-3 searches** to understand typical pillar structures for this domain. Examples:
- "Main features of {domain} apps"
- "How {competitor} structures their app"
- "Capability areas in {domain} apps"

Use this to suggest a starting set of pillars (3-5 candidates) rather than asking the user cold.

### Step 3 — Structured interview

**Q1. Starting set.** Show the candidate pillars from research:

> "Based on similar apps, common pillars for this kind of tool are: A, B, C, D, E. Which feel right? Which are wrong? Anything missing?"

Don't anchor too hard — it's a starting point, not a prescription.

**Q2. Refine names.** For each pillar the user accepted, ask for a clear short name (1-3 words).

**Q3. Purpose per pillar.** For each pillar:
- "One sentence — what does this pillar give the user?"
- Push for outcome language, not implementation.

**Q4. In-scope per pillar.** "Inside this pillar, what kinds of things live? (don't list features yet — just categories.)" 3-5 items per pillar.

**Q5. Out-of-scope per pillar.** "What might naturally creep in but doesn't belong here?" Especially valuable when pillars overlap.

**Q6. Coverage check.** "Look at this list. Is everything in your vision covered by at least one pillar? Any pillar that doesn't trace back to the vision?"
- Flag orphan pillars (no vision link) — either drop them or revise vision.
- Flag vision items with no pillar — add or extend a pillar.

**Q7. Count check.** Aim for 4-7 pillars. If they have 10+, push to consolidate. If 2-3, push to split. Justify based on cognitive load (pillars are how the user remembers the app's shape).

Allow "park this" at any point — call `sps-idea-parker` with `scope: 02-pillars/backlog.md`.

### Step 4 — Synthesize draft

Write `v{N}.md`:

```markdown
# Pillars — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Vision:** linked to `01-vision/current.md` (v{X})

## Pillar 1: {Name}

**Purpose:** {one sentence}

**In scope:**
- ...
- ...

**Out of scope:**
- ...

## Pillar 2: {Name}
...

## Coverage Map

| Vision element | Covered by pillar(s) |
|---|---|
| {promise component 1} | Pillar 1, 3 |
| {success criterion 1} | Pillar 2 |
| ... | ... |

---

*Frozen on: {date when frozen}*
```

Show to user. Iterate.

### Step 5 — Visual

Call `sps-visual-maker`:
- type: `pillar-tree`
- format: ask (default ASCII; suggest HTML if more than 5 pillars)
- content: app name + list of pillars with purposes
- output_path: `visuals/02-pillar-tree-v{N}.{ext}`

### Step 6 — Freeze gate

Story summary via `sps-visual-maker` (type: `story-summary`):

```
=================================================
  FREEZE GATE — L2 Pillars
=================================================

  ✓ Defined {N} pillars for {App Name}

    1. {Pillar 1}
    2. {Pillar 2}
    ...

  → Next: L3, feature lists per pillar (loops {N} times)

=================================================
```

Ask: "Freeze L2 at v{N}? (freeze / revise / backlog)"

### Step 7 — On freeze

1. Write `02-pillars/v{N}.md` with status FROZEN.
2. Update `02-pillars/current.md`.
3. Update `00-meta/freeze-status.md`:
   - L2 → `FROZEN`, version `v{N}`.
   - L3 → `PENDING` (was BLOCKED).
   - Populate the **L3 Features (per pillar)** loop progress table — one row per pillar, all `PENDING`:
     ```
     | Pillar | Status | Version |
     |---|---|---|
     | onboarding | PENDING | — |
     | content | PENDING | — |
     ...
     ```
4. Confirm: "L2 frozen at v{N}. {N} pillars seeded into L3 loop. Run **sps-app-architect** or **sps-feature-lister** to begin L3."

## Pillar naming convention

For folder names in `03-features/` and `04-specs/`, use: `pillar-XX-{slug}` where XX is a 2-digit zero-padded index and slug is the pillar name lowercased with hyphens. Example: `pillar-01-onboarding`. The L3 loop table in freeze-status uses the same slug.

## Backlog hook

Park-to-backlog at any interview question. Common cases at L2:
- "Should this be a pillar or a feature inside another?" → park as a question
- "Maybe a future pillar but not now" → park as an idea

## Revision cascade

If revising L2, downstream layers (L3, L4, L5, L6, L7) may also need revision. After freezing the new version:
- Mark all downstream FROZEN entries as `NEEDS_REVISION` in freeze-status.
- Tell the user: "L2 changes will likely require updates to L3-L7 — `sps-app-architect` will route you through them when you continue."

## Critical rules

- **4-7 pillars.** Hard ceiling at 8. If they want more, almost certainly some are features, not pillars.
- **Every pillar must trace to vision.** No orphans.
- **Don't drop into features yet.** Park feature-level thoughts to backlog.
- **Always seed the L3 loop table** on freeze. This is what enables L3 to know what to iterate over.
- **Visual is mandatory.**
