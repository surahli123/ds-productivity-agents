# Design: Emoji Dashboard Bolt-On

**Date:** 2026-02-15
**Status:** Approved
**Approach:** B (Emoji Bolt-On) — minimal changes, zero restructuring

## Problem

The review output lacks visual hierarchy:
1. Lens dashboard is all text — can't instantly see which areas are healthy vs problematic
2. Findings all look the same — a CRITICAL has the same visual weight as a MINOR

## Solution

Add emoji indicators to three locations in the output. No structural changes.

### 4-Tier Emoji Mapping

| Emoji | Rating | Meaning |
|---|---|---|
| ✅ | SOUND | No issues found |
| ⚠️ | MINOR | Minor polish items |
| 🔴 | MAJOR | Needs meaningful work |
| ❌ | CRITICAL | Invalidates or fundamentally undermines the analysis |

### Change 1: Lens Dashboard Table

Rating column gets emoji prefix:

```
| Dimension | Lens | Rating |
|---|---|---|
| Analysis | Methodology & Assumptions | ❌ CRITICAL |
| Analysis | Logic & Traceability | ⚠️ MINOR |
| Communication | Structure & TL;DR | ✅ SOUND |
```

### Change 2: Finding Severity Badges

Inline emoji before severity label in finding headers:

```
**Finding 1: Title** (❌ CRITICAL, -15)
**Finding 2: Title** (🔴 MAJOR, -10)
**Finding 3: Title** (⚠️ MINOR, -3)
```

### Change 3: Top 3 Fixes Headers

Emoji prefix on fix titles:

```
### 1. ❌ TL;DR completely absent (CRITICAL)
### 2. 🔴 Vague recommendation (MAJOR)
### 3. ⚠️ Data dictionary in main body (MINOR)
```

## What Does NOT Change

- Section order
- Section content / finding detail level
- Score math (DR, credits, floor rules)
- Metadata line
- Quick mode / draft mode formats
- Per-dimension section structure

## Implementation Scope

Only file affected: `plugin/agents/ds-review-lead.md` (Step 10 output templates).

Three output modes need updating:
1. Full mode — all 3 changes
2. Quick mode — Change 1 only (status table, not lens dashboard)
3. Draft mode — no changes (no numeric scores or lens dashboard)

## Token Impact

~1 emoji token per finding + 8 emoji tokens in dashboard = ~15-20 tokens added per review. Negligible.

## Design Decisions

- 4-tier over 3-tier: differentiating MAJOR (🔴) from CRITICAL (❌) was a stated pain point
- Emoji prefix, not replacement: keep the text label for accessibility and clipboard pasting
- No structural changes: saves implementation time and avoids pipeline risk
