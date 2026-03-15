# DS Productivity Agents

A Claude Code plugin skill set for data science workflows in Search Relevance. Refactored from a custom multi-agent system (`agents/` + `shared/skills/`) into a portable, eval-validated skill set architecture (`skills/`).

**v0.6 Highlights:** 2 independent skills, 4 calibration rounds, 39/39 structural eval assertions, 4 independent expert reviews (DS Lead, PM Lead, Principal AI Engineer, IC9 Search SME).

## Skills

### 📊 DS Analysis Review (`/ds-review`)

Reviews completed DS analyses across three dimensions:
- **Analysis:** Methodology, logic, completeness, metrics (domain-agnostic)
- **Communication:** Narrative, audience fit, visualization, actionability (domain-agnostic)
- **Domain Knowledge:** Domain-specific techniques, benchmarks, pitfalls (v0.5+)

Dispatches 3 parallel reviewer subagents, fuses scores with diminishing returns and deduplication, and produces a scored review with per-lens ratings and priority fixes.

**Usage:**
```bash
/ds-review path/to/analysis.md
/ds-review path/to/analysis.md --mode quick --audience exec --workflow proactive
/ds-review --domain search-ranking path/to/analysis.md  # 3-dimension review (50/25/25)
```

**Scoring:** 100-point scale with deduction tables, strength credits (capped at +15/dimension), diminishing returns, and floor rules. Calibrated through 4 rounds (R1-R4) with known baselines.

**Status:** ✅ Shipped (v0.6.0)

---

### 🔍 SQL Review (`/sql-review`)

Reviews SQL queries for syntax correctness and domain-specific patterns.

**Status:** 🚧 Planned (Q2 2026)

---

### 📈 Search Metric Analysis (`/metric-analysis`)

Analyzes search experiment metrics and generates insights.

**Status:** 🚧 Planned (Q2 2026)

---

## Shared Infrastructure

### Domain Knowledge (`search-domain-knowledge` skill)

Curated Search Relevance expertise consumed by all skills:
- **Digests:** `search-ranking.md`, `query-understanding.md`, `search-cross-domain.md`
- **Authority model:** Authoritative (full deductions) vs Advisory (capped at -2)
- **Audience filtering:** `[audience: all]`, `[audience: ds]`, `[audience: eng]`
- **Staleness checks:** Fresh (<14d), Warning (14-30d), Critical (>30d)
- **Refresh:** Manual only (v0.6). Trigger via `--refresh-domain`.

### Review Framework (`references/framework.md`)

Shared rubrics for the DS review skill:
- Severity definitions (CRITICAL, MAJOR, MINOR, ADVISORY)
- Deduction tables for 11 review lenses across 3 dimensions
- Strength credit tables with per-dimension caps
- Floor rules, audience personas, dimension boundary routing

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Skills (Plugin Layer)                              │
│  ├── ds-review/                                     │
│  │   ├── SKILL.md (orchestrator)                    │
│  │   └── references/ (reviewers + framework)        │
│  └── search-domain-knowledge/                       │
│      ├── SKILL.md (consumption contract)            │
│      └── digests/ (domain knowledge)                │
└─────────────────────────────────────────────────────┘
         ↑              ↑              ↑
         │              │              │
    ┌────┴───┐     ┌────┴───┐     ┌────┴────────┐
    │ DS     │     │ SQL    │     │ Metric      │
    │ Review │     │ Review │     │ Analysis    │
    └────────┘     └────────┘     └─────────────┘
     (shipped)     (planned)       (planned)
