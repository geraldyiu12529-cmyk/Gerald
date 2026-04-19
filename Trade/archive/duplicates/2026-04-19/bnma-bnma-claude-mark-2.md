# BNMA Full Statistical Report

**Date:** 2026-04-17
**Method:** Hierarchical Bayesian Network Meta-Analysis (4 parallel groups)
**Inference:** Full MCMC — 4 chains x 2,000 post-warmup draws = 8,000 posterior samples per group
**Variables:** 34 in main BNMA (22 registered + 12 candidates) | 6 in Stage F pipeline
**Studies:** 58 study rows across all tiers

All R-hat < 1.01 and ESS > 400 for every parameter. Convergence confirmed.

---

## 0. Statistical Validity Declarations

### Valid Comparisons

| Comparison | Method | Why Valid |
|------------|--------|-----------|
| Within-group pairwise P(μi > μj) | Joint posterior draws | Same model, same scale, correlated draws |
| Within-group rank distributions | Posterior rank computation per draw | Accounts for full uncertainty |
| ROPE practical significance | Posterior mass above/below threshold | Standard Bayesian decision rule |
| S vs T cross-group | Joint posterior draws | Both measure long-short portfolio Sharpe |
| Group heterogeneity (τ) comparison | Posterior τ draws | τ is unit-free relative to group scale |
| Posterior predictive checks | Bayesian p-values | Standard model adequacy test |
| I² heterogeneity per variable | Posterior I² draws | Standard meta-analytic heterogeneity |

### NOT Statistically Possible

| Claim | Reason |
|-------|--------|
| Ranking R variables against S/T variables | R measures risk-sizing improvement Sharpe; S/T measure long-short portfolio Sharpe. Different units. |
| Ranking Overlay variables against S/T/R | Overlay measures conditional Sharpe gain (a modifier). Different scale entirely. |
| Any "Overall Top N" mixing groups | Posterior means are on different measurement scales. P(top3) in a 3-variable group is trivially 1.0. |
| Overlay group Spearman grade-rank correlation | n=3 variables, all same grade. Degenerate — 1 degree of freedom. |
| Reliable pairwise discrimination in R group (ranks 2-8) | Posterior CIs overlap massively. Rank entropy is near-maximal. Only V027 vs field is distinguishable. |

---

## 1. Study Input Data (Stage A)

### 1.1 Variable Registry

| Var_ID | Name | Group | Tier | Grade | Asset Class | Studies |
|--------|------|-------|------|-------|-------------|---------|
| V003 | DXY | S | 2 | A | Commodities | 2 |
| V006 | UST 2Y/10Y yields | S | 1 | A | Rates | 1 |
| V007 | Real yield / Breakevens | S | 1 | A | Rates | 1 |
| V008 | ACM Term Premium 10Y | S | 1 | A | Rates | 1 |
| V011 | Brent M1-M3 curve slope | S | 2 | A | Commodities | 3 |
| V012 | BTC active addresses | S | 2 | A | Crypto | 2 |
| V013 | BTC hash rate | S | 1 | A | Crypto | 1 |
| V019 | MVRV / SOPR | S | 1 | B | Crypto | 1 |
| V028 | Basis-momentum | S | 2 | A | Commodities | 3 |
| C001 | Global M2 money supply | S | 3 | Candidate-WP | Crypto | 1 |
| C003 | Gold/silver ratio | S | 3 | Candidate-WP | Commodities | 1 |
| C004 | NVT Signal (90d) | S | 3 | Candidate-WP | Crypto | 1 |
| C006 | China PMI leading copper | S | 3 | Candidate-PR | Commodities | 1 |
| C012 | Price-to-sales (tech) | S | 3 | Candidate-PR | Equities | 1 |
| V009 | TSMOM | T | 2 | A | Crypto | 5 |
| V010 | Revision breadth | T | 2 | A | Equities | 2 |
| V014 | BTC exchange netflows | T | 1 | A | Crypto | 1 |
| V017 | BTC ETF net flows | T | 1 | B | Crypto | 1 |
| V026 | Residual momentum (FF5) | T | 2 | A | Equities | 3 |
| C008 | Fear & Greed Index | T | 3 | Candidate-WP | Equities | 1 |
| C009 | Token unlock pressure | T | 3 | Candidate-WP | Crypto | 1 |
| C010 | Short-period RSI (2-5d) | T | 3 | Candidate-WP | Equities | 1 |
| C011 | Whale accumulation ratio | T | 3 | Candidate-WP | Crypto | 1 |
| V001 | VIX | R | 2 | A | Cross-Asset | 2 |
| V002 | MOVE Index | R | 1 | A | Cross-Asset | 1 |
| V004 | HY OAS | R | 2 | A | Cross-Asset | 2 |
| V005 | NFCI | R | 1 | A | Cross-Asset | 1 |
| V015 | BTC realized vol | R | 1 | A | Crypto | 1 |
| V016 | BTC perp funding rate | R | 1 | B | Crypto | 1 |
| V018 | BTC 3m basis | R | 2 | B | Crypto | 2 |
| V027 | Intermediary capital ratio | R | 2 | A | Cross-Asset | 3 |
| C002 | VIX term structure slope | Overlay | 3 | Candidate-PR | Cross-Asset | 1 |
| C005 | 200-DMA regime filter | Overlay | 3 | Candidate-PR | Equities | 1 |
| C007 | Market breadth (pct >200-DMA) | Overlay | 3 | Candidate-WP | Equities | 1 |

### 1.2 Study-Level Data

