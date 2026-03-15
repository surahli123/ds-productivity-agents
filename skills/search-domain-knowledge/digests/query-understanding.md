# query-understanding domain digest
# Version: 2026-02-21T14:30:00Z
# Previous: none
# Token budget: 8000
# Audience tags: all, ds, eng

---

## Foundational Knowledge [authority: authoritative] [audience: all]

This section covers the core concepts, evaluation standards, and methodology that anyone
working in query understanding should know — DS, engineering, and PM alike. These are
established facts from peer-reviewed research and major production deployments. Contradicting
this content in an analysis review indicates a foundational knowledge gap.

### Query Classification: Broder's Taxonomy

The foundational classification of web search queries divides them into three intent
categories (Broder, 2002):

1. **Informational:** The user wants to learn something (e.g., "how does NDCG work"). No
   further interaction beyond reading is expected. This is the dominant category.
2. **Navigational:** The user wants to reach a specific website (e.g., "airbnb login").
   Typically has a single "right" answer.
3. **Transactional:** The user wants to perform an action — purchase, download, sign up
   (e.g., "buy running shoes").

**Query distribution:** Broder's original self-reported distribution was approximately 73%
informational, 26% navigational, 36% transactional (percentages exceed 100% because some
queries were classified into multiple categories). Jansen et al. (2008) operationalized
this taxonomy at scale, analyzing over 1.5 million queries from search engine logs with an
automated classification algorithm achieving 74% accuracy. Their refined distribution:
**80%+ informational, ~10% navigational, ~10% transactional.**

**Why informational dominance matters:** Because informational queries make up 80%+ of
search traffic, evaluation metrics designed for informational search — like NDCG over
graded relevance — tend to drive the most business impact. Any query classification system
that doesn't acknowledge Broder's three categories, or explain why its taxonomy differs, is
likely missing foundational context. The distribution also means that investments in
informational query understanding (broader topic matching, entity disambiguation, intent
refinement) have disproportionate ROI compared to navigational or transactional
optimizations.

### Query Segmentation

Query segmentation (also called query parsing or query tagging) breaks a search query into
meaningful semantic units. For example, "blue check casual shirt for men" becomes:
color=blue, pattern=check, style=casual, product_type=shirt, gender=men. Getting
segmentation right is critical because **QU errors have larger impact than ranking errors** —
if the system misidentifies "apple" as a fruit when the user meant the brand, downstream
ranking cannot recover regardless of how sophisticated the ranking model is.

**Key references:**

- **QueryNER dataset** (Hao et al., LREC-COLING 2024): Introduces a manually-annotated
  dataset for e-commerce query segmentation. E-commerce queries are noisier and more
  unstructured than traditional NER text. The dataset proposes broadly applicable entity
  types rather than domain-specific categories, enabling cross-domain query segmentation
  research.

- **TripleLearn** (Chen et al., AAAI 2021): An end-to-end NER framework for e-commerce
  search, deployed on homedepot.com for 9+ months. Uses an iterative learning approach
  across three separate training datasets. Online A/B tests showed significant improvements
  in user engagement and revenue conversion. This demonstrates that production-grade query
  segmentation delivers measurable business impact, not just academic metric gains.

**Reviewer check:** Any analysis that evaluates ranking improvements without verifying that
query segmentation is correct upstream is potentially measuring the wrong thing. A +2%
NDCG gain from a ranking model change may actually be attributable to (or masked by) query
segmentation quality.

### Spell Correction Fundamentals

Spell correction involves a fundamental **precision-recall tension:**

- **Aggressive correction** (high recall): Catches more typos but risks "correcting" valid
  queries — e.g., correcting a brand name the system doesn't recognize. This is particularly
  dangerous in e-commerce where brand names and product terms are often unusual words.
- **Conservative correction** (high precision): Only corrects clear misspellings but misses
  non-obvious errors like phonetic misspellings and transliteration errors.

**Scale of the problem:** Approximately **32% of e-commerce queries contain spelling
mistakes** (Pande et al., CIKM 2022). This is not a niche issue — it affects roughly one
in three queries. The error distribution in e-commerce differs significantly from web
search: phonetic errors (influenced by spoken accents), transliteration errors (from
non-Latin scripts), and brand-specific terms that look like misspellings to generic models
all contribute.

