---
name: ds-review-framework
description: >
  Shared rubrics, scoring tables, audience personas, and routing rules for the DS analysis
  review agent system. Auto-loaded by ds-review-lead, analysis-reviewer, and communication-reviewer
  agents. Contains: (1) severity definitions with verdict impact, (2) deduction tables for 8 review
  lenses across analysis and communication dimensions, (2b) strength credit tables for crediting
  good practices, (3) floor rules that cap verdicts on CRITICAL findings, (4) audience persona
  definitions (exec, tech, DS, mixed) with thinking styles, (5) dimension boundary routing table
  for gray-zone finding ownership, (6) workflow context definitions (proactive, reactive, general),
  (7) common anti-patterns with catching lenses, (8) Confluence structural element guide for
  TL;DR detection.
auto_activate: true
---

# DS Review Framework

Shared knowledge for ds-review-lead, analysis-reviewer, and communication-reviewer agents.
This file is auto-loaded. Agents reference specific sections — do not restructure without
updating all three agent prompts.

---

## 1. Severity Definitions

| Severity | Definition | Impact on Verdict |
|---|---|---|
| CRITICAL | A fundamental flaw that would cause the analysis to fail its purpose — wrong conclusions reached, key audience misled, or decisions made on faulty foundation. The analysis is NOT ready to share. | Floor rule: caps verdict at Minor Fix (max 79). 2+ CRITICAL caps at Major Rework (max 59). |
| MAJOR | A significant gap that weakens the analysis but doesn't invalidate it. The reader can still reach roughly correct conclusions, but the analysis loses impact, credibility, or actionability. | Standard deduction applies (-8 to -12). Multiple MAJORs compound. |
| MINOR | A polish issue that doesn't affect the core message or analytical validity. Nice to fix, not blocking. | Small deduction (-3 to -5). |

---

## 2. Deduction Table

### Analysis Dimension

| Issue Type | Lens | Severity | Deduction | Example |
|---|---|---|---|---|
| Unstated critical assumption | Methodology & Assumptions | CRITICAL | -20 | Causal claim without stating comparability assumption |
| Flawed statistical methodology | Methodology & Assumptions | CRITICAL | -20 | Using correlation to claim causation without acknowledgment |
| Unacknowledged sampling/selection bias | Methodology & Assumptions | MAJOR | -10 | Conclusions from non-representative sample without acknowledging limitation |
| Conclusion doesn't trace to evidence | Logic & Traceability | MAJOR | -10 | Backward check fails — recommendation has no supporting finding |
| Unsupported logical leap | Logic & Traceability | MAJOR | -10 | Key finding not backed by presented evidence |
| Misrepresented source/benchmark | Completeness & Source Fidelity | MAJOR | -8 | "Industry average is X" but source says Y |
| Missing obvious analysis | Completeness & Source Fidelity | MAJOR | -8 | Obvious follow-up question unaddressed |
| Missing baseline/benchmark | Metrics | MAJOR | -10 | Metric reported without comparison point |
| Experimental claims without statistical validation | Methodology & Assumptions | CRITICAL | -15 | A/B test reports observed lift or uses "significant" without p-value, confidence interval, or named statistical test. The presence of experimental structure (test/control, hypotheses) creates an expectation of validation; its absence misleads readers into trusting results that may be noise. |

### Communication Dimension

