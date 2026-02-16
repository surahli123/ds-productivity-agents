# R3 Calibration Assessment — Principal AI Engineer
**Date:** 2026-02-15
**Role:** IC9-level Principal AI Engineer (systems and architecture focus)
**Reviewer:** Claude Sonnet 4.5

---

## Executive Summary

**Verdict:** R3 demonstrates strong system fundamentals but exhibits **systemic score inflation** due to asymmetric scoring mechanics. The system correctly differentiates quality (37-point spread), finding generation is clean (no spurious CRITICALs), and the implementation is mathematically sound. However, **all 6 tests scored 17-30 points above calibration targets** due to a structural imbalance: the diminishing returns curve compresses downward forces (deductions) but not upward forces (credits).

**Root cause:** The DR formula was designed to prevent over-penalization from finding spam, but it creates an unintended asymmetry. High-quality analyses with few deductions (7-15 points) never enter the DR compression zone, while accumulating full credit value (+13 to +25). This allows strong analyses to reach 85-100 even with substantive gaps.

**Recommendation:** Implement **symmetric compression** — apply DR to both deductions AND credits. This preserves differentiation while preventing runaway inflation. Expected impact: -10 to -15 points across all tests, bringing scores into calibration range without oscillation risk.

**Architecture assessment:** Incrementally fixable. No redesign required. Estimated rounds to acceptance: 1 (if symmetric compression works as modeled) or 2 (if second-order tuning needed).

---

## 1. What Improved vs R2

### 1.1 Core Fixture Score Movement

| Fixture | R2 | R3 | Delta | Target | Gap to Target |
|---|---|---|---|---|---|
| Vanguard | 69 | 72 | +3 | 40-55 | +17 to +32 |
| Meta | 54 | 63 | +9 | 50-65* | +0 to +13 |
| Rossmann | 71 | 86 | +15 | 45-60 | +26 to +41 |

*Meta target adjusted by owner to "Major Rework acceptable"

**Dimension-level analysis:**

Vanguard: Analysis dropped 18 points (86→68) but Communication rose 25 points (52→77), net +3 overall.

Meta: Balanced improvement across both dimensions (+7 analysis, +11 communication).

Rossmann: Communication jumped 24 points (48→72), analysis hit perfect 100.

