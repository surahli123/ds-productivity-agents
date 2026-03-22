# Eval Audit Report: ds-review v2 Eval Suite

**Date:** 2026-03-21
**Audited by:** eval-audit methodology (Hamel Husain's framework)
**Scope:** v2 binary eval suite, autoresearch infrastructure, test fixtures

---

## Summary

The v2 eval suite has good structural foundations (binary evals, specific failure modes for most evals) but critical gaps in grounding: no systematic error analysis, no judge validation, and insufficient labeled data. The 100% score is likely an artifact of measuring a narrow slice of quality rather than evidence of actual comprehensiveness.

**Priority order for remediation:**
1. Error analysis on real traces (Gulf of Comprehension — blocks everything else)
2. Expand labeled data via trace collection + synthetic generation
3. Write and validate automated judges grounded in observed failure modes
4. Re-audit after pipeline changes

---

## Diagnostic Findings

### 1. Error Analysis

#### 1a. No Systematic Error Analysis
**Status:** Problem exists
The 5 eval criteria were selected through brainstorming and ad hoc testing, not by systematically reading traces and cataloging failures. The evals target reasonable quality dimensions (location precision, fix actionability, finding correctness, dimension balance, severity calibration), but these were chosen based on what *seemed* important during calibration rounds, not what was *observed* to fail in practice.

**Evidence:** The changelog shows Experiment 0 baseline (96%), then 2 targeted mutations — both focused on location precision, which was noticed during manual testing. No record of systematic trace review that led to the eval categories.

**Impact:** HIGH — The eval suite may be missing failure modes that are frequent in practice but weren't anticipated during brainstorming. Classic case of "measuring what you thought to measure, not what matters."

**Fix:** Run `error-analysis` on 20-25 diverse traces. Let failure categories emerge from observation. → **Phase 2 of our plan.**

#### 1b. Failure Categories Were Brainstormed, Not Observed
**Status:** Problem exists
The eval categories read like generic quality dimensions: "location precision," "fix actionability," "finding correctness." While E1 (location precision) turned out to be grounded — it was discovered through actual failures during testing — the others show signs of brainstorming: E2 (actionability) and E3 (correctness) are broad enough to pass most outputs, and E4 (dimension balance) uses hardcoded thresholds for specific fixtures rather than a generalizable criterion.

**Evidence:**
- E4 (Dimension Balance) encodes fixture-specific expectations: "Fixture 5: Analysis score ≥ Communication + 30" — this tests ONE specific fixture's expected pattern, not a generalizable failure mode.
- E3 (Finding Correctness) says "each finding can be verified by reading the source" — this is holistic quality, not a specific failure mode. What KIND of correctness errors occur? Hallucinated sections? Misattributed claims? Wrong severity? These are different failure modes with different fixes.

**Fix:** Decompose broad evals (E3, E4) into specific, observed failure modes after error analysis. → **Phase 4.**

---

### 2. Evaluator Design

#### 2a. Evals Are Binary — Good
**Status:** OK
All 5 evals use binary Pass/Fail with explicit definitions. This is correct practice — avoids the Likert scale calibration problem.

#### 2b. Some Evals Are Too Holistic
**Status:** Problem exists
E2 (Fix Actionability + Impact) and E3 (Finding Correctness) each bundle multiple failure modes into one eval. E2 checks both "concrete action" AND "why it matters" — these are independent failure modes. A fix could be specific but miss the impact, or explain the impact but be vague on the action. Bundling them means a single Fail verdict doesn't tell you which problem occurred.

E3 is the most holistic: "each finding can be verified by reading the source." This is really 3+ distinct checks:
- Does the cited section exist? (hallucination)
- Is the quoted claim accurate? (misattribution)
- Is the identified gap real? (false positive)

**Fix:** After error analysis reveals which correctness failures actually occur, split E3 into specific judges per failure mode. Some (e.g., "cited section exists") could be code-based checks. → **Phases 2 and 4.**

#### 2c. Code-Based Checks Underused
**Status:** Problem exists
E1 (Location Precision) checks for banned phrases like "throughout" and "entire document." This is a regex/keyword check — no LLM judge needed. Currently evaluated by an LLM scorer, which adds cost and non-determinism for an objectively checkable criterion.

E4's score arithmetic (Analysis ≥ Communication + 30) is also pure math — no judge needed.

**Fix:** Convert E1 and E4 to code-based checks during judge construction. → **Phase 4.**

---

### 3. Judge Validation

#### 3a. No Judge Validation
**Status:** Problem exists (CRITICAL)
No LLM judges exist yet (evals are run by the autoresearch scorer reading outputs). When we build automated judges in Phase 4, they will need validation. Currently: zero confusion matrices, zero TPR/TNR measurements, zero alignment data.

**Fix:** Build golden dataset with human labels, validate judges with TPR/TNR > 90% on held-out test set. → **Phase 5.**

#### 3b. No Train/Dev/Test Split
**Status:** Problem exists
The 5 fixtures serve as both the development set (used to iterate during autoresearch) and the test set (used to measure final performance). The 100% score was achieved by iterating on these same 5 fixtures — classic train-test leakage.

**Evidence:** Changelog shows E2 100% was reached after 2 mutations, both tested against the same 5 fixtures. No held-out data exists to verify the mutations generalize.

**Fix:** Expand to ~30+ fixtures. Split into train (few-shot examples for judges), dev (iteration), and test (final measurement). → **Phases 3 and 5.**

---

### 4. Human Review Process

#### 4a. Ad Hoc Review Without Structured Process
**Status:** Problem exists
Human review happened during calibration rounds (R1-R4) with role-based review personas (DS Lead, PM Lead, Principal AI Engineer). These reviews were thorough but ad hoc — different fixtures in each round, different focus areas, no systematic coverage of all failure modes across all fixtures.

**Evidence:** Backlog shows R1-R4 calibration with 6 fixtures, but reviewers focused on different aspects in each round (severity calibration, credit inflation, dimension balance). No single systematic pass through all outputs looking for ALL failure types.

**Fix:** Error analysis (Phase 2) provides the systematic human review process. User reads every output, judges Pass/Fail, and notes what went wrong — no pre-defined categories.

#### 4b. Output-Only Review
**Status:** Acceptable for this use case
The plan calls for reviewing final outputs only, not subagent traces. This is deliberate — the consumer sees only the final review output. Digging into subagent traces is reserved for cases where the root cause of a final-output failure is unclear.

**Rationale in plan:** "Reading all 4 outputs (3 subagents + synthesis) for 20+ traces is too much. Final output is what the consumer sees."

**Status:** OK — intentional design decision, not an oversight.

---

### 5. Labeled Data

#### 5a. Insufficient Labeled Data
**Status:** Problem exists (CRITICAL)
The eval suite uses 5 fixtures. Total labeled data points: 5 fixtures × 5 evals = 25 binary labels. This is far below the ~100 traces needed for error analysis saturation and the ~50 Pass + 50 Fail examples needed for judge validation.

**Evidence:**
- 28 fixtures exist but only 5 are used in evals
- No labeled dataset beyond the 25 eval scores
- No failure rate computation possible with this sample

**Fix:** Collect 20-25 traces for error analysis (Phase 2), expand to ~30 fixtures with synthetic data (Phase 3), build golden dataset with ~50+ labeled traces for judge validation (Phase 5).

#### 5b. No Sampling Strategy
**Status:** Problem exists
The 5 eval fixtures were selected for convenience and to cover known edge cases (prescriptive guide, good-analysis-bad-comms). No systematic sampling across dimensions like document type, domain, quality level, length, or audience.

**Evidence:** All 5 fixtures are in "full mode" — no quick mode coverage. 2 are search-domain, 2 are synthetic, 1 is a general A/B test. Missing: non-DS domain, very short docs, Kaggle notebooks, Meta engineering blog posts.

**Fix:** Use `generate-synthetic-data` dimensions to systematically cover the input space. → **Phase 3.**

---

### 6. Pipeline Hygiene

#### 6a. Evals Not Re-Run After Mutations
**Status:** Problem exists (minor)
The eval suite was written before the location precision mutation was applied to production SKILL.md. The 100% score reflects the optimized SKILL.md, but the evals themselves weren't re-validated against the new prompt — they were designed to test the pre-mutation prompt's weaknesses.

**Evidence:** Eval suite says "Baseline (Experiment 0): 21/25 (84%)" but the current SKILL.md has already absorbed both mutations. The evals now test a skill that was specifically tuned to pass them.

**Fix:** This is a minor concern since we're about to replace the eval suite entirely. The new judges (Phase 4-5) will be built from fresh error analysis.

#### 6b. No Evaluator Maintenance Process
**Status:** Problem exists
No process for re-running error analysis after skill mutations, model changes, or fixture updates. The eval suite is "set and forget."

**Fix:** Add to session-end protocol: re-audit after significant pipeline changes. Document in `autoresearch-ds-review/` README.

---

## What's Working

These aspects of the current eval infrastructure are sound and should carry forward:

1. **Binary evals** — All 5 use Pass/Fail with explicit definitions. This is correct.
2. **Specific failure modes for E1 and E5** — Location precision (E1) and severity inflation (E5) target real, observed issues. These may survive as judges.
3. **Fixture diversity** — 28 fixtures exist across real, synthetic, and varied domains. The raw material for Phase 2-3 is already here.
4. **Autoresearch infrastructure** — Changelog format, mutation-test-keep/discard cycle, and per-fixture result tables are reusable.
5. **Calibration history** — R1-R4 calibration rounds produced valuable reference scores that can benchmark new judges.

---

## Remediation Priority

| # | Gap | Impact | Fix | Phase |
|---|-----|--------|-----|-------|
| 1 | No systematic error analysis | Evals may miss real failure modes | Run error-analysis on 20-25 traces | **Phase 2** |
| 2 | Insufficient labeled data (25 points) | Can't validate judges or compute failure rates | Collect 20-25 traces + expand to ~30 fixtures | **Phases 2-3** |
| 3 | No judge validation | Can't trust automated eval results | Build golden dataset, validate TPR/TNR > 90% | **Phase 5** |
| 4 | Train/test leakage (5 fixtures used for both) | 100% score is inflated | Split into train/dev/test after expansion | **Phase 5** |
| 5 | Holistic evals (E2, E3) bundling failure modes | Fails don't diagnose which sub-problem occurred | Decompose into specific judges after error analysis | **Phase 4** |
| 6 | Code-based checks underused (E1, E4) | LLM judges used for objective criteria | Convert to regex/arithmetic checks | **Phase 4** |
| 7 | No evaluator maintenance process | Evals drift after pipeline changes | Add re-audit protocol to session-end | **Post-Phase 7** |

---

## Next Step

**Phase 2: Error Analysis.** Run `/ds-review` on 20-25 diverse inputs. User reads every output, judges Pass/Fail, and notes what went wrong. Let failure categories emerge from observation — do NOT use the 5 existing eval categories as a starting taxonomy. Fresh eyes, fresh categories.
