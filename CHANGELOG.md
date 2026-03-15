# Changelog

All notable changes to DS Productivity Agents (formerly DS Analysis Review Agent).

## [Unreleased]

### v0.6.0 — Plugin Skill Set Refactoring (2026-03-14)

**Status:** COMPLETE. Migrated from custom agents/ + shared/skills/ to Claude Code plugin skill set.

#### Structural Changes
- **New plugin structure** — `.claude-plugin/plugin.json` + `skills/` + thin command
- **2 skills created** — `ds-review` (orchestrator + 3 reviewer references + framework) and `search-domain-knowledge` (digests + domain index + consumption contract)
- **Thin command** — `.claude/commands/ds-review.md` reduced from 44 to 10 lines, delegates to SKILL.md
- **Path resolution** — skill-relative within skills, project-relative for cross-skill and subagent dispatch
- **Old directories removed** — `agents/`, `shared/`, `plugin/`, `dist/`

#### Bug Fixes
- **Credit cap aligned** — +25 → +15 in orchestrator Step 9 and all 3 reviewer files. Now consistent with framework.md Section 2b. (DS Lead recommendation, R4 calibration validated +15.)
- **Bare SKILL.md disambiguation** — ~35 bare `SKILL.md` references in reviewer files updated to `framework.md` to avoid ambiguity with orchestrator SKILL.md.

#### Documentation
- CLAUDE.md, README.md updated for skill architecture
- `.claude/rules/plugin-conventions.md` rewritten for skill-based development
- IC9 Search SME findings captured in backlog (domain knowledge gaps, missing feedback loop)

#### Review Process
- 4 independent reviews: DS Lead, PM Lead, Principal AI Engineer, IC9 Search SME
- Plugin discovery mechanism validated (Task 0 gate)
- Path resolution strategy confirmed (skill-relative, no ${CLAUDE_PLUGIN_ROOT})
- Verify-before-delete ordering applied

---

### v0.5 — Domain Expert Agent: Design & Layer 1 Implementation (2026-02-16 to 2026-02-21)

**Status:** COMPLETE. Layer 1 + Layer 2 + full `--domain` calibration passed. Ship-ready.

#### R4 Extended Calibration (2026-02-21)

- **Credit cap fix** — `shared/skills/ds-review-framework/SKILL.md` Section 2b
  - Reduced per-dimension credit cap from +25 to +15
  - Root cause: R3 score inflation (17-30 points above targets) from uncapped credit accumulation
  - R4 results: Vanguard 72→57, Meta 63→60, Rossmann 86→63 (all within or ±2 of targets)
  - Secondary fix (MAJOR deduction increases) not needed — primary fix sufficient
- **3 search-domain test fixtures added** — `dev/test-fixtures/real/`
  - `airbnb-search-interleaving.md` — Airbnb interleaving experiments
  - `atlassian-rovo-search-relevance.md` — Atlassian Rovo multi-layer ranking
  - `eppo-search-ranking-experiments.md` — Eppo search ranking experimentation guide

#### Full `--domain search-ranking` Calibration (2026-02-21)

- **10-run calibration matrix** completed across 4 phases
  - Phase 1: 3 search fixtures scored 60-95 (domain adds genuine value)
  - Phase 2: 3 non-search fixtures scored 64-83 (domain correctly finds 0 issues, ~10pt inflation from weighting)
  - Phase 3: 3 consistency runs scored 93-95 (2-point spread, pass criteria ±10)
  - Phase 4: All 4 criteria passed → **SHIP AS-IS**
- **Flat parallel dispatch validated** — 9 agents dispatched simultaneously, all returned successfully
- **Key finding:** Communication dimension has highest variance (5pt across identical runs vs 2-3pt for analysis/domain)
- Session log: `dev/sessions/2026-02-21-r4-domain-calibration-full.md`

**Goal:** Add a 3rd review dimension (Domain Knowledge) to the DS Review agent. Standalone Domain Knowledge Skill (Layer 1) that any agent can consume, plus a thin Domain Expert Reviewer subagent (Layer 2) and lead agent integration (Layer 3).

#### Layer 2 Implementation (2026-02-21) — PR #4

- **New subagent** — `agents/ds-review/domain-expert-reviewer.md` (144 lines)
  - 3 lenses: Technique Appropriateness, Benchmark & External Validity, Domain Pitfall Awareness
  - Authority-aware scoring: `[authority: authoritative]` → full deductions, `[authority: advisory]` → capped at ADVISORY (-2)
  - Web search verification with 3-5 search budget and hallucination guard
  - 13 rules, output format matches existing subagents + Authority field
