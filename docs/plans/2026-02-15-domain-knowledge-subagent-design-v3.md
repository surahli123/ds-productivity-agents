# Domain Knowledge Subagent — Design Document

**Date:** 2026-02-15
**Status:** v3 — Extracted Domain Knowledge Skill + gap fixes
**Target version:** v0.5
**Domain scope:** Search (Query Understanding, Search Ranking, Search Infrastructure)

**v2 → v3 Changelog:**
- Extracted Domain Knowledge Skill as standalone service, independent of DS review agent
- Domain Expert Reviewer becomes thin subagent: calls skill for context, applies review rubric
- Fixed Gap 1: Discovered docs default to workstream tier
- Fixed Gap 2: Cross-domain digest shares budget with requesting domain
- Fixed Gap 3: Deduplication specified as heuristic-first with LLM fallback
- Fixed Gap 4: Added ADVISORY severity level for recent-learning-sourced findings
- Fixed Gap 5: `--reference` always supplements, never overrides
- Fixed Gap 6: Workstream knowledge takes precedence over foundational when they conflict
- Fixed Gap 7: Floor rules apply equally regardless of scoring weight (explicit decision)
- Fixed Gap 8: Digests are versioned with rollback support

---

## 1. Problem Statement

The current review system has two dimensions — Analysis (generic DS rigor) and Communication
(presentation quality). Neither checks whether the analysis uses **correct domain-specific
knowledge**: right techniques for the problem space, valid benchmarks, awareness of known
pitfalls, or factually accurate claims.

A generalist DS reviewer can check "is the method internally consistent?" but not "is this
the method an expert in search relevance / causal inference / NLP would use?"

This subagent is scoped to **Search** as the MVP domain, covering three sub-domains: Query
Understanding, Search Ranking, and Search Infrastructure. The architecture is designed so
other teams can build their own domain-knowledge agents reusing the same design concepts
and engineering paradigm.

---

## 2. Architectural Overview (Revised in v3)

