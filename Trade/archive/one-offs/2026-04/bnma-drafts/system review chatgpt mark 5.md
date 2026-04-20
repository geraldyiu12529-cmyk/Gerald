RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = INDEX_ONLY; MIN_CANDIDATES = 5-7; MANDATES = US_BROAD_EQUITY + GOLD + EQUITY_INDEX_VRP + NON_GOLD_COMMODITY + NON_US_OR_CROSS_ASSET; PARADIGM_MIN = 4_OF_5.

**Implementation note.** “Today’s close” is interpreted as the latest completed market close, **Friday, April 17, 2026**.

# 1. Executive Summary

The strongest additions are **commodity hedging pressure / futures-market-interest for WTI**, **equity-index correlation risk premium / implied-correlation state**, and a **real-time macro-nowcast/surprise overlay for duration**. WTI hedging pressure ranks first because the mechanism is old, intuitive, and repeatedly replicated, and the current tape is directionally aligned: managed-money crude longs remained large into April while oil then fell sharply as Hormuz reopening headlines removed war-premium support. Correlation-risk / implied-correlation comes second because newer option-implied work shows materially better out-of-sample properties than plain SPX VRP, and the current COR3M reading is unusually low, arguing for **flat-to-underweight U.S. equity beta rather than aggressive long exposure**. The macro-nowcast/surprise composite ranks third because it fills a true zero-coverage paradigm gap and currently points to **short duration** rather than long Treasuries. The weakest mandatory slot is **gold**: a public-data, gold-specific, independently replicated timing signal that fully clears the screen is still scarce, so the retained gold candidate enters only as a **low-grade, cautious positioning indicator**, not a core driver.

Primary sources used included journal articles, working papers, official data pages, and current market/state pages, including:
- Basu & Miffre (2013): https://www.sciencedirect.com/science/article/abs/pii/S0378426613001283
- Goyal, Welch & Zafirov (2024) replication audit: https://academic.oup.com/rfs/article/37/11/3490/7749383

# 2. Search Log

I screened the **19 seed families** specified plus supplemental searches around replication, post-publication performance, public-data feasibility, and current live readings. Primary source types used were journal abstracts/pages, NBER/working-paper abstracts, a large post-2021 replication audit for equity-premium predictors, official data pages from CBOE/FRED/Philadelphia Fed/CFTC-linked series, and current market prints for the executable checks. In this pass, roughly **36 identifiable records** were screened at title/abstract level, **24** were examined in fuller detail, **8** survived mechanism + deployability review, and **6** made the final ranked list. The biggest attrition drivers were: failure on recent replication, hidden dependence on cross-sectional single-name construction, or public-data implementation weakness.

## Seed Disposition Table

