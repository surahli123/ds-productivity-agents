# Handoff: Claude Code → Claude Web Session

**Date:** 2026-02-15
**Purpose:** Let Claude Web independently evaluate the scoring rubric while Claude Code executes calibration rounds.

---

## What This Project Is

A Claude Code plugin that reviews DS analyses across two dimensions:
- **Analysis:** methodology, logic, completeness, metrics (4 lenses)
- **Communication:** structure/TL;DR, audience fit, conciseness, actionability (4 lenses)

The system uses a lead orchestrator agent that dispatches two specialized reviewer subagents in parallel, synthesizes their outputs, and produces a unified review with a score out of 100.

---

## What Just Happened (v0.4 Calibration Sprint)

### The Problem

The scoring system couldn't differentiate quality. Three real-world tests produced:

| Document | Type | Score | Verdict |
|----------|------|-------|---------|
| Meta LLM Bug Reports | Blog post (exec/proactive) | 18/100 | Major Rework |
| Rossmann Sales Prediction | Kaggle project (mixed/proactive) | 29/100 | Major Rework |
| Vanguard A/B Test | Real experiment (tech/reactive) | 16/100 | Major Rework |

**Vanguard scored LOWER than Meta** despite having real experimental design, pre-specified hypotheses, covariate balance checks, and specific quantitative results. The system only counted what was missing, never what was present.

### Root Causes (Consensus from 3 Role Reviews)

1. **No strength credits** — scoring is purely subtractive (100 minus deductions). Good analytical practices earn zero points.
2. **Deduction stacking** — 15 findings at -8 to -20 each drives any real analysis to near-zero.
3. **CRITICAL over-assignment** — structural communication gaps (missing TL;DR, no story arc, no limitations section) were CRITICAL, triggering floor rules that capped verdicts.
4. **Teardown-style output** — the review reads like a destruction, not helpful feedback.

### Three Expert Role Reviews Conducted

Each reviewed the same test outputs from different perspectives:

1. **Principal AI Engineer** (`dev/reviews/2026-02-15-principal-ai-engineer-assessment.md`)
   - Focus: scoring math, formula behavior, implementation correctness
   - Key insight: diminishing returns formula needed as safety net

2. **PM Lead** (`dev/reviews/2026-02-15-pm-lead-calibration-review.md`)
   - Focus: user experience, output quality, trustworthiness
   - Key insight: strength credits (+15/dim), output restructure needed

3. **DS Lead** (`dev/test-results/2026-02-15-ds-lead-assessment.md`)
   - Focus: finding quality, whether each finding is legitimate
   - Key insight: strength credits (+25/dim), cap findings at 8, finding-by-finding audit showed 5 agree / 4 partial / 6 disagree with the agent's findings

### Owner Decisions (5 Resolved)

| # | Decision | Choice |
|---|----------|--------|
| 1 | Strength credit cap | +25 per dimension |
| 2 | Meta target score | 42-50 (Minor Fix) |
| 3 | Finding volume cap | Cap at 10, defer to Phase 2 |
| 4 | Severity escalation bug | Fix — prevent escalation beyond table |
| 5 | Diminishing returns | Yes, include in Phase 1 |

---

## What Was Implemented (Round 1 Fixes)

### Fix 1: Strength Credit System (new SKILL.md Section 2b)

Subagents now award credits for demonstrated good practices. Cap: +25/dimension.

**Analysis credits:** Real experimental design (+8), pre-specified hypotheses (+5), success threshold (+3), covariate check (+3), specific quantitative results (+3), external validation (+3), sensitivity check (+3), reproducibility detail (+2). Max possible: +30, capped at +25.

**Communication credits:** Effective TL;DR (+5), story arc matches audience (+5), audience-calibrated detail (+3), actionable recommendations with owners (+5), clear limitations (+3), effective visualization (+3), progressive disclosure (+3), professional polish (+2). Max possible: +29, capped at +25.

**Why this matters:** Vanguard should earn ~20-25 analysis credits (experiment, hypotheses, balance check, specific results). Meta earns ~0-5. This is the primary differentiator.

### Fix 2: CRITICAL Reclassification (SKILL.md Section 2)

Three structural communication findings downgraded:

