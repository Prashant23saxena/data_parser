---
name: sps-memory-keeper
description: Centralized memory operations for sps app-design projects. Reads and writes the shared memory files in 00-meta/ — activity-log.md, decisions.md, glossary.md, open-questions.md, revision-flags.md, agent-claims.md. Every other sps skill calls this utility instead of writing those files directly. Use when any skill needs to log an activity, record a decision, add a glossary term, raise an open question, flag a revision, claim/release a work package as an agent, or fetch a memory snapshot for context. Horizontal utility — callable by all other sps skills.
---

# Memory Keeper

The single point of access for shared project memory. Every other sps skill calls this utility for memory reads/writes so the format stays consistent and changes happen in one place.

## When this skill runs

Embedded in nearly every sps skill — at start of run (read context), during run (log decisions, glossary, questions), at end (log completion).

Standalone use: user says "show me what we've decided so far", "list open questions", "show project memory snapshot".

## Memory files managed

```
00-meta/
├── activity-log.md          ← append-only timeline of every skill action
├── decisions.md             ← key decisions with reasoning
├── glossary.md              ← project-specific vocabulary
├── open-questions.md        ← cross-layer unresolved questions
├── revision-flags.md        ← NEEDS_REVISION cascade tracking
└── agent-claims.md          ← live build-time WP claims (created at L8 freeze)
```

`freeze-status.md` and `project-name.md` are NOT managed by this skill — they're owned by `sps-app-architect` and `sps-project-builder` respectively. This skill reads them when producing snapshots.

## Actions

### 1. read-context

**Purpose:** Return a memory snapshot tailored for the calling skill.

**Input:** `caller` — the calling skill's name (e.g. `sps-pillar-mapper`)

**Steps:**
1. Read `freeze-status.md` to determine current state.
2. Read `decisions.md` (always relevant for context).
3. Read `glossary.md` (always relevant for vocabulary).
4. Read `open-questions.md` and filter to questions that affect or are likely to affect the caller's layer.
5. Read `revision-flags.md` for any flags pointing at the caller.
6. If `00-meta/references/index.md` exists, list available reference docs.
7. Return a structured snapshot:
   ```
   PROJECT MEMORY SNAPSHOT for {caller}
   
   Current state: {summary from freeze-status}
   
   Relevant decisions: {filtered list}
   Glossary terms: {full list, terse}
   Open questions affecting you: {filtered}
   Revision flags pointing here: {if any}
   References available: {list}
   ```

The caller uses this to ground its interview and avoid re-asking things.

### 2. log-activity

**Purpose:** Append a one-line entry to `activity-log.md`.

**Inputs:** `caller`, `event` (short string)

**Steps:**
1. Read or create `activity-log.md` (template below if missing).
2. Append: `{ISO timestamp} | {caller} | {event}`
3. No confirmation needed — silent operation.

Template if file missing:
```markdown
# Activity Log

> Append-only. Every skill action gets a line. Latest at bottom.

```

### 3. record-decision

**Purpose:** Append to `decisions.md`.

**Inputs:** `caller`, `decision` (short title), `reason`, `affects` (which layers/components)

**Steps:**
1. Read or create `decisions.md` (template below).
2. Determine next D-NNN ID.
3. Append:
   ```
   ## D-{NNN}: {decision title}
   Layer: {caller's layer}
   Date: {today}
   Reason: {reason}
   Affects: {affects}
   ```
4. Confirm: "Recorded D-{NNN}."

Template:
```markdown
# Decisions Log

> Decisions made during design that should be remembered. Append new decisions; do not edit old ones.

```

### 4. add-glossary

**Purpose:** Append a term to `glossary.md`. If the term already exists, do nothing or update only if the calling skill asked to revise.

**Inputs:** `term`, `definition`

**Steps:**
1. Read or create `glossary.md` (template below).
2. Search for `## {term}` heading. If exists, return "already defined" with the existing definition.
3. Otherwise append:
   ```
   ## {Term}
   {definition}
   ```
4. Keep entries alphabetical when easy; append-only is acceptable.

Template:
```markdown
# Glossary

> Project-specific vocabulary. Used to keep naming consistent across layers.

```

### 5. raise-question

**Purpose:** Append to `open-questions.md`.

**Inputs:** `caller`, `question` (short title), `context`, `default` (optional — if a default behavior exists), `status` (default `PROPOSED`)

**Steps:**
1. Read or create `open-questions.md`.
2. Determine next OQ-NNN ID.
3. Append:
   ```
   ## OQ-{NNN} — {question title}
   Raised at: {caller's layer + scope}
   Date: {today}
   Status: {status}
   Context: {context}
   {if default} Default: {default}
   ```