| Seed | Status | Disposition reason |
|---|---|---|
| Bollerslev-Tauchen-Zhou (2009) VRP | **INCLUDED** | Mandatory VRP slot; strong original in-sample evidence, but retained with downgraded confidence because the 2024 broad replication audit found weak extended-sample and poor investment performance. |
| Bekaert-Hoerova (2014) VRP decomposition | **INCLUDED** | Included as the refinement / decomposition support for the VRP candidate, but also downgraded because the same 2024 audit judged the updated VP measure weak in homologous OOS use. |
| Martin (2017) SVIX | **EXCLUDED** | The large 2024 replication audit reports negative OOSCT \(R^2\), poor investment performance, and explicitly dismisses it as a useful predictor. |
| Gârleanu-Pedersen-Poteshman (2009) demand-based option pricing | **EXCLUDED** | Mechanism is credible, but it does not yield a clean public-data daily signal on standard futures/ETF rails without richer option-demand / dealer-position data than most non-institutional stacks have. |
| Kelly-Jiang (2014) tail risk | **EXCLUDED** | The predictor is built from a **cross-sectional** stock-tail statistic, which is outside scope even though it was studied for aggregate-return prediction. |
| Driessen-Maenhout-Vilkov (2009) correlation risk | **INCLUDED** | Core building block for the correlation-risk / implied-correlation candidate. |
| Hong-Yogo (2012) futures market interest | **INCLUDED** | Included in the commodity candidate; public-data feasible and mechanism-grounded. |
| Basu-Miffre (2013) hedging pressure | **INCLUDED** | Included in the commodity candidate; direct, replicated, and implementation-ready. |
| Erb-Harvey (2013) commodity framework | **PARTIAL** | Useful synthesis, but not a distinct, stand-alone daily/monthly signal with independent replication strong enough to rank as a separate candidate. |
| Neely-Rapach-Tu-Zhou (2014) ERP combination | **PARTIAL** | Informative for combination forecasting, but too close to existing trend/technical machinery (especially V009) to add as a separate registry variable. |
| Bańbura-Modugno (2014) mixed-frequency DFM | **PARTIAL** | Kept as methodology support for the macro-nowcast candidate, not as a stand-alone trading variable. |
| Aruoba-Diebold-Scotti (2009) ADS | **INCLUDED** | Included as a component of the macro-nowcast candidate. |
| Scotti (2016) surprise / uncertainty indexes | **INCLUDED** | Included as a component of the macro-nowcast candidate. |
| Kolanovic public dealer-gamma notes | **EXCLUDED** | Public sell-side notes are not enough under the inclusion rule; not peer-reviewed and not independently replicated in a stable, transparent public construction. |
| Barbon-Buraschi (2021) gamma fragility | **EXCLUDED** | Interesting, but still a lightly cited working-paper line and more intraday-fragility than durable end-of-day deployable signal under the criteria. |
| Tuzun / Ivanov-Lenkey / Bogousslavsky end-of-day pressure | **EXCLUDED** | The literature supports flow pressure effects, but not yet a clean, robust, public-data close-to-close index-timing signal that beats the bar for registry addition. |
| Koijen-Moskowitz-Pedersen-Vrugt (2018) Carry | **EXCLUDED** | Explicitly excluded because it was flagged as already on the radar and the request was for **variants only**. |
| Baker-Bloom-Davis (2016) EPU | **INCLUDED** | Included, but only as a **risk-budget scalar / gate**, not a standalone high-conviction directional predictor. |
| Barro (2006) rare-disaster risk | **EXCLUDED** | Mechanism is relevant for gold, but public real-time deployment is too indirect for a near-term, named-instrument close-of-day rule. |

# 3. Ranked Candidate Table

## CAND-01 — Commodity hedging pressure / futures-market-interest (WTI)

| Field | Value |
|---|---|
| Signal type | **DIRECTIONAL_TIMING** |
| Factor name | WTI hedging pressure / speculative-hedger imbalance |
| Primary citation | Basu & Miffre (2013), “Capturing the Risk Premium of Commodity Futures: The Role of Hedging Pressure,” *Journal of Banking & Finance* 37(7):2652–2664. DOI 10.1016/j.jbankfin.2013.02.031. |
| Replication citations | Hong & Yogo (2012) on open interest as return-relevant; later commodity studies continue to use hedging-pressure/open-interest channels. |
| Asset coverage | **Non-gold commodity** — WTI / Brent via CL or USO |
| Target gap filled | Gap 6 |
| Mechanism | Commercial hedgers pay risk-transfer premia to speculators; when hedgers are very short and speculators very long, expected returns embed compensation for warehousing commodity risk. |
| Signal construction | Rank the contract on hedging pressure using CFTC disaggregated positions; bullish when producer/commercial short pressure dominates and speculative longs are not yet crowded; bearish when spec longing is already heavy and the macro catalyst rolls over. Use weekly CFTC data with position-extreme thresholds and trade the nearest liquid future / ETF. |
| Data requirements | CFTC CoT; weekly; public. Instrument execution via CL futures or USO. Current price proxy: USO 116.04 on Apr. 17, 2026. |
| Infrastructure required | **FUTURES_ETF_ONLY / NONE_STANDARD_DATA** |
| Effect size (in-sample) | Basu-Miffre report fully collateralized hedging-pressure long–short portfolios with Sharpe ratios **0.27 to 0.93**, average **0.51** over 1992–2011. |
| Effect size (OOS) | **NO_CLEAN_PUBLIC_POST-PUBLICATION_SHARPE_EXTRACTED_IN_THIS_PASS**; replication channel remains directionally supportive but not with a single standardized OOS Sharpe. |
| Sharpe decay | **NOT_QUANTIFIED_CLEANLY** |
| Real-time implementability | **HIGH** |
| Executability check | Managed-money WTI positions were still large on Apr. 14, 2026 (long **200,130**, short **101,762**) while WTI then plunged and Brent fell 10.5% / WTI 11.1% on Apr. 17 after Hormuz reopening headlines. **If deployed at Apr. 17 close on USO/CL: SHORT.** |
| Correlation with V009 TSMOM | Basu-Miffre explicitly state hedging-pressure predictability differs from momentum and term-structure effects. |
| Correlation with shortlist | Likely modest overlap with gold positioning; no published \|ρ\| extracted. |
| Recommended Grade | **B** |
| Recommended group | **S** |
| Methodology paradigm | **Classical-risk-premium** |
| Confidence | **HIGH** |
| Why it fills a gap | The registry has Brent slope and commodity basis-momentum, but **not** a direct hedger/speculator pressure signal. This fills the empty “commodity term-structure beyond basis-momentum” and “behavioral/futures positioning” hole with public data. |
| Risk of adoption | Weekly cadence, crowding reversals, and geopolitical jump risk can dominate the slow-moving CoT signal. |
| Deployability timeline | **IMMEDIATE** |

