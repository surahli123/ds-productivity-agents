# Domain Knowledge References

**Purpose:** Research backing for the domain knowledge digest files. Each entry includes
source, key finding, citation, and which digest section/tier it maps to. This document
feeds into the actual digest files (`shared/skills/search-domain-knowledge/digests/*.md`) during Layer 1 implementation.

**Organization:** Batches correspond to domains. Batch 1 covers Search Ranking (the
largest and template domain). Batch 2 covers Query Understanding. Batch 3 covers
Cross-Domain evaluation. Batch 4 covers Emerging Search Paradigms (AI Search, Agentic
Search, Generative Retrieval).

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

### 1. Query Classification and Intent Detection

#### 1.1 Broder's Taxonomy (Informational / Navigational / Transactional)

**Key paper:** Broder, A. (2002). "A Taxonomy of Web Search." *ACM SIGIR Forum*, 36(2), 3–10.

**What it is:** The foundational classification of web search queries into three intent categories:
1. **Informational:** User wants to learn something (e.g., "how does NDCG work"). No further
   interaction beyond reading is expected.
2. **Navigational:** User wants to reach a specific website (e.g., "airbnb login"). Typically
   has a single "right" answer.
3. **Transactional:** User wants to perform an action — purchase, download, sign up
   (e.g., "buy running shoes").

**Key finding (query distribution):** Broder reported approximately 73% informational, 26%
navigational, and 36% transactional queries. Percentages exceed 100% because some queries
were classified into multiple categories.

**Why it matters for DS review:** This taxonomy is the baseline for all query intent work.
Any query classification system that doesn't acknowledge these three categories — or explain
why its taxonomy differs — is likely missing foundational context. The distribution also
matters: informational queries dominate, which means evaluation metrics for informational
search (like NDCG over graded relevance) tend to drive the most business impact.

**Digest mapping:** Foundational Knowledge > Query Understanding Fundamentals [authority: authoritative] [audience: all]

---

#### 1.2 Operationalizing Broder's Taxonomy

**Key paper:** Jansen, B. J., Booth, D. L., & Spink, A. (2008). "Determining the Informational,
Navigational, and Transactional Intent of Web Queries." *Information Processing and Management*,
44(3), 1251–1266.

**What it adds:** Jansen et al. operationalized Broder's taxonomy into an automatic classification
system and validated it at scale:
- Analyzed over 1.5 million queries from multiple search engine logs
- Developed an automated classification algorithm achieving 74% accuracy against manual labels
- Refined the distribution: **80%+ informational**, ~10% navigational, ~10% transactional
- Defined hierarchical sub-categories within each intent class

**Key insight for digest:** The gap between Broder's self-reported numbers (73/26/36) and
Jansen's log-based analysis (80/10/10) illustrates a methodological lesson: self-reported
intent vs. observed behavior differ significantly. DS analysts should be cautious about
how intent labels are generated.

**Digest mapping:** Foundational Knowledge > Query Understanding Fundamentals [authority: authoritative] [audience: ds]

---

#### 1.3 Modern Intent Classification with Transformers

**Benchmarks and approaches:**

Transformer-based models have become the standard for intent classification since 2018:

| Model | Dataset | Accuracy | Notes |
|---|---|---|---|
| Joint BERT (Chen et al.) | ATIS | >97% | Joint intent + slot filling |
| Joint BERT | Snips | ~98.6% | Surpasses RNN-attention and slot-gated models |
| DistilBERT | Various | Near BERT-level | 40% smaller, 60% faster, minimal accuracy loss |
| LaBSE (Language-Agnostic BERT Sentence Embedding) | Multilingual | Highest accuracy | Significant memory requirements |

**LLM-based intent detection (2024+):**

Recent work evaluates LLMs (GPT-4, Claude, Llama) for intent detection in task-oriented
dialogue, highlighting a performance-latency tradeoff: LLMs achieve competitive accuracy
with zero/few-shot prompting but at significantly higher latency and cost compared to
fine-tuned BERT classifiers.

**Reference:** Arora, A. et al. (2024). "Intent Detection in the Age of LLMs."
*arXiv: 2410.01627.*

**Key insight for digest:** For production query classification, fine-tuned BERT/DistilBERT
models remain dominant due to latency constraints. LLMs are useful for labeling training data
and handling long-tail or ambiguous queries. The right architecture depends on latency budget
and query volume.

**Digest mapping:** Foundational Knowledge > Query Understanding Fundamentals [authority: authoritative] [audience: all]

---

### 2. Query Rewriting and Expansion

#### 2.1 Query Rewriting Evaluation: Downstream vs. Intrinsic

**Key distinction:** Query rewriting can be evaluated two ways:
1. **Intrinsic evaluation:** How well does the rewrite match a "gold standard" query?
   (BLEU, exact match, manual judgment.)
2. **Downstream evaluation:** How much does the rewrite improve retrieval quality?
   (MRR, NDCG, Recall at various cutoffs on the rewritten query vs. the original.)

**Key finding:** Downstream evaluation is more reliable but harder to set up. A rewrite that
scores high on BLEU may not improve retrieval, and vice versa. The best rewriting systems
are now evaluated end-to-end against retrieval metrics.

**Reference:** Ma, X. et al. (2023). "Query Rewriting for Retrieval-Augmented Large Language
Models." *Proceedings of EMNLP 2023.* (Demonstrates that query rewriting significantly
improves RAG pipeline accuracy when evaluated end-to-end.)

**Reference:** Song, R. et al. (2024). "RaFe: Ranking Feedback Improves Query Rewriting
for RAG." *Findings of EMNLP 2024.* (arXiv: 2405.14431.) (Uses ranking feedback to
iteratively improve query rewrites, evaluated via downstream retrieval metrics.)

**Key insight for digest:** When reviewing a QU analysis, check whether rewriting quality
was measured intrinsically (BLEU/edit distance) or via downstream impact (NDCG/MRR change).
Intrinsic-only evaluation is a red flag — rewrites need to improve actual search results.