| Issue Type | Lens | Severity | Deduction | Example |
|---|---|---|---|---|
| TL;DR completely absent | Structure & TL;DR | CRITICAL | -12 | No executive summary, no upfront conclusion, no key insight anywhere in the top 20% of the document. Distinct from an ineffective TL;DR — this is total absence. |
| Missing or ineffective TL;DR | Structure & TL;DR | MAJOR | -10 | Proactive: opens with methodology instead of key insight + business impact. Reactive: opens with background instead of answering the question asked. Use this when a TL;DR exists but is weak or buried — not when it is completely absent. |
| No clear story arc or structure | Structure & TL;DR | MAJOR | -8 | Reader can't follow the argument from setup to conclusion |
| Buried key finding | Structure & TL;DR | MAJOR | -10 | "So what" appears on page 8 instead of upfront |
| Generic/non-actionable headings | Structure & TL;DR | MINOR | -2 | Heading says "Results" instead of "Churn dropped 15% after intervention" |
| Audience mismatch | Audience Fit | MAJOR | -10 | Technical jargon in exec-targeted deck, or insufficient rigor for peer DS |
| Recycled presentation for wrong audience | Audience Fit | MAJOR | -8 | Same deck sent to exec and peer DS without adaptation |
| Limitations/scope unclear for downstream | Audience Fit | MAJOR | -10 | ML Eng builds production model on exploratory finding because caveats were buried |
| Too long / buries signal in noise | Conciseness & Prioritization | MAJOR | -10 | 30-page deck that should be 10; appendix material in main body |
| Data without narrative context | Conciseness & Prioritization | MAJOR | -8 | Metrics table dumped without explanation of what matters |
| Unclear or misleading visualization | Conciseness & Prioritization | MAJOR | -8 | Chart missing axis labels, wrong chart type, or chartjunk |
| Unnecessary chart or table | Conciseness & Prioritization | MINOR | -2 | Chart showing long-tail data that adds no insight |
| Sloppy formatting / inconsistent polish | Conciseness & Prioritization | MINOR | -3 | Mixed fonts, broken indentation, spelling errors |
| Vague recommendation or answer | Actionability | MAJOR | -8 | "We should look into this further" without specifics |
| Recommendation scoped to wrong decision level | Actionability | MAJOR | -8 | VP-level funding decision framed as team-level action item |
| No named owner or next step | Actionability | MINOR | -5 | Recommendation says what but not who or when |
| Missing "so what" for key finding | Actionability | MAJOR | -8 | Finding presented as trivia without business implication |
| Measurement not interpretable by requester | Actionability | MAJOR | -8 | A/B test result without confidence interval or practical significance |
| Over-interpretation boundary unclear | Actionability | MAJOR | -8 | Result presented without stating what the data can and cannot support |

**Severity Escalation Guard:** Subagents MUST use the exact severity and deduction values from
this table. Do not escalate a MINOR to MAJOR or a MAJOR to CRITICAL based on context, workflow
mode, or audience. If an issue type is listed as MINOR above, it stays MINOR at its listed
deduction in every review. The table is the source of truth — no exceptions.

---

## 2b. Strength Credit Table

Subagents award credits for demonstrated good practices. Credits partially offset deductions,
ensuring that analyses which do substantive work score higher than those that don't —
even when both have gaps. Credits reflect effort and rigor that the reader benefits from.

**Cap:** Maximum +25 credits per dimension. Credits beyond the cap are noted but not scored.

### Analysis Dimension Credits

