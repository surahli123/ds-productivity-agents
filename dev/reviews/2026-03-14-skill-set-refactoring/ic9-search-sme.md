# IC9 Search SME Review — Skill Set Refactoring Implementation Plan

**Reviewer:** IC9 Search SME (Principal/Distinguished Engineer — Search Relevance systems at scale)
**Document:** `docs/plans/2026-03-14-skill-set-refactoring.md`
**Date:** 2026-03-14

---

## Overall Assessment

This is a competent directory restructuring plan for a system that has more interesting problems to solve than where its files live. The 3 prior reviewers covered the mechanical risks well (plugin discovery, verify-before-delete, credit cap). I am not going to re-litigate those. Instead, I am going to focus on what matters from a search relevance evaluation perspective: Is the domain knowledge architecture sound? Is the scoring system actually catching the right things? And is this refactoring the highest-leverage work available? The answer to the first two is "surprisingly good for a v0.5, with specific gaps." The answer to the third is "probably not."

---

## Domain Knowledge Architecture

### The digest-based approach is the right pattern. The current content is shallow.

Separating `search-domain-knowledge` as a standalone skill with a consumption contract is architecturally correct. The analogy to how real search teams work is apt: you have a knowledge base (digests), a contract for consuming it (SKILL.md), an authority model (authoritative vs. advisory), and consumers that read but do not modify it (domain-expert-reviewer, and in the future, SQL review, metric analysis). This is essentially a curated retrieval index for the review agent, which is a pattern I have seen work at scale.

What I like specifically:

- **The authority model is sound.** Authoritative vs. advisory maps directly to how real search teams operate: the textbook says X, our experiments show Y, Y wins for our context. The conflict resolution section (SKILL.md Section 6, "workstream takes precedence") with explicit documentation of overrides is exactly how a team with a mature evaluation culture handles knowledge conflicts. The -2 deduction cap for advisory findings prevents the system from being dogmatic about recent learnings while still surfacing them.

- **The audience filtering (all/ds/eng) is well-designed.** This prevents context bloat and mirrors how different consumers of domain knowledge actually need different subsets. A DS reviewer does not need latency budgets; an engineering reviewer does not need click model taxonomy.

However, the content itself has gaps that matter more than the directory structure:

1. **The search-ranking digest is heavily biased toward offline evaluation and experiment methodology.** It covers NDCG, MRR, ERR, position bias, click models, LTR, interleaving, A/B testing. Good. But real search DS analyses are increasingly about online metric ecosystems, not isolated offline metrics. Where is the coverage of:
   - **Guardrail metrics** — dwell time, pogo-sticking, session success rate, zero-result rate? The CTR optimization incident (DEMO) touches this but as a post-mortem, not as foundational knowledge. A reviewer needs to know the standard guardrail framework.
   - **Engagement vs. satisfaction decomposition?** Every major search team has learned (painfully) that engagement metrics and satisfaction metrics can diverge. CTR goes up, satisfaction goes down. This is the single most common mistake in search metric analysis, and the digest barely mentions it beyond one DEMO incident.
   - **Query-level segmentation for metric analysis?** Head/torso/tail behavior is mentioned in the deduction table (Domain Pitfall Awareness, "Known edge case unaddressed," -8) but the digest does not teach the reviewer what to look for. What is the expected metric variance across segments? What does a head-only evaluation typically miss?

2. **The cross-domain digest covers RAG evaluation (UDCG, RAGAS) which is forward-looking but the pipeline evaluation content is generic.** The component attribution section is useful but reads like a textbook. Real search teams struggle with specific attribution problems: "NDCG went up but conversion went down — is the ranking model wrong or is the query understanding layer routing differently?" The digest does not equip the reviewer to catch this class of issue.

3. **No coverage of feature importance and model interpretability as a review concern.** In practice, a large fraction of search DS analyses involve feature launch evaluations — "we added feature X, here's the offline lift." The reviewer should know how to evaluate whether a feature impact claim is valid (holdout methodology, feature ablation, partial dependence), and the digest has nothing on this.

