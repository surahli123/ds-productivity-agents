# search-ranking domain digest
# Version: 2026-02-21T14:00:00Z
# Previous: none
# Token budget: 8000
# Audience tags: all, ds, eng

---

## Foundational Knowledge [authority: authoritative] [audience: all]

This section covers the core evaluation standards, known pitfalls, and methodology that
anyone working in search ranking should know — DS, engineering, and PM alike. These are
established facts from peer-reviewed research and major benchmark evaluations. Contradicting
this content in an analysis review indicates a foundational knowledge gap.

### Evaluation Metrics

Three metrics dominate search ranking evaluation. Choosing the wrong one for your task is
a common analysis error.

**NDCG (Normalized Discounted Cumulative Gain)** is the standard metric for evaluating
ranked results with graded (multi-level) relevance judgments. It sums relevance scores at
each position with a logarithmic discount for lower positions, then normalizes by the ideal
ranking to produce a score between 0 and 1 (Järvelin & Kekäläinen, 2002).

- **When to use:** Ranking tasks where multiple documents can be relevant at different
  quality levels. Most common cutoff: NDCG@10. This is the default choice for web search,
  e-commerce search, and recommendation ranking where you care about the entire first page
  of results, not just the top result.
- **When NOT to use:** Single-answer retrieval (use MRR). Binary relevance without graded
  judgments (use Precision@k or MAP). If you only have relevant/not-relevant labels and no
  grade distinctions, NDCG still works but MAP may be simpler to interpret.
- **Common error:** Citing "industry standard NDCG of 0.90" — actual ranges for passage
  ranking are typically 0.40–0.70 depending on domain and query difficulty. An NDCG@10 of
  0.90 would be extraordinary and should be scrutinized for data leakage or overly easy
  evaluation queries.

**MRR (Mean Reciprocal Rank)** measures the average reciprocal rank of the first relevant
result across a query set. If the first relevant result is at position k, the reciprocal
rank for that query is 1/k. MRR was popularized in the TREC Question Answering track
(Voorhees, 1999) and became the primary metric for MS MARCO passage ranking.

- **When to use:** Question answering, known-item search, navigational queries — any task
  where only the position of the first relevant result matters. MRR is the right choice
  when the user's intent is to find *one* specific thing.
- **When NOT to use:** Multi-graded relevance tasks (use NDCG). Tasks where multiple
  relevant documents matter (use MAP or NDCG). MRR ignores everything beyond the first
  relevant result — a system that puts relevant results at positions 2, 3, and 4 but misses
  position 1 scores identically to a system that only has one relevant result at position 2.
- **Interpretation guide:** MRR@10 of 0.50 means the average first relevant result appears
  at rank 2. MRR@10 of 0.33 means rank 3 on average. MRR@10 of 0.184 (BM25 baseline on
  MS MARCO) means the average first relevant result is between rank 5 and 6.

**ERR (Expected Reciprocal Rank)** extends reciprocal rank to graded relevance with a
cascade user model: the user scans top-to-bottom and stops when satisfied. A highly
relevant document at position 1 discounts the contribution of everything below — unlike
NDCG, which treats positions independently (Chapelle et al., 2009).

- **When to use:** Web search ranking where satisfaction depends on finding one good result.
  Complement to NDCG when cascade-like browsing behavior is expected. ERR captures the
  intuition that a perfect result at position 1 makes the results at positions 2-10
  essentially irrelevant.
- **Key insight:** ERR correlates better with click-based metrics than NDCG does because
  it models the "satisfied user" stopping behavior that clicks actually reflect. If your
  evaluation is click-based, ERR may be more aligned with what you are measuring.
- **Practical note:** ERR is less commonly used as a primary metric than NDCG or MRR, but
  appears in TREC evaluations and is valuable as a complementary metric when you suspect
  cascade-like user behavior.

### Benchmark Ranges

These are the specific numbers a reviewer should know to sanity-check metric claims in
analyses. If someone reports a metric value outside these ranges without explanation, it
warrants investigation.

