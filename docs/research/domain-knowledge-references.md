# Domain Knowledge References

**Purpose:** Research backing for the domain knowledge digest files. Each entry includes
source, key finding, citation, and which digest section/tier it maps to. This document
feeds into the actual digest files (`plugin/digests/*.md`) during Layer 1 implementation.

**Organization:** Batches correspond to domains. Batch 1 covers Search Ranking (the
largest and template domain). Batches 2 and 3 cover Query Understanding and Cross-Domain.

**Authority tagging convention:**
- `[authority: authoritative]` = real paper, benchmark, or verified production blog post
- `[DEMO]` = synthetic workstream content (placeholders for team-specific knowledge)

**Audience tagging convention:**
- `[audience: all]` = relevant to both DS and engineering consumers
- `[audience: ds]` = primarily relevant to DS analysis and evaluation
- `[audience: eng]` = primarily relevant to engineering implementation

---

## Batch 1: Search Ranking

### 1. Evaluation Metrics

#### 1.1 NDCG (Normalized Discounted Cumulative Gain)

**Key paper:** Järvelin, K. & Kekäläinen, J. (2002). "Cumulated Gain-Based Evaluation of
IR Techniques." *ACM Transactions on Information Systems (TOIS)*, 20(4), 422–446.

**What it is:** NDCG is the standard metric for evaluating ranked retrieval results with
graded (multi-level) relevance judgments. It sums relevance scores at each position with
a logarithmic discount for lower positions, then normalizes by the ideal ranking to produce
a score between 0 and 1.

**When to use:** Ranking tasks where multiple documents can be relevant at different levels
of quality. The most common cutoff is NDCG@10 (top 10 results).

**When NOT to use:** Single-answer retrieval tasks (use MRR instead). Binary relevance tasks
where graded judgments are unavailable (Precision@k or MAP may suffice).

**Benchmark ranges (MS MARCO passage ranking, dev set, MRR@10):**

| Model | MRR@10 | Year | Notes |
|---|---|---|---|
| BM25 (default, k1=0.9, b=0.4) | 0.184 | 2019 | Traditional baseline |
| BM25 (tuned, k1=0.82, b=0.68) | 0.187 | 2019 | Optimized for recall@1000 |
| BM25 (tuned for MRR, k1=0.60, b=0.62) | 0.189 | 2019 | Best BM25 variant |
| monoBERT (BERT-base re-ranker) | 0.347–0.376 | 2019–2020 | ~2x improvement over BM25 |
| monoT5 (T5-base re-ranker) | 0.380–0.388 | 2020–2021 | Pointwise T5 re-ranker |
| ColBERT (late interaction) | 0.344–0.354 | 2020 | Dense retrieval, not re-ranking |
| Top leaderboard entries | 0.40+ | 2022+ | Ensemble and large-model approaches |

*Source: Castorini/Anserini benchmark reproductions, MS MARCO leaderboard.*
*Note: MS MARCO passage ranking uses MRR@10 as primary metric (binary relevance labels),
not NDCG@10. TREC Deep Learning Track uses NDCG@10 with graded relevance.*

**Benchmark ranges (TREC Deep Learning Track, passage ranking, NDCG@10):**

| System Type | NDCG@10 Range | Track Year | Notes |
|---|---|---|---|
| BM25 baseline | ~0.51 (2019), ~0.28 (2023) | 2019, 2023 | Varies by query set difficulty |
| Best traditional (non-neural) | ~0.49–0.56 | 2019–2023 | BM25 + query expansion (RM3) |
| Best neural (NNLM) | ~0.60–0.65 | 2019–2022 | BERT/T5-based re-rankers |
| Best LLM-based (prompt) | ~0.70 | 2023 | GPT-4 re-ranking (naverloo-rgpt4: 0.6994) |

*Source: TREC Deep Learning Track overview papers (2019–2023). TREC 2023: best passage
NDCG@10 = 0.6994 (h2oloo group using GPT-4 prompting), best traditional = 0.2825.*

**Key insight for digest:** A DS analyst citing "industry standard NDCG of 0.90" would be
flagged — actual ranges are domain-dependent but typically 0.40–0.70 for passage ranking.

**Digest mapping:** Foundational Knowledge > Evaluation Standards [authority: authoritative] [audience: all]

---

#### 1.2 MRR (Mean Reciprocal Rank)