### The 3 domain reviewer lenses are the right decomposition, with one gap.

Technique Appropriateness, Benchmark & External Validity, and Domain Pitfall Awareness are the right top-level decomposition. They map to the three classes of domain errors I see in practice: wrong method, wrong numbers, and ignored pitfalls.

The gap: **there is no lens for metric selection and metric interpretation**. The analysis-reviewer has a Metrics lens (Lens 4), and the routing table sends "right metrics selected" to analysis-reviewer. But the domain-expert-reviewer should own a harder question: "Is this the right metric for this *search domain problem*?" Choosing NDCG for a navigational query task is a domain error, not a generic DS error. Choosing CTR as the primary success metric for a relevance experiment is a domain error. The analysis-reviewer can catch "metric without context" but cannot catch "wrong metric for this search sub-domain." The routing table partially addresses this (row: "Domain-specific technique choice" goes to domain-expert-reviewer under Technique Appropriateness), but metric selection is not a technique — it is a measurement decision that requires its own evaluation framework.

I would not block on this for the refactoring, but it should be tracked. In a v1.0, I would expect a fourth domain lens: **Metric Fitness** — is the chosen metric appropriate for this search problem type, and are known metric pathologies (position bias in CTR, graded vs. binary in NDCG vs. MRR, proxy metric risk) addressed?

---

## Scoring System Integrity

### The refactoring introduces minimal risk to calibration. The credit cap fix is overdue.

The plan correctly treats the scoring system as a controlled artifact. Copy-verbatim, verify line counts, diff digests, grep for stale paths — this is the right level of paranoia for content that has been calibrated through 4 rounds with known baselines.

The credit cap discrepancy (+25 in 4 files, +15 in framework) is a genuine bug that should be fixed during migration. The DS Lead is right. The R4 calibration was validated against +15. The lead agent's Step 9 says +25. When the LLM follows Step 9 (which it does, since Step 9 is the operative scoring instruction), it applies a +25 cap, potentially inflating scores by up to 10 points on credit-rich analyses. This is not a theoretical concern — the Airbnb interleaving test scored 95/100 with domain credits hitting the cap. If the cap were +25 instead of +15, that score would have been meaningfully higher, breaking the calibration. I agree with the plan's updated Task 10 that fixes this.

### The deduction table is well-designed but has three calibration concerns.

1. **Multi-objective tradeoff at MINOR (-7) may be underweighted.** In production search, ignoring multi-objective tradeoffs is one of the most consequential mistakes an analyst can make. An analysis that optimizes relevance without acknowledging the diversity/freshness/monetization tradeoff can lead to a launched model that degrades the user experience on dimensions the analyst did not measure. In my experience, this is closer to a MAJOR (-10) issue in severity. The R4 calibration notes say "fired consistently across domain reviewers (3/4 Airbnb runs) — no change needed," but consistency of detection is not the same as correctness of severity. I would watch this.

2. **Position bias as CRITICAL (-15) is context-dependent, and the context rules are good.** The domain-expert-reviewer Rule 13 correctly distinguishes between click data informing model decisions (CRITICAL) vs. exploratory analysis with acknowledged limitations (MAJOR). This is one of the few places where the system shows genuine domain sophistication rather than mechanical rule application.

3. **The "Evaluation without exploration/exploitation separation" deduction (-8 MAJOR) is too generous.** In practice, evaluating a ranking model on mixed exploration/exploitation traffic can produce wildly misleading results — exploration traffic often has 2-5x higher metric variance and fundamentally different conversion patterns. If the analysis draws conclusions from this mixed signal, the conclusions may be directionally wrong. This should be CRITICAL when the analysis uses mixed traffic metrics for launch decisions, MAJOR when used for directional analysis. The current flat MAJOR underweights the launch-decision case.

### The 50/25/25 weighting is defensible but creates a known distortion.