## CAND-02 — Equity-index correlation risk premium / implied-correlation state (SPY)

| Field | Value |
|---|---|
| Signal type | **REGIME_GATE / DIRECTIONAL_TIMING** |
| Factor name | SPX correlation risk premium / implied correlation |
| Primary citation | Driessen, Maenhout & Vilkov (2009), “The Price of Correlation Risk: Evidence from Equity Options,” *Journal of Finance* 64(3). |
| Replication citations | Buss et al. (2018) report quarterly OOS \(R^2\) up to **10%** and annual OOS \(R^2\) up to **8%**; Hollstein et al. (2019) find CRP predicts returns in- and out-of-sample and timing utility gains **>4.63% per annum**. |
| Asset coverage | U.S. broad equity index — SPY / ES |
| Target gap filled | Gaps 2 and 3 |
| Mechanism | When option markets price high dependence across constituents, investors require a larger premium for systematic crash/comovement risk. |
| Signal construction | Estimate implied correlation from index-option IV versus single-stock basket IV, or use Cboe COR3M as a live proxy. Signal is bullish only when implied correlation / CRP is sufficiently high relative to realized or relative to its own history; low correlation implies thin compensation for market beta. |
| Data requirements | COR3M / SPX and single-name option data; daily; Cboe / options vendor. SPY closed at 710.14 proxy. |
| Infrastructure required | **OPTIONS_CHAIN** |
| Effect size (in-sample) | In Driessen et al., average implied correlation for S&P 500 was **39.46%** versus realized **32.59%**, a premium of >**21%** over realized; Pollet-Wilson report positive predictive relation of average correlation for future market returns. |
| Effect size (OOS) | Buss et al.: OOS \(R^2\) up to **10% quarterly** and **8% annual**; Hollstein et al.: CRP timing strategy utility gains **>4.63%/yr**. |
| Sharpe decay | **ACCEPTABLE_RELATIVE_TO_PEERS**, though no single standardized decay figure extracted. |
| Real-time implementability | **MEDIUM-HIGH** |
| Executability check | Cboe/Investing show COR3M at **14.80** on Apr. 17, 2026, far below Reuters’ cited five-year median of about **35**. That is a **low-compensation** state, not a high-premium buy state. **If deployed at Apr. 17 close on SPY: FLAT.** |
| Correlation with V009 TSMOM | **NOT_REPORTED**; mechanism is crash-comovement pricing, not trend. |
| Correlation with shortlist | Possible overlap with VRP; no published pairwise \|ρ\| extracted here. |
| Recommended Grade | **B** |
| Recommended group | **R** |
| Methodology paradigm | **Option-implied** |
| Confidence | **MEDIUM-HIGH** |
| Why it fills a gap | This directly fills the zero-coverage **option-implied premium** row and is a better orthogonal add than another plain volatility-level variable. |
| Risk of adoption | Requires cleaner options infrastructure than futures-only signals; levels can remain low for extended bull phases. |
| Deployability timeline | **NEAR** |

## CAND-03 — Macro-nowcast / surprise composite for duration (TLT)