**Digest mapping:** Foundational Knowledge > Evaluation Standards [authority: authoritative] [audience: ds]

---

#### 2.2 Query Rewriting in Production

**General framework:** Query rewriting encompasses several techniques applied in sequence:
- **Synonym expansion:** Adding related terms to improve recall
- **Query relaxation:** Removing overly restrictive terms when results are sparse
- **Query augmentation:** Adding context (e.g., user location, session history)
- **Semantic rewriting:** Replacing surface-level query with a semantically equivalent form

**Key reference:** Williams, H. E. (2012). "Query Rewriting in Search Engines." *Blog post.*
(Practical overview of production query rewriting from a former Yahoo! VP of Engineering.)

**Production consideration:** The order of QU techniques matters significantly. Applying
synonym expansion before spell correction can amplify errors. Applying query relaxation
too aggressively reduces precision. Most production systems use a pipeline where each
stage's output becomes the next stage's input, with quality gates between stages.

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

### 3. Spell Correction

#### 3.1 Spell Correction Evaluation and Tradeoffs

**The fundamental tradeoff:** Spell correction involves a precision-recall tension:
- **Aggressive correction** (high recall): Catches more typos but risks "correcting" valid
  queries (e.g., correcting a brand name the system doesn't recognize)
- **Conservative correction** (high precision): Only corrects clear misspellings but misses
  non-obvious errors (phonetic misspellings, transliteration errors)

**Evaluation metrics:**
- **Detection precision:** Of all queries flagged as misspelled, how many actually are?
- **Detection recall:** Of all misspelled queries, how many were detected?
- **Correction accuracy:** Of detected misspellings, how many were corrected to the right term?
- **End-to-end impact:** Does spell correction improve downstream search metrics (CTR, NDCG)?

**Key reference:** Hasan, S. et al. (2015). "Spelling Correction of User Search Queries
through Statistical Machine Translation." *Proceedings of ACL 2015 (EMNLP Workshop on
Noisy User-generated Text).*

**Key insight for digest:** A common mistake is evaluating spell correction in isolation
(intrinsic accuracy) without measuring downstream impact on search quality. A spell
corrector with 95% accuracy can still hurt search if the 5% errors involve high-traffic
brand names or product terms.

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: all]

---

#### 3.2 Spell Correction in E-Commerce Search

**Key paper 1:** Kakkar, H. et al. (2023). "Search Query Spell Correction with Weak
Supervision in E-commerce." *Proceedings of ACL 2023 (Industry Track).*

- Systematically groups spelling errors into error classes (typos, phonetic, transliteration)
- Leverages Transformer models for contextual spell correction
- Proposes synthetic data generation to overcome limited human-labeled data
- Uses weak supervision with curriculum learning for difficult spelling mistakes

**Key paper 2:** Amazon Science. (2022). "Spelling Correction using Phonetics in E-commerce
Search." *Proceedings of ECNLP Workshop 2022.*

- Addresses phonetic errors in e-commerce (customers influenced by spoken accents)
- Integrates phonetic similarity into the correction pipeline without additional latency
- Key finding: generic spell correction systems trained on clean English sources perform
  poorly on e-commerce queries with phonetic/vernacular errors

**Key paper 3:** Pande, A. et al. (2022). "Learning-to-Spell: Weak Supervision based
Query Correction in E-Commerce Search with Small Strong Labels." *Proceedings of CIKM 2022.*

- Reports that ~32% of e-commerce queries contain spelling mistakes
- Demonstrates weak supervision can significantly reduce the need for expensive human labels
- Achieves competitive F1 scores using a fraction of the labeled data

**Key insight for digest:** E-commerce spell correction is a distinct challenge from web
search spell correction. The error distribution (phonetic, transliteration, brand-specific)
differs significantly, and off-the-shelf solutions trained on web data underperform.

**Digest mapping:** Foundational Knowledge > Known Pitfalls [authority: authoritative] [audience: all]

---

### 4. Query Segmentation and Entity Recognition

#### 4.1 Query Segmentation for Search

**What it is:** Query segmentation (also called query parsing or query tagging) breaks a
search query into meaningful semantic units. For example, "blue check casual shirt for men"
becomes: color=blue, pattern=check, style=casual, product_type=shirt, gender=men.

**Key reference:** Hao, J. et al. (2024). "QueryNER: Segmentation of E-commerce Queries."
*Proceedings of LREC-COLING 2024.* (arXiv: 2405.09507.)

- Introduces a manually-annotated dataset for e-commerce query segmentation
- E-commerce queries are more noisy and unstructured than traditional NER text
- Proposes broadly applicable entity types rather than domain-specific categories

**Industry application:** Chen, C. et al. (2021). "An End-to-End Solution for Named Entity
Recognition in eCommerce Search." *Proceedings of AAAI 2021.*

- "TripleLearn" framework: iteratively learns from three separate training datasets
- Deployed on homedepot.com for 9+ months
- Online A/B tests showed significant improvements in user engagement and revenue conversion

**Key insight for digest:** Query segmentation quality directly affects retrieval: if the
system misidentifies "apple" as a fruit when the user meant the brand, downstream ranking
cannot recover. This is why QU errors tend to have larger impact than ranking model errors.

**Digest mapping:** Foundational Knowledge > Methodology [authority: authoritative] [audience: all]

---

### 5. Workstream-Tier Content (QU Engineering Blog Posts)

These entries represent real published engineering blog posts about query understanding
decisions and experiments.

#### 5.1 Pinterest: SearchSage — Learning Query Representations

**Source:** Pinterest Engineering. "SearchSage: Learning Search Query Representations at
Pinterest." *Pinterest Engineering Blog (Medium).*

**Key decisions/learnings:**
- SearchSage learns a query embedding in the same space as PinSage (pin embeddings)
  using a two-tower architecture with the candidate tower frozen
- Replaced the prior approach of representing queries as clusters of historically-engaged
  pin embeddings — a common but brittle pattern that fails for new/rare queries
- Results: 11% increase in 35s+ click-throughs on product Pins in search, 42% increase
  in related searches
