# Proposal: SKILL.md Immediate Fixes for v1.0

**Date:** 2026-02-15
**Author:** Independent Reviewer (Claude)
**Status:** Proposal for Claude Code implementation
**Scope:** 6 targeted changes to SKILL.md — no architecture changes, all table edits

---

## Background

This proposal is grounded in two independent evaluation passes:

1. **Blog post calibration (6 articles):** I independently scored 6 published DS analyses from Meta, Airbnb, Netflix, and Udemy using (a) gut feeling and (b) the v1 PRD rubric, then compared. This produced 6 systematic biases and 8 recommendations.

2. **Current system evaluation:** I reviewed the latest SKILL.md, ADR-003, and all three R2 review outputs (Vanguard, Meta, Rossmann), then cross-referenced against the blog post findings to identify what was fixed and what remains.

The R2 calibration (ADR-003) successfully fixed the two most severe problems: the absence of strength credits (Bias 4) and linear deduction stacking (Bias 6). Scores moved from 16-29 (R0) to 54-71 (R2), which is a defensible range.

Six gaps remain. Each is traceable to specific scoring failures observed in the blog post analysis, the current review outputs, or both. All six are implementable as SKILL.md table edits.

---

## Fix 1: Duplicate-Finding Detection Rule

### Problem

The same root cause gets penalized in both the analysis and communication dimensions, inflating the total score penalty.

### Evidence

**In the Vanguard review (current R2 output):** "No statistical tests reported" fires as:
- Finding #3 (Metrics lens, MAJOR -10): results reported without statistical testing
- Finding #6 (Actionability lens, MAJOR -8): results not interpretable without confidence intervals

These are the same underlying absence. The analysis reviewer correctly identifies the gap; the communication reviewer then re-penalizes its downstream consequence. Cost: -18 instead of -10, which inflates the communication deductions and drops the final score by ~4 points.

**In my Udemy blog analysis (v1 rubric):** A fluffy opening was penalized as both "no TL;DR" (-10) and "not concise" (-5) — same root cause, two deductions.

The routing table (Section 5) handles gray-zone *ownership* well but has no rule for *same-root-cause duplication* across dimensions.

### Proposed Change

Add to SKILL.md Section 5 (Dimension Boundary Routing Table), after the existing rule:

> **Duplicate suppression rule:** When the same root cause produces findings in both dimensions, the subagent that owns the root cause applies its deduction at full value. The other subagent may reference the finding for context but does NOT apply a separate deduction. The root cause owner is determined by the routing table above. Example: "No statistical tests reported" is owned by analysis-reviewer (Metrics lens). The communication-reviewer may note "as identified in the analysis dimension, the absence of statistical tests limits interpretability for this audience" but does not apply an Actionability deduction for the same gap.

### Expected Impact

+3 to +4 points on reviews like Vanguard where statistical rigor gaps currently get double-counted. No impact on reviews where findings are genuinely independent across dimensions.

---

## Fix 2: Novel Framework / Methodology Credit

### Problem

The analysis credit table rewards methodological *discipline* (experimental design, hypotheses, balance checks) but not methodological *contribution* (novel frameworks, original insights, new conceptual connections). This means a mediocre A/B test with pre-specified hypotheses earns +13, while a groundbreaking analytical framework earns +0.

### Evidence

**From my blog post analysis (6 articles):**
- Airbnb Listing LTV's three-tier framework (baseline → incremental → marketing-induced LTV) is the article's most important contribution. Credit earned: +0.
- Netflix proxy metrics' connection between proxy construction and weak instrumental variables was published at KDD 2024. Credit earned: +0.
- Meta's asymmetric experiment technique with the nonlinear tradeoff derivation is directly useful to any experimentation team. Credit earned: +0.
- Airbnb FIV's propensity score matching platform with the counterintuitive insight about high AUC being bad for matching quality. Credit earned: +0.

All four articles' strongest qualities are invisible to the credit system. Meanwhile, all 8 existing analysis credits reward *process compliance* — which is important but not sufficient. This is the structural root of Bias 1 (Anti-Research Bias) from my blog analysis.

### Proposed Change

Add to SKILL.md Section 2b, Analysis Dimension Credits:

| Strength | Credit | Criteria |
|---|---|---|
| Novel analytical framework or methodology | +5 | Introduces a new decomposition, framework, or conceptual connection that goes beyond applying an existing method to new data. Must be evident in the document — do not infer from author reputation. Examples: a new metric framework, a novel connection between two fields, an original problem decomposition. Counter-examples: applying standard PSM, running a standard A/B test, using off-the-shelf ML models. |

