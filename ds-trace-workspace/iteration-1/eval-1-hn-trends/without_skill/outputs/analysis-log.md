# EDA: Hacker News Tech Trend Velocity Dataset

**Dataset:** `/Users/surahli/Downloads/Hacker_News_Tech_Trend_Velocity_Final.csv`
**Date:** 2026-03-20

---

## Step 1: Load and Inspect Structure

**What I did:** Loaded the CSV with pandas. Checked shape, column names, dtypes, null counts, descriptive statistics, and unique values for low-cardinality columns.

**What I found:**
- **Shape:** 9,999 rows x 11 columns (close to the expected 10,000).
- **Columns:** Post_ID, Title, Post_Type, Score, Comments, Age_In_Hours, Score_Velocity, Comment_Velocity, Title_Length, Title_Word_Count, Is_Viral.
- **No nulls** in any column. Clean dataset.
- **Post_Type** has 3 values: Standard_Link (8,337 / 83.4%), Show_HN (1,416 / 14.2%), Ask_HN (246 / 2.5%).
- **Is_Viral** is binary: 8,994 non-viral (89.9%), 1,005 viral (10.1%).
- **Heavy right skew** in Score and Comments: median Score is 2 (mean 16.5), median Comments is 0 (mean 8.4). The max Score is 4,224 and max Comments is 1,668. This is a classic long-tail engagement distribution.
- **Velocity columns** are similarly skewed: median Score_Velocity is 0.03 (mean 0.35), median Comment_Velocity is 0.00 (mean 0.14). 61.4% of posts have zero Comment_Velocity.
- **Title_Length** ranges 1-88 chars (mean 53.2); **Title_Word_Count** ranges 1-18 (mean 8.7). Roughly normal distributions.
- **Age_In_Hours** ranges 0.1 to 211.2 (mean 105.2, median 96.9). Posts span roughly 0-9 days of age.

**Decision:** Data is clean. No missing values to handle. The extreme skew in engagement metrics means medians are more informative than means for typical-post comparisons, but means capture the impact of viral outliers. I will use both throughout.

---

## Step 2: Engagement by Post Type

**What I did:** Grouped by Post_Type and computed mean, median, max for Score and Comments. Also computed percentile distributions (p25-p99) and Score/Comment ratios for each type.

**What I found:**

### Mean and Median Engagement

| Post_Type | Count | Score Mean | Score Median | Score Max | Comments Mean | Comments Median | Comments Max | Viral Rate |
|-----------|-------|-----------|-------------|-----------|--------------|----------------|-------------|------------|
| Standard_Link | 8,337 | 18.3 | 2 | 4,224 | 9.3 | 0 | 1,668 | 10.9% |
| Show_HN | 1,416 | 7.1 | 2 | 462 | 2.9 | 0 | 355 | 5.2% |
| Ask_HN | 246 | 7.5 | 2 | 427 | 8.2 | 2 | 617 | 8.1% |

### Key Takeaways

1. **Standard_Link dominates in engagement volume and upside.** Highest mean Score (18.3), highest max Score (4,224), highest viral rate (10.9%). This makes sense: external links to notable content have the broadest audience appeal and highest ceiling.

2. **Ask_HN has the highest comment engagement relative to its score.** The Score/Comment ratio (median 1.0, mean 1.28) is the lowest of all types, meaning Ask_HN posts generate roughly 1 comment per upvote. Compare to Standard_Link (median 2.0, mean 3.46) which gets 2-3x more upvotes per comment. This is intuitive: Ask_HN posts are questions that invite discussion, so comments are the primary engagement mode.

3. **Show_HN underperforms on both dimensions.** Lowest mean Score (7.1), lowest comments mean (2.9), lowest viral rate (5.2%). The p95 Score for Show_HN is only 14, vs. 74 for Standard_Link. Show_HN posts are project launches, which appeal to a narrower audience. Most don't gain traction.

4. **Median Score is 2 for all three types.** The typical post, regardless of type, gets minimal engagement. The distribution is dominated by the long tail. Virality is rare and type-dependent.

5. **Percentile breakdowns reveal the "hockey stick":** For Standard_Link, the jump from p90 (15 points) to p99 (373 points) is 25x. Engagement is concentrated in a tiny fraction of posts.

