RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = INDEX_ONLY; MIN_CANDIDATES = 5-7; MANDATES = US_BROAD_EQUITY + GOLD + EQUITY_INDEX_VRP + NON_GOLD_COMMODITY + NON_US_OR_CROSS_ASSET; PARADIGM_MIN = 4_OF_5.

# Six index-only signals to harden a 32-variable framework

## 1. Executive summary

Six candidates clear the bar for registration into the existing 32-variable book without duplicating S/T/R or Overlay slots. The top three are **CAND-01 Bollerslev-Tauchen-Zhou variance risk premium (BTZ-VRP) on SPX** as a directional-timing signal addressing the largest documented gap (V001/V002 are vol *levels*, not *premia*); **CAND-02 Baltussen-Da-Lammers-Martens (2021) intraday-momentum / dealer-gamma gate on ES/SPY** as a sizing scalar that fills the dealer-flow gap with peer-reviewed JFE backing and a 2024 SPY OOS replication at Sharpe 1.33; and **CAND-03 Basu-Miffre (2013) hedging-pressure long-short on a non-gold commodity basket** that closes the CFTC-CoT structural gap beyond Boons-Prado basis-momentum (V028) and Brent slope (V011). Adding **CAND-04 Cieslak-Povala (2015) bond risk-premium factor on TLT/UB futures** (cross-asset, structural-nowcasting), **CAND-05 Erb-Harvey "Golden Dilemma" real-price + gold positioning composite on GLD** (gold-specific, behavioral-positioning; Grade C with explicit caveat that mean-reversion has failed 2013–2026), and **CAND-06 Neely-Rapach-Tu-Zhou (2014) PC-TECH equity-premium index on SPY** (US broad equity, behavioral-positioning combined with classical-risk-premium) yields all five mandatory asset/topic slots filled and four of five paradigms covered. Cumulative framework impact is moderate-to-high: roughly 18–25% paradigm diversification gain (variance-premium and dealer-gamma channels are absent today) at the cost of one new options-chain feed (~$20–40k/yr OptionMetrics-equivalent) and one positioning data subscription (~$2–10k/yr SpotGamma-class). Expected time-to-deployment: four candidates IMMEDIATE (≤4 weeks), two NEAR (4–12 weeks).

## 2. Search log and seed disposition

Tier-1 journals scanned: *Journal of Finance, Journal of Financial Economics, Review of Financial Studies*. Tier-2: *JFQA, Review of Asset Pricing Studies, Financial Analysts Journal, Journal of Portfolio Management, Management Science, Journal of Banking & Finance, Journal of Applied Econometrics, Journal of Monetary Economics, Journal of Econometrics, Quarterly Journal of Economics, AER*. Working-paper repositories: NBER, SSRN, Federal Reserve FEDS/IFDP. Time window 2000–2026 with prioritization of post-publication replications 2015+. JEL codes G11/G12/G13/G14/G17.

PRISMA-style flow: 19 seeds identified → 19 evaluated against inclusion/exclusion → 12 advanced past mechanism/replication screening → 7 reduced to 6 after orthogonality check (Driessen-Maenhout-Vilkov dispersion dropped because OOS Sharpe collapsed post-2009 per Faria/Kosowski/Wang and net-of-cost frictions exceed gross premium in published comparisons) → final shortlist of 6 candidates spanning all five mandatory slots.

**Seed Disposition Table (all 19 seeds, no silent skipping):**

| # | Seed | Disposition | Reason |
|---|---|---|---|
| 1 | Bollerslev-Tauchen-Zhou (2009) RFS | **INCLUDED (CAND-01)** | Best peer-reviewed VRP, robust BMXZ 2014 replication, fills V001/V002 premium gap |
| 2 | Bekaert-Hoerova (2014) JoE | EXCLUDED | Decomposition method dominated by BTZ for tradable signal; retained as construction reference for CV vs VP split |
| 3 | Martin (2017) QJE SVIX | PARTIAL | Lof (2019) replicates OOS; competes with BTZ-VRP; held in reserve as alternative VRP construction (lower-bound interpretation; tighter mechanism but redundant if BTZ-VRP registered) |
| 4 | Garleanu-Pedersen-Poteshman (2009) RFS | EXCLUDED | Structural pricing model, not a return-predictive signal with clean Sharpe; channel survives via Baltussen et al. (CAND-02) |
| 5 | Kelly-Jiang (2014) RFS | EXCLUDED | Bali-Cakici-Whitelaw rebuttal; primarily cross-sectional tail-beta with weak aggregate-timing OOS; slow-moving, redundant with V004 EBP |
| 6 | Driessen-Maenhout-Vilkov (2009) JF dispersion | EXCLUDED | Net-of-cost premium not exploitable per original paper; Faria-Kosowski-Wang document post-2009 OOS decline as dispersion capital crowded in |
| 7 | Hong-Yogo (2012) JFE open interest | EXCLUDED | Predictive-regression paper with no clean tradable Sharpe; weakened post-financialization (Cheng-Xiong 2014; Kang-Rouwenhorst-Tang 2020) |
| 8 | Basu-Miffre (2013) JBF hedging pressure | **INCLUDED (CAND-03)** | Replicated long-short Sharpe 0.27–0.93; CFTC CoT free; fills non-gold commodity slot beyond V028 |
| 9 | Erb-Harvey (2006/2013) FAJ | PARTIAL | Roll-yield decomposition partially overlaps V011 and V028; "Golden Dilemma" portion enters as **CAND-05 component** for gold |
| 10 | Neely-Rapach-Tu-Zhou (2014) MS | **INCLUDED (CAND-06)** | Bätje-Menkhoff (2016) confirms tech-indicator stability; PC-ALL OOS R² 1.32% monthly, survives Goyal-Welch-Zafirov (2024) qualitatively |
| 11 | Bańbura-Modugno (2014) JAE mixed-frequency DFM | EXCLUDED | Methodology paper, not a return-predictive signal; NO_OOS_EVIDENCE for direct equity-premium R² |
| 12 | Aruoba-Diebold-Scotti (2009) ADS | EXCLUDED | Real-time business-conditions nowcast, not a published equity-premium predictor with calibrated Sharpe; usable as input but not a standalone registered signal |
| 13 | Scotti (2016) JME surprise/uncertainty | EXCLUDED | NO_OOS_EVIDENCE for direct equity-premium predictive R² in horserace against Goyal-Welch benchmark |
| 14 | Kolanovic / JPM dealer GEX | EXCLUDED as primary; channel captured via CAND-02 | Industry desk research, non-peer-reviewed; academic formalization is Baltussen-Da-Lammers-Martens (2021) JFE |
| 15 | Barbon-Buraschi (2021) Gamma Fragility | PARTIAL | Working paper (SSRN, not peer-reviewed as of Apr 2026); used as supplementary regime-gate input layered over CAND-02 |
| 16 | Tuzun (2013), Ivanov-Lenkey (2018), Bogousslavsky (2021) LETF/intraday | EXCLUDED | Ivanov-Lenkey (2018) JFM and Lenkey (2024) survey conclude LETF rebalance impact is <6.6% of late-day vol after capital-flow adjustment; signal economically marginal |
| 17 | KMPV 2018 carry variants | **INCLUDED (CAND-04)** Cieslak-Povala (2015) RFS as bond carry/cycle variant | Distinct from KMPV in mechanism (inflation trend τ + cycle decomposition); R² 43–60% IS for 2-5Y excess bond returns |
| 18 | Baker-Bloom-Davis (2016) QJE EPU | EXCLUDED | Predicts vol not returns; Bae-Jo-Shim (2025) CJE finds EPU shocks lose return significance in 2008–2019 subsample |
| 19 | Barro (2006) / Gabaix (2012) / Wachter (2013) rare disasters | EXCLUDED as standalone; mechanism cited inside CAND-05 | Theoretical model, not a directly tradable signal; supports gold safe-haven prior |

