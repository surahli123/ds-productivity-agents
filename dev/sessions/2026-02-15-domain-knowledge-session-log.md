# Domain Knowledge Subagent — Design Session Log

**Date:** 2026-02-15
**Participants:** DS Lead (user), Claude (IC9 Search architect role)
**Input:** `2026-02-15-domain-knowledge-subagent-design.md` (v1)
**Output:** `2026-02-15-domain-knowledge-subagent-design-v3.md` (v3)
**Session type:** Design review → iterative refinement → architecture revision

---

## Session Summary

Started with a v1 design doc for a Domain Knowledge Subagent (third review dimension for a
Claude Code plugin that reviews DS analyses). Through iterative discussion, evolved from v1
to v3 with a major architectural pivot: extracting the domain knowledge system as a
standalone reusable skill, independent of the DS review agent.

---

## Discussion Flow

### Phase 1: Initial Review (v1 → v2 feedback)

**Role:** Senior DS Lead focusing on Search.

Reviewed the v1 doc across 6 focus areas. Key critiques:

1. **Lens 4 (Claim Verification) — merge into Lens 2.** Lens 4 is domain-agnostic (claim
   checking doesn't require domain expertise) and overlaps with Lens 2's web search
   verification. Recommended merging into a broader "Benchmark & External Validity" lens.
   Result: 3 lenses instead of 4.

2. **33/33/33 scoring weight — too aggressive for domain.** Equal weighting implies domain
   knowledge is as important as analytical rigor. Recommended 50/25/25
   (Analysis/Communication/Domain). Analysis rigor is foundational.

3. **Generic/specialist boundary leaks in practice.** Both subagents can fire on the same
   issue (e.g., t-test on non-normal data). Need a deduplication rule + prompt guardrail
   in the analysis-reviewer.

4. **Curated Index + Live Fetch has a shelf-life of 3-6 months.** YAML index will go stale.
   Recommended `last-reviewed` field and planning the digest evolution sooner.

5. **Missing deduction types for Search:** offline metric without online validation (Lens 1),
   selection bias in training data (Lens 3), Goodhart's Law risk (Lens 3).

6. **Open items resolved:** Merge Lens 4 into Lens 2. Start with 3-5 pages per domain.
   Don't skip dimension on Confluence failure — run with LLM + web search, warn user.

7. **New gaps identified:** Multi-domain support needed (analyses span sub-domains).
   No feedback loop for false positives. Latency underestimated.

**Correction during review:** Initially recommended dropping Lens 1 CRITICAL from -20 to -15.
Retracted after re-reading — the gap between Lens 1 (-20, wrong technique) and Lens 3
(-15, missed pitfall) is justified.

### Phase 2: Scoping to Search MVP

**Role switch:** IC9 Search architect.

User requested narrowing scope to Search domain to validate MVP. Other teams can reuse the
architecture for their own domains.

**Key scoping decisions (via interactive Q&A):**

| Question | Decision |
|---|---|
| Which Search sub-domains in scope? | All three: QU, Ranking, Infra |
| Knowledge velocity handling? | Two tiers (discussed below) |
| Post-mortems in scope? | Yes — critical for Search reviews |

### Phase 3: Knowledge Refresh Architecture

**Problem:** Search domain knowledge moves at different speeds.

Discussed three velocity layers:
- Foundational (position bias theory, NDCG methodology) — stable, changes yearly
- Team standards (evaluation playbooks, experiment standards) — changes quarterly
- Experiment learnings / post-mortems — changes weekly

**User clarification:** Weekly refresh needed for workstream content because critical project
initiatives (like new search strategies) evolve fast. Foundational can be monthly.

**Decision: Two-tier refresh**
- Foundational tier: monthly refresh. Authoritative — contradicting triggers hard deductions.
- Workstream tier: weekly refresh. Standards are authoritative. Learnings are advisory.
- Both tiers stored in single digest file per domain, separated by section headers.

**Token budget discussion:** Digest files could get too long, hurting subagent performance.

| Question | Decision |
|---|---|
| Token budget per domain? | 5,000 tokens (room for post-mortems) |
| Two-pass retrieval? | Yes, but as v1 evolution. MVP uses full digest. |

### Phase 4: Doc Importance Scoring

**Problem:** Not all docs deserve equal token budget in the digest.

**Evolution of approach (4 iterations):**

1. **Doc type + Confluence signals (initial proposal).** Static weights by type
   (strategy=4, standard=3, post-mortem=2, experiment-note=1) with Confluence metadata
   as modifier. User challenged: how to classify doc type without labels?

2. **Tier-specific Confluence signal weights.** Principal Search engineer challenge revealed
   problems: editor count overweights process docs, incoming links penalize recent docs,
   view count is noisy. Proposed tier-specific weights (recency dominates for workstream,
   links dominate for foundational) and replacing view count with comment count.

3. **Doc type as primary, Confluence as tiebreaker.** After user shared org context
   (remote-first, poor labeling, variable doc quality, IC8/9 write important docs with
   few signals), realized Confluence signals are all too noisy. Shifted to type as primary
   ranking with Confluence as small tiebreaker (±0.3).

4. **LLM-scored importance (final decision).** User pointed out doc type classification
   itself is unreliable without labels. Final approach: LLM scores each doc during refresh
   on two dimensions — `knowledge_density` (0.0-1.0) and `review_impact` (0.0-1.0).
   Confluence signals reduced to tiebreaker only (±0.05).

**Importance formula:**
```
llm_importance = (0.6 * review_impact) + (0.4 * knowledge_density)
confluence_tiebreaker = 0.05 * normalized(0.40*recency + 0.35*comments + 0.25*links)
final_importance = llm_importance + confluence_tiebreaker
token_budget_per_doc = (final_importance / sum_all) * 5000
```

### Phase 5: Author Identity / Persona

**User raised:** Doc author's entity/persona matters for importance scoring. Clarified this
means the *Confluence doc author*, not the DS analyst whose work is being reviewed.

**Doc author ↔ analysis author relationship:** Identified as important latent signal but
deferred to v2 due to complexity.

**Problem:** No reliable API to link Confluence authors to role/title.

**Three options discussed:**
- A: Manual roster for everyone — rejected (maintenance burden)
- B: Infer from Confluence signals — rejected (misses senior authors with low activity)
- C: Minimal roster for IC7+ + inference for rest — **chosen**

**Decision:** Maintain roster entries only for 5-8 senior people. For everyone else, infer
authority from Confluence signals (doc count, incoming links on their docs, cross-space
contribution). Inferred authority nudges importance score but doesn't override LLM assessment.

**Expertise-level-aware feedback** (calibrating tone for senior vs junior): deferred to v1.
MVP treats everyone the same.

### Phase 6: v2 Doc Generation and Gap Review

Generated complete v2 design doc (719 lines). Then did a fresh re-read and found 8 gaps:

| Gap | Problem | Resolution |
|---|---|---|
| 1 | Discovered docs have no tier assignment | Default to workstream. Only explicit YAML entries can be foundational. |
| 2 | Cross-domain digest has no token budget | Shares budget with requesting domain (not additive). |
| 3 | Deduplication underspecified | Two-stage: heuristic match first (fast), LLM fallback when inconclusive. |
| 4 | Advisory vs authoritative has no scoring mechanism | New ADVISORY severity at -2. Advisory-sourced findings capped here. |
| 5 | `--reference` override vs supplement unclear | Always supplements, never overrides. |
| 6 | Foundational-workstream conflicts unhandled | Workstream takes precedence. Conflicts flagged. Reviewed at next foundational refresh. |
| 7 | Floor rules + 50/25/25 interaction | Explicit decision: floor rules apply equally regardless of weight. |
| 8 | No digest versioning or rollback | Timestamped versions, anomaly detection, `--rollback-domain` flag. |

### Phase 7: Architecture Pivot (v2 → v3)

**User insight:** The domain knowledge system should be independent of the DS review agent.
It could be a standalone skill/service that any agent can call.

**This was the biggest architectural change of the session.**

v3 splits the system into three layers:
- **Layer 1: Domain Knowledge Skill** — standalone service. Owns YAML index, roster,
  digests, refresh pipeline, importance scoring. Exposes `get_domain_context()` API.
- **Layer 2: Domain Expert Reviewer** — thin subagent. Calls Layer 1 for context, applies
  3 lenses and scoring rubric. No knowledge management logic.
- **Layer 3: DS Review Lead** — orchestrator. Dispatches subagents, handles deduplication
  and scoring.

**Benefits:** Reduced review-time latency (skill pre-computes context), reusable across
agents (code review, planning, onboarding), independent lifecycle, simpler reviewer.

---

## All Decisions (Comprehensive)

### Lens & Scoring Decisions

| Decision | Choice |
|---|---|
| Lens count | 3 (merged Lens 4 into Lens 2) |
| Lens 2 name | "Benchmark & External Validity" |
| Scoring weight | 50/25/25 (Analysis / Communication / Domain) |
| Severity levels | CRITICAL, MAJOR, MINOR, ADVISORY (new) |
| ADVISORY deduction | -2, only for advisory-sourced findings |
| Floor rules + weights | Floor rules apply equally regardless of weight |
| Deduction range | -2 to -20 |

### Knowledge Architecture Decisions

| Decision | Choice |
|---|---|
| Architecture | Standalone skill (Layer 1) + thin reviewer (Layer 2) |
| Refresh tiers | Foundational (monthly) + Workstream (weekly) |
| Digest format | Single file per domain, section headers separating tiers |
| Token budget | 5,000 per domain. Cross-domain shares budget. |
| Doc importance | LLM-scored (knowledge_density + review_impact) |
| Confluence signals | Tiebreaker only (±0.05). Recency/comments/links. |
| Tier precedence | Workstream overrides foundational on conflict |
| Discovered doc tier | Default to workstream |
| Digest versioning | Timestamped, anomaly detection, rollback support |

### Author & Persona Decisions

| Decision | Choice |
|---|---|
| Author identity | Minimal roster (IC7+) + Confluence inference for rest |
| Roster size | 5-8 senior people |
| Expertise-level feedback | Deferred to v1. MVP treats all levels the same. |
| Doc author ↔ analysis author | Deferred to v2. Important latent signal. |

### Boundary & Integration Decisions

| Decision | Choice |
|---|---|
| Generic/specialist boundary | Model B with deduplication rule |
| Deduplication method | Two-stage: heuristic first, LLM fallback |
| Analysis-reviewer guardrail | Prompt instruction to skip domain-specific issues |
| `--reference` flag | Supplements digest, never overrides |
| `--domain` flag | Comma-separated, maps to domain-index.yaml |
| Graceful degradation | Run with LLM + web search, warn user, keep 3-way scoring |

### Search MVP Scope

| Decision | Choice |
|---|---|
| Sub-domains in scope | QU, Ranking, Infra (all three) |
| Multi-domain support | Comma-separated `--domain` + cross-domain entries |
| Post-mortems | In scope |
| Two-pass retrieval | v1 evolution (topic_hints parameter) |
| Feedback mechanism | v1 evolution |

### Added Deduction Types (Search-specific)

| Lens | Issue Type | Severity | Deduction |
|---|---|---|---|
| Lens 1 | Offline metric without online validation | MAJOR | -10 |
| Lens 3 | Selection bias in training data unacknowledged | MAJOR | -8 |
| Lens 3 | Metric gaming / Goodhart's Law risk unaddressed | MAJOR | -8 |
| All | Recent learning suggests improvement (advisory) | ADVISORY | -2 |

---

## Org Context Provided by User (Important for Implementation)

These details about the user's organization shape multiple design decisions:

1. **Remote-first company.** Engineers review docs by reading + commenting, not by editing.
   Editor count is an anti-signal for importance (correlates with shared living docs, not
   important decisions).

2. **Confluence hygiene is low.** People don't label docs. No consistent structure. Doc
   quality ranges from poorly written to highly detailed. Some docs are narrow/focused,
   some are broad.

3. **Personal spaces used for important docs.** Engineers sometimes write critical docs in
   personal Confluence spaces rather than team spaces. Discovery mechanism won't find these
   automatically — need explicit page IDs in YAML.

4. **IC8/9 write important docs with few signals.** Senior engineers write critical strategy
   docs that may have few views, few comments, and few editors. Confluence signals alone
   would underrank these. This is why the minimal senior roster exists.

5. **Search sub-domains are not cleanly separable.** Most meaningful analyses touch at least
   two sub-domains (e.g., QU change evaluated by ranking metrics). Cross-domain support is
   first-class, not an add-on.

6. **Critical workstreams evolve fast.** New project initiatives (like third-party connector)
   can produce important strategy decisions weekly. This drives the weekly workstream refresh.

7. **No internal entity linking API** reliably connects Confluence authors to roles/titles.
   This is why we use a minimal roster instead of automated role lookup.

---

## Files Generated This Session

| File | Description |
|---|---|
| `2026-02-15-domain-knowledge-agent-review.md` | Initial review feedback (v1 critique) |
| `2026-02-15-domain-knowledge-subagent-design-v2.md` | v2 design doc (intermediate) |
| `2026-02-15-domain-knowledge-subagent-design-v3.md` | v3 design doc (final — standalone skill architecture) |
| `2026-02-15-domain-knowledge-session-log.md` | This file |

---

## Next Steps for Claude Code

### Immediate (Phase 1a — Layer 1: Domain Knowledge Skill)
1. Implement `get_domain_context()` skill API per spec in v3 doc Section 5
2. Create `domain-index.yaml` with real Confluence page IDs for Search sub-domains
3. Create `team-roster.yaml` with IC7+ Search authors
4. Build refresh pipeline (`refresh.sh`) with:
   - Confluence fetch (indexed pages + discovery)
   - LLM importance scoring (knowledge_density + review_impact)
   - Token budget allocation
   - Digest generation with tier sections + authority tags
   - Anomaly detection + versioned output

### Then (Phase 1b — Layer 2: Domain Expert Reviewer)
5. Write `domain-expert-reviewer.md` subagent prompt:
   - 3 lenses with ADVISORY severity
   - Authority-aware scoring (authoritative vs advisory content)
   - Rubric separated from domain context in prompt structure

### Then (Phase 1c — Layer 3: Lead Agent Integration)
6. Update `ds-review-lead.md`:
   - Step 6.5: call skill API
   - Step 9: two-stage deduplication + 50/25/25 weighted scoring
   - Step 10: 11-row dashboard + warning banners
7. Update `review.md` command with new flags

### Calibration (Phase 2)
8. Run fixtures, compare 3-way vs 2-way scores
9. Test importance scoring on 20-30 real Search docs
10. Test deduplication with gray-zone fixtures
11. Calibration loop (R0 → R1 → R2)
