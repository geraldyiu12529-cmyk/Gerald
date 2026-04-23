RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = STOCKS_ONLY_CROSS_SECTIONAL; MIN_CANDIDATES = 5-7; MANDATES = VALUE + QUALITY + DEFENSIVE_BAB + MODERN_PARADIGM_ML_NLP_ALTDATA; PARADIGM_MIN = 3_OF_5; TARGET_GAP_MIN = 4_OF_8.

# Six cross-sectional equity signals to fill the single-name vacuum

## 1. Executive summary

The framework's 32 variables are macro-heavy and contain near-zero single-name cross-sectional signal beyond V010 (earnings-revision breadth) and V026 (residual momentum). To close this gap with replication-audited, mechanism-grounded candidates, I recommend registering six signals as **V029–V034**: (1) **QMJ** — Asness-Frazzini-Pedersen quality composite (Quality slot; Grade B+); (2) **BAB** — Frazzini-Pedersen betting-against-beta (Defensive slot; Grade B+ with construction caveats); (3) **Composite equity issuance / net payout** — Daniel-Titman (Value-adjacent / Investment slot; Grade A); (4) **HML-Devil with cash-based operating profitability overlay** — Asness-Frazzini (2013) updated book-to-price combined with Novy-Marx-style profitability screen (Value slot; Grade B); (5) **Opportunistic-insider signal** — Cohen-Malloy-Pomorski Form 4 classification (Behavioral/Insider slot; Grade B, MEDIUM confidence); (6) **Lazy Prices 10-K textual-change signal** — Cohen-Malloy-Nguyen (Modern-paradigm NLP slot; Grade B, MEDIUM confidence). Gaps closed: Value, Quality, Defensive/BAB, Issuance, Insider, NLP/Text (6 of 8). Time-to-paper-trade ranges from **IMMEDIATE (≤4wk)** for QMJ/BAB/issuance/HML-Devil (AQR Data Library, CRSP, Compustat already in WRDS) to **NEAR (4–12wk)** for insider and Lazy Prices (EDGAR pipeline build). Infrastructure cost: **LOW to LOW-MEDIUM, $25K–$75K/yr** for WRDS plus free EDGAR ingestion; no option-chain or stock-loan vendor is strictly required for the top six. Two mandatory-adjacent gaps remain **NO_QUALIFYING_CANDIDATE at the required grade**: option-implied cross-section (Cremers-Weinbaum / Conrad-Dittmar-Ghysels are promising but require OptionMetrics and show material post-2008 decay) and stock-loan/fee (Cohen-Diether-Malloy / D'Avolio-Drechsler require Markit Securities Finance at $150K–$500K/yr). These should enter a dedicated sub-review.

## 2. Search log

**Tier 1 journals screened**: *Journal of Finance* (JF), *Journal of Financial Economics* (JFE), *Review of Financial Studies* (RFS). **Tier 2**: *JFQA*, *Review of Asset Pricing Studies* (RAPS), *Review of Accounting Studies* (RoAS), *Management Science* (MS), *Accounting Review* (AR), *Journal of Accounting Research* (JAR), *FAJ*, *JPM*, *Critical Finance Review* (CFR). **Working papers**: NBER, SSRN in JEL G11/G12/G14/G17/M41. Replication benchmarks: **Jensen-Kelly-Pedersen (2023, JF 78(5):2465–2518)**, **Hou-Xue-Zhang (2020, RFS 33(5):2019–2133)**, **McLean-Pontiff (2016, JF 71(1):5–32)**, **Chen-Zimmermann (2022, CFR 27)**.

**Keyword sets used**: "cross-section of expected stock returns"; "gross profitability premium"; "quality minus junk"; "betting against beta low volatility"; "empirical asset pricing machine learning"; "IPCA characteristics covariances"; "10-K textual analysis sentiment Lazy Prices"; "short interest lending fee utilization"; "Form 4 opportunistic routine insider"; "accruals earnings quality"; "inflation beta climate beta cross section"; "alternative data satellite parking".

**PRISMA-style flow**: Identified through primary citations and seed list: 27 candidate signals. Duplicates with V010/V026 removed: 0 (V010 is analyst revisions; none of the seeds duplicate). Screened on inclusion criteria 1–2 (ranked journal + independent replication): 27 → 22 (five dropped: Tetlock 2007 index-level not cross-sectional; Katona et al. narrow universe of 44 retailers with no scaled strategy; Froot-Kang-Ozik-Sadka narrow consumer-sector scope with limited OOS; Boehme-Danielsen-Sorescu no standalone long-short alpha; pure LM dictionary not independently tradeable standalone). Screened on exclusion criteria (IS/OOS decay > 60%, proprietary data, country-specific): 22 → 13. Final Step-5 ranking with mandatory-slot, paradigm-diversification and orthogonality weights: 13 → **6 registered candidates**.

### Seed Disposition Table

