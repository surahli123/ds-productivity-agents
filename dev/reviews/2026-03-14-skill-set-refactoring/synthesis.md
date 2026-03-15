# Review Synthesis — Skill Set Refactoring Implementation Plan

**Date:** 2026-03-14
**Iterations:** 1
**Calibration status:** Calibrated — all 3 roles passed on first iteration

## Consensus Points

All three reviewers agree on these findings (high-confidence):

1. **Scope discipline is excellent (9/10 across all three).** The plan correctly avoids content rewrites and preserves calibrated material. The "Content unchanged" principle is the plan's strongest quality.

2. **Plugin discovery mechanism is unvalidated (all three flag this).** The plan assumes `.claude-plugin/plugin.json` at the repo root will be recognized by Claude Code but never tests this assumption. If it doesn't work, the entire migration is pointless. DS Lead and PM Lead call this a blocker; Principal calls it a blocker.

3. **Deletion before verification is risky (all three flag this).** Task 8 deletes old directories before Task 9 Step 4 runs the end-to-end test. If the test fails, old files are gone from the working tree. All three recommend: verify first, delete second.

4. **`plugin-conventions.md` update is incomplete.** DS Lead notes it's underspecified (no replacement text). Principal notes it's not committed (missing from `git add` in Task 7 Step 4). Both are valid — the file is updated but neither fully specified nor staged.

5. **Orphaned `agents/` directory creates confusion.** All three note that keeping `agents/sql-review/` and `agents/search-metric-analysis/` alongside the new `skills/` structure sends mixed signals. Recommendation: remove `agents/` entirely, track future skills in backlog.

## Conflicts & Tensions

### 1. Credit cap fix: now or later?

- **DS Lead** (strongly): Fix it now. It's a one-line change in 4 files, every file is already being touched, and deferral risks forgetting. The lead orchestrator Step 9 says +25 but the framework says +15 — this is a live scoring bug.
- **PM Lead** (neutral): Acknowledged as a known issue. Fixing it is consistent with scope discipline if framed as a bug fix, not a feature.
- **Principal** (neutral): Notes it as a pre-existing issue. Doesn't push either way.

**Tension:** DS Lead says fixing this IS scope discipline (it's a bug). The plan says deferring it IS scope discipline (it's not a restructuring task). Both are defensible positions.

**Recommendation for product owner:** Fix it. It's 4 one-line changes, the files are already open, and the R4 calibration validated +15. Carrying forward a known discrepancy when you're already touching every file is a missed opportunity.

### 2. Value proposition: is this worth a session?

- **PM Lead** (skeptical): The current `/ds-review` command already works. This migration produces zero functional improvement. Dogfood testing, output restructure, and genre detection would deliver more value.
- **DS Lead** (supportive): The plugin structure makes the agent more portable and the domain knowledge more accessible to future agents. Net positive.
- **Principal** (conditional): Architecturally sound, but only if plugin discovery works. If it doesn't, the migration is wasted effort.

**Tension:** PM Lead questions whether this is the right use of a session. DS Lead and Principal see architectural value but with conditions.

**Recommendation for product owner:** This is your call. The PM Lead's challenge is fair — you should be clear-eyed that this is a maintenance/architecture investment, not a user-facing improvement. If you're committed to the multi-agent platform vision (SQL review, metric analysis), the plugin structure is a prerequisite. If you'd rather improve the existing tool first, the backlog has higher-impact items.

### 3. Path reference strategy: plugin-root-relative vs skill-relative

- **Principal** (flags as concern): Superpowers uses skill-relative filenames (`code-reviewer.md`). This plan uses plugin-root-relative paths (`skills/ds-review/references/framework.md`). If installed globally, plugin-root-relative paths break.
- **DS Lead** (does not flag): Accepts the path strategy as presented.
- **PM Lead** (does not flag): Focuses on value, not path mechanics.

**Tension:** This is an architecture question only the Principal raises, but it's potentially critical for the stated goal of global installability.

**Recommendation for product owner:** This needs investigation before execution. Check how Claude Code resolves paths in plugin SKILL.md files — relative to skill directory, plugin root, or working directory. A 15-minute test could save hours of rework.

## Decision Points for Product Owner

### Decision 1: Validate plugin discovery BEFORE executing the plan
All three reviewers flag this. Spend 15 minutes testing:
- Does Claude Code recognize `.claude-plugin/plugin.json` at the project root?
- How does `claude plugins list` work?
- What path resolution strategy does Claude Code use for plugin files?

If plugin discovery doesn't work as assumed, revise the plan before moving files.

### Decision 2: Fix the credit cap discrepancy during migration?
- **Yes** = 4 one-line edits (+25 → +15 in reviewer files and lead Step 9). Clean, low-risk.
- **No** = Carry forward as documented known issue. Risk of forgetting.
- DS Lead recommends Yes. Plan currently says No.

### Decision 3: Reorder tasks — verify before delete?
- Move Task 9 Steps 1-4 (end-to-end verification) BEFORE Task 8 (deletion).
- Unanimous recommendation from all three reviewers.

### Decision 4: Remove `agents/` directory entirely?
- **Yes** = Cleaner structure, no mixed signals. Future skills tracked in backlog only.
- **No** = Keep placeholders as visual reminders. Risk of structural confusion.
- All three lean toward removing entirely.

### Decision 5: Thin command vs. current command?
- **Principal** recommends making the command genuinely thin (5 lines, not 40+) to avoid dispatch duplication.
- Current plan keeps detailed dispatch instructions in both SKILL.md and command.
- Trade-off: thin command = single source of truth but relies on SKILL.md loading correctly. Detailed command = redundancy but more resilient if SKILL.md loading fails.

## Score Summary

| Dimension | DS Lead | PM Lead | Principal | Avg |
|-----------|---------|---------|-----------|-----|
| Completeness | 8 | 8 | 7 | 7.7 |
| Clarity | 8 | 8 | 8 | 8.0 |
| Risk Mitigation | 7 | 7 | 7 | 7.0 |
| Scope Discipline | 9 | 9 | 9 | 9.0 |
| Feasibility | 8 | 7 | 7 | 7.3 |

**Overall average: 7.8/10** — Strong plan with specific, addressable gaps.

## Individual Reviews
- [DS Lead Review](ds-lead.md)
- [PM Lead Review](pm-lead.md)
- [Principal AI Engineer Review](principal-ai-engineer.md)
