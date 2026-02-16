# Plugin Registration Process

**Created:** 2026-02-15
**Status:** Project-level command registered, pending restart test
**Command:** `/ds-review`

---

## How Claude Code Discovers Commands, Skills, and Agents

Claude Code has three discovery mechanisms for commands:

| Type | Location | Label in /help | Scope |
|------|----------|---------------|-------|
| **Project command** | `.claude/commands/*.md` | (project) | Current project only |
| **Personal command** | `~/.claude/commands/*.md` | (user) | All your projects |
| **Plugin command** | Installed plugin `commands/` | (plugin:name) | When plugin enabled |

**Skills** are only auto-discovered from installed plugins (`~/.claude/plugins/cache/`).
**Agents** in plugins are auto-discovered from `agents/` directories.

**Discovery timing:** Commands are loaded at session start. Adding a new command requires restarting Claude Code.

---

## What We Did

### Problem

We built a plugin at `plugin/` with the standard plugin structure:
```
plugin/
├── .claude-plugin/plugin.json    # Plugin manifest
├── commands/review.md            # Command definition (had custom `agent:` frontmatter)
├── agents/
│   ├── ds-review-lead.md         # Orchestrator
│   ├── analysis-reviewer.md      # Analysis subagent
│   └── communication-reviewer.md # Communication subagent
└── skills/ds-review-framework/
    └── SKILL.md                  # Shared rubrics
```

But `/ds-review:review` gave "Unknown skill" because:
1. **The plugin isn't installed** — files exist in the project but aren't in `~/.claude/plugins/`
2. **The `agent:` frontmatter doesn't exist** — Claude Code command frontmatter only supports: `description`, `allowed-tools`, `model`, `argument-hint`, `disable-model-invocation`
3. **The namespaced format `plugin:command`** only works for installed marketplace/GitHub plugins

### Solution: Project-Level Command

Created `.claude/commands/ds-review.md` — a project-level command that:
- Instructs Claude to read the existing agent prompt (`plugin/agents/ds-review-lead.md`)
- Instructs Claude to read the shared rubrics (`plugin/skills/ds-review-framework/SKILL.md`)
- Passes user arguments (`$ARGUMENTS`) to the pipeline
- Reminds Claude about key architectural constraints (subagent dispatch, strength logs, etc.)

**Command appears as:** `/ds-review` (project) — not `/ds-review:review`

### Why `/review` didn't work

Our first attempt named the command `review.md`. This collided with the `review` skill from the installed `code-review@context-engineering-kit` plugin. Claude Code matched the plugin skill instead of our project command. Renamed to `ds-review.md` to avoid the collision.

---

## Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `.claude/commands/ds-review.md` | **Created** | Project-level command — entry point for reviews |
| `plugin/commands/review.md` | Unchanged | Original command definition (kept for future plugin install) |
| `plugin/.claude-plugin/plugin.json` | Unchanged | Plugin manifest (kept for future plugin install) |

---

## How to Test

### After restarting Claude Code:

```bash
# 1. Check the command appears in help
/help
# Look for: /ds-review (project) — Review a DS analysis...

# 2. Quick test with Vanguard fixture
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode quick --audience tech --workflow reactive

# 3. Full test
/ds-review dev/test-fixtures/real/vanguard-ab-test.md --mode full --audience tech --workflow reactive
```

### What to verify:
- [ ] Command appears in `/help` output
- [ ] Command triggers ds-review-lead orchestration (reads agent prompt)
- [ ] Two subagents are dispatched in parallel via Task tool
- [ ] Review output follows the Step 10 format from ds-review-lead.md
- [ ] Score calculation includes diminishing returns and strength credits

### If something goes wrong:

**"Unknown skill" on /ds-review:**
- Verify file exists: `ls .claude/commands/ds-review.md`
- Restart Claude Code (commands load at startup)

**Command loads but doesn't follow the agent pipeline:**
- The command instructs Claude to READ the agent prompt file. If Claude skips this, the command prompt may need to embed the instructions directly instead of referencing them.
- Fallback: use `@plugin/agents/ds-review-lead.md` syntax in the command to embed the file contents inline.

**Subagents don't produce proper output:**
- Check that the Task tool payload includes instructions to read both the agent prompt AND SKILL.md
- This is specified in the command's "Subagent Dispatch" section

---

## Future: Upgrading to Full Plugin Install (Option B)

When ready to distribute the plugin or get the `ds-review:review` namespacing:

### Option 1: GitHub repo install
```bash
# 1. Push plugin/ directory to a GitHub repo
# 2. The repo root should contain:
#    .claude-plugin/plugin.json, commands/, agents/, skills/
# 3. Install:
claude plugins install your-username/ds-review-plugin
# 4. Plugin appears in ~/.claude/settings.json under enabledPlugins
```

### Option 2: Local marketplace
```bash
# 1. Create ~/.claude/plugins/marketplaces/local/
# 2. Add marketplace.json and symlink/copy the plugin
# 3. Add to enabledPlugins in ~/.claude/settings.json
```

### What changes with full plugin install:
- Command becomes `/review (plugin:ds-review)` instead of `/ds-review (project)`
- SKILL.md auto-activates (no explicit read needed)
- Agents are auto-discovered
- `${CLAUDE_PLUGIN_ROOT}` variable available for portable paths
- Plugin can be shared with others via `claude plugins install`

---

## Key Learnings

1. **Claude Code plugin system is marketplace-driven** — plugins install from GitHub repos or official marketplace, not from local project directories.

2. **Project commands are the simplest path** — `.claude/commands/` works immediately for project-specific tools. No installation or configuration needed.

3. **Command frontmatter is limited** — only 5 fields recognized. Custom fields like `agent:` and `name:` are silently ignored. The command body must contain all instructions.

4. **Naming conflicts are real** — if your command name matches a skill from any installed plugin, the plugin skill wins. Use distinctive names.

5. **Commands are prompts** — a command file is literally a prompt that Claude receives. Write it as instructions TO Claude, not documentation FOR humans.

6. **Discovery is at startup** — new commands require restarting Claude Code. This is the same for project commands and plugin commands.

---

## Architecture: How It All Connects

```
User types: /ds-review myfile.md --mode full --audience tech

                    ┌─────────────────────────┐
                    │  .claude/commands/       │
                    │  ds-review.md            │ ← Claude Code loads this at startup
                    │  (project command)       │
                    └──────────┬──────────────┘
                               │ Claude reads instructions
                               ▼
                    ┌─────────────────────────┐
                    │  plugin/agents/          │
                    │  ds-review-lead.md       │ ← 10-step pipeline
                    │  (orchestrator)          │
                    └──────────┬──────────────┘
                               │ Step 7: dispatch
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐  ┌──────────────────────┐
          │ analysis-       │  │ communication-        │
          │ reviewer.md     │  │ reviewer.md           │
          │ (Task tool)     │  │ (Task tool)           │
          └────────┬────────┘  └──────────┬────────────┘
                   │                      │
                   │  Both read:          │
                   ▼                      ▼
          ┌─────────────────────────────────────┐
          │  plugin/skills/ds-review-framework/ │
          │  SKILL.md                           │ ← Shared rubrics
          │  (severity, deductions, credits)    │
          └─────────────────────────────────────┘
```
