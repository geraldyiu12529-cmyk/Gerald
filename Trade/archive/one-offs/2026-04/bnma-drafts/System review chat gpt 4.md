RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = STOCKS_ONLY_CROSS_SECTIONAL; MIN_CANDIDATES = 5-7; MANDATES = VALUE + QUALITY + DEFENSIVE_BAB + MODERN_PARADIGM_ML_NLP_ALTDATA; PARADIGM_MIN = 3_OF_5; TARGET_GAP_MIN = 4_OF_8.

# Cross-Sectional Single-Name Equity Signal Candidates
## Structured Systematic Review with Replication Audit

## 1) Executive Summary

This targeted screen supports a **6-candidate** short-list for the single-name equity sleeve. The strongest first-wave registrations are **Timely Value / HML-Devil**, **Gross Profitability (GP/A)**, and **Betting Against Beta (BAB)** because they directly close the highest-priority empty rows in the stock cross-section, have strong or at least clear independent replication support, and are implementable with standard CRSP/Compustat-style infrastructure. **Composite Equity Issuance** and **Sloan Accruals** are credible second-wave adds that expand the framework into issuance and earnings-quality mispricing, while **GKX-style ML expected-return ranking** fills the required modern-paradigm slot but should be treated as a higher-cost research build rather than an immediate production signal.

Under a strict replication screen, I do **not** elevate a pure options-chain signal, insider/Form-4 signal, or proprietary stock-loan signal into the first deployment cohort; those remain candidates for dedicated sub-reviews. Expected time to paper-trade is **4–12 weeks** for the top 3 classical signals and **3–12 months** for the ML sleeve.

**Important caveat:** the “Executability Check” below is **characteristic-level**, not a live constituent list. I did not run a live point-in-time CRSP/Compustat universe pull in this session, so “today’s close” is expressed as the **expected top/bottom portfolio profile**, not named stocks.

---

## 2) Search Log

### Search design
Targeted review, not a full bibliometric export. I screened the **27 user-specified seeds** plus **6 replication / benchmark papers** centered on Hou-Xue-Zhang, Chen-Zimmermann, McLean-Pontiff, and Jensen-Kelly-Pedersen. Inclusion standard was deliberately strict: cross-sectional equity ranking, mechanism-grounded, deployable, and not clearly failing replication screens.

Hou-Xue-Zhang show that most published anomalies do **not** survive modern replication filters, while Chen-Zimmermann’s open-source exercise is materially more favorable for well-known characteristics. McLean-Pontiff documents broad post-publication decay.

### PRISMA-style flow
- Records identified in structured screen: **33**
- Seed studies screened at abstract / summary level: **27**
- Full-text or detailed extracts reviewed: **22**
- Excluded after full-text screen: **16**
- Included in ranked short-list: **6**
- Explicitly left as `NO_QUALIFYING_CANDIDATE` gap-level outcomes: **3 gaps** (strict option-implied, insider/institutional, macro-linked)

### Seed Disposition Table