- Now used for 15+ use cases across organic and ads ranking
- Evolution: OmniSearchSage (2024) unifies query, pin, and product embeddings,
  yielding >8% relevance, >7% engagement, >5% ads CTR improvements

**Fits as:** Workstream Standard (query representation architecture decision)
[authority: authoritative] [audience: all]

---

#### 5.2 Pinterest: LLMs for Search Relevance

**Source:** Pinterest Engineering. (2024). "Improving Pinterest Search Relevance Using Large
Language Models." *Pinterest Engineering Blog (Medium).* Also published as arXiv: 2410.17152.

**Key decisions/learnings:**
- LLMs used to generate relevance labels for training ranking models at scale
- Replaced expensive human annotation with LLM-generated labels
- LLM labels used as training signal, not for direct inference (avoids latency issues)
- Demonstrates the "LLM as labeler" pattern that avoids serving-time LLM costs

**Fits as:** Workstream Learning (LLM integration pattern for QU/ranking)
[authority: authoritative] [audience: all]

---

#### 5.3 DoorDash: LLMs for Search Retrieval and Query Understanding

**Source:** DoorDash Engineering. (2024). "How DoorDash Leverages LLMs for Better Search
Retrieval." *DoorDash Careers Blog.*

**Key decisions/learnings:**
- Combined LLMs with knowledge graph for query segmentation and entity linking
- Used RAG to constrain LLM outputs to a controlled vocabulary (preventing hallucinated
  entity names)
- Query rewriting, entity disambiguation, and search path recommendation as key QU tasks
- Results: 30% improvement in popular dish carousel trigger rate, >2% whole-page relevance
  increase, higher conversion rates
- Architecture: LLM processes query → knowledge graph grounds entities → retrieval
  system fetches results

**Fits as:** Workstream Standard (LLM + knowledge graph QU architecture)
[authority: authoritative] [audience: all]

---

#### 5.4 Spotify: Agentic Query Understanding with LLM Routers

**Source:** Palumbo, E. et al. (2025). "You Say Search, I Say Recs: A Scalable Agentic
Approach to Query Understanding and Exploratory Search at Spotify." *Proceedings of RecSys 2025.*

**Key decisions/learnings:**
- Proposed a "Parallel Fusion Router" (PFR) architecture: an intermediate design between
  simple rule-based routing and full LLM orchestration
- LLM router enriches queries with temporal, genre, and entity-type filters (e.g., "new
  indie rock releases" → adds time filter, genre facet, content-type facet)
- Key scalability decision: pass only the query (not user features) to the LLM router
  to maximize cache hit rate, keeping latency low
- Sub-agents invoke LLMs only when necessary (external knowledge, complex reasoning,
  SERP refinement), otherwise use traditional ML retrievers/rankers
- Represents the trend of agentic QU — treating query understanding as a planning problem
  rather than a classification problem

**Fits as:** Workstream Standard (agentic QU architecture, caching strategy)
[authority: authoritative] [audience: all]

---

## Batch 3: Cross-Domain (Search-Wide)

### 1. Multi-Stage Ranking Pipeline Evaluation

#### 1.1 The Selection Bias Problem Across Stages

**Key paper:** Hager, P. et al. (2024). "Full Stage Learning to Rank: A Unified Framework
for Multi-Stage Systems." *Proceedings of The Web Conference (WWW) 2024.*

**What it is:** Modern search systems use multi-stage pipelines (retrieval → pre-ranking →
ranking → re-ranking), and each stage introduces *selection bias* — the upstream stage
determines what the downstream stage sees. This paper introduces the Generalized Probability
Ranking Principle (GPRP) to account for this.

**Key insight:** Each stage's model is trained to rank all candidates well, but in practice
it only needs to rank well enough to get its top results past the next stage's filter.
Optimizing for end-to-end system output (not stage-local metrics) produces better results.

**Why it matters for DS review:** When evaluating a ranking change, the impact depends on
where in the pipeline it sits. A retrieval-stage improvement may not surface in end-to-end
NDCG if the re-ranker already compensates. Understanding which stage is the bottleneck
requires cross-stage metric attribution, not just stage-local evaluation.

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: ds]

---

#### 1.2 Multi-Stage Re-Ranking with Neural Models

**Key reference:** Nogueira, R. et al. (2019). "Multi-Stage Document Ranking with BERT."
*arXiv: 1910.14424.*

**Architecture pattern:** The standard multi-stage pipeline is:
1. **Retrieval (Stage 0):** Fast, low-precision method (BM25, two-tower embeddings) retrieves
   top ~1000 candidates from millions/billions of documents
2. **Pre-ranking (Stage 1):** Lightweight model (GBDT, small neural model) narrows to
   top ~100 candidates
3. **Ranking (Stage 2):** More expensive model (cross-encoder BERT, T5) scores top ~100
4. **Re-ranking (Stage 3):** Business logic, diversity, freshness adjustments on top ~20

**Key evaluation challenge:** Each stage has different latency budgets (retrieval: <50ms,
ranking: <200ms, re-ranking: <50ms) and different candidate pool sizes. Metrics computed
at one stage don't directly predict end-to-end user experience.

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: all]

---

### 2. End-to-End Search Evaluation

#### 2.1 Offline vs. Online Metric Alignment

**The fundamental challenge:** Offline metrics (NDCG, MRR computed on held-out test sets)
don't always predict online metrics (click-through rate, conversion, engagement). The gap
comes from:
- **Relevance label quality:** Offline metrics assume labels are correct; in practice,
  labels are noisy, biased, or incomplete
- **User behavior complexity:** Real users exhibit position bias, query reformulation,
  session-level learning effects
- **Feature distribution shift:** Training/test data may not match production query distribution

**Practical guidance (from industry consensus):**
- Use offline metrics for fast iteration (model development, feature selection)
- Use interleaving for medium-confidence online validation (see Batch 1, Section 5.1)
- Use A/B testing for final launch decisions with full business metrics
- Track offline-online metric correlation over time — if the correlation degrades,
  your offline evaluation setup needs recalibration

