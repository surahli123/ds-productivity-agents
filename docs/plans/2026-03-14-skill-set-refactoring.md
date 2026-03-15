# DS Productivity Skill Set Refactoring — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the DS Review agent system from a custom `agents/` + `shared/skills/` project structure into a clean plugin-compatible skill set layout (`ds-productivity`). Project-level command (`.claude/commands/`) retained for proven reliability. Marketplace publishing deferred until global install is needed.

**Architecture (Option B — Pragmatic):** Skills reorganized under `skills/` at project root. Command stays at `.claude/commands/ds-review.md` (project-level, auto-discovered, proven working). `.claude-plugin/plugin.json` added at project root for future marketplace publishing. Two independent skills — `ds-review` (orchestrator + reviewers + framework) and `search-domain-knowledge` (domain digests + consumption contract).

**Path resolution strategy (validated via Task 0):**
- **Within a skill:** Use skill-relative paths (`references/framework.md`) — proven pattern (superpowers, PDF skill)
- **Cross-skill references:** Use explicit project-relative paths (`skills/search-domain-knowledge/digests/{domain}.md`) — the command and orchestrator know the project root
- **Command → skill files:** Use project-relative paths (`skills/ds-review/SKILL.md`) — command runs in project context
- **`${CLAUDE_PLUGIN_ROOT}` NOT used:** Explicitly removed by planning-with-files plugin due to reliability issues. Avoided.
- **Subagent dispatch payloads:** Use project-relative paths (subagents run in project working directory)

**Tech Stack:** Markdown (SKILL.md files), JSON (plugin.json), YAML (domain-index.yaml)

**Rollback:** All changes are committed incrementally. To rollback: `git revert <commit>..HEAD` to undo specific commits, or `git reset --hard <pre-migration-commit>` to revert everything. Original files exist in git history.

---

## File Structure

### New Files (Create)

```
ds-productivity-agents/                          # repo root = plugin root
├── .claude-plugin/
│   └── plugin.json                              # NEW — plugin manifest (for future marketplace)
├── .claude/
│   └── commands/
│       └── ds-review.md                         # KEEP+EDIT — project-level command (proven, auto-discovered)
├── skills/
│   ├── ds-review/
│   │   ├── SKILL.md                             # NEW — lead orchestrator pipeline + entry logic
│   │   └── references/
│   │       ├── framework.md                     # COPY from shared/skills/ds-review-framework/SKILL.md
│   │       ├── analysis-reviewer.md             # COPY from agents/ds-review/analysis-reviewer.md
│   │       ├── communication-reviewer.md        # COPY from agents/ds-review/communication-reviewer.md
│   │       └── domain-expert-reviewer.md        # COPY from agents/ds-review/domain-expert-reviewer.md
│   └── search-domain-knowledge/
│       ├── SKILL.md                             # COPY+EDIT from shared/skills/search-domain-knowledge/SKILL.md
│       ├── references/
│       │   └── domain-index.yaml                # COPY from shared/skills/search-domain-knowledge/config/domain-index.yaml
│       └── digests/
│           ├── search-ranking.md                # COPY from shared/skills/search-domain-knowledge/digests/search-ranking.md
│           ├── query-understanding.md           # COPY
│           └── search-cross-domain.md           # COPY
```

### Files to Remove (After Verification)

```
agents/                                          # REMOVE entirely — migrated to skills/
shared/skills/                                   # REMOVE — migrated to skills/
plugin/                                          # REMOVE — old v1 distribution structure
dist/                                            # REMOVE — old v1 distribution package
ds-analysis-review-agent-structure.md            # REMOVE — old design doc at repo root, superseded by docs/plans/
```

Note: `.claude/commands/ds-review.md` is KEPT and EDITED (not removed).

### Files That Stay Unchanged

```
dev/                                             # Development artifacts — not part of plugin
docs/                                            # Design docs — not part of plugin
CLAUDE.md                                        # Project instructions (update path refs)
README.md                                        # Project README (update structure section)
CHANGELOG.md                                     # Changelog
.gitignore                                       # Git config
```

### Path Reference Updates

Claude Code resolves paths in SKILL.md **relative to the skill directory** for co-located files.
Cross-skill and command references use **project-relative paths** (no `${CLAUDE_PLUGIN_ROOT}`).