- **SKILL.md expanded** — `shared/skills/ds-review-framework/SKILL.md`
  - ADVISORY severity level (4th tier: capped at -2, never triggers floor rules)
  - Domain Knowledge deduction table: 25 issue types across 3 lenses (7+9+9)
  - Domain Knowledge credit table: 11 strength types (+36 possible, capped at +25)
  - Floor rules 5-6: ADVISORY exclusion + cross-dimension equality
  - 7 domain routing rows + cross-dimension dedup rules in Section 5
  - All 8 PSE (Principal Search Engineer) findings incorporated
- **Lead agent updated** — `agents/ds-review/ds-review-lead.md`
  - Step 6.5: Domain digest loading with staleness checks (<14d/14-30d/>30d/missing)
  - Step 7: Conditional 3rd subagent dispatch with domain context brief
  - Step 8: 3-subagent failure handling with fallback weights
  - Step 9: Two-stage cross-dimension dedup + 50/25/25 scoring formula
  - Step 10: 11-row dashboard, Domain Knowledge section, ADVISORY emoji (📋)
- **Analysis reviewer guardrail** — `agents/ds-review/analysis-reviewer.md` Rule 10
  - Defers domain-specific findings to domain-expert-reviewer when `--domain` active
  - Benchmark routing clarification per PSE review
- **Command file updated** — `.claude/commands/ds-review.md`
  - New flags: `--domain d1,d2,...`, `--reference path`, `--refresh-domain domain`
  - 3-dimension review (50/25/25) with `--domain`; backward-compatible 2-dimension (50/50) without

#### Layer 1 Implementation (2026-02-21)

- **Research doc** — `docs/research/domain-knowledge-references.md` with 55 sources across 4 batches
  - Batch 1: Search Ranking (metrics, LTR, position bias, click models) — 15 sources
  - Batch 2: Query Understanding (intent, spell correction, rewriting) — 14 sources
  - Batch 3: Cross-Domain + Industry Case Studies — 14 sources
  - Batch 4: Emerging Paradigms (AI Search, Agentic Search, Generative Retrieval) — 12 sources (added per product owner request)
- **domain-index.yaml** — `shared/skills/search-domain-knowledge/config/domain-index.yaml` (14 curated sources, 3 domains)
- **SKILL.md contract** — `shared/skills/search-domain-knowledge/SKILL.md` (6 sections: digest format, consumption, staleness, refresh, scoring, precedence)
- **3 digest files:**
  - `search-ranking.md` — 5,076 words, 14 cited sources + 6 [DEMO] synthetic workstream entries
  - `query-understanding.md` — 3,956 words, 15 cited sources + 5 [DEMO] synthetic workstream entries
  - `search-cross-domain.md` — 1,094 words, 5 cited sources (foundational only, no workstream in cross-domain for MVP)
- **Public data proxy approach:** All sources are public (papers, engineering blogs, conference proceedings). Synthetic [DEMO] entries demonstrate how internal team decisions would be documented.

#### Design Artifacts Created

**v3 Design Spec** — `docs/plans/domain-knowledge/design-v3.md`
- 914 lines, 21 design decisions finalized
- 3-layer architecture: Domain Knowledge Skill → Domain Expert Reviewer → Lead Integration
- 3 review lenses: Terminology Accuracy, Methodological Alignment, Domain-Specific Standards
- Weighted scoring: 50/25/25 (Analysis / Communication / Domain)
- ADVISORY severity level for recent workstream learnings (-2 deduction cap)
- Two-tier digest system: foundational (monthly) + workstream (weekly)
- Two-stage deduplication: heuristic + LLM fallback
- Versioned digests with rollback support

**MVP Design Doc** — `docs/plans/domain-knowledge/mvp-design.md`
- PM-led design review resolving 5 implementation challenges (A1-A5)
- A1: Reframed API as file contract + refresh workflow (no callable code)
- A2: Audience-tagged sections (`all`, `ds`, `eng`) + token budget increased 5K → 8K
- A3: Manual-only refresh for v0.5 (no auto-discovery, no cron)
- A4: Dropped team roster (LLM content scoring sufficient for v0.5)
- A5: Cross-domain gets additive 1,500-token budget (not shared with domain budgets)

**Layer 1 Implementation Plan** — `dev/internal/2026-02-16-domain-knowledge-layer1-implementation-plan.md`
- 5 tasks, all file creation (markdown + YAML, no scripts)
- Files: domain-index.yaml, SKILL.md contract, 3 digest files (ranking, QU, cross-domain)
- Includes full file contents, validation steps, and commit strategy
- Scope: Layer 1 only. Layer 2 (reviewer) and Layer 3 (integration) deferred

