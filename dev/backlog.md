# Development Backlog

Last updated: 2026-02-16

## Repository Rebrand Decision (2026-02-16)

**Decision:** Rename repository from `DS-Analysis-Review-Agent` to `ds-productivity-agents` to reflect multi-agent platform scope.

**Rationale:**
- Building 3 peer-level agents (DS review, SQL review, Search metric analysis)
- All agents share `search-domain-knowledge` skill infrastructure
- DS review is domain-agnostic; can work with any domain knowledge skill (Search, Causal, NLP, etc.)
- SQL review is also domain-agnostic with pluggable domain guidance
- Metric analysis agent calls both the skill and DS review agent as dependencies
- "DS Productivity Agents" accurately describes the platform scope

**Status:**
- [x] Decision made
- [x] Rename steps documented in `dev/RENAME-STEPS.md`
- [x] Migration plan written in `dev/migration-plan.md`
- [x] Execute GitHub rename (COMPLETE - 2026-02-16)
- [x] Execute file reorganization (COMPLETE - 2026-02-16)
- [x] Update documentation (COMPLETE - 2026-02-16)
- [x] Commit and push all changes (COMPLETE - commit 7aa989f)

**Result:** Repository successfully migrated to multi-agent platform structure. All changes committed and pushed to GitHub. See `dev/sessions/2026-02-16-multi-agent-platform-migration.md` for full details.

---

## Current Sprint: v1.1 — Multi-Agent Platform (COMPLETE)

### Done — Platform Migration (2026-02-16)
- [x] **Repository renamed** — `DS-Analysis-Review-Agent` → `ds-productivity-agents`
- [x] **File reorganization complete** — `shared/skills/`, `agents/ds-review/`, placeholders for future agents
- [x] **Documentation updated** — CLAUDE.md, README.md (rewritten), MEMORY.md, backlog.md
- [x] **Path references updated** — 6 files updated to new structure
- [x] **Migration artifacts created** — migration-plan.md, RENAME-STEPS.md, session logs
- [x] **Domain knowledge design docs moved** — from Downloads to `docs/plans/` and `dev/sessions/`
- [x] **All changes committed and pushed** — commits e695ccc, 7aa989f, 45e0172
- [x] **CHANGELOG updated** — v1.1.0 entry added
- [x] **Session log** — `dev/sessions/2026-02-16-multi-agent-platform-migration.md`

**Outcome:** Repository is now a multi-agent platform ready for v0.5 (domain knowledge skill) and Q2 2026 agents (SQL review, metric analysis).

---

## Previous Sprint: v1.0 — Public Distribution (SHIPPED)

### Done — v1.0 Distribution (2026-02-15)
- [x] **Distribution package created** — `dist/ds-analysis-review/` with standalone plugin structure
- [x] **Path migration** — All `plugin/` → `${CLAUDE_PLUGIN_ROOT}/`, all `/ds-review:review` → `/review`
- [x] **plugin.json v1.0.0** — Auto-discovery, MIT license, keywords for discoverability
- [x] **README.md** — Install, usage, architecture, scoring (150 lines)
- [x] **GitHub repo published** — `surahli123/ds-analysis-review` (public)
- [x] **Vibe coding journey doc** — `docs/vibe-coding-journey.md` (~1,566 words, storytelling format)
  - 3 communication-reviewer rounds during drafting
  - Reviewed and accepted by product owner
- [x] **Session log** — `dev/sessions/2026-02-15-v1-distribution-and-journey-doc.md`

### Done — Plugin Command Validation (2026-02-16)
- [x] **Project command validated** — `/ds-review` tested after session restart, 7/7 checks passed
- [x] **File-reference approach confirmed** — single source of truth working (command → reads agent/skill files)
- [x] **Score comparison with R3** — Vanguard scored 60/51 (Quick/Full) vs R3's 72, expected due to v0.4.1 fixes
- [x] **Cross-run variability measured** — ±9-11 points between Quick and Full modes (at edge of acceptable)
- [x] **Test log created** — `dev/test-results/2026-02-16-plugin-registration-test.md`
- [x] **Session log** — `dev/sessions/2026-02-16-plugin-command-validation.md`

