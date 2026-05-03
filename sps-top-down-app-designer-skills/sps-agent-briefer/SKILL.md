---
name: sps-agent-briefer
description: Layer 8.8 of the sps app-design workflow. The eighth and final sub-step of L8 implementation architecture, and the LAST design step before build. Produces the generic-agent-protocol document (agent-instructions.md) that any coding agent reads to know how to claim work, build, test, mark done, and escalate. Also generates the initial live execution checklist (checklist.md) that agents update as they work. Use after L8.7 (UAT) is frozen, when sps-app-architect routes here, or when the user says "produce the agent instructions", "generate the build checklist", "wrap up architecture so we can start building". Once this freezes, the design phase is complete and any compatible coding agent can be pointed at the project to begin building.
---

# Agent Briefer (Layer 8.8)

The final sub-skill of L8, and the final design step in the entire workflow. After this freezes, the design phase is complete. The artifacts produced here turn the spec into something a coding agent can execute against.

Two primary outputs:
1. **`agent-instructions.md`** — the protocol any agent follows when working on this project
2. **`checklist.md`** — the live execution checklist agents update as they work

## Preconditions

- L8.7 (UAT scenarios) must be `FROZEN`.
- L8.1 through L8.7 all FROZEN (guaranteed by precondition chain).
- L8.8 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read every L8 artifact:
- L8.1 data model
- L8.2 components
- L8.3 contracts (index)
- L8.4 build graph
- L8.5 work packages (index + count)
- L8.6 integration tests
- L8.7 UAT scenarios

Plus L1 vision (for the project intro section in agent-instructions).

### Step 2 — Verify readiness

Sanity check before producing instructions:
- Are there any `PROPOSED` open questions in `00-meta/open-questions.md`? If yes, push back: "These OQs are still open. Resolve or park-with-default before starting build, or agents will hit them and stall."
- Are there any `PENDING` revision flags? Same push-back.
- Are all WPs in L8.5 properly defined (non-empty acceptance, test invocation, etc.)? Spot-check.

### Step 3 — Generate agent-instructions.md

Write `08-architecture/08-agent-instructions/v{N}.md` (and a copy as `08-architecture/agent-instructions.md` at the L8 root for easy access by agents):

```markdown
# Agent Instructions — {App Name}

**Project:** {App Name}
**Vision:** (one paragraph from L1)
**Last updated:** {today}
**Architecture version:** L8.1 v{X}, L8.2 v{Y}, ..., L8.7 v{Z}

## Welcome, agent.

You are about to build {App Name}. The full spec is in this project. Read this document first; it contains everything you need to know about how to operate.

## Your job

Pick up a work package (WP), build it, test it, mark it done. Move to the next available WP. When all WPs are done, run integration tests, then UAT.

## Where things live

```
{project root}/
├── 00-meta/                 ← project memory (you write to some of these)
├── 01-vision/               ← what we're building
├── 02-pillars/              ← high-level capability areas
├── 03-features/             ← features per pillar
├── 04-specs/                ← feature specs + tests (sibling files)
├── 05-screens/              ← screens and flows
├── 06-mockups/              ← visual references
├── 07-build/                ← phase plan (you operate inside one phase at a time)
└── 08-architecture/
    ├── 01-data-model/       ← READ-ONLY for you
    ├── 02-components/       ← READ-ONLY for you
    ├── 03-contracts/        ← READ-ONLY (each contract is a separate folder)
    ├── 04-build-graph/      ← READ-ONLY
    ├── 05-work-packages/    ← YOUR WORK lives here
    ├── 06-integration/      ← READ-ONLY (you run these)
    ├── 07-uat/              ← READ-ONLY (you or a human runs these)
    └── checklist.md         ← LIVE — update as you work