| Finding | Before | After |
|---------|--------|-------|
| Missing/ineffective TL;DR | CRITICAL (-15) | MAJOR (-10) |
| No clear story arc | CRITICAL (-12) | MAJOR (-8) |
| Limitations/scope unclear | CRITICAL (-12) | MAJOR (-10) |

**Consequence:** Communication dimension now has ZERO CRITICAL entries. Only analysis CRITICALs (wrong methodology, flawed stats, broken evidence chain) trigger floor rules. Structural gaps are significant but don't "cause wrong conclusions."

### Fix 3: Diminishing Returns (ds-review-lead Step 9)

Raw deductions are compressed before scoring:
- First 30 points: 100% applied
- Points 31-50: 50% of marginal deductions
- Points 51+: 25% of marginal deductions

Example: raw -88 → effective -50 (instead of -88). Prevents any real analysis from scoring near zero.

### Fix 4: Severity Escalation Guard (SKILL.md Section 2)

New rule: subagents MUST use exact severity/deduction values from the table. Cannot escalate MINOR to MAJOR or MAJOR to CRITICAL based on context. Prevents the bug where "no named owner" (MINOR -5) got escalated to CRITICAL in proactive workflow.

### Scoring Formula (New)

```
dimension_score = 100 - effective_deductions(DR) + credits(capped at 25)
final_score = (analysis_score + communication_score) / 2
```

---

## Files to Review

### Architecture & Design
- `docs/plans/2026-02-14-architecture-design.md` — Architecture doc (Rev 4)
- `docs/plans/2026-02-14-implementation-plan.md` — Implementation plan (Rev 3)
- `dev/specs/PRD-DS-Analysis-Review-Agent.md` — PRD

### Current Implementation (Post-Fixes)
- `plugin/skills/ds-review-framework/SKILL.md` — Shared rubrics (now ~260 lines, 9 sections including 2b)
- `plugin/agents/ds-review-lead.md` — Lead orchestrator (10-step pipeline)
- `plugin/agents/analysis-reviewer.md` — Analysis subagent (4 lenses)
- `plugin/agents/communication-reviewer.md` — Communication subagent (4 lenses)

### Calibration Evidence
- `dev/test-results/2026-02-15-calibration-notes.md` — Root cause analysis from 3 real-world tests
- `dev/reviews/2026-02-15-principal-ai-engineer-assessment.md` — Engineer role review
- `dev/reviews/2026-02-15-pm-lead-calibration-review.md` — PM role review
- `dev/test-results/2026-02-15-ds-lead-assessment.md` — DS Lead role review
- `dev/test-results/2026-02-15-meta-llm-bug-reports-review.md` — R0 Meta review output
- `dev/test-results/2026-02-15-vanguard-ab-test-full-review.md` — R0 Vanguard review output

### Calibration Loop
- `docs/plans/2026-02-15-calibration-loop-workflow.md` — Iterative 8-task loop design
- `dev/test-results/2026-02-15-r1-*-review.md` — Round 1 test results (being generated now)

---

## What We Want From Web Session

1. **Independently review the scoring rubric** (SKILL.md) — are the deduction values reasonable? Are the credit values balanced? Are there missing issue types or missing strength indicators?

2. **Review 4 company blog analyses** (Meta, Airbnb, Udemy) and mentally score them — what would a fair score look like? Where would our rubric get it right vs. wrong?

3. **Propose critiques** for the scoring rubric based on those independent evaluations. Especially:
   - Are there common patterns in company blogs that our rubric doesn't handle well?
   - Should the credit system have different values?
   - Should any deductions be adjusted?
   - Are there missing lenses or blind spots?

4. **Evaluate the architecture** — does the two-dimension split (analysis + communication) make sense? Is the 50/50 weighting right? Does the orchestrator design hold up?

Feed findings back to the owner, who will bring them into the next Claude Code session for implementation.

---

## Key Design Decisions Still Open

- **Genre/format awareness** — deferred to v0.5. Blog posts, Kaggle notebooks, and internal analyses all evaluated against the same rubric. May need a `--format` flag.
- **Finding volume cap** — approved at 10, deferred to Phase 2.
- **Output restructure** — approved (move strengths before findings, compress per-lens detail, add emoji indicators), deferred to Phase 2.
- **Communication CRITICALs** — currently zero in the table. May need to add one back if testing shows genuinely misleading communication patterns getting off easy.