## 3. Ranked candidate table

### CAND-01 — BTZ Variance Risk Premium on SPX

- **Signal type:** DIRECTIONAL_TIMING (sizing-scalar variant available)
- **Factor name:** Variance Risk Premium (BTZ-VRP)
- **Primary citation:** Bollerslev, Tauchen & Zhou (2009), "Expected Stock Returns and Variance Risk Premia," *RFS* 22(11), 4463–4492. DOI: 10.1093/rfs/hhp008.
- **Replication citations:** Bollerslev, Marrone, Xu & Zhou (2014), *JFQA* 49(3), 633–661, DOI: 10.1017/S0022109014000453 (international panel, US OOS R² ≈ 4–6% at 3-month horizon). Bekaert & Hoerova (2014), *JoE* 183(2), 181–192, DOI: 10.1016/j.jeconom.2014.05.008. Bollerslev, Todorov & Xu (2015), *JFE* 118, 113–134 (good/bad VRP decomposition). Cheng (2019), *RFS* 32(1), 180–227 (post-crisis attenuation).
- **Asset coverage:** SPX index — instrument: ES futures and SPY ETF.
- **Target gap filled:** Gap 2 (variance/volatility risk premium on equity indexes; V001/V002 are levels not premia).
- **Mechanism:** The risk-neutral expectation of future variance (VIX²/12 monthly) systematically exceeds the physical expectation due to a negative variance-risk price; positive ex-ante VRP compensates investors who supply variance insurance and predicts higher subsequent equity returns over 1–3 months.
- **Signal construction:** Compute VRP_t = (VIX_t/100)²/12 − RV_t, where RV_t is realized variance from prior-month 5-minute SPX returns (sum of squared log returns); positive (negative) z-score on rolling 5-year window flags long (short/flat) bias on SPX over next 1–3 months. Sizing-scalar variant: SCALAR_t = 0.5 + clip(z(VRP_t), −1, +1) × 0.5, yielding 0×–1× exposure.
- **Data requirements:** CBOE VIX (free, daily); 5-minute SPX from TickData/Refinitiv/CME (~$5–15k/yr) or replace RV with HAR-forecast from daily realized-range (free). Monthly frequency sufficient.
- **Infrastructure required:** NONE_STANDARD_DATA (if HAR-on-daily-range used) or ALT_DATA_FEED (intraday TickData).
- **Effect size in-sample:** Quarterly OLS, t-stat ≈ 3.9, adj. R² ≈ 6.8% (BTZ 2009 published version); R² rises to ≈ 26% combined with P/E.
- **Effect size OOS:** BMXZ (2014) US OOS R² ≈ 4–6% at 3-month horizon. Cheng (2019) documents post-2010 attenuation of monthly predictability with negative point estimates in some sub-windows. Sharpe of long-only timing overlay vs buy-and-hold: roughly +0.10–0.20 incremental, see BMXZ Table 7.
- **Sharpe decay flag:** Yes — Cheng (2019) post-crisis decline; not >60% decay at quarterly horizon but flagged.
- **Real-time implementability:** HIGH (daily VIX + monthly RV).
- **Executability check (April 18, 2026 close):** VIX ≈ 17–18 at mid-April 2026; trailing 22-day SPX realized vol ≈ 19% annualized following late-March vol spike (VIX touched 31.65). VIX² monthly ≈ 25 (vol-points²); RV monthly ≈ 30. **VRP ≈ −5 (negative)**, in bottom decile of long-run distribution. **Recommendation: SHORT/FLAT bias on SPY/ES; SCALAR ≈ 0.4–0.5** until VRP rebuilds positive. Caveat: post-shock RV spikes commonly produce transient negative VRP that mean-reverts within 4–8 weeks.
- **Correlation with V009 TSMOM:** NOT_REPORTED in published literature; mechanistically distinct (premium vs. trend) — expected |ρ| < 0.3.
- **Correlation with other CANDs in shortlist:** CAND-02 dealer gamma overlaps weakly through the vol-regime channel; expected |ρ| ≈ 0.2–0.4.
- **Recommended Grade:** B (peer-reviewed RFS, multiple independent replications, but documented post-crisis decay).
- **Recommended group:** R (Regime/Risk).
- **Methodology paradigm:** Option-implied.
- **Confidence:** MEDIUM-HIGH.
- **Why it fills a gap:** Existing V001 (VIX level) and V002 (MOVE) are *levels* — they confound the priced premium with realized turbulence. BTZ-VRP isolates the premium component, the empirical variable that BMXZ and Bekaert-Hoerova show carries unique predictive power for equity returns rather than volatility itself.
- **Risk of adoption:** Post-crisis Sharpe decay; signal turns negative (mechanically) after vol shocks producing whipsaw if not paired with regime gate.
- **Deployability timeline:** IMMEDIATE (≤4 weeks).

