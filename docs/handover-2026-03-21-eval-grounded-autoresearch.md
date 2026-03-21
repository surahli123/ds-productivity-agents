# Handover: Eval-Grounded AutoResearch for ds-review

**Project:** DS Productivity Agents (`/Users/surahli/ds-productivity-agents`)
**Branch:** feature/autoresearch-ds-review-location-precision
**Date:** 2026-03-21

## Last Session Summary

We analyzed an article about the Three Gulfs framework (Hamel Husain's eval methodology) and designed a plan to integrate it into our autoresearch workflow. We installed Hamel's `evals-skills` plugin (7 skills for error analysis, judge design, judge validation, synthetic data generation, and eval auditing). The plan is approved and saved.

## Current State

- **Plan approved:** `docs/plans/eval-grounded-autoresearch.md` — 7-phase plan
- **Hamel's evals-skills installed:** `evals-skills@hamelsmu-evals-skills` in settings.json. Skills should be available this session.
- **Existing autoresearch:** v2 eval suite with 100% pass rate, but may have blind spots (evals weren't grounded in systematic error analysis)
- **PR #7 still open:** Location precision changes from previous autoresearch run

## Next Steps (Priority Order)

1. **Verify evals-skills loaded** — Check that `error-analysis`, `eval-audit`, `write-judge-prompt`, `validate-evaluator`, `generate-synthetic-data` appear in available skills

2. **Phase 1: Run eval-audit** — Invoke `eval-audit` against our current eval infrastructure:
   - Eval suite: `skills/ds-review/autoresearch-ds-review/eval-suite.md`
   - Results: `skills/ds-review/autoresearch-ds-review/results.json`
   - Changelog: `skills/ds-review/autoresearch-ds-review/changelog.md`
   - Expected: confirms missing error analysis, unvalidated judges, missing labeled data

3. **Phase 2: Start error analysis** — Run `/ds-review` on 20-25 diverse inputs. User must read every output and write failure notes. This is the manual comprehension step — cannot be skipped or automated.

## Key Context

- **Three Gulfs:** Comprehension → Specification → Generalization. Must close in order. AutoResearch only addresses Generalization. We skipped Comprehension.
- **Design decisions:** 20-25 traces (not 100), final output only (not full subagent traces), automated LLM judges (not manual evals)
- **Article reference:** `docs/research/three-gulfs-autoresearch-evals.md`
- **Hamel's skills reference:** `~/.claude/plugins/marketplaces/hamelsmu-evals-skills/skills/`

## Relevant Files to Read First

1. `docs/plans/eval-grounded-autoresearch.md` — the approved plan
2. `skills/ds-review/autoresearch-ds-review/eval-suite.md` — current v2 evals (will be audited)
3. `skills/ds-review/autoresearch-ds-review/changelog.md` — autoresearch history
4. `dev/backlog.md` — updated with 7-phase items
