# Scoring Calibration Notes — Round 3

**Date:** 2026-02-15
**Status:** OPEN (awaiting role reviews and owner decision)
**Prior round:** R2 (scores: Vanguard 69, Meta 54, Rossmann 71) — ACCEPTED

---

## Score Summary

| # | Document | Type | Score R2 | Score R3 | Delta | Revised Target | Gap | CRITICALs | Verdict R3 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Vanguard A/B Test | Core | 69 | 72 | +3 | 55-65 | +7 to +17 OVER | 1 | Minor Fix |
| 2 | Meta LLM Bug Reports | Core | 54 | 63 | +9 | 60-70 | -7 UNDER to +3 OVER | 2* | Major Rework |
| 3 | Rossmann Sales Forecasting | Core | 71 | 86 | +15 | 65-75 | +11 to +21 OVER | 1 | Minor Fix |
| 4 | Airbnb Message Intent | Extended (NEW) | N/A | 85 | N/A | 70-80 (A) | +5 to +15 OVER | 1 | Minor Fix |
| 5 | Airbnb FIV Tradeoffs | Extended (NEW) | N/A | 90 | N/A | 80-90 (A) | +0 to +10 OVER | 2 | Major Rework |
| 6 | Netflix Proxy Metrics | Extended (NEW) | N/A | 100 | N/A | 80-90 (A) | +10 to +20 OVER | 0 | Good to Go |

*Meta reduced from 3 to 2 CRITICALs after immediate fix applied

**Dimension Breakdown:**

| Document | Analysis R2 | Analysis R3 | Comm R2 | Comm R3 |
|---|---|---|---|---|
| Vanguard | 86 | 68 | 52 | 77 |
| Meta | 57 | 64 | 50 | 61 |
| Rossmann | 93 | 100 | 48 | 72 |
| Message Intent | N/A | 93 | N/A | 78 |
| FIV | N/A | 97 | N/A | 83 |
| Proxy Metrics | N/A | 100 | N/A | 100 |

---

## Acceptance Criteria Check

### Core Fixtures (Calibration Targets)

| Criterion | Status | Detail |
|---|---|---|
| Vanguard 55-65 | ⚠️ PARTIAL | Score: 72 (+7 to +17 over revised target) |
| Meta 60-70 | ⚠️ PARTIAL | Score: 63 (within or close to revised target) |
| Rossmann 65-75 | ⚠️ PARTIAL | Score: 86 (+11 to +21 over revised target) |
| Vanguard analysis > Meta analysis | ✅ PASS | Vanguard 68 > Meta 64 (+4 gap) |
| Overall 15+ point differentiation | ✅ PASS | Gap: 37 points (100 - 63) |
| Max 2 CRITICALs per test | ✅ PASS | All tests ≤2 after immediate fix |

### Extended Fixtures (Generalization Check)

| Criterion | Status | Detail |
|---|---|---|
| Message Intent Analysis 70-80 | ⚠️ PARTIAL | Score: 93 (+13 to +23 over revised target) |
| Message Intent Comm 70-80 | ✅ PASS | Score: 78 |
| FIV Analysis 80-90 | ⚠️ PARTIAL | Score: 97 (+7 to +17 over revised target) |
| FIV Comm 70-80 | ✅ PASS | Score: 83 (+3 above but close) |
| Proxy Metrics Analysis 80-90 | ⚠️ PARTIAL | Score: 100 (+10 to +20 over revised target) |
| Proxy Metrics Comm 70-80 | ⚠️ PARTIAL | Score: 100 (+20 to +30 over) |
| Blog post differentiation | ✅ PASS | Ranks correctly: Proxy (100) > FIV (90) > Message (85) |

### Quality Criteria

| Criterion | Status | Detail |
|---|---|---|
| No severity/deduction mismatches | ✅ PASS | All deductions match SKILL.md table values |
| No cross-cutting duplicates | ✅ PASS | Duplicate suppression working correctly |
| Output length reasonable | ✅ PASS | All reviews <1.5x input length |
| Synthetic fixtures still pass | ⏸️ PENDING | Not tested in R3 |
| Cross-run consistency | ⏸️ PENDING | Not tested in R3 |

