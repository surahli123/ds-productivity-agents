# ADR-003: Scoring Calibration Approach

**Date:** 2026-02-15
**Status:** Accepted

## Context

v0.3 scoring produced 16-29/100 on real-world DS analyses that experts would rate 40-65.
The system had no quality differentiation — Vanguard (a well-designed A/B test) scored 16
while Meta (a blog post with no methodology) scored 18. Three independent assessments
(Principal AI Engineer, PM Lead, DS Lead) diagnosed the root causes and proposed fixes.

## Problem

Four root causes identified across all three assessments:

1. **No strength credits:** Good analytical work (experimental design, hypothesis testing)
   had zero impact on score. Only deductions counted.
2. **Deduction stacking:** 15+ findings with additive deductions compressed all scores
   below 30, regardless of document quality.
3. **CRITICAL over-assignment:** Structural communication gaps (missing TL;DR, no story arc)
   were classified as CRITICAL, triggering floor rules inappropriately.
4. **No diminishing returns:** Each additional finding deducted at full value, so the 10th
   MINOR issue had the same marginal impact as the 1st MAJOR issue.

## Decision

Implement a 4-component calibration system:

### 1. Strength Credit Table (SKILL.md Section 2b)
- 8 analysis credits (+2 to +8 each) for demonstrated good practices
- 8 communication credits (+2 to +5 each) for effective communication
- Cap: +25 per dimension (prevents credit inflation)
- Evidence required: only credit what's demonstrably in the document

### 2. CRITICAL Reclassification
- 3 communication CRITICALs demoted to MAJOR: missing TL;DR, no story arc, limitations absent
- 1 communication CRITICAL retained: "TL;DR completely absent" (-12) — fires only when
  there is literally no summary anywhere in the document
- Analysis CRITICALs unchanged (3 entries: unstated assumption, flawed methodology,
  conclusion doesn't trace)

### 3. Diminishing Returns Curve
- First 30 points of deductions: 100% (full impact)
- Points 31-50: 75% (slightly reduced marginal impact)
- Points 51+: 50% (heavy compression for extreme deduction totals)
- Applied by lead agent during synthesis (Step 9), not by subagents

### 4. Severity Escalation Guard
- Subagents must use exact severity and deduction values from the deduction table
- No context-based escalation (MINOR stays MINOR regardless of audience or workflow)
- The table is the source of truth — no exceptions

## Calibration Process

Used an iterative fix-test-diagnose loop:

- **R0 (baseline):** Scores 16-29, 2-5 CRITICALs per test, no differentiation
- **R1 (initial fix):** Over-corrected to 59-73. DR curve (100/50/25) too aggressive,
  zero communication CRITICALs removed all floor rule pressure
- **R2 (tuning):** Tightened DR to 100/75/50, added back "TL;DR absent" CRITICAL.
  Scores: 54-71 with 15-point differentiation gap. Accepted by owner.

## Alternatives Considered

1. **Cluster-based scoring** (Engineer proposal): Group correlated findings, deduct once
   per cluster. Deferred to v1.5 — requires finding-level dependency tracking.
2. **Per-dimension deduction cap at -70** (calibration notes): Made redundant by
   diminishing returns — DR naturally caps effective deductions.
3. **CRITICAL-ABSENT vs CRITICAL-INCOMPLETE gradation** (calibration notes): Added
   complexity without clear benefit. Simple reclassification achieved the same goal.
4. **DR curve at 100/70/50** (R1 diagnosis recommendation): Owner chose gentler 100/75/50
   to avoid over-correcting in the other direction.

## Consequences

- Scores now differentiate correctly: Vanguard (real experiment) scores 15+ points above
  Meta (blog post with no methodology)
- Verdicts match human judgment: Vanguard/Rossmann = Minor Fix, Meta = Major Rework
- Analysis dimension correctly rewards methodological rigor (86-93 for strong work)
- Communication dimension still has room to penalize weak structure (48-52 range)
- Extended validation needed: untested fixtures, cross-run consistency, synthetic rerun
- Finding volume cap (10 max) deferred to Phase 2 — scoring calibration is the priority
