# Tracing Guide

You are tracing your work for this analysis session. This guide defines what to log,
how to format entries, and what to skip. The trace serves two audiences:

1. **The DS reviewing your work** — they want to understand your decisions and where
   you spent time. Think of it as a lab notebook they can skim.
2. **A future agent reflecting on this trace** — it will extract lessons and patterns
   from your entries. Consistent structure makes this reliable.

---

## What to Log

For every **meaningful step** in the analysis, write a trace entry. A meaningful step
is one where you made a decision, produced a result, or encountered a problem.

### Successful Steps

Use this format:

```markdown
### ✅ Step: [short description of what you did]
- **Action:** What you did (1 sentence)
- **Decision:** What you chose and why (the reasoning behind your approach)
- **Result:** What happened (quantify when possible — row counts, metrics, scores)
- **Execution:**
  - 🔧 Tools: [which tools you used, e.g. `Read(file.csv)`, `Bash(python)`, `WebSearch`]
  - 📂 Files read: [list of files you opened]
  - 📝 Files written: [list of files you created or modified]
  - 💻 Commands: [key bash commands you ran]
  - 🔍 Search: [search queries and result counts, if any]
  - ⏱️ Duration: [approximate time spent]
  - 🪙 Tokens: [approximate token usage]
  - 💰 Est. cost: [estimated cost in USD]
```

### Optional Fields (add when relevant)

- **Reasoning:** For non-obvious decisions — explain the tradeoff you weighed
- **Alternative considered:** What you almost did instead and why you didn't
- **Issue:** Something unexpected you noticed (data quality, missing values, outliers)
- **Insight:** A finding worth highlighting (patterns, anomalies, business implications)

Not every step needs every field. Use your judgment — if a decision was obvious
(e.g., "used pandas to read a CSV"), you don't need a Reasoning field.

### Error and Debugging Steps

When you hit an error, trace the full debugging journey. These are often the most
valuable entries for learning:

```markdown
### ❌ Error: [short description of what went wrong]
- **Trigger:** What you were doing when the error occurred
- **Root cause:** What actually caused the problem
- **Debug steps:**
  1. [First thing you tried]
  2. [Second thing you tried]
  3. [What finally worked]
- **Fix:** [The actual fix, ideally a code snippet]
- **Lesson:** [What to do differently next time to avoid this]
- **Execution:**
  - 🔧 Tools: [tools used during debugging]
  - 📂 Files read: [files you inspected]
  - 🔍 Grep: [search patterns you used to investigate]
  - ⏱️ Duration: [time spent — flag if this was a bottleneck]
  - 🪙 Tokens: [tokens consumed during debugging]
  - 💰 Est. cost: [cost of the debugging detour]
```

The **Lesson** field is critical — it's what the reflect step extracts for compound
learning. Write it as an actionable rule: "Always X before Y" or "Check Z when you see W."

### Warning Steps

For risky decisions that worked but deserve flagging:

```markdown
### ⚠️ Step: [short description]
- **Action:** What you did
- **Decision:** What you chose
- **Risk:** Why this is risky or might cause problems later
- **Result:** What happened (for now)
```

---

## Phase Headers

Organize your trace with phase headers. These are **suggested categories** — use
whichever apply to your analysis. Don't force phases that don't exist.

```markdown
## Phase: Data Loading
## Phase: Exploratory Analysis
## Phase: Feature Engineering
## Phase: Modeling
## Phase: Evaluation
## Phase: Reporting
```

Add a new phase header when you transition to a clearly different stage of work.
Remove unused phase headers at session end.

---

## Execution Block Details

The Execution block captures engineering-level observability. Here's what each field tracks:

| Field | What to Log | Example |
|-------|------------|---------|
| 🔧 Tools | Claude Code tools used | `Read(data.csv)`, `Bash(python)`, `Grep("col_name")` |
| 📂 Files read | Every file you opened | `data/customers.csv`, `notebooks/eda.py` |
| 📝 Files written | Every file you created/modified | `notebooks/01_clean.py`, `output/report.md` |
| 💻 Commands | Key bash/shell commands | `pip install pandas`, `python train.py` |
| 🔍 Search | Web searches + code searches | `WebSearch("churn definition")` → 4 hits, 2 used |
| 🎯 Skills | Any skills invoked | `/ds-review`, `/browse` |
| ⏱️ Duration | Approximate wall-clock time | ~5 min, ~20 min |
| 🪙 Tokens | Approximate token usage | ~2,500 (prompt: 1,800, completion: 700) |
| 💰 Est. cost | Estimated USD cost | $0.04 |

**When to include the full Execution block:**
- Steps involving tool calls, file access, or searches — always include
- Pure reasoning steps (deciding strategy, choosing approach) — skip Execution

**Token and cost estimation:**
- You won't have exact numbers. Estimate based on the complexity of the step.
- A simple file read + short response: ~500-1,000 tokens, ~$0.01
- A complex multi-tool step with reasoning: ~3,000-8,000 tokens, ~$0.05-0.12
- Extended debugging with multiple attempts: ~5,000-15,000 tokens, ~$0.08-0.25
- These are rough guides. Directional accuracy is more valuable than precision.

---

## What NOT to Log

Skip these — they add noise without value:

- **Routine file reads** where no decision was made (reading a file just to check format)
- **Minor formatting or cleanup** (fixing indentation, renaming a variable)
- **Tool invocation boilerplate** (the internal mechanics of how you called a tool)
- **Repeated identical operations** (if you read the same file 5 times, mention it once with "x5")
- **Your internal chain of thought** (the trace captures decisions, not stream of consciousness)

---

## Session Summary

At the end of the session, write a summary before the Session Totals:

```markdown
## Session Summary
- **Key decisions:** [List the 3-5 most important decisions you made]
- **Open questions:** [What's unresolved? What needs follow-up?]
- **What went well:** [What worked smoothly?]
- **What went wrong:** [Where did you struggle or waste time?]
- **Suggested next steps:** [What should happen in the next session?]
```

Then update the **Session Totals** section with aggregated metrics.

---

## YAML Frontmatter Updates

Update the YAML frontmatter at the top of the trace file at session end:
- Set `status: complete` (or `error` if the analysis didn't finish)
- Fill in `total_duration_min`, `total_tokens`, `total_cost_usd`
- Fill in `steps_success`, `steps_error`
- Fill in `tools_summary` with tool usage counts
- Fill in `files_read`, `files_written` with total counts
