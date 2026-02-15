# Development Backlog

Last updated: 2026-02-15

## Current Sprint: v0.4 — Calibration & Testing (IN PROGRESS)

### Done
- [x] First real-world test: meta-llm-bug-reports (scored 18/100 — too harsh)
- [x] Second real-world test: rossmann-sales-prediction (scored 29/100 — too harsh)
- [x] Third real-world test: vanguard-ab-test (scored 16/100 — LOWER than Meta's 18 despite being a better analysis)
- [x] Calibration notes written: `dev/test-results/2026-02-15-calibration-notes.md`
- [x] Principal AI Engineer assessment: `dev/test-results/2026-02-15-principal-ai-engineer-assessment.md`
- [x] PM Lead review completed: `dev/reviews/2026-02-15-pm-lead-calibration-review.md`
- [x] DS Lead assessment completed: `dev/test-results/2026-02-15-ds-lead-assessment.md`
- [x] UX decisions approved: compressed per-lens detail, emoji lens dashboard, highlighted rewrites
- [x] 12 real-world fixtures collected in `dev/test-fixtures/real/`
- [x] All 3 calibration perspectives collected
- [x] A3 fix plan synthesized: `dev/test-results/2026-02-15-calibration-fix-plan.md`
- [x] Calibration loop workflow planned: `docs/plans/2026-02-15-calibration-loop-workflow.md`
- [x] **All 5 owner decisions resolved** (see CHANGELOG for details)
- [x] **P0: Strength Credits implemented** — Section 2b added to SKILL.md (+25 cap/dimension), STRENGTH LOG added to both subagent output formats, lead Step 9 updated
- [x] **P0: CRITICALs reclassified** — 3 communication CRITICALs → MAJOR (missing TL;DR, no story arc, limitations absent). Added Severity Escalation Guard.
- [x] **P0: Diminishing Returns implemented** — Lead Step 9 rewritten with DR formula + credits
- [x] **P0: Severity escalation guard** — Subagents cannot escalate beyond deduction table values
- [x] **Calibration R1 complete** — Scores: Vanguard 73, Meta 59, Rossmann 71 (over-corrected, all above targets)
  - R1 notes: `dev/test-results/2026-02-15-r1-calibration-notes.md`
  - Comparison: `dev/test-results/2026-02-15-r1-vs-r0-comparison.md`
- [x] **R2 fix: Tightened DR curve** from 100/50/25 to 100/75/50
- [x] **R2 fix: Added "TL;DR completely absent" CRITICAL (-12)** back to communication table
- [x] **Calibration R2 complete — ACCEPTED** — Scores: Vanguard 69, Meta 54, Rossmann 71
  - R2 notes: `dev/test-results/2026-02-15-r2-calibration-notes.md`
  - Differentiation: 15 points (Vanguard vs Meta) — meets target
  - CRITICALs: 1 per test — within ≤2 target
  - All scores within updated target ranges
- [x] ADR-003 created: `dev/decisions/ADR-003-calibration-approach.md`

### To Do — Extended Validation
- [ ] **Review Airbnb Message Intent** (`dev/test-fixtures/airbnb-message-intent-classification.md`)
  - Expected: Analysis 55-65/100, Communication 70-80/100
  - Test: Can agent spot both strengths (CNN justification, error analysis) AND gaps (missing F1, no business impact)?
  - Domain: NLP/ML classification (two-phase: LDA → CNN)
- [ ] **Review Airbnb Future Value (FIV)** (`dev/test-fixtures/airbnb-future-value-tradeoffs.md`)
  - Expected: Analysis 65-75/100, Communication 70-80/100
  - Test: Different methodology (causal inference via PSM vs ML classification)
  - Domain: Propensity score matching, counterfactual reasoning
- [ ] **Review Netflix Proxy Metrics** (`dev/test-fixtures/netflix-proxy-metrics.md`)
  - Expected: Analysis 60-70/100, Communication 65-75/100
  - Test: Experimental design focus (metric selection, not model building)
  - Domain: Statistical estimators (TC, JIVE, LIML), correlated measurement error
  - Note: Shorter article (17KB) - may lack depth in some areas
- [ ] Cross-run consistency: same doc 3x, verify scores within ±10
- [ ] Rerun 2-3 synthetic fixtures to verify floor rules still work
- [x] Web session independent rubric evaluation received and reviewed
  - IC9 architect review: `dev/reviews/2026-02-15-ic9-architect-review-of-web-session.md`
  - PM Lead review: `dev/reviews/2026-02-15-pm-lead-review-of-web-session.md`
  - 5 of 6 fixes accepted, 1 deferred to v0.5

### To Do — Web Session Fixes (Reviewed, Not Yet Implemented)
- [ ] **P0: Duplicate-finding detection** — Add dedup rule to ds-review-lead.md Step 9 (NOT SKILL.md — subagents run in parallel). When findings share same root cause across dimensions, apply larger deduction only.
- [ ] **P0: Formatting deduction -5 → -3** — SKILL.md Section 2, "Sloppy formatting / inconsistent polish"
- [ ] **P1: Worked example credit (+3)** — Add to SKILL.md Section 2b Communication credits
- [ ] **P1: Honest negative result credit (+3)** — Add to SKILL.md Section 2b Analysis credits
- [ ] **P1: Tighten "Reports specific quantitative results" criteria** — Require contextualizing element (comparison, CI, benchmark)
- [ ] **P1: Headings -3 → -2, unnecessary chart -3 → -2** — SKILL.md Section 2
- [ ] **P1: Fix self-deliberation in communication-reviewer prompt** — Add single-pass commit instruction

### To Do — P1 Items (Post-Calibration)
- [ ] **P1: Output Restructure**
  - Add emoji indicators to lens dashboard (✅/⚠️/❌)
  - Compress per-lens detail to 1-2 sentences
  - Use blockquote format for suggested rewrites
  - Update lead agent Step 10 output templates
- [ ] **P1: Reduce Finding Volume** — Cap at 10, defer implementation to Phase 2

### Deferred
- Genre/format auto-detection — DS Lead recommends for v0.5 (affects finding generation, not just scoring)
- Novel framework credit (+5) — Deferred to v0.5 (evidence from blog posts, not internal analyses; subjectivity risk at +5)
- Communication dimension asymmetry (134 vs 101 deduction points) — Track for v0.5, design-level issue
- Audience-weighted dimension averaging — v1.5 architecture change
- CRITICAL-ABSENT vs CRITICAL-INCOMPLETE gradation — try reclassification first, add gradation if needed
- Per-dimension deduction cap at -70 — diminishing returns makes this redundant
- Cross-cutting deduction deduplication — diminishing returns partially addresses
- Cluster-based scoring — Engineer recommends for v1.5

## Previous Sprint: v0.3 — Implementation (COMPLETE)

### Done
- [x] Architecture approved by product owner
- [x] Implementation plan v1 created (writing-plans skill)
- [x] IC8 review of implementation plan — 3 Critical + 5 Major issues identified
- [x] Agent prompts written (complete production prose, not outlines):
  - `plugin/agents/analysis-reviewer.md` (146 lines, 4 lenses, 17 checklist items)
  - `plugin/agents/communication-reviewer.md` (108 lines, 4 lenses, 18 checklist items)
  - `plugin/agents/ds-review-lead.md` (178 lines, 10-step pipeline)
- [x] Implementation plan revised to Rev 2 — all IC8 issues addressed
- [x] Parallel Opus code review of architecture + implementation plan (v0.2.2)
  - Architecture: 1C / 6M / 4m → all resolved
  - Impl plan: 1C / 3M / 4m → all resolved
- [x] Doc consistency fixes — 9 files, 28 edits, verified clean
- [x] Implementation plan revised to Rev 3 — skill-creator approach + .gitignore + enhanced frontmatter

### Done (Implementation)
- [x] Task 0: Validate auto_activate runtime behavior in subagent contexts
  - Finding: auto_activate does NOT work in subagents. ADR-002 created.
  - Fix: lead agent instructs subagents to read SKILL.md from disk.
- [x] Task 1: Write SKILL.md (209 lines, 8 sections, all rubrics and deduction tables)
- [x] Task 2: Validate agent prompts (instruction counts: analysis ~47, comm ~52, lead ~105)
- [x] Task 3: Update review.md command definition with --mode, --audience, --workflow flags
- [x] Task 4: Update plugin.json to v0.3.0
- [x] Task 5: Create 8 synthetic test fixtures (all in dev/test-fixtures/synthetic/)
- [x] Task 6: Integration smoke test — 59/59 checks pass across 9 test runs
- [x] Task 7: Session wrap-up (this update)

## Previous Sprint: v0.2 — Architecture Design (COMPLETE)

- [x] PRD and reference docs imported to `dev/specs/`
- [x] Architecture design session completed
- [x] 13 architecture decisions resolved
- [x] Architecture design document written (Rev 4)
- [x] PM lead review completed
- [x] CHANGELOG.md created

## Backlog: v1.0 and Beyond

### v0.5: Genre Awareness (if needed after v0.4 calibration)
- [ ] Evaluate whether recalibrated scores are reasonable across genres without format detection
- [ ] If still off: design `--format` parameter or auto-detection (ADR needed)

### v1.0: Ship
- [ ] All agents passing manual eval rubric
- [ ] Output format verified across all modes
- [ ] Plugin.json updated to v1.0
- [ ] Handoff documentation complete

### v1.5: Auto-Eval & Iteration
- [ ] Build LLM-as-Judge auto-eval pipeline (Section 15.3)
- [ ] Add review quality feedback loop ("Was this helpful?")
- [ ] Calibrate score weighting by workflow context
- [ ] Add workflow context inference (if usage data justifies)
- [ ] Add predictive session freshness detection (if reviews frequently fail)
- [ ] Support non-Confluence/non-md input formats

### v2.0: Extended Features
- [ ] Multi-page Confluence analysis review
- [ ] Iterative review with diff mode (compare to previous review)
- [ ] Agent Studio deployment for non-technical users

## Notes
- Architecture doc: `docs/plans/2026-02-14-architecture-design.md` (Rev 4)
- Implementation plan: `docs/plans/2026-02-14-implementation-plan.md` (Rev 3)
- Implementation order: Tasks 0-5 parallel → Task 6 smoke test → Task 7 wrap-up
