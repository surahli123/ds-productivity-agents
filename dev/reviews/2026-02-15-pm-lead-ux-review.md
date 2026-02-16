# PM Lead Review: Emoji Dashboard UX Design

**Reviewer:** PM Lead
**Date:** 2026-02-15
**Artifact Reviewed:** `docs/plans/2026-02-15-emoji-dashboard-design.md`
**Verdict:** Approve with Concerns

---

## Summary Verdict

The emoji bolt-on is a sensible, low-risk starting point that addresses the stated pain points — but it only solves the *scanning* problem and leaves the deeper *reading experience* problem untouched. Approve for implementation as-is, but treat this as Phase 1 of a broader output UX pass rather than a complete solution.

---

## What Works Well

1. **Right instinct on the 4-tier mapping.** Differentiating MAJOR (🔶) from CRITICAL (❌) with distinct emoji is the single most impactful micro-decision in this design. In the current output, a CRITICAL and a MAJOR both render as plain text — "CRITICAL" vs "MAJOR ISSUES" — and the reader's eye treats them as equivalents. The orange diamond creates a visual middle band that communicates "needs work but isn't broken." This maps cleanly to how DS authors actually triage: red means stop, orange means fix before sharing, yellow means polish when you have time, green means move on. That mental model is intuitive without explanation.

2. **Emoji-as-prefix, not emoji-as-replacement.** Keeping the text label alongside the emoji preserves accessibility (screen readers, clipboard paste into Slack/Jira, terminal rendering) while adding the visual signal. This is the right tradeoff for a tool that runs in a CLI — you can't assume rich rendering. It also means the emoji degrades gracefully in environments that don't render Unicode well.

3. **Zero structural change keeps implementation risk near zero.** By scoping to three insertion points in Step 10 templates only, this change can ship in a single commit with no risk of breaking the 10-step pipeline, subagent dispatch, or scoring math. For a project in active calibration (R3 just landed, R4 pending), avoiding pipeline disruption is the right call.

---

## Concerns

### 1. The lens dashboard solves scanning, but not the "so now what?" flow (MAJOR)

**Severity:** MAJOR

**Explanation:** The design says users can "instantly see which areas are healthy vs problematic" once emoji appear in the lens dashboard. That's true — the dashboard becomes a scannable heat map. But scan-then-what? The current reading order is:

```
Score → Dashboard → Top 3 Fixes → What You Did Well → Analysis Details → Communication Details
```

After scanning the dashboard, a user who sees 🔶 on Actionability has to scroll past Top 3 Fixes (which may or may not include that lens), past What You Did Well, past the entire Analysis Dimension section, and finally into the Communication Dimension to find the Actionability findings. The dashboard creates a *promise* of quick navigation that the output structure doesn't deliver on.

**Suggested fix:** Consider adding lens anchors or a "jump to" hint in the dashboard. Even a simple parenthetical — `🔶 MAJOR ISSUES (see Finding 5)` — would connect the scan layer to the detail layer. This doesn't require structural changes; it's just a dashboard cell format update. Alternatively, note this as a known gap and address it in a Phase 2 output restructuring.

---

### 2. The verdict line has no emoji treatment, breaking the visual language (MAJOR)

**Severity:** MAJOR

**Explanation:** The design adds emoji to the dashboard, finding headers, and Top 3 fixes — but the single most important line in the entire output gets nothing:

```
**Score: 72/100 — Minor Fix**
```

This is the first thing the user reads. It sets the emotional frame for everything that follows. "Minor Fix" is one of three possible verdicts (Good to Go / Minor Fix / Major Rework), and each carries very different weight. Yet it renders identically to a bold text label. Meanwhile, the dashboard *below* it is getting full emoji treatment.

The hierarchy is inverted: the summary is plain, but the details are rich. That's backwards from how users actually process information — they need the strongest signal at the top, with decreasing visual intensity as they go deeper.

**Suggested fix:** Add emoji to the verdict line:

```
**Score: 72/100 — ⚠️ Minor Fix**
**Score: 86/100 — ✅ Good to Go**
**Score: 42/100 — ❌ Major Rework**
```

This is a one-line template change and reinforces the 3-tier verdict system with the same visual language the rest of the output already uses. Note: this reuses existing emoji from the 4-tier set (mapping 3 verdicts to 3 emoji: ✅/⚠️/❌), which keeps the visual language coherent without introducing new symbols.

---

### 3. "What You Did Well" is visually invisible in the current design (MINOR)

**Severity:** MINOR

**Explanation:** The design focuses entirely on the problem-oriented sections (dashboard ratings, finding severity badges, fix headers). The "What You Did Well" section — which is non-negotiable per the lead agent rules — gets zero visual treatment. In the current test outputs (Vanguard, Rossmann), it's a numbered list of bold titles with paragraph explanations, identical in visual weight to the findings sections above and below it.