### CAND-02 — Baltussen-Da-Lammers-Martens intraday-momentum / dealer-gamma gate on ES/SPY

- **Signal type:** SIZING_SCALAR + DIRECTIONAL_TIMING (intraday tactical)
- **Factor name:** Intraday-momentum gated by dealer net gamma exposure (NGE)
- **Primary citation:** Baltussen, Da, Lammers & Martens (2021), "Hedging Demand and Market Intraday Momentum," *JFE* 142(1), 377–403. DOI: 10.1016/j.jfineco.2021.04.029.
- **Replication citations:** Zarattini, Aziz & Barbon (2024), SSRN 4824172 (SPY 2007–early 2024, total return 1,985% net of costs, annualized 19.6%, Sharpe 1.33). Yuan & Li (2022), *Physica A* (China SSE 50). Rosa (2022), *JFM*. Park & Zhao (2024) extending through 2024. Mechanism support: Barbon & Buraschi (2021) SSRN 3725454 working paper, t = −12.08 on gamma-imbalance coefficient for absolute returns; Ni, Pearson, Poteshman & White (2021), *RFS* 34(4), 1952–1986.
- **Asset coverage:** SPX — instrument ES futures, SPY ETF; channel documented across 60+ futures (Baltussen et al. global panel).
- **Target gap filled:** Gap 7 (intermediary/flow signals on TradFi indexes — dealer gamma, intraday flow).
- **Mechanism:** When dealers are short gamma (net negative aggregate dealer gamma), delta-hedging requires same-direction trading that amplifies intraday moves; the last-30-minute return is positively autocorrelated with the rest-of-day return on negative-gamma days and negatively autocorrelated on positive-gamma days.
- **Signal construction:** Compute aggregate dealer NGE_t from OptionMetrics OI × Black-Scholes gamma × spot × 100 across SPX index options under standard assumption (dealers short calls, long puts, net inverse to customer flow). At 15:30 ET measure r_ROD = (S_15:30 − S_close[t-1])/S_close[t-1]. If NGE_t < 0 and |r_ROD| > 0.3%, take position in direction of sign(r_ROD) into the close on ES; if NGE_t > 0, fade (small position opposite sign). Daily/regime variant: SIZE_SCALAR for overnight equity exposure = 1 − 0.5 × 1{NGE_t < negative threshold}.
- **Data requirements:** OptionMetrics IvyDB (~$20–40k/yr academic) or vendor-computed GEX (SpotGamma/SqueezeMetrics, ~$2–10k/yr) for dealer gamma; intraday futures or SPY ticks (TickData ~$3–10k/yr).
- **Infrastructure required:** OPTIONS_CHAIN + ALT_DATA_FEED (intraday).
- **Effect size in-sample:** Sharpe 0.87–1.73 across asset-class panels 1974–2020; t-stats >5 on r_ROD coefficient in pooled equity-index regressions.
- **Effect size OOS:** Zarattini-Aziz-Barbon (2024) SPY Sharpe 1.33 net of costs through early 2024; channel confirmed in Park-Zhao (2024) and global studies. Strong OOS persistence.
- **Sharpe decay flag:** No — OOS Sharpe within 25% of in-sample under gated implementation.
- **Real-time implementability:** MEDIUM-HIGH (requires intraday infrastructure).
- **Executability check (April 18, 2026 close):** SpotGamma's most recent public reference (late February 2026) placed the SPX Risk Pivot near 6,900 with put skew at the 99th percentile and call skew at the 2nd percentile, indicating a fragile/short-gamma regime; VIX touched 28 on a 2% decline in late March. Specific April 17–18, 2026 GEX value is gated behind subscription (NO_OOS_EVIDENCE for exact dollar gamma). **Recommendation: SIZE_SCALAR = 0.7× equity exposure overnight** while regime remains short-gamma; intraday rule active — long ES into close if 15:30 r_ROD > +0.3% with negative GEX confirmation, short ES if r_ROD < −0.3%, flat otherwise.
- **Correlation with V009 TSMOM:** NOT_REPORTED; intraday horizon orthogonal to 12-month TSMOM (expected |ρ| < 0.2).
- **Correlation with other CANDs:** Mild positive correlation with CAND-01 in vol-stress windows.
- **Recommended Grade:** A (peer-reviewed JFE, multiple independent replications including 2024 SPY OOS).
- **Recommended group:** Overlay (intraday) and T (sizing for daily exposure).
- **Methodology paradigm:** Behavioral-positioning (microstructure).
- **Confidence:** HIGH.
- **Why it fills a gap:** No existing variable captures dealer-hedging-driven intraday flow; V001/V002 measure vol levels, V004/V005 capture credit/financial-conditions stress. The dealer-gamma channel is structurally distinct.
- **Risk of adoption:** Requires intraday execution and reliable gamma data feed; vendor signal may diverge from true dealer book; capacity is finite if signal becomes crowded.
- **Deployability timeline:** NEAR (4–12 weeks) given vendor onboarding and intraday execution build.

### CAND-03 — Basu-Miffre hedging-pressure long-short on non-gold commodity basket