#### Design Sessions (Chronological)

| Date | Session | Key Output |
|---|---|---|
| 2026-02-15 | Domain knowledge brainstorm | Initial concept exploration |
| 2026-02-15 | Domain knowledge design | v3 spec (21 decisions, 8 gaps resolved) |
| 2026-02-16 | MVP design review | 5 challenges resolved (A1-A5) |
| 2026-02-16 | Implementation planning | Layer 1 plan (5 tasks, ready to execute) |

#### Architecture Summary

```
Layer 1 — Domain Knowledge Skill (standalone, reusable)
├── shared/skills/search-domain-knowledge/config/domain-index.yaml — Curated source index
├── shared/skills/search-domain-knowledge/SKILL.md                 — Format contract + consumption guide
└── shared/skills/search-domain-knowledge/digests/                 — Pre-built digest files
    ├── search-ranking.md               — Ranking/relevance domain knowledge
    ├── query-understanding.md          — QU pipeline evaluation standards
    └── search-cross-domain.md          — Cross-cutting search evaluation

Layer 2 — Domain Expert Reviewer (PR #4)
├── agents/ds-review/domain-expert-reviewer.md — 3 lenses, authority-aware scoring
├── shared/skills/ds-review-framework/SKILL.md — ADVISORY severity, domain deduction/credit tables
├── agents/ds-review/ds-review-lead.md         — Step 6.5, 3-way dispatch, 50/25/25 scoring
├── agents/ds-review/analysis-reviewer.md      — Rule 10: domain-aware guardrail
└── .claude/commands/ds-review.md              — --domain, --reference, --refresh-domain
```

#### PR #4 Merged & R4 Calibration (2026-02-21)

- **PR #4 merged to main** — 7 commits, fast-forward merge, pushed to remote
- **Backward compatibility confirmed** — Vanguard without `--domain`: 57/100 (no domain content leaked)
- **Search-domain test fixture** — `dev/test-fixtures/synthetic/09-search-ranking-domain-issues.md` (5 planted issues)
- **R4 domain calibration results:**
  - 5/5 planted issues detected at exact severity/deduction values
  - Cross-dimension dedup: 3 analysis findings correctly suppressed for domain versions
  - Diminishing returns: domain raw 103 → effective 71.5 (31% compression)
  - Final: 55/100 (Analysis 63, Communication 64, Domain 30) — Major Rework
  - Floor rules: 5 CRITICALs correctly triggered 2+ CRITICAL cap
  - Authority-aware scoring: all findings correctly tagged authoritative
  - Domain reviewer added genuine value over 2-dimension review

#### What's Next

- v0.5 is feature-complete and calibrated. Ready for production use.
- P1 output restructure (compressed lens detail, effort-based grouping)
- SQL Review Agent planning (Q2 2026)
- Monitor calibration watch items during real usage

---

## [1.1.0] — 2026-02-16

### Multi-Agent Platform Migration

**Status:** Complete. Repository reorganized as multi-agent platform.

#### Repository Rebrand
- **Repository name:** `DS-Analysis-Review-Agent` → `ds-productivity-agents`
- **Project scope:** Single agent → Multi-agent platform
- **Rationale:** Building 3 peer-level agents (DS review, SQL review, Search metric analysis) that share domain knowledge infrastructure

#### File Reorganization
- **Created `shared/skills/`** — Reusable infrastructure layer
  - Moved `plugin/skills/ds-review-framework/` → `shared/skills/ds-review-framework/`
- **Created `agents/`** — Agent implementations layer
  - Moved `plugin/agents/*.md` → `agents/ds-review/*.md` (3 agent files)
  - Created `agents/sql-review/` placeholder (Q2 2026)
  - Created `agents/search-metric-analysis/` placeholder (Q2 2026)
- **Updated all path references** across 6 files:
  - `.claude/commands/ds-review.md`
  - `agents/ds-review/ds-review-lead.md`
  - `.claude/rules/plugin-conventions.md`
  - Documentation files (CLAUDE.md, README.md, MEMORY.md)

#### Documentation
- **README.md** — Complete rewrite (172 lines)
  - Multi-agent platform overview
  - All 3 agents documented (DS review shipped, SQL review + metric analysis planned)
  - Architecture diagram showing shared infrastructure pattern
  - Professional GitHub presentation
- **CLAUDE.md** — Updated for multi-agent scope
  - Platform description with all 3 agents
  - Updated agent architecture section
  - All file paths updated to new structure
