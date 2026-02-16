# DS Lead Review: SKILL.md Immediate Fixes Proposal

**Date:** 2026-02-15
**Reviewer Role:** Senior DS Lead (highest-level technical leadership)
**Reviewing:** `dev/specs/proposal_skillmd_immediate_fixes.md` (6 proposed SKILL.md edits)
**Supporting Evidence Reviewed:** `dev/reviews/2026-02-15-independent-rubric-evaluation.md`, `dev/test-results/ds_blog_rubric_analysis.md`, `dev/decisions/ADR-003-calibration-approach.md`, `plugin/skills/ds-review-framework/SKILL.md`, all 3 R2 review outputs

---

## Overall Assessment

The independent reviewer did strong diagnostic work. The blog post calibration analysis is genuinely impressive — methodical, well-evidenced, and honest about what it found. But the proposed fix set is trying to solve the wrong problem at the wrong time, and several fixes are weaker than they appear.

The R2 calibration (ADR-003) successfully moved scores from 16-29 to 54-71. The system is in a defensible range. The remaining question is not "are the scores exactly right?" but "does the system work robustly across diverse inputs?" — and 6 incremental rubric edits won't answer that. Extended validation will.

---

## Fix-by-Fix Review

### Fix 1: Duplicate-Finding Detection Rule — ACCEPT (P0)

**The problem is real.** The Vanguard review double-counts "no statistical tests" as both a Metrics finding (-10) and an Actionability finding (-8). That's -18 for one root cause.

**Challenge on the mechanism:** The routing table already has anti-duplication language. Line 192 of SKILL.md says:

> *"Never report the same issue from both subagents."*

That rule exists. It's being ignored. Why? Because the agent treats "A/B test results without statistical testing" (analysis-owned) and "A/B test results not interpretable without confidence intervals" (communication-owned) as *different findings*. They're close but not identical — one is about whether the analysis is valid, the other is about whether the reader can act on it.

Adding another paragraph of prose instruction to a section that already has prose the agent ignores may not change behavior. The real fix might need to be in the agent prompt, not just the rubric.

**Verdict:** Accept, but track whether the agent actually follows it during validation. If it still double-counts, escalate to a prompt-level fix.

**Expected impact:** +3 to +4 on Vanguard-style reviews. This is the only fix that addresses a real scoring error.

---

### Fix 2: Novel Framework/Methodology Credit (+5) — DEFER TO v1.5

**This is scope creep from the blog post calibration exercise.**

The entire evidence base comes from published blog posts — Airbnb LTV, Netflix proxy metrics, Meta asymmetric experiments. These are elite DS publications from companies with dedicated technical writing teams. They are *not* the tool's primary use case.

The tool is built for **internal DS deliverables**: churn analyses, A/B test reports, measurement frameworks shared on Confluence. How often does an internal analysis introduce a "novel analytical framework or methodology"? Almost never. 95% of internal DS work is applying known methods to new data. This credit would fire maybe once every 20 reviews.

The proposal says the credit "addresses the structural root of Bias 1 (Anti-Research Bias)." But Bias 1 was identified *on blog posts*, not on internal analyses. For internal work, there IS no anti-research bias — the rubric correctly values methodological rigor (experimental design +8, pre-specified hypotheses +5) over intellectual novelty.

**Risk if added now:** The criteria ("goes beyond applying an existing method to new data") require judgment that could be inconsistent. An agent might award +5 every time someone uses XGBoost instead of linear regression and calls it "novel." Tight criteria need testing, and testing on 3 internal-style fixtures won't validate this credit.

**Verdict:** Defer to v1.5 when/if genre detection is added. For v1.0, this adds complexity without improving the primary use case.

---

### Fix 3: Worked Example Credit (+3) — ACCEPT (P1)

**This fills a real gap.** The Rossmann review stretches "data visualization" (+3) to credit a revenue scenario table — that's a genuine taxonomy problem. The best/worst revenue scenario is a worked example, not a visualization.

Worked examples are valuable in both internal and external content. When a DS explains a causal inference framework to a PM, a concrete "if Store A has X bookings..." walkthrough is the difference between understanding and glazing over. The credit table should have a home for this.

The criteria are tight enough: "Must walk through specific values, not just describe the approach generically." This won't over-fire.

**Verdict:** Accept. Genuinely useful for the primary use case.

---

### Fix 4: Honest Negative/Null Result Credit (+3) — ACCEPT (P1)

**Philosophically aligned.** Null results are one of the most valuable and underreported things in DS. Creating a positive incentive is the right move.

**Practical firing rate challenge:** On the current three test fixtures:
- Rossmann: *maybe* for the linear model underperforming the average model. Borderline.
- Vanguard: No — doesn't report any failures.
- Meta: No — everything is spun as positive.

This credit will fire rarely enough that it won't materially change calibration. It's a principled addition, not a calibration fix.

**Verdict:** Accept because it creates the right incentive. Don't count it as a calibration improvement.

---

### Fix 5: Reduce MINOR Communication Deductions — ACCEPT (P1), but challenge the impact

