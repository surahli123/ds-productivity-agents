# Pickup Guide for Next Session

**Last updated:** 2026-02-15
**Current branch:** `feat/v0.4.1-credit-redesign`
**Current state:** Plugin registered as project command (`/ds-review`), pending restart test

---

## Quick Context

You just completed **R3 calibration round** (all 6 test fixtures reviewed, 3 role assessments done, fix plan synthesized). The system is **production-ready for plugin registration**, but scores are inflated (+17 to +30 points above targets). R4 calibration is deferred until after plugin registration.

**One immediate fix was applied:** Downgraded "Conclusion doesn't trace" from CRITICAL to MAJOR (Meta now has 2 CRITICALs instead of 3).

---

## What's Next: Two Parallel Tracks

### Track A: Plugin Registration — DONE (pending restart test)

**What was done:**
- [x] Researched Claude Code plugin registration process
- [x] Created project-level command: `.claude/commands/ds-review.md`
- [x] Structural validation passed (7/7 checks)
- [x] Documented process: `dev/PLUGIN-REGISTRATION-PROCESS.md`
- [ ] **Test `/ds-review` command after restarting Claude Code**
- [ ] Verify subagent dispatch works correctly

**Key finding:** The `plugin/` directory structure is correct but plugins must be installed via marketplace/GitHub — they don't auto-load from project dirs. Project-level commands (`.claude/commands/`) are the simplest path for local use.

**Command name:** `/ds-review` (not `/ds-review:review` — namespaced format requires full plugin install)

**To test after restart:**
```bash
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode quick --audience tech --workflow reactive
```

**Key files:**
- `.claude/commands/ds-review.md` (**NEW** — project command entry point)
- `plugin/agents/*.md` (3 agent prompts — unchanged, referenced by command)
- `plugin/skills/ds-review-framework/SKILL.md` (shared rubrics — unchanged, referenced by command)
- `dev/PLUGIN-REGISTRATION-PROCESS.md` (**NEW** — full documentation)

---

### Track B: R4 Calibration (DEFERRED)

When ready to continue calibration (after plugin registration):

**To-do:**
- [ ] Read `dev/test-results/2026-02-15-r3-calibration-fix-plan.md` (Section 6: Implementation Plan)
- [ ] Implement **Fix 1: Reduce credit cap from +25 → +15**
  - File: `plugin/skills/ds-review-framework/SKILL.md`, Section 2b
  - Change: "Cap: Maximum +25 credits per dimension" → "Cap: Maximum +15 credits per dimension"
- [ ] Run all 6 test fixtures as R4:
  - Vanguard, Meta, Rossmann (core)
  - Airbnb Message Intent, Airbnb FIV, Netflix Proxy Metrics (extended)
- [ ] Evaluate scores against revised targets:
  - Vanguard: target 55-65 (R3: 72, R4 expected: ~62) ✅
  - Meta: target 60-70 (R3: 63, R4 expected: ~53-58)
  - Rossmann: target 65-75 (R3: 86, R4 expected: ~76)
- [ ] If R4 scores still high, apply **Fix 2A: Increase 2-3 MAJOR deductions by +2**
  - Missing baseline/benchmark: -10 → -12
  - Missing/ineffective TL;DR: -10 → -12
  - Too long/buries signal: -10 → -12
- [ ] Run cross-run consistency test (same doc 3x, verify ±10 variance)
- [ ] Rerun 2-3 synthetic fixtures to verify floor rules still work

**Estimated rounds to acceptance:** 1-2 (R4, potentially R5)

**Key files:**
- Fix plan: `dev/test-results/2026-02-15-r3-calibration-fix-plan.md`
- Calibration loop workflow: `docs/plans/2026-02-15-calibration-loop-workflow.md`

---

## Current System State

### Scores (R3)

| Fixture | Score | Target | Status |
|---|---|---|---|
| Vanguard | 72 | 40-55 | +17 OVER |
| Meta | 63 | 50-65 | WITHIN ✅ |
| Rossmann | 86 | 45-60 | +26 OVER |
| Message Intent | 85 | 55-65 (A) | +28 OVER |
| FIV | 90 | 65-75 (A) | +22 OVER |
| Proxy Metrics | 100 | 60-70 (A) | +30 OVER |

### What's Working ✅