- **MEMORY.md** — Updated for future sessions
  - New project structure documented
  - Key files paths updated
  - Added migration-plan.md reference

#### Migration Artifacts
- `dev/migration-plan.md` (500 lines) — Comprehensive reorganization guide
- `dev/RENAME-STEPS.md` — GitHub rename instructions
- `dev/sessions/2026-02-16-multi-agent-platform-migration.md` — Full session log
- `dev/sessions/2026-02-16-repository-architecture-discussion.md` — Design discussion log
- `docs/plans/domain-knowledge/design-v3.md` — v0.5 design spec

#### Architecture

**Three-Agent Platform:**
```
Shared Skills Layer:
├── ds-review-framework (current)
└── search-domain-knowledge (v0.5)

Agent Layer:
├── DS Review (v1.0) - domain-agnostic analysis reviewer
├── SQL Review (Q2 2026) - domain-agnostic SQL checker with pluggable domain guidance
└── Search Metric Analysis (Q2 2026) - metric analysis + calls DS review for quality gate
```

**Key relationships:**
- All agents share `search-domain-knowledge` skill for consistent domain expertise
- Metric Analysis agent calls DS Review agent as quality gate
- DS Review and SQL Review are domain-agnostic with pluggable domain knowledge skills

#### Git History
- All file moves executed via `git mv` (history preserved)
- 3 commits: file reorganization, documentation updates, session logs
- Final commit: `45e0172`

#### Breaking Changes
- **File paths:** All `plugin/agents/` → `agents/ds-review/`, all `plugin/skills/` → `shared/skills/`
- **Repository URL:** `github.com/surahli123/ds-productivity-agents` (GitHub redirects old URLs)

#### Non-Breaking
- `/ds-review` command still works (paths updated internally)
- All skills load correctly
- No functionality changes (pure reorganization)

---

## [1.0.0] — 2026-02-15

### v1.0.0 — First Public Distribution

**Status:** Shipped to GitHub. Installable via `claude plugins install surahli123/ds-analysis-review`.

**Plugin Validation (2026-02-16):** Project-level command `/ds-review` validated post-restart. 7/7 registration checks passed. File-reference approach functioning (single source of truth). Test log: `dev/test-results/2026-02-16-plugin-registration-test.md`.

#### Added
- **Distribution package** — `dist/ds-analysis-review/` with standalone plugin structure
  - `.claude-plugin/plugin.json` (v1.0.0, auto-discovery, MIT license)
  - `commands/review.md` — plugin command entry point
  - `agents/ds-review-lead.md`, `analysis-reviewer.md`, `communication-reviewer.md`
  - `skills/ds-review-framework/SKILL.md` — shared rubrics
  - `README.md` — install, usage, architecture, scoring docs (150 lines)
- **GitHub repo** — `surahli123/ds-analysis-review` (public)
- **Vibe coding journey doc** — `docs/vibe-coding-journey.md` (~1,566 words)
  - Storytelling format: Day 1 (PM decisions + rubric design), Day 2 (scoring crisis + calibration)
  - Honest about limitations (6 blog posts, ±10 variability, not peer-review ready)
  - 3 communication-reviewer rounds used during drafting (R1: 100, R2: 89, R3: 100)

#### Changed
- All `plugin/` paths → `${CLAUDE_PLUGIN_ROOT}/` in distribution files
- All `/ds-review:review` → `/review` in distribution files
- Plugin name simplified from `ds-review:review` to `review` for installed plugin context

---

## [0.4.1] — 2026-02-15

### Credit Redesign + R3 Calibration + Emoji Dashboard

**Status:** Merged to main via PR #1. R4 calibration pending.

**Problem:** R2 rank order wrong — Rossmann 71, Vanguard 69, Meta 54. Correct order: Rossmann > Meta > Vanguard. Root cause: analysis credit table was experiment-biased, awarding Vanguard +22 for unvalidated experimental scaffolding while Meta's deployed system earned +0.

**Design principle:** "False confidence from unvalidated experiments is more dangerous than vague attribution from deployed systems."

#### Changed

