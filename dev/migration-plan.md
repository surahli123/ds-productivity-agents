# Multi-Agent Platform Migration Plan

**Status:** Ready to execute (deferred to v0.5 implementation session)
**Date Created:** 2026-02-16
**Target Completion:** During v0.5 search-domain-knowledge skill implementation

---

## Overview

This plan reorganizes the repository from a single-agent structure to a multi-agent platform structure, supporting:
- DS Analysis Review Agent (current)
- SQL Review Agent (Q2 2026)
- Search Metric Analysis Agent (Q2 2026)

**Key principle:** Shared infrastructure (skills) separated from agent implementations.

---

## Current vs Target Structure

### Current Structure
```
DS-Analysis-Review-Agent/  (renamed to ds-productivity-agents)
├── plugin/
│   ├── agents/
│   │   ├── ds-review-lead.md
│   │   ├── analysis-reviewer.md
│   │   └── communication-reviewer.md
│   └── skills/
│       └── ds-review-framework/
├── .claude/
│   └── commands/
│       └── ds-review.md
├── dev/
├── docs/
├── CLAUDE.md
└── README.md
```

### Target Structure
```
ds-productivity-agents/
├── shared/
│   └── skills/
│       ├── ds-review-framework/           ← Moved from plugin/skills/
│       └── search-domain-knowledge/       ← New in v0.5
│           ├── SKILL.md
│           ├── config/
│           │   ├── domain-index.yaml
│           │   └── team-roster.yaml
│           └── digests/
├── agents/
│   ├── ds-review/                         ← Moved from plugin/agents/
│   │   ├── ds-review-lead.md
│   │   ├── analysis-reviewer.md
│   │   ├── communication-reviewer.md
│   │   └── domain-expert-reviewer.md      ← New in v0.5
│   ├── sql-review/                        ← Placeholder for Q2
│   │   └── README.md
│   └── search-metric-analysis/            ← Placeholder for Q2
│       └── README.md
├── .claude/
│   └── commands/
│       └── ds-review.md                   ← Stays here (discovery requirement)
├── dev/                                   ← Unchanged
├── docs/                                  ← Unchanged
├── CLAUDE.md                              ← Update content
├── README.md                              ← Complete rewrite
└── .gitignore                             ← Unchanged
```

---

## Migration Steps

### Phase 1: File Reorganization

**1. Create new directory structure:**

```bash
cd ~/ds-productivity-agents  # Or wherever your repo is

# Create shared/skills/
mkdir -p shared/skills

# Create agents/ subdirectories
mkdir -p agents/ds-review
mkdir -p agents/sql-review
mkdir -p agents/search-metric-analysis
```

**2. Move existing content:**

```bash
# Move ds-review-framework skill
git mv plugin/skills/ds-review-framework shared/skills/

# Move ds-review agents
git mv plugin/agents/ds-review-lead.md agents/ds-review/
git mv plugin/agents/analysis-reviewer.md agents/ds-review/
git mv plugin/agents/communication-reviewer.md agents/ds-review/

# Note: domain-expert-reviewer.md will be created in v0.5, goes directly to agents/ds-review/
```

**3. Clean up old plugin/ directory:**

```bash
# Check that plugin/ is now empty
ls -la plugin/

# If empty, remove it
rmdir plugin/agents
rmdir plugin/skills
rmdir plugin
```

**4. Create placeholder READMEs for future agents:**

```bash
# SQL Review placeholder
cat > agents/sql-review/README.md << 'EOF'
# SQL Review Agent

**Status:** Planned for Q2 2026

## Purpose

Reviews SQL queries for:
- SQL syntax errors
- Domain-specific anti-patterns (e.g., Search SQL best practices)
- Performance issues

## Architecture

- **Core:** SQL syntax checking (domain-agnostic)
- **Domain layer:** Calls domain knowledge skills for SQL guidance
- **Command:** `/sql-review --domain search analysis.sql`

## Dependencies

- `shared/skills/search-domain-knowledge/` (for Search SQL patterns)
- Future: Other domain skills for SQL guidance
EOF

# Search Metric Analysis placeholder
cat > agents/search-metric-analysis/README.md << 'EOF'
# Search Metric Analysis Agent

**Status:** Planned for Q2 2026

## Purpose

Analyzes search experiment metrics and generates insights.

## Workflow

1. Load metrics from CSV/database
2. Call `search-domain-knowledge` skill for context
3. Analyze metrics, detect anomalies, generate insights
4. Write analysis document
5. Call `/ds-review` to review the generated analysis
6. Return analysis + review feedback to user

## Architecture

- **Inputs:** Metric data (CSV, database query results)
- **Calls:** `search-domain-knowledge` skill, `ds-review` agent
- **Outputs:** Analysis document + review feedback

## Dependencies

- `shared/skills/search-domain-knowledge/`
- `agents/ds-review/` (used as quality gate)
EOF
```

