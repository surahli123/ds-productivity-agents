# DS Lead Review: Emoji Dashboard UX Design

**Reviewer perspective:** DS Lead managing a team of 8 data scientists. Evaluating whether this design improves the practitioner experience and whether I would adopt this tool in my team's review workflow.

**Documents reviewed:**
- Design spec: `docs/plans/2026-02-15-emoji-dashboard-design.md`
- Updated lead agent: `plugin/agents/ds-review-lead.md` (Step 10 templates)
- Current output examples: Vanguard (score 72) and Rossmann (score 86) reviews

---

## Summary Verdict

**Approve with concerns.** The emoji bolt-on is a low-risk improvement that genuinely helps with visual scanning, but the design stops short of addressing the output issues that would actually change how my team uses the tool. The emojis solve the "visual hierarchy" problem as stated, but the stated problem is not the most important UX problem in this output.

---

## What Works Well

### 1. The 4-tier mapping is cognitively sound
The SOUND/MINOR/MAJOR/CRITICAL tiers map naturally to how data scientists triage review feedback. When I read a review of someone's work, my first question is "how bad is this?" — and the 4-tier split answers that faster than scanning text labels. The choice to differentiate MAJOR from CRITICAL with distinct icons (orange diamond vs red X) is correct. In my experience, the most common misunderstanding in code review and analysis review is conflating "this needs work" (MAJOR) with "this is fundamentally broken" (CRITICAL). The visual distinction reinforces the semantic distinction.

### 2. Emoji-prefix-not-replacement is the right call
Keeping the text label alongside the emoji is important for two practical reasons: (a) senior data scientists who find emoji patronizing will still see the text-based severity they expect, and (b) when review output gets pasted into Slack, Confluence comments, or Jira tickets, the text label survives formatting loss. This is a small decision that shows good design judgment.

### 3. Minimal blast radius
Confining changes to Step 10 output templates and leaving scoring math, section order, and pipeline logic untouched is the right approach for a bolt-on. I have seen too many "small UX improvements" that inadvertently change scoring behavior or introduce regressions. The explicit "What Does NOT Change" section in the design doc builds confidence.

---

## Concerns

### 1. The lens dashboard is not the primary scanning bottleneck (MAJOR)

**Explanation:** The design identifies "can't instantly see which areas are healthy vs problematic" as the problem, and the lens dashboard is the first thing it fixes. But looking at the Vanguard and Rossmann outputs, the lens dashboard is already the most scannable part of the review. It is an 8-row table with one-word ratings. A senior DS can parse it in under 5 seconds without emojis.

The actual scanning bottleneck is the per-dimension findings sections (Sections 8 and 9 in Step 10). In the Vanguard review, the Analysis Dimension section is 30+ lines of dense prose. In the Rossmann review, the Communication Dimension section runs even longer. When a DS gets this review, they need to answer: "Which findings do I need to act on, and in what order?" The emoji badges on finding headers help marginally, but the real issue is that every finding is a paragraph of text with no visual separation between the problem statement, the diagnosis, and the fix.

**Suggested fix:** Consider adding horizontal rules or a compact summary line (severity + lens + one-sentence issue) before the full finding detail. This would let a DS scan the findings list in 10 seconds and then drill into the ones that matter. The emoji on the finding header is a garnish on an unsolved layout problem.

### 2. Orange diamond (🔶) reads as "warning/danger" rather than "needs work" (MAJOR)

**Explanation:** The 🔶 emoji is visually alarming. On most platforms, it renders as a bright orange diamond that carries more urgency than the yellow warning triangle (⚠️). This creates a visual inversion: MINOR issues (⚠️) look like standard caution, while MAJOR issues (🔶) look like an emergency — closer in visual weight to the red X (❌) than intended.

In the DS mental model, MAJOR means "this weakens your analysis but doesn't break it." It is the most common severity in calibrated reviews (looking at the test results, most findings are MAJOR). If the most common severity looks alarming, the entire review will feel more punitive than intended. Junior DSs in particular will read a review with four 🔶 findings and feel like their work is failing, when the actual message is "solid foundation, specific things to address."

**Suggested fix:** Consider 🟡 (yellow circle) or 🟠 (orange circle) instead of 🔶. The circle is visually calmer and sits more naturally between ⚠️ and ❌ on the severity spectrum. Alternatively, test the rendering on the actual platforms your team uses (Slack, VS Code terminal, Confluence) — emojis render very differently across contexts and what looks balanced in a markdown preview may look unbalanced in a terminal.

### 3. Emojis may create false precision in the lens dashboard (MINOR)