**MS MARCO passage ranking (dev set, MRR@10):**

| Model | MRR@10 | Year | Notes |
|---|---|---|---|
| BM25 (default, k1=0.9, b=0.4) | 0.184 | 2019 | Traditional baseline, no ML |
| BM25 (tuned for MRR, k1=0.60, b=0.62) | 0.189 | 2019 | Best BM25 variant |
| monoBERT (BERT-base re-ranker) | 0.347–0.376 | 2019–2020 | ~2x improvement over BM25 |
| ColBERT (late interaction) | 0.344–0.354 | 2020 | Dense retrieval, not re-ranking |
| monoT5 (T5-base re-ranker) | 0.380–0.388 | 2020–2021 | Pointwise T5 re-ranker |
| Top leaderboard (ensemble/LLM) | 0.40+ | 2022+ | Ensemble and large-model approaches |

*Source: Castorini/Anserini benchmark reproductions, MS MARCO leaderboard. Note: MS MARCO
uses MRR@10 as its primary metric because it has binary relevance labels, not graded
judgments. TREC Deep Learning Track uses NDCG@10 with graded relevance.*

**TREC Deep Learning Track (passage ranking, NDCG@10):**

| System Type | NDCG@10 Range | Track Year | Notes |
|---|---|---|---|
| BM25 baseline | ~0.51 (2019), ~0.28 (2023) | 2019–2023 | Varies significantly by query difficulty |
| Best traditional (non-neural) | ~0.49–0.56 | 2019–2023 | BM25 + query expansion (RM3) |
| Best neural (BERT/T5 re-rankers) | ~0.60–0.65 | 2019–2022 | Fine-tuned cross-encoders |
| Best LLM-based (GPT-4 prompting) | ~0.70 | 2023 | naverloo-rgpt4: 0.6994 |

*Source: TREC DL Track overview papers (2019–2023). The BM25 baseline varies substantially
across years because query sets change in difficulty — this is not a degradation of BM25
but a property of the evaluation setup.*

**Key interpretation for reviewers:** The jump from BM25 (0.184 MRR@10) to neural models
(0.35–0.39) is roughly 2x, which is the largest single improvement in the history of
passage ranking. Each subsequent generation (BERT→T5→LLM) adds only incremental gains but
at substantially higher computational cost.

### Position Bias

Clicks are **informative but biased** (Joachims et al., 2005, 2007). This is the single
most important pitfall in search relevance evaluation. Any analysis that uses click data
without addressing position bias has a foundational methodological flaw.

**Core findings from eye-tracking studies:**

- Users scan search results top-to-bottom with strong position bias in both eye fixations
  and clicks. Position 1 receives disproportionate attention regardless of result quality.
- A higher-ranked result gets more clicks even when a lower-ranked result is objectively
  more relevant. This is not just an attention effect — it reflects a systematic bias.
- When a relevant result was placed at position 2 (with a less relevant result at position
  1), subjects failed to click the more relevant link significantly more often
  (Fisher Exact Test, **p = 0.003**). This is direct evidence that position causally
  affects clicking behavior.
- **Trust bias:** Users tend to trust the search engine's ranking, clicking higher-ranked
  results even when they have examined lower results and could distinguish quality. This
  means position bias is not purely an examination effect — users actively defer to the
  ranking's implied authority.
- Absolute click rates are unreliable as relevance signals — but *relative preferences*
  derived from clicks (e.g., "user clicked result at position 3 but skipped position 2")
  are reasonably accurate on average.

**Position bias correction methods:**

- **IPW (Inverse Propensity Weighting):** Re-weights click signals by the inverse of
  examination probability at each position, compensating for lower examination rates at
  lower positions (Wang et al., 2016). Propensity is typically estimated via a
  randomization experiment — swapping pairs of results at adjacent positions and observing
  the change in click rates. The ratio of click rates at different positions estimates the
  relative examination probabilities.
