# Domain Knowledge Subagent — Design Document

**Date:** 2026-02-15
**Status:** v1 — Design Complete
**Target version:** v0.5

---

## 1. Problem Statement

The current review system has two dimensions — Analysis (generic DS rigor) and Communication
(presentation quality). Neither checks whether the analysis uses **correct domain-specific
knowledge**: right techniques for the problem space, valid benchmarks, awareness of known
pitfalls, or factually accurate claims.

A generalist DS reviewer can check "is the method internally consistent?" but not "is this
the method an expert in search relevance / causal inference / NLP would use?"

---

## 2. Design Decisions

All decisions finalized during brainstorming session on 2026-02-15.

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Core purpose | Domain expertise + factual accuracy (combined) | Single subagent covers both specialist knowledge and claim verification |
| D2 | Knowledge source | User-provided context + web search | Curated index of Confluence pages + WebSearch for claim verification |
| D3 | Scoring model | Full third dimension (scored /100) | Treated equally with Analysis and Communication |
| D4 | Lenses | 4: Technique Appropriateness, Benchmark Validity, Domain Pitfall Awareness, Claim Verification | Matches the 4-lens-per-dimension pattern |
| D5 | Boundary with analysis-reviewer | Model B: Generic vs. Domain-Specific | Analysis-reviewer stays generic. Domain-knowledge adds specialist knowledge. No changes to analysis-reviewer. |
| D6 | Web search | Active verification | Agent searches web to verify claims and benchmarks |
| D7 | Architecture | Approach A: Standalone Parallel Subagent | Dispatched in parallel with existing two. Calibrate independently. |
| D8 | Deduction range | -3 to -20 (same as other dimensions) | Consistency across all dimensions |
| D9 | Strength credit cap | +25 (same as other dimensions) | Uniform scoring system |
| D10 | Web search failure | Flag as "unverified" — no deduction | User decides whether to investigate. Agent limitation shouldn't penalize author. |
| D11 | No --domain flag | Require --domain — skip subagent if not passed | 2-way score (analysis + communication) when domain not specified. No bad context is better than guessed context. |
| D12 | Scoring weight | Equal 33/33/33 | Simplest. Adjust in v2 if needed after calibration data. |
| D13 | Knowledge pre-processing | Curated Index + Live Fetch (Approach D) | YAML index maps domains to Confluence page IDs. Fetched live at review time. |

---

## 3. Boundary: Generic vs. Domain-Specific (Model B)

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

---

## 4. Knowledge Source Architecture

### Curated Index + Live Fetch (Approach D)

A YAML config maps domain names to authoritative Confluence pages. At review time, the lead
agent reads the index, fetches the listed pages via Confluence MCP, extracts relevant knowledge,
and passes it to the domain-knowledge subagent.

```yaml
# plugin/config/domain-index.yaml
search-relevance:
  pages:
    - id: "12345"   # Search Ranking Standards
      title: "Search Ranking Standards"
    - id: "12346"   # Evaluation Playbook
      title: "Evaluation Playbook"
    - id: "12347"   # Known Pitfalls & Gotchas
      title: "Known Pitfalls & Gotchas"
  labels: ["search-standards", "ranking-eval"]

query-understanding:
  pages:
    - id: "12350"   # QU Pipeline Standards
      title: "QU Pipeline Standards"
  labels: ["qu-standards"]
```

### Flow

```
1. User passes --domain search-relevance
2. Lead reads domain-index.yaml → finds 3 page IDs
3. Lead fetches those 3 pages via Confluence MCP
4. Lead extracts relevant knowledge into a domain context brief
5. Domain context brief + document content → domain-knowledge subagent
```

### Why This Approach

| Approach considered | Verdict |
|---|---|
| A: RAG pipeline (vector search) | Rejected — overkill for plugin scale. Needs embedding model + vector DB. |
| B: Periodic digest (AI-synthesized playbook) | Rejected for v1 — good evolution path if latency becomes an issue. |
| C: Just-in-time Confluence search | Rejected — depends on Confluence labeling quality. Less control. |
| **D: Curated index + live fetch** | **Chosen** — simplest thing that works. You control exactly which pages are authoritative. |

### Evolution Path

