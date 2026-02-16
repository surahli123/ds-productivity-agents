# Synthesis: Final Implementation Spec

**Date:** 2026-02-15
**Author:** TPM Synthesis (Claude Code)
**Role:** Chief of Staff — synthesizing IC9 Architect, PM Lead, and DS Lead reviews
**Status:** All decisions made — ready for implementation
**Weighting note:** DS Lead opinions are weighted most heavily throughout. This is an internal DS productivity tool — the DS Lead understands the end user best.

---

## Section 1: Consensus Matrix

| Item | Web Session | IC9 Architect | PM Lead | DS Lead | Consensus |
|---|---|---|---|---|---|
| **Fix 1: Duplicate detection** | P0, SKILL.md §5 | Accept problem, redirect to lead Step 9 | Ship P0, redirect to Step 9, add partial-overlap guidance | Accept P0, question if prose changes agent behavior | **CONSENSUS: Ship P0.** All agree it's real and highest priority. Redirect to lead agent Step 9 (unanimous). |
| **Fix 2: Novel framework credit (+5)** | P1, SKILL.md §2b | Defer to v0.5 | Defer to v0.5 | Defer to v1.5 (scope creep from blog posts) | **CONSENSUS: Defer.** Unanimous. Exact version TBD (see Section 6). |
| **Fix 3: Worked example credit (+3)** | P1, SKILL.md §2b | Accept | Ship P1 | Accept P1 | **CONSENSUS: Ship P1.** Unanimous. |
| **Fix 4: Honest negative result (+3)** | P1, SKILL.md §2b | Accept | Ship P1 (rank above Fix 3) | Accept P1, note low firing rate | **CONSENSUS: Ship P1.** Unanimous. DS Lead + PM both value the behavioral incentive. |
| **Fix 5a: Formatting -5→-3** | P0 (bundled) | Accept | Ship P0 | Accept P1, challenge impact (+1-2 pts) | **MAJORITY: Ship.** IC9/PM say P0, DS Lead says P1. Call: P1 — DS Lead is right that +1-2 pts is cosmetic, not a scoring error. |
| **Fix 5b: Headings -3→-2, chart -3→-2** | P0 (bundled) | Downgrade to P1 | Ship when convenient | Accept P1, cosmetic | **CONSENSUS: Ship P1.** All agree trivial impact. Do not validate separately. |
| **Fix 6: Tighten quant results text** | P0 | Accept (documentation fix) | Ship P1 | Accept P1, agent already applies correctly | **CONSENSUS: Ship P1.** All agree it's a documentation fix with zero scoring impact. |
| **Self-deliberation fix** *(not in proposal)* | — | Flagged, should fix | P1, trust issue | **P0**, most important for user trust | **CALL: P0.** DS Lead's argument is decisive — a DS practitioner seeing the agent argue with itself will immediately distrust the tool. Trivial to fix, visible in production output. |
| **Extended validation** *(not in proposal)* | — | Mentioned briefly | Run after fixes, clean attribution | **P0**, run before more edits | **CONFLICT — see Section 2.** |
| **Cross-run consistency** *(not in proposal)* | — | Flagged variability concern | Proposed 3x Vanguard post-fix | Not explicitly addressed | **CALL: Include in validation plan.** Low cost, high information value. |

---

## Section 2: Conflict Resolution

### Conflict A: Fix 1 Implementation Location

**Web session says:** SKILL.md Section 5 (routing table instruction to subagents).
**IC9 says:** Lead agent Step 9 (synthesis step).
**DS Lead adds:** The routing table already says "Never report the same issue from both subagents" — and the agent ignores it.

**Resolution: IC9 is correct. Step 9 in ds-review-lead.md.**

This is a technical fact, not a judgment call. Subagents run in parallel via separate Task calls (Step 7). The communication-reviewer never sees the analysis-reviewer's findings. You cannot tell a subagent to suppress duplicates it can't see. The lead agent's synthesis step (Step 9) is the only place where both outputs are visible.

DS Lead's point strengthens this: the routing table already has anti-duplication prose that the agent ignores. Adding more prose to the same section won't help. Step 9 is structurally correct because it's where deduplication can actually happen.

