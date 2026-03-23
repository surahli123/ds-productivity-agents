# Handover: AutoRefine v2 Live Dogfood Complete

## Project
- **Name:** DS Productivity Agents
- **Path:** `/Users/surahli/ds-productivity-agents/`
- **Branch:** `feature/autoresearch-ds-review-location-precision`

## Last Session Summary
Ran the full AutoRefine v2 pipeline (Phases 1-7, both gates) on ds-review to validate v2's Smart Phase 3 features. All mechanisms worked end-to-end. 5 mutations produced, 77.4% → 100% on code judges. User feedback: "eval is way too long for some skills."

## Current State
- **AutoRefine workspace:** `skills/ds-review/autoresearch-ds-review/` — complete v2 pipeline artifacts
- **5 mutations ready:** in `ds-review-optimized.md` (credit ceiling, dim gap warning, structural CRITICAL, contradiction escalation, doc type classification)
- **NOT merged to production** — mutations need review before applying to production SKILL.md
- **Dashboard:** `python3 -m http.server 8080 --directory skills/ds-review/autoresearch-ds-review/` → `localhost:8080/dashboard.html`

## Next Steps (Priority Order)

### 1. AutoRefine v2 go/no-go decision (parallel session in skill-improvement repo)
Read these two files:
1. `docs/session-record-2026-03-22-autorefine-v2-dogfood.md` — full session record with all results
2. This handover

Decide whether autorefine v2 (PR #3 in skill-improvement repo) is ready to merge. Key observations:
- All v2 mechanisms validated ✓
- Pipeline is too long (~90 min) for simpler skills — needs tiered depth
- Override logging mechanism exists but wasn't exercised (no user overrides in this run)
- Agent judges (E1, E5) are noisy — need more fixtures to validate properly

### 2. Review ds-review mutations
The 5 mutations in `ds-review-optimized.md` address real failure modes. Consider merging the code-judge-validated ones (Exp 1-3) first, deferring Exp 4-5 until agent judges are refined:
- **Exp 1 (credit ceiling):** Low risk, well-validated
- **Exp 2 (dim gap warning):** Low risk, output format only
- **Exp 3 (structural CRITICAL):** Low risk, narrow scope
- **Exp 4 (contradiction escalation):** Medium risk, not validated with code judge
- **Exp 5 (doc type classification):** High impact, needs subagent prompt updates too

### 3. Expand fixture set
Current: 15 fixtures. E1 has 5 testable, E3/E5 have 1 each. Need:
- 5+ more blog/guide fixtures for E1
- 2+ more unstructured fixtures for E3
- 2+ more contradiction fixtures for E5

### 4. Production validation
Inline execution (single agent plays all roles) produces different output than production dispatch (3 parallel subagents). The mutations were tested inline — need to verify they work with real subagent dispatch.

## Key Context
- AutoRefine v2 SKILL.md is at `/Users/surahli/Documents/projects/skill-improvement/autorefine/SKILL.md` (PR #3, not yet merged)
- The v1.1 deployed version doesn't have Smart Phase 3 features
- Prior autoresearch workspace backed up at `autoresearch-ds-review-prev/`
- Hamel's evals-skills plugin is installed at `~/.claude/plugins/marketplaces/hamelsmu-evals-skills/`
