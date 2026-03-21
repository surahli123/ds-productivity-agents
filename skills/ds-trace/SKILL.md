---
name: ds-trace
description: >
  Trace coding agent work during data analysis — captures decisions, reasoning,
  tool usage, and engineering metrics for compound learning. Use this skill whenever
  a data scientist starts an analysis session and wants observability into how the
  coding agent works. Trigger when: the user says "trace", "start tracing",
  "observe my session", "log what you do", "ds-trace", or wants to reflect on
  how an analysis session went. Also trigger when the user asks to "reflect",
  "review what went wrong", "extract learnings", or "what did we learn".
  Two modes: `start` (begin tracing) and `reflect` (extract learnings at session end).
metadata:
  pattern: pipeline+generator+reviewer
  version: "0.7.0"
---

# DS Trace — Agent Observability for Data Analysis

You are the **ds-trace** orchestrator. You help data scientists observe and learn from
how coding agents work during analysis sessions.

**Two modes:**
- `start` — Begin tracing. Creates a trace file, injects tracing instructions.
- `reflect` — End-of-session reflection. Reads the trace, extracts compound learnings.

---

## Mode Routing

Parse the first argument from `$ARGUMENTS` to determine the mode:

- If the first word is `start` → execute **Start Mode** below
- If the first word is `reflect` → execute **Reflect Mode** below
- If no argument or unclear → ask the user: "Would you like to start tracing a new
  analysis session, or reflect on a completed one?"

---

## Start Mode (Generator Pattern)

**Purpose:** Create a structured trace file and inject tracing instructions so the
agent logs its work throughout the session.

### Step 1 — Parse the topic

Extract the topic from the arguments after `start`. Examples:
- `/ds-trace start "churn analysis"` → topic = "churn analysis"
- `/ds-trace start investigating Q1 revenue drop` → topic = "investigating Q1 revenue drop"

If no topic is provided, ask: "What analysis are you working on? (e.g., 'churn analysis',
'Q1 revenue deep-dive')"

### Step 2 — Create the traces directory

Check if a `traces/` directory exists in the current project. If not, create it.

### Step 3 — Create the trace file

1. Read the trace template: `assets/trace-template.md`
2. Fill in the placeholders:
   - `{{YYYY-MM-DD}}` → today's date
   - `{{topic-slug}}` → topic converted to kebab-case (e.g., "churn-analysis")
   - `{{Topic}}` → original topic text
   - `{{objective}}` → topic text (the DS can refine this later)
3. Write to: `traces/trace-{{YYYY-MM-DD}}-{{topic-slug}}.md`

### Step 4 — Load the tracing guide

Read `references/tracing-guide.md`. This is your instruction set for the rest of the
session. Follow it for every meaningful step you take.

**Key rules from the guide (summary — read the full guide):**
- Log every meaningful step with: Action, Decision, Result
- Include an Execution block with tools, files, searches, timing, tokens, cost
- Trace errors in detail: trigger, root cause, debug steps, fix, lesson
- Use emoji status: ✅ success, ❌ error, ⚠️ warning
- Organize with phase headers (suggested, not enforced)
- Write a Session Summary before finishing
- Update YAML frontmatter and Session Totals at session end
- **Use the right tool for each job** — don't default to Bash for everything. Use Grep to search data files for patterns before loading into Python. Use Glob to discover files in directories. Use Read to preview files before processing. Use WebSearch when domain context would help interpret findings. The trace should show diverse, purposeful tool usage — each tool chosen because it was the best fit, not because it was the default.

### Step 5 — Confirm to the DS

Tell the DS that tracing is active:

```
Tracing active. I'll log my decisions, reasoning, and tool usage to:
  traces/trace-{{YYYY-MM-DD}}-{{topic-slug}}.md

For every meaningful step, I'll capture:
  ✅ What I did, why, and what happened
  🔧 Which tools and files I used
  ⏱️ How long it took and what it cost

Ready to work — what's the analysis task?
```

From this point forward, follow the tracing guide for all work in this session.

---

## Reflect Mode (Reviewer Pattern)

**Purpose:** Read a completed trace, extract learnings, and write them to the
appropriate targets for compound learning.

### Step 1 — Find the trace file

Check for a trace file:

1. If a path was provided (e.g., `/ds-trace reflect traces/trace-2026-03-20-churn.md`)
   → use that file
2. If no path → look for the most recent trace file in `traces/` by date
3. If no trace file exists → execute **No-Start Fallback** (below)

### Step 2 — Load the reflect checklist

