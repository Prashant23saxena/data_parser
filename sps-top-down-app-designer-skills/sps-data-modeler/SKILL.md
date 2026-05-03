---
name: sps-data-modeler
description: Layer 8.1 of the sps app-design workflow. The first sub-step of L8 implementation architecture. Walks every feature spec to derive the canonical data model — entities, attributes, relationships, source of truth, lifecycle, constraints, access patterns. Use after L7 (build plan) is frozen, when sps-app-architect routes here, or when the user says "derive the data model", "what entities does this app need", "model the data". Produces 08-architecture/01-data-model/v1.md plus an entity-relationship visual. Foundation that L8.2 components and L8.3 contracts depend on.
---

# Data Modeler (Layer 8.1)

The first sub-skill of L8 implementation architecture. Derives the data model that everything downstream depends on. This is the foundation — get it wrong and components/contracts/work-packages all suffer.

## Preconditions

- L7 (build plan) must be `FROZEN`.
- L8.1 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context` with caller=`sps-data-modeler`.

Read every frozen spec:
- L1 vision (constraints, non-goals — e.g. "single user" → no org entity)
- L2 pillars (mental groupings)
- L3 features (every feature across all pillars)
- L4 specs (states, inputs, side effects — these reveal entities and lifecycle)
- L5 screens (access patterns — what data is shown together)
- L7 build plan (tech stack — informs whether SQL/NoSQL/local)
- `00-meta/references/*.md` if present (competitor data models)

Greet:

> "Starting L8.1 data model. I'll walk every feature spec to derive entities, relationships, and constraints. Tech stack from L7: {db}. Let's go."

### Step 2 — Domain research

3-5 searches focused on data modeling for this domain and stack:
- "Data model for {app type}"
- "Schema design for {tech stack}"
- "{feature type} data model patterns" — for any complex features
- "Entity-relationship for {domain}"

### Step 3 — First-pass entity extraction (you do this, not the user)

Walk the L3 + L4 specs and surface candidate entities. Look for:
- Nouns that have identity ("a user", "a task", "a workspace")
- Things that are created, edited, deleted
- Things that have attributes
- Things that get listed
- Things that have IDs in URLs

For each, draft:
- Name
- 3-7 attributes (most obvious ones from spec)
- Likely relationships to other candidates

Show the user the candidate list:

> "From your specs I'm seeing these entities: User, Workspace, Task, Tag, Session, Notification. Let's refine."

### Step 4 — Refine entities (interview)

For each candidate, with the user:

**4a. Confirm or merge.** "Is Task and Item the same thing? Or different?"

**4b. Attributes.** Walk through the L4 specs that touch this entity, list every attribute mentioned. Add types (string, int, datetime, enum, json, ref).

**4c. Identity.** "What identifies this entity uniquely? Auto-ID? Composite? UUID? Slug?"

**4d. Relationships.** "User has many Tasks?" / "Task belongs to one Workspace?" / "Tags are many-to-many with Tasks?"

**4e. Source of truth.** Critical question: where does this data physically live?
- Server DB only?
- Client local only (e.g. localStorage, SQLite on device)?
- Both with sync (and which wins on conflict)?
- Derived from other entities (computed, not stored)?

**4f. Lifecycle.** When is it created? Deleted? Soft-deleted? Versioned? Audited?

**4g. Constraints.** Uniqueness, validation rules (lift from L4 inputs), foreign-key constraints.

**4h. Access patterns.** What queries does the app need? List them — they drive index choices.

### Step 5 — Cross-cutting concerns

Ask the hard questions:

- **Auth model:** Where do credentials live? Sessions / tokens — entity or external?
- **Audit log / history:** Needed? For which entities? Append-only?
- **Soft delete:** All entities? Some? Recovery window?
- **Multi-device sync:** If yes, which entities, what conflict strategy? (Often becomes an OQ → call `sps-memory-keeper raise-question`.)
- **Privacy / PII:** Which fields are sensitive? Encryption-at-rest needed?
- **Multi-tenancy:** Single user (per L1), or future-proof for teams?

For each unresolved hard question, call `sps-memory-keeper raise-question` with a default if you can propose one.

### Step 6 — Synthesize draft

Write `08-architecture/01-data-model/v{N}.md`:

```markdown
# Data Model — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Tech stack ref:** L7 build plan v{X}

## Overview

{Plain-language summary: how many entities, key relationships, source-of-truth pattern (e.g. "server-authoritative with read replicas, local cache for offline").}

## Entities

### User
**Identity:** UUID (primary), email (unique secondary)
**Source of truth:** server DB
**Lifecycle:** created on signup; soft-delete with 30-day recovery; never hard-deleted
**Audit:** login events to separate audit table

| Field | Type | Required | Default | Constraints | Notes |
|---|---|---|---|---|---|
| id | uuid | yes | gen_random_uuid() | PK | |
| email | varchar(254) | yes | — | unique, lowercase, RFC 5322 | |
| display_name | varchar(80) | yes | — | non-empty | |
| created_at | timestamptz | yes | now() | | |
| deleted_at | timestamptz | no | null | | soft-delete marker |
| ... | ... | ... | ... | ... | ... |

**Relationships:**
- has_many Tasks (cascade soft-delete)
- has_many Sessions (cascade hard-delete on user hard-delete)

**Indexes:**
- (email) unique
- (created_at) for analytics queries
- (deleted_at) where null, for filtering active users

### Task
...

### Workspace
...

## Relationships diagram

(rendered separately by sps-visual-maker)

## Source-of-truth matrix

| Entity | Server | Client local | Sync? | Conflict strategy |
|---|---|---|---|---|
| User | yes | cached | server-wins | refresh on login |
| Task | yes | yes | yes (background) | last-write-wins (v1), CRDT (v2 — see OQ-007) |
| Session | yes | yes (token only) | no | new session on conflict |
| ... | ... | ... | ... | ... |

## Cross-cutting decisions

- **Auth:** server-stored sessions, JWT in client, 30-day refresh window. (D-XXX)
- **Soft delete:** users + tasks; hard delete for sessions, notifications. (D-XXX)
- **Audit log:** separate `audit_events` table, append-only, retains 1yr.
- **PII:** email and display_name are PII; encrypted at rest via DB-level encryption.

## Access patterns

| Pattern | Triggered by | Frequency | Index used |
|---|---|---|---|
| List active tasks for user | home screen, every load | high | tasks(user_id, deleted_at) |
| Search tasks by title | search screen | medium | full-text on tasks(title) |
| ... | ... | ... | ... |

## Open questions

- OQ-007: CRDT vs LWW for task sync (PROPOSED)
- ...

---

*Frozen on: {date when frozen}*
```

### Step 7 — Visuals

Call `sps-visual-maker`:
- type: `entity-relationship` (a custom variant of dep-graph — entities as nodes, relationships as labeled edges)
- format: ask (HTML recommended for >5 entities; ASCII for fewer)
- content: entities + their relationships
- output_path: `visuals/08-data-model-v{N}.{ext}`

If type isn't directly supported, use `dep-graph` shape with entities as nodes and relationships as labeled arrows.

### Step 8 — Freeze gate

Story summary via `sps-visual-maker`:

```
=================================================
  FREEZE GATE — L8.1 Data Model
=================================================

  ✓ Data model locked for {App Name}
  
    Entities: {N}
    Relationships: {N}
    Source-of-truth split: {S} server / {C} client / {B} both
    Cross-cutting decisions: {N}
    Open questions: {N} ({P} proposed need answers before final freeze)

  → Next: L8.2, component architecture (groups entities into 
    services/modules)

=================================================
```

Ask: "Freeze L8.1 at v{N}? (freeze / revise / backlog)"

If any OQ is `PROPOSED`, push back: "OQ-007 is proposed. Freeze with `PARKED-WITH-DEFAULT` or resolve now?"

### Step 9 — On freeze

1. Write FROZEN status into `v{N}.md`. Update `current.md`.
2. Update freeze-status.md: L8.1 → FROZEN, v{N}.
3. L8.2 → PENDING (was BLOCKED).
4. Call `sps-memory-keeper`:
   - `log-activity` — froze L8.1 v{N}
   - `record-decision` for each cross-cutting decision (auth approach, soft-delete policy, etc.)
   - `add-glossary` for any data-model-specific terms (e.g. "audit_event", "soft-delete window")
5. Confirm: "L8.1 frozen. Run **sps-app-architect** or **sps-component-mapper** to start L8.2."

## Backlog hook

Common parking moments at L8.1:
- Future entities for v2 features
- Schema migration concerns
- Performance optimization ideas

Park to `08-architecture/01-data-model/backlog.md`.

## Critical rules

- **Source of truth must be explicit per entity.** "It just lives in the DB" is not enough — say so explicitly.
- **No fabricated entities.** Every entity must be justified by at least one feature spec referencing it.
- **Cross-cutting questions must be answered or parked.** Auth/sync/audit/soft-delete cannot be left blank.
- **Indexes follow access patterns, not guesses.** Document the pattern, then the index.
- **Visual is mandatory.**
- **Hand off cleanly to L8.2** — components depend on the entity list being settled.
