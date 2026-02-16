# Calibration Loop Workflow — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Define a repeatable calibration loop that cycles through fix → test → document → review → synthesize until scoring acceptance criteria are met.

**Architecture:** Each round produces a fixed set of artifacts (test notes, calibration notes, 3 role reviews, fix plan). Each round compares against the prior round's artifacts to measure progress. The loop exits when acceptance criteria pass. All artifacts are files in `dev/` — no state lives in conversation context, so the loop survives session boundaries.

**Tech Stack:** Claude Code (agent dispatch), markdown files, ds-review-lead pipeline

---

## The Loop

```
┌──────────────────────────────────────────────────────────────┐
│                    CALIBRATION ROUND N                        │
│                                                              │
│  ┌─────────┐   ┌──────────┐   ┌──────────────┐              │
│  │ 1. FIX  │──→│ 2. TEST  │──→│ 3. TEST NOTES│              │
│  │ (plugin │   │ (run 6   │   │ (per fixture │              │
│  │  files) │   │ fixtures)│   │  results)    │              │
│  └─────────┘   └──────────┘   └──────┬───────┘              │
│                                      │                       │
│  ┌──────────────┐   ┌────────────────▼───────┐               │
│  │ 5. COMPARE   │←──│ 4. CALIBRATION NOTES   │               │
│  │ (round N vs  │   │ (synthesize test       │               │
│  │  round N-1)  │   │  results + root cause) │               │
│  └──────┬───────┘   └────────────────────────┘               │
│         │                                                    │
│  ┌──────▼───────────────────────────────────┐                │
│  │ 6. THREE ROLE REVIEWS (parallel)         │                │
│  │  • Principal AI Engineer                 │                │
│  │  • PM Lead                               │                │
│  │  • DS Lead                               │                │
│  └──────────────┬───────────────────────────┘                │
│                 │                                            │
│  ┌──────────────▼───────────────────────────┐                │
│  │ 7. SYNTHESIZE → FIX PLAN                 │                │
│  │  (A3 format, owner decisions)            │                │
│  └──────────────┬───────────────────────────┘                │
│                 │                                            │
│  ┌──────────────▼───────────────────────────┐                │
│  │ 8. OWNER REVIEW + DECISIONS              │                │
│  │  • Approve fix plan OR request changes   │                │
│  │  • Accept calibration OR start round N+1 │                │
│  └──────────────────────────────────────────┘                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
         │                                    │
         │ Acceptance criteria NOT met         │ Acceptance criteria MET
         ▼                                    ▼
    ROUND N+1                            SHIP v0.4
```

---

## File Naming Convention

Every artifact includes the round number so rounds can be compared. The
convention extends the existing date-based naming:

```
dev/test-results/YYYY-MM-DD-rN-{artifact}.md
dev/reviews/YYYY-MM-DD-rN-{artifact}.md
```

Where `rN` = round number (r0 = current baseline, r1 = first fix round, etc.)

### Artifacts Per Round

| # | Artifact | Path | Created By |
|---|---|---|---|
| 1 | Vanguard test review | `dev/test-results/{date}-rN-vanguard-review.md` | ds-review-lead pipeline |
| 2 | Meta test review | `dev/test-results/{date}-rN-meta-review.md` | ds-review-lead pipeline |
| 3 | Rossmann test review | `dev/test-results/{date}-rN-rossmann-review.md` | ds-review-lead pipeline |
| 4 | Airbnb Message Intent review | `dev/test-results/{date}-rN-airbnb-message-intent-review.md` | ds-review-lead pipeline |
| 5 | Airbnb FIV review | `dev/test-results/{date}-rN-airbnb-fiv-review.md` | ds-review-lead pipeline |
| 6 | Netflix Proxy Metrics review | `dev/test-results/{date}-rN-netflix-proxy-metrics-review.md` | ds-review-lead pipeline |
| 7 | Calibration notes | `dev/test-results/{date}-rN-calibration-notes.md` | Claude (synthesis step) |
| 8 | Round comparison | `dev/test-results/{date}-rN-vs-rN-1-comparison.md` | Claude (diff step) |
| 9 | AI Engineer review | `dev/test-results/{date}-rN-principal-ai-engineer-assessment.md` | Claude (role-play) |
| 10 | PM Lead review | `dev/reviews/{date}-rN-pm-lead-calibration-review.md` | Claude (role-play) |
| 11 | DS Lead review | `dev/test-results/{date}-rN-ds-lead-assessment.md` | Claude (role-play) |
| 12 | Fix plan (A3) | `dev/test-results/{date}-rN-calibration-fix-plan.md` | Claude (A3 synthesis) |