**Definition:** MRR measures the average of reciprocal ranks of the first relevant result
across a set of queries. If the first relevant result is at position k, the reciprocal rank
for that query is 1/k.

**When to use:**
- Question answering tasks (single correct answer expected)
- Known-item search (user is looking for one specific thing)
- Navigational queries
- Any task where only the position of the first relevant result matters

**When NOT to use:**
- Multi-graded relevance tasks (use NDCG)
- When multiple relevant documents matter (use MAP, NDCG)
- MRR ignores all results beyond the first relevant one

**Key reference:** Voorhees, E. M. (1999). "The TREC-8 Question Answering Track Report."
*Proceedings of TREC-8.* (MRR was popularized in the QA track evaluation.)

**Benchmark range:** MS MARCO passage ranking uses MRR@10. BM25 baseline: 0.184–0.189.
State-of-the-art neural models: 0.38–0.40+.

**Digest mapping:** Foundational Knowledge > Evaluation Standards [authority: authoritative] [audience: all]

---

#### 1.3 ERR (Expected Reciprocal Rank)

**Key paper:** Chapelle, O., Metzler, D., Zhang, Y., & Grinspan, P. (2009). "Expected
Reciprocal Rank for Graded Relevance." *Proceedings of the 18th ACM Conference on
Information and Knowledge Management (CIKM 2009)*, Hong Kong.

**What it is:** ERR extends reciprocal rank to handle graded relevance. It models a
"cascade" user browsing pattern: the user scans results top-to-bottom and stops when
satisfied. The probability of stopping depends on the relevance grade of each document.
This means a highly relevant document at position 1 discounts the contribution of all
subsequent documents — unlike NDCG, which treats each position independently.

**When to use:**
- Web search ranking where user satisfaction depends on finding one good result
- Tasks where the value of lower-ranked results depends on what appeared above them
- Complement to NDCG when cascade-like behavior is expected

**Key insight:** ERR correlates better with click-based metrics than NDCG does, because it
models the "satisfied user" stopping behavior that clicks actually reflect.

**Digest mapping:** Foundational Knowledge > Evaluation Standards [authority: authoritative] [audience: ds]

---

### 2. Position Bias

#### 2.1 Foundational Studies: Eye-Tracking Evidence

**Key paper 1:** Joachims, T., Granka, L., Pan, B., Hembrooke, H., & Gay, G. (2005).
"Accurately Interpreting Clickthrough Data as Implicit Feedback." *Proceedings of ACM
SIGIR 2005.*

**Key paper 2:** Joachims, T., Granka, L., Pan, B., Hembrooke, H., Radlinski, F., & Gay, G.
(2007). "Evaluating the Accuracy of Implicit Feedback from Clicks and Query Reformulations
in Web Search." *ACM Transactions on Information Systems (TOIS)*, 25(2).

**Key findings:**
- Users scan search results top-to-bottom with strong position bias in both eye fixations
  and clicks
- Clicks are *informative but biased*: a higher-ranked result gets more clicks even when
  a lower-ranked result is objectively more relevant
- When a relevant result was placed in position 2 (with a less relevant result in position 1),
  subjects failed to click the more relevant link significantly more often (Fisher Exact
  Test, p = 0.003)
- Absolute click rates are unreliable as relevance signals — but *relative preferences*
  derived from clicks (e.g., "user clicked result at position 3 but skipped result at
  position 2") are reasonably accurate on average
- The "trust bias" effect: users tend to trust the search engine's ranking, clicking
  higher-ranked results even when they have examined and could distinguish quality

**Why it matters for DS review:** Any analysis using click-through data without acknowledging
position bias has a foundational flaw. This is the single most important pitfall in search
relevance evaluation.

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: all]

---

#### 2.2 IPW (Inverse Propensity Weighting) for Ranking

**Key paper:** Wang, X., Bendersky, M., Metzler, D., & Najork, M. (2016). "Learning to
Rank with Selection Bias in Personal Search." *Proceedings of ACM SIGIR 2016.*

**Related work:** Ai, Q., Bi, K., Luo, C., Guo, J., & Croft, W. B. (2018). "Unbiased
Learning to Rank with Unbiased Propensity Estimation." *Proceedings of ACM SIGIR 2018.*

**Method:** Estimate the probability of a user examining a result at each position
(the "propensity"), then re-weight click signals by the inverse of this propensity.
Results in lower positions get higher weight to compensate for lower examination rates.

