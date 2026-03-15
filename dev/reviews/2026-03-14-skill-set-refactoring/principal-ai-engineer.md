### Principal AI Engineer Review

**Overall Assessment:** This is a well-structured migration plan that correctly identifies the target plugin pattern and produces a layout consistent with established plugins (superpowers, kaizen). The plan is disciplined about preserving calibrated content and includes verification steps at each stage. However, it has a meaningful architectural gap around how the plugin will actually be discovered and loaded at runtime, a fragile path reference strategy that relies on string-level grep verification rather than structural guarantees, and some structural decisions that diverge from established plugin conventions without justification.

#### Scores
| Dimension | Score | Justification |
|-----------|-------|---------------|
| Completeness | 7/10 | All files are accounted for and the migration path is traceable. However, the plan does not address how the plugin gets installed or discovered (project-local vs global `~/.claude/plugins/`), leaves the `agents/sql-review/` and `agents/search-metric-analysis/` placeholder directories in an orphaned state, and omits the `.claude/rules/plugin-conventions.md` commit from Task 7 (Step 2 updates it, Step 4 commits only CLAUDE.md and README.md). |
| Clarity for Zero-Context Implementer | 8/10 | File paths, shell commands, and expected outputs are explicit. The path replacement tables are precise. The SKILL.md disambiguation (Category B in Task 3) is the kind of detail that saves hours. One gap: the SKILL.md body edits in Task 2 describe what to change but not where exactly in the file (beyond 4 line numbers for command references), which means an implementer must read the entire 290-line source to find all "bare SKILL.md" references. |
| Risk Mitigation | 7/10 | Verification steps are present at each task (grep for old paths, line count checks, diff comparisons). The rollback strategy exists but is rudimentary ("git revert" or "git reset --hard"). The risk table is honest. The biggest mitigation gap is the absence of a functional smoke test before deletion — Task 8 deletes old directories, but Task 9 Step 4 (the actual end-to-end test) happens after deletion. If the plugin structure is not recognized, the old files are already gone from the working tree. |
| Scope Discipline | 9/10 | This is the plan's strongest dimension. It explicitly avoids content rewrites, preserves calibrated material, and calls out the credit cap discrepancy as a known issue to fix later. The decision to keep `agents/sql-review/` and `agents/search-metric-analysis/` as-is is disciplined (though it creates a structural inconsistency — see detailed feedback). No feature additions, no premature optimization. |
| Feasibility | 7/10 | The plan is realistic for one session. Dependencies between tasks are correctly ordered. However, there is no time estimate, and the plan underestimates the effort of Task 2 (SKILL.md body edits) which requires careful reading of a 290-line file to identify all bare `SKILL.md` references. The "session restart to pick up plugin structure" note in Task 9 Step 4 is a feasibility risk — if the plugin is not recognized, the implementer is stuck mid-migration with deleted source files and no functional system. |

#### Detailed Feedback

**1. Plugin Discovery and Installation (Blocker)**

The plan says "the repo root becomes the plugin root" and places `.claude-plugin/plugin.json` at the root. But it never explains how this plugin gets loaded. Is this a project-local plugin (recognized because the repo is the working directory)? Or does it need to be installed globally via `claude plugins install`? The reference plugins (superpowers, kaizen) live in `~/.claude/plugins/cache/` with a specific `<registry>/<name>/<version>/` path structure. This plan produces a repo that looks like a plugin but may not be recognized as one by Claude Code.

This is the most important question in the entire plan, and it is never addressed. The Risk Assessment mentions "Plugin not recognized by Claude Code" as "Medium likelihood, Medium impact" — but if the plugin structure is not recognized, nothing works. The entire migration is pointless. This should be validated in Task 1, not Task 9.

**Concrete suggestion:** Add a Step 0 or Task 0 that validates how Claude Code discovers project-local plugins. Run `claude plugins list` or inspect the Claude Code plugin loader documentation to confirm that a `.claude-plugin/plugin.json` at the project root is sufficient for project-scoped plugin behavior. If it is not, the entire plan needs to be revised before any files are moved.

