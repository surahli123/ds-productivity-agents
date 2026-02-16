# Prompt for Next Claude Code Session: Synthesize Multi-Role Reviews

Copy everything below the line into a new Claude Code session.

---

I'm continuing calibration work on the DS analysis review agent. A Claude Web session produced an independent evaluation of our rubric and proposed 6 SKILL.md fixes. Three different reviewer roles then critiqued that proposal from their own perspectives. I need you to synthesize all the feedback into a single implementation decision document.

## Your Role: Chief of Staff / Technical Program Manager

You are the person who sits across IC9 Architect, PM Lead, and DS Lead — you don't own any single function, but you own the decision. Your job is to:

1. **Find the consensus** — where do all 3 reviewers agree? Those items are ready to ship.
2. **Resolve the conflicts** — where do reviewers disagree, what is the right call, and why?
3. **Identify blind spots** — what did none of the 3 reviewers address that still matters?
4. **Produce a final implementation spec** — exactly what changes go into which files, in what order, with what validation criteria. This spec should be directly executable by the next Claude Code session with zero ambiguity.

## Context Files — Read in This Order

### Layer 1: The Original Proposal (what's being reviewed)
1. `dev/specs/proposal_skillmd_immediate_fixes.md` — 6 proposed SKILL.md edits with evidence, priority, and validation criteria
2. `dev/reviews/2026-02-15-independent-rubric-evaluation.md` — Full independent rubric critique from Claude Web session (8 proposed changes, 6 distilled into the proposal)
3. `dev/test-results/ds_blog_rubric_analysis.md` — Upstream evidence: gut-feel vs rubric scoring of 6 published DS blog posts, identifying 6 systematic biases

### Layer 2: The Three Reviewer Perspectives
4. `dev/reviews/2026-02-15-ic9-architect-review-of-web-session.md` — IC9 Principal Architect review. Key contributions: caught that Fix 1 can't work in SKILL.md (subagents run in parallel), flagged cross-run variability concern, deferred Fix 2 to v0.5.
5. `dev/reviews/2026-02-15-pm-lead-review-of-web-session.md` — PM Lead review. Key contributions: trust framework for prioritization, partial-overlap guidance for Fix 1, product risk analysis (dimension asymmetry, interaction effects, self-deliberation urgency).
6. `dev/reviews/2026-02-15-ds-lead-proposal-review.md` — Senior DS Lead review. Key contributions: challenged Fix 5's actual impact (cosmetic +1-2 pts), challenged blog-post evidence driving internal-tool changes, elevated extended validation as P0.

### Layer 3: System Context (what already exists)
7. `dev/decisions/ADR-003-calibration-approach.md` — What R2 calibration already fixed (don't revert)
8. `plugin/skills/ds-review-framework/SKILL.md` — Current rubric (the file being edited)
9. `plugin/agents/ds-review-lead.md` — Orchestrator agent (where Fix 1 should actually go per IC9)
10. `plugin/agents/communication-reviewer.md` — Where self-deliberation fix goes
11. `dev/backlog.md` — Current sprint state and deferred items

### Layer 4: R2 Review Outputs (evidence base)
12. `dev/test-results/2026-02-15-r2-vanguard-review.md` — Score 69, duplicate-counting visible
13. `dev/test-results/2026-02-15-r2-meta-review.md` — Score 54, baseline for "weak analysis stays low"
14. `dev/test-results/2026-02-15-r2-rossmann-review.md` — Score 71, self-deliberation visible in strength log

## What to Produce

A single markdown file saved to `dev/specs/synthesis-final-implementation-spec.md` containing:

### Section 1: Consensus Matrix
A table showing each proposed change, what each reviewer said, and where they agree/disagree. Include the items reviewers added that weren't in the original proposal (self-deliberation fix, extended validation, cross-run consistency).

### Section 2: Conflict Resolution
For each disagreement, state the conflict, weigh the arguments, and make a call. Explain your reasoning. Key conflicts to resolve:
- **Fix 1 implementation location:** Web session says SKILL.md Section 5, IC9 says lead agent Step 9. (IC9 is likely right on the technical merits — but verify by reading the agent files.)
- **Fix 5 priority:** Web session says P0, IC9 splits into P0/P1, DS Lead says all P1 (cosmetic impact). What's the right call?
- **Self-deliberation fix priority:** IC9 says "should be fixed," PM says P1, DS Lead says P0. Where does it land?
- **Extended validation timing:** DS Lead says P0 (run before more edits), PM says run after fixes with clean attribution. What's the right sequencing?

### Section 3: Final Implementation Spec
For each accepted change:
- **Exact file** to edit
- **What to add/change** (specific enough that the next session can copy-paste or Edit directly)
- **Priority** (P0 = ship now, P1 = ship in same batch but lower urgency)
- **Validation criteria** (what to check after the edit)

### Section 4: Deferred Items
What was rejected or deferred, why, and what would trigger reconsideration.

### Section 5: Implementation Order
The exact sequence of steps for the next Claude Code session. Account for:
- Dependencies between fixes (e.g., Fix 1 depends on reading the lead agent to understand Step 9)
- Whether to ship fixes incrementally or as a batch
- When to run validation (after each fix? after all fixes? both?)

### Section 6: Open Questions for Product Owner
Any decisions that the three reviewers flagged but couldn't resolve without the product owner's input. These should be yes/no or A-vs-B questions, not open-ended.

## What NOT to Do

- Do not implement any changes. This session is synthesis only.
- Do not re-review the original proposal from scratch. The three reviewers already did that work — synthesize their findings.
- Do not add new fixes beyond what the reviewers identified. If you spot something, flag it in Section 6 (Open Questions) for the product owner.
- Do not change the DR curve, floor rules, CRITICAL assignments, or severity escalation guard. ADR-003 locked those.

## Tone

You are writing for a product owner who makes decisions, not a technical audience that implements them. Be direct. Use tables. State your recommendation clearly and explain why in 1-2 sentences. The product owner should be able to read Section 3 and say "go" without reading the rest.