| Seed | Disposition | Reason |
|---|---|---|
| Fama-French 5-factor (2015) | EXCLUDED | Asset-pricing framework, not a single deployable stock-ranking signal. |
| Hou-Xue-Zhang Q-factor (2015) | EXCLUDED | Same issue: model, not a standalone production signal. |
| Novy-Marx GP/A (2013) | INCLUDED | Strong quality/profitability candidate with good replication support. |
| QMJ (2019) | PARTIAL | Credible, but too composite for first deployment; overlaps GP/A + accrual/safety content. |
| BAB (2014) | INCLUDED | Best defensive-family candidate. |
| HML Devil / timely value (2013) | INCLUDED | Best value-family candidate. |
| Piotroski F-score (2000) | EXCLUDED | Useful conditional value overlay, but less parsimonious than HML-Devil + GP/A. |
| Sloan accruals (1996) | INCLUDED | Quality / earnings-quality slot with durable academic footprint. |
| MAX (2011) | EXCLUDED | Interesting lottery-demand proxy, but not the cleanest first-wave signal under strict replication discipline. |
| Ang et al. IVOL (2006) | EXCLUDED | Subsequent literature is mixed; not robust enough for first-wave registration. |
| Conrad-Dittmar-Ghysels RNSkew (2013) | EXCLUDED | Higher infra burden, thinner independent replication in this screen. |
| Cremers-Weinbaum put-call parity (2010) | EXCLUDED | Same: options data burden and thinner replication path here. |
| Gu-Kelly-Xiu (2020) | INCLUDED | Best modern ML benchmark. |
| Kelly-Pruitt-Su IPCA (2019) | PARTIAL | Strong framework, but less turnkey as a production ranking sleeve. |
| Chen-Pelger-Zhu deep learning (2023) | EXCLUDED | Promising, but replication / production standard not yet as clear as GKX in this screen. |
| Loughran-McDonald (2011) | PARTIAL | Valuable NLP foundation; not selected as the strongest first production signal. |
| Tetlock (2007) | EXCLUDED | Primarily market/news-sentiment framing, not the cleanest stock-ranking sleeve here. |
| Cohen-Malloy-Nguyen Lazy Prices (2020) | EXCLUDED | Interesting text signal, but replication support located here was thinner than desired. |
| Froot-Kang-Ozik-Sadka alt-data sales (2017) | EXCLUDED | Vendor dependence too high for first-wave inclusion. |
| Katona et al. satellite (2021 WP) | EXCLUDED | Same; proprietary alt-data and thinner independent replication. |
| Boehme-Danielsen-Sorescu (2006) | EXCLUDED | Short-sale-constraint family plus data friction. |
| Cohen-Diether-Malloy (2007) | EXCLUDED | Proprietary stock-loan data burden. |
| Daniel-Titman issuance (2006) | INCLUDED | Best issuance-family candidate. |
| Ikenberry-Lakonishok-Vermaelen buyback (1995) | EXCLUDED | Event-driven, not as clean a standing rank signal as CEI. |
| Cohen-Malloy-Pomorski insider trades (2012) | EXCLUDED | Attractive, but replication support located here was not strong enough for first-wave registration. |
| Boons et al. inflation-beta (2020) | EXCLUDED | Later-priority macro-linked gap; not stronger than core empty rows. |
| Bolton-Kacperczyk climate-beta (2021) | EXCLUDED | Same; newer and more unsettled for first production use. |

---

## 3) Ranked Candidate Table

### CAND-01 — Timely Value / HML-Devil

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Timely Book-to-Market / HML-Devil |
| Primary citation | Asness & Frazzini (2013), *The Devil in HML’s Details*, *Journal of Portfolio Management*. |
| Replication citations | Hou, Xue & Zhang (2020) replicate the related `Bmj` value signal at **0.46%/month**, **t=2.12** under NYSE breakpoints and value-weighting. Chen & Zimmermann broadly reproduce the classical cross-sectional literature at high rates. |
| Universe | Russell 1000 or CRSP common stocks, excluding financials if desired for implementation consistency. |
| Portfolio construction | Monthly rebalance; rank on timely B/M using latest available book value and current price; **LONG_TOP_DECILE / SHORT_BOTTOM_DECILE**, value-weighted or rank-weighted. Original factor uses size × value sorts and value weights. |
| Target gap filled | **Gap 1 — Value-family** |
| Mechanism | Standard HML uses stale prices; timely price updates produce a cleaner value proxy and reduce unintended momentum contamination. |
| Signal construction | Book equity with conservative reporting lag; divide by **current** price rather than stale fiscal-year-end price; sort cross-sectionally each month or each June refresh with monthly reweighting. |
| Data requirements | PIT fundamentals + monthly prices; CRSP/Compustat or equivalent. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED |
| Effect size (in-sample) | More timely monthly HML adds **305 bps/year** of statistically significant alpha versus the stale implementation; annual-current adds **143 bps/year**. |
| Effect size (OOS) | HXZ replication: **0.46%/month**, **t=2.12**. |
| Sharpe decay | **NO_CLEAN_APPLES-TO-APPLES_ESTIMATE** located; replication magnitude is lower but still significant. |
| Real-time implementability | **HIGH** with PIT accounting lag control. |
| Executability check | On **Russell 1000 at today’s close**, expect **LONG_TOP_DECILE** to skew toward cheaper, more mature balance-sheet-heavy industrial, financial, energy, and select old-tech names; **SHORT_BOTTOM_DECILE** toward expensive long-duration software / consumer-growth franchises with low B/M. |
| Correlation with V026 | **NOT_REPORTED**; but the original paper shows standard HML carries meaningful momentum contamination, which the timely version reduces. |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | No published \|ρ\|>0.5 pair located in this screen. |
| Capacity / crowding | High capacity, but value crowding and long drawdowns are real. |
| Recommended Grade | **A** |
| Recommended group | **T** |
| Methodology paradigm | Classical-risk-premium |
| Confidence | **HIGH** |
| Why it fills a gap | The current framework has **no value row at all** on single names. This is the cleanest, most production-ready value candidate. |
| Risk of adoption | Value can suffer multi-year relative drawdowns; PIT data discipline is non-negotiable. |
| Infrastructure cost | **MEDIUM** |
| Deployability timeline | **IMMEDIATE / NEAR** |