- **New CRITICAL deduction: Unvalidated experimental claims (-15)** — Fires when A/B test reports lift or uses "significant" without p-value, CI, or named statistical test. Added to SKILL.md Section 2 Analysis Dimension table.
- **Replaced analysis credit table (Section 2b)** — 9 methodology-agnostic credits replacing 8 experiment-biased ones. Key changes:
  - Removed: "Real experimental design" (+8), "Pre-specified hypotheses" (+5), "Pre-specified success threshold" (+3), "Covariate or balance check" (+3), "Sensitivity or robustness check" (+3)
  - Added: "Appropriate methodology for the question" (+5), "Systematic model or method comparison" (+5), "Validation methodology present" (+5), "Demonstrated real-world impact" (+8)
  - Renamed/refined: "Pre-specified goals or hypotheses" (+3), "Reports specific quantitative results with context" (+3)
  - Kept: "External validation or benchmarking" (+3), "Honest negative or null result reported" (+3), "Reproducibility detail provided" (+2)
- **Conditional halving rule (Credit Rule 6)** — When experimental structure is present but unvalidated: methodology credit halved, hypotheses credit halved, validation credit zeroed, quantitative results credit halved. Does NOT apply to non-experimental analyses.
- **Tightened duplicate suppression (lead Step 9, item 3)** — Explicit same-root-cause AND same-observable-problem test. Cross-dimension findings with different harms both stand.
- **Finding volume cap (lead Step 9, item 8)** — Max 10 findings displayed, ranked by severity. Scoring uses all findings.
- **Self-deliberation fix (communication-reviewer Rule 12)** — Single-pass evaluation: commit to each decision on first assessment, no visible deliberation.
- **Step 10 output format** — Updated Analysis/Communication dimension sections to reference volume cap.
- **Severity Escalation Guard wording** — Updated to reflect variable MINOR deduction values (-2 to -5).

#### Projected Scores (pending validation)

| Fixture | R2 | v0.4.1 Projected | Target Range |
|---|---|---|---|
| Rossmann | 71 | ~75 | 72-80 |
| Meta | 54 | ~61 | 58-65 |
| Vanguard | 69 | ~59 | 55-62 |

#### R3 Calibration Results (2026-02-15)

**All 6 fixtures tested (3 core + 3 extended blog posts):**

| Fixture | R2 | R3 | Delta | Revised Target | Status |
|---|---|---|---|---|---|
| Vanguard | 69 | 72 | +3 | 55-65 | +7 to +17 OVER ⚠️ |
| Meta | 54 | 63 | +9 | 60-70 | CLOSE ✅ |
| Rossmann | 71 | 86 | +15 | 65-75 | +11 to +21 OVER ⚠️ |
| Airbnb Message Intent | N/A | 85 | N/A | Analysis 70-80 | +5 to +15 OVER ⚠️ |
| Airbnb FIV | N/A | 90 | N/A | Analysis 80-90 | +0 to +10 OVER ⚠️ |
| Netflix Proxy Metrics | N/A | 100 | N/A | Analysis 80-90 | +10 to +20 OVER ⚠️ |

**Key findings:**
- ✅ All P0/P1 fixes worked correctly (no bugs, no rollbacks)
- ✅ Finding quality excellent (DS Lead audit: 8/8 Vanguard findings legitimate)
- ✅ Differentiation strong (37-point gap: Netflix 100 vs Meta 63)
- ⚠️ Score inflation: All tests 17-30 points above targets
- ✅ Meta CRITICAL count reduced from 3 → 2 (immediate fix applied)

**Root cause:** Credit additions (+6) without offsetting deductions created +10-12 point inflation per test.

**System health:** Architecturally sound. Tuning problem, not redesign needed.

#### R3 Artifacts Created

- 6 review outputs: `dev/test-results/2026-02-15-r3-*-review.md`
- Calibration notes: `dev/test-results/2026-02-15-r3-calibration-notes.md`
- R3 vs R2 comparison: `dev/test-results/2026-02-15-r3-vs-r2-comparison.md`
- 3 role reviews (parallel):
  - Principal AI Engineer: `dev/test-results/2026-02-15-r3-principal-ai-engineer-assessment.md`
  - PM Lead: `dev/reviews/2026-02-15-r3-pm-lead-calibration-review.md`
  - DS Lead: `dev/test-results/2026-02-15-r3-ds-lead-assessment.md`
- Fix plan: `dev/test-results/2026-02-15-r3-calibration-fix-plan.md`
- Session log: `dev/sessions/2026-02-15-r3-calibration-execution.md`

#### Immediate Fix Applied (2026-02-15)

- **Severity downgrade:** "Conclusion doesn't trace to evidence" from CRITICAL (-15) to MAJOR (-10)
- **Impact:** Meta now has 2 CRITICALs (was 3), meeting ≤2 acceptance criteria
- **Commit:** `7649c41 fix(skill): downgrade 'Conclusion doesn't trace' from CRITICAL to MAJOR`

#### R4 Fix Plan (Deferred to After Plugin Registration)