| Seed | Status | Reason |
|---|---|---|
| Fama-French (2015) FF5 | PARTIAL — used as benchmark not standalone registered signal | FF5's RMW/CMA are absorbed by QMJ and by Daniel-Titman net issuance; direct replication of FF5 adds little beyond those. |
| Hou-Xue-Zhang (2015) Q-factor | PARTIAL — benchmark | ROE and I/A legs are captured by QMJ profitability + Daniel-Titman investment; avoiding redundancy. |
| Novy-Marx (2013) GP/A | PARTIAL — included inside QMJ composite and HML-Devil overlay | Standalone gross profitability survives JKP 2023 (profitability cluster) and HXZ 2020 (Gpa t=2.62), but QMJ dominates on orthogonality and risk-adjusted Sharpe. |
| **Asness-Frazzini-Pedersen (2019) QMJ** | **INCLUDED (V029)** | Mandatory Quality slot; survives JKP 2023 quality cluster; global replication; AQR data library public. |
| **Frazzini-Pedersen (2014) BAB** | **INCLUDED (V030)** | Mandatory Defensive slot; US Sharpe 0.78 1926–2012 published; JKP 2023 explicitly defends BAB against HXZ 2020 on CAPM-alpha grounds; global (20 markets). Flag Novy-Marx-Velikov (2022 JFE) construction critique. |
| **Asness-Frazzini (2013) HML-Devil** | **INCLUDED as overlay on Value (V031)** | Mandatory Value slot; monthly-updated book-to-price dominates Fama-French annual HML by ~300–500 bps/yr; paired with cash-based profitability screen to address value-trap. |
| Piotroski (2000) F-score | PARTIAL — overlapping with QMJ quality dimension | F-score alpha concentrates within high-B/M; would double-count with HML-Devil × profitability overlay. |
| Sloan (1996) accruals | PARTIAL — overlapping with QMJ earnings-quality | Accruals anomaly replicates in JKP 2023 accruals cluster but is subsumed by QMJ earnings-quality leg. |
| Bali-Cakici-Whitelaw (2011) MAX | EXCLUDED — high correlation with IVOL/BAB | Lottery/MAX is mechanically co-monotone with idiosyncratic vol and low-beta; redundant with BAB in the recommended set. |
| Ang-Hodrick-Xing-Zhang (2006) IVOL | EXCLUDED — same slot as BAB, sign ambiguity | IVOL anomaly (high IVOL → low returns) is contested in HXZ 2020; BAB carries the defensive slot more cleanly. |
| Conrad-Dittmar-Ghysels (2013) RN-skew | EXCLUDED — sign reversal in Stilger-Kostakis-Poon (2017 MS) | Option-implied skew literature is internally inconsistent; OptionMetrics cost high without clear sign. |
| Cremers-Weinbaum (2010) IV-spread | EXCLUDED at this grade — post-2008 decay, OptionMetrics gating | Option-implied cross-section remains NO_QUALIFYING_CANDIDATE at Grade A/B until sub-review. |
| Gu-Kelly-Xiu (2020) ML | PARTIAL — flagged for dedicated ML deep-dive | Published NN3 value-weighted decile Sharpe 1.35 (not 2.4–2.6 as sometimes misquoted; 2.45 is the equal-weighted figure). Infrastructure and re-training burden mandates a separate sub-review. |
| Kelly-Pruitt-Su (2019) IPCA | PARTIAL — same dedicated sub-review | K=5 IPCA predictive R² ≈ 0.6%/month OOS; input characteristics overlap heavily with registered candidates (QMJ, issuance). |
| Chen-Pelger-Zhu (2023) Deep SDF | PARTIAL — same dedicated sub-review | GAN-SDF OOS Sharpe ≈ 2.6, but signal is SDF not a single long-short portfolio. |
| Loughran-McDonald (2011) LM dictionary | EXCLUDED standalone — dictionary input, not tradeable | LM is the input to Lazy Prices / Jegadeesh-Wu composites; not a standalone long-short. |
| Tetlock (2007) | EXCLUDED — index-level not cross-sectional | Uses WSJ "Abreast of the Market" to predict DJIA; out of scope. |
| **Cohen-Malloy-Nguyen (2020) Lazy Prices** | **INCLUDED (V034)** | Mandatory Modern-paradigm/NLP slot; 5-factor alpha up to 188 bps/month on similarity-based long-short; EDGAR-only data; replicable. |
| Froot-Kang-Ozik-Sadka (2017) card | EXCLUDED — narrow universe, limited OOS | Consumer-sector only; event-study framing; requires geolocation vendor. |
| Katona et al. (2024 JFQA) satellite | EXCLUDED — 44 retailers, capacity-bound | Narrow universe prevents decile sorts on S&P 500/R1000. |
| Boehme-Danielsen-Sorescu (2006) | EXCLUDED — no standalone long-short alpha | Double-sort framework, not a ranked signal. |
| Cohen-Diether-Malloy (2007) shorting demand | EXCLUDED at this grade — Markit/DataLend cost | Promising (–2.98%/mo abnormal return) but $150K–$500K/yr vendor; defer to sub-review. |
| D'Avolio (2002) / Drechsler-Drechsler (2014) CME | EXCLUDED at this grade — same stock-loan vendor gating | |
| **Daniel-Titman (2006) composite issuance** | **INCLUDED (V031b)** | Survives JKP 2023 investment cluster and HXZ 2020; free data (CRSP + Compustat); orthogonal to QMJ/BAB. |
| Ikenberry-Lakonishok-Vermaelen (1995) buybacks | PARTIAL — captured in net-payout leg of Daniel-Titman | BHAR methodology debated (Fama 1998); calendar-time alpha from Peyer-Vermaelen 2009 ~3–4%/yr is already reflected in net-issuance. |
| **Cohen-Malloy-Pomorski (2012) opportunistic insider** | **INCLUDED (V033)** | Form 4 opportunistic-vs-routine VW alpha 82 bps/mo t=2.15; free EDGAR data. |
| Boons-Duarte-de Roon-Szymanowska (2020) inflation-beta | EXCLUDED — conditional sign flip full-sample insignificant | Pre- vs post-2000 sign reversal makes unconditional long-short Sharpe unreliable. |
| Bolton-Kacperczyk (2021) carbon | EXCLUDED — active replication dispute | Aswani-Raghunandan-Rajgopal (2024 RoF) and Zhang (2023) show fragility to disclosed-vs-estimated emissions and timing; sign unstable. |

## 3. Ranked candidate table

### V029 — Quality Minus Junk (QMJ) — RANK 1

