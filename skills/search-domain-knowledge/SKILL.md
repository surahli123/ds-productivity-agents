---
name: search-domain-knowledge
description: >
  Domain knowledge for Search Relevance — curated digests of evaluation standards, methodology
  guidelines, and team learnings for search-ranking, query-understanding, and cross-domain topics.
  Pre-built digest files that any agent can consume.
---

# Search Domain Knowledge Skill

Curated domain knowledge for Search Relevance, organized as pre-built digest files. Any
consumer agent (DS reviewer, engineering assistant, onboarding tool) reads digest files
directly — no function calls, no assembly logic. This file defines the contract: how
digests are structured, how to consume them, when they're stale, and how to refresh them.

**Architecture context:** This is Layer 1 of a 3-layer system.
- **Layer 1 (this skill):** Standalone domain knowledge — digest files + consumption contract
- **Layer 2:** Domain Expert Reviewer — `skills/ds-review/references/domain-expert-reviewer.md`
- **Layer 3:** Lead agent integration — `ds-productivity:ds-review` skill

**Key files:**
- `SKILL.md` — this contract (you are here)
- `references/domain-index.yaml` — curated source index
- `digests/` — generated digest files (the product)

---

## 1. Digest File Contract

Every digest file follows a strict format so consumer agents can parse them reliably.
Think of this like a schema definition — if a digest doesn't match this format, something
went wrong during generation.

### Metadata Header

Each digest file starts with metadata headers (markdown comments that double as parseable fields):

```markdown
# [domain-name] domain digest
# Version: [ISO 8601 timestamp, e.g. 2026-02-21T14:30:00Z]
# Previous: [ISO 8601 timestamp of prior version, or "none" if first version]
# Token budget: [number, e.g. 8000]
# Audience tags: all, ds, eng
```

- **Version** is used for staleness checks (see Section 3).
- **Previous** enables rollback — the prior digest is retained alongside the current one.
- **Token budget** documents the target. Actual content should be within ~5% of this number.

### Section Structure

Digest sections appear in this order. Not all sections will have content in every digest,
but the headings must be present (empty sections get a "No content for this section" note).

| Order | Section Heading | Authority | Audience | Content |
|-------|----------------|-----------|----------|---------|
| 1 | `## Foundational Knowledge [authority: authoritative] [audience: all]` | authoritative | all | Broad evaluation standards, core concepts, seminal definitions |
| 2 | `## Foundational Knowledge [authority: authoritative] [audience: ds]` | authoritative | ds | DS-specific methodology — statistical methods, modeling approaches, experiment design |
| 3 | `## Foundational Knowledge [authority: authoritative] [audience: eng]` | authoritative | eng | Engineering-specific standards — latency requirements, system design, infrastructure |
| 4 | `## Workstream Standards [authority: authoritative] [audience: all]` | authoritative | all | Team decisions and standards that override textbook defaults |
| 5 | `## Workstream Learnings [authority: advisory] [audience: ds]` | advisory | ds | Recent experiment results, post-mortems, lessons learned |
| 6 | `## Conflicts` | — | all | Entries where workstream knowledge overrides foundational (see Section 6) |

### Authority Levels

Authority tags control how consumer agents weigh contradictions during review scoring:

- **`authoritative`** — This is established truth (peer-reviewed, team-ratified, or battle-tested).
  Contradicting authoritative content in a review triggers **hard deductions** (-5 to -20
  depending on severity). Example: claiming NDCG handles ties correctly when the foundational
  literature says otherwise.

- **`advisory`** — This is current best thinking, but context-dependent. Contradicting advisory
  content triggers **ADVISORY severity** (-2 max deduction). Example: a team post-mortem found
  that position bias correction wasn't needed for their specific setup — another team's analysis
  might validly disagree.

### Audience Tags

Audience tags control which sections a consumer agent loads, keeping context windows lean:

- **`all`** — Content relevant to any consumer: DS, engineering, PM, onboarding
- **`ds`** — DS-specific content: methodology, statistics, modeling, experiment design
- **`eng`** — Engineering-specific content: latency, systems architecture, indexing, serving

Consumer agents filter by tag at read time (see Section 2). A DS reviewer reads `all` + `ds`
sections. An engineering assistant reads `all` + `eng` sections.

