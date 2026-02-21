# Domain Knowledge Layer 1 — Public Data Proxy Design

**Date:** 2026-02-21
**Status:** Approved
**Parent specs:**
- `docs/plans/domain-knowledge/design-v3.md` — Full v3 spec (21 decisions)
- `docs/plans/domain-knowledge/mvp-design.md` — MVP scope decisions (A1-A5)
- `dev/internal/2026-02-16-domain-knowledge-layer1-implementation-plan.md` — Original implementation plan

**Purpose:** Adapt the Layer 1 implementation plan to use public data sources instead
of internal Confluence, enabling both architecture validation and portfolio demonstration.

---

## Context

The original Layer 1 plan assumes access to internal Confluence pages from a Search
Relevance team. This session is building with public data only. We need content that:
1. Validates the digest architecture works end-to-end
2. Looks impressive as a portfolio demo
3. Is shareable (no proprietary content)
4. Can be swapped for real Confluence content later

---

## Content Strategy

### Foundational Tier (authoritative)
- **Source:** Existing draft content from original plan, enhanced with specific numbers,
  benchmarks, and citations from academic papers and public IR research.
- **Examples:** MS MARCO leaderboard ranges, TREC evaluation methodology, key IR papers
  (BM25, LambdaMART, position bias correction methods).
- **Label:** Citations inline (e.g., "ref: Joachims et al., 2017").

### Workstream Standards Tier (authoritative)
- **Source:** Hybrid of public engineering blog decisions + synthetic team decisions.
- **Public sources:** Google AI Blog, Airbnb Search Engineering, LinkedIn Engineering,
  Netflix Tech Blog — real published decisions about search systems.
- **Synthetic entries:** Realistic team decisions for patterns without public analogs.
- **Label:** Synthetic entries marked `[DEMO]`. Public entries cite source.

### Workstream Learnings Tier (advisory)
- **Source:** Hybrid of published experiment results + synthetic post-mortems.
- **Public sources:** Published A/B test results, experiment write-ups from engineering blogs.
- **Synthetic entries:** Realistic experiment outcomes and incident learnings.
- **Label:** Synthetic entries marked `[DEMO]`. Public entries cite source.

### Conflicts Section
- At least 1 realistic conflict demonstrating workstream-overrides-foundational behavior.
- Labeled `[DEMO]` to indicate it's a demonstration scenario.

---

## Research Phase (New Pre-Step)

### Scope
Comprehensive research covering all major topics with real references.

### Organization
By digest domain — 3 batches mapping directly to digest files:

**Batch 1: search-ranking**
- Evaluation metrics (NDCG, MRR, ERR benchmarks and ranges)
- Position bias (IPW, doubly-robust papers, empirical results)
- Click models (PBM, DBN research)
- Learning to Rank (LambdaMART, neural ranking, benchmark results)
- Experiment design (interleaving studies, minimum duration evidence)
- Industry blog posts on ranking decisions and experiments

**Batch 2: query-understanding**
- Query classification taxonomies (informational/navigational/transactional)
- Query rewriting evaluation methods
- Spell correction precision/recall tradeoffs
- Intent detection methods and benchmarks
- Industry blog posts on QU systems

**Batch 3: cross-domain**
- End-to-end search evaluation frameworks
- Cross-component metric attribution methods
- Full-stack experiment design patterns

### Output
Saved to `docs/research/domain-knowledge-references.md` as a structured reference
document. User reviews before content is folded into digest files.

### Sources
- **Academic:** MS MARCO, TREC, SIGIR/WSDM/KDD papers, key IR textbook references
- **Industry:** Google AI Blog, Airbnb Engineering, LinkedIn Engineering, Netflix Tech
  Blog, Spotify R&D, Microsoft Research Blog

---

## Revised Task Sequence

| Task | What | Changes from Original |
|---|---|---|
| 0 (new) | Deep research — 3 batches by domain | New task |
| 0b | User reviews research, corrects/adjusts | New task |
| 1 | Create `domain-index.yaml` | Public source URLs instead of Confluence IDs |
| 2 | Create `SKILL.md` contract | Unchanged |
| 3 | Create `search-ranking.md` digest | Enriched with research + hybrid workstream |
| 4 | Create `query-understanding.md` + `search-cross-domain.md` | Enriched with research |
| 5 | Validation and cleanup | Unchanged |

---

## What Stays the Same (from original plan)

- File paths and directory structure
- Digest format contract (headers, authority tags, audience tags)
- Token budgets (8K/domain + 1.5K cross-domain)
- SKILL.md sections (6 sections, same spec)
- 5-task structure (with research pre-step added)
- All 21 design decisions from v3 spec

---

## Decisions Made

| # | Decision | Rationale |
|---|---|---|
| P1 | Public data only | No Confluence access. Content must be shareable. |
| P2 | Foundational: existing draft + public citations | Fastest path to credible, citable content |
| P3 | Workstream: hybrid public blogs + synthetic [DEMO] | Real sources where they fit, synthetic fills gaps |
| P4 | Deep research scope | Portfolio-impressive quality requires comprehensive references |
| P5 | Research organized by digest domain | Maps directly to implementation — each batch → one digest |
| P6 | Separate research doc before digests | Allows user review of research before it becomes product |
| P7 | Synthetic entries labeled [DEMO] | Honest about what's real vs. demonstrated |