**Severity: Blocker.** If plugin discovery does not work as assumed, the migration produces a non-functional system.

**2. Path Reference Strategy is Fragile (Concern)**

The plan relies on string-based path references (`skills/ds-review/references/framework.md`) that are validated by grep. This means every path is a hardcoded string embedded in markdown prose. There is no indirection, no variable, no single source of truth for paths.

Compare to superpowers, which uses co-located files within the skill directory (e.g., `code-reviewer.md` next to `SKILL.md` in `requesting-code-review/`). Superpowers references companion files by filename alone (`code-reviewer.md`), not by full relative path (`skills/requesting-code-review/code-reviewer.md`). This is more resilient — if the plugin is installed at a different cache path, relative-to-skill references still resolve.

The plan's approach puts reference files in a `references/` subdirectory and references them with paths relative to the plugin root (`skills/ds-review/references/framework.md`). This works only if the working directory is the plugin root. If the plugin is installed globally, the working directory will be whatever project the user is in, and these paths will break.

**Concrete suggestion:** Investigate whether Claude Code resolves paths in SKILL.md relative to the skill directory, relative to the plugin root, or relative to the working directory. If it is relative to the skill directory, change all path references to be relative to the skill (e.g., `references/framework.md` instead of `skills/ds-review/references/framework.md`). If it is relative to the working directory, the entire path reference model is fragile and needs a different approach (perhaps using `${PLUGIN_ROOT}` placeholders if supported).

**Severity: Concern.** Works for project-local usage, but will break if the plugin is ever installed globally — and the stated goal of the refactoring is to make the plugin installable.

**3. Structural Inconsistency with Remaining `agents/` Directory (Concern)**

The plan deletes `agents/ds-review/` but keeps `agents/sql-review/` and `agents/search-metric-analysis/` as "future skill placeholders." After this migration, the repo will have:

- `skills/` — the new plugin structure
- `agents/` — old structure, containing only placeholder READMEs for future work

This is confusing for anyone encountering the repo fresh. Are agents and skills different concepts? Is `agents/` deprecated? The plan says "when they are implemented, they will become skills under `skills/`" — but it does not add any signposting (a README in `agents/` explaining the planned migration, for example).

**Concrete suggestion:** Either (a) remove `agents/` entirely and track future skills in `dev/backlog.md` where they are already listed, or (b) add a README to `agents/` explaining that these are planned future skills that will live under `skills/` when implemented. Option (a) is cleaner.

**Severity: Concern.** Not a functional issue, but will confuse future sessions and new contributors.

**4. Command Location Deviates from Reference Plugins (Concern)**

Superpowers places commands at `commands/` (at plugin root). Kaizen has no commands directory — its skills are all auto-triggered. The plan places the command at `commands/ds-review.md`, which matches the superpowers pattern.

However, the current command lives at `.claude/commands/ds-review.md`, which is the Claude Code project-command location. The plan says to delete the old `.claude/commands/ds-review.md` and create `commands/ds-review.md` (plugin-level). This is correct for a plugin, but only if the plugin is recognized — circling back to the discovery issue in point 1. If the plugin is not recognized, the command disappears entirely.

**Concrete suggestion:** Keep `.claude/commands/ds-review.md` as a fallback until plugin discovery is validated. Delete it only after confirming that `commands/ds-review.md` is picked up by the plugin loader.

**Severity: Concern.** Covered by the Task 9 smoke test, but the deletion happens in Task 8 before the test runs.

**5. Task 7 Step 2 is Updated but Not Committed (Blocker)**

Task 7 has three steps that modify files:
- Step 1: Update CLAUDE.md
- Step 2: Update `.claude/rules/plugin-conventions.md`
- Step 2 (duplicate numbering): Update README.md

But Step 4 (Commit) stages only `CLAUDE.md` and `README.md`:

```bash
git add CLAUDE.md README.md
git commit -m "docs: update project docs for plugin skill set structure"
```

`.claude/rules/plugin-conventions.md` is modified but never staged or committed. This file is auto-loaded as a project rule, so having stale content pointing to `agents/` and `shared/skills/` will actively mislead Claude Code in future sessions.