---

## 2. How to Consume Digests

Consumer agents use the Read tool to load digest files. No function calls, no APIs — just
file reads with audience filtering. This keeps consumption trivial and debuggable.

### Single Domain

To consume one domain's knowledge (e.g., search-ranking for a DS reviewer):

```
1. Read digests/search-ranking.md
2. Read digests/search-cross-domain.md  (always include)
3. Filter sections by audience tag: keep [audience: all] + [audience: ds]
4. Check staleness via Version header (see Section 3)
```

The cross-domain digest is **always included** because it contains evaluation frameworks
and methodologies that apply across all search domains.

### Multi-Domain

To consume multiple domains (e.g., both search-ranking and query-understanding):

```
1. Read each requested domain's digest file
2. Read digests/search-cross-domain.md  (once, not per-domain)
3. Concatenate all content, filtering by audience tag
4. Check staleness on each digest's Version header
```

### Token Budgets

Token budgets prevent context window bloat while ensuring sufficient depth:

| Component | Token Budget | Notes |
|-----------|-------------|-------|
| Per-domain digest | 8,000 tokens | Covers foundational + workstream for one domain |
| Cross-domain digest | 1,500 tokens | Additive — not shared with per-domain budget |
| **Single domain effective** | **~9,500 tokens** | 8,000 + 1,500 cross-domain |
| **After audience filtering (DS)** | **~5,000-6,000 tokens** | Excludes [audience: eng] sections |
| **After audience filtering (eng)** | **~5,000-6,000 tokens** | Excludes [audience: ds] sections |
| **Multi-domain (2 domains)** | **~17,500 tokens** | (8,000 × 2) + 1,500 cross-domain |

**Why these numbers:** 8,000 tokens per domain is enough to cover 5-7 foundational sources
and 2-3 workstream sources with meaningful synthesis. After audience filtering, effective
consumption is ~5,000-6,000 tokens — well within a subagent's context budget.

---

## 3. Staleness Thresholds

Digests are snapshots — they can go stale. Consumer agents must check the `# Version:` header
in each digest and compare to the current date. This prevents agents from confidently citing
knowledge that may have been superseded.

| Threshold | Condition | Consumer Behavior |
|-----------|-----------|-------------------|
| **Fresh** | Version < 14 days old | Proceed normally. No warnings. |
| **14-day warning** | Version 14-30 days old | Emit warning: "Domain digest for [domain] is [N] days old. Knowledge may be outdated. Consider running a refresh." Continue with digest content. |
| **30-day critical** | Version > 30 days old | Emit critical warning: "Domain digest for [domain] is [N] days old — exceeds 30-day threshold. Recommend refreshing before using for review scoring." Continue with digest content but flag reduced confidence. |
| **Missing / empty** | Digest file doesn't exist or is empty | **Fatal error.** Consumer should NOT proceed with domain-specific review. Emit: "No digest found for [domain]. Cannot perform domain knowledge review. Run refresh first." |

### How to Check Staleness

Consumer agents parse the Version header and compare:

```
1. Read first 5 lines of digest file
2. Extract ISO timestamp from "# Version: ..." line
3. Compare to current date
4. If difference > 14 days → emit warning
5. If difference > 30 days → emit critical warning
6. If file missing or empty → fatal, do not proceed with domain review
```

---

## 4. Refresh Workflow

Refresh is **manual-only** in v0.5. No cron jobs, no CI pipelines, no auto-discovery.
A human triggers refresh explicitly, and the process runs inside a Claude Code session.

### Trigger

Refresh is invoked via explicit command (future: `--refresh-domain <domain>`). In v0.5,
the user tells the agent which domain to refresh.

### Process Steps

```
1. Read references/domain-index.yaml for target domain
2. Fetch/review each indexed source (papers, blog posts, case studies)
3. For each source: assess importance using the scoring formula (see Section 5)
   - review_impact: How likely is it that NOT knowing this leads to review errors?
   - knowledge_density: How much extractable domain knowledge does this contain?
4. Rank sources by final_importance score
5. Generate updated digest within token budget (8,000 per domain, 1,500 cross-domain)
   - Prioritize highest-importance sources
   - Synthesize into digest sections following the format in Section 1
   - Tag each section with appropriate authority level and audience
6. Write new versioned digest file
   - Update Version header to current timestamp
   - Set Previous header to prior version's timestamp
7. Retain previous version for rollback (keep up to 4 versions per domain-index config)
8. Anomaly check: if digest is empty or token count dropped >50% from previous version,
   warn the user and keep the previous version as primary
```