### To Do — Post-Ship
- [ ] **Test `claude plugins install surahli123/ds-analysis-review`** in fresh session
- [ ] **Test `/review` command** after plugin install (vs project command `/ds-review`)
- [ ] **Publish journey doc** to LinkedIn/portfolio

---

## Previous Sprint: v0.4 — Calibration & Testing (COMPLETE)

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
- [x] Calibration loop workflow planned: `dev/internal/2026-02-15-calibration-loop-workflow.md`
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
- [x] **Session: Blog Articles & Workflow Update** (2026-02-15)
  - Downloaded 5 DS blog articles using Playwright (Airbnb x3, Netflix, Udemy)
  - Evaluated and selected 3 best candidates (Message Intent, FIV, Proxy Metrics)
  - Updated calibration loop workflow to 6 fixtures (3 core + 3 extended)
  - Session log: `dev/sessions/2026-02-15-blog-articles-and-workflow-update.md`

### Done — R3 Calibration (2026-02-15)
- [x] **All 6 test fixtures reviewed** — 3 core + 3 extended blog posts
  - Vanguard: 72/100 (Analysis 68, Communication 77)
  - Meta: 63/100 (Analysis 64, Communication 61)
  - Rossmann: 86/100 (Analysis 100, Communication 72)
  - Airbnb Message Intent: 85/100 (Analysis 93, Communication 78)
  - Airbnb FIV: 90/100 (Analysis 97, Communication 83)
  - Netflix Proxy Metrics: 100/100 (Analysis 100, Communication 100)
- [x] **R3 calibration notes** — `dev/test-results/2026-02-15-r3-calibration-notes.md`
- [x] **R3 vs R2 comparison** — `dev/test-results/2026-02-15-r3-vs-r2-comparison.md`
- [x] **3 role reviews completed (parallel)**
  - Principal AI Engineer: `dev/test-results/2026-02-15-r3-principal-ai-engineer-assessment.md`
  - PM Lead: `dev/reviews/2026-02-15-r3-pm-lead-calibration-review.md`
  - DS Lead: `dev/test-results/2026-02-15-r3-ds-lead-assessment.md`
- [x] **R3 fix plan synthesized** — `dev/test-results/2026-02-15-r3-calibration-fix-plan.md`
- [x] **Immediate fix applied** — Downgraded "Conclusion doesn't trace" from CRITICAL to MAJOR (Meta now has 2 CRITICALs)
- [x] **Session log** — `dev/sessions/2026-02-15-r3-calibration-execution.md`

**Key R3 Findings:**
- Score inflation: All 6 tests scored 17-30 points above targets
- Root cause: Credit additions (+6) without offsetting deductions created +10-12 point inflation
- All P0/P1 fixes worked correctly (no bugs)
- Finding quality excellent (8/8 Vanguard findings legitimate per DS Lead audit)
- System is 1-2 rounds from acceptance (tuning problem, not architecture problem)

### Done — Plugin Registration (2026-02-15)
- [x] **Researched Claude Code plugin system** — plugins install via marketplace/GitHub, not project dirs
- [x] **Created project-level command** — `.claude/commands/ds-review.md` (invoke as `/ds-review`)
- [x] **Naming conflict resolved** — renamed from `/review` (collided with code-review plugin)
- [x] **Structural validation** — 7/7 checks passed (frontmatter, file refs, agent/skill files)
- [x] **Documented process** — `dev/PLUGIN-REGISTRATION-PROCESS.md`
- [x] **Test `/ds-review` after session restart** — 7/7 checks passed, file-reference approach validated. Test log: `dev/test-results/2026-02-15-plugin-registration-test.md`
- Key finding: `agent:` frontmatter field doesn't exist in Claude Code — command body must contain all instructions
- Open question: `model: opus` frontmatter may not override session-level `/model` selection — needs verification