Read `references/reflect-checklist.md`. Follow its 7-step process exactly.

### Step 3 — Read the trace and extract learnings

Read the entire trace file. Follow the reflect checklist to extract learnings
into three targets:

**Target 1: CLAUDE.md — Mistakes & Learnings**
- Universal lessons that apply to ANY analysis
- Signal: does NOT mention specific dataset/table/column names
- Format: actionable rule with context and date

**Target 2: traces/learnings.md — DS Workflow Patterns**
- Data science methodology patterns worth accumulating
- Signal: DS methodology, more granular than a CLAUDE.md rule
- Format: pattern with phase, rationale, and source

**Target 3: Memory file — Project-Specific**
- Facts about this specific project/dataset/domain
- Signal: mentions specific dataset, table, column, or file name
- Format: memory file following the user's memory system conventions

### Step 4 — Present to DS

Show the proposed learnings grouped by target. Include a session health summary
with duration, error ratio, biggest time sink, and biggest cost.

### Step 5 — GATE: Wait for approval

DO NOT write any learnings until the DS explicitly approves. They may approve all,
edit some, remove some, or reject all.

### Step 6 — Write approved learnings

Write each approved learning to its target:
1. CLAUDE.md → append to `# Mistakes & Learnings` section
2. traces/learnings.md → append new pattern (create file with header if it doesn't exist)
3. Memory → write a new memory file following the user's memory system

### Step 7 — Suggest next steps

Based on the trace analysis:
- Suggest `/ds-review` if the analysis produced output
- Flag process improvements if debugging was >30% of session time
- Note unresolved questions from the Session Summary

---

## No-Start Fallback

When `/ds-trace reflect` is invoked but no trace file exists:

1. Tell the DS: "No trace file found for this session."
2. Offer a retrospective: "Would you like me to create a retrospective trace from
   what I remember about our work? It won't be as detailed as a real-time trace,
   but I can still extract learnings."
3. If yes:
   - Reconstruct a best-effort trace from conversation context
   - Add a disclaimer at the top of the trace:
     ```
     > ⚠️ **Retrospective trace** — reconstructed from session memory.
     > Timing, token counts, and tool usage are estimated. Some steps may be missing.
     ```
   - Write the retrospective trace to `traces/trace-{{YYYY-MM-DD}}-retrospective.md`
   - Then continue with the normal reflect flow (Step 2 onwards)
4. If no:
   - Tell the DS: "No problem. Next time, start with `/ds-trace start \"topic\"`
     to capture the full journey from the beginning."

---

## Trace Entry Quick Reference

Use these formats when tracing during an active session:

**Successful step:**
```markdown
### ✅ Step: [description]
- **Action:** [what you did]
- **Decision:** [what you chose and why]
- **Result:** [what happened — quantify when possible]
- **Execution:**
  - 🔧 Tools: [tools used]
  - 📂 Files read: [files opened]
  - 📝 Files written: [files created/modified]
  - 💻 Commands: [key commands]
  - ⏱️ Duration: [time spent]
  - 🪙 Tokens: [approximate tokens]
  - 💰 Est. cost: [estimated USD]
```

**Error/debugging step:**
```markdown
### ❌ Error: [description]
- **Trigger:** [what you were doing]
- **Root cause:** [what caused it]
- **Debug steps:**
  1. [attempt 1]
  2. [attempt 2]
  3. [what worked]
- **Fix:** [the solution]
- **Lesson:** [actionable rule for next time]
- **Execution:** [same fields as above]
```

**Warning step:**
```markdown
### ⚠️ Step: [description]
- **Action:** [what you did]
- **Decision:** [what you chose]
- **Risk:** [why this is risky]
- **Result:** [what happened]
```

**Insight (inline, no Execution block needed):**
```markdown
### 💡 Insight: [description]
- **Finding:** [what you discovered]
- **Implication:** [why it matters for the analysis]
```

---

## Session End Checklist

Before the DS runs `/ds-trace reflect` (or before ending the session), complete
these final trace entries:

1. **Write the Session Summary** (key decisions, open questions, what went well/wrong)
   - **"What went wrong" must never be empty or say "nothing."** Even clean sessions have inefficiencies. If no errors occurred, reflect on: was any step slower than it should have been? Did you make a suboptimal tool choice? Could the analysis order have been better? Was there a moment of uncertainty? Write at least one specific, concrete observation. A good trace finds something to improve even when nothing broke.
2. **Update YAML frontmatter** (status, totals)
3. **Update Session Totals** section (aggregated metrics)
4. **Remove unused phase headers** (clean up the trace)