**Primary fix:** Reduce credit cap from +25 → +15 per dimension
- Expected impact: -10 points per test
- Estimated rounds to acceptance: 1-2
- No architecture changes needed

**Secondary fix (if R4 still high):** Increase 2-3 MAJOR deductions by +2 each

**Recommendation:** System is production-ready for plugin registration. Score recalibration can wait until R4.

#### Emoji Dashboard (2026-02-15)

- **4-tier emoji severity indicators** — Added to lens dashboard, finding headers, top 3 fixes, and verdict line
  - ✅ SOUND, ⚠️ MINOR, 🔴 MAJOR, ❌ CRITICAL
- **Explicit Unicode lookup table** in lead agent Step 10 — prevents LLM from substituting markdown shortcodes (`:x:`, `:warning:`)
- **Verdict line emoji** — `✅ Good to Go | ⚠️ Minor Fix | ❌ Major Rework`
- **Quick mode status table** — `✅ Pass / ⚠️ Issues Found / ❌ Critical Issues`
- **Design doc:** `dev/internal/2026-02-15-emoji-dashboard-design.md`
- **3 UX reviews:** Principal AI Engineer, PM Lead, DS Lead — all approved with concerns, 3 quick fixes applied
- **Verified** in both full and quick mode — 100% Unicode emoji rendering

#### Earlier Commits

1. `fix(comm-reviewer): add single-pass commit rule to suppress self-deliberation`
2. `fix(lead): add tightened duplicate suppression and finding volume cap to Step 9`
3. `feat(skill): add CRITICAL deduction for unvalidated experimental claims`
4. `feat(skill): replace analysis credits with methodology-agnostic table and conditional halving rule`
5. `fix(skill): reduce 3 MINOR comm deductions, add worked example credit`
6. `feat(skill): implement P1 calibration fixes from web session review` (P1 fixes)
7. `fix(skill): downgrade 'Conclusion doesn't trace' from CRITICAL to MAJOR` (R3 immediate fix)

### v0.4.0 — Calibration Sprint (2026-02-15)

**Status:** Calibration complete. Scoring system validated through 2 rounds. Extended validation pending.

#### Implemented (Phase 1 — P0 Fixes)

- **Strength Credit System (Section 2b):** Added to SKILL.md. 8 analysis credits + 8 communication credits, capped at +25/dimension. Both subagent output formats updated with STRENGTH LOG section.
- **CRITICAL Reclassification:** 3 communication CRITICALs demoted to MAJOR: missing TL;DR (-15→-10), no story arc (-12→-8), limitations absent (-12→-10). Eliminates false floor rule triggers.
- **Diminishing Returns Curve:** Lead agent Step 9 rewritten. Formula: 100% up to 30 pts, 75% for 31-50, 50% for 51+. Prevents score cratering from deduction stacking.
- **Severity Escalation Guard:** Added to SKILL.md Section 2 footer. Subagents cannot escalate beyond table-defined severity/deduction values.
- **Score Breakdown:** Lead agent Step 10 output now shows `Raw deductions → Effective (DR) | Credits: +Z | Score: W` per dimension.
- **Dispatch Payload Updated:** Lead agent Step 7 now instructs subagents to produce STRENGTH LOG and reference Section 2b.

#### Calibrated (R2 Tuning)

- **Tightened DR Curve:** From 100/50/25 (R1) to 100/75/50 (R2) at 30/50 thresholds. R1 over-corrected; R2 brings scores into target range.
- **Added "TL;DR completely absent" CRITICAL (-12):** Reinstated as the only communication CRITICAL. Distinct from "ineffective TL;DR" (MAJOR -10). Fires only when no summary exists anywhere in the document.

#### Calibration Results

| Fixture | R0 | R1 | R2 (Final) | Updated Target |
|---|---|---|---|---|
| Vanguard A/B Test | 16 | 73 | **69** | 60-75 |
| Meta LLM Bug Reports | 18 | 59 | **54** | 45-58 |
| Rossmann Sales | 29 | 71 | **71** | 60-75 |
| Differentiation gap | 2 pts | 14 pts | **15 pts** | 15+ |
| CRITICALs per test | 2-5 | 0-1 | **1** | ≤2 |

Key outcome: System now differentiates correctly (15-point gap between best and worst analysis), assigns appropriate verdicts, and credits good analytical work.

#### Final Scoring Parameters

| Parameter | Value |
|---|---|
| Diminishing returns curve | 100/75/50 at 30/50 thresholds |
| Strength credit cap | +25 per dimension |
| Communication CRITICALs | 1 entry: "TL;DR completely absent" (-12) |
| Analysis CRITICALs | 3 entries: unstated assumption (-20), flawed methodology (-20), conclusion doesn't trace (-15) |
| Severity escalation guard | Active |

