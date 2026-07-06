# Pickup: Phase 2 Error Analysis (12/22 traces done)

Project: /Users/surahli/ds-productivity-agents
Branch: feature/autoresearch-ds-review-location-precision

Last session: Completed Phase 1 (eval-audit) and collected 12/22 Phase 2
error analysis traces. User annotated all 12. Three failure modes discovered.
Paused to test with autorefine v2.

Read first:
1. docs/plans/eval-grounded-autoresearch.md — the approved 7-phase plan
2. skills/ds-review/autoresearch-ds-review/error-analysis-traces.md — trace log with annotations
3. skills/ds-review/autoresearch-ds-review/eval-audit-report.md — Phase 1 output
4. dev/backlog.md — updated with Phase 1-2 progress

## Current state

Phase 1 (eval-audit): COMPLETE — 7 findings, report written.
Phase 2 (error analysis): 12/22 traces annotated.
- Batch 1 (5 traces): All annotated. T-01/T-02/T-03/T-04 Pass, T-05 FAIL.
- Batch 2 (7 traces): T-06 annotated (FAIL — too harsh). T-07 through T-12 presented but NOT yet annotated by user.
- Batch 3 (10 traces): Not started.

## Failure modes discovered (3 + 1 meta-pattern)

1. **Missing narrative synthesis not caught** (T-05)
   - Review flags individual structural issues but doesn't recognize when they
     compound into a fundamental lack of narrative
   - Gave 83/100 Good to Go for a document that is a data dump without narrative

2. **Wrong rubric for document type** (T-06)
   - Review applies empirical analysis standards (causal methodology, baselines)
     to a system description blog post
   - 62/100 Major Rework is too harsh for a doc that's describing what was built,
     not presenting an A/B test

3. **Score inflation** (soft pattern, T-01/T-02/T-03/T-04)
   - Scores tend to run slightly high

4. **Meta-pattern: Document-type awareness gap** (FM1 + FM2)
   - The review doesn't understand what kind of document it's evaluating
   - Like using the same relevance criteria for navigational vs informational queries

## Next steps (in priority order)

1. **Finish Batch 2 annotations** — User needs to Pass/Fail T-07 through T-12
2. **Collect Batch 3 traces** (10 remaining fixtures) and annotate
3. **Build failure taxonomy** — Group all failure notes into 5-10 categories
   (error-analysis methodology says start grouping after ~15 annotated traces)
4. **Decide fix vs evaluate per category** — Some failures can be fixed directly
   in SKILL.md, others need automated judges
5. **Phase 3+** — Expand inputs, write judges, validate, run autoresearch

## Key context for autorefine v2

- The 3 failure modes discovered here are the REAL evaluation criteria that
  autorefine v2 should optimize against — not the v2 eval suite (which the
  eval-audit showed has blind spots)
- The narrative quality instruction added to Batch 2 agents worked — agents
  consistently flagged narrative gaps. This instruction should be formalized
  in SKILL.md
- Inline execution (used for all 12 traces) produces higher-quality output
  than dispatched subagents — eval results may not transfer to production
- The autorefine skill at ~/.claude/skills/autorefine/ was validated on
  ds-trace (36%→89%, 8/8 keeps) — ready for v2 integration with these
  error-analysis-grounded evals

## Batch 2 traces awaiting annotation

| Trace | Fixture | Score | Verdict |
|-------|---------|-------|---------|
| T-07 | meta-llm-product-analytics | 60 | Major Rework |
| T-08 | meta-asymmetric-experiments | 82 | Good to Go |
| T-09 | capstone-customer-churn | 53 | Major Rework |
| T-10 | kaggle-house-prices-eda | 62 | Major Rework |
| T-11 | kaggle-titanic-solutions | 56 | Major Rework |
| T-12 | atlassian-rovo-search | 62 | Minor Fix |

Also saved at dev/sessions/2026-03-22-phase1-2-error-analysis.md (local only, gitignored).
