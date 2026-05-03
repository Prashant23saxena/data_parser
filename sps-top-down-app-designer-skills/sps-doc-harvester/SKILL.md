---
name: sps-doc-harvester
description: Ingest external product documentation, help centers, manuals (PDF), changelogs, READMEs, or pasted notes and convert them into structured reference material saved to 00-meta/references/. Use when starting a new app project and the user wants to reference competitor docs, when the user pastes a product manual or notes from a previous app, or when sps-project-builder asks for reference URLs at scaffold time. Also use when a vertical layer skill wants to ingest fresh reference material mid-project. Extracts feature inventories, hierarchy, settings, edge cases, vocabulary, and integrations into reference files that every vertical layer's domain-research step reads. Horizontal utility.
---

# Doc Harvester

Converts external product documentation into structured reference docs that vertical skills read during their domain-research step. Every harvested source is preserved and indexed.

## When this skill runs

- During scaffolding (invoked by `sps-project-builder` if user provides URLs)
- Mid-project when user wants to add a reference: "harvest the Notion docs", "ingest this PDF manual", "I have notes from my old app, save them as reference"
- Standalone: "show me the references I've harvested"

## Inputs

- `source_type` — one of: `url`, `pdf`, `text`, `multi-url`
- `source` — the URL, file path, pasted text, or list of URLs
- `mode` — one of: `structure-only` (TOC and headers only), `feature-inventory` (every feature mention with description), `deep` (also settings, edge cases, integrations, vocabulary)
- `slug` — short identifier for the saved reference (e.g. `notion-docs`, `linear-changelog`)

If invoked standalone without these, ask the user.

## Process

### Step 1 — Acknowledge and plan

Tell the user what's about to happen:

> "Harvesting {source} as `{slug}` in `{mode}` mode. I'll save the result to `00-meta/references/{slug}.md` and update `00-meta/references/index.md`."

### Step 2 — Fetch / read content

- **URL:** use `web_fetch` for the main URL. Then look for sitemap.xml, /docs, /help paths. Recursively fetch up to 15 pages, prioritizing pages with structural keywords (features, getting started, reference, API, settings).
- **PDF:** invoke the existing `pdf-reading` skill (read `/mnt/skills/public/pdf-reading/SKILL.md` first). Extract text page by page.
- **Text:** the user pasted it; just process directly.
- **Multi-URL:** loop over each URL.

If fetching fails (network error, paywall, auth wall): note the failure and continue with what was retrieved.

### Step 3 — Extract structured content

Run the source through the chosen mode's extraction pass.

**structure-only mode:** Just headers and table of contents. Output:
- Source URL/file
- Top-level sections in order
- Sub-sections under each (one level deep)

**feature-inventory mode:** structure-only PLUS:
- Every feature mention found in the content
- Description (1-3 sentences) for each
- Hierarchy (which section it lives under)
- Cross-links between features when mentioned

**deep mode:** feature-inventory PLUS:
- Settings / configuration options mentioned
- Edge cases described in docs (look for "if", "when", "unless", "however", error codes)
- Integration points (third-party services, APIs)
- Vocabulary glossary (distinctive nouns the product uses)
- Notable workflows (multi-step user journeys)

Be honest about what you can and can't extract — if the docs are sparse on edge cases, say so rather than fabricating.

### Step 4 — Write reference file

Write to `00-meta/references/{slug}.md`:

```markdown
# Reference — {slug}

**Source:** {URL or file path or "user-pasted"}
**Harvested:** {today}
**Mode:** {mode}
**Pages/sources processed:** {count}

## Summary

One paragraph: what this product is, what it does, who it's for. Inferred from the docs.

## Hierarchy

The product's own structural breakdown (their pillar/section structure).

```
- Top section 1
  - Sub 1.1
  - Sub 1.2
- Top section 2
  - ...
```

## Feature inventory

Every feature mentioned, deduped, grouped by hierarchy.

### {Section name}

- **{Feature name}** — {description from docs}
- **{Feature name}** — {description}
...

## Settings / configuration

(if deep mode)
- {setting 1} — {description}
- ...

## Edge cases mentioned

(if deep mode)
- {edge case + handling described}
- ...

## Integrations

(if deep mode)
- {integration name} — {what it does}
- ...

## Vocabulary

(if deep mode)
- **{term}** — {their definition}
- ...

## Notable workflows

(if deep mode)
- {workflow name}: {step 1 → step 2 → step 3}

## Coverage notes

What I could extract well, what I couldn't, and why.
```

### Step 5 — Update index

Read or create `00-meta/references/index.md`:

```markdown
# References Index

> Sources harvested into this project. Vertical layer skills read these during domain-research.

| Slug | Source | Harvested | Mode | Notes |
|---|---|---|---|---|
| {slug} | {URL/file} | {date} | {mode} | {short note} |
```

Append the new entry. If updating an existing slug (re-harvest), append a new row with the same slug and let both rows exist (latest is the active one).

### Step 6 — Memory hygiene

Call `sps-memory-keeper`:
- `log-activity` — caller=sps-doc-harvester, event="harvested {slug} from {source}"
- `add-glossary` for any high-value vocabulary terms (deep mode only) — but be conservative; don't pollute the glossary with every term, only ones that look load-bearing for the user's app domain.

### Step 7 — Important: anti-anchoring nudge

When done, tell the user:

> "Saved as `00-meta/references/{slug}.md`. Reminder: reference docs are for completeness checks ('did I forget settings?'), not scope definition ('what does my vision actually need?'). Your L1 vision and non-goals are still the boss."

This counters the natural tendency to copy a competitor's feature list.

## How vertical skills use harvested references

In their domain-research step, they:
1. List `00-meta/references/*.md` (or read `index.md`).
2. For each relevant reference, read the section that maps to their layer (e.g. L2 reads the Hierarchy section, L3 reads Feature inventory, L4 reads Edge cases, etc.).
3. Use the references AS WELL AS web search — references are project-specific, web is generic-domain.
4. Cite reference content when suggesting candidate items: "Notion uses 'workspaces' and 'pages' as their hierarchy — does that map to your structure?"

## Source-type-specific guidance

### URL harvesting

- Don't fetch more than 15 pages per harvest call (network and time cost).
- Prefer canonical sources: their official docs over third-party reviews.
- If the site is JS-rendered (SPA) and `web_fetch` returns mostly empty, note this — content extraction will be poor.
- Always get the date if available — older docs may not reflect current product.

### PDF harvesting

- Invoke `pdf-reading` skill properly (read its SKILL.md first).
- For long PDFs (>50 pages), focus on TOC + the chapters that look most feature-relevant.
- OCR'd PDFs may have noisy text; flag this.

### Text harvesting

- Format-flexible — could be markdown, plain text, structured notes, raw paste.
- Try to detect structure from indentation, headers, bullets.
- If text is purely freeform prose, the output will be looser; that's fine.

## Critical rules

- **Don't fabricate.** If the source doesn't have edge cases, don't invent them. Say "edge cases not extensively documented in source."
- **Cite sources.** Every reference file has the source URL/path. Don't lose attribution.
- **Anti-anchor reminder is mandatory.** Always nudge the user that references are checks, not scope.
- **Don't pollute glossary.** Be selective when calling add-glossary.
- **Idempotent re-harvest.** If a slug exists, save the new harvest with a versioned name (`{slug}-v2.md`) and update index — don't overwrite the original.
- **Respect copyright limits.** Paraphrase descriptions, don't copy paragraphs verbatim. Quotes under 15 words; one quote per source max.