**Key reference:** Chapelle, O. et al. (2012). "Large-Scale Validation and Analysis of
Interleaved Search Evaluation." *TOIS 2012.* (Validates that interleaving has strong
agreement with manual relevance judgments.)

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: ds]

---

#### 2.2 Component-Level Metric Attribution

**The question:** When end-to-end search quality improves (or degrades), which component
was responsible — retrieval, ranking, query understanding, or blending?

**Attribution methods in practice:**
- **Ablation studies:** Turn off or randomize one component while keeping others fixed.
  Measures the *marginal contribution* of each component.
- **Counterfactual evaluation:** Use logged data to estimate what would have happened
  with a different component. Related to offline A/B testing and counterfactual LTR.
- **Stage-local metrics:** Measure each stage's quality independently (retrieval recall@1000,
  ranking NDCG@10, QU intent accuracy). Risk: stage-local improvements may not translate
  to end-to-end gains.
- **Error analysis:** Manually inspect failure cases and classify the root cause by component.
  Most reliable but least scalable.

**Key insight for digest:** End-to-end metric movement without component attribution is
a common oversight in search analyses. "NDCG went up 2%" is incomplete without understanding
*why* — was it better retrieval, better ranking, or better query understanding?

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: ds]

---

### 3. RAG Evaluation Frameworks (Cross-Domain for AI Search Systems)

#### 3.1 RAGAS: Reference-Free RAG Evaluation

**Key paper:** Es, S. et al. (2024). "RAGAS: Automated Evaluation of Retrieval Augmented
Generation." *Proceedings of EACL 2024 (System Demonstrations).* (arXiv: 2309.15217.)

**What it is:** RAGAS is a framework for evaluating RAG pipelines without requiring human
reference answers. It decomposes evaluation into four metrics:
- **Faithfulness:** Is the generated answer factually grounded in the retrieved context?
  (Number of correct statements / total statements.)
- **Answer Relevancy:** Does the answer address the query?
- **Context Precision:** Are the retrieved documents relevant (signal-to-noise ratio)?
- **Context Recall:** Was all necessary information retrieved?

**Why it matters for DS review:** As search systems incorporate generative components
(AI Overviews, RAG-based answers), traditional IR metrics (NDCG, MRR) are insufficient.
RAGAS provides a bridge between traditional retrieval evaluation and generative AI evaluation.

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: all]

---

#### 3.2 UDCG: Bridging IR Metrics and RAG Accuracy

**Key paper:** Wang, Y. et al. (2025). "Redefining Retrieval Evaluation in the Era of LLMs."
*arXiv: 2510.21440.*

**What it is:** Utility and Distraction-aware Cumulative Gain (UDCG) is a metric designed
specifically for RAG systems. It substitutes human relevance with machine utility and applies
an LLM-oriented positional discount that directly optimizes correlation between the IR metric
and end-to-end answer accuracy.

**Key finding:** UDCG exhibits substantially stronger correlation with end-to-end RAG
accuracy than traditional IR metrics like NDCG, with improvements of up to 36% in
correlation.

**Key insight for digest:** This suggests that as search moves toward generative answers,
the metrics we use to evaluate retrieval need to evolve. NDCG optimizes for human scanning
behavior; UDCG optimizes for LLM consumption of retrieved documents.

**Digest mapping:** Foundational Knowledge > Cross-Domain Evaluation [authority: authoritative] [audience: ds]

---

### 4. Workstream-Tier Content (Cross-Domain Engineering Blog Posts)

#### 4.1 Algolia: Query Understanding 101

**Source:** Algolia. "Query Understanding 101." *Algolia Blog.*

**Key decisions/learnings:**
- Defines QU as a pipeline: tokenization → spell correction → synonym expansion →
  intent detection → query rewriting
- Emphasizes that the order of QU pipeline stages matters: spell correction must come
  before synonym expansion
- Highlights the precision-recall tradeoff in each QU stage
- Practical guide for search teams building QU pipelines from scratch

**Fits as:** Workstream Standard (QU pipeline design, stage ordering)
[authority: authoritative] [audience: all]

---

#### 4.2 Daniel Tunkelang: Precision, Recall, and Desirability

**Source:** Tunkelang, D. "Precision, Recall, and Desirability." *Medium / LinkedIn.*

**Key decisions/learnings:**
- Extends the precision-recall framework to include "desirability" — a practical metric
  that accounts for business relevance beyond topical relevance
- Argues that recall is often overlooked in production search evaluation because it's
  harder to measure (you need to know the full set of relevant documents)
- Practical frameworks for evaluating search quality across the full pipeline

**Fits as:** Workstream Learning (evaluation philosophy, full-pipeline thinking)
[authority: authoritative] [audience: ds]

---

## Batch 4: Emerging Search Paradigms

*This section covers paradigm shifts that are reshaping search systems and their evaluation.
These are more recent (2023–2026) and represent where the field is heading. Content here
informs both the foundational tier (for established techniques) and a new "Emerging
Paradigms" section in the digests.*

### 1. AI-Powered Search (LLM Re-Ranking and RAG)

#### 1.1 LLM-Based Re-Ranking: RankGPT

**Key paper:** Sun, W. et al. (2023). "Is ChatGPT Good at Search? Investigating Large
Language Models as Re-Ranking Agents." *Proceedings of EMNLP 2023.* **Outstanding Paper
Award.**

**What it is:** RankGPT uses LLMs (ChatGPT, GPT-4) as zero-shot listwise re-rankers. Given
a query and a set of candidate passages, the LLM generates a global ordering. A sliding
window strategy enables ranking more passages than the LLM's context window allows.

**Key results:**
- GPT-4 as a re-ranker achieves performance competitive with or exceeding fine-tuned
  neural rankers on standard benchmarks
- Zero-shot (no task-specific training needed) — a fundamental shift from the fine-tuning
  paradigm
- The sliding window strategy (ranking from back to front) is now widely adopted in
  subsequent work

