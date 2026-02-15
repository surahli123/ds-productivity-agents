# PM Lead Review: Web Session Rubric Proposal

**Date:** 2026-02-15
**Reviewer:** PM Lead
**Reviewing:** Web session's independent rubric evaluation, 6 proposed SKILL.md fixes, and IC9 architect review
**Input files:** `proposal_skillmd_immediate_fixes.md`, `independent_rubric_evaluation.md`, `ds_blog_rubric_analysis.md`, `ic9-architect-review-of-web-session.md`, R2 calibration notes, R2 review outputs (Vanguard, Rossmann, Meta)
**Status:** Review complete

---

## Overall Assessment

The web session produced genuinely useful work. The blog post calibration methodology — scoring external content with gut-feel, then with the rubric, then analyzing the gap — is the kind of external validation that builds confidence in a scoring system. The 6 systematic biases identified are real and well-evidenced. The distillation into 6 implementable fixes is well-scoped.

However, I have a fundamental concern about **who we are building for and what problem we are solving right now.** The evidence base for these fixes is split between two populations: (1) our actual users — DS teams reviewing internal analyses before sharing with stakeholders, and (2) a population we do not yet serve — external blog posts from industry-leading research teams. Three of the six fixes are primarily motivated by the blog post population. That does not make them wrong, but it changes the urgency calculus significantly.

The IC9 review caught the most important technical issue (Fix 1 cannot work as proposed due to parallel subagent execution). I agree with that assessment and will not re-litigate it. My review focuses on user impact, prioritization, and product risk.

---

## The Trust Question

Before diving into per-fix assessment, one framing point that shapes my entire review.

The number one product risk for a review tool aimed at DS practitioners is **perceived unfairness.** Data scientists are critical thinkers by training. If the tool over-penalizes good work or misses obvious strengths, users will not just disagree with the score — they will stop using the tool. Trust is binary: either the tool feels like a thoughtful peer reviewer, or it feels like a blunt rubric being mechanically applied. There is no middle ground.

R2 calibration got us from "obviously broken" (scores of 16-29) to "defensible" (scores of 54-71). That is real progress. The question for these fixes is: **do they move us from "defensible" to "trusted"?**

The fixes that improve trust the most are the ones that fix cases where the tool is visibly wrong in a way a DS practitioner would immediately notice. Specifically:

- **Penalizing the same problem twice** (Fix 1) is the kind of error that makes a user say "this tool doesn't understand my work." High trust impact.
- **Crediting good practices the tool currently ignores** (Fixes 3, 4) makes the tool feel like it "gets it." Moderate trust impact.
- **Over-penalizing polish issues** (Fix 5) feels petty if the analytical work is strong. Moderate trust impact.
- **Tightening criteria text** (Fix 6) prevents future inconsistency but has zero impact on current user experience.
- **Rewarding novel frameworks** (Fix 2) matters for a population we don't yet serve.

This ordering shapes my prioritization.

---

## Per-Fix Assessment

### Fix 1: Duplicate-Finding Detection Rule

**User impact: HIGH. This is the single most impactful fix.**

The Vanguard review penalizes "no statistical tests" twice — once in Analysis (-10) and again in Communication (-8). A DS practitioner reading this review would immediately notice: "You're hitting me for the same thing twice." That reaction destroys trust faster than any individual scoring error.

The evidence is concrete and visible in a current fixture, not inferred from blog post analysis. The Vanguard double-count costs ~4 points on the final score. More importantly, it makes the review feel unfair in a way that is obvious to the reader.

**IC9 redirect is correct:** This must live in the lead agent's synthesis step (Step 9), not the SKILL.md routing table, because subagents run in parallel and cannot see each other's findings. The implementation location changes; the user-facing outcome is the same.

**One product concern the architect did not flag:** The duplicate suppression rule needs clear guidance for ambiguous cases. "Same root cause" is straightforward for "no statistical tests" — but what about cases where two findings share a *partial* root cause? Example: "no limitations section" could fire in both Audience Fit (downstream consumers misled) and Actionability (over-interpretation boundary unclear). These are related but not identical — one is about what is missing, the other is about what the reader might incorrectly infer. The synthesis step needs a decision rule for partial overlaps, not just exact duplicates. Suggest: "If two findings from different dimensions share more than 50% of their remediation (i.e., the same fix would address both), suppress the smaller deduction."

**Verdict: Ship. P0. Redirect to lead agent Step 9 as IC9 recommended. Add partial-overlap guidance.**

---

### Fix 2: Novel Framework / Methodology Credit (+5)

