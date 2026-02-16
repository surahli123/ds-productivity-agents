# Repository Architecture Discussion — Session Log

**Date:** 2026-02-16
**Session Type:** Architecture discussion (no code changes)
**Participants:** Product Owner (user), Claude Code

---

## Session Summary

Discussed repository organization strategy for the domain knowledge skill and upcoming agents. Concluded with decision to rename repository to `ds-productivity-agents` and reorganize as a multi-agent platform.

---

## Context

User has two files in Downloads:
1. `2026-02-15-domain-knowledge-session-log.md` - design review session log
2. `2026-02-15-domain-knowledge-subagent-design-v3.md` - final design spec for v0.5

**Key insight from design doc:** Domain Knowledge Skill (Layer 1) is designed as a standalone reusable service, independent of the DS review agent. Other agents can call this skill.

**User's upcoming roadmap (next 2-3 months):**
1. DS Analysis Review Agent (current)
2. SQL Review Agent - reviews SQL code for syntax + domain-specific patterns (domain-agnostic core)
3. Search Metric Analysis Agent - analyzes search metrics, calls domain knowledge skill + DS review agent

---

## Discussion Flow

### Phase 1: File Organization

Moved two domain knowledge design files from Downloads to project:
- Session log → `dev/sessions/2026-02-15-domain-knowledge-session-log.md`
- Design doc v3 → `docs/plans/2026-02-15-domain-knowledge-subagent-design-v3.md`

### Phase 2: Repository Organization Options

**Initial question:** How to organize repos given that the domain knowledge skill is reusable?

**Options presented:**
1. **Monorepo (current state)** - everything in DS-Analysis-Review-Agent
2. **Separate repo for skill** - extract domain knowledge skill to its own repo
3. **Monorepo with boundaries** - organize as `shared/skills/` and `agents/`
4. **DS toolkit umbrella repo** - broader scope for future shared components

**Initial recommendation:** Option 3 (monorepo with boundaries), extract to Option 2 later when second consumer emerges.

### Phase 3: User Clarifications (Critical Pivot)

User clarified two key points that changed the recommendation:

**Clarification 1: SQL Review Agent is Option B (domain-agnostic)**
- Checks SQL syntax (generic)
- Uses domain knowledge skills for SQL guidance (e.g., Search SQL patterns)
- Similar to DS review: core is generic, domain expertise is pluggable

**Clarification 2: Search Metric Analysis Agent is a peer product**
- NOT a helper/subagent of DS review
- Independent workflow with its own purpose
- Calls `search-domain-knowledge` skill for context
- Calls `ds-review` agent to review its own output (agent-calling-agent pattern)

**Key realization:** We're building a **platform of 3 peer-level agents** that share infrastructure, not a single agent with helpers.

### Phase 4: User Pushback on Naming

**Claude suggested:** Rename to `search-relevance-toolkit`

**User pushback:** DS Analysis Review Agent is domain-agnostic, works for any domain (Search, Causal, NLP, etc.). Renaming to "search-relevance-toolkit" artificially limits scope.

**Correct framing:**
- **DS Review Agent** - domain-agnostic product (can review any DS analysis)
- **Domain knowledge skills** - pluggable content modules (Search, Causal, NLP)
- **Search-specific helpers** - SQL review and metric analysis (but SQL review is also domain-agnostic!)

**Revised insight:** This is a **DS productivity platform** with:
- Domain-agnostic core agents (DS review, SQL review)
- Pluggable domain knowledge skills (Search, Causal, NLP)
- Domain-specific agents (Search metric analysis)

### Phase 5: Final Recommendation

**Recommendation: Option 3 → Rename to `ds-productivity-agents`**

**Rationale:**
1. Three peer-level agents sharing infrastructure (monorepo reduces overhead)
2. All agents are DS productivity tools (coherent suite)
3. User is solo dev in fast iteration mode (monorepo simplifies workflow)
4. Agent-calling-agent pattern easier in monorepo (metric analysis calls DS review)
5. Scales to future domains (add `causal-domain-knowledge` skill, agents auto-support it)

**User decision:** "Maybe A, let's go with that."

---

## Deliverables

### 1. File Moves
- `dev/sessions/2026-02-15-domain-knowledge-session-log.md` (moved from Downloads)
- `docs/plans/2026-02-15-domain-knowledge-subagent-design-v3.md` (moved from Downloads)

### 2. Documentation Created

