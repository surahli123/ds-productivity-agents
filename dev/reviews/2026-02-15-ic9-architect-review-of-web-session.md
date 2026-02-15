# IC9 Architecture Review: Web Session Rubric Proposal

**Date:** 2026-02-15
**Reviewer:** IC9 Principal Architect
**Reviewing:** Web session's independent rubric evaluation and 6 proposed SKILL.md fixes
**Input files:** `proposal_skillmd_immediate_fixes.md`, `independent_rubric_evaluation.md`, `ds_blog_rubric_analysis.md`
**Status:** Review complete — recommendations below

---

## Overall Assessment

The web session did strong independent work. The blog post calibration analysis (gut-feel vs rubric scoring on 6 articles, then gap analysis per article) is the most valuable artifact — it provides external calibration evidence we didn't have from internal fixtures alone. The 6 systematic biases identified are real and well-evidenced. The distillation from 8 recommendations into 6 implementable fixes is correctly scoped.

Concerns exist with 3 of the 6 proposed fixes: one has an architectural mismatch, one is calibrated against the wrong use case, and one overstates its urgency.

---

## Per-Fix Assessment

### Fix 1: Duplicate-Finding Detection Rule (proposed P0)

**Problem: AGREE.** The Vanguard review double-counts "no statistical tests" — once as Analysis Finding #3 (Metrics, -10) and again as Communication Finding #6 (Actionability, -8). The root cause is identical: no statistical tests were run. The communication reviewer penalizes the *consequence* of an analytical absence, but the fix for the communication issue IS to fix the analysis issue. Cost: -18 instead of -10, inflating the score by ~4 points.

**Implementation: CHALLENGE.** The proposal adds a paragraph to SKILL.md Section 5 (Routing Table) telling subagents to suppress duplicates. This can't work because **subagents run in parallel** (ds-review-lead Step 7 dispatches both via separate Task calls). The communication-reviewer never sees the analysis-reviewer's findings when generating its own output. It cannot "reference the analysis finding" because it hasn't seen it.

**Redirect:** This must be a **synthesis-step rule in ds-review-lead.md Step 9**, not a SKILL.md routing table rule. The lead agent sees both outputs and can deduplicate during synthesis. Proposed wording: "When findings from both dimensions share the same root cause, apply the larger deduction only. Note the suppressed finding in the output as 'subsumed by [dimension] finding [#X].'"

**Verdict: Accept the problem. Redirect implementation from SKILL.md Section 5 to ds-review-lead.md Step 9.**

---

### Fix 2: Novel Framework / Methodology Credit (+5, proposed P1)

**SKEPTICAL — defer to v0.5.**

The evidence base is blog posts from industry-leading research teams (Airbnb LTV, Netflix proxy metrics, Meta asymmetric experiments, Airbnb FIV). The tool is designed for internal DS deliverables — churn analyses, A/B test reports, measurement reports. Internal analyses rarely introduce novel frameworks; they apply known methods to business problems.

Specific concerns:

1. **"Novel" is subjective and hard for an LLM to evaluate consistently.** Where's the line between "novel decomposition" and "applying a known method in a new context"? The counter-examples help but expect high variance across reviews.
2. **+5 is the second-highest credit.** If it fires inconsistently, it creates ±5 point cross-run variability — risking our ±10 consistency target for the wrong reason.
3. **Fires on 0 of 3 calibrated fixtures.** We can't validate it against our existing test suite. Adding unvalidatable changes to a calibrated system is architectural risk.

The "anti-research bias" identified in the blog analysis is real. But it doesn't affect our current use case or test fixtures. When blog post support is added (v0.5 genre awareness), this credit becomes essential.

**Verdict: Defer to v0.5. Not wrong, but not yet needed or validatable.**

---

### Fix 3: Worked Example Credit (+3, proposed P1)

**AGREE.**

The Rossmann R2 review proves this gap exists. The agent credits the revenue scenario table under "Effective data visualization" (+3) but it's not a visualization — it's a numerical worked example. The agent is already trying to credit this pattern but has to stretch an existing category.

Clear criteria ("walks through specific values, not just describe the approach generically"), modest credit (+3), fires on at least one existing fixture (Rossmann). Clean addition.

**Verdict: Accept.**

---

### Fix 4: Honest Negative / Null Result Credit (+3, proposed P1)

**AGREE.**

The Rossmann review calls out "linear models performed worse than the average model" as a positive finding — this IS reporting a null/negative result. The criteria is clear ("reports a result that didn't work without spinning it"), the credit is modest (+3), and it incentivizes intellectual honesty which is genuinely rare and valuable in DS analyses.

The web session's Udemy example is from a blog post, but the Rossmann fixture proves this fires on internal analyses too.

**Verdict: Accept.**

---

### Fix 5: Reduce MINOR Communication Deductions (proposed P0)

