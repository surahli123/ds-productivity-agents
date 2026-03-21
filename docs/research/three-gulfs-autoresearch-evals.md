# The Three Gulfs: Why AutoResearch Alone Isn't Enough

**Source:** Article by an AI PM practitioner (shared 2026-03-21)
**Key references:** Hamel Husain & Shreya Shankar's "Application-Centric AI Evals" course, Karpathy's AutoResearch library, Ole's AutoResearch-as-skill fork

## Core Thesis

AutoResearch (automated prompt optimization loops) only addresses the **Gulf of Generalization** — the third of three gulfs. Without closing the first two gulfs manually, you're "optimizing against a fantasy."

## The Three Gulfs (from Hamel's Evals Course)

### 1. Gulf of Comprehension
- **Gap:** What you think your system does vs. what it actually does
- **How to close:** Manual error analysis. Read every output. No automation can close this gulf.
- **Must be closed first** — everything downstream depends on it.

### 2. Gulf of Specification
- **Gap:** What you want your system to do vs. what your judges actually measure
- **Direct consequence of skipping comprehension.** If you haven't seen real failure, you can't write judges that measure what matters.
- **Symptom:** Judges measuring an imagined target. Optimizing against a fantasy.

### 3. Gulf of Generalization
- **Gap:** Test performance vs. real-world performance on unseen inputs
- **This is what AutoResearch's optimization loop addresses.** But only if the first two gulfs are already closed.

## The Analyze-Measure-Improve Lifecycle

### Phase 1: Error Analysis (closes Gulf of Comprehension)

1. **Open coding** — Run skill on diverse inputs. Read every output. Write freeform notes on what's wrong. Don't categorize yet. Build intuition about failure that no tool can build for you.

2. **Axial coding** — Group freeform notes into a coherent **failure taxonomy**: a small set of distinct, binary failure categories. Examples: "Too abstract," "missed enterprise constraints," "wrong level of specificity." These become what your judges should measure.

### Phase 2: Judge Design (closes Gulf of Specification)

3. **Write judges grounded in the taxonomy** — Each judge maps to an observed failure mode, not an imagined one.

4. **Validate judges with golden dataset** — Manually score 15-20 outputs per criterion before trusting any judge to run autonomously. Check whether the judge agrees with your own labels on cases you've already reasoned about.

### Phase 3: Optimization (closes Gulf of Generalization)

5. **Run AutoResearch** — Only now does automated optimization make sense.

## Author's Three Takes (Progression)

| Take | What Changed | Result |
|------|-------------|--------|
| **1** | Pointed AutoResearch at skill. Let it generate inputs, judges, everything. | Scores went up. Skill got worse. Optimized the wrong things. |
| **2** | Used Hamel's eval skill for structured input generation (dimensions, personas, scenarios). | Better inputs, more diverse. But still no manual reading. Judges still measuring imagined targets. |
| **3** | Read outputs manually. Open-coded failures. Built taxonomy. Wrote judges against observed failures. Validated on 15 outputs. Then ran AutoResearch. | Actually improved the skill. |

## Key Quote

> "If you are not willing to look at some data manually on a regular cadence you are wasting your time with evals."

## Hamel's Eval Skill: Structured Input Generation

More principled than asking a model to generate test cases:
- Define **dimensions of the input space** (what feature, what persona, what scenario)
- Generate **structured tuples** across combinations
- Produces more diverse inputs with better edge case coverage
- But inputs alone aren't enough — judges are where comprehension lives

## Product Parallel

The Gulf of Comprehension has a product equivalent: the gap between what you think users struggle with and what they actually struggle with. It doesn't close from a survey dashboard. It closes when you've personally read enough customer conversations, support tickets, and interviews.

## Relevance to DS Productivity Agents

Our autoresearch runs on ds-review and ds-trace followed a pattern closer to Take 2:
- We designed structured eval suites (v2 evals were better than v1)
- Some evals were grounded in observed failures (location precision came from real observation)
- But we didn't do systematic open coding → axial coding → judge validation
- No golden dataset for judge calibration
- Inline execution may mask production-mode failures

The article suggests our next evolution should add the comprehension phase before running autoresearch optimization loops.
