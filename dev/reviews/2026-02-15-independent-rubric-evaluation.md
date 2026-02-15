# Independent Evaluation: DS Review Agent Rubric & Calibration

---

## 1. Rubric Critique (SKILL.md)

### 1a. Deduction Table — What's Good

The deduction table is well-structured. The analysis dimension covers the right four lenses, and the routing table (Section 5) is one of the strongest parts of the design — it solves a real problem (duplicate findings across subagents) that most multi-agent systems ignore. The severity escalation guard is a smart constraint; without it, the agent would almost certainly over-escalate everything to CRITICAL.

The communication dimension's four lenses are comprehensive. The Actionability lens in particular — with its split between proactive (specific recommendations) and reactive (interpretable measurements) modes — is well-thought-out and reflects real DS workflow pain.

### 1b. Deduction Table — What's Missing or Wrong

**Missing issue type: "Selective reporting / cherry-picking."** The analysis dimension has no entry for presenting only favorable results while omitting unfavorable ones. This is different from "missing obvious analysis" (which is about follow-up questions) — cherry-picking is about presenting only the subset of results that supports the desired conclusion. Example: reporting the 10% completion lift but not showing the full-period results that might tell a different story. Proposed: add to Completeness & Source Fidelity, MAJOR, -8.

**Missing issue type: "Metric definition ambiguity."** The Metrics lens catches "missing baseline/benchmark" but not "metric is undefined or ambiguously defined." The Meta review actually flags this ("topline bug reports is undefined") but has to file it under "missing baseline" because there's no better home. These are different problems — you can have a well-benchmarked metric that nobody can define. Proposed: add to Metrics, MAJOR, -8. Example: "Engagement improved by 15%" without defining what engagement means.

**Missing issue type: "Inappropriate generalization scope."** Logic & Traceability has "unsupported logical leap" and "conclusion doesn't trace to evidence," but neither cleanly captures the case where the analysis is valid for the studied population but the conclusion generalizes beyond it. Example: testing on US users, concluding it works globally. This is subtly different from "over-interpretation boundary unclear" (which is a communication issue about *stating* boundaries) — this is an analytical error of *drawing* an overly broad conclusion. Proposed: add to Logic & Traceability, MAJOR, -10.

**"Flawed statistical methodology" (-20 CRITICAL) is too coarse.** This single entry covers everything from "using a t-test on non-normal data with n=5" to "correlation-as-causation." These are vastly different severity levels. A minor methodological concern (e.g., not accounting for multiple comparisons) shouldn't carry the same -20 as a fundamental causal inference error. Proposed: split into "Fundamental methodological flaw" (CRITICAL, -20 — wrong causal framework, survivorship bias presented as finding) and "Methodological weakness" (MAJOR, -10 — suboptimal test choice, missing correction, marginal assumption violation).

**Communication deductions are too flat.** Eight of the eleven communication deductions are MAJOR at -8 to -10. This creates a compression problem — finding 5 communication issues (easy to do on any draft) means -40 to -50 in raw deductions before diminishing returns even kicks in. Meanwhile, the *most* impactful communication failure (TL;DR completely absent) is only -12, while a merely "ineffective" TL;DR is -10. The spread between the worst and the median communication failure is only 2-4 points. Proposed: create more separation. "Buried key finding" is more damaging than "generic headings" but both are in the -8 to -10 range. Consider: reduce "generic headings" to -2, "unnecessary chart" to -2, and "sloppy formatting" to -3. This gives more room for the high-impact items to dominate.

### 1c. Deduction Table — Severity Assignments

Most severity assignments are reasonable. Two specific disagreements:

**"No clear story arc or structure" was correctly reclassified from CRITICAL to MAJOR (-8).** The ADR confirms this was done in calibration and it was the right call. A document can lack a clean arc and still convey useful information.

**"Limitations/scope unclear for downstream" at MAJOR (-10) feels right for internal analyses but slightly harsh for some contexts.** This is on the borderline — I'd keep it but note that this deduction fires on almost every blog post ever written (very few public posts have explicit scope boundaries). If the tool is only used for internal analyses, this is correctly calibrated. If it ever evaluates external content, this will over-fire.

### 1d. Proportionality Check