**PARTIALLY AGREE.**

**Formatting (-5 → -3): Justified.** -5 is 63% of a MAJOR (-8). The severity label says "polish issue" but the deduction value is in MAJOR territory. Reducing to -3 creates clearer separation between severity tiers (MINOR: -2 to -3 vs MAJOR: -8 to -10).

**Other two (-3 → -2): Marginal.** They save 2 raw deduction points combined, which after DR translates to ~0.5-1 point on the final score. Cross-run variability is ±10. This is within noise.

The proportionality analysis is structurally important: 134 possible communication deduction points vs ~101 for analysis. This asymmetry means communication is structurally easier to penalize. The DR curve partially addresses it, but the MINOR reductions are a small step in the right direction.

**Verdict: Accept -5 → -3 for formatting. Accept -3 → -2 for the other two but downgrade from P0 to P1 — trivial changes with trivial impact shouldn't share priority with active scoring errors.**

---

### Fix 6: Tighten "Reports Specific Quantitative Results" Credit (proposed P0)

**AGREE.**

The current criteria text ("Actual numbers reported, not vague claims") doesn't match how the agent actually applies the credit. The Vanguard review awards it because numbers come WITH comparisons. The Meta review correctly doesn't award it because "double digits" is vague. The proposed text aligns criteria with observed behavior.

Zero scoring impact on current fixtures. Prevents future inconsistency.

**Verdict: Accept. This is a documentation fix, not a scoring change.**

---

## What the Web Session Got Right

1. **The blog post calibration methodology.** Scoring 6 articles with gut-feel AND rubric, then analyzing the gap per article — this is exactly the right external validation approach. It surfaces biases that internal-only fixtures can't.

2. **The proportionality analysis.** Quantifying 134 vs 101 total deduction points across dimensions is a structural insight that explains why communication scores are consistently 30-40 points below analysis scores across all fixtures.

3. **The deferred items are correctly scoped.** Genre detection, audience-weighted averaging, and the methodology CRITICAL split are all correctly identified as future-version changes. The web session resisted scope creep.

4. **The self-deliberation flag (Rossmann lines 236-263).** The agent visibly debates itself about credit assignments in the output. This is a legitimate prompt engineering issue for the communication-reviewer agent — should be fixed with a "single-pass commit" instruction. Correctly identified as separate from SKILL.md.

---

## What the Web Session Missed or Got Wrong

1. **Fix 1 can't be enforced as proposed.** The routing table is read by subagents that run in parallel. Duplicate suppression must happen in the lead agent's synthesis step, which is the only place both outputs are visible.

2. **Predicted score impacts are overconfident.** "Vanguard increases 3-5 points" assumes deterministic agent behavior. Finding generation is non-deterministic — Rossmann scored 71 in both R1 and R2 but with completely different dimension breakdowns (Analysis 88→93, Communication 53→48). Predicting ±2 point precision is not realistic. Validation criteria should be "directionally correct and within ±5" not "exactly 72-74."

3. **Interaction with finding volume cap not analyzed.** Rossmann has 9 communication findings generating 76 raw deduction points. The existing P1 backlog item caps findings at 10. If we implement finding cap + MINOR reductions + duplicate suppression simultaneously, these changes interact in ways that aren't modeled. Fewer findings = fewer deductions = MINOR reductions matter even less.

4. **The "anti-research bias" evidence doesn't apply to current fixtures.** The web session's strongest argument (Netflix proxy metrics deserving 90 but getting 76) is about blog posts. Our three test fixtures are internal-style analyses. Fix 2 is the most affected — it fires on 0 of 3 current fixtures. Changes calibrated against a use case we don't yet serve carry higher validation risk.

---

## Summary

| Fix | Web Session Priority | IC9 Assessment | Verdict |
|---|---|---|---|
| 1. Duplicate detection | P0 | Problem real, implementation wrong | **Accept problem, redirect to lead agent Step 9** |
| 2. Novel framework credit | P1 | Evidence from wrong use case | **Defer to v0.5** |
| 3. Worked example credit | P1 | Clean addition, validated by fixture | **Accept** |
| 4. Honest negative result | P1 | Clean addition, validated by fixture | **Accept** |
| 5a. Formatting -5→-3 | P0 | Justified — MINOR/MAJOR gap too narrow | **Accept** |
| 5b. Headings -3→-2, chart -3→-2 | P0 | Marginal — within cross-run noise | **Downgrade to P1** |
| 6. Tighten quant results text | P0 | Documentation fix, zero score impact | **Accept** |

**Additional task (not in proposal):** Fix self-deliberation in communication-reviewer prompt. Add single-pass commit instruction.

**Net: 5 of 6 fixes accepted (1 redirected). 1 deferred to v0.5. 1 downgraded from P0 to P1.**