**5. Commit reorganization:**

```bash
git add -A
git status  # Review changes

git commit -m "refactor: reorganize as multi-agent platform

- Move skills to shared/skills/ (reusable across agents)
- Move ds-review agents to agents/ds-review/
- Create placeholders for sql-review and metric-analysis agents
- Remove empty plugin/ directory

Preparing for:
- v0.5: search-domain-knowledge skill
- Q2 2026: SQL review and metric analysis agents

Breaking change: File paths updated. See migration-plan.md.
"
```

---

### Phase 2: Update .claude/commands/ds-review.md

**Current content (likely):**
```yaml
---
description: Review a DS analysis across methodology, logic, narrative, and actionability
---

[Content referring to plugin/agents/ds-review-lead.md]
```

**Update to:**
```yaml
---
description: Review a DS analysis across methodology, logic, narrative, and actionability
---

[Content referring to agents/ds-review/ds-review-lead.md]
```

**Specific changes needed:**
- Search file for any references to `plugin/agents/`
- Replace with `agents/ds-review/`
- Search for any references to `plugin/skills/`
- Replace with `shared/skills/`

**Commit:**
```bash
git add .claude/commands/ds-review.md
git commit -m "fix: update command to reference new agent paths"
```

---

### Phase 3: Update Documentation

#### 3.1 Update CLAUDE.md

**File:** `/Users/surahli/ds-productivity-agents/CLAUDE.md`

**Changes needed:**

1. **Section: "# DS Analysis Review Agent" → "# DS Productivity Agents"**

```markdown
# DS Productivity Agents

## What This Is
A suite of Claude Code agents for DS productivity in Search Relevance:
- **DS Analysis Review Agent:** Reviews DS analyses across methodology, logic, communication, and domain expertise
- **SQL Review Agent:** (Q2 2026) Reviews SQL queries for syntax and domain-specific patterns
- **Search Metric Analysis Agent:** (Q2 2026) Analyzes search metrics and generates insights

All agents share domain knowledge infrastructure for consistent Search Relevance expertise.
```

2. **Update "Agent Architecture" section:**

```markdown
## Agent Architecture

### DS Analysis Review
- ds-review-lead.md — orchestrator (invoked via /ds-review command)
- analysis-reviewer.md — subagent for analysis dimension
- communication-reviewer.md — subagent for communication dimension
- domain-expert-reviewer.md — subagent for domain dimension (v0.5+)

### Shared Skills
- ds-review-framework — shared rubrics and personas (auto-loaded)
- search-domain-knowledge — Search Relevance domain expertise (v0.5+)
```

3. **Update file paths in "Current State" and other sections**

Replace:
- `plugin/agents/` → `agents/ds-review/`
- `plugin/skills/` → `shared/skills/`

#### 3.2 Rewrite README.md

**File:** `/Users/surahli/ds-productivity-agents/README.md`

**Complete replacement:**

