# Plan: Eval-Grounded AutoResearch for ds-review

**Status:** Approved
**Date:** 2026-03-21
**Goal:** Integrate Hamel Husain's Three Gulfs eval methodology into our autoresearch workflow so that automated prompt optimization runs against validated, grounded judges — not imagined targets.

## Context

Our current autoresearch approach (v2 eval suite, 7 fixtures, binary evals) followed "Take 2" from the Three Gulfs article: structured evals with some observational grounding, but no systematic error analysis, no golden dataset, no judge validation. We achieved 100% on our eval suite, but the evals may have blind spots in failure modes we haven't systematically looked for.

This plan adds the comprehension and specification phases that make the optimization phase meaningful.

## Design Decisions

| Tension | Decision | Rationale |
|---------|----------|-----------|
| **Scale** | ~20-25 traces for error analysis, expand to ~50 for judge validation via synthetic data | 100 traces is impractical for a prompt-based skill. 20-25 is sufficient to reach saturation for a skill with 3 reviewer dimensions. |
| **Trace depth** | Read final output only; dig into subagent traces only when a failure's root cause is unclear | Reading all 4 outputs (3 subagents + synthesis) for 20+ traces is too much. Final output is what the consumer sees. |
| **Judge automation** | Build automated LLM-as-Judge evaluators (Option B) | Automated judges enable truly scalable optimization loops. Manual evals don't scale for autoresearch. |

## Dependencies

- **Hamel's evals-skills plugin** — installed at `~/.claude/plugins/marketplaces/hamelsmu-evals-skills/`, enabled in settings.json. Skills available: `error-analysis`, `generate-synthetic-data`, `write-judge-prompt`, `validate-evaluator`, `eval-audit`.
- **Existing assets** — 7 test fixtures, v2 eval suite, autoresearch changelog, v0.5 calibration reference scores.

## Phases

### Phase 1: Audit Current Evals
**Skill:** `eval-audit`
**Input:** Our existing v2 eval suite (`skills/ds-review/autoresearch-ds-review/eval-suite.md`), test fixtures, autoresearch results
**Process:**
1. Invoke `eval-audit` against our current eval infrastructure
2. It checks 6 diagnostic areas: error analysis, evaluator design, judge validation, human review process, labeled data, pipeline hygiene
3. Produces a prioritized findings report

**Expected outcome:** A concrete list of gaps in our eval system, confirming which of our 5 evals are grounded vs. which are measuring imagined targets. This sets the agenda for Phase 2.

**Deliverable:** `skills/ds-review/autoresearch-ds-review/eval-audit-report.md`

---