This matters because the positives section serves a critical product function: it prevents the review from feeling purely punitive. If a DS author opens a review, sees a wall of red/orange emoji in the findings, and then hits a positives section that looks identical to the problems section, the emotional impact of the positives is muted. They don't *feel* like positives; they feel like more of the same.

**Suggested fix:** This doesn't need to be solved in this phase, but flag it for Phase 2. Options include: a simple ✅ prefix on each positive (mirroring the SOUND rating), a green header bar if rendering supports it, or even just a different heading level to create visual separation. The goal is a clear visual shift when the user transitions from "here's what to fix" to "here's what works."

---

### 4. Emoji fatigue risk in dense reviews (MINOR)

**Severity:** MINOR

**Explanation:** In a clean review (few findings, mostly SOUND lenses), the emoji treatment will feel balanced and helpful. But in a harsh review — say, 8+ findings with 2 CRITICAL and 4 MAJOR — the output will contain roughly 20+ emoji: 8 in the dashboard, 3 in Top 3 fixes, and 8-10 in finding headers. At that density, the visual signal-to-noise ratio starts to degrade. Every line screams for attention, and the user can't differentiate the most important emoji from the least important because they're everywhere.

Looking at the Vanguard test output: it had 8 findings. With emoji, that's 8 dashboard emoji + 3 fix emoji + 8 finding emoji = 19 emoji in a single review. The Rossmann review would have a similar count. For reviews that hit the 10-finding cap, you'd see 21+ emoji.

**Suggested fix:** This is likely acceptable for v1 — the alternative (selectively applying emoji) introduces complexity that contradicts the "bolt-on" philosophy. But monitor user feedback after implementation. If dense reviews feel noisy, consider suppressing emoji on individual findings within the per-dimension detail sections (keeping them only in the dashboard and Top 3 fixes, which are the primary scanning surfaces). The per-dimension sections are already the "detail layer" — users reading them have already committed to deep reading and don't need the same scanning affordance.

---

### 5. Quick mode emoji mapping doesn't align with full mode (MINOR)

**Severity:** MINOR

**Explanation:** The design specifies Quick mode gets "Change 1 only" — a 2-row status table with Pass/Issues Found/Critical Issues. But the full mode dashboard uses a 4-tier emoji system (✅/⚠️/🔶/❌), while the Quick mode status table compresses to 3 tiers (✅ Pass / ⚠️ Issues Found / ❌ Critical Issues). The 🔶 MAJOR tier disappears entirely in Quick mode.

This creates a subtle inconsistency: a user who runs Quick mode, sees "⚠️ Issues Found" on Analysis, and then re-runs in Full mode may be surprised to see "🔶 MAJOR ISSUES" on one lens and "⚠️ MINOR ISSUES" on another within that same dimension. The dimension-level summary in Quick mode collapses information that the lens-level dashboard in Full mode distinguishes.

**Suggested fix:** Accept this as an inherent tradeoff of Quick mode's compression — it's a summary, and summaries lose nuance. But consider documenting the mapping logic: Quick mode dimension status = worst lens rating within that dimension. If any lens is CRITICAL → ❌; if any is MAJOR → 🔶 (add the orange diamond to Quick mode too); if any is MINOR → ⚠️; otherwise → ✅. This preserves the 4-tier system across both modes.

---

## Recommendations

1. **Ship this as Phase 1, but name it that way.** Call this "UX Phase 1: Visual Scanning" in the backlog and CHANGELOG. It solves the scanning problem. Phase 2 should tackle the reading flow (navigation from dashboard to findings, positives section differentiation, potential output restructuring for progressive disclosure).

2. **Add verdict-line emoji before shipping.** This is a one-line change that completes the visual hierarchy. The verdict is the single most important output element — it shouldn't be the only element without visual treatment. This belongs in Phase 1, not Phase 2.

3. **Test with the Rossmann review.** The Rossmann review is the best test case because it has the widest spread: Analysis is 100/100 (all SOUND) while Communication has a CRITICAL and multiple MAJOR findings. The emoji dashboard should make this asymmetry instantly visible. If the dashboard doesn't make a user say "analysis is clean, communication needs work" within 2 seconds of seeing it, the design isn't working.

4. **Consider a lightweight Phase 2 scope.** Based on the concerns above, Phase 2 could include: (a) finding cross-references in dashboard cells, (b) positives section visual treatment, (c) optional emoji suppression in per-dimension detail sections if fatigue feedback emerges. These are all small changes that don't require pipeline work.

5. **Don't add the blockquote rewrite format in the same commit.** The session notes mention blockquote rewrites as part of the same UX sprint. Ship emoji separately — they're orthogonal changes, and bundling them makes it harder to isolate which UX change moved the needle on readability.