**Concrete suggestion:** Add `.claude/rules/plugin-conventions.md` to the `git add` in Task 7 Step 4. This is a straightforward omission.

**Severity: Blocker.** Stale project rules will cause incorrect path guidance in every future session.

**6. Dispatch Duplication Between Command and SKILL.md (Suggestion)**

The plan acknowledges that the command wrapper "repeats subagent dispatch instructions that also exist in SKILL.md Step 7" and calls this intentional, with the command being authoritative for file paths. This creates a maintenance surface — if a path changes, you must update it in two places, and the plan designates the command as the "authoritative" source but the SKILL.md as authoritative for "pipeline logic."

In the superpowers pattern, the command (`commands/brainstorm.md`) is truly thin — it says little more than "use the brainstorming skill." The skill handles everything. The proposed command here is 40+ lines with detailed dispatch instructions, path references, and key reminders. That is not thin.

**Concrete suggestion:** Make the command genuinely thin. Remove the Subagent Dispatch and Key Reminders sections from the command. Let the SKILL.md be the single authoritative source for both paths and logic. The command should be: "Read `skills/ds-review/SKILL.md` and `skills/ds-review/references/framework.md`. Execute the 10-step pipeline on: $ARGUMENTS." That is 5 lines, not 40.

**Severity: Suggestion.** The current approach works but doubles the maintenance surface for path references and risks drift between the two sources of truth.

**7. Deletion Before Verification Ordering (Concern)**

Task 8 (Remove old directories) runs before Task 9 Step 4 (Run the `/ds-review` command on a test fixture). This means if the end-to-end test fails, the old source files are already deleted from the working tree. Yes, they exist in git history and can be recovered, but the plan's rollback instruction ("git revert or git reset --hard") is a blunt instrument for a vibe-coding user who may not be comfortable with git recovery.

**Concrete suggestion:** Reorder tasks: run Task 9 Steps 1-4 (end-to-end verification) between Task 7 and Task 8. Delete old directories only after confirming the new structure works. This is the standard "verify before you destroy" pattern. If the smoke test requires a session restart (as noted), do the restart, verify, then return to delete.

**Severity: Concern.** The current ordering creates a window where the system is non-functional if anything goes wrong with plugin discovery.

**8. No `.claude/rules/` Update for Plugin Context (Suggestion)**

The plan updates `plugin-conventions.md` with new paths, but it does not consider whether the conventions file should also describe the new plugin structure conceptually — i.e., that skills have SKILL.md files with frontmatter, that `references/` contains subagent prompts and data files, that `commands/` provides explicit invocation entry points. The current conventions file describes an `agents/` + `shared/skills/` + `.claude/commands/` + `plugin/` world. After migration, none of those top-level directories exist in the same way.

**Concrete suggestion:** Task 7 Step 2 should rewrite `plugin-conventions.md` to describe the new structure, not just update path references. Otherwise the conceptual model in the rules file will not match the actual codebase structure.

**Severity: Suggestion.** The plan says "update all path conventions" but a conceptual rewrite would be more durable.

#### Key Questions for the Author

1. **How does Claude Code discover this plugin?** You say "the repo root becomes the plugin root," but have you validated that Claude Code recognizes a `.claude-plugin/plugin.json` at the project root as a project-scoped plugin? The reference plugins all live in `~/.claude/plugins/cache/` with a registry path structure. If project-root discovery does not work, the entire migration is building toward a non-functional target. What is the specific mechanism?

2. **What happens to path references when this plugin is installed globally?** The plan uses paths like `skills/ds-review/references/framework.md` throughout. These resolve only if the working directory is the plugin root. If a user installs this plugin via `claude plugins install` and runs `/ds-review` from a different project, will those paths resolve? Superpowers uses skill-relative filenames (`code-reviewer.md`), not plugin-root-relative paths. Why does this plan use a different pattern, and has it been tested?

3. **Why delete old files before running the end-to-end smoke test?** Task 8 removes source files, Task 9 Step 4 tests whether the new structure works. If the test fails, the user needs to recover files from git history. Given that the target user is a vibe-coder with minimal debugging ability, why not verify first and delete second?