The R4 calibration shows that when `--domain` is used on non-search content (Vanguard, Meta, Rossmann), the domain reviewer correctly finds 0 issues and awards a perfect 100, inflating the final score by ~10 points. The plan and calibration notes call this "acceptable since --domain is opt-in," and I agree for now. But this reveals a deeper issue: **the 50/25/25 weighting assumes the domain dimension has comparable information content to analysis.** When the analysis is not domain-specific, the domain dimension is noise, not signal. A smarter weighting would be adaptive: if the domain reviewer finds 0 issues and awards 0 deductions, reduce domain weight to 0 and revert to 50/50. This is a v1.5 item, not a migration blocker, but the system should not permanently reward opt-in domain review for non-domain-specific content.

---

## Extensibility Assessment

### The plugin structure will support SQL Review and Search Metric Analysis, with one architectural concern.

The two-skill separation (ds-review owns the review pipeline, search-domain-knowledge owns the digests) is the right cut for extensibility. A future SQL Review skill would:
- Live at `skills/sql-review/` with its own SKILL.md and references
- Consume `search-domain-knowledge` digests via the same `${CLAUDE_PLUGIN_ROOT}/skills/search-domain-knowledge/digests/` path
- Have its own deduction table, credit table, and subagent prompts

This works cleanly. The consumption contract (SKILL.md Section 2) is generic enough that any consumer agent can follow it.

The architectural concern: **the domain knowledge skill is currently hardcoded to search relevance.** The skill is called `search-domain-knowledge`, the digests are `search-ranking.md`, `query-understanding.md`, `search-cross-domain.md`, and the domain-index.yaml is titled "Domain Knowledge Index — Search Relevance." The plan's vision includes agents that serve "any domain knowledge skill (Search, Causal, NLP, etc.)" — but the current architecture assumes a single domain knowledge skill. If you later need `causal-domain-knowledge` and `nlp-domain-knowledge`, each would need its own skill directory, its own consumption contract, and its own digest format. This is fine architecturally (just add more skills), but the ds-review orchestrator's Step 6.5 is hardcoded to look for digests at `search-domain-knowledge/digests/`. Extending to multiple domain knowledge skills would require modifying the orchestrator to accept a domain knowledge skill path, not just a domain name.

This is not a blocker. It is a note for when you expand beyond search. The right fix when the time comes is to add a `--domain-skill` flag or a registry that maps domain names to skill paths.

### The digest format is a good abstraction boundary, but needs versioning hygiene.

The digest format contract (Section 1 of search-domain-knowledge SKILL.md) is well-specified: metadata header, section structure, authority/audience tags. This is the kind of contract that survives multiple consumers without breaking.

One gap: the "retain 4 versions" policy in domain-index.yaml has no mechanism for garbage collection. Who deletes version 5? The SKILL.md says "Retain previous version for rollback (keep up to 4 versions per domain-index config)" but there is no versioned file naming convention, no cleanup step in the refresh workflow, and no way to identify which version is current vs. historical. For a v0.5 with manual refresh and a single user, this is fine. For a multi-agent system where multiple consumers read digests, version confusion is a real failure mode.

---

## Missing Capabilities

These are capabilities I would expect from a search relevance review system at production maturity. Ordered by impact.

### Must-have for v1.0 (not blocking this refactoring)

1. **Online metric awareness.** The system reviews analyses as documents but has no structured way to evaluate whether an analysis correctly handles online metrics. Does the analysis distinguish between engagement and satisfaction? Does it define guardrail metrics? Does it account for novelty effects? The deduction table has fragments of this (novelty is mentioned under A/B testing duration in the digest), but there is no lens or checklist item that systematically evaluates online metric methodology. For a search relevance review system, this is a gap. Most search analyses that go wrong do so because of incorrect online metric interpretation, not because of incorrect offline metric calculation.

2. **Causal inference methodology for search.** The analysis-reviewer catches generic causal claim errors ("correlation is not causation"). But search-specific causal inference has its own failure modes: interleaving designs that violate SUTVA (interference between treatment and control), difference-in-differences with non-parallel trends across query segments, regression discontinuity misapplied to ranking thresholds. These require domain expertise to catch and should eventually live in the domain expert reviewer.