```markdown
# DS Productivity Agents

A suite of Claude Code agents for data science workflows in Search Relevance. Built on shared domain knowledge for Query Understanding, Search Ranking, and Search Infrastructure.

## Agents

### 📊 DS Analysis Review (`/ds-review`)

Reviews completed DS analyses across three dimensions:
- **Analysis:** Methodology, logic, completeness, metrics (domain-agnostic)
- **Communication:** Narrative, audience fit, visualization, actionability (domain-agnostic)
- **Domain Knowledge:** Domain-specific techniques, benchmarks, pitfalls (v0.5+)

**Usage:**
```bash
/ds-review path/to/analysis.md
/ds-review --domain search-ranking path/to/analysis.md  # v0.5+
```

**Status:** ✅ Shipped (v0.4.1)

---

### 🔍 SQL Review (`/sql-review`)

Reviews SQL queries for syntax correctness and domain-specific patterns.

**Checks:**
- SQL syntax errors
- Search-specific SQL anti-patterns
- Performance issues
- Alignment with domain best practices

**Usage:**
```bash
/sql-review --domain search path/to/query.sql
```

**Status:** 🚧 Planned for Q2 2026

---

### 📈 Search Metric Analysis (`/metric-analysis`)

Analyzes search experiment metrics and generates insights.

**Workflow:**
1. Load metrics from CSV or database
2. Fetch Search domain context
3. Analyze metrics, detect anomalies
4. Generate analysis document
5. Review analysis via DS Review agent
6. Return analysis + review feedback

**Usage:**
```bash
/metric-analysis experiments/ranking-v2.csv
```

**Status:** 🚧 Planned for Q2 2026

---

## Shared Infrastructure

### Domain Knowledge Skills

**search-domain-knowledge** (v0.5+)
- Search Relevance expertise: Query Understanding, Search Ranking, Search Infrastructure
- Used by: DS review, SQL review, metric analysis agents
- Auto-refreshed weekly (workstream) and monthly (foundational)

**Future domains:**
- `causal-domain-knowledge` - Causal Inference
- `nlp-domain-knowledge` - NLP

### Review Framework

**ds-review-framework**
- Analysis and Communication rubrics
- Scoring models, deduction tables
- Used by: DS review agent

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Shared Skills (Infrastructure Layer)              │
│  ├── ds-review-framework                           │
│  └── search-domain-knowledge                       │
└─────────────────────────────────────────────────────┘
         ↑              ↑              ↑
         │              │              │
    ┌────┴───┐     ┌────┴───┐     ┌────┴────────┐
    │ DS     │     │ SQL    │     │ Metric      │
    │ Review │     │ Review │     │ Analysis    │
    └────────┘     └────────┘     └─────────────┘
                                        │
                                        ├─ calls ─→ DS Review
                                        └─ for quality gate
```

**Key relationships:**
- All agents share `search-domain-knowledge` for consistent domain expertise
- Metric Analysis agent calls DS Review agent as a quality gate for its output
- DS Review is domain-agnostic; domain expertise comes from pluggable skills

---

## Project Structure

```
ds-productivity-agents/
├── shared/skills/          # Reusable infrastructure
├── agents/                 # Agent implementations
│   ├── ds-review/
│   ├── sql-review/
│   └── search-metric-analysis/
├── .claude/commands/       # Command entry points
├── dev/                    # Development artifacts
│   ├── backlog.md
│   ├── sessions/
│   ├── test-results/
│   └── decisions/
└── docs/                   # Design docs, plans
```

---

## Current Status

**Shipped:**
- v0.4.1: DS Analysis Review Agent (2-dimension scoring)

**In Progress:**
- v0.5: Domain Knowledge dimension (3rd review dimension)
  - Search domain knowledge skill
  - Domain expert reviewer subagent
  - 50/25/25 weighted scoring

**Planned (Q2 2026):**
- SQL Review Agent
- Search Metric Analysis Agent

See `dev/backlog.md` for detailed roadmap.

---

## Development

### Session Start Protocol
1. Read `dev/backlog.md` for current priorities
2. Read latest `dev/sessions/*.md` for context
3. Check `dev/decisions/` for architectural decisions

### Session End Protocol
1. Update `dev/backlog.md`
2. Create `dev/sessions/YYYY-MM-DD-description.md`
3. Update `CHANGELOG.md` if anything shipped
4. Create `dev/decisions/ADR-*.md` if design choice was made

---

## Contributing

This is a personal project for learning vibe coding and building DS productivity tools.

## License

MIT
```

#### 3.3 Update MEMORY.md

**File:** `~/.claude/projects/-Users-surahli-ds-productivity-agents/memory/MEMORY.md`

**Changes needed:**

1. **Update title:**
```markdown
# DS Productivity Agents — Memory
```

2. **Update Project Structure section:**
```markdown
## Project Structure
- Shared infrastructure: `shared/skills/` (ds-review-framework, search-domain-knowledge)
- Agent implementations: `agents/` (ds-review, sql-review, metric-analysis)
- Commands: `.claude/commands/`
- Dev artifacts: `dev/` (backlog, sessions, test-results, reviews, decisions, test-fixtures)
- Plans: `docs/plans/`
- Session end protocol: update backlog, create session log, update CHANGELOG if shipped, create ADR if design decision made
```

3. **Update Key Files section:**
```markdown
## Key Files
- `dev/backlog.md` — always read first for current state
- Latest `dev/sessions/*.md` — context from prior session
- `.claude/commands/ds-review.md` — project command entry point (invoke as `/ds-review`)
- `shared/skills/ds-review-framework/SKILL.md` — shared rubrics (~270 lines, 8 sections + 2b)
- `agents/ds-review/ds-review-lead.md` — orchestrator (10-step pipeline, ~195 lines)
- `shared/skills/search-domain-knowledge/` — Search domain expertise (v0.5+)
- `dev/migration-plan.md` — multi-agent platform reorganization plan
```

**Commit all documentation:**
```bash
git add CLAUDE.md README.md
git add ~/.claude/projects/-Users-surahli-ds-productivity-agents/memory/MEMORY.md
git commit -m "docs: update for multi-agent platform rebrand

