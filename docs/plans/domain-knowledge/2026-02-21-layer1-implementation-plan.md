# Domain Knowledge Skill (Layer 1) — Implementation Plan (Public Data Proxy)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a standalone Domain Knowledge Skill for Search using public data sources, producing pre-built digest files that any agent can consume. Validates the architecture and serves as a portfolio demo.

**Architecture:** YAML index defines which public sources to track. SKILL.md defines the digest format contract. Digest files are the product — pre-built, versioned markdown with structured sections, authority tags, and audience tags. Consumer agents just read the files. Public sources (academic papers, engineering blogs) populate foundational content. Workstream content uses a hybrid of public case studies + synthetic `[DEMO]` entries.

**Tech Stack:** Markdown, YAML. No scripts, no external dependencies.

**Scope:** Layer 1 only. Layer 2 (reviewer subagent) and Layer 3 (lead integration) come after validation.

**Design docs:**
- `docs/plans/domain-knowledge/2026-02-21-public-data-proxy-design.md` — Public data proxy decisions
- `docs/plans/domain-knowledge/mvp-design.md` — MVP scope decisions (A1-A5)
- `docs/plans/domain-knowledge/design-v3.md` — Full v3 spec (21 decisions)

**Path note:** Original plan used `plugin/` paths. After the multi-agent platform migration (2026-02-16), shared skills live in `shared/skills/[skill-name]/`. This plan uses the correct post-migration paths.

---

## Files to Create

| File | Purpose |
|---|---|
| `docs/research/domain-knowledge-references.md` | Research reference doc — all findings, sources, benchmarks organized by domain |
| `shared/skills/search-domain-knowledge/config/domain-index.yaml` | Curated domain-to-source mapping (2 sub-domains + cross-domain) |
| `shared/skills/search-domain-knowledge/SKILL.md` | Skill contract: digest format, consumption guide, staleness rules, refresh workflow |
| `shared/skills/search-domain-knowledge/digests/search-ranking.md` | Primary digest — Search Ranking foundational + hybrid workstream |
| `shared/skills/search-domain-knowledge/digests/query-understanding.md` | QU pipeline evaluation standards |
| `shared/skills/search-domain-knowledge/digests/search-cross-domain.md` | Cross-cutting Search evaluation knowledge |

**Deferred domains:** search-infra (least useful for DS review), search-experience (future).

---

## Task 0: Research — Search Ranking Domain (Batch 1)

**Files:**
- Create: `docs/research/domain-knowledge-references.md`

**Goal:** Gather specific benchmarks, numbers, citations, and blog post content for the search-ranking digest. This is the largest domain and template for the others.

**Step 1: Research evaluation metrics**

Web search for:
- MS MARCO leaderboard — current NDCG@10 ranges for passage and document ranking
- TREC Deep Learning track — evaluation methodology and metric ranges
- Key papers: NDCG (Järvelin & Kekäläinen, 2002), MRR usage in QA tasks, ERR (Chapelle et al., 2009)

Record: metric name, recommended use case, typical benchmark ranges, key citation.

**Step 2: Research position bias**

Web search for:
- Joachims et al. (2005, 2007) — original eye-tracking position bias studies
- IPW for ranking: Wang et al. (2016) "Learning to Rank with Selection Bias"
- Doubly-robust estimation for ranking: recent papers (2020+)
- Any Airbnb/Google/LinkedIn blog posts about position bias correction in production

Record: method name, when to use, key paper, any reported effectiveness numbers.

**Step 3: Research click models**

Web search for:
- Click model survey papers (Chuklin et al., 2015 "Click Models for Web Search")
- PBM, Cascade, DBN — original papers and when each model is appropriate
- Production usage examples from engineering blogs

Record: model name, assumptions, appropriate query type, key citation.

**Step 4: Research Learning to Rank**

Web search for:
- LambdaMART (Burges, 2010) — benchmark results
- Neural ranking models (BERT re-ranking, ColBERT) — MS MARCO results
- Industry blog posts about LTR in production (Airbnb, LinkedIn, Etsy)

Record: method, benchmark performance, production considerations, key citation.

**Step 5: Research experiment design**

Web search for:
- Interleaving experiments: Chapelle et al. (2012) "Large-scale Validation and Analysis of Interleaved Search Evaluation"
- A/B testing for search: minimum duration evidence, novelty effects
- Industry blog posts about search experimentation (Google, Netflix, Airbnb)

