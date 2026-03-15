# PM Lead Review — Skill Set Refactoring Implementation Plan

**Reviewer:** PM Lead persona
**Document:** `docs/plans/2026-03-14-skill-set-refactoring.md`
**Date:** 2026-03-14

---

## Overall Assessment

This is a well-structured refactoring plan that reorganizes existing, battle-tested content into a Claude Code plugin-compatible directory layout. The plan is methodical about preserving calibrated content verbatim and includes adequate verification steps. However, the plan lacks a clear articulation of **who benefits from this change, by how much, and when** — the user-facing value proposition ("portability, installability") is assumed rather than validated. The cost of executing this migration (a full session, 9 tasks, 8+ commits) is non-trivial for what is functionally a directory rename with no behavioral improvement, while two planned features (SQL Review, Search Metric Analysis) remain unstarted and are the actual vectors for user value growth.

---

## Scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Completeness | 8/10 | All files are accounted for with source-to-destination mappings. The path reference update tables are thorough. Minor gap: no mention of how `.claude/rules/plugin-conventions.md` content changes are validated (Task 7 Step 2 says "update" but gives no verification step). The plan also leaves `agents/sql-review/` and `agents/search-metric-analysis/` as orphaned placeholders in a structure that no longer uses `agents/` — incomplete cleanup. |
| Clarity for Zero-Context Implementer | 8/10 | Exact file paths, bash commands, expected outputs, and line counts are specified for nearly every step. The bare `SKILL.md` disambiguation (Task 3 Step 2) is particularly well-documented — a real footgun that gets explicit handling. However, Task 7 (documentation updates) provides the new text inline but does not specify where in CLAUDE.md each replacement goes (which line, which heading to find-and-replace). An implementer unfamiliar with CLAUDE.md would need to hunt. |
| Risk Mitigation | 7/10 | The risk assessment table is honest and covers the high-probability items. The "verify before delete" pattern (Task 8 depends on Tasks 1-7) is sound. Rollback strategy is mentioned but thin — "git revert" works mechanically but does not address the scenario where the new plugin structure has been picked up by Claude Code sessions, caches are stale, and reverting creates a broken state. The biggest risk — "Plugin not recognized by Claude Code" — gets only "may need session restart" as mitigation, which is hand-wavy for the single most important acceptance criterion. |
| Scope Discipline | 9/10 | This is the plan's strongest dimension. It explicitly avoids content changes, documents pre-existing issues (credit cap discrepancy) without fixing them, and limits itself to restructuring. The decision log is clean. One minor concern: Task 5 Step 2 adds new content to the search-domain-knowledge SKILL.md ("Update the Architecture context to note that Layer 2 and Layer 3 are now implemented") — this is a functional documentation change, not a restructure. Small, but it's scope creep by the plan's own standard of "Content unchanged." |
| Feasibility | 7/10 | Nine tasks with 30+ individual steps, 8+ commits, and an end-to-end verification that requires a Claude Code session restart — this is achievable in one session but leaves no room for surprises. If the plugin recognition test (Task 9 Step 4) fails, debugging that in the same session is unrealistic. The plan has no time estimates and no "stop point" — if Task 5 takes longer than expected, there's no guidance on what to defer. For a user who is learning to code via vibe coding, the operational complexity of 8 sequential commits with interleaved verification is high. |

---

## Detailed Feedback

### Does this deliver user-facing value?

**Severity: Concern (should address)**

The plan's stated goal is to make the system "installable globally at `~/.claude/plugins/`" — but the backlog shows the current project-level command (`/ds-review`) already works (validated in R4 calibration, 7/7 checks passed). The plan never answers the question: **who is blocked by the current structure, and what can they do after this migration that they cannot do today?**

If the answer is "just me, and it's about cleanliness," that's a valid reason — but then the cost-benefit framing should be honest about it being a maintenance/hygiene investment, not a user-facing capability improvement. The plan frames this as a feature ("feat" commit prefixes) when it's actually a refactor.

If the answer is "other users can install this as a plugin," then the plan should validate that `claude plugins install` actually works with this structure — and that validation is punted to Task 9 Step 4 with a note about "may need session restart." That's not a plan; that's a hope.

**Suggestion:** Add a "Success Criteria" section at the top of the plan that defines exactly what "done" looks like in user-observable terms. Something like: "After migration, `/ds-review` produces identical output to pre-migration on the Vanguard fixture (score within +/-5 points)."

### Is the scope realistic?