**User impact: LOW for current users. MEDIUM for future users.**

The IC9 review correctly identified that this fix is calibrated against the wrong population. The evidence is blog posts from Airbnb, Netflix, and Meta research teams. Our users are internal DS teams reviewing churn analyses, A/B test reports, and measurement studies. Internal analyses rarely introduce novel frameworks — they apply known methods to business problems.

I agree with the IC9 deferral, but I want to add a product reason beyond "we can't validate it on current fixtures."

The deeper problem with this credit is **subjectivity.** Where is the line between "novel decomposition" and "applying a known method creatively"? A DS practitioner who builds a new metric framework for their team genuinely believes they have created something novel. A reviewer might disagree. At +5 (the second-highest credit), inconsistent application creates visible unfairness — exactly the trust problem we are trying to avoid. Fixing this requires tighter criteria than the proposal provides, and the right time to develop those criteria is when we have test fixtures that actually exercise this credit.

**One exception worth noting:** If we ship extended validation fixtures (per the R2 calibration notes, "run 2-3 untested real-world fixtures"), and one of those fixtures contains a genuinely novel framework, this credit becomes immediately validatable and should be reconsidered. Tag it accordingly.

**Verdict: Defer to v0.5. Not wrong, not yet needed, and subjectivity risk is too high at +5 without validation fixtures.**

---

### Fix 3: Worked Example Credit (+3)

**User impact: MODERATE. This directly serves internal DS teams.**

This is the cleanest fix in the proposal. The evidence comes from an existing fixture (Rossmann), not just blog posts. The agent is already trying to credit this pattern — it awards "Effective data visualization" (+3) for the Rossmann revenue scenario table, which is not a visualization but a numerical worked example. The agent is stretching the wrong category because the right category does not exist.

For internal DS teams, worked examples are high-value communication tools. "If Store A has 1,000 daily visitors and our model predicts 15% uplift, that translates to 150 additional visits worth approximately $X" is exactly the kind of bridge between methodology and business impact that makes an analysis land with stakeholders. Rewarding this encourages the right behavior.

The criteria are clear ("walks through specific values, not just describe the approach generically"), the credit is modest (+3), and it fires on at least one existing fixture. Low risk, moderate reward.

**Verdict: Ship. P1 is the right priority — it adds capability rather than fixing an active error.**

---

### Fix 4: Honest Negative / Null Result Credit (+3)

**User impact: MODERATE. Incentivizes a behavior that is genuinely rare and valuable.**

This is the fix I find most compelling from a product standpoint. Reporting what did not work is one of the highest-value, lowest-frequency behaviors in data science. Most analyses only show what worked. When a DS practitioner reports "we tested approach X and it failed," that saves their teammates from repeating the same experiment. The fact that our tool has no mechanism to recognize this means we are implicitly discouraging intellectual honesty through omission.

The Rossmann fixture provides direct evidence: the reviewer notes "linear models performed worse than the average model" as a positive finding, but has no credit category for it. The criteria are clear and falsifiable ("reports a result that didn't work without spinning it"), the credit is modest (+3), and it fires on an existing fixture.

**One product consideration:** This credit is especially important for our primary use case — internal DS teams reviewing their own analyses before sharing with stakeholders. In an internal context, reporting null results is politically risky. A DS who says "my experiment showed no effect" risks having stakeholders question why they spent time on it. Our tool giving explicit credit for this honesty is a positive signal that reinforces good practice. This is not just scoring accuracy — it is product positioning. We are telling users "we value intellectual integrity" by rewarding it.

**Verdict: Ship. P1 is right, but I would rank this above Fix 3 within P1 because of the behavioral incentive it creates.**

---

### Fix 5: Reduce MINOR Communication Deductions

**User impact: LOW-to-MODERATE depending on the specific change.**

The IC9 split is correct. Let me evaluate each sub-change from a user perspective.

**5a. Formatting -5 to -3: Ship.**
A DS practitioner who writes an analytically rigorous analysis but has some typos and inconsistent formatting should not see 63% of a MAJOR deduction for polish issues. This feels disproportionate and petty. The user reaction is "I know my formatting isn't perfect, but that's not the point of my analysis." Reducing to -3 creates clearer separation between "polish issue" and "structural problem." This matters for trust.

**5b. Headings -3 to -2 and unnecessary chart -3 to -2: Defer or batch.**
The IC9 review is right that these save ~0.5-1 final-score point after diminishing returns compression. That is within cross-run noise. I do not object to shipping these — they are one-character edits — but they should not be called P0 and they should not be part of the validation criteria. If we ship them alongside other changes, they will be invisible in the noise. If we ship them alone, there is nothing to validate. The risk is not that they are wrong; the risk is that tracking trivial changes clutters the calibration story.

