---
name: sps-mockup-painter
description: Layer 6 of the top-down app-design workflow. Creates a visual mockup for each screen — ASCII wireframe, HTML mockup, or generated image — so the user can see and feel the app before any code is written. Loops once per screen. Use after L5 is frozen, when sps-app-architect routes here for the next pending screen, or when the user says "mock up the {screen} screen", "let's design the visual for {screen}", "show me what {screen} would look like". Allows the user to spot flow problems and flag earlier layers as NEEDS_REVISION.
---

# Mockup Painter (Layer 6)

The sixth vertical layer. **Loops once per screen.** Produces a visual mockup per screen so flaws in the spec become visible *before* any code.

This is also the layer where "wait, this flow doesn't actually work" tends to surface. The skill explicitly supports flagging earlier layers as NEEDS_REVISION.

## Preconditions

- L5 must be `FROZEN`.
- Target screen must be in the L6 loop table with status `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`
- **Loop target: screen ID** (e.g. `S-01-home`)


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-mockup-painter`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Identify the screen

If no target was passed, read freeze-status.md L6 loop table. Default to the first PENDING.

Show user the next 3 pending screens, confirm.

### Step 2 — Load context for the screen

Read:
- `05-screens/current.md` → the section for this screen (purpose, pillar, features, states, in/out edges)
- For every feature on this screen, its `04-specs/{pillar}/{feature}/current.md` → states, inputs, error messages

> "Mocking up **S-01: Home**.
> Purpose: Landing + summary.
> Features on this screen: F-ON-005 (welcome banner), F-CO-001 (recent items list).
> States: logged out, logged in, loading."

### Step 3 — Choose fidelity and format

Ask:

> "Mockup fidelity for this screen?
> - **Low (ASCII wireframe)** — fast, no visual style, focuses on layout
> - **Medium (HTML wireframe)** — boxes/labels, light styling, in browser
> - **High (generated image)** — full visual, looks closer to a real design
>
> Default: start low, you can re-run at higher fidelity later. Pick one."

Also ask: "Per-state mockup or just primary state? Most users start with primary, then add states for tricky screens."

### Step 4 — Domain research (light)

**1-2 searches** for visual conventions specific to this screen type:
- "How do {domain} apps design their home screen"
- "Common layout for {screen type}"

Use only to inform layout choices, not to dictate.

### Step 5 — Draft the mockup

For each state being mocked:

**ASCII (low fidelity):**
```
+--------------------------------------------------+
| [☰]  AppName                            [👤]    |
+--------------------------------------------------+
|                                                  |
|  Welcome back, {name}                            |
|                                                  |
|  Recent items                                    |
|  +--------------------------------------------+  |
|  | • Item 1                          [→]      |  |
|  | • Item 2                          [→]      |  |
|  | • Item 3                          [→]      |  |
|  +--------------------------------------------+  |
|                                                  |
|              [ + New item ]                      |
|                                                  |
+--------------------------------------------------+
| [Home]  [Search]  [Profile]                      |
+--------------------------------------------------+
```

**HTML (medium):**
Generate a single self-contained HTML file with simple CSS. Use plain boxes, system fonts, light gray backgrounds. Save to mockups folder.

**Image (high):**
Use image generation if available. Prompt should include:
- App description from L1
- Screen purpose from L5
- Key elements present (from features and states)
- Style notes from L1 (tone)
- Format: "minimalist UI mockup, no logos, no real brand names"

Always call `sps-visual-maker` to handle the actual generation:
- type: `mockup`
- format: per fidelity choice
- content: structured screen description (elements, copy, states, style notes)
- output_path: `06-mockups/{screen-id}/v{N}-{state}.{ext}`

### Step 6 — Show + critique

Show the mockup to the user. Ask:

> "Does this match what you imagined? Anything wrong?"

Then explicitly probe for problems that L6 catches:

1. **Flow problems** — "Looking at this, is the next-step button in a sensible place? Does the path from here to the next screen feel natural?"
2. **Missing features** — "Are all the features you listed for this screen actually visible on it? Anything missing?"
3. **Spec gaps** — "Are there visible elements here that don't have a feature? If so, we missed a feature in L3."
4. **State coverage** — "Did we forget a state? E.g., the empty state, the offline state."

This is where NEEDS_REVISION often gets flagged.

### Step 7 — Handle revision flags

If the user identifies a problem in an earlier layer:

- "Missing feature" → flag the relevant pillar in L3 as `NEEDS_REVISION`. Cascade to L4 (any new feature needs a spec) and L5 (the new feature needs a screen home).
- "State missing" → flag the relevant feature in L4 as `NEEDS_REVISION`. Cascade to L5 if the new state needs a screen-level treatment.
- "Screen wrong" → flag L5 as `NEEDS_REVISION`.
- "Flow wrong" → could be L3 (feature dependency) or L5 (sitemap). Diagnose and flag.

When flagging, write a note in freeze-status.md describing what triggered it. Tell the user:

> "Flagged L4 / F-ON-001 as NEEDS_REVISION because we need to add an 'expired session' state. Run **sps-app-architect** to revise it, or continue mocking up other screens first."

### Step 8 — Synthesize and save

Write `06-mockups/{screen-id}/v{N}.md` (a markdown sidecar describing the mockup):

```markdown
# Mockup — {Screen ID}: {Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Fidelity:** ascii / html / image
**Files:**
- `v{N}-primary.{ext}` — primary state
- `v{N}-loading.{ext}` — loading state (if mocked)
- ...

## Screen ref

Linked to `05-screens/current.md` → S-XX

## Notes

{user feedback, design decisions, things to revisit}

## Revision flags raised

- {if any} flagged L4/F-XX-YYY for missing state
- ...

---

*Frozen on: {date when frozen}*
```

The actual visual files go in the same folder.

### Step 9 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L6 Mockup / {screen ID}
=================================================

  ✓ Mockup locked for {Screen Name}

    Fidelity: {ascii/html/image}
    States mocked: {count}
    {if any} Revision flags raised: {layer/IDs}

  → Next: next screen in L6, or advance to L7 when all
    screens are mocked. Resolve revision flags via
    sps-app-architect when convenient.

=================================================
```

Ask: "Freeze L6/{screen ID} at v{N}? (freeze / revise / backlog)"

### Step 10 — On freeze

1. Save mockup files + sidecar md with FROZEN status.
2. Update `06-mockups/{screen-id}/current.md` (or the equivalent pointer).
3. Update freeze-status.md:
   - This screen's row → `FROZEN`, v{N}.
   - **If this is the last pending screen:**
     - L6 → `FROZEN`.
     - L7 → `PENDING`.
   - Otherwise L6 stays `IN PROGRESS`.
4. Tell user: more screens or advance to L7.

## Backlog hook

Common parking moments at L6:
- Alternate visual styles ("let's also try a card layout")
- Animation / interaction details
- Visual polish for v2

Park to `06-mockups/backlog.md`.

## Critical rules

- **Don't write code.** This is mockups. HTML mockups are static visuals, not working interfaces.
- **Mock the primary state minimum.** Optional but valuable: error/empty/loading states.
- **Always probe for revision flags.** L6 is the natural place to catch L3-L5 mistakes.
- **One screen per run.** Don't mock multiple screens in one session.
- **Re-runs at higher fidelity are encouraged.** First pass ASCII for everything, then re-run problem screens at HTML/image.
- **Image generation must be brand-safe.** No real logos or brand names in prompts.
