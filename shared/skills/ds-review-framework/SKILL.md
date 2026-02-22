---
name: ds-review-framework
description: >
  Shared rubrics, scoring tables, audience personas, and routing rules for the DS analysis
  review agent system. Auto-loaded by ds-review-lead, analysis-reviewer, communication-reviewer,
  and domain-expert-reviewer agents. Contains: (1) severity definitions with verdict impact
  including ADVISORY, (2) deduction tables for 11 review lenses across analysis, communication,
  and domain knowledge dimensions, (2b) strength credit tables, (3) floor rules, (4) audience
  persona definitions, (5) dimension boundary routing table with cross-dimension dedup rules,
  (6) workflow context definitions, (7) common anti-patterns, (8) Confluence structural element guide.
auto_activate: true
---

# DS Review Framework

Shared knowledge for ds-review-lead, analysis-reviewer, communication-reviewer, and domain-expert-reviewer agents.
This file is auto-loaded. Agents reference specific sections — do not restructure without
updating all four agent prompts.

---

## 1. Severity Definitions

| Severity | Definition | Impact on Verdict |
|---|---|---|
| CRITICAL | A fundamental flaw that would cause the analysis to fail its purpose — wrong conclusions reached, key audience misled, or decisions made on faulty foundation. The analysis is NOT ready to share. | Floor rule: caps verdict at Minor Fix (max 79). 2+ CRITICAL caps at Major Rework (max 59). |
| MAJOR | A significant gap that weakens the analysis but doesn't invalidate it. The reader can still reach roughly correct conclusions, but the analysis loses impact, credibility, or actionability. | Standard deduction applies (-8 to -12). Multiple MAJORs compound. |
| MINOR | A polish issue that doesn't affect the core message or analytical validity. Nice to fix, not blocking. | Small deduction (-3 to -5). |
| ADVISORY | A suggestion sourced from recent team learnings or post-mortem data (advisory authority). Worth considering but context-dependent — the analysis may validly disagree. | Capped at -2 deduction. Never triggers floor rules. |

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

### Domain Knowledge Dimension

| Issue Type | Lens | Severity | Deduction | Example |
|---|---|---|---|---|
| Fundamentally wrong technique for this domain | Technique Appropriateness | CRITICAL | -20 | Using pointwise classification for a ranking task where pairwise or listwise LTR is standard — the pointwise loss does not optimize for ranking quality [PSE: subtler example] |
| Domain-standard technique ignored without justification | Technique Appropriateness | MAJOR | -10 | Using t-test for conversion rates when chi-squared or bootstrap is domain standard |
| Offline metric used to justify production/launch decision without online validation plan | Technique Appropriateness | MAJOR | -10 | Recommends ranking model change based solely on offline NDCG lift without online experiment plan [PSE: scoped to production decisions] |
| Domain-specific data characteristic unaddressed | Technique Appropriateness | MAJOR | -8 | Click model without position bias correction in search relevance |
| Multi-objective ranking tradeoffs ignored | Technique Appropriateness | MINOR | -7 | Analysis optimizes a single ranking objective without acknowledging known tradeoffs with other dimensions (relevance vs. diversity, relevance vs. freshness, engagement vs. satisfaction) [PSE: added] |
| Non-standard technique used without domain justification | Technique Appropriateness | MINOR | -7 | Novel approach without explaining why standard approach was insufficient |
| Recent learning suggests a better approach | Technique Appropriateness | ADVISORY | -2 | Recent team experiment found that approach X outperforms approach Y for this use case |
| Cited benchmark is fabricated or grossly wrong | Benchmark & External Validity | CRITICAL | -20 | "Industry standard NDCG is 0.90" when actual domain range is 0.40-0.55 |
| Key claim is factually wrong and influences conclusions | Benchmark & External Validity | CRITICAL | -20 | "Google's 2024 study showed X" but study actually showed the opposite |
| External source mischaracterized | Benchmark & External Validity | MAJOR | -10 | Paper cited as supporting the approach, but paper found mixed results |
| Outdated benchmark used as current reference | Benchmark & External Validity | MAJOR | -10 | Using pre-2020 CTR benchmarks for a 2026 search system |
| Cited number is inaccurate but doesn't change conclusions | Benchmark & External Validity | MAJOR | -8 | "Industry average is 12%" when it's actually 8% |
| Benchmark from wrong sub-domain applied | Benchmark & External Validity | MAJOR | -8 | E-commerce search benchmarks applied to document retrieval |
| Internal baseline not sanity-checked against domain norms | Benchmark & External Validity | MINOR | -5 | Reporting a metric without noting whether it's in the expected range |
| Claim unverifiable — no source, web search finds nothing | Benchmark & External Validity | MINOR | -3 | "Research shows that..." with no citation and no verifiable basis |
| Recent learning suggests benchmark is outdated | Benchmark & External Validity | ADVISORY | -2 | Recent team experiment found different baseline than the one cited |
| Known critical pitfall completely ignored | Domain Pitfall Awareness | CRITICAL | -15 | Search relevance eval with no mention of position bias when using click data. Note: CRITICAL when click data informs model decisions or evaluation conclusions. MAJOR (-10) when used for exploratory analysis with acknowledged limitations. [PSE: contextual note] |
| Domain anti-pattern present | Domain Pitfall Awareness | MAJOR | -10 | Optimizing CTR alone in search when it's known to favor clickbait over relevance |
| Selection bias in training data unacknowledged | Domain Pitfall Awareness | MAJOR | -10 | Click-through model trained on logged data without acknowledging logging policy bias. Creates feedback loop: model learns to prefer items it already ranked highly. [PSE: bumped from -8] |
| Metric gaming / Goodhart's Law risk unaddressed | Domain Pitfall Awareness | MAJOR | -8 | Optimizes single engagement metric without discussing proxy risk |
| Known edge case unaddressed | Domain Pitfall Awareness | MAJOR | -8 | Ranking model evaluated only on head queries, no mention of tail query performance. Note: top 1% of queries (head) = 30-50% of traffic; tail queries (30-40% unique) often worst-performing segment. [PSE: emphasis] |
| Evaluation without exploration/exploitation separation | Domain Pitfall Awareness | MAJOR | -8 | Evaluation metrics computed on mixed traffic without separating exploration from exploitation — exploration traffic produces systematically different metric distributions [PSE: added] |
| Pitfall acknowledged but mitigation missing | Domain Pitfall Awareness | MINOR | -5 | "We know position bias exists" but no correction or justification for skipping it |
| Annotation position bias in relevance labels | Domain Pitfall Awareness | MINOR | -5 | Relevance labels collected without randomized presentation order may contain systematic annotation bias, propagating into "gold standard" labels used for offline evaluation [PSE: added] |
| Recent learning highlights a pitfall not addressed | Domain Pitfall Awareness | ADVISORY | -2 | Recent post-mortem found a failure mode relevant to this analysis |

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