**Key reference for TREC results:** TREC 2023 Deep Learning Track: GPT-4 prompting achieved
NDCG@10 of 0.6994, surpassing the best fine-tuned neural model at ~0.597 — a ~17%
improvement. (See Batch 1, Section 4.2 for context.)

**Why it matters for DS review:** LLM re-ranking introduces new evaluation questions:
- How to measure re-ranking quality when the LLM has no explicit relevance model?
- How to attribute ranking improvements to the LLM vs. the upstream retrieval stage?
- Cost-quality tradeoffs: LLM re-ranking may be 100x more expensive per query than
  traditional re-rankers

**Digest mapping:** Emerging Paradigms > AI Search [authority: authoritative] [audience: all]

---

#### 1.2 The Impact of AI Overviews on Search Evaluation

**Context:** Google AI Overviews (AIOs), Perplexity, and Bing Copilot represent a
fundamental shift in search: instead of returning a ranked list of links, the search engine
generates a synthesized answer with citations.

**Key data points (2024–2025 industry studies):**

| Metric | Impact | Source |
|---|---|---|
| Organic CTR decline | -61% (from 1.76% to 0.61%) when AIO present | Seer Interactive, Sept 2025 |
| Paid CTR decline | -68% (from 19.7% to 6.34%) when AIO present | Seer Interactive, Sept 2025 |
| Top-ranking page CTR | -58% average when AIO present | Ahrefs, Dec 2025 |
| Zero-click searches | 60% of Google searches end without a click | Multiple sources, 2025 |
| AIO prevalence | 18.55% of SERPs (Q3 2024) → 49.92% (Q4 2025) | seoClarity, 2025 |
| Citation advantage | +35% organic clicks for brands cited in AIOs | Seer Interactive, 2025 |

**Implications for search evaluation:**
- Traditional CTR as a metric loses meaning when users get answers without clicking
- New metrics needed: "citation rate," "share of voice in AI answers," "answer coverage"
- NDCG still relevant for the *retrieval* component feeding the LLM, but the end-user
  experience metric is now answer quality, not ranking quality
- Faithfulness and grounding metrics (see RAGAS, Section 3.1 above) become critical

**Key insight for DS review:** Any analysis of search performance that relies solely on
click-based metrics (CTR, clicks/search) may be systematically biased by AIO prevalence.
Analysts need to segment by "AIO present" vs. "AIO absent" queries, or switch to
answer-quality metrics.

**Digest mapping:** Emerging Paradigms > AI Search [authority: authoritative] [audience: all]

---

#### 1.3 RAG Evaluation: The New Search Quality Stack

**Key survey:** Zhang, Y. et al. (2025). "Retrieval Augmented Generation Evaluation in
the Era of Large Language Models: A Comprehensive Survey." *arXiv: 2504.14891.*

**The evaluation stack for AI search systems:**

| Layer | What's Evaluated | Key Metrics |
|---|---|---|
| Retrieval | Document/passage relevance | NDCG, MRR, Recall@k (traditional IR) |
| Generation | Answer quality | Faithfulness, Answer Relevancy (RAGAS) |
| End-to-end | User satisfaction | Task completion rate, answer correctness |
| Attribution | Source quality | Context Precision, Context Recall (RAGAS) |

**Key finding:** Traditional IR metrics still dominate evaluation usage in published
research, but LLM-based evaluation methods (RAGAS, LLM-as-a-Judge) are growing rapidly.
The most robust evaluation combines both: traditional metrics for the retrieval component
and LLM-based metrics for the generation component.

**Key benchmarks:** CRUD-RAG, RAGBench with TRACe, MIRAGE (medical), Long2RAG (long-context).

**Digest mapping:** Emerging Paradigms > AI Search [authority: authoritative] [audience: all]

---

### 2. Agentic Search

#### 2.1 Agentic RAG: Multi-Step Retrieval and Reasoning

**Key survey:** Singh, A. et al. (2025). "Agentic Retrieval-Augmented Generation: A Survey
on Agentic RAG." *arXiv: 2501.09136.*

**What it is:** Agentic RAG embeds autonomous AI agents into the RAG pipeline. Instead of
a single retrieval-then-generate step, agents plan, execute multi-step queries, reflect
on intermediate results, and adapt their retrieval strategy.

**Key design patterns:**
- **Reflection:** Agent evaluates its own answer and decides whether to retrieve more
- **Planning:** Agent decomposes complex queries into sub-queries before retrieving
- **Tool use:** Agent calls specialized APIs (knowledge graphs, databases, calculators)
  alongside document retrieval
- **Multi-agent collaboration:** Multiple specialized agents (retriever, verifier, synthesizer)
  coordinate on a task

**Benchmark results:** Hierarchical retrieval agentic RAG achieves 94.5% on HotpotQA and
89.7% on 2WikiMultiHop with GPT-4o-mini, while using comparable or fewer retrieved tokens
than single-step RAG.

**Counter-finding:** On scientific literature retrieval, BM25 outperforms LLM-based agentic
retrievers by approximately 30% because agents tend to generate keyword-oriented sub-queries
that match poorly against technical vocabulary. This highlights that agentic search is not
universally superior.

**Digest mapping:** Emerging Paradigms > Agentic Search [authority: authoritative] [audience: all]

---

#### 2.2 Evaluating Agentic Search Systems

**The evaluation challenge:** Traditional search evaluation assumes a single query → single
result list. Agentic search involves:
- Multiple intermediate retrievals (how to aggregate quality across steps?)
- Planning decisions (was the decomposition strategy good?)
- Tool selection (did the agent use the right tools?)
- Final synthesis (is the combined answer faithful to all sources?)

**Emerging evaluation approaches:**
- **Agent-as-a-Judge:** Use LLM agents to evaluate other agents' outputs. Generalizes
  "LLM-as-a-Judge" to multi-step workflows.
- **Multi-Agent-as-Judge:** Multiple evaluator agents with different personas (accuracy
  checker, completeness checker, source verifier) jointly assess output.