### Round 0 Baseline (Already Exists)

The current files ARE Round 0. No renaming needed — the plan references them
by their existing names:

| Artifact | Existing File |
|---|---|
| Vanguard R0 review | `dev/test-results/2026-02-15-vanguard-ab-test-full-review.md` |
| Meta R0 review | `dev/test-results/2026-02-15-meta-llm-bug-reports-review.md` |
| Calibration notes R0 | `dev/test-results/2026-02-15-calibration-notes.md` |
| AI Engineer R0 | `dev/test-results/2026-02-15-principal-ai-engineer-assessment.md` |
| PM Lead R0 | `dev/reviews/2026-02-15-pm-lead-calibration-review.md` |
| DS Lead R0 | `dev/test-results/2026-02-15-ds-lead-assessment.md` |
| Fix plan R0 | `dev/test-results/2026-02-15-calibration-fix-plan.md` |

---

## Acceptance Criteria (Exit Conditions)

The loop exits when ALL of these pass:

### Scoring Criteria

**Core Fixtures (calibration targets):**

| Criterion | Test | Pass Condition |
|---|---|---|
| Vanguard score | Run review on `dev/test-fixtures/real/vanguard-ab-test.md` (tech/reactive) | Score 40-55, Verdict: Minor Fix |
| Meta score | Run review on `dev/test-fixtures/real/meta-llm-bug-reports.md` (exec/proactive) | Score in owner-chosen target range |
| Rossmann score | Run review on `dev/test-fixtures/real/rossmann-sales-prediction.md` (mixed/proactive) | Score 45-60, Verdict: Minor Fix |
| Tier separation | Compare Vanguard vs Meta analysis dimension scores | Vanguard analysis > Meta analysis by 5+ points |
| Overall differentiation | Compare highest and lowest scores across all 3 core | 15+ point gap between strongest and weakest |
| CRITICAL count | Count CRITICALs per test | Max 2 per test; only genuinely misleading findings |

**Extended Fixtures (generalization check):**

| Criterion | Test | Pass Condition |
|---|---|---|
| Airbnb Message Intent | Run review on `dev/test-fixtures/airbnb-message-intent-classification.md` (mixed/general) | Analysis 55-65, Communication 70-80 |
| Airbnb FIV | Run review on `dev/test-fixtures/airbnb-future-value-tradeoffs.md` (mixed/general) | Analysis 65-75, Communication 70-80 |
| Netflix Proxy Metrics | Run review on `dev/test-fixtures/netflix-proxy-metrics.md` (mixed/general) | Analysis 60-70, Communication 65-75 |
| Blog post differentiation | Compare extended fixture scores | Correctly ranks FIV ≥ Message Intent ≥ Proxy Metrics |
| Genre consistency | Compare blog posts vs core fixtures | Blog posts not systematically over-penalized for missing business metrics |

### Quality Criteria

| Criterion | Test | Pass Condition |
|---|---|---|
| No severity/deduction mismatches | Audit each review's deduction log | Every severity label matches its deduction table entry |
| No cross-cutting duplicates | Check both dimensions for same-root-cause findings | Each root cause appears in ONE dimension only |
| Output length reasonable | Word count of review vs. word count of input | Review ≤ 1.5x input document length |
| Synthetic fixtures still pass | Rerun 2-3 synthetic fixtures | Floor rules fire correctly, dimension separation holds |
| Cross-run consistency | Run same doc 3x | Scores within ±10 |

### Owner Gut Check

After all quantitative criteria pass, the owner reads the full review output
for each test fixture and answers: "Would I trust this review if someone handed
it to me?" If yes → ship. If no → another round with specific feedback on what
feels wrong.

---

## Task-by-Task: One Full Round

Each round follows these tasks in order. Task numbers restart each round.
Replace `{date}` with the current date and `N` with the round number.

---

### Task 1: Implement Fixes from Prior Round's Fix Plan

**Files:** As specified in the fix plan from round N-1
**Input:** `dev/test-results/{date}-r{N-1}-calibration-fix-plan.md`

**Step 1: Read the fix plan and confirm owner's decisions**