| Field | Value |
|---|---|
| Signal type | **OVERLAY_COMBO / DIRECTIONAL_TIMING** |
| Factor name | ADS–Scotti real-time macro-nowcast and surprise overlay |
| Primary citation | Aruoba, Diebold & Scotti (2009) ADS index; Scotti (2016) “Surprise and Uncertainty Indexes,” *Journal of Monetary Economics* 82:1–19; Bańbura & Modugno (2014) for mixed-frequency factor-model estimation. |
| Replication citations | Neely et al. (2014) and later ERP-combination work support macro-plus-combination forecasting; Scotti shows the surprise index preserves asset-price-relevant macro-surprise information. |
| Asset coverage | **Cross-asset** — U.S. Treasury duration via TLT / ZN |
| Target gap filled | Gap 4 |
| Mechanism | Real-time growth nowcasts and surprise aggregation should move both the discount-rate and growth paths; for duration, stronger-than-expected macro usually hurts long bonds. |
| Signal construction | Compute a daily nowcast state from ADS or equivalent mixed-frequency DFM. Overlay a surprise measure built from standardized macro-release surprises. Trade duration long only when nowcast and surprise composite are sufficiently weak; short when both are positive. |
| Data requirements | ADS/nowcast data; macro consensus surprises; daily/weekly; official/public feeds plus calendar consensus. TLT proxy price 87.07. |
| Infrastructure required | **NONE_STANDARD_DATA** |
| Effect size (in-sample) | **NO_SINGLE_CANONICAL_SHARPE** because this is a factor-definition composite, not one paper’s backtest. Scotti’s contribution is informational sufficiency of the surprise index, not a single trading Sharpe. |
| Effect size (OOS) | **NO_STANDARDIZED_OOS_SHARPE_EXTRACTED** |
| Sharpe decay | **NOT_AVAILABLE** |
| Real-time implementability | **MEDIUM** |
| Executability check | The ADS index page states the latest release used data available on **Apr. 9, 2026**; the April Philly Fed current-activity index then rose to **26.7** from **18.1**, well above consensus. That is a positive growth-surprise state. **If deployed at Apr. 17 close on TLT: SHORT.** |
| Correlation with V009 TSMOM | **NOT_REPORTED**; conceptually orthogonal. |
| Correlation with shortlist | Likely positive overlap with EPU gate only during recession scares; no published \|ρ\| extracted. |
| Recommended Grade | **B-** |
| Recommended group | **Overlay** |
| Methodology paradigm | **Structural-nowcasting** |
| Confidence | **MEDIUM** |
| Why it fills a gap | The matrix has no mixed-frequency DFM / nowcast row at all. This is the cleanest public-data way to fill it. |
| Risk of adoption | Depends on consensus-surprise feeds and revision handling; mapping from macro state to equities and bonds is regime-dependent. |
| Deployability timeline | **NEAR** |

## CAND-04 — News-based policy uncertainty gate (SPY)

| Field | Value |
|---|---|
| Signal type | **SIZING_SCALAR / REGIME_GATE** |
| Factor name | News-based Economic Policy Uncertainty (EPU) gate |
| Primary citation | Baker, Bloom & Davis (2016), “Measuring Economic Policy Uncertainty,” *Quarterly Journal of Economics*. |
| Replication citations | Bekiros, Gupta & Majumdar (2016) report significant nonlinear OOS information for U.S. equity-premium models; Nonejad (2022) finds many newspaper-based uncertainty measures matter but standard EPU is less successful than some EMV-linked variants. |
| Asset coverage | U.S. broad equity index — SPY |
| Target gap filled | Gap 8 / alt-data TradFi |
| Mechanism | Policy uncertainty can raise discount rates and widen required premia, but its predictive content is nonlinear and better used as a conditioning variable than a naked directional rule. |
| Signal construction | Use the news-based EPU index. When EPU is elevated relative to its own trailing range, reduce index-beta risk budget; only restore full size when uncertainty normalizes. |
| Data requirements | Monthly FRED EPU data; public. SPY proxy price 710.14. |
| Infrastructure required | **NONE_STANDARD_DATA** |
| Effect size (in-sample) | **NO_STABLE_SINGLE_NUMBER_EXTRACTED** in this pass. |
| Effect size (OOS) | Qualitatively positive in nonlinear specifications, but Nonejad (2022) says plain EPU is less successful than some alternative news-based measures. |
| Sharpe decay | **LIKELY_MATERIAL** |
| Real-time implementability | **HIGH** |
| Executability check | FRED’s news-based U.S. policy-uncertainty index rose to **382.22** in Mar. 2026 from **374.19** in Feb. 2026. That supports **reduced** beta, not aggressive outright shorting. **If deployed at Apr. 17 close on SPY: SIZE_SCALAR = 0.5.** |
| Correlation with V009 TSMOM | **NOT_REPORTED** |
| Correlation with shortlist | Some overlap with macro-nowcast stress states. |
| Recommended Grade | **C+** |
| Recommended group | **Overlay** |
| Methodology paradigm | **ML-or-Altdata** |
| Confidence | **MEDIUM-LOW** |
| Why it fills a gap | This is the cleanest public **text/news** candidate in a framework that currently has none. |
| Risk of adoption | Publication lags, regime nonlinearities, and weak standalone performance. |
| Deployability timeline | **IMMEDIATE** |

