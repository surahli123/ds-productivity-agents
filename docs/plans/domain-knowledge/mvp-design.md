# Domain Knowledge Skill — MVP Design (v0.5)

**Date:** 2026-02-16
**Status:** Approved — ready for implementation planning
**Parent spec:** `docs/plans/domain-knowledge/design-v3.md`
**Purpose:** MVP-scoped design adjustments to make Layer 1 feasible and immediately useful

---

## Context

The v3 design doc (914 lines, 21 decisions) defines a 3-layer Domain Knowledge system.
During PM-led design review on 2026-02-16, five challenges were identified in Layer 1.
This document captures the agreed-upon adjustments that narrow v0.5 scope to what's
feasible and testable without infrastructure dependencies.

Layer 1 (Domain Knowledge Skill) is the immediate build target. It should be useful
beyond DS review — Search Engineers are a second audience who want to stay current
with domain knowledge. The architecture supports this without redesign.

---

## Design Adjustments (5 Challenges Resolved)

### A1: Reframe the "API" as a file contract + refresh workflow

**Problem:** `get_domain_context()` function signature implies callable code, but Layer 1
is a markdown skill. Every consumer would re-implement assembly logic.

**Resolution:** Layer 1 has two components:

| Component | When | What | Complexity |
|---|---|---|---|
| Refresh workflow | Explicitly triggered | Fetches docs, LLM scores importance, generates versioned digest files | High |
| Query interface | At review time | Consumer reads digest file(s), checks staleness from version header | Trivial |

- SKILL.md defines the **contract**: digest file format, section headers, authority tags,
  version headers, staleness thresholds, audience tags
- Digest files are the product. Any consumer agent uses the Read tool to access them
- Multi-domain: consumer concatenates digest files. Staleness: parse version header
- The `get_domain_context()` signature is retained as contract documentation, not a callable

### A2: Audience-tagged sections + increased token budget (8,000)

**Problem:** 5,000 tokens per domain can't serve both DS reviewers and Search Engineers.

**Resolution:**
- Token budget increased from 5,000 → **8,000 per domain**
- Each digest section tagged with `[audience: all | ds | eng]`
- Consumer agents filter by audience tag (simple string matching)
- DS review agent reads `all` + `ds` sections (~5,000-6,000 effective tokens)
- Engineering consumer reads `all` + `eng` sections (~5,000-6,000 effective tokens)
- YAML index pages get optional `audience` field (default: `all`)
- LLM digest generation prompt includes audience tagging instructions

### A3: Manual-only refresh for v0.5 (no auto-discovery, no scheduled cadence)

**Problem:** Weekly automated refresh requires infrastructure that doesn't exist
(no cron, no CI, runs on laptop). Auto-discovery hits low-hygiene Confluence.

**Resolution:**
- All docs manually curated in YAML index (no auto-discovery in v0.5)
- Refresh triggered explicitly via `--refresh-domain <domain>` command
- Runs inside Claude Code session (Read/Write tools + LLM for scoring)
- No `refresh.sh` shell script in v0.5
- SKILL.md documents recommended cadence as guidance, not enforcement
- Staleness warning emitted when digest version is >14 days old
- Auto-discovery deferred to v1 (after digest format is validated on curated docs)

### A4: Drop team roster for v0.5

**Problem:** Roster adds maintenance burden (YAML file, lookup step, quarterly updates)
for a problem that LLM content scoring may already solve.

**Resolution:**
- No `team-roster.yaml` in v0.5
- No author lookup or inferred authority logic
- Importance formula simplified to pure LLM content scoring:
  `final_importance = (0.6 * review_impact) + (0.4 * knowledge_density)`
- No Confluence tiebreaker (was +/-0.05 — essentially noise)
- Validate during calibration: if brief-but-important docs score low, add roster in v1

### A5: Cross-domain gets additive budget (1,500 tokens)

**Problem:** Cross-domain sharing domain budget punishes domain-specific depth.

**Resolution:**
- Cross-domain budget: **1,500 tokens (additive, not shared)**
- Single domain total: 8,000 + 1,500 = 9,500
- Multi-domain: 8,000 per domain + 1,500 cross-domain (included once)
- Cross-domain content is a small curated set (1-3 overview docs)

---

## What v0.5 Builds (Scope Summary)

### Layer 1 — Domain Knowledge Skill (standalone, reusable)

**Files to create:**
- `plugin/skills/domain-knowledge/SKILL.md` — skill definition, file contract, digest
  format spec, refresh workflow instructions, staleness thresholds
- `plugin/config/domain-index.yaml` — curated domain-to-pages mapping (3 Search
  sub-domains + cross-domain). No auto-discovery blocks. Includes audience tags.
- `plugin/digests/` — directory for versioned digest files
- Initial digest files for search-ranking, query-understanding, search-infra, cross-domain

**Not in v0.5:**
- No `team-roster.yaml` (dropped per A4)
- No `refresh.sh` script (refresh is a prompted workflow per A3)
- No auto-discovery (all docs explicit in YAML per A3)
- No Confluence tiebreaker scoring (dropped per A4)
- No `topic_hints` filtering (deferred to v1)

### Layer 2 — Domain Expert Reviewer (thin subagent for DS review)

**Files to create:**
- `plugin/agents/domain-expert-reviewer.md` — 3 lenses, authority-aware scoring,
  ADVISORY severity, rubric separated from domain context

**Files to modify:**
- `plugin/skills/ds-review-framework/SKILL.md` — add Domain Knowledge deduction table,
  strength credits, ADVISORY severity, routing rules, deduplication rule

### Layer 3 — Lead Agent Integration (DS review orchestrator)

**Files to modify:**
- `plugin/agents/ds-review-lead.md` — parse --domain, call skill (read digest files),
  dispatch 3rd subagent, two-stage dedup, 50/25/25 scoring, 11-row dashboard
- `plugin/agents/analysis-reviewer.md` — add domain-specific skip guardrail
- `plugin/commands/review.md` — add --domain, --reference, --refresh-domain flags

---

## Decisions Carried Forward from v3 (Unchanged)

All 21 decisions from the v3 spec remain valid except where adjusted above:
- D14 updated: 5,000 → 8,000 tokens per domain + 1,500 additive cross-domain
- D15 simplified: LLM scoring only, no Confluence tiebreaker, no roster
- D16 deferred: team roster moved to v1

Everything else (3 lenses, 50/25/25 weighting, ADVISORY severity, two-stage dedup,
floor rules, workstream precedence, digest versioning) carries forward unchanged.

---

## V1 Additions (Deferred from v0.5)

- Auto-discovery via Confluence space search
- Team roster for IC7+ authors (if LLM scoring proves insufficient)
- Confluence tiebreaker scoring
- `topic_hints` filtering for targeted context retrieval
- Scheduled refresh (requires infrastructure decision)
- Feedback mechanism for false positives
