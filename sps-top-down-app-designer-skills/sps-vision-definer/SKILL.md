---
name: sps-vision-definer
description: Layer 1 of the top-down app-design workflow. Locks the app's vision — purpose, target user, core promise, success criteria, and (critically) non-goals — into a frozen v1.md before any other layer can run. Use when starting a new app project after sps-project-builder has scaffolded it, or when sps-app-architect routes here, or when the user says "let's define the vision", "lock down what this app is", "freeze the purpose", "I want to start defining my app". Performs light domain research, runs a structured interview, allows parking ideas to backlog via sps-idea-parker, generates a pitch-box visual via sps-visual-maker, and freezes the layer in freeze-status.md.
---

# Vision Definer (Layer 1)

The first vertical layer. Produces a one-page, frozen vision doc that every subsequent layer reads.

## Preconditions

- Project root must exist with `00-meta/freeze-status.md`. If not, route the user to `sps-project-builder` first.
- L1 status in freeze-status.md must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`. If `FROZEN`, ask the user if they want to revise (creating a new version).

## Inputs

- Project root path
- Mode: `fresh` or `revise`


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-vision-definer`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Greet and orient

Read `00-meta/project-name.md` to get the app name and one-liner. Greet:

> "Starting Layer 1: Vision Lock for **{app-name}**. We'll define purpose, user, promise, success criteria, and non-goals. By the end you'll freeze a v1.md that every later layer reads. Ready?"

If `revise` mode: read existing `01-vision/current.md`, summarize it, ask what's changing.

### Step 2 — Domain research

Do **1-2 web searches** to sharpen domain-specific questions. Examples:
- Search the app concept ("note-taking app", "habit tracker", whatever) to see common patterns.
- Search for "common mistakes when defining {domain} apps" or competitor positioning.

Use the results internally to generate sharper questions in Step 3. Don't dump search results on the user.

### Step 3 — Structured interview

Ask the user, one question at a time. Allow "park this" as a valid answer to anything (then call `sps-idea-parker` to add to `01-vision/backlog.md`).

**Q1. The problem.** "What's the actual problem this app solves? Describe it as the user feeling it, not as a feature." Probe if the answer is feature-shaped ("X but better"). Push for the underlying pain.

**Q2. The user.** "Who specifically uses this? Just you? You + people like you? A specific role?" Note: since they're building for themselves, "me" is a valid answer — but push for "me when X" (context).

**Q3. The promise.** "If someone uses this for a week, what's different about their life? One sentence." This is the core value prop.

**Q4. Success criteria.** "How will you know this app is working for you? Be concrete — daily usage? Specific outcome? A feeling?"

**Q5. Non-goals (most important).** "What is this app explicitly NOT? List 3-5 things. This is the most useful boundary you'll set."
- Domain-aware prompts based on research: "Many {domain} apps drift into doing X — is that on or off the table?"
- Push back if the list is empty. A vision without non-goals is leaky.

**Q6. Tone / feel.** "If this app were a personality — calm, sharp, playful, professional — what?" Skip if the user finds this too abstract.

**Q7. Anchors / inspiration.** "Apps you love that this should feel like? Apps you hate that this should NOT be like?"

### Step 4 — Synthesize draft

Write a draft of `v{N}.md` (v1 if fresh, v2/v3 if revise). Use this template:

```markdown
# Vision — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}

## The Problem

{from Q1}

## The User

{from Q2}

## The Promise

{from Q3 — one sentence in bold}

## Success Criteria

- {item 1}
- {item 2}
- ...

## Non-Goals

This app is explicitly **NOT**:
- {item 1}
- {item 2}
- ...

## Tone

{from Q6 — short phrase}

## Anchors

**Like:** {apps loved}
**Unlike:** {apps disliked}

---

*Frozen on: {date when frozen}*
```

Show the draft to the user. Ask: "Does this match? Anything to change before we visualize and freeze?"

Iterate until the user is satisfied.

### Step 5 — Generate visual

Call `sps-visual-maker` with:
- type: `pitch-box`
- format: ask user (default ASCII)
- content: derived from the draft (name, promise, user, non_goals)
- output_path: `visuals/01-pitch-box-v{N}.{ext}`

Show it inline.

### Step 6 — Freeze gate

Generate the freeze-gate story summary via `sps-visual-maker` (type: `story-summary`):

```
=================================================
  FREEZE GATE — L1 Vision
=================================================

  ✓ Vision locked for {App Name}

    For: {user}
    Promise: {promise}
    Not: {non_goals[0]}, {non_goals[1]}...

  → Next: L2, define 4-7 pillars (high-level capabilities)

=================================================
```

Ask the user:

> "Freeze L1 at v{N}? Options:
> - **freeze** — lock it, advance to L2
> - **revise** — keep editing
> - **backlog** — park something before freezing"

### Step 7 — On freeze

1. Write `01-vision/v{N}.md` with status changed from DRAFT to FROZEN, add freeze date.
2. Update (or create) `01-vision/current.md` to point to / contain v{N}.md content.
3. Update `00-meta/freeze-status.md`: L1 status → `FROZEN`, version → `v{N}`, last-updated → today.
4. Confirm: "L1 frozen at v{N}. Run **sps-app-architect** or **sps-pillar-mapper** to start L2."

## Backlog hook

At any interview question, the user can say "park this", "backlog it", "remember this for later". Call `sps-idea-parker` with:
- scope: `01-vision/backlog.md`
- type: `question` or `idea` based on context
- title: the user's words
- priority: ask quickly ("parking / maybe / promote-soon?")

Then continue the interview where you left off.

## Critical rules

- **Don't skip non-goals.** They're the highest-leverage part of L1. If the user resists, push gently.
- **Don't go deeper than vision.** No features, no screens, no implementation. Anything that's lower-level → park to backlog.
- **Always create a new version on revise.** Never overwrite `v1.md`.
- **Always update freeze-status.md on freeze.** This is the contract with `sps-app-architect`.
- **Visual is mandatory.** Even if simple ASCII pitch-box. Don't skip.
