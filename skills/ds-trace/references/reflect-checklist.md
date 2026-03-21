# Reflect Checklist

You are reflecting on a completed trace to extract compound learnings. This checklist
guides you through reading the trace, identifying patterns, and routing learnings to
the right targets.

---

## Step 1: Read the Trace

Read the full trace file. Pay special attention to:

- **Error blocks** (### ❌) — these almost always contain extractable lessons
- **Warning blocks** (### ⚠️) — risky decisions that may need a rule
- **Session Summary** — the agent's own assessment of what went well/wrong
- **Duration bottlenecks** — steps that took disproportionate time
- **Token/cost spikes** — steps that consumed disproportionate resources

---

## Step 2: Extract Learnings

For each learning you identify, classify it into one of three targets using these
routing rules.

### Target 1: CLAUDE.md — Mistakes & Learnings

**What goes here:** Universal lessons that apply to ANY analysis, not just this one.
These prevent the same mistake from happening in a different project.

**Routing signal:** The learning does NOT mention a specific dataset, table, column,
or project name. It's a general principle.

**Format:** Write as an actionable rule with context:
```
- **[Category]: [Rule].** [Brief explanation of what happened and why this matters.]
  (Learned: YYYY-MM-DD)
```

**Examples:**
- **Data quality: Always check dtypes before merging DataFrames.** A merge produced 0
  rows because customer_id was int in one table and string in another. 20 min debugging.
  (Learned: 2026-03-20)
- **Modeling: Check class balance before training a classifier.** Trained on 95/5
  imbalanced data without noticing — model predicted majority class for everything.
  (Learned: 2026-03-20)

**Quality bar:** Only extract learnings that would genuinely save time or prevent
errors in future sessions. Not every step produces a learning. If the session went
smoothly with no surprises, it's fine to have zero CLAUDE.md entries.

### Target 2: traces/learnings.md — DS Workflow Patterns

**What goes here:** Data science methodology patterns worth accumulating over time.
These build up a personal "DS playbook" — recurring best practices the agent discovers
through experience.

**Routing signal:** The pattern is about DS methodology (not a specific dataset) and
is more granular than a CLAUDE.md rule — it's a workflow habit or technique.

**Format:** Write as a pattern with context:
```
### [Pattern Name]
**Phase:** [which phase this applies to — EDA, Modeling, Evaluation, etc.]
**Pattern:** [What to do]
**Why:** [Why this works]
**Learned from:** [Brief reference to the session where this was discovered]
**Date:** YYYY-MM-DD
```

**Examples:**
```markdown
### Null Percentage First
**Phase:** EDA
**Pattern:** Before any analysis, compute null % for every column and flag those >5%.
**Why:** Prevents silent data loss in aggregations and unexpected model behavior.
**Learned from:** Churn analysis — missed 12% nulls in tenure, had to backtrack.
**Date:** 2026-03-20
```

```markdown
### Baseline Before Tuning
**Phase:** Modeling
**Pattern:** Always train a simple baseline (logistic regression or decision tree)
before trying complex models.
**Why:** Establishes a performance floor and often reveals that simple models are sufficient.
**Learned from:** Spent 30 min tuning XGBoost only to find logistic regression was 2% behind.
**Date:** 2026-03-20
```

### Target 3: Memory File — Project-Specific

**What goes here:** Facts about this specific project, dataset, or domain that will
be useful in future sessions on the same project. These are NOT universal lessons —
they're contextual knowledge.

**Routing signal:** The learning mentions a specific dataset name, table name, column
name, file path, or domain-specific quirk.

**Format:** Write as a project memory following the user's memory system conventions:
```markdown
---
name: [descriptive name]
description: [one-line description]
type: project
---

[Fact or pattern]. **Why:** [context]. **How to apply:** [when this matters].
```

**Examples:**
```markdown
---
name: customer-events-dtype-quirk
description: customer_events.csv stores customer_id as string, not int — must cast before joining
type: project
---

customer_events.csv uses string type for customer_id while all other tables use int.
**Why:** Legacy data pipeline exports IDs as zero-padded strings.
**How to apply:** Always cast customer_id to int before any merge/join operation.
```

---

## Step 3: Check for Cross-Cutting Patterns

After extracting individual learnings, look for meta-patterns:

- **Time sinks:** Did debugging consume >30% of session time? → suggest a pre-check
  that would have caught the issue earlier
- **Repeated tool usage:** Was the same tool called 10+ times? → might indicate an
  inefficient workflow worth streamlining
- **Research patterns:** Were many web searches needed? → the domain might benefit
  from a knowledge digest (like search-domain-knowledge)

---

## Step 4: Present to DS for Approval

Present all proposed learnings grouped by target. For each one, show:

1. **Target:** Where this will be written (CLAUDE.md / learnings.md / memory)
2. **Proposed text:** The exact text you'll write
3. **Source:** Which trace entry this came from (quote the step title)

**Format your presentation like this:**

```markdown
## 🔍 Reflection Summary

I found [N] learnings from this session:

### → CLAUDE.md (universal lessons)
1. **[Rule]** — [brief explanation]
   _Source: [trace step title]_

### → traces/learnings.md (DS patterns)
1. **[Pattern name]** — [brief explanation]
   _Source: [trace step title]_

### → Memory (project-specific)
1. **[Fact]** — [brief explanation]
   _Source: [trace step title]_

### 📊 Session Health
- Session duration: X min
- Error ratio: X errors / Y total steps
- Biggest time sink: [step name] (X min, Y% of session)
- Biggest cost: [step name] ($X, Y% of total)

Approve these learnings? Edit any before I save?
```

---

## Step 5: GATE — Wait for Approval

DO NOT write any learnings until the DS explicitly approves. They may:
- Approve all → write everything
- Edit some → apply their edits, then write
- Remove some → skip those, write the rest
- Reject all → write nothing (that's fine — not every session produces learnings)

---

## Step 6: Write Approved Learnings

Write each approved learning to its target:

1. **CLAUDE.md:** Append to the `# Mistakes & Learnings` section at the bottom
2. **traces/learnings.md:** Append the new pattern. Create the file if it doesn't exist
   (with a header: `# DS Workflow Patterns\n\nAccumulated patterns from analysis sessions.\n`)
3. **Memory file:** Write a new memory file following the user's memory system conventions

---

## Step 7: Suggest Next Steps

After writing learnings, suggest actionable next steps:

- If the analysis produced output (a notebook, report, or dashboard):
  → "Run `/ds-review` on the final analysis to check methodology and communication"
- If debugging consumed >30% of session time:
  → "Consider building a pre-analysis data quality check for this dataset"
- If the same manual pattern appeared 3+ times in the trace:
  → "This workflow could be automated — consider it for a future skill (v2)"
- If there are open questions in the Session Summary:
  → "These questions are unresolved: [list]. Want to continue in a new session?"