The domain knowledge system is split into two independent layers:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Domain Knowledge Skill (standalone service)   │
│                                                         │
│  Owns: YAML index, team roster, digests, refresh        │
│        pipeline, importance scoring, token budgeting     │
│                                                         │
│  API:  get_domain_context(domains, topic_hints?)        │
│        → returns context brief (within token budget)    │
│                                                         │
│  Lifecycle: independent. Refresh runs on its own        │
│             cadence. Any agent can call this skill.      │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Domain Expert Reviewer (thin subagent)        │
│                                                         │
│  Owns: 3 lenses, deduction tables, scoring rubric       │
│                                                         │
│  Calls: Layer 1 for domain context                      │
│  Calls: WebSearch for claim verification                │
│                                                         │
│  Focus: purely review logic. No knowledge management.   │
├─────────────────────────────────────────────────────────┤
│  Layer 3: DS Review Lead (orchestrator)                 │
│                                                         │
│  Dispatches: analysis-reviewer, communication-reviewer, │
│              domain-expert-reviewer (Layer 2)            │
│  Handles: deduplication, weighted scoring, output        │
└─────────────────────────────────────────────────────────┘
```

**Why this separation matters:**

1. **Reduced review-time latency.** The skill pre-computes and caches context briefs. The reviewer subagent receives a ready-made brief instead of building one at review time.
2. **Reusable across agents.** Any agent can call the Domain Knowledge Skill — code review agents checking implementation against team standards, planning agents pulling recent learnings for proposals, onboarding agents surfacing domain context for new team members.
3. **Independent lifecycle.** The skill's refresh pipeline runs on its own cadence (weekly/monthly). The review agent doesn't need to know about Confluence, YAML indexes, or importance scoring.
4. **Simpler review agent.** The domain-expert reviewer becomes a thin agent focused purely on applying lenses and scoring. Knowledge management complexity is fully isolated.

---

## 3. Design Decisions

All decisions finalized during brainstorming session on 2026-02-15. Updated in v2 and v3 reviews.

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Core purpose | Domain expertise + factual accuracy (combined) | Single subagent covers both specialist knowledge and claim verification |
| D2 | Knowledge source | Standalone skill + web search | Domain Knowledge Skill provides context brief. WebSearch for live claim verification. |
| D3 | Scoring model | Full third dimension (scored /100) | Weighted 50/25/25 with Analysis and Communication |
| D4 | Lenses | 3: Technique Appropriateness, Benchmark & External Validity, Domain Pitfall Awareness | Lens 4 (Claim Verification) merged into Lens 2. 3 lenses, each clearly domain-specific. |
| D5 | Boundary with analysis-reviewer | Model B: Generic vs. Domain-Specific | Analysis-reviewer stays generic. Domain-knowledge adds specialist knowledge. Deduplication rule added. |
| D6 | Web search | Active verification | Reviewer subagent searches web to verify claims and benchmarks |
| D7 | Architecture | Standalone Skill + Thin Reviewer Subagent | Skill provides knowledge. Reviewer applies rubric. Dispatched in parallel with other subagents. |
| D8 | Deduction range | -2 to -20 | Extended from v1 range (-3 to -20) to include ADVISORY severity at -2 |
| D9 | Strength credit cap | +25 (same as other dimensions) | Uniform scoring system |
| D10 | Web search failure | Flag as "unverified" — no deduction | User decides whether to investigate. Agent limitation shouldn't penalize author. |
| D11 | No --domain flag | Require --domain — skip subagent if not passed | 2-way score (analysis + communication) when domain not specified. |
| D12 | Scoring weight | 50/25/25 (Analysis / Communication / Domain) | Analysis rigor is foundational. Domain knowledge and communication are important but secondary. |
| D13 | Knowledge pre-processing | Curated Index + Automated Digest + Live Web Search | Two-tier refresh. Digest pre-built by skill. Web search at review time. |
| D14 | Token budget | 5,000 tokens per domain digest (cross-domain shares budget) | Balances coverage with subagent focus. |
| D15 | Doc importance scoring | LLM-scored (knowledge density + review impact) | Directly measures usefulness for reviews. Handles variable doc quality. |
| D16 | Author identity | Minimal senior roster + Confluence-signal inference | Roster for IC7+ (5-8 people). Everyone else inferred. |
| D17 | Multi-domain support | Comma-separated --domain + cross-domain entries | Analyses often span sub-domains. |
| D18 | Persona (doc author ↔ analysis author) | Deferred to v2 | Latent signal — important but adds complexity. |
| D19 | Knowledge tier precedence | Workstream overrides foundational when they conflict | Team's current understanding supersedes textbook defaults. Conflicts flagged. |
| D20 | Floor rules and weights | Floor rules apply equally regardless of scoring weight | A CRITICAL in any dimension caps the verdict, even if that dimension has lower weight. |
| D21 | Digest versioning | Timestamped digests with rollback | Bad refresh can be reverted. Lead agent falls back to previous version. |

---

## 4. Boundary: Generic vs. Domain-Specific (Model B)

The analysis-reviewer checks **generic DS rigor** (applies to any analysis). The domain-knowledge
reviewer checks **what a specialist in THIS domain would notice** that a generalist wouldn't.

| Scenario | Analysis-reviewer (generic) | Domain-knowledge (specialist) |
|---|---|---|
| Regression without multicollinearity check | "Unstated assumption" | (silent — generic stats issue) |
| Search eval missing position bias correction | (silent — doesn't know search conventions) | "Position bias unaddressed — standard is IPW or randomized experiments" |
| Analyst cites "industry churn rate is 5%" | (silent) | "Verified: plausible for SaaS (3-7% monthly median)" |
| A/B test uses t-test on non-normal data | "Method assumes normality" | "For conversion rate data, chi-squared or bootstrap is domain standard" |
| NDCG@10 used for single-answer search task | "Metric selected — seems reasonable" | "MRR preferred when there's a single right answer" |

**Rule:** If the issue requires domain-specific expertise to identify, it belongs to the
domain-knowledge reviewer. If a generalist DS could identify it, it belongs to the
analysis-reviewer.

### Deduplication Rule (v2+)

When both subagents flag the same underlying finding, the lead agent applies deduplication
in Step 9 using a two-stage approach:

**Stage 1 — Heuristic match (fast, no LLM call):**
- Same metric or method name mentioned in both findings
- Same section of the analysis document referenced
- Both findings recommend the same or similar alternative
- If any two of these match → deduplicate. Keep domain version.

**Stage 2 — LLM fallback (only if Stage 1 is inconclusive):**
- Lead agent presents both findings and asks: "Are these flagging the same underlying issue?"
- If yes → deduplicate. Keep domain version.
- If no → both stand as separate findings.

This two-stage approach avoids an LLM call in the common case (obvious overlaps caught by
heuristic) while handling subtle overlaps correctly.

### Analysis-Reviewer Prompt Guardrail (v2+)

Add to the analysis-reviewer prompt: *"Do not flag issues that require domain-specific
expertise to identify. If you are unsure whether an issue is generic or domain-specific,
skip it."*

---

## 5. Domain Knowledge Skill (Layer 1)

This is a **standalone skill** that manages domain knowledge independently of any consuming
agent. It can be called by the DS review agent, code review agents, planning agents, or
any other tool that needs domain context.

### Skill API

```
get_domain_context(
    domains: list[str],          # e.g., ["search-ranking", "query-understanding"]
    topic_hints: list[str]?,     # optional — topics from the analysis for relevance filtering (v1)
    max_tokens_per_domain: int?  # optional — override default 5,000
) → DomainContextBrief

DomainContextBrief:
    content: str                 # Merged digest content, within token budget
    domains_included: list[str]  # Which domains were included (incl. cross-domain)
    knowledge_tier: dict         # Per-section: "foundational" | "workstream"
    authority_level: dict        # Per-section: "authoritative" | "advisory"
    version: str                 # Digest version timestamp for traceability
    warnings: list[str]          # e.g., "Digest older than 14 days", "Confluence was unavailable"