#### Testing & Diagnosis Artifacts
- `dev/test-results/2026-02-15-r1-calibration-notes.md` — R1 diagnosis (over-correction, DR too aggressive)
- `dev/test-results/2026-02-15-r1-vs-r0-comparison.md` — R0→R1 score trajectory and fix impact
- `dev/test-results/2026-02-15-r2-calibration-notes.md` — R2 final calibration notes (ACCEPTED)
- `dev/test-results/2026-02-15-r1-*.md` and `r2-*.md` — Per-fixture review outputs from both rounds
- `dev/decisions/ADR-003-calibration-approach.md` — Calibration architecture decision record

#### Earlier in v0.4 (Discovery Phase)
- 12 real-world fixtures collected in `dev/test-fixtures/real/`
- 3 independent calibration assessments (Engineer, PM, DS Lead)
- A3 fix plan synthesized: `dev/test-results/2026-02-15-calibration-fix-plan.md`
- Calibration loop workflow: `dev/internal/2026-02-15-calibration-loop-workflow.md`
- 5 owner decisions resolved (strength cap +25, Meta target 42-50, finding cap deferred, fix escalation bug, include DR)
- UX decisions approved (emoji dashboard, compressed lens detail, blockquote rewrites) — deferred to P1

#### Remaining
- Extended validation: untested fixtures, cross-run consistency, synthetic fixture rerun
- P1: Output restructure (emoji dashboard, compressed lens detail, blockquote rewrites)
- P1: Finding volume cap (10 max) — deferred to Phase 2
- Web session feedback integration

### v0.3.0 — Implementation Complete (2026-02-15)

**Status:** Complete. All agents, rubrics, command, and test fixtures implemented. Smoke tests pass 59/59.

#### Added
- `plugin/skills/ds-review-framework/SKILL.md` (209 lines, 8 sections)
  - Severity definitions (CRITICAL/MAJOR/MINOR)
  - Deduction table (8 analysis rows + 18 communication rows)
  - Floor rules with verdict bands
  - Audience persona definitions (exec/tech/DS/mixed)
  - Dimension boundary routing table (10 gray-zone scenarios)
  - Workflow context calibration (proactive/reactive/general)
  - Common anti-patterns (10 entries)
  - Confluence structure guide
- `plugin/commands/review.md` — full command definition with `--mode`, `--audience`, `--workflow` flags
- `dev/test-fixtures/synthetic/` — 8 synthetic test fixtures:
  - 01-no-tldr.md, 02-causal-without-method.md, 03-good-analysis-bad-comms.md,
    04-contradicts-data.md, 05-data-dump.md, 06-wrong-audience.md,
    07-partial-input-bullets.md, 08-unstructured-text.md
- `dev/test-results/2026-02-14-smoke-test.md` — full smoke test results (59/59 pass)
- `dev/decisions/ADR-002-auto-activate-in-subagents.md` — auto_activate not visible in subagent contexts
- `.gitignore` — excludes real test fixtures with sensitive data

#### Changed
- `plugin/agents/ds-review-lead.md` — Step 7 dispatch payload updated to instruct subagents to read SKILL.md from disk (auto_activate fallback)
- `plugin/.claude-plugin/plugin.json` — version bumped from 0.1.0 to 0.3.0

#### Validated
- Agent prompt instruction counts: analysis ~47, communication ~52, lead ~105 (all under 120 red flag)
- All cross-references between agents and SKILL.md verified
- Dimension separation confirmed (fixture 03: analysis 100, communication 37, no cross-contamination)
- Floor rules fire correctly (1 CRITICAL → Minor Fix, 2+ CRITICAL → Major Rework)
- All output formats verified (Full, Quick, Draft Feedback)
- Special paths work (partial input detection, unstructured document handling)

### v0.2.2 — Doc Consistency Review (2026-02-14)

**Status:** Complete. All active docs aligned with architecture.