4. Confirm with the OQ ID.

Status values: `PROPOSED` (unresolved, blocks freeze), `PARKED-WITH-DEFAULT` (default used, revisit later), `DEFERRED-TO-V2`, `DECIDED` (move to decisions.md instead — actually use `record-decision` and mark OQ as DECIDED here).

Template:
```markdown
# Open Questions Registry

> Questions raised during design. Must be resolved or explicitly parked before final freeze.

```

### 6. resolve-question

**Purpose:** Update an OQ's status.

**Inputs:** `id` (OQ-NNN), `new_status`, `note` (optional)

**Steps:**
1. Find the OQ block in `open-questions.md`.
2. Update its `Status:` line.
3. Append a `Resolved: {today} — {note}` line below.

### 7. flag-revision

**Purpose:** Log a NEEDS_REVISION flag with full cascade context.

**Inputs:** `caller`, `target` (which layer/item to revise), `reason`, `cascade` (other layers likely affected)

**Steps:**
1. Read or create `revision-flags.md`.
2. Determine next RF-NNN ID.
3. Append:
   ```
   ## RF-{NNN}
   Raised by: {caller}
   Target: {target}
   Reason: {reason}
   Cascade: {cascade}
   Date: {today}
   Status: PENDING
   ```
4. Also update `freeze-status.md` to mark the target with NEEDS_REVISION (this is the only place memory-keeper writes to freeze-status).
5. Confirm with the RF ID.

Template:
```markdown
# Revision Flags

> NEEDS_REVISION flags raised by later layers about earlier ones. Tracks cascades.

```

### 8. claim-wp / release-wp / mark-wp-done / mark-wp-blocked

**Purpose:** Agent-build-time operations on `agent-claims.md`. Used during L8 execution.

**Inputs (claim):** `agent_id`, `wp_id`, `note`
**Inputs (release):** `agent_id`, `wp_id`, `reason`
**Inputs (done):** `agent_id`, `wp_id`, `result_note` (e.g. "tests 12/12 pass")
**Inputs (blocked):** `agent_id`, `wp_id`, `blocker` (e.g. "OQ-007 raised")

**Steps:**
1. Read or create `agent-claims.md` (template below).
2. Append a line: `{ISO timestamp} | {agent_id} | {ACTION} | {wp_id} | {note/reason/result/blocker}`
3. ACTION is one of: CLAIMED, RELEASED, DONE, BLOCKED.

Template:
```markdown
# Agent Claims

> Live, mutable, append-only log. Agents append claim lines.
> The latest line for any WP is its current status.

```

### 9. show-snapshot

**Purpose:** User-facing summary of project memory state.

**Inputs:** `verbosity` — `terse`, `normal`, `full`

**Steps:**
1. Read freeze-status.md, decisions.md, glossary.md, open-questions.md, revision-flags.md.
2. Render a clean summary:
   ```
   === {Project Name} — Memory Snapshot ===
   
   Last activity: {last line from activity-log}
   
   Layers frozen: L1, L2, L3 (3 of 4 pillars), L4 (12 of 23 features)...
   
   Decisions logged: {count}, latest: D-{NNN} {title}
   Glossary terms: {count}
   Open questions: {count} ({count} proposed, {count} parked)
   Revision flags: {count} pending
   
   {at full verbosity, list everything}
   ```

## How callers should use this

A typical vertical skill at start of run:

```
1. Call sps-memory-keeper read-context with caller=self
2. Use the snapshot to inform interview questions
3. During interview, when user makes a decision → call record-decision
4. When user introduces a new term → call add-glossary
5. When user parks something unresolvable → call raise-question
6. At end of run → call log-activity with the freeze event
```

Do NOT skip these calls. Memory hygiene is what keeps multi-day projects sane.

## Concurrency

Most operations are append-only, so safe under concurrent access. The exceptions:
- `freeze-status.md` updates from `flag-revision` — small risk, accept it for v1.
- `resolve-question` edits in place — usually only one caller at a time.

For agent-claims.md during L8 execution: append-only, latest-line-wins. Multiple agents can append safely; readers parse the file by walking lines and keeping the most recent line per WP-ID.

## Critical rules

- **Never delete entries.** Memory is append-mostly. Edits only for status updates on OQ/RF.
- **Always include date** (use today's date in ISO format).
- **Always log activity** at start and end of any sps skill run.
- **Don't duplicate glossary entries** — search before adding.
- **Don't write to freeze-status.md** except via `flag-revision`.
- **Don't write to project-name.md** ever (owned by sps-project-builder).