**Decision:** Standard_Link is the clear winner for engagement, but Ask_HN is interesting for comment-driven engagement. The Score/Comment ratio is a useful signal for understanding engagement mode (vote-driven vs. discussion-driven).

---

## Step 3: Score_Velocity vs. Comment_Velocity Relationship

**What I did:** Computed Pearson and Spearman correlations (overall and by Post_Type), built a decile analysis of Score_Velocity, verified that velocity is simply Score/Age_In_Hours, and identified divergent-velocity posts (high SV + low CV and vice versa).

**What I found:**

### Correlation

| Scope | Pearson | Spearman |
|-------|---------|----------|
| Overall | 0.767 | 0.385 |
| Standard_Link | 0.768 | 0.393 |
| Show_HN | 0.790 | 0.340 |
| Ask_HN | 0.503 | 0.631 |

- **Pearson r = 0.77** suggests a strong linear relationship: posts that accumulate upvotes quickly also accumulate comments quickly.
- **Spearman rho = 0.38** is much lower, indicating that the rank-order relationship is weaker. The high Pearson is driven by the extreme outliers in the tail (a few high-velocity posts pull the linear correlation up).
- **Ask_HN is the exception:** Spearman (0.63) exceeds Pearson (0.50), meaning the rank-order relationship is more consistent for discussion posts. The linear relationship is weaker because Ask_HN doesn't produce the same extreme outliers.

### Velocity Construction

Velocity is confirmed to be approximately `Score / Age_In_Hours` (and `Comments / Age_In_Hours`). 99.1% of rows match within 0.015. The small differences are likely rounding. This means velocity is purely a normalization of raw engagement by post age -- not a separate signal.

### Decile Analysis

The Score_Velocity decile table reveals a stark pattern:

| SV Decile | SV Mean | CV Mean | Score Mean | Comments Mean | Viral Rate |
|-----------|---------|---------|-----------|--------------|------------|
| 1-8 | 0.01-0.08 | 0.003-0.018 | 1.5-5.1 | 0.4-1.2 | 0% |
| 9 | 0.18 | 0.04 | 10.0 | 3.0 | 0.5% |
| 10 | 3.06 | 1.35 | 133.2 | 75.8 | 100% |

- Deciles 1-8 are essentially indistinguishable: low velocity, low engagement, 0% viral.
- Decile 9 is the "middle ground" with modest engagement and near-zero viral rate.
- Decile 10 is where all the action is: **100% viral rate**, 133 mean Score, 75.8 mean Comments.
- The jump from decile 9 to decile 10 is 17x in SV and 34x in CV. This is not a gradient -- it's a cliff.

### Divergent Velocity Posts

- **213 posts with high SV (>=p90) but zero CV:** These are very young posts (Age_In_Hours = 0.1) with low absolute scores (2-4) but technically high velocity because they're so new. Examples: "China Approves the First Brain Chips for Sale" (Score 4, Age 0.1h, SV=40.0). These are artifacts of the velocity calculation for brand-new posts, not genuinely fast-growing content.
- **Only 1 post with high CV but low SV:** "Show HN: An Article About How I Starting Programming" (Score 1, Comments 5). A post that generated discussion but no upvotes.

**Decision:** The Pearson/Spearman gap is the most interesting finding here. The two velocities are correlated, but the strength of that correlation is exaggerated by outliers. For most posts, there's only a weak tendency for score and comment velocity to move together. The velocity calculation also has an artifact problem for very young posts (Age < 1 hour), where even 1-2 upvotes can create extreme velocity values.

---

## Step 4: Viral Content Patterns (Is_Viral)

**What I did:** Compared viral vs. non-viral posts across all metrics. Tested various thresholds to identify what determines viral status. Examined the boundary between viral and non-viral posts.

**What I found:**

### Viral vs. Non-Viral Comparison

| Metric | Viral Mean | Non-Viral Mean | Ratio |
|--------|-----------|---------------|-------|
| Score | 132.7 | 3.5 | 38x |
| Comments | 75.4 | 0.9 | 84x |
| Score_Velocity | 3.05 | 0.05 | 68x |
| Comment_Velocity | 1.34 | 0.01 | 122x |
| Age_In_Hours | 68.9 | 109.3 | 0.6x |
| Title_Length | 53.0 | 53.2 | 1.0x |
| Title_Word_Count | 8.6 | 8.7 | 1.0x |