| Strength | Credit | Criteria |
|---|---|---|
| Appropriate methodology for the question | +5 | The chosen analytical approach fits the question being asked. Experiments for causal questions, predictive models for forecasting, classification for categorization, descriptive statistics for exploration. The method must be well-matched to the stated objective, not just present. |
| Systematic model or method comparison | +5 | Compared multiple approaches, models, or methods and justified the final selection. At least 2 alternatives with comparable evaluation metrics. Examples: multi-model comparison with CV scores, A/B test vs. pre-post comparison, multiple feature engineering approaches evaluated. |
| Pre-specified goals or hypotheses | +3 | Goals, hypotheses, or success criteria stated before results. Can be formal hypotheses (experiment), target metrics (ML), or research questions (exploratory). Must appear before the results section, not retrofitted. |
| Validation methodology present | +5 | Claims supported by an appropriate validation approach. Experiments: statistical tests with significance levels and confidence intervals. ML: cross-validation, holdout evaluation, or train/test split with reported metrics. Systems: production metrics, before/after measurement, or impact evaluation. Observational: sensitivity analysis or robustness checks. The validation must match the claim type. |
| Reports specific quantitative results with context | +3 | Specific quantitative results with at least one contextualizing element: comparison to baseline, confidence interval, significance test, or benchmark. A bare number without context (e.g., "accuracy was 70%" with no comparison point) does not qualify. |
| External validation or benchmarking | +3 | Results compared against external baseline, prior period, industry benchmark, or known standard. Must be a genuine external comparison point. |
| Demonstrated real-world impact | +8 | Analysis drove a concrete, measurable real-world outcome: a shipped product change with tracked metrics, a deployed model or system in production with measured performance, or a business decision with stated result. Must point to specific evidence of impact in the document, not just a recommendation or projected benefit. |
| Honest negative or null result reported | +3 | Reports a result that did not work, an approach that failed, or an unexpected finding without spinning it as positive. Must be a substantive finding, not a throwaway mention. |
| Reproducibility detail provided | +2 | Enough methodological detail for another analyst to replicate the approach: data sources, key parameters, methodology steps, and evaluation criteria. |

### Communication Dimension Credits

| Strength | Credit | Criteria |
|---|---|---|
| Effective TL;DR present | +5 | Key insight, business impact, and action/answer stated upfront |
| Story arc matches audience | +5 | Inductive for exec, deductive for tech, layered for mixed — correctly applied |
| Audience-calibrated detail level | +3 | Technical depth appropriate for stated audience, jargon matched to reader |
| Actionable recommendations with owners | +5 | Specific next steps, named owners or teams, timeline or priority indicated |
| Clear limitations stated | +3 | Scope boundaries and caveats presented accessibly for downstream consumers |
| Effective data visualization | +3 | Charts have clear titles stating the takeaway, labeled axes, right chart type |
| Effective worked example or scenario | +3 | Concrete numerical example or relatable scenario that makes an abstract methodology, framework, or finding tangible for the reader. Must walk through specific values, not just describe the approach generically. |
| Progressive disclosure structure | +3 | Summary accessible to all, detail available for those who need it |
| Professional polish throughout | +2 | Consistent formatting, visual hierarchy, no errors — signals credibility |

### Credit Rules

1. **Evidence required:** Only credit strengths you can point to in the document. No inferred credit.
2. **Partial credit allowed:** If a strength is partially present, award half the credit value (round down).
3. **Cap is per-dimension:** Analysis credits cap at +25. Communication credits cap at +25 independently.
4. **Credits do not cancel floor rules:** If a CRITICAL finding triggers a floor rule (Section 3),
   the credit still applies to the numeric score, but the verdict cap remains.
5. **Report in STRENGTH LOG:** Subagents list each credited strength with its value in the output.
6. **Conditional credit for unvalidated experimental claims:** When an analysis presents
   experimental design (test vs. control groups, random assignment, or quasi-experimental
   structure) but reports NO statistical validation for the experimental results (no p-values,
   no confidence intervals, no named statistical tests for any hypothesis), apply:
   - "Appropriate methodology for the question": halved (round down)
   - "Pre-specified goals or hypotheses": halved (round down)
   - "Validation methodology present": award +0 (validation is absent, not partial)
   - "Reports specific quantitative results with context": halved (round down), because
     the reported results are unvalidated experimental claims
   This rule applies ONLY when experimental structure is present but unvalidated. It does NOT
   apply to non-experimental analyses (ML, systems, operational, exploratory), which have their
   own validation forms captured by "Validation methodology present."

---

## 3. Floor Rules

1. **Any CRITICAL finding** in either dimension → verdict capped at **Minor Fix (max 79)**, regardless of computed score.
2. **Two or more CRITICAL findings** across either dimension → verdict capped at **Major Rework (max 59)**.
3. Floor rules override the **verdict band only**, not the numeric score. User sees both: `Score: 85 → Verdict: Minor Fix (floor rule applied)`.
4. Rationale: An analysis with a flawed methodology or missing TL;DR should never be "Good to Go" regardless of arithmetic.

