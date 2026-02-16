# Changelog

All notable changes to the DS Analysis Review Agent.

## [1.0.0] — 2026-02-15

### v1.0.0 — First Public Distribution

**Status:** Shipped to GitHub. Installable via `claude plugins install surahli123/ds-analysis-review`.

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

## [Unreleased]

### v0.4.1 — Credit Redesign + R3 Calibration (2026-02-15)

**Status:** R3 calibration complete. R4 fixes identified. Ready for plugin registration.

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
- Calibration loop workflow: `docs/plans/2026-02-15-calibration-loop-workflow.md`
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
- Implementation plan (`docs/plans/2026-02-14-implementation-plan.md`, Rev 1→3)
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
- Architecture design document (`docs/plans/2026-02-14-architecture-design.md`, Rev 4)
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