Record: method, sensitivity claims, minimum duration evidence, key citation.

**Step 6: Research workstream-tier content (ranking blogs)**

Web search for 3-5 engineering blog posts about search ranking decisions or experiments:
- Airbnb search ranking blog posts (known to exist)
- LinkedIn search ranking improvements
- Google AI Blog on ranking changes
- Any published post-mortem or experiment result related to search ranking

Record: source, key decision/learning, date, whether it fits as "standard" or "learning".

**Step 7: Write Batch 1 to research doc**

Create `docs/research/domain-knowledge-references.md` with:
- Header explaining purpose
- Batch 1: Search Ranking section with all findings organized by topic
- Each entry: source, key finding, citation, suggested digest tier/section
- Leave space for Batch 2 and 3

**Step 8: Commit**

```bash
git add docs/research/domain-knowledge-references.md
git commit -m "research(domain-knowledge): add search-ranking references (Batch 1)"
```

---

## Task 1: Research — Query Understanding + Cross-Domain (Batches 2-3)

**Files:**
- Modify: `docs/research/domain-knowledge-references.md`

**Step 1: Research query classification**

Web search for:
- Broder (2002) taxonomy: informational/navigational/transactional
- Modern intent classification approaches and benchmarks
- Industry blog posts on query understanding systems

Record: taxonomy, evaluation methods, key citation.

**Step 2: Research query rewriting**

Web search for:
- Query rewriting evaluation — downstream ranking impact vs. rewrite quality
- Spell correction precision/recall tradeoffs in production
- Industry blog posts (Google, Bing, Pinterest) about QU pipelines

Record: evaluation method, key finding, citation.

**Step 3: Research cross-domain evaluation**

Web search for:
- End-to-end search evaluation frameworks
- Cross-component metric attribution methods
- Papers on full-stack search experiment design

Record: framework, key insight, citation.

**Step 4: Research workstream-tier content (QU + cross-domain blogs)**

Web search for 2-3 engineering blog posts about:
- Query understanding decisions or experiments
- Cross-component search evaluation challenges

Record: source, key decision/learning, date.

**Step 5: Write Batches 2-3 to research doc**

Append to `docs/research/domain-knowledge-references.md`:
- Batch 2: Query Understanding section
- Batch 3: Cross-Domain section
- Same format as Batch 1

**Step 6: Commit**

```bash
git add docs/research/domain-knowledge-references.md
git commit -m "research(domain-knowledge): add QU and cross-domain references (Batches 2-3)"
```

---

## ⏸️ CHECKPOINT: User Reviews Research

**Before proceeding:** User reviews `docs/research/domain-knowledge-references.md`.
- Are the sources credible and relevant?
- Are there key topics missing?
- Any corrections needed for accuracy?
- Which blog posts work well for workstream content?

**Resume after user approval.**

---

## Task 2: Create directory structure and domain-index.yaml

**Files:**
- Create: `shared/skills/search-domain-knowledge/config/domain-index.yaml`
- Create: `shared/skills/search-domain-knowledge/digests/` (directory)

**Step 1: Create directories**

```bash
mkdir -p shared/skills/search-domain-knowledge/config
mkdir -p shared/skills/search-domain-knowledge/digests
```

**Step 2: Create domain-index.yaml**

Curated index with public source references instead of Confluence page IDs.
Audience tags per MVP decision A2. Token budgets per A2/A5.

Content should include:
- `search-ranking` domain with 4-5 foundational sources (papers) + 1-2 workstream (blogs)
- `query-understanding` domain with 3-4 foundational sources + 1 workstream
- `search-cross-domain` with 2 foundational sources, `applies-to` both domains
- Each entry: `id` (source identifier), `title`, `tier`, `audience`, `url` (public source)
- Refresh config: token budgets (8000/domain, 1500/cross-domain), retain-versions: 4
- Source IDs use descriptive prefixes (e.g., `SR-FOUND-001`, `QU-FOUND-001`)
- Placeholder Confluence IDs replaced with descriptive IDs referencing public papers/blogs