3. **Feature evaluation methodology.** A large class of search DS analyses are feature launch evaluations. The system has no specific checklist items for: feature ablation methodology, holdout vs. cross-validation for feature importance, partial dependence interpretation, and the common error of confusing marginal feature contribution with total feature impact in a correlated feature space. This is a gap because incorrect feature evaluation can lead to launching (or killing) features based on flawed evidence.

### Nice-to-have for v1.5+

4. **Multi-query analysis evaluation.** Search analyses often involve comparing metric distributions across query segments (head vs. tail, navigational vs. informational). The system does not have specific guidance for evaluating whether segment-level comparisons are statistically valid (e.g., are confidence intervals computed per-segment or pooled? Is the sample size adequate per segment?).

5. **LLM/generative search evaluation.** The cross-domain digest mentions RAGAS and UDCG, which is good. But as search systems increasingly incorporate generative components (AI Overviews, synthesized answers), the review system needs evaluation lenses for faithfulness, hallucination, and grounding quality. This is not needed for the current v0.5 but will become essential within 12 months.

6. **Historical calibration tracking.** The system has 4 rounds of calibration with known baselines, but this history exists only in the backlog. A structured calibration log (fixture, expected score, actual score, delta, date, version) would make regression detection trivial and is a prerequisite for any automated eval loop.

---

## The Refactoring Plan

### Is this the right work to be doing right now?

The PM Lead already asked this question and the answer is: it depends on your time horizon. If you plan to build SQL Review and Search Metric Analysis in Q2 2026 (as the backlog says), you will need the plugin structure eventually. Doing it now, while the system is small (2,800 lines of content, 12 target files), is cheaper than doing it later when there are 3 skills and 10+ files. The cost of delay compounds.

However, the PM Lead is also right that there is untapped value in the existing system. The dogfood test is still open. The output restructure Phase 2 is still open. Genre auto-detection is deferred. These items would make the existing tool more useful to its single user today.

My recommendation: **execute the refactoring, but keep it to one session and do not let it expand scope.** The plan is well-contained at ~12 files of content migration. The three fixes from the review (verify-before-delete reorder, plugin discovery validation, credit cap fix) are all reasonable and the updated plan includes them. Get it done, ship v0.6, and move on to building actual capabilities. Do not spend a second session polishing the plugin structure.

### What the previous reviewers missed

The three prior reviews are solid and I do not have major disagreements with their findings. But they all focused on the migration mechanics and missed two systemic issues:

1. **The review system has no feedback loop.** The calibration rounds (R1-R4) were manual, human-judged adjustments. There is no mechanism for the system to learn from its own reviews. In a production search system, you would never ship an evaluation framework without a meta-evaluation layer: "Did the review scores correlate with actual document quality as judged by downstream consumers?" The plan mentions an "LLM-as-Judge auto-eval pipeline" in the v1.5 backlog — this should be higher priority than it currently is. Without feedback, calibration drift is inevitable.

2. **The system conflates search *evaluation* expertise with search *relevance* expertise.** The digests cover evaluation methodology (NDCG, click models, interleaving) extensively. But a search DS analysis might be about user segmentation, query classification, cold-start strategies, or marketplace dynamics — topics that require search relevance expertise but are not about evaluation methodology. The domain-expert-reviewer's three lenses (Technique Appropriateness, Benchmark & External Validity, Domain Pitfall Awareness) are evaluation-centric. A v1.0 should explicitly decide: is this a search evaluation review system or a search relevance review system? The answer changes what domain knowledge needs to be in the digests.

### What I would do differently

If I were designing this system from scratch with the same constraints (single user, learning to code, side project):

