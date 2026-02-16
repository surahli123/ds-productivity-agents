# Calibration Round Comparison: R3 vs R2

**Date:** 2026-02-15

---

## Score Trajectory

| Document | R0 | R1 | R2 | R3 | Target | Gap to Target |
|---|---|---|---|---|---|---|
| Vanguard | 16 | 73 | 69 | 72 | 40-55 | +17 to +32 (ABOVE) |
| Meta | 18 | 59 | 54 | 63 | 50-65* | +0 to +13 (WITHIN/ABOVE) |
| Rossmann | 29 | 71 | 71 | 86 | 45-60 | +26 to +41 (ABOVE) |

*Meta target adjusted by owner to "Major Rework acceptable" in R2

### Extended Fixtures (New in R3)

| Document | R3 | Target | Gap to Target |
|---|---|---|---|
| Airbnb Message Intent | 85 | Analysis 55-65, Comm 70-80 | Analysis +28 ABOVE |
| Airbnb FIV | 90 | Analysis 65-75, Comm 70-80 | Analysis +22 ABOVE |
| Netflix Proxy Metrics | 100 | Analysis 60-70, Comm 65-75 | Analysis +30 ABOVE, Comm +25 ABOVE |

---

## CRITICAL Count Trajectory

| Document | R0 | R1 | R2 | R3 | Target |
|---|---|---|---|---|---|
| Vanguard | 5 | 1 | 1 | 1 | ≤2 ✅ |
| Meta | 4 | 2 | 2 | 3 | ≤2 ❌ |
| Rossmann | 2 | 1 | 1 | 1 | ≤2 ✅ |

**New fixtures:**
- Airbnb Message Intent: 1 CRITICAL ✅
- Airbnb FIV: 2 CRITICALs ✅
- Netflix Proxy Metrics: 0 CRITICALs ✅

---

## Finding Count Trajectory

| Document | R0 | R1 | R2 | R3 | Target |
|---|---|---|---|---|---|
| Vanguard | 16 | ~10 | ~10 | 8 | ≤10 ✅ |
| Meta | 15 | ~10 | ~10 | 9 | ≤10 ✅ |
| Rossmann | 15 | ~10 | ~10 | 5 | ≤10 ✅ |

**New fixtures:**
- Airbnb Message Intent: 7 findings ✅
- Airbnb FIV: 8 findings ✅
- Netflix Proxy Metrics: 2 findings ✅

---

## Dimension Score Trajectory

### Vanguard

| Round | Analysis | Communication | Overall |
|---|---|---|---|
| R0 | ~20 | ~12 | 16 |
| R1 | 81 | 65 | 73 |
| R2 | 86 | 52 | 69 |
| R3 | 68 | 77 | 72 |

**Notable:** Analysis dropped 18 points (86 → 68) due to conditional credit halving rule, but Communication jumped 25 points (52 → 77), resulting in net +3 overall.

### Meta

| Round | Analysis | Communication | Overall |
|---|---|---|---|
| R0 | ~22 | ~14 | 18 |
| R1 | 63 | 55 | 59 |
| R2 | 57 | 50 | 54 |
| R3 | 64 | 61 | 63 |

**Notable:** Steady improvement across both dimensions (+7 analysis, +11 communication). Still in Major Rework territory due to 3 CRITICALs.

### Rossmann

| Round | Analysis | Communication | Overall |
|---|---|---|---|
| R0 | ~35 | ~23 | 29 |
| R1 | 88 | 53 | 71 |
| R2 | 93 | 48 | 71 |
| R3 | 100 | 72 | 86 |

**Notable:** Achieved perfect Analysis score (100/100). Communication jumped 24 points (48 → 72) due to worked example credit and MINOR deduction reductions.

---

## What Changed Between Rounds

### Fixes Applied in R3

**From parallel session (between R2 and R3):**
1. Self-deliberation suppression (communication-reviewer.md Rule 12)
2. Duplicate-finding detection (ds-review-lead.md Step 9)
3. Conditional credit halving for experimental analyses without validation (SKILL.md Section 2b)