### CAND-02 — Gross Profitability (GP/A)

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Gross Profits-to-Assets |
| Primary citation | Novy-Marx (2013), *The Other Side of Value: The Gross Profitability Premium*, *JFE*. |
| Replication citations | HXZ replicate `Gpa` at **0.37%/month**, **t=2.63** under NYSE-VW sorts; Chen-Zimmermann broadly support reproducibility for major characteristics. |
| Universe | Russell 1000 / Russell 3000 / CRSP common stocks. |
| Portfolio construction | Annual June rebalance on GP/A; hold monthly; **LONG_TOP_DECILE / SHORT_BOTTOM_DECILE**, usually value-weighted. |
| Target gap filled | **Gap 2 — Quality-family / Profitability** |
| Mechanism | Gross profitability is a persistent quality/profitability signal that is distinct from simple valuation and captures durable operating efficiency. |
| Signal construction | **GP/A = (Revenue − COGS) / Total Assets**; rank cross-sectionally after accounting lag; decile sort. |
| Data requirements | PIT income statement + balance sheet; Compustat-level feed. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED |
| Effect size (in-sample) | Most profitable minus least profitable firms earn **0.31%/month**, **t=2.49**; FF3 alpha **0.52%/month**, **t=4.49**. |
| Effect size (OOS) | HXZ replication: **0.37%/month**, **t=2.63**. |
| Sharpe decay | Roughly moderate, but the original and replicated estimates are not perfectly apples-to-apples. |
| Real-time implementability | **HIGH** with four- to six-month accounting lag discipline. |
| Executability check | On **Russell 1000 at today’s close**, expect **LONG_TOP_DECILE** to hold high-margin, asset-efficient franchises and disciplined industrial/healthcare names; **SHORT_BOTTOM_DECILE** to skew toward weak-margin, capital-hungry or deteriorating operators. |
| Correlation with V026 | NOT_REPORTED |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | Likely conceptual overlap with Sloan/QMJ family, but no published \|ρ\| threshold breach located here. |
| Capacity / crowding | Large smart-beta footprint; still implementable with large-cap focus. |
| Recommended Grade | **A** |
| Recommended group | **T** |
| Methodology paradigm | Classical-risk-premium |
| Confidence | **HIGH** |
| Why it fills a gap | The current single-name framework has **no profitability / quality row**. GP/A is one of the cleanest ways to close it. |
| Risk of adoption | Can underperform in speculative junk rallies; accounting lag must be enforced. |
| Infrastructure cost | **MEDIUM** |
| Deployability timeline | **IMMEDIATE / NEAR** |

