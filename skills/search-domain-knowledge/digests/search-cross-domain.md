# search-cross-domain domain digest
# Version: 2026-02-21T14:30:00Z
# Previous: none
# Token budget: 1500
# Audience tags: all, ds, eng

---

## Foundational Knowledge [authority: authoritative] [audience: all]

This section covers evaluation concepts that span across search domains — pipeline-level
evaluation, offline-to-online alignment, and emerging RAG metrics. These apply regardless of
whether you are working on ranking, query understanding, or another search component. This
digest is always loaded alongside domain-specific digests (see SKILL.md Section 2).

### Multi-Stage Pipeline Evaluation

Modern search systems use multi-stage pipelines: retrieval (candidate generation) →
pre-ranking → ranking → re-ranking. Each stage introduces **selection bias** — the upstream
stage determines what the downstream stage sees. Hager et al. (WWW 2024) formalize this
with the Generalized Probability Ranking Principle (GPRP), showing that each stage's model
only needs to rank well enough to pass its best candidates to the next stage, not rank the
entire candidate set perfectly.

**Why this matters:** Improvements at one stage may not surface in end-to-end metrics if
another stage compensates. A retrieval-stage recall improvement may not change NDCG@10 if
the re-ranker was already finding the relevant documents through a different path.
Conversely, a re-ranking improvement may be bottlenecked by poor retrieval upstream.
Understanding which stage is the bottleneck requires cross-stage metric attribution, not
just stage-local evaluation.

The standard multi-stage architecture pattern (Nogueira et al., 2019) is:
1. **Retrieval (Stage 0):** Fast, broad methods (BM25, ANN search) over the full index.
   Returns hundreds to low thousands of candidates.
2. **Pre-ranking (Stage 1):** Lightweight model (GBDT, small neural model) narrows to
   top ~100 candidates.
3. **Ranking (Stage 2):** Expensive model (cross-encoder BERT, T5) scores top ~100.
4. **Re-ranking (Stage 3):** Business logic, diversity, freshness adjustments on top ~20.

### End-to-End Evaluation Framework

The practical approach to search evaluation uses a three-stage process:

1. **Offline iterations** — Use NDCG, MRR, and Recall on held-out test sets for fast model
   development and feature selection. This is where most iteration happens.
2. **Interleaving validation** — Use interleaving experiments (10-100x more sensitive than
   A/B tests) to validate that offline gains translate to online preference. This prunes
   bad candidates quickly with minimal traffic.
3. **A/B testing for launch** — Run full A/B tests on surviving candidates for final launch
   decisions with complete business metrics (revenue, conversion, engagement).

**Offline-online metric correlation** should be tracked over time. If offline metric
improvements stop predicting online wins, the offline evaluation setup needs recalibration
— typically the relevance labels are stale, the test query distribution has drifted, or
user behavior has shifted (Chapelle et al., 2012).

### RAG Evaluation

As search systems incorporate generative components (AI Overviews, RAG-based answers),
traditional IR metrics alone are insufficient. RAGAS (Es et al., EACL 2024) provides a
framework for evaluating RAG pipelines without requiring human reference answers:

- **Faithfulness:** Is the generated answer factually grounded in the retrieved context?
- **Answer Relevancy:** Does the answer address the query?
- **Context Precision:** Are the retrieved documents relevant (signal-to-noise ratio)?
- **Context Recall:** Was all necessary information retrieved?

**Beyond NDCG for RAG:** Wang et al. (2025) introduce UDCG (Utility and Distraction-aware
Cumulative Gain), a metric designed specifically for RAG systems. UDCG correlates **36%
better** with end-to-end RAG accuracy than traditional NDCG. The key insight: NDCG
optimizes for human scanning behavior (logarithmic position discount), while UDCG optimizes
for LLM consumption of retrieved documents — a fundamentally different access pattern.

---

## Foundational Knowledge [authority: authoritative] [audience: ds]

DS-specific methodology for cross-component evaluation: attribution methods and the
offline-online gap that data scientists must navigate when evaluating search system changes.

### Component-Level Attribution

When end-to-end search quality changes, the critical question is *which component was
responsible* — retrieval, ranking, query understanding, or blending? "NDCG went up 2%"
is incomplete without component attribution.

**Attribution methods in practice:**
- **Ablation studies:** Turn off or randomize one component while keeping others fixed.
  Measures the marginal contribution of each component. Most rigorous but requires the
  ability to isolate components.
- **Counterfactual evaluation:** Use logged data to estimate what would have happened
  with a different component. Related to offline A/B testing and counterfactual LTR.
- **Stage-local metrics:** Measure each stage independently (retrieval recall@1000,
  ranking NDCG@10, QU intent accuracy). Risk: stage-local improvements may not translate
  to end-to-end gains due to cross-stage compensation.
- **Error analysis:** Manually inspect failure cases and classify root cause by component.
  Most reliable but least scalable.

**Reviewer check:** Any analysis reporting end-to-end metric movement without component
attribution should be questioned. The improvement could be coming from an unexpected
component, or multiple components could be interacting in ways that aggregate metrics hide.

### Offline vs. Online Metric Alignment

Three factors create the gap between offline metrics (NDCG/MRR on test sets) and online
metrics (CTR, conversion, engagement):

1. **Label quality:** Offline metrics assume relevance labels are correct. In practice,
   labels are noisy (annotator disagreement), biased (position bias in click labels), or
   incomplete (missing relevant documents). A model that optimizes for noisy labels may not
   optimize for true relevance.
2. **User behavior complexity:** Real users exhibit position bias, query reformulation,
   session-level learning effects, and satisfaction signals that static test sets cannot
   capture. A ranking change may alter user behavior in ways that offline evaluation
   cannot predict.
3. **Feature distribution shift:** Training and test data may not match the production query
   distribution. Seasonal shifts, trending queries, and evolving user demographics create
   ongoing drift.

**Practical guidance:** Track offline-to-online correlation as a meta-metric. When the
correlation degrades, recalibrate the offline setup: refresh labels, update the test query
sample, and verify feature distributions match production. Teams that ignore this drift
gradually lose the ability to iterate offline and become dependent on slow, expensive
online experiments.

---

## Foundational Knowledge [authority: authoritative] [audience: eng]

Brief engineering-specific notes on cross-domain latency constraints.

### Latency Budgets per Pipeline Stage

Each stage of the multi-stage search pipeline operates under a distinct latency budget.
These are approximate targets based on published production constraints:

| Stage | Latency Budget | Candidate Pool |
|---|---|---|
| Retrieval (Stage 0) | <50ms total | Full index → hundreds/thousands |
| Pre-ranking (Stage 1) | <30ms total | Hundreds → ~100 |
| Ranking (Stage 2) | <200ms total | ~100 → top ~20 |
| Re-ranking (Stage 3) | <50ms total | ~20 → final order |

The end-to-end budget for the full pipeline is typically **250ms** (see search-ranking
digest for Etsy's published constraint). Cross-reference the search-ranking digest
[audience: eng] section for detailed latency architecture and the LinkedIn multi-aspect
ranker case study.

---

*Cross-domain content is foundational-only in MVP. Workstream Standards, Workstream
Learnings, and Conflicts sections will be added when team-specific cross-component
learnings are available.*