```

**Key relationships:**
- All skills share `search-domain-knowledge` for consistent domain expertise
- DS Review is domain-agnostic; domain expertise comes from pluggable domain skills
- Command at `.claude/commands/ds-review.md` delegates to `skills/ds-review/SKILL.md`
- Paths: skill-relative within skills, project-relative for cross-skill references

---

## Project Structure

```
ds-productivity-agents/
├── .claude-plugin/            # Plugin manifest (for future marketplace)
├── .claude/commands/          # Project-level command entry points
│   └── ds-review.md           # /ds-review command (thin, delegates to SKILL.md)
├── skills/                    # Skill definitions
│   ├── ds-review/             # DS Analysis Review skill
│   │   ├── SKILL.md           # Lead orchestrator pipeline (10 steps)
│   │   ├── evals/             # Eval framework (3 test cases, 39 assertions)
│   │   └── references/        # Reviewer prompts + framework
│   │       ├── framework.md   # Deduction tables, credits, floor rules
│   │       ├── analysis-reviewer.md
│   │       ├── communication-reviewer.md
│   │       └── domain-expert-reviewer.md
│   └── search-domain-knowledge/
│       ├── SKILL.md           # Consumption contract
│       ├── references/        # Domain index (domain-index.yaml)
│       └── digests/           # Domain knowledge digests
│           ├── search-ranking.md
│           ├── query-understanding.md
│           └── search-cross-domain.md
└── docs/                      # Design docs and plans
```

---

## v0.6 Refactoring: Agents → Skills

The system was originally built as a custom multi-agent architecture with agent prompts in `agents/`, shared rubrics in `shared/skills/`, and a 44-line command dispatcher. v0.6 refactored everything into a Claude Code plugin skill set — a portable, standards-compliant structure that follows the same patterns as [superpowers](https://github.com/obra/superpowers) and [kaizen](https://github.com/NeoLabHQ/context-engineering-kit).

**What changed:**
- `agents/ds-review/` (4 agent prompts) → `skills/ds-review/references/` (co-located with SKILL.md)
- `shared/skills/ds-review-framework/SKILL.md` (338-line rubric) → `skills/ds-review/references/framework.md`
- `shared/skills/search-domain-knowledge/` → `skills/search-domain-knowledge/` (standalone skill)
- 44-line command → 10-line thin command (delegates to SKILL.md, single source of truth)
- Credit cap bug fixed: +25 → +15 across all files (R4 calibration validated +15)
- ~35 bare `SKILL.md` references disambiguated to `framework.md` (preventing subagent confusion)

**Why:** Portability (skill works from any project), clean separation (domain knowledge is independent of the review pipeline), and extensibility (new skills like SQL Review drop in under `skills/` without touching existing code).

### Validation

The refactoring was validated with both structural and scoring tests to ensure nothing broke:

**Structural Contract Eval (39/39 PASS):**

| Eval | Document | Config | Assertions | Code Path |
|------|----------|--------|------------|-----------|
| Vanguard | A/B test (1,125 words) | quick/tech/reactive | 17/17 | 2-dim, floor rules, conditional credits |
| Rossmann | ML forecasting (7,452 words) | quick/mixed/general | 11/11 | 2-dim, credit cap maxing, large doc Tier 3 |
| Eppo | Search ranking (550 words) | quick/ds/proactive+domain | 11/11 | 3-dim, domain digests, cross-dim dedup, floor override |

**Scoring Pipeline Features Validated:**

| Feature | Status |
|---------|--------|
| 2-dimension scoring (50/50) | ✅ |
| 3-dimension scoring (50/25/25) | ✅ |
| Diminishing returns formula | ✅ |
| Credit cap (+15 per dimension) | ✅ |
| Conditional credit rule (halved for unvalidated experiments) | ✅ |
| Floor rules (confirming, non-overriding, overriding) | ✅ all 3 variants |
| Cross-dimension dedup (Stage 2) | ✅ |
| Domain digest loading + staleness warning | ✅ |
| Skill-relative path resolution | ✅ |
| Cross-skill path resolution | ✅ |

**Baseline Comparison:**

| Fixture | R4 Baseline | Post-Migration | Delta | Tolerance | Status |
|---------|------------|----------------|-------|-----------|--------|
| Vanguard | 57 | 59 | +2 | ±5 | ✅ PASS |

### Review Process

4 independent reviews informed the design before implementation:

| Reviewer | Focus | Key Finding |
|----------|-------|-------------|
| DS Lead (8/10) | Scoring integrity | Flagged credit cap discrepancy (+25 vs +15) — fixed |
| PM Lead (7.8/10) | Value proposition | Challenged priority vs. backlog — validated architecture investment |
| Principal AI Engineer (7.6/10) | Plugin architecture | Flagged `${CLAUDE_PLUGIN_ROOT}` unreliability — led to Option B (project-relative paths) |
| IC9 Search SME | Domain depth | Flagged domain knowledge content gaps — captured in backlog for v1.0 |

Eval definitions at `skills/ds-review/evals/evals.json`.

---

## Current Status

**Shipped:**
- v0.6.0: Plugin skill set refactoring — 2 skills, thin command, eval framework, credit cap fix
- v0.5.0: Domain Knowledge dimension — 3rd review dimension, search domain digests, authority model
- v0.4.1: Calibrated scoring — 4 calibration rounds, diminishing returns, strength credits

**Calibration Baselines (R4):**
| Fixture | Score | Consistency |
|---------|-------|-------------|
| Vanguard A/B test | 57-59 | ±2 |
| Airbnb interleaving | 93-95 | ±2 |
| Rossmann sales | 63-71 | — |

**Planned (Q2 2026):**
- SQL Review skill
- Search Metric Analysis skill

---

## Contributing

This is a personal project for learning vibe coding and building DS productivity tools.

## License

MIT
