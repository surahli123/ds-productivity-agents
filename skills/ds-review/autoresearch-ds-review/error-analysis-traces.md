# Error Analysis Traces: ds-review

**Phase:** 2 (Gulf of Comprehension)
**Date started:** 2026-03-21
**Method:** Run ds-review (inline, full mode, no --domain) on diverse fixtures. User reads every output and judges Pass/Fail. Failure notes are observations, not explanations.

## Trace Log

| Trace | Fixture | Pass/Fail | What went wrong |
|-------|---------|-----------|-----------------|
| T-01 | real/vanguard-ab-test | Pass | Scoring could be improved (minor) |
| T-02 | real/meta-posttreatment-variables | Pass | Score too high — should be ~90-95, not 95. Good review but slightly inflated. |
| T-03 | real/kaggle-ibm-churn-lowquality | Pass | Scoring could be improved (minor) |
| T-04 | syn/04-contradicts-data | Pass | Scoring could be improved (minor). Caught planted contradiction. |
| T-05 | syn/08-unstructured-text | **FAIL** | Review missed the fundamental flaw: document lacks narrative synthesis — it's all tables and segment profiles without a summative story explaining what it all means. Review flagged individual structural issues (no headings, jargon, too detailed) but never identified the overarching problem. Gave 83/100 Good to Go for a document that is a data dump without narrative. Mixture of: (a) review didn't connect individual findings into a coherent meta-assessment, and (b) review didn't catch that the source doc fails to synthesize its own data into a narrative. |

## Fixture Set (22 total — first batch of 5 this session)

### Batch 1 (Session 2026-03-21)
1. real/vanguard-ab-test — known baseline
2. real/meta-posttreatment-variables — high quality prescriptive
3. real/kaggle-ibm-churn-lowquality — low quality stress test
4. syn/04-contradicts-data — planted contradictions
5. syn/08-unstructured-text — no headings

### Batch 2 (Next session)
6. real/meta-llm-bug-reports
7. real/meta-llm-product-analytics
8. real/meta-asymmetric-experiments
9. real/capstone-customer-churn
10. real/kaggle-house-prices-eda
11. real/kaggle-titanic-solutions
12. real/atlassian-rovo-search-relevance

### Batch 3 (Next session continued)
13. real/tips-regression-analysis
14. real/rossmann-sales-prediction
15. real/credit-card-churn-segmentation
16. syn/01-no-tldr
17. syn/03-good-analysis-bad-comms
18. syn/05-data-dump
19. syn/07-partial-input-bullets
20. real/airbnb-search-interleaving
21. real/eppo-search-ranking-experiments
22. syn/02-causal-without-method

## Trace Summaries (Batch 1)

Full outputs presented in-session. Key data persisted here for durability.

### T-01: real/vanguard-ab-test
- **Score:** 54/100 — ❌ Major Rework (3 CRITICALs, floor rule)
- **Analysis:** 51/100 (raw: 73→56.5 DR, credits: +7)
- **Communication:** 57/100 (raw: 51→45.5 DR, credits: +2)
- **Top 3:** (1) ❌ Unstated critical assumptions (-20), (2) ❌ No statistical validation (-15), (3) ❌ TL;DR absent (-12)
- **Total findings:** 13 (6 analysis, 7 communication), displayed 10
- **Key observations:** All 3 hypotheses lack p-values/CIs. H2 conclusion contradicts data (test group slower, not faster). Error rate finding has no actual numbers. No segment analysis despite rich demographics. No limitations section.
- **Pass/Fail:**
- **User notes:**

### T-02: real/meta-posttreatment-variables
- **Score:** 95/100 — ✅ Good to Go
- **Analysis:** 100/100 (raw: 8→8 DR, credits: +13, capped)
- **Communication:** 90/100 (raw: 23→23 DR, credits: +13)
- **Top 3:** (1) 🔴 Scope unclear for downstream (-10), (2) 🔴 Over-interpretation boundary unclear (-8), (3) 🔴 Simulation lacks reproducibility (-8)
- **Total findings:** 5 (1 analysis, 4 communication)
- **Key observations:** High-quality prescriptive article on posttreatment bias. Sound causal reasoning. TL;DR effective. Main gaps: recommendations not scoped to randomized experiments, simulation DGP not documented, formatting artifacts from Medium export.
- **Pass/Fail:**
- **User notes:**

### T-03: real/kaggle-ibm-churn-lowquality
- **Score:** 49/100 — ❌ Major Rework (3 CRITICALs, floor rule)
- **Analysis:** 43/100 (raw: 88→64 DR, credits: +7)
- **Communication:** 54/100 (raw: 56→48 DR, credits: +2)
- **Top 3:** (1) ❌ No holdout — model trained on full dataset (-20), (2) ❌ TL;DR absent (-12), (3) ❌ Label encoding on nominal vars unstated (-20)
- **Total findings:** 14 (7 analysis, 7 communication), displayed 10
- **Key observations:** Low-quality Kaggle notebook. Raw code presented as analysis. `gbc.fit(X, y)` on all data with no test set. Label encoding imposes ordinal on 51 states. No correlation check (minutes×charges deterministic). Accuracy reported without naive baseline (85.5%). No recommendations, no limitations, 40% of doc is Watson ML deployment boilerplate.
- **Pass/Fail:**
- **User notes:**