If live-fetching 5+ pages adds too much latency, evolve to **Approach B**: run a periodic
digest script that synthesizes the same indexed pages into a `domain-digest.md`. The index
file becomes the input to the digest pipeline. No architecture change needed — just swap
live fetch for digest read.

---

## 5. Architecture

### File Changes

| File | Change |
|---|---|
| `plugin/agents/domain-knowledge-reviewer.md` | **NEW** — subagent prompt (4 lenses, web search, domain context) |
| `plugin/config/domain-index.yaml` | **NEW** — curated domain-to-pages mapping |
| `plugin/skills/ds-review-framework/SKILL.md` | Add: Domain Knowledge deduction table (Section 2), strength credits (Section 2b), routing rules (Section 5) |
| `plugin/agents/ds-review-lead.md` | Update: Step 1 (parse --domain flag), Step 7 (dispatch 3rd subagent), Step 8 (handle 3 results), Step 9 (3-way scoring), Step 10 (12-row dashboard) |
| `plugin/commands/review.md` | Add: `--domain` (required for domain review) and `--reference` (optional override) flags |

### Pipeline Change

```
Step 1:    Parse input — extract --domain flag. If absent, skip domain subagent.
Step 2-6:  (unchanged)
Step 6.5:  NEW — If --domain present: read domain-index.yaml, fetch Confluence pages,
           build domain context brief.
Step 7:    Dispatch subagents in parallel:
             ├── analysis-reviewer        → Task tool
             ├── communication-reviewer   → Task tool
             └── domain-knowledge-reviewer → Task tool (+ WebSearch + domain context brief)
           If no --domain: dispatch only 2 subagents (existing behavior).
Step 8:    Handle 2 or 3 subagent results.
Step 9:    Synthesize:
           - 3 dimensions: score = (analysis + communication + domain_knowledge) / 3
           - 2 dimensions: score = (analysis + communication) / 2 (no --domain)
           DR + credits applied per dimension as before.
Step 10:   Output:
           - With domain: 12-row lens dashboard, 3 dimension sections
           - Without domain: 8-row lens dashboard, 2 dimension sections (unchanged)
```

### New Command Flags

- `--domain <name>` — Required to activate domain review. Maps to an entry in `domain-index.yaml`. If not passed, review runs with 2 dimensions only (backward compatible).
- `--reference <path>` — Optional. Path to a local file that overrides or supplements the domain index. Injected directly into the subagent payload alongside indexed Confluence content.

---

## 6. Lens Definitions

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
| Domain-specific data characteristic unaddressed | MAJOR | -8 | Click model without position bias correction in search relevance |
| Non-standard technique used without domain justification | MINOR | -5 | Novel approach without explaining why standard approach was insufficient |

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Domain-standard technique applied correctly | +5 | Technique matches what experts in this domain would choose |
| Alternative techniques considered with domain rationale | +3 | Justified why chosen technique over domain alternatives |
| Domain-specific data preprocessing applied | +3 | Addressed known data issues for this domain (e.g., position debiasing) |

---

### Lens 2: Benchmark & Baseline Validity

**What it checks:** Are cited benchmarks real, current, and appropriate for this domain?

**Checklist:**
1. Are cited benchmarks/baselines real and verifiable? (web search to confirm)
2. Are benchmark values current — not outdated by significant domain shifts?
3. Are benchmarks appropriate for the specific sub-domain?
4. Are internal baselines reasonable compared to known domain ranges?

**Deduction table:**

| Issue Type | Severity | Deduction | Example |
|---|---|---|---|
| Cited benchmark is fabricated or grossly wrong | CRITICAL | -20 | "Industry standard NDCG is 0.90" when actual domain range is 0.40-0.55 |
| Outdated benchmark used as current reference | MAJOR | -10 | Using pre-2020 CTR benchmarks for a 2026 search system |
| Benchmark from wrong sub-domain applied | MAJOR | -8 | E-commerce search benchmarks applied to document retrieval |
| Internal baseline not sanity-checked against domain norms | MINOR | -5 | Reporting a metric without noting whether it's in the expected range |

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Benchmarks cited with verifiable sources | +5 | External benchmarks include source, date, and context |
| Multiple reference points provided | +3 | Compared against >1 baseline (prior period + industry + competitor) |
| Benchmark recency acknowledged | +2 | Noted when benchmarks are from and whether domain has shifted since |

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
| Known edge case unaddressed | MAJOR | -8 | Ranking model evaluated only on head queries, no mention of tail query performance |
| Pitfall acknowledged but mitigation missing | MINOR | -5 | "We know position bias exists" but no correction or justification for skipping it |

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| Proactively addresses domain pitfalls | +5 | Identifies and mitigates known pitfalls without being prompted |
| Domain edge cases explicitly considered | +3 | Analysis addresses known edge cases (segments, tail behavior, cold-start) |
| Anti-pattern awareness demonstrated | +2 | Explains why a common shortcut was avoided or why it's acceptable here |