**How propensity is estimated:** Typically via a *randomization experiment* — swap pairs
of results at adjacent positions and observe the change in click rates. The ratio of
click rates at different positions estimates the relative examination probabilities.

**When to use:**
- Training ranking models on click data (unbiased learning-to-rank)
- Evaluating ranking quality from logged click data
- When randomization experiments are feasible to estimate propensities

**When NOT to use:**
- When propensity estimates are inaccurate (high-variance, small data)
- When the examination model doesn't hold (e.g., visual layout effects, not just position)
- When a simpler approach (randomized evaluation) is available

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: all]

---

#### 2.3 Doubly Robust Estimation for Ranking

**Key paper:** Oosterhuis, H. (2022/2023). "Doubly-Robust Estimation for Correcting
Position-Bias in Click Feedback for Unbiased Learning to Rank." *ACM Transactions on
Information Systems*, 41(3). (arXiv: 2203.17118, March 2022; published 2023.)

**What it adds over IPW:**
- Combines IPW with a relevance model (imputation) to reduce variance
- First DR approach specifically designed for position-bias in ranking
- Uses *expected treatment per rank* instead of actual treatment, which existing DR
  estimators use — this is a key technical distinction
- More robust unbiasedness conditions than IPW alone

**Key result:** The DR estimator requires "several orders of magnitude fewer datapoints to
converge at optimal performance" compared to IPW alone. This is a major practical advantage
for teams with limited traffic.

**When to use:**
- When IPW estimates have high variance (low-traffic scenarios)
- When you have a reasonable relevance model to serve as the imputation component
- When position bias correction needs to be maximally data-efficient

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: ds]

---

#### 2.4 Position Bias in Production (Industry)

**Airbnb — Position Bias Correction in Search:**

Haldar, M., Abdool, M., et al. (2020). "Improving Deep Learning for Airbnb Search."
*Proceedings of KDD 2020.*

- Airbnb addressed position bias as one of the "ABCs" of improving their DNN ranking
  model (Architecture, Bias, Cold start)
- Position bias was identified as one of the most significant challenges for their deep
  neural network ranker, particularly affecting historically under-represented inventory
- The paper describes a novel position bias handling approach that led to significant
  improvements in ranking quality for difficult-to-rank inventory

**Airbnb — Interleaving as Position Bias Mitigation:**

Zhang, Q. et al. (2022). "Beyond A/B Test: Speeding up Airbnb Search Ranking
Experimentation through Interleaving." *Airbnb Tech Blog.*

- Position bias is minimized in interleaving because listings from control/treatment
  are ranked above each other ~50% of the time (coin flip per competitive pair)
- Achieves 50x speedup over A/B testing while controlling for position effects

**Comprehensive Review:**

Yates, A. "An Unusually Comprehensive Review of Position Bias Correction Methods in
Search and Ads Ranking." *Medium (Promoted).*

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: all]

---

### 3. Click Models

#### 3.1 Survey Reference

**Key reference:** Chuklin, A., Markov, I., & de Rijke, M. (2015). *Click Models for Web
Search.* Morgan & Claypool Publishers. (Synthesis Lectures on Information Concepts,
Retrieval, and Services.)

This is the canonical survey of click models for web search. It covers all major models
(PBM, Cascade, DBN, UBM, CCM, and variants) with their assumptions, estimation procedures,
and comparative evaluations. Available at: https://clickmodels.weebly.com/

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

#### 3.2 Position-Based Model (PBM)

**Key paper:** Richardson, M., Dominowska, E., & Ragno, R. (2007). "Predicting Clicks:
Estimating the Click-Through Rate for New Ads." *Proceedings of the 16th International
Conference on World Wide Web (WWW 2007)*, 521–530.

**Core assumption (Examination Hypothesis):** A user clicks on a result if and only if they
(1) examine it AND (2) find it attractive. These two events are independent:
`P(click) = P(examine) × P(attractive)`.

**Key characteristic:** Examination of each result is independent of all other results in
the ranking. The examination probability depends only on position.

**When appropriate:**
- Ads ranking (the original context)
- Scenarios where user browsing is non-sequential (e.g., visual layouts, grid displays)
- When results are relatively independent of each other

**Limitations:**
- Cannot model sequential dependencies between results
- Assumes examination is purely position-based (ignores content above)

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

#### 3.3 Cascade Model