- **Process-level evaluation:** Evaluate each step of the agent's plan, not just the final
  answer. Rewards good intermediate retrieval even if the final answer is wrong.
- **Task completion rate:** For tool-use agents, measure whether the user's underlying
  task was accomplished, not just whether the answer was "relevant."

**Key reference:** PaperArena benchmark (arXiv: 2510.10909) evaluates tool-augmented
scientific research agents on multi-step retrieval and synthesis tasks.

**Key insight for DS review:** Evaluating agentic search requires fundamentally different
metrics than traditional search. A DS analyst applying NDCG to an agentic system would be
measuring the wrong thing — the relevant question is whether the agent's *plan* was good,
not whether a single retrieval step returned relevant documents.

**Digest mapping:** Emerging Paradigms > Agentic Search [authority: authoritative] [audience: all]

---

### 3. Generative Retrieval

#### 3.1 Differentiable Search Index (DSI)

**Key paper:** Tay, Y. et al. (2022). "Transformer Memory as a Differentiable Search Index."
*Proceedings of NeurIPS 2022.*

**What it is:** DSI encodes an entire corpus into the parameters of a single Transformer
model. Given a query, the model directly generates relevant document identifiers (docids)
autoregressively — no separate index, no retrieval stage, no re-ranking stage.

**Key results:**
- On NQ10K (smallest corpus): DSI achieves 33.9% Hits@1, more than 2x the performance
  of dual encoders (12.4%)
- The 11B-parameter T5 DSI model shows >25 points Hits@1 improvement over dual encoders
  on small corpora and >15 points on large corpora
- DSI exhibits more optimistic scaling properties than dual encoders as model size increases

**Limitations:** DSI requires re-training the model whenever documents are added or updated.
This makes it impractical for dynamic corpora (e.g., web search, news) without incremental
learning extensions.

**Digest mapping:** Emerging Paradigms > Generative Retrieval [authority: authoritative] [audience: all]

---

#### 3.2 GENRE: Autoregressive Entity Retrieval

**Key paper:** De Cao, N., Izacard, G., Riedel, S., & Petroni, F. (2021). "Autoregressive
Entity Retrieval." *Proceedings of ICLR 2021.*

**What it is:** GENRE retrieves entities by generating their names token-by-token using a
fine-tuned BART model with constrained beam search (only valid entity names from a pre-built
prefix tree can be generated).

**Key results:**
- State-of-the-art or competitive results on 20+ datasets for entity disambiguation,
  end-to-end entity linking, and document retrieval
- Uses a tiny fraction of the memory footprint of competing systems (no large entity
  embedding table needed)
- The constrained beam search idea has been widely adopted in subsequent generative
  retrieval work

**Key insight for digest:** GENRE demonstrates that retrieval can be formulated as
*generation under constraints*. This is a foundational idea for generative retrieval:
instead of scoring all candidates, generate the answer directly but constrain the
generation to valid outputs.

**Digest mapping:** Emerging Paradigms > Generative Retrieval [authority: authoritative] [audience: all]

---

#### 3.3 OneSug: End-to-End Generative Query Suggestion (Generated Search in Production)

**Key paper:** Kuaishou Research. (2025). "OneSug: End-to-End Generative Query Suggestion."
*arXiv: 2506.06913.*

**What it is:** OneSug is an industrial-scale framework for e-commerce query suggestion
that replaces the traditional multi-stage cascading architecture (recall → pre-ranking →
ranking) with a single generative model. It is described as "the first end-to-end generative
framework for e-commerce query suggestion" and is deployed on Kuaishou (one of China's
largest short-video/e-commerce platforms, serving billions of daily queries).

**Core architecture:**
1. **Prefix2Query Representation Enhancement (PRE):** Enriches short user input prefixes
   using semantically related queries. Uses RQ-VAE to generate hierarchical semantic IDs,
   reducing computational complexity.
2. **Unified Encoder-Decoder:** Takes user prefixes, related queries, historical behavior,
   and user profiles as inputs; directly generates suggested queries via Transformer-based
   autoregressive decoding (built on Qwen2.5-3B).
3. **Reward-Weighted Ranking (RWR):** Categorizes user behaviors into six levels and
   constructs weighted preference pairs. Applies Direct Preference Optimization (DPO)
   with dynamic weighting to capture fine-grained user preferences.

**Key results:**

| Metric | Value | Notes |
|---|---|---|
| HitRate@16 | 93.37% | OneSug (Qwen2.5-3B), offline |
| MRR | 66.31% | OneSug (Qwen2.5-3B), offline |
| Top click position reduction | -9.33% | Online A/B test (1+ month on Kuaishou) |
| CTR increase | +2.01% | Online A/B test |
| Order increase | +2.04% | Online A/B test |
| Revenue improvement | +1.69% | Online A/B test |
| System response time reduction | -43.21% | Unified model is faster than multi-stage |
| Query quality improvement | +22.51% | Manual evaluation |

**Why this matters:**
- Demonstrates that generative retrieval can *replace* (not just supplement) traditional
  multi-stage pipelines in production
- The unified model is actually *faster* than the cascading baseline (43% latency reduction)
  because it eliminates inter-stage communication overhead
- Addresses the key limitation of cascading systems: "the performance of the previous stage
  determines the upper bound of the next stage"
- Revenue improvements validate the approach on real business metrics, not just offline benchmarks

**Key insight for DS review:** OneSug challenges the assumption that multi-stage pipelines
are necessary for production search quality. When evaluating a generated search system,
traditional stage-by-stage metrics (retrieval recall, ranking NDCG) are replaced by
end-to-end generation metrics (HitRate@k, MRR on generated suggestions) and business
metrics (CTR, conversion, revenue).

**Digest mapping:** Emerging Paradigms > Generative Retrieval [authority: authoritative] [audience: all]

---

#### 3.4 Generative Information Retrieval: Survey and Taxonomy

**Key survey:** Li, Y. et al. (2025). "From Matching to Generation: A Survey on Generative
Information Retrieval." *ACM Transactions on Information Systems (TOIS)*, 2025.