## CAND-05 — SPX variance risk premium (SPY)

| Field | Value |
|---|---|
| Signal type | **REGIME_GATE / SIZING_SCALAR** |
| Factor name | SPX variance risk premium (BTZ/BH construction family) |
| Primary citation | Bollerslev, Tauchen & Zhou (2009), “Expected Stock Returns and Variance Risk Premia,” *Review of Financial Studies* 22(11):4463–4492. |
| Replication citations | Bekaert & Hoerova (2014) refine the measure; Goyal, Welch & Zafirov (2024) provide the key adverse replication audit. |
| Asset coverage | U.S. broad equity index — SPY / ES |
| Target gap filled | Gap 2 |
| Mechanism | Investors pay to hedge future variance; high VRP should proxy high required compensation for bearing market risk. |
| Signal construction | VRP = implied variance minus realized / conditional variance forecast over the same horizon. Go risk-on only when VRP is sufficiently positive; otherwise flat or underweight. |
| Data requirements | SPX options, realized variance estimator, daily/monthly. SPY proxy price 710.14. |
| Infrastructure required | **OPTIONS_CHAIN** |
| Effect size (in-sample) | In BTZ, the simple quarterly regression has coefficient **0.86**, t-stat **3.94**, adjusted \(R^2\) **15.14%** over 1990Q1–2005Q1. |
| Effect size (OOS) | The 2024 replication audit reports OOSCT \(R^2\) **positive but small and not statistically significant**, and investment performance **2.6%/yr to 7.0%/yr worse** than all-equity-all-the-time. |
| Sharpe decay | **SEVERE** |
| Real-time implementability | **MEDIUM-HIGH** |
| Executability check | VIX closed at **17.48** on Apr. 17, 2026; SPY 30-day historical volatility was about **18.64%** on the same date. A simple public proxy therefore gives a flat-to-negative VRP. **If deployed at Apr. 17 close on SPY: FLAT.** |
| Correlation with V009 TSMOM | **NOT_REPORTED** |
| Correlation with shortlist | Overlaps economically with CRP; no robust pairwise \|ρ\| extracted here. |
| Recommended Grade | **C** |
| Recommended group | **R** |
| Methodology paradigm | **Option-implied** |
| Confidence | **MEDIUM-LOW** |
| Why it fills a gap | It is still the canonical public VRP construction, but it now fills the gap only **weakly** because post-publication evidence is disappointing. |
| Risk of adoption | Severe decay risk; can look attractive exactly when it is failing structurally. |
| Deployability timeline | **IMMEDIATE** |

## CAND-06 — Gold speculative-positioning crowd signal (GLD)

| Field | Value |
|---|---|
| Signal type | **REGIME_GATE / DIRECTIONAL_TIMING** |
| Factor name | COMEX gold speculative crowding / managed-money positioning |
| Primary citation | Bosch & Pradkhan (2015), “The Impact of Speculation on Precious Metals Futures Markets,” *Resources Policy* 44:118–134. |
| Replication citations | Coyle, Gogolin & Kearney (2018) show extreme speculation changes model accuracy and that a speculation-informed composite outperforms in gold futures. |
| Asset coverage | **Gold** — GLD / GC |
| Target gap filled | Gap 1 |
| Mechanism | Extreme speculative crowding in gold futures can distort near-term pricing and precede reversals or destabilizing volatility. |
| Signal construction | Use managed-money long and short positions from CoT. Treat extreme net-long states as late-cycle / crowding risk and only buy after crowding normalizes. |
| Data requirements | CFTC CoT; weekly; public. GLD price proxy 445.93. |
| Infrastructure required | **FUTURES_ETF_ONLY / NONE_STANDARD_DATA** |
| Effect size (in-sample) | Bosch/Pradkhan document that speculators’ positions predict returns and volatility in precious metals, but a single standardized trading Sharpe is not extractable from the accessible abstract in this pass. |
| Effect size (OOS) | Coyle et al. report the speculation-informed composite outperforms in gold futures markets, but again without a clean public Sharpe in the accessible abstract. |
| Sharpe decay | **UNKNOWN** |
| Real-time implementability | **HIGH** |
| Executability check | As of Apr. 14, 2026, COMEX gold managed-money positions were **125,422 long** and **30,281 short**; Reuters and other reporting still point to heavy structural demand from central banks, which offsets the crowding bearishness. Net result: crowding says “don’t chase,” macro backdrop says “don’t blindly short.” **If deployed at Apr. 17 close on GLD: FLAT.** |
| Correlation with V009 TSMOM | **NOT_REPORTED** |
| Correlation with shortlist | Likely low with CRP/VRP; some overlap with commodity positioning. |
| Recommended Grade | **C** |
| Recommended group | **S** |
| Methodology paradigm | **Behavioral-positioning** |
| Confidence | **LOW** |
| Why it fills a gap | Gold is the emptiest cell in the framework. This is the only public-data, near-deployable, gold-specific candidate that survived even a partial strict screen. |
| Risk of adoption | Thin replication base; official-sector buying can overpower futures crowding for long stretches. |
| Deployability timeline | **IMMEDIATE** |

