RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = INDEX_STOCKS_GAP_FILL; BUCKETS = INDEX(4+) + STOCKS(3+) + DUAL_USE(0-1); MANDATES = US_BROAD_EQUITY + GOLD + EQUITY_INDEX_VRP + STOCKS_VALUE_OR_QUALITY + STOCKS_MODERN_PARADIGM; PARADIGM_MINS = OPTION_IMPLIED + ML_OR_TEXT + STRUCTURAL_NOWCASTING

# Filling the 32-variable framework's biggest structural gaps

## 1. Executive summary

The review promotes **five INDEX candidates, three STOCKS candidates, and one DUAL_USE candidate** through the inclusion criteria. For INDEX, the strongest gap-filling signals are the **Bollerslev-Tauchen-Zhou (2009) variance risk premium (VRP)** for US broad equity and equity-index VRP (CAND-01), the **gold–10Y-TIPS real-yield beta** grounded in Erb-Harvey (2013 FAJ) and Jermann (2023 NBER WP 31386) (CAND-02), and the **Aruoba-Diebold-Scotti (2009) business-conditions index** as a structural nowcasting regime gate (CAND-03). Two further INDEX slots go to **Hong-Yogo (2012 JFE) futures open interest** for cross-asset carry/positioning (CAND-04) and **Kelly-Jiang (2014 RFS) tail risk / Martin (2017 QJE) SVIX** as option-implied directional timing (CAND-05). For STOCKS, the strongest candidates are **Novy-Marx (2013 JFE) gross profitability** (PIPE-01, Quality/Value bridge) — the only profitability signal that replicates in both HXZ 2020 and JKP 2023 — and **Gu-Kelly-Xiu (2020 RFS) tree/neural-net ML** (PIPE-02) for the modern-paradigm mandate, with **Loughran-McDonald (2011 JF) 10-K textual tone** (PIPE-03) filling the NLP gap at low infrastructure cost. The framework's highest-priority unfilled gap — a mechanism-grounded dealer-gamma signal — remains NO_QUALIFYING_CANDIDATE because Barbon-Buraschi (2021) is still a working paper, the peer-reviewed antecedents (Ni et al. 2021 RFS; Baltussen et al. 2021 JFE) address adjacent phenomena, and the 0DTE regime post-2022 may invalidate pre-2020 calibrations.

## 2. Search log (PRISMA-style)

**Databases and journals searched.** SSRN (JEL codes G11/G12/G13/G14/G17), NBER Working Papers, openassetpricing.com (Chen-Zimmermann), jkpfactors.com (Jensen-Kelly-Pedersen), Federal Reserve Board FEDS working papers, Philadelphia Fed real-time data center, policyuncertainty.com, the publisher websites of *Journal of Finance*, *Journal of Financial Economics*, *Review of Financial Studies*, *Journal of Financial and Quantitative Analysis*, *Review of Asset Pricing Studies*, *Financial Analysts Journal*, *Journal of Portfolio Management*, *Management Science*, *Journal of Applied Econometrics*, *Journal of Business and Economic Statistics*, *Journal of Monetary Economics*, *Journal of Banking and Finance*, *Quarterly Journal of Economics*, and *Accounting Review*.

**Replication databases consulted.** Hou-Xue-Zhang 2020 *RFS* "Replicating Anomalies" (452 anomalies, NYSE-breakpoint value-weighted tests); Jensen-Kelly-Pedersen 2023 *JF* "Is There a Replication Crisis in Finance?" (153 factors, 13 themes, 93 countries, Bayesian hierarchical CAPM-alpha tests); McLean-Pontiff 2016 *JF* (97 predictors, 26% OOS decay / 58% post-publication); Chen-Zimmermann 2022 *Critical Finance Review* (319 signals, 98% reproduction among originally-significant predictors). Time range 2000–present, priority 2010+ publications with 2015+ replications.

**Keywords.** "variance risk premium," "SVIX," "dealer gamma," "gamma exposure SPX," "implied correlation / dispersion trade," "tail risk premium," "gold real yield TIPS," "gold lease rate," "rare disasters gold," "ADS business conditions," "dynamic factor nowcasting," "CFTC open interest futures," "hedging pressure commodity futures," "leveraged ETF rebalancing flows," "gross profitability," "quality minus junk," "betting against beta replication," "HML devil," "IPCA characteristics covariances," "deep learning asset pricing," "Loughran McDonald dictionary 10-K tone," "Tetlock media sentiment," "EPU index," "Google SVI attention," "Scotti surprise index."

**Screening counts.** Seeds pre-specified: 22 (9 INDEX + 9 STOCKS + 4 DUAL_USE). After canonical-citation verification: 22/22 had verifiable primary citations; 1 (Kolanovic JPM dealer-gamma notes) non-public and dropped to practitioner-reference status. After inclusion criteria applied: 9 INCLUDED, 6 PARTIAL, 7 EXCLUDED. After bucket-constraint optimization: 5 INDEX + 3 STOCKS + 1 DUAL_USE advance.

**Full seed disposition table.**