```

## How to start a session

1. Read `00-meta/freeze-status.md` to verify the design is frozen.
2. Read `00-meta/agent-claims.md` to see what other agents are doing.
3. Open `08-architecture/checklist.md` to see overall build progress.
4. Pick the next available WP (see "Picking a WP" below).

## Picking a WP

A WP is **available** if:
- Its status is `PENDING` (not CLAIMED, IN_PROGRESS, BLOCKED, or DONE)
- All its hard dependencies have status `DONE`
- Soft dependencies can be mocked per the contract specs

Suggested order:
1. Foundation (Stream A) — must finish first
2. Critical-path WPs first within each stream (marked CRITICAL PATH in their files)
3. Then any other available WPs

To check WP status, read the latest line for that WP-ID in `00-meta/agent-claims.md`. If no line exists, status is PENDING.

## Claiming a WP

Before working, claim it. This prevents two agents working the same WP.

Use the sps-memory-keeper utility (or directly append to `00-meta/agent-claims.md`):

```
{ISO timestamp} | {your-agent-id} | CLAIMED | WP-{ID} | {short note}
```

Then read the WP file: `08-architecture/05-work-packages/WP-{ID}-{slug}/v1.md`

The WP file contains:
- What to build
- Inputs (paths to specs)
- Hard and soft dependencies
- Build steps (in order)
- Outputs (files/folders to produce)
- Test invocation (exact command)
- Acceptance checklist

## During work

Update status when you transition:
- `CLAIMED` → `IN_PROGRESS` when you actually start building
- `IN_PROGRESS` → `BLOCKED` if you hit something you can't resolve (see "Blockers" below)
- `IN_PROGRESS` → `DONE` when all acceptance checkboxes are ticked

Append a new line each time. Don't edit existing lines.

## Building

Follow the build steps in the WP file in order. They're written so you can execute them mostly mechanically.

Use the contracts in `08-architecture/03-contracts/` as your source of truth for any cross-component interaction. Don't invent shapes.

For mocked dependencies: use the mock spec from the contract file. The mock should return realistic data per the contract's example.

## Testing

After build, run the test invocation from the WP file. ALL tests must pass before marking DONE.

Tests are at multiple levels:
1. Unit tests you write while building (per WP)
2. Test scenarios from `04-specs/{pillar}/{feature}/v{N}-tests.md` (run when you finish a feature)
3. Contract validation tests (verify your output matches the contract)
4. Integration tests from `08-architecture/06-integration/` (run when paired components are both DONE)
5. UAT scenarios from `08-architecture/07-uat/` (run at the very end, before shipping)

If any test fails, do not mark DONE. Either fix the test cause, or mark BLOCKED with the specific failure.

## Marking DONE

Only mark DONE when:
- All build steps complete
- All acceptance checkboxes ticked
- Test invocation passes (all green)
- No console errors / lint errors
- No TODOs left in code

Update agent-claims.md:
```
{ISO timestamp} | {agent-id} | DONE | WP-{ID} | tests {pass/total} pass
```

Also update `08-architecture/checklist.md` to tick the WP's checkbox.

## Blockers

If you can't proceed:

1. Check if the issue is a known open question. Read `00-meta/open-questions.md`. If found, follow the documented default. If no default, raise it (next step).

2. Raise a new open question via sps-memory-keeper:
   - Title: short
   - Context: what you found, what you tried
   - Default: a reasonable default if you have one (so others can unblock)

3. Mark WP as BLOCKED in agent-claims with reference to the OQ:
   ```
   {timestamp} | {agent-id} | BLOCKED | WP-{ID} | OQ-{NNN} raised
   ```

4. Move to a different available WP.

## Avoiding conflicts with other agents

- **Never edit another agent's IN_PROGRESS WP.**
- **Never edit anything in 00-meta/* directly except via sps-memory-keeper.**
- **Never edit specs in 04-specs/, 05-screens/, etc.** — these are frozen design artifacts.
- **Build outputs go ONLY in the paths the WP file specifies.** Don't create files outside.
- **Integration tests:** only one agent should run integration tests at a time. Claim integration test runs the same way as WPs (use INT-{ID} in claims log).

## Coordinating completion

A "stream" is done when all its WPs are DONE.

A "phase" (from L7 build plan) is done when all WPs in that phase are DONE AND the relevant integration tests pass.

The "build" is done when all WPs are DONE, all integration tests pass, and all UATs pass.

## Communication with the human

The human in charge will read `00-meta/activity-log.md` and `08-architecture/checklist.md` periodically. Keep these accurate.

If you need a human decision (a question can't be defaulted), mark the WP BLOCKED, raise the OQ, and stop work on it. Don't guess.

## Code style

(insert any style decisions from L8.2 components or L7 build plan)

- Language: {from L7}
- Linter: {from L7 or convention}
- Test framework: {from L7}
- Folder convention: per L8.2 components

## Final acceptance

The project is shippable when:
- All WPs DONE
- All integration tests pass
- All critical-flow UATs pass
- ≥80% of edge UATs pass
- All non-functional UATs pass

At that point, hand back to the human for final review.

---

Good luck. The spec is complete; your job is to execute against it.
```