**Explanation:** A lens rated "⚠️ MINOR ISSUES" in the dashboard could mean one trivial finding (-2 points) or two substantive findings (-5 each). The emoji flattens this into a single visual signal. When I look at the Vanguard dashboard, "Conciseness & Prioritization" is rated MINOR ISSUES — which could mean "move a data dictionary to the appendix" (trivial, 5 minutes) or "your entire prioritization structure needs rethinking" (significant, hours). The emoji makes both of these look identical.

This is less of a problem for CRITICAL and SOUND (those are binary — either it is fundamentally broken or it is not). But for MINOR and MAJOR, the emoji hides meaningful variance.

**Suggested fix:** This is not blocking, but consider whether the lens dashboard should show the deduction total alongside the rating: `⚠️ MINOR (-2)` vs `⚠️ MINOR (-8)`. This gives practitioners a second signal for effort estimation. If that feels too busy, accept the tradeoff — the finding details provide the nuance anyway.

### 4. The design does not address the "what do I do next?" workflow (MAJOR)

**Explanation:** When one of my data scientists gets a review back, their workflow is: (1) read the score and verdict to understand severity, (2) scan for critical/blocking items, (3) estimate total effort to address findings, (4) prioritize fixes into their current sprint or revision cycle. The emoji design helps with step 2 (visual scan for red X items) but does nothing for step 3 or 4.

The current output groups findings by dimension (Analysis, then Communication), which mirrors the reviewer's mental model, not the author's. An author revising their work thinks in terms of effort and location: "What can I fix in 5 minutes? What requires re-analysis? What needs a new section?" The design spec explicitly states section order does not change, but this is the UX improvement that would actually change adoption.

**Suggested fix:** This is out of scope for the emoji bolt-on (and correctly so — the design says no structural changes). But flag this as a v2 consideration: an optional "Revision Checklist" view that groups findings by estimated effort (quick fix / moderate rework / re-analysis needed) or by document location (ordered by where they appear in the author's document). This would be a mode toggle, not a replacement for the current structure.

### 5. No consideration for self-review vs peer-review vs lead-review contexts (MINOR)

**Explanation:** I would use this tool differently depending on context. When a junior DS runs a self-review before sharing their work, they want encouragement alongside critique — the emoji system is fine here. When I as a lead use the tool to pre-screen an analysis before a stakeholder presentation, I care most about CRITICALs and want to skip everything else — the emoji helps me scan but the output is still too long. When a peer reviews a colleague's work, the emoji severity badges might feel like a performance rating rather than collaborative feedback.

The design treats all review consumers identically. The current output already has mode toggles (full/quick/draft), but these affect depth, not tone or framing.

**Suggested fix:** Not blocking for this iteration. For v2, consider whether the output preamble or framing should adapt based on an optional `--context` flag (self-review, peer-review, lead-review). The emoji system itself does not need to change, but the surrounding language could soften ("areas to strengthen" vs "issues found") or sharpen ("blocking items for sign-off") depending on context.

---

## Recommendations

### Ship the emoji bolt-on as designed, with one change
Replace 🔶 with a less alarming MAJOR indicator. Test rendering on your actual output surfaces before committing. Everything else in the design is sound and low-risk.

### Prioritize finding-level scannability over dashboard prettiness
The emoji on the lens dashboard is the least impactful of the three changes. The emoji on finding headers (Change 2) is the most impactful because findings are where practitioners spend 80% of their reading time. If you had to ship only one change, ship Change 2.

### Track whether the emoji system changes perceived severity
After shipping, compare whether the same review content gets different reactions with and without emojis. Specifically: does a review with three 🔶 MAJOR findings feel more punitive than the same review with three text-only MAJOR findings? If your junior DSs start treating MAJOR as "my work is bad" rather than "my work needs specific improvements," the visual system is hurting more than helping.

### Plan the effort-based grouping as a v2 feature
The biggest gap in the current output is not visual hierarchy — it is actionability for the author. A "Revision Checklist" that groups findings by effort-to-fix and document location would be a bigger adoption driver than emojis. The emoji bolt-on is a fine v1 incremental improvement, but do not mistake it for the UX breakthrough that makes this tool indispensable for a DS team.

### Consider a compact summary mode for lead review
As a DS lead pre-screening work before a stakeholder meeting, I want: score, verdict, CRITICAL findings only, and the top 3 fixes. Everything else is noise for that use case. The current "quick mode" is close but still includes non-critical findings. A `--context lead-review` flag that filters to CRITICALs + top 3 would make me use this tool daily instead of occasionally.

---

*Review conducted from the perspective of a DS Lead evaluating tool adoption for a team of 8 data scientists. Focus areas: practitioner workflow, severity perception, and adoption barriers.*
