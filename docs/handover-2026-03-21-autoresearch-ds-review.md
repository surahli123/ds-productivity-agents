# Handover: Autoresearch on ds-review — Location Precision

## Project
- **Path:** `/Users/surahli/ds-productivity-agents`
- **Branch:** `feature/autoresearch-ds-review-location-precision` (PR #7 open, targeting main)
- **Repo:** https://github.com/surahli123/ds-productivity-agents

## Last Session (2026-03-21)
Ran autoresearch optimization loop on the ds-review skill (analysis review orchestrator). Designed IC9-quality binary evals, ran 2 experiments across 7 test fixtures, improved from 85.7% to 100% pass rate. Code review caught a placement blocker (rule only in orchestrator, not subagent prompts) — fixed before shipping. PR #7 created with 25 insertions across 4 files.

## Current State
- **PR #7 is open** — `feature/autoresearch-ds-review-location-precision` → main (4 files, +25/-3)
- **PR #6 is still open** — `feature/v0.7-ds-trace-skill` → main (39 files, ds-trace skill)
- **Autoresearch working dir** at `skills/ds-review/autoresearch-ds-review/` — not committed, contains dashboard/results/changelog
- **3 new learnings added to CLAUDE.md** — autoresearch eval design, user problem > persona opinion, inline ≠ production

## Next Steps (Priority Order)
1. **Merge PR #6** (ds-trace) then **PR #7** (autoresearch) to main — PR #7 branched from main, independent of #6
2. **Document-type awareness** — The Eppo E5 improvement (no false CRITICAL on prescriptive guides) came from subagent prompt context, not SKILL.md. Need to add document-type detection to SKILL.md to make this durable.
3. **Production validation** — Run actual `/ds-review` with subagent dispatch (not inline) on 2-3 fixtures and compare to autoresearch eval results. Inline execution may overstate quality.
4. **Score accuracy eval** — Design an eval testing whether review scores land within ±10 of calibration baselines (Vanguard ~57, Airbnb ~95, Eppo ~60)
5. **Update README.md** — Document ds-trace (from PR #6) and the autoresearch optimization

## Key Context
- The autoresearch skill lives at `skills/autoresearch/SKILL.md` — installed during the ds-trace session
- 7 test fixtures used: Vanguard, Airbnb, Eppo, Causal (syn), GoodBadComms (syn), Meta LLM, IBM Churn
- The eval suite v2 is at `skills/ds-review/autoresearch-ds-review/eval-suite.md` — reusable for future autoresearch runs
- Inline execution (one agent plays all reviewer roles) produces better output than production subagent dispatch — this is a known limitation of autoresearch on multi-agent skills

## Files to Read First
1. `skills/ds-review/autoresearch-ds-review/changelog.md` — what mutations were tried and why
2. `skills/ds-review/autoresearch-ds-review/eval-suite.md` — eval definitions (reusable)
3. `dev/backlog.md` — current priorities
4. `dev/sessions/2026-03-21-autoresearch-ds-review.md` — full session log