**Evaluation dimensions:**
- **Detection precision:** Of all queries flagged as misspelled, how many actually are?
- **Detection recall:** Of all misspelled queries, how many were detected?
- **Correction accuracy:** Of detected misspellings, how many were corrected to the right term?
- **End-to-end impact:** Does spell correction improve downstream search metrics (CTR, NDCG)?

**Common error:** Evaluating spell correction in isolation (intrinsic accuracy) without
measuring downstream impact on search quality. A spell corrector with 95% accuracy can
still hurt search if the 5% errors involve high-traffic brand names or product terms.

### Query Rewriting in Production

Query rewriting encompasses several techniques typically applied in a pipeline:

- **Synonym expansion:** Adding related terms to improve recall (e.g., "couch" → "couch OR
  sofa"). Broadens the match set but can reduce precision if synonyms are too loose.
- **Query relaxation:** Removing overly restrictive terms when results are sparse. Useful
  for long-tail queries that return zero results.
- **Query augmentation:** Adding context from user signals — location, session history,
  personalization features. Enriches the query without changing the user's explicit intent.
- **Semantic rewriting:** Replacing the surface-level query with a semantically equivalent
  form better suited for retrieval (e.g., "cheap flights NYC to LA" → "affordable airfare
  New York Los Angeles").

**Pipeline ordering matters.** The order of QU techniques has significant impact on quality
(ref: Algolia, "Query Understanding 101"). The canonical ordering is: spell correction →
synonym expansion → query relaxation → semantic rewriting. Violating this ordering creates
compounding errors:

- Applying **synonym expansion before spell correction** amplifies errors — a misspelled
  word gets expanded into synonyms of the wrong term, and the error propagates to every
  downstream stage.
- Applying **query relaxation too aggressively** reduces precision — dropping a key
  qualifier from "red nike running shoes" may return all running shoes, not just red Nikes.
- Applying **semantic rewriting before intent detection** may transform the query in a way
  that obscures the original intent signal.

Most production systems use a sequential pipeline where each stage's output becomes the next
stage's input, with quality gates between stages. If a stage has low confidence in its
output, it passes the input through unmodified rather than risk a bad transformation
cascading downstream.

### Intent Classification

Transformer-based models have become the standard for intent classification:

| Model | Dataset | Accuracy | Notes |
|---|---|---|---|
| Joint BERT (Chen et al.) | ATIS | >97% | Joint intent + slot filling |
| Joint BERT | Snips | ~98.6% | Surpasses RNN-attention and slot-gated models |
| DistilBERT | Various | Near BERT-level | 40% smaller, 60% faster, minimal accuracy loss |

**LLM-based intent detection (2024+):** Recent work evaluates LLMs (GPT-4, Claude, Llama)
for intent detection in task-oriented dialogue. LLMs achieve competitive accuracy with
zero/few-shot prompting but at significantly higher latency and cost compared to fine-tuned
BERT classifiers (Arora et al., 2024). The performance-latency tradeoff is the key decision
factor:

- **LLMs excel at:** Labeling training data at scale, handling long-tail or ambiguous
  queries where fine-tuned models lack coverage, and bootstrapping intent taxonomies for
  new domains where no labeled data exists.
- **Fine-tuned BERT/DistilBERT excels at:** Production serving where latency is constrained
  to single-digit milliseconds, high-throughput classification, and cost efficiency at
  scale (orders of magnitude cheaper per query than LLM inference).
- **The practical architecture:** Use LLMs offline to generate training labels, then train
  a smaller model for production. This "LLM-as-labeler" pattern is increasingly standard
  (see Workstream Standards section for Pinterest's deployment of this pattern).

---

## Foundational Knowledge [authority: authoritative] [audience: ds]

DS-specific methodology: evaluation approaches, spell correction nuances, and operationalization
details that a data scientist working in query understanding should master. This section assumes
familiarity with the concepts in the [audience: all] section above.

### Query Rewriting Evaluation: Intrinsic vs. Downstream

Query rewriting can be evaluated two fundamentally different ways, and the choice matters:

1. **Intrinsic evaluation:** How well does the rewrite match a "gold standard" query? Measured
   via BLEU score, exact match rate, or manual judgment. Fast to compute, easy to set up, but
   can be misleading — a rewrite that scores high on BLEU may not improve retrieval at all.

2. **Downstream evaluation:** How much does the rewrite improve retrieval quality? Measured
   via NDCG/MRR change on the rewritten query vs. the original. More reliable but harder to
   set up because it requires running the full retrieval pipeline.

**Key finding:** Downstream evaluation is more reliable. Ma et al. (EMNLP 2023) demonstrate
that query rewriting significantly improves RAG pipeline accuracy when evaluated end-to-end
— but the intrinsic quality of the rewrite (measured by text similarity to a reference) is
only weakly correlated with downstream improvement. Song et al. (2024) show that using
ranking feedback to iteratively improve query rewrites (evaluated via downstream retrieval
metrics) produces better rewrites than optimizing intrinsic quality directly.

**Red flag for reviewers:** An analysis that evaluates query rewriting quality using only
intrinsic metrics (BLEU, edit distance) without measuring downstream impact on search metrics
is incomplete. The rewrite may look good on paper but fail to improve — or even hurt — actual
search results. Always ask: "What happened to NDCG/MRR when this rewrite was applied?"

**Decision guide — which evaluation when:**

| Evaluation Type | Use When | Limitation |
|---|---|---|
| Intrinsic (BLEU, exact match) | Fast iteration during development | Weak correlation with actual search quality |
| Downstream (NDCG/MRR change) | Launch decisions, experiment reports | Requires full retrieval pipeline, slower |
| Hybrid (intrinsic for dev, downstream for launch) | Best practice for production teams | More infrastructure to maintain |

### Spell Correction in E-Commerce

E-commerce spell correction is a distinct challenge from web search spell correction. The
error distribution differs significantly, and off-the-shelf solutions trained on web data
underperform.

**Error classes:**
- **Typos:** Standard keyboard errors (adjacent key hits, transpositions). The easiest class
  to correct with traditional edit-distance methods.
- **Phonetic errors:** Users type what they hear, influenced by spoken accents. "fone" for
  "phone," "nife" for "knife." These require phonetic similarity models, not just edit
  distance.
- **Transliteration errors:** Users typing product names from non-Latin scripts in Latin
  characters. Common in multilingual e-commerce where the same product may be searched in
  multiple languages.

**Key finding:** Generic spell correction models trained on clean English web data perform
poorly on e-commerce queries with phonetic and vernacular errors (Amazon Science, ECNLP
2022). The phonetic similarity integration addresses accented errors without adding latency
to the correction pipeline.

**Weak supervision approach:** Kakkar et al. (ACL 2023) demonstrate that weak supervision
with curriculum learning can significantly reduce the need for expensive human-labeled spell
correction data. Synthetic data generation overcomes limited labeled examples, and curriculum
learning handles the progression from easy (clear typos) to hard (phonetic, transliteration)
correction tasks. This is practically important because labeling spell correction data
requires linguists, not general annotators — a single misspelling can have multiple valid
corrections depending on context, making annotation expensive and slow.

**Practical implication for DS:** When building or evaluating a spell correction system for
e-commerce, always test on domain-specific error distributions — not just standard spelling
benchmark datasets. Web search spell correction benchmarks under-represent the phonetic and
transliteration errors that dominate e-commerce queries.

### Jansen's Operationalization of Intent Classification

Jansen et al. (2008) analyzed 1.5 million queries with an automated classification algorithm
achieving **74% accuracy** against manual labels. Two key methodological insights for DS:

1. **Self-reported intent vs. observed behavior differ significantly.** Broder's original
   distribution was based on user surveys (self-reported intent), while Jansen used log-based
   behavioral classification. The gap (Broder: 73/26/36 vs. Jansen: 80/10/10) illustrates
   that what users *say* they want and what their queries *reveal* about their intent are
   different. DS analysts should be cautious about how intent labels are generated — survey-
   based labels are systematically different from log-based labels.

2. **Hierarchical sub-categories exist within each intent class.** Informational queries
   alone subdivide into directed (specific fact-seeking), undirected (exploratory browsing),
   advice-seeking, and find-type queries. This matters for evaluation design: aggregating
   all informational queries into one bucket may mask performance differences across
   sub-categories. A ranking improvement that helps directed informational queries may hurt
   undirected exploratory queries — and aggregate metrics won't reveal this.

**Reviewer check:** When reviewing intent classification work, always check how labels were
generated (self-reported surveys, observed log behavior, annotator judgment, or automated
classification). Each method has known biases, and the label generation method should be
documented and justified.

---

## Foundational Knowledge [authority: authoritative] [audience: eng]

Engineering-specific standards for query understanding infrastructure: pipeline architecture
and latency considerations that shape what is practically possible in production QU systems.

### QU Pipeline Architecture

The standard production QU pipeline processes queries through sequential stages, where each
stage's output feeds the next. Stage ordering is critical because errors compound downstream:

```
User Query
  → Tokenization (normalize whitespace, casing, special characters)
  → Spell Correction (fix misspellings before expanding)
  → Synonym Expansion (broaden the corrected query)
  → Intent Detection (classify the expanded query's intent)
  → Query Rewriting (final transformation for retrieval)
  → Retrieval System
```

**Why ordering matters (engineering perspective):**
- Spell correction **must** precede synonym expansion. If "nife" gets expanded before
  correction, the system may expand a misspelling into irrelevant synonyms.
- Intent detection benefits from running after spell correction and expansion because
  the cleaned, expanded query provides stronger signal for classification.
- Quality gates between stages prevent error propagation: if spell correction confidence
  is below threshold, pass the original query through unmodified rather than risk a bad
  correction cascading through all downstream stages.

### Production Latency Considerations

For production query understanding, the latency budget is tight because QU runs before
retrieval and ranking — every millisecond added to QU delays the entire search response.

**Model choice for production serving:**
- **Fine-tuned BERT/DistilBERT** is the dominant choice for intent classification and
  query classification in production. DistilBERT offers 40% size reduction and 60% speed
  improvement over BERT with minimal accuracy loss — this tradeoff is almost always worth
  taking in production.
- **LLMs (GPT-4, Claude, etc.)** are too slow for serving-time QU at scale. Typical LLM
  inference adds seconds per query, far exceeding the millisecond-level QU latency budget.
  However, LLMs are highly effective for **offline labeling** — generating training data
  for the smaller models that actually serve in production.

**The LLM-as-labeler pattern:** Use LLMs to generate high-quality intent labels and query
classification labels offline. Train a smaller, faster model (BERT, DistilBERT) on these
LLM-generated labels for production serving. This gives you LLM-quality labels at
DistilBERT-level latency. Pinterest has deployed this pattern successfully for search
relevance (ref: Pinterest Engineering, 2024).

---

## Workstream Standards [authority: authoritative] [audience: all]

Team decisions and production standards drawn from published engineering case studies.
These represent the kind of choices a query understanding team makes and ratifies —
architecture decisions, methodology standards, and tooling choices. Real entries are cited
from public engineering blog posts; synthetic entries are labeled [DEMO] to demonstrate how
internal team decisions would be documented.

### Pinterest SearchSage: Query Embedding Architecture

Pinterest's SearchSage learns a query embedding in the same space as PinSage (pin
embeddings) using a **two-tower architecture** with the candidate tower frozen. This replaced
the prior approach of representing queries as clusters of historically-engaged pin
embeddings — a common but brittle pattern that fails for new and rare queries.

**Results:** 11% increase in 35s+ click-throughs on product Pins in search, 42% increase in
related searches. Now used for 15+ use cases across organic and ads ranking.

**Evolution:** OmniSearchSage (2024) unifies query, pin, and product embeddings into a single
embedding space, yielding **>8% relevance improvement, >7% engagement, >5% ads CTR**
improvements. The progression from separate embeddings → unified embedding space is a
recurring architecture pattern in production search systems.

(ref: Pinterest Engineering, "SearchSage: Learning Search Query Representations at Pinterest,"
2023; OmniSearchSage, 2024)

### DoorDash: LLM + Knowledge Graph for Query Understanding

DoorDash combined LLMs with a knowledge graph for query segmentation and entity linking. The
architecture uses **RAG to constrain LLM outputs to a controlled vocabulary**, preventing
hallucinated entity names. The LLM processes the query, the knowledge graph grounds entities
to canonical forms, and the retrieval system fetches results using the grounded entities.

**Results:** 30% improvement in popular dish carousel trigger rate, >2% whole-page relevance
increase, and higher conversion rates. Key QU tasks addressed: query rewriting, entity
disambiguation, and search path recommendation.

**Architecture lesson:** Using RAG to constrain LLM generation to known entities is a
practical pattern for deploying LLMs in QU without hallucination risk. The knowledge graph
acts as a guardrail, not just a data source. Without this constraint, the LLM might generate
plausible but non-existent entity names (e.g., inventing a restaurant name that sounds
real but doesn't exist in the catalog), which would produce zero results and a poor user
experience.

**Decision guide for LLM + KG architecture:** This pattern works best when (1) the entity
catalog is well-defined and maintained, (2) query ambiguity is the primary QU challenge
(rather than recall), and (3) the team can invest in knowledge graph maintenance alongside
the LLM pipeline.

(ref: DoorDash Engineering, "How DoorDash Leverages LLMs for Better Search Retrieval," 2024)

### Spotify: Parallel Fusion Router for Agentic QU

Spotify proposed a **Parallel Fusion Router (PFR)** architecture — an intermediate design
between simple rule-based routing and full LLM orchestration. The LLM router enriches
queries with temporal, genre, and entity-type filters (e.g., "new indie rock releases" →
adds time filter, genre facet, content-type facet).

**Key scalability decision:** Pass **only the query** (not user features) to the LLM router
to maximize cache hit rate. This keeps latency low because identical queries hit the cache
regardless of which user issued them. Sub-agents invoke LLMs only when necessary (external
knowledge, complex reasoning, SERP refinement); otherwise they use traditional ML
retrievers/rankers.

This represents the trend of **agentic QU** — treating query understanding as a planning
problem rather than a classification problem. Instead of asking "what intent class does this
query belong to?", agentic QU asks "what enrichments, filters, and retrieval strategies will
best satisfy this query?" This shift is particularly relevant for exploratory and ambiguous
queries where a single intent classification is insufficient.

**Trade-off:** Agentic QU adds architectural complexity. The PFR pattern mitigates this by
keeping LLM invocations optional (cache-first) and limiting the LLM's scope to query-level
enrichment rather than full session reasoning.

(ref: Palumbo et al., "You Say Search, I Say Recs: A Scalable Agentic Approach to Query
Understanding and Exploratory Search at Spotify," RecSys 2025)

### [DEMO] Query Rewriting Evaluation Standard

[DEMO] **Team decision (2025-Q4):** All query rewriting experiments must measure downstream
NDCG/MRR impact, not just intrinsic BLEU scores. Rationale: multiple experiments showed
weak correlation between BLEU improvement and actual search quality change. A rewrite
scoring +0.15 BLEU showed no NDCG lift, while a rewrite scoring -0.02 BLEU (slightly
different from reference) showed +1.3% NDCG@10. Intrinsic-only evaluation is now flagged
as incomplete in experiment reviews.

### [DEMO] Spell Correction Deployment Threshold

[DEMO] **Team decision (2025-Q3):** Spell correction models require **detection precision >
98%** before production deployment. Rationale: a false positive on a high-traffic brand
query (e.g., "correcting" a valid brand name to something else) has outsized negative impact
because it affects every user who searches for that brand. The 98% threshold was calibrated
by estimating the revenue impact of miscorrecting the top-100 brand queries. Recall
improvements are evaluated separately and launched only after the precision gate is met.

---

## Workstream Learnings [authority: advisory] [audience: ds]

Lessons from production experiments and post-mortems — the kind of hard-won knowledge that
doesn't appear in textbooks. Published results are cited; synthetic entries are labeled
[DEMO]. These carry advisory authority: they reflect what specific teams learned in specific
contexts. Your context may differ, but these patterns are worth knowing.

### Pinterest: LLM-as-Labeler for Search Relevance

Pinterest used LLMs to generate relevance labels for training ranking and QU models at
scale, replacing expensive human annotation. The key insight is the **LLM-as-labeler
pattern**: LLMs generate training labels offline, and a smaller, faster model (fine-tuned
BERT or similar) is trained on those labels for production serving. This avoids serving-time
LLM costs entirely while capturing LLM-quality understanding in the training data.

**Practical implications for DS review:**
- When evaluating a QU model's training pipeline, check whether the labels were
  human-generated, LLM-generated, or a hybrid.
- LLM-generated labels at scale can outperform small human-labeled datasets because
  coverage matters more than per-label accuracy for training, especially on long-tail
  queries where human annotators lack context.
- The quality of LLM-generated labels should still be validated via human spot-checking on
  a random sample — LLMs can have systematic biases (e.g., over-classifying ambiguous
  queries as informational) that distort the training distribution.

(ref: Pinterest Engineering, "Improving Pinterest Search Relevance Using Large Language
Models," 2024; also arXiv: 2410.17152)

### [DEMO] Query Expansion A/B: Brand Query Precision Loss

[DEMO] **Post-mortem (2025-Q4):** An aggressive query expansion model was launched to
improve recall on broad informational queries. The model expanded queries by adding
semantically related terms (e.g., "running shoes" → "running shoes OR athletic footwear
OR jogging sneakers"). Overall NDCG@10 improved +0.8%, but a segment analysis revealed that
**brand queries lost -3.2% precision** — "Nike running shoes" was being expanded to include
non-Nike results. The expansion was rolled back for brand-detected queries while kept active
for non-brand segments. Resolution: added a brand-detection gate before the expansion stage.
If the query contains a recognized brand entity, expansion is suppressed or limited to
within-brand synonyms only.

**Lesson:** Query expansion effects must be analyzed by query segment, not just in
aggregate. Brand queries and non-brand queries have fundamentally different expansion needs.
Aggregate metric improvements can mask significant harm to specific high-value segments.

### [DEMO] Intent Classifier Migration: Rule-Based to BERT

[DEMO] **Post-mortem (2026-Q1):** Migrated the production intent classifier from a rule-
based system (~500 hand-written rules) to a fine-tuned BERT classifier. Overall intent
accuracy improved from 81% to 93%. However, the BERT classifier introduced regressions on
**multilingual queries** — queries mixing two languages (e.g., English + Spanish) were
classified with only 62% accuracy compared to the rule-based system's 78%. The rule-based
system had explicit rules for common bilingual patterns that the BERT model hadn't seen
enough of in training data. Resolution: added a language-detection pre-filter that routes
multilingual queries to a fallback rule-based classifier while BERT handles monolingual
queries. The hybrid system achieves 91% overall accuracy with 76% on multilingual queries.

**Lesson:** Model migrations from rule-based to ML should include segment-level regression
analysis, not just aggregate accuracy comparison. Rules often encode edge-case knowledge
that ML models won't learn from data unless those edge cases are well-represented in
training data. A hybrid approach (ML for the head, rules for the tail) is often the
practical outcome. This mirrors a common pattern in search: ML models handle the head of the
query distribution well, but the long tail — which may account for 30-40% of unique queries —
often requires specialized handling that rules or separate models provide.

---

## Conflicts

This section documents cases where workstream knowledge overrides foundational guidance.
Workstream takes precedence per the Knowledge Tier Precedence rules (SKILL.md Section 6),
because the team's direct experimental evidence is more informative for their specific
context than general principles.

### [DEMO] Spell Correction Evaluation Override

**CONFLICT:**

- **Foundational says:** "Evaluate spell correction by intrinsic accuracy — detection
  precision, detection recall, and correction accuracy" (standard evaluation framework from
  the spell correction literature, including Hasan et al., 2015).

- **Workstream standard says:** "Only downstream search metric impact matters for
  spell correction evaluation." The team's experience is that a spell corrector with 95%
  intrinsic accuracy can still hurt search if the 5% errors involve high-traffic brand
  names. Intrinsic accuracy is tracked as a diagnostic but launch decisions are based solely
  on downstream NDCG/CTR impact.

- **Resolution:** Workstream takes precedence for launch decisions. Intrinsic metrics remain
  useful for model debugging and development iteration (they're faster to compute), but they
  are not sufficient for go/no-go decisions. Flagged for foundational review — consider
  updating the foundational guidance to explicitly recommend both intrinsic and downstream
  evaluation, with downstream as the decision metric.