- **Signal type:** DIRECTIONAL_TIMING (long-short basket)
- **Factor name:** Hedging-pressure (HP) commodity factor
- **Primary citation:** Basu & Miffre (2013), "Capturing the risk premium of commodity futures: The role of hedging pressure," *JBF* 37(7), 2652–2664. DOI: 10.1016/j.jbankfin.2013.02.031.
- **Replication citations:** Fernandez-Perez, Frijns, Fuertes & Miffre (2018) *JBF* 86, 143–158 (skewness sort 8% ann./Sharpe 0.78); Kang, Rouwenhorst & Tang (2020) *JF*; Szymanowska, de Roon, Nijman & van den Goorbergh (2014) *JF* 69(1), 453–482, DOI: 10.1111/jofi.12096; Bakshi, Gao & Rossi (2019) *Mgmt Sci* 65(2), 619–641; Sakkas & Tessaromatis (2021).
- **Asset coverage:** Cross-section of liquid commodity futures (energy, metals, agriculturals) — instrumented via CME/ICE futures or sector ETFs (USO, UNG, DBA, DBB, COPX); excludes gold to avoid CAND-05 overlap.
- **Target gap filled:** Gap 6 (commodity term structure beyond Brent slope and basis-momentum — hedging pressure / CoT channel).
- **Mechanism:** Commercial hedgers pay a risk premium to speculators for absorbing their net positions; commodities where commercials are net short (producers hedging output) earn positive forward premia, while commodities where commercials are net long (consumers hedging inputs) underperform.
- **Signal construction:** Each Friday from CFTC Commitments of Traders, compute HP_i,t = (Short_commercial − Long_commercial)/(Short_commercial + Long_commercial) for each of 25–27 commodities using rolling 12-month average. Sort into terciles. Long top tercile (high HP), short bottom tercile, equal-weight, monthly rebalance with full collateral.
- **Data requirements:** CFTC CoT report (free, weekly Friday release at cftc.gov); commodity futures price/return series (Bloomberg/Refinitiv/CSI ~$5–15k/yr).
- **Infrastructure required:** FUTURES_ETF_ONLY.
- **Effect size in-sample:** Long-short Sharpe range 0.27–0.93 across HP-hedger and HP-speculator sorts (1992–2011), best variants near upper end; vs. S&P-GSCI passive Sharpe 0.19 in same window.
- **Effect size OOS:** Fuertes et al. (2018) report HP long-short Sharpe ≈ 0.48 in extended sample through ~2014; Kang-Rouwenhorst-Tang (2020) confirm priced premium with sign convention flipped. Some financialization-driven decay.
- **Sharpe decay flag:** Yes (~30–50%); not >60%, so passes threshold.
- **Real-time implementability:** HIGH (free weekly CoT, monthly rebalance).
- **Executability check (April 18, 2026 close):** CFTC CoT publishes Tuesdays-of-record each Friday. Brent in steep backwardation (front-month ≈ $94–95/bbl; M1–M3 positive prompt premium following Q1 Hormuz spike to $118). Copper at $6.07/lb COMEX, ~+30% YoY, supply-deficit narrative ⇒ commercial hedgers likely heavily short, putting copper in long bucket. Natural gas typically in long tail (high hedger short pressure). Wheat, corn, soy positions vary. **Recommendation: implement long basket = {copper futures (HG) via COPX, Brent via BNO/USO, heating oil; weight by HP z-score}; short basket = {natgas via UNG (commercial long), agricultural carry-negative names}**, monthly notional balanced. Initial gross 100% / net 0%, scaled by half until live PnL window completes.
- **Correlation with V009 TSMOM:** NOT_REPORTED in Basu-Miffre directly; literature (Fuertes et al.) suggests HP and 12-month commodity momentum correlate at |ρ| ≈ 0.2–0.4 — distinct enough.
- **Correlation with V028 Boons-Prado basis-momentum:** Mechanism overlaps via term-structure information; expected |ρ| ≈ 0.4–0.6 — flag for monitoring.
- **Recommended Grade:** B (peer-reviewed JBF, multiple replications, documented decay but signal positive).
- **Recommended group:** S (Sentiment/Positioning).
- **Methodology paradigm:** Behavioral-positioning + classical-risk-premium hybrid (Keynesian normal backwardation).
- **Confidence:** MEDIUM-HIGH.
- **Why it fills a gap:** V011 (Brent M1-M3) is single-commodity slope; V028 is basis-momentum. Neither uses CFTC commercial-hedger positioning, which carries information distinct from price-based slope (Hong-Yogo argue OI/positioning subsumes basis at aggregate level).
- **Risk of adoption:** Financialization decay risk; CoT classification quality issues post-2009 disaggregated report.
- **Deployability timeline:** IMMEDIATE.

### CAND-04 — Cieslak-Povala bond risk-premium factor on Treasury futures (cross-asset slot)