**Severity: Suggestion (nice to have)**

The scope is disciplined but the execution is heavy. Nine tasks with fine-grained verification is appropriate for a system with 4 rounds of calibration to protect — but the plan lacks any prioritization within itself. If something goes wrong at Task 5, should the implementer finish Chunks 1-2 and skip Chunk 3? Can the old directories coexist with the new ones temporarily?

The plan's incremental commit strategy does enable partial rollback, but there's no explicit "minimum viable migration" — the point at which the new structure is usable even if cleanup isn't complete.

**Suggestion:** Identify the minimum viable state (probably: Tasks 1-4 complete = ds-review skill works, old directories still exist but are ignored). Call this out as the "safe stopping point."

### What's the cost-benefit of refactoring now vs. building new features?

**Severity: Concern (should address)**

The backlog shows two planned features (SQL Review, Search Metric Analysis) with a "Q2 2026" target. The backlog also shows multiple deferred items (genre/format auto-detection, novel framework credit, output restructure Phase 2, dogfood testing) that would directly improve the review quality for the user.

This refactoring consumes a full session for zero functional improvement. The plan's implicit argument is "we need the plugin structure before we can add SQL Review and Metric Analysis" — but this is never stated or validated. Could the next skill simply be added under `shared/skills/sql-review/` in the current structure? If the answer is "yes, but it would be ugly," that's a different cost-benefit than "yes, but it would be impossible."

The pre-existing backlog item "Post-Ship: Test `claude plugins install`" has been open since February and remains untested. Investing a full session in restructuring for plugin compatibility without first validating that the plugin install mechanism works at all is a sequencing risk.

**Suggestion:** Before executing this plan, spend 15 minutes testing whether `claude plugins install surahli123/ds-analysis-review` works with the current `plugin/` + `dist/` structure. If it doesn't work, you know the plugin mechanism needs investigation regardless of directory structure. If it does work, you have a baseline to compare against.

### Orphaned `agents/` directory

**Severity: Concern (should address)**

The plan removes `agents/ds-review/` but keeps `agents/sql-review/` and `agents/search-metric-analysis/` as "future skill placeholders." After migration, the project will have both a `skills/` directory (the new canonical home) and an `agents/` directory (with placeholder READMEs for future work). This creates exactly the kind of structural ambiguity the migration is trying to eliminate. A new contributor — or future-you in a new session — will see both directories and wonder which pattern to follow.

**Suggestion:** Either remove `agents/` entirely (future skills go under `skills/` from day one) or document in CLAUDE.md that `agents/` is deprecated and exists only as a reminder of planned work. The plan's own conventions file update (Task 7 Step 2) should address this.

### Plugin recognition is the riskiest acceptance test

**Severity: Blocker (must fix)**

Task 9 Step 4 — the end-to-end test — says "This step requires a Claude Code session restart to pick up the new plugin structure. If the command doesn't work immediately, restart the session and retry." This is the entire point of the migration, and the plan treats it as an afterthought.

If this test fails, the entire migration has produced a directory structure that looks correct but doesn't function. There is no diagnostic path in the plan for "plugin not recognized" — no troubleshooting steps, no reference to Claude Code plugin documentation, no fallback to the project-level command approach.

**Suggestion:** Move plugin recognition validation earlier. After Task 1 (plugin.json creation), verify that Claude Code recognizes the plugin manifest. If it doesn't, stop — the rest of the plan is predicated on a mechanism that doesn't work. Add specific troubleshooting steps for the "plugin not recognized" failure mode.

---

## Key Questions for the Author

1. **Who is the user of this migration, and what can they do after it that they cannot do today?** The current `/ds-review` command works via the project-level `.claude/commands/` approach. The plan replaces this with a plugin-level `commands/` approach. What user-observable improvement does this create? If the answer is "portability" — has `claude plugins install` been validated to work with any plugin structure, let alone this one?

2. **Why is this migration higher priority than the open backlog items that directly improve review quality?** The backlog has untouched items (dogfood testing, output restructure Phase 2, genre auto-detection) that would make `/ds-review` more useful to the actual user. This refactoring makes it more portable to hypothetical other users. How does the author weigh these competing investments, and what evidence supports this sequencing?

3. **What happens if Task 9 Step 4 fails — the plugin is not recognized by Claude Code?** The plan has no contingency for the most important acceptance test failing. Is there a fallback where the new directory structure still works via the project-level command mechanism? If so, what was gained over the current structure? If not, what's the rollback plan beyond "git revert"?
