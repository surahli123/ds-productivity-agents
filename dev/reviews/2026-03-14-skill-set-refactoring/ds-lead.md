# DS Lead Review — Skill Set Refactoring Implementation Plan

**Reviewer:** DS Lead (Statistical rigor, methodology, scoring system integrity)
**Document:** `docs/plans/2026-03-14-skill-set-refactoring.md`
**Date:** 2026-03-14

---

## Overall Assessment

This is a well-structured migration plan that correctly treats the 2,800 lines of calibrated content as a controlled artifact requiring careful handling. The plan's strongest quality is its awareness of the disambiguation risk (bare `SKILL.md` references) and its explicit strategy for addressing it. However, there are several risks to scoring system integrity that the plan acknowledges but does not fully mitigate — most notably the credit cap discrepancy (+25 vs +15) being carried forward rather than fixed, and the lack of a quantitative verification step to confirm that review scores remain stable after migration. A restructuring plan that does not include a before/after score comparison is incomplete from a DS rigor standpoint.

---

## Scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Completeness | 8/10 | All files are explicitly accounted for with source and destination paths. The path reference mapping table is thorough. Loses points for not addressing the credit cap discrepancy fix (acknowledged but deferred without a tracking mechanism), and for not specifying what happens to `plugin-conventions.md` content in detail — Step 2 of Task 7 says "update all path conventions" but does not provide the replacement text like it does for CLAUDE.md and README.md. |
| Clarity for Zero-Context Implementer | 8/10 | Exact file paths, bash commands, grep verification commands, and expected outputs are specified for nearly every step. The bare `SKILL.md` disambiguation instructions (Task 3, Step 2) are unusually clear about a subtle problem. Loses points because the SKILL.md body creation in Task 2 says "Copy the full content of `agents/ds-review/ds-review-lead.md` into `skills/ds-review/SKILL.md` with these modifications" but does not provide the full resulting text — an implementer must manually apply ~8 path replacements across a 290-line file, which introduces human error risk. |
| Risk Mitigation | 7/10 | Verification steps at each task are well-designed (grep for old paths, wc -l for line counts, diff for content integrity). The risk assessment table is realistic. However, the plan lacks the single most important verification for a calibrated scoring system: a before/after score comparison on at least one test fixture. Task 9 Step 4 runs the review command but does not compare the output score against the known baseline (Vanguard quick: 57, per backlog). Without this, you cannot confirm that path changes did not break subagent dispatch, framework loading, or deduction table resolution. |
| Scope Discipline | 9/10 | Exceptionally well-scoped. The plan explicitly says "Content unchanged — 4 calibration rounds validated — restructure only, no rewrites." The Known Pre-existing Issues section is honest about the credit cap discrepancy without attempting to fix it. The decision to keep `agents/sql-review/` and `agents/search-metric-analysis/` as placeholders (not migrating them prematurely) shows restraint. The only scope concern is Task 5 Step 2, which asks the implementer to "Update the architecture context to note that Layer 2 and Layer 3 are now implemented" — this is a content change, not a path update, and introduces a small scope expansion. |
| Feasibility | 8/10 | The 9-task structure with incremental commits is realistic for one session. Dependencies are correctly sequenced (Tasks 2-4 before Task 6, all before Task 8 deletion). The only feasibility concern is that Task 9 Step 4 (end-to-end test) requires a Claude Code session restart to pick up the new plugin structure — this is called out but could block the session if the restart invalidates session state or if plugin recognition fails. |

---

## DS Review Agent Usefulness Assessment

### Will the refactored plugin structure make the DS review agent more useful?

**Marginally, yes — but the value is portability, not functionality.** The migration does not change what the agent does or how it scores. It changes how the agent is discovered and invoked. Moving from a project-scoped command (`.claude/commands/ds-review.md`) to a plugin-scoped command (`commands/ds-review.md` under a `.claude-plugin/` manifest) enables global installation via `claude plugins install`. For a DS practitioner who wants to use this tool across multiple projects without copying files, this is a genuine improvement.

However, the plan does not address whether the plugin will actually be installable globally. The `plugin.json` specifies metadata but the plan never tests `claude plugins install` from a different project directory. Task 9 Step 1 only verifies the directory structure exists — it does not verify Claude Code recognizes it as a valid plugin. This is a feasibility gap, not a completeness gap, but it undermines the primary user-facing value proposition of this refactoring.

### Does the refactoring preserve calibration quality?

**Mostly yes, with one documented risk.** The plan correctly identifies that calibrated content (deduction tables, credit tables, severity definitions, floor rules) must not change. The "copy verbatim" approach for reviewer files and the "remove frontmatter only" approach for the framework are the right strategies.

However, there are two specific risks to scoring integrity:

1. **Credit cap discrepancy propagation (Concern, should address).** The reviewer files reference "capped at +25" in their output format templates (lines 125, 91, 119 of analysis/communication/domain reviewers respectively). The framework.md Section 2b says "Maximum +15 credits per dimension." The plan acknowledges this in "Known Pre-existing Issues" but carries it forward as-is. This is problematic because: (a) the lead orchestrator in Step 9 also says "capped at +25 per dimension" on line 201 of ds-review-lead.md, which is the operative instruction since the lead recomputes scores; (b) the R4 calibration was validated with the +15 cap in the framework, but the lead agent's Step 9 still references +25. If the LLM follows the lead's Step 9 instruction (+25) rather than the framework's Section 2b (+15), scores will inflate by up to 10 points on credit-heavy analyses. The plan should either fix this discrepancy during migration (it is a one-line change in 4 files) or explicitly document which instruction is authoritative and verify the LLM follows the correct one.

2. **Bare `SKILL.md` disambiguation (Concern, plan addresses adequately).** The plan's handling of the `SKILL.md` to `framework.md` rename in reviewer files is thorough. The approximate instance counts in the plan (12, 9, 14) overestimate the actual counts (9, 7, 12), but overestimating is safer than underestimating — it means the implementer will look harder for instances rather than stopping early.

### Domain knowledge accessibility for future agents

**Properly separated.** The `search-domain-knowledge` skill as a standalone directory under `skills/` with its own `SKILL.md` consumption contract is the correct architecture for future agents. The domain-index.yaml, digest files, and SKILL.md consumption contract are self-contained — an SQL review agent or metric analysis agent could read the SKILL.md and follow the same digest loading pattern without knowing anything about `ds-review`. The plan preserves the `[authority: ...]` tagging system, which is essential for the advisory/authoritative severity differentiation to work correctly in any consuming agent.

One gap: the plan does not verify that `search-domain-knowledge/SKILL.md` can be consumed independently — i.e., that it does not reference `ds-review` internals after path updates. Task 5 Step 6 only checks for old `shared/skills` paths, not for cross-skill references that would create coupling.

---

## Detailed Feedback

### Completeness (8/10)

**Strengths:**
- The file structure table at the top is clear and complete — every source file, destination, and operation (CREATE, COPY, COPY+EDIT, REMOVE) is explicit.
- The path reference mapping table covers all known cross-references.
- The Known Pre-existing Issues section is honest about the credit cap discrepancy rather than hiding it.

**Issues:**

1. **(Concern) `plugin-conventions.md` update is underspecified.** Task 7 Step 2 says to update all path conventions in `.claude/rules/plugin-conventions.md` but does not provide the replacement text, unlike CLAUDE.md and README.md which get exact replacement blocks. This file is auto-loaded as a project rule and contains 6+ path patterns that need updating. An implementer without context would have to figure out the correct replacements from the path mapping table, which is error-prone. Provide the exact replacement sections.

2. **(Suggestion) Add `dist/` files to the accounting.** The plan says to remove `dist/` but does not account for the files inside it (`dist/ds-analysis-review/README.md`, `dist/ds-analysis-review/agents/*.md`, etc.). These files also contain the +25 credit cap references and old path patterns. While they are being deleted, explicitly listing them confirms nothing is being lost that should be preserved.

### Clarity for Zero-Context Implementer (8/10)

**Strengths:**
- Verification commands with expected outputs at every step are excellent. An implementer can mechanically verify correctness.
- The "Dispatch duplication note" in Task 6 explaining why the command wrapper repeats subagent dispatch instructions is the kind of documentation that prevents future confusion.
- The "Category A / Category B" separation in Task 3 Step 2 makes the disambiguation problem clear.

**Issues:**

1. **(Concern) Task 2 does not provide the complete SKILL.md text.** The plan says "Copy the full content of `agents/ds-review/ds-review-lead.md` into `skills/ds-review/SKILL.md` with these modifications" and then lists 8 path replacements plus 4 `/ds-review:review` to `/ds-review` changes plus bare `SKILL.md` to `framework.md` changes. For a 290-line file with 12+ modifications, providing only the diff instructions (not the full target text) creates risk. The implementer must correctly apply all changes without missing any. Consider providing the full target file content, or at minimum, a sed script that applies all replacements.

2. **(Suggestion) Line number references in Task 2 may drift.** The plan references specific line numbers (161, 259, 270, 271) for `/ds-review:review` replacements. If any prior edit shifts line numbers, these references become wrong. Use grep-based identification instead ("the line containing 'Level 2 defer message'") alongside line numbers.

### Risk Mitigation (7/10)

**Strengths:**
- The risk assessment table is realistic — it identifies the right risks (path references, bare SKILL.md ambiguity, framework section numbering, digest modification) with appropriate likelihood/impact ratings.
- Grep-based verification after each copy step is the correct approach for path migration.
- The incremental commit strategy means each task can be reverted independently.

**Issues:**