### CAND-03 — Betting Against Beta (BAB)

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Betting Against Beta |
| Primary citation | Frazzini & Pedersen (2014), *Betting Against Beta*, *JFE*. |
| Replication citations | Chen-Zimmermann reproduce BAB in a simpler open-source decile implementation; the original paper also documents strong international evidence. |
| Universe | CRSP common stocks / Russell 1000. |
| Portfolio construction | Rank on trailing beta; go long low-beta sleeve and short high-beta sleeve, scaled toward beta neutrality. Monthly rebalance. |
| Target gap filled | **Gap 3 — Defensive / BAB / Low-vol** |
| Mechanism | Leverage and benchmarking constraints can cause investors to overpay for high-beta stocks, leaving low-beta stocks with superior risk-adjusted returns. |
| Signal construction | Estimate trailing market beta; sort low-to-high; long low-beta, short high-beta; rescale sleeves to comparable beta exposure. |
| Data requirements | Price history and market index only. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + NONE_STANDARD_DATA |
| Effect size (in-sample) | U.S. BAB excess return **0.70%/month**, **t=7.12**; 4-factor alpha **0.55%/month**, **t=5.59**; annualized Sharpe **0.78**. |
| Effect size (OOS) | **NO_CLEAN_POST-PUBLICATION_DECAY_ESTIMATE_LOCATED** in this screen; open-source reproduction exists. |
| Sharpe decay | Not cleanly estimable from sources retrieved here. |
| Real-time implementability | **HIGH** |
| Executability check | On **Russell 1000 at today’s close**, expect **LONG_TOP_DECILE** to skew toward utilities, staples, low-beta healthcare, and stable mega-cap defensives; **SHORT_BOTTOM_DECILE** toward high-beta cyclicals, speculative tech, smaller energy/materials, and crowded risk-on names. |
| Correlation with V026 | NOT_REPORTED |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | Usually orthogonal enough to value and profitability to justify inclusion; no screened pair crossed the requested threshold in published evidence located here. |
| Capacity / crowding | Very crowded in smart-beta form; use large-cap and turnover control. |
| Recommended Grade | **B** |
| Recommended group | **T** |
| Methodology paradigm | Classical-risk-premium |
| Confidence | **HIGH** |
| Why it fills a gap | The framework currently has **no defensive row at all** for single names. BAB is the canonical repair. |
| Risk of adoption | Crowding and occasional sharp reversals when junk/high-beta rips. |
| Infrastructure cost | **LOW** |
| Deployability timeline | **IMMEDIATE** |

### CAND-04 — Composite Equity Issuance (CEI)

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Composite Equity Issuance |
| Primary citation | Daniel & Titman (2006), *Market Reactions to Tangible and Intangible Information*, *JF*. |
| Replication citations | HXZ replication: `Cei` high-minus-low average return **−0.57%/month**, **t=3.32**; `Nsi` is even stronger at **−0.64%/month**, **t=4.47**. |
| Universe | CRSP common stocks / Russell 3000. |
| Portfolio construction | Annual June rebalance; **LONG_BOTTOM_DECILE** issuance / net repurchasers, **SHORT_TOP_DECILE** issuers. |
| Target gap filled | **Gap 6 — Issuance / buyback / net equity issuance** |
| Mechanism | Firms tend to issue more equity when expected returns are low or when shares are expensive; repurchase-heavy firms go the other way. |
| Signal construction | **CEI = log(ME_t / ME_{t-5}) − r(t−5,t)**; sort annually in June. HXZ define it as growth in market equity not attributable to stock return. |
| Data requirements | Market cap history, shares, returns; CRSP plus basic fundamentals helpful. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED |
| Effect size (in-sample) | Original paper reports the CEI coefficient remains highly significant in Fama-MacBeth tests, with **t-stat 3.5–5** even after SEO/repurchase controls. |
| Effect size (OOS) | HXZ replication: **−0.57%/month**, **t=3.32**. |
| Sharpe decay | **NO_CLEAN_APPLES-TO-APPLES_ESTIMATE** located, but replication remains strong. |
| Real-time implementability | **HIGH** |
| Executability check | On **Russell 1000 at today’s close**, expect **LONG_BOTTOM_DECILE** to skew toward buyback-heavy, mature, cash-generative firms with shrinking share count; **SHORT_TOP_DECILE** toward serial equity issuers, stock-funded acquirers, and names with aggressive SBC / capital-raising behavior. |
| Correlation with V026 | NOT_REPORTED |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | Conceptual overlap with value, but distinct enough to merit a separate slot. |
| Capacity / crowding | Reasonable capacity in large caps; less crowded than the big style ETFs. |
| Recommended Grade | **B** |
| Recommended group | **T** |
| Methodology paradigm | Behavioral-positioning |
| Confidence | **MEDIUM-HIGH** |
| Why it fills a gap | Issuance / buyback is a fully empty cell in the current matrix. CEI is the cleanest broad version. |
| Risk of adoption | Can look like value and can lag in speculative issuance booms. |
| Infrastructure cost | **MEDIUM** |
| Deployability timeline | **NEAR** |