The analysis dimension's deduction table sums to a theoretical maximum of -101 (if every issue fired). The communication dimension sums to -134. This means the communication dimension is structurally easier to penalize than the analysis dimension. With diminishing returns, this is partially mitigated, but it still means a document that's analytically flawed but well-written will score higher than a document that's analytically strong but poorly written. Given that the final score is a simple average of the two dimensions, this asymmetry matters.

The Vanguard review illustrates this perfectly: Analysis 86, Communication 52. The 34-point spread feels too large. The document is analytically solid with one real issue (post-hoc windowing) — but the communication dimension stacks 8 separate deductions totaling 62 raw points. Is the communication really 34 points worse than the analysis? In my gut assessment, the gap should be closer to 15-20 points.

**Proposed fix:** Either (a) reduce the number of communication deduction entries that can simultaneously fire (max 6 per review), or (b) weight the dimensions unequally (e.g., 55% analysis, 45% communication for a tech audience; 45%/55% for an exec audience). This would also help the Netflix proxy metrics problem I identified earlier, where strong methodology got dragged down by communication penalties.

---

## 2. Strength Credit Table Critique

### 2a. What's Good

The credit table exists at all — this was the single most important calibration fix. The ADR correctly identifies that without credits, a well-designed experiment with one unstated assumption scores the same as a blog post with no methodology. The +8 for real experimental design is appropriately the largest single credit and creates the right incentive gradient.

The evidence requirement ("only credit what's demonstrably in the document") and partial credit rule are both good constraints that prevent credit inflation.

### 2b. What's Missing

**Missing analysis credit: "Novel analytical framework or methodology."** None of the current credits reward intellectual contribution — creating a new way to think about a problem, connecting two fields that weren't previously connected, or proposing an original framework. The Airbnb Listing LTV three-tier framework, the Netflix proxy-as-portfolio insight, and the Meta asymmetric experiments technique would all earn zero credits despite being their articles' strongest features. Proposed: +5 for "Novel framework, methodology, or conceptual contribution that advances how the problem is approached." Criteria: must be more than applying an existing method; must introduce a new lens, decomposition, or connection.

**Missing analysis credit: "Honest negative or null result reported."** The rubric has no mechanism to reward intellectual honesty when things don't work. The Udemy article's admission that fine-tuning failed, or a hypothetical A/B test report saying "we found no significant effect" — these are valuable and should be credited. Too many DS analyses hide null results, and a credit here creates a positive incentive. Proposed: +3 for "Reports a negative, null, or unexpected result without spinning it."

**Missing communication credit: "Effective worked example or scenario."** Several of the best articles in my review set used concrete worked examples to make abstract concepts tangible — Airbnb FIV's booking example, Meta's 10%/10% → 6%/30% holdout calculation, Airbnb Message Intent's Hawaii/Paris scenarios. Worked examples are one of the highest-impact communication tools in DS and the credit table doesn't reward them. Proposed: +3 for "Concrete worked example that makes the methodology or finding tangible."

**The communication credit cap (+25) is too generous relative to actual scores.** In both review outputs, communication credits are +1 (Meta) and +6 (Rossmann). The +25 cap is never approached. Meanwhile, the analysis credit cap (+25) is approached in Vanguard (+22). This suggests the communication credits are either (a) too hard to earn, or (b) missing categories that would naturally fire. Given my review of 5+ blog posts, I think it's (b) — the missing "worked example" credit would help, and the "effective TL;DR" credit (+5) is all-or-nothing when partial credit for a *functional* (but not ideal) opening should be more available.

### 2c. Credit Values — Proportionality

The credit-to-deduction ratio feels about right. The largest single credit (+8 for experimental design) can offset one MAJOR deduction, which is proportionate — having a real experiment is roughly as valuable as fixing one significant gap. The +25 cap prevents credits from overwhelming deductions, which is correct.

One concern: **"Reports specific quantitative results" at +3 is too easy to earn.** Almost any analysis that reports a number gets this credit. It should require that the results are specific *and contextualized* — a bare number like "accuracy was 70%" shouldn't earn the same credit as "accuracy was 70%, up from 45% baseline, with 95% CI [67%, 73%]." Proposed: tighten the criteria to "specific quantitative results with at least one contextualizing element (comparison, CI, or significance test)."

---

## 3. Review Output Evaluation

### 3a. Vanguard Review (69/100)