Read the fix plan from the prior round. Check that all "DECISION NEEDED" items
have owner-approved answers. If any decision is unresolved, STOP and ask the owner.

**Step 2: Implement fixes in dependency order**

Follow the fix plan's Implementation Plan section. Make each change to the
specified files. The fix plan has exact file paths and specific change descriptions.

**Step 3: Self-verify changes**

After all fixes applied, read each modified file and verify:
- Changes match the fix plan's specifications
- No formatting damage to surrounding content
- SKILL.md sections still properly numbered and internally consistent
- Agent prompts still reference correct SKILL.md section numbers

**Step 4: Commit**

```bash
git add plugin/ (only changed files)
git commit -m "feat(calibration): implement round N fixes — [brief description]"
```

---

### Task 2: Run the Six Test Fixtures

**Core Fixtures:**
- Input: `dev/test-fixtures/real/vanguard-ab-test.md`
- Input: `dev/test-fixtures/real/meta-llm-bug-reports.md`
- Input: `dev/test-fixtures/real/rossmann-sales-prediction.md`

**Extended Fixtures (Blog Posts):**
- Input: `dev/test-fixtures/airbnb-message-intent-classification.md`
- Input: `dev/test-fixtures/airbnb-future-value-tradeoffs.md`
- Input: `dev/test-fixtures/netflix-proxy-metrics.md`

**Step 1: Run Vanguard review (core)**

Invoke the ds-review-lead pipeline on the Vanguard fixture:
```
/ds-review:review dev/test-fixtures/real/vanguard-ab-test.md --mode full --audience tech --workflow reactive
```
Save the complete output to `dev/test-results/{date}-rN-vanguard-review.md`.

**Step 2: Run Meta review (core)**

```
/ds-review:review dev/test-fixtures/real/meta-llm-bug-reports.md --mode full --audience exec --workflow proactive
```
Save to `dev/test-results/{date}-rN-meta-review.md`.

**Step 3: Run Rossmann review (core)**

```
/ds-review:review dev/test-fixtures/real/rossmann-sales-prediction.md --mode full --audience mixed --workflow proactive
```
Save to `dev/test-results/{date}-rN-rossmann-review.md`.

**Step 4: Run Airbnb Message Intent review (extended)**

```
/ds-review:review dev/test-fixtures/airbnb-message-intent-classification.md --mode full --audience mixed --workflow general
```
Save to `dev/test-results/{date}-rN-airbnb-message-intent-review.md`.

**Step 5: Run Airbnb FIV review (extended)**

```
/ds-review:review dev/test-fixtures/airbnb-future-value-tradeoffs.md --mode full --audience mixed --workflow general
```
Save to `dev/test-results/{date}-rN-airbnb-fiv-review.md`.

**Step 6: Run Netflix Proxy Metrics review (extended)**

```
/ds-review:review dev/test-fixtures/netflix-proxy-metrics.md --mode full --audience mixed --workflow general
```
Save to `dev/test-results/{date}-rN-netflix-proxy-metrics-review.md`.

**Step 7: Quick sanity check**

After all 6 tests, extract scores into a comparison table:

| Test | Type | R{N-1} Score | R{N} Score | Delta | R{N} CRITICALs | R{N} Findings |
|---|---|---|---|---|---|---|
| Vanguard | Core | ? | ? | ? | ? | ? |
| Meta | Core | ? | ? | ? | ? | ? |
| Rossmann | Core | ? | ? | ? | ? | ? |
| Airbnb Message Intent | Extended | ? | ? | ? | ? | ? |
| Airbnb FIV | Extended | ? | ? | ? | ? | ? |
| Netflix Proxy Metrics | Extended | ? | ? | ? | ? | ? |

Check:
- Core fixtures: If any score went DOWN from the prior round where it should have gone up, flag immediately
- Extended fixtures: Verify scores within expected ranges (see Acceptance Criteria)
- Differentiation: Blog posts should differentiate quality (FIV > Message Intent > Proxy Metrics expected)

---

### Task 3: Write Test Notes

**Files:**
- Create: Test notes section within each review file (already saved in Task 2)
- These are the raw review outputs — no additional test notes file needed.
  The calibration notes (Task 4) are the synthesis.

**Step 1: Append pipeline metadata to each review file**

At the bottom of each review output file, add:

```markdown
---
## Pipeline Observations — Round N

- **Subagent dispatch:** [Both successful? Any failures?]
- **Output format compliance:** [PER-LENS RATINGS, FINDINGS, STRENGTH LOG all present?]
- **Deduction table adherence:** [All deductions match SKILL.md Section 2?]
- **Strength credit adherence:** [All credits match SKILL.md Section 2b?]
- **Dimension boundary respect:** [Any cross-cutting duplicates?]
- **Floor rules correctly applied:** [Correct CRITICAL count? Correct verdict cap?]
- **Severity/deduction consistency:** [Any mismatches between severity labels and deduction amounts?]
- **New issues observed:** [Anything unexpected?]
```

---

### Task 4: Write Calibration Notes

**Files:**
- Create: `dev/test-results/{date}-rN-calibration-notes.md`
- Read: All 3 review outputs from Task 2
- Read: Prior round calibration notes for comparison

**Step 1: Create the calibration notes document**

Use this template:

```markdown
# Scoring Calibration Notes — Round N

**Date:** {date}
**Status:** [OPEN | RESOLVED]
**Prior round:** [link to round N-1 calibration notes]

---

## Score Summary

| # | Document | Type | Score R{N-1} | Score R{N} | Delta | CRITICALs | Findings | Verdict |
|---|---|---|---|---|---|---|---|---|

## Acceptance Criteria Check

| Criterion | Status | Detail |
|---|---|---|
| Vanguard 40-55 | PASS/FAIL | Score: X |
| Meta in target range | PASS/FAIL | Score: X |
| Rossmann 45-60 | PASS/FAIL | Score: X |
| Vanguard analysis > Meta analysis | PASS/FAIL | Gap: X points |
| Overall 15+ point differentiation | PASS/FAIL | Gap: X points |
| Max 2 CRITICALs per test | PASS/FAIL | Counts: X, Y, Z |
| No severity/deduction mismatches | PASS/FAIL | [details] |
| No cross-cutting duplicates | PASS/FAIL | [details] |

## What Improved from Round N-1

[List specific improvements with before/after data]

## What Didn't Improve (or Got Worse)

[List remaining problems with data]

## Root Cause Analysis (for remaining problems)

[Why do the remaining problems persist? What did we miss?]

## Remaining Problems (Ranked by Impact)

1. [Problem] — impact on which fixture, how many points
2. ...

## Proposed Fix Direction (Inputs to Role Reviews)

[Brief hypothesis about what to try next, for the role reviewers to react to]
```

---

### Task 5: Compare Against Prior Round

**Files:**
- Create: `dev/test-results/{date}-rN-vs-r{N-1}-comparison.md`
- Read: Round N calibration notes
- Read: Round N-1 calibration notes

**Step 1: Create the comparison document**

Use this template:

```markdown
# Calibration Round Comparison: R{N} vs R{N-1}

**Date:** {date}

## Score Trajectory

| Document | R0 | R1 | ... | R{N} | Target | Gap to Target |
|---|---|---|---|---|---|---|
| Vanguard | 16 | ? | ... | ? | 40-55 | ? |
| Meta | 18 | ? | ... | ? | [target] | ? |
| Rossmann | 29 | ? | ... | ? | 45-60 | ? |

## CRITICAL Count Trajectory

| Document | R0 | R1 | ... | R{N} | Target |
|---|---|---|---|---|---|
| Vanguard | 5 | ? | ... | ? | ≤2 |
| Meta | 4 | ? | ... | ? | ≤2 |
| Rossmann | 2 | ? | ... | ? | ≤2 |

## Finding Count Trajectory

| Document | R0 | R1 | ... | R{N} | Target |
|---|---|---|---|---|---|
| Vanguard | 16 | ? | ... | ? | ≤10 |
| Meta | 15 | ? | ... | ? | ≤10 |
| Rossmann | 15 | ? | ... | ? | ≤10 |

## What Changed Between Rounds

### Fixes Applied in R{N}
[List from the fix plan]

### Expected Impact vs Actual Impact
| Fix | Expected Effect | Actual Effect | Assessment |
|---|---|---|---|
| [Fix 1] | [expected] | [actual] | Worked / Partially / Didn't work |

## Convergence Assessment

- **Are scores converging toward targets?** [Yes/No + data]
- **Is differentiation improving?** [Yes/No + gap trajectory]
- **Estimated rounds remaining:** [0 = done, 1-2 = close, 3+ = rethink approach]
- **Risk of oscillation:** [Are fixes helping one fixture while hurting another?]
```