### Phase 2: Error Analysis (Gulf of Comprehension)
**Skill:** `error-analysis`
**Input:** 20-25 ds-review outputs on diverse analysis documents
**Process:**
1. **Collect traces** — Run `/ds-review` on 20-25 inputs:
   - Our existing 7 fixtures (already have outputs from v2 baseline)
   - 5-8 new real-world analysis documents (user's own analyses when available, plus new blog posts / reports)
   - 5-8 synthetic documents covering gaps (short drafts, non-search domains, unconventional formats)
   - Each trace = the full final review output (verdict, scores, top findings, dimension breakdowns)

2. **Open coding** — User reads every output. For each, judge: did the review produce useful, accurate feedback? Pass or Fail. For failures, note what went wrong — observations, not explanations.
   - Template: `| Trace ID | Input Document | What went wrong | Pass/Fail |`
   - Do NOT start with pre-defined failure categories. Let them emerge.

3. **Axial coding** — After reviewing ~15 traces, group similar failure notes into 5-10 distinct, binary failure categories.
   - Split notes with different root causes (e.g., "hallucinated finding" vs. "finding exists but wrong severity")
   - Group notes with same root cause (e.g., "vague location" + "says 'throughout'" → "Non-specific finding location")

4. **Label every trace** — Go back through all traces and apply binary labels (pass/fail) per failure category.

5. **Compute failure rates** — Most frequent failure category = where to focus first.

6. **Decide what to fix vs. evaluate** — For each failure category:
   - Can we just fix it? (Add instruction to SKILL.md, fix subagent prompt) → Fix first.
   - Does it warrant an evaluator? (Frequent, high-impact, requires ongoing guard) → Build a judge.
   - Is it rare/low-impact? → Skip for now.

**User's role:** Reading outputs and writing failure notes is irreplaceable manual work. "No automation can close this gulf."

**Deliverable:** `skills/ds-review/autoresearch-ds-review/failure-taxonomy.md`

---

### Phase 3: Expand Input Coverage (Structured)
**Skill:** `generate-synthetic-data`
**Input:** Failure taxonomy from Phase 2, existing fixtures
**Process:**
1. **Define dimensions** for ds-review input space:
   - Document type: empirical analysis, prescriptive guide, exploratory EDA, model evaluation, case study
   - Domain: search-ranking, non-search, no-domain
   - Quality level: high, medium, low
   - Audience: tech, leadership, ds
   - Length: short (<2K words), medium (2-5K), long (5K+)

2. **Draft 20 tuples** — Combinations of dimension values representing realistic test cases. User validates that tuples reflect real scenarios.

3. **Generate more tuples** — LLM generates additional combinations for diversity.

4. **Convert tuples to documents** — For each tuple, either find a matching real document or generate a synthetic analysis document that fits the characteristics.

5. **Filter for quality** — User reviews synthetic documents for realism. Discard and regenerate unrealistic ones.

**Target:** Expand from 7 to ~30 fixtures with systematic coverage. These feed into Phase 4-5.

**Deliverable:** Expanded fixture set + `skills/ds-review/autoresearch-ds-review/input-coverage-matrix.md`

---

### Phase 4: Write Automated Judges (Gulf of Specification)
**Skill:** `write-judge-prompt`
**Input:** Failure taxonomy from Phase 2, labeled traces
**Process:**

For each failure mode that warrants an evaluator (from Phase 2, Step 6):

1. **Design the judge** — Each judge has 4 components:
   - Task + evaluation criterion (one failure mode per judge)
   - Binary Pass/Fail definitions (from the failure taxonomy)
   - Few-shot examples (from training split of labeled data — clear Pass, clear Fail, borderline)
   - Structured output format (critique-first, then verdict)

2. **Decide what to feed the judge** — For ds-review, judges typically need:
   - The input analysis document (or relevant excerpt)
   - The ds-review output (findings, scores, verdict)
   - For correctness checks: both the source and the finding that claims to reference it

3. **Prefer code-based checks where possible** — Some failure modes don't need an LLM judge:
   - Location precision → regex/keyword check for banned phrases ("throughout", "entire document")
   - Dimension score consistency → arithmetic check on score math
   - Reserve LLM judges for subjective criteria (finding relevance, fix actionability, severity appropriateness)

**Deliverable:** Judge prompt files in `skills/ds-review/autoresearch-ds-review/judges/` — one per failure mode.

---

### Phase 5: Validate Judges (Gulf of Specification, continued)
**Skill:** `validate-evaluator`
**Input:** Judge prompts from Phase 4, labeled traces from Phase 2
**Process:**

1. **Split labeled data** — Train (10-20%, source of few-shot examples), Dev (40-45%, iteration), Test (40-45%, final measurement). ~50 labeled traces needed total (expand with synthetic data from Phase 3 if needed).

2. **Run each judge on dev set** — Compare judge predictions to human labels.

3. **Measure TPR and TNR** per judge:
   - TPR: When human says Pass, how often does judge agree?
   - TNR: When human says Fail, how often does judge agree?
   - Target: both > 90%. Minimum acceptable: both > 80%.

4. **Inspect disagreements** — For every case where judge ≠ human:
   - False Pass (judge too lenient): Strengthen Fail definitions, add edge-case examples
   - False Fail (judge too strict): Clarify Pass definitions, adjust examples

5. **Iterate** — Refine judge prompt, re-run on dev set. Repeat until TPR/TNR stabilize.

6. **Final measurement** — Run once on held-out test set. Record final TPR/TNR. Do not iterate after seeing test results.

**User's role:** Providing the human labels (Pass/Fail per failure mode per trace). This is the golden dataset — the calibration ground truth.

**Deliverable:** `skills/ds-review/autoresearch-ds-review/golden-dataset.md` + judge validation report with TPR/TNR per judge.

---

### Phase 6: Run AutoResearch (Gulf of Generalization)
**Skill:** Our existing autoresearch workflow
**Input:** Validated judges from Phase 5, expanded fixtures from Phase 3
**Process:**

1. **Reset baseline** — Run current SKILL.md through ALL validated judges on ALL fixtures. This is Experiment 0 for the new eval suite. Expect baseline well below 100% — that's the signal that judges are measuring real gaps.

2. **Run `eval-audit`** — Meta-check the new eval pipeline before trusting optimization results.

3. **Optimization loop** — Same mutation-test-keep/discard cycle:
   - Propose mutation to SKILL.md or subagent prompts
   - Run against all fixtures with automated judges
   - Keep if pass rate improves, discard if not
   - Track in changelog

4. **Apply winning mutations** — Update production SKILL.md and subagent prompts.

**Deliverable:** Updated SKILL.md + `skills/ds-review/autoresearch-ds-review/changelog.md` (v3)

---

### Phase 7: Production Validation
**Input:** Optimized SKILL.md from Phase 6
**Process:**

1. Run actual `/ds-review` (with real subagent dispatch via Task tool) on 3-5 fixtures.
2. Compare output quality to inline autoresearch results.
3. Measure the inline-vs-production gap — we know inline execution scores higher.
4. If gap is significant, consider adding production-specific mutations.

**Deliverable:** `skills/ds-review/autoresearch-ds-review/production-validation.md`

---

## Execution Notes

### Phase Dependencies
```
Phase 1 (Audit) → informs Phase 2
Phase 2 (Error Analysis) → feeds Phase 3, 4, 5
Phase 3 (Input Expansion) can run in parallel with Phase 4
Phase 4 (Write Judges) → feeds Phase 5
Phase 5 (Validate Judges) → feeds Phase 6
Phase 6 (AutoResearch) → feeds Phase 7
```

### Session Boundaries
- **Session 1:** Phase 1 (audit) + Phase 2 start (run reviews, user reads outputs)
- **Session 2:** Phase 2 finish (taxonomy) + Phase 3 (expand inputs) + Phase 4 (write judges)
- **Session 3:** Phase 5 (validate judges) + Phase 6 (autoresearch optimization)
- **Session 4:** Phase 7 (production validation)

Phase 2 requires the most user involvement (reading outputs). The other phases are more collaborative with Claude doing the mechanical work.

### What Carries Forward from Current State
- 7 existing fixtures → core of trace set
- v2 evals that ARE grounded (location precision, severity inflation) → may survive as judges
- Autoresearch infrastructure (changelog, results format) → reused
- v0.5 calibration reference scores → separate validation benchmark

### What Gets Replaced
- v2 eval suite → replaced by taxonomy-grounded automated judges
- Ad hoc fixture selection → replaced by dimension-based coverage matrix
- Manual eval scoring → replaced by automated LLM-as-Judge evaluation

## References
- Article: `docs/research/three-gulfs-autoresearch-evals.md`
- Hamel's skills: `~/.claude/plugins/marketplaces/hamelsmu-evals-skills/skills/`
- Current eval suite: `skills/ds-review/autoresearch-ds-review/eval-suite.md`
- Current autoresearch changelog: `skills/ds-review/autoresearch-ds-review/changelog.md`