**PM's partial-overlap guidance is adopted.** The 50% remediation overlap test ("if the same fix would address both findings, suppress the smaller deduction") gives the lead agent a concrete decision rule for ambiguous cases, not just exact duplicates. This matters for cases like "no limitations section" firing in both Audience Fit and Actionability.

### Conflict B: Fix 5a Priority (Formatting -5→-3)

**IC9/PM say:** P0 — disproportionate penalty, trust issue.
**DS Lead says:** P1 — cosmetic impact, +1-2 points after DR.

**Resolution: P1. DS Lead is right.**

The math is clear: formatting -5→-3 saves 2 raw points. After DR compression, that's ~1 point on the final score. Cross-run variability is ±10. This change is within noise. IC9 and PM are correct that -5 is disproportionate for a "polish issue" — but the impact on scores is negligible. Calling it P0 overstates its importance relative to Fix 1 and self-deliberation, which are the only two items that visibly change the user experience.

Ship it, but as P1 — meaning it goes in the same batch, just not called out as an active scoring error.

### Conflict C: Self-Deliberation Fix Priority

**IC9 says:** Should be fixed (no explicit priority).
**PM says:** P1, trust issue alongside credit additions.
**DS Lead says:** P0, more important for user trust than any of the 6 proposed fixes.

**Resolution: P0. DS Lead is decisive.**

The DS Lead's argument: "A user seeing an agent debate itself in the output will not trust any score it produces." This is the end-user perspective from the person who understands DS practitioners best. A review that contains "Hmm, I keep going back and forth. Let me commit..." is immediately disqualifying — a DS practitioner will dismiss the entire review.

The fix is one line in the communication-reviewer prompt. Zero scoring impact, zero calibration risk, immediate trust improvement. There is no reason to delay this.

PM's reasoning for P1 ("it's a polish fix, not a scoring error") is technically accurate but misses the point. DS Lead correctly identifies that this is a production readiness issue. A scoring error costs you 4 points. Visible self-deliberation costs you the user.

### Conflict D: Extended Validation Timing

**DS Lead says:** P0, run before more rubric edits. Risk of overfitting to 3 fixtures.
**PM says:** Run after fixes with clean attribution. Otherwise you run validation twice.

**Resolution: Ship fixes first, then validate. But honor DS Lead's overfitting concern with a specific safeguard.**

Reasoning:
1. The fixes address documented errors (duplicate counting is a real scoring bug, not fixture-specific tuning). Waiting to validate before fixing known bugs adds a round-trip for no information gain.
2. Running validation before AND after fixes doubles the work. PM's attribution concern is practical.
3. DS Lead's overfitting worry is valid but applies more to the *next* round of changes. These 7 fixes were identified through structural analysis (blog post calibration + rubric proportionality analysis), not by tuning to hit specific scores on 3 fixtures.

**Safeguard for DS Lead's concern:** After implementing fixes, run validation on the 3 new fixtures FIRST (before re-running Vanguard/Meta/Rossmann). If the new fixtures produce reasonable scores without further changes, that's the strongest evidence against overfitting. If they don't, stop and diagnose before tweaking further.

### Conflict E: Novel Framework Deferral Target

**IC9/PM say:** Defer to v0.5 (when genre detection exists or extended fixtures exercise it).
**DS Lead says:** Defer to v1.5 (scope creep, doesn't serve primary use case).

**Resolution: Defer to v0.5, with DS Lead's trigger condition.**

DS Lead is right that internal analyses rarely introduce novel frameworks. But the v0.5 extended validation may surface a fixture that does — the Airbnb FIV fixture uses propensity score matching in a novel way. IC9 and PM both said "revisit if extended fixtures exercise this credit."

Compromise: park it at v0.5 but it only gets implemented if (a) a test fixture naturally fires it AND (b) the criteria can be tightened to prevent inconsistent application. If neither condition is met by v0.5 completion, push to v1.5 per DS Lead.

---

## Section 3: Final Implementation Spec

### P0 Changes (ship now)

#### P0-1: Self-Deliberation Suppression

- **File:** `plugin/agents/communication-reviewer.md`
- **Location:** Add as Rule 12 (after existing Rule 11)
- **Add:**
```
12. **Single-pass evaluation.** Commit to each credit and finding decision on your first assessment. Do not deliberate, revise, or second-guess in your output. Internal reasoning should not be visible to the reader. If you are uncertain about a credit, award the lower value and move on.
```
- **Validation:** Re-run Rossmann review. Output should contain zero instances of "I keep going back," "let me commit," "actually, I think," or other deliberation language. Strength credit values may shift slightly — that's acceptable.

#### P0-2: Duplicate-Finding Detection (Lead Agent Step 9)

- **File:** `plugin/agents/ds-review-lead.md`
- **Location:** Step 9: Synthesize, add as item 8.5 (new item between existing items 8 and current final item)
- **Add after item 8 ("Cross-cutting issues..."):**
```
9. **Duplicate suppression:** Compare findings across both dimensions. When two findings share
   the same root cause — meaning the same fix would resolve both — apply the larger deduction
   only. Suppress the smaller finding and note it in the output as "subsumed by [dimension]
   finding [#X]." For partial overlaps where more than half of the remediation is shared, apply
   the same rule. When findings are genuinely independent (different root causes, different
   remediations), both stand.
   Example: "No statistical tests" fires as Analysis -10 and Communication -8. Root cause is
   identical (no tests were run). Keep the Analysis -10, suppress the Communication -8, note:
   "Communication Finding #6 subsumed by Analysis Finding #3 (same root cause: no statistical tests)."
```
- **Renumber** the existing final item in Step 9 from 8 to 10 (or whatever is needed to maintain sequential numbering — check the actual file).
- **Validation:** Re-run Vanguard review. The "no statistical tests" finding should appear in Analysis only, not duplicated in Communication. Vanguard score should increase by 2-5 points from R2 baseline of 69. Acceptable range: 69-76.

### P1 Changes (ship in same batch)

#### P1-1: Worked Example Credit (+3)

- **File:** `plugin/skills/ds-review-framework/SKILL.md`
- **Location:** Section 2b, Communication Dimension Credits table — add as new row after "Effective data visualization"
- **Add row:**

| Strength | Credit | Criteria |
|---|---|---|
| Effective worked example or scenario | +3 | Concrete numerical example or relatable scenario that makes an abstract methodology, framework, or finding tangible for the reader. Must walk through specific values, not just describe the approach generically. |

- **Validation:** Re-run Rossmann review. The revenue scenario table should earn this credit instead of stretching "data visualization." Net score impact: ~0 (credit moves from one category to another), but output becomes more accurate.

#### P1-2: Honest Negative/Null Result Credit (+3)

- **File:** `plugin/skills/ds-review-framework/SKILL.md`
- **Location:** Section 2b, Analysis Dimension Credits table — add as new row after "Sensitivity or robustness check"
- **Add row:**

| Strength | Credit | Criteria |
|---|---|---|
| Honest negative or null result reported | +3 | Reports a result that didn't work, an approach that failed, or an unexpected finding without spinning it as positive. Must be a substantive finding, not a throwaway mention. |

- **Validation:** Re-run Rossmann review. "Linear models performed worse than the average model" should earn +3. Net impact: +1-2 points after DR (this is a new credit, not a recategorization).

#### P1-3: Tighten "Reports Specific Quantitative Results" Credit

- **File:** `plugin/skills/ds-review-framework/SKILL.md`
- **Location:** Section 2b, Analysis Dimension Credits table — edit the existing "Reports specific quantitative results" row
- **Change criteria from:**
```
Actual numbers reported (not vague claims like "significant improvement")
```
- **To:**
```
Specific quantitative results with at least one contextualizing element: comparison to baseline, confidence interval, significance test, or benchmark. A bare number without context (e.g., "accuracy was 70%" with no comparison point) does not qualify.
```
- **Validation:** Re-run all 3 fixtures. Vanguard and Rossmann should still earn +3 (both already contextualize their numbers). Meta should still earn +0. Zero score change expected.

#### P1-4: Formatting Deduction -5→-3

- **File:** `plugin/skills/ds-review-framework/SKILL.md`
- **Location:** Section 2, Communication Dimension deductions table — edit "Sloppy formatting / inconsistent polish" row
- **Change:** `-5` → `-3`
- **Validation:** No separate validation. Impact is +1 point after DR on reviews where this fires. Within cross-run noise.

#### P1-5: Headings -3→-2, Unnecessary Chart -3→-2

- **File:** `plugin/skills/ds-review-framework/SKILL.md`
- **Location:** Section 2, Communication Dimension deductions table
- **Change:** "Generic/non-actionable headings" from `-3` to `-2`
- **Change:** "Unnecessary chart or table" from `-3` to `-2`
- **Validation:** No separate validation. Combined impact is <1 point after DR. Within cross-run noise.

---

## Section 4: Deferred Items

| Item | Deferred To | Reason | Trigger for Reconsideration |
|---|---|---|---|
| Novel framework credit (+5) | v0.5 | Evidence from blog posts, not internal analyses. Internal DS work rarely introduces novel frameworks. Subjectivity risk at +5 without validation fixtures. (DS Lead's reasoning is primary.) | Extended validation fixture naturally fires this credit AND criteria can be tightened for consistent application. If neither by v0.5, push to v1.5. |
| Communication dimension asymmetry (134 vs 101 deduction points) | v0.5 design | Structural issue, not fixable with point adjustments. MINOR reductions shave 4 points off 134 — doesn't close the gap. | Users consistently ask "why is my communication score so much lower?" — that's a product problem requiring design intervention (dimension weighting, steeper comm DR, or dimension-specific caps). |
| Finding volume cap (10 max) | Separate release | Already in backlog as P1. Interacts with these fixes (fewer findings = MINOR reductions matter even less, duplicate suppression fires less). | Ship separately to maintain clean attribution. If shipped simultaneously, widen validation acceptance ranges. |
| Audience-weighted dimension averaging | v1.5 | Architecture change. Current 50/50 weighting is correct for v1.0. | Enough user feedback data to design audience-specific weights. |

---

## Section 5: Implementation Order

### Batch 1: Prompt Fixes (no scoring impact, immediate trust improvement)

1. **Self-deliberation fix** → `communication-reviewer.md` Rule 12
   - One line addition. Zero scoring impact. Immediate output quality improvement.

### Batch 2: Scoring Fixes (all SKILL.md + lead agent edits)

2. **Duplicate detection** → `ds-review-lead.md` Step 9
   - This is the only P0 scoring fix. Implement before the others so its impact is identifiable in output.
3. **Formatting -5→-3** → `SKILL.md` Section 2
4. **Headings -3→-2, chart -3→-2** → `SKILL.md` Section 2
5. **Tighten quant results criteria** → `SKILL.md` Section 2b
6. **Worked example credit (+3)** → `SKILL.md` Section 2b
7. **Honest negative result credit (+3)** → `SKILL.md` Section 2b

### Batch 3: Validation

8. **Re-run Rossmann** — Primary check: self-deliberation gone from output, worked example credit properly categorized, honest negative result credit fires.
9. **Re-run Vanguard** — Primary check: duplicate suppression fires (score should increase 2-5 points), no self-deliberation artifacts.
10. **Re-run Meta** — Sanity check: score should stay in 50-58 range. None of these fixes should benefit a weak analysis.
11. **Cross-run consistency:** Run Vanguard 3x, verify scores within ±8 of each other.

### Batch 4: Extended Validation (new fixtures)

12. **Run Airbnb Message Intent** — Expected: Analysis 55-65, Communication 70-80.
13. **Run Airbnb FIV** — Expected: Analysis 65-75, Communication 70-80. Watch for novel framework credit opportunity.
14. **Run Netflix Proxy Metrics** — Expected: Analysis 60-70, Communication 65-75. Shorter article, may lack depth.
15. **Verify rank ordering across all 6 fixtures makes intuitive sense.** If any score feels clearly wrong, stop and diagnose.

### Ship vs. batch decision

All fixes ship as a single batch. Rationale:
- The fixes interact minimally (duplicate suppression is in the lead agent; all others are in SKILL.md credit/deduction tables).
- Shipping incrementally adds validation round-trips without information gain (the individual changes are too small to measure in isolation given ±10 cross-run variability).
- DS Lead's concern about overfitting is addressed by running new fixtures first in Batch 4 — if the system works on unseen content without further changes, overfitting is ruled out.

### Validation Acceptance Criteria

| Fixture | R2 Baseline | Post-Fix Range | Key Check |
|---|---|---|---|
| Vanguard | 69 | 69-76 | Duplicate suppression fires. No double-counted "statistical tests" finding. |
| Meta | 54 | 50-58 | Score does NOT increase meaningfully. Weak analysis stays low. |
| Rossmann | 71 | 71-77 | Self-deliberation gone. Worked example credit categorized correctly. |
| Rank order | Ross ≥ Van > Meta | Preserved | If this inverts, stop and investigate. |
| Differentiation | 15 pts (Van vs Meta) | ≥ 13 pts | Gap must remain meaningful. |
| Cross-run (Vanguard 3x) | — | Within ±8 | If wider, the fixes introduced new variance — investigate duplicate suppression consistency. |

---

## Section 6: Open Questions for Product Owner

### Q1: Novel framework deferral — v0.5 or v1.5?

IC9 and PM say v0.5 (revisit when extended fixtures exist). DS Lead says v1.5 (scope creep, doesn't serve primary use case).

**TPM recommendation:** v0.5 with a gate condition — only implement if a test fixture naturally fires it. If no fixture exercises it by v0.5, auto-push to v1.5.

**DECISION (owner):** Accepted v0.5-with-gate. If no fixture fires it by v0.5, auto-push to v1.5.

### Q2: Finding volume cap — same release or separate?

The existing backlog P1 item (cap findings at 10) interacts with these fixes. PM flagged: fewer findings means MINOR reductions matter even less, and duplicate suppression becomes less necessary if the cap naturally prevents some findings.

**TPM recommendation:** Ship separately. These fixes are well-scoped and the cap is a different kind of change (limits agent output volume vs. adjusting scoring weights). Mixing them makes attribution impossible.

**DECISION (owner):** Ship bundled. Accept that attribution will be harder — speed matters more here. Widen validation acceptance ranges accordingly.

### Q3: DS Lead's behavior concern — what if duplicate detection prose doesn't work?

DS Lead pointed out that the routing table already says "Never report the same issue from both subagents" and the agent ignores it. What if the new Step 9 dedup rule is also ignored?

**TPM recommendation:** Implement the Step 9 rule first and validate. If the lead agent still fails to suppress duplicates after the rule is in Step 9 (where it can actually see both outputs), then escalate to a structural fix — either post-processing logic or explicit finding-ID matching. But Step 9 is the right place to try first because the lead agent has the information it needs.

**DECISION (owner):** Accepted. Try Step 9 prose first, escalate to structural fix if it doesn't change behavior.

---

## Appendix: Reviewer Weight Rationale

This synthesis weighted DS Lead opinions most heavily for the following reason: the tool's end users are data scientists reviewing their own analyses. DS Lead understands what a DS practitioner expects from a review tool, what damages their trust, and which improvements matter vs. which are cosmetic. IC9 provides essential technical architecture guidance (Fix 1 redirect was critical). PM provides product framing and validation rigor. But when reviewers disagree on *user impact*, DS Lead's judgment takes precedence.

Specific instances where DS Lead's view prevailed:
- **Fix 5a priority:** DS Lead's P1 (cosmetic) overrode IC9/PM's P0 (disproportionate). The math supports DS Lead.
- **Self-deliberation priority:** DS Lead's P0 (production readiness) overrode PM's P1 (polish). The user impact argument is stronger.
- **Extended validation framing:** DS Lead's overfitting concern shaped the safeguard (run new fixtures first) even though the timing decision went with PM (fix first, validate after).
- **Fix 2 deferral reasoning:** DS Lead's "scope creep from blog posts" argument is the primary rationale, strengthened by IC9/PM's "wrong population" framing.