---

### Task 6: Three Role Reviews (Run in Parallel)

**Files:**
- Create: `dev/test-results/{date}-rN-principal-ai-engineer-assessment.md`
- Create: `dev/reviews/{date}-rN-pm-lead-calibration-review.md`
- Create: `dev/test-results/{date}-rN-ds-lead-assessment.md`
- Read: Round N calibration notes, comparison doc, all 6 review outputs (3 core + 3 extended)

**IMPORTANT:** These three reviews run as **parallel subagents** via the Task tool.
Each subagent receives the same input context but reviews through a different lens.

**Step 1: Dispatch all three role-play reviews in parallel**

Each subagent receives this context payload:

```
ROLE: [Principal AI Engineer | PM Lead | DS Lead]

You are role-playing as a {role} reviewing the DS Analysis Review Agent's
calibration progress. Read all the files below and produce your assessment.

## Context Files (read in order)

1. Prior round fix plan: dev/test-results/{date}-r{N-1}-calibration-fix-plan.md
2. Round N calibration notes: dev/test-results/{date}-rN-calibration-notes.md
3. Round comparison: dev/test-results/{date}-rN-vs-r{N-1}-comparison.md
4. Current SKILL.md: plugin/skills/ds-review-framework/SKILL.md
5. Current lead agent: plugin/agents/ds-review-lead.md
6. Current analysis agent: plugin/agents/analysis-reviewer.md
7. Current communication agent: plugin/agents/communication-reviewer.md

## Test Results (read for scoring context)

**Core fixtures:**
8. Vanguard review: dev/test-results/{date}-rN-vanguard-review.md
9. Meta review: dev/test-results/{date}-rN-meta-review.md
10. Rossmann review: dev/test-results/{date}-rN-rossmann-review.md

**Extended fixtures (blog posts):**
11. Airbnb Message Intent review: dev/test-results/{date}-rN-airbnb-message-intent-review.md
12. Airbnb FIV review: dev/test-results/{date}-rN-airbnb-fiv-review.md
13. Netflix Proxy Metrics review: dev/test-results/{date}-rN-netflix-proxy-metrics-review.md

## Your Task

Produce an assessment covering:
1. What improved vs prior round (cite specific scores and deltas)
2. What's still broken (with evidence from the test reviews)
3. Root cause of remaining problems
4. Proposed fixes for next round (specific files, specific changes)
5. Whether the acceptance criteria can be met with incremental fixes
   or whether a larger redesign is needed
```

**Role-specific instructions appended to each:**

**Principal AI Engineer:**
```
Focus on: system mechanics, scoring math, formula behavior, implementation
correctness, edge cases. Think about whether the diminishing returns curve
and credit system interact correctly. Look for mathematical issues.
```

**PM Lead:**
```
Focus on: user experience, output quality, whether scores feel trustworthy,
whether the review output would help a real DS improve their work. Think about
the product: would you ship this to users? What would make you hesitate?
```

**DS Lead:**
```
Focus on: finding quality, whether each finding is legitimate and correctly
prioritized, whether strengths are being properly credited, whether the review
reflects how a senior DS would actually evaluate the work. Do a finding-by-
finding audit of at least one test review. Grade the findings, not just the scores.
```

**Step 2: Save outputs**

Save each subagent's output to its designated file path.

---

### Task 7: Synthesize into Fix Plan

**Files:**
- Create: `dev/test-results/{date}-rN-calibration-fix-plan.md`
- Read: All 3 role reviews from Task 6
- Read: Round N calibration notes and comparison doc

**Step 1: Read all three role reviews**

**Step 2: Produce A3 synthesis using the same format as Round 0's fix plan**

Use the A3 Problem Analysis template from the `kaizen:analyse-problem` skill:
1. Background (round context, what was tried)
2. Current Condition (scores, deltas, remaining gaps)
3. Goal/Target (acceptance criteria status)
4. Root Cause Analysis (consensus + disagreements from 3 reviewers)
5. Countermeasures (ordered fix plan with exact file paths)
6. Implementation Plan (dependency-ordered steps)
7. Follow-up (what to verify, decisions needed)

Save to `dev/test-results/{date}-rN-calibration-fix-plan.md`.

---

### Task 8: Owner Review + Decision