**From this session (P1 fixes):**
4. Worked example credit (+3) added to Communication credits
5. Honest negative result credit (+3) added to Analysis credits
6. Tightened "quantitative results" criteria (requires contextualizing element)
7. Formatting deduction reduced: -5 → -3
8. Minor deductions reduced: headings -3 → -2, chart -3 → -2

---

## Expected Impact vs Actual Impact

| Fix | Expected Effect | Actual Effect | Assessment |
|---|---|---|---|
| **P0-1: Self-deliberation suppression** | Remove visible agent deliberation from output | ✅ Worked - no deliberation artifacts in R3 reviews | SUCCESS |
| **P0-2: Duplicate detection** | Reduce double-counting of same root cause | ⚠️ Partial - worked on some tests (Meta subsumed 1 finding), but impact smaller than expected | PARTIAL |
| **Conditional credit halving** | Penalize experimental analyses without validation | ✅ Worked - Vanguard analysis dropped 18 points | SUCCESS (but created dimension imbalance) |
| **P1-1: Worked example credit** | Reward concrete numerical examples | ✅ Worked - fired on Rossmann, Meta, FIV, Message Intent | SUCCESS |
| **P1-2: Honest negative result credit** | Reward reporting failures | ✅ Worked - fired on Rossmann, Message Intent | SUCCESS |
| **P1-3: Tightened quant results criteria** | Prevent bare numbers from earning credit | ✅ Worked - Meta correctly denied credit for "double digit" claim | SUCCESS |
| **P1-4: Formatting -5 → -3** | Reduce over-penalization of polish issues | ⚠️ Too effective - contributed to score inflation | OVER-CORRECTED |
| **P1-5: Headings/chart -3 → -2** | Reduce MINOR deduction severity | ⚠️ Too effective - contributed to score inflation | OVER-CORRECTED |

---

## Convergence Assessment

### Are scores converging toward targets?

**❌ NO — scores diverging ABOVE targets**

- R0: All scores too low (16-29, targets 40-60)
- R1: Over-corrected too high (59-73, targets 40-60)
- R2: Brought down closer to targets (54-71, targets 40-60) — ACCEPTED
- R3: Scores rose again (63-86, targets 40-60) — DIVERGING

**Trajectory:**
```
100 |                                    ● R3 Rossmann (86)
 90 |                               ● R3 FIV (90)
 80 |                          ● R3 Message Intent (85)
 70 |              ● R1      ● R2/R3 Vanguard (69-72)
 60 | [TARGET]    ● R1      ● R2 Rossmann (71)
 50 | [TARGET]    ● R2/R3 Meta (54-63)
 40 | [TARGET]
 30 |    ● R0 Rossmann (29)
 20 |    ● R0 Meta/Vanguard (16-18)
  0 |
     R0        R1         R2         R3
```

Scores are **not converging** — they moved from too low (R0) → too high (R1) → acceptable (R2) → too high again (R3).

### Is differentiation improving?

**✅ YES — differentiation maintained and strengthened**

- R0: 13-point gap (Rossmann 29 vs Vanguard 16)
- R1: 12-point gap (Vanguard 73 vs Meta 59)
- R2: 15-point gap (Rossmann 71 vs Meta 54) — MET TARGET
- R3: 23-point gap (Rossmann 86 vs Meta 63) — EXCEEDS TARGET
- **Extended fixtures:** 37-point gap (Netflix 100 vs Message Intent 85)

Differentiation is strong. The system correctly ranks quality: Netflix (100) > FIV (90) > Rossmann (86) > Message Intent (85) > Vanguard (72) > Meta (63).

### Estimated rounds remaining

**1-2 rounds** if we can identify the correct fix for score inflation.