### Expected Impact

+5 for articles with genuine intellectual contributions. Does not fire on routine analyses. The +25 cap per dimension prevents this from dominating the score.

---

## Fix 3: Worked Example Credit

### Problem

Concrete worked examples are one of the most effective communication tools in methodology-heavy DS content, but the credit table doesn't reward them. The closest credit ("Effective data visualization," +3) is specifically about charts.

### Evidence

**From my blog post analysis:**
- Meta asymmetric experiments: the 10%/10% symmetric → 6%/30% asymmetric holdout calculation with the 4.4% engagement gain quantification. This is the moment the article becomes tangible. Credit earned: +0.
- Airbnb FIV: the guest booking example that walks through focal vs. complement groups. Makes PSM concrete. Credit earned: +0.
- Airbnb Message Intent: the Hawaii bed-count and Paris cancellation scenarios. Immediately relatable. Credit earned: +0.

**In the Rossmann R2 review:** The reviewer calls out "business translation of model error into revenue scenarios" as a positive finding — the best/worst scenario table translating MAPE into R$ ranges. This is a worked example that bridges methodology and business impact. The reviewer credits it under "Effective data visualization" (+3), but it's not a visualization — it's a numerical scenario. The category is a stretch.

### Proposed Change

Add to SKILL.md Section 2b, Communication Dimension Credits:

| Strength | Credit | Criteria |
|---|---|---|
| Effective worked example or scenario | +3 | Concrete numerical example or relatable scenario that makes an abstract methodology, framework, or finding tangible for the reader. Must walk through specific values, not just describe the approach generically. |

### Expected Impact

+3 for articles and analyses that include concrete examples. Gives a proper home for the Rossmann revenue scenario credit instead of stretching "data visualization." Would also reward internal analyses that include "for example, if Store A has X bookings..." walkthroughs.

---

## Fix 4: Honest Negative / Null Result Credit

### Problem

The rubric has no mechanism to reward intellectual honesty when things don't work. Reporting failures is valuable and rare — most DS analyses hide null results.

### Evidence

**From my blog post analysis:**
- Udemy intent article: honestly reports that fine-tuning embeddings with hard negatives failed after "many experimental trials using different embedding models and different loss functions." This is valuable information for anyone building a similar system. Credit earned: +0.

**In the Rossmann R2 review:** The reviewer notes "the honest reporting that linear models performed worse than the average model is a sign of analytical integrity" as a positive finding. This is a null/negative result — the linear models didn't work, and the author reports this rather than omitting them from the comparison. But there's no credit category for it.

### Proposed Change

Add to SKILL.md Section 2b, Analysis Dimension Credits:

| Strength | Credit | Criteria |
|---|---|---|
| Honest negative or null result reported | +3 | Reports a result that didn't work, an approach that failed, or an unexpected finding without spinning it as positive. Must be a substantive finding, not a throwaway mention. Examples: "We tested approach X and it did not improve performance," "Hypothesis Y was not supported by the data." |

### Expected Impact

+3 for analyses that report what didn't work. Creates a positive incentive for intellectual honesty. Does not fire on analyses that only report successes.

---

## Fix 5: Reduce Low-Severity Communication Deductions

### Problem

The communication dimension has 134 possible deduction points vs ~101 for analysis. Eight of eleven communication deductions are MAJOR (-8 to -10), creating a compression problem where finding 5 communication issues — easy on any draft — means -40 to -50 raw deductions. Three MINOR deductions are priced too high relative to their actual impact on the reader.

### Evidence

**In the Vanguard R2 review:** Communication raw deductions total 62 from 8 findings. Three MINOR deductions contribute -16 total: generic headings (-3), sloppy formatting (-5), and the remaining MAJORs. The formatting deduction at -5 is disproportionate — it's a polish issue scored at 63% of a MAJOR.

**In the Rossmann R2 review:** Communication raw deductions total 76 from 9 findings. The -5 for sloppy formatting and -3 for generic headings contribute -8, which is enough to shift the dimension score by 3-4 points after DR.

**From my blog analysis:** I noted that MINOR deductions "stack with every MAJOR finding to push communication scores into the 40s-50s routinely." Both current R2 outputs confirm this — Vanguard communication: 52, Rossmann communication: 48.

