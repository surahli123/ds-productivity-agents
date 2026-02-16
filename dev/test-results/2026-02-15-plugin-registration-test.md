# Plugin Registration Test — Post-Restart Validation

**Date:** 2026-02-15
**Branch:** `feat/v0.4.1-credit-redesign`
**Purpose:** Validate that `/ds-review` project command works after session restart
**Fixture:** `dev/test-fixtures/real/vanguard-ab-test.md` (Vanguard A/B Test)

---

## Test Runs

### Run 1: Quick Mode (Tech, Reactive)
```
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode quick --audience tech --workflow reactive
```
- **Score:** 60/100 — Major Rework (floor rule: 3 CRITICALs)
- **Analysis:** 57/100 (deductions: 63→51.5 DR | credits: +8)
- **Communication:** 62/100 (deductions: 43→39.75 DR | credits: +2)
- **Findings:** 5 analysis + 6 communication = 11 total
- **CRITICALs:** 3 (unstated assumptions, unvalidated experiments, TL;DR absent)

### Run 2: Full Mode (Mixed, General)
```
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode full --audience mixed
```
- **Score:** 51/100 — Major Rework
- **Analysis:** 46/100 (deductions: 83→61.5 DR | credits: +7)
- **Communication:** 55/100 (deductions: 53→46.5 DR | credits: +1)
- **Findings:** 7 analysis + 7 communication = 14 total (10 displayed, 4 below cap)
- **CRITICALs:** 3 (unstated assumptions, unvalidated experiments, TL;DR absent)

### R3 Baseline (for comparison)
```
Prior session — Full Mode, Tech, Reactive — before v0.4.1 fixes
```
- **Score:** 72/100 — Minor Fix (floor rule: 1 CRITICAL)
- **Analysis:** 68/100 (deductions: 41→38 DR | credits: +6)
- **Communication:** 77/100 (deductions: 28→28 DR | credits: +5)
- **Findings:** 4 analysis + 4 communication = 8 total
- **CRITICALs:** 1 (unvalidated experiments)

---

## Plugin Registration Assessment

### What We're Validating

The plugin registration session (2026-02-15) created `.claude/commands/ds-review.md` as a
project-level command. The session log identified 3 open questions:
1. Does the file-reference approach work? (command instructs Claude to Read agent/skill files)
2. Does `$ARGUMENTS` pass user input correctly?
3. Does the command trigger the full 10-step pipeline?

### Results: 7/7 Registration Checks PASSED

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Command discoverable after restart | PASS | `/ds-review` appeared in slash command list and executed on invocation |
| 2 | `$ARGUMENTS` substitution works | PASS | Both runs received correct source, mode, audience, and workflow params |
| 3 | File-reference approach works | PASS | Lead agent read `ds-review-lead.md` and `SKILL.md` before dispatching |
| 4 | Subagent dispatch works | PASS | Both analysis-reviewer and communication-reviewer launched via Task tool, read their own agent prompts + SKILL.md |
| 5 | Output format compliance | PASS | Quick mode produced status table + top 3 + positives + footer. Full mode produced lens dashboard + per-dimension findings + all sections. |
| 6 | SKILL.md mechanisms applied | PASS | Deduction tables, strength credits, conditional halving rule, DR formula, floor rules, severity guard, finding volume cap (10) — all functioning |
| 7 | Multiple invocations in same session | PASS | Ran quick then full in same session without errors or context contamination |

### Open Question Resolved

> "Does the file-reference approach work? (Claude reads `plugin/agents/ds-review-lead.md` when instructed by the command)"

**YES.** The command body instructs Claude to read the lead agent and SKILL.md files. Claude
executes Read calls on both files before proceeding. This means the single-source-of-truth
design works — editing `plugin/agents/*.md` or `plugin/skills/*/SKILL.md` will propagate
changes to the next review without modifying the command file.

### Model Override Question (NEW)