```

The `authority_level` field is critical — it tells the consuming agent whether a piece of
knowledge should trigger hard deductions (authoritative) or soft flags (advisory). This is
how the tier distinction flows through to the reviewer.

### Two-Tier Digest System

The knowledge base is organized into two tiers with different refresh cadences, stored in a
single digest file per domain with clear section headers.

**Foundational tier (monthly refresh):**
Position bias theory, NDCG/MRR methodology, IPW, interleaving experiment design, offline
vs. online metric relationships, LTR fundamentals. Stable domain knowledge that rarely
changes. Content in this tier is **authoritative** — contradicting it triggers hard deductions.

**Workstream tier (weekly refresh):**
Team standards, project decisions, experiment post-mortems, recent learnings, design doc
outcomes. Fast-moving knowledge that evolves with active work.
- **Standards** within the workstream tier are **authoritative** (hard deductions).
- **Recent learnings** within the workstream tier are **advisory** (ADVISORY severity, -2 deduction, or flags).

### Knowledge Tier Precedence (D19 — Gap 6 fix)

When foundational and workstream knowledge conflict (e.g., foundational says "use IPW for
position bias" but a recent post-mortem says "our randomization makes IPW unnecessary"):

1. **Workstream takes precedence** — the team's current understanding overrides textbook defaults.
2. **The conflict is flagged** in the context brief so the consuming agent can surface it.
3. **During the next foundational refresh**, the conflict triggers a review: should the foundational content be updated?

### Digest File Structure

Each domain produces a single digest file with section headers separating tiers and
authority levels:

```markdown
# search-ranking domain digest
# Version: 2026-02-15T09:00:00Z
# Previous: 2026-02-08T09:00:00Z

## Foundational Knowledge [authority: authoritative] (monthly refresh)
### Evaluation Standards
- NDCG@10 is the primary metric for ranking quality...
- MRR is preferred for single-answer retrieval tasks...

### Known Pitfalls
- Position bias in click data: standard correction is IPW or randomization...
- Selection bias from logging policy: training data reflects current ranker...

### Methodology
- Interleaving experiments are preferred over A/B for ranking changes...

## Workstream Standards [authority: authoritative] (weekly refresh)
### Active Project Decisions
- [2026-02-12] Third-party connector: decided to use federated ranking...
- [2026-02-08] Position bias v2: switching from IPW to doubly-robust...

## Workstream Learnings [authority: advisory] (weekly refresh)
### Recent Experiment Learnings
- [2026-02-10] Embedding retrieval A/B: p99 latency regressed 40ms...
- [2026-02-03] Head vs. tail segmentation: tail queries showed 3x variance...

### Recent Post-Mortems
- [2026-01-28] CTR optimization incident: optimizing CTR alone led to...

## Conflicts
- [2026-02-08] CONFLICT: Foundational says "use IPW for position bias."
  Workstream post-mortem (2026-02-08) says "randomization makes IPW unnecessary
  for our setup." → Workstream takes precedence. Flagged for foundational review.
```

### Digest Versioning and Rollback (D21 — Gap 8 fix)

Digests are versioned with timestamps. Each refresh produces a new version while retaining
the previous version for rollback.

```
plugin/digests/
├── search-ranking.md                    # Current (symlink or copy)
├── search-ranking.2026-02-15T09:00.md   # This week's version
├── search-ranking.2026-02-08T09:00.md   # Previous version (rollback target)
└── ...
```

**Rollback trigger:** If the skill detects an anomaly (digest is empty, token count dropped
by >50% from previous version, LLM importance scores are all near-zero), it emits a warning
and falls back to the previous version. Manual rollback via `--rollback-domain search-ranking`.

### YAML Index Schema

```yaml
# plugin/config/domain-index.yaml

search-ranking:
  # Team space discovery (automatic — finds new/modified docs)
  discovery:
    spaces: ["SEARCH-RANKING"]
    labels: ["ranking-standards", "ranking-eval"]
    # Discovered docs default to workstream tier (Gap 1 fix)
    default-tier: workstream

  # Explicit pages from any space, including personal spaces
  pages:
    - id: "12345"
      title: "Search Ranking Standards"
      tier: foundational
    - id: "12346"
      title: "Evaluation Playbook"
      tier: foundational
    - id: "12347"
      title: "Known Pitfalls & Gotchas"
      tier: foundational
    - id: "99887"
      title: "Q1 2026 Ranking Architecture Direction"
      tier: workstream
      space: "~seniorengineer"   # Personal space — won't be auto-discovered

  # External reference URLs with TTL
  external-references:
    - url: "https://microsoft.github.io/msmarco/"
      description: "MS MARCO leaderboard"
      ttl-days: 30
    - url: "https://trec.nist.gov/pubs.html"
      description: "TREC evaluation guidelines"
      ttl-days: 180

  refresh:
    foundational-cadence: monthly
    workstream-cadence: weekly
    digest-path: "plugin/digests/search-ranking.md"
    retain-versions: 4   # Keep last 4 versions for rollback

query-understanding:
  discovery:
    spaces: ["SEARCH-QU"]
    labels: ["qu-standards", "qu-eval"]
    default-tier: workstream
  pages:
    - id: "12350"
      title: "QU Pipeline Standards"
      tier: foundational
  refresh:
    foundational-cadence: monthly
    workstream-cadence: weekly
    digest-path: "plugin/digests/query-understanding.md"
    retain-versions: 4

search-infra:
  discovery:
    spaces: ["SEARCH-INFRA"]
    labels: ["infra-standards", "latency-budgets"]
    default-tier: workstream
  pages:
    - id: "12360"
      title: "Search Infra Latency Standards"
      tier: foundational
  refresh:
    foundational-cadence: monthly
    workstream-cadence: weekly
    digest-path: "plugin/digests/search-infra.md"
    retain-versions: 4

# Cross-domain knowledge — auto-included when any listed sub-domain is requested
# Shares token budget with requesting domain (Gap 2 fix)
search-cross-domain:
  pages:
    - id: "12370"
      title: "End-to-End Search Evaluation Guide"
      tier: foundational
  applies-to: ["search-ranking", "query-understanding", "search-infra"]
  # No discovery block — cross-domain requires explicit curation
  refresh:
    foundational-cadence: monthly
    digest-path: "plugin/digests/search-cross-domain.md"
    retain-versions: 4
