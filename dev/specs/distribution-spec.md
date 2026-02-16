# Distribution Spec: DS Review Plugin

**Status:** Draft — implement after `/ds-review` command is tested locally
**Goal:** Make the plugin installable by anyone via `claude plugins install`

---

## Overview

To distribute the plugin, we need to:
1. Create a standalone GitHub repo with the plugin at root level
2. Change 3 hardcoded `plugin/` paths to use `${CLAUDE_PLUGIN_ROOT}`
3. Rewrite the command for the plugin context (no longer project-level)

---

## Step 1: Create GitHub Repo

Create a new repo (e.g., `surahli/ds-review-plugin`) with this structure:

```
ds-review-plugin/                   ← repo root IS the plugin root
├── .claude-plugin/
│   └── plugin.json                 ← already correct
├── commands/
│   └── review.md                   ← rewritten for plugin context
├── agents/
│   ├── ds-review-lead.md           ← copy from plugin/agents/
│   ├── analysis-reviewer.md        ← copy from plugin/agents/
│   └── communication-reviewer.md   ← copy from plugin/agents/
├── skills/
│   └── ds-review-framework/
│       └── SKILL.md                ← copy from plugin/skills/
└── README.md                       ← usage instructions
```

**Key difference from current structure:** The repo root IS the plugin root. No `plugin/` subdirectory.

---

## Step 2: Path Changes (3 files)

### Change 1: `commands/review.md` (rewrite for plugin context)

The command uses `${CLAUDE_PLUGIN_ROOT}` to reference files portably:

```markdown
---
description: Review a DS analysis across methodology, logic, narrative, and actionability
argument-hint: [source] [--mode full|quick] [--audience exec|tech|ds|mixed] [--workflow proactive|reactive]
model: opus
---

You are the **ds-review-lead** orchestrator for a DS analysis review system.

## Setup

Before doing anything else, read these two files in parallel:
1. `${CLAUDE_PLUGIN_ROOT}/agents/ds-review-lead.md` — your complete 10-step review pipeline
2. `${CLAUDE_PLUGIN_ROOT}/skills/ds-review-framework/SKILL.md` — severity definitions, deduction tables, strength credits, floor rules

These are your authoritative instructions. Follow them exactly.

## Review Request

Execute the full 10-step pipeline from `ds-review-lead.md` on this input:

**Source and options:** $ARGUMENTS

## Subagent Dispatch

When you reach Step 7 (Dispatch Subagents), use the Task tool to launch two parallel agents:
- For the **analysis-reviewer**: include the full payload from Step 7, and instruct it to read `${CLAUDE_PLUGIN_ROOT}/agents/analysis-reviewer.md` and `${CLAUDE_PLUGIN_ROOT}/skills/ds-review-framework/SKILL.md`
- For the **communication-reviewer**: include the full payload from Step 7, and instruct it to read `${CLAUDE_PLUGIN_ROOT}/agents/communication-reviewer.md` and `${CLAUDE_PLUGIN_ROOT}/skills/ds-review-framework/SKILL.md`

## Key Reminders

- You orchestrate only — NEVER review the analysis directly
- Both subagents MUST produce a STRENGTH LOG (Section 2b of SKILL.md)
- Apply diminishing returns and duplicate suppression in Step 9
- Cap displayed findings at 10 total (scoring uses all findings)
- Always include positive findings — non-negotiable
```

### Change 2: `agents/ds-review-lead.md` — Step 7 payload paths

In the subagent dispatch payload (Step 7), change:

```
# FROM:
plugin/skills/ds-review-framework/SKILL.md
plugin/agents/[your-agent-name].md

# TO:
${CLAUDE_PLUGIN_ROOT}/skills/ds-review-framework/SKILL.md
${CLAUDE_PLUGIN_ROOT}/agents/[your-agent-name].md
```

This is the only change needed in the lead agent file.

### Change 3: `agents/ds-review-lead.md` — Step 8 footer path

In Step 8 and Step 10 output, change:

```
# FROM:
/ds-review:review

# TO:
/review
```

The command name changes because plugin commands use the filename (`review.md` → `/review`), not a namespace prefix.

---

## Step 3: Update plugin.json

The existing `plugin.json` is almost correct. Small cleanups:

```json
{
  "name": "ds-review",
  "version": "0.4.0",
  "description": "Review DS analyses across methodology, logic, narrative, and actionability dimensions",
  "author": {
    "name": "surahli"
  },
  "repository": "https://github.com/surahli/ds-review-plugin",
  "license": "MIT",
  "keywords": ["data-science", "analysis", "review", "methodology", "communication"]
}
```

Note: `agents`, `commands`, `skills` fields removed — Claude Code auto-discovers from default directories.

---

## Step 4: How Users Install

```bash
# Install the plugin
claude plugins install surahli/ds-review-plugin

# Use it
/review myanalysis.md --mode full --audience exec
```

That's it. One command to install, one command to use.

---

## What Stays the Same

- All agent prompt content (analysis-reviewer.md, communication-reviewer.md)
- All SKILL.md content (rubrics, deductions, credits)
- The 10-step pipeline logic
- Scoring mechanics (DR, credits, floor rules)

Only FILE PATHS change — the actual logic is untouched.

---

## Testing Before Distribution

1. Test `/ds-review` locally first (project command)
2. Once confirmed working, create the GitHub repo
3. Install your own plugin: `claude plugins install surahli/ds-review-plugin`
4. Test `/review` (plugin command)
5. Run at least 2 test fixtures to verify scores match
6. Write README with usage instructions
7. Share the repo URL

---

## Timeline

- **Now:** Test `/ds-review` locally (project command)
- **After local test passes:** Create distribution repo (30 min of work)
- **After R4 calibration:** Publish for community use