### T-04: syn/04-contradicts-data
- **Score:** 83/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 71/100 (raw: 40→37.5 DR, credits: +8)
- **Communication:** 95/100 (raw: 20→20 DR, credits: +15)
- **Top 3:** (1) ❌ Conclusion contradicts data — says "improved" when data shows -8% (-10), (2) ❌ Blinder-Oaxaca decomposition without methodology/uncertainty (-20), (3) 🔴 Limitations absent (-10)
- **Total findings:** 6 (3 analysis, 3 communication)
- **Key observations:** Planted contradiction CAUGHT — the conclusion says "daily active sessions improved" but data shows 8% decline. Blinder-Oaxaca 61/39 split flagged for no uncertainty bounds. Strong TL;DR, good recommendations with guardrails. Communication scored 95 — document genuinely communicates well, the problems are analytical. Score (83) vs verdict (Major Rework) gap due to floor rule is notable.
- **Pass/Fail:** Pass (minor — score slightly inflated)
- **User notes:**

### T-05: syn/08-unstructured-text
- **Score:** 83/100 — ✅ Good to Go
- **Analysis:** 87/100 (raw: 28→28 DR, credits: +15)
- **Communication:** 78/100 (raw: 33→32 DR, credits: +10)
- **Top 3:** (1) 🔴 Jargon not calibrated for mixed audience (-10), (2) 🔴 Ungrounded 15% conversion assumption → $14.1M projection (-10), (3) 🔴 Survey n=342 of 150K segment, representativeness unaddressed (-10)
- **Total findings:** 7 (3 analysis, 4 communication)
- **Key observations:** Unstructured 2,100-word doc with zero headings. Location precision held up — all findings cite paragraph positions (e.g., "paragraph 8", "paragraph 10"). Content-signal scanning triggered. Found real analytical issues: ungrounded conversion assumption, survey bias, missing CLV. Communication correctly flagged no headings, jargon, buried signal. Thorough limitations acknowledged.
- **Pass/Fail:** **FAIL**
- **User notes:** Review missed the fundamental flaw: document lacks narrative synthesis — it's all tables and segment profiles without a summative story. Review flagged individual structural issues but never identified the overarching problem. Gave 83/100 Good to Go for what is essentially a data dump without narrative.

## Batch 2 Trace Summaries (Session 2026-03-21 continued)

### T-06: real/meta-llm-bug-reports
- **Source:** `dev/test-fixtures/real/meta-llm-bug-reports.md` — ~1,200 words, Meta blog about using LLMs to classify bug reports. Playbook format. Claims "double digits" bug reduction.
- **Score:** 62/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 63/100 (raw: 48→43.5 DR, credits: +6)
- **Communication:** 60/100 (raw: 48→43.5 DR, credits: +3)
- **Top 3:** (1) ❌ Causal claim without methodology — "reducing bug reports by double digits" with no controlled comparison (-20), (2) ❌ TL;DR absent (-12), (3) 🔴 Limitations/scope absent (-10)
- **Key observations:** Flagged causal claim as CRITICAL. Noted outage detection is a weak evidence example (any keyword system could do it). Narrative flag: "reads as corporate blog — success narrative that tells what was built, not how we know it worked."
- **Pass/Fail:** **FAIL** (too harsh)
- **User notes:** Review applies empirical analysis standards to a system description / operational blog post. The doc describes what was built and how it works — demanding causal methodology and controlled comparisons is the wrong rubric for this document type. User knows the author and work; acknowledges doc could be more solid, but 62/Major Rework is miscalibrated. Emerging failure mode: review doesn't adapt rigor expectations to document type.

### T-07: real/meta-llm-product-analytics
- **Source:** `dev/test-fixtures/real/meta-llm-product-analytics.md` — ~1,821 words, Meta blog about using Llama for customer feedback analysis. RAG pipeline description. No evaluation results.
- **Score:** 60/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 61/100 (raw: 48→44 DR, credits: +5)
- **Communication:** 59/100 (raw: 53→47 DR, credits: +6)
- **Top 3:** (1) ❌ No validation that the LLM tool works — zero accuracy metrics, user studies, or before/after (-20), (2) ❌ TL;DR absent — thesis buried after 400 words of preamble (-12), (3) 🔴 Vague recommendations — no measurable outcomes for any application (-8)
- **Key observations:** Narrative flag: "reads as product feature announcement dressed as analytics blog post." Central thesis (qualitative = quantitative) never demonstrated with evidence. Strong problem framing + RAG walkthrough; weak on validation.
- **Pass/Fail:**
- **User notes:**