# 4. Gap Coverage Matrix

**Interpretation.** Check marks indicate a **direct** fill of one of the seven ranked target gaps. A half-step mention means “adjacent but not clean enough to count as a primary fill.” Under that rule, **CAND-04 (EPU)** does **not** count toward the seven target gaps; it was retained only as a lower-priority methodology-diversifier because it is public, deployable, and text-based.

| Target gap | CAND-01 WTI hedging pressure | CAND-02 SPX correlation risk | CAND-03 ADS/Scotti macro-nowcast | CAND-04 EPU gate | CAND-05 SPX VRP | CAND-06 Gold positioning | Status |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1. Gold-specific directional signals |  |  |  |  |  | ✓ | **Filled weakly** |
| 2. Equity-index VRP |  | ✓ |  |  | ✓ |  | **Filled** |
| 3. Option-implied directional signals on indexes |  | ✓ |  |  | ✓ |  | **Filled** |
| 4. Macro-nowcasting / structural equity-premium predictors |  |  | ✓ |  |  |  | **Filled** |
| 5. Cross-asset carry variants beyond KMPV 2018 |  |  |  |  |  |  | **NO_QUALIFYING_CANDIDATE** |
| 6. Commodity term-structure / hedging-pressure beyond basis-momentum and Brent slope | ✓ |  |  |  |  |  | **Filled** |
| 7. Intermediary / flow signals on TradFi indexes |  |  |  |  |  |  | **NO_QUALIFYING_CANDIDATE** |

**Bottom line.** The shortlist covers **5 of the 7** ranked target gaps. The two unresolved holes are exactly the ones where public, independently replicated, end-of-day deployable constructions remain weakest: **cross-asset carry variants beyond KMPV** and **dealer/CTA/flow-style TradFi index signals**.

# 5. Paradigm Diversification Check

The final six candidates span **five** paradigms, which clears the **minimum 4-of-5** requirement:

- **Classical-risk-premium:** CAND-01
- **Option-implied:** CAND-02, CAND-05
- **Structural-nowcasting:** CAND-03
- **ML-or-Altdata / text-derived:** CAND-04
- **Behavioral-positioning:** CAND-06

That is a meaningful diversification improvement over the current registry, which is heavy in reduced-form price, macro levels, and a small number of derivative levels/slopes, but light in **true premia**, **nowcasting**, and **public text / uncertainty** signals.

# 6. Asset Coverage Check

Mandatory slots are met:

| Mandatory slot | Filled by | Pass? |
|---|---|:---:|
| US broad equity index | CAND-02, CAND-04, CAND-05 on SPY/ES | ✓ |
| Gold | CAND-06 on GLD/GC | ✓ |
| Equity-index VRP | CAND-05 on SPY/ES | ✓ |
| Non-gold commodity | CAND-01 on CL/USO | ✓ |
| Non-US or cross-asset application | CAND-03 on U.S. duration (TLT/ZN) as cross-asset macro-nowcast | ✓ |

The weakest of these passes is still **gold**. The literature supports speculative-positioning relevance for precious metals and specifically gold, but the replication base and directly accessible out-of-sample trading evidence are materially thinner than for WTI hedging pressure or option-implied correlation risk.

# 7. Correlation / Orthogonality Analysis

There is **good qualitative orthogonality** versus the existing registry in three cases.

First, **CAND-01** is the cleanest non-duplicative add. Basu–Miffre’s hedging-pressure effect is not just commodity trend or commodity basis repackaged, and Hong–Yogo show open-interest / futures-market-interest adds predictive content beyond standard predictors. That makes it materially different from both **V028 commodity basis-momentum** and generic **V009 TSMOM**.

Second, **CAND-03** is methodologically distinct from price trend. ADS is a mixed-frequency activity tracker built from claims, payrolls, industrial production, income, sales, and GDP, while Scotti’s surprise index aggregates release surprises in real time. That is conceptually orthogonal to V009 even though published pairwise \(\rho\) versus TSMOM is not reported.