**Verdict Bands:**

| Score | Verdict | Meaning |
|---|---|---|
| 80-100 | Good to Go | Analysis ready to share. Minor polish optional. |
| 60-79 | Minor Fix | Solid foundation, specific issues to address before sharing. |
| 0-59 | Major Rework | Significant gaps that would undermine effectiveness. |

---

## 4. Audience Persona Definitions

### Business Executive
- **Thinking style:** Inductive — "so what?" first, evidence second
- **Expects:** Impact framing, business context, clear recommendation, minimal technical detail
- **Red flags:** Jargon without explanation, methodology-heavy opening, no bottom line upfront
- **TL;DR pattern:** Key insight + business impact + recommended action

### Technical Lead
- **Thinking style:** Deductive — evidence first, conclusion follows
- **Expects:** Sufficient technical detail to evaluate feasibility, clear scope boundaries, implementation implications
- **Red flags:** Hand-wavy methodology, missing edge cases, no limitations section
- **TL;DR pattern:** Direct answer + key evidence + technical caveats

### Peer Data Scientist
- **Thinking style:** Full rigor — wants to evaluate methodology end-to-end
- **Expects:** Statistical detail, reproducibility info, assumption enumeration, alternative approaches considered
- **Red flags:** Causal claims without methodology justification, missing confidence intervals, no sensitivity analysis
- **TL;DR pattern:** Key finding + methodology summary + open questions

### Mixed Audience (Default)
- **Thinking style:** Cross-audience synthesis
- **Expects:** Layered structure — summary accessible to all, detail available for those who need it
- **Red flags:** Content that only works for one audience, missing progressive disclosure
- **TL;DR pattern:** Key insight framed for broadest audience + signposts to detail sections

### Structural Principle
- **Inductive framing** (exec): conclusion → supporting evidence → detail
- **Deductive framing** (tech/DS): evidence → analysis → conclusion
- **Mixed framing**: conclusion upfront, evidence structure below, detail in appendix

---

## 5. Dimension Boundary Routing Table

Defines which subagent owns gray-zone feedback. Prevents duplicate or conflicting findings.

| Gray-Zone Scenario | Owner | Lens | Rationale |
|---|---|---|---|
| Metric without context | analysis-reviewer | Metrics | Missing baseline is an analytical gap |
| Metric without audience-appropriate baseline | communication-reviewer | Audience Fit | The baseline exists but isn't calibrated for the reader |
| Missing limitation | communication-reviewer | Audience Fit | Impact is on downstream consumer interpretation |
| Flawed methodology | analysis-reviewer | Methodology & Assumptions | Even if it affects communication, the root cause is analytical |
| Conclusion without evidence | analysis-reviewer | Logic & Traceability | Unless it's purely a framing/placement issue |
| Buried key finding | communication-reviewer | Structure & TL;DR | The finding exists but isn't positioned for impact |
| Causal claim without comparability | analysis-reviewer | Methodology & Assumptions | Methodological flaw regardless of how it's presented |
| Number without decision context | communication-reviewer | Actionability | The analysis produced the number; comms failed to contextualize it |
| Statistical vs practical significance confusion | analysis-reviewer | Metrics | If the analysis itself conflates them |
| Statistical vs practical significance not communicated | communication-reviewer | Actionability | If the analysis distinguishes them but the presentation doesn't |

**Rule:** When in doubt, assign to the subagent whose lens checklist most directly addresses the issue. If a finding genuinely spans both dimensions, the analysis-reviewer owns the root cause and the communication-reviewer owns the presentation impact — but only if both are independently actionable. Never report the same issue from both subagents.

---

## 6. Workflow Context

