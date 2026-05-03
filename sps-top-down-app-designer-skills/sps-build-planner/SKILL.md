---
name: sps-build-planner
description: Layer 7 of the top-down app-design workflow — the final layer. Decides tech stack, sequences the build into phases (thin slice first, then depth), identifies risks, and produces a build plan that turns the frozen spec into a buildable roadmap. Use after L6 is fully frozen, when sps-app-architect routes here, or when the user says "now let's plan how to build this", "what tech stack should I use", "give me a build plan", "what do I build first". Searches current tech stack norms, runs an interview, generates a build timeline visual, and freezes the project — at which point the design is fully done and implementation can begin.
---

# Build Planner (Layer 7)

The seventh and final vertical layer. Converts the frozen spec into a build sequence the user can actually execute.

## Preconditions

- L6 must be fully `FROZEN` (every screen in the loop table FROZEN).
- L7 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Scope note (important)

L7 is the **what + when + risks + stack** layer:
- Tech stack
- Build phases (calendar / time-budget oriented)
- Thin slice definition
- Risks and mitigations
- Definition of v1 shipped

L7 is NOT the *how* layer. The detailed implementation architecture (data model, components, contracts, dependency graph, work packages, integration tests, UAT, agent instructions) is **L8**, a sub-pipeline of 8 sub-skills that runs after L7 freezes.

L7's phases will be referenced by L8's work packages and dependency graph. Keep L7 high-level and trust L8 to detail the rest.

If during the L7 interview the user wants to dive into specific architectural questions ("what should the data model look like?"), park those — they belong in L8.1 onwards.

## Inputs

- Project root path
- Mode: `fresh` or `revise`


## Memory integration (mandatory)

At the start of every run, call `sps-memory-keeper read-context` with caller=`sps-build-planner`. The snapshot tells you which layers are frozen, what decisions have been made, what's in the glossary, what open questions affect this layer, and which references have been harvested.

During the run, call:
- `sps-memory-keeper add-glossary` whenever a new project-specific term is introduced
- `sps-memory-keeper record-decision` when a meaningful decision is locked
- `sps-memory-keeper raise-question` when something must be parked unresolved
- `sps-memory-keeper log-activity` at start and at freeze

## References (read if available)

If `00-meta/references/index.md` exists and lists harvested sources, read those references during the domain-research step. They are project-specific and outweigh generic web search for this domain. Reminder: references are for completeness checks, not scope definition. The vision (L1) is still the boss.

## Process

### Step 1 — Greet and load full context