- Finding quality excellent (8/8 Vanguard findings legitimate)
- Differentiation strong (37-point gap maintained)
- All P0/P1 fixes working correctly (no bugs)
- Duplicate suppression working
- Self-deliberation eliminated
- Conditional credit halving working
- Meta CRITICAL count: 2 (meets ≤2 target)

### What Needs Fixing ⚠️

- **Score inflation:** All tests 17-30 points above targets
- **Root cause:** Credit additions (+6) without offsetting deductions
- **Fix:** Reduce credit cap from +25 → +15 (deferred to R4)

---

## Git Status

**Current branch:** `feat/v0.4.1-credit-redesign`

**Commits on this branch (not yet merged to main):**
1. `fe4e519` - fix(comm-reviewer): add single-pass commit rule
2. `82f919d` - fix(lead): add tightened duplicate suppression and finding volume cap
3. `c282036` - feat(skill): add CRITICAL deduction for unvalidated experimental claims
4. `6d5c2e7` - feat(skill): replace analysis credits with methodology-agnostic table
5. `898f7dd` - fix(skill): reduce 3 MINOR comm deductions, add worked example credit
6. `7649c41` - fix(skill): downgrade 'Conclusion doesn't trace' from CRITICAL to MAJOR (latest)

**Uncommitted changes:**
- `dev/backlog.md` (updated with R3 results)
- `CHANGELOG.md` (updated with R3 results)

---

## Key Files to Read First

When starting next session, read these in order:

1. **dev/backlog.md** - Current state and priorities
2. **dev/sessions/2026-02-15-r3-calibration-execution.md** - What just happened
3. **This file (dev/PICKUP.md)** - Where to go next
4. **For plugin registration:**
   - Claude Code plugin documentation (search web or docs)
   - `plugin/.claude-plugin/plugin.json`
5. **For R4 calibration (when ready):**
   - `dev/test-results/2026-02-15-r3-calibration-fix-plan.md`
   - `docs/plans/2026-02-15-calibration-loop-workflow.md`

---

## Outstanding Decisions

### From R3 Fix Plan (Section 7)

**Q1: Which path for R4?**
- Conservative (recommended): Fix 1 only, evaluate, then Fix 2A if needed
- Aggressive: Fix 1 + Fix 2A together
- Mathematical: Symmetric DR on credits (more complex)
- **DECISION NEEDED:** Owner to choose when ready for R4

**Q2: Should we run R4 now or after plugin registration?**
- **DECISION MADE:** After plugin registration

**Q3: Do we need cross-run consistency testing before shipping?**
- **DECISION DEFERRED:** Run in R4 alongside calibration

---

## Open Questions for Future Rounds

1. If Fix 1 brings scores to 55-70 (just above targets), is that acceptable?
2. Should blog post targets be adjusted upward? (Currently 55-80, actually scoring 85-100)
3. Is Vanguard analysis drop (-18) a concern for users? Should we soften conditional halving?
4. Floor rule UX: Should we suppress numeric score when floor applies? (Deferred to v0.5)

---

## Session End Checklist ✅

- [x] R3 calibration complete (6 fixtures, 3 role reviews, fix plan)
- [x] Immediate fix applied (Meta CRITICAL downgrade)
- [x] CHANGELOG updated
- [x] Backlog updated
- [x] Session log created
- [x] Pickup guide created (this file)
- [x] All artifacts saved to `dev/`
- [x] Git commits made for code changes
- [ ] Merge to main (deferred until after plugin registration validation)

---

## Quick Commands for Next Session

```bash
# Check current branch and status
git status
git branch

# Read key context files
cat dev/backlog.md
cat dev/PICKUP.md
cat dev/sessions/2026-02-15-r3-calibration-execution.md

# For plugin registration (research first)
# TBD based on Claude Code plugin registration process

# For R4 calibration (when ready)
cat dev/test-results/2026-02-15-r3-calibration-fix-plan.md
# Then implement Fix 1, run 6 reviews, evaluate
```

---

## Contact Context

**Owner preferences:**
- Plans before code, always
- Explain everything (learning through vibe coding)
- Product/DS analogies preferred
- Never assume debugging capability
- Web session handles evaluation/critique, Claude Code handles engineering

**Skills frequently used:**
- kaizen:analyse-problem (A3 format)
- superpowers:writing-plans
- superpowers:executing-plans

**Division of labor:**
- Web session: Evaluation, critique, design decisions
- Claude Code: Implementation, testing, technical execution