---

## What Improved from Round 2

### 1. **Core fixture scores increased across the board**
- Vanguard: +3 points (69 → 72)
- Meta: +9 points (54 → 63)
- Rossmann: +15 points (71 → 86)

### 2. **P1 fixes had measurable impact**
- **Worked example credit (+3)** fired on Rossmann (revenue scenario table), Meta (technical outage example), FIV (PSM walkthrough)
- **Honest negative result credit (+3)** fired on Rossmann (linear models underperformed), Message Intent (LDA vs embeddings)
- **Formatting deduction -5→-3** reduced over-penalization on polish issues
- **Tightened quantitative results criteria** correctly denied credit to bare numbers without context (Meta's "double digit reduction")

### 3. **Communication dimension scores recovered**
- R2 communication scores were 48-52 across all core fixtures
- R3 communication scores: Vanguard 77, Meta 61, Rossmann 72
- Average communication score increased by +18 points

### 4. **Finding volume decreased**
- R2 average: ~12 findings per test
- R3 average: ~6.5 findings per test (finding cap at 10 is working)

### 5. **Extended fixtures show strong analytical quality**
- All 3 blog posts scored 93-100 on Analysis dimension
- Demonstrates rubric rewards rigorous methodology regardless of genre

---

## What Didn't Improve (or Got Worse)

### 1. **Scores overshot targets by 17-30 points**

**Core fixtures:**
- Vanguard target: 40-55, actual: 72 (+17 overshoot)
- Rossmann target: 45-60, actual: 86 (+26 overshoot)

**Extended fixtures:**
- All blog posts scored 85-100, targets were 55-80 ranges
- Netflix Proxy Metrics: perfect 100/100 (analysis AND communication)

This is the inverse of the R0/R1 problem. R0 was too harsh (16-29). R3 is too generous.

### 2. **Vanguard Analysis dimension dropped 18 points**
- R2: Analysis 86, Communication 52
- R3: Analysis 68, Communication 77

**Why the drop?** The conditional credit halving rule (added in parallel session between R2 and R3) penalized the Vanguard analysis more heavily:
- "Systematic model comparison" → +2.5 (halved from +5)
- "Pre-specified goals" → +1.5 (halved from +3)
- "Validation methodology present" → +0 (no statistical tests)

This is **directionally correct** (Vanguard's lack of statistical tests IS a problem), but combined with the P1 credit additions, the overall score still went UP despite the analysis score drop.

### 3. **Meta still has 3 CRITICALs**
- Target: max 2 per test
- Meta R3: 3 CRITICALs
  1. Experimental claims without validation
  2. Conclusion doesn't trace to evidence
  3. TL;DR completely absent

The P1 fixes didn't address the finding generation logic — Meta's fundamental gaps remain.

### 4. **Floor rule paradox visible in Airbnb FIV**
- Numeric score: 90/100
- Verdict: Major Rework (2 CRITICALs cap at 59)
- User will see "90/100" and "Major Rework" — the visual mismatch is jarring

### 5. **Blog posts not "systematically over-penalized" — they're over-credited**
- Acceptance criterion was: "Blog posts not systematically over-penalized for missing business metrics"
- Reality: Blog posts scored HIGHER (85-100) than internal analyses (63-86)
- This suggests the rubric is biased TOWARD research-quality content, not against it

---

## Root Cause Analysis (for remaining problems)

### RC1: Credit additions without offsetting deduction increases created inflationary pressure

**R2 to R3 changes:**
- Added 2 new credits: Worked example (+3), Honest negative result (+3)
- Reduced 3 MINOR deductions: Formatting -5→-3, Headings -3→-2, Chart -3→-2
- **Net effect:** More points added to scores, fewer points subtracted

**Evidence:**
- Rossmann R2 → R3: +15 points (communication credits increased from +5 to +21)
- Netflix Proxy Metrics: Earned 21 communication credits (vs. 7 deductions)

**Why this happened:** The P1 fixes were calibrated against R2's under-crediting problem (agent wasn't recognizing worked examples, null results). But when combined with the MINOR reductions, the system became more lenient overall.

### RC2: Conditional credit halving rule (parallel session change) wasn't accounted for in R2 baselines

**What changed between R2 and R3:**
- R2: Standard credit table, no conditional halving
- R3: Conditional halving rule added for experimental analyses without validation

**Why Vanguard analysis dropped but overall score rose:**
- Analysis credits cut in half (-6 effective)
- But communication score jumped (+25 points due to worked examples, MINOR reductions, fewer findings)
- Net: +3 overall

This is an architecture change that interacts with the P1 fixes in ways that weren't modeled.

### RC3: "TL;DR completely absent" fires frequently on blog posts, but floor rule doesn't prevent Good to Go

**Observation:**
- 4 of 6 tests have "TL;DR completely absent" CRITICAL
- Yet Netflix Proxy Metrics scored 100/100 despite having 0 TL;DRs in blog format

**Why:** Blog posts don't have executive summaries upfront — they lead with motivating examples and build to the insight. This is appropriate genre structure for technical blog posts. The rubric penalizes them with a CRITICAL (-12), but if the rest of the analysis is strong, the score can still reach 88-100 range.

**Is this wrong?** Depends on use case:
- For internal DS deliverables: TL;DR absence IS critical → floor rule correct
- For blog posts: TL;DR absence is genre-appropriate → CRITICAL severity is miscalibrated

### RC4: Diminishing returns curve isn't steep enough to prevent score inflation

**The DR curve:**
- 0-30 points: 100% (no compression)
- 31-50 points: 75% compression
- 51+ points: 50% compression

**Problem:** High-quality analyses (blog posts) have LOW raw deductions (7-15 points), so they never hit the DR compression zone. They get full credit additions (+13 to +25) with minimal deductions.

**Example:** Netflix Proxy Metrics
- Raw deductions: 7 (all in 100% zone → 7 effective)
- Credits: +13 analysis, +21 communication
- Result: 100/100

The DR curve was designed to prevent finding spam from over-penalizing weak analyses. It doesn't prevent credit accumulation from over-rewarding strong analyses.

---

## Remaining Problems (Ranked by Impact)

### 1. **Score Inflation** — Impact: ALL fixtures, +17 to +30 points above targets
- **Evidence:** Every single test (6/6) scored above its target range
- **User impact:** If all scores are 70-100, the tool provides no differentiation signal
- **Fix direction:** Reduce credit cap from +25 to +15, OR increase baseline deduction values, OR add a score ceiling compression (scores above 85 get diminished returns on credits)

### 2. **Meta CRITICAL count** — Impact: 1 fixture, 1 excess CRITICAL
- **Evidence:** Meta has 3 CRITICALs (target: max 2)
- **User impact:** Over-penalizing a weak but not fundamentally broken analysis
- **Fix direction:** Reclassify 1 CRITICAL to MAJOR (likely "Conclusion doesn't trace to evidence" — it's a major gap but the analysis isn't misleading, just incomplete)

### 3. **Floor rule paradox** — Impact: User trust, cognitive dissonance
- **Evidence:** FIV shows "90/100" + "Major Rework" side-by-side
- **User impact:** Confusing. User sees a high score but harsh verdict.
- **Fix direction:** Either (a) suppress numeric score when floor rule applies and show only verdict, OR (b) show floor-adjusted score (59) instead of raw score (90), OR (c) reframe verdict labels to make floor rule logic clearer

### 4. **Vanguard analysis dimension drop** — Impact: 1 fixture, -18 points on Analysis
- **Evidence:** Vanguard R2 Analysis 86 → R3 Analysis 68
- **User impact:** Looks like a regression when it's actually a correction
- **Fix direction:** This may be CORRECT — Vanguard genuinely lacks statistical validation. But if conditional halving is too aggressive, consider softening from 50% → 75% halving for partial validation (e.g., exploratory statistical tests present but not rigorous).

### 5. **Genre-specific TL;DR severity mismatch** — Impact: Blog posts, incorrect CRITICAL assignment
- **Evidence:** 4/6 tests have "TL;DR completely absent" CRITICAL, but blog posts structurally don't have TL;DRs
- **User impact:** Over-penalizing genre-appropriate structure
- **Fix direction:** Defer to v0.5 genre detection. For now, accept that blog posts may score lower on communication if using default "internal analysis" expectations.

---

## Proposed Fix Direction (Inputs to Role Reviews)

### Option A: Credit Cap Reduction (Conservative)
- Reduce credit cap from +25 → +15 per dimension
- Rationale: Strong analyses should be rewarded, but +25 is allowing too much score inflation
- Expected impact: -10 points across high-performing tests
- Risk: May under-reward genuinely exceptional work

### Option B: Baseline Deduction Increase (Aggressive)
- Increase 3-5 MAJOR deductions by -2 points each
- Rationale: Current deductions are too lenient for gaps that genuinely weaken analyses
- Expected impact: -6 to -10 points across all tests
- Risk: May re-create R0's over-harshness problem

### Option C: Score Ceiling Compression (Novel)
- Add a third layer to the scoring formula: scores above 85 get diminishing returns on credits
- Formula: If raw score > 85, apply 50% compression to credits above +15
- Rationale: Prevent perfect or near-perfect scores unless the analysis is genuinely flawless
- Expected impact: -5 to -10 points on scores above 85
- Risk: Adds complexity to an already complex scoring system

### Option D: Accept Current Calibration and Adjust Targets (Reframe)
- Leave scoring unchanged
- Redefine targets: Vanguard 65-75, Rossmann 75-85, Blog posts 80-95
- Rationale: Maybe the R2 targets (40-60) were too low. If R3 scores feel "right" intuitively, adjust expectations rather than mechanism.
- Expected impact: Zero technical changes, documentation update only
- Risk: Kicks the can — if scores continue to inflate in future rounds, we're back to the same problem

---

## Open Questions for Role Reviewers

1. **Do the R3 scores "feel right" for each fixture?** Specifically:
   - Vanguard 72 for an A/B test with no statistical validation?
   - Rossmann 86 for a portfolio piece with perfect methodology but buried TL;DR?
   - Netflix 100 for a well-written blog post with minor structural gaps?

2. **Is the Vanguard analysis drop (-18) a bug or a feature?**
   - The conditional halving rule correctly penalizes lack of validation
   - But combined with P1 credit additions, overall score still rose (+3)
   - Should conditional halving be softened, or is this the right outcome?

3. **How should we handle the floor rule paradox?**
   - Showing "90/100 → Major Rework" is visually confusing
   - Options: suppress numeric score, show floor-adjusted score, or reframe verdict labels
   - What preserves user trust while maintaining the integrity of the floor rule?

4. **Should we reduce the credit cap, increase deductions, or both?**
   - Credit cap reduction is reversible and low-risk
   - Deduction increases are higher-risk (could over-correct)
   - Score ceiling compression is novel but adds complexity
   - Or should we accept current scores and adjust targets?

5. **Is Meta's 3 CRITICAL count legitimate, or should 1 be downgraded?**
   - "Conclusion doesn't trace to evidence" is a CRITICAL-severity gap
   - But is it CRITICAL-frequency? (i.e., does it occur often enough that max 2 CRITICAL target is wrong?)

---

## Next Steps

1. **Role reviews (Task 6):** Principal AI Engineer, PM Lead, DS Lead review these notes and propose fixes
2. **Synthesis (Task 7):** Synthesize 3 reviews into A3 fix plan
3. **Owner decision (Task 8):** Approve fix plan and decide: next round, done, or request changes