### Proactive / Advisory Mode
- **Trigger:** User passes `--workflow proactive` (or analysis is self-initiated)
- **TL;DR expectation:** Leads with key insight + business impact + recommended action
- **Actionability expectation:** Specific, prioritized recommendations with named owners and next steps
- **Example:** "We should invest in feature X because our analysis shows Y. Here's the implementation plan."

### Reactive / Support Mode
- **Trigger:** User passes `--workflow reactive` (or analysis answers a specific question)
- **TL;DR expectation:** Leads with direct answer to the question asked
- **Actionability expectation:** Measurement clear enough for stakeholder to act, confidence intervals provided, practical significance contextualized
- **Example:** "The A/B test shows a 3.2% lift in conversion (95% CI: 1.1%-5.3%, p=0.003). This translates to ~$2.1M annual revenue."

### General Mode (v1 Default)
- **Trigger:** No `--workflow` flag specified (default)
- **TL;DR expectation:** Key insight or answer is clear and upfront
- **Actionability expectation:** Findings have "so what?" context, recommendations are specific enough to act on
- **Key principle:** TL;DR and Actionability are always heavily evaluated regardless of workflow mode

---

## 7. Common Anti-Patterns

| Anti-Pattern | Catching Lens | Description |
|---|---|---|
| Burying the lede | Structure & TL;DR | Key insight appears deep in the document instead of upfront. Reader must wade through context to find the point. |
| Recycled deck | Audience Fit | Same presentation reused for a different audience without adapting detail level, framing, or emphasis. |
| Data dump | Conciseness & Prioritization | Tables, charts, and numbers presented without narrative thread. Reader is left to draw their own conclusions. |
| Unsupported conclusion | Logic & Traceability | Final recommendation or conclusion that doesn't trace back to evidence presented in the analysis. |
| Causal claim without comparability | Methodology & Assumptions | "X caused Y" without establishing a valid comparison group or acknowledging confounders. |
| Number without decision context | Actionability | "Churn is 5.2%" — but is that good or bad? What was it before? What's the benchmark? What should the reader do? |
| Over-interpretation boundary unclear | Actionability | Results presented without stating what the data can and cannot support, risking stakeholder over-extrapolation. |
| Missing TL;DR | Structure & TL;DR | No executive summary, no upfront conclusion. Reader doesn't know the point until the end (if then). |
| Jargon soup | Audience Fit | Technical terminology used without regard for audience. NDCG, p-values, and confidence intervals thrown at a business exec. |
| Zombie appendix | Conciseness & Prioritization | Appendix material (exploratory charts, raw data tables, code snippets) in the main body instead of a clearly separated appendix. |

---

## 8. Confluence Structure Guide

### Where TL;DR Typically Lives
1. Info/Note/Success panel in top 20% of page
2. Bold/emphasized block before first H2 heading
3. Section explicitly named "TL;DR", "Executive Summary", "Summary", "Key Findings"
4. First paragraph (if it reads like a summary)
5. Content-signal scan (keyword detection as fallback)
6. ABSENT — becomes a communication finding

### Structural Elements

| Element | Signal | Agent Usage |
|---|---|---|
| Info/Note/Warning panel | Key callout — likely TL;DR, caveat, or key finding | TL;DR detection checks panels in top 20% |
| Expand macro | Appendix-like content, supplementary detail | Deprioritize in extraction — note existence, don't include |
| Status macro | Draft / In Review / Final | Drafts get lighter polish penalties |
| Table of Contents macro | Page has intentional structure | Positive signal for Structure lens |
| Page labels | May indicate target audience or workflow stage | Informational context, not used for inference |
| Inline comments | Existing reviewer feedback | Note that peer review is in progress |
| Child pages | Analysis spans multiple pages | Note but don't review (v1: single page only) |

### Label Conventions
- Labels like "exec-review", "ds-team", "eng-handoff" provide audience signals
- Labels like "draft", "in-review", "final" provide status signals
- These are informational — the agent does not infer audience from labels in v1