### To Do — R4 Calibration (command test PASSED — ready to proceed)
- [ ] **Primary fix:** Reduce credit cap from +25 → +15 per dimension
- [ ] **Secondary fix (if needed):** Increase 2-3 MAJOR deductions by +2 each
- [ ] **Re-run all 6 test fixtures** as R4
- [ ] **Cross-run consistency:** Same doc 3x, verify scores within ±10
- [ ] **Rerun 2-3 synthetic fixtures** to verify floor rules still work
- [x] Web session independent rubric evaluation received and reviewed
  - IC9 architect review: `dev/reviews/2026-02-15-ic9-architect-review-of-web-session.md`
  - PM Lead review: `dev/reviews/2026-02-15-pm-lead-review-of-web-session.md`
  - DS Lead review: `dev/reviews/2026-02-15-ds-lead-proposal-review.md`
  - All 3 roles reviewed. 5 of 6 fixes accepted, 1 deferred to v0.5
- [x] **Synthesize all 3 reviews** — Final implementation spec: `dev/specs/synthesis-final-implementation-spec.md`
  - 7 fixes accepted (2 P0, 5 P1), 1 deferred (novel framework → v0.5 with gate)
  - DS Lead opinions weighted most heavily (internal DS tool)
  - 3 open questions for product owner (Section 6)
- [x] **Product owner decisions on 3 open questions** — All resolved:
  - Q1: v0.5-with-gate for novel framework credit (auto-push to v1.5 if no fixture fires it)
  - Q2: Bundle finding volume cap with these fixes (accept harder attribution)
  - Q3: Try Step 9 dedup prose first, escalate if needed
- [ ] **Next: Implement fixes** per synthesis spec Section 5 (implementation order)

### Done — Web Session Fixes (v0.4.1, implemented on `feat/v0.4.1-credit-redesign`)
- [x] **P0: Duplicate-finding detection** — Tightened dedup rule in ds-review-lead.md Step 9 (item 3). Same root cause AND same observable problem test. Cross-dimension different-harm findings both stand.
- [x] **P0: Formatting deduction -5 → -3** — SKILL.md Section 2 (applied in prior session)
- [x] **P0: CRITICAL deduction for unvalidated experiments (-15)** — NEW. Added to SKILL.md Section 2.
- [x] **P0: Analysis credit table replaced** — 9 methodology-agnostic credits + conditional halving rule (Credit Rule 6)
- [x] **P1: Worked example credit (+3)** — SKILL.md Section 2b Communication credits (applied in prior session)
- [x] **P1: Honest negative result credit (+3)** — SKILL.md Section 2b Analysis credits (applied in prior session)
- [x] **P1: Tighten "Reports specific quantitative results" criteria** — Requires contextualizing element (applied in prior session)
- [x] **P1: Headings -3 → -2, unnecessary chart -3 → -2** — SKILL.md Section 2 (applied in prior session)
- [x] **P1: Fix self-deliberation** — communication-reviewer Rule 12: single-pass evaluation
- [x] **P1: Finding volume cap (10 max)** — Lead Step 9 item 8. Score uses all findings, display capped.

### Done — Emoji Dashboard (2026-02-15)
- [x] **P1: Emoji severity indicators (Phase 1)** — 4-tier mapping added to lens dashboard, findings, top 3 fixes, verdict line
  - Design doc: `dev/internal/2026-02-15-emoji-dashboard-design.md`
  - 3 UX reviews (Principal AI Engineer, PM Lead, DS Lead) — all approved
  - Verified in both full and quick mode
  - Merged to main via PR #1

### To Do — P1 Items (Post-Calibration)
- [ ] **P1: Output Restructure — Phase 2** (from UX reviewer feedback)
  - Compress per-lens detail to 1-2 sentences
  - Use blockquote format for suggested rewrites
  - Dashboard-to-findings navigation (cross-references)
  - "What You Did Well" visual treatment
  - Effort-based finding grouping

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

### v0.5: Domain Knowledge Dimension + Genre Awareness

