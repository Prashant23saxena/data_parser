---
name: sps-contract-definer
description: Layer 8.3 of the sps app-design workflow. The third sub-step of L8 implementation architecture and the most critical for enabling parallel agent builds. For every cross-component interaction, defines the contract — API endpoints with request/response shapes, event names with payloads, shared data types — locked as standalone files (one per contract) so two agents can build against the same contract independently. Use after L8.2 (components) is frozen, when sps-app-architect routes here, or when the user says "lock the contracts", "define the APIs", "what are the wires between components". Each contract file freezes individually. Once a contract freezes, both sides can build in parallel — this is what unlocks the parallel build streams.
---

# Contract Definer (Layer 8.3)

**The most important skill in L8 for parallelism.** Each cross-component wire becomes a single file. Once the file is frozen, both sides can build independently against it. This is what turns "serial dependencies" into "parallel streams."

Each contract is its own freeze unit — you don't have to lock all contracts at once. Lock the foundation contracts first (auth, base data), and parallel work can begin while you're still locking later ones.

## Preconditions

- L8.2 (components) must be `FROZEN`.
- L8.3 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read:
- L4 specs (inputs, error messages — drive request/response shapes)
- L5 screens (data needs per screen — drive query endpoint shapes)
- L8.1 data model (entity shapes — basis for response types)
- L8.2 components (component boundaries — every cross-boundary call is a contract)

### Step 2 — Enumerate every contract

Walk the component dependency graph from L8.2. Every dependency arrow is at least one contract. Categorize:

**HTTP API contracts** — REST or GraphQL endpoints between frontend and backend, or between backend services.

**Event contracts** — pub/sub messages, webhook payloads.

**Shared data contracts** — types/schemas shared across components (e.g. the User shape used in many endpoints).

**Database contracts** — schema as contract for the DB-owning component (less common to formalize, but worth it for shared schemas).

Produce a list of contracts to define. Number each: C-001, C-002, ...

Show the user the list before defining individual ones:

> "I count {N} contracts. Want to lock them all in one session, or do the foundation contracts first ({list of foundation: auth, user, base data}) and revisit the rest?"

This matters because foundation contracts unblock the most parallel work.

### Step 3 — For each contract: structured definition

For each contract, walk the user through:

**3a. Identity.**
- Contract ID (C-NNN)
- Name (e.g. "Auth API", "Task Created Event", "User Type")
- Type (HTTP API / event / shared type / DB schema)
- Producer component (who owns/exposes it)
- Consumer components (who calls/listens)

**3b. Versioning policy.**
- Version (start at v1)
- Breaking-change rule: "Producer must bump major version on breaking change. Consumer pinning enforced."

**3c. Shape.**

For HTTP API contracts:
```
POST /auth/signup
Request body (JSON):
{
  "email": "string, RFC 5322, max 254",
  "password": "string, min 12, must contain letter+number",
  "display_name": "string, 1-80 chars"
}
Response 201 (JSON):
{
  "user": { "id": "uuid", "email": "string", "display_name": "string" },
  "session": { "token": "string", "expires_at": "iso8601" }
}
Error 400 (validation):
{ "error_code": "validation_failed", "fields": { "email": "format" } }
Error 409 (conflict):
{ "error_code": "email_exists" }
Error 500:
{ "error_code": "internal" }
Auth required: no
Idempotency: not idempotent (use idempotency-key header for retries)
Rate limit: 5/min per IP
```

For event contracts:
```
Event name: task.created
Producer: content-service
Consumers: notifications-service, analytics-service
Payload (JSON):
{
  "event_id": "uuid",
  "occurred_at": "iso8601",
  "task_id": "uuid",
  "user_id": "uuid",
  "title": "string",
  "created_via": "enum: web | api | import"
}
Delivery: at-least-once
Ordering: per user_id key only (best-effort)
Retention: 7 days for replay
```

For shared types:
```
Type: User (canonical shape)
Used in: contracts C-001, C-005, C-008
Definition (TypeScript-like):
interface User {
  id: string;          // uuid
  email: string;       // lowercased, RFC 5322
  display_name: string; // 1-80 chars
  created_at: string;  // iso8601
  // PII-sensitive: email, display_name
}
```

**3d. Test scenarios for the contract.** Each contract needs:
- A "happy path" example (concrete request + expected response)
- An error case example
- An edge case (large payload, slow response, etc.)

These get written as part of the contract file and feed into integration tests later.

**3e. Mock specification.**