### CAND-05 — Sloan Accruals

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Operating / Total Accruals |
| Primary citation | Sloan (1996), *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?*, *Accounting Review*. |
| Replication citations | HXZ replication: operating accruals `Oa` **−0.27%/month**, **t=−2.13** with q-factor alpha **−0.54%/month**, **t=−3.77**. |
| Universe | CRSP/Compustat common stocks. |
| Portfolio construction | Annual decile sort; **LONG_LOWEST_ACCRUAL_DECILE / SHORT_HIGHEST_ACCRUAL_DECILE**. |
| Target gap filled | **Gap 2 — Quality-family / earnings quality** |
| Mechanism | Markets overweight reported earnings and underweight the lower persistence of the accrual component relative to cash-flow earnings. |
| Signal construction | Total accruals = change in non-cash current assets minus change in current liabilities ex short-term debt and taxes, minus depreciation, all scaled by average assets. |
| Data requirements | PIT accounting statements. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED |
| Effect size (in-sample) | Year-1 hedge return from long lowest-accrual decile vs short highest-accrual decile: **10.4%**, **t=4.71**; year-2 **4.8%**, **t=3.15**. |
| Effect size (OOS) | HXZ replication: **−0.27%/month**, **t=−2.13**; q-factor alpha **−0.54%/month**, **t=−3.77**. |
| Sharpe decay | Material, but still survives. |
| Real-time implementability | **MEDIUM-HIGH** |
| Executability check | On **Russell 1000 at today’s close**, expect **LONG_LOWEST_ACCRUAL_DECILE** to hold cash-backed, cleaner earnings names; **SHORT_HIGHEST_ACCRUAL_DECILE** to hold firms with more aggressive working-capital or accounting accrual build. |
| Correlation with V026 | NOT_REPORTED |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | Highest conceptual overlap is with GP/A and other quality composites, but not enough evidence here to drop it. |
| Capacity / crowding | Reasonable; more implementation-sensitive in smaller names. |
| Recommended Grade | **B** |
| Recommended group | **T** |
| Methodology paradigm | Classical-risk-premium |
| Confidence | **MEDIUM-HIGH** |
| Why it fills a gap | The quality row is empty; GP/A closes profitability, and Sloan closes earnings-quality specifically. |
| Risk of adoption | Strong dependence on clean PIT accounting treatment; more fragile in microcaps. |
| Infrastructure cost | **MEDIUM** |
| Deployability timeline | **NEAR** |

### CAND-06 — GKX-style ML Expected-Return Ranking

| Field | Assessment |
|---|---|
| Signal type | CROSS_SECTIONAL |
| Factor name | Machine-Learned Expected Return Score (GKX benchmark) |
| Primary citation | Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning*, *RFS*. |
| Replication citations | Drobetz & Otto (2021) European replication: `nn_1` OOS \(R^2\) **1.23%**; decile **H-L = 3.26%/month**, annualized Sharpe **3.89**; long-only top-decile Sharpe **1.41**. |
| Universe | Russell 1000 / MSCI World Large Cap / CRSP common stocks with broad feature panel. |
| Portfolio construction | Monthly retraining and monthly rebalance; sort on predicted excess return; **LONG_TOP_DECILE / SHORT_BOTTOM_DECILE** or long-only top decile. |
| Target gap filled | **Gap 4 — Modern paradigm (ML / high-dimensional)** |
| Mechanism | Nonlinear interactions and state dependence among standard characteristics can improve expected-return ranking beyond linear factor models. |
| Signal construction | Train penalized / tree / neural model on broad characteristic panel; score each stock at month-end; rank by predicted excess return. |
| Data requirements | Large PIT characteristic panel, prices, fundamentals, and model pipeline. |
| Infrastructure required | SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED |
| Effect size (in-sample) | **NO_STANDARD_IN-SAMPLE_SORT_REPORTED** in the retrieved evidence; the original paper is explicitly OOS-focused. |
| Effect size (OOS) | Original paper: long-short decile spread for `NN4` annualized Sharpe **2.45** in equal-weight form; one OOS machine-learning portfolio earns **2.3%/month** with annualized Sharpe **1.35**. European replication: `nn_1` decile **H-L 3.26%/month**, Sharpe **3.89**; long-only top decile Sharpe **1.41**. |
| Sharpe decay | Not cleanly decomposable from sources retrieved here. |
| Real-time implementability | **MEDIUM-LOW** |
| Executability check | On **Russell 1000 at today’s close**, the long and short sleeves would be model-driven blends rather than a single style bucket; expect longs to over-weight multi-signal winners and shorts to concentrate in stocks that look simultaneously expensive, weak-quality, aggressive-investment, and poor short-horizon expected-return names. |
| Correlation with V026 | NOT_REPORTED |
| Correlation with V010 | NOT_REPORTED |
| Correlation with shortlist | By construction it will absorb information from many characteristics; treat as a separate research sleeve, not a direct substitute for the transparent top-3. |
| Capacity / crowding | Capacity depends on universe and turnover control; crowding hard to observe ex ante. |
| Recommended Grade | **B** |
| Recommended group | **T** |
| Methodology paradigm | ML-or-Altdata |
| Confidence | **MEDIUM** |
| Why it fills a gap | The current framework has **no ML / high-dimensional stock-ranking row at all**. This is the best-documented benchmark. |
| Risk of adoption | Higher model risk, lower interpretability, greater implementation fragility. |
| Infrastructure cost | **HIGH** |
| Deployability timeline | **MEDIUM** |