**Overall assessment: Score feels about right, maybe 2-3 points low.**

My independent gut rating for a document like this (real A/B test, pre-specified hypotheses, no statistical tests reported, no TL;DR, post-hoc windowing) would be about 65-72 for a tech audience. So 69 is in the right zone.

**Findings I agree with:**
- The post-hoc 55-day window (CRITICAL) is the right call. This is genuinely the most important issue — it undermines the causal claim that is the entire point of the analysis.
- Missing statistical tests (MAJOR) is correctly flagged and appropriately not escalated to CRITICAL. The absence of p-values is bad practice but the results could still be directionally valid.
- No TL;DR for a reactive analysis (MAJOR) — correctly identified. The downgrading from CRITICAL to MAJOR (because this is "ineffective" not "absent") is a good calibration call.

**Findings I'd score differently:**
- "A/B test results not interpretable without confidence intervals" (Actionability, MAJOR -8) substantially overlaps with "A/B test results reported without statistical testing" (Metrics, MAJOR -10). The root cause is the same: no statistical tests. The routing table should catch this — the Metrics finding owns the analytical gap, while Actionability should only fire if the statistical context *exists* but isn't *communicated* for the audience. As written, both fire on the same underlying absence. This inflates the communication deductions by -8. Net impact: Vanguard should score ~72-73 instead of 69.

**Missing finding:**
- The Vanguard review doesn't flag that the analysis uses the word "significant" repeatedly without statistical definition. This is listed in the suggested fix for Finding #2, but it deserves its own minor finding under Audience Fit or Metrics. For a tech audience, misusing "significant" is a meaningful credibility issue.

### 3b. Meta Review (54/100)

**Overall assessment: Score feels about right, maybe 2-3 points high.**

My independent gut rating for the Meta LLM bug report article was around 50-55 when evaluated as an exec-targeted proactive analysis. This is a blog post with a causal claim that has no supporting methodology, one vague quantitative result, and no limitations. 54 is reasonable.

**Findings I agree with:**
- Causal attribution without methodology (CRITICAL -20) is absolutely correct. This is the textbook case for this deduction.
- Missing LLM performance evaluation (MAJOR -8) is correct — you can't claim a classification system works without any accuracy metrics.
- Every communication finding is well-identified and well-justified.

**Findings I'd push back on:**
- "Unsupported logical leap: broad impact claim" (Logic, MAJOR -10) partially overlaps with the CRITICAL causal attribution finding. The conclusion overstating impact is downstream of the fundamental problem that the causal claim has no methodology. Penalizing both feels like double-counting the same root cause through two lenses. I'd reduce this to -5 or eliminate it and let the CRITICAL carry the weight.

**What the review gets right that's hard to get right:**
- The distinction between "TL;DR completely absent" (CRITICAL) and "Missing or ineffective TL;DR" (MAJOR) is correctly applied. The Meta article DOES have general framing in its opening — it's just not effective for an exec/proactive context. Calling this MAJOR (-10) rather than CRITICAL (-12) is the right severity call and shows the calibration from ADR-003 is working.

### 3c. Rossmann Review (71/100)

**Overall assessment: Score feels 3-5 points low. I'd rate this 74-76.**

The Rossmann analysis is a thorough end-to-end ML project with strong methodology (time-series CV, 5-model comparison, hypothesis-driven EDA) but terrible communication for its stated audience (CFO in a mixed setting). 71 captures this tension, but the communication dimension at 48 is too punitive.

**Specific concerns with the communication score:**

The Rossmann review stacks 9 communication deductions totaling 76 raw points. Even with diminishing returns compressing this to 58 effective, the communication score of 48 feels too low for a document that has 15+ well-designed charts, a clear hypothesis summary table, and coherent section-by-section logic. The problem isn't that any individual finding is wrong — each one is correct — it's that the *volume* of findings overwhelms the credits.

**The "thinking out loud" in the Strength Log is a red flag.** Lines 236-263 show the agent going back and forth on credit assignments, second-guessing itself three times on Professional Polish, and changing its Story Arc credit twice. This produces the right answer eventually (+6), but in production, this kind of indecision would erode user trust. The agent should commit to an assessment and explain its reasoning once, not debate itself in the output. This is a prompt engineering issue — the subagent prompt should require a single pass with reasoning, not iterative deliberation in the output.