```

### Token Budget and Cross-Domain Handling (D14 — Gap 2 fix)

Each domain gets a **5,000 token budget**. Cross-domain content **shares** the budget of the
requesting domain rather than getting its own allocation.

```
Single domain:   --domain search-ranking
  → 5,000 tokens total, split between search-ranking + cross-domain content

Two domains:     --domain search-ranking,query-understanding
  → 5,000 per domain = 10,000 total
  → Cross-domain content deduplicated (included once, split across both budgets)

Three domains:   --domain search-ranking,query-understanding,search-infra
  → 15,000 total. Cross-domain included once.
```

### Refresh Pipeline Flow

```
Weekly refresh (workstream tier):
1. Read domain-index.yaml for target domain
2. Fetch indexed workstream pages (by ID) via Confluence MCP
3. Discover new/modified pages via Confluence space search (last 14 days)
   → Discovered pages assigned to workstream tier by default (Gap 1)
4. For each doc:
   a. Look up author in team roster (if present) → get author context
   b. If author not in roster → infer authority from Confluence signals
   c. LLM assessment: score knowledge_density + review_impact
   d. Apply Confluence tiebreaker (±0.05)
5. Allocate token budget proportionally by importance score
   → Cross-domain content shares budget with parent domain (Gap 2)
6. LLM synthesis: generate workstream section of digest within token budget
   → Tag each section with authority level (authoritative | advisory)
   → Detect conflicts with foundational tier, add to Conflicts section (Gap 6)
7. Merge with existing foundational section → write new versioned digest file
8. Anomaly check: if digest is empty or token count dropped >50%, warn + keep previous (Gap 8)
9. Flag discovered pages not in index as "candidates for inclusion"

Monthly refresh (foundational tier):
Same flow, but processes foundational-tier pages and rewrites the
foundational section. Also reviews any flagged conflicts from workstream refreshes.

14-day lookback window note: weekly refresh uses a 14-day lookback for discovery,
meaning consecutive weeks overlap. This is intentional — discovery is idempotent
(same doc scored with latest data, latest score wins).
```

### Doc Importance Scoring

Instead of static doc-type weights, importance is scored by LLM during refresh.

**Assessment prompt:**

```
You are a senior Search DS reviewer. Given this document and its author
context, assess:

1. knowledge_density (0.0-1.0): How much extractable domain knowledge
   does this contain? Look for: methodology decisions, evaluation
   standards, experiment results with learnings, pitfalls discovered,
   best practices, architectural constraints.

2. review_impact (0.0-1.0): If a DS analyst writing a search analysis
   did NOT know the contents of this doc, how likely is it that their
   analysis would contain a domain-knowledge error?

Author context: [role, domain, projects — from roster or inferred]

Respond with JSON: {"knowledge_density": X, "review_impact": Y, "rationale": "..."}
```

**Importance formula:**

```
llm_importance = (0.6 * review_impact) + (0.4 * knowledge_density)

confluence_tiebreaker = 0.05 * normalized(
    0.40 * recency_score    +
    0.35 * comment_count    +
    0.25 * incoming_links
)
# Tiebreaker range: -0.05 to +0.05

final_importance = llm_importance + confluence_tiebreaker

token_budget_per_doc = (final_importance / sum_of_all_importances) * budget
# where budget = 5,000 minus cross-domain allocation for this domain
```

### Author Identity

**Minimal senior roster** for IC7+ authors whose seniority materially affects doc importance:

```yaml
# plugin/config/team-roster.yaml
team:
  - confluence-username: "jchen"
    role: "IC9 Principal Engineer"
    primary-domain: search-ranking
    active-projects: ["third-party connector", "position bias v2"]
  - confluence-username: "mwang"
    role: "IC8 Staff Engineer"
    primary-domain: query-understanding
    active-projects: ["query rewriting v3"]
```

**For authors not in roster:** infer authority from Confluence signals:
- Total doc count in team spaces (prolific author = likely senior)
- How many of their docs have high incoming links (referenced author = likely authoritative)
- Cross-space contribution (writes in multiple team spaces = likely senior/cross-functional)

The inferred authority is a softer signal than roster data — it nudges the importance score
but doesn't override the LLM's content-based assessment.

**Doc author ↔ analysis author relationship:** Deferred to v2.

---

## 6. Domain Expert Reviewer (Layer 2)

This is a **thin subagent** that receives a context brief from the Domain Knowledge Skill
and applies the review rubric. It owns no knowledge management logic.

### Inputs

```
1. Analysis document content (from lead agent)
2. Domain context brief (from Domain Knowledge Skill — Layer 1)
   → Includes authority_level per section
3. WebSearch tool access (for live claim verification)
4. Review rubric (3 lenses, deduction tables, scoring rules — embedded in prompt)
```

### Rubric Separation

The subagent prompt is structured to separate the instruction set from the reference material:

```
[SECTION 1: Review Rubric — lenses, deduction tables, scoring rules]
  → Positioned first. This is the instruction set.

[SECTION 2: Domain Context Brief — from skill]
  → Positioned second. This is reference material.
  → Each section tagged with authority level.

[SECTION 3: Analysis Document — the thing being reviewed]
  → Positioned last.