**Taxonomy of generative IR:**
1. **Generative Document Retrieval (GDR):** Model memorizes corpus in its parameters and
   generates document identifiers given a query (DSI, GENRE, and variants)
2. **Reliable Response Generation (RRG):** Model generates user-facing answers grounded in
   retrieved evidence (RAG systems)

**Key challenges identified:**
- **Corpus dynamics:** GDR models struggle with document addition/deletion (requires
  incremental learning or model re-training)
- **Scalability:** Current GDR models work well on 10K–100K document corpora but
  struggle at web scale (billions of documents)
- **Evaluation:** No consensus on evaluation protocols for generative retrieval — should
  we measure document ID prediction accuracy, end-to-end answer quality, or both?
- **Hallucination:** Both GDR (generating non-existent docids) and RRG (generating
  unsupported claims) face hallucination risks

**Recent advances (2024–2025):**
- MixLoRA-DSI: Dynamically expandable Mixture-of-LoRA experts for handling document
  corpus updates without full retraining (EMNLP 2025)
- DiffuGR: Using diffusion models for generative retrieval (arXiv 2025)
- Distillation-enhanced generative retrieval: Knowledge distillation from large to small
  generative retrievers (ACL 2024 Findings)

**Digest mapping:** Emerging Paradigms > Generative Retrieval [authority: authoritative] [audience: all]

---

### 4. Implications for DS Analysis Review

**How emerging paradigms change DS review criteria:**

| Paradigm | Traditional Evaluation | New Evaluation Needed |
|---|---|---|
| LLM Re-ranking | NDCG, MRR on test sets | Cost-per-query, latency, zero-shot vs. fine-tuned comparison |
| AI Overviews / RAG | CTR, clicks per search | Faithfulness, citation accuracy, answer completeness |
| Agentic Search | Single-query NDCG | Multi-step plan quality, task completion rate, tool selection accuracy |
| Generative Retrieval | Retrieval recall, stage-local metrics | End-to-end HitRate, generation fidelity, hallucination rate |

**Key review questions for emerging paradigm analyses:**
1. Does the analysis acknowledge that traditional metrics may be insufficient?
2. If using LLM-based evaluation (LLM-as-Judge), is the evaluation LLM different from
   the system LLM? (Avoiding circular evaluation.)
3. For AI search: are queries segmented by "AI answer present" vs. "traditional results"?
4. For agentic systems: is the agent's planning evaluated, not just its final output?
5. For generative retrieval: how is hallucination measured and reported?

**Digest mapping:** Emerging Paradigms > DS Review Implications [authority: authoritative] [audience: ds]

---

## Source Index

Quick reference of all cited sources, sorted alphabetically by first author.