Third, **CAND-02** and **CAND-05** are the pair most likely to be internally overlapping. That is an inference from construction, not a published pairwise correlation in this pass: both are built off SPX option-implied compensation for bearing market risk, whereas CAND-02 isolates **comovement / correlation risk** and CAND-05 isolates **variance risk premium** more broadly. I would therefore avoid promoting both as equal-weight production signals at the same time.

| Pair | Overlap risk | Reason |
|---|---|---|
| CAND-02 vs CAND-05 | **High** | Same SPX-options family; likely related compensation channel |
| CAND-01 vs CAND-06 | Low–Medium | Both use CFTC positioning, but on different commodity complexes |
| CAND-03 vs CAND-04 | Medium | Both are macro-state overlays, but one is activity/surprise, the other uncertainty/news |

No published pairwise \(|\rho|>0.5\) was located in this pass. Where “high” is flagged, that is a **mechanism-based implementation warning**, not an empirical correlation estimate.

# 8. Replication-Audit Summary

## CAND-01 — WTI hedging pressure
This remains the strongest replication profile in the list. Basu–Miffre report commodity hedging-pressure portfolios with Sharpe ratios from **0.27 to 0.93** and average **0.51** over 1992–2011, and Hong–Yogo separately show that commodity-market interest predicts commodity returns beyond other known predictors. A single clean post-publication standardized OOS Sharpe for WTI alone was not extracted in this pass, so the grade remains **B**, not A.

## CAND-02 — SPX correlation risk premium
This is the best **option-implied** addition. Driessen–Maenhout–Vilkov establish priced correlation risk from equity options, and later work reports meaningful out-of-sample forecasting and economic utility. The evidence is good enough for **B**, but not A, because implementation requires better options infrastructure and the public live proxy set is still thinner than for classical futures signals.

## CAND-03 — ADS/Scotti macro-nowcast overlay
This candidate clears the **methodology gap** more than it clears a classic “single-paper factor” replication screen. ADS and Scotti’s surprise index are both well-established, and Bańbura–Modugno gives the right mixed-frequency estimation framework, but the exact trading rule still needs house calibration. That supports **B-** rather than a stronger grade.

## CAND-04 — EPU gate
This one has mixed evidence. Baker–Bloom–Davis clearly establish the measure itself, but later out-of-sample work suggests the plain EPU index is not the strongest newspaper-based uncertainty predictor relative to other variants. That keeps it at **C+** and in “optional overlay / watchlist” territory rather than a core promotion.

## CAND-05 — SPX VRP
This is the biggest downgrade from the original canonical story. BTZ and Bekaert–Hoerova remain the classic sources, but the 2024 broad replication audit explicitly dismisses both the BH-style variance-premium predictor and BTZ VRP as useful modern equity-premium predictors, citing weak homologous in-sample strength, weak or insignificant out-of-sample \(R^2\), and poor investment performance. This caps the grade at **C** despite the importance of the gap it fills.

## CAND-06 — Gold speculative crowding
The gold slot survives only because the framework otherwise has a near-empty gold row. Bosch–Pradkhan show speculative positions predict precious-metals returns and volatility, and Coyle–Gogolin–Kearney argue extreme gold speculation changes which variable families work best. But the replication depth is still too thin for anything above **C**.

# 9. Registration Recommendations

## Promote now

| Proposed ID | Candidate | Grade | Group | Tracking instrument | OOS tracking window | Recommendation |
|---|---|---:|---|---|---|---|
| **V029** | WTI hedging pressure / futures-market-interest | **B** | **S** | CL front / USO | 6 months weekly | **Promote now** |
| **V030** | SPX implied correlation / correlation-risk premium | **B** | **R** | SPY / ES + COR3M | 3 months daily | **Promote now** |
| **V031** | ADS–Scotti macro-nowcast overlay | **B-** | **Overlay** | TLT / ZN | 3 months daily | **Promote now** |

These three are the highest-value additions because they combine decent literature support, real orthogonality, and immediate or near-immediate implementation. CAND-01 also has the cleanest live executable check: WTI positioning was still long-heavy into Apr. 14, 2026, and crude then collapsed on Apr. 17; that is exactly the kind of state where a positioning-risk-premium signal is operationally useful.

## Shadow-book only