```

### Authority-Aware Scoring (Gap 4 fix)

The reviewer uses the `authority_level` tag from the context brief to calibrate deductions:

- **Authoritative content** (foundational knowledge, workstream standards):
  Finding sourced from this content → apply full deduction per tables below.
- **Advisory content** (workstream learnings, recent post-mortems):
  Finding sourced from this content → capped at ADVISORY severity (-2).
  Presented as: "Recent team learning suggests [X] — worth considering."

---

## 7. Lens Definitions

### Lens 1: Technique Appropriateness

**What it checks:** Is the DS method the right one for this domain? Would a domain expert
choose this approach?

**Checklist:**
1. Is the chosen technique standard/appropriate for this problem type in this domain?
2. Are there domain-standard alternatives the analyst should have considered or justified not using?
3. If a non-standard technique is used, is the choice justified with domain-specific reasoning?
4. Does the technique account for domain-specific data characteristics?

**Deduction table:**

| Issue Type | Severity | Deduction | Example |
|---|---|---|---|
| Fundamentally wrong technique for this domain | CRITICAL | -20 | Using simple correlation for a ranking problem where LTR is standard; no justification |
| Domain-standard technique ignored without justification | MAJOR | -10 | Using t-test for conversion rates when chi-squared or bootstrap is domain standard |
| Offline metric used where online validation is standard | MAJOR | -10 | Recommends ranking model change based solely on offline NDCG lift without online experiment plan |
| Domain-specific data characteristic unaddressed | MAJOR | -8 | Click model without position bias correction in search relevance |
| Non-standard technique used without domain justification | MINOR | -7 | Novel approach without explaining why standard approach was insufficient |
| Recent learning suggests a better approach | ADVISORY | -2 | Recent team experiment found that approach X outperforms approach Y for this use case |

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Domain-standard technique applied correctly | +5 | Technique matches what experts in this domain would choose |
| Alternative techniques considered with domain rationale | +3 | Justified why chosen technique over domain alternatives |
| Domain-specific data preprocessing applied | +3 | Addressed known data issues for this domain (e.g., position debiasing) |

---

### Lens 2: Benchmark & External Validity (merged with former Lens 4)

**What it checks:** Are cited benchmarks real, current, and appropriate for this domain?
Are specific factual claims accurate?

**Checklist:**
1. Are cited benchmarks/baselines real and verifiable? (web search to confirm)
2. Are benchmark values current — not outdated by significant domain shifts?
3. Are benchmarks appropriate for the specific sub-domain?
4. Are internal baselines reasonable compared to known domain ranges?
5. Are externally cited numbers accurate? (web search to verify)
6. Are referenced papers/studies accurately characterized? (not cherry-picked)
7. Are attributed quotes or findings traceable to their stated source?
8. Are domain-specific facts correct? (verifiable, not opinion)

**Deduction table:**

| Issue Type | Severity | Deduction | Example |
|---|---|---|---|
| Cited benchmark is fabricated or grossly wrong | CRITICAL | -20 | "Industry standard NDCG is 0.90" when actual domain range is 0.40-0.55 |
| Key claim is factually wrong and influences conclusions | CRITICAL | -20 | "Google's 2024 study showed X" but study actually showed the opposite |
| External source mischaracterized | MAJOR | -10 | Paper cited as supporting the approach, but paper found mixed results |
| Outdated benchmark used as current reference | MAJOR | -10 | Using pre-2020 CTR benchmarks for a 2026 search system |
| Cited number is inaccurate but doesn't change conclusions | MAJOR | -8 | "Industry average is 12%" when it's actually 8% |
| Benchmark from wrong sub-domain applied | MAJOR | -8 | E-commerce search benchmarks applied to document retrieval |
| Internal baseline not sanity-checked against domain norms | MINOR | -5 | Reporting a metric without noting whether it's in the expected range |
| Claim unverifiable — no source, web search finds nothing | MINOR | -3 | "Research shows that..." with no citation and no verifiable basis |
| Recent learning suggests benchmark is outdated | ADVISORY | -2 | Recent team experiment found different baseline than the one cited |

**Web search failure rule (D10):** When web search *fails* (timeout, no results), the claim
is flagged as "unverified" with **no deduction**. The -3 MINOR above applies only when the
agent actively searched and found the claim to be unsupported.

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Benchmarks cited with verifiable sources | +5 | External benchmarks include source, date, and context |
| All key claims cited and verifiable | +3 | Major factual claims include sources that check out |
| Multiple reference points provided | +3 | Compared against >1 baseline (prior period + industry + competitor) |
| Accurate characterization of external work | +2 | Referenced studies described fairly, not cherry-picked |
| Benchmark recency acknowledged | +2 | Noted when benchmarks are from and whether domain has shifted since |

> **Note:** Credit cap remains +25 per dimension (D9). Total possible credits for this lens
> (+15) intentionally exceed per-lens average to reflect the merged scope. The dimension cap
> prevents inflation.

---

### Lens 3: Domain Pitfall Awareness

**What it checks:** Does the analysis account for known gotchas in this domain?

**Checklist:**
1. Are known domain-specific pitfalls addressed or acknowledged?
2. If a pitfall is not addressed, is the omission justified?
3. Are domain-specific edge cases considered?
4. Does the analysis avoid known domain anti-patterns?

**Deduction table:**

| Issue Type | Severity | Deduction | Example |
|---|---|---|---|
| Known critical pitfall completely ignored | CRITICAL | -15 | Search relevance eval with no mention of position bias when using click data |
| Domain anti-pattern present | MAJOR | -10 | Optimizing CTR alone in search when it's known to favor clickbait over relevance |
| Selection bias in training data unacknowledged | MAJOR | -8 | Click-through model trained on logged data without acknowledging logging policy bias |
| Metric gaming / Goodhart's Law risk unaddressed | MAJOR | -8 | Optimizes single engagement metric without discussing proxy risk |
| Known edge case unaddressed | MAJOR | -8 | Ranking model evaluated only on head queries, no mention of tail query performance |
| Pitfall acknowledged but mitigation missing | MINOR | -5 | "We know position bias exists" but no correction or justification for skipping it |
| Recent learning highlights a pitfall not addressed | ADVISORY | -2 | Recent post-mortem found a failure mode relevant to this analysis |

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Proactively addresses domain pitfalls | +5 | Identifies and mitigates known pitfalls without being prompted |
| Domain edge cases explicitly considered | +3 | Analysis addresses known edge cases (segments, tail behavior, cold-start) |
| Anti-pattern awareness demonstrated | +2 | Explains why a common shortcut was avoided or why it's acceptable here |

---

## 8. Scoring

### Formula

```
With --domain:    final = (analysis * 0.50) + (communication * 0.25) + (domain_knowledge * 0.25)
Without --domain: final = (analysis + communication) / 2  (backward compatible)
```

Each dimension uses the same DR curve and credit system:
- First 30 points of deductions: 100%
- Points 31-50: 75%
- Points 51+: 50%
- Credits capped at +25 per dimension
- `dimension_score = 100 - effective_deductions + credits` (min 0, max 100)

### Severity Levels

| Severity | Deduction Range | Knowledge Source |
|---|---|---|
| CRITICAL | -15 to -20 | Authoritative (foundational or workstream standards) |
| MAJOR | -8 to -10 | Authoritative |
| MINOR | -3 to -7 | Authoritative |
| ADVISORY | -2 | Advisory (workstream learnings only) |

ADVISORY is new in v3. Findings sourced from advisory content (recent learnings,
post-mortems) are capped at ADVISORY regardless of the issue type. This prevents
a recent experiment note from triggering a MAJOR deduction.

### Floor Rules (D20 — Gap 7 fix)

Floor rules apply **equally across all dimensions regardless of scoring weight.** A CRITICAL
in the domain dimension (25% weight) caps the verdict just as a CRITICAL in analysis (50%
weight) does. This is an explicit design decision: a fabricated benchmark or ignored critical
pitfall should cap the verdict regardless of how much weight domain knowledge carries in
the score formula.

- Any CRITICAL in any dimension → verdict capped at Minor Fix (max 79)
- 2+ CRITICAL across any dimensions → verdict capped at Major Rework (max 59)
- ADVISORY findings never trigger floor rules

### Recalibration Plan

Adding a third dimension with weighted scoring changes the formula. Existing calibrated
scores (Vanguard 69, Meta 54, Rossmann 71) will shift. Recalibration steps:

1. Run existing 3 fixtures with domain-knowledge subagent added
2. Compare weighted 3-way scores to current 2-way calibrated scores
3. Determine if DR curve or credit caps need adjustment for the new dimension
4. Target: scores remain in same verdict band (Good/Minor/Major) as current calibration
5. Budget 2-3 calibration rounds (R0 → R1 → R2)

---

## 9. Review Pipeline (Layer 3 — Lead Agent)

### Pipeline Change

```
Step 1:    Parse input — extract --domain flag (comma-separated).
           If absent, skip domain subagent.