**Verdict: Ship 5a (formatting -5 to -3). Accept 5b but downgrade to "ship when convenient" — do not validate separately.**

---

### Fix 6: Tighten "Reports Specific Quantitative Results" Credit

**User impact: LOW now. MEDIUM for long-term consistency.**

This is a documentation fix. The current criteria text ("Actual numbers reported, not vague claims") does not match the standard the agent actually applies. The Vanguard review awards this credit because numbers come with comparisons. The Meta review does not award it because "double digits" is vague. The proposed text aligns the written criteria with observed behavior.

Zero scoring impact on current fixtures. No user will see a different score because of this change. But it prevents a future inconsistency where a bare number like "accuracy was 70%" earns +3 without any context. For a DS practitioner, a number without a baseline or comparison is not a "specific quantitative result" — it is trivia. Tightening the criteria protects against that drift.

**Verdict: Ship. P1 is right — this is preventive maintenance, not an active fix.**

---

## What I Would Ship vs. Defer

### Ship Now (v0.4 patch)

| Priority | Fix | Rationale |
|---|---|---|
| P0 | Fix 1: Duplicate detection (in lead agent Step 9) | Visible unfairness in current output. Trust-destroying. |
| P0 | Fix 5a: Formatting -5 to -3 | Disproportionate penalty visible in current output. |
| P1 | Fix 4: Honest negative result credit (+3) | Validated by fixture. Incentivizes the right behavior. |
| P1 | Fix 3: Worked example credit (+3) | Validated by fixture. Agent is already stretching to credit this. |
| P1 | Fix 6: Tighten quantitative results criteria text | Documentation alignment. Zero scoring risk. |
| P1 | Fix 5b: Headings -3 to -2, chart -3 to -2 | Trivial change, trivial impact. Ship when convenient. |

### Defer to v0.5

| Fix | Rationale |
|---|---|
| Fix 2: Novel framework credit (+5) | Wrong population, unvalidatable, subjectivity risk at +5. Revisit when genre-aware mode exists or when extended fixtures exercise it. |

---

## Validation Approach: Product Perspective

The proposal's validation criteria are directionally right but the precision is wrong. The IC9 review flagged this too — predicting "Vanguard increases 3-5 points" implies deterministic agent behavior that does not exist. Rossmann scored 71 in both R1 and R2 but with completely different dimension breakdowns (Analysis 88 to 93, Communication 53 to 48). The agent is non-deterministic at the finding level.

**Realistic validation criteria:**

1. **Vanguard:** Score should be 69 or higher (not lower than R2 baseline). If duplicate suppression fires, expect directional increase of 2-5 points. Acceptable range: 69-76.
2. **Meta:** Score should remain in the 50-58 range. None of these fixes should benefit a weak analysis. If Meta goes up materially, something is miscalibrated.
3. **Rossmann:** Score should be 71 or higher. Worked example credit and MINOR reduction should provide a small lift. Acceptable range: 71-77.
4. **Rank ordering preserved:** Rossmann >= Vanguard > Meta. If this inverts, stop and investigate.
5. **Differentiation gap preserved:** Rossmann/Vanguard to Meta gap should remain >= 13 points.

**One additional validation I would add that nobody has proposed:**

Run the **same** fixture (pick Vanguard) three times post-fix and check that scores are within +/-8 of each other. The R2 calibration notes list "cross-run consistency: verify scores within +/-10" as remaining validation. These fixes change the scoring surface, so consistency should be re-verified. If the fixes introduce new variance (especially duplicate suppression, which depends on finding generation that varies across runs), we need to know before declaring them stable.

---

## Product Risks the Architect Missed

### 1. Interaction Effects Are Unmodeled

The IC9 review mentions this briefly ("if we implement finding cap + MINOR reductions + duplicate suppression simultaneously, these changes interact") but does not prescribe a mitigation. From a product standpoint, shipping multiple scoring changes simultaneously makes it impossible to attribute score movements to specific fixes. If Vanguard goes from 69 to 75 post-fix, was that duplicate suppression (+4), MINOR reduction (+1), or something else?

**Mitigation:** Ship Fix 1 (duplicate detection) first, re-run fixtures, observe the isolated impact. Then ship Fixes 3-6 together (they are all credit/criteria changes that interact minimally with each other). This adds one extra validation run but gives us clean attribution.