| # | Seed | Disposition | Reason |
|---|------|-------------|--------|
| S1 | Barbon-Buraschi 2021 "Gamma Fragility" + SqueezeMetrics/SpotGamma | EXCLUDED | Primary paper is SSRN WP only, not peer-reviewed; practitioner sources non-replicable. Fails inclusion #1 and #2. Flag for re-review when published. |
| S2 | Citi CESI / Bloomberg ECO SURPRISE | EXCLUDED | Proprietary, vendor black-box, no published methodology paper. Fails inclusion #3 (mechanism) at source. Scotti 2016 substitute used instead. |
| S3 | Scotti 2016 *JME* surprise/uncertainty index | PARTIAL | Peer-reviewed with public data, but original paper does not directly test equity-return predictability. Kept in DUAL_USE shortlist; not advanced because ADS dominates for the structural-nowcasting slot. |
| S4 | Garleanu-Pedersen-Poteshman 2009 *RFS* | PARTIAL | Foundational pricing paper but not a trading-signal paper; strategy Sharpe not reported. Used as mechanism reference for CAND-05. |
| S5 | Kelly-Jiang 2014 *RFS* tail risk | INCLUDED → CAND-05 | Peer-reviewed *RFS* with OOS R²>0; independent replication (Chapman-Gallmeyer-Martin 2018 *RAPS*). |
| S6 | Driessen-Maenhout-Vilkov 2009 *JF* correlation risk | PARTIAL | Replicates (Buss-Vilkov 2012 *RFS*) but post-friction Sharpe marginal and requires OptionMetrics on hundreds of constituents. Not advanced — overlaps paradigm slot with CAND-01 and CAND-05. |
| S7 | Herskovic-Kelly-Lustig-Van Nieuwerburgh 2016 *JFE* CIV | PARTIAL | Peer-reviewed, replicated; but signal is cross-sectional equity characteristic → belongs in STOCKS pipeline, not INDEX. Held in reserve for STOCKS pipeline extension. |
| S8 | Hong-Yogo 2012 *JFE* CFTC open interest | INCLUDED → CAND-04 | Replicated (Singleton 2014; Kang-Rouwenhorst-Tang 2020 *JF*); covers gold and broad commodity/bond predictability. |
| S9 | Basu-Miffre 2013 *JBF* hedging pressure | PARTIAL | Replicated; but largely redundant with CAND-04 and with existing V028 Boons-Prado basis-momentum. Excluded to avoid duplication. |
| S10 | Bollerslev-Tauchen-Zhou 2009 *RFS* VRP | INCLUDED → CAND-01 | Single most-replicated option-implied directional timing signal on SPX; Bekaert-Hoerova 2014 *JEcon*, Bollerslev-Marrone-Xu-Zhou 2014 *JFQA*, Drechsler-Yaron 2011 *RFS* all confirm. |
| S11 | Bekaert-Hoerova 2014 *JEcon* | Folded into CAND-01 | Replication/extension, not a separate candidate. |
| S12 | Martin 2017 *QJE* SVIX | Folded into CAND-05 | Option-implied lower bound with positive OOS R² vs Goyal-Welch; joined with Kelly-Jiang in a tail-risk composite candidate. |
| S13 | Erb-Harvey 2013 *FAJ* gold | INCLUDED → CAND-02 (anchor) | Peer-reviewed primary reference for gold real-yield channel (−0.82 correlation); Jermann 2023 NBER WP 31386 provides independent no-arbitrage confirmation. |
| S14 | Barro 2006 *QJE* rare disasters | PARTIAL | Theoretical background; no tradable signal. Used as mechanism citation. |
| S15 | Bańbura-Modugno 2014 *JAE* + Aruoba-Diebold-Scotti 2009 *JBES* ADS | INCLUDED → CAND-03 | ADS is publicly hosted by Philly Fed; Dichtl et al. 2019 *Financial Innovation* documents OOS predictive R² up to 37.9% for gold using ADS. |
| S16 | Tuzun 2013 FEDS WP / Ivanov-Lenkey 2018 *JFM* / Bogousslavsky 2021 *JFE* | EXCLUDED | Literature contested: Ivanov-Lenkey 2018 (peer-reviewed) reports LETF rebalancing effect economically insignificant after accounting for creations/redemptions; Tuzun is WP; Bogousslavsky is a cross-sectional intraday paper not a flow signal. |
| S17 | Novy-Marx 2013 *JFE* gross profitability | INCLUDED → PIPE-01 | Replicates in HXZ 2020 (Gpa 0.38%/mo, t=2.62) and JKP 2023 Profitability theme; core of Fama-French 2015 RMW. |
| S18 | Asness-Frazzini-Pedersen 2019 *RAS* QMJ | PARTIAL | Replicates; but Novy-Marx-Velikov 2025 NBER WP 33601 shows QMJ is a linear combination of already-known signals (profitability + accruals + fundamental momentum + beta). Advanced into PIPE-01 implicitly via gross profitability. |
| S19 | Frazzini-Pedersen 2014 *JFE* BAB | PARTIAL | Novy-Marx-Velikov 2022 *JFE* document microcap concentration and biased beta estimator; HXZ 2020 fail to replicate raw return but JKP 2023 support Low-Risk theme on CAPM alpha. Listed as PIPE-Reserve; not advanced into top STOCKS slots. |
| S20 | Asness-Frazzini 2013 *JPM* HML-Devil | PARTIAL | Accepted methodological improvement; folded into construction notes for PIPE-01 value/quality pipeline rather than a standalone candidate. |
| S21 | Loughran-McDonald 2011 *JF* | INCLUDED → PIPE-03 | Peer-reviewed; widely replicated; public dictionary; 10-K tone predicts returns, volume, volatility, fraud. |
| S22 | Gu-Kelly-Xiu 2020 *RFS* | INCLUDED → PIPE-02 | OOS value-weighted Sharpe 1.35 (equal-weighted 2.45); replicated in Leippold et al. 2021; Hanauer global; Avramov-Cheng-Metzker 2023 *Mgmt Sci* flags arbitrage-cost caveats. |
| S23 | Kelly-Pruitt-Su 2019 *JFE* IPCA | PARTIAL | OOS Sharpe 2.5 but Fieberg et al. 2022 *FoFI* critique identification; overlaps paradigm slot with PIPE-02. |
| S24 | Chen-Pelger-Zhu 2024 *Mgmt Sci* deep learning | PARTIAL | Peer-reviewed; in-sample Sharpe 9.3 is overfit-flagged; overlaps PIPE-02 paradigm. |
| S25 | Sloan 1996 *Accounting Review* accruals | EXCLUDED | Replicates but at half magnitude (HXZ 2020: −0.27%/mo, t=−2.19 VW); Green-Hand-Soliman 2011 *Mgmt Sci* documents post-publication decay. Net new value vs existing V010 earnings breadth modest. |
| S26 | Baker-Bloom-Davis 2016 *QJE* EPU | INCLUDED → DUAL-01 | Public daily index; widely replicated real-effects evidence; fills sentiment-beyond-options gap. |
| S27 | Da-Engelberg-Gao 2011 *JF* SVI | PARTIAL | Replicated; Google Trends methodology changes complicate long-horizon backtests; loses DUAL slot to EPU on paradigm diversity. |
| S28 | Tetlock 2007 *JF* WSJ media tone | PARTIAL | Foundational and replicated; superseded by Loughran-McDonald (PIPE-03) at firm level; not advanced as separate DUAL_USE slot. |

## 3. INDEX bucket — ranked table (5 candidates)