**Key paper:** Craswell, N., Zoeter, O., Taylor, M., & Ramsey, B. (2008). "An Experimental
Comparison of Click Position-Bias Models." *Proceedings of the 1st ACM International
Conference on Web Search and Data Mining (WSDM 2008).*

**Core assumption (Cascade Hypothesis):** Users scan results strictly top-to-bottom and
leave as soon as they find a satisfying result. A result at rank r >= 2 is examined if
and only if the previous result was examined AND not clicked.

**Key finding:** Among the models tested, the cascade model best explained position bias
in early ranks in a web search setting.

**When appropriate:**
- Navigational queries (user wants one specific answer)
- Known-item search
- Any scenario where users exhibit strict top-to-bottom scanning

**Limitations:**
- Can only describe sessions with a single click
- Cannot model users who continue browsing after clicking
- Cannot explain non-linear browsing patterns (e.g., skipping results)

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

#### 3.4 Dynamic Bayesian Network (DBN)

**Key paper:** Chapelle, O. & Zhang, Y. (2009). "A Dynamic Bayesian Network Click Model
for Web Search Ranking." *Proceedings of the 18th International Conference on World Wide
Web (WWW 2009).*

**Core contribution:** Extends the cascade model to handle user satisfaction after clicking.
After clicking a result, the user may be satisfied (and stop) or unsatisfied (and continue
browsing). This introduces a "satisfaction" parameter per query-document pair.

**Key result:** DBN outperforms other click models (including PBM and Cascade) in predicting
both click-through rate and actual relevance. The model achieves best performance with a
persistence parameter γ ≈ 0.9, indicating users are persistent in finding relevant documents.

**When appropriate:**
- General web search (the most flexible of the three basic models)
- When users may click multiple results per query
- When satisfaction varies across results (some clicks lead to satisfaction, others don't)

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

#### 3.5 Which Click Model When? (Decision Guide)

| Query Type | Recommended Model | Reasoning |
|---|---|---|
| Navigational (single answer) | Cascade Model | User stops after finding the answer |
| Informational (browse many) | DBN | User may click multiple results, satisfaction varies |
| Ads / non-sequential layout | PBM | Independence assumption fits non-linear browsing |
| General web search | DBN | Most flexible, handles multi-click sessions |
| Quick evaluation / baseline | PBM | Simplest to estimate, fewest parameters |

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

### 4. Learning to Rank (LTR)

#### 4.1 LambdaMART

**Key paper:** Burges, C. J. C. (2010). "From RankNet to LambdaRank to LambdaMART: An
Overview." *Microsoft Research Technical Report MSR-TR-2010-82.*

**Related:** Burges, C. J. C. et al. (2011). "Learning to Rank Using an Ensemble of
Lambda-Gradient Models." *Proceedings of the Yahoo! Learning to Rank Challenge (JMLR
Workshop and Conference Proceedings, Vol. 14).*

**What it is:** LambdaMART combines the LambdaRank gradient idea with gradient boosted
decision trees (MART/GBDT). Instead of optimizing a differentiable surrogate loss,
LambdaRank directly defines gradients that approximate optimizing NDCG or ERR.

**Benchmark results:**
- Won Track 1 of the Yahoo! Learning to Rank Challenge (2010)
- The winning system used 12 models: 8 bagged LambdaMART, 2 LambdaRank neural nets,
  2 MART logistic regression
- NDCG@1 on MQ2007: 0.4200 (with bagging), vs. prior best of 0.4134 (RankBoost)
- Key insight from the Challenge: the performance advantage of LambdaMART came from the
  expressiveness of boosted trees, not from the lambda-gradient idea itself

**Production relevance:**
- LambdaMART (and GBDT variants like XGBoost, LightGBM) remains the dominant LTR approach
  in production systems due to interpretability, feature engineering flexibility, and
  training speed
- Often serves as Stage 1 ranker in multi-stage systems, with neural re-rankers in Stage 2

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

#### 4.2 Neural Ranking Models (BERT, ColBERT, T5)

**BERT re-ranking:**

Nogueira, R. & Cho, K. (2019). "Passage Re-ranking with BERT." *arXiv: 1901.04085.*

- First application of BERT to passage re-ranking on MS MARCO
- MRR@10: ~0.358 (BERT-base), vs. BM25 baseline of ~0.184 — a ~95% relative improvement
- Became the top entry on the MS MARCO leaderboard, outperforming previous state of the
  art by 27% in MRR@10