**The diagnosis is correct.** Communication has 134 possible deduction points vs ~101 for analysis. The dimension is structurally over-punitive. The independent reviewer identified this clearly.

**The proposed fix is too weak to matter.** The math:

| Change | Savings |
|---|---|
| Generic headings: -3 → -2 | 1 point |
| Unnecessary chart: -3 → -2 | 1 point |
| Sloppy formatting: -5 → -3 | 2 points |
| **Maximum total savings** | **4 raw points** |

After DR compression: **+1 to +2 on the final score.**

The Rossmann communication score is 48. This fix moves it to 49 or 50. The 45-point gap between analysis (93) and communication (48) shrinks to a 43-point gap. That's noise, not signal.

**The real problem** is that 8 of 11 communication deductions are MAJOR (-8 to -10), and 5-8 of them fire on every review. The fix should either:
- Cap the number of communication findings (already deferred in backlog as "cap at 10")
- Reduce some MAJORs to a lower value
- Apply dimension-specific DR (steeper compression for communication)

**Verdict:** Accept because the numbers are directionally correct (MINORs at -5 are too close to MAJORs at -8). But don't pretend this solves the communication over-punitiveness problem. It's cosmetic.

---

### Fix 6: Tighten "Reports Specific Quantitative Results" Credit — ACCEPT (P1)

**The current agent is already applying this correctly.** Vanguard gets +3 (numbers with context). Meta gets +0 (vague "double digits"). The agent's behavior matches the proposed tighter criteria.

This fix makes the criteria text match what the agent is already doing. Valuable for consistency across future reviews and agents, but it won't change any scores on the current test fixtures.

**Verdict:** Accept. Cheap, defensive, correct. Documentation fix, not a calibration fix.

---

## What's Missing from the Proposal

### Missing P0: Self-Deliberation Suppression in Agent Output

The Rossmann review (lines 236-264) shows the communication-reviewer arguing with itself about credit assignments, changing its mind three times, and leaving its internal deliberation visible in the output:

> "Professional polish throughout → +3 half credit → +2 rounded down to +1 — wait..."
> "Hmm, I keep going back and forth. Let me commit..."
> "Actually, I think I should give..."

This is not a SKILL.md fix — it's a prompt engineering fix in the communication-reviewer agent. But it's **more important for user trust than any of the 6 proposed fixes.** A user seeing an agent debate itself in the output will not trust any score it produces.

**This should be P0.** Add a single-pass commit rule to the communication-reviewer prompt.

### Missing P0: Extended Validation Before More Rubric Changes

The backlog has three untested fixtures (Airbnb Message Intent, Airbnb FIV, Netflix Proxy Metrics). Running these will tell you far more about the system's robustness than tweaking MINOR deductions by 1 point.

If the system produces reasonable scores on diverse inputs *without further changes*, that's a much stronger signal than getting 6 edits to match 3 fixtures you've already been tuning against.

**Risk of skipping this:** You're overfitting the rubric to 3 test fixtures. Every edit makes the rubric better at scoring Vanguard, Meta, and Rossmann — but you have no idea if it generalizes.

---

## The Blog Post Calibration Problem

The 6-article blog post analysis identified real biases: anti-research, genre mismatch, concrete numbers penalty. But several of these biases are **features, not bugs** when the tool evaluates internal deliverables:

- **Anti-research bias:** The tool *should* penalize internal analyses that lack baselines, statistical tests, and actionable recommendations. That's the whole point.
- **Concrete numbers penalty:** Internal analyses *should* report specific numbers with context. Penalizing vagueness is correct behavior.
- **Genre mismatch:** The tool is designed for internal deliverables. Blog posts are out of scope for v1.0.

The blog post findings become actionable bugs when genre detection is added (v0.5 in the backlog). Until then, they're calibration context, not calibration targets. Don't let strong research on the wrong use case drive changes to the right use case.

---

## Recommended Priority Order

| Priority | Action | Type | Rationale |
|---|---|---|---|
| **P0** | Fix 1: Duplicate detection rule | SKILL.md edit | Only fix addressing a real scoring error |
| **P0** | Self-deliberation suppression | Agent prompt edit | Production readiness, user trust |
| **P0** | Extended validation (3 fixtures) | Testing | Prevents overfitting to current 3 fixtures |
| **P1** | Fix 3: Worked example credit | SKILL.md edit | Real taxonomy gap, useful for primary use case |
| **P1** | Fix 4: Null result credit | SKILL.md edit | Right incentive, low immediate impact |
| **P1** | Fix 5: Reduce MINORs | SKILL.md edit | Directionally correct, cosmetic impact (+1-2 pts) |
| **P1** | Fix 6: Tighten quant credit | SKILL.md edit | Documentation fix, agent already applies correctly |
| **Defer** | Fix 2: Novel framework credit | v1.5 | Scope creep from blog post analysis, doesn't serve primary use case |

---

## Bottom Line

Fix 1 and the self-deliberation fix are the only things that materially improve the system right now. Everything else is polish that's fine to include but shouldn't be confused with calibration progress.

Extended validation should happen *before* another round of rubric edits, not after — otherwise you're overfitting to three fixtures.
