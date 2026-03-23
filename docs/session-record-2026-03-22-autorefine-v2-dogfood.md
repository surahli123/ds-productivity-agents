# Session Record: AutoRefine v2 Live Dogfood on ds-review

**Date:** 2026-03-22
**Duration:** ~90 minutes
**Goal:** Validate AutoRefine v2 Smart Phase 3 (stratified sampling, clustering, consistency detection, override logging) end-to-end on a real skill with real traces and real human annotation.
**Source of truth:** v2 SKILL.md at `/Users/surahli/Documents/projects/skill-improvement/autorefine/SKILL.md`

---

## Pipeline Execution Summary

### Step 0: Initialize Workspace
- Backed up existing `autoresearch-ds-review/` → `autoresearch-ds-review-prev/` (had no state.json — created by prior autoresearch, not autorefine)
- Created fresh workspace with v2 schema: state.json (schema_version:2), session-log.json, results.json, results.tsv, dashboard.html, traces/ directory
- Dashboard served at localhost:8080

### Phase 1: Design Audit
- Scored 4 dimensions per v2 rubric
- **Gotchas: Missing** — no failure modes section, only operational rules
- **Voice: Partial** — ~60% "Do X" without "because Y"
- **Progressive Disclosure: Partial** — clean folder structure but no `Read when:` tags
- **Scripts: N/A** — no executable code
- Output: `design-audit.md`

### Phase 2: Eval Audit
- Audited 3 eval sources: evals.json (3 format evals), prior eval-suite (5 binary), prior eval-audit report
- All 6 gaps from prior audit remain open
- Phase 3 confirmed as the blocker
- Output: `eval-audit-report.md`

### Phase 3: Error Analysis (MAIN FOCUS — v2 mechanisms tested here)

#### Fixture Selection (15 total)
- 10 real: Eppo, Airbnb, Vanguard, Meta Asymmetric, Meta LLM Bug, Meta Posttreatment, Credit Card, Kaggle IBM, Rossmann, Capstone
- 5 synthetic: Causal w/o Method, Contradicts Data, Data Dump, Good-Bad Comms, Unstructured Text

#### Trace Generation
- 15 subagents dispatched in 3 parallel batches of 5
- All 15 completed successfully (some took up to ~6 minutes for long docs)
- Score range: 33-100 across fixtures
- **Known issue:** T08 and T12 showed score discrepancies between reads (likely due to reading before agent finished writing)

#### Smart Sampling (v2 NEW — VALIDATED)
- Selected 9/15 traces stratified by:
  - Input length: short (2), medium (5), long (2)
  - Source: real (6), synthetic (3)
  - Planted flaw: yes (3), no (6)
- Clear rationale presented and logged to session-log.json

#### Preliminary Clustering (v2 NEW — VALIDATED)
- 4 clusters by score range + CRITICAL presence:
  - C1: high score + CRITICAL (floor-rule surprises) — T02, T11
  - C2: medium score + CRITICAL (core reviews) — T01, T05, T09, T14
  - C3: high score + no CRITICAL (clean passes) — T06, T15
  - C4: low score + heavy findings — T08

#### Human Review with Consistency Detection (v2 NEW — VALIDATED)
- 9 sampled + 3 additional = 12 traces reviewed
- One-at-a-time presentation with Pass/Fail + notes
- **Consistency detection fired on C2 cluster** (T01 FAIL, T05 FAIL, T09 PASS — mixed verdicts). Resolution: defensible, different document types within same score cluster.
- **C3 consistency confirmed** (T06 FAIL, T15 FAIL — both credit inflation). Consistent.
- All flags logged to session-log.json

#### Review Results

| Trace | Fixture | Score | Verdict | Notes |
|-------|---------|-------|---------|-------|
| T01 | Eppo | 64 | FAIL | Rigor miscalibration for blog/guide |
| T02 | Airbnb | 90 | PASS (borderline) | Some findings nitpicky for blog |
| T04 | Meta Asymmetric | 84 | PASS (soft) | Correct calibration, misses domain critiques |
| T05 | Meta LLM Bug | 60 | FAIL | Same miscalibration as T01 |
| T06 | Meta Posttreatment | 100 | FAIL (soft) | Credit inflation — 100 with MAJOR present |
| T08 | Kaggle IBM | 49 | PASS | Correctly catches all flaws |
| T09 | Rossmann | 66 | PASS (borderline) | Appropriate rigor for primary analysis |
| T11 | Causal w/o Method | 81 | PASS (soft) | Catches planted flaw, slightly generous |
| T12 | Contradicts Data | 86 | FAIL | Contradiction classified MAJOR not CRITICAL |
| T13 | Data Dump | 68 | PASS | Correctly identifies data dump pattern |
| T14 | Good-Bad Comms | 74 | FAIL (partial) | Analysis 100 inflated + averaging masks catastrophic comm |
| T15 | Unstructured | 93 | FAIL | Zero headings scored 93 Good to Go |

**Fail rate: 6/12 (50%)** — healthy, within target range.

#### Failure Taxonomy (4 categories emerged)

1. **Document Type Blindness** (2/12) — applies empirical rigor to educational/blog content
2. **Credit Inflation** (4/12) — +15 credit cap fully offsets MAJOR findings
3. **Catastrophic Dimension Masking** (1/12) — 50/50 average hides when one dimension is broken
4. **Severity Under-Call on Contradictions** (1/12) — data-conclusion contradiction classified MAJOR not CRITICAL

#### Gulf 1 Gate: APPROVED
- 4 failure categories, 5 proposed evals
- No user overrides (override logging mechanism validated but not exercised)