- Cross-encoder approach: query and passage are concatenated and fed through BERT jointly

**ColBERT (late interaction):**

Khattab, O. & Zaharia, M. (2020). "ColBERT: Efficient and Effective Passage Search via
Contextualized Late Interaction over BERT." *Proceedings of ACM SIGIR 2020.*

- Late interaction: encode query and document separately, then compute fine-grained
  similarity via MaxSim operation over token embeddings
- MRR@10 on MS MARCO: ~0.349 (ColBERTv1), competitive with cross-encoders but much faster
  at inference (amenable to vector index pre-computation)
- ColBERTv2 (Santhanam et al., NAACL 2022): improved with residual compression, negligible
  loss in MRR (<0.1%)

**monoT5:**

Nogueira, R., Jiang, Z., Pradeep, R., & Lin, J. (2020). "Document Ranking with a
Pretrained Sequence-to-Sequence Model." *arXiv: 2003.06713.*

- T5-based pointwise re-ranker; generates "true" or "false" for each query-document pair
- monoT5-base MRR@10 on MS MARCO: ~0.380–0.388 (entire dev set)

**LLM-based re-ranking (2023+):**

- TREC 2023 Deep Learning Track: GPT-4 prompting achieved NDCG@10 of 0.6994, surpassing
  the best neural language model (NNLM) approach at ~0.597 — a ~17% improvement
- This represents a paradigm shift: LLM-based ranking via prompting outperformed fine-tuned
  models for the first time in a major benchmark

**Key insight for digest:** The progression BM25 → BERT → T5 → LLM represents roughly
a 2x improvement in effectiveness (MRR@10: 0.18 → 0.36 → 0.39 → 0.40+), but each
step adds significant latency and infrastructure complexity.

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

#### 4.3 LTR in Production (Industry Blog Posts)

**Airbnb — ML-Powered Search Ranking (Experiences):**

Grbovic, M. (2019). "Machine Learning-Powered Search Ranking of Airbnb Experiences."
*Airbnb Tech Blog.*

- Describes three phases of ML ranking at different marketplace sizes:
  - Small marketplace: rule-based ranking
  - Mid-size: GBDT model (launched mid-2015)
  - Large: DNN with 2 hidden layers (launched 2018)
- Key lesson: "start simple" — deep learning isn't always better than traditional models
  right away; feature engineering still matters
- At scale, Airbnb deprecated complexity by scaling training data 10x and moving to a DNN
- Interpretability challenge solved with "TopBot" — comparing feature distributions of
  top-ranked vs. bottom-ranked listings

**Airbnb — Improving Deep Learning for Search (KDD 2020):**

Haldar, M. et al. (2020). "Improving Deep Learning for Airbnb Search." *KDD 2020.*

- The "ABCs" framework: Architecture, Bias (position bias), Cold start
- Novel position bias handling approach yielded one of their most significant ranking
  improvements
- Cold start for new listings addressed as a distinct modeling challenge

**Etsy — Deep Learning for Search Ranking:**

Etsy Engineering. "Deep Learning for Search Ranking at Etsy." *Code as Craft Blog.*

- Transitioned from GBDT (which delivered first personalized search) to DNN after
  hitting diminishing returns from feature engineering