**Design & Planning Complete — Ready to Implement Layer 1**

#### Done — Design (2026-02-15 to 2026-02-16)
- [x] **Design doc v3 complete** — `docs/plans/domain-knowledge/design-v3.md`
  - 3rd review dimension: domain expertise + claim verification (3 lenses, Lens 4 merged into Lens 2)
  - **Architecture:** Standalone Domain Knowledge Skill (Layer 1) + Thin Domain Expert Reviewer (Layer 2)
  - Layer 1: YAML index, digests, refresh pipeline, importance scoring, token budgeting
  - Layer 2: 3 lenses, deduction tables, scoring rubric, calls Layer 1 for context
  - 21 design decisions finalized, 8 gaps resolved in v3
  - Weighted scoring: 50/25/25 (Analysis / Communication / Domain)
  - ADVISORY severity level for recent learnings (-2 deduction cap)
  - Two-tier digest system: foundational (monthly) + workstream (weekly)
  - Deduplication: two-stage (heuristic + LLM fallback)
  - Versioned digests with rollback support
- [x] **MVP design review** — `docs/plans/domain-knowledge/mvp-design.md`
  - 5 challenges resolved (A1-A5): file contract, audience tags, manual refresh, no roster, additive cross-domain budget
  - Token budget: 8K/domain + 1.5K cross-domain (additive)
  - search-infra deferred (least useful for DS review MVP)
- [x] **Layer 1 implementation plan** — `dev/internal/2026-02-16-domain-knowledge-layer1-implementation-plan.md`
  - 5 tasks: domain-index.yaml, SKILL.md contract, 3 digest files
  - Full file contents specified, validation steps, commit strategy
  - Markdown + YAML only, no scripts or dependencies
- [x] **Design session logs** — `dev/sessions/2026-02-15-domain-knowledge-session-log.md`, `dev/sessions/2026-02-16-domain-knowledge-layer1-planning.md`
- [x] **Repository structure prepared** — `shared/skills/search-domain-knowledge/` ready for implementation

#### Next — Layer 1 Implementation (next session)
- [ ] Execute Layer 1 plan: `dev/internal/2026-02-16-domain-knowledge-layer1-implementation-plan.md`
  - Task 1: domain-index.yaml (curated YAML index, 2 sub-domains + cross-domain)
  - Task 2: SKILL.md (digest format contract, consumption guide, staleness rules)
  - Task 3: search-ranking.md digest (foundational knowledge + workstream placeholders)
  - Task 4: query-understanding.md + search-cross-domain.md digests
  - Task 5: Validation and cleanup

#### Future — Layer 2 & 3 (after Layer 1 validated)
- [ ] Create `agents/ds-review/domain-expert-reviewer.md` (3 lenses, authority-aware scoring)
- [ ] Update `shared/skills/ds-review-framework/SKILL.md` with domain dimension rubrics + ADVISORY severity
- [ ] Update `agents/ds-review/ds-review-lead.md` for 3-dimension scoring (--domain flag, 50/25/25)
- [ ] Update `plugin/commands/review.md` with --domain, --reference, --refresh-domain flags
- [ ] Calibration R4+: Test with domain dimension, adjust DR curve if needed
- [ ] Evaluate whether recalibrated scores are reasonable across genres without format detection
- [ ] If still off: design `--format` parameter or auto-detection (ADR needed)

### v1.0: Ship — COMPLETE (2026-02-15)
- [x] All agents passing manual eval rubric
- [x] Output format verified across all modes
- [x] Plugin.json updated to v1.0
- [x] Handoff documentation complete (README.md in dist/)
- [x] GitHub repo published: `surahli123/ds-analysis-review`

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
- Architecture doc: `docs/plans/ds-analysis-review/architecture-design.md` (Rev 4)
- Implementation plan: `dev/internal/2026-02-14-implementation-plan.md` (Rev 3)
- Implementation order: Tasks 0-5 parallel → Task 6 smoke test → Task 7 wrap-up