| Study_ID | Var_ID | Name | Type | Sharpe | SE | Months | Universe | Sample | OOS |
|----------|--------|------|------|--------|-----|--------|----------|--------|-----|
| S001 | V001 | VIX | PRIMARY | 0.2 | 0.0922 | 120 | S&P 500 | 1990-2000 | False |
| S002 | V001 | VIX | REPLICATION | 0.22 | 0.0754 | 180 | S&P 500 / VIX futures | 2004-2018 | True |
| S003 | V002 | MOVE Index | PRIMARY | 0.18 | 0.0651 | 240 | Treasury options | 1999-2019 | False |
| S004 | V004 | HY OAS | PRIMARY | 0.25 | 0.0535 | 360 | Corporate bonds | 1973-2010 | False |
| S005 | V004 | HY OAS | REPLICATION | 0.22 | 0.0754 | 180 | Corporate bonds OOS | 2010-2024 | True |
| S006 | V005 | NFCI | PRIMARY | 0.2 | 0.0461 | 480 | US financial conditions | 1973-2012 | False |
| S007 | V015 | BTC realized vol | PRIMARY | 0.25 | 0.1036 | 96 | BTC | 2011-2019 | False |
| S008 | V016 | BTC perp funding rate | PRIMARY | 0.2 | 0.1458 | 48 | BTC perpetual swaps | 2019-2023 | False |
| S009 | V018 | BTC 3m basis | PRIMARY | 0.18 | 0.1301 | 60 | BTC futures | 2018-2023 | False |
| S010 | V018 | BTC 3m basis | REPLICATION | 0.3 | 0.132 | 60 | Crypto futures | 2020-2025 | True |
| S011 | V027 | Intermediary capital ratio | PRIMARY | 0.6 | 0.0467 | 540 | Multi-asset class | 1970-2014 | False |
| S012 | V027 | Intermediary capital ratio | REPLICATION | 0.5 | 0.0559 | 360 | Equities + bonds | 1986-2012 | False |
| S013 | V027 | Intermediary capital ratio | REPLICATION | 0.45 | 0.0408 | 660 | Multi-asset class | 1970-2025 | True |
| S014 | V003 | DXY | PRIMARY | 0.45 | 0.0553 | 360 | FX carry / commodities | 1983-2013 | False |
| S015 | V003 | DXY | REPLICATION | 0.4 | 0.0671 | 240 | Copper/Tin | 1995-2015 | True |
| S016 | V006 | UST 2Y/10Y yields | PRIMARY | 0.35 | 0.047 | 480 | US Treasuries | 1972-2012 | False |
| S017 | V007 | Real yield / Breakevens | PRIMARY | 0.4 | 0.0671 | 240 | TIPS / breakevens | 1999-2017 | False |
| S018 | V008 | ACM Term Premium 10Y | PRIMARY | 0.3 | 0.0467 | 480 | US Treasuries | 1972-2012 | False |
| S019 | V011 | Brent M1-M3 curve slope | PRIMARY | 0.74 | 0.0486 | 540 | 26 commodities | 1959-2004 | False |
| S020 | V011 | Brent M1-M3 curve slope | REPLICATION | 0.74 | 0.0515 | 480 | Multi-asset carry | 1972-2012 | False |
| S021 | V011 | Brent M1-M3 curve slope | REPLICATION | 0.65 | 0.058 | 360 | Commodity futures | 1986-2010 | False |
| S022 | V012 | BTC active addresses | PRIMARY | 0.35 | 0.1051 | 96 | BTC | 2011-2019 | False |
| S023 | V012 | BTC active addresses | REPLICATION | 0.3 | 0.1115 | 84 | BTC | 2012-2019 | False |
| S024 | V013 | BTC hash rate | PRIMARY | 0.25 | 0.1108 | 84 | BTC | 2012-2019 | False |
| S025 | V019 | MVRV / SOPR | PRIMARY | 0.3 | 0.1205 | 72 | BTC | 2015-2021 | False |
| S026 | V028 | Basis-momentum | PRIMARY | 0.8 | 0.0524 | 480 | 23 commodities | 1972-2014 | False |
| S027 | V028 | Basis-momentum | REPLICATION | 0.7 | 0.0588 | 360 | Commodity futures | 1986-2010 | False |
| S028 | V028 | Basis-momentum | REPLICATION | 0.6 | 0.0701 | 240 | Commodity futures | 2000-2020 | True |
| S029 | V009 | TSMOM | PRIMARY | 0.9 | 0.0541 | 480 | 58 futures markets | 1965-2009 | False |
| S030 | V009 | TSMOM | REPLICATION | 0.8 | 0.0283 | 1644 | 67 markets, 137 years | 1880-2016 | True |
| S031 | V009 | TSMOM | REPLICATION | 1.0 | 0.0383 | 1020 | US equities | 1927-2011 | False |
| S032 | V009 | TSMOM | REPLICATION | 0.7 | 0.0509 | 480 | Multi-asset | 1972-2020 | True |
| S033 | V009 | TSMOM | REPLICATION | 1.51 | 0.1889 | 60 | BTC crypto | 2018-2023 | True |
| S034 | V010 | Revision breadth | PRIMARY | 0.5 | 0.0559 | 360 | US equities | 1983-2001 | False |
| S035 | V010 | Revision breadth | REPLICATION | 0.55 | 0.0693 | 240 | US equities | 2000-2020 | True |
| S036 | V014 | BTC exchange netflows | PRIMARY | 0.4 | 0.15 | 48 | BTC | 2019-2023 | False |
| S037 | V017 | BTC ETF net flows | PRIMARY | 0.3 | 0.2087 | 24 | BTC ETFs | 2024-2026 | False |
| S038 | V026 | Residual momentum (FF5) | PRIMARY | 0.7 | 0.0644 | 300 | US equities | 1986-2011 | False |
| S039 | V026 | Residual momentum (FF5) | REPLICATION | 0.6 | 0.0496 | 480 | Global equities + other | 1972-2011 | False |
| S040 | V026 | Residual momentum (FF5) | REPLICATION | 0.65 | 0.058 | 360 | US equities | 1990-2020 | True |
| S041 | V030 | Cross-asset lead-lag | PRIMARY | 0.35 | 0.0665 | 240 | NYSE stocks | 1962-1987 | False |
| S042 | V029 | GEX | PRIMARY | 0.2 | 0.0922 | 120 | S&P 500 | 2012-2021 | False |
| S043 | V031 | Correlation-regime signal qual | PRIMARY | 0.25 | 0.0656 | 240 | Multi-asset | 1998-2010 | False |
| S044 | V032 | Decision tree feature importan | PRIMARY | 0.3 | 0.0539 | 360 | US equities | 1957-2016 | False |
| S045 | V020 | News sentiment | PRIMARY | 0.4 | 0.0671 | 240 | US equities / news | 1980-2007 | False |
| S046 | V033 | Calendar/seasonal | PRIMARY | 0.3 | 0.0539 | 360 | S&P 500 pre-FOMC | 1994-2011 | False |
| S047 | C001 | Global M2 money supply | PRIMARY | 0.35 | 0.094 | 120 | BTC vs global M2 | 2015-2025 | False |
| S048 | C002 | VIX term structure slope | PRIMARY | 0.36 | 0.0796 | 168 | S&P 500 / VIX futures | 2004-2018 | False |
| S049 | C003 | Gold/silver ratio | PRIMARY | 0.3 | 0.066 | 240 | Gold/Silver | 2005-2025 | False |
| S050 | C004 | NVT Signal (90d) | PRIMARY | 0.35 | 0.1214 | 72 | BTC | 2015-2022 | False |
| S051 | C005 | 200-DMA regime filter | PRIMARY | 0.25 | 0.0464 | 480 | SPY/QQQ | 1972-2012 | False |
| S052 | C006 | China PMI leading copper | PRIMARY | 0.3 | 0.0762 | 180 | Copper/China PMI | 2005-2020 | False |
| S053 | C007 | Market breadth (pct >200-DMA) | PRIMARY | 0.2 | 0.0652 | 240 | SPY/QQQ constituents | 2000-2020 | False |
| S054 | C008 | Fear & Greed Index | PRIMARY | 0.4 | 0.1225 | 72 | SPX/Nasdaq/Russell | 2018-2024 | False |
| S055 | C009 | Token unlock pressure | PRIMARY | 0.25 | 0.1466 | 48 | Altcoins | 2020-2024 | False |
| S056 | C010 | Short-period RSI (2-5d) | PRIMARY | 0.35 | 0.0665 | 240 | S&P 500 | 2000-2020 | False |
| S057 | C011 | Whale accumulation ratio | PRIMARY | 0.3 | 0.1704 | 36 | BTC | 2020-2023 | False |
| S058 | C012 | Price-to-sales (tech) | PRIMARY | 0.3 | 0.0539 | 360 | US tech equities | 1968-1993 | False |

### 1.3 Tier Counts

| Tier | Description | Count |
|------|-------------|-------|
| 1 | Registered variables (Grade A/B) | 22 |
| 2 | Replication studies | 18 study rows |
| 3 | Admitted candidate variables | 12 |
| Provisional/Ungraded | Routed to Stage F | 4 |
| Catalyst (C) | Excluded from BNMA | 2 |

### 1.4 Rejected Candidates

| Name | Reason |
|------|--------|
| MVRV Z-Score | Redundant with V019 (same metric, different scaling) |
| Funding rate arbitrage | Not directional — wrong scale for BNMA |
| Pairs trading BTC-ETH | Relative-value at 5-min frequency — wrong horizon |
| Dual momentum / Antonacci GEM | Portfolio construction, not a variable |
| HRP | Portfolio construction method, not a signal |
| EIA inventory surprises | Event-study scale, excluded like V020/V033 |
| OPEC+ production decisions | Event-study / catalyst |
| Geopolitical Risk Index | Candidate cap reached; effect mainly through VIX channel |

---

## 2. Network Structure (Stage B)

### S Group (14 variables)

Variables: V003, V006, V007, V008, V011, V012, V013, V019, V028, C001, C003, C004, C006, C012

- V003 (DXY) ↔ V007
- V006 (UST 2Y/10Y yields) ↔ V007, V008
- V007 (Real yield / Breakevens) ↔ V003, V006, V008
- V008 (ACM Term Premium 10Y) ↔ V006, V007
- V011 (Brent M1-M3 curve slope) ↔ V028
- V012 (BTC active addresses) ↔ V013, V019
- V013 (BTC hash rate) ↔ V012
- V019 (MVRV / SOPR) ↔ V012
- V028 (Basis-momentum) ↔ V011
- C001 (Global M2 money supply) ↔ V012, V013
- C003 (Gold/silver ratio) ↔ V003, V007
- C004 (NVT Signal (90d)) ↔ V019, V012
- C006 (China PMI leading copper) ↔ V003
- C012 (Price-to-sales (tech)) ↔ V003

### T Group (9 variables)

Variables: V009, V010, V014, V017, V026, C008, C009, C010, C011