**Step 3: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('shared/skills/search-domain-knowledge/config/domain-index.yaml'))"
```

Expected: no errors (silent success).

**Step 4: Commit**

```bash
git add shared/skills/search-domain-knowledge/config/domain-index.yaml
git commit -m "feat(domain-knowledge): add curated domain index with public sources"
```

---

## Task 3: Create SKILL.md contract

**Files:**
- Create: `shared/skills/search-domain-knowledge/SKILL.md`

**Step 1: Write SKILL.md**

Use the SKILL.md content from the original implementation plan
(`dev/internal/2026-02-16-domain-knowledge-layer1-implementation-plan.md`, Task 2).
This is unchanged — the format contract is source-agnostic.

Required sections:
1. Digest File Contract (headers, section structure, authority levels, audience tags)
2. How to Consume Digests (single domain, multi-domain, token budgets)
3. Staleness Thresholds (14-day warning, 30-day critical, missing/empty)
4. Refresh Workflow (manual trigger, process steps, rollback)
5. Importance Scoring (LLM formula: 0.6 × review_impact + 0.4 × knowledge_density)
6. Knowledge Tier Precedence (workstream overrides foundational, conflicts flagged)

Frontmatter: `name: search-domain-knowledge`, `description`, `auto_activate: true`.

Update paths from `plugin/` to `shared/skills/search-domain-knowledge/`.

**Step 2: Validate structure**

Check: frontmatter present (name, description, auto_activate), all 6 sections present,
paths reference correct post-migration locations.

**Step 3: Commit**

```bash
git add shared/skills/search-domain-knowledge/SKILL.md
git commit -m "feat(domain-knowledge): add skill contract definition"
```

---

## Task 4: Create search-ranking digest

**Files:**
- Create: `shared/skills/search-domain-knowledge/digests/search-ranking.md`
- Reference: `docs/research/domain-knowledge-references.md` (Batch 1)

**Step 1: Write search-ranking.md**

This is the primary and largest digest. Use the original plan's draft structure
as the skeleton, then enrich with research findings from Batch 1.

Required sections (in order):
1. Metadata headers: Version, Previous, Token budget, Audience tags
2. `## Foundational Knowledge [authority: authoritative] [audience: all]` — evaluation
   metrics with specific benchmark ranges (from research), position bias methods with
   paper citations, experiment methodology with evidence
3. `## Foundational Knowledge [authority: authoritative] [audience: ds]` — click models
   with citations, LTR methods with benchmark results
4. `## Foundational Knowledge [authority: authoritative] [audience: eng]` — serving
   latency budgets
5. `## Workstream Standards [authority: authoritative] [audience: all]` — hybrid content:
   public blog decisions (with source citation) + synthetic entries (labeled `[DEMO]`)
6. `## Workstream Learnings [authority: advisory] [audience: ds]` — hybrid content:
   published experiment results (cited) + synthetic post-mortems (labeled `[DEMO]`)
7. `## Conflicts` — at least 1 `[DEMO]` conflict demonstrating workstream-overrides-foundational

Key enrichments from research:
- Specific NDCG@10 ranges from MS MARCO (not generic "0.40-0.55")
- Paper citations in format: (Author et al., Year)
- Blog post references for workstream entries: (ref: Source, Year)

**Step 2: Verify format matches SKILL.md contract**

Check: metadata headers present, all section types present, authority + audience tags
on every section header, citations inline, `[DEMO]` labels on synthetic entries.

**Step 3: Rough token count check**

```bash
wc -w shared/skills/search-domain-knowledge/digests/search-ranking.md
```

Target: ~5,000-6,000 words ≈ ~7,000-8,000 tokens. Should be under 8,000 token budget.

**Step 4: Commit**

```bash
git add shared/skills/search-domain-knowledge/digests/search-ranking.md
git commit -m "feat(domain-knowledge): add search-ranking digest with public sources"
```

---

## Task 5: Create remaining digests

**Files:**
- Create: `shared/skills/search-domain-knowledge/digests/query-understanding.md`
- Create: `shared/skills/search-domain-knowledge/digests/search-cross-domain.md`
- Reference: `docs/research/domain-knowledge-references.md` (Batches 2-3)

**Step 1: Write query-understanding.md**

Same format as search-ranking. Smaller content. Enriched with Batch 2 research.

Required content:
- Foundational [audience: all]: query classification (Broder taxonomy with citation),
  intent detection evaluation, query segmentation
- Foundational [audience: ds]: query rewriting impact measurement (downstream ranking
  metrics, not just BLEU), spell correction precision > recall tradeoff
- Workstream: hybrid public + synthetic (same pattern as ranking)
- Conflicts: none for initial digest (or 1 demo if natural)

**Step 2: Write search-cross-domain.md**

Smallest digest. Foundational-only in MVP (no workstream section). Enriched with Batch 3.