---

## 4. Comparison Against My Independent Analysis

### 4a. Where the Rubric Aligns with My Gut

The rubric's *direction* is consistently correct across all reviewed articles. Articles I rate higher get higher rubric scores; articles I rate lower get lower rubric scores. The rank ordering is right. Specifically:

| Article | My Gut | Rubric Likely Score | Rank Match? |
|---|---|---|---|
| Netflix Proxy Metrics | 90 | ~76 | Same tier |
| Airbnb Listing LTV | 88 | ~84 | Yes |
| Airbnb FIV | 85 | ~73 | Same tier |
| Airbnb Message Intent | 72 | ~63 | Yes |
| Vanguard (actual) | ~70 | 69 | Yes |
| Udemy Intent | 58 | ~28 (pre-calibration estimate) | Rank preserved but magnitude wrong |
| Meta LLM (actual) | ~52 | 54 | Yes |

The calibration (ADR-003) was effective at bringing the scoring into a reasonable range. The R0 scores (16-29) were absurd; the R2 scores (54-71) are defensible.

### 4b. Where the Rubric Diverges from My Gut

**Gap 1: The rubric undervalues methodological elegance and intellectual contribution.** The Netflix proxy metrics article and the Meta asymmetric experiments article are among the best DS writing in the industry, yet the rubric would score them lower than the Airbnb Listing LTV article — because the rubric rewards *framework + use cases* structure over *insight + mathematical rigor*. The credit table has no mechanism to reward "this is a genuinely novel idea" or "this derivation is elegant and illuminating." For internal analyses this may not matter. For evaluating influential DS work, it's a significant blind spot.

**Gap 2: The rubric can't distinguish between "many moderate gaps" and "a few serious gaps."** This is the diminishing returns problem from a different angle. The DR curve helps but doesn't fully solve it. An article with 8 MINOR/MAJOR communication issues (each individually correct) gets hammered, while an article with 2 issues of equal total severity gets a much better score because fewer individual deductions fire. The *experience* of reading these two articles is similar — both need work — but the rubric creates a 15-20 point spread.

**Gap 3: The rubric doesn't account for content genre.** This is my biggest finding from reviewing 6 blog posts. The rubric is calibrated for internal DS deliverables (which the Vanguard and Rossmann fixtures represent). When applied to public blog posts, it systematically penalizes for confidentiality-appropriate vagueness (no exact numbers), genre-appropriate scope (no named owners for a blog post), and audience-appropriate assumptions (not spelling out standard statistical assumptions for a DS audience). The current fixtures don't test this because all three are internal-style analyses. If you ever apply this tool to blog posts, conference talks, or research summaries, the scoring will be systematically too low.

### 4c. The Rossmann Review Exposes a Dimension-Weighting Problem

The Rossmann review has the most extreme dimension split: Analysis 93, Communication 48. The simple average gives 71. But is 71 the right way to value a document that's analytically excellent but communicatively poor?

It depends on the audience. For a peer DS reviewer who will read the full document and can navigate past communication issues, the analytical rigor matters more — maybe 75% analysis weight → score ~82. For the CFO who needs to make a budget decision and will only read the first page, communication matters more — maybe 35% analysis weight → score ~64.

The rubric currently uses a 50/50 split regardless of audience. This underweights analysis for DS peers and underweights communication for execs. The audience persona system (Section 4) is well-designed but only affects *what* gets flagged, not *how the dimensions are weighted*.

---

## 5. Specific Proposed Changes

### Change 1: Add missing deduction types

| Issue Type | Lens | Severity | Deduction | Example |
|---|---|---|---|---|
| Selective reporting / cherry-picking | Completeness & Source Fidelity | MAJOR | -8 | Presenting favorable subgroup results while omitting overall null result |
| Metric definition ambiguity | Metrics | MAJOR | -8 | "Engagement improved 15%" without defining engagement |
| Inappropriate generalization scope | Logic & Traceability | MAJOR | -10 | Tested on US users, concluding it works globally |

Expected impact: catches 1-2 additional findings per review that currently go unreported or get filed under imprecise categories.

### Change 2: Split "Flawed statistical methodology"