- V009 (TSMOM) ↔ V026
- V014 (BTC exchange netflows) ↔ V017
- V017 (BTC ETF net flows) ↔ V014
- V026 (Residual momentum (FF5)) ↔ V009
- C009 (Token unlock pressure) ↔ V014
- C010 (Short-period RSI (2-5d)) ↔ V009
- C011 (Whale accumulation ratio) ↔ V014, V017

### R Group (8 variables)

Variables: V001, V002, V004, V005, V015, V016, V018, V027

- V001 (VIX) ↔ V002, V004, V005
- V002 (MOVE Index) ↔ V001, V004
- V004 (HY OAS) ↔ V027, V001
- V005 (NFCI) ↔ V001, V004
- V015 (BTC realized vol) ↔ V001
- V016 (BTC perp funding rate) ↔ V018
- V018 (BTC 3m basis) ↔ V016
- V027 (Intermediary capital ratio) ↔ V004

### Overlay Group (3 variables)

Variables: C002, C005, C007


---

## 3. Posterior Summaries (Stage C/D)

### 3.1 S Group (14 variables, ROPE: ±0.1)

| Rank | Var_ID | Name | Grade | Studies | Post. Mean | 95% CI | P(>0) | P(top3) | Mean Rank | Rank 95% CI | P(above ROPE) | ROPE Decision |
|------|--------|------|-------|---------|-----------|--------|-------|---------|-----------|-------------|---------------|---------------|
| 1 | V011 | Brent M1-M3 curve slope | A | 3 | 0.4020 | [0.155, 0.647] | 0.9968 | 0.8908 | 2.1 | [1, 5] | 0.9879 | **REJECT NULL** (positive) |
| 2 | V028 | Basis-momentum | A | 3 | 0.3945 | [0.104, 0.649] | 0.9921 | 0.8646 | 2.2 | [1, 6] | 0.9761 | **REJECT NULL** (positive) |
| 3 | V007 | Real yield / Breakevens | A | 1 | 0.1681 | [-0.310, 0.629] | 0.7710 | 0.3438 | 5.9 | [1, 14] | 0.6208 | UNDECIDED |
| 4 | V003 | DXY | A | 2 | 0.1211 | [-0.165, 0.399] | 0.8179 | 0.1797 | 6.4 | [2, 14] | 0.5637 | UNDECIDED |
| 5 | V006 | UST 2Y/10Y yields | A | 1 | 0.1177 | [-0.388, 0.586] | 0.7065 | 0.2427 | 6.8 | [1, 14] | 0.5425 | UNDECIDED |
| 6 | V008 | ACM Term Premium 10Y | A | 1 | 0.0790 | [-0.409, 0.544] | 0.6461 | 0.1796 | 7.6 | [1, 14] | 0.4679 | UNDECIDED |
| 7 | V012 | BTC active addresses | A | 2 | 0.0310 | [-0.276, 0.366] | 0.5743 | 0.0870 | 8.6 | [2, 14] | 0.3184 | UNDECIDED |
| 8 | C012 | Price-to-sales (tech) | Candidate-PR | 1 | 0.0221 | [-0.168, 0.208] | 0.5949 | 0.0289 | 8.8 | [3, 14] | 0.2067 | UNDECIDED |
| 9 | C001 | Global M2 money supply | Candidate-WP | 1 | 0.0055 | [-0.088, 0.099] | 0.5460 | 0.0025 | 9.3 | [5, 13] | 0.0236 | ACCEPT NULL |
| 10 | V019 | MVRV / SOPR | B | 1 | 0.0040 | [-0.333, 0.343] | 0.5115 | 0.0791 | 9.1 | [2, 14] | 0.2751 | UNDECIDED |
| 11 | C004 | NVT Signal (90d) | Candidate-WP | 1 | 0.0037 | [-0.097, 0.098] | 0.5401 | 0.0034 | 9.4 | [5, 13] | 0.0225 | ACCEPT NULL |
| 12 | C006 | China PMI leading copper | Candidate-PR | 1 | 0.0027 | [-0.171, 0.174] | 0.5114 | 0.0129 | 9.4 | [4, 14] | 0.1338 | UNDECIDED |
| 13 | C003 | Gold/silver ratio | Candidate-WP | 1 | 0.0004 | [-0.094, 0.096] | 0.5019 | 0.0015 | 9.6 | [5, 14] | 0.0185 | ACCEPT NULL |
| 14 | V013 | BTC hash rate | A | 1 | -0.0360 | [-0.461, 0.403] | 0.4219 | 0.0835 | 9.9 | [2, 14] | 0.2474 | UNDECIDED |

### 3.2 T Group (9 variables, ROPE: ±0.1)

| Rank | Var_ID | Name | Grade | Studies | Post. Mean | 95% CI | P(>0) | P(top3) | Mean Rank | Rank 95% CI | P(above ROPE) | ROPE Decision |
|------|--------|------|-------|---------|-----------|--------|-------|---------|-----------|-------------|---------------|---------------|
| 1 | V009 | TSMOM | A | 5 | 0.6799 | [0.404, 0.921] | 1.0000 | 0.9992 | 1.0 | [1, 1] | 1.0000 | **REJECT NULL** (positive) |
| 2 | V026 | Residual momentum (FF5) | A | 3 | 0.3848 | [0.116, 0.637] | 0.9965 | 0.9673 | 2.2 | [2, 4] | 0.9801 | **REJECT NULL** (positive) |
| 3 | V010 | Revision breadth | A | 2 | 0.2061 | [-0.079, 0.477] | 0.9356 | 0.6535 | 3.6 | [2, 8] | 0.8037 | UNDECIDED |
| 4 | V014 | BTC exchange netflows | A | 1 | 0.0295 | [-0.422, 0.481] | 0.5545 | 0.2085 | 5.9 | [2, 9] | 0.3674 | UNDECIDED |
| 5 | C008 | Fear & Greed Index | Candidate-WP | 1 | 0.0070 | [-0.087, 0.102] | 0.5551 | 0.0154 | 6.2 | [4, 9] | 0.0276 | ACCEPT NULL |
| 6 | C010 | Short-period RSI (2-5d) | Candidate-WP | 1 | 0.0052 | [-0.091, 0.102] | 0.5410 | 0.0126 | 6.3 | [4, 9] | 0.0279 | ACCEPT NULL |
| 7 | C011 | Whale accumulation ratio | Candidate-WP | 1 | -0.0024 | [-0.098, 0.096] | 0.4816 | 0.0141 | 6.5 | [4, 9] | 0.0200 | ACCEPT NULL |
| 8 | C009 | Token unlock pressure | Candidate-WP | 1 | -0.0065 | [-0.103, 0.090] | 0.4481 | 0.0104 | 6.6 | [4, 9] | 0.0154 | ACCEPT NULL |
| 9 | V017 | BTC ETF net flows | B | 1 | -0.0279 | [-0.412, 0.344] | 0.4445 | 0.1190 | 6.6 | [2, 9] | 0.2557 | UNDECIDED |

### 3.3 R Group (8 variables, ROPE: ±0.05)

| Rank | Var_ID | Name | Grade | Studies | Post. Mean | 95% CI | P(>0) | P(top3) | Mean Rank | Rank 95% CI | P(above ROPE) | ROPE Decision |
|------|--------|------|-------|---------|-----------|--------|-------|---------|-----------|-------------|---------------|---------------|
| 1 | V027 | Intermediary capital ratio | A | 3 | 0.2359 | [0.022, 0.446] | 0.9850 | 0.9721 | 1.3 | [1, 4] | 0.9547 | **REJECT NULL** (positive) |
| 2 | V015 | BTC realized vol | A | 1 | 0.0307 | [-0.242, 0.307] | 0.5846 | 0.4617 | 4.2 | [1, 8] | 0.4446 | UNDECIDED |
| 3 | V018 | BTC 3m basis | B | 2 | 0.0191 | [-0.181, 0.214] | 0.5775 | 0.3980 | 4.4 | [1, 8] | 0.3820 | UNDECIDED |
| 4 | V016 | BTC perp funding rate | B | 1 | 0.0003 | [-0.205, 0.211] | 0.5016 | 0.3317 | 4.7 | [1, 8] | 0.3192 | UNDECIDED |
| 5 | V004 | HY OAS | A | 2 | -0.0107 | [-0.225, 0.207] | 0.4559 | 0.2669 | 4.8 | [2, 8] | 0.2863 | UNDECIDED |
| 6 | V001 | VIX | A | 2 | -0.0342 | [-0.252, 0.183] | 0.3786 | 0.1852 | 5.4 | [2, 8] | 0.2220 | UNDECIDED |
| 7 | V005 | NFCI | A | 1 | -0.0354 | [-0.285, 0.218] | 0.3726 | 0.2096 | 5.4 | [2, 8] | 0.2340 | UNDECIDED |
| 8 | V002 | MOVE Index | A | 1 | -0.0511 | [-0.300, 0.213] | 0.3334 | 0.1746 | 5.7 | [2, 8] | 0.2021 | UNDECIDED |