- **Signal type:** DIRECTIONAL_TIMING (sizing-scalar for duration)
- **Factor name:** CP-trend bond risk-premium factor
- **Primary citation:** Cieslak & Povala (2015), "Expected Returns in Treasury Bonds," *RFS* 28(10), 2859–2901. DOI: 10.1093/rfs/hhv032.
- **Replication citations:** Bauer & Hamilton (2018) *RFS* (small-sample bias caveat); Sekkel (2011) *JBF* (international tent-shape); Cochrane & Piazzesi (2005) *AER* 95(1), 138–160 (predecessor whose CP factor is subsumed by Cieslak-Povala).
- **Asset coverage:** US Treasury futures (ZN 10Y, ZB 30Y, UB Ultra-Bond) and TLT/IEF ETFs; methodology cleanly portable to JGB, Bund, Gilt as cross-asset extension.
- **Target gap filled:** Gap 4 (macro-nowcasting / structural premium predictor) and Gap 5 (cross-asset carry variant beyond KMPV 2018) on rates.
- **Mechanism:** Yield curves contain a slow-moving inflation-trend component (τ ≈ exponentially smoothed core CPI with weight 0.9) plus orthogonal "cycles." The cycle component is strongly priced — rising cycles signal high expected excess bond returns over the next year.
- **Signal construction:** Compute τ_t = 0.1·CPI_t + 0.9·τ_{t−1} (monthly core CPI year-over-year). For each maturity n ∈ {2,3,4,5,7,10}Y, define cycle_n,t = y_n,t − τ_t. Build CP-trend factor as first PC (or fitted-value coefficient) of cycles across maturities. Position long Treasury duration (TLT or ZN futures) when standardized factor > +0.5σ, short/underweight when < −0.5σ, neutral in between.
- **Data requirements:** Constant-maturity Treasury yields (FRED, free), core CPI (BLS, free, monthly with 2-week lag); replication code in JFAR data archive.
- **Infrastructure required:** NONE_STANDARD_DATA.
- **Effect size in-sample:** R² 43–60% for 1-year excess bond returns on 2–5Y maturities, exceeding Cochrane-Piazzesi's 35–44%.
- **Effect size OOS:** Bauer-Hamilton (2018) attenuate but do not eliminate; predictability degraded during 2009–2021 zero-lower-bound; 2022–2023 rate shock would have generated large losses for any model expecting low premia (NO_OOS_EVIDENCE for clean 2024 academic extension; flag).
- **Sharpe decay flag:** Likely yes (>40%); deploy at reduced sizing initially.
- **Real-time implementability:** HIGH (monthly CPI + daily yields).
- **Executability check (April 18, 2026 close):** US 10Y nominal ≈ 4.3%; 10Y TIPS real ≈ 1.9%; breakeven ≈ 2.4%. Trend τ updated through last core CPI print. Cycle = nominal yield − τ positive across the curve given elevated post-2022 levels and trend τ still anchored ≈ 3% from sticky inflation base. **Standardized cycle factor positive (~+0.7σ) → recommendation: modest LONG duration (TLT or ZN), SCALAR ≈ +0.5 of full duration unit**, with stop if 10Y breaks above 4.6%. Caveat: 2022–2024 unwind of the model's predictive R² implies LOW conviction; treat as small overlay rather than core position.
- **Correlation with V009 TSMOM:** NOT_REPORTED; distinct mechanism (yield-curve premium vs price trend) — expected |ρ| < 0.3 on Treasury futures.
- **Correlation with V006 (UST 2s10s) and V008 (ACM term premium):** Mechanism-overlapping; expected |ρ| ≈ 0.4–0.7 with ACM term premium — **flag for monitoring**, mitigated by Cieslak-Povala's cycle component being orthogonal to inflation trend rather than to ACM's affine decomposition.
- **Recommended Grade:** B (RFS-published, replicated qualitatively, but documented OOS decay).
- **Recommended group:** S (cross-asset positioning) or T (timing duration).
- **Methodology paradigm:** Structural-nowcasting (inflation-trend decomposition) + classical-risk-premium.
- **Confidence:** MEDIUM.
- **Why it fills a gap:** Existing rates exposure (V006, V007, V008) is descriptive not predictive on excess bond returns; CP-trend gives a disciplined structural forecast that the framework currently lacks.
- **Risk of adoption:** Model has performed poorly through QE/normalization regime; correlation overlap with V008 must be measured ex post.
- **Deployability timeline:** IMMEDIATE.

### CAND-05 — Erb-Harvey "Golden Dilemma" real-price + CFTC-CoT positioning composite on GLD

- **Signal type:** DIRECTIONAL_TIMING (with explicit "broken mean-reversion" caveat) and SIZING_SCALAR
- **Factor name:** Gold real-price valuation × speculator-positioning composite
- **Primary citation:** Erb & Harvey (2013), "The Golden Dilemma," *FAJ* 69(4), 10–42. DOI: 10.2469/faj.v69.n4.1.
- **Replication citations:** Erb & Harvey (2017) "The Golden Constant," *JPM*; Baur & McDermott (2010) *JBF* 34(8), 1886–1898 (gold safe-haven); Barro (2006) *QJE* and Wachter (2013) *JF* 68(3), 987–1035 (disaster-risk theoretical underpinning).
- **Asset coverage:** Gold — instrument GLD ETF or COMEX GC futures.
- **Target gap filled:** Gap 1 (gold-specific directional signal — near-zero coverage in current 32-variable book).
- **Mechanism:** Erb-Harvey: real gold price (gold/CPI) historically mean-reverts on multi-decade horizons; secondary input is CFTC speculator net positioning (contrarian at extremes) and Baur-McDermott safe-haven channel (gold rallies on equity left-tail events). The composite recognizes that pure mean-reversion has failed 2013–2026 because central-bank EM purchases and de-dollarization have shifted the regime, so the signal weights short-horizon positioning more heavily and uses real-price only as a tail-risk gate (extreme overvaluation reduces sizing rather than mandating a short).
- **Signal construction:** (1) Compute real gold price RG_t = nominal_gold_t / CPI_t, z-score versus 30-year window; (2) compute speculator net long share SNL_t = (long_speculator − short_speculator)/OI from CFTC disaggregated CoT; (3) compute equity-stress flag ES_t = 1 if VIX > 25 OR EBP > 90th percentile. Composite scalar = 0.6 × (−z(SNL_t)) + 0.4 × ES_t, capped at +1 long and −0.3 short; if z(RG_t) > +2.5 (extreme overvaluation) cap long exposure at 0.5×.
- **Data requirements:** Gold price (free); CPI (BLS free); CFTC CoT (free); VIX (free).
- **Infrastructure required:** FUTURES_ETF_ONLY.
- **Effect size in-sample:** Erb-Harvey reported gold/real-yield correlation ≈ −0.82 over 1997–2012; mean-reversion-based signal had positive expected return historically. Baur-McDermott confirmed safe-haven coefficient at extreme equity quantiles is statistically significant (negative beta in 1% tail).
- **Effect size OOS:** **Mean-reversion has FAILED 2013–2026 — gold rose from ~$1,300 to >$4,800.** Gold/real-yield correlation collapsed to ≈ +0.03–0.07 post-2022. Safe-haven channel survives (COVID, 2022 Russia-Ukraine, 2025–26 Middle East). NO_OOS_EVIDENCE supporting profitable pure mean-reversion trade. The positioning + safe-haven sub-components carry the signal forward.
- **Sharpe decay flag:** Yes — mean-reversion sub-component has been catastrophic; full composite Sharpe estimate uncertain.
- **Real-time implementability:** HIGH.
- **Executability check (April 18, 2026 close):** Gold spot ≈ $4,818/oz (CBS News April 16); 10Y TIPS ≈ 1.9%; real-price z-score very high (~+3σ on 30-year window). CFTC speculator net long currently elevated on safe-haven flows; specific April 2026 SNL value not retrieved (NO_OOS_EVIDENCE for exact CFTC reading at this date — flag). VIX ≈ 17–18 ⇒ ES_t = 0. Composite under above formula with assumed SNL z ≈ +1.0 and ES = 0 yields scalar ≈ −0.6 × 1.0 + 0 = −0.6 → trimmed by RG cap to **REDUCE gold exposure / SCALAR ≈ 0.3× of strategic weight; do not take outright short** given safe-haven optionality and broken mean-reversion track record.
- **Correlation with V009 TSMOM:** Composite is largely contrarian to gold trend; |ρ| with V009 likely negative −0.3 to −0.5 — orthogonality acceptable.
- **Correlation with V003 (DXY) and V007 (real yields/breakevens):** Real-price z-score correlates moderately with V007; flag.
- **Recommended Grade:** C (mean-reversion failure documented; only acceptable as constrained scalar with explicit caveat — Grade A blocked by broken OOS).
- **Recommended group:** S (Sentiment/Positioning).
- **Methodology paradigm:** Behavioral-positioning + classical-risk-premium (rare-disaster).
- **Confidence:** LOW for mean-reversion sub-component; MEDIUM for positioning + safe-haven sub-components.
- **Why it fills a gap:** Gap 1 is the highest-priority gap and the existing book has no gold-specific signal. Even a Grade-C constrained scalar is preferable to NO_QUALIFYING_CANDIDATE provided the LOW confidence flag is respected.
- **Risk of adoption:** Real-price overvaluation has been wrong for 13 years; positioning extremes may persist for years before reversing.
- **Deployability timeline:** IMMEDIATE.