Alternatively, if speed matters more than attribution: ship all at once, accept that we cannot decompose the score change, and validate only the aggregate criteria above. This is acceptable if we trust the directional logic. I lean toward this option given that R2 was just accepted and these are refinements, not emergency fixes.

### 2. The Communication Dimension Asymmetry Is Not Resolved

The web session's most important structural finding is that the communication dimension has 134 possible deduction points vs. ~101 for analysis. This means communication is structurally easier to penalize. The MINOR reductions (Fix 5) shave 4 points off the theoretical max, bringing it to ~130 vs. ~101. This does not close the gap.

The practical consequence is visible in every R2 output: Vanguard (Analysis 86, Communication 52), Rossmann (Analysis 93, Communication 48), Meta (Analysis 57, Communication 50). Communication scores are consistently 30-40 points below analysis scores. The 50/50 averaging means a document that is analytically excellent but communicatively mediocre (Rossmann) scores 71, while a DS practitioner's intuition would put it higher.

None of the proposed fixes address this. The web session proposed audience-weighted dimension averaging (deferred to v1.5 in the evaluation, not included in the 6 fixes). The IC9 review did not comment on it. I flag this as the most important **unaddressed** product issue. It will become visible to users in every review where the analysis-communication gap exceeds 25 points.

I am not proposing a fix now — this is a v0.5 design question. But it should be tracked explicitly. If users consistently react with "why is my communication score so much lower than my analysis score?" we have a product problem, not a calibration problem.

### 3. The Self-Deliberation Issue Is a Polish Problem With Trust Implications

The IC9 review flagged the Rossmann review's visible self-deliberation (lines 236-263 in the output) and correctly identified it as a prompt engineering fix for the communication-reviewer agent, not a SKILL.md change. I agree but want to add urgency.

A DS practitioner reading a review that says "Hmm, I keep going back and forth. Let me commit..." will lose confidence in the tool immediately. This is a credibility issue with the same trust impact as the duplicate-finding problem. It should be P1 alongside the credit additions, not deferred or backgrounded.

The fix is small — add a "single-pass commit" instruction to the communication-reviewer prompt — and it costs nothing in terms of scoring calibration. It is pure output quality.

### 4. The Backlog Finding Volume Cap Interacts With These Fixes

The R2 calibration notes mention an existing P1 backlog item to cap findings at 10. If that cap ships alongside these fixes, the interaction is significant: fewer findings means fewer deductions, which means the MINOR reductions (Fix 5) matter even less, and the duplicate suppression (Fix 1) becomes less necessary if the cap naturally prevents some findings from firing.

This does not change the verdict on any fix — duplicate suppression and MINOR reductions are correct on their own merits — but the **validation criteria should account for whether the finding cap ships in the same release.** If it does, expected score increases will be larger than predicted. Build this into the acceptance ranges.

---

## Summary Table

| Fix | Web Proposal | IC9 Verdict | PM Verdict | Rationale |
|---|---|---|---|---|
| 1. Duplicate detection | P0, SKILL.md | Accept problem, redirect to Step 9 | **Ship P0, add partial-overlap guidance** | Highest trust impact. Visible unfairness. |
| 2. Novel framework credit | P1, +5 | Defer to v0.5 | **Defer to v0.5** | Wrong population, unvalidatable, subjectivity risk. |
| 3. Worked example credit | P1, +3 | Accept | **Ship P1** | Clean addition. Agent already stretching to credit this. |
| 4. Honest negative result | P1, +3 | Accept | **Ship P1 (rank above Fix 3)** | Behavioral incentive aligns with product positioning. |
| 5a. Formatting -5 to -3 | P0 | Accept | **Ship P0** | Disproportionate penalty. Trust issue. |
| 5b. Headings/chart -3 to -2 | P0 | Downgrade to P1 | **Ship when convenient** | Trivial impact. Do not validate separately. |
| 6. Tighten quant results text | P0 | Accept | **Ship P1** | Documentation fix. Prevents future drift. |

**Additional tasks identified:**
- Self-deliberation fix in communication-reviewer prompt (P1, trust issue)
- Communication dimension asymmetry analysis for v0.5 scoping (track, do not fix now)
- Cross-run consistency check post-fix (add to validation plan)

---

## Final Note

These are good refinements to a system that has come a long way from R0. The R2 calibration was the hard part — moving from 16-29 to 54-71 required structural changes (strength credits, diminishing returns, severity escalation guard). These fixes are about moving from "defensible" to "feels right," which is the product work that converts a technically correct tool into one that DS practitioners actually trust and use repeatedly. That transition matters more than any individual point adjustment.