Required content:
- Foundational [audience: all]: end-to-end evaluation (component vs. full-stack metrics),
  cross-component experiment effects
- Foundational [audience: ds]: metric attribution methods, full-stack experiment design
- No workstream sections (cross-domain is foundational-only in MVP)
- No conflicts section

**Step 3: Verify both digests match contract**

For each digest:
- Metadata headers present (Version, Previous, Token budget, Audience tags)
- Section headers follow SKILL.md contract pattern
- Authority and audience tags on every section
- Citations inline where applicable
- `[DEMO]` labels on synthetic entries

**Step 4: Rough token count check**

```bash
wc -w shared/skills/search-domain-knowledge/digests/query-understanding.md
wc -w shared/skills/search-domain-knowledge/digests/search-cross-domain.md
```

Targets: QU ~4,000-5,000 words, cross-domain ~1,000-1,200 words.

**Step 5: Commit**

```bash
git add shared/skills/search-domain-knowledge/digests/
git commit -m "feat(domain-knowledge): add QU and cross-domain digests"
```

---

## Task 6: Final validation and cleanup

**Step 1: Verify complete file set**

```bash
ls -la shared/skills/search-domain-knowledge/config/domain-index.yaml
ls -la shared/skills/search-domain-knowledge/SKILL.md
ls -la shared/skills/search-domain-knowledge/digests/
```

Expected: 1 YAML file, 1 SKILL.md, 3 digest files.

**Step 2: Validate YAML index paths match actual digest file paths**

Cross-check each `digest-path` in domain-index.yaml against files in `digests/`.

**Step 3: Validate cross-domain applies-to references**

Check that `search-cross-domain.applies-to` lists domains that exist in the index.

**Step 4: Read each digest and verify contract compliance**

For each of the 3 digests, verify:
- [ ] Metadata headers present and correctly formatted
- [ ] All section headers include `[authority: ...]` and `[audience: ...]` tags
- [ ] Foundational sections contain citations to public sources
- [ ] Workstream sections have hybrid content (public cited + synthetic `[DEMO]`)
- [ ] At least 1 Conflicts entry exists (in search-ranking digest)
- [ ] Token budgets approximately respected

**Step 5: Update backlog**

Update `dev/backlog.md`:
- Mark Layer 1 tasks as complete
- Note: research doc available at `docs/research/domain-knowledge-references.md`
- Note: ready for Layer 2 (Domain Expert Reviewer subagent)

**Step 6: Create session log**

Create `dev/sessions/2026-02-21-domain-knowledge-layer1-implementation.md` with:
- What was built
- Files created/modified
- Key decisions made during implementation
- Research sources used
- What comes next (Layer 2)

**Step 7: Update CHANGELOG**

Update `CHANGELOG.md` with v0.5 Layer 1 completion entry.

**Step 8: Commit**

```bash
git add dev/backlog.md dev/sessions/ CHANGELOG.md
git commit -m "docs: complete Layer 1 implementation — update backlog, session log, changelog"
```

---

## Verification Checklist

| Check | How |
|---|---|
| YAML parses cleanly | `python3 -c "import yaml; yaml.safe_load(open(...))"` |
| All 3 digests exist | `ls shared/skills/search-domain-knowledge/digests/` → 3 .md files |
| Digest format matches contract | Manual: headers, sections, authority/audience tags |
| Cross-domain references valid | Index `applies-to` lists match domain names in index |
| Digest paths in index match files | Each `digest-path` points to an existing file |
| Foundational content has citations | Each topic references at least 1 public source |
| Workstream content is hybrid | Mix of public (cited) and synthetic (`[DEMO]` labeled) |
| At least 1 conflict exists | search-ranking digest has a Conflicts entry |
| Token budgets respected | `wc -w` on each digest within target range |
| Research doc is complete | 3 batches, organized by domain, all sources recorded |

---

## What Comes Next (Future Sessions)

| Phase | What | Depends on |
|---|---|---|
| Layer 2 | Domain Expert Reviewer subagent (3 lenses, deduction tables) | Layer 1 validated by user |
| Layer 2 | Update ds-review-framework SKILL.md (ADVISORY severity, domain routing) | Layer 1 validated |
| Layer 3 | Lead agent integration (--domain flag, 3rd subagent, 50/25/25 scoring) | Layer 2 complete |
| Layer 3 | Update review.md command with new flags | Layer 2 complete |
| Calibration | Run fixtures with 3-dimension scoring, compare to 2-dimension baselines | Layer 3 complete |