### Domain Knowledge Dimension Credits

| Strength | Credit | Criteria |
|---|---|---|
| Domain-standard technique applied correctly | +5 | Technique matches what experts in this domain would choose |
| Alternative techniques considered with domain rationale | +3 | Justified why chosen technique over domain alternatives |
| Domain-specific data preprocessing applied | +3 | Addressed known data issues for this domain (e.g., position debiasing) |
| Benchmarks cited with verifiable sources | +5 | External benchmarks include source, date, and context |
| All key claims cited and verifiable | +3 | Major factual claims include sources that check out |
| Multiple reference points provided | +3 | Compared against >1 baseline (prior period + industry + competitor) |
| Accurate characterization of external work | +2 | Referenced studies described fairly, not cherry-picked |
| Benchmark recency acknowledged | +2 | Noted when benchmarks are from and whether domain has shifted since |
| Proactively addresses domain pitfalls | +5 | Identifies and mitigates known pitfalls without being prompted |
| Domain edge cases explicitly considered | +3 | Analysis addresses known edge cases (segments, tail behavior, cold-start) |
| Anti-pattern awareness demonstrated | +2 | Explains why a common shortcut was avoided or why it's acceptable here |

### Credit Rules

1. **Evidence required:** Only credit strengths you can point to in the document. No inferred credit.
2. **Partial credit allowed:** If a strength is partially present, award half the credit value (round down).
3. **Cap is per-dimension:** Analysis credits cap at +25. Communication credits cap at +25. Domain Knowledge credits cap at +25. Each is independent.
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
7. **ADVISORY coexistence:** ADVISORY findings sourced from advisory content do not affect credit eligibility. A credit and an ADVISORY finding for the same aspect can coexist.

---

## 3. Floor Rules

1. **Any CRITICAL finding** in any dimension → verdict capped at **Minor Fix (max 79)**, regardless of computed score.
2. **Two or more CRITICAL findings** across any dimension → verdict capped at **Major Rework (max 59)**.
3. Floor rules override the **verdict band only**, not the numeric score. User sees both: `Score: 85 → Verdict: Minor Fix (floor rule applied)`.
4. Rationale: An analysis with a flawed methodology or missing TL;DR should never be "Good to Go" regardless of arithmetic.
5. **ADVISORY findings never trigger floor rules.** ADVISORY severity (-2) is informational only. It does not count toward CRITICAL thresholds. Even 10 ADVISORY findings do not affect the verdict.
6. **Floor rules apply equally across all dimensions regardless of scoring weight.** A CRITICAL in the domain dimension (25% weight) caps the verdict identically to a CRITICAL in the analysis dimension (50% weight).

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
| Domain-specific technique choice | domain-expert-reviewer | Technique Appropriateness | Requires specialist knowledge to evaluate |
| Generic statistical method choice | analysis-reviewer | Methodology & Assumptions | Any statistician could evaluate |
| Benchmark accuracy (requires domain knowledge to identify — knowing plausible range) | domain-expert-reviewer | Benchmark & External Validity | Domain-specific range knowledge needed [PSE: routing clarification] |
| Benchmark accuracy (verifiable by reading cited source directly) | analysis-reviewer | Completeness & Source Fidelity | General fact-checking, source says X analysis says Y [PSE: routing clarification] |
| Benchmark accuracy (both could catch, --domain active) | domain-expert-reviewer | Benchmark & External Validity | Domain version takes priority for scoring coherence [PSE: tiebreaker] |
| Domain pitfall (known in the field) | domain-expert-reviewer | Domain Pitfall Awareness | Requires field-specific expertise |
| Unstated assumption (general stats) | analysis-reviewer | Methodology & Assumptions | Generic DS rigor |

**Rule:** When in doubt, assign to the subagent whose lens checklist most directly addresses the issue. If a finding genuinely spans both dimensions, the analysis-reviewer owns the root cause and the communication-reviewer owns the presentation impact — but only if both are independently actionable. Never report the same issue from both subagents.

**Cross-dimension deduplication (analysis vs. domain):** When both analysis-reviewer and
domain-expert-reviewer flag the same underlying issue, the lead agent deduplicates in Step 9.
Two-stage approach: (1) Heuristic — same metric/method name, same document section, and/or
same suggested alternative → deduplicate, keep domain version (more specific). (2) If heuristic
is inconclusive, lead agent compares findings and keeps the domain version if they address
the same root cause. The domain version is preferred because it provides more specific,
actionable feedback.

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