**Signal type**: CROSS_SECTIONAL. **Factor name**: Quality Minus Junk (profitability + growth + safety + payout composite). **Primary citation**: Asness, Frazzini, Pedersen (2019), "Quality Minus Junk," *Review of Accounting Studies* 24(1):34–112, doi:10.1007/s11142-018-9470-2. **Replication citations**: Jensen-Kelly-Pedersen 2023 JF (quality cluster, survivor); Hou-Xue-Zhang 2020 RFS (cash-based operating profitability Cop replicates t=2.62); Chen-Zimmermann 2022 CFR (reproduction); AQR Data Library (live monthly series, US + 24 international markets). **Universe**: CRSP common stocks (shrcd 10/11), or S&P 500 / Russell 1000 for deployment. **Portfolio construction**: within-size-group ranks on z-scored composite of profitability (GP/A, ROE, CFO/A, GMAR, low accruals), growth (5yr ∆ profitability), safety (low beta, low idio-vol, low leverage, low bankruptcy score), payout (net equity + debt payout); value-weight long-top-decile minus short-bottom-decile monthly rebalance. **Target gap filled**: Quality (gap 2). **Mechanism**: high-quality firms should trade at premium P/B; when they don't, they earn positive risk-adjusted return; rooted in Gordon-growth decomposition. **Data requirements**: Compustat (fundamentals), CRSP (returns), no I/B/E/S required for composite. **Infrastructure required**: SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED. **Effect size in-sample**: US QMJ monthly return ≈ 0.61%, Sharpe ≈ 0.77, FF3 alpha ≈ 0.56% t ≈ 7–8 (AFP 2019, Tables 5–6); global (24 markets) Sharpe ≈ 1.14. **OOS**: AQR live QMJ series 1990–2025 preserves positive Sharpe ~0.5 after 2010 (Sharpe decay ≈ 35–40%, below 60% threshold). **Real-time implementability**: monthly, quarterly-data PIT-lagged four months per JKP protocol. **Executability check**: on S&P 500 at today's close, long-top-decile ≈ 50 names biased toward mega-cap profitable stable non-leveraged (tech leaders, large health-care, staples), short-bottom-decile ≈ 50 names biased toward low-profitability high-leverage small-cap (distressed biotech, high-growth-unprofitable, over-levered cyclicals). **Correlation with V026**: low (AFP 2019 Table 7: QMJ-residual-momentum ≈ 0.1–0.2). **Correlation with V010**: low, QMJ is stock-level fundamentals not analyst-revisions. **Intra-shortlist correlations**: QMJ-BAB ≈ 0.55–0.60 (flag); QMJ-issuance ≈ 0.3; QMJ-Lazy-Prices ≈ 0.05. **Capacity**: high (mega-cap). **Recommended grade**: B+ (Grade A withheld only because QMJ as a composite was not part of HXZ 2020's 452-factor list verbatim, though each constituent was). **Group**: **S** (Sentiment/Positioning — quality is a structural investor preference). **Paradigm**: Classical risk-premium + partial Behavioral (safety demand). **Confidence**: HIGH. **Why it fills a gap**: single-name quality is currently absent; AFP 2019 demonstrates OOS in 24 countries. **Risk of adoption**: crowding; quality has drawn trillions in smart-beta AUM; decay risk is real. **Infrastructure cost**: LOW ($25K–$75K WRDS). **Timeline**: IMMEDIATE — AQR monthly QMJ series can be used for paper-trade within 2 weeks; in-house replication 4 weeks.

### V030 — Betting Against Beta (BAB) — RANK 2

**Signal type**: CROSS_SECTIONAL. **Primary citation**: Frazzini, Pedersen (2014), "Betting Against Beta," *JFE* 111(1):1–25, doi:10.1016/j.jfineco.2013.10.005. **Replication**: Jensen-Kelly-Pedersen 2023 JF ("failure to replicate in Hou-Xue-Zhang 2020 actually supports BAB theory" — CAPM-alpha replication 82.4%; BAB is a flagship survivor of the Bayesian replication); global in 19 MSCI markets per original paper; AQR BAB live series; critique by Novy-Marx-Velikov (2022 JFE). **Universe**: CRSP common stocks; practical deployment S&P 500 or Russell 1000 to avoid micro-cap dependency Novy-Marx-Velikov flag. **Portfolio construction**: estimate ex-ante beta per Frazzini-Pedersen (shrinkage of Dimson-adjusted one-year daily + five-year monthly vol); rank stocks by beta; go long low-beta leveraged to β=1, short high-beta de-leveraged to β=1; rebalance monthly. **Target gap filled**: Defensive/BAB/Low-vol (gap 3). **Mechanism**: leverage-constrained investors tilt to high-beta stocks → flat security market line → BAB captures the premium. **Data**: CRSP daily returns only. **Infrastructure**: SINGLE_NAME_UNIVERSE only. **Effect size in-sample**: US Sharpe 0.78 (1926–March 2012); all-BAB aggregate 0.77%/mo t=8.8; survives FF3, Carhart, FF5 + liquidity controls. **OOS**: 2012–2024 US BAB Sharpe has compressed to ~0.3–0.5 per Barroso-Santa-Clara (2018) and AQR updates (Sharpe decay ≈ 40–55%, at the edge of 60% threshold; flag). **Sharpe decay**: flagged borderline. **Real-time implementability**: monthly. **Executability check**: on S&P 500 today, long-top-decile ≈ 50 low-beta names (utilities, staples, health-care-pharma, some regulated financials) levered ~1.5–2x to β=1, short-bottom-decile ≈ 50 high-beta names (high-beta tech, regional banks, cyclicals, levered small-growth) de-levered. **Correlation with V026**: low 0.1–0.2 (residual momentum is price-based residual; BAB is level-beta). **Correlation with V010**: low. **Intra-shortlist**: BAB-QMJ 0.55–0.60 (flag). **Capacity**: medium — Novy-Marx-Velikov show Frazzini-Pedersen rank-weighting implicitly over-weights micro-caps; use value-weighted Novy-Marx-Velikov variant (SR 0.49 net of costs) for deployment. **Grade**: B+ with construction flag. **Group**: **R** (Regime/Risk — low-beta is regime-sensitive; performs in bear regimes and underperforms when funding constraints ease). **Paradigm**: Classical risk-premium + Behavioral/limits-of-arbitrage. **Confidence**: HIGH on existence, MEDIUM on magnitude post-2015. **Risk**: construction-sensitive; NMV 2022 critique; crowded. **Cost**: LOW. **Timeline**: IMMEDIATE.

### V031 — Composite equity issuance / net payout (Daniel-Titman) — RANK 3

**Signal type**: CROSS_SECTIONAL. **Primary citation**: Daniel, Titman (2006), "Market Reactions to Tangible and Intangible Information," *JF* 61(4):1605–1643, doi:10.1111/j.1540-6261.2006.00884.x. **Replication**: JKP 2023 investment/debt-issuance clusters (robust across 93 countries); HXZ 2020 — composite issuance is one of a handful surviving NYSE-breakpoint VW protocol; Chen-Zimmermann 2022 reproduces; Pontiff-Woodgate (2008 JF) and McLean-Pontiff-Watanabe (2009 JFE) international. **Universe**: CRSP common stocks. **Portfolio construction**: for each stock at month t, compute 5-year log change in market equity minus log 5-year return-without-dividends (≡ log increase in shares); decile-sort; long low-issuance (or net-repurchasers) minus short high-issuance; value-weight; rebalance monthly with annual characteristic update. **Target gap filled**: Issuance/Buyback (gap 6); also fills part of Investment (gap 2 adjacent). **Mechanism**: managers time issuance (Stein 1996; Baker-Wurgler 2002); issuance ≈ overvaluation signal; buyback ≈ undervaluation signal. **Data**: CRSP + Compustat. **Infrastructure**: SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED. **Effect size in-sample**: Fama-MacBeth t ≈ –5 to –7 on 5yr composite issuance; quintile spread ≈ 6–8%/yr after B/M and past-return controls; JKP 2023 eqnpo_12m in tangency portfolio with positive weight. **OOS**: international replication in McLean-Pontiff-Watanabe 2009; McLean-Pontiff 2016 post-publication decay for issuance-family is near the 58% average but factor remains significant. **Sharpe decay**: near-average ~40%; not flagged. **Real-time implementability**: monthly. **Executability check**: on R1000 today, long-decile ≈ 100 net-repurchasers with shrinking share count (recent examples cluster in mature tech, consumer staples, energy majors), short-decile ≈ 100 high-dilution names (recent IPO/SPAC survivors, biotech cash-burners, growth-tech with heavy stock-based comp). **Correlation with V026**: moderate ≈ 0.2–0.3; issuance captures distinct "intangible return" component. **Correlation with V010**: low. **Intra-shortlist**: issuance-QMJ 0.3; issuance-HML-Devil 0.35 (flag as positive — repurchasers tilt value). **Capacity**: high. **Grade**: **A** — one of the cleanest surviving factors across all four replication papers. **Group**: **S**. **Paradigm**: Classical risk-premium / Behavioral. **Confidence**: HIGH. **Cost**: LOW. **Timeline**: IMMEDIATE.

### V032 — HML-Devil with cash-profitability overlay — RANK 4

**Signal type**: CROSS_SECTIONAL. **Primary citation**: Asness, Frazzini (2013), "The Devil in HML's Details," *JoPM* 39(4):49–68, doi:10.3905/jpm.2013.39.4.049; overlay: Novy-Marx (2013) "The Other Side of Value: The Gross Profitability Premium," *JFE* 108(1):1–28; cash-based refinement Ball-Gerakos-Linnainmaa-Nikolaev (2016) *JFE*. **Replication**: JKP 2023 value cluster (survivor with positive tangency weight); HXZ 2020 BM replicates at VW+NYSE; AQR data library HML-Devil live; cop_at identified by JKP as "strongest factor in the factor zoo" (Hanauer-quoted GRS test). **Universe**: CRSP common stocks; deployed S&P 500 / R1000. **Portfolio construction**: compute book-to-price (B/P) using **most recent quarterly book equity with ≥ four-month PIT lag** and **current-month price** (the HML-Devil update — Fama-French's original HML uses a stale June-lagged price); overlay profitability screen — within top-two B/P quintiles, keep only stocks in top two cash-based operating profitability (Cop) quintiles; symmetric short leg (low B/P × low Cop). Value-weighted decile long-short, monthly rebalance on price (value leg moves monthly), quarterly rebalance on Cop (when earnings reported). **Target gap filled**: Value (gap 1). **Mechanism**: value premium as risk premium plus behavioral extrapolation error; profitability overlay eliminates "value trap" (firms cheap for good reason). **Data**: Compustat + CRSP. **Infrastructure**: SINGLE_NAME_UNIVERSE + FUNDAMENTALS_FEED. **Effect size in-sample**: HML-Devil US 1950–2012 monthly 0.46% vs FF-HML 0.32%; annual alpha vs HML ≈ 3–5%/yr (Asness-Frazzini 2013 Table 3); profitability overlay adds ~2–3%/yr per Novy-Marx (2013). **OOS**: JKP 2023 global value cluster preserves positive CAPM alpha; US value has struggled 2017–2020 then recovered 2021–2023. **Sharpe decay**: value has experienced large post-publication drag; flagged as borderline, but profitability overlay materially restores post-2015 Sharpe per AQR 2022 review. **Real-time implementability**: monthly. **Executability check**: today on R1000, long-decile ≈ 100 names of cheap + profitable (mature banks/insurers, integrated energy, selected consumer-discretionary, Japanese/European dual-listings in global version), short-decile ≈ 100 expensive + low-profit (high-multiple growth without earnings, unprofitable biotechs, high-multiple SaaS without cash conversion). **Correlation with V026**: low 0.1–0.2. **V010**: low. **Intra-shortlist**: HML-Devil-Daniel-Titman 0.35 (flag moderate positive); HML-Devil-QMJ ≈ 0.2 after profitability overlay (without overlay it would be negative). **Capacity**: high. **Grade**: B (profitability-overlay variant has less published OOS than pure HML-Devil alone). **Group**: **S**. **Paradigm**: Classical risk-premium + Behavioral. **Confidence**: MEDIUM-HIGH. **Cost**: LOW. **Timeline**: IMMEDIATE.

### V033 — Opportunistic-insider signal (Form 4) — RANK 5

**Signal type**: CROSS_SECTIONAL. **Primary citation**: Cohen, Malloy, Pomorski (2012), "Decoding Inside Information," *JF* 67(3):1009–1043, doi:10.1111/j.1540-6261.2012.01740.x. **Replication**: JKP 2023 includes insider-trading-adjacent signal in their 153-factor set (cluster "Value" via net-payout) and insider-trading cluster tested in follow-ups; Ahern (2017); Cziraki-Lyandres-Michaely (2021 JFE) for additional support. **Universe**: CRSP common stocks. **Portfolio construction**: collect all Form 4 filings from EDGAR (2-business-day post-trade filing deadline); classify each insider as ROUTINE if they have filed a trade in the same calendar month for ≥ 3 consecutive years, else OPPORTUNISTIC; aggregate dollar-net insider purchases (buys – sells) by opportunistic insiders per firm over trailing 6 months, scaled by market cap; decile-sort; long top decile (heavy opportunistic buying), short bottom decile (heavy opportunistic selling); value-weighted, monthly rebalance with daily updating. **Target gap filled**: Insider/Institutional (gap 7). **Mechanism**: opportunistic insiders hold non-public information; their deviations from routine pattern are information-rich; routine trades (e.g., 10b5-1 plans) are not. **Data**: SEC EDGAR Form 4 (free) + Compustat/CRSP. **Infrastructure**: SINGLE_NAME_UNIVERSE + NLP_TEXT_FEED (lightweight — structured XML, not NLP proper). **Effect size in-sample**: VW alpha long-short = **0.82%/month** (t=2.15); EW = 1.80%/month (t=6.07); routine portfolio alpha insignificant (CMP 2012 Table III). **OOS**: 2008–2020 update in Akbas-Jiang-Koch (2020 MS) preserves ~50–60% of VW alpha (~40 bps/mo); modest decay below 60% threshold. **Real-time**: daily (Form 4 deadline is 2 business days). **Executability check**: today on R1000, long-decile ≈ 100 names where CEOs/CFOs/directors making non-routine purchases in past 6 months (typically after drawdowns; often small/mid-cap financials and energy in recent cohorts), short-decile ≈ 100 names with heavy non-routine insider selling (often recently-rallied tech, lockup-expiring recent-IPOs). **Correlation with V026**: low 0.1; correlated positively with short-leg of momentum in short sub-sample. **V010**: low-moderate 0.2 (opportunistic insider buys sometimes precede analyst revisions). **Intra-shortlist**: low with all other five. **Capacity**: medium (short-leg crowds with low-liquidity names). **Grade**: B, **MEDIUM confidence**. **Group**: **S**. **Paradigm**: Behavioral/limits-of-arbitrage + informational. **Risk**: regulatory (10b5-1 reforms 2022 tightened insider plan rules; may compress signal). **Cost**: LOW ($25K WRDS + developer time for EDGAR parser; free data). **Timeline**: NEAR (4–12 weeks — EDGAR Form 4 XML parser and routine/opportunistic classifier needs to be built and backtested).

### V034 — Lazy Prices 10-K similarity signal — RANK 6

**Signal type**: CROSS_SECTIONAL. **Primary citation**: Cohen, Malloy, Nguyen (2020), "Lazy Prices," *JF* 75(3):1371–1415, doi:10.1111/jofi.12885. **Replication**: Not in JKP 2023 (JKP excludes textual signals); independent replications on Alpha Architect, Sadlo (2020) thesis, Padmakumar-Mani (2022); extended by Brown-Tucker (2011) on 10-K similarity; Loughran-McDonald (2011 JF) provides dictionary foundation. **Universe**: all SEC-reporting common stocks; deployed R1000. **Portfolio construction**: download all 10-K and 10-Q filings from EDGAR; for each firm-filing, compute quarter-over-quarter (or year-over-year for 10-K) cosine similarity (or Jaccard) of the full text excluding boilerplate; decile-sort on *negative* of similarity (i.e., "changer" firms in lowest similarity decile); long high-similarity minus short low-similarity (non-changers minus changers); value-weight; monthly rebalance keyed to most recent filing timestamp per firm. **Target gap filled**: NLP/Text (gap 4 — modern paradigm). **Mechanism**: material textual changes in 10-K/10-Q signal hidden risk/negative news that market underreacts to; "lazy prices" because markets slow to process 200+ page filings. **Data**: SEC EDGAR (free) + CRSP. **Infrastructure**: SINGLE_NAME_UNIVERSE + NLP_TEXT_FEED. **Effect size in-sample**: 5-factor alpha up to **188 bps/month** (≈ 22%/yr annualized) on long-short (Cohen-Malloy-Nguyen 2020 Table IV); Jaccard main spec t ≈ 3.29–3.51 in high-litigiousness subsample; overall Sharpe ≈ 1.0–1.3. **OOS**: replication studies 2018–2023 preserve ~50–70% of alpha (decay ~30–50%, below threshold). **Sharpe decay**: moderate ~40%; not flagged. **Real-time**: monthly rebalance on most-recent-filing similarity; daily-updating EDGAR pipeline. **Executability check**: today on R1000, long-decile ≈ 100 "non-changer" firms whose latest 10-Q is >95% similar to prior (typically stable mature-industry names — staples, utilities, industrial-incumbents), short-decile ≈ 100 "changer" firms with materially rewritten filings (often names quietly introducing new risk-factors, changing revenue-recognition language, or altering MD&A narrative; historically includes pre-blow-up accounting frauds). **Correlation with V026**: low (<0.1 — pure textual, no price input). **V010**: low 0.1. **Intra-shortlist**: low with all (unique data source). **Capacity**: medium (signal concentrates in mid-cap). **Grade**: B, **MEDIUM confidence** (not in JKP 153; but independently replicated). **Group**: **S**. **Paradigm**: Modern NLP/text + Behavioral (investor inattention). **Risk**: LLM-era arbitrage — hedge funds now parse 10-Ks automatically; post-2020 alpha may decay faster. **Cost**: LOW-MEDIUM ($25K WRDS + $10K–$30K/yr developer/compute for filing-text pipeline and similarity computation; LM dictionary free). **Timeline**: NEAR (4–12 weeks — build EDGAR ingestion, tokenization, similarity matrix).

## 4. Gap coverage matrix (8 × 6)

| Target gap | V029 QMJ | V030 BAB | V031 Issuance | V032 HML-Devil+Cop | V033 Insider | V034 Lazy Prices |
|---|---|---|---|---|---|---|
| 1. Value | — | — | partial | **YES** | — | — |
| 2. Quality | **YES** | partial (safety) | — | overlay only | — | — |
| 3. Defensive/BAB | partial (safety leg) | **YES** | — | — | — | — |
| 4. Modern ML/NLP/Alt | — | — | — | — | partial (XML parsing) | **YES** |
| 5. Option-implied | — | — | — | — | — | — |
| 6. Short-interest/Issuance | — | — | **YES** | — | — | — |
| 7. Insider/Institutional | — | — | — | — | **YES** | — |
| 8. Macro-linked cross-section | — | — | — | — | — | — |

**Gaps covered**: 6 of 8 (Value, Quality, Defensive, Modern NLP, Issuance, Insider). **Uncovered gaps flagged**: Option-implied cross-section (gap 5) and Macro-linked cross-section (gap 8) — both **NO_QUALIFYING_CANDIDATE**, see Section 11.

## 5. Paradigm diversification check

The six candidates span four of five paradigms: **Classical risk-premium** (V029 QMJ, V030 BAB, V031 issuance, V032 HML-Devil) ✓; **Behavioral / limits-of-arbitrage** (V030 BAB via leverage constraints, V033 insider, V034 Lazy Prices via inattention) ✓; **ML / NLP / Alt-data** (V034 Lazy Prices via textual similarity; partial on V033 via EDGAR XML) ✓; **Option-implied** (none) — not met; **Structural-nowcasting** (none) — not met. **PARADIGM_MIN = 3_OF_5 SATISFIED (4 of 5 present).**

## 6. Mandatory-slot check

| Mandatory slot | Filled by | Status |
|---|---|---|
| Value | V032 HML-Devil + cash-profitability overlay | ✓ |
| Quality | V029 QMJ | ✓ |
| Defensive/BAB | V030 BAB | ✓ |
| Modern-paradigm ML/NLP/Alt-data | V034 Lazy Prices | ✓ |

All four mandatory slots filled. TARGET_GAP_MIN = 4_OF_8 **satisfied** (six gaps covered).

## 7. Correlation / orthogonality analysis

Published and inferred correlations of the six signals with the existing framework's single-name exposures:

| Pair | ρ | Flag |
|---|---|---|
| QMJ ↔ V026 residual momentum | 0.10–0.20 | ok |
| BAB ↔ V026 | 0.10–0.20 | ok |
| Issuance ↔ V026 | 0.20–0.30 | ok |
| HML-Devil ↔ V026 | 0.10–0.20 | ok |
| Insider ↔ V026 | 0.10 | ok |
| Lazy Prices ↔ V026 | <0.10 | ok |
| Any ↔ V010 earnings-revision breadth | 0.10–0.25 across all | ok |
| **QMJ ↔ BAB** | **0.55–0.60** | **flag — both load on safety/low-beta** |
| HML-Devil ↔ Issuance | 0.30–0.35 | borderline, not flagged |
| All others intra-shortlist | <0.3 | ok |

**Only the QMJ–BAB pair exceeds the |0.5| threshold.** Mitigation: both have been shown to carry independent alphas in multi-factor regressions (AFP 2019 Table 10: QMJ alpha ≈ 3–5%/yr after controlling for BAB). Recommend sizing QMJ and BAB jointly with a correlation-aware risk-parity overlay rather than naive equal weight. Published global evidence (AFP 2019, Frazzini-Pedersen 2014) confirms incremental information in each.

## 8. Replication-audit summary

| Candidate | Replicator | Year | OOS window | Sharpe preserved | JKP 2023 status | Caveats |
|---|---|---|---|---|---|---|
| V029 QMJ | JKP 2023; AFP 2019 (24 countries) | 2019–2023 | 1990–2025 live | ~60–65% (Sharpe 0.77 IS → ~0.5 post-2010) | **SURVIVOR — quality cluster in tangency portfolio** | composite signal; constituents tested separately |
| V030 BAB | JKP 2023; Barroso-Santa-Clara 2018; Novy-Marx-Velikov 2022 | 2014–2024 | 2012–2024 | ~45–55%; NMV value-weighted variant SR 0.49 net | **SURVIVOR on CAPM alpha** (JKP: "HXZ 'failure' supports BAB theory") | construction-sensitive; NMV show micro-cap dependence |
| V031 Issuance | JKP 2023; HXZ 2020; Chen-Zimmermann 2022; MPW 2009 (intl) | 2009–2023 | 2006–2024 | ~55–65% | **SURVIVOR — investment + debt issuance clusters** | robust, crosses all four replication benchmarks |
| V032 HML-Devil + Cop | JKP 2023 value cluster; HXZ 2020 BM; Novy-Marx 2013; Ball et al. 2016 | 2013–2023 | 2013–2024 | ~40–60% (value struggled 2017–2020, recovered 2021–2023) | **SURVIVOR — value cluster** (Cop_at noted as strongest single factor in JKP follow-up) | value drawdowns; overlay is less-tested variant |
| V033 Insider | Akbas-Jiang-Koch 2020; Cziraki et al. 2021 | 2007–2020 | 2008–2022 | ~50–60% | Not directly tested as CMP-classification factor; insider-trading cluster adjacent | 10b5-1 reforms 2022; classifier implementation choices |
| V034 Lazy Prices | Alpha Architect 2020; Padmakumar-Mani 2022; Sadlo 2020 | 2018–2023 | 2014–2023 | ~50–70% | **NOT-TESTED** (JKP excludes textual) | not a JKP survivor by default; rely on independent textual replications |

McLean-Pontiff (2016) JF benchmark post-publication decay: average 58%; our six candidates' estimated decay ranges 35–60%, with BAB near the upper bound. Chen-Zimmermann (2022) reproduce ~90% of clear predictors when categorized correctly; HXZ 2020's 65% failure rate is primarily driven by micro-cap-dependent and trading-friction factors (96% of trading-friction anomalies fail) — our recommended six avoid that category.

## 9. Infrastructure and data summary

| Candidate | Vendor feed | PIT caveats | Annual cost | Rebalance freq |
|---|---|---|---|---|
| V029 QMJ | WRDS (CRSP + Compustat); optional AQR Data Library for cross-check | four-month accounting lag (JKP protocol) | $25K–$50K | monthly |
| V030 BAB | CRSP daily only | none (price-only); use shrinkage beta | $15K–$25K | monthly |
| V031 Issuance | CRSP + Compustat | four-month lag | $25K–$50K | monthly |
| V032 HML-Devil + Cop | CRSP + Compustat quarterly | four-month lag on book and Cop; same-month price | $25K–$50K | monthly |
| V033 Insider | SEC EDGAR (free) + CRSP | Form 4 filed within 2 business days of trade | $15K–$35K (dev cost) | daily signal, monthly rebalance |
| V034 Lazy Prices | SEC EDGAR (free) + CRSP | 10-Q/10-K filing dates | $15K–$50K (dev + compute for text similarity) | monthly on latest filing |

**Aggregate annual infrastructure cost for all six**: approximately **$30K–$100K/yr** (mainly a single WRDS subscription covers most, plus developer time for EDGAR pipelines shared between V033 and V034). This is LOW-MEDIUM range. No option-chain feed, no stock-loan feed, no alt-data vendor required for the top six.

## 10. Registration recommendations

| ID | Factor | Grade | Group | OOS tracking period | Paper-trade universe |
|---|---|---|---|---|---|
| V029 | QMJ composite | B+ | S | 24 months | S&P 500 (value-weighted, decile long-short) |
| V030 | BAB (Novy-Marx-Velikov value-weighted variant) | B+ | R | 24 months | Russell 1000 |
| V031 | Composite equity issuance / net payout | A | S | 18 months | Russell 1000 |
| V032 | HML-Devil × Cop overlay | B | S | 24 months | Russell 1000 |
| V033 | Opportunistic-insider Form 4 signal | B | S | 18–24 months | Russell 1000 (avoid micro-cap) |
| V034 | Lazy Prices 10-K similarity | B | S | 24 months (longer given uncertain LLM-era decay) | Russell 1000 |

All six registered in group **S (Sentiment/Positioning)** except V030 BAB, which belongs in **R (Regime/Risk)** given its explicit leverage-constraint regime dependence (funding stress regimes invert BAB). None required as Overlay. None as T (Tactical Timing), since all are slow-moving cross-sectional ranks, not timing signals.

## 11. Gaps still unfilled

**Gap 5 — Option-implied cross-section: NO_QUALIFYING_CANDIDATE at Grade A/B.** Cremers-Weinbaum (2010) IV-spread was the strongest candidate (~50 bps/week IS; FFC alpha significant 1996–2005) but (a) post-2008 material decay in multiple follow-ups, (b) not in JKP 153, (c) requires OptionMetrics IvyDB at $30K–$50K WRDS add-on. Conrad-Dittmar-Ghysels (2013) RN-skew has sign reversal (Stilger-Kostakis-Poon 2017 MS find opposite sign). Bali-Cakici-Whitelaw MAX is collinear with BAB/IVOL. **Recommendation**: warrant dedicated sub-review.

**Gap 8 — Macro-linked cross-section: NO_QUALIFYING_CANDIDATE at Grade A/B.** Boons-Duarte-de Roon-Szymanowska (2020) inflation-beta has conditional sign flip around 2000 making unconditional long-short insignificant full-sample. Bolton-Kacperczyk (2021) carbon-beta is in active replication dispute (Aswani-Raghunandan-Rajgopal 2024 RoF; Zhang 2023) with sensitivity to disclosed-vs-Trucost-estimated emissions. Hsu-Li-Tsou (2023 JF) pollution premium is promising (~4.4%/yr t≈3) but single published study. **Recommendation**: monitor; defer to dedicated ESG/climate-beta sub-review when two-sided replication literature matures.

**Gap 3 — stock-loan sub-cell unfilled by budget, not by evidence.** Cohen-Diether-Malloy (2007) and Drechsler-Drechsler (2014) show powerful stock-lending-fee signals (–2.98%/mo abnormal return for demand-outward shifts; CME factor 4-factor alpha 1.53%/mo) but require Markit Securities Finance or DataLend at $150K–$500K/yr, outside the framework's LOW-MEDIUM budget. **Recommendation**: add to infrastructure-expansion wishlist.

**ML/alt-data narrow deep-dive not done here.** GKX 2020, KPS 2019 IPCA, Chen-Pelger-Zhu 2023 GAN-SDF require dedicated ML asset-pricing sub-review with compute infrastructure plan (monthly re-estimation; NN3 value-weighted Sharpe 1.35 in GKX not 2.4–2.6 as sometimes misquoted). Lazy Prices V034 is the lightweight NLP representative; full ML sub-review should follow.

## 12. Suggested next steps

**Enter OOS paper-trade ledger 4–12 weeks**: V029 QMJ, V030 BAB (Novy-Marx-Velikov VW variant), V031 Composite issuance, V032 HML-Devil × Cop — all **IMMEDIATE (≤4 weeks)** given WRDS + AQR Data Library already cover the inputs; develop monthly rebalance logic; target universe Russell 1000 value-weighted decile long-short; track vs FF5+UMD benchmark.

**Require additional evidence / near-term build**: V033 opportunistic-insider (4–12 weeks build — EDGAR Form 4 XML parser, routine/opportunistic classifier, point-in-time backtester; monitor post-2022 10b5-1 reform impact); V034 Lazy Prices (4–12 weeks — EDGAR text ingestion, cosine/Jaccard similarity pipeline, LM dictionary overlay; register longer 24-month OOS ledger given LLM-era decay risk).

**Dedicated sub-reviews warranted**:
1. **Option-implied cross-section sub-review** — to resolve sign ambiguity in RN-skew, post-2008 decay in Cremers-Weinbaum IV-spread, and to evaluate MAX/IVOL jointly with BAB. Budget implication: $30K–$50K/yr OptionMetrics via WRDS.
2. **ML asset-pricing deep-dive** — covering GKX 2020 (NN3/NN4 published VW Sharpe 1.35), KPS 2019 IPCA K=5 predictive R² 0.6%/mo, Chen-Pelger-Zhu 2023 GAN-SDF; should evaluate compute cost (annual re-training, monthly inference) and the out-of-sample performance preservation evidence accumulated since publication.
3. **Stock-loan / short-fee sub-review** — contingent on budget approval for Markit Securities Finance or DataLend ($150K–$500K/yr); then Cohen-Diether-Malloy and Drechsler-Drechsler become registerable at Grade A.
4. **ESG / climate-beta replication watching brief** — track Aswani et al. vs Bolton-Kacperczyk debate; register only after two-sided evidence converges.

**Infrastructure build requirements**: (a) EDGAR full-text ingestion pipeline (shared V033 + V034; est. 6–8 engineering weeks); (b) point-in-time fundamentals join layer on Compustat (shared V029 + V031 + V032); (c) monthly rebalancing orchestration with value-weighted decile long-short logic on Russell 1000 universe; (d) reporting harness tracking realized decile Sharpe vs published decile Sharpe per candidate at monthly cadence into the OOS ledger.

**Bottom line**: the six recommended candidates (V029–V034) take the framework from two single-name cross-sectional variables (V010 + V026) to eight, close six of eight target gaps, span four of five methodology paradigms, satisfy all four mandatory slots, and require only LOW-MEDIUM infrastructure (<$100K/yr) with IMMEDIATE-to-NEAR deployment timelines. The remaining two gaps (option-implied cross-section, macro-linked betas) are explicitly flagged NO_QUALIFYING_CANDIDATE pending dedicated sub-reviews and, in the option case, budget approval for OptionMetrics.

---

**References (full list)**

Ahern, K. (2017). "Information networks: Evidence from illegal insider trading tips." *JFE* 125(1):26–47.
Akbas, F., Jiang, C., Koch, P. (2020). "Insider investment horizon." *Management Science* 66(10):4551–4572.
Ang, A., Hodrick, R., Xing, Y., Zhang, X. (2006). "The cross-section of volatility and expected returns." *JF* 61(1):259–299.
Asness, C., Frazzini, A. (2013). "The devil in HML's details." *JoPM* 39(4):49–68.
Asness, C., Frazzini, A., Pedersen, L. H. (2019). "Quality minus junk." *Review of Accounting Studies* 24(1):34–112.
Aswani, J., Raghunandan, A., Rajgopal, S. (2024). "Are carbon emissions associated with stock returns?" *Review of Finance*.
Bali, T., Cakici, N., Whitelaw, R. (2011). "Maxing out: Stocks as lotteries and the cross-section of expected returns." *JFE* 99(2):427–446.
Ball, R., Gerakos, J., Linnainmaa, J., Nikolaev, V. (2016). "Accruals, cash flows, and operating profitability in the cross section of stock returns." *JFE* 121(1):28–45.
Barroso, P., Santa-Clara, P. (2018). "Managing the risk of the betting-against-beta anomaly." Working paper.
Boehme, R., Danielsen, B., Sorescu, S. (2006). "Short-sale constraints, differences of opinion, and overvaluation." *JFQA* 41(2):455–487.
Bolton, P., Kacperczyk, M. (2021). "Do investors care about carbon risk?" *JFE* 142(2):517–549.
Boons, M., Duarte, F., de Roon, F., Szymanowska, M. (2020). "Time-varying inflation risk and stock returns." *JFE* 136(2):444–470.
Chen, A., Zimmermann, T. (2022). "Open source cross-sectional asset pricing." *Critical Finance Review* 27(2):207–264.
Chen, L., Pelger, M., Zhu, J. (2024). "Deep learning in asset pricing." *Management Science* 70(2):714–750.
Cohen, L., Diether, K., Malloy, C. (2007). "Supply and demand shifts in the shorting market." *JF* 62(5):2061–2096.
Cohen, L., Malloy, C., Nguyen, Q. (2020). "Lazy prices." *JF* 75(3):1371–1415.
Cohen, L., Malloy, C., Pomorski, L. (2012). "Decoding inside information." *JF* 67(3):1009–1043.
Conrad, J., Dittmar, R., Ghysels, E. (2013). "Ex ante skewness and expected stock returns." *JF* 68(1):85–124.
Cremers, M., Weinbaum, D. (2010). "Deviations from put-call parity and stock return predictability." *JFQA* 45(2):335–367.
Daniel, K., Titman, S. (2006). "Market reactions to tangible and intangible information." *JF* 61(4):1605–1643.
D'Avolio, G. (2002). "The market for borrowing stock." *JFE* 66(2-3):271–306.
Drechsler, I., Drechsler, Q. (2018). "The shorting premium and asset pricing anomalies." NBER w20282.
Engle, R., Giglio, S., Kelly, B., Lee, H., Stroebel, J. (2020). "Hedging climate change news." *RFS* 33(3):1184–1216.
Fama, E., French, K. (2015). "A five-factor asset pricing model." *JFE* 116(1):1–22.
Frazzini, A., Pedersen, L. H. (2014). "Betting against beta." *JFE* 111(1):1–25.
Froot, K., Kang, N., Ozik, G., Sadka, R. (2017). "What do measures of real-time corporate sales say about earnings surprises?" *JFE* 125(1):143–162.
Gu, S., Kelly, B., Xiu, D. (2020). "Empirical asset pricing via machine learning." *RFS* 33(5):2223–2273.
Hou, K., Xue, C., Zhang, L. (2015). "Digesting anomalies: An investment approach." *RFS* 28(3):650–705.
Hou, K., Xue, C., Zhang, L. (2020). "Replicating anomalies." *RFS* 33(5):2019–2133.
Hsu, P.-H., Li, K., Tsou, C.-Y. (2023). "The pollution premium." *JF* 78(3):1343–1392.
Ikenberry, D., Lakonishok, J., Vermaelen, T. (1995). "Market underreaction to open market share repurchases." *JFE* 39(2–3):181–208.
Jensen, T. I., Kelly, B., Pedersen, L. H. (2023). "Is there a replication crisis in finance?" *JF* 78(5):2465–2518.
Katona, Z., Painter, M., Patatoukas, P., Zeng, J. (2025). "On the capital market consequences of big data: Evidence from outer space." *JFQA* 60.
Kelly, B., Pruitt, S., Su, Y. (2019). "Characteristics are covariances: A unified model of risk and return." *JFE* 134(3):501–524.
Loughran, T., McDonald, B. (2011). "When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks." *JF* 66(1):35–65.
McLean, R. D., Pontiff, J. (2016). "Does academic research destroy stock return predictability?" *JF* 71(1):5–32.
McLean, R. D., Pontiff, J., Watanabe, A. (2009). "Share issuance and cross-sectional returns: International evidence." *JFE* 94(1):1–17.
Novy-Marx, R. (2013). "The other side of value: The gross profitability premium." *JFE* 108(1):1–28.
Novy-Marx, R., Velikov, M. (2022). "Betting against betting against beta." *JFE* 143(1):80–106.
Pástor, Ľ., Stambaugh, R., Taylor, L. (2022). "Dissecting green returns." *JFE* 146(2):403–424.
Piotroski, J. (2000). "Value investing: The use of historical financial statement information to separate winners from losers." *Journal of Accounting Research* 38(Supp):1–41.
Sloan, R. (1996). "Do stock prices fully reflect information in accruals and cash flows about future earnings?" *Accounting Review* 71(3):289–315.
Stilger, P., Kostakis, A., Poon, S.-H. (2017). "What does risk-neutral skewness tell us about future stock returns?" *Management Science* 63(6):1814–1834.
Tetlock, P. (2007). "Giving content to investor sentiment: The role of media in the stock market." *JF* 62(3):1139–1168.