**This task is the owner (human), not Claude.**

Owner reads the fix plan and either:

**A. Approves and starts next round** → Return to Task 1 for Round N+1

**B. Approves and declares calibration done** → Proceed to Wrap-Up Tasks

**C. Requests changes** → Claude revises the fix plan, then back to owner review

---

## Wrap-Up Tasks (After Loop Exits)

### Task W1: Create ADR-003 for Calibration Approach

**Files:**
- Create: `dev/decisions/ADR-003-calibration-approach.md`

Document: what was tried across all rounds, what worked, what was discarded,
final parameter values (credit cap, diminishing returns curve, CRITICAL
definitions), and the rationale for each choice.

### Task W2: Update Backlog

**Files:**
- Modify: `dev/backlog.md`

Move all completed calibration items to "Done." Add any deferred items
(genre detection, cluster-based scoring) to the appropriate future sprint.

### Task W3: Update CHANGELOG

**Files:**
- Modify: `CHANGELOG.md`

Add v0.4 entry with: what changed, why, and the calibration test results.

### Task W4: Create Session Log

**Files:**
- Create: `dev/sessions/{date}-calibration-complete.md`

Document: final scores, number of rounds, key decisions made, pickup context
for future sessions.

### Task W5: Run Extended Validation

Run 2-3 untested real-world fixtures to confirm calibration generalizes:
- Suggested: `capstone-customer-churn.md`, `credit-card-churn-segmentation.md`,
  `tips-regression-analysis.md`

Run cross-consistency test: same doc 3x, verify scores within ±10.

Run 2-3 synthetic fixtures to verify floor rules still work.

---

## Session Management

### Starting a New Session Mid-Loop

If a session ends mid-loop, the pickup protocol is:

1. Read `dev/backlog.md` for current state
2. Read the latest `dev/sessions/` log
3. Find the highest-numbered round artifacts in `dev/test-results/`
4. Read the latest fix plan to see where you are in the task sequence
5. Resume from the next incomplete task

### Context Window Management

Each round generates ~8 files of significant length. To prevent context bloat:

- **Use subagents** for the 3 role-play reviews (Task 6) — they run in separate
  context windows
- **Summarize, don't paste** — when reading prior round artifacts, extract the
  key numbers and conclusions, don't load full files into the main context
- **Start fresh sessions** between rounds if context is getting heavy. The files
  on disk are the source of truth, not conversation history.

### Estimated Rounds

Based on the gap between current scores and targets:

| Scenario | Estimated Rounds | Why |
|---|---|---|
| All P0 fixes work as projected | 1-2 | One round to implement + test, one to fine-tune |
| Strength credits need tuning | 2-3 | May need to adjust credit values or cap |
| Finding quality is the blocker | 3-4 | Requires prompt changes to subagents, harder to calibrate |
| Fundamental redesign needed | Exit loop, write new architecture | Role reviews will flag this if incremental fixes aren't converging |

---

## Quick Reference: Round Checklist

Copy this checklist at the start of each round:

```markdown
## Round N Checklist

- [ ] Task 1: Implement fixes from R{N-1} fix plan
  - [ ] Read fix plan, confirm all decisions resolved
  - [ ] Apply changes to plugin files
  - [ ] Self-verify changes
  - [ ] Commit
- [ ] Task 2: Run 6 test fixtures
  - [ ] Vanguard (tech/reactive) → save review
  - [ ] Meta (exec/proactive) → save review
  - [ ] Rossmann (mixed/proactive) → save review
  - [ ] Airbnb Message Intent (mixed/general) → save review
  - [ ] Airbnb FIV (mixed/general) → save review
  - [ ] Netflix Proxy Metrics (mixed/general) → save review
  - [ ] Quick sanity check (score comparison table for all 6)
- [ ] Task 3: Append pipeline observations to each review
- [ ] Task 4: Write calibration notes (synthesize + root cause)
- [ ] Task 5: Write round comparison (R{N} vs R{N-1} with trajectory)
- [ ] Task 6: Run 3 role reviews in parallel
  - [ ] Principal AI Engineer assessment
  - [ ] PM Lead review
  - [ ] DS Lead assessment
- [ ] Task 7: Synthesize into A3 fix plan
- [ ] Task 8: Owner review + decision
  - [ ] Next round? → repeat from Task 1
  - [ ] Done? → proceed to Wrap-Up Tasks
```
