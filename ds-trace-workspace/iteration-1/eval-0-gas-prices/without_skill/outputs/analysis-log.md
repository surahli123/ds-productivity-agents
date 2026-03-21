# EDA: Iran War Gas Prices by State

**Dataset:** `/Users/surahli/Downloads/iran_war_gas_prices_by_state.csv`
**Source:** AAA State Gas Price Averages — March 19, 2026

---

## Step 1: Load Data and Check Structure

**What I did:** Loaded the CSV and inspected shape, columns, dtypes, and nulls.

**Result:**
- **Shape:** 50 rows x 9 columns (all 50 US states; DC not included)
- **Columns:**
  - `state` (str) — state name
  - `region` (str) — one of West, Midwest, Northeast, South
  - `gas_price_mar19_2026` (float) — current price as of March 19, 2026
  - `gas_price_prewar_feb27` (float) — price just before war started (Feb 27)
  - `gas_price_jan08_2026` (float) — earlier baseline (Jan 8)
  - `price_increase_since_war` (float) — absolute $ increase from Feb 27 to Mar 19
  - `pct_increase_since_war` (float) — percentage increase from Feb 27 to Mar 19
  - `price_vs_national_avg` (float) — current price minus the national average ($3.88)
  - `source` (str) — all rows cite the same AAA source
- **Nulls:** Zero across all columns. Clean dataset.
- **Dtypes:** All numeric columns are float64 as expected.

**Decision:** No cleaning needed. Data is well-structured and pre-computed. I verified the derived columns (`price_increase_since_war`, `pct_increase_since_war`) against raw values — all 50 rows match perfectly. The implied national average is consistently $3.88 across all rows (note: this is not the unweighted mean of state prices, which is $3.84 — the national average is likely population-weighted).

**Region distribution:**
| Region    | States |
|-----------|--------|
| South     | 14     |
| West      | 13     |
| Midwest   | 12     |
| Northeast | 11     |

---

## Step 2: States Most Impacted by Gas Price Increases

**What I did:** Ranked states by both absolute dollar increase and percentage increase since the war began (Feb 27 to Mar 19).

### Top 10 by Absolute Dollar Increase

| Rank | State       | Region  | Pre-War  | Current  | Increase | % Increase |
|------|-------------|---------|----------|----------|----------|------------|
| 1    | Hawaii      | West    | $4.02    | $5.07    | +$1.05   | 26.1%      |
| 2    | California  | West    | $4.52    | $5.53    | +$1.01   | 22.3%      |
| 3    | Washington  | West    | $4.18    | $5.15    | +$0.97   | 23.2%      |
| 4    | Nevada      | West    | $3.72    | $4.66    | +$0.94   | 25.3%      |
| 5    | Oregon      | West    | $3.82    | $4.70    | +$0.88   | 23.0%      |
| 6    | Kentucky    | South   | $2.84    | $3.72    | +$0.88   | 31.0%      |
| 7    | Alaska      | West    | $3.62    | $4.48    | +$0.86   | 23.8%      |
| 8    | Utah        | West    | $3.02    | $3.88    | +$0.86   | 28.5%      |
| 9    | Colorado    | West    | $2.98    | $3.82    | +$0.84   | 28.2%      |
| 10   | Illinois    | Midwest | $3.08    | $3.92    | +$0.84   | 27.3%      |

**Observation:** The top 7 by absolute increase are all West region states. This is heavily dominated by states that already had high gas prices pre-war. Kentucky is the lone non-West state in the top 6.

### Top 10 by Percentage Increase

| Rank | State       | Region  | Pre-War  | Current  | Increase | % Increase |
|------|-------------|---------|----------|----------|----------|------------|
| 1    | Kentucky    | South   | $2.84    | $3.72    | +$0.88   | 31.0%      |
| 2    | Arkansas    | South   | $2.66    | $3.42    | +$0.76   | 28.6%      |
| 3    | Utah        | West    | $3.02    | $3.88    | +$0.86   | 28.5%      |
| 4    | Nebraska    | Midwest | $2.68    | $3.44    | +$0.76   | 28.4%      |
| 5    | Alabama     | South   | $2.68    | $3.44    | +$0.76   | 28.4%      |
| 6    | Indiana     | Midwest | $2.76    | $3.54    | +$0.78   | 28.3%      |
| 7    | Colorado    | West    | $2.98    | $3.82    | +$0.84   | 28.2%      |
| 8    | Georgia     | South   | $2.78    | $3.56    | +$0.78   | 28.1%      |
| 9    | Louisiana   | South   | $2.70    | $3.46    | +$0.76   | 28.1%      |
| 10   | Mississippi | South   | $2.64    | $3.38    | +$0.74   | 28.0%      |