- **Doubly-robust estimation:** Combines IPW with a relevance model (imputation) to reduce
  variance. The DR estimator requires "several orders of magnitude fewer datapoints to
  converge at optimal performance" compared to IPW alone (Oosterhuis, 2022). This is a
  major practical advantage for teams with limited traffic.

**Reviewer check:** Any analysis using click-through data without acknowledging position
bias should be flagged. The correction method matters less than whether bias was addressed
at all.

### Experiment Design for Search

Search ranking experiments have unique properties that make standard A/B testing practices
insufficient. Two key methods dominate.

**Interleaving** shows each user a blended ranking from both systems (control and
treatment), then uses a credit assignment function to determine which system the user
"preferred" based on their clicks. This within-subject design eliminates user-level
confounders because every user sees both systems.

- **10–100x more sensitive** than traditional A/B testing for detecting ranking quality
  differences. The sensitivity advantage comes from within-subject comparison: variance
  from user-level confounders is eliminated (Chapelle et al., 2012).
- Airbnb reports **50x speedup** over A/B testing: interleaving uses ~6% of A/B traffic
  and 1/3 of running length. Motivation: marketplace metrics (bookings) have low
  transaction frequency, making A/B tests prohibitively slow (ref: Zhang et al., 2022).
- Netflix uses a **two-stage approach:** fast interleaving to prune algorithm candidates
  in days, then traditional A/B test on the surviving candidates. This reduces total
  experiment duration and member exposure to suboptimal algorithms
  (ref: Netflix TechBlog, 2020).
- DoorDash reports **>100x sensitivity** over traditional A/B methods. Key confounder
  removed: user hunger level — presenting multiple rankers in the same context controls
  for time-varying satiety effects (ref: DoorDash Engineering).
- Thumbtack uses interleaving to accelerate ranking experimentation with similar
  sensitivity gains (ref: Zhao & Sathe, Thumbtack Engineering).

**A/B testing for search ranking:**

- **Minimum 4-week duration** for ranking changes that significantly alter user behavior.
  Two weeks risks capturing the novelty effect but not the steady-state behavior.
- **Novelty effect:** Engagement metrics (especially CTR) typically peak in the first few
  days after exposure to a new ranking, then decline as the novelty wears off. Tests
  stopped at 1–2 weeks may report inflated treatment effects that do not hold long-term.
- **Business cycle rule:** Run for at least 2 full business cycles, regardless of sample
  size. For most consumer products, this means 2–4 weeks.
- **Search-specific consideration:** Ranking changes can have delayed effects on user
  behavior — users adjust their search strategy over time (e.g., learning to add different
  query terms because the new ranking responds differently). This makes longer test
  durations particularly important for search versus other product surfaces.

### Learning to Rank: The Production Landscape

The evolution from traditional to neural ranking follows a clear pattern, and understanding
where your system sits on this spectrum is essential for identifying realistic improvements.

**LambdaMART** (gradient boosted trees with lambda-gradient optimization) remains the
dominant LTR approach in production systems due to interpretability, feature engineering
flexibility, and training speed (Burges, 2010). It won Track 1 of the Yahoo! Learning to
Rank Challenge (2010) and its variants (XGBoost, LightGBM) are used as Stage 1 rankers in
most multi-stage production systems. Key insight from the Challenge: the performance
advantage came from the expressiveness of boosted trees, not from the lambda-gradient idea
itself.

**The generational progression** BM25 → BERT → T5 → LLM represents roughly a 2x
improvement in effectiveness (MRR@10: 0.18 → 0.36 → 0.39 → 0.40+), but each step adds
significant latency and infrastructure complexity. This creates a fundamental trade-off
that every search team must navigate.