- Used TF Ranking (TensorFlow's LTR library) at the core
- Latency constraint: entire pipeline (fetch ~300 features, score, rank) must complete
  within 250ms
- Iterated for exactly one year before launching first unified deep learning ranking model

**Etsy — LLMs for Search Relevance:**

Etsy Engineering. "How Etsy Uses LLMs to Improve Search Relevance." *Code as Craft Blog.*

- Recent post describing how Etsy leverages LLMs in their search relevance pipeline
- Shows the progression from traditional LTR → DNN → LLM augmentation

**LinkedIn — Improving Post Search:**

LinkedIn Engineering. (2022). "Improving Post Search at LinkedIn." *LinkedIn Engineering Blog.*

- Multi-aspect First Pass Ranker: each aspect optimized through an independent ML model
- Re-architecture reduced feature development time from 6 weeks to 2 weeks
- Latency improvements: ~62ms (Android), ~34ms (iOS), ~30ms (web)
- Reduced time to build new search entity type from 21 weeks to 1 week

**Digest mapping:** Workstream tier (Standards) [authority: authoritative] [audience: all]
*Note: These are public engineering blog posts, not synthetic team content. They serve as
authoritative references for production LTR approaches.*

---

### 5. Experiment Design for Search

#### 5.1 Interleaving Experiments

**Key paper:** Chapelle, O., Joachims, T., Radlinski, F., & Yue, Y. (2012). "Large-Scale
Validation and Analysis of Interleaved Search Evaluation." *ACM Transactions on Information
Systems (TOIS)*, 30(1), 6:1–6:41.

**What interleaving is:** Instead of splitting users into control and treatment groups (A/B),
interleaving shows each user a blended ranking from both systems. A credit assignment
function determines which system the user "preferred" based on their clicks.

**Key findings:**
- Validated using data from two major commercial search engines (Microsoft, Yahoo!) and
  a scientific literature retrieval system
- Interleaving shows strong agreement with manual relevance judgments
- Significantly higher statistical power than traditional A/B testing for detecting ranking
  quality differences
- The paper proposes learning improved credit-assignment functions for clicks that further
  increase sensitivity

**Sensitivity advantage:**
- Literature reports 10–100x higher sensitivity than A/B testing for detecting which
  ranking system is better
- The advantage comes from within-subject design: every user sees both systems, reducing
  variance from user-level confounders

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

#### 5.2 Interleaving in Production (Industry)

**Airbnb — Beyond A/B Test:**

Zhang, Q. et al. (2022). "Beyond A/B Test: Speeding up Airbnb Search Ranking
Experimentation through Interleaving." *Airbnb Tech Blog.* Also published as:
Zhang, Q. et al. (2025). "Harnessing the Power of Interleaving and Counterfactual
Evaluation for Airbnb Search Ranking." *KDD 2025.*

- **50x speedup** over A/B testing given the same traffic
- Each interleaving experiment uses ~6% of regular A/B test traffic and 1/3 of running
  length
- Interleaving is now part of Airbnb's standard experimentation procedure as the main
  evaluation technique before A/B test
- Comprehensive validation showed high correlation with traditional A/B test outcomes
- Motivation: Airbnb's conversion-focused metrics have low transaction frequency, making
  A/B tests slow

**Netflix — Interleaving for Personalization:**

Netflix Technology Blog. (2020). "Innovating Faster on Personalization Algorithms at
Netflix Using Interleaving." *Netflix TechBlog.*

- Two-stage online experimentation: (1) fast interleaving to prune algorithm candidates
  in days, (2) traditional A/B test on the surviving candidates
- Interleaving "is highly sensitive to ranking algorithm quality and reliably identifies
  the best algorithms with considerably smaller sample size"
- Reduced total experiment duration and member exposure to suboptimal algorithms

**DoorDash — Interleaving for Search:**

DoorDash Engineering. "How DoorDash is Pushing Experimentation Boundaries with Interleaving
Designs." *DoorDash Careers Blog.*

- Reports >100x sensitivity over traditional A/B testing methods
- Multiple conditions tested simultaneously on the same user in the same screen
- Key confounder removed: user hunger level (presenting multiple rankers in the same
  context controls for time-varying satiety effects)
- Interleaving integrated into their experimentation platform and SDK

**Thumbtack — Accelerating Ranking Experimentation:**

Zhao, D. & Sathe, D. "Accelerating Ranking Experimentation at Thumbtack with
Interleaving." *Thumbtack Engineering Blog (Medium).*

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

#### 5.3 A/B Testing for Search: Duration and Novelty Effects

**Key findings from multiple sources:**

- **Minimum duration:** 4 weeks is the consensus minimum for search ranking A/B tests that
  significantly change user behavior. Two weeks risks capturing the novelty effect but not
  the steady-state behavior.
- **Novelty effect:** Metric values (especially engagement metrics like CTR) typically peak
  in the first few days after exposure to a new ranking, then decline as the novelty wears
  off. Tests stopped at 1–2 weeks may report inflated treatment effects.
- **Business cycle recommendation:** Run for at least 2 full business cycles, regardless
  of sample size. For most consumer products, this means 2–4 weeks.
- **Specific to search ranking:** Ranking changes can have delayed effects on user behavior
  (e.g., users adjust their search strategy over time), making longer test durations
  particularly important.

**Reference:** Netflix Technology Blog. (2016). "It's All A/Bout Testing: The Netflix
Experimentation Platform." *Netflix TechBlog.* (Discusses experiment platform design
including duration considerations.)

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: ds]