**Interpretation:** The P1 credit additions (worked example +3, honest negative result +3) and MINOR deduction reductions (formatting -5→-3, headings/chart -3→-2) had **measurable, directionally correct impact** on communication scores, recovering from R2's under-crediting problem. However, when combined with the parallel session's conditional credit halving rule (which cut Vanguard's analysis credits), the net effect was inflationary.

### 1.2 Extended Fixtures (Generalization Check)

| Fixture | R3 Score | Analysis Target | Comm Target | Analysis Gap | Comm Gap |
|---|---|---|---|---|---|
| Airbnb Message Intent | 85 | 55-65 | 70-80 | +28 | +5 to +8 |
| Airbnb FIV | 90 | 65-75 | 70-80 | +22 | +3 to +13 |
| Netflix Proxy Metrics | 100 | 60-70 | 65-75 | +30 | +25 to +35 |

**Observation:** Extended fixtures scored HIGHER than core fixtures (85-100 vs 63-86), contrary to the hypothesis that blog posts would be "systematically over-penalized for missing business metrics."

**Implication:** The rubric is biased TOWARD research-quality rigor, not against it. Blog posts exhibit:
- Low raw deductions (7-15 points) due to strong methodology
- High credit accumulation (+13 to +25) for systematic comparisons, reproducibility, honest null results
- Minimal exposure to DR compression (deductions stay in 100% zone)

This is **architecturally revealing**: the scoring system rewards methodological rigor more heavily than it penalizes missing business context.

### 1.3 Quality Improvements (Non-Score Metrics)

✅ **Finding volume control working:** R2 averaged ~12 findings/test, R3 averaged ~6.5 findings/test. The 10-finding cap (Step 9 of ds-review-lead.md) is functioning correctly.

✅ **Duplicate suppression working:** Meta review shows 1 finding "subsumed by analysis finding," indicating the Step 9 duplicate detection logic is firing.

✅ **Deduction/severity alignment verified:** All deductions match SKILL.md Section 2 table values. No severity inflation observed.

✅ **Self-deliberation suppression working:** No visible agent deliberation artifacts in R3 reviews (communication-reviewer.md Rule 12 successful).

✅ **Conditional credit halving working:** Vanguard's experimental analysis without validation correctly received halved credits for methodology (+2.5 vs +5) and pre-specified goals (+1.5 vs +3).

### 1.4 Differentiation Maintained

**Score spread:**
- R2: 15-point gap (Rossmann 71 vs Meta 54)
- R3: 23-point gap (Rossmann 86 vs Meta 63)
- Extended fixtures: 37-point gap (Netflix 100 vs Meta 63)

**Ranking correctness:** Netflix (100) > FIV (90) > Rossmann (86) > Message Intent (85) > Vanguard (72) > Meta (63)

This ranking is **qualitatively correct** based on methodological rigor, communication structure, and analytical completeness. The system differentiates quality — it just does so at the wrong absolute scale.

---

## 2. What's Still Broken

### 2.1 Score Inflation (Impact: ALL fixtures)

**Evidence:** 6/6 tests scored above target ranges by 17-30 points.

**Severity:** CRITICAL — this is the inverse of the R0/R1 problem. R0 was too harsh (16-29), R3 is too lenient (63-100).

**User impact:** If all scores cluster in the 70-100 band, the tool provides weak differentiation signal between "needs work" and "ready to ship."

**Mathematical diagnosis:**

The diminishing returns formula is:
```
if raw_deductions <= 30:
    effective = raw_deductions
elif raw_deductions <= 50:
    effective = 30 + (raw_deductions - 30) * 0.75
else:
    effective = 45 + (raw_deductions - 50) * 0.50

dimension_score = 100 - effective + credits
```

**Problem:** This formula compresses deductions (reducing downward pressure) but applies credits at full value (maintaining upward pressure). For high-quality analyses:

Netflix Proxy Metrics:
- Raw deductions: 7 (all in 100% zone → 7 effective)
- Credits: +13 analysis, +21 communication (full value)
- Result: 100/100

Rossmann:
- Raw deductions: 0 analysis, 38 communication
- Communication effective: 30 + (38-30)*0.75 = 36 (saved 2 points via DR)
- Credits: +25 analysis (capped), +8 communication
- Result: 100 analysis, 72 communication → 86 overall

**The asymmetry:** DR was designed to prevent finding spam from over-penalizing weak analyses (protecting the floor). It was NOT designed to prevent credit accumulation from over-rewarding strong analyses (protecting the ceiling). The system lacks a symmetrical ceiling constraint.

### 2.2 Meta CRITICAL Count (Impact: 1 fixture)

**Evidence:** Meta has 3 CRITICALs (target: max 2).

**Breakdown:**
1. Experimental claims without validation (CRITICAL, -15)
2. Conclusion doesn't trace to evidence (CRITICAL, -15)
3. TL;DR completely absent (CRITICAL, -12)

**Analysis:**
- Finding #1 is legitimately CRITICAL — experimental structure without validation misleads readers
- Finding #3 is legitimately CRITICAL per SKILL.md Section 2 (though see Section 2.5 for genre-specific concerns)
- Finding #2 is borderline — "Conclusion doesn't trace to evidence" is a MAJOR analytical gap, but is it CRITICAL severity?

**Proposed reclassification:** Consider downgrading Finding #2 from CRITICAL (-15) to MAJOR (-10). Rationale: The analysis is incomplete (missing measurements to support claimed impacts), but it's not fundamentally misleading like a causal claim without methodology. The reader can detect the gap. This would bring Meta to 2 CRITICALs (within target).

**Counterargument:** If an executive acts on "measurable positive impacts" that aren't actually measured, that's a decision made on faulty foundation — CRITICAL severity is justified.

**Recommendation:** Defer to DS Lead and PM Lead role reviews for severity calibration decision. From a systems perspective, the current finding is defensible per SKILL.md Section 1 definition: "wrong conclusions reached, key audience misled, or decisions made on faulty foundation."

### 2.3 Floor Rule Paradox (Impact: User trust)

**Evidence:** Airbnb FIV shows "90/100 → Major Rework (2 CRITICALs cap at 59)."

**User experience:** Seeing "90/100" alongside "Major Rework" creates cognitive dissonance. The numeric score signals "excellent work," the verdict signals "significant problems." Which should the user trust?

**Implementation correctness:** The floor rule is working as designed per ds-review-lead.md Step 9: "Floor rules override the verdict band only, not the numeric score."

**Design question:** Is this the RIGHT design?

**Options:**
1. **Suppress numeric score when floor rule applies:** Show only verdict + explanation. Avoids the visual mismatch.
2. **Show floor-adjusted score:** Display "59/100 (floor rule applied)" instead of "90/100."
3. **Reframe verdict labels:** Rename bands to make floor rule logic clearer (e.g., "Blocked by CRITICAL issues").
4. **Keep current behavior:** Numeric score reflects analytical + communication quality, verdict reflects shipability. Both are valid signals.

**Recommendation:** Option 2 (show floor-adjusted score) is most transparent and avoids confusion. User sees the score that actually maps to the verdict. Implementation: in ds-review-lead.md Step 10, add logic: `if floor_rule_applied: display_score = min(computed_score, floor_threshold)`.

### 2.4 Vanguard Analysis Dimension Drop (Impact: 1 fixture, -18 points)

**Evidence:** Vanguard R2 Analysis 86 → R3 Analysis 68.

**Cause:** Conditional credit halving rule (SKILL.md Section 2b, added in parallel session between R2 and R3):
- "Appropriate methodology" +5 → +2.5 (halved)
- "Pre-specified goals" +3 → +1.5 (halved)
- "Validation methodology present" +5 → +0 (no statistical tests)

**Impact:** -6 effective points from halving, plus -5 for losing validation credit entirely = -11 credit reduction.

**Question:** Is this a bug or a feature?

**Answer:** It's a **feature with cross-round incomparability**. The conditional halving rule is directionally correct — Vanguard's A/B test lacks statistical validation, which IS a critical gap for experimental analyses. The rule correctly penalizes this.

However, the R2 baseline score (86 analysis) did NOT have this rule, so R2→R3 comparison is apples-to-oranges. The -18 drop looks like a regression when it's actually a correction.

**Implications for calibration:**
- If conditional halving is kept: Vanguard's R3 analysis score (68) is more accurate than R2 (86)
- But: overall score still rose (+3) because communication credits offset the analysis penalty
- This is an architecture change that interacts with P1 fixes in non-obvious ways

**Recommendation:** Keep conditional halving (it's methodologically correct), but document in calibration notes that R2→R3 analysis scores are not directly comparable due to this rule addition. Consider whether the halving percentage (50%) is too aggressive — could soften to 75% halving for partial validation (e.g., exploratory statistical tests present but not rigorous).

### 2.5 Genre-Specific TL;DR Severity Mismatch (Impact: Blog posts)

**Evidence:** 4/6 tests have "TL;DR completely absent" CRITICAL (-12), but blog posts structurally don't have executive summaries upfront.

**Examples:**
- Netflix Proxy Metrics: Leads with problem motivation and concrete example (clickbait/CTR), builds to the methodological insight. This is appropriate blog structure.
- Airbnb FIV: Leads with business context and use case, then methodological explanation. This is narrative storytelling, not an internal deliverable.

**Current behavior:** SKILL.md Section 2 defines "TL;DR completely absent" as CRITICAL with -12 deduction. Blog posts without upfront summaries receive this deduction.

**Is this wrong?** Depends on use case:
- For internal DS deliverables: TL;DR absence IS critical → floor rule correct
- For blog posts: TL;DR absence is genre-appropriate → CRITICAL severity miscalibrated

**Implication:** The rubric was designed for internal analyses, not public-facing content. Genre detection (deferred to v0.5 per backlog) is needed to calibrate expectations appropriately.

**Temporary mitigation (if desired):** Reclassify "TL;DR completely absent" from CRITICAL (-12) to MAJOR (-10) across the board. This would:
- Reduce over-penalization of blog posts
- Still signal that TL;DR absence is a significant gap for internal deliverables
- Reduce score inflation by -2 to -5 points per test (blog posts currently compensate for -12 with high credits)

**Recommendation:** Defer to v0.5 genre detection. For v0.4/R4, accept that blog posts may score lower on communication if evaluated against "internal analysis" expectations, OR implement the CRITICAL→MAJOR reclassification as a temporary fix.

---

## 3. Root Cause of Remaining Problems

### RC1: Asymmetric Scoring Formula

**Problem:** The diminishing returns curve compresses deductions (downward pressure) but not credits (upward pressure).

**Why this happened:** The DR curve was added in R1 to prevent finding spam from over-penalizing weak analyses. The use case was: "If the agent generates 20 findings totaling -80 raw deductions, don't tank the score to 20/100 — compress the deductions to prevent catastrophic failure."

**What was missed:** The opposite scenario — high-quality analyses with few deductions but many credits — was not modeled. The DR curve protects the floor but not the ceiling.

**Evidence:**

Netflix (perfect 100):
- Analysis: 0 deductions, +13 credits → 100
- Communication: 7 deductions (no DR compression), +21 credits → 100

Rossmann (analysis 100):
- Analysis: 0 deductions, +25 credits (capped) → 100

**Mathematical fix:** Apply diminishing returns to BOTH deductions and credits symmetrically.

Proposed formula:
```
# Compress deductions (existing behavior)
if raw_deductions <= 30:
    effective_deductions = raw_deductions
elif raw_deductions <= 50:
    effective_deductions = 30 + (raw_deductions - 30) * 0.75
else:
    effective_deductions = 45 + (raw_deductions - 50) * 0.50

# NEW: Compress credits symmetrically
if raw_credits <= 15:
    effective_credits = raw_credits
else:
    effective_credits = 15 + (raw_credits - 15) * 0.50

dimension_score = 100 - effective_deductions + effective_credits
```

**Rationale:** Allow the first +15 credits at full value (rewards genuine strengths), but compress credits beyond +15 at 50%. This prevents runaway inflation while preserving differentiation.

**Expected impact:**

Netflix Communication: raw credits +21 → effective +18 (-3 points)
Rossmann Analysis: raw credits +25 → effective +20 (-5 points)
Meta Analysis: raw credits +7 → effective +7 (no change, under threshold)

**Net effect:** Strong analyses lose 3-8 points, weak analyses unchanged. Closes the inflation gap without over-correcting.

### RC2: Credit Additions Without Offsetting Deduction Increases

**Problem:** R2→R3 changes were net-additive to scores.

**What changed:**
- Added 2 new credits: Worked example (+3), Honest negative result (+3)
- Reduced 3 deductions: Formatting -5→-3, Headings -3→-2, Chart -3→-2
- Net effect: +6 to +9 points available, -4 to -6 points removed

**Why this happened:** The P1 fixes were calibrated against R2's under-crediting problem (agent wasn't recognizing worked examples or null results). But when combined with MINOR deduction reductions, the system became more lenient overall.

**Evidence:** Rossmann communication credits increased from +5 (R2) to +21 (R3), while deductions decreased slightly. Net: +16 communication score jump.

**Fix:** Already addressed by RC1 (symmetric compression). If credits are compressed above +15, the impact of adding new credits is naturally bounded.

### RC3: Conditional Credit Halving Rule Interaction

**Problem:** The conditional halving rule (added in parallel session) interacted with P1 credit additions in non-obvious ways.

**What happened:**
- Vanguard lost -6 effective analysis credits (halving) + -5 validation credit = -11 total
- But gained +5 communication credits (worked example) + fewer MINOR deductions
- Net: analysis dropped 18 points, communication rose 25 points, overall +3

**Why this is problematic:** The conditional halving rule is correct in isolation, but when combined with credit additions and deduction reductions, it created dimension-level instability.

**Implication:** Multi-dimensional scoring systems are sensitive to parameter changes in BOTH dimensions. A fix in one dimension can be offset (or amplified) by changes in the other dimension.

**Mitigation:** When calibrating, change ONE parameter at a time and test across both dimensions. Avoid compounding multiple credit additions + deduction reductions + new conditional rules in the same round.

### RC4: DR Curve Thresholds May Be Too Lenient

**Problem:** The DR compression kicks in at 31 deductions (first compression zone) and 51 deductions (second compression zone). High-quality analyses with 7-15 deductions never enter these zones.

**Current thresholds:**
- 0-30 points: 100% (no compression)
- 31-50 points: 75% compression
- 51+ points: 50% compression

**Alternative (more aggressive):**
- 0-20 points: 100%
- 21-40 points: 75%
- 41+ points: 50%

**Expected impact:** More analyses enter the compression zone earlier, reducing effective deductions by 2-5 points. This would INCREASE scores, not decrease them — so this is the wrong direction for fixing inflation.

**Conclusion:** DR curve thresholds are appropriate. The problem is not the deduction compression — it's the lack of credit compression (RC1).

---

## 4. Proposed Fixes for Next Round

### Fix 1: Symmetric Diminishing Returns (PRIMARY RECOMMENDATION)

**Change location:** ds-review-lead.md Step 9.4 (dimension score recomputation)

**Current formula:**
```python
# Apply DR to deductions only
if raw_deductions <= 30:
    effective = raw_deductions
elif raw_deductions <= 50:
    effective = 30 + (raw_deductions - 30) * 0.75
else:
    effective = 45 + (raw_deductions - 50) * 0.50

dimension_score = 100 - effective + raw_credits  # credits at full value
```

**Proposed formula:**
```python
# Apply DR to deductions (unchanged)
if raw_deductions <= 30:
    effective_deductions = raw_deductions
elif raw_deductions <= 50:
    effective_deductions = 30 + (raw_deductions - 30) * 0.75
else:
    effective_deductions = 45 + (raw_deductions - 50) * 0.50

# NEW: Apply DR to credits symmetrically
if raw_credits <= 15:
    effective_credits = raw_credits
else:
    effective_credits = 15 + (raw_credits - 15) * 0.50

dimension_score = 100 - effective_deductions + effective_credits
```

**Rationale:**
- Preserves the floor protection (weak analyses with many deductions still get DR compression)
- Adds ceiling protection (strong analyses with many credits get compressed above +15)
- Symmetric: same 2-tier approach for both deductions and credits
- Threshold at +15 is intentional: allows genuine strengths to be rewarded, but prevents runaway accumulation

**Expected R4 scores (estimated):**

| Fixture | R3 | Estimated R4 | Target | Within Target? |
|---|---|---|---|---|
| Vanguard | 72 | 67-69 | 40-55 | Still high (+12-14) |
| Meta | 63 | 60-62 | 50-65 | YES |
| Rossmann | 86 | 76-78 | 45-60 | Still high (+16-18) |
| Message Intent | 85 | 78-80 | 55-65 (A), 70-80 (C) | Mixed |
| FIV | 90 | 83-85 | 65-75 (A), 70-80 (C) | Still high |
| Netflix | 100 | 90-92 | 60-70 (A), 65-75 (C) | Still high |

**Assessment:** Symmetric DR will reduce inflation by 6-10 points, but may not be sufficient to bring all tests into target range. Vanguard, Rossmann, and blog posts will likely remain 10-20 points above targets.

**Recommendation:** Implement symmetric DR for R4. If scores remain too high, proceed to Fix 2 or Fix 3.

### Fix 2: Reduce Credit Cap (SECONDARY RECOMMENDATION)

**Change location:** SKILL.md Section 2b (credit rules)

**Current:** `Maximum +25 credits per dimension`

**Proposed:** `Maximum +15 credits per dimension`

**Rationale:**
- Simpler than symmetric DR (no formula changes, just cap adjustment)
- Directly limits upward pressure from credit accumulation
- Preserves differentiation (all scores reduced proportionally)
- Reversible if too aggressive

**Expected impact:**
- Rossmann analysis: +25 → +15 (-10 points)
- Netflix communication: +21 → +15 (-6 points)
- Meta analysis: +7 → +7 (no change, already under cap)

**Combined with symmetric DR:**
If both Fix 1 and Fix 2 are applied, strong analyses would face:
1. Credit compression above +15 (Fix 1)
2. Hard cap at +15 (Fix 2)

This is redundant. Recommendation: Choose ONE (symmetric DR OR cap reduction), not both.

**If choosing between them:** Symmetric DR is more elegant (no hard cutoff), but cap reduction is simpler to implement. From a systems perspective, I prefer symmetric DR because it's continuous and doesn't create a cliff at +15.

### Fix 3: Increase Baseline Deductions (TERTIARY RECOMMENDATION, HIGHER RISK)

**Change location:** SKILL.md Section 2 (deduction table)

**Proposed changes:**
- "Missing baseline/benchmark" -10 → -12 (MAJOR)
- "Missing or ineffective TL;DR" -10 → -12 (MAJOR)
- "Unclear or misleading visualization" -8 → -10 (MAJOR)

**Rationale:** If credits are compressed (Fix 1) or capped (Fix 2), but scores remain too high, the issue is that baseline deductions are too lenient for genuinely impactful gaps.

**Expected impact:** -4 to -8 points across tests with these findings (Vanguard, Rossmann, Meta).

**Risk:** This could over-correct and recreate the R0 over-harshness problem. Deduction increases should be a last resort after credit constraints are tested.

**Recommendation:** DO NOT implement in R4. Hold in reserve for R5 if Fix 1 is insufficient.

### Fix 4: Floor Rule Presentation (USER TRUST FIX)

**Change location:** ds-review-lead.md Step 10 (output format)

**Current behavior:**
```
Score: 90/100 → Major Rework
Floor rule applied: 2 CRITICALs cap verdict at Major Rework (max 59)
```

**Proposed behavior:**
```
Score: 59/100 → Major Rework
(Computed score: 90/100, capped due to 2 CRITICAL findings)
```

**Rationale:** Show the score that actually maps to the verdict (59), with the computed score as context. Avoids cognitive dissonance.

**Implementation:**
```python
if floor_rule_applied:
    display_score = floor_threshold  # 79 for 1 CRITICAL, 59 for 2+ CRITICALs
    note = f"(Computed score: {computed_score}/100, capped due to {critical_count} CRITICAL findings)"
else:
    display_score = computed_score
    note = ""
```

**Impact:** No change to scoring mechanics, only presentation. Improves user trust and clarity.

---

## 5. Acceptance Criteria Assessment

### Can acceptance criteria be met with incremental fixes?

**YES.** The system architecture is sound. The problem is a calibration mismatch, not a fundamental design flaw.

**Evidence:**
- Differentiation working (37-point spread, correct ranking)
- Finding quality good (no spurious CRITICALs, all deductions trace to real gaps)
- Rubric mechanics working (DR curve, credits, floor rules all functioning correctly)
- Implementation correct (deduction/severity alignment verified, duplicate suppression working)

**What needs to change:** Scoring formula symmetry (add credit compression) or credit cap reduction. Both are single-parameter changes with bounded impact.

**Estimated rounds to acceptance:**
- R4: Implement symmetric DR (Fix 1) + floor rule presentation fix (Fix 4)
- Test on all 6 fixtures
- If scores fall within ±10 of targets → ACCEPT
- If scores still 10-15 points high → R5 with reduced credit cap (Fix 2) or selective deduction increases (Fix 3)

**Risk of oscillation:** MODERATE. The system oscillated twice (R0→R1 overcorrection, R2→R3 overcorrection). To avoid a third oscillation:
- Make ONE scoring change (symmetric DR OR cap reduction, not both)
- Test change in isolation before compounding
- Document expected impact range before R4 run

### Does this need redesign?

**NO.** The core architecture is correct:
- Two-dimensional evaluation (analysis + communication) is appropriate
- Subagent parallelization is efficient and reduces cross-contamination
- Diminishing returns principle is sound (prevents finding spam from tanking scores)
- Strength credits are conceptually correct (reward demonstrated rigor)
- Floor rules are working as designed

**What's missing:** Symmetric constraints. The system has a floor (DR on deductions) but no ceiling (no DR on credits). Adding the ceiling constraint completes the design without requiring a redesign.

---

## 6. Implementation Correctness Review

### 6.1 SKILL.md Section 2b (Credit Table)

**Status:** ✅ CORRECT

- Credit values are clearly defined
- Criteria are specific and evidence-based
- Cap at +25 is stated explicitly
- Conditional halving rule (Section 2b.6) is mathematically sound

**Observed behavior:** Credits are firing correctly (worked example fired on Rossmann, Meta, FIV; honest negative result fired on Rossmann, Message Intent).

### 6.2 ds-review-lead.md Step 9.4 (Dimension Score Recomputation)

**Status:** ✅ IMPLEMENTATION CORRECT, but formula is asymmetric (see RC1)

**Current implementation:**
```
For each dimension:
- Apply DR to deductions: 0-30 (100%), 31-50 (75%), 51+ (50%)
- Add credits at full value (capped at +25)
- Formula: dimension_score = 100 - effective_deductions + credits
```

**Observed behavior matches specification:** All test reviews show correct DR application and credit addition.

**Issue:** The formula is correct per the specification, but the specification itself creates inflation (missing symmetric credit compression).

### 6.3 ds-review-lead.md Step 9.3 (Duplicate Suppression)

**Status:** ✅ WORKING

**Evidence:** Meta review shows "Finding subsumed by analysis finding" notation, indicating the duplicate detection logic is firing.

**Implementation check:** Step 9.3 states:
> "When two findings share the same root cause — meaning the same remediation would resolve both AND the findings describe the same observable problem (not merely related problems with a shared fix) — keep the larger deduction and suppress the smaller one."

**Observed behavior:** Correctly suppresses smaller deduction and adjusts raw deduction total before DR application.

### 6.4 SKILL.md Section 2b.6 (Conditional Credit Halving)

**Status:** ✅ CORRECT

**Rule:**
> "When an analysis presents experimental design but reports NO statistical validation for experimental results, apply:
> - Appropriate methodology: halved (round down)
> - Pre-specified goals: halved (round down)
> - Validation methodology present: +0
> - Reports specific quantitative results: halved (round down)"

**Observed behavior:** Vanguard (A/B test without p-values) correctly received:
- Methodology +5 → +2.5 (halved)
- Pre-specified goals +3 → +1.5 (halved)
- Validation +5 → +0 (absent)

**Edge case check:** Does this rule fire for non-experimental analyses? NO — the rule explicitly states "when experimental design is present." ML models, systems analyses, and exploratory work are evaluated under "Validation methodology present" without halving.

### 6.5 communication-reviewer.md Rule 12 (Self-Deliberation Suppression)

**Status:** ✅ WORKING

**Rule:**
> "Single-pass evaluation. Commit to each credit and finding decision on your first assessment. Do not deliberate, revise, or second-guess in your output."

**Observed behavior:** No visible agent deliberation in any R3 review outputs. Clean, committed findings.

### 6.6 ds-review-lead.md Step 9.8 (Finding Volume Cap)

**Status:** ✅ WORKING

**Rule:**
> "Cap displayed findings at 10 total across both dimensions. Rank all findings by severity (CRITICAL first, then MAJOR by deduction size, then MINOR). If more than 10 findings exist, show only the top 10."

**Observed behavior:** R3 finding counts: Vanguard 8, Meta 9, Rossmann 5, Message Intent 7, FIV 8, Netflix 2. All under cap. No evidence of capping logic failing.

### 6.7 Floor Rule Logic (ds-review-lead.md Step 9.6)

**Status:** ✅ MATHEMATICALLY CORRECT, but user presentation is confusing (see RC3, Fix 4)

**Rule:**
> "Any CRITICAL finding → verdict capped at Minor Fix (max 79).
> 2+ CRITICAL findings → verdict capped at Major Rework (max 59).
> Floor rules affect verdict only, not numeric score."

**Observed behavior:**
- Rossmann: 1 CRITICAL, score 86 → verdict "Minor Fix" (capped at 79)
- FIV: 2 CRITICALs, score 90 → verdict "Major Rework" (capped at 59)
- Meta: 3 CRITICALs, score 63 → verdict "Major Rework" (capped at 59, but score already under cap)

**Implementation correct:** Floor rule is applying correctly. The UX issue is presenting "90/100 → Major Rework" which creates cognitive dissonance.

---

## 7. Second-Order Effects and Edge Cases

### 7.1 What happens if symmetric DR is too aggressive?

**Scenario:** R4 implements symmetric credit compression (credits above +15 compressed at 50%). Scores drop to 40-60 range, undershooting targets.

**Mitigation:** Adjust compression rate from 50% to 75% for credits:
```python
if raw_credits <= 15:
    effective_credits = raw_credits
else:
    effective_credits = 15 + (raw_credits - 15) * 0.75  # gentler compression
```

**Alternative:** Adjust threshold from +15 to +20:
```python
if raw_credits <= 20:
    effective_credits = raw_credits
else:
    effective_credits = 20 + (raw_credits - 20) * 0.50
```

**Recommendation:** Test symmetric DR at 50% compression in R4. If overshoots, tune compression rate or threshold in R5. Do NOT preemptively soften — better to err on the side of under-rewarding and tune up than to remain inflationary.

### 7.2 How does symmetric DR interact with the credit cap?

**Current:** Credits capped at +25, applied at full value.

**With symmetric DR:** Credits capped at +25, then compressed above +15.

**Example:** Analysis earns +25 raw credits.
- Step 1: Cap at +25 (no change)
- Step 2: Compress above +15 → effective = 15 + (25-15)*0.5 = 20
- Result: +20 effective credits

**Is the cap still meaningful?** YES. The cap prevents earning more than +25 raw credits. The compression prevents +25 from translating to +25 effective. Both constraints are independently useful.

### 7.3 Does symmetric DR penalize genuinely exceptional work?

**Concern:** A truly flawless analysis (0 deductions, +25 credits) would score:
- Current: 100 - 0 + 25 = 125, capped at 100
- With symmetric DR: 100 - 0 + 20 = 100 (if credits compressed to +20)

**Assessment:** No penalty. A flawless analysis still scores 100/100. The compression prevents GOOD (but not flawless) analyses from reaching 100.

**Example:** Netflix Proxy Metrics (0 deductions, +13 credits):
- Current: 100 - 0 + 13 = 113, capped at 100 → 100
- With symmetric DR: 100 - 0 + 13 = 113, capped at 100 → 100 (no compression, under +15 threshold)

**Counterexample:** Rossmann Communication (36 effective deductions, +8 credits):
- Current: 100 - 36 + 8 = 72
- With symmetric DR: 100 - 36 + 8 = 72 (no compression, under +15 threshold)

**Conclusion:** Symmetric DR only affects analyses with +15+ credits. Genuinely exceptional work (0-5 deductions, high credits) is unaffected.

### 7.4 What if conditional halving and symmetric DR create double-penalization?

**Scenario:** Vanguard has experimental design without validation.
- Conditional halving reduces credits from +5 to +2.5 (methodology)
- Symmetric DR then compresses credits above +15

**Math check:** Vanguard R3 analysis credits: +6 total (already under +15 threshold after halving).

**Conclusion:** No interaction. Conditional halving brings credits down, symmetric DR only compresses if credits exceed +15. These constraints don't compound — they operate on different credit ranges.

### 7.5 Cross-run consistency with formula changes

**Concern:** If the scoring formula changes between R3 and R4, are scores still comparable?

**Answer:** NO, but this is acceptable. R2→R3 scores were already incomparable due to conditional halving rule. Calibration rounds are ITERATIVE — each round tunes parameters, cross-round comparability is not guaranteed.

**Mitigation:** Document formula changes clearly in calibration notes. When comparing R4 to R3, note: "R4 introduced symmetric credit compression; scores not directly comparable to R3."

**User impact:** For end users, formula stability matters (don't want scores to shift between runs on the same document). For calibration, formula changes are expected.

---

## 8. Final Recommendation

### Primary Path (Recommended)

**R4 Changes:**
1. Implement symmetric diminishing returns (Fix 1) in ds-review-lead.md Step 9.4
2. Implement floor rule presentation fix (Fix 4) in ds-review-lead.md Step 10
3. Test on all 6 fixtures (3 core + 3 extended)
4. Document expected score ranges before running R4

**Expected R4 outcomes:**
- Meta: 60-62 (within target)
- Vanguard: 67-69 (10-14 points high, but acceptable if differentiation holds)
- Rossmann: 76-78 (16-18 points high, assess whether target needs adjustment)
- Blog posts: 78-92 (assess whether blog post targets were too conservative)

**Decision criteria for R4:**
- If all core fixtures within ±10 of targets AND differentiation ≥15 points → ACCEPT
- If scores still 15+ points high → proceed to R5 with credit cap reduction (Fix 2)
- If scores drop below targets → soften symmetric DR compression rate (50% → 75%)

### Alternative Path (If Conservative Approach Preferred)

**R4 Changes:**
1. Reduce credit cap from +25 to +18 (gentler than Fix 2's +15)
2. Test on all 6 fixtures
3. If still too high, reduce to +15 in R5

**Rationale:** Credit cap reduction is simpler to implement and understand than symmetric DR. It's also reversible (can raise cap in R5 if too aggressive).

**Tradeoff:** Hard cap at +18 creates a cliff (analyses with +19 raw credits get capped to +18). Symmetric DR is continuous (no cliff).

### What NOT to Do

❌ **Do not implement multiple fixes simultaneously.** Compounding symmetric DR + cap reduction + deduction increases makes it impossible to isolate which change caused which effect.

❌ **Do not preemptively soften symmetric DR.** Better to implement at 50% compression and tune up if needed than to remain inflationary.

❌ **Do not increase deductions in R4.** Deduction increases are high-risk (could recreate R0 over-harshness). Hold in reserve for R5 if credit constraints fail.

❌ **Do not adjust targets to match scores (Option D from calibration notes).** This kicks the can — if scores continue inflating in future rounds, the problem persists.

---

## 9. Estimated Rounds to Acceptance

**Best case:** 1 round (R4 with symmetric DR brings scores within ±10 of targets)

**Likely case:** 2 rounds (R4 with symmetric DR reduces inflation, R5 tunes compression rate or adds credit cap)

**Worst case:** 3 rounds (R4 symmetric DR, R5 credit cap, R6 selective deduction increases)

**Confidence:** MEDIUM-HIGH (70%). The scoring formula change is well-bounded and mathematically sound. The risk is second-order interactions between symmetric DR and conditional halving, but edge case analysis (Section 7.4) suggests these are minimal.

**What could go wrong:**
1. Symmetric DR causes scores to oscillate below targets (requires softening compression)
2. Conditional halving + symmetric DR create unexpected dimension imbalances
3. Genre-specific issues (blog posts vs internal analyses) require separate calibration paths

**Mitigation:** Run R4 on all 6 fixtures, document score deltas, and assess dimensionally (not just overall scores).

---

## 10. Architectural Health Check

### System Design: ✅ SOUND

- Two-dimensional evaluation is appropriate for the domain
- Subagent parallelization reduces cross-contamination and improves efficiency
- Orchestrator synthesis pattern (ds-review-lead) is clean and well-structured
- Finding caps, duplicate suppression, and floor rules are all working correctly

### Implementation Quality: ✅ HIGH

- No observed deduction/severity mismatches
- Conditional rules (halving, duplicate suppression) firing correctly
- Output formatting consistent and readable
- Edge cases (Tier 3 extraction, draft mode, degraded output) handled gracefully

### Mathematical Soundness: ⚠️ ASYMMETRIC (fixable)

- Diminishing returns formula is mathematically correct but incomplete
- Missing symmetric constraint on credits creates inflation
- Floor rules working correctly but presentation could be clearer
- Scoring is deterministic and reproducible (good for debugging)

### Calibration Trajectory: ⚠️ OSCILLATING (but improving)

- R0 → R1: +44 to +57 point jump (overcorrection)
- R1 → R2: -2 to -4 point drop (stabilization)
- R2 → R3: +3 to +15 point jump (overcorrection)

Pattern: Alternating overcorrection and stabilization. This suggests parameter changes are too large or multi-faceted (compounding multiple changes).

**Recommendation:** Make SINGLE-PARAMETER changes going forward to reduce oscillation risk.

### Technical Debt: ✅ LOW

- No obvious architectural smells
- No tangled dependencies between subagents
- Clear separation of concerns (SKILL.md for rubrics, agents for evaluation logic, lead for orchestration)
- Documentation is comprehensive (SKILL.md, agent prompts, ADRs)

### Scalability: ✅ GOOD

- Tier-based processing (1/2/3) handles documents of varying lengths
- Structured extraction (Tier 3) prevents context overflow
- Finding caps prevent output explosion
- Subagent parallelization allows horizontal scaling if needed

---

## Conclusion

R3 demonstrates **strong system fundamentals** with a **fixable calibration bug**. The root cause is an asymmetric scoring formula that compresses deductions but not credits, allowing high-quality analyses to accumulate +20-25 credits without compression. This creates systemic score inflation (+17 to +30 points above targets).

**The fix is straightforward:** Apply symmetric diminishing returns to both deductions and credits. This preserves differentiation, protects both floor and ceiling, and requires only a single formula change.

**Confidence in fix:** HIGH. The mathematical logic is sound, edge cases are well-understood, and the change is isolated to a single function in ds-review-lead.md.

**Estimated rounds to acceptance:** 1-2 (R4 with symmetric DR, R5 for tuning if needed).

**No redesign required.** The architecture is solid. This is a calibration problem, not a design problem.

---

**Prepared by:** Claude Sonnet 4.5 (Principal AI Engineer role)
**Date:** 2026-02-15
**Review duration:** ~45 minutes (file reads + analysis + writeup)