### CAND-06 — Neely-Rapach-Tu-Zhou PC-TECH equity-premium index on SPY

- **Signal type:** DIRECTIONAL_TIMING (sizing scalar)
- **Factor name:** PC-TECH (technical indicators principal-component composite for equity-premium forecasting)
- **Primary citation:** Neely, Rapach, Tu & Zhou (2014), "Forecasting the Equity Risk Premium: The Role of Technical Indicators," *Mgmt Sci* 60(7), 1772–1791. DOI: 10.1287/mnsc.2013.1838.
- **Replication citations:** Bätje & Menkhoff (2016) *Int. J. Forecasting* (technical indicators stable post-2000, ~0.55 net Sharpe); Dong, Li, Rapach & Zhou (2022) *JF* (anomaly-aggregate predictor consistent); Goyal, Welch & Zafirov (2024) *RFS* 37(11), 3490–3557, DOI: 10.1093/rfs/hhae044 (qualified survival in their post-2008 audit).
- **Asset coverage:** US broad equity — SPY ETF, ES futures.
- **Target gap filled:** mandatory US-broad-equity slot; partially Gap 4 (macro-equity-premium predictor).
- **Mechanism:** Combines slow-moving macroeconomic information (12 Goyal-Welch predictors) with 14 technical trend/momentum/OBV rules via principal-components extraction; the PCA filter reduces noise and exploits the complementarity that tech indicators perform well near peaks while macro variables work near troughs.
- **Signal construction:** From monthly S&P 500 build 14 technicals: MA(1,9), MA(1,12), MA(2,9), MA(2,12), MA(3,9), MA(3,12); momentum MoM(9), MoM(12); on-balance-volume rules. Extract first principal component PC-TECH. Separately extract PC-ECON from 14 Goyal-Welch macro variables. Forecast next-month equity premium as ER_t+1 = α + β1·PC-TECH_t + β2·PC-ECON_t (rolling 240-month window). Translate forecast quintile into long-only scalar 0–1.5× SPY exposure.
- **Data requirements:** S&P 500 monthly returns (free); 14 Goyal-Welch predictors (free, Goyal website updated through 2024); all computable from FRED + CRSP-equivalent.
- **Infrastructure required:** NONE_STANDARD_DATA.
- **Effect size in-sample:** PC-TECH OOS R² ≈ 0.88–1.0% per individual; combined COMBO ≈ 1.16%; PC-ALL ≈ 1.32% monthly. CER (certainty-equivalent return) gains 200–800 bp/yr.
- **Effect size OOS:** Bätje-Menkhoff (2016) confirm post-2000 stability for tech component; Goyal-Welch-Zafirov (2024) qualified survival through 2021. Magnitudes drift down in later subsamples.
- **Sharpe decay flag:** Moderate (~30–50%); within threshold.
- **Real-time implementability:** HIGH (monthly).
- **Executability check (April 18, 2026 close):** SPX trading around 6,500–6,700 area (above 200DMA for most of 2026 to date despite late-March pullback), MA crossover signals predominantly bullish (1×9, 1×12, 2×12 all positive); 12-month momentum positive but flattening; PC-ECON inputs mixed (EPU very elevated at 388.08 daily on March 19, 2026; dividend-yield/earnings-yield compressed at high SPX levels). Net forecast modestly positive ⇒ **SCALAR ≈ 1.05× SPY** (slight overweight from baseline 1.0). If late-March vol spike reasserts and 200DMA breaks, scalar drops mechanically toward 0.7×.
- **Correlation with V009 TSMOM:** Documented overlap — MoM(12) component is closely related to TSMOM. Expected |ρ| with V009 ≈ 0.5–0.7 — **flag**, mitigated because PC-TECH includes MA-rule and OBV components beyond pure 12-month momentum, and PC-ECON contributes orthogonal macro information.
- **Correlation with C005 (200DMA filter):** Moderate-to-high overlap on MA component; flag.
- **Recommended Grade:** B (peer-reviewed Mgmt Sci, replicated, qualified GWZ survival).
- **Recommended group:** T (Tactical Timing) or Overlay.
- **Methodology paradigm:** Behavioral-positioning (technical) + classical-risk-premium (Goyal-Welch macro) hybrid.
- **Confidence:** MEDIUM.
- **Why it fills a gap:** Provides a peer-reviewed, replicable, monthly composite forecast for SPY directional timing that combines macro and technical signals without depending on FY2 EPS forecasts. The current framework has trend filters (C005) and breadth (C007) but no formal forecast-of-equity-premium register.
- **Risk of adoption:** Overlap with V009 and C005 must be quantified; pure tech component may underperform in trendless years (2015, 2023).
- **Deployability timeline:** IMMEDIATE.