---

## 4) Gap Coverage Matrix

| Target gap | HML Devil | GP/A | BAB | CEI | Sloan | GKX | Status |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1. Value | ✓ |  |  |  |  |  | Covered |
| 2. Quality |  | ✓ |  |  | ✓ |  | Covered |
| 3. Defensive / BAB |  |  | ✓ |  |  |  | Covered |
| 4. Modern ML / NLP / Alt-data |  |  |  |  |  | ✓ | Covered |
| 5. Option-implied cross-section |  |  |  |  |  |  | **NO_QUALIFYING_CANDIDATE** |
| 6. Short-interest / loan / issuance |  |  |  | ✓ |  |  | Covered |
| 7. Insider / institutional holdings |  |  |  |  |  |  | **NO_QUALIFYING_CANDIDATE** |
| 8. Macro-linked cross-section |  |  |  |  |  |  | **NO_QUALIFYING_CANDIDATE** |

---

## 5) Paradigm Diversification Check

Represented paradigms:
- **Classical-risk-premium:** HML Devil, GP/A, BAB, Sloan
- **Behavioral-positioning:** CEI
- **ML-or-Altdata:** GKX

Result: **3 paradigms represented**, so the diversification requirement is met.

---

## 6) Mandatory-slot Check

- **Value:** HML Devil ✅
- **Quality:** GP/A and Sloan ✅
- **Defensive / BAB:** BAB ✅
- **Modern-paradigm:** GKX ✅

Result: **All mandatory slots filled.**

---

## 7) Correlation / Orthogonality Analysis

Published pairwise correlations against **V026 residual momentum** and **V010 earnings-revision breadth** were generally **not reported** in the sources retrieved here. The one meaningful orthogonality result located is structural rather than numeric: standard stale HML carries material momentum contamination, and the timely-value construction is explicitly designed to reduce that contamination.

Within the short-list, no published \|ρ\| > 0.5 pair was located in this screen. The main conceptual overlap risks are:
- **HML Devil ↔ CEI** (both can load on mispricing / cheapness)
- **GP/A ↔ Sloan** (both sit in quality / earnings quality)

That argues for **sequential** rather than simultaneous adoption: top-3 first, then add CEI and Sloan only if they show incremental paper-trade value.

---

## 8) Replication-Audit Summary

- **HML Devil:** original evidence is strong; HXZ replicate the related timely value variable at **0.46%/month**, **t=2.12**. Survives stricter anomaly screening better than many later zoo variables.
- **GP/A:** one of the better-quality survivors. Original FF3 alpha **0.52%/month**; HXZ replication **0.37%/month**, **t=2.63**.
- **BAB:** original evidence is very strong across U.S. and international samples; open-source reproduction exists, but a clean post-publication decay estimate was not located in this pass.
- **CEI:** original paper gives strong cross-sectional coefficient evidence; HXZ replication remains economically large at **−0.57%/month**.
- **Sloan accruals:** classic anomaly with noticeable decay but still survives replication at reduced magnitude.
- **GKX:** modern benchmark rather than “factor survivor” in the old-anomaly sense; original paper is OOS-focused, and external European replication is favorable.