- Update CLAUDE.md to reflect multi-agent scope
- Rewrite README with agent suite overview
- Update MEMORY.md with new file paths and structure
- Document shared infrastructure pattern
"
```

---

### Phase 4: Update Backlog

**File:** `dev/backlog.md`

Add a note at the top:

```markdown
## Repository Rebrand (Completed 2026-02-16)

Renamed from `DS-Analysis-Review-Agent` to `ds-productivity-agents` to reflect multi-agent platform scope.

**Organizational changes:**
- Shared skills: `shared/skills/` (reusable across agents)
- Agent implementations: `agents/ds-review/`, `agents/sql-review/`, `agents/search-metric-analysis/`
- Future agents can be added to `agents/` and reuse shared skills

**No functional changes** — this was a pure reorganization.
```

---

### Phase 5: Verification

**Run these checks after migration:**

1. **Test DS review command:**
```bash
cd ~/ds-productivity-agents
# In Claude Code session, run:
/ds-review dev/test-fixtures/vanguard-analysis.md
# Should work without errors
```

2. **Check file paths:**
```bash
# Verify old paths are gone
find . -type f -name "*.md" -exec grep -l "plugin/agents" {} \;
find . -type f -name "*.md" -exec grep -l "plugin/skills" {} \;
# Should return nothing (or only in session logs / changelogs)

# Verify new paths exist
ls -la shared/skills/ds-review-framework/
ls -la agents/ds-review/
```

3. **Check git status:**
```bash
git status
# Should be clean (or only uncommitted v0.5 work)

git log --oneline -5
# Should show migration commits
```

---

## Rollback Plan

If something breaks during migration:

**Before Phase 2 commit:**
```bash
git reset --hard HEAD  # Discard all changes
```

**After Phase 2 commit:**
```bash
git log --oneline -5   # Find commit before migration
git revert <commit-sha>  # Create revert commit
# OR
git reset --hard <commit-before-migration>
git push --force  # Only if you haven't shared the branch
```

**If .claude/commands broken:**
- Command discovery happens at session start
- Worst case: manually edit `.claude/commands/ds-review.md` back to old paths
- Restart Claude Code session

---

## Success Criteria

Migration is complete when:

- [ ] All files moved to new structure
- [ ] `plugin/` directory removed
- [ ] `.claude/commands/ds-review.md` references correct paths
- [ ] CLAUDE.md updated with new structure
- [ ] README.md rewritten for multi-agent platform
- [ ] MEMORY.md updated with new paths
- [ ] `dev/backlog.md` notes the migration
- [ ] `/ds-review` command works in Claude Code
- [ ] All commits pushed to GitHub
- [ ] No references to old `plugin/` paths in active code

---

## Post-Migration: Building v0.5

After migration is complete, proceed with v0.5 implementation:

1. Create `shared/skills/search-domain-knowledge/` (follow design doc)
2. Create `agents/ds-review/domain-expert-reviewer.md`
3. Update `agents/ds-review/ds-review-lead.md` for 3-dimension scoring
4. Test with calibration fixtures

See `docs/plans/2026-02-15-domain-knowledge-subagent-design-v3.md` for v0.5 spec.

---

## Questions / Issues

If you encounter issues during migration:

1. Check this plan's Rollback section
2. Check `dev/sessions/` for migration session log
3. Verify paths in `.claude/commands/ds-review.md`
4. Test command with a known-good fixture

**Common issues:**
- Command not found → Check `.claude/commands/` still has `ds-review.md`
- Agent file not found → Check `agent:` path in command file matches new location
- Skill not loading → Check skill path references in agent prompts