Step 2-6:  (unchanged)
Step 6.5:  NEW — If --domain present:
           a. Call Domain Knowledge Skill:
              get_domain_context(domains=["search-ranking","query-understanding"])
           b. Receive DomainContextBrief (pre-built, cached, within token budget)
           c. Check warnings (stale digest, Confluence unavailable, etc.)
Step 7:    Dispatch subagents in parallel:
             ├── analysis-reviewer         → Task tool
             ├── communication-reviewer    → Task tool
             └── domain-expert-reviewer    → Task tool (+ WebSearch + context brief)
           If no --domain: dispatch only 2 subagents (existing behavior).
Step 8:    Handle 2 or 3 subagent results.
Step 9:    Synthesize:
           a. Deduplication (two-stage: heuristic first, LLM fallback):
              → Match overlapping findings between analysis-reviewer and
                domain-expert-reviewer. Keep domain version, suppress generic.
           b. Score:
              - 3 dimensions: final = (analysis * 0.50) + (communication * 0.25)
                              + (domain_knowledge * 0.25)
              - 2 dimensions: final = (analysis + communication) / 2
           c. DR + credits applied per dimension as before.
           d. Floor rules checked across all dimensions.
Step 10:   Output:
           - With domain: 11-row lens dashboard (4+4+3), 3 dimension sections
           - Without domain: 8-row lens dashboard, 2 dimension sections (unchanged)
           - If context brief had warnings: display warning banner above results