---

### Lens 4: Claim Verification (Provisional)

> **Note:** This lens is provisional. It may be less impactful than Lenses 1-3 and overlaps
> with web search verification already used by Lens 2. Revisit scope and priority in the
> next architecture design session.

**What it checks:** Are specific factual claims accurate? Uses web search to verify.

**Checklist:**
1. Are externally cited numbers accurate? (web search to verify)
2. Are referenced papers/studies accurately characterized? (not cherry-picked)
3. Are attributed quotes or findings traceable to their stated source?
4. Are domain-specific facts correct? (verifiable, not opinion)

**Deduction table:**

| Issue Type | Severity | Deduction | Example |
|---|---|---|---|
| Key claim is factually wrong and influences conclusions | CRITICAL | -20 | "Google's 2024 study showed X" but study actually showed the opposite |
| External source mischaracterized | MAJOR | -10 | Paper cited as supporting the approach, but paper found mixed results |
| Cited number is inaccurate but doesn't change conclusions | MAJOR | -8 | "Industry average is 12%" when it's actually 8%" |
| Claim unverifiable — no source, web search finds nothing | MINOR | -3 | "Research shows that..." with no citation and no verifiable basis |

**Web search failure rule (D10):** When web search *fails* (timeout, no results), the claim
is flagged as "unverified" with **no deduction**. The -3 MINOR above applies only when the
agent actively searched and found the claim to be unsupported.

**Strength credits:**

| Strength | Credit | Criteria |
|---|---|---|
| All key claims cited and verifiable | +5 | Major factual claims include sources that check out |
| Accurate characterization of external work | +3 | Referenced studies described fairly, not cherry-picked |
| Domain facts precise and current | +2 | Domain-specific facts are accurate and reflect current state |

---

## 7. Scoring

### Formula

```
With --domain:    final = (analysis + communication + domain_knowledge) / 3
Without --domain: final = (analysis + communication) / 2  (backward compatible)
```

Each dimension uses the same DR curve and credit system:
- First 30 points of deductions: 100%
- Points 31-50: 75%
- Points 51+: 50%
- Credits capped at +25 per dimension
- `dimension_score = 100 - effective_deductions + credits` (min 0, max 100)

### Floor Rules

Existing floor rules extend to the third dimension:
- Any CRITICAL in any dimension → verdict capped at Minor Fix (max 79)
- 2+ CRITICAL across any dimensions → verdict capped at Major Rework (max 59)

### Recalibration Plan

Adding a third dimension changes the denominator. Existing calibrated scores (Vanguard 69,
Meta 54, Rossmann 71) will shift. Recalibration steps:

1. Run existing 3 fixtures with domain-knowledge subagent added
2. Compare 3-way scores to current 2-way calibrated scores
3. Determine if DR curve or credit caps need adjustment for the new dimension
4. Target: scores remain in same verdict band (Good/Minor/Major) as current calibration
5. Budget 2-3 calibration rounds (R0 → R1 → R2)

---

## 8. Approaches Considered

### Architecture Approaches

| Approach | Verdict |
|---|---|
| **A: Standalone Parallel Subagent** | **Chosen** — cleanest, follows existing pattern, calibrate independently |
| B: Sequential Enrichment Agent | Rejected — breaks parallel pattern, adds latency, harder to test |
| C: Parallel + Post-hoc Cross-Reference | Rejected — marginal benefit over A, adds Step 9 complexity |

### Knowledge Source Approaches

