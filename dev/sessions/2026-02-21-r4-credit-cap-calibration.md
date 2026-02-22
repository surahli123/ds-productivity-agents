# Session: R4 Credit Cap Calibration

**Date:** 2026-02-21
**Branch:** main
**Commit:** 41c58fe
**Status:** Credit cap fix accepted, domain calibration deferred to next session

## What Was Done

### 1. Credit Cap Fix (Primary R4 Fix)
Changed per-dimension credit cap from +25 to +15 in `shared/skills/ds-review-framework/SKILL.md`:
- Section 2b header (line 116): cap description
- Credit Rule 3 (line 166): all three dimension caps

This was the consensus fix from all 3 R3 reviewers (Principal AI Engineer, PM Lead, DS Lead).

### 2. R4 Calibration Runs (3 Core Fixtures, No --domain)

| Fixture | R3 | R4 | Delta | Target | Status |
|---------|----|----|-------|--------|--------|
| Vanguard | 72 | 57 (A:58, C:55) | -15 | 55-65 | In range |
| Meta | 63 | 60 (A:61, C:59) | -3 | 60-70 | In range |
| Rossmann | 86 | 63 (A:72, C:53) | -23 | 65-75 | 2 pts below |

**Key observations:**
- Credit cap fix worked as predicted for Vanguard and Meta
- Rossmann dropped more than expected (23 pts vs predicted ~10)
- Meta moved least (only -3) because it had fewer credits to begin with
- Secondary fix (MAJOR deduction increases) not needed

### 3. Search-Domain Test Fixtures Created
Found and saved 3 search relevance blog posts for `--domain` calibration:
- `dev/test-fixtures/real/airbnb-search-interleaving.md` — Airbnb interleaving experiments, competitive pairs, attribution logic
- `dev/test-fixtures/real/atlassian-rovo-search-relevance.md` — Atlassian Rovo multi-layer ranking (BM25, KNN, cross-encoder), evaluation metrics
- `dev/test-fixtures/real/eppo-search-ranking-experiments.md` — Search ranking experimentation methodology (Slack, Airbnb references)

## Process Notes

### Subagent-Driven Development
Used the `superpowers:subagent-driven-development` skill:
- Tasks 1 (credit cap fix) and 2 (find search docs) dispatched as parallel subagents
- Task 1 subagent completed clean edit, spec compliance review passed
- Task 2 subagent failed (tool use rejected during web fetch) — recovered in main context
- Task 3 (calibration runs) dispatched as 3 parallel background subagents

### Subagent Limitation Discovered
The review subagents (Vanguard, Meta, Rossmann) couldn't dispatch their own sub-subagents via Task tool. They executed the reviewer logic inline instead (single agent acting as both analysis + communication reviewer). This means:
- Scores may differ slightly from true `/ds-review` runs with independent subagents
- Inline execution may compress scores (single agent more self-consistent)
- True `/ds-review` runs in next session will validate

### WebFetch Lessons
- Medium.com returns 403 for all WebFetch attempts
- Airbnb's own tech blog (airbnb.tech) works fine as alternative
- Atlassian and Eppo blogs fetched without issues
- Parallel fetch (3 at once) works when one doesn't fail

## What's Next (Next Session)

1. Run 3 search fixtures WITH `--domain search-ranking` using actual `/ds-review` command
2. Run 3 R3 core fixtures WITH `--domain search-ranking` (cross-genre test)
3. Cross-run consistency: same doc 3x, verify ±10
4. Consider committing test fixtures (currently untracked)