**Observation:** The percentage view tells a very different story. Kentucky leads at 31.0% — the only state above 30%. The top 10 by percentage is dominated by South (6 states) and low-prewar-price states. The expensive West Coast states (CA, WA, OR) that led on absolute increases actually have the *lowest* percentage increases (22-23%).

**Key insight:** The two measures tell opposite stories. States that already had expensive gas saw the largest dollar increases but the smallest percentage increases. States with cheap gas saw smaller dollar increases but the largest percentage hits relative to what they were paying.

---

## Step 3: Regional Patterns

**What I did:** Aggregated by region to find systematic patterns.

### Regional Summary

| Region    | Avg Current | Avg Pre-War | Avg $ Increase | Avg % Increase | Spread (CV) |
|-----------|-------------|-------------|----------------|----------------|-------------|
| West      | $4.32       | $3.45       | +$0.87         | 25.5%          | 10.9%       |
| Northeast | $3.96       | $3.15       | +$0.82         | 26.0%          | 2.3%        |
| South     | $3.53       | $2.75       | +$0.77         | 28.1%          | 5.2%        |
| Midwest   | $3.55       | $2.79       | +$0.76         | 27.3%          | 6.3%        |

### Key Regional Findings

1. **West has the highest absolute increases** (avg +$0.87) but the **lowest percentage increases** (avg 25.5%). This is because West states started from a much higher base ($3.45 avg pre-war vs $2.75 for South). The absolute-vs-percentage paradox is a regional phenomenon, not just individual states.

2. **South has the highest percentage increases** (avg 28.1%) despite the lowest absolute increases (avg +$0.77). Consumers in Southern states experienced proportionally larger price shocks relative to what they were paying.

3. **Northeast is the most uniform region.** The coefficient of variation for absolute increases is only 2.3% (range: $0.80 to $0.84). All 11 Northeast states saw nearly identical dollar increases. This suggests a more interconnected/regulated fuel distribution network in the Northeast.

4. **West is the most heterogeneous region.** CV of 10.9% with increases ranging from $0.76 (Wyoming) to $1.05 (Hawaii). The Pacific Coast states (CA, WA, HI, OR, NV) form a distinct sub-cluster well above the Mountain West states.

5. **States above the national average ($3.88):** 16 states — 8 West, 7 Northeast, 1 Midwest (Illinois). Zero Southern states are above the national average. The geographic divide is stark.

### Pre-War Price vs. Increase (Correlation Analysis)

| Relationship                           | Correlation |
|---------------------------------------|-------------|
| Pre-war price vs. absolute increase    | +0.891      |
| Pre-war price vs. percentage increase  | -0.777      |
| Jan price vs. absolute increase        | +0.919      |

**Interpretation:** There is a very strong positive correlation between how expensive gas already was and how much the dollar price went up. States where gas was already expensive saw bigger absolute jumps. But the reverse is true for percentages — cheap-gas states experienced disproportionately large relative increases. This is partially mechanical (same dollar increase on a lower base = higher percentage) but the magnitudes vary enough that it's not purely arithmetic.

### By Pre-War Price Quartile

| Quartile             | Avg Pre-War | Avg $ Increase | Avg % Increase |
|----------------------|-------------|----------------|----------------|
| Q1 (cheapest, <$2.72)| $2.68       | +$0.75         | 27.9%          |
| Q2 ($2.72-$2.88)     | $2.85       | +$0.78         | 27.4%          |
| Q3 ($2.88-$3.14)     | $3.02       | +$0.82         | 27.2%          |
| Q4 (most expensive)  | $3.58       | +$0.88         | 24.6%          |

The gradient is monotonic in both directions: more expensive states saw bigger dollar jumps but smaller percentage jumps. Q4 states averaged +$0.88 vs Q1's +$0.75, a 17% difference in absolute impact.

---

## Step 4: Price Decomposition (Pre-War Trend vs. War Period)

**What I did:** Decomposed the Jan 8 to Mar 19 price movement into two periods: (1) Jan 8 to Feb 27 (pre-war trend), and (2) Feb 27 to Mar 19 (war period).

**Result:**
- Average Jan-to-Feb increase (pre-war): +$0.36
- Average Feb-to-Mar increase (war period): +$0.81
- **The war period accounts for ~70% of the total Jan-to-Mar price increase.**

By region:
| Region    | Jan→Feb (pre-war) | Feb→Mar (war) | War Share |
|-----------|-------------------|---------------|-----------|
| West      | +$0.43            | +$0.87        | 67.9%     |
| Northeast | +$0.40            | +$0.82        | 67.0%     |
| Midwest   | +$0.31            | +$0.76        | 71.1%     |
| South     | +$0.31            | +$0.77        | 71.7%     |

**Observation:** Prices were already rising before the war (seasonal pattern + other factors), but the war roughly doubled the rate of increase. South and Midwest saw a slightly higher war share (~71%) vs West and Northeast (~68%), meaning the war-specific shock was proportionally larger in cheaper-gas regions even though the pre-existing upward trend was smaller there.

---

## Step 5: Outlier Detection

**What I did:** Applied two outlier detection methods — IQR (1.5x) and Z-score (|z| > 2) — across the key numeric columns.

### IQR Method Results

**Absolute price increase (fences: $0.64 - $0.96):**
- Upper outliers (3): Hawaii (+$1.05), California (+$1.01), Washington (+$0.97)
- No lower outliers

**Percentage increase (fences: 23.1% - 30.8%):**
- Upper outlier (1): Kentucky (31.0%)
- Lower outliers (2): California (22.3%), Oregon (23.0%)

**Current price (fences: $2.87 - $4.61):**
- Upper outliers (5): California ($5.53), Washington ($5.15), Hawaii ($5.07), Oregon ($4.70), Nevada ($4.66)
- No lower outliers

### Z-Score Method Results

**Absolute increase (|z| > 2):**
- Hawaii (z=3.40), California (z=2.84), Washington (z=2.28) — all West/Pacific

**Percentage increase (|z| > 2):**
- Kentucky (z=2.51) — high outlier
- California (z=-2.67), Oregon (z=-2.26), Washington (z=-2.14) — low outliers

### Outlier Summary

Two clusters of outliers emerged:

1. **Pacific Coast cluster (CA, WA, HI, OR, NV):** Outliers on absolute price increase and current price level. These states have structurally higher gas prices (taxes, regulations, refinery capacity, island logistics for HI) and the war amplified their already-elevated levels. They are NOT outliers on percentage increase — in fact CA, WA, and OR have the *lowest* percentage increases in the country.

2. **Kentucky:** The single standout outlier on percentage increase (31.0% vs national avg of 26.8%). Within the South region, Kentucky's z-score is 3.21 — more than 3 standard deviations above the regional mean. The next closest Southern state is Arkansas at 28.6%. Kentucky's +$0.88 absolute increase is also high for a state with a $2.84 pre-war price — it behaves more like a West Coast state on absolute increase while having a Southern-level base price. This anomaly deserves investigation (possible factors: refinery disruptions, pipeline dependencies, state tax changes, or data quality issues).

---

## Summary of Key Findings

1. **Absolute vs. percentage tells opposite stories.** West Coast states dominate absolute dollar increases (HI +$1.05, CA +$1.01). Southern/Midwestern states dominate percentage increases (KY 31.0%, AR 28.6%). The choice of metric changes the narrative about who is "most impacted."

2. **Strong regional stratification.** The West averages +$0.87, the South +$0.77. But on percentage terms, the South (28.1%) outpaces the West (25.5%). The Northeast is remarkably uniform — all 11 states within a $0.04 range of each other on absolute increase.

3. **Pre-war price is the strongest predictor.** r=0.89 between pre-war price and absolute increase. States that were already expensive got hit hardest in dollar terms. This suggests the war shock was roughly multiplicative (proportional to existing price) rather than additive (flat dollar amount across states).

4. **War period accounts for ~70% of Jan-Mar price increase.** Prices were already trending up, but the war approximately doubled the rate. South and Midwest saw slightly higher war-attributable shares (71-72%) vs West and Northeast (67-68%).

5. **Kentucky is a genuine anomaly.** It is 3.2 standard deviations above the South regional mean on percentage increase and appears in outlier lists for both methods. Worth investigating.

6. **No data quality issues detected.** Zero nulls, all derived columns verify correctly, national average is internally consistent at $3.88.