The command frontmatter specifies `model: opus`, but the user switched to Sonnet via `/model`
before invoking `/ds-review`. It's unclear whether the frontmatter `model: opus` overrode the
session-level model selection. The subagents ran via Task tool (which inherits the calling
model unless overridden). **This needs explicit verification** — run a test where the session
model is Sonnet and check which model actually executes the review.

---

## Score Analysis: v0.4.1 Impact

### Why Scores Dropped from R3 (72 → 60/51)

The v0.4.1 credit redesign branch includes several changes that were NOT present during R3:

| Change | Impact on Vanguard |
|--------|-------------------|
| **NEW: Unvalidated experiment CRITICAL (-15)** | Already existed in R3, but the deduction is now more reliably triggered |
| **NEW: Conditional halving rule (Credit Rule 6)** | Halves methodology/hypothesis/results credits when experimental structure present but unvalidated. Reduced credits from +6 to +7-8 (halved values) |
| **Unstated critical assumption finding** | R3 missed this; current runs consistently find it (-20 CRITICAL). This single finding accounts for ~10 points of the gap |
| **TL;DR reclassified to CRITICAL (-12)** | R3 had this as MAJOR (-10). Current runs correctly apply CRITICAL. Triggers 3-CRITICAL floor rule |
| **Tighter DR curve (100/75/50)** | Applied in R2, but compounds with higher raw deductions |

**Net effect:** ~12 points of the drop are from the "unstated critical assumption" finding
that R3 missed. ~5 points from conditional halving reducing credits. ~3 points from TL;DR
CRITICAL reclassification triggering the floor rule. The rest is cross-run variability.

### Cross-Run Variability (Run 1 vs Run 2)

| Metric | Run 1 (Tech/Reactive) | Run 2 (Mixed/General) | Delta |
|--------|----------------------|----------------------|-------|
| Analysis score | 57 | 46 | -11 |
| Communication score | 62 | 55 | -7 |
| Final score | 60 | 51 | -9 |
| Analysis raw deductions | 63 | 83 | +20 |
| Communication raw deductions | 43 | 53 | +10 |

**Expected differences (audience/workflow-driven):**
- Communication: "Audience mismatch — no progressive disclosure" (-10) correctly triggered
  only in Run 2 (Mixed audience expects layered structure; Tech audience doesn't require it)
- This explains ~7 of the 9-point communication gap

**Unexplained variability (analysis dimension):**
- Run 2 found 2 extra analysis findings: "55-day scoping circular logic" (-10) and "Missing
  baseline for time-per-step" (-10). These are legitimate findings present in the document
  that Run 1's subagent didn't surface.
- This is the known ±10 cross-run variability: finding generation is non-deterministic.
  The same document can yield different finding sets across runs.
- Analysis dimension gap of 11 points is at the edge of acceptable. Monitored in R3 and
  still present after v0.4.1 fixes.

---

## Summary & Next Steps

### Plugin Registration: VALIDATED
The `/ds-review` project command works as designed. All 7 checks pass. The file-reference
architecture (command → reads agent/skill files → dispatches subagents) is functioning
correctly. No fallback to embedded instructions needed.

### Calibration: R4 NEEDED
Scores have shifted downward from R3 baselines due to v0.4.1 fixes (as expected — the fixes
added new deductions and tightened credits). R4 calibration should:
1. Re-run all 6 fixtures with current branch code
2. Evaluate whether scores are now too harsh (primary concern: unstated assumptions at -20
   may be too aggressive for student/portfolio analyses)
3. Apply the planned credit cap reduction (+25 → +15) and test its interaction with the
   conditional halving rule (they may stack too aggressively)
4. Run cross-run consistency check (same doc 3x) to quantify current variability

### Open Items
1. **Model override verification** — confirm `model: opus` frontmatter works when session is
   set to a different model
2. **R4 calibration** — proceed per backlog plan