1. **(Blocker) No before/after score comparison.** This is the most significant gap in the plan. The system has been calibrated through 4 rounds with known baseline scores (Vanguard: 57 without domain, 64 with domain; Meta: 60; Rossmann: 63). Task 9 Step 4 runs a review but does not compare the output against these baselines. A migration that changes how files are loaded and referenced could silently break scoring — for example, if a subagent fails to read `framework.md` because it looks for `SKILL.md`, the re-dispatch logic in Step 7 would embed sections 1-7 directly, but the section content might differ if the frontmatter removal shifted numbering. Without a quantitative comparison, you cannot claim the migration preserved calibration. **Fix:** Add a verification step: "Run the Vanguard quick review and verify the score is within +/-5 of the known baseline (57). If outside this range, investigate before proceeding."

2. **(Concern) No rollback test.** The plan mentions rollback (`git revert <commit>..HEAD`) but does not verify that the rollback actually works. If the commit history has merge commits or the `git rm` steps create conflicts during revert, the rollback could fail when you most need it. **Suggestion:** After Task 8 Step 5 (removal commit), verify: `git stash && git revert --no-commit HEAD && git diff HEAD~1 --stat && git reset --hard HEAD` to confirm the revert would be clean.

3. **(Concern) Session restart risk in Task 9.** The plan notes that a Claude Code session restart may be needed for plugin recognition. If the restart clears session context, the implementer loses the ability to run verification steps that depend on knowing what was changed. **Suggestion:** Complete all verification steps that do not require plugin recognition before the restart, and have a separate post-restart verification checklist.

### Scope Discipline (9/10)

**Strengths:**
- "Content unchanged" as an explicit principle is the single most important scope decision. The plan adheres to it rigorously.
- The decision to not migrate `agents/sql-review/` and `agents/search-metric-analysis/` (future placeholders) prevents premature abstraction.
- The Known Pre-existing Issues section draws a clear boundary: "these exist but are not our problem today."

**Issues:**

1. **(Suggestion) Task 5 Step 2 architecture context update is scope creep.** The plan asks the implementer to update `search-domain-knowledge/SKILL.md` to "note that Layer 2 and Layer 3 are now implemented (not future)." This is a content change that goes beyond path migration. It is small and arguably correct, but it introduces a modification to a calibrated file that was not driven by the structural migration. If you are going to update content, document it as a deliberate content change, not as a path update.

### Feasibility (8/10)

**Strengths:**
- The 9-task breakdown with checkboxes is the right granularity for a single session.
- Dependency ordering is correct (scaffold first, content second, command third, cleanup last).
- Commit strategy (one commit per task) provides clean revert points.

**Issues:**

1. **(Concern) `plugin.json` schema validity.** Task 1 validates that `plugin.json` is valid JSON, but does not verify it conforms to the Claude Code plugin schema. If the schema requires fields that are not present (e.g., `skills` array, `commands` array, or a `main` entry point), the plugin will not be recognized even though the JSON is valid. **Suggestion:** Add a step to compare against a known working plugin.json (e.g., the `ralph-wiggum` plugin at `~/.claude/plugins/cache/ralph-wiggum/`).

2. **(Suggestion) Total line count verification in Task 9 Step 3 is weak.** Checking that 12 files exist tells you nothing about whether they are correct. The content verification happens in earlier tasks, but Task 9 should also verify that the total line count of all skill files matches the pre-migration total (minus frontmatter removals). This is a cheap sanity check.

---

## Key Questions for the Author

1. **Why is the credit cap discrepancy being carried forward rather than fixed during this migration?** The lead orchestrator's Step 9 says "capped at +25 per dimension" while the framework says "Maximum +15." R4 calibration validated +15, but the lead agent reads +25. This is a one-line fix in 4 files. If you are already touching every file in the system for path updates, why not fix this? The risk of deferral is that a future session forgets, and the next calibration run shows inflated scores that trace to this discrepancy. What is the concrete reason for not fixing it now?

2. **How will you know the migration succeeded from a scoring perspective?** The plan verifies file structure, path references, and line counts — but never verifies that the system produces the same scores as before. Given that 4 rounds of calibration produced known baselines, what is your acceptance criterion for "the migration did not break scoring"? If the answer is "I will run a review and eyeball it," that is not rigorous enough for a system that was calibrated to within 2-point spreads (Airbnb consistency test: 93-95).

3. **What happens if the plugin is not recognized by Claude Code after migration?** Task 9 Step 4 says "may need session restart" — but what if, after restart, the `/ds-review` command does not trigger? The plan has no fallback. The old `.claude/commands/ds-review.md` is deleted in Task 8. If the new command does not work, you have a system that cannot be invoked at all until the problem is diagnosed. Should the old command deletion be deferred until after the new command is verified working?

---

*Review completed independently. No other reviewer perspectives consulted.*