```

### New Command Flags

- `--domain <d1,d2,...>` — Required to activate domain review. Comma-separated list mapping to entries in `domain-index.yaml`. If not passed, review runs with 2 dimensions only.
- `--reference <path>` — Optional. **Supplements** (never overrides) the domain digest. Injected into the subagent payload alongside context brief from skill. (Gap 5 fix)
- `--rollback-domain <domain>` — Reverts to the previous digest version for the specified domain.
- `--refresh-domain <domain>` — Forces an on-demand refresh outside the scheduled cadence.

---

## 10. File Changes

| File | Layer | Change |
|---|---|---|
| `plugin/skills/domain-knowledge/SKILL.md` | L1 | **NEW** — Skill definition, API spec, configuration |
| `plugin/skills/domain-knowledge/refresh.sh` | L1 | **NEW** — Refresh pipeline script (weekly/monthly) |
| `plugin/config/domain-index.yaml` | L1 | **NEW** — Curated domain-to-pages mapping |
| `plugin/config/team-roster.yaml` | L1 | **NEW** — Minimal senior author roster |
| `plugin/digests/` | L1 | **NEW** — Directory for versioned domain digest files |
| `plugin/agents/domain-expert-reviewer.md` | L2 | **NEW** — Thin subagent prompt (3 lenses, rubric, authority-aware scoring) |
| `plugin/skills/ds-review-framework/SKILL.md` | L2 | Add: Domain Knowledge deduction table, strength credits, routing rules, deduplication rule |
| `plugin/agents/ds-review-lead.md` | L3 | Update: Step 1 (parse --domain), Step 6.5 (call skill), Step 7 (dispatch), Step 9 (dedup + scoring), Step 10 (output) |
| `plugin/commands/review.md` | L3 | Add: `--domain`, `--reference`, `--rollback-domain`, `--refresh-domain` flags |

---

## 11. Context Management

### Token Budget

Each domain digest is capped at **5,000 tokens**. Cross-domain content shares the budget of
the requesting domain (not additive). Multi-domain reviews scale linearly per domain.

### Two-Pass Retrieval (v1 Evolution)

In v1, the Domain Knowledge Skill will accept `topic_hints` from the lead agent and use them
to filter digest sections before returning the context brief. This reduces effective context
size for multi-domain reviews.

```
v1 get_domain_context(
    domains=["search-ranking"],
    topic_hints=["position bias", "click model", "offline evaluation"]
) → filtered brief containing only sections relevant to those topics
```

---

## 12. Approaches Considered

### Architecture Approaches

| Approach | Verdict |
|---|---|
| A: Monolithic subagent (knowledge + review in one agent) | v2 design — replaced in v3. Knowledge management bloats the reviewer. |
| **B: Standalone Skill + Thin Reviewer** | **Chosen in v3** — clean separation. Skill reusable. Reviewer focused. |
| C: Shared knowledge microservice (external) | Rejected — overkill for plugin scale. Good future evolution if multiple teams adopt. |

### Knowledge Source Approaches

| Approach | Verdict |
|---|---|
| LLM built-in knowledge only | Rejected — insufficient for team-specific standards |
| User-provided context only | Rejected — too much per-review effort |
| **Standalone skill (hybrid: digest + web search)** | **Chosen** — skill provides digest, reviewer does live web search |

### Pre-processing Approaches

| Approach | Verdict |
|---|---|
| A: RAG pipeline (vector search) | Rejected — overkill for plugin scale |
| **B: Periodic digest (AI-synthesized)** | **Adopted** — combined with curated index. Two-tier refresh. |
| C: Just-in-time Confluence search | Rejected — depends on labeling quality |
| D: Curated index + live fetch (v1 design) | Evolved — replaced by pre-built digest for latency and token control |

### Doc Importance Approaches

| Approach | Verdict |
|---|---|
| Static doc-type weights only | Rejected — doesn't handle quality variance |
| Confluence signals only | Rejected — too noisy for remote-first org |
| Human-assigned priority (P0/P1/P2) | Rejected — not feasible |
| **LLM-scored importance (knowledge density + review impact)** | **Chosen** — directly measures what matters |

### Author Identity Approaches

| Approach | Verdict |
|---|---|
| Manual team roster for everyone | Rejected — maintenance burden |
| Infer everything from Confluence signals | Rejected — misses senior authors with low activity |
| **Minimal roster (IC7+) + inference for rest** | **Chosen** — minimal maintenance, captures highest-impact signal |

### Scoring Approaches

| Approach | Verdict |
|---|---|
| Equal 33/33/33 | Rejected — over-weights domain relative to analysis |
| **50/25/25 (Analysis / Communication / Domain)** | **Chosen** — analysis rigor is foundational |

---

## 13. Risks

| Risk | Mitigation |
|---|---|
| Scoring recalibration breaks existing scores | Calibration loop. Budget 2-3 rounds. Target: same verdict bands. |
| Web search adds latency | All 3 subagents run in parallel. Set per-subagent latency budget. |
| Web search returns wrong/outdated info | Agent cites sources. User verifies. |
| Confluence unavailable during refresh | Skill emits warning. Reviewer uses cached digest. |
| Confluence unavailable during review | Skill serves cached digest. Warning in output. |
| Overlap with analysis-reviewer | Two-stage deduplication. Prompt guardrail. Gray-zone fixtures. |
| Digest goes stale between refreshes | Weekly workstream refresh. On-demand `--refresh-domain`. |
| LLM importance scoring inconsistent | Log scores with rationale. Monitor drift. |
| Multi-domain reviews exceed context | 5,000 token budget per domain. Two-pass retrieval in v1. |
| Senior author roster goes stale | Small roster (5-8). Review quarterly. |
| Discovery misses personal-space docs | Explicit page IDs in YAML. Coverage limitation flagged. |
| Poorly-written docs underscored | Author context compensates. Roster provides authority boost. |
| Bad refresh produces corrupt digest | Anomaly detection + versioned rollback (Gap 8). |
| Advisory learnings over-penalize | ADVISORY severity capped at -2. Never triggers floor rules. |
| Foundational-workstream conflicts confuse reviewer | Conflicts section in digest. Workstream takes precedence. Flagged for review. |
| Skill API becomes bottleneck if many agents call it | Skill serves pre-built digests (file read, not computation). Scales trivially. |

---

## 14. Implementation To-Do List

### Phase 1a: Build the Domain Knowledge Skill (Layer 1)
- [ ] Define skill API spec (`get_domain_context` interface)
- [ ] Create `plugin/skills/domain-knowledge/SKILL.md`
- [ ] Create `plugin/config/domain-index.yaml` with initial Search domains (QU, Ranking, Infra, cross-domain)
- [ ] Create `plugin/config/team-roster.yaml` with IC7+ Search authors
- [ ] Build `refresh.sh` — refresh pipeline with LLM importance scoring, Confluence discovery, digest generation, anomaly detection, versioning
- [ ] Run initial refresh to generate digests for all three Search sub-domains + cross-domain
- [ ] Test rollback mechanism

### Phase 1b: Build the Domain Expert Reviewer (Layer 2)
- [ ] Write `plugin/agents/domain-expert-reviewer.md` agent prompt (3 lenses, authority-aware scoring, rubric separation)
- [ ] Add Domain Knowledge deduction table (including ADVISORY) to SKILL.md Section 2
- [ ] Add Domain Knowledge strength credits to SKILL.md Section 2b
- [ ] Update SKILL.md Section 5 routing table with Model B boundary rules + deduplication rule

### Phase 1c: Integrate with Lead Agent (Layer 3)
- [ ] Update analysis-reviewer prompt with domain-specific skip guardrail
- [ ] Update `ds-review-lead.md` Step 1 to parse --domain flag (comma-separated)
- [ ] Add Step 6.5: call Domain Knowledge Skill, receive context brief
- [ ] Update Step 7 to conditionally dispatch 3rd subagent
- [ ] Update Step 8 to handle 2 or 3 results
- [ ] Update Step 9: two-stage deduplication + weighted scoring + floor rules
- [ ] Update Step 10 output templates (conditional 8 or 11-row dashboard + warnings)
- [ ] Update `review.md` with `--domain`, `--reference`, `--rollback-domain`, `--refresh-domain` flags

### Phase 2: Test & Calibrate
- [ ] Test with Vanguard fixture + --domain (expected domain score TBD)
- [ ] Test with Meta fixture + --domain (expected domain score TBD)
- [ ] Test with Rossmann fixture + --domain (expected domain score TBD)
- [ ] Compare weighted 3-way vs 2-way scores — assess recalibration need
- [ ] Run 3 new fixtures (Airbnb x2, Netflix) with all 3 dimensions
- [ ] Test multi-domain review (--domain search-ranking,query-understanding)
- [ ] Test deduplication: gray-zone fixtures, verify no double-penalization
- [ ] Test LLM importance scoring on 20-30 real Search Confluence docs
- [ ] Test rollback: corrupt a digest, verify fallback works
- [ ] Test graceful degradation: Confluence unavailable, verify cached digest serves
- [ ] Cross-run consistency check (same doc 3x, ±10 target)
- [ ] Calibration loop (R0 → R1 → R2 as needed)

### Phase 3: Polish
- [ ] Update CHANGELOG.md
- [ ] Create ADR for domain-knowledge dimension + skill architecture decisions
- [ ] Document refresh pipeline usage (weekly cron + manual trigger + rollback)
- [ ] Document Domain Knowledge Skill API for other agent teams
- [ ] Session end protocol (backlog, session log)

---

## 15. Open Items for Next Session

1. **Skill API implementation** — Implement `get_domain_context` with caching, warning generation, and cross-domain merging.
2. **Refresh pipeline** — Build `refresh.sh` with LLM importance scoring, Confluence discovery, tier assignment, conflict detection, anomaly checking, and versioned output.
3. **Domain index: initial content** — Populate all three Search sub-domains with real Confluence page IDs. Start with 3-5 pages per sub-domain.
4. **Team roster: initial content** — Identify IC7+ Search authors.
5. **Importance scoring calibration** — Score 20-30 real docs, verify against intuition, tune 0.6/0.4 weighting.
6. **Confluence signal weights** — Validate tiebreaker weights against real data.
7. **Cross-domain digest content** — Identify cross-domain knowledge vs. sub-domain-specific.
8. **Deduplication testing** — Build gray-zone fixtures that trigger both reviewers, verify heuristic stage catches common cases.

---

## 16. Version Roadmap

| Version | Key Additions |
|---|---|
| **v0.5 (MVP)** | Domain Knowledge Skill (standalone) + thin reviewer. 3 lenses, 3 Search sub-domains, two-tier digest, LLM importance scoring, minimal roster, 50/25/25 weighting, ADVISORY severity, deduplication, versioned digests. |
| **v1** | Two-pass retrieval via `topic_hints`. Expanded external references. Feedback mechanism for false positives. |
| **v2** | Doc author ↔ analysis author entity linking. Expertise-level-aware feedback. Cross-team domain support (other teams build their own domain indexes against the same skill). |