| Current | Proposed |
|---|---|
| Flawed statistical methodology (CRITICAL, -20) | **Fundamental methodological flaw** (CRITICAL, -20): Wrong causal framework, survivorship bias as finding, correlation-as-causation |
| | **Methodological weakness** (MAJOR, -10): Suboptimal test choice, missing multiple comparison correction, marginal assumption violation |

Expected impact: prevents minor methodological concerns from triggering CRITICAL floor rules. Reduces false CRITICAL rate.

### Change 3: Add missing credits

| Strength | Credit | Criteria |
|---|---|---|
| Novel framework or methodology | +5 | Introduces a new decomposition, connection, or approach that goes beyond applying existing methods |
| Honest negative/null result | +3 | Reports a result that didn't work without spinning it as positive |
| Effective worked example | +3 | Concrete scenario that makes abstract methodology tangible for the reader |

Expected impact: +3 to +8 for articles with intellectual contributions that currently earn zero credit. Directly addresses the anti-research bias.

### Change 4: Tighten "Reports specific quantitative results" credit

Current: +3 for "Actual numbers reported (not vague claims)."  
Proposed: +3 for "Specific quantitative results with at least one contextualizing element (comparison, CI, significance test, or baseline)."

Expected impact: removes easy +3 for bare numbers. Vanguard still earns it (specific numbers with baseline comparison). Meta blog does not (vague "double digits").

### Change 5: Reduce low-severity communication deduction values

| Issue Type | Current | Proposed |
|---|---|---|
| Generic/non-actionable headings | MINOR, -3 | MINOR, -2 |
| Unnecessary chart or table | MINOR, -3 | MINOR, -2 |
| Sloppy formatting / inconsistent polish | MINOR, -5 | MINOR, -3 |

Expected impact: reduces communication deduction stack by 3-5 points for typical reviews. Makes the gap between MINOR and MAJOR deductions clearer.

### Change 6: Add duplicate-finding detection rule to SKILL.md

Add to Section 5 (Routing Table): "When the same root cause produces findings in both dimensions, apply the LARGER deduction and suppress the smaller one. Example: 'no statistical tests reported' should fire as a Metrics deduction (-10); it should NOT also fire as an Actionability deduction (-8) for the same missing statistical context. The communication reviewer can reference the analysis finding ('as noted by the analysis reviewer, statistical tests are absent — this impacts interpretability') without applying a separate deduction."

Expected impact: -5 to -10 on Vanguard-style reviews where missing statistical tests get double-counted. Vanguard would move from 69 to ~73-74.

### Change 7: Audience-weighted dimension averaging (v1.5)

Instead of 50/50 averaging, weight by audience persona:

| Audience | Analysis Weight | Communication Weight |
|---|---|---|
| Business Executive | 40% | 60% |
| Technical Lead | 55% | 45% |
| Peer Data Scientist | 60% | 40% |
| Mixed (default) | 50% | 50% |

Expected impact: Rossmann (peer DS) would score ~78 instead of 71. An exec-targeted analysis with strong communication but weak methodology would score lower than today. Creates natural alignment between audience expectations and scoring weight.

### Change 8: Suppress self-deliberation in output

Add to subagent prompts: "Commit to each credit and deduction assessment in a single pass. Do not show deliberation, second-guessing, or revision in the output. If a credit is borderline, apply partial credit and state your reasoning once. The user should see a confident assessment, not an internal debate."

Expected impact: fixes the Rossmann "thinking out loud" problem. Improves output professionalism and user trust.

---

## 6. Summary Assessment

The system after R2 calibration is significantly better than R0. The core architecture (lens-based review, deduction + credit, diminishing returns, floor rules) is sound. The ADR-003 decisions were correct. The two example review outputs are detailed, well-structured, and mostly accurate.

The remaining gaps fall into three categories:

**Fixable now (v1.0 polish):** duplicate-finding detection, output self-deliberation suppression, minor deduction value adjustments, tightening the quantitative results credit.

**Important for v1.5:** audience-weighted dimension averaging, the three missing deduction types, splitting "flawed methodology," the three missing credits.

**Design-level awareness (not necessarily fixable):** genre sensitivity for non-deliverable content, the inherent tension between comprehensiveness (catching everything) and proportionality (not over-penalizing for many small issues).

The biggest single improvement available right now is **duplicate-finding detection** — it would immediately fix the Vanguard double-counting problem and is a logic rule, not a rubric redesign.