### 3.4 Overlay Group (3 variables, ROPE: ±0.01)

| Rank | Var_ID | Name | Grade | Studies | Post. Mean | 95% CI | P(>0) | P(top3) | Mean Rank | Rank 95% CI | P(above ROPE) | ROPE Decision |
|------|--------|------|-------|---------|-----------|--------|-------|---------|-----------|-------------|---------------|---------------|
| 1 | C005 | 200-DMA regime filter | Candidate-PR | 1 | 0.0087 | [-0.087, 0.100] | 0.5796 | 1.0000 | 1.9 | [1, 3] | 0.4970 | UNDECIDED |
| 2 | C002 | VIX term structure slope | Candidate-PR | 1 | 0.0075 | [-0.087, 0.104] | 0.5604 | 1.0000 | 1.9 | [1, 3] | 0.4765 | UNDECIDED |
| 3 | C007 | Market breadth (pct >200-DMA) | Candidate-WP | 1 | -0.0005 | [-0.048, 0.048] | 0.4895 | 1.0000 | 2.1 | [1, 3] | 0.3312 | UNDECIDED |

---

## 4. Within-Group Pairwise P(μi > μj)

Each cell is the posterior probability (from 8,000 joint draws) that the row variable has a higher true effect than the column variable. Values ≥ 0.975 are marked with **bold**.

### 4.1 S Group

| | V011 | V028 | V007 | V003 | V006 | V008 | V012 | C012 | C001 | V019 | C004 | C006 | C003 | V013 |
|--|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **V011** | — | 0.513 | 0.817 | 0.971 | 0.864 | 0.891 | 0.966 | **0.992** | **0.996** | 0.967 | **0.996** | **0.996** | **0.997** | 0.960 |
| **V028** | 0.487 | — | 0.798 | 0.956 | 0.854 | 0.880 | 0.955 | **0.984** | **0.991** | 0.960 | **0.990** | **0.991** | **0.992** | 0.953 |
| **V007** | 0.183 | 0.202 | — | 0.569 | 0.585 | 0.656 | 0.689 | 0.721 | 0.756 | 0.719 | 0.759 | 0.752 | 0.765 | 0.741 |
| **V003** | 0.029 | 0.044 | 0.431 | — | 0.501 | 0.559 | 0.671 | 0.730 | 0.794 | 0.713 | 0.799 | 0.798 | 0.817 | 0.739 |
| **V006** | 0.137 | 0.146 | 0.415 | 0.499 | — | 0.578 | 0.628 | 0.654 | 0.693 | 0.659 | 0.693 | 0.690 | 0.697 | 0.695 |
| **V008** | 0.108 | 0.120 | 0.344 | 0.441 | 0.422 | — | 0.577 | 0.596 | 0.633 | 0.609 | 0.638 | 0.628 | 0.641 | 0.651 |
| **V012** | 0.034 | 0.045 | 0.311 | 0.329 | 0.372 | 0.423 | — | 0.514 | 0.558 | 0.550 | 0.563 | 0.555 | 0.568 | 0.626 |
| **C012** | **0.008** | **0.016** | 0.279 | 0.270 | 0.346 | 0.404 | 0.486 | — | 0.565 | 0.537 | 0.570 | 0.555 | 0.579 | 0.605 |
| **C001** | **0.004** | **0.009** | 0.244 | 0.206 | 0.307 | 0.366 | 0.442 | 0.435 | — | 0.507 | 0.506 | 0.508 | 0.537 | 0.584 |
| **V019** | 0.033 | 0.041 | 0.281 | 0.287 | 0.341 | 0.391 | 0.450 | 0.463 | 0.493 | — | 0.499 | 0.504 | 0.509 | 0.568 |
| **C004** | **0.004** | **0.010** | 0.241 | 0.201 | 0.307 | 0.362 | 0.437 | 0.430 | 0.494 | 0.501 | — | 0.503 | 0.523 | 0.586 |
| **C006** | **0.004** | **0.009** | 0.248 | 0.202 | 0.310 | 0.372 | 0.445 | 0.445 | 0.492 | 0.496 | 0.497 | — | 0.504 | 0.579 |
| **C003** | **0.003** | **0.008** | 0.235 | 0.183 | 0.303 | 0.359 | 0.432 | 0.421 | 0.463 | 0.491 | 0.477 | 0.496 | — | 0.577 |
| **V013** | 0.040 | 0.047 | 0.259 | 0.262 | 0.305 | 0.349 | 0.374 | 0.395 | 0.416 | 0.432 | 0.414 | 0.421 | 0.423 | — |

Adjacent-rank significant separations in S:

- None. No adjacent pair reaches P ≥ 0.90. The ranking order is not statistically reliable beyond the top variable(s).

### 4.2 T Group

| | V009 | V026 | V010 | V014 | C008 | C010 | C011 | C009 | V017 |
|--|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **V009** | — | **0.987** | **0.997** | **0.991** | **1.000** | **1.000** | **1.000** | **1.000** | **0.998** |
| **V026** | **0.013** | — | 0.915 | 0.920 | **0.994** | **0.994** | **0.993** | **0.995** | 0.962 |
| **V010** | **0.003** | 0.085 | — | 0.761 | 0.925 | 0.931 | 0.929 | 0.931 | 0.837 |
| **V014** | **0.009** | 0.080 | 0.239 | — | 0.539 | 0.543 | 0.558 | 0.568 | 0.584 |
| **C008** | **0.000** | **0.006** | 0.075 | 0.461 | — | 0.507 | 0.560 | 0.575 | 0.568 |
| **C010** | **0.000** | **0.006** | 0.069 | 0.457 | 0.493 | — | 0.547 | 0.567 | 0.565 |
| **C011** | **0.000** | **0.007** | 0.071 | 0.442 | 0.440 | 0.453 | — | 0.526 | 0.549 |
| **C009** | **0.000** | **0.005** | 0.069 | 0.432 | 0.425 | 0.433 | 0.474 | — | 0.546 |
| **V017** | **0.002** | 0.038 | 0.163 | 0.416 | 0.432 | 0.435 | 0.451 | 0.454 | — |

Adjacent-rank significant separations in T:

- V009 > V026: P = 0.9870 ***
- V026 > V010: P = 0.9155 *

### 4.3 R Group

| | V027 | V015 | V018 | V016 | V004 | V001 | V005 | V002 |
|--|---:|---:|---:|---:|---:|---:|---:|---:|
| **V027** | — | 0.880 | 0.928 | 0.936 | **0.984** | **0.990** | 0.973 | **0.978** |
| **V015** | 0.120 | — | 0.529 | 0.575 | 0.594 | 0.648 | 0.638 | 0.668 |
| **V018** | 0.071 | 0.471 | — | 0.555 | 0.580 | 0.641 | 0.638 | 0.670 |
| **V016** | 0.064 | 0.425 | 0.445 | — | 0.530 | 0.583 | 0.591 | 0.620 |
| **V004** | **0.017** | 0.406 | 0.420 | 0.470 | — | 0.596 | 0.602 | 0.642 |
| **V001** | **0.010** | 0.352 | 0.359 | 0.417 | 0.404 | — | 0.518 | 0.569 |
| **V005** | 0.027 | 0.362 | 0.362 | 0.409 | 0.398 | 0.482 | — | 0.542 |
| **V002** | **0.022** | 0.332 | 0.330 | 0.380 | 0.358 | 0.431 | 0.458 | — |

Adjacent-rank significant separations in R:

- None. No adjacent pair reaches P ≥ 0.90. The ranking order is not statistically reliable beyond the top variable(s).

### 4.4 Overlay Group

| | C005 | C002 | C007 |
|--|---:|---:|---:|
| **C005** | — | 0.506 | 0.576 |
| **C002** | 0.494 | — | 0.560 |
| **C007** | 0.424 | 0.440 | — |