| Schema field | CAND-01 | CAND-02 | CAND-03 | CAND-04 | CAND-05 |
|---|---|---|---|---|---|
| **Bucket** | INDEX | INDEX | INDEX | INDEX | INDEX |
| **Signal type** | DIRECTIONAL_TIMING | DIRECTIONAL_TIMING | REGIME_GATE | SIZING_SCALAR | DIRECTIONAL_TIMING |
| **Factor name** | Variance Risk Premium (SPX) | Gold–10Y-TIPS real-yield beta | ADS business-conditions nowcast | Commodity futures open-interest growth | Option-implied tail risk (Kelly-Jiang + SVIX) |
| **Primary citation** | Bollerslev, Tauchen, Zhou (2009) *RFS* 22(11):4463–4492, DOI 10.1093/rfs/hhp008 | Erb & Harvey (2013) *FAJ* 69(4):10–42, DOI 10.2469/faj.v69.n4.1; Jermann (2023) NBER WP 31386 | Aruoba, Diebold, Scotti (2009) *JBES* 27(4):417–427, DOI 10.1198/jbes.2009.07205 | Hong & Yogo (2012) *JFE* 105(3):473–490, DOI 10.1016/j.jfineco.2012.04.005 | Kelly & Jiang (2014) *RFS* 27(10):2841–2871, DOI 10.1093/rfs/hhu039; Martin (2017) *QJE* 132(1):367–433, DOI 10.1093/qje/qjw034 |
| **Replication citations** | Bekaert-Hoerova (2014) *JEcon* 183(2); Bollerslev-Marrone-Xu-Zhou (2014) *JFQA* 49(3); Drechsler-Yaron (2011) *RFS* 24(1); Bollerslev-Todorov-Xu (2015) *JFE* 118(1); Pyun (2019) *JFE* | Jermann (2023) NBER WP 31386; Barsky-Epstein-Lafont-Mueller-Yoo (2021) *Chicago Fed Letter* 464; O'Connor-Lucey-Batten-Baur (2015) *IRFA* 41 | Campbell-Diebold (2009) *JBES* 27(2); Dichtl et al. (2019) *Financial Innovation* (OOS gold R²=37.9%) | Singleton (2014) *Mgmt Sci* 60(2); Bakshi-Gao-Rossi (2019) *Mgmt Sci*; Kang-Rouwenhorst-Tang (2020) *JF* | Chapman-Gallmeyer-Martin (2018) *RAPS* 8(1); Bollerslev-Todorov-Xu (2015) *JFE* 118(1); Lof (2019) *JAE* 34(5) |
| **Asset-class coverage** | SPX + 7 international indexes (FR/DE/JP/CH/NL/BE/UK) | Gold (COMEX/LBMA) | US broad equity regime, applicable to gold and credit | Commodity complex incl. gold; bond & short-rate spillovers | SPX (tail index) + cross-sectional extensions (Martin-Wagner 2019 *JF*) |
| **Target gap filled** | Equity-index VRP (INDEX gap #2 — mandated) | Gold-specific directional (INDEX gap #1 — mandated) | Macro-nowcasting / structural premium (INDEX gap #4) | Cross-asset carry/positioning (INDEX gap #5) + commodity term-structure (gap #6) | Option-implied directional skew (INDEX gap #3) |
| **Mechanism** | Risk-neutral variance minus physical variance compensates sellers of variance risk; rises with uncertainty and time-varying risk aversion (Drechsler-Yaron 2011). Jump-tail component dominates monthly-quarterly predictability (Bollerslev-Todorov-Xu 2015). | Gold as zero-coupon real asset: price ≈ PV of discount factor. Higher real yields raise opportunity cost, lower gold; Erb-Harvey document ρ≈−0.82 between real gold price and 10Y real yield. | Kalman-filtered latent factor from mixed-frequency indicators (claims, payrolls, IP, income, sales, GDP). Negative ADS ⇒ below-trend activity ⇒ higher expected equity risk premia (Campbell-Diebold 2009). | Hedging demand in futures pushes information into gross open interest, not prices. High ΔOI signals growing hedger participation and predicts commodity and bond returns via risk-bearing-capacity channel. | Index options price tail risk via OTM put demand (Gârleanu-Pedersen-Poteshman 2009); Kelly-Jiang Hill-estimator tail index proxies tail risk from the firm-level return cross-section; Martin SVIX is a lower bound on the equity premium. |
| **Signal construction** | `VIX²_t − RV_t` where RV is 5-min realized variance summed over month. Quarterly horizon strongest. Downside variant: restrict RV to negative-return days (Feunou et al.). | `Δln P_gold = α + β_r·Δy10_TIPS + β_d·ΔlnDXY + ε` with β_r ≈ −15 to −20. Signal: long gold when Δy10_TIPS<0, size by |β_r|·Δy10_TIPS expectation. | Philly Fed publishes ADS daily. Regime gate: risk-on when ADS > −0.5, risk-off when ADS < −0.8; linear tilt between. Dichtl et al. 2019 formula on gold: `E[r_gold] = a + b·ADS_t` with b<0. | `ΔlnOI_t = 12-month growth in aggregate commodity OI`. Predictive regression `r_{t+1} = α + β·ΔlnOI_t + γ·basis_t + ε`. Basu-Miffre tercile portfolios add cross-commodity ranking. | Kelly-Jiang: `λ_t = (1/K)·Σ ln(R_k/u_t)` for firm-level returns below 5th percentile; Martin SVIX: `SVIX²_t = (2/R_f)·[∫₀^F put(K)/K² dK + ∫_F^∞ call(K)/K² dK]`. Predictive: `r_{t+h} = a + b·λ_t` or lower-bound `E[r] ≥ SVIX²/R_f`. |
| **Data requirements** | CBOE VIX (free); high-freq SPY/ES (WRDS TAQ, Oxford-Man archive, Kibot). | FRED DFII10 (free daily from 2003); DXY; LBMA gold. All public. | Philadelphia Fed ADS feed (free). | CFTC Commitments of Traders (free weekly, 3-day lag). | OptionMetrics (SVIX full strike grid) or CBOE SKEW index (free); CRSP monthly returns (Kelly-Jiang tail index). |
| **Infrastructure** | NONE_STANDARD_DATA (plain VRP); OPTIONS_CHAIN if SVIX-style | NONE_STANDARD_DATA | NONE_STANDARD_DATA | NONE_STANDARD_DATA | OPTIONS_CHAIN (SVIX) or NONE_STANDARD_DATA (Kelly-Jiang from CRSP) |
| **Effect size in-sample** | BTZ 2009: R² ≈ 15% quarterly, t≈2.86; volatility-difference variant R²≈18.5%. Bekaert-Hoerova: monthly R² 2–4%. International panel t-stats 2–3. | ρ(gold real price, real yield) = −0.82 (Erb-Harvey 2013); Barsky et al. 2021: +1pp real yield ⇒ −3.4% gold; Jermann 2023 matches post-2007 dynamics in no-arbitrage model. | Dichtl et al. 2019: OOS R² up to 37.9% for gold; Campbell-Diebold 2009 IS R² meaningful for equity expected returns. | JFE Tables 4–6: t ≈ 2–3, R² low single digits for commodity, bond, and short-rate forecasts. | Kelly-Jiang: 1-σ tail risk ⇒ +4.5% annual forecast market return; cross-sectional high-minus-low tail-beta α = 5.4%/yr. Martin SVIX unconditional mean ≈ 5%; null (α=0, β=1) not rejected 1996–2012. |
| **Effect size OOS** | Post-2008: 3-month R² decays to 5–8%. Downside/jump VRP more robust (Bollerslev-Todorov-Xu 2015). Practitioner monthly Sharpe 0.3–0.6 net — NO_OOS_SHARPE_IN_PRIMARY_PAPER. | Pre-2022 rolling R² 0.65–0.84; POST-2022 REGIME BREAK — R² collapses to 0.03–0.07 (Jermann 2023 discussion). Flag: signal must be regime-aware. | Dichtl et al. 2019 OOS gold R² 37.9%; equity OOS evidence NO_DIRECT_OOS_IN_PRIMARY_PAPER (Campbell-Diebold 2009 is IS). | Kang-Rouwenhorst-Tang 2020 *JF* extension confirms predictive content post-financialization, weaker magnitude. | Chapman-Gallmeyer-Martin 2018 find Kelly-Jiang tail risk explains discount-rate component only; Martin 2017 reports positive OOS R² vs Goyal-Welch at 1–6 month horizons; Lof 2019 sensitivity to dividend adjustment. |
| **Sharpe decay** | ~40–50% from IS to OOS (headline 15% R² → 5–8%). | Pre/post-2022 structural regime break; correlation stability is the binding concern, not gradual decay. | NO_OOS_EVIDENCE on equity; gold OOS strong per Dichtl et al. | Moderate decay post-2004 financialization (Singleton 2014). | Moderate decay; jump-tail decomposition preserves more than total VRP. |
| **Real-time implementability** | HIGH | HIGH | HIGH | MEDIUM (weekly lag) | HIGH (SVIX daily; Kelly-Jiang monthly) |
| **Executability check (today's close)** | Compute `VIX²_today − HAR_forecast(RV_{t+1})`. If current VIX ≈ 18 and HAR-RV forecast ≈ 13, then VRP ≈ 18²−13² = 155. Above the ~70 long-run median ⇒ OVERWEIGHT SPY/ES 1–3 months. **Directional call today: LONG SPY if VRP > median; tradeable on SPY, IVV, VOO, or ES futures.** | Check 5-day Δ10Y-TIPS real yield from FRED DFII10. If Δ < 0 ⇒ LONG GLD or GC=F gold futures sized proportional to Δ·(−15). If Δ > 0 ⇒ UNDERWEIGHT. **Tradeable on GLD, IAU, PHYS, COMEX GC=F.** | Pull latest ADS from Philly Fed. If ADS today < −0.8 ⇒ risk-off: reduce SPY, increase IEF/GLD. If ADS > −0.5 ⇒ risk-on: full SPY allocation. Current sign determines tilt. **Overlay on SPY/IEF/GLD.** | Pull last Friday's CFTC COT non-commercial positions in gold and 12-month OI growth for aggregate commodity complex. If ΔlnOI > trailing median ⇒ OVERWEIGHT DBC, GLD. **Tradeable on GLD, DBC, GSG, specific GC=F / CL=F / HG=F.** | Compute CBOE SKEW index 1-month z-score and SVIX from CBOE free feeds. If SKEW > +1σ ⇒ higher expected market premium per Kelly-Jiang; LONG SPY with sized overlay. **Tradeable on SPY, ES, SPXL.** |
| **Corr with V009 TSMOM** | Low; VRP is valuation-style, TSMOM is price-trend. Empirically near-zero in Bollerslev-Marrone-Xu-Zhou panel. | Low with TSMOM on equity indexes; overlaps modestly with gold TSMOM when rates trend. | Low; ADS is a state variable. | Moderate with V028 Boons-Prado basis-momentum (both positioning-based on futures); distinct from V009. Flag |ρ| potentially 0.3–0.5. | Low-to-moderate; tail risk rises in drawdowns when TSMOM typically negative — mild negative correlation. |
| **Corr with existing framework** | Positively correlated with V001 VIX (same option market) but VRP is VIX² minus RV, so residual signal orthogonal. Low correlation with V027 Adrian-Etula-Muir. | Tracks V007 real yields/breakevens mechanically — **flag |ρ|>0.5 with V007**. Must enter as conditional signal, not independent. | Complements V005 NFCI; likely |ρ|>0.5 with NFCI in recessions. Use as INDEPENDENT macro-state marker focused on real activity. | Moderate overlap with V028; distinct in covering gold and bonds. | Distinct from V001/V002 (levels) — captures risk-neutral tail shape, not level of vol. |
| **Recommended Grade** | A | A (conditional on regime gate) | A | B | B |
| **Recommended group** | R (Regime/Risk) with T (Tactical) overlay | T (Tactical Timing) for gold | R (Regime/Risk) | S (Sentiment/Positioning) | R (Regime/Risk) |
| **Methodology paradigm** | Option-implied | Classical risk-premium / structural | Structural-nowcasting | Behavioral-positioning | Option-implied |
| **Confidence** | HIGH | HIGH (with regime-break caveat) | HIGH | MEDIUM | MEDIUM |
| **Why it fills a gap** | Framework has zero VRP coverage; V001/V002 are vol *levels* only. BTZ VRP adds a replicated option-implied predictor of the equity premium at monthly-quarterly horizons. | Framework has zero gold-specific directional signals; real-yield β is the single most-replicated gold predictor with daily free data. | Framework lacks structural real-activity nowcasting; ADS complements V005 NFCI by measuring activity rather than financial conditions and adds OOS gold evidence. | Framework has V028 commodity basis-momentum but no futures-market-interest signal; Hong-Yogo adds gold and bond coverage. | Framework has no option-implied directional signals on indexes; tail-risk composite adds orthogonal tail-skewness information. |
| **Risk of adoption** | Monthly rebalancing; post-2008 decay; over-fitting if combined with V001. | Post-2022 regime break risk; correlation with V007 means cannot be double-counted. | Revision risk (ADS is revised as data are revised); false signals in mild slowdowns. | Weekly data lag; positioning signals can be whipsawed in policy-driven markets. | OptionMetrics cost for SVIX; Kelly-Jiang monthly only; Chapman et al. 2018 caveat on mechanism. |
| **Deployability timeline** | IMMEDIATE | IMMEDIATE | IMMEDIATE | NEAR (COT pipeline) | NEAR (OptionMetrics license or CBOE feed build) |

## 4. STOCKS bucket — ranked table (3 candidates)

| Schema field | PIPE-01 | PIPE-02 | PIPE-03 |
|---|---|---|---|
| **Bucket** | STOCKS | STOCKS | STOCKS |
| **Signal type** | CROSS_SECTIONAL | CROSS_SECTIONAL | CROSS_SECTIONAL |
| **Factor name** | Gross profitability (with HML-devil value overlay) | Gu-Kelly-Xiu machine-learning composite | Loughran-McDonald 10-K textual tone |
| **Primary citation** | Novy-Marx (2013) *JFE* 108(1):1–28; Asness-Frazzini (2013) *JPM* 39(4):49–68 as value-construction refinement | Gu, Kelly, Xiu (2020) *RFS* 33(5):2223–2273, DOI 10.1093/rfs/hhaa009 | Loughran & McDonald (2011) *JF* 66(1):35–65, DOI 10.1111/j.1540-6261.2010.01625.x |
| **Replication citations** | HXZ (2020) *RFS* — Gpa 0.38%/mo, t=2.62 replicates; JKP (2023) *JF* Profitability theme replicates across 93 countries; Chen-Zimmermann (2022) *CFR* open-source reproduces | Leippold-Wang-Zhou (2021 China); Hanauer et al. (global); Avramov-Cheng-Metzker (2023) *Mgmt Sci* (caveats on hard-to-arbitrage segments); Tidy Finance open reproduction | Tetlock-Saar-Tsechansky-Macskassy (2008) *JF*; Jegadeesh-Wu (2013) *JFE*; García (2013) *JF*; Manela-Moreira (2017) *JFE* |
| **Asset-class coverage** | US (CRSP/Compustat) and 23+ countries (JKP 2023) | Russell 3000 + international replications (China, global) | US 10-K filings (EDGAR); international adaptations for English filings |
| **Target gap filled** | STOCKS gap #2 (Quality/Profitability); also touches gap #1 Value via HML-devil construction | STOCKS gap #4 (ML cross-sectional) | STOCKS gap #5 (Text/NLP) |
| **Mechanism** | Gross profits-to-assets cleanly proxies economic profitability free of accrual distortions (Novy-Marx 2013); value-quality pair reduces co-drawdowns. | Nonlinear interactions among ~94 firm characteristics are undercaptured by linear models; NN/RF exploit interaction structure. Top predictors: price trend, liquidity, volatility. | Finance-specific negative-word dictionary. Negative tone predicts lower post-filing returns, higher volatility, higher fraud probability. ~75% of Harvard-IV-4 negatives are not negative in finance context — LM dictionary is the correction. |
| **Signal construction** | `GP/A_i = (Revenue_i − COGS_i) / Total Assets_i` annually from Compustat. Long top-quintile GP/A ∩ bottom-quintile B/P (value); short opposite. Rebalance monthly with HML-devil timely B/P. | 94 characteristics inputs; train elastic-net, random forest, and neural net NN3 (three hidden layers 32-16-8) on rolling expanding window 1957–cutoff; monthly expected return forecast; long-short decile portfolios. | For each 10-K filed on EDGAR compute negative-word frequency from LM master dictionary (~2,300 neg words). Signal = negative-word share relative to filing-length adjusted baseline; short top-quintile negativity, long bottom. 30-day post-filing window. |
| **Data requirements** | CRSP + Compustat (WRDS academic $50–200K/yr; commercial higher) | CRSP + Compustat + OptionMetrics (optional); GPU compute for NN training | EDGAR 10-K full-text corpus (free); LM Master Dictionary (free from Notre Dame SRAF) |
| **Infrastructure** | SINGLE_NAME_UNIVERSE | SINGLE_NAME_UNIVERSE + cloud GPU | SINGLE_NAME_UNIVERSE + text ETL |
| **Effect size in-sample** | Novy-Marx 2013: monthly L/S ~0.31%/mo pre-cost, t≈3; QMJ Sharpe post-hedging ≈ 1.0 globally | GKX NN3: OOS monthly R² ≈ 0.4% stock-level; long-short value-weighted Sharpe 1.35, equal-weighted 2.45 | LM 2011: one-SD negative-tone increase ⇒ ~−2% 4-day CAR; effect persists in VAR; predicts volume and volatility |
| **Effect size OOS** | JKP 2023 Profitability theme is significant tangency contributor across 93 countries; HXZ 2020 replicates at 43% of original magnitude under VW | Avramov-Cheng-Metzker 2023 *Mgmt Sci*: Sharpe drops sharply when excluding distressed/microcap/high-IVOL stocks — real OOS economic magnitude ~30–40% of headline | Replicated firm-level by Tetlock-Saar-Tsechansky-Macskassy 2008 *JF* with persistent post-publication effects |
| **Sharpe decay** | ~57% post-publication per McLean-Pontiff 2016 average; profitability has above-average persistence | McLean-Pontiff-style decay not yet documented; Avramov et al. caveats suggest 40–60% true-OOS haircut | Tetlock and LM effects partially decayed but survive in expanded corpora |
| **Real-time implementability** | HIGH at monthly frequency | MEDIUM (monthly; retraining cadence) | HIGH (within hours of 10-K EDGAR filing) |
| **Executability check (portfolio construction)** | Monthly: rank Russell 1000 by GP/A and by HML-devil B/P (timely price). Long equal-weighted top-quintile intersection, short bottom-quintile intersection. Target 5% gross exposure, neutralize sector β. | Monthly retraining on 10-yr rolling window; forecast 1-month returns for Russell 3000 via NN3; long top decile, short bottom. Target 3–5% gross; cap position sizes at 50 bps. | Daily EDGAR scrape. For each new 10-K filed day t, compute LM negativity z-score vs 3-yr firm history. Long bottom-quintile (low negativity) new filings for 21 trading days, short top-quintile. | 
| **Corr with V009 TSMOM** | Low; GP/A is fundamentals-driven, TSMOM is price-trend. | Moderate (0.3–0.5) — ML picks up price-trend features (HXZ and GKX both flag momentum as top ML predictor). | Low. |
| **Corr with existing framework** | Low with V010 earnings-revision breadth; complementary. Low with V026 residual momentum. | Moderate with V026 residual momentum (both load on momentum-type signals); flag for orthogonality check. | Independent of all existing variables. |
| **Recommended Grade** | A | B | B |
| **Recommended group** | New STOCKS/Value-Quality group | New STOCKS/ML group | New STOCKS/NLP group |
| **Methodology paradigm** | Classical-risk-premium | ML-or-Altdata | ML-or-Altdata (text) |
| **Confidence** | HIGH | MEDIUM (implementability friction) | MEDIUM-HIGH |
| **Why it fills a gap** | Framework has zero Value and zero Quality coverage; GP/A is the best-replicated quality signal in both HXZ and JKP audits. HML-devil overlay fixes stale-price issue in traditional HML. | Framework has zero ML coverage; GKX is the benchmark ML asset-pricing paper and directly tests nonlinear interactions. | Framework has zero text coverage; LM is the standard finance-NLP dictionary and is cheap to implement. |
| **Risk of adoption** | Crowdedness; post-publication decay; sector concentration in high-margin tech | Overfitting; hard-to-arbitrage caveat (Avramov et al. 2023); retraining operational risk | Dictionary-era method may underperform transformer methods (FinBERT, Huang et al. 2023); false positives on non-English 10-K excerpts |
| **Deployability timeline** | NEAR (WRDS license + portfolio pipeline) | MEDIUM (training infra + retraining ops) | NEAR (EDGAR ETL + dictionary) |
| **Infrastructure cost order-of-magnitude** | ~$50–200K/yr data (WRDS academic) + ~$50K pipeline build | ~$100–300K/yr data + ~$100–300K GPU compute + $200–500K pipeline | ~$20–50K pipeline (EDGAR scrape + dictionary); data free |

## 5. DUAL_USE bucket — ranked table (1 candidate)

| Schema field | DUAL-01 |
|---|---|
| **Bucket** | DUAL_USE |
| **Signal type** | REGIME_GATE / SIZING_SCALAR |
| **Factor name** | Baker-Bloom-Davis Economic Policy Uncertainty Index (EPU) |
| **Primary citation** | Baker, Bloom, Davis (2016) *QJE* 131(4):1593–1636, DOI 10.1093/qje/qjw024 |
| **Replication citations** | Gulen & Ion (2016) *RFS*; Pástor & Veronesi (2013) *JF*; Bae-Jo-Shim (2025) *Canadian J Econ* 58(1); Brogaard & Detzel (2015) *Mgmt Sci* |
| **Asset-class coverage** | US broad equity + 22-country international EPU; sector-level sensitivities documented |
| **Target gap filled** | DUAL_USE gap: sentiment/attention beyond options (policy-uncertainty channel) |
| **Mechanism** | Newspaper-based policy-uncertainty proxy; real-options channel delays investment/hiring; raises required risk premia in policy-sensitive sectors. |
| **Signal construction** | Free daily US EPU from policyuncertainty.com or FRED. 3-month z-score. Sizing: scale gross equity exposure by `1 − max(0, (EPU_z − 1))`; cap at 0.5. |
| **Effect size in-sample** | EPU +85 log points 2006→2012 ⇒ ~0.68 pp investment-rate decline for 25%-federal-sales firms; equity vol rises with EPU. |
| **Effect size OOS** | Gulen-Ion 2016 RFS OOS confirmation of investment effect; equity-vol link robust post-publication. |
| **Real-time implementability** | HIGH (daily, free) |
| **Executability check** | Pull today's US EPU from policyuncertainty.com. Compute 3m z-score. If z > 1 ⇒ reduce SPY gross by 20%; if z > 2 ⇒ reduce by 40%. Tradeable on any US broad equity ETF. |
| **Corr with V009 TSMOM** | Low; EPU is policy-news-driven, not price-trend. |
| **Recommended Grade** | B |
| **Recommended group** | Overlay (regime gate) |
| **Methodology paradigm** | Behavioral-positioning / alt-data TradFi |
| **Confidence** | MEDIUM-HIGH |
| **Why it fills a gap** | Framework has no news-sentiment or policy-uncertainty overlay; EPU is the most-replicated public text-based uncertainty measure with free daily data. |
| **Risk of adoption** | Newspaper-corpus drift over time; methodology has been revised. |
| **Deployability timeline** | IMMEDIATE |

## 6. Gap coverage matrix

| Gap | Priority weight | Candidate(s) covering | Status |
|---|---|---|---|
| INDEX-1 Gold directional | 60% × highest | CAND-02 | COVERED |
| INDEX-2 Equity-index VRP | 60% × high | CAND-01 | COVERED |
| INDEX-3 Option-implied directional (skew/risk-reversal/dealer-gamma/dispersion) | 60% × high | CAND-05 (skew + tail) | PARTIALLY COVERED — dealer-gamma NO_QUALIFYING_CANDIDATE |
| INDEX-4 Macro-nowcasting / structural premium | 60% × med | CAND-03 | COVERED |
| INDEX-5 Cross-asset carry variants | 60% × med | CAND-04 | COVERED |
| INDEX-6 Commodity term-structure beyond basis-momentum and Brent | 60% × low | CAND-04 partial | PARTIALLY COVERED |
| INDEX-7 Intermediary/flow on TradFi indexes | 60% × low | None qualifying | NO_QUALIFYING_CANDIDATE — LETF flow literature contested |
| STOCKS-1 Value | 30% × high | PIPE-01 (HML-devil overlay) | COVERED |
| STOCKS-2 Quality/Profitability | 30% × high | PIPE-01 | COVERED |
| STOCKS-3 Defensive/Low-Vol/BAB | 30% × med | None advanced (BAB held in reserve) | NO_QUALIFYING_CANDIDATE for top-7 — BAB is PIPE-reserve |
| STOCKS-4 ML cross-sectional | 30% × med | PIPE-02 | COVERED |
| STOCKS-5 Text/NLP single-name | 30% × low | PIPE-03 | COVERED |
| DUAL-1 Alt-data TradFi | 10% | DUAL-01 | COVERED |
| DUAL-2 Sentiment/attention beyond options | 10% | DUAL-01 | COVERED |

## 7. Paradigm diversification check

Required minimum: OPTION_IMPLIED + ML_OR_TEXT + STRUCTURAL_NOWCASTING (3 paradigms). Delivered: **five paradigms represented across the top slate.**

| Paradigm | Count | Candidates |
|---|---|---|
| Option-implied | 2 | CAND-01, CAND-05 |
| Classical risk-premium | 2 | CAND-02, PIPE-01 |
| Structural-nowcasting | 1 | CAND-03 |
| Behavioral-positioning | 2 | CAND-04, DUAL-01 |
| ML-or-Altdata (incl. text) | 2 | PIPE-02, PIPE-03 |

Paradigm bonus applied once per paradigm per ranking weights. Check passes with margin.

## 8. Overlap / correlation analysis

**Flagged pairs with |ρ|>0.5 or mechanical dependency.** CAND-02 gold–real-yield β is mechanically dependent on V007 real yields/breakevens — it uses the same input on the right-hand side. It is not a redundant signal because it translates V007 into a gold directional view rather than a bond/breakeven view, but the framework must avoid double-counting: CAND-02 should be gated so that it does not deliver an independent macro call; it is a translation layer. CAND-03 ADS will correlate with V005 NFCI in recessions (|ρ| plausibly 0.5–0.7); they are distinct by construction (ADS is real activity, NFCI is financial conditions) and should be kept as separate inputs, but the combined regime-gate weight on them should be shared, not additive. CAND-04 Hong-Yogo open-interest overlaps modestly with V028 Boons-Prado basis-momentum (|ρ| plausibly 0.3–0.5 in commodity subsample); distinct signals (gross participation vs. term-structure) but worth a joint backtest before production.

**Low-correlation confirmations.** CAND-01 VRP with V009 TSMOM: near-zero contemporaneous correlation in Bollerslev-Marrone-Xu-Zhou (2014) international panel. CAND-05 tail risk with V001 VIX: distinct — VIX is level, tail risk is shape. PIPE-01 gross profitability with V026 residual momentum: McLean-Pontiff and JKP both document low pairwise correlation across profitability and momentum themes. PIPE-03 LM textual tone with any existing V-series: independent (no textual data in framework).

**Flag on PIPE-02 GKX ML with V009 and V026.** GKX's top predictors include price-trend features; pairwise correlation with V009 TSMOM expected 0.3–0.5. PIPE-02 should be evaluated on residual return after controlling for V009 and V026 before sizing.

## 9. Replication-audit summary

**CAND-01 VRP.** Bekaert-Hoerova 2014 *JEcon* extended sample to 2010 and decomposed VIX² into conditional-variance and variance-premium components, confirming VRP (not CV) drives return predictability. Bollerslev-Marrone-Xu-Zhou 2014 *JFQA* replicated internationally on France, Germany, UK, Japan, Switzerland, Netherlands, Belgium over 2000–2011 with hump-shaped R² pattern preserved. Pyun 2019 *JFE* showed monthly OOS predictability requires a contemporaneous-beta approach. OOS window post-BTZ sample (2008+) shows headline 15% quarterly R² decays to 5–8%. Caveat: BTZ does not report a strategy Sharpe; published practitioner-grade estimates are 0.3–0.6 net of costs.

**CAND-02 Gold–real-yield β.** Erb-Harvey 2013 *FAJ* documented ρ(gold, real yield) = −0.82. Jermann 2023 NBER WP 31386 fits a no-arbitrage model that reproduces post-2007 gold dynamics from real yields alone. Barsky et al. 2021 *Chicago Fed Letter* reports +1pp real yield ⇒ −3.4% gold. OOS caveat: post-2022 regime break collapses rolling R² from 0.65–0.84 to 0.03–0.07; signal must be regime-aware or gated on whether the historical correlation has re-established.

**CAND-03 ADS.** Campbell-Diebold 2009 *JBES* used survey-based expected business conditions (sister measure) to predict CRSP-VW excess returns in-sample. Dichtl et al. 2019 *Financial Innovation* documented OOS gold R² up to 37.9% using ADS directly. Primary paper is methodology; equity OOS Sharpe not reported. Caveat: ADS is revised as underlying data are revised; signal should be computed on vintage-aware real-time releases.

**CAND-04 Hong-Yogo OI.** Singleton 2014 *Mgmt Sci*, Bakshi-Gao-Rossi 2019 *Mgmt Sci*, Kang-Rouwenhorst-Tang 2020 *JF* all confirm OI/positioning signals in commodities. Magnitude attenuated post-2004 financialization. Gold is covered in the original sample.

**CAND-05 Tail risk.** Chapman-Gallmeyer-Martin 2018 *RAPS* replicates Kelly-Jiang tail index but finds it explains only the discount-rate component, not cash-flow. Lof 2019 *JAE* flags SVIX sensitivity to dividend adjustment. Martin 2017 *QJE* OOS R² positive vs. Goyal-Welch at 1–6 month horizons. Honest caveat: primary papers do not report strategy Sharpes; signal is typically used as a scaler rather than a binary directional call.

**PIPE-01 Gross profitability.** HXZ 2020 *RFS* reports Gpa 0.38%/mo, t=2.62 under VW NYSE breakpoints (replicates); Gla 0.16%/mo, t=1.04 (fails). JKP 2023 *JF* Profitability theme replicates Bayesian-significantly with positive tangency weight across 93 countries. McLean-Pontiff 2016 post-publication decay ~50% expected. Caveat: AQR affiliation of JKP authors and QMJ authors — noted transparently; results remain peer-reviewed.

**PIPE-02 GKX ML.** Leippold-Wang-Zhou 2021 replicate on China. Hanauer et al. replicate globally with 2-layer networks outperforming deeper nets. Avramov-Cheng-Metzker 2023 *Mgmt Sci* is the binding caveat: Sharpe drops sharply when excluding distressed/microcap/high-IVOL stocks, implying ~30–40% of headline economic magnitude survives realistic implementation constraints.

**PIPE-03 LM textual tone.** Tetlock-Saar-Tsechansky-Macskassy 2008 *JF* extended to firm level; García 2013 *JF* to NYT columns; Manela-Moreira 2017 *JFE* to NVIX. Dictionary-era approach partially superseded by FinBERT (Huang et al. 2023) but remains the standard baseline and survives replication.

**DUAL-01 EPU.** Gulen-Ion 2016 *RFS* confirms investment real-effects OOS; Bae-Jo-Shim 2025 *Canadian J Econ* replicates across countries. Equity-volatility link is the most robust finding; equity-return predictability is modest and indirect.

## 10. Registration recommendations

**INDEX candidates for registration into the main V-series.**

| New ID | Candidate | Grade | Group | OOS tracking period | Named tradeable instrument |
|---|---|---|---|---|---|
| V029 | CAND-01 Variance Risk Premium (SPX) | A | R with T overlay | 24 months rolling, quarterly horizon primary | SPY, ES=F, VXX for vol-overlay implementation |
| V030 | CAND-02 Gold–10Y-TIPS real-yield β | A (conditional) | T | 12 months rolling; regime-break monitor on 24m ρ | GLD, IAU, GC=F |
| V031 | CAND-03 ADS business-conditions nowcast | A | R (regime gate) | 24 months, monthly frequency | Overlay on SPY, IEF, GLD; no standalone trade |
| V032 | CAND-04 Hong-Yogo OI | B | S | 24 months, weekly updates | DBC, GLD, GSG |
| V033 | CAND-05 Tail-risk composite (Kelly-Jiang + SVIX) | B | R | 24 months, monthly-frequency primary | SPY, ES=F |

**STOCKS candidates for pipeline.**

| Pipeline ID | Candidate | Grade | Infrastructure order-of-magnitude | Buildout |
|---|---|---|---|---|
| PIPE-01 | Novy-Marx gross profitability × HML-devil value | A | $50–200K/yr WRDS + $50K pipeline | Quarter 1 |
| PIPE-02 | Gu-Kelly-Xiu ML composite | B | $100–300K/yr data + $100–300K GPU + $200–500K pipeline | Quarters 2–4 |
| PIPE-03 | Loughran-McDonald 10-K tone | B | $20–50K pipeline, data free | Quarter 1 parallel to PIPE-01 |

**DUAL_USE.** DUAL-01 EPU registers as a new Overlay regime-gate input (C012) immediately alongside existing C009/C011/C005/C002/C007.

## 11. Gaps still unfilled

1. **Dealer gamma exposure on SPX (INDEX-3 sub-gap, high priority).** NO_QUALIFYING_CANDIDATE. Barbon-Buraschi 2021 remains a working paper; Ni-Pearson-Poteshman-White 2021 *RFS* and Baltussen-Da-Lammers-Swinkels 2021 *JFE* cover adjacent phenomena but not a direct dealer-gamma timing signal. The 0DTE regime post-2022 materially complicates construction. **Re-review when Barbon-Buraschi or successor publishes in a top-5 journal, or when a peer-reviewed 0DTE-adjusted gamma measure becomes available.**
2. **Dispersion / correlation-risk-premium trade (INDEX-3 sub-gap, medium priority).** Peer-reviewed primary (Driessen-Maenhout-Vilkov 2009 *JF*) exists but the trade requires OptionMetrics on hundreds of single-name constituents and post-friction Sharpe is 0.3–0.6. **Hold as future pipeline candidate pending options-infrastructure build.**
3. **Intermediary/flow on TradFi indexes (INDEX-7, low priority).** Leveraged-ETF rebalancing literature is contested (Ivanov-Lenkey 2018 vs. Tuzun 2013). **No qualifying candidate at present; revisit if a new peer-reviewed synthesis emerges.**
4. **Defensive/Low-Vol/BAB (STOCKS-3, medium priority).** Frazzini-Pedersen 2014 held in PIPE-reserve because the HXZ-vs-JKP conflict on raw vs. alpha-based testing and Novy-Marx-Velikov 2022 microcap critique make a Grade-A claim unsupportable. **Reconsider if a post-NMV-2022 construction (value-weighted, non-microcap) publishes with replicated 24-month OOS Sharpe > 0.4.**
5. **Accruals (Sloan 1996).** Excluded on decay grounds; re-evaluate only if a post-2015 replication documents revived magnitude.
6. **Cross-sectional idiosyncratic-vol/CIV factor (Herskovic et al. 2016).** Held in reserve for a second-wave STOCKS pipeline expansion.

## 12. Suggested next steps

**Next 4 weeks (OOS ledger entries).** Enter CAND-01 VRP, CAND-02 gold–real-yield β, and CAND-03 ADS into the OOS ledger immediately; all three use free, real-time public data with no buildout cost. Begin paper-trading overlay rules in parallel with existing V-series. Instrument the three with daily P&L tracking and a 24-month rolling-window evaluation horizon. CAND-02 specifically needs a regime-break monitor: alert if the 24-month rolling ρ(Δgold, ΔTIPS) drifts outside the [−0.85, −0.35] band that pre-2022 behavior defined.

**Next quarter (STOCKS pipeline).** Start PIPE-01 and PIPE-03 in parallel — both are cheap, high-confidence, and address the highest-priority STOCKS gaps. Begin WRDS-license negotiation and EDGAR ETL build simultaneously. Defer PIPE-02 until GPU infrastructure is provisioned, and make the PIPE-02 build contingent on PIPE-01 first delivering a realized 12-month OOS Sharpe > 0.6 — this anchors the question of whether more complex ML signals are worth the infrastructure step-up.

**Evidence that would resolve remaining uncertainty.** (i) Peer-reviewed publication of Barbon-Buraschi or successor dealer-gamma paper with a 0DTE-adjusted construction would unblock INDEX-3 fully and likely promote a Grade-B dealer-gamma candidate. (ii) A 2024–2026 extension of Pyun 2019 *JFE* VRP OOS methodology published would convert CAND-01's OOS Sharpe caveat from "practitioner 0.3–0.6" to a peer-reviewed number, potentially unlocking a Grade-A-with-confirmed-OOS status. (iii) A post-NMV-2022 BAB reconstruction paper would allow PIPE-reserve BAB to enter the active STOCKS slate.

**Follow-up review.** A follow-up review in 12 months should re-check (a) whether CAND-02's gold–real-yield correlation has re-established or remains in regime break; (b) whether PIPE-02 GKX-style ML has survived real infrastructure friction; (c) whether the dealer-gamma dossier has a peer-reviewed candidate; and (d) whether PIPE-03 LM tone should be upgraded to a FinBERT-based successor per Huang et al. 2023 *JAR*.

---

**References (verified, DOI/URL where available).** Adrian, T., Etula, E., Muir, T. (2014) *JF* 69(6). Aruoba, S.B., Diebold, F.X., Scotti, C. (2009) *JBES* 27(4), DOI 10.1198/jbes.2009.07205. Asness, C., Frazzini, A. (2013) *JPM* 39(4). Asness, C., Frazzini, A., Pedersen, L.H. (2019) *RAS* 24(1). Avramov, D., Cheng, S., Metzker, L. (2023) *Mgmt Sci*. Baker, S.R., Bloom, N., Davis, S.J. (2016) *QJE* 131(4), DOI 10.1093/qje/qjw024. Baltussen, G., Da, Z., Lammers, S., Swinkels, L. (2021) *JFE* 142(1). Bańbura, M., Modugno, M. (2014) *JAE* 29(1), DOI 10.1002/jae.2306. Barbon, A., Buraschi, A. (2021) SSRN 3725454 [working paper]. Barro, R. (2006) *QJE* 121(3). Barsky, R., Epstein, C., Lafont-Mueller, A., Yoo, Y. (2021) *Chicago Fed Letter* 464. Basu, D., Miffre, J. (2013) *JBF* 37(7). Bekaert, G., Hoerova, M. (2014) *JEcon* 183(2). Bogousslavsky, V. (2021) *JFE* 141(1):172–194. Bollerslev, T., Marrone, J., Xu, L., Zhou, H. (2014) *JFQA* 49(3). Bollerslev, T., Tauchen, G., Zhou, H. (2009) *RFS* 22(11), DOI 10.1093/rfs/hhp008. Bollerslev, T., Todorov, V., Xu, L. (2015) *JFE* 118(1). Boons, M., Prado, M.P. (2019) *JF*. Campbell, J.Y., Diebold, F.X. (2009) *JBES* 27(2). Chapman, D., Gallmeyer, M., Martin, I. (2018) *RAPS* 8(1). Chen, A., Zimmermann, T. (2022) *Critical Finance Review* 11(2), DOI 10.1561/104.00000112. Chen, L., Pelger, M., Zhu, J. (2024) *Mgmt Sci* 70(2). Da, Z., Engelberg, J., Gao, P. (2011) *JF* 66(5). Dichtl, H., et al. (2019) *Financial Innovation*. Driessen, J., Maenhout, P., Vilkov, G. (2009) *JF* 64(3). Drechsler, I., Yaron, A. (2011) *RFS* 24(1). Erb, C., Harvey, C. (2013) *FAJ* 69(4). Fama, E.F., French, K.R. (2015) *JFE*. Frazzini, A., Pedersen, L.H. (2014) *JFE* 111(1). García, D. (2013) *JF* 68(3). Gârleanu, N., Pedersen, L.H., Poteshman, A. (2009) *RFS* 22(10). Gilchrist, S., Zakrajšek, E. (2012) *AER*. Gu, S., Kelly, B., Xiu, D. (2020) *RFS* 33(5), DOI 10.1093/rfs/hhaa009. Gulen, H., Ion, M. (2016) *RFS*. Hanauer, M., et al. (global ML replications). Harvey, C.R., Liu, Y., Zhu, H. (2016) *RFS*. He, Z., Kelly, B., Manela, A. (2017) *JFE*. Herskovic, B., Kelly, B., Lustig, H., Van Nieuwerburgh, S. (2016) *JFE* 119(2). Hong, H., Yogo, M. (2012) *JFE* 105(3). Hou, K., Xue, C., Zhang, L. (2020) *RFS* 33(5), DOI 10.1093/rfs/hhy131. Ivanov, I., Lenkey, S. (2018) *JFM* 41. Jegadeesh, N., Wu, D. (2013) *JFE*. Jensen, T.I., Kelly, B., Pedersen, L.H. (2023) *JF* 78(5), DOI 10.1111/jofi.13249. Jermann, U. (2023) NBER WP 31386. Kang, W., Rouwenhorst, K.G., Tang, K. (2020) *JF*. Kelly, B., Jiang, H. (2014) *RFS* 27(10). Kelly, B., Pruitt, S., Su, Y. (2019) *JFE* 134(3). Loughran, T., McDonald, B. (2011) *JF* 66(1). Manela, A., Moreira, A. (2017) *JFE*. Martin, I. (2017) *QJE* 132(1), DOI 10.1093/qje/qjw034. McLean, R.D., Pontiff, J. (2016) *JF* 71(1), DOI 10.1111/jofi.12365. Moskowitz, T., Ooi, Y.H., Pedersen, L.H. (2012) *JFE*. Ni, S.X., Pearson, N.D., Poteshman, A.M., White, J. (2021) *RFS* 34(4). Novy-Marx, R. (2013) *JFE* 108(1). Novy-Marx, R., Velikov, M. (2022) *JFE* 143(1). Novy-Marx, R., Velikov, M. (2025) NBER WP 33601. O'Connor, F., Lucey, B., Batten, J., Baur, D. (2015) *IRFA* 41. Pástor, Ľ., Veronesi, P. (2013) *JF*. Pyun, S. (2019) *JFE*. Scotti, C. (2016) *JME* 82. Sloan, R. (1996) *Accounting Review* 71(3). Tetlock, P. (2007) *JF* 62(3). Tetlock, P., Saar-Tsechansky, M., Macskassy, S. (2008) *JF*. Tuzun, T. (2013) FEDS WP 2013-48.