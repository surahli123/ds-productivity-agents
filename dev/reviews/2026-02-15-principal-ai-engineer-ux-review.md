# Principal AI Engineer Review: Emoji Dashboard UX Design

**Reviewer:** Principal AI Engineer (IC9)
**Date:** 2026-02-15
**Artifact:** `docs/plans/2026-02-15-emoji-dashboard-design.md`
**Scope:** Technical implementation concerns — prompt engineering, rendering, token handling, LLM reliability, accessibility

---

## Summary Verdict

**Approve with concerns.** The design is minimal, low-risk, and directionally correct — bolting emoji prefixes onto existing text labels is the right instinct. However, there are three issues that will cause real problems in practice: (1) the `⚠️` and `🔶` emojis are visually confusable in many terminal environments, which undermines the entire "instant visual scan" goal; (2) the prompt instructions in Step 10 don't give the LLM enough structural guidance to produce consistent emoji-rating pairings across runs; and (3) the design omits Quick mode and Draft mode emoji handling in the actual prompt, creating a spec-implementation gap.

---

## What Works Well

1. **Emoji-as-prefix, not replacement.** Keeping the text label (`CRITICAL`, `MAJOR`, etc.) alongside the emoji is the single most important design decision here. It means clipboard pasting, screen readers, and monochrome terminals all degrade gracefully. The emoji adds a visual channel without removing the textual one. This is exactly right.

2. **Scoped blast radius.** Only one file changes (`ds-review-lead.md`, Step 10 templates). No scoring math, no subagent prompts, no SKILL.md modifications. This means if the emoji instructions cause unexpected LLM behavior, you can revert a single file and lose nothing. The "bolt-on" framing is accurate and appropriate.

3. **Correct token impact estimate.** Emoji are typically 1-2 tokens in Claude's tokenizer. For a review that already runs 1,500-3,000 tokens of output, adding 15-20 emoji tokens is genuinely negligible — well under 1% of output token budget. This won't push any runs into degraded mode or affect latency.

---

## Concerns

### 1. Visual Confusability Between MAJOR (🔶) and MINOR (⚠️)

**Severity: MAJOR**

The core promise of this design is "instant visual scan" — but `🔶` (orange diamond) and `⚠️` (warning triangle) are dangerously similar in several rendering contexts:

- **macOS Terminal (default):** Both render as small orange/yellow shapes. At the 12-14px sizes typical in terminal output, the geometric distinction (diamond vs. triangle) is subtle. A user scanning a lens dashboard table will not reliably distinguish them at a glance.
- **GitHub markdown / rendered markdown:** Both appear yellow-orange. The distinction is slightly clearer than in terminal, but still requires deliberate inspection rather than enabling the "instant scan" the design promises.
- **Slack / Notion / Confluence:** Rendering varies by platform. Some platforms render `🔶` as a distinctly orange diamond, others as a yellow-orange shape that is very close to `⚠️`.
- **Colorblind users:** Both emojis rely on the yellow-orange spectrum. Users with protanopia or deuteranopia (red-green colorblindness, ~8% of males) may see them as nearly identical.

The design works at the extremes — `✅` (green check) and `❌` (red X) are universally distinct. The problem is in the middle two tiers, which is exactly where you need the most differentiation (a MAJOR issue needs meaningfully different urgency signaling than a MINOR one).

**Suggested fix:** Replace `🔶` MAJOR with `🟠` (orange circle) or, better yet, use a shape-based system that doesn't rely on color alone:
- `✅` SOUND (green check — universally clear)
- `⚠️` MINOR (yellow triangle — universally recognized as "caution")
- `🔴` MAJOR (red circle — clearly escalated from yellow)
- `❌` CRITICAL (red X — universally recognized as "stop/fail")

Alternatively, if you want to keep four visually distinct tiers without relying on red for two levels, consider: `✅` / `💛` / `🔶` / `❌`. The key constraint is: each tier must be distinguishable by *shape*, not just color.

### 2. Prompt Instructions Are Insufficiently Constraining for Consistent Emoji-Rating Pairing

**Severity: MAJOR**

The Step 10 prompt currently says:

> Prefix each Rating with its emoji: ✅ SOUND, ⚠️ MINOR ISSUES, 🔶 MAJOR ISSUES, ❌ CRITICAL.

This is a single inline instruction embedded within a larger output format description. In my experience with prompt engineering for structured output, this creates two reliability risks:

**Risk A — Omission drift.** When the LLM is generating a long structured output (the full review is 1,500-3,000 tokens), single-line formatting instructions embedded mid-template have a meaningful chance of being dropped, especially toward the end of generation. The emoji instructions appear once in the lens dashboard description and once in the finding format, but the LLM must apply them consistently across 8 dashboard rows and up to 10 finding headers. Without reinforcement, later findings may lose their emoji prefixes. This is the classic "instruction decay over long generation" problem.

**Risk B — Mapping confusion.** The prompt defines the emoji-rating mapping inline. If the LLM's training data includes other emoji-severity conventions (and it does — `⚠️` is commonly associated with warnings/errors, not "minor"), there's a non-trivial chance the LLM will map emojis incorrectly, especially `⚠️` for MINOR vs. `🔶` for MAJOR. The training distribution for `⚠️` skews toward "warning" (which semantically maps closer to MAJOR than MINOR), creating a subtle prior that works against the design's intended mapping.

**Suggested fix:** Add a dedicated lookup table to the prompt, separate from the template description, and reference it explicitly:

```
EMOJI SEVERITY MAP (use exactly as shown — do not substitute):
  ✅ = SOUND
  ⚠️ = MINOR ISSUES
  🔶 = MAJOR ISSUES
  ❌ = CRITICAL

Apply this map to: (1) every Rating cell in the Lens Dashboard,
(2) every finding header severity badge, (3) every Top 3 fix title.
```