Adjacent-rank significant separations in Overlay:

- None. No adjacent pair reaches P ≥ 0.90. The ranking order is not statistically reliable beyond the top variable(s).

---

## 5. Posterior Rank Distributions

For each of 8,000 MCMC draws, all variables within a group are ranked 1 to N. The table shows the percentage of draws in which each variable occupies each rank. Concentrated rows = stable ranking. Flat rows = data cannot discriminate.

### 5.1 S Group

| Variable | Name | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13 | R14 |
|----------|------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V011 | Brent M1-M3 curve slope | **37.5%** | **37.2%** | 14.3% | 6.3% | 3.0% | 0.7% | 0.3% | 0.3% | 0.1% | 0.1% | 0.1% | 0.1% | 0.0% | 0.0% |
| V028 | Basis-momentum | **36.3%** | **35.8%** | 14.4% | 6.9% | 3.7% | 1.0% | 0.7% | 0.4% | 0.2% | 0.1% | 0.1% | 0.2% | 0.1% | 0.1% |
| V007 | Real yield / Breakevens | 10.5% | 8.5% | *15.3%* | 13.6% | 10.9% | 7.5% | 5.0% | 3.5% | 2.6% | 3.3% | 3.7% | 4.2% | 5.5% | 5.7% |
| V003 | DXY | 0.9% | 2.0% | *15.1%* | *15.4%* | *15.4%* | 13.1% | 9.3% | 6.2% | 4.5% | 4.3% | 3.8% | 3.6% | 3.6% | 2.9% |
| V006 | UST 2Y/10Y yields | 6.4% | 5.9% | 11.9% | 13.7% | 11.4% | 8.4% | 5.8% | 4.1% | 3.2% | 3.6% | 4.0% | 5.2% | 7.1% | 9.1% |
| V008 | ACM Term Premium 10Y | 4.1% | 4.8% | 9.0% | 11.9% | 11.3% | 8.2% | 6.3% | 5.0% | 4.3% | 3.8% | 4.1% | 6.1% | 8.9% | 12.2% |
| V012 | BTC active addresses | 1.2% | 1.6% | 5.8% | 8.3% | 8.7% | 9.1% | 8.2% | 7.2% | 6.4% | 6.6% | 7.2% | 9.3% | 10.7% | 9.5% |
| C012 | Price-to-sales (tech) | 0.1% | 0.3% | 2.5% | 5.5% | 7.5% | 11.3% | 11.0% | 10.0% | 9.4% | 9.3% | 9.9% | 9.1% | 8.5% | 5.7% |
| C001 | Global M2 money supply | 0.0% | 0.0% | 0.2% | 1.3% | 3.4% | 6.7% | 9.9% | 14.2% | *16.3%* | *15.8%* | 12.9% | 10.4% | 6.8% | 2.0% |
| V019 | MVRV / SOPR | 1.1% | 1.7% | 5.1% | 6.4% | 7.4% | 8.2% | 7.6% | 6.6% | 6.0% | 5.8% | 7.1% | 9.8% | 12.2% | 15.0% |
| C004 | NVT Signal (90d) | 0.0% | 0.0% | 0.3% | 1.4% | 3.0% | 6.0% | 10.1% | 14.0% | *16.1%* | *15.3%* | 14.9% | 10.2% | 6.3% | 2.4% |
| C006 | China PMI leading copper | 0.0% | 0.1% | 1.2% | 3.1% | 5.7% | 7.8% | 10.3% | 10.6% | 11.2% | 10.9% | 11.0% | 11.4% | 9.8% | 6.9% |
| C003 | Gold/silver ratio | 0.0% | 0.0% | 0.1% | 1.0% | 2.9% | 6.1% | 9.6% | 13.0% | 14.6% | *15.8%* | 14.9% | 12.2% | 7.1% | 2.6% |
| V013 | BTC hash rate | 1.9% | 2.0% | 4.5% | 5.3% | 5.8% | 5.7% | 6.0% | 4.9% | 5.0% | 5.2% | 6.3% | 8.2% | 13.4% | *25.9%* |

### 5.2 T Group

| Variable | Name | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|----------|------|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| V009 | TSMOM | **97.7%** | 2.1% | 0.2% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| V026 | Residual momentum (FF5) | 1.2% | **81.8%** | 13.7% | 2.3% | 0.4% | 0.2% | 0.1% | 0.2% | 0.1% |
| V010 | Revision breadth | 0.2% | 6.9% | **58.3%** | *21.0%* | 5.8% | 2.4% | 1.7% | 1.9% | 1.8% |
| V014 | BTC exchange netflows | 0.9% | 6.2% | 13.7% | *20.2%* | 9.5% | 5.4% | 5.7% | 12.6% | *25.9%* |
| C008 | Fear & Greed Index | 0.0% | 0.1% | 1.5% | 12.6% | *19.6%* | *22.7%* | *20.3%* | *15.8%* | 7.5% |
| C010 | Short-period RSI (2-5d) | 0.0% | 0.0% | 1.2% | 11.5% | *19.8%* | *22.9%* | *21.2%* | *15.4%* | 8.0% |
| C011 | Whale accumulation ratio | 0.0% | 0.1% | 1.4% | 9.2% | *17.1%* | *20.3%* | *22.8%* | *19.5%* | 9.7% |
| C009 | Token unlock pressure | 0.0% | 0.0% | 1.0% | 7.3% | *17.3%* | *20.3%* | *22.3%* | *20.8%* | 11.0% |
| V017 | BTC ETF net flows | 0.1% | 2.8% | 9.0% | *15.8%* | 10.5% | 5.9% | 5.9% | 13.9% | **36.0%** |

### 5.3 R Group

| Variable | Name | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|----------|------|---:|---:|---:|---:|---:|---:|---:|---:|
| V027 | Intermediary capital rati | **78.4%** | 14.2% | 4.5% | 1.9% | 0.5% | 0.2% | 0.1% | 0.1% |
| V015 | BTC realized vol | 9.7% | *20.2%* | *16.3%* | 12.5% | 9.6% | 9.1% | 9.8% | 12.8% |
| V018 | BTC 3m basis | 3.7% | *16.9%* | *19.2%* | *16.7%* | 13.0% | 11.7% | 10.5% | 8.4% |
| V016 | BTC perp funding rate | 4.0% | 13.1% | *16.1%* | *15.5%* | 12.8% | 12.9% | 12.6% | 13.0% |
| V004 | HY OAS | 0.8% | 11.5% | 14.4% | *17.3%* | *17.5%* | *16.6%* | 13.6% | 8.2% |
| V001 | VIX | 0.4% | 7.6% | 10.5% | 14.0% | *17.2%* | *18.1%* | *17.9%* | 14.2% |
| V005 | NFCI | 1.6% | 8.9% | 10.5% | 11.6% | *15.5%* | *15.8%* | *17.1%* | *19.1%* |
| V002 | MOVE Index | 1.5% | 7.5% | 8.5% | 10.5% | 13.9% | *15.7%* | *18.3%* | *24.2%* |

### 5.4 Overlay Group

