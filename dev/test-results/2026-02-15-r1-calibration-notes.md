# Scoring Calibration Notes — Round 1

**Date:** 2026-02-15
**Status:** OPEN — Fixes over-corrected, R2 needed
**Prior round:** R0 (`dev/test-results/2026-02-15-calibration-notes.md`)

---

## Score Summary

| # | Document | Type | Score R0 | Score R1 | Delta | CRITICALs | Findings | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Vanguard A/B Test | A/B test (tech/reactive) | 16 | 73 | +57 | 0 | ~11 | Minor Fix |
| 2 | Meta LLM Bug Reports | Blog (exec/proactive) | 18 | 59 | +41 | 1 | ~13 | Major Rework |
| 3 | Rossmann Sales Prediction | Kaggle (mixed/proactive) | 29 | 71 | +42 | ~0 | ~13 | Minor Fix |

### Dimension Scores

| Document | Analysis R0 | Analysis R1 | Comms R0 | Comms R1 |
|---|---|---|---|---|
| Vanguard | 12 | 84 | 19 | 62 |
| Meta | 12 | 62 | 24 | 56 |
| Rossmann | 39 | 88 | 19 | 53 |

## Acceptance Criteria Check

| Criterion | Status | Detail |
|---|---|---|
| Vanguard 40-55 | **FAIL** | Score: 73 (over by 18) |
| Meta in target range (42-50) | **FAIL** | Score: 59 (over by 9) |
| Rossmann 45-60 | **FAIL** | Score: 71 (over by 11) |
| Vanguard analysis > Meta analysis by 5+ | **PASS** | 84 vs 62 = 22 point gap |
| Overall 15+ point differentiation | **FAIL** | Vanguard(73) vs Meta(59) = 14 (1 short) |
| Max 2 CRITICALs per test | **PASS** | Counts: 0, 1, 0 |
| No severity/deduction mismatches | **PASS** | All deductions match SKILL.md table values |
| No cross-cutting duplicates | **PASS** | Each root cause appears in one dimension only |

**Result: 4 FAIL / 4 PASS. Scores over-corrected — all 3 above target ranges.**

## What Improved from Round 0

1. **Differentiation now exists.** R0 had a 2-point gap (Vanguard 16 vs Meta 18). R1 has a 14-point gap (73 vs 59). Direction is correct even if magnitudes are off.

2. **Analysis dimension differentiates strongly.** Vanguard 84, Rossmann 88, Meta 62. The strength credit system correctly rewards real analytical work (experimental design, hypothesis-driven EDA, cross-validation) while giving minimal credit to Meta (no methodology).

3. **CRITICAL count is reasonable.** R0 had 2-5 CRITICALs per test. R1 has 0-1. Only genuinely misleading methodology (Meta's causal claim) gets CRITICAL. Structural communication gaps correctly stay at MAJOR.

4. **Severity escalation guard worked.** No findings show severity/deduction mismatches. The guard prevented the R0 bug where "no named owner" was escalated to CRITICAL.

5. **Verdicts make sense directionally.** Vanguard and Rossmann as Minor Fix, Meta as Major Rework — this matches human judgment about which analyses need more work.

## What Didn't Improve (or Got Worse)

1. **All scores too high.** Every fixture is 9-18 points above its target range. The system went from too harsh to too lenient.

2. **Differentiation gap too narrow.** 14 points (Vanguard vs Meta) — target was 15+. The fixes helped differentiation but the gap between "good work with gaps" and "fundamentally flawed" isn't wide enough.

3. **Communication scores too compressed.** Comms scores are 53, 56, 62 — only a 9-point spread across 3 very different documents. The DR curve is absorbing too much variance in the communication dimension.

## Root Cause Analysis (for remaining problems)

### RC1: DR curve 51+ tier at 25% is too aggressive

The 25% marginal rate above 50 points of deductions absorbs enormous amounts of variance. Rossmann communication had raw -90 deductions compressed to effective -50. That's 40 points of legitimate deductions being discarded. The curve was designed to prevent scores from cratering to near-zero, but it's now preventing scores from reaching the 30-50 range where they should land for weak communication.

**Evidence:**
- Rossmann comms: raw -90 → effective -50. Score 53. Should be ~35-45.
- Meta comms: raw -72 → effective -45.5. Score 56. Should be ~40-50.
- Vanguard comms: raw -64 → effective -43.5. Score 62. Should be ~45-55.

### RC2: Zero communication CRITICALs = no floor rule circuit breaker

In R0, the 2+ CRITICAL floor rule was devastating but served as a circuit breaker for genuinely broken documents. R1 removed ALL communication CRITICALs, so the floor rule never triggers for communication issues. A document with literally no TL;DR, no story arc, and no limitations should probably trigger at least 1 CRITICAL — these are not just "nice to have" for a proactive/exec document.

**Evidence:**
- Vanguard: 0 CRITICALs despite having zero TL;DR and zero limitations section
- Rossmann: 0 CRITICALs despite having zero TL;DR and wrong audience framing

### RC3: Credits + DR compound effect

Both mechanisms push scores higher. For Vanguard analysis: DR saved 0 points (raw deductions only 28) but credits added +12, pushing score from 72 to 84. For Rossmann analysis: DR saved 0 points (raw deductions only 20) but credits added +8, pushing score from 80 to 88. The credits alone pushed analysis scores into the 84-88 range, which may be too generous for documents that still have legitimate gaps.

## Remaining Problems (Ranked by Impact)

1. **DR curve too lenient** — 51+ tier at 25% absorbs too much. All 3 communication scores 10-15 points too high. (~15 points of impact per fixture)
2. **No communication CRITICAL available** — eliminates the floor rule as a severity signal for genuinely absent structural elements (~5-10 points of verdict impact)
3. **Credits may be slightly generous on analysis** — 84 and 88 on analysis for documents with real gaps (no p-values, model selection rationale weak) (~5-8 points)
4. **Differentiation gap 1 point short** — 14 vs target 15. This may self-correct if DR curve is tightened (~1-2 points)

## Proposed Fix Direction (Inputs to R2)

### Primary fix: Tighten DR curve to 100/70/50

| Tier | R1 (current) | Proposed R2 |
|---|---|---|
| 0-30 points | 100% | 100% |
| 31-50 points | 50% | 70% |
| 51+ points | 25% | 50% |

Projected impact:
- Rossmann comms: -90 raw → -65 effective (was -50). Score: 38 (was 53). ✓ In range.
- Meta comms: -72 raw → -51 effective (was -45.5). Score: 50 (was 56). ✓ In range.
- Vanguard comms: -64 raw → -47 effective (was -43.5). Score: 58 (was 62). ✓ Closer to range.

### Secondary fix: Add "TL;DR completely absent" CRITICAL (-12)

Only fires when there is literally no summary anywhere. Distinct from "ineffective TL;DR" (MAJOR -10). Triggers floor rule (Minor Fix cap) when combined with 1+ other CRITICAL.

### Leave credits unchanged

Credits are doing their primary job (differentiation). The over-scoring is primarily from DR, not credits.

### DECISION NEEDED (Owner)

1. **DR curve values:** Accept 100/70/50 proposal, or suggest different values?
2. **Add back "TL;DR absent" CRITICAL?** Yes (adds floor rule pressure) or no (keep it simple)?
3. **Adjust credit values?** Leave as-is (recommended) or reduce?
