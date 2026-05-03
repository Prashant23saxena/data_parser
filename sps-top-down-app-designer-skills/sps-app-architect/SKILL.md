---
name: sps-app-architect
description: Master orchestrator for the top-down app-design workflow. Reads the project's freeze-status.md and routes the user to the correct next skill — sps-vision-definer, sps-pillar-mapper, sps-feature-lister, sps-feature-detailer, sps-screen-planner, sps-mockup-painter, or sps-build-planner. Use when the user says "continue working on my app project", "where am I in {project}", "what's next for the {app-name} app", "let's keep building the spec for X", or any phrase that implies resuming or navigating an existing app-design project. Also handles loop progression (next pillar in L3, next feature in L4, next screen in L6) and revision routing (when a later layer flagged an earlier one as NEEDS_REVISION).
---

# App Architect

The master orchestrator. The user calls this skill whenever they want to make progress on an app-design project. It figures out where they are and runs the right next thing.

## When this skill runs

The user invokes it with phrases like:
- "Let's continue with my todo-app project"
- "Where am I in the {app-name} design?"
- "What's the next step?"
- "Resume {app-name}"
- "I want to keep working on the spec"

## Process

### Step 1 — Locate the project

Look at recent context to identify the project folder. If the user named it, find it. If not, ask:

> "Which project? I'll look for `00-meta/freeze-status.md`. You can give me the path or the name (I'll check `~/projects/`)."

If only one project exists in the default location, propose it.

### Step 2 — Read freeze-status.md

Read `{project-root}/00-meta/freeze-status.md` carefully. Parse:
- Status of each of L1–L7
- Loop progress tables (L3 per pillar, L4 per feature, L6 per screen)
- Any `NEEDS_REVISION` flags

### Step 3 — Determine next action

Apply this decision tree, in order:

1. **Any layer marked NEEDS_REVISION?**
   → Run that layer's skill in revise mode. (Most recent flag wins if multiple.)

2. **L1 PENDING?**
   → Run `sps-vision-definer`.

3. **L1 FROZEN, L2 not yet FROZEN?**
   → Run `sps-pillar-mapper`.

4. **L2 FROZEN, L3 has any pillar not yet FROZEN?**
   → Run `sps-feature-lister` with the next pending pillar as the target.

5. **All L3 pillars FROZEN, L4 has any feature not yet FROZEN?**
   → Run `sps-feature-detailer` with the next pending feature as the target.

6. **All L4 features FROZEN, L5 not yet FROZEN?**
   → Run `sps-screen-planner`.

7. **L5 FROZEN, L6 has any screen not yet FROZEN?**
   → Run `sps-mockup-painter` with the next pending screen as the target.

8. **All L6 screens FROZEN, L7 not yet FROZEN?**
   → Run `sps-build-planner`.

9. **L7 FROZEN, L8.1 not yet FROZEN?**
   → Run `sps-data-modeler`.

10. **L8.1 FROZEN, L8.2 not yet FROZEN?**
    → Run `sps-component-mapper`.

11. **L8.2 FROZEN, L8.3 not yet FROZEN (overall)?**
    → Run `sps-contract-definer` (per-contract freeze; user can pause and resume).

12. **L8.3 FROZEN overall, L8.4 not yet FROZEN?**
    → Run `sps-dependency-grapher`.

13. **L8.4 FROZEN, L8.5 not yet FROZEN?**
    → Run `sps-work-packager`.

14. **L8.5 FROZEN, L8.6 not yet FROZEN?**
    → Run `sps-integration-mapper`.

15. **L8.6 FROZEN, L8.7 not yet FROZEN?**
    → Run `sps-uat-scripter`.

16. **L8.7 FROZEN, L8.8 not yet FROZEN?**
    → Run `sps-agent-briefer` (FINAL design step).

17. **L8.8 FROZEN (everything FROZEN)?**
    → Design phase complete. Switch to **build monitoring mode**:
       - Read `00-meta/agent-claims.md` for current build progress.
       - Show user: "{X} of {N} WPs done. Critical path: {status}. Last activity: {tail of activity-log}."
       - Offer: "regenerate checklist, view OQs raised by agents, view recent activity, or pause."

### Step 4 — Show status and confirm

Before invoking the next skill, show the user a clean status snapshot:

```
=== {App Name} — Status ===

L1 Vision           ✓ frozen (v2)
L2 Pillars          ✓ frozen (v1) — 4 pillars defined
L3 Features         ⟳ in progress
   - onboarding     ✓ frozen (v1) — 6 features
   - content        ✓ frozen (v2) — 9 features
   - discovery      → NEXT
   - settings       … pending
L4 Specs            ⊘ blocked
L5 Screens          ⊘ blocked
L6 Mockups          ⊘ blocked
L7 Build            ⊘ blocked

Backlog summary: 8 active items across 3 layers

Next: sps-feature-lister for pillar "discovery"

Proceed? (yes / show backlog first / jump elsewhere / pause)
```

Symbols: ✓ frozen, ⟳ in progress, → next, … pending, ⊘ blocked, ⚠ needs revision.

### Step 5 — Handle the user's response

- **yes** → invoke the next skill, passing the project root path and any loop target (pillar name, feature ID, screen ID).
- **show backlog first** → invoke `sps-idea-parker` with cross-layer-view, then return to this prompt.
- **jump elsewhere** → ask which layer/iteration, validate it makes sense (e.g. can't jump to L4 if L3 isn't frozen), and route there.
- **pause** → save no state (freeze-status already has everything), tell the user how to resume.

## Invoking sub-skills

When invoking a vertical skill, pass:
- Project root path
- Mode: `fresh` (first time) or `revise` (NEEDS_REVISION) or `loop-next` (next iteration in L3/L4/L6)
- Loop target if applicable: pillar name, feature ID, or screen ID

## Loop handling rules

### L3 (sps-feature-lister, loops per pillar)

After L2 freezes, the freeze-status.md will list pillars. This skill picks the first one with status PENDING and routes to `sps-feature-lister`. After it returns, refresh status and route to the next pending pillar — or, if all pillars done, advance to L4.

Always offer the user a "skip this pillar for now / do them out of order" option. They might want to define discovery before content.

### L4 (sps-feature-detailer, loops per feature)

After every L3 pillar is frozen, the freeze-status.md will list every feature. Loop through, picking next pending. Same skip/reorder option.

### L6 (sps-mockup-painter, loops per screen)

After L5 freezes, screens are listed. Loop one by one.

## Revision handling

When a later layer flags an earlier one (e.g., `sps-mockup-painter` realizes L3 missed a feature), it sets `NEEDS_REVISION` on L3 with a note. Next time `sps-app-architect` runs, it sees the flag, routes to `sps-feature-lister` in revise mode, and the user updates that pillar (creating a new version, e.g. `v2.md`). Then downstream layers are also marked `NEEDS_REVISION` cascadingly — the user may need to update them too.

This is the cost of going back, and the architect is honest about it: "Updating L3/pillar-02 will likely require revising L4 specs that depend on it. Continue?"

## Critical rules

- **Never produce artifacts directly.** This skill only routes.
- **Always read freeze-status.md fresh** — never cache.
- **Always show status before routing** — the user should always know where they are.
- **Respect user override** — if they want to skip ahead or revisit, allow it (with warnings if it breaks the freeze chain).
- **Project root must contain `00-meta/freeze-status.md`** — if not, the project wasn't built by `sps-project-builder`. Tell the user to run `sps-project-builder` first.