**Within ds-review skill (SKILL.md and references/*.md):**

| Old Path | New Path (skill-relative) | Context |
|---|---|---|
| `shared/skills/ds-review-framework/SKILL.md` | `references/framework.md` | Within ds-review skill |
| `agents/ds-review/analysis-reviewer.md` | `references/analysis-reviewer.md` | Within ds-review skill |
| `agents/ds-review/communication-reviewer.md` | `references/communication-reviewer.md` | Within ds-review skill |
| `agents/ds-review/domain-expert-reviewer.md` | `references/domain-expert-reviewer.md` | Within ds-review skill |
| `agents/ds-review/[your-agent-name].md` | `references/[your-agent-name].md` | Within ds-review skill |

**Cross-skill references (ds-review → search-domain-knowledge) — project-relative:**

| Old Path | New Path (project-relative) | Context |
|---|---|---|
| `shared/skills/search-domain-knowledge/digests/{domain}.md` | `skills/search-domain-knowledge/digests/{domain}.md` | Cross-skill |
| `shared/skills/search-domain-knowledge/digests/search-cross-domain.md` | `skills/search-domain-knowledge/digests/search-cross-domain.md` | Cross-skill |
| `shared/skills/search-domain-knowledge/config/domain-index.yaml` | `skills/search-domain-knowledge/references/domain-index.yaml` | Cross-skill |

**Within search-domain-knowledge skill (SKILL.md):**

| Old Path | New Path (skill-relative) | Context |
|---|---|---|
| `shared/skills/search-domain-knowledge/config/domain-index.yaml` | `references/domain-index.yaml` | Within skill |
| `shared/skills/search-domain-knowledge/digests/` | `digests/` | Within skill |

**In commands (commands/ds-review.md):**

| Reference | Path (project-relative) |
|---|---|
| SKILL.md | `skills/ds-review/SKILL.md` |
| Framework | `skills/ds-review/references/framework.md` |
| Analysis reviewer | `skills/ds-review/references/analysis-reviewer.md` |
| Communication reviewer | `skills/ds-review/references/communication-reviewer.md` |
| Domain expert reviewer | `skills/ds-review/references/domain-expert-reviewer.md` |

**In subagent dispatch payloads (from SKILL.md Step 7):**
Subagents run in the project working directory. Dispatch payloads use project-relative paths.

---

## Chunk 0: Plugin Discovery Validation (GATE — must pass before proceeding)

### Task 0: Validate plugin discovery mechanism

Before moving any files, confirm that Claude Code will recognize the new plugin structure.

- [ ] **Step 1: Check how existing plugins are registered**

```bash
cat ~/.claude/plugins/installed_plugins.json | python3 -m json.tool | head -30
```

Observe the registry format: plugins are registered as `name@marketplace` with an `installPath`.

- [ ] **Step 2: Check if Claude Code recognizes project-local plugins**

```bash
# Does a .claude-plugin/ at project root get recognized?
claude plugin list 2>/dev/null || echo "Check plugin list manually in Claude Code session"
```

Also check whether the existing `plugin/.claude-plugin/plugin.json` in this repo is currently
being loaded by Claude Code as a project-local plugin.

- [ ] **Step 3: Validate path resolution for skill files**

Create a minimal test to confirm how paths resolve in SKILL.md:
```bash
# Check how superpowers references companion files (should be skill-relative)
grep -r "references/\|@" ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.0.2/skills/test-driven-development/SKILL.md | head -5
```

Confirm: paths in SKILL.md resolve relative to the skill directory, not plugin root.

- [ ] **Step 4: Confirm project-relative paths work for subagents**

When the lead orchestrator dispatches subagents via the Task tool, subagents inherit the project
working directory. Confirm this by checking that previous ds-review runs (R4 calibration)
successfully had subagents read files at project-relative paths like `agents/ds-review/analysis-reviewer.md`.

This is the existing behavior — we are preserving it, just changing the paths from `agents/` to `skills/`.

- [ ] **Step 5: Decision gate**

If Steps 1-4 confirm:
- `.claude/commands/ds-review.md` is auto-discovered as a project command (already working)
- Skill-relative paths resolve correctly within skill directories
- Subagents can read files via project-relative paths (already working)

→ **PROCEED** to Chunk 1.

If any mechanism doesn't work as expected:
→ **STOP.** Diagnose the gap and revise the plan before moving files. The old structure still works.

---

## Chunk 1: Plugin Scaffold + ds-review Skill

### Task 1: Create plugin.json

**Files:**
- Create: `.claude-plugin/plugin.json`

- [ ] **Step 1: Create directory**

```bash
mkdir -p .claude-plugin
```

- [ ] **Step 2: Write plugin.json**

```json
{
  "name": "ds-productivity",
  "description": "DS productivity skill set — review DS analyses across methodology, communication, and domain expertise. Shared search domain knowledge for consistent expertise.",
  "version": "0.6.0",
  "author": {
    "name": "surahli"
  },
  "license": "MIT",
  "keywords": ["data-science", "review", "search-relevance", "domain-knowledge", "analysis"]
}
```

Version note: 0.6.0 because this is the first plugin-structured release, succeeding the v0.5 agent-based structure.

- [ ] **Step 3: Verify plugin.json is valid JSON**

Run: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('VALID')"`
Expected: `VALID`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "chore: add plugin.json for ds-productivity skill set"
```

---

### Task 2: Create ds-review SKILL.md

**Files:**
- Create: `skills/ds-review/SKILL.md`
- Source: `agents/ds-review/ds-review-lead.md` (290 lines — becomes the skill body)

The SKILL.md body IS the lead orchestrator pipeline. The key change is:
1. Add proper skill frontmatter (name + description)
2. Update all internal file paths from old to new structure
3. Remove the old frontmatter format and replace with skill frontmatter

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/ds-review/references
```

- [ ] **Step 2: Write SKILL.md**

Copy the full content of `agents/ds-review/ds-review-lead.md` into `skills/ds-review/SKILL.md` with these modifications:

**Frontmatter** — replace the old agent frontmatter:
```yaml
---
name: ds-review
description: >
  Review completed DS analyses across methodology, logic, communication, and domain expertise.
  Dispatches parallel reviewer subagents (analysis, communication, domain) and produces a unified
  scored review. Use when user asks to review, score, or evaluate a data science analysis document
  via /ds-review command or by asking to review a DS analysis. Supports --mode, --audience,
  --workflow, --domain flags.
---
```

**Path updates** — SKILL.md paths resolve relative to the skill directory. Cross-skill refs use project-relative paths.

**Within-skill references (skill-relative):**

| Old | New |
|---|---|
| `shared/skills/ds-review-framework/SKILL.md` | `references/framework.md` |
| `agents/ds-review/analysis-reviewer.md` | `references/analysis-reviewer.md` |
| `agents/ds-review/communication-reviewer.md` | `references/communication-reviewer.md` |
| `agents/ds-review/domain-expert-reviewer.md` | `references/domain-expert-reviewer.md` |
| `agents/ds-review/[your-agent-name].md` | `references/[your-agent-name].md` |

**Cross-skill references (project-relative paths):**

| Old | New |
|---|---|
| `shared/skills/search-domain-knowledge/digests/{domain}.md` | `skills/search-domain-knowledge/digests/{domain}.md` |
| `shared/skills/search-domain-knowledge/digests/search-cross-domain.md` | `skills/search-domain-knowledge/digests/search-cross-domain.md` |
| `shared/skills/search-domain-knowledge/config/domain-index.yaml` | `skills/search-domain-knowledge/references/domain-index.yaml` |

**Subagent dispatch payloads (Step 7):** Subagents run in project working directory. Use
project-relative paths:
- `skills/ds-review/references/analysis-reviewer.md`
- `skills/ds-review/references/framework.md`
- etc.

**Body edits:**
- In the Role section, add after the first paragraph: "Reference files are in `references/` (relative to this skill directory). The review framework (rubrics, deductions, credits) is at `references/framework.md`."
- Remove `auto_activate: true` if present (skills don't use this field)
- Change `/ds-review:review` → `/ds-review` at these locations (4 instances in output templates):
  - Line 161: Level 2 defer message
  - Line 259: Quick mode footer ("Run `/ds-review --mode full`...")
  - Line 270: Level 1 degraded output message
  - Line 271: Level 2 degraded output message
  **Note:** This is intentional — the new plugin command is `/ds-review`, not `/ds-review:review`.
- Also replace all bare `SKILL.md` references that mean the framework → `framework.md`
  (same disambiguation as Task 3 — the orchestrator body also references framework sections)

- [ ] **Step 3: Verify line count**

Run: `wc -l skills/ds-review/SKILL.md`
Expected: ~290-300 lines (under 500 limit)

- [ ] **Step 4: Verify all paths reference new locations**

Run: `grep -n "shared/skills\|agents/ds-review\|plugin/" skills/ds-review/SKILL.md`
Expected: No matches (all old paths replaced)

- [ ] **Step 5: Commit**

```bash
git add skills/ds-review/SKILL.md
git commit -m "feat(ds-review): create SKILL.md from lead orchestrator with updated paths"
```

---

### Task 3: Copy reviewer agent prompts to references

**Files:**
- Create: `skills/ds-review/references/analysis-reviewer.md`
- Create: `skills/ds-review/references/communication-reviewer.md`
- Create: `skills/ds-review/references/domain-expert-reviewer.md`
- Source: `agents/ds-review/*.md` (3 files, 161+113+144 = 418 lines total)

These files are copied verbatim — their content is calibrated through 4 rounds and must not change. The only modifications are internal path references.

- [ ] **Step 1: Copy all three reviewer files**

```bash
cp agents/ds-review/analysis-reviewer.md skills/ds-review/references/
cp agents/ds-review/communication-reviewer.md skills/ds-review/references/
cp agents/ds-review/domain-expert-reviewer.md skills/ds-review/references/
```

- [ ] **Step 2: Update path references in all three files**

In each file, apply TWO categories of replacements:

**Category A — Full path references (use skill-relative paths):**
- `shared/skills/ds-review-framework/SKILL.md` → `references/framework.md`
- `agents/ds-review/` → `references/`
- `ds-review-framework SKILL.md` → `framework.md (at references/framework.md)`

Note: Reviewer files live inside `skills/ds-review/references/`, so their references to sibling
files use just `framework.md` (same directory). References to their own location are unnecessary.

**Category B — Bare `SKILL.md` references (CRITICAL: disambiguate):**
After migration, there are TWO `SKILL.md` files: the orchestrator (`skills/ds-review/SKILL.md`) and the
framework (now `skills/ds-review/references/framework.md`). All bare `SKILL.md` references in reviewer
files historically meant the framework. They MUST be updated to `framework.md` to avoid ambiguity.

Replace ALL instances of bare `SKILL.md` → `framework.md` in all three reviewer files:
- `SKILL.md Section 1` → `framework.md Section 1`
- `SKILL.md Section 2` → `framework.md Section 2`
- `SKILL.md Section 2b` → `framework.md Section 2b`
- `SKILL.md Section 4` → `framework.md Section 4`
- `SKILL.md Section 5` → `framework.md Section 5`
- `SKILL.md Section 6` → `framework.md Section 6`
- `SKILL.md deduction table` → `framework.md deduction table`
- Any other bare `SKILL.md` reference → `framework.md`

Approximate instance counts:
- `analysis-reviewer.md`: ~12 instances of bare `SKILL.md`
- `communication-reviewer.md`: ~9 instances
- `domain-expert-reviewer.md`: ~14 instances

- [ ] **Step 3: Verify no old paths remain**

Run: `grep -rn "shared/skills\|agents/ds-review\|plugin/" skills/ds-review/references/`
Expected: No matches

- [ ] **Step 4: Verify line counts match originals (±5 lines for path edits)**

Run: `wc -l skills/ds-review/references/*.md`
Expected: analysis ~161, communication ~113, domain-expert ~144

- [ ] **Step 5: Commit**

```bash
git add skills/ds-review/references/analysis-reviewer.md
git add skills/ds-review/references/communication-reviewer.md
git add skills/ds-review/references/domain-expert-reviewer.md
git commit -m "feat(ds-review): copy reviewer subagent prompts to skill references"
```

---

### Task 4: Copy review framework to references

**Files:**
- Create: `skills/ds-review/references/framework.md`
- Source: `shared/skills/ds-review-framework/SKILL.md` (338 lines)

The framework is copied with minimal changes — remove skill frontmatter (it's no longer a standalone skill, it's a reference file), keep all section numbering intact.

- [ ] **Step 1: Copy framework file**

```bash
cp shared/skills/ds-review-framework/SKILL.md skills/ds-review/references/framework.md
```

- [ ] **Step 2: Remove skill frontmatter from framework.md**

Remove the YAML frontmatter block (lines 1-12) from `skills/ds-review/references/framework.md`. The file should start directly with `# DS Review Framework`. This file is now a reference document, not a skill — it doesn't need name/description/auto_activate.

- [ ] **Step 3: Update internal references**

Replace any path references within framework.md:
- References to agent file paths should use the new `skills/ds-review/references/` paths
- Section numbering (Section 1-8) must stay identical — all reviewer agents reference these

- [ ] **Step 4: Verify section numbering is intact**

Run: `grep -n "^## " skills/ds-review/references/framework.md`
Expected: 8 sections matching the original (1. Severity Definitions through 8. Confluence Structure Guide)

- [ ] **Step 5: Verify line count**

Run: `wc -l skills/ds-review/references/framework.md`
Expected: ~326 lines (338 minus frontmatter)

- [ ] **Step 6: Commit**

```bash
git add skills/ds-review/references/framework.md
git commit -m "feat(ds-review): copy review framework as skill reference"
```

---

## Chunk 2: search-domain-knowledge Skill

### Task 5: Create search-domain-knowledge skill

**Files:**
- Create: `skills/search-domain-knowledge/SKILL.md`
- Create: `skills/search-domain-knowledge/references/domain-index.yaml`
- Create: `skills/search-domain-knowledge/digests/search-ranking.md`
- Create: `skills/search-domain-knowledge/digests/query-understanding.md`
- Create: `skills/search-domain-knowledge/digests/search-cross-domain.md`
- Source: `shared/skills/search-domain-knowledge/` (entire directory, ~1,786 lines total)

- [X] **Step 1: Create directory structure**

```bash
mkdir -p skills/search-domain-knowledge/references
mkdir -p skills/search-domain-knowledge/digests
```

- [X] **Step 2: Copy SKILL.md with path updates**

```bash
cp shared/skills/search-domain-knowledge/SKILL.md skills/search-domain-knowledge/SKILL.md
```

Update paths in `skills/search-domain-knowledge/SKILL.md` (use skill-relative paths):

| Old | New (skill-relative) |
|---|---|
| `shared/skills/search-domain-knowledge/SKILL.md` | (self-reference — remove or use "this file") |
| `shared/skills/search-domain-knowledge/config/domain-index.yaml` | `references/domain-index.yaml` |
| `shared/skills/search-domain-knowledge/digests/` | `digests/` |
| `shared/skills/search-domain-knowledge/digests/search-ranking.md` | `digests/search-ranking.md` |
| `shared/skills/search-domain-knowledge/digests/query-understanding.md` | `digests/query-understanding.md` |
| `shared/skills/search-domain-knowledge/digests/search-cross-domain.md` | `digests/search-cross-domain.md` |

Remove `auto_activate: true` from frontmatter (not a valid skill field).

Update the "Key files" section to reflect new skill-relative paths.

Update the "Architecture context" to note that Layer 2 and Layer 3 are now implemented (not future):
- Layer 2: Domain Expert Reviewer → `skills/ds-review/references/domain-expert-reviewer.md`
- Layer 3: Lead agent integration → `ds-productivity:ds-review` skill

- [X] **Step 3: Copy domain-index.yaml**

```bash
cp shared/skills/search-domain-knowledge/config/domain-index.yaml skills/search-domain-knowledge/references/domain-index.yaml
```

No content changes needed — the YAML is self-contained.

- [X] **Step 4: Copy all digest files**

```bash
cp shared/skills/search-domain-knowledge/digests/search-ranking.md skills/search-domain-knowledge/digests/
cp shared/skills/search-domain-knowledge/digests/query-understanding.md skills/search-domain-knowledge/digests/
cp shared/skills/search-domain-knowledge/digests/search-cross-domain.md skills/search-domain-knowledge/digests/
```

No content changes — digests are self-contained documents.

- [X] **Step 5: Verify all files exist and match originals**

Run:
```bash
diff <(wc -l shared/skills/search-domain-knowledge/digests/*.md | tail -1) \
     <(wc -l skills/search-domain-knowledge/digests/*.md | tail -1)
```
Expected: Same total line count (1241)

Run: `wc -l skills/search-domain-knowledge/SKILL.md`
Expected: ~290-310 lines (original 302 ± edits for path updates and architecture context)

Run: `wc -l skills/search-domain-knowledge/references/domain-index.yaml`
Expected: 243 lines

- [X] **Step 6: Verify no old paths remain in SKILL.md**

Run: `grep -n "shared/skills" skills/search-domain-knowledge/SKILL.md`
Expected: No matches

- [X] **Step 7: Commit**

```bash
git add skills/search-domain-knowledge/
git commit -m "feat(search-domain-knowledge): create skill with digests and domain index"
```

---

## Chunk 3: Command + Cleanup + Verification

### Task 6: Create thin command wrapper

**Files:**
- Create: `commands/ds-review.md`

The command is a genuinely thin entry point — 5 lines, not 40. All logic lives in SKILL.md (single
source of truth). The command just loads the skill and passes arguments.

**Dependency:** Requires Tasks 2-4 to be complete (command references files created in those tasks).

Commands run in the project working directory, so they use project-relative paths.

- [ ] **Step 1: Create commands directory**

```bash
mkdir -p commands
```

- [ ] **Step 2: Write command file**

```markdown
---
description: Review a DS analysis across methodology, logic, narrative, actionability, and domain expertise
argument-hint: [source] [--mode full|quick] [--audience exec|tech|ds|mixed] [--workflow proactive|reactive] [--domain d1,d2,...] [--reference path] [--refresh-domain domain]
model: opus
---

You are the **ds-review-lead** orchestrator. Read these files and follow them exactly:

1. `skills/ds-review/SKILL.md` — your complete 10-step review pipeline
2. `skills/ds-review/references/framework.md` — severity definitions, deduction tables, credits, floor rules

Execute the full pipeline on: $ARGUMENTS
```

Note: This EDITS the existing `.claude/commands/ds-review.md` — it does not create a new file.
The command stays at `.claude/commands/` for project-level auto-discovery.

- [ ] **Step 3: Verify command file has correct frontmatter**

Run: `head -5 commands/ds-review.md`
Expected: YAML frontmatter with description, argument-hint, model

- [ ] **Step 4: Commit**

```bash
git add commands/ds-review.md
git commit -m "feat(ds-review): create thin command wrapper for plugin"
```

---

### Task 7: Update project documentation

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`
- Modify: `.claude/rules/plugin-conventions.md`

- [ ] **Step 1: Update CLAUDE.md — all sections**

The following sections need updates (not just Agent Architecture):

**"What This Is" section:** Replace "agents" language → "skills":
```markdown
## What This Is
A Claude Code plugin (skill set) for DS productivity in Search Relevance:
- **DS Analysis Review** (`ds-productivity:ds-review`): Reviews DS analyses across methodology, logic, communication, and domain expertise
- **Search Domain Knowledge** (`ds-productivity:search-domain-knowledge`): Curated domain expertise for Search Relevance
- **SQL Review:** (Q2 2026) Reviews SQL queries for syntax and domain-specific patterns
- **Search Metric Analysis:** (Q2 2026) Analyzes search metrics and generates insights
```

**"Agent Architecture" section:** Replace with:
```markdown
## Skill Architecture

### DS Analysis Review
- skills/ds-review/SKILL.md — orchestrator (invoked via /ds-review command or ds-productivity:ds-review skill)
- skills/ds-review/references/analysis-reviewer.md — subagent for analysis dimension
- skills/ds-review/references/communication-reviewer.md — subagent for communication dimension
- skills/ds-review/references/domain-expert-reviewer.md — subagent for domain dimension (v0.5+)

### Shared References
- skills/ds-review/references/framework.md — shared rubrics and personas
- skills/search-domain-knowledge/ — Search Relevance domain expertise (v0.5+)
```

**"Current State" section:** Update to reference `dev/backlog.md` (unchanged) and latest session log.

**"Pickup Instructions" section:** Keep as-is (references dev/ files which are unchanged).

- [ ] **Step 2: Update `.claude/rules/plugin-conventions.md`**

This file is auto-loaded as a project rule and currently references old paths (`agents/[agent-name]/`,
`shared/skills/`, `.claude/commands/`, `plugin/`). Update all path conventions to the new structure:

- `agents/[agent-name]/` → `skills/[skill-name]/references/` (for subagent prompts)
- `shared/skills/[skill-name]/` → `skills/[skill-name]/` (skills are now top-level)
- `.claude/commands/` → `commands/` (plugin-level commands)
- Remove `plugin/` references (no longer applicable)
- Update the "Plugin Structure (ds-review)" section to describe the new skill structure
- Update "Skill Design" section to reference `references/` instead of separate skill directories

- [ ] **Step 2: Update README.md project structure**

Replace the Project Structure section:
```markdown
## Project Structure

ds-productivity-agents/
├── .claude-plugin/            # Plugin manifest
├── skills/                    # Skill definitions
│   ├── ds-review/             # DS Analysis Review skill
│   │   ├── SKILL.md           # Lead orchestrator pipeline
│   │   └── references/        # Reviewer prompts + framework
│   └── search-domain-knowledge/  # Domain expertise skill
│       ├── SKILL.md           # Consumption contract
│       ├── references/        # Domain index
│       └── digests/           # Domain knowledge digests
├── commands/                  # Command entry points
│   └── ds-review.md           # /ds-review command
├── dev/                       # Development artifacts
│   ├── backlog.md
│   ├── sessions/
│   ├── test-results/
│   └── decisions/
└── docs/                      # Design docs, plans
```

- [ ] **Step 3: Update README.md usage section**

Update the invocation examples:
```markdown
/ds-review path/to/analysis.md
/ds-review --domain search-ranking path/to/analysis.md
```

Or trigger the skill naturally:
```
"Review this analysis for me" → auto-triggers ds-productivity:ds-review
```

- [ ] **Step 4: Commit (include ALL modified docs)**

```bash
git add CLAUDE.md README.md .claude/rules/plugin-conventions.md
git commit -m "docs: update project docs for plugin skill set structure"
```

---

### Task 8: End-to-end verification (BEFORE deletion)

**Moved here from old Task 9:** Verify before delete — all 3 reviewers recommended this reorder.

- [ ] **Step 1: Verify plugin structure is recognized**

```bash
test -f .claude-plugin/plugin.json && echo "plugin.json: OK" || echo "MISSING"
test -d skills/ds-review && echo "ds-review skill: OK" || echo "MISSING"
test -d skills/search-domain-knowledge && echo "domain-knowledge skill: OK" || echo "MISSING"
test -f commands/ds-review.md && echo "command: OK" || echo "MISSING"
```
Expected: All OK

- [ ] **Step 2: Verify all cross-references resolve**

Run: `grep -rn "references/\|digests/" skills/ .claude/commands/ | grep -oE '(references|digests)/[^ "]+' | sort -u`

For each unique path, verify the file exists relative to its skill directory:
```bash
# Check ds-review skill references
for f in framework.md analysis-reviewer.md communication-reviewer.md domain-expert-reviewer.md; do
  test -f "skills/ds-review/references/$f" && echo "OK: $f" || echo "MISSING: $f"
done

# Check search-domain-knowledge skill references
test -f skills/search-domain-knowledge/references/domain-index.yaml && echo "OK: domain-index" || echo "MISSING"
for f in search-ranking.md query-understanding.md search-cross-domain.md; do
  test -f "skills/search-domain-knowledge/digests/$f" && echo "OK: $f" || echo "MISSING: $f"
done
```
Expected: All OK

- [ ] **Step 3: Verify total file count**

Run: `find skills/ commands/ .claude-plugin/ -type f | wc -l`
Expected: 12 files

- [ ] **Step 4: Verify migration content integrity — diff check**

```bash
# Digests (should be identical)
diff shared/skills/search-domain-knowledge/digests/search-ranking.md skills/search-domain-knowledge/digests/search-ranking.md
diff shared/skills/search-domain-knowledge/digests/query-understanding.md skills/search-domain-knowledge/digests/query-understanding.md
diff shared/skills/search-domain-knowledge/digests/search-cross-domain.md skills/search-domain-knowledge/digests/search-cross-domain.md

# Domain index (should be identical)
diff shared/skills/search-domain-knowledge/config/domain-index.yaml skills/search-domain-knowledge/references/domain-index.yaml
```
Expected: Digests and domain-index show no diff.

- [ ] **Step 5: Run /ds-review on test fixture — compare against baseline**

```
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode quick --audience tech --workflow reactive
```

Expected: Command triggers, reads SKILL.md, dispatches subagents, produces a scored review.
**Baseline comparison:** Vanguard quick score should be within ±5 of known baseline (57).
If outside this range, investigate before proceeding to deletion.

Note: May require a Claude Code session restart to pick up the new plugin structure.

- [ ] **Step 6: Verify no old paths in SKILL.md files**

Run: `grep -rn "shared/skills\|agents/ds-review\|plugin/" skills/ commands/`
Expected: No matches (all old paths replaced)

**GATE:** If Steps 1-6 all pass → proceed to Task 9 (deletion). If any fail → diagnose before deleting.

---

### Task 9: Remove old directories

**IMPORTANT:** Only execute after Task 8 verification passes. Old files remain as fallback until verified.

- [ ] **Step 1: Remove all old directories (use git rm for explicit tracking)**

```bash
git rm -r agents/
git rm -r shared/
git rm -r plugin/
git rm -r dist/
git rm ds-analysis-review-agent-structure.md
```

Note: `.claude/commands/ds-review.md` is KEPT (edited in Task 6, not removed).

Note: Removes `agents/` entirely (including sql-review and search-metric-analysis placeholders).
Future skills will be created directly under `skills/` — tracked in `dev/backlog.md`.

- [ ] **Step 2: Verify directory structure is clean**

Run: `find skills/ commands/ .claude-plugin/ -type f | sort`
Expected:
```
.claude-plugin/plugin.json
commands/ds-review.md
skills/ds-review/SKILL.md
skills/ds-review/references/analysis-reviewer.md
skills/ds-review/references/communication-reviewer.md
skills/ds-review/references/domain-expert-reviewer.md
skills/ds-review/references/framework.md
skills/search-domain-knowledge/SKILL.md
skills/search-domain-knowledge/digests/query-understanding.md
skills/search-domain-knowledge/digests/search-cross-domain.md
skills/search-domain-knowledge/digests/search-ranking.md
skills/search-domain-knowledge/references/domain-index.yaml
```

- [ ] **Step 3: Verify no dangling references to old paths in docs**

Run: `grep -rn "shared/skills\|agents/ds-review\|plugin/commands\|plugin/agents\|plugin/skills" CLAUDE.md README.md .claude/rules/`
Expected: No matches

- [ ] **Step 4: Commit removal**

```bash
git commit -m "chore: remove old agent/shared/plugin/dist directories — migrated to skills/"
```

(Files already staged via `git rm` in Step 1.)

---

### Task 10: Fix credit cap discrepancy

Per DS Lead review: fix the +25 → +15 credit cap inconsistency. One-line change in 4 files.
Files are already migrated, so edit in the new locations.

- [ ] **Step 1: Fix lead orchestrator (SKILL.md Step 9)**

In `skills/ds-review/SKILL.md`, find "capped at +25 per dimension" and change to "capped at +15 per dimension".

- [ ] **Step 2: Fix reviewer files**

In each of these files, find "capped at +25" or "Cap at +25" and change to "+15":
- `skills/ds-review/references/analysis-reviewer.md`
- `skills/ds-review/references/communication-reviewer.md`
- `skills/ds-review/references/domain-expert-reviewer.md`

- [ ] **Step 3: Verify consistency**

Run: `grep -rn "cap.*25\|capped.*25" skills/`
Expected: No matches (all changed to +15)

Run: `grep -rn "cap.*15\|capped.*15\|Maximum +15" skills/`
Expected: Matches in framework.md Section 2b AND in all 4 files above

- [ ] **Step 4: Commit**

```bash
git add skills/ds-review/SKILL.md skills/ds-review/references/analysis-reviewer.md skills/ds-review/references/communication-reviewer.md skills/ds-review/references/domain-expert-reviewer.md
git commit -m "fix(ds-review): align credit cap to +15 across all files (was +25 in 4 files, +15 in framework)"
```

---

### Task 11: Finalize — backlog, changelog, session log

- [ ] **Step 1: Update backlog and changelog**

Update `dev/backlog.md`:
- Add "v0.6: Skill Set Refactoring" section — mark as COMPLETE
- Note the migration from agents/ to skills/
- Remove `agents/sql-review/` and `agents/search-metric-analysis/` references — future skills go under `skills/`

Update `CHANGELOG.md`:
- Add v0.6.0 entry documenting the plugin restructure + credit cap fix

- [ ] **Step 2: Create session log**

Create `dev/sessions/2026-03-14-skill-set-refactoring.md` documenting:
- What was migrated
- Path mapping table (skill-relative + project-relative strategy)
- Plugin discovery validation results (Task 0)
- Vanguard baseline comparison result
- Credit cap fix (+25 → +15)
- Any issues encountered

- [ ] **Step 3: Final commit**

```bash
git add dev/backlog.md CHANGELOG.md dev/sessions/2026-03-14-skill-set-refactoring.md
git commit -m "docs: complete v0.6 skill set refactoring — session log, backlog, changelog"
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Plugin discovery doesn't work as assumed | Medium | Critical — entire migration pointless | Task 0: validate BEFORE moving files |
| Path references missed during migration | Medium | High — broken subagent dispatch | Task 8 Step 6 grep verification |
| Skill-relative vs plugin-root-relative paths wrong | Medium | High — files not found at runtime | Task 0 Step 3: validate path resolution pattern |
| Bare `SKILL.md` ambiguity (orchestrator vs framework) | High if missed | High — subagents read wrong file | Task 3 Step 2: replace ALL bare `SKILL.md` → `framework.md` |
| Framework section numbering changed | Low | High — all reviewers reference by section number | Task 4 Step 4 section count verification |
| Digest content accidentally modified | Low | Medium — calibration results invalidated | Task 8 Step 4 diff verification |
| Scoring integrity broken by path changes | Medium | High — calibration invalidated | Task 8 Step 5: Vanguard baseline comparison (±5 of 57) |
| `.claude/rules/plugin-conventions.md` stale | High if missed | Medium — future sessions get wrong path guidance | Task 7 Step 2 + Step 4 commit includes it |
| Old paths in dev/ artifacts | Low | Low — dev files are historical | Not updating dev/ — they're historical records |

## Decision Log

| Decision | Rationale |
|---|---|
| Plugin name: `ds-productivity` | Matches repo purpose, enables future skills (sql-review, metric-analysis) |
| Two skills, not one | Domain knowledge is shared infrastructure, not ds-review-specific |
| Reviewer prompts as references, not skills | They're consumed by subagents, not auto-triggered |
| Framework as reference, not skill | It's a data file (rubrics/tables), not a workflow |
| Command + skill (Option C) | Explicit invocation via `/ds-review` + auto-trigger on "review this analysis" |
| Thin command (5 lines) | Single source of truth — all logic in SKILL.md, no dispatch duplication |
| Skill-relative paths | Claude Code resolves SKILL.md paths relative to skill directory. Confirmed by superpowers pattern. |
| Project-relative paths for cross-skill | `${CLAUDE_PLUGIN_ROOT}` unreliable (removed by planning-with-files plugin). Project-relative paths work because command/orchestrator run in project root. |
| Verify before delete | Task 8 (verification) before Task 9 (deletion). Unanimous reviewer recommendation. |
| Remove `agents/` entirely | No orphaned placeholder directories. Future skills tracked in backlog only. |
| Fix credit cap +25 → +15 | DS Lead: one-line fix in 4 files, files already open, avoids carrying known discrepancy. |
| Content unchanged (except credit cap) | 4 calibration rounds validated — restructure only, credit cap is a bug fix not a rewrite |
| Version 0.6.0 | First plugin-structured release, follows v0.5 agent-based |
| Task 0 gate | Validate plugin discovery mechanism before moving any files. All 3 reviewers flagged this. |