Placing this as a standalone block before the output templates — rather than inline within them — gives it more salience and reduces the chance of mapping errors. Additionally, consider adding the mapping to the SKILL.md severity definitions table (Section 1) so that subagents also internalize the mapping, even though they don't directly produce the emoji output.

### 3. Spec-Implementation Gap: Quick Mode and Draft Mode Emoji Handling

**Severity: MINOR**

The design doc specifies:

> 1. Full mode — all 3 changes
> 2. Quick mode — Change 1 only (status table, not lens dashboard)
> 3. Draft mode — no changes

But examining the actual Step 10 prompt in `ds-review-lead.md`, the Quick Mode output template uses emoji in the Status table:

> Status — 2-row table: Dimension | Status (✅ Pass / ⚠️ Issues Found / ❌ Critical Issues)

This is a *different* emoji mapping than the 4-tier system used in Full mode. Quick mode uses a 3-tier system (Pass / Issues Found / Critical Issues) while Full mode uses 4-tier (SOUND / MINOR / MAJOR / CRITICAL). This is actually fine from a UX perspective — Quick mode is intentionally coarser — but the design doc doesn't document this divergence. Someone reading the design doc would expect Quick mode to use the same 4-tier mapping.

Additionally, the design doc says Quick mode gets "Change 1 only (status table, not lens dashboard)" — but it also says the Top 3 Priority Fixes use "same format" as Full mode. Does "same format" mean with emoji or without? The Step 10 prompt for Quick mode says `## Top 3 Priority Fixes (same format)` but doesn't explicitly state whether the emoji severity badges apply. The LLM will likely carry them forward from the Full mode template (since both are in the same prompt), but this is implicit rather than explicit.

**Suggested fix:** Update the design doc to explicitly document the Quick mode 3-tier mapping and confirm whether Top 3 fixes in Quick mode get emoji badges. This is a documentation gap, not a functionality gap, but it matters for maintainability when future contributors read the design doc.

### 4. Emoji Tokens in Score Parsing Edge Case

**Severity: MINOR**

The current output includes score math like:

> `Raw deductions: X → Effective (DR): Y | Credits: +Z | Score: W`

And finding headers like:

> `**Finding 1: Title** (CRITICAL, -15)`

The design adds emoji to the finding header:

> `**Finding 1: Title** (❌ CRITICAL, -15)`

If the lead agent's Step 9 synthesis logic ever re-parses its own output (or if downstream tooling parses the review output), the emoji tokens could interfere with regex-based extraction of severity labels and deduction values. Currently this isn't a problem because the lead agent computes scores before generating output, but it's worth noting for future-proofing.

More concretely: if you ever build automated tooling that parses review output (e.g., for calibration tracking, score aggregation, or regression testing), you'll need emoji-aware parsing. The pattern `(❌ CRITICAL, -15)` is slightly harder to regex than `(CRITICAL, -15)` because emoji have variable byte widths.

**Suggested fix:** No action required now, but add a note in the design doc: "Downstream parsers of review output should use severity text labels as anchors, not emoji characters, for extraction reliability."

### 5. Accessibility: Screen Reader Behavior with Emoji

**Severity: MINOR**

The design correctly keeps text labels alongside emoji, which is the most important accessibility decision. However, screen readers (VoiceOver on macOS, NVDA on Windows) will read emoji aloud:

- `❌ CRITICAL` reads as "cross mark CRITICAL"
- `✅ SOUND` reads as "check mark SOUND"
- `🔶 MAJOR ISSUES` reads as "large orange diamond MAJOR ISSUES"
- `⚠️ MINOR ISSUES` reads as "warning MINOR ISSUES"

The `🔶` readout ("large orange diamond") is non-semantic — it doesn't convey severity, just describes the glyph. Meanwhile `⚠️` reads as "warning," which actually sounds *more severe* than "large orange diamond," inverting the intended hierarchy for screen reader users. This reinforces Concern #1: the `⚠️`/`🔶` pairing has problems beyond visual confusability.

**Suggested fix:** If you adopt the alternative emoji mapping from Concern #1 (using `🔴` for MAJOR), screen readers would read "red circle MAJOR ISSUES" — which is semantically clearer. The general principle: choose emoji whose screen reader descriptions reinforce rather than contradict the severity hierarchy.

---

## Recommendations

1. **Swap the MAJOR emoji before shipping.** This is the highest-leverage change. Replace `🔶` with an emoji that is (a) visually distinct from `⚠️` across terminal, markdown, and collaboration tool renderers, and (b) semantically coherent when read aloud by a screen reader. `🔴` is my top recommendation; `🟠` is acceptable.

2. **Extract the emoji-severity mapping into a standalone prompt block.** Don't rely on inline mentions within template descriptions. A separate, clearly labeled lookup table placed before the output templates will significantly improve cross-run consistency. Consider also adding it to SKILL.md Section 1 as a non-functional annotation.

3. **Add a quick validation test.** After implementing, run the review 3 times on the same document and verify: (a) all 8 dashboard rows have the correct emoji, (b) all finding headers have emoji badges, (c) Top 3 fixes have emoji prefixes, (d) no emoji appear in Draft mode output. This is your regression test for instruction-following reliability.

4. **Document the Quick mode emoji divergence.** The 3-tier vs. 4-tier mapping difference is a conscious design choice — make it explicit in the design doc so it doesn't look like an oversight.

5. **Test in your primary consumption environments.** Render one emoji-enhanced review in (a) Claude Code terminal, (b) GitHub markdown preview, and (c) whatever tool your users paste reviews into (Confluence, Notion, Slack). Verify the MAJOR/MINOR distinction is visually clear in each. If it's not, that's your signal to change the emoji before it ships.