Read everything frozen:
- L1 vision (purpose, non-goals)
- L2 pillars
- L3 features (every pillar's features)
- L4 specs (states, edge cases — needed for risk assessment)
- L5 screens (sitemap, flows)
- L6 mockups (just confirm they exist; the visuals already informed L5/L6)

> "Loaded full spec for {App Name}. {N} pillars, {M} features, {S} screens, {F} mockups. Now we plan the build."

### Step 2 — Domain research

**3-5 searches** for current tech stack norms and build patterns:
- "Best tech stack for {app type} in {current year}"
- "Solo developer building a {app type}"
- "Common pitfalls when building {app type}"
- "MVP vs full build for {app type}"

Important: searches should be current-year-aware. The user is building this now.

### Step 3 — Structured interview

**Q1. Build context.** "Solo build or team? Time budget? Hard deadline?"

**Q2. Tech stack constraints.** "Any languages, frameworks, or platforms you're committed to (or want to avoid)?"

**Q3. Tech stack recommendation.** Based on research and answers:
- Frontend: ...
- Backend: ...
- Database: ...
- Auth: ...
- Hosting / deployment: ...
- Monitoring: ...

Justify each pick in one sentence. Allow the user to override anything.

**Q4. Thin slice definition.** "What's the minimum end-to-end working version that proves the core promise from L1?"
This is the first build phase. It should:
- Cover at least one critical user flow from L5
- Use only `must` features from L3
- Skip polish, edge cases, and most error states

**Q5. Phasing.** Group features/screens into phases:
- **Phase 1: Thin slice** — end-to-end happy path
- **Phase 2: Robustness** — error states, edge cases from L4, retry/recovery
- **Phase 3: Should-have features** — round out the app
- **Phase 4: Polish + could-haves** — animations, settings, edge UX

For each phase: features included, screens included, rough effort estimate (days/weeks).

**Q6. Risks and unknowns.** Walk through the spec and flag:
- Features with unclear technical solution
- Features depending on external services (APIs, third parties)
- Features with security/privacy implications
- Cross-pillar links that look hard
For each risk: mitigation or "spike" (timeboxed exploration) before committing.

**Q7. Definition of "done" for the project.** "What does shipped v1 look like? Which features must be working? Which are explicitly v2?"
This separates `must` from `could` honestly.

**Q8. Order of pillars to build.** Within each phase, which pillar to tackle first? Suggest based on dependencies (from L3 cross-pillar links). Often: foundation pillars (auth, data) first, then user-facing pillars.

Allow "park this" — call `sps-idea-parker` with `scope: 07-build/backlog.md`.

### Step 4 — Synthesize draft

Write `07-build/v{N}.md`:

```markdown
# Build Plan — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}

## Context

- Solo / team: {...}
- Time budget: {...}
- Deadline: {...}

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | ... | ... |
| Backend | ... | ... |
| Database | ... | ... |
| Auth | ... | ... |
| Hosting | ... | ... |
| Monitoring | ... | ... |

## Project layout (suggested)

```
app-root/
├── frontend/...
├── backend/...
├── shared/...
└── ...
```

## Phases

### Phase 1: Thin slice — {estimate}

**Goal:** End-to-end happy path proving the core promise.

**Critical flow covered:** {flow name from L5}

**Features:** F-ON-001, F-ON-002, F-CO-001 (must-haves only)
**Screens:** S-01, S-02, S-06 (primary state only)
**Skipped intentionally:** error states, edge cases (Phase 2)

**Definition of done for this phase:**
- {scenario 1 works}
- {scenario 2 works}

### Phase 2: Robustness — {estimate}

**Goal:** Make Phase 1 production-grade.

**Adds:** error states, validation, retry flows, edge cases from L4.
**Features touched:** all Phase 1 features (deepened)
**Screens touched:** add error / loading / empty states

### Phase 3: Should-have features — {estimate}

**Adds:** features with priority `should` from L3.
...

### Phase 4: Polish & could-haves — {estimate}

**Adds:** features with priority `could`, animations, refinements.
...

## Risks

| # | Risk | Layer | Mitigation |
|---|---|---|---|
| R1 | OAuth integration unclear | F-ON-001 | Spike: 1 day evaluating Auth0 vs Clerk |
| R2 | Sync conflict handling | F-CO-005 | Defer to Phase 3, design CRDT later |
| ... | ... | ... | ... |

## Pillar build order

1. {Pillar} — foundation
2. {Pillar} — depends on 1
3. ...

## Definition of v1 shipped

- {must-haves working}
- {explicit v2 list}

## What's NOT in v1

- {list things explicitly punted to v2}

---

*Frozen on: {date when frozen}*
```

Show the draft. Iterate — especially on phasing, since this is what the user will actually execute against.

### Step 5 — Visual

Call `sps-visual-maker`:
- type: `build-timeline`
- format: ask (ASCII default; HTML if many phases / many features)
- content: phases + items per phase + estimates
- output_path: `visuals/07-build-timeline-v{N}.{ext}`

### Step 6 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L7 Build Plan (FINAL LAYER)
=================================================

  ✓ Build plan locked for {App Name}

    Tech stack: {top-level summary}
    Phases: {count}
    Phase 1 estimate: {time}
    Total estimate: {time}
    Risks identified: {count}

  → All 7 layers frozen. Design is complete.
    Implementation can begin.

=================================================
```

Ask: "Freeze L7 at v{N}? (freeze / revise / backlog)"

### Step 7 — On freeze

1. Write `07-build/v{N}.md` with FROZEN status.
2. Update `07-build/current.md`.
3. Update freeze-status.md:
   - L7 → `FROZEN`, v{N}.
   - Add a final line: **All layers frozen. Design phase complete on {date}.**
4. Final celebration message to user:

```
🎉  All 7 layers of {App Name} are frozen.

You have a complete top-down spec:
- Vision locked (L1)
- {P} pillars defined (L2)
- {F} features specified across pillars (L3, L4)
- {S} screens mapped (L5)
- {M} mockups visualized (L6)
- Build plan with {phases} phases and {risks} risks (L7)

Everything lives in: {project root}

Ready to build? Open Phase 1 of `07-build/current.md` and start with the thin slice.

If you'd like a single export combining all layers into one document, ask me to "export {App Name} as a master spec".
```

## Backlog hook

L7 backlog usually catches:
- Future tech stack ideas ("when traffic grows, switch to X")
- v2 features that came up while planning
- Operational concerns ("set up monitoring later")

## Optional: master spec export

After freezing L7, if the user asks, the skill can produce a single combined document `00-meta/master-spec.md` that concatenates the current versions of all 7 layers in order. This is useful for sharing the full spec or feeding it to a code generation agent.

## Critical rules

- **Phase 1 must be a true thin slice.** End-to-end, even if narrow. Not "build the backend then the frontend."
- **Risks are mandatory.** A build plan with no risks is dishonest.
- **Definition of v1 must explicitly list what's NOT included.** Otherwise scope creeps.
- **Tech stack research must be current.** Use search; don't rely on training data alone.
- **Visual is mandatory** (build timeline).