| Generation | Representative | MRR@10 (MS MARCO) | Latency Profile | Trade-off |
|---|---|---|---|---|
| Traditional | BM25 | 0.184 | Sub-millisecond | Fast, no training needed |
| LTR/GBDT | LambdaMART | ~0.30–0.35 | Sub-millisecond per candidate | Needs feature engineering, fast inference |
| Neural Stage 1 | BERT cross-encoder | 0.347–0.376 | ~50-100ms per batch | Expensive inference, ~95% gain over BM25 |
| Neural Stage 2 | monoT5 | 0.380–0.388 | ~100-200ms per batch | Higher quality, higher latency |
| LLM | GPT-4 prompting | 0.40+ | Seconds per query | Highest quality, highest cost, not yet production-viable at scale |

**Practical implication:** Most production systems use a multi-stage architecture where
cheaper models (BM25, GBDT) handle retrieval and first-pass ranking over the full candidate
set, and expensive neural models re-rank only the top-N candidates (typically 50–200). This
is not a temporary compromise — it is the established architecture pattern.

---

## Foundational Knowledge [authority: authoritative] [audience: ds]

DS-specific methodology: click models, statistical methods, and position bias correction
approaches that a data scientist working in search should master. This section assumes
familiarity with the concepts in the [audience: all] section above.

### Click Models

Click models are probabilistic models of user clicking behavior on search results. They
are essential for (1) training ranking models on implicit feedback and (2) understanding
what click data actually measures. The canonical survey is Chuklin, Markov, & de Rijke
(2015), *Click Models for Web Search*, covering all major models with their assumptions,
estimation procedures, and comparative evaluations.

**Position-Based Model (PBM):** A user clicks if they (1) examine the result and (2) find
it attractive. These two events are assumed independent. Examination of each result depends
*only* on its position, independent of all other results in the ranking:
`P(click) = P(examine | position) × P(attractive | query, document)`
(Richardson et al., 2007).

- **Best for:** Ads ranking (the original context for PBM), non-sequential layouts (grids,
  carousels), scenarios where results are relatively independent of each other. The
  independence assumption fits when users don't scan sequentially.
- **Limitation:** Cannot model sequential dependencies between results. If the user's
  decision to look at result 3 depends on what they saw at results 1 and 2, PBM misses
  this entirely.
- **Parameter estimation:** Typically via EM algorithm. Relatively few parameters, making
  it the simplest model to fit and a good baseline.

**Cascade Model:** Users scan results strictly top-to-bottom and leave as soon as they find
a satisfying result. A result at rank r ≥ 2 is examined if and only if the previous result
was examined AND not clicked (Craswell et al., 2008). Among the models tested in the
original paper, the cascade model best explained position bias in early ranks in web search.

- **Best for:** Navigational queries (user wants one specific answer), known-item search —
  any scenario with strict top-to-bottom scanning and a single target.
- **Limitation:** Can only describe sessions with a single click. Cannot model users who
  click and then continue browsing. Cannot explain non-linear browsing patterns (e.g.,
  skipping results based on snippet content).

**Dynamic Bayesian Network (DBN):** Extends the cascade model by adding a satisfaction
parameter — after clicking a result, the user may be satisfied (and stop) or unsatisfied
(and continue browsing). This introduces a satisfaction probability per query-document pair.
DBN achieves best performance with persistence parameter γ ≈ 0.9, indicating users are
persistent in finding relevant documents (Chapelle & Zhang, 2009).