---

### 6. Workstream-Tier Content (Ranking Engineering Blog Posts)

These entries represent the kind of content that would populate the workstream tier of the
search-ranking digest. For the public data proxy (Layer 1 v0.5), these are real published
sources tagged as authoritative. In a production setup with Confluence, these would be
replaced by internal team documents.

#### 6.1 Airbnb: ML-Powered Ranking Evolution

**Source:** Grbovic, M. (2019). "Machine Learning-Powered Search Ranking of Airbnb
Experiences." *Airbnb Tech Blog.*

**Key decisions/learnings:**
- Started with rule-based ranking, moved to GBDT (2015), then DNN (2018)
- Feature engineering matters even with deep learning; don't skip the fundamentals
- At sufficient scale, 10x more training data + simple DNN beat complex feature engineering
- Interpretability solved with distribution-comparison tool (TopBot)

**Fits as:** Workstream Standard (ranking architecture evolution pattern)
[authority: authoritative] [audience: all]

---

#### 6.2 Airbnb: Position Bias and Deep Learning Improvements

**Source:** Haldar, M. et al. (2020). "Improving Deep Learning for Airbnb Search." *KDD 2020.*

**Key decisions/learnings:**
- Position bias handling was one of the most impactful improvements
- "ABCs" framework: Architecture, Bias, Cold start as the three levers for DNN ranking
- Cold start for new listings requires explicit modeling, not just more data

**Fits as:** Workstream Learning (production position bias correction case study)
[authority: authoritative] [audience: all]

---

#### 6.3 Etsy: From GBDT to Deep Learning for Search

**Source:** Etsy Engineering. "Deep Learning for Search Ranking at Etsy." *Code as Craft Blog.*

**Key decisions/learnings:**
- GBDT hit diminishing returns from feature engineering — motivation for DNN transition
- One-year iteration cycle from start to production DNN launch
- 250ms latency budget for entire ranking pipeline (feature fetch + scoring + ranking)
- TF Ranking library as the core LTR framework
- Personalization was the first major win from GBDT, not relevance improvement

**Fits as:** Workstream Standard (ranking system evolution, latency budget)
[authority: authoritative] [audience: eng]

---

#### 6.4 LinkedIn: Multi-Aspect Search Ranking

**Source:** LinkedIn Engineering. (2022). "Improving Post Search at LinkedIn."
*LinkedIn Engineering Blog.*

**Key decisions/learnings:**
- Multi-aspect First Pass Ranker with independent ML models per aspect
- Developer productivity as a ranking team metric (6 weeks → 2 weeks for new features)
- Platform investment enabling faster experimentation (21 weeks → 1 week for new entity)
- Latency improvements quantified per platform (Android, iOS, web)

**Fits as:** Workstream Standard (multi-aspect ranking, developer productivity)
[authority: authoritative] [audience: eng]

---

#### 6.5 Airbnb: Interleaving Experimentation at Scale

**Source:** Zhang, Q. et al. (2022). "Beyond A/B Test: Speeding up Airbnb Search Ranking
Experimentation through Interleaving." *Airbnb Tech Blog.*

**Key decisions/learnings:**
- 50x sensitivity improvement over A/B testing (validated)
- Interleaving uses 6% of A/B traffic, 1/3 of running length
- Now the default first-stage evaluation before A/B test
- Motivation: marketplace metrics (bookings) have low frequency, making A/B tests slow

**Fits as:** Workstream Standard (experimentation methodology decision)
[authority: authoritative] [audience: all]

---

## Batch 2: Query Understanding

*To be researched in a separate task. Topics will include:*
- Query classification and intent detection
- Query rewriting and expansion
- Spell correction evaluation
- Query segmentation
- Semantic matching vs. lexical matching
- Industry blog posts on QU systems

---

## Batch 3: Cross-Domain (Search-Wide)

*To be researched in a separate task. Topics will include:*
- End-to-end search evaluation (offline vs. online metrics)
- Multi-stage ranking pipelines (retrieval → re-ranking → blending)
- Latency-quality tradeoffs in production search
- Search system observability and debugging
- Industry blog posts on search platform architecture

---

## Source Index

Quick reference of all cited sources, sorted alphabetically by first author.