| Proposed ID | Candidate | Grade | Group | Tracking instrument | OOS tracking window | Recommendation |
|---|---|---:|---|---|---|---|
| **V032** | Gold speculative crowding | **C** | **S** | GC / GLD | 6 months weekly | **Shadow only** |
| **V033** | SPX variance risk premium | **C** | **R** | SPY / ES | 3 months daily | **Benchmark only** |
| **V034** | EPU sizing gate | **C+** | **Overlay** | SPY | 6 months monthly | **Optional watchlist** |

For **V033**, it should be registered only as a **benchmark / monitor**, not as a production signal. The literature matters historically, but the newer replication evidence is too adverse to justify full promotion.

# 10. Gaps Still Unfilled

## NO_QUALIFYING_CANDIDATE — Gap 5
**Cross-asset carry variants beyond KMPV 2018** remain unfilled. Nothing both (a) clearly distinct from what is already in the framework and (b) strong enough on independent replication and public-data deployability cleared the bar in this pass.

## NO_QUALIFYING_CANDIDATE — Gap 7
**Intermediary / flow signals on TradFi indexes** also remain unfilled. Dealer gamma, gamma-fragility, vol-target flows, and leveraged-ETF rebalance papers are interesting, but no candidate simultaneously met the standards for transparent public-data construction, replication, and end-of-day deployability.

## Gold remains only partially solved
The framework now has a gold-specific placeholder, but not a high-confidence one. A stronger gold addition would probably require a dedicated review of **lease-rate / GOFO-style carry history**, **gold–real-rate state interaction**, and **central-bank / ETF flow** literature, with a stricter focus on signals that are both public and actually tradeable on GC/GLD at a daily or weekly cadence.

# 11. Suggested Next Steps

1. **Enter CAND-01, CAND-02, and CAND-03 into the live OOS ledger within 4 weeks.**  
   These are the only candidates from this pass that should be treated as serious near-term production adds. Current live checks are also coherent: WTI hedging pressure points **SHORT**, COR3M is very low at **14.80** which argues for **FLAT / underweight SPY beta**, and the activity/surprise complex points **SHORT duration** rather than long Treasuries.

2. **Keep gold in shadow mode, not production.**  
   Managed-money gold positioning was still heavily net long into Apr. 14, 2026, while GLD closed strong on Apr. 17. That combination is consistent with a “do not chase” interpretation, but not with a high-confidence outright short.

3. **Do not promote SPX VRP beyond benchmark status yet.**  
   The classical papers are important historically, but the 2024 replication review is too negative to ignore. VRP should remain a monitored comparator, not a lead signal.

4. **Run two dedicated sub-reviews next:**  
   **(a)** gold-specific public-data signals; **(b)** dealer/CTA/flow TradFi index signals. Those are the two structurally important gaps this pass could not close cleanly.

# Reference Links

## Core literature
- Basu & Miffre (2013): https://www.sciencedirect.com/science/article/abs/pii/S0378426613001283
- Hong & Yogo (2012, NBER version): https://www.nber.org/system/files/working_papers/w16712/revisions/w16712.rev0.pdf
- Driessen, Maenhout & Vilkov (2009): https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2009.01467.x
- Aruoba, Diebold & Scotti index page: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/ads
- Scotti (2016): https://www.sciencedirect.com/science/article/abs/pii/S0304393216300320
- Baker, Bloom & Davis (2016): https://academic.oup.com/qje/article-abstract/131/4/1593/2468873
- Bollerslev, Tauchen & Zhou (2009): https://academic.oup.com/rfs/article/22/11/4463/1565787
- Bekaert & Hoerova (2014): https://www.sciencedirect.com/science/article/abs/pii/S0304407614001110
- Bosch & Pradkhan (2015): https://ideas.repec.org/a/eee/jrpoli/v44y2015icp118-134.html
- Coyle, Gogolin & Kearney (2018): https://eprints.whiterose.ac.uk/140400/
- Bańbura & Modugno (2014): https://onlinelibrary.wiley.com/doi/10.1002/jae.2306

## Replication / review
- Goyal, Welch & Zafirov (2024): https://academic.oup.com/rfs/article/37/11/3490/7749383

## Current-state / executability sources used
- Cboe implied-correlation complex: https://www.cboe.com/us/indices/implied/
- Cboe COR3M dashboard: https://www.cboe.com/us/indices/dashboard/cor3m/
- Cboe VIX page: https://www.cboe.com/tradable-products/vix/
- FRED EPU release table: https://fred.stlouisfed.org/release/tables?eid=841710&rid=279
- Barchart CL / USO / GC pages: https://www.barchart.com/
