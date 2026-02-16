# Session: Domain Knowledge Subagent Brainstorm

**Date:** 2026-02-15
**Branch:** `feat/v0.4.1-credit-redesign`
**Commit:** `e5cfd48` — design doc only

## What Happened

Brainstormed and designed a third review dimension (Domain Knowledge) for the DS analysis
review agent. Used the `superpowers:brainstorming` skill to structure the process.

## Decisions Made (13 total)

| # | Decision | Choice |
|---|---|---|
| D1 | Core purpose | Domain expertise + factual accuracy (combined) |
| D2 | Knowledge source | User-provided context + web search |
| D3 | Scoring model | Full third dimension (scored /100) |
| D4 | Lenses | 4: Technique Appropriateness, Benchmark Validity, Domain Pitfall Awareness, Claim Verification |
| D5 | Boundary model | Model B: Generic vs. Domain-Specific (analysis-reviewer unchanged) |
| D6 | Web search | Active verification |
| D7 | Architecture | Approach A: Standalone Parallel Subagent |
| D8 | Deduction range | -3 to -20 (same as other dimensions) |
| D9 | Strength credit cap | +25 (same as other dimensions) |
| D10 | Web search failure | Flag as "unverified" — no deduction |
| D11 | No --domain flag | Require it — skip subagent if not passed (2-way score) |
| D12 | Scoring weight | Equal 33/33/33 |
| D13 | Knowledge pre-processing | Curated Index + Live Fetch (YAML maps domains to Confluence page IDs) |

## Key Design Choices Explored

- **Boundary models:** Model A (internal vs. external validity) vs. Model B (generic vs.
  domain-specific). Chose B — cleaner separation, analysis-reviewer doesn't change.
- **Knowledge pre-processing:** RAG pipeline, periodic digest, just-in-time search, or
  curated index. Chose curated index — simplest, most controllable, with evolution path
  to periodic digest if latency is an issue.
- **Architecture:** Parallel subagent vs. sequential enrichment vs. post-hoc cross-reference.
  Chose parallel — follows existing pattern, calibrate independently.

## Artifacts

- Design doc: `docs/plans/2026-02-15-domain-knowledge-subagent-design.md` (v1)
- Backlog updated with v0.5 section

## Open Items for Next Session

1. Lens 4 (Claim Verification) scope — keep, merge with Lens 2, or remove?
2. Domain index: populate with real Confluence page IDs
3. Graceful degradation when Confluence fetch fails
4. User flagged Lens 4 may be less important than Lenses 1-3

## Next Steps

1. Web session: review design doc as senior DS lead (prompt prepared)
2. Resolve open items based on web session feedback
3. Architecture design session to finalize
4. Then: implementation planning (writing-plans skill)