| # | Citation | Year | Topic | Type |
|---|---|---|---|---|
| 1 | Ai, Q. et al. "Unbiased Learning to Rank with Unbiased Propensity Estimation." SIGIR 2018. | 2018 | Position bias / IPW | Paper |
| 2 | Algolia. "Query Understanding 101." Algolia Blog. | 2023 | QU pipeline design | Blog |
| 3 | Amazon Science. "Spelling Correction using Phonetics in E-commerce Search." ECNLP 2022. | 2022 | Spell correction | Paper |
| 4 | Arora, A. et al. "Intent Detection in the Age of LLMs." arXiv: 2410.01627. | 2024 | Intent classification | Paper |
| 5 | Broder, A. "A Taxonomy of Web Search." ACM SIGIR Forum 2002. | 2002 | Query classification | Paper |
| 6 | Burges, C. J. C. "From RankNet to LambdaRank to LambdaMART: An Overview." MSR-TR-2010-82. | 2010 | Learning to Rank | Tech Report |
| 7 | Burges, C. J. C. et al. "Learning to Rank Using an Ensemble of Lambda-Gradient Models." JMLR W&CP Vol. 14. | 2011 | LambdaMART benchmark | Paper |
| 8 | Chapelle, O. & Zhang, Y. "A Dynamic Bayesian Network Click Model for Web Search Ranking." WWW 2009. | 2009 | Click models (DBN) | Paper |
| 9 | Chapelle, O. et al. "Expected Reciprocal Rank for Graded Relevance." CIKM 2009. | 2009 | Evaluation metrics (ERR) | Paper |
| 10 | Chapelle, O. et al. "Large-Scale Validation and Analysis of Interleaved Search Evaluation." TOIS 2012. | 2012 | Interleaving experiments | Paper |
| 11 | Chen, C. et al. "An End-to-End Solution for Named Entity Recognition in eCommerce Search." AAAI 2021. | 2021 | Query segmentation / NER | Paper |
| 12 | Chuklin, A. et al. *Click Models for Web Search.* Morgan & Claypool, 2015. | 2015 | Click model survey | Book |
| 13 | Craswell, N. et al. "An Experimental Comparison of Click Position-Bias Models." WSDM 2008. | 2008 | Click models (Cascade) | Paper |
| 14 | De Cao, N. et al. "Autoregressive Entity Retrieval." ICLR 2021. | 2021 | Generative retrieval (GENRE) | Paper |
| 15 | DoorDash Engineering. "How DoorDash is Pushing Experimentation Boundaries with Interleaving Designs." | 2023 | Interleaving in production | Blog |
| 16 | DoorDash Engineering. "How DoorDash Leverages LLMs for Better Search Retrieval." | 2024 | LLM + KG for QU | Blog |
| 17 | Es, S. et al. "RAGAS: Automated Evaluation of Retrieval Augmented Generation." EACL 2024. | 2024 | RAG evaluation | Paper |
| 18 | Etsy Engineering. "Deep Learning for Search Ranking at Etsy." Code as Craft. | 2022 | LTR in production | Blog |
| 19 | Etsy Engineering. "How Etsy Uses LLMs to Improve Search Relevance." Code as Craft. | 2024 | LLMs for ranking | Blog |
| 20 | Grbovic, M. "Machine Learning-Powered Search Ranking of Airbnb Experiences." Airbnb Tech Blog. | 2019 | LTR in production | Blog |
| 21 | Hager, P. et al. "Full Stage Learning to Rank: A Unified Framework for Multi-Stage Systems." WWW 2024. | 2024 | Multi-stage evaluation | Paper |
| 22 | Haldar, M. et al. "Improving Deep Learning for Airbnb Search." KDD 2020. | 2020 | DNN ranking, position bias | Paper |
| 23 | Hao, J. et al. "QueryNER: Segmentation of E-commerce Queries." LREC-COLING 2024. | 2024 | Query segmentation | Paper |
| 24 | Hasan, S. et al. "Spelling Correction of User Search Queries through Statistical Machine Translation." ACL 2015. | 2015 | Spell correction | Paper |
| 25 | Jansen, B. J. et al. "Determining the Informational, Navigational, and Transactional Intent of Web Queries." IPM 2008. | 2008 | Query classification | Paper |
| 26 | Järvelin, K. & Kekäläinen, J. "Cumulated Gain-Based Evaluation of IR Techniques." TOIS 2002. | 2002 | Evaluation metrics (NDCG) | Paper |
| 27 | Joachims, T. et al. "Accurately Interpreting Clickthrough Data as Implicit Feedback." SIGIR 2005. | 2005 | Position bias, eye tracking | Paper |
| 28 | Joachims, T. et al. "Evaluating the Accuracy of Implicit Feedback..." TOIS 2007. | 2007 | Position bias, eye tracking | Paper |
| 29 | Kakkar, H. et al. "Search Query Spell Correction with Weak Supervision in E-commerce." ACL 2023. | 2023 | Spell correction | Paper |
| 30 | Khattab, O. & Zaharia, M. "ColBERT: Efficient and Effective Passage Search..." SIGIR 2020. | 2020 | Neural ranking (ColBERT) | Paper |
| 31 | Kuaishou Research. "OneSug: End-to-End Generative Query Suggestion." arXiv: 2506.06913. | 2025 | Generative retrieval (production) | Paper |
| 32 | Li, Y. et al. "From Matching to Generation: A Survey on Generative Information Retrieval." TOIS 2025. | 2025 | Generative retrieval survey | Survey |
| 33 | LinkedIn Engineering. "Improving Post Search at LinkedIn." | 2022 | Search ranking platform | Blog |
| 34 | Ma, X. et al. "Query Rewriting for Retrieval-Augmented Large Language Models." EMNLP 2023. | 2023 | Query rewriting for RAG | Paper |
| 35 | Netflix Technology Blog. "Innovating Faster on Personalization Algorithms at Netflix Using Interleaving." | 2020 | Interleaving in production | Blog |
| 36 | Nogueira, R. & Cho, K. "Passage Re-ranking with BERT." arXiv: 1901.04085. | 2019 | Neural ranking (BERT) | Paper |
| 37 | Nogueira, R. et al. "Document Ranking with a Pretrained Sequence-to-Sequence Model." arXiv: 2003.06713. | 2020 | Neural ranking (monoT5) | Paper |
| 38 | Nogueira, R. et al. "Multi-Stage Document Ranking with BERT." arXiv: 1910.14424. | 2019 | Multi-stage ranking | Paper |
| 39 | Oosterhuis, H. "Doubly-Robust Estimation for Correcting Position-Bias..." TOIS 2023. | 2023 | Position bias / DR | Paper |
| 40 | Palumbo, E. et al. "You Say Search, I Say Recs: Agentic Query Understanding at Spotify." RecSys 2025. | 2025 | Agentic QU | Paper |
| 41 | Pande, A. et al. "Learning-to-Spell: Weak Supervision based Query Correction." CIKM 2022. | 2022 | Spell correction | Paper |
| 42 | Pinterest Engineering. "Improving Pinterest Search Relevance Using Large Language Models." | 2024 | LLMs for relevance | Blog/Paper |
| 43 | Pinterest Engineering. "SearchSage: Learning Search Query Representations at Pinterest." | 2021 | Query embeddings | Blog |
| 44 | Richardson, M. et al. "Predicting Clicks: Estimating the Click-Through Rate for New Ads." WWW 2007. | 2007 | Click models (PBM) | Paper |
| 45 | Seer Interactive. "AIO Impact on Google CTR." | 2025 | AI Overviews impact | Industry Study |
| 46 | Singh, A. et al. "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG." arXiv: 2501.09136. | 2025 | Agentic search survey | Survey |
| 47 | Song, R. et al. "RaFe: Ranking Feedback Improves Query Rewriting for RAG." EMNLP 2024 Findings. | 2024 | Query rewriting | Paper |
| 48 | Sun, W. et al. "Is ChatGPT Good at Search? LLMs as Re-Ranking Agents." EMNLP 2023. | 2023 | LLM re-ranking (RankGPT) | Paper |
| 49 | Tay, Y. et al. "Transformer Memory as a Differentiable Search Index." NeurIPS 2022. | 2022 | Generative retrieval (DSI) | Paper |
| 50 | Tunkelang, D. "Precision, Recall, and Desirability." Medium/LinkedIn. | 2023 | Search evaluation philosophy | Blog |
| 51 | Wang, X. et al. "Learning to Rank with Selection Bias in Personal Search." SIGIR 2016. | 2016 | Position bias / IPW | Paper |
| 52 | Wang, Y. et al. "Redefining Retrieval Evaluation in the Era of LLMs." arXiv: 2510.21440. | 2025 | RAG evaluation (UDCG) | Paper |
| 53 | Williams, H. E. "Query Rewriting in Search Engines." Blog post. | 2012 | Query rewriting | Blog |
| 54 | Zhang, Q. et al. "Beyond A/B Test: Speeding up Airbnb Search Ranking Experimentation through Interleaving." Airbnb Tech Blog / KDD 2025. | 2022/2025 | Interleaving in production | Blog/Paper |
| 55 | Zhang, Y. et al. "RAG Evaluation in the Era of LLMs: A Comprehensive Survey." arXiv: 2504.14891. | 2025 | RAG evaluation survey | Survey |