**`dev/RENAME-STEPS.md`** - Step-by-step guide for GitHub rename:
- Rename repo on GitHub
- Update local git remote
- Rename local directory (optional)
- Verification steps

**`dev/migration-plan.md`** (~500 lines) - Comprehensive migration plan:
- Current vs target structure diagrams
- Phase 1: File reorganization (bash commands)
- Phase 2: Update `.claude/commands/ds-review.md` paths
- Phase 3: Update documentation (CLAUDE.md, README.md, MEMORY.md)
- Phase 4: Update backlog
- Phase 5: Verification checklist
- Rollback plan
- Success criteria
- Post-migration: v0.5 building instructions

### 3. Backlog Updated

Added "Repository Rebrand Decision" section to `dev/backlog.md`:
- Decision rationale
- Status checklist
- Next steps

---

## Target Repository Structure

```
ds-productivity-agents/  (renamed from DS-Analysis-Review-Agent)
├── shared/
│   └── skills/
│       ├── ds-review-framework/           ← Existing, moved from plugin/skills/
│       └── search-domain-knowledge/       ← New in v0.5
├── agents/
│   ├── ds-review/                         ← Existing, moved from plugin/agents/
│   ├── sql-review/                        ← Placeholder for Q2
│   └── search-metric-analysis/            ← Placeholder for Q2
├── .claude/commands/
│   └── ds-review.md                       ← Stays here (discovery requirement)
├── dev/                                   ← Unchanged
├── docs/                                  ← Unchanged
├── CLAUDE.md                              ← Update content
└── README.md                              ← Complete rewrite
```

---

## Architecture Relationships

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
- All 3 agents share `search-domain-knowledge` for consistent domain expertise
- Metric Analysis agent calls DS Review agent as a quality gate for its output
- DS Review and SQL Review are domain-agnostic; domain expertise comes from pluggable skills

---

## Execution Plan

### Now (This Session)
- [x] Move domain knowledge design files from Downloads
- [x] Write `dev/RENAME-STEPS.md`
- [x] Write `dev/migration-plan.md`
- [x] Update `dev/backlog.md`
- [x] Create this session log

### Next (User Action)
- [ ] Execute `dev/RENAME-STEPS.md` to rename GitHub repo
- [ ] Update local clone

### Later (v0.5 Implementation Session)
- [ ] Execute `dev/migration-plan.md` to reorganize files
- [ ] Build `shared/skills/search-domain-knowledge/` per design doc
- [ ] Build `agents/ds-review/domain-expert-reviewer.md`
- [ ] Update documentation (CLAUDE.md, README.md, MEMORY.md)

---

## Key Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Rename to `ds-productivity-agents` | Accurately reflects multi-agent platform scope |
| D2 | Monorepo structure | Solo dev, shared infrastructure, fast iteration |
| D3 | Defer file reorganization to v0.5 | Natural time to reorganize when building new skill |
| D4 | Separate rename from reorganization | GitHub rename is low-risk; file moves can be planned |

---

## Analogies Used (Product/DS Context)

- **Shared library vs product monolith** - Core tension in organizing code
- **Platform service vs product feature** - Domain knowledge skill (platform) vs DS review agent (product)
- **Ranking model framework** - DS review agent is like a framework (generic), domain skills are like feature sets (pluggable)
- **Data platform team** - Building a suite of tools with shared infrastructure, not a single product
- **Microservices vs monolith** - Option 2 (separate repos) vs Option 3 (monorepo with boundaries)

---

## Open Questions

None - all questions resolved during session.

---

## Next Session Pickup

1. **If doing GitHub rename:** User executes `dev/RENAME-STEPS.md`
2. **If starting v0.5:** Read `dev/migration-plan.md`, execute file reorganization, then build domain knowledge skill per `docs/plans/2026-02-15-domain-knowledge-subagent-design-v3.md`
3. **Check:** `dev/backlog.md` for current priorities

---

## Files Modified This Session

- Created: `dev/RENAME-STEPS.md`
- Created: `dev/migration-plan.md`
- Created: `dev/sessions/2026-02-15-domain-knowledge-session-log.md` (moved from Downloads)
- Created: `docs/plans/2026-02-15-domain-knowledge-subagent-design-v3.md` (moved from Downloads)
- Updated: `dev/backlog.md` (added rebrand decision section)
- Created: This session log

---

## Session Duration

~30 minutes (discussion + documentation)

## Session Mode

Discussion only - no code changes, no implementation