| Approach | Verdict |
|---|---|
| LLM built-in knowledge only | Rejected — insufficient for team-specific standards |
| User-provided context only | Rejected — too much per-review effort |
| **User context + web search (hybrid)** | **Chosen** — playbook + web verification |

### Pre-processing Approaches

| Approach | Verdict |
|---|---|
| A: RAG pipeline (vector search) | Rejected — overkill for plugin scale |
| B: Periodic digest (AI-synthesized) | Rejected for v1 — good evolution path for latency |
| C: Just-in-time Confluence search | Rejected — depends on labeling quality |
| **D: Curated index + live fetch** | **Chosen** — simplest, you control exactly which pages matter |

### Scoring Approaches

| Approach | Verdict |
|---|---|
| Supplementary (flags only, no score) | Rejected — user wanted full dimension |
| Weighted modifier (±10) | Rejected — not expressive enough |
| **Full third dimension (/100)** | **Chosen** — equal weight, consistent with existing pattern |

---

## 9. Risks

| Risk | Mitigation |
|---|---|
| Scoring recalibration breaks existing calibrated scores | Run calibration loop. Budget 2-3 rounds. Target: same verdict bands. |
| Web search adds latency (may be slowest subagent) | All 3 run in parallel — total time = max(3 agents). Acceptable if < 2 min. |
| Web search returns wrong/outdated info | Agent cites sources and flags confidence. User verifies. |
| Confluence pages unavailable at review time | Graceful degradation: run with LLM + web search only, warn user. |
| Overlap with analysis-reviewer despite Model B | Add explicit routing rules to SKILL.md Section 5. Test with gray-zone fixtures. |
| Lens 4 (Claim Verification) may be low-value | Marked provisional. Revisit in architecture session. May merge with Lens 2 or remove. |
| Domain index goes stale | Lightweight YAML — easy to update. Consider periodic reminder or freshness check. |

---

## 10. Implementation To-Do List

### Phase 1: Build the Subagent
- [ ] Create `plugin/config/domain-index.yaml` with initial search-relevance domain
- [ ] Add Domain Knowledge deduction table to SKILL.md Section 2
- [ ] Add Domain Knowledge strength credits to SKILL.md Section 2b
- [ ] Update SKILL.md Section 5 routing table with Model B boundary rules
- [ ] Write `plugin/agents/domain-knowledge-reviewer.md` agent prompt
- [ ] Update `ds-review-lead.md` Step 1 to parse --domain flag
- [ ] Add Step 6.5 to lead: read domain index, fetch Confluence pages, build context brief
- [ ] Update `ds-review-lead.md` Step 7 to conditionally dispatch 3rd subagent
- [ ] Update `ds-review-lead.md` Step 8 to handle 2 or 3 results
- [ ] Update `ds-review-lead.md` Step 9 scoring formula (conditional 2-way or 3-way)
- [ ] Update `ds-review-lead.md` Step 10 output templates (conditional 8 or 12-row dashboard)
- [ ] Update `review.md` command with `--domain` and `--reference` flags

### Phase 2: Test & Calibrate
- [ ] Test with Vanguard fixture + --domain (expected domain score TBD)
- [ ] Test with Meta fixture + --domain (expected domain score TBD)
- [ ] Test with Rossmann fixture + --domain (expected domain score TBD)
- [ ] Compare 3-way vs 2-way scores — assess recalibration need
- [ ] Run 3 new fixtures (Airbnb x2, Netflix) with all 3 dimensions
- [ ] Cross-run consistency check (same doc 3x, ±10 target)
- [ ] Calibration loop (R0 → R1 → R2 as needed)

### Phase 3: Polish
- [ ] Update CHANGELOG.md
- [ ] Create ADR for domain-knowledge dimension design decisions
- [ ] Session end protocol (backlog, session log)

---

## 11. Open Items for Next Session

1. **Lens 4 (Claim Verification) scope** — Is it valuable enough as a standalone lens, or should it merge with Lens 2 (Benchmark Validity) into a broader "External Validation" lens?
2. **Domain index: initial content** — Populate the search-relevance entry with real Confluence page IDs from the team's actual docs.
3. **Graceful degradation** — If Confluence fetch fails at review time, what's the fallback? LLM + web search only? Or skip dimension entirely?
