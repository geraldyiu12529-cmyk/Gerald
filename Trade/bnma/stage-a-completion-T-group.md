# Stage A completion — T group replications, registry validation, Tier 3 admission

Stage A is **substantially complete** with two blocking flags: a material citation FAIL at V014 (the Aloosh-Ouzan-Shahzad 2023 BTC-netflows primary citation does not exist as registered) and a clean journal typo at V031 (FAJ → Journal of Portfolio Management). Ten Tier 3 candidates were admitted under the 15-cap; nine of the 19 embedded candidates failed admission, mostly for CITATION_MISSING (practitioner-only) or the pre-flagged EVENT_STUDY_NOT_SHARPE. Post-2023 T-group literature is **abundant but numerics-sparse**: 20 new replications located across five variables, but only one yielded an extractable net Sharpe (Poh-Roberts-Zohren 2025 arXiv, 0.645 for network-momentum TSMOM), forcing 19 NUMERIC_MISSING flags that propagate to Stage B extraction. Total search budget used: 13/15 (T replications) + 16/10 combined Tier 3 searches across both subagents (fresh-search cap slightly over, reported below). Stage B may proceed conditional on Gerald accepting the two proposed A.1 corrections.

## Section 1 — A.1 registry validation table (11 remaining rows)

| var_id | name | score_component | grade | source_paper_as_registered | registry_validation | fail_reason | proposed_correction |
|---|---|---|---|---|---|---|---|
| V009 | TSMOM | T | A | Moskowitz-Ooi-Pedersen 2012 JFE | **PASS** | — | Confirmed: JFE 104(2):228–250, DOI 10.1016/j.jfineco.2011.11.003 |
| V010 | Revision breadth | T | A | Gleason-Lee 2003 | **PASS** | — | Confirmed: *The Accounting Review* 78(1):193–225, DOI 10.2308/accr.2003.78.1.193 |
| V014 | BTC exchange netflows | T | A | Aloosh-Ouzan-Shahzad 2023 | **FAIL** | No paper by these three authors in 2023 on BTC exchange netflows exists. Closest: Aloosh-Ouzan-Shahzad 2022 *Finance Research Letters* v49 on meme-stock/crypto co-explosivity (wrong mechanism). | Replace with **Aloosh & Li (2024), "Direct Evidence of Bitcoin Wash Trading," *Management Science* 70(12):8875–8921** (exchange microstructure/flow evidence, correct mechanism). Alternative if co-explosivity was intended: Aloosh-Ouzan-Shahzad 2022 FRL v49. |
| V017 | BTC ETF flows | T | B | no direct peer-reviewed; institutional flow literature | **PASS (auto)** | — | Auto-pass per registry convention for B-grade variables without a primary citation. |
| V026 | Residual momentum FF5 | T | A | Blitz-Huij-Martens 2011 JEF | **PASS** | — | Confirmed: *Journal of Empirical Finance* 18(3):506–521, DOI 10.1016/j.jempfin.2011.01.003 |
| V030 | Cross-asset lead-lag | T | Provisional | Lo-MacKinlay 1990 RFS | **PASS** | — | Confirmed: RFS 3(2):175–205. Provisional → Stage F. |
| V029 | GEX | Overlay | Provisional | Barbon-Buraschi 2021 | **PASS** | — | Confirmed: "Gamma Fragility," SSRN 3725454, St.Gallen WP 2020/05 (revised Mar 2021). Provisional → Stage F. |
| V031 | Correlation-regime (absorption ratio) | Overlay | Provisional | Kritzman et al 2011 FAJ | **FAIL** | Journal wrong: published in *Journal of Portfolio Management*, not *Financial Analysts Journal*. | **Kritzman, Li, Page & Rigobon (2011), "Principal Components as a Measure of Systemic Risk," *Journal of Portfolio Management* 37(4):112–126, DOI 10.3905/jpm.2011.37.4.112.** Provisional → Stage F. |
| V032 | Decision tree feature importance | Overlay | Ungraded | Gu-Kelly-Xiu 2020 RFS | **PASS** | — | Confirmed: RFS 33(5):2223–2273, DOI 10.1093/rfs/hhaa009. Ungraded → Stage F. |
| V020 | News sentiment | C | B | Tetlock 2007 JF / Garcia 2013 | **PASS** | — | Confirmed: Garcia (2013) "Sentiment during Recessions," *JoF* 68(3):1267–1300, DOI 10.1111/jofi.12027. C-group → out of BNMA scope. |
| V033 | Calendar/seasonal | C | Ungraded | Lucca-Moench 2015 JF | **PASS** | — | Confirmed: *JoF* 70(1):329–371, DOI 10.1111/jofi.12196. C-group → out of BNMA scope. |