- **Best for:** General web search (the most flexible of the three basic models),
  multi-click sessions, when satisfaction varies across results (some clicks lead to
  satisfaction, others don't). DBN should be the default choice when unsure.
- **Key result:** DBN outperforms both PBM and Cascade in predicting both click-through
  rate and actual relevance, making it the best general-purpose click model.

**Decision guide — which click model when:**

| Query Type | Recommended Model | Reasoning |
|---|---|---|
| Navigational (single answer) | Cascade | User stops after finding the answer; single-click |
| Informational (browse many) | DBN | User may click multiple results, satisfaction varies |
| Ads / non-sequential layout | PBM | Independence assumption fits non-linear browsing |
| General web search | DBN | Most flexible, handles multi-click sessions |
| Quick evaluation / baseline | PBM | Simplest to estimate, fewest parameters |
| Multi-click + sequential | DBN | Only model that handles satisfaction after clicking |

### Statistical Methods for Position Bias Correction

Two primary methods exist for correcting position bias in click data. The choice between
them depends on traffic volume and whether a relevance model is available.

**IPW vs. Doubly-Robust comparison:**

| Dimension | IPW | Doubly-Robust |
|---|---|---|
| **What it needs** | Randomization experiment for propensity estimation | Propensity estimates + a relevance model (imputation) |
| **Variance** | High with small data; degrades with inaccurate propensities | Orders of magnitude lower than IPW |
| **Convergence** | Requires large amounts of data for stable estimates | Converges at optimal performance with "several orders of magnitude fewer datapoints" (Oosterhuis, 2022) |
| **When to choose** | When no relevance model is available; when traffic is large enough for stable propensity estimates | When traffic is limited; when a reasonable relevance model exists |
| **Risk** | Unstable estimates with low traffic; propensity misspecification | Requires a relevance model — if both propensity and relevance model are wrong, can still be biased |

Key technical distinction: the doubly-robust estimator uses *expected treatment per rank*
instead of actual treatment — this is what gives it more robust unbiasedness conditions than
IPW alone (Oosterhuis, 2022). This is the first DR approach specifically designed for
position-bias in ranking.

**How propensity is estimated for IPW:** Typically via a randomization experiment — swap
pairs of results at adjacent positions and observe the change in click rates. The ratio of
click rates at different positions estimates the relative examination probabilities
(Wang et al., 2016; Ai et al., 2018).

### A/B Test Duration Considerations for Search

Search ranking A/B tests require longer durations than typical product experiments due to
several search-specific factors:

- **Minimum 4 weeks** for ranking changes that significantly alter user behavior. This is
  a consensus figure across multiple industry sources, not a conservative estimate.
- **Novelty effect:** Engagement metrics (especially CTR) peak in the first few days after
  exposure to a new ranking, then decline as novelty wears off. Tests stopped at 1–2 weeks
  may report inflated treatment effects. This is particularly dangerous for search because
  CTR is a commonly used proxy metric.
- **Business cycle rule:** Run for at least 2 full business cycles (typically 2–4 weeks for
  consumer products). Weekend vs. weekday search patterns can be dramatically different.
- **Search-specific delayed effects:** Ranking changes can alter user search strategy over
  time. Users learn that certain query formulations work better (or worse) with the new
  ranking and adapt. This adaptation takes weeks to stabilize, meaning early metric readings
  may not reflect steady-state behavior.
- **Reference:** Netflix's experimentation platform documentation discusses duration
  considerations including novelty effects (ref: Netflix TechBlog, 2016).

---

## Foundational Knowledge [authority: authoritative] [audience: eng]

Engineering-specific standards for search ranking infrastructure: latency budgets, serving
architecture, and multi-stage pipeline design. This section provides the performance
constraints that shape what is practically possible in production ranking systems.

### Serving Latency Budgets

Latency directly impacts user experience and conversion rates. These are published
production constraints from major search systems:

**Etsy:** The entire ranking pipeline — fetching ~300 features, scoring, and ranking — must
complete within **250ms end-to-end** (ref: Etsy Engineering, "Deep Learning for Search
Ranking at Etsy"). This covers everything from receiving the query to returning ranked
results. Etsy iterated for exactly one year before launching their first unified deep
learning ranking model that met this constraint.

This 250ms budget is representative of e-commerce search constraints. Exceeding it degrades
user experience (perceived slowness), increases abandonment rates, and reduces conversion.
The constraint means any model improvement must be evaluated not just on relevance metrics
but on whether it fits within the latency budget.

### Multi-Stage Architecture

The standard production pattern is a pipeline of increasingly expensive rankers. This is
not a design choice but an engineering necessity — no single model can be both
comprehensive enough to cover the full index and expressive enough to capture fine-grained
relevance, all within latency budget.

**Stage 0: Retrieval (Candidate Generation)**
- Methods: BM25, approximate nearest neighbor (ANN) search, embedding-based retrieval
- Operates over the full index (millions to billions of documents)
- Returns hundreds to low thousands of candidates
- Latency: sub-millisecond per candidate, ~10-50ms total

**Stage 1: First-Pass Ranking**
- Methods: LambdaMART / GBDT scoring with pre-computed features
- Operates on retrieved candidates (hundreds to low thousands)
- Sub-millisecond per candidate; total ~10-30ms for the batch
- This is where LambdaMART and its variants (XGBoost, LightGBM) dominate

**Stage 2: Re-Ranking**
- Methods: Neural re-ranker (BERT cross-encoder, monoT5, DNN)
- Operates on top-N from Stage 1 (typically 50–200 candidates)
- Higher latency per candidate (~1-10ms each); total ~50-200ms for the batch
- This is where neural models add the most value without blowing the latency budget

**LinkedIn example:** Multi-aspect First Pass Ranker using independent ML models per
aspect (relevance, timeliness, engagement). The re-architecture yielded latency
improvements of **~62ms (Android), ~34ms (iOS), ~30ms (web)** and reduced feature
development time from 6 weeks to 2 weeks. Additionally, time to build a new search entity
type dropped from 21 weeks to 1 week (ref: LinkedIn Engineering, 2022).

**Trade-off:** Each neural stage adds latency. Production systems balance effectiveness
gains against the 250ms-class end-to-end budget by limiting re-ranking to top-N candidates.
Increasing N improves potential relevance but risks latency regression — a common failure
mode in production.

---

## Workstream Standards [authority: authoritative] [audience: all]

Team decisions and production standards drawn from published engineering case studies.
These represent the kind of choices a ranking team makes and ratifies — architecture
decisions, methodology standards, and tooling choices. Real entries are cited from public
engineering blog posts; synthetic entries are labeled [DEMO] to demonstrate how internal
team decisions would be documented.

### Ranking Architecture Evolution

**Airbnb ranking progression** — rules → GBDT → DNN:

- Phase 1 (small marketplace): Rule-based ranking, no ML. Sufficient when inventory and
  query volume are low.
- Phase 2 (mid-size, 2015): GBDT model with hand-engineered features. First ML model
  launched when marketplace grew large enough to generate training data.
- Phase 3 (large, 2018): DNN with 2 hidden layers. Enabled by 10x increase in training
  data. At sufficient scale, the DNN with more data beat complex feature engineering.
- Key principle: **"Start simple."** Deep learning isn't always better right away. Feature
  engineering still matters at smaller scale, and GBDT with good features can outperform
  a DNN with poor data or insufficient volume (ref: Grbovic, 2019).
- Interpretability challenge was solved with "TopBot" — a tool comparing feature
  distributions of top-ranked vs. bottom-ranked listings, providing model understanding
  without sacrificing DNN expressiveness.

**Etsy GBDT → DNN transition:**

- GBDT delivered Etsy's first personalized search (a major win), but hit diminishing
  returns from additional feature engineering — the signal was in the model architecture,
  not more features.
- One-year iteration cycle from project start to production DNN launch.
- Hard constraint: **250ms end-to-end latency budget** for the full pipeline (feature
  fetch + scoring + ranking for ~300 features).
- Used TF Ranking (TensorFlow's LTR library) as the core framework.
- The GBDT → DNN transition pattern matches Airbnb's experience: traditional models first,
  DNN when you have enough data and have exhausted feature engineering (ref: Etsy Engineering).

### Multi-Aspect Ranking

**LinkedIn multi-aspect ranker:**

- Each search aspect (relevance, timeliness, engagement, etc.) is optimized through an
  independent ML model rather than one monolithic ranker. This decomposition enables
  parallel development and faster iteration.
- Developer productivity treated as a first-class team metric alongside relevance:
  feature development time reduced from **6 weeks → 2 weeks**; time to build a new search
  entity type reduced from **21 weeks → 1 week**.
- Latency improvements per platform: **~62ms (Android), ~34ms (iOS), ~30ms (web)**.
- The architectural lesson: decomposing the ranking problem into independent aspects pays
  off not just in model quality but in team velocity (ref: LinkedIn Engineering, 2022).

### Experimentation Methodology

**Interleaving as standard pre-A/B evaluation:**

- Airbnb adopted interleaving as the default first-stage evaluation technique before any
  A/B test. Every ranking change goes through interleaving first.
- 50x sensitivity improvement validated against traditional A/B outcomes — interleaving
  agrees with A/B results but reaches conclusions 50x faster.
- Uses only 6% of regular A/B traffic and 1/3 of running length.
- Motivation: Airbnb's conversion-focused metrics (bookings) have low transaction
  frequency, making A/B tests too slow for rapid iteration on ranking improvements.
- Position bias is minimized in interleaving because listings from control and treatment
  are ranked above each other ~50% of the time (coin flip per competitive pair)
  (ref: Zhang et al., 2022).

### [DEMO] Position Bias Correction Standard

[DEMO] **Team decision (2025-Q3):** Adopted doubly-robust estimation over IPW as the
standard position bias correction method for all ranking evaluations. Rationale: our
traffic volume is insufficient for stable IPW propensity estimates — variance was too high
for reliable evaluation on query segments with fewer than 10K impressions/week. Doubly-
robust converges with orders of magnitude fewer datapoints (per Oosterhuis, 2022). All new
ranking model evaluations must use the doubly-robust pipeline unless the experiment lead
documents a specific exception.

### [DEMO] Feature Store Migration

[DEMO] **Team decision (2025-Q4):** Migrated ranking feature serving from batch (daily
refreshed feature tables) to real-time feature store (streaming updates via Kafka →
feature store). Reduced feature freshness from 24 hours to <1 minute for time-sensitive
signals (listing availability, price changes, trending queries). A/B test showed +1.2%
NDCG@10 lift, concentrated in time-sensitive query segments (e.g., "available tonight,"
"new arrivals"). Non-time-sensitive segments showed no meaningful change, confirming the
improvement is from freshness, not feature store infrastructure.

### [DEMO] Evaluation Metric Standard

[DEMO] **Team decision (2025-Q2):** Adopted NDCG@10 as the primary offline evaluation
metric for all ranking models, replacing a mix of MRR@10, Precision@5, and recall@100 that
different sub-teams were using. Rationale: our search has graded relevance judgments
(4-level scale), making NDCG the natural choice. MRR is retained as a secondary metric for
navigational query segments only. All experiment reports must include NDCG@10 as the first
metric reported.

---

## Workstream Learnings [authority: advisory] [audience: ds]

Lessons from production experiments and post-mortems — the kind of hard-won knowledge that
doesn't appear in textbooks. Published results are cited; synthetic entries are labeled
[DEMO]. These carry advisory authority: they reflect what specific teams learned in specific
contexts. Your context may differ, but these patterns are worth knowing.

### Position Bias as the Highest-Impact DNN Improvement

Airbnb's "ABCs" framework (Architecture, Bias, Cold start) identified position bias
handling as one of their most significant DNN ranking improvements. The novel position bias
approach led to measurable gains, particularly for historically under-represented inventory
that suffered disproportionately from position bias — these items were rarely shown in top
positions, received fewer clicks, and were therefore further depressed by models trained on
biased click data. The feedback loop amplifies position bias into an inventory fairness
problem (ref: Haldar et al., KDD 2020).

**Takeaway:** When improving an existing DNN ranker, position bias correction should be
among the first interventions evaluated — it often yields larger gains than architecture
changes alone. It is also a fairness intervention: items stuck at low positions due to
historical bias get a fairer chance.

### Cold Start Requires Explicit Modeling

Airbnb found that cold start for new listings (items with no interaction history) requires
explicit modeling, not just more training data. New listings were systematically
disadvantaged by models trained on historical engagement data — they lacked the behavioral
signals (clicks, bookings, reviews) that the model relied on most heavily. Content features
alone were insufficient to compensate (ref: Haldar et al., KDD 2020).

**Takeaway:** Any ranking system with a meaningful new-item rate (marketplace, news,
job postings) should have a dedicated cold-start strategy. Common approaches include
exploration bonuses, content-based initial scoring, and separate cold-start models. Relying
solely on content features is insufficient when behavioral features dominate the model's
importance distribution.

### [DEMO] Embedding Retrieval Latency Regression

[DEMO] **Post-mortem (2025-Q4):** An A/B test of embedding-based retrieval (replacing
BM25 as the first-stage candidate generator) showed +2.1% NDCG@10 improvement in offline
evaluation, but p99 latency regressed by 40ms in production when the candidate set doubled
from 500 to 1,000. The embedding model retrieved a broader set of semantically similar
candidates (good for recall) but the downstream re-ranking stage couldn't process double
the candidates within the 250ms budget. The test was reverted after 10 days when the latency
SLA breach was flagged by the infrastructure team. Resolution: added index sharding to keep
candidate-set size constant (500) while improving recall within that budget, then
re-launched successfully with +1.8% NDCG@10 and no latency regression.

**Lesson:** Offline metric gains from retrieval changes must be validated against latency
SLAs before launch. Doubling candidate sets is a common failure mode — the improvement in
recall is real but the latency cost is often underestimated. Always measure end-to-end
latency, not just model latency.

### [DEMO] CTR Optimization Incident

[DEMO] **Post-mortem (2026-Q1):** Optimizing click-through rate (CTR) as the sole ranking
objective led to clickbait-style results surfacing in top positions — high CTR but low
dwell time and high pogo-sticking rate (user clicks, immediately returns to search, clicks
something else). The issue was caught 3 days into the A/B test when the dwell-time
guardrail metric dropped 8%. The CTR-optimized model had learned to rank results with
sensational titles and thumbnails above genuinely relevant results. Resolution: added
dwell-time as a secondary guard metric with a hard 5% regression threshold. Revised the
ranking objective to a weighted combination of CTR (40%) and satisfaction score (60%),
where satisfaction is proxied by dwell time > 30 seconds.

**Lesson:** Single-metric optimization in ranking is dangerous. Always define guard metrics
that capture dimensions the primary metric misses. CTR without a satisfaction check will
reliably surface clickbait. This is not a theoretical risk — it is one of the most common
failure modes in production ranking optimization.

---

## Conflicts

This section documents cases where workstream knowledge overrides foundational guidance.
Workstream takes precedence per the Knowledge Tier Precedence rules (SKILL.md Section 6),
because the team's direct experimental evidence is more informative for their specific
context than general principles. Conflicts are flagged here for review during the next
foundational refresh.

### [DEMO] Position Bias Correction Method Override

**CONFLICT:**

- **Foundational says:** "Use IPW for position bias correction" — clicks exhibit strong
  position bias that must be corrected via inverse propensity weighting (Joachims et al.,
  2007; Wang et al., 2016). This is the standard recommendation in the unbiased
  learning-to-rank literature.

- **Workstream post-mortem (2026-01) says:** "Our randomization design in interleaving
  experiments makes IPW unnecessary for evaluation." The team's experiment platform
  randomizes result positions for a holdout set, eliminating the need for post-hoc bias
  correction during evaluation. Because interleaving already controls for position (each
  system's results appear above each other ~50% of the time), adding IPW correction on top
  of interleaving evaluation is redundant and can introduce unnecessary variance.

- **Resolution:** Workstream takes precedence for evaluation use cases. IPW guidance applies
  to teams without position randomization but not to ours when evaluating via interleaving.
  IPW remains necessary for training-time click debiasing (where interleaving is not
  applicable). Flagged for foundational review — consider splitting the foundational
  guidance into evaluation vs. training contexts, as the position bias correction needs are
  fundamentally different.