#### Fixed
- Architecture design doc: 5 edits — tier thresholds (Section 2.1 matched to 3.2.4), Quick mode dashboard labels (3-level), lens rating shorthand (4-level), degradation level reference (Level 1-2), section cross-reference (15.3)
- PRD: 4 edits — narrowed v1 input formats to Confluence + markdown only, Quick mode latency (3 min), scoring description (equal-weight average), In Scope list alignment
- CLAUDE.md: removed auto-detection reference (explicit invocation only)
- Repo structure doc: 5 edits — removed auto-detection (2 locations), updated lens names (structure & TL;DR, conciseness & prioritization), updated input format in diagram, updated orchestrator description
- Plugin README: 4 edits — updated lens names, input formats, removed auto-detection section, updated orchestrator description
- review.md command: 2 edits — updated input format references, updated description frontmatter
- communication-reviewer.md: 1 edit — updated frontmatter description to current lens names
- v1-review-plugin spec: 3 edits — removed auto-detection, updated lens names, updated testing plan

#### Changed
- Implementation plan updated to Rev 3:
  - Added skill-creator hybrid approach guidance to Task 1 (single file, optimized frontmatter, token-efficient format, cross-reference stability)
  - Enhanced SKILL.md frontmatter description for better triggering
  - Added .gitignore step for `dev/test-fixtures/real/`
  - Added revision history entry

#### Process
- Parallel code review of architecture design + implementation plan (2 Opus subagents)
  - Architecture review: 1 CRITICAL, 6 MAJOR, 4 MINOR issues found
  - Implementation plan review: 1 CRITICAL, 3 MAJOR, 4 MINOR issues found
- All issues resolved across 9 files, 28 total edits
- Verification grep checks: all stale references cleared from active docs

### v0.2.1 — Implementation Planning (2026-02-14)

**Status:** Complete. Implementation plan Rev 3 ready. Agent prompts written. Execution pending in fresh session.

#### Added
- Implementation plan (`dev/internal/2026-02-14-implementation-plan.md`, Rev 1→3)
  - 8 tasks: auto_activate validation, SKILL.md, prompt validation, command, plugin.json, 8 fixtures, smoke test, wrap-up
  - Self-contained plan with full SKILL.md content embedded
  - IC8 Engineering Lead review conducted — 3 Critical + 5 Major issues identified and fixed
- Agent prompts written (complete production prose):
  - `plugin/agents/analysis-reviewer.md` (146 lines, 4 lenses, 17 checklist items, 8 rules)
  - `plugin/agents/communication-reviewer.md` (107 lines, 4 lenses, 18 checklist items, 10 rules)
  - `plugin/agents/ds-review-lead.md` (178 lines, 10-step pipeline, 4 output templates, 9 rules)

### v0.2 — Architecture Design (2026-02-14)

**Status:** Complete. Architecture approved.

#### Added
- Architecture design document (`docs/plans/ds-analysis-review/architecture-design.md`, Rev 4)
  - 13 consolidated architecture decisions
  - System data flow with 3-agent parallel dispatch
  - Token budget model calibrated to 200K context window
  - 3-level graceful degradation (Normal → Quick downgrade → Defer)
  - Tiered pre-processing for long documents (Tier 1/2/3)
  - Confluence integration via Atlassian MCP
  - Unstructured document handling with keyword/positional heuristics
  - Quick mode vs Full mode comparison
  - Agent prompt design (Pedro Sant'Anna's pattern)
  - Deduction-based scoring with floor rules
  - Output format templates (Full, Quick, Degraded, Draft)
  - Partial input handling with qualitative draft feedback
  - SKILL.md structure outline (8 sections)
  - Cost estimation per review
  - Testing & evaluation strategy (manual eval + auto-eval pipeline design)

- PRD and reference docs moved to `dev/specs/`
  - `PRD-DS-Analysis-Review-Agent.md`
  - `architecture-session-handoff.md`
  - `full-prd-session-record.md`

- Plugin conventions rule (`.claude/rules/plugin-conventions.md`)

#### Key Architecture Decisions (Rev 4)
1. Hybrid skill file approach (core in prompts, detail in SKILL.md)
2. Tiered pre-processing (< 2K pass-through, 2-5K section map, 5K+ extraction)
3. Quick mode: skip plan-first, default mixed audience, < 3 min target
4. Draft feedback: qualitative only, no numeric score
5. Equal weight scoring (50/50 analysis/communication)
6. Workflow context: default "general", flag-based (no inference)
7. Session handling: reactive failure handling, no predictive detection
8. Graceful degradation: 3 levels (cut from 5)
9. Confluence + local markdown only for v1

#### Decisions Made
- ADR 001: Two-dimension split (`dev/decisions/001-two-dimension-split.md`)

---

## [0.1.0] — 2026-02-14

### Added
- Initial repository structure and scaffolding
- Placeholder files for all agents, commands, and skills
- CLAUDE.md with project context and pickup instructions
- Dev tracking setup (backlog, sessions, decisions)
- Repository structure spec (`ds-analysis-review-agent-structure.md`)