| # | Citation | Year | Topic | Type |
|---|---|---|---|---|
| 1 | Ai, Q. et al. "Unbiased Learning to Rank with Unbiased Propensity Estimation." SIGIR 2018. | 2018 | Position bias / IPW | Paper |
| 2 | Burges, C. J. C. "From RankNet to LambdaRank to LambdaMART: An Overview." MSR-TR-2010-82. | 2010 | Learning to Rank | Tech Report |
| 3 | Burges, C. J. C. et al. "Learning to Rank Using an Ensemble of Lambda-Gradient Models." JMLR W&CP Vol. 14. | 2011 | LambdaMART benchmark | Paper |
| 4 | Chapelle, O. & Zhang, Y. "A Dynamic Bayesian Network Click Model for Web Search Ranking." WWW 2009. | 2009 | Click models (DBN) | Paper |
| 5 | Chapelle, O. et al. "Expected Reciprocal Rank for Graded Relevance." CIKM 2009. | 2009 | Evaluation metrics (ERR) | Paper |
| 6 | Chapelle, O. et al. "Large-Scale Validation and Analysis of Interleaved Search Evaluation." TOIS 2012. | 2012 | Interleaving experiments | Paper |
| 7 | Chuklin, A. et al. *Click Models for Web Search.* Morgan & Claypool, 2015. | 2015 | Click model survey | Book |
| 8 | Craswell, N. et al. "An Experimental Comparison of Click Position-Bias Models." WSDM 2008. | 2008 | Click models (Cascade) | Paper |
| 9 | DoorDash Engineering. "How DoorDash is Pushing Experimentation Boundaries with Interleaving Designs." | 2023 | Interleaving in production | Blog |
| 10 | Etsy Engineering. "Deep Learning for Search Ranking at Etsy." Code as Craft. | 2022 | LTR in production | Blog |
| 11 | Etsy Engineering. "How Etsy Uses LLMs to Improve Search Relevance." Code as Craft. | 2024 | LLMs for ranking | Blog |
| 12 | Grbovic, M. "Machine Learning-Powered Search Ranking of Airbnb Experiences." Airbnb Tech Blog. | 2019 | LTR in production | Blog |
| 13 | Haldar, M. et al. "Improving Deep Learning for Airbnb Search." KDD 2020. | 2020 | DNN ranking, position bias | Paper |
| 14 | Järvelin, K. & Kekäläinen, J. "Cumulated Gain-Based Evaluation of IR Techniques." TOIS 2002. | 2002 | Evaluation metrics (NDCG) | Paper |
| 15 | Joachims, T. et al. "Accurately Interpreting Clickthrough Data as Implicit Feedback." SIGIR 2005. | 2005 | Position bias, eye tracking | Paper |
| 16 | Joachims, T. et al. "Evaluating the Accuracy of Implicit Feedback..." TOIS 2007. | 2007 | Position bias, eye tracking | Paper |
| 17 | Khattab, O. & Zaharia, M. "ColBERT: Efficient and Effective Passage Search..." SIGIR 2020. | 2020 | Neural ranking (ColBERT) | Paper |
| 18 | LinkedIn Engineering. "Improving Post Search at LinkedIn." | 2022 | Search ranking platform | Blog |
| 19 | Netflix Technology Blog. "Innovating Faster on Personalization Algorithms at Netflix Using Interleaving." | 2020 | Interleaving in production | Blog |
| 20 | Nogueira, R. & Cho, K. "Passage Re-ranking with BERT." arXiv: 1901.04085. | 2019 | Neural ranking (BERT) | Paper |
| 21 | Nogueira, R. et al. "Document Ranking with a Pretrained Sequence-to-Sequence Model." arXiv: 2003.06713. | 2020 | Neural ranking (monoT5) | Paper |
| 22 | Oosterhuis, H. "Doubly-Robust Estimation for Correcting Position-Bias..." TOIS 2023. | 2023 | Position bias / DR | Paper |
| 23 | Richardson, M. et al. "Predicting Clicks: Estimating the Click-Through Rate for New Ads." WWW 2007. | 2007 | Click models (PBM) | Paper |
| 24 | Wang, X. et al. "Learning to Rank with Selection Bias in Personal Search." SIGIR 2016. | 2016 | Position bias / IPW | Paper |
| 25 | Zhang, Q. et al. "Beyond A/B Test: Speeding up Airbnb Search Ranking Experimentation through Interleaving." Airbnb Tech Blog / KDD 2025. | 2022/2025 | Interleaving in production | Blog/Paper |