The issue isn't that any individual deduction is wrong. It's that the spread between the lowest MINOR (-3) and the median MAJOR (-8 to -10) is only 3-5 points, which means MINORs carry disproportionate weight in the total.

### Proposed Change

Modify SKILL.md Section 2, Communication Dimension deductions:

| Issue Type | Current | Proposed | Rationale |
|---|---|---|---|
| Generic/non-actionable headings | MINOR, -3 | MINOR, -2 | Headings are a polish issue, not a structural failure |
| Unnecessary chart or table | MINOR, -3 | MINOR, -2 | Clutter is minor relative to missing or misleading charts |
| Sloppy formatting / inconsistent polish | MINOR, -5 | MINOR, -3 | Currently priced at 63% of a MAJOR; should be ~30-38% |

### Expected Impact

Saves 3-4 raw deduction points on typical reviews. After DR compression, this translates to +1 to +2 on the final score. Small but consistent — addresses the structural over-punitiveness of the communication dimension without changing any rank ordering.

---

## Fix 6: Tighten "Reports Specific Quantitative Results" Credit

### Problem

The current criteria — "Actual numbers reported (not vague claims like 'significant improvement')" — is too easy to earn. Any analysis that reports a bare number ("accuracy was 70%") qualifies, even when the number lacks context that would make it meaningful.

### Evidence

**From my blog post analysis:** The Meta LLM bug report article reports "double digits" — vague enough to correctly NOT earn this credit. But an article reporting "accuracy was 70%" with no baseline, no CI, and no benchmark would earn +3, despite being barely more useful. A number without context is closer to trivia than to a "specific quantitative result."

**In the Vanguard R2 review:** The credit is correctly awarded (+3) because the analysis reports specific numbers WITH comparison context (10% lift vs 5% threshold, retention rates across steps). This is the right standard — but the criteria text doesn't require the comparison context.

**In the Meta R2 review:** The credit is correctly NOT awarded (+0) because the only number is "double digits." But the criteria text ("Actual numbers reported") could be read as awarding credit for any specific number, which would create inconsistent application across reviews.

### Proposed Change

Modify SKILL.md Section 2b, Analysis Dimension Credits:

| Strength | Current Criteria | Proposed Criteria |
|---|---|---|
| Reports specific quantitative results (+3) | Actual numbers reported (not vague claims like "significant improvement") | Specific quantitative results with at least one contextualizing element: comparison to baseline, confidence interval, significance test, or benchmark. A bare number without any context (e.g., "accuracy was 70%" with no comparison point) does not qualify. |

### Expected Impact

Prevents unearned +3 on weak analyses that report bare numbers. No impact on analyses that already contextualize their results (Vanguard, Rossmann both still qualify). Makes the credit criteria consistent with what the agent is actually doing in the R2 outputs.

---

## Implementation Priority

All 6 fixes are SKILL.md table edits. No architecture changes, no prompt restructuring, no new agents.

| Priority | Fix | Type | Effort |
|---|---|---|---|
| **P0** | Fix 1: Duplicate-finding detection | Add rule to Section 5 | One paragraph |
| **P0** | Fix 5: Reduce MINOR communication deductions | Change 3 values in Section 2 | Three number edits |
| **P0** | Fix 6: Tighten quantitative results credit | Edit criteria text in Section 2b | One sentence |
| **P1** | Fix 2: Novel framework credit | Add row to Section 2b | One table row |
| **P1** | Fix 3: Worked example credit | Add row to Section 2b | One table row |
| **P1** | Fix 4: Honest negative result credit | Add row to Section 2b | One table row |

P0 fixes correct active scoring errors visible in the current R2 outputs. P1 fixes add capability that is missing but hasn't caused a scoring failure on the current test fixtures (it would on blog posts).

---

## Validation Approach

After implementing these 6 fixes, re-run the three R2 fixtures (Vanguard, Meta, Rossmann) and verify:

1. **Vanguard score increases by 3-5 points** (from 69 to ~72-74) due to duplicate suppression and MINOR reduction
2. **Meta score stays roughly the same** (~54 ± 2) — none of the fixes benefit a weak analysis without methodology
3. **Rossmann score increases by 2-4 points** (from 71 to ~73-75) due to MINOR reduction and potential worked-example credit for the revenue scenario table
4. **Rank ordering preserved:** Rossmann ≈ Vanguard > Meta
5. **Differentiation gap preserved or slightly widened:** currently 15 points (Rossmann 71 vs Meta 54), should remain 15+ points