### T-08: real/meta-asymmetric-experiments
- **Source:** `dev/test-fixtures/real/meta-asymmetric-experiments.md` — ~750 words, Meta blog on asymmetric experiments. TL;DR present. Math formulas as images. Feed holdout worked example.
- **Score:** 82/100 — ✅ Good to Go
- **Analysis:** 83/100 (raw: 28→28 DR, credits: +11)
- **Communication:** 80/100 (raw: 30→30 DR, credits: +10)
- **Top 3:** (1) 🔴 No summative narrative / concluding synthesis — ends abruptly (-8), (2) 🔴 Math without progressive disclosure for mixed audience (-10), (3) 🔴 Assumptions not enumerated as limitations (-10)
- **Key observations:** Narrative quality instruction caught the missing conclusion. Clean logical chain from math to practice. Concise at 750 words.
- **Pass/Fail:**
- **User notes:**

### T-09: real/capstone-customer-churn
- **Source:** `dev/test-fixtures/real/capstone-customer-churn.md` — ~3,920 words, academic capstone project. K-means segmentation + XGBoost churn prediction. SMOTE. SHAP values.
- **Score:** 53/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 54/100 (raw: 73→57 DR, credits: +11)
- **Communication:** 52/100 (raw: 57→49 DR, credits: +1)
- **Top 3:** (1) ❌ Train accuracy 1.0 dismissed by flawed "5% threshold" heuristic (-20), (2) ❌ No executive summary — abstract leads with methodology (-12), (3) 🔴 Causal/prescriptive claims from correlational SHAP analysis (-10)
- **Key observations:** Caught overfitting signal (1.0 train accuracy). Caught SMOTE leakage risk. Flagged precision optimization without business justification (churn usually favors recall). Narrative flag: "notebook-as-report without narrative synthesis."
- **Pass/Fail:**
- **User notes:**

### T-10: real/kaggle-house-prices-eda
- **Source:** `dev/test-fixtures/real/kaggle-house-prices-eda.md` — ~5,100 words, philosophical EDA walkthrough with Hair et al. framework. Extended fictional narrative framing ("meeting SalePrice at a party").
- **Score:** 62/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 65/100 (raw: 48→44 DR, credits: +8)
- **Communication:** 58/100 (raw: 68→54 DR, credits: +12)
- **Top 3:** (1) ❌ TL;DR absent — opens with Thales of Miletus quote (-12), (2) ❌ No baselines or benchmarks for any reported metric (-10), (3) 🔴 No narrative synthesis — teaches EDA technique but never says what EDA revealed (-8)
- **Key observations:** Narrative flag explicit: "teaches how to do EDA but doesn't tell you what the EDA found." Extended fictional framing creates audience mismatch. Honest about uncertainty (rare). Categorical variables acknowledged as underexplored but never revisited.
- **Pass/Fail:**
- **User notes:**

### T-12: real/atlassian-rovo-search-relevance
- **Source:** `dev/test-fixtures/real/atlassian-rovo-search-relevance.md` — ~720 words, Atlassian blog describing Rovo search architecture. Names metrics (QSR, NDCG, MRR) but reports zero values.
- **Score:** 62/100 — ⚠️ Minor Fix (1 CRITICAL, floor caps at 79)
- **Analysis:** 66/100 (raw: 38→36 DR, credits: +2)
- **Communication:** 58/100 (raw: 48→44 DR, credits: +2)
- **Top 3:** (1) ❌ TL;DR absent (-12), (2) 🔴 Conclusions not traceable — claims "delivers relevant results" with zero evidence (-10), (3) 🔴 Audience mismatch — uniformly technical, no layering (-10)
- **Key observations:** Narrative flag: "catalog of architecture components without narrative thread — tells anatomy but not health." Names evaluation metrics but never reports a single result. Read as reference manual, not analysis.
- **Pass/Fail:**
- **User notes:**

### T-11: real/kaggle-titanic-solutions
- **Source:** `dev/test-fixtures/real/kaggle-titanic-solutions.md` — ~7,521 words, Kaggle Titanic walkthrough with 9 models. Companion book format. Heavy code + raw DataFrames. Training-only evaluation.
- **Score:** 56/100 — ❌ Major Rework (2 CRITICALs, floor rule)
- **Analysis:** 61/100 (raw: 58→49 DR, credits: +10)
- **Communication:** 51/100 (raw: 68→54 DR, credits: +5)
- **Top 3:** (1) ❌ All models evaluated on training accuracy only — no CV, no holdout (-20), (2) ❌ TL;DR absent (-12), (3) 🔴 LogReg coefficients mislabeled as "Correlation" (-10)
- **Key observations:** Caught training-only evaluation as CRITICAL. Caught coefficient mislabeling (log-odds ≠ correlation). Narrative flag: "teaches how to do a Kaggle workflow but never communicates what the data reveals." 9-model comparison is strong practice but built on invalid metric.
- **Pass/Fail:**
- **User notes:**

---