### Recommended Cadence

These are guidelines, not enforced schedules. The staleness thresholds (Section 3)
provide the actual enforcement mechanism.

| Tier | Recommended Cadence | Rationale |
|------|-------------------|-----------|
| Foundational | Monthly | Seminal papers rarely change; new foundational work appears quarterly at best |
| Workstream | Weekly (when internal sources are available) | Team learnings, post-mortems, and experiment results change frequently |

---

## 5. Importance Scoring

When generating digests, sources must be prioritized within the token budget. Not everything
fits — importance scoring determines what makes the cut.

### Formula

```
final_importance = (0.6 * review_impact) + (0.4 * knowledge_density)
```

Both components are scored 0.0 to 1.0 by the LLM during refresh. The weighting reflects
that **review impact matters more than raw density** — a concise methodology decision that
prevents review errors outweighs a dense survey that's rarely relevant.

### Component Definitions

**`review_impact`** (0.0 - 1.0): Likelihood that NOT knowing this content leads to
domain-knowledge errors in an analysis review.

- 1.0 = Essential. Reviewer would make incorrect domain claims without this.
  *Example: NDCG definition and its graded relevance assumption.*
- 0.5 = Useful. Reviewer would miss context but not make outright errors.
  *Example: History of click model evolution from DBN to NCM.*
- 0.0 = Nice-to-know. No impact on review quality.
  *Example: Author biographical details.*

**`knowledge_density`** (0.0 - 1.0): Amount of extractable domain knowledge per unit of
content — methodology decisions, evaluation standards, experiment results, pitfalls,
best practices.

- 1.0 = Every paragraph contains actionable domain knowledge.
  *Example: A post-mortem documenting why IPW failed and what replaced it.*
- 0.5 = Mixed content — some knowledge, some filler.
  *Example: A survey paper with useful sections buried in literature review.*
- 0.0 = No extractable knowledge for review purposes.
  *Example: A marketing blog post about search relevance.*

### What's Not Included (v0.5)

- **No team roster tiebreaker.** Dropped per MVP decision A4. If LLM scoring proves
  insufficient (brief-but-important docs scoring too low), a roster will be added in v1.
- **No Confluence-based adjustments.** No page view counts, no recency boosts from
  Confluence metadata.

---

## 6. Knowledge Tier Precedence

When foundational knowledge and workstream knowledge conflict, the digest must resolve
the conflict explicitly. This is the most important design decision in the skill:
**workstream takes precedence over foundational.**

### Precedence Rules

1. **Workstream takes precedence** — the team's current understanding, validated through
   their own experiments and production systems, overrides textbook defaults. This mirrors
   how real teams operate: you follow the literature until your data tells you otherwise.

2. **Conflicts are flagged** in the `## Conflicts` section of the digest. Every override
   is documented with:
   - What the foundational source says
   - What the workstream evidence says
   - Why workstream takes precedence

3. **During next foundational refresh**, each conflict triggers a review: should the
   foundational content be updated to reflect the team's findings, or is the conflict
   context-specific?

### Example

```
Foundational says: "Use IPW for position bias correction"
  Source: Joachims et al. (2007) — clicks exhibit strong position bias that must
  be corrected via inverse propensity weighting.

Workstream post-mortem says: "Our randomization design makes IPW unnecessary"
  Source: [Team] Q4 2025 post-mortem — our experiment platform randomizes result
  positions for a holdout set, eliminating the need for post-hoc bias correction.

→ Workstream takes precedence. IPW guidance applies to teams without position
  randomization but not to ours. Flagged in Conflicts section.
```

### Why Workstream Wins

This is analogous to Bayesian updating: foundational knowledge is the prior, workstream
evidence is the likelihood. When the team has direct experimental evidence that contradicts
a general principle, the team's evidence is more informative for their specific context.
The foundational principle isn't wrong — it's just not the best guidance for this team's
situation.
