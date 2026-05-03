---
name: sps-screen-planner
description: Layer 5 of the top-down app-design workflow. Defines every screen the app needs, the sitemap (which screen goes where), navigation between screens, and which features live on which screen. Use after L4 is fully frozen, when sps-app-architect routes here, or when the user says "let's plan the screens", "what screens does the app need", "build the sitemap", "map features to screens". Generates a sitemap visual and a navigation flow chart, then seeds the L6 mockup loop.
---

# Screen Planner (Layer 5)

The fifth vertical layer. Bridges the abstract feature world (L3/L4) to the visual world (L6). Every feature must live on at least one screen.

## Preconditions

- L4 must be fully `FROZEN` (every feature in the loop table FROZEN).
- L5 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-screen-planner`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Greet and load full context

Read:
- `01-vision/current.md` (one-line)
- `02-pillars/current.md` (pillar list)
- All `03-features/{pillar}/current.md` (every feature)
- All `04-specs/{pillar}/{feature}/current.md` (full specs — needed because screens map to states)

Show user a summary:

> "Loaded {N} features across {P} pillars. Now we map them to screens and define navigation."

### Step 2 — Domain research

**3-5 searches** for screen patterns and information architecture in this domain:
- "Information architecture for {domain} apps"
- "Common screens in {domain} apps"
- "Navigation patterns for {domain} apps"
- "Mobile vs desktop screen structure for {domain}"

Use this to suggest a candidate screen list and a default nav pattern (tabs / sidebar / drawer / single-page).

### Step 3 — Structured interview

**Q1. Platform.** "What platforms? Web (desktop / mobile-responsive) / iOS / Android / multiple?" This shapes nav patterns and screen count.

**Q2. Top-level navigation pattern.** "How does the user move between major areas? Suggest based on research:
- Bottom tabs (mobile-first)
- Sidebar (desktop-first)
- Drawer
- Single-page
- Other"

Map nav to pillars typically — each top-level destination tends to be a pillar or a combination.

**Q3. Candidate screen list.** Based on research and pillar structure, propose a screen list. For each:
- Screen name
- Purpose (one line)
- Which pillar(s) does it serve
- Which features live on it (from L3)

Iterate with the user. Add, remove, rename.

**Q4. Feature-to-screen mapping.** Walk through every feature in L3 and confirm which screen(s) it lives on. Flag features that don't have a home — either add a screen or revise.

**Q5. Screen states (high-level).** From L4 specs, surface state-driven screens. E.g., a "details" screen has loaded / loading / not-found / error variants. List them.

**Q6. Navigation flows (key paths).** "Walk me through 3-5 critical user flows." Examples:
- First-run: open app → onboarding → main → first action
- Daily use: open app → main → primary action → confirmation
- Recovery: forgot password → reset email → enter new password → back to login

For each flow, list the screen sequence.

**Q7. Modals vs full screens.** Decide which interactions are modals/sheets/popovers vs dedicated screens. Common rule: short interruptions = modal, long flows = screen.

**Q8. Empty / error / loading screens.** Are these dedicated screens or in-screen states? Make this consistent.

Allow "park this" — call `sps-idea-parker` with `scope: 05-screens/backlog.md`.

### Step 4 — Synthesize draft

Write `05-screens/v{N}.md`:

```markdown
# Screens — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}

## Platform

{platforms}

## Top-level navigation

**Pattern:** {tabs / sidebar / drawer / single-page}
**Destinations:**
1. {Dest 1} → {pillar(s)}
2. {Dest 2} → {pillar(s)}
...

## Screen index

| ID | Name | Purpose | Pillar(s) | Features | Type |
|---|---|---|---|---|---|
| S-01 | Home | Landing + summary | onboarding, content | F-ON-005, F-CO-001 | full screen |
| S-02 | Sign up | New account flow | onboarding | F-ON-001 | full screen |
| S-03 | Confirm delete | Destructive action confirm | (any) | — | modal |
| ... | ... | ... | ... | ... | ... |

## Sitemap

```
Home (S-01)
├── Sign up (S-02)
│   └── Verify email (S-04)
├── Login (S-03)
│   └── Forgot password (S-05)
└── Main app
    ├── ...
```
(this section will be visualized separately)

## Screens

### S-01: Home
**Purpose:** ...
**Pillar:** ...
**Features:** F-ON-001, ...
**States shown:** logged out / logged in / loading
**Type:** full screen
**Reachable from:** (entry), S-03, S-04
**Goes to:** S-02, S-03, S-06

### S-02: Sign up
...

## Critical user flows

### Flow 1: First-run signup
S-01 → S-02 → S-04 → S-06 (main)

### Flow 2: Daily use
S-06 (main) → S-08 (action) → S-09 (confirmation)

### Flow 3: Forgot password
S-03 → S-05 → email → S-07 → S-03

## Coverage check

| Feature | On screen(s) |
|---|---|
| F-ON-001 | S-02 |
| F-ON-002 | S-04 |
| ... | ... |

(no feature should be unmapped)

---

*Frozen on: {date when frozen}*
```

Show draft. Iterate.

### Step 5 — Visuals (two of them)

**Visual A — Sitemap.** Call `sps-visual-maker`:
- type: `sitemap`
- format: ask (ASCII default; HTML if more than 12 screens)
- content: screen list + parent-child relationships
- output_path: `visuals/05-sitemap-v{N}.{ext}`

**Visual B — Critical flow charts.** Call `sps-visual-maker` for each critical flow (or one combined):
- type: `flow-chart`
- format: ask
- content: ordered screen sequences with branches
- output_path: `visuals/05-flow-{flow-name}-v{N}.{ext}`

### Step 6 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L5 Screens
=================================================

  ✓ {N} screens defined for {App Name}

    Platform: {platforms}
    Nav pattern: {pattern}
    Critical flows mapped: {count}

    Every feature mapped to at least one screen ✓

  → Next: L6, mockups for each screen ({N} loop iterations)

=================================================
```

Ask: "Freeze L5 at v{N}? (freeze / revise / backlog)"

### Step 7 — On freeze

1. Write `05-screens/v{N}.md` with FROZEN status.
2. Update `05-screens/current.md`.
3. Update freeze-status.md:
   - L5 → `FROZEN`, v{N}.
   - L6 → `PENDING`.
   - **Seed the L6 loop table** — one row per screen, all `PENDING`:
     ```
     | Screen | Status | Version |
     |---|---|---|
     | S-01-home | PENDING | — |
     | S-02-signup | PENDING | — |
     ...
     ```
4. Tell user: "L5 frozen. {N} screens seeded into L6. Run **sps-mockup-painter** to begin Layer 6."

## Coverage rule (hard)

Before freezing, every feature in L3 must appear in the screen-feature mapping table. If any are missing, push back: "Feature F-XX-YYY isn't on any screen. Add it to a screen, or this is a gap."

## Backlog hook

Common parking moments at L5:
- Alternative nav patterns to try later
- Screens for v2 of the app
- Variant layouts (e.g., "compact mode")

## Revision cascade

Revising L5 invalidates L6 (mockups depend on screens). Mark all L6 entries as `NEEDS_REVISION`.

## Critical rules

- **Every feature must map to a screen.** No exceptions.
- **Modal vs screen distinction must be consistent.** Document the rule.
- **Critical flows are mandatory.** At least 3.
- **Two visuals (sitemap + flow chart).** Both required.
- **Always seed L6 loop table** on freeze.