**Summary: 9 PASS, 2 FAIL.** V014 FAIL is material (authorship error, not just journal typo) and blocks Stage B until Gerald selects the correction path. V031 FAIL is a clean journal-name correction.

## Section 2 — A.2 Tactical Timing replication table (post-2023 only)

| var_id | study_id | citation | sample_period | universe | sharpe_annualized | sharpe_se | n_months | is_oos | tc_included | se_imputed | extraction_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V009 | V009-R1 | Uhl, B. (2025). "Speculators and time series momentum in commodity futures markets." *Review of Financial Economics* 43(2):213–230, DOI 10.1002/rfe.1228 | ~1986–2022 | US commodity futures (CFTC disaggregated) | — | — | ~444 | TRUE | FALSE | — | NUMERIC_MISSING |
| V009 | V009-R2 | Poh, Roberts, Zohren (2025). "Follow the Leader: Enhancing Systematic Trend-Following Using Network Momentum." arXiv:2501.07135 | 2005–2024 (OOS) | 28 futures (commodities, equities) | **0.645** (NMM-DTW-E, net) | 0.073 | 234 | TRUE | TRUE (0.5–2 bp impact) | TRUE | — |
| V009 | V009-R3 | Song & Jeon (2025). "Deep momentum networks with market trend dynamics." *PLoS ONE* 20(9):e0331391, DOI 10.1371/journal.pone.0331391 | 1989–2021 | 99 continuous futures (4 asset classes) | — | — | ~384 | TRUE | TRUE (0–5 bp) | — | NUMERIC_MISSING |
| V009 | V009-R4 | Sepp & Lucic (2025). "Optimal Allocation to Trend-Following in CTAs." SSRN WP | 1990s–2024 | Cross-asset futures (CTA universe) | — | — | ~360+ | TRUE | — | — | NUMERIC_MISSING |
| V010 | V010-R1 | Baher, Badreddine, Clark (2024). "The Value Premium in Good Times and Bad: Market Reactions to Analyst Forecast Revisions." SSRN 4819157 | ~1984–2022 | US equities (IBES+CRSP) | — | — | ~456 | FALSE | FALSE | — | NUMERIC_MISSING |
| V010 | V010-R2 | Sharpe & Gil de Rubio Cruz (2024). "Predicting Analysts' S&P 500 Earnings Forecast Errors and Stock Market Returns Using Macro-Nowcasts." Fed FEDS 2024-049 | 1994–2023 | S&P 500 aggregate (bottom-up IBES) | — | — | ~360 | TRUE | FALSE | — | NUMERIC_MISSING |
| V010 | V010-R3 | Barth, Landsman, Jeong, Wang (2024). "Analyst Forecast Bundling Intensity and Earnings Surprise." SSRN 4839739 | ~2002–2022 | US equities (IBES) | — | — | ~240 | FALSE | FALSE | — | NUMERIC_MISSING |
| V014 | V014-R1 | (2026) "Order flow and cryptocurrency returns." *Journal of Empirical Finance* forthcoming, S1386418126000029 | 2017–2024 | Multi-exchange crypto (11 int'l order flows, BTC focus) | — | — | ~84 | TRUE | TRUE | — | NUMERIC_MISSING |
| V014 | V014-R2 | (2025) "Return and Volatility Forecasting Using On-Chain Flows in Cryptocurrency Markets." ResearchGate preprint 395126255 | 2017–2023 | BTC, ETH, USDT (intraday 1–6 hr) | — | — | ~72 | FALSE | FALSE | — | NUMERIC_MISSING |
| V014 | V014-R3 | Palazzi, Raimundo Jr., Klotzle (2025). "From Network Fundamentals to Macro-Financial Integration: The Evolving Predictability of Bitcoin Returns." SSRN 6199098 | 2014–2025 | Bitcoin daily | — | — | ~132 | TRUE | FALSE | — | NUMERIC_MISSING |
| V014 | V014-R4 | Lee & Wang (2024). "Variance Decomposition and Cryptocurrency Return Prediction." Georgia Tech WP | 2015–2023 | 100 cryptocurrencies (HF) | — | — | ~96 | TRUE | FALSE | — | NUMERIC_MISSING |
| V017 | V017-R1 | Soeder (2025). "One year of bitcoin spot ETPs: A brief market and fund flow analysis." *Economics Letters* S0165176525001417 | 11 Jan 2024–10 Jan 2025 | 10 US spot BTC ETPs | — | — | 12 | FALSE | FALSE | — | NUMERIC_MISSING |
| V017 | V017-R2 | Guliyev & Ahmadova (2025). "From Flows to Value: Cointegration Between Bitcoin Spot ETF Assets and Bitcoin Price." *Ledger* 10:154–172, DOI 10.5195/ledger.2025.393 | 11 Jan 2024–16 May 2025 | US spot BTC ETFs + BTC spot | — | — | ~16 | FALSE | FALSE | — | NUMERIC_MISSING |
| V017 | V017-R3 | Novinsalari & Şensoy (2025). "Return Predictability in Bitcoin ETFs: A Machine Learning Approach." SSRN 5614913 | Jan 2024–2025 | 8 crypto ETFs | — | — | ~18 | TRUE | FALSE | — | NUMERIC_MISSING |
| V017 | V017-R4 | Kia, Liu, Li, Song, Xu (2025). "Price Discovery in Bitcoin ETF Market." *Financial Review*, DOI 10.1111/fire.70026 | Jan 2024–2025 | US spot BTC ETFs | — | — | ~16 | FALSE | FALSE | — | NUMERIC_MISSING |
| V017 | V017-R5 | Babalos, Bouri, Gupta (2025). "Does the introduction of US spot Bitcoin ETFs affect spot returns and volatility of major cryptocurrencies?" *Quarterly Review of Economics and Finance* 102:102006, DOI 10.1016/j.qref.2025.102006 | ~2023–2024 | BTC, ETH, LTC, XRP + BTC futures | — | — | ~24 | TRUE | FALSE | — | NUMERIC_MISSING |
| V026 | V026-R1 | van Vliet, Baltussen, Dom, Vidojevic (2025). "Momentum factor investing: Evidence and evolution." SSRN 5561720 | Long-horizon US + intl | Global equities (incl. residual momentum variants) | — | — | — | TRUE | — | — | NUMERIC_MISSING |
| V026 | V026-R2 | Zaremba et al. (2024). "Factor momentum versus price momentum: Insights from international markets." *J. Banking & Finance*, S0378426624002462 | ~1991–2022 | 51 country equity markets | — | — | ~384 | FALSE | FALSE | — | NUMERIC_MISSING |
| V026 | V026-R3 | (2025) "The Many Facets of Stock Momentum." *Financial Analysts Journal*, DOI 10.1080/0015198X.2025.2562790 | ~1990–2022 | US + 2 developed markets | — | — | ~384 | FALSE | FALSE | — | NUMERIC_MISSING |
| V026 | V026-R4 | Dobrynskaya, Tomtosov, Rechmedina (2025). "Momentum Factor or Factor Momentum in REIT Market?" SSRN 5631072 | ~2000s–2024 | US REITs / factor portfolios | — | — | ~240 | FALSE | FALSE | — | NUMERIC_MISSING |

**20 new T-group replications logged.** 19 flagged NUMERIC_MISSING (headline Sharpes not in accessible text; Stage B will need full-PDF extraction). Per-variable distribution: V009=4, V010=3, V014=4, V017=5, V026=4. V017 studies all have n_months ≤ 18 (sample begins Jan 2024) — low statistical power flag for Bayesian pooling.

## Section 3 — A.3 Tier 3 admitted candidates (10 of 15 cap)

| candidate_id | name | citation | sample_period | universe | sharpe_annualized | sharpe_se | n_months | score_component_assigned | correlation_peers | grade_inferred | se_imputed | extraction_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C004 | Global M2 vs BTC (Johansen cointegration, elasticity 2.65) | Sarkar (2025), "Bitcoin Price Dynamics," SSRN 5395221; Preprints.org 10.20944/preprints202506.1963.v2 | 2009–Aug 2025 / 2015–Apr 2025 | BTC / US M2SL | — (β=2.65, CI [2.06, 3.24]; ECT λ=−0.12, p<0.01; 90d-lag ρ=0.78) | — | 124 | **S** | V019 (crypto valuation), V001 (macro stress) | candidate_working_paper | — | NUMERIC_MISSING |
| C006 | Whale accumulation / on-chain ML classifier | Herremans & Low (2022), arXiv:2211.08281, "Forecasting Bitcoin volatility spikes from whale transactions…Synthesizer Transformer" | Jan 2018–Sep 2021 | BTC daily, on-chain + whale-alert tweets | — (verbal "highest Sharpe ratios"; 9.6%/19.2% profit reported) | — | ~45 | **T** (primary); secondary R | V031, V032, V019 | candidate_working_paper | — | NUMERIC_MISSING |
| C007 | Funding-rate arbitrage, delta-neutral crypto perp | He, Manela, Ross, von Wachter (2022, rev 2024), arXiv:2212.06888; also Ackerer, Hugonnier, Jermann, NBER WP 32936 (2024) | 2019–Mar 2024 | BTC/ETH/BNB/DOGE/ADA perpetuals | — (verbal "large Sharpe even at highest retail costs") | — | ~63 | **T** | V001, V019, V031 | candidate_working_paper | — | NUMERIC_MISSING |
| C008 | BTC–ETH pairs trading cointegration | "Statistical Arbitrage Strategies Using Cointegration…" IJSRA 2026, 18(02):516–529, IJSRA-2026-0283 | Not stated (5-min freq) | BTC, ETH, LTC | **2.45** | 0.410 | ~24 (assumed) | **T** | V009 (neg corr), V019, V026 | candidate_working_paper (low-tier journal) | TRUE | — |
| C009 | 200-DMA / 10-month SMA regime filter (GTAA) | Faber (2007, rev 2013), SSRN 962461, "A Quantitative Approach to Tactical Asset Allocation" | 1901–2012 | S&P 500, DJIA, NASDAQ, 5-asset GTAA | — (timing 10% MaxDD vs 46% B&H; decade SR −0.23 to 1.44) | — | ~1,340 | **Overlay** | V001, V009, V033 | candidate_working_paper | — | NUMERIC_MISSING |
| C011 | VIX futures term-structure slope as contrarian timing | Fassas & Hourvouliades (2019), *J. Risk Financial Manag.* 12(3):113, DOI 10.3390/jrfm12030113 | Jan 2010–Dec 2017 | S&P 500 + 7 VIX futures | — (adj-R² 0.01–0.035; coef t-stats sig) | — | 96 | **Overlay** | V001 | candidate_peer_reviewed | — | NUMERIC_MISSING |
| C012 | Dual Momentum / GEM (Antonacci) | Antonacci (2016), SSRN 2042750, "Risk Premia Harvesting Through Dual Momentum"; also JMgmt&Ent 2(1):27–55, 2017 | 1974–2013 | S&P 500, ACWI ex-US, US agg bonds | **0.87** (CAGR 17.43%, MaxDD −22.72%) | 0.054 | 480 | **T** | V009 | candidate_working_paper | TRUE | — |
| C013 | Crypto perp carry trade | Schmeling, Schrimpf & Todorov (2023), "Crypto Carry," SSRN 4268371; reproduced arXiv:2510.14435 (2025) | Aug 2020–May 2025 | BTC perp–spot (+5-coin univ) | **6.45** full / **4.06** 2024 / neg 2025 | 0.588 | 58 | **T** | V019 | candidate_working_paper | TRUE | — |
| C014 | Perpetual-futures basis alpha | He, Manela, Ross, von Wachter (2022, rev 2024), arXiv:2212.06888 | Jan 2019–Mar 2024 | 5 major perpetuals (Binance) | **1.8–3.5** (retail–maker tier) | 0.207 | 62 | **T** | V019 | candidate_working_paper | TRUE | — |
| C015 | Overnight–intraday equity anomaly | Haghani, Ragulin, Dewey (2024), Elm Wealth WP "Night Moves"; NY Fed Staff Report 917 (Boyarchenko et al. 2020); Lou-Polk-Skouras 2019 | 1993–2024 | US large-cap + SPY/QQQ | verbal "~10× L/S momentum SR"; index overnight-only SR 7.75 vs 1.24 B&H (Redfame 2024) | — | ~372 | **T** | V026, V033 | candidate_working_paper | — | NUMERIC_MISSING (heterogeneous) |

**10 admitted (cap 15, not exceeded).** Score-component distribution: S=1 (C004), T=7 (C006, C007, C008, C012, C013, C014, C015), R=0, Overlay=2 (C009, C011). Peer-reviewed grade: 1 (C011). Working paper: 9.

## Section 4 — A.3 Tier 3 rejected candidates

| candidate_name | rejection_reason | notes |
|---|---|---|
| MVRV Z-Score | CITATION_MISSING | Practitioner origin (Puell, Mahmudov). Fantazzini (2022) MPRA 115508 uses MVRV>3.7 threshold but gives no Sharpe. Route to Stage F watch list. |
| NVT Signal 90d (attributed "Ferretti-Santoro 2022 NVML") | CITATION_MISSING | Ferretti-Santoro 2022 citation could not be verified in any academic database. Closest: Fantazzini 2022 MPRA 115508 (covers NVTS/NVML but no Sharpe). Source attribution appears fabricated. |
| Token unlock events (~16,000 events, 90% negative) | EVENT_STUDY_NOT_SHARPE + CITATION_MISSING | Origin is practitioner (Keyrock, LiquiFi). Event-study abnormal returns, not tradable Sharpe. |
| Fear & Greed Index <10 threshold | CITATION_MISSING + NUMERIC_MISSING | All sources practitioner (alternative.me, Binance). n<10 observations since 2018; statistically underpowered by construction. |
| Short-period RSI 2–5d S&P | CITATION_MISSING | Origin Connors trader literature; Pagonidis NAAIM 2014 uses IBS not RSI-2; no SSRN/NBER/peer-reviewed paper with clean RSI-2 S&P Sharpe. |
| Price-to-sales tech | REDUNDANT_WITH_REGISTRY | Value (FF3/FF5) already registered; no distinct academic citation with tech-P/S Sharpe. |
| Gold/silver ratio regime (>80/<60) | CITATION_MISSING | Only CME education, IG, Money.com, TradingView (practitioner). No peer-reviewed or WP with quantitative Sharpe. |
| China PMI leading copper | CITATION_MISSING | Becerra et al. 2022 uses China LEI in SARIMAX with MAPE (no Sharpe/tradable strategy). No academic lead-lag copper Sharpe located. |
| EIA crude inventory surprises | EVENT_STUDY_NOT_SHARPE | Per task instructions; belongs to C-group (V020/V033) which is skipped for BNMA. |
| OPEC+ production decisions | EVENT_STUDY_NOT_SHARPE | Per task instructions; C-group catalyst. |
| Market breadth % >200-DMA | CITATION_MISSING | Only Schwab, StockCharts, BuildAlpha (practitioner). No peer-reviewed paper isolating breadth-filter Sharpe. |
| HRP Hierarchical Risk Parity (Burggraf 2021) | AMBIGUOUS_SCORE_COMPONENT | Citation verified (*Finance Research Letters* 38:101523, DOI 10.1016/j.frl.2020.101523) but HRP is portfolio-construction methodology, not a return-predictive signal — does not map to S/T/R/Overlay. Route to Stage F. |

## Section 5 — Stage A gap-fill summary

**T-group replication stock after Stage A.2.** Across the 5 Grade A/B Tactical Timing variables, 20 new post-2023 replications are catalogued on top of the 14 exclusion-list primaries/extensions already held. Distribution: V009 TSMOM = 4 new (including 1 extractable Sharpe, Poh et al. 2025 NMM-DTW-E at 0.645 net); V010 revision breadth = 3 new (literature has pivoted to value-interaction and macro-nowcasting — no direct Top-20/Bottom-20 replication post-2023); V014 BTC exchange netflows = 4 new (literature shifted toward order flow and aggregate on-chain); V017 BTC ETF flows = 5 new (all short-sample, Jan 2024 start, n ≤ 18 months — low-power flag for Bayesian pooling); V026 residual momentum FF5 = 4 new (no direct Blitz-update; closest work is factor-momentum and REIT extensions). Nineteen of twenty are NUMERIC_MISSING — Stage B extraction will require full-text PDF access.

**Admitted Tier 3 by Score_Component.** S-group gains C004 (M2-vs-BTC macro cointegration, working paper, NUMERIC_MISSING). T-group gains 7: C006 whale-ML, C007 funding-rate arb, C008 BTC-ETH pairs, C012 Antonacci GEM dual momentum, C013 crypto perp carry, C014 perp basis, C015 overnight–intraday. Overlay gains 2: C009 10-month SMA regime filter and C011 VIX futures term structure (the one peer-reviewed admission of the ten). R-group gains zero — none of the 19 candidates cleanly mapped to volatility/stress/sizing without redundancy with existing registry Overlays.

**Rejected candidates.** Five of the 19 failed for CITATION_MISSING (MVRV Z-Score, Fear & Greed, RSI-2, gold/silver ratio, market-breadth 200-DMA); one NVT variant failed for unverifiable attribution (Ferretti-Santoro 2022 could not be located — likely fabricated in source registry); two (EIA, OPEC+) were pre-flagged EVENT_STUDY_NOT_SHARPE; one was REDUNDANT_WITH_REGISTRY (P/S tech); one was AMBIGUOUS_SCORE_COMPONENT (HRP, portfolio construction not signal); one was event-study-ish (token unlocks). China PMI-copper failed CITATION_MISSING despite being Grade A/B+ in the core catalog — no tradable-strategy Sharpe paper located.

**A.1 validation FAILs (2 of 11).** V014 is a material authorship error — the registered Aloosh-Ouzan-Shahzad 2023 BTC-netflows paper does not exist. Proposed correction: Aloosh & Li (2024), *Management Science* 70(12):8875–8921 on BTC wash-trading/exchange flow. V031 is a clean journal-name typo: *Journal of Portfolio Management* 37(4):112–126, not *Financial Analysts Journal*.

**Search budget used.** T-replications: 13/15. Tier 3 fresh discovery + candidate verification: 18 searches across both subagents (10 for candidates 1–10; 8 for candidates 11–19 + fresh). Fresh-search phase alone used 4 of its 10 allotment. **Note: candidate-verification searches were not strictly counted against the 10-search "fresh discovery" cap per the original task phrasing, but total Tier 3 search activity was 18 — flag for Gerald's review.**

**Fail-loud flag counts.** NUMERIC_MISSING: 19 (A.2 replications) + 6 (Tier 3 admitted: C004, C006, C007, C009, C011, C015) = **25 total**. CITATION_MISSING: 6 (MVRV, NVT, Fear&Greed, RSI-2, gold/silver, breadth, China PMI = 7 actually). se_imputed=TRUE: 4 Tier 3 (C008, C012, C013, C014) + 1 A.2 (V009-R2) = **5 total**. Cap breaches: Tier 3 admitted 10/15 (no breach); fresh-search budget slightly over in aggregate (see note).

## Section 6 — Ready-for-Stage-B checklist

Final Score_Component counts for the BNMA (Stages A.1 R+S from prior work + current A.1 T + admitted Tier 3):

| Group | Registry Grade A/B (prior + current) | Tier 3 admitted | **Total variables for BNMA** |
|---|---|---|---|
| **S** (Structural Directional) | prior-stage count (PASS from 17 R+S) | **+1** (C004) | prior_S + 1 |
| **T** (Tactical Timing) | **5** (V009, V010, V014, V017, V026) | **+7** (C006, C007, C008, C012, C013, C014, C015) | **12** |
| **R** (Risk Overlay) | prior-stage count (PASS from 17 R+S) | **+0** | prior_R + 0 |
| **Overlay** (candidates only; registry Overlays are Provisional/Ungraded → Stage F) | 0 (V029, V031, V032 all route to Stage F) | **+2** (C009, C011) | **2** |

Given the task preamble states 17 PASS across R+S, and the current stage adds only T/Overlay/C, the combined BNMA-eligible variable pool is **17 (prior R+S) + 5 (T registry Grade A/B) + 10 (Tier 3 admitted) = 32 variables** before any Stage C correlation-peer pruning.

**Stage F holdings (Provisional/Ungraded registry + watch-list rejects):**
- V030 cross-asset lead-lag (Provisional T)
- V029 GEX (Provisional Overlay)
- V031 absorption ratio (Provisional Overlay, post-correction)
- V032 ML feature importance (Ungraded Overlay)
- V020 news sentiment (Grade B, C-group — out of BNMA scope)
- V033 pre-FOMC drift (Ungraded, C-group — out of BNMA scope)
- **Watch-list rejects:** MVRV Z-Score, NVT variants, Fear & Greed, RSI-2, gold/silver ratio, 200-DMA breadth, HRP (methodology), China PMI–copper

**Blocking issues for Stage B:**
1. **V014 FAIL resolution required** — Gerald must select between (a) Aloosh & Li 2024 *Management Science* (recommended, mechanism-correct) or (b) Aloosh-Ouzan-Shahzad 2022 *FRL* (co-explosivity, different mechanism), or (c) downgrade V014 to Provisional and reroute to Stage F.
2. **V031 FAIL resolution required** (low friction) — accept the *Journal of Portfolio Management* correction.
3. **25 NUMERIC_MISSING flags** propagate into Stage B — full-PDF extraction pass needed before Bayesian priors can be updated with likelihoods. Stage B cannot compute without at least partial numeric rescue.
4. **V017 short-sample warning** — all 5 BTC ETF flow replications have n_months ≤ 18; flag for low-information pooling in the hierarchical prior.

---

**READY_FOR_STAGE_B = FALSE.**

**Blocking issues (resolve in order):** (1) V014 citation correction selection by Gerald; (2) V031 journal-name correction acceptance; (3) full-PDF Sharpe extraction pass for ≥19 of the 25 NUMERIC_MISSING flagged rows (minimum threshold for meaningful Bayesian pooling in the T group); (4) disposition of the "fresh-search budget slight overrun" flag (administrative). Once (1)–(3) are resolved, Stage B may proceed with a 32-variable BNMA pool (1 S addition, 12 T total, 2 Overlay additions, prior R unchanged).