This is the parallel-build enabler. For each contract, specify how the OTHER side mocks it:

> "While the producer is being built, consumers should mock this endpoint with: returns 201 with example shape on email containing '@', returns 409 if email starts with 'taken+', returns 400 if email omitted. Mock fixture: see `mocks/auth-signup.json`."

This is what lets the frontend agent build without waiting for the backend agent.

### Step 4 — Synthesize: one file per contract

Write each contract to its own file:

`08-architecture/03-contracts/C-{NNN}-{slug}/v1.md`

Folder per contract because each freezes independently and may be revised at different times.

```markdown
# Contract C-{NNN}: {Name}

**Version:** v1
**Status:** DRAFT
**Last updated:** {today}
**Type:** http-api / event / shared-type / db-schema
**Producer:** {component}
**Consumers:** {list}

## Purpose

One paragraph: why this contract exists.

## Versioning policy

{policy}

## Shape

(detailed shape per type, as per Step 3c above)

## Examples

### Happy path
Request: ...
Response: ...

### Error: validation
...

### Edge case: ...
...

## Mock specification

{how to mock this for parallel builds}

## Linked specs

- L4 features depending on this: F-XX-YYY, F-XX-ZZZ
- L5 screens displaying data from this: S-NN
- L8.1 entities referenced: User, Session

---

*Frozen on: {date when frozen}*
```

Plus an index file: `08-architecture/03-contracts/index.md`

```markdown
# Contracts Index

| Contract | Name | Type | Producer | Consumers | Status | Version |
|---|---|---|---|---|---|---|
| C-001 | Auth API | http-api | auth-service | frontend-onboarding, frontend-app-shell | FROZEN | v1 |
| C-002 | User Type | shared-type | shared-types | (multiple) | FROZEN | v1 |
| C-003 | Task API | http-api | content-service | frontend-content | DRAFT | v1 |
| ... | ... | ... | ... | ... | ... | ... |
```

### Step 5 — Per-contract freeze gate

Each contract gets its own freeze gate, NOT one big freeze for L8.3 as a whole. After defining each contract, ask:

> "Freeze C-{NNN}? (freeze / revise / move on, lock later)"

A contract that freezes individually unlocks parallel work for the components on either side immediately. The user can choose to lock 3 foundation contracts now, leave 5 in draft, and come back to those.

### Step 6 — On individual contract freeze

1. Write FROZEN status to `C-{NNN}-{slug}/v1.md`.
2. Update `current.md` in that folder.
3. Update `08-architecture/03-contracts/index.md` row for this contract.
4. Call `sps-memory-keeper log-activity` — "froze contract C-{NNN}".
5. Tell user: "C-{NNN} locked. Producer ({component}) and consumers ({list}) can now build in parallel against this contract."

### Step 7 — L8.3 overall freeze

L8.3 as a whole is FROZEN only when ALL contracts in the index are FROZEN. The skill tracks this and only marks L8.3 → FROZEN in freeze-status when the last one locks.

If the user tries to freeze L8.3 with contracts still DRAFT, push back: "5 contracts still DRAFT. L8.4 dependency graph needs all contracts to know what's parallel-able. Lock them or revisit?"

### Step 8 — On L8.3 overall freeze

1. Update freeze-status.md: L8.3 → FROZEN.
2. L8.4 → PENDING.
3. Story summary:
   ```
   ✓ All {N} contracts locked. {M} parallel build streams now possible.
   ```
4. Tell user to run sps-dependency-grapher next.

## Backlog hook

Common parking at L8.3:
- Future contract versions (v2 with new fields)
- Performance optimizations (batch endpoints to add later)
- Webhook contracts to add when integrations grow

## Revision cascade

Revising a frozen contract is destructive — it invalidates work both sides may have done. Treat as a major action:
- Bump contract to v2
- Both sides need to update
- Mark all WPs that depend on the contract as `NEEDS_REVISION`

The skill should warn loudly when revising a contract that's already in production.

## Critical rules

- **One file per contract.** Don't bundle.
- **Every contract has examples.** No abstract definitions.
- **Mock spec is mandatory.** Without it, parallelism breaks.
- **Producers and consumers are explicit per contract.** No "everyone uses this" — list them.
- **Versioning policy stated.** How will breaking changes be handled.
- **Per-contract freeze independent.** Foundation contracts freeze first, others can follow.
- **L8.3 overall freeze requires all contracts frozen.**
- **PII fields flagged in shared types.** Helps downstream encryption/log-redaction decisions.