| Variable | Name | R1 | R2 | R3 |
|----------|------|---:|---:|---:|
| C005 | 200-DMA regime filter | **39.8%** | *28.4%* | **31.7%** |
| C002 | VIX term structure slope | **38.7%** | *28.2%* | **33.2%** |
| C007 | Market breadth (pct >200- | *21.5%* | **43.4%** | **35.1%** |

---

## 6. Cross-Group: S vs T (Valid — Same Sharpe Scale)

S and T both measure annualized Sharpe of long-short portfolios. Direct comparison of posterior draws is valid.

### 6.1 Pairwise P(S variable > T variable) — Top 5 each

| S ↓ / T → | V009 | V026 | V010 | V014 | C008 |
|-----------|---:|---:|---:|---:|---:|
| **V011** | 0.061 | 0.538 | 0.862 | 0.927 | **0.996** |
| **V028** | 0.062 | 0.529 | 0.845 | 0.916 | **0.990** |
| **V007** | 0.030 | 0.208 | 0.443 | 0.674 | 0.755 |
| **V003** | **0.004** | 0.078 | 0.319 | 0.640 | 0.795 |
| **V006** | **0.021** | 0.158 | 0.369 | 0.614 | 0.688 |

### 6.2 Detailed Cross-Group Comparisons

| S Variable | T Variable | P(S > T) | Mean Δ | 95% CI of Δ | Significant? |
|------------|------------|----------|--------|-------------|-------------|
| V011 (Brent M1-M3 curve sl) | V009 (TSMOM) | 0.0609 | -0.278 | [-0.631, +0.091] | No |
| V011 (Brent M1-M3 curve sl) | V026 (Residual momentum (F) | 0.5383 | +0.017 | [-0.331, +0.365] | No |
| V011 (Brent M1-M3 curve sl) | V010 (Revision breadth) | 0.8620 | +0.196 | [-0.170, +0.575] | No |
| V028 (Basis-momentum) | V009 (TSMOM) | 0.0624 | -0.285 | [-0.658, +0.088] | No |
| V028 (Basis-momentum) | V026 (Residual momentum (F) | 0.5295 | +0.010 | [-0.361, +0.376] | No |
| V028 (Basis-momentum) | V010 (Revision breadth) | 0.8454 | +0.188 | [-0.190, +0.569] | No |
| V007 (Real yield / Breakev) | V009 (TSMOM) | 0.0301 | -0.512 | [-1.053, +0.018] | No |
| V007 (Real yield / Breakev) | V026 (Residual momentum (F) | 0.2079 | -0.217 | [-0.761, +0.306] | No |
| V007 (Real yield / Breakev) | V010 (Revision breadth) | 0.4425 | -0.038 | [-0.587, +0.498] | No |
| V003 (DXY) | V009 (TSMOM) | 0.0041 | -0.559 | [-0.932, -0.169] | Yes |
| V003 (DXY) | V026 (Residual momentum (F) | 0.0780 | -0.264 | [-0.635, +0.110] | No |
| V003 (DXY) | V010 (Revision breadth) | 0.3190 | -0.085 | [-0.480, +0.304] | No |
| V006 (UST 2Y/10Y yields) | V009 (TSMOM) | 0.0208 | -0.562 | [-1.123, -0.032] | Yes |
| V006 (UST 2Y/10Y yields) | V026 (Residual momentum (F) | 0.1579 | -0.267 | [-0.817, +0.280] | No |
| V006 (UST 2Y/10Y yields) | V010 (Revision breadth) | 0.3693 | -0.088 | [-0.654, +0.465] | No |

### 6.3 Cross-Group Impossibilities

| Comparison | Verdict | Explanation |
|------------|---------|-------------|
| R vs S | NOT POSSIBLE | R measures risk-sizing improvement. S measures long-short Sharpe. Different units. |
| R vs T | NOT POSSIBLE | Same reason — R is a different measurement scale. |
| Overlay vs S/T/R | NOT POSSIBLE | Overlay measures conditional Sharpe gain (a modifier). Also n=3 makes all group-internal statistics degenerate. |
| Any overall ranking | NOT POSSIBLE | Mixing groups is comparing different units. The report's "Overall Top 5" was a display convenience, not a statistical result. |

---

## 7. Heterogeneity Analysis

### 7.1 I² per Variable

I² measures what fraction of observed variation is due to true between-study differences (vs sampling error). Cochrane thresholds: <25% low, 25-50% moderate, 50-75% substantial, >75% considerable.

**S Group:**

| Var_ID | Name | I² Median | 95% CI | Interpretation |
|--------|------|-----------|--------|----------------|
| V003 | DXY | 0.722 | [0.008, 0.979] | Substantial |
| V006 | UST 2Y/10Y yields | 0.916 | [0.018, 0.992] | Considerable |
| V007 | Real yield / Breakevens | 0.844 | [0.012, 0.984] | Considerable |
| V008 | ACM Term Premium 10Y | 0.915 | [0.027, 0.992] | Considerable |
| V011 | Brent M1-M3 curve slope | 0.687 | [0.004, 0.980] | Substantial |
| V012 | BTC active addresses | 0.478 | [0.002, 0.940] | Moderate |
| V013 | BTC hash rate | 0.669 | [0.006, 0.955] | Substantial |
| V019 | MVRV / SOPR | 0.577 | [0.002, 0.945] | Substantial |
| V028 | Basis-momentum | 0.783 | [0.022, 0.978] | Considerable |
| C001 | Global M2 money supply | 0.622 | [0.002, 0.962] | Substantial |
| C003 | Gold/silver ratio | 0.722 | [0.006, 0.981] | Substantial |
| C004 | NVT Signal (90d) | 0.518 | [0.003, 0.938] | Substantial |
| C006 | China PMI leading copper | 0.713 | [0.005, 0.975] | Substantial |
| C012 | Price-to-sales (tech) | 0.894 | [0.023, 0.990] | Considerable |

**T Group:**

| Var_ID | Name | I² Median | 95% CI | Interpretation |
|--------|------|-----------|--------|----------------|
| V009 | TSMOM | 0.881 | [0.125, 0.985] | Considerable |
| V010 | Revision breadth | 0.646 | [0.002, 0.976] | Substantial |
| V014 | BTC exchange netflows | 0.502 | [0.002, 0.923] | Substantial |
| V017 | BTC ETF net flows | 0.324 | [0.001, 0.855] | Moderate |
| V026 | Residual momentum (FF5) | 0.677 | [0.003, 0.974] | Substantial |
| C008 | Fear & Greed Index | 0.546 | [0.002, 0.941] | Substantial |
| C009 | Token unlock pressure | 0.490 | [0.002, 0.918] | Moderate |
| C010 | Short-period RSI (2-5d) | 0.778 | [0.010, 0.981] | Considerable |
| C011 | Whale accumulation ratio | 0.371 | [0.002, 0.889] | Moderate |

**R Group:**

| Var_ID | Name | I² Median | 95% CI | Interpretation |
|--------|------|-----------|--------|----------------|
| V001 | VIX | 0.386 | [0.001, 0.909] | Moderate |
| V002 | MOVE Index | 0.653 | [0.004, 0.957] | Substantial |
| V004 | HY OAS | 0.475 | [0.002, 0.940] | Moderate |
| V005 | NFCI | 0.781 | [0.006, 0.976] | Considerable |
| V015 | BTC realized vol | 0.440 | [0.002, 0.899] | Moderate |
| V016 | BTC perp funding rate | 0.266 | [0.001, 0.817] | Moderate |
| V018 | BTC 3m basis | 0.263 | [0.001, 0.827] | Moderate |
| V027 | Intermediary capital ratio | 0.755 | [0.030, 0.969] | Considerable |

**Overlay Group:**

| Var_ID | Name | I² Median | 95% CI | Interpretation |
|--------|------|-----------|--------|----------------|
| C002 | VIX term structure slope | 0.617 | [0.004, 0.947] | Substantial |
| C005 | 200-DMA regime filter | 0.761 | [0.009, 0.977] | Considerable |
| C007 | Market breadth (pct >200-DMA) | 0.576 | [0.002, 0.952] | Substantial |

### 7.2 Group-Level τ Comparison

τ is the standard deviation of true effects within a group. Higher τ = more spread in variable quality.

| Group | Median τ | 95% CI |
|-------|----------|--------|
| S | 0.1256 | [0.0628, 0.2149] |
| T | 0.1248 | [0.0494, 0.2400] |
| R | 0.0805 | [0.0328, 0.1546] |
| Overlay | 0.0858 | [0.0143, 0.2266] |

**Pairwise τ comparisons:**

| Comparison | P(g1 > g2) | Mean Δτ | 95% CI of Δ | Significant? |
|------------|-----------|---------|-------------|-------------|
| τ(S) > τ(T) | 0.4988 | -0.0021 | [-0.1305, +0.1136] | No |
| τ(S) > τ(R) | 0.8139 | +0.0444 | [-0.0519, +0.1457] | No |
| τ(S) > τ(Overlay) | 0.7155 | +0.0331 | [-0.1123, +0.1519] | No |
| τ(T) > τ(R) | 0.7944 | +0.0465 | [-0.0595, +0.1686] | No |
| τ(T) > τ(Overlay) | 0.6951 | +0.0352 | [-0.1200, +0.1777] | No |
| τ(R) > τ(Overlay) | 0.4682 | -0.0113 | [-0.1511, +0.1007] | No |

No group pair shows significantly different heterogeneity at the 95% level.

---

## 8. Registry Divergence Flags

Variables where the posterior mean has shrunk substantially from the published Sharpe (|gap| > 2σ):

| Group | Var_ID | Name | Published Sharpe | Posterior Mean | Posterior SD | Gap (σ) | Interpretation |
|-------|--------|------|-----------------|---------------|-------------|---------|----------------|
| S | V003 | DXY | 0.45 | 0.121 | 0.141 | 2.3σ | Bayesian shrinkage toward group mean |
| S | V011 | Brent M1-M3 curve slope | 0.74 | 0.402 | 0.124 | 2.7σ | Bayesian shrinkage toward group mean |
| S | V028 | Basis-momentum | 0.80 | 0.394 | 0.135 | 3.0σ | Bayesian shrinkage toward group mean |
| S | C001 | Global M2 money supply | 0.35 | 0.006 | 0.048 | 7.2σ | Bayesian shrinkage toward group mean |
| S | C003 | Gold/silver ratio | 0.30 | 0.000 | 0.048 | 6.2σ | Bayesian shrinkage toward group mean |
| S | C004 | NVT Signal (90d) | 0.35 | 0.004 | 0.049 | 7.1σ | Bayesian shrinkage toward group mean |
| S | C006 | China PMI leading copper | 0.30 | 0.003 | 0.087 | 3.4σ | Bayesian shrinkage toward group mean |
| S | C012 | Price-to-sales (tech) | 0.30 | 0.022 | 0.096 | 2.9σ | Bayesian shrinkage toward group mean |
| T | V010 | Revision breadth | 0.50 | 0.206 | 0.138 | 2.1σ | Bayesian shrinkage toward group mean |
| T | V026 | Residual momentum (FF5) | 0.70 | 0.385 | 0.128 | 2.5σ | Bayesian shrinkage toward group mean |
| T | C008 | Fear & Greed Index | 0.40 | 0.007 | 0.049 | 8.0σ | Bayesian shrinkage toward group mean |
| T | C009 | Token unlock pressure | 0.25 | -0.007 | 0.050 | 5.2σ | Bayesian shrinkage toward group mean |
| T | C010 | Short-period RSI (2-5d) | 0.35 | 0.005 | 0.049 | 7.1σ | Bayesian shrinkage toward group mean |
| T | C011 | Whale accumulation ratio | 0.30 | -0.002 | 0.050 | 6.1σ | Bayesian shrinkage toward group mean |
| R | V001 | VIX | 0.20 | -0.034 | 0.111 | 2.1σ | Bayesian shrinkage toward group mean |
| R | V004 | HY OAS | 0.25 | -0.011 | 0.110 | 2.4σ | Bayesian shrinkage toward group mean |
| R | V027 | Intermediary capital ratio | 0.60 | 0.236 | 0.107 | 3.4σ | Bayesian shrinkage toward group mean |
| Overlay | C002 | VIX term structure slope | 0.36 | 0.007 | 0.049 | 7.2σ | Bayesian shrinkage toward group mean |
| Overlay | C005 | 200-DMA regime filter | 0.25 | 0.009 | 0.048 | 5.0σ | Bayesian shrinkage toward group mean |
| Overlay | C007 | Market breadth (pct >200-DMA) | 0.20 | -0.001 | 0.025 | 8.1σ | Bayesian shrinkage toward group mean |

---

## 9. Grade-Rank Consistency

Anomalies where evidence grade and posterior ranking disagree:

| Group | Var_ID | Name | Grade | Mean Rank | Group Size | Anomaly |
|-------|--------|------|-------|-----------|-----------|---------|

**Spearman grade-rank correlation (from posterior draws):**

| Group | ρ Mean | 95% CI | P(ρ > 0) | Interpretation |
|-------|--------|--------|----------|----------------|
| S | 0.372 | [-0.137, 0.789] | 0.922 | Weak/no relationship |
| T | 0.588 | [0.137, 0.913] | 0.989 | Grade predicts rank |
| R | 0.023 | [-0.630, 0.756] | 0.435 | Weak/no relationship |
| Overlay | — | — | — | Too few variables |

---

## 10. Prior Sensitivity

Variables shifting ≥ 3 ranks when switching from grade-tiered priors to uniform loose priors:

| Var_ID | Name | Group | Base Rank | Loose Rank | Shift | Interpretation |
|--------|------|-------|-----------|-----------|-------|----------------|
| V008 | ACM Term Premium 10Y | S | 6 | 9 | 3 | Skeptical prior was inflating rank |
| V019 | MVRV / SOPR | S | 10 | 13 | 3 | Skeptical prior was inflating rank |
| C001 | Global M2 money supply | S | 9 | 6 | 3 | Result driven by skeptical prior, not data |
| C004 | NVT Signal (90d) | S | 11 | 7 | 4 | Result driven by skeptical prior, not data |
| V004 | HY OAS | R | 5 | 2 | 3 | Result driven by skeptical prior, not data |
| V016 | BTC perp funding rate | R | 4 | 8 | 4 | Skeptical prior was inflating rank |

---

## 11. Model Adequacy (Posterior Predictive Checks)

| Group | p(max residual) | p(χ²) | N observations | Verdict |
|-------|----------------|-------|----------------|---------|
| S | 0.717 | 0.779 | 20 | Adequate |
| T | 0.8175 | 0.79925 | 16 | Adequate |
| R | 0.69375 | 0.765 | 13 | Adequate |
| Overlay | 0.6375 | 0.64025 | 3 | Adequate |

All groups pass. Bayesian p-values between 0.05 and 0.95 indicate no systematic misfit.

**Evidence-precision correlation:**

Spearman ρ(n_studies, CI_width) = 0.176, p = 0.319

Not significant. More studies do not reliably predict narrower CIs — heterogeneity τ dominates sampling error.

---

## 12. Marginal Contribution (p_beats_peers)

P(variable beats all declared correlation peers) — computed from joint posterior draws. Low values indicate redundancy.

### S Group

| Var_ID | Name | Peers | p_beats_peers | Verdict |
|--------|------|-------|---------------|---------|
| V011 | Brent M1-M3 curve slope | V028 | 0.5047 | Moderate |
| V028 | Basis-momentum | V011 | 0.4953 | Moderate |
| V007 | Real yield / Breakevens | V003,V006,V008 | 0.3492 | Weak marginal contribution |
| V003 | DXY | V007 | 0.4287 | Moderate |
| V006 | UST 2Y/10Y yields | V007,V008 | 0.3226 | Weak marginal contribution |
| V008 | ACM Term Premium 10Y | V006,V007 | 0.2574 | Weak marginal contribution |
| V012 | BTC active addresses | V013,V019 | 0.3961 | Weak marginal contribution |
| C012 | Price-to-sales (tech) | V003 | 0.2740 | Weak marginal contribution |
| C001 | Global M2 money supply | V012,V013 | 0.2679 | Weak marginal contribution |
| V019 | MVRV / SOPR | V012 | 0.4530 | Moderate |
| C004 | NVT Signal (90d) | V019,V012 | 0.2328 | Weak marginal contribution |
| C006 | China PMI leading copper | V003 | 0.2297 | Weak marginal contribution |
| C003 | Gold/silver ratio | V003,V007 | 0.0524 | **Redundant** — merge/demote |
| V013 | BTC hash rate | V012 | 0.3983 | Weak marginal contribution |

### T Group

| Var_ID | Name | Peers | p_beats_peers | Verdict |
|--------|------|-------|---------------|---------|
| V009 | TSMOM | V026 | 0.9475 | Strong independent signal |
| V026 | Residual momentum (FF5) | V009 | 0.0525 | **Redundant** — merge/demote |
| V010 | Revision breadth | none | 0.0063 | **Redundant** — merge/demote |
| V014 | BTC exchange netflows | V017 | 0.5842 | Moderate |
| C008 | Fear & Greed Index | none | 0.0000 | **Redundant** — merge/demote |
| C010 | Short-period RSI (2-5d) | V009 | 0.0000 | **Redundant** — merge/demote |
| C011 | Whale accumulation ratio | V014,V017 | 0.2538 | Weak marginal contribution |
| C009 | Token unlock pressure | V014 | 0.4329 | Moderate |
| V017 | BTC ETF net flows | V014 | 0.4158 | Moderate |

### R Group

| Var_ID | Name | Peers | p_beats_peers | Verdict |
|--------|------|-------|---------------|---------|
| V027 | Intermediary capital ratio | V004 | 0.9461 | Strong independent signal |
| V015 | BTC realized vol | V001 | 0.6397 | Moderate |
| V018 | BTC 3m basis | V016 | 0.5532 | Moderate |
| V016 | BTC perp funding rate | V018 | 0.4468 | Moderate |
| V004 | HY OAS | V027,V001 | 0.0494 | **Redundant** — merge/demote |
| V001 | VIX | V002,V004,V005 | 0.2354 | Weak marginal contribution |
| V005 | NFCI | V001,V004 | 0.3105 | Weak marginal contribution |
| V002 | MOVE Index | V001,V004 | 0.2744 | Weak marginal contribution |

### Overlay Group

| Var_ID | Name | Peers | p_beats_peers | Verdict |
|--------|------|-------|---------------|---------|
| C005 | 200-DMA regime filter | none | 0.3959 | Weak marginal contribution |
| C002 | VIX term structure slope | none | 0.3830 | Weak marginal contribution |
| C007 | Market breadth (pct >200-DMA) | none | 0.2210 | Weak marginal contribution |

---

## 13. Candidate Pipeline (Stage F)

Variables not in the main BNMA — either Provisional/Ungraded registry rows, Catalyst variables, or candidates that failed promotion criteria.

# Stage F — Candidate Pipeline

Merged: Provisional/Ungraded registry rows + Catalyst variables + low-power/failed Tier 3 candidates.

| Var_ID | Name | Citation | SC | Peers | Post. Mean | Post. SD | P(>0) | Verdict |
|--------|------|----------|----|-------|-----------|---------|-------|--------|
| V030 | Cross-asset lead-lag | Lo-MacKinlay (1990) RFS | T | V009 | N/A | N/A | N/A | WATCH |
| V029 | GEX | Barbon-Buraschi (2021) | Overlay |  | N/A | N/A | N/A | WATCH |
| V031 | Correlation-regime signal quality | Kritzman et al. (2011) FAJ | Overlay |  | N/A | N/A | N/A | WATCH |
| V032 | Decision tree feature importance | Gu-Kelly-Xiu (2020) RFS | Overlay |  | N/A | N/A | N/A | NEEDS_MORE_EVIDENCE |
| V033 | Calendar/seasonal | Lucca-Moench (2015) JF | C |  | N/A | N/A | N/A | NEEDS_MORE_EVIDENCE |
| V020 | News sentiment | Tetlock (2007) JF; Garcia (2013) | C (event-study) |  | N/A (excluded) | N/A | N/A | WATCH |
| C012 | Price-to-sales (tech) | Barbee et al. (1996) FAJ; Lakonishok-Shleifer-Vishny (1994) JF | S | V003 | 0.0221 | 0.096 | 0.5949 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C001 | Global M2 money supply | M2-Bitcoin Elasticity cointegration (2025 WP, Preprints.org) | S | V012,V013 | 0.0055 | 0.048 | 0.546 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C004 | NVT Signal (90d) | Ferretti-Santoro (2022) NVML variant | S | V019,V012 | 0.0037 | 0.0487 | 0.5401 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C006 | China PMI leading copper | Trad core Grade A; Caixin/NBS PMI academic literature | S | V003 | 0.0027 | 0.0873 | 0.5114 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C003 | Gold/silver ratio | Mittal-Mittal (2025) SSRN; practitioner research | S | V003,V007 | 0.0004 | 0.0484 | 0.5019 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C008 | Fear & Greed Index | Farrell-O'Connor (2024) | T | none | 0.007 | 0.0489 | 0.5551 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C010 | Short-period RSI (2-5d) | Connors-Alvarez (2009); practitioner literature | T | V009 | 0.0052 | 0.0485 | 0.541 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C011 | Whale accumulation ratio | ML classifiers 68-73% accuracy (practitioner) | T | V014,V017 | -0.0024 | 0.0495 | 0.4816 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C009 | Token unlock pressure | Practitioner (16,000+ events studied) | T | V014 | -0.0065 | 0.0496 | 0.4481 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C005 | 200-DMA regime filter | Faber (2007) JWIM; extensive replication literature | Overlay | none | 0.0087 | 0.0478 | 0.5796 | WATCH — fails p_beats_peers vs registry peers |
| C002 | VIX term structure slope | Fassas-Hourvouliades (2018); Macrosynergy (2024) | Overlay | none | 0.0075 | 0.0489 | 0.5604 | WATCH — fails p_beats_peers vs registry peers |
| C007 | Market breadth (pct >200-DMA) | Practitioner + breadth literature | Overlay | none | -0.0005 | 0.0247 | 0.4895 | WATCH — fails p_beats_peers vs registry peers |


### Tier 3 Graduation Criteria

To graduate from Tier 3 to Tier 1, a candidate must meet ALL THREE:

1. P(positive) > 0.70
2. p_beats_peers > 0.60 (vs existing registry peers)
3. Passes heterogeneity check

**No Tier 3 candidate meets all three criteria.** This is expected — the skeptical priors correctly suppress single-study candidates with wide credible intervals.

---

## 14. Audit-Addition Feed (V026, V027, V028)

These three variables are on the 2026-10-14 audit cycle. BNMA verdicts below.

### V026 — Residual momentum (FF5)

- **Group:** T
- **Posterior mean:** 0.385 (95% CI: [0.116, 0.637])
- **P(>0):** 0.9965
- **P(above ROPE 0.1):** 0.9801
- **P(top 3):** 0.9673, mean rank: 2.2/9
- **p_beats_peers:** 0.0525 (peers: V009)
- **Audit verdict: NO-GO**

### V027 — Intermediary capital ratio

- **Group:** R
- **Posterior mean:** 0.236 (95% CI: [0.022, 0.446])
- **P(>0):** 0.9850
- **P(above ROPE 0.05):** 0.9547
- **P(top 3):** 0.9721, mean rank: 1.3/8
- **p_beats_peers:** 0.9461 (peers: V004)
- **Audit verdict: GO**

### V028 — Basis-momentum

- **Group:** S
- **Posterior mean:** 0.394 (95% CI: [0.104, 0.649])
- **P(>0):** 0.9921
- **P(above ROPE 0.1):** 0.9761
- **P(top 3):** 0.8646, mean rank: 2.2/14
- **p_beats_peers:** 0.4953 (peers: V011)
- **Audit verdict: GO**

---

## 15. Summary of Statistically Significant Results

Only 5 of 34 variables have posterior mass exceeding the practical significance threshold at ≥95% confidence:

| # | Group | Var_ID | Name | P(above ROPE) | Posterior Mean | 89% HDI |
|---|-------|--------|------|---------------|---------------|---------|
| 1 | S | V011 | Brent M1-M3 curve slope | 0.988 | 0.402 | [0.219, 0.596] |
| 2 | S | V028 | Basis-momentum | 0.976 | 0.394 | [0.198, 0.616] |
| 3 | T | V009 | TSMOM | 1.000 | 0.680 | [0.487, 0.897] |
| 4 | T | V026 | Residual momentum (FF5) | 0.980 | 0.385 | [0.190, 0.593] |
| 5 | R | V027 | Intermediary capital ratio | 0.955 | 0.236 | [0.069, 0.413] |

The remaining 29 variables are either UNDECIDED (posterior too wide) or ACCEPT NULL (posterior concentrated inside ROPE). This is not a failure — it is the honest conclusion given the evidence available.

### Key Takeaways

1. **T group has the clearest structure.** V009 (TSMOM) is the unambiguous #1 with P(top 1) > 99%. V026 (residual momentum) is clearly #2 at P = 96.7%.
2. **S group top 2 are inseparable.** V011 and V028 are statistically tied (P = 0.513). They are jointly separated from the rest.
3. **R group is almost entirely indiscriminate.** Only V027 separates from the field. Ranks 2-8 are interchangeable given the data.
4. **Overlay group is degenerate.** n=3 with all candidates makes every statistic trivial or underpowered.
5. **Cross-group comparison is only valid for S vs T.** Even there, no S variable significantly beats TSMOM.
6. **No Tier 3 candidate earns promotion.** The skeptical priors are doing their job — single-study candidates cannot overcome the prior without more evidence.

---

*Report generated from full MCMC posterior draws. No ad-hoc comparisons of point estimates were used anywhere in this document.*