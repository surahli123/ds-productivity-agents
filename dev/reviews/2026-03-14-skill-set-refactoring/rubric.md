# Calibration Rubric — Skill Set Refactoring Implementation Plan

## Context

This rubric evaluates an implementation plan for refactoring a DS Analysis Review agent system from a custom `agents/` + `shared/skills/` project structure into a proper Claude Code plugin skill set. The plan migrates ~2,800 lines of battle-tested content (4 calibration rounds) into a new directory structure without changing functional behavior.

## Target Ranges

| Dimension | Target Min | Target Max | Description |
|-----------|-----------|-----------|-------------|
| Completeness | 7 | 9 | Does the plan cover all migration steps without gaps? Are all files accounted for? Are edge cases (path references, naming collisions) addressed? |
| Clarity for Zero-Context Implementer | 7 | 9 | Could someone with no prior context follow this plan without guessing? Are exact file paths, commands, and expected outputs specified? |
| Risk Mitigation | 6 | 9 | Are verification steps adequate? Is there a rollback plan? Are the highest-risk steps (file deletion, path renaming) safeguarded? |
| Scope Discipline | 7 | 10 | Does the plan stay focused on restructuring without scope creep? Does it avoid unnecessary rewrites, feature additions, or premature optimization? |
| Feasibility | 7 | 9 | Is the plan realistic for one session? Are steps correctly ordered with dependencies respected? Are time estimates reasonable? |

## Scoring Guide

- **9-10:** Exceptional. No meaningful gaps. Ready to execute as-is.
- **7-8:** Strong. Minor issues that don't block execution. Fix before or during implementation.
- **5-6:** Adequate but needs work. Issues that could cause confusion or errors during implementation.
- **3-4:** Significant gaps. Major rework needed before this plan is executable.
- **1-2:** Fundamentally flawed. Needs complete redesign.

## Role-Specific Evaluation Notes

### DS Lead
In addition to the standard dimensions, evaluate:
- **Usefulness of the DS review agent after refactoring:** Will the plugin structure make the review agent more useful, more accessible, or more maintainable for a DS practitioner? Does the refactoring preserve the calibrated review quality? Are there risks to the scoring system's integrity?
- **Domain knowledge accessibility:** Is the search domain knowledge skill properly separated so it can be consumed by future agents (SQL review, metric analysis)?

### PM Lead
Focus on:
- Does this refactoring deliver user-facing value (portability, installability)?
- Is the scope realistic vs. ambitious? Are we over-engineering the migration?
- What's the cost-benefit of doing this now vs. building new features?

### Principal AI Engineer
Focus on:
- Is the plugin architecture sound? Does it follow established patterns (superpowers, kaizen)?
- Are there structural issues that will cause maintenance burden later?
- Is the path reference strategy robust or fragile?