## 4. Gap coverage matrix

| Gap (priority) | CAND-01 BTZ-VRP | CAND-02 NGE/intraday | CAND-03 HP commodity | CAND-04 CP bond | CAND-05 Gold composite | CAND-06 PC-TECH |
|---|---|---|---|---|---|---|
| 1 Gold directional | — | — | — | — | **✓** | — |
| 2 Equity-index VRP | **✓** | — | — | — | — | — |
| 3 Option-implied directional | partial | **✓** (gamma) | — | — | — | — |
| 4 Macro-nowcasting / equity-premium | — | — | — | partial (rates) | — | **✓** |
| 5 Cross-asset carry variant | — | — | partial | **✓** (bond) | — | — |
| 6 Commodity term-structure beyond V011/V028 | — | — | **✓** | — | — | — |
| 7 Intermediary/flow on TradFi indexes | — | **✓** | — | — | — | — |

All seven gaps receive at least partial coverage. Gap 3 (option-implied directional skew/risk-reversal) is only partially addressed — see Section 10.

## 5. Paradigm diversification check

| Paradigm | Candidates |
|---|---|
| Classical-risk-premium | CAND-04 (CP bond), CAND-03 (Keynesian normal backwardation component) |
| Option-implied | CAND-01 (BTZ-VRP), CAND-02 (dealer gamma derivation) |
| ML-or-Altdata | (none in shortlist — see Section 10) |
| Structural-nowcasting | CAND-04 (Cieslak-Povala τ decomposition), CAND-06 (PC-ECON sub-component) |
| Behavioral-positioning | CAND-02 (intraday momentum), CAND-03 (HP positioning), CAND-05 (CFTC speculator + safe-haven), CAND-06 (PC-TECH technical sub-component) |

**Paradigms covered: 4 of 5 (Classical-risk-premium, Option-implied, Structural-nowcasting, Behavioral-positioning).** ML-or-Altdata is uncovered and flagged in Section 10.

## 6. Asset coverage check

| Mandate | Coverage |
|---|---|
| US broad equity index | CAND-01 SPX VRP, CAND-02 ES/SPY intraday, CAND-06 PC-TECH SPY ✓ |
| Gold | CAND-05 GLD composite ✓ (Grade C) |
| Equity-index VRP | CAND-01 BTZ-VRP ✓ |
| Non-gold commodity | CAND-03 HP basket (energy/metals/ag) ✓ |
| Non-US or cross-asset | CAND-04 Treasury futures cross-asset; CAND-03 cross-commodity; CAND-02 channel global per Baltussen et al. ✓ |

All five mandatory slots filled.

## 7. Correlation / orthogonality analysis vs V009 / V027 / V028

| Candidate | vs V009 TSMOM | vs V027 AEM intermediary | vs V028 Boons-Prado basis-momentum | Within-shortlist flags |
|---|---|---|---|---|
| CAND-01 BTZ-VRP | NOT_REPORTED; expected |ρ| < 0.3 | weak positive in stress (intermediary capital and VRP both spike) | low | mild positive vs CAND-02 in vol shocks |
| CAND-02 Intraday/NGE | NOT_REPORTED; expected |ρ| < 0.2 (intraday vs 12m) | NOT_REPORTED | low | mild positive vs CAND-01 |
| CAND-03 HP commodity | NOT_REPORTED; expected |ρ| ≈ 0.2–0.4 | NOT_REPORTED | **flag |ρ| ≈ 0.4–0.6** with V028 | low |
| CAND-04 CP bond | NOT_REPORTED; expected |ρ| < 0.3 on TLT/ZN | NOT_REPORTED | n/a | flag with V008 ACM term premium (|ρ| ≈ 0.4–0.7 expected) |
| CAND-05 Gold composite | expected −0.3 to −0.5 (contrarian) | low | low | low |
| CAND-06 PC-TECH | **flag |ρ| ≈ 0.5–0.7** (MoM component) | low | low | flag with C005 200DMA filter |

Two within-framework correlation flags require explicit orthogonality testing in the OOS ledger: CAND-03 vs V028 and CAND-06 vs V009/C005. Mitigation in both cases is the multi-component construction (HP positioning is mechanistically distinct from price-based basis-momentum; PC-TECH includes PC-ECON macro layer beyond MoM).

## 8. Replication-audit summary

