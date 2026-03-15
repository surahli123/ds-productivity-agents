# DS Productivity Agents

A Claude Code plugin skill set for data science workflows in Search Relevance. Built on shared domain knowledge for Query Understanding, Search Ranking, and Search Infrastructure.

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
├── dev/                       # Development artifacts
│   ├── backlog.md             # Priorities + IC9 findings
│   ├── sessions/              # Session logs
│   ├── reviews/               # Calibration reviews
│   ├── test-fixtures/         # Real + synthetic test documents
│   ├── test-results/          # Calibration results (R1-R4)
│   └── decisions/             # Architecture Decision Records
└── docs/                      # Design docs, plans, handovers
```

---

## Current Status

**Shipped:**
- v0.6.0: Plugin skill set refactoring — 2 skills, thin command, credit cap fix (+25→+15), eval framework
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

See `dev/backlog.md` for detailed roadmap including IC9 Search SME findings.

---

## Development

### Session Start Protocol
1. Read `dev/backlog.md` for current priorities
2. Read latest `dev/sessions/*.md` for context
3. Read `docs/handover-*.md` for most recent handover
4. Check `dev/decisions/` for architectural decisions

### Session End Protocol
1. Update `dev/backlog.md`
2. Create `dev/sessions/YYYY-MM-DD-description.md`
3. Update `CHANGELOG.md` if anything shipped
4. Create handover prompt at `docs/handover-YYYY-MM-DD-topic.md`

---

## Contributing

This is a personal project for learning vibe coding and building DS productivity tools.

## License

MIT