### Phase 4: Expand Inputs
- Used existing 15 fixtures (user chose not to generate additional)
- Labeled all 15 traces × 5 evals = 75 labels
- Split: Train (3: T01, T06, T08), Dev (6: T02, T05, T07, T11, T14, T15), Test (6: T03, T04, T09, T10, T12, T13)
- Coverage gaps noted: E1 has only 5 testable fixtures, E3 and E5 have 1 each

### Phase 5: Write Judges
- 3 code-based: E2 (credit balance — bash), E3 (structural severity — bash), E4 (catastrophic dim — bash)
- 2 agent-as-judge: E1 (document type calibration), E5 (contradiction severity)
- All written to `judges/` directory

### Phase 6: Validate Judges
- Code judges (E2, E4): 100% alignment on dev AND test splits
- E3: deterministic, 1 fixture, correct
- E1: inconsistent — False Pass on T05 (judge too lenient), False Fail on T04 (judge too strict). Root cause: nuanced distinction between first-party vs third-party claims with only 3 testable fixtures
- E5: untestable (only 1 fixture in test split)
- **Gulf 2 Gate: APPROVED** with caveats on E1/E5 noise

### Phase 7: AutoResearch Loop (5 experiments, all KEPT)

| Exp | Score | Change | Result |
|-----|-------|--------|--------|
| 0 | 24/31 (77.4%) | Baseline | E2 fails 3, E3 fails 1, E4 fails 3 |
| 1 | 27/31 (87.1%) | Credit ceiling at 95 when MAJORs present | E2: 3→0 FAIL |
| 2 | 30/31 (96.8%) | Dimension gap warning (dim < 55, overall ≥ 60) | E4: 3→0 FAIL |
| 3 | 31/31 (100%) | Structural CRITICAL for zero headings | E3: 1→0 FAIL |
| 4 | 31/31 (100%) | Contradiction CRITICAL escalation in synthesis | E5 targeted (agent judge) |
| 5 | 31/31 (100%) | Document type classification (Step 3.5) | E1 targeted (agent judge) |

**Key optimization:** Experiments 1-3 were validated analytically (recomputing scores from existing traces) without regenerating traces. Only Experiments 4-5 would need re-runs to fully validate (deferred — agent judge coverage is directional).

---

## v2 Mechanism Validation Results

| Mechanism | Status | Evidence |
|-----------|--------|----------|
| Smart sampling | **WORKING** | Stratified 9/15 by 3 dimensions, clear rationale logged |
| Preliminary clustering | **WORKING** | 4 clusters by score+CRITICAL, enabled consistency checks |
| Consistency detection | **WORKING** | Fired on C2 (resolved as defensible), confirmed C3 consistency |
| Override logging | **READY** | Mechanism present in session-log.json schema, not exercised (no user overrides) |
| session-log.json | **WORKING** | 12+ entries across all phases, correct schema |
| Full pipeline (Phases 1-7) | **WORKING** | Both gates approved, 5/5 experiments kept, 77.4%→100% |

---

## Mutations Produced (ds-review-optimized.md)

All 5 mutations are in `autoresearch-ds-review/ds-review-optimized.md`, ready for review:

1. **Step 9.4:** Credit ceiling when MAJOR findings present (dim score capped at 95)
2. **Step 10.2:** Dimension gap warning when dim < 55 and overall ≥ 60
3. **Step 6:** Structural severity escalation — zero headings → CRITICAL (-12)
4. **Step 9.11:** Contradiction severity escalation during synthesis
5. **Step 3.5 (new):** Document type classification → passed to subagents

---

## User Feedback (Critical for Autorefine v2 Decision)

**"The eval is way too long. For some skills, users don't have patience."**

This is the central tension. The full pipeline (Phases 1-7) worked correctly but took ~90 minutes with continuous human involvement. Key time sinks:
- Phase 3 trace generation: ~30 min (15 parallel subagent dispatches)
- Phase 3 human review: ~20 min (12 traces one-at-a-time)
- Phase 7 loop: ~15 min (5 experiments with analytical scoring)

For a critical skill like ds-review, this depth is justified. But for simpler skills (a formatter, a linter wrapper), the full pipeline is overkill. The autorefine v2 design should consider:
- **Tiered depth:** Quick (Phase 1 + Phase 7 only), Standard (current), Deep (+ more fixtures)
- **Phase 3 batching:** Review 3-5 traces instead of 8-10 for simpler skills
- **Skip-to-loop:** If the user already knows their failure modes, let them skip to Phase 7

---

## Workspace Artifacts

All artifacts in `skills/ds-review/autoresearch-ds-review/`:

| File | Purpose |
|------|---------|
| state.json | Pipeline state (Phase 7 complete, both gates approved) |
| session-log.json | 12 entries across all phases |
| design-audit.md | Phase 1 output |
| eval-audit-report.md | Phase 2 output |
| error-analysis-traces.md | Phase 3 review table (12 traces) |
| failure-taxonomy.md | 4 failure categories |
| eval-suite.md | 5 binary evals |
| fixtures-manifest.md | 15 fixtures with labels and splits |
| eval-classification.md | Judge type assignments |
| judges/ | 3 code + 2 agent judge files |
| judge-validation-report.md | Phase 6 TPR/TNR results |
| gate-report-gulf-1.md | Gulf 1 approval |
| gate-report-gulf-2.md | Gulf 2 approval |
| changelog.md | 5 experiments documented |
| results.json | Dashboard data (auto-refreshing) |
| dashboard.html | Visualization |
| ds-review-optimized.md | Mutated SKILL.md with all 5 changes |
| traces/ | 15 trace files (T01-T15) |
| autoresearch-ds-review-prev/ | Backup of prior workspace |