1. **I would not have separate analysis and communication reviewers.** In practice, the most impactful review feedback addresses the intersection: "Your methodology is sound but your presentation of the results will mislead an exec because you buried the confidence interval in a footnote." Splitting analysis and communication into independent reviewers means this class of feedback requires cross-cutting issue detection in the lead orchestrator (Step 9, item 10), which is a fragile mechanism. A single reviewer with 8 lenses (the current 4+4) and explicit instruction to connect methodology to communication in findings would produce more actionable output. But this is an architecture change, not a migration issue, and the 4-round calibration argues against rearchitecting now.

2. **I would invest in the domain digest content before the directory structure.** The search-ranking digest is ~5,000 words. It covers the standard topics (NDCG, position bias, interleaving, LTR) but is thin on practical patterns (guardrail frameworks, feature evaluation, online metric interpretation). Adding 2,000 words of practical content to the search-ranking digest would make the domain reviewer meaningfully more useful than moving the digest from `shared/skills/` to `skills/`. Content quality > file organization.

3. **I would build the calibration fixture suite into the plugin.** The test fixtures in `dev/test-fixtures/` are the most valuable artifacts in this project after the deduction tables. They are the ground truth for regression detection. They should be first-class citizens of the plugin, not development artifacts. A `fixtures/` directory at the plugin root with a `calibration-baselines.yaml` (fixture name, expected score range, known findings) would make regression detection automatic rather than human-memory-dependent.

---

## Key Questions for the Author

1. **Is this a search evaluation review system or a search relevance review system?** The current domain knowledge is almost entirely about evaluation methodology (NDCG, click models, position bias, interleaving). But search DS analyses cover a much broader space: user segmentation, query taxonomies, cold-start modeling, marketplace ranking tradeoffs. If you intend to review those analyses too, the domain digests need substantial expansion beyond evaluation methodology. If you intend to stay focused on evaluation methodology reviews, the system is better positioned but should be named and scoped accordingly. Which is it?

2. **What is your plan for preventing calibration drift as the system evolves?** R4 calibration was validated with specific content, specific deduction values, and specific credit caps. Every content change (new digest content, new deduction types, severity adjustments) risks drifting the calibration. You have 6 test fixtures with known baselines. Will you run all 6 after every content change? After every other change? The current process is manual and depends on you remembering to do it. What happens when you forget?

3. **Why is the feedback loop (v1.5: LLM-as-Judge auto-eval) deprioritized relative to this refactoring and the planned Q2 agents?** The most important missing capability in this system is not SQL Review or Search Metric Analysis — it is the ability to know whether the reviews it produces are actually useful. Without feedback, you are calibrating against your own judgment, which is a sample size of 1. Has any downstream consumer of a ds-review output confirmed that the scoring matched their assessment of the document quality?

4. **Have you considered using the domain digests as retrieval context rather than fixed prompt context?** The current design loads full digest content into the subagent prompt. At 5,000-6,000 tokens after filtering, this is manageable. But if you expand to more domains or add practical content (per my suggestion), token budgets will become a constraint. A retrieval-augmented approach — where the domain reviewer first identifies the relevant topics from the analysis, then retrieves only the relevant digest sections — would scale better and produce more focused domain feedback. This is a v2.0 consideration but worth thinking about before you commit to loading full digests as a permanent pattern.

5. **What is the failure mode for the cross-dimension deduplication when domain knowledge is sparse?** The two-stage dedup (heuristic then LLM comparison) assumes both the analysis reviewer and domain reviewer independently identify the same issue. When domain knowledge is thin (the advisory/demo content in the current digests), the domain reviewer may flag issues at ADVISORY (-2) that the analysis reviewer catches at MAJOR (-10). The dedup logic keeps the domain version ("more specific"), but the domain version has a weaker deduction. Is this the intended behavior? It means adding domain review to a non-search analysis could actually reduce the severity of legitimate analysis findings. The R4 calibration shows this does not happen in practice (domain finds 0 issues on non-search content), but what about analyses that are partially search-related?

---

*Review completed independently. Prior reviews read for context after completing my own evaluation — no findings were adjusted based on other reviewers' perspectives. Domain expertise actively applied throughout.*