### Step 4 — Generate initial checklist.md

Write `08-architecture/checklist.md` — the live build dashboard:

```markdown
# Build Checklist — {App Name}

**Generated:** {today}
**Source of truth for status:** `00-meta/agent-claims.md` (latest line per WP wins)
**Regenerate this view:** run sps-agent-briefer in regenerate mode

## Summary

- Work packages total: {N}
- WPs complete: 0 / {N}
- Streams: {N}
- Critical path: {WPs}
- Integration tests: {N}
- UAT scenarios: {N}

## Stream A: Foundation

- [ ] WP-A01: {title} — PENDING
- [ ] WP-A02: {title} — PENDING
- [ ] WP-A03: {title} — PENDING

## Stream B: Backend domain

- [ ] WP-B01: {title} — PENDING
- [ ] WP-B02: {title} — PENDING
...

## Stream C: Frontend app shell
...

## Stream D: Frontend features
...

## Stream E: External integrations
...

## Integration tests (run when WP preconditions DONE)

- [ ] INT-001: {title} — needs WP-A01, WP-B01, WP-B03
- [ ] INT-002: ...

## UAT scenarios (run at end)

- [ ] UAT-001: {title} — critical flow
- [ ] UAT-002: ...

## Recently active

(read from activity-log.md tail; helps human see what's happening)
```

This file is **regenerable** — sps-agent-briefer can rebuild it from current agent-claims state. Agents are also free to update it directly (tick checkboxes) but the source of truth is agent-claims.

### Step 5 — Optional: master spec export

Offer the user: "Want a single combined master spec document? (`00-meta/master-spec.md` concatenating all current versions)"

If yes, generate by reading every layer's `current.md` and concatenating in order with section headers.

### Step 6 — Freeze gate (the final freeze)

Story summary:

```
=================================================
  FREEZE GATE — L8.8 Agent Briefer (FINAL DESIGN STEP)
=================================================

  ✓ Agent instructions and live checklist generated
  
    L8 fully frozen
    L1-L7 fully frozen
    Open questions resolved or parked: {N}
    Revision flags resolved: {N}
    
    Total WPs ready for build: {N}
    Foundation WPs (start here): {N}

  → DESIGN PHASE COMPLETE
  
  Hand `08-architecture/agent-instructions.md` to your build agent(s).
  They will pick up WPs and execute.
  
  Track progress at `08-architecture/checklist.md`.

=================================================
```

Ask: "Freeze L8.8 (and complete the design phase)?"

### Step 7 — On freeze

1. Save agent-instructions.md as v{N} in `08-architecture/08-agent-instructions/`, plus copy at L8 root.
2. Save checklist.md at L8 root.
3. Update freeze-status.md:
   - L8.8 → FROZEN
   - L8 overall → FROZEN
   - Add line: "**DESIGN PHASE COMPLETE on {date}.** Build phase ready to begin."
4. Call `sps-memory-keeper log-activity`.
5. Final celebration message:

```
🎉 Design phase complete for {App Name}.

You have:
- 8 layers frozen (L1 vision through L8 implementation architecture)
- {N} features specified
- {N} work packages ready to build
- {N} integration tests defined
- {N} UAT scenarios defined
- Agent instructions written

To begin build:
- Point your coding agent(s) at `08-architecture/agent-instructions.md`
- They will claim WPs from Stream A (foundation) first
- Track progress at `08-architecture/checklist.md`
- Watch `00-meta/agent-claims.md` for live status

For the human:
- Read `00-meta/activity-log.md` periodically
- Resolve any new OQs raised by agents in `00-meta/open-questions.md`
- Run UAT scenarios when build phase finishes

Good luck!
```

## Regenerate mode

If called in regenerate mode (the L8 is already frozen, but the user wants a fresh checklist):
1. Read agent-claims.md.
2. Compute current status of every WP.
3. Rewrite `08-architecture/checklist.md` with updated checkboxes and counts.
4. Don't update any frozen files. Don't change freeze-status.

## Critical rules

- **Don't freeze with PROPOSED OQs.** Hard rule.
- **Don't freeze with PENDING revision flags.** Hard rule.
- **Agent instructions must be agent-platform-agnostic.** No Cursor-specific or Claude-Code-specific assumptions. Generic protocol.
- **Checklist is regenerable.** Source of truth is agent-claims.md.
- **The freeze of L8.8 marks the end of design.** The orchestrator's behavior changes after this.