- Viral posts have **38x more Score, 84x more Comments, 68x more Score_Velocity, 122x more Comment_Velocity**.
- Viral posts are **younger on average** (69 vs 109 hours). This makes sense: younger posts with high velocity haven't had time to "decay."
- **Title characteristics are identical** between viral and non-viral. Title length and word count have zero predictive power for virality in this dataset.

### The Viral Threshold: A Clean Cutoff

This is the most important finding in the analysis:

**`Is_Viral = 1` if and only if `Score_Velocity >= 0.32`.**

This is a perfect, deterministic boundary:
- Max Score_Velocity among non-viral posts: **0.31**
- Min Score_Velocity among viral posts: **0.32**
- Posts in the overlap zone: **0**

At `SV >= 0.32`: 1,005 viral + 0 non-viral. Zero misclassification in either direction. This means `Is_Viral` is not a subjective label or a model prediction -- it is a derived column computed directly from Score_Velocity.

### Viral Rate by Post Type

| Post_Type | Viral Rate |
|-----------|-----------|
| Standard_Link | 10.9% |
| Ask_HN | 8.1% |
| Show_HN | 5.2% |

Standard_Link has 2x the viral rate of Show_HN. This aligns with the engagement findings from Step 2.

### Viral Post Age Distribution

Viral posts skew younger:
- Viral p10: 1.7 hours vs non-viral p10: 28.5 hours
- Viral p25: 11.6 hours vs non-viral p25: 60.1 hours
- Viral p50: 43.8 hours vs non-viral p50: 104.0 hours

Many viral posts are very young (<2 hours), which means their high velocity could be partly an artifact of the `Score / Age` calculation. A post with Score=4 at Age=0.1 hours gets SV=40.0, which looks explosive but may just be noise from a brand-new post.

### Comment/Score Velocity Ratio for Viral Posts

For viral posts with nonzero Comment_Velocity, the CV/SV ratio has mean 0.53 and median 0.41. This means on average, viral posts accumulate comments at about half the rate they accumulate upvotes. The standard deviation is 0.44, indicating meaningful variation in how "discussion-heavy" viral content is.

**Decision:** `Is_Viral` is a deterministic function of `Score_Velocity` with a clean cutoff at 0.32. It is a derived feature, not an independent label. This has implications for any downstream modeling: using both `Score_Velocity` and `Is_Viral` as features would be redundant (perfect multicollinearity above/below the threshold). The velocity-based artifact for very young posts (Age < 1 hour) inflates some posts to viral status based on minimal absolute engagement (e.g., Score=3 at Age=0.1h yields SV=30.0).

---

## Summary of Key Findings

1. **Standard_Link posts dominate engagement.** They have the highest mean Score (18.3), highest comments (9.3), and highest viral rate (10.9%). Show_HN underperforms across the board (5.2% viral rate). Ask_HN is distinct in generating comment-heavy engagement (1:1 score-to-comment ratio vs 2-3:1 for links).

2. **Score_Velocity and Comment_Velocity are correlated but the strength is misleading.** Pearson r=0.77 is driven by extreme outliers; Spearman rho=0.38 reflects the weaker rank-order relationship for typical posts. For most of the dataset (deciles 1-8), both velocities are near-zero and weakly related.

3. **`Is_Viral` is a deterministic threshold: `Score_Velocity >= 0.32`.** There is zero overlap between viral and non-viral posts on this boundary. It is a derived column, not an independent signal. Any model using both `Score_Velocity` and `Is_Viral` would have perfect information leakage.

4. **Very young posts create velocity artifacts.** Posts with Age_In_Hours < 1 can have extreme velocities from minimal absolute engagement (e.g., Score=3 yields SV=30.0 at Age=0.1h). These are technically "viral" by the threshold definition but may not represent genuinely trending content.

5. **Title characteristics (length, word count) have zero relationship with engagement or virality.** The distributions are identical for viral and non-viral posts.