For the broad benchmark, McLean-Pontiff report that post-publication returns across published predictors are much lower on average, which is why transparent, core signals rank ahead of more fragile esoteric ones.

---

## 9) Infrastructure & Data Summary

| Candidate | Core data | PIT caveat | Cost |
|---|---|---|---|
| HML Devil | CRSP + Compustat | Must lag book data appropriately | MEDIUM |
| GP/A | Compustat fundamentals + prices | Four- to six-month accounting lag | MEDIUM |
| BAB | Price history only | Beta estimation window choice matters | LOW |
| CEI | Shares, market cap, returns | Share-count cleanliness matters | MEDIUM |
| Sloan | Detailed accounting items | PIT accounting lag essential | MEDIUM |
| GKX | Broad characteristic panel + model infra | Highest implementation risk | HIGH |

---

## 10) Registration Recommendations

1. **V029 — Timely Value / HML-Devil**  
   Grade: **A**  
   Group: **T**  
   Paper-trade universe: **Russell 1000**  
   Rebalance: **monthly**  
   OOS tracking: **12 months minimum**

2. **V030 — Gross Profitability (GP/A)**  
   Grade: **A**  
   Group: **T**  
   Paper-trade universe: **Russell 1000**  
   Rebalance: **monthly, with annual characteristic refresh**  
   OOS tracking: **12 months minimum**

3. **V031 — BAB**  
   Grade: **B**  
   Group: **T**  
   Paper-trade universe: **Russell 1000**  
   Rebalance: **monthly**  
   OOS tracking: **12 months minimum**

---

## 11) Gaps Still Unfilled

- **Gap 5 — Option-implied cross-section:** `NO_QUALIFYING_CANDIDATE`
- **Gap 7 — Insider / institutional holdings:** `NO_QUALIFYING_CANDIDATE`
- **Gap 8 — Macro-linked cross-section:** `NO_QUALIFYING_CANDIDATE`

Those are not “bad research areas.” They just did not clear the current screen strongly enough relative to the top-priority empty rows.

---

## 12) Suggested Next Steps

Start with a **transparent top-3 pilot**: **V029 HML-Devil**, **V030 GP/A**, **V031 BAB** on **Russell 1000**, monthly rebalanced, value-weighted and rank-weighted variants, 12-month paper-trade ledger. After that, add **CEI** and **Sloan** only if they demonstrate incremental value net of overlap.

Run **GKX** as a **separate research build**, not as a substitute for the transparent sleeve. In parallel, schedule two dedicated follow-on reviews: one for **strict options-chain cross-sectional signals** and one for **insider / holdings signals**, because those remain the most obvious uncovered stock-specific gaps.

---

## References

- Asness, C., & Frazzini, A. (2013). *The Devil in HML’s Details*. *Journal of Portfolio Management*.
- Frazzini, A., & Pedersen, L. H. (2014). *Betting Against Beta*. *Journal of Financial Economics*.
- Novy-Marx, R. (2013). *The Other Side of Value: The Gross Profitability Premium*. *Journal of Financial Economics*.
- Sloan, R. G. (1996). *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?* *Accounting Review*.
- Daniel, K., & Titman, S. (2006). *Market Reactions to Tangible and Intangible Information*. *Journal of Finance*.
- Gu, S., Kelly, B., & Xiu, D. (2020). *Empirical Asset Pricing via Machine Learning*. *Review of Financial Studies*.
- Hou, K., Xue, C., & Zhang, L. (2020). *Replicating Anomalies*. *Review of Financial Studies*.
- Chen, A. Y., & Zimmermann, T. (2022). *Open Source Cross-Sectional Asset Pricing*. *Critical Finance Review*.
- McLean, R. D., & Pontiff, J. (2016). *Does Academic Research Destroy Stock Return Predictability?* *Journal of Finance*.
- Jensen, T. I., Kelly, B., & Pedersen, L. H. (2023). *Is There a Replication Crisis in Finance?* *Journal of Finance*.
- Drobetz, W., & Otto, M. (2021). *Empirical Asset Pricing via Machine Learning: Evidence from the European Stock Market*. *Journal of Asset Management*.
