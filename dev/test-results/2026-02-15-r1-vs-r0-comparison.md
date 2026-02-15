# Calibration Round Comparison: R1 vs R0

**Date:** 2026-02-15

## Score Trajectory

| Document | R0 | R1 | Target | Gap to Target |
|---|---|---|---|---|
| Vanguard | 16 | 73 | 40-55 | +18 over |
| Meta | 18 | 59 | 42-50 | +9 over |
| Rossmann | 29 | 71 | 45-60 | +11 over |

## CRITICAL Count Trajectory

| Document | R0 | R1 | Target |
|---|---|---|---|
| Vanguard | 5 | 0 | ≤2 |
| Meta | 4 | 1 | ≤2 |
| Rossmann | 2 | 0 | ≤2 |

## Finding Count Trajectory

| Document | R0 | R1 | Target |
|---|---|---|---|
| Vanguard | 16 | ~11 | ≤10 |
| Meta | 15 | ~13 | ≤10 |
| Rossmann | 15 | ~13 | ≤10 |

## What Changed Between Rounds

### Fixes Applied in R1

1. Strength credit system (Section 2b) — +25/dimension cap
2. CRITICAL reclassification — 3 communication CRITICALs → MAJOR
3. Diminishing returns curve — 100/50/25 at 30/50 thresholds
4. Severity escalation guard — prevent table violations

### Expected Impact vs Actual Impact

| Fix | Expected Effect | Actual Effect | Assessment |
|---|---|---|---|
| Strength credits | +15-25 for good analyses, +0-5 for weak ones | Vanguard +12, Rossmann +8, Meta +1 (analysis). All low on comms. | **Worked** — differentiates as intended |
| CRITICAL reclassification | Fewer floor rule triggers, less verdict capping | 0 communication CRITICALs across all 3 tests. No floor rules for Vanguard/Rossmann. | **Over-corrected** — went from too many to zero |
| Diminishing returns | Prevent scores from cratering below 20 | Scores landed at 53-88 per dimension instead of 12-39 | **Over-corrected** — prevents scores from reaching 30-50 range too |
| Escalation guard | Prevent severity/deduction mismatches | Zero mismatches in all 3 tests | **Worked** — clean enforcement |

## Convergence Assessment

- **Are scores converging toward targets?** Partially. Direction is correct (R0 too low, R1 higher) but R1 overshot. Scores need to come down 10-18 points.
- **Is differentiation improving?** Yes. R0 gap was 2 points (Vanguard vs Meta). R1 gap is 14 points. Target is 15+. Close.
- **Estimated rounds remaining:** 1-2. The DR curve tightening is a mechanical fix that should land scores in range. If not, credit tuning is the second lever.
- **Risk of oscillation:** Low. The R2 fix (tightening DR from 100/50/25 to 100/70/50) is a partial adjustment, not a reversal. Credits stay unchanged. This should move scores down ~10-15 points without reverting to R0's problems.

## Key Insight

The R1 fixes solved the right problems (differentiation, CRITICAL over-assignment, deduction stacking) but the parameter values were too aggressive. R2 is a tuning exercise, not a redesign. The architecture is working — the numbers just need calibration.
