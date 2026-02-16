# Session Pickup: Plugin Registration Testing

**Context:** You're picking up the DS Analysis Review Agent project. R3 calibration is complete (6 test fixtures reviewed, scores documented, fix plan ready). The system is production-ready but the plugin is NOT yet registered, which means the `/ds-review:review` command and skills don't work yet.

**Your task:** Test plugin registration process so the review command can be invoked properly.

---

## Quick Background

This is a Claude Code plugin that reviews DS analyses across two dimensions:
- **Analysis:** methodology, logic, completeness, metrics
- **Communication:** structure, audience fit, conciseness, actionability

**Architecture:**
- 1 lead agent (`ds-review-lead`) orchestrates the review
- 2 subagent reviewers (`analysis-reviewer`, `communication-reviewer`) run in parallel
- 1 shared skill (`ds-review-framework`) contains scoring rubrics
- 1 command (`review`) invokes the lead agent

**Current state:**
- All code is written and committed on branch `feat/v0.4.1-credit-redesign`
- R3 calibration complete (scores: 63-100, slight inflation but acceptable)
- Plugin files exist but are NOT registered in the Claude Code system
- Attempted to invoke `/ds-review:review` in prior session → failed with "Unknown skill"

---

## What You Need to Do

### Step 1: Understand Plugin Registration Requirements

**Research question:** How do Claude Code plugins get registered?

Look for:
- Official Claude Code plugin documentation
- Plugin registration process/commands
- Directory structure requirements (we have `plugin/.claude-plugin/plugin.json`)
- Whether there's a CLI command to register a local plugin
- Whether plugins auto-load from specific directories

**Key files to examine:**
- `plugin/.claude-plugin/plugin.json` (our plugin manifest)
- `plugin/commands/review.md` (command definition)
- `plugin/agents/*.md` (3 agent prompts)
- `plugin/skills/ds-review-framework/SKILL.md` (shared rubrics)

### Step 2: Test Plugin Registration

Once you understand the process:
1. Register the plugin (if there's a registration command)
2. Verify the plugin is loaded (`/skills` command or similar)
3. Test invoking the review command:
   ```
   /ds-review:review dev/test-fixtures/real/vanguard-ab-test.md --mode full --audience tech --workflow reactive
   ```
4. Verify the command triggers the ds-review-lead agent
5. Confirm the agent can read SKILL.md and dispatch subagents

### Step 3: Document the Process

Create a document:
- `dev/PLUGIN-REGISTRATION-PROCESS.md`
- Step-by-step instructions for registering the plugin
- Any issues encountered and how to fix them
- Verification steps to confirm it's working
- Update `dev/PICKUP.md` with plugin registration status

---

## Files to Read First

**Priority 1 (context):**
1. `dev/PICKUP.md` - Where we left off
2. `dev/backlog.md` - Current priorities
3. `CLAUDE.md` - Project instructions

**Priority 2 (plugin structure):**
4. `plugin/.claude-plugin/plugin.json` - Plugin manifest
5. `plugin/commands/review.md` - Command definition
6. `.claude/rules/plugin-conventions.md` - Our plugin conventions

**Priority 3 (testing):**
7. `dev/test-fixtures/real/vanguard-ab-test.md` - Test fixture to use

---

## Expected Outcome

By end of session, you should have:
- ✅ Understanding of Claude Code plugin registration
- ✅ Plugin registered and loaded
- ✅ `/ds-review:review` command working
- ✅ Test run on Vanguard fixture (or at least command invocation works)
- ✅ Documentation of the process in `dev/PLUGIN-REGISTRATION-PROCESS.md`
- ✅ Updated `dev/PICKUP.md` with registration status

---

## Why This Matters

**The problem:** In the prior session, we invoked reviews using the Task tool with general-purpose agents. This works but is inefficient:
```
# What we did (workaround):
Task tool → general-purpose agent → "pretend to be ds-review-lead" → run review

# What we want (proper):
/ds-review:review <file> → ds-review-lead agent → review
```

**The blocker:** Skills and commands don't work until the plugin is registered. We need to figure out how to register it.

**Once working:** We can run calibration rounds more efficiently and users can invoke reviews with simple commands.

---

## Troubleshooting Tips

If registration fails:
1. Check if `plugin.json` format is correct
2. Verify all referenced files exist (agents, commands, skills)
3. Look for Claude Code plugin logs/debug output
4. Try restarting Claude Code session after registration
5. Check if there's a plugin validation command

If command invocation fails:
1. Verify the command name matches `plugin/commands/review.md` frontmatter
2. Check if agents can be found at their paths
3. Test if SKILL.md is accessible from agent context
4. Look for error messages about missing dependencies

---

## Important Notes

- **Don't re-run calibration yet** - Just test registration and basic command invocation
- **Don't modify plugin code** - It's already complete and tested
- **Do document everything** - Next session will use your process notes
- **Branch:** Stay on `feat/v0.4.1-credit-redesign`

---

## Quick Commands to Start

```bash
# Check current state
git status
git branch

# Read context
cat dev/PICKUP.md
cat dev/backlog.md

# Check plugin structure
ls -la plugin/
cat plugin/.claude-plugin/plugin.json

# After registration, test with:
/ds-review:review dev/test-fixtures/real/vanguard-ab-test.md --mode full --audience tech --workflow reactive
```

---

## Success Criteria

You know you're done when:
1. The `/ds-review:review` command is recognized (not "Unknown skill")
2. The command triggers the ds-review-lead agent
3. You can see the agent dispatch subagents
4. A review output is generated (even if it fails partway through)
5. You have clear documentation of how to register plugins

**Questions to answer:**
- How do you register a Claude Code plugin?
- Does it require a specific directory structure?
- Are there any config files needed?
- How do you verify a plugin is loaded?
- How do you troubleshoot registration issues?