The system is fundamentally sound:
- Finding quality is good (no spurious CRITICALs, deductions trace to real gaps)
- Differentiation works (scores rank analyses correctly by quality)
- Rubric mechanics work (DR curve, credits, floor rules all functioning)

The only issue is **calibration level**: scores are 15-30 points too high. This is a tuning problem, not an architecture problem.

**Options:**
1. **Conservative fix (1 round):** Reduce credit cap from +25 → +15. Test on R4.
2. **Aggressive fix (1-2 rounds):** Reduce credit cap AND increase 3-5 MAJOR deductions by -2. Test on R4, tune on R5 if needed.
3. **Novel fix (2 rounds):** Add score ceiling compression (scores >85 get DR on credits). Test on R4, debug on R5 if it creates unexpected interactions.

### Risk of oscillation

**⚠️ MODERATE RISK**

Evidence:
- R0 → R1: +44 point jump (Vanguard 16 → 73)
- R1 → R2: -2 to -4 point drop (Vanguard 73 → 69, Rossmann 71 → 71)
- R2 → R3: +3 to +15 point jump (Vanguard 72, Rossmann 86)

The system has oscillated twice (R0 → R1 overcorrection, R2 → R3 overcorrection). We need to avoid a third oscillation in R4.

**Mitigation:** Use a single, well-bounded change (credit cap reduction) rather than multiple interacting changes. Test the change's isolated impact before compounding.

---

## Key Insights

### 1. **Credit additions without deduction offsets create inflation**

R2 → R3 added:
- +2 new credits (worked example, honest negative)
- Reduced 3 deductions (formatting, headings, chart) by -4 to -6 total points

Net effect: More points available, fewer points removed → scores rise.

### 2. **Communication dimension recovered, but Analysis dimension became unstable**

R2 communication was under-scored (48-52). R3 fixed this (61-77).
But R3 introduced Analysis instability: Vanguard Analysis 86 → 68 (-18) due to conditional halving.

The conditional halving rule is correct in principle but creates cross-round incomparability.

### 3. **Extended fixtures reveal rubric bias**

Blog posts scored HIGHER (85-100) than internal analyses (63-86), contrary to expectations.

This suggests:
- The rubric rewards research-quality rigor (systematic comparisons, methodological transparency)
- The rubric does NOT systematically penalize missing business context
- Genre detection (deferred to v0.5) may be needed to calibrate expectations appropriately

### 4. **Floor rule is working but visually confusing**

FIV scored 90 numerically but verdict Major Rework due to 2 CRITICALs. This is mathematically correct but creates cognitive dissonance for users.

Recommendation: Revisit floor rule presentation in v0.5 (either suppress numeric score or show floor-adjusted score).

### 5. **Diminishing returns curve doesn't prevent credit inflation**

DR compresses deductions (to prevent finding spam from over-penalizing).
DR does NOT compress credits (strong analyses accumulate +20-25 credits without compression).

If the goal is to prevent scores above 90, we need either:
- Credit cap reduction (simple)
- Score ceiling compression (complex but comprehensive)

---

## Recommendation for Next Round

**Primary fix:** Reduce credit cap from +25 → +15 per dimension.

**Rationale:**
- Simple, reversible, low-risk
- Directly addresses score inflation (+10 points less per test)
- Preserves differentiation (all scores reduced proportionally)
- Does not require re-tuning other parameters

**Expected R4 scores with credit cap -10:**
- Vanguard: 72 → ~67 (within 40-55 target? Still above, but closer)
- Meta: 63 → ~58 (within adjusted target)
- Rossmann: 86 → ~76 (within 45-60 target? Still above, but closer)
- Blog posts: 85-100 → ~75-90 (closer to targets, differentiation preserved)

**Secondary fix (if R4 still too high):** Increase 2-3 MAJOR deductions by -2 each:
- "Missing baseline/benchmark" -10 → -12
- "Missing TL;DR" -10 → -12
- "Vague recommendation" -8 → -10

This would reduce scores by another -4 to -6 points, bringing Rossmann/Vanguard into target range.