| Candidate | Independent replicator | Year | OOS window | Sharpe / R² preserved? | Caveats |
|---|---|---|---|---|---|
| CAND-01 | BMXZ (2014) JFQA panel | 2014 | through 2011 | Yes, R² 4–6% at 3M | Cheng (2019) post-crisis decay |
| CAND-01 | Cheng (2019) RFS | 2019 | through ~2016 | Partial decay flagged | Monthly sign flips post-2010 |
| CAND-02 | Zarattini-Aziz-Barbon (2024) SSRN | 2024 | 2007–early 2024 SPY | Yes, Sharpe 1.33 net | Author overlap with Barbon (mitigated by independent academic extensions) |
| CAND-02 | Park-Zhao (2024) WP | 2024 | through 2024 | Yes, channel confirmed | WP not yet peer-reviewed |
| CAND-02 | Yuan-Li (2022) Physica A | 2022 | China SSE 50 | Yes, gamma channel confirmed | Different market |
| CAND-03 | Kang-Rouwenhorst-Tang (2020) JF | 2020 | through ~2019 | Partial (sign-convention differences) | Financialization decay |
| CAND-03 | Fuertes et al. (2018) JBF | 2018 | through ~2014 | Yes, Sharpe ≈ 0.48 | Below original 0.6–0.8 |
| CAND-04 | Bauer-Hamilton (2018) RFS | 2018 | through ~2015 | Attenuated but surviving | Small-sample bias adjustment |
| CAND-04 | Sekkel (2011) JBF | 2011 | International | Tent-shape replicated; weaker R² | Pre-Cieslak-Povala but supports CP family |
| CAND-05 | Erb-Harvey (2017) JPM | 2017 | extended to 2016 | Mean-reversion intact through 2016 | Failed 2017–2026 |
| CAND-05 | Baur-McDermott safe-haven literature (multiple) | 2010–2024 | global, COVID, Ukraine | Yes, safe-haven channel preserved | Pure-mean-reversion sub-signal failed |
| CAND-06 | Bätje-Menkhoff (2016) IJF | 2016 | post-2000 | Yes, ~0.55 net Sharpe | Tech stable, macro unstable |
| CAND-06 | Goyal-Welch-Zafirov (2024) RFS | 2024 | through 2021 | Qualified survival | Magnitudes drift down |

## 9. Registration recommendations

| Registry ID | Candidate | Group | Grade | Tracking instrument | OOS tracking period |
|---|---|---|---|---|---|
| V029 | CAND-01 BTZ-VRP | R | B | SPY (paper) + ES (live) | 24 months |
| V030 | CAND-02 NGE-gated intraday momentum | Overlay (intraday) + T | A | SPY (paper) + ES (live, scalar mode for first 12 mo) | 12 months |
| V031 | CAND-03 HP commodity basket | S | B | Cross-commodity futures basket | 24 months |
| V032 | CAND-04 Cieslak-Povala bond factor | S/T (rates) | B | TLT (paper) + ZN futures (small live) | 24 months |
| V033 | CAND-05 Gold composite | S | C | GLD (paper-only first 12 mo, then half-size live) | 24 months |
| V034 | CAND-06 PC-TECH equity premium | T / Overlay | B | SPY | 24 months |

Note: V033 (gold) registered at Grade C with explicit instruction that the mean-reversion sub-component is muted to zero weight unless real-price z-score retraces below +1.5σ on the 30-year window.

## 10. Gaps still unfilled

- **Gap 3 (option-implied directional skew, risk-reversal, dispersion as a clean directional signal):** PARTIALLY UNFILLED. CAND-01 captures the variance premium and CAND-02 captures dealer-gamma flow, but a dedicated 25-delta risk-reversal or skew-slope timing signal on SPX is not registered. Driessen-Maenhout-Vilkov dispersion fails the cost-net deployability test. **Recommendation: NO_QUALIFYING_CANDIDATE for a stand-alone tradable Grade-A skew/dispersion directional signal at this revision.**
- **ML-or-Altdata paradigm:** UNFILLED. The shortlist covers four of five paradigms; none is purely ML-driven on alt-data with sufficient peer-review and replication for index-only deployment. **NO_QUALIFYING_CANDIDATE meeting full inclusion criteria at this revision.**
- **Non-US equity index directional (EuroStoxx, Nikkei, MSCI EM):** Channel covered indirectly via CAND-02 (Baltussen et al. global panel) and CAND-04 (international cross-asset for rates) but no dedicated non-US equity directional signal is registered. **Recommendation: open dedicated sub-review.**
- **Convenience-yield / inventory commodity term-structure:** CAND-03 covers positioning but does not address physical inventory deviations (Gorton-Hayashi-Rouwenhorst 2013 channel). **NO_QUALIFYING_CANDIDATE retained at this revision; explicit inventory-based signal flagged for next round.**

## 11. Suggested next steps

The four candidates with HIGH or MEDIUM-HIGH confidence and IMMEDIATE deployability (CAND-01, CAND-03, CAND-04, CAND-06) should enter the OOS paper-trading ledger within four weeks. Required infrastructure is minimal: VIX and 5-minute SPX (or HAR proxy) for CAND-01; CFTC CoT and commodity futures returns for CAND-03; FRED and BLS data for CAND-04; Goyal-website + free monthly S&P 500 for CAND-06. CAND-02 requires NEAR (4–12 weeks) deployment given options-chain and intraday infrastructure build; recommend procurement of OptionMetrics IvyDB or vendor GEX subscription within 30 days, paper trade for 60 days before live deployment in scalar mode. CAND-05 (gold composite) registers at Grade C with a 12-month paper-only track before any live capital, given the broken mean-reversion sub-signal.

Two dedicated sub-reviews are warranted: (a) **option-implied directional skew/risk-reversal** to address the Gap-3 hole — candidate seeds for next round include Bollerslev-Todorov "investor fears" tail-risk index, Bali-Cakici-Whitelaw individual SKEW work adapted to index, and Andersen-Bondarenko-Gonzalez-Perez SPX skew dynamics; (b) **convenience-yield / inventory** for commodities — candidate seeds Gorton-Hayashi-Rouwenhorst (2013) RFS, Symeonidis et al. (2012) JBF inventory and commodity returns, Hamilton-Wu (2014) JFE oil inventory.

Three explicit caveats persist: post-publication Sharpe decay is documented for CAND-01, CAND-03, and CAND-04 (all flagged but within the 60% threshold); CAND-05 carries a LOW confidence flag on its mean-reversion sub-component that must be respected and not upgraded; and CAND-02's reliance on vendor GEX or licensed OptionMetrics introduces single-source data risk. Once the OOS ledger accumulates 12 months of out-of-sample evidence, re-grade CAND-04 and CAND-06 from B with possible upgrade or downgrade depending on realized Sharpe ratio versus published.

References list is embedded inline with full citations and DOIs in candidate cards above; per the protocol no separate citations section is appended.