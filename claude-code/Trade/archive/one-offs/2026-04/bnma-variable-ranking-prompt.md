# Bayesian Network Meta-Analysis — Variable Ranking Prompt (v4, self-contained)

**Purpose:** produce posterior distributions over effect size, probabilistic rank, and marginal-contribution probability for every candidate variable — registered, replication-augmented, and newly-discovered — stratified by Score_Component (S / T / R / Overlay). Under-evidenced variables are excluded **by the posterior** (aggressive skeptical priors drive P(rank ∈ top 3) to zero), not by a hard gate.

**How to use:** paste this entire file into any frontier-LLM session with ≥128k context (Claude Opus, GPT-5/4o, Gemini Pro all work). All required context — variable registry, literature catalog, framework definitions, methodology reconciliation — is embedded below. Web search is **optional** (it improves Tier 2 replication discovery and Tier 3 candidate discovery). Python / PyMC execution is **recommended** (four small MCMC fits); if the LLM cannot execute code, it must output the PyMC model code plus an analytical posterior approximation and flag every numeric result as "approximation pending full MCMC."

**What changed from v3:** v3 depended on local files (`master-data-log.xlsx`, `Coin core.md`, `Trad core.md`, `Methodology Prompt.md`). v4 embeds all of that inline so the prompt is portable. The analytical design — four parallel BNMAs, grade-tiered priors, marginal-contribution output, exclusion-by-posterior — is unchanged from v3.

---

## Execution recommendations

1. **Use an LLM with code execution if possible.** Four small Bayesian hierarchical models fit fast (< 10 minutes total). Without code execution, the analysis degrades to expert-judgment synthesis — still useful but clearly labeled as such.
2. **Stop after Stage A.** Validate the candidate list and replication roster before fitting. Bad candidates admitted under clever priors pollute the posterior quietly.
3. **Validate top 3 per group against their primary citation.** The paper names and reported Sharpe numbers are embedded below. Cross-check manually if outputs look surprising.
4. **Natural exclusion only works if you don't override it.** Do not rescue a variable with wide CIs because it "looks interesting." If its posterior says noise, it's noise.
5. **Quarterly re-run.** The analysis feeds framework-review decisions. Next mandatory run is ahead of the 2026-10-14 six-month audit on V026 / V027 / V028.

---

## PROMPT BODY (paste this into the new session)

You are performing a **Bayesian network meta-analysis (BNMA)** on a defined set of trading variables. All context is embedded in the sections below. You will: validate the registry, discover additional studies and candidate variables, fit four parallel hierarchical Bayesian models, and produce a ranking with marginal-contribution probabilities.

---

### Embedded Context — Gerald's Trading Framework

**Asset universe.**
- Crypto: BTC, ETH
- Equities: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC
- ETFs / Indices: QQQ, SPY, EWJ, EWY
- Commodities / Metals: Brent, WTI, Gold, Silver, Copper, Palladium, Platinum

**Evidence grades.**
- **Grade A** — strong, replicated across samples/regions, coherent mechanism, long history.
- **Grade B** — moderate, works in most samples, regime-dependent or thinner academic coverage.
- **Grade C** — weak, small samples, narrative-heavy. Not used as sole entry trigger.
- **Provisional** — candidate awaiting replication or formal grading.
- **Ungraded** — insufficient evidence base yet; watchlist.

**Score_Components (categorical boundary, NOT meta-analysis moderator).**
- **S (Structural directional)** — slow-moving valuation, carry, term structure, network-value, regime-stable signal. Horizon 1–12 months. Effect size = annualized Sharpe of long-short portfolio sorted on the variable.
- **T (Tactical timing)** — price/flow momentum, trend, revision breadth, short-horizon forecast. Horizon 1 week–3 months. Effect size = annualized Sharpe of long-short.
- **R (Risk overlay)** — volatility, stress, sizing/dealer-capacity. Used to size positions, not predict direction. Effect size = Sharpe *improvement* when used as vol-targeting / regime-conditional sizing vs fixed-size baseline. Scale ~0.0 to ~0.4.
- **C (Catalyst)** — event-driven (news, calendar, earnings). Skipped in this BNMA (only 2 variables; event-study scale).
- **Overlay (Regime filter)** — conditional filter that improves other signals' quality. Effect size = conditional Sharpe gain when filter is ON vs OFF.

**Methodology reconciliation notes (must inform priors and reporting).**
- McLean-Pontiff (2015, JF): documented anomalies decay 26% out-of-sample and 58% post-publication. Apply a 30–50% Sharpe haircut to published results by default.
- Bailey-López de Prado et al. (2015): in-sample Sharpe has R² < 0.025 for predicting out-of-sample performance across 888 Quantopian strategies. Discount reported Sharpes aggressively when backtests are the sole evidence.
- Finance publication bias is severe. Err toward skeptical priors.

---

### Embedded Context — The VariableRegistry (28 variables, authoritative)

Columns: Var_ID | Name | Asset_Class | Category | Score_Component | Use_Type | Grade | Source_Paper | Published_Sharpe | Decay_Haircut | Proj_Op_Sharpe | Correlation_w_Existing | Intuition.

#### Risk overlay (R) — 8 variables

- **V001 — VIX.** Cross-Asset / Volatility / R / Risk Management / **Grade A** / Whaley (2000) JD; extensive follow-on literature. Low (<0.3) with HY OAS in normal regimes; high (>0.7) in stress. *Fear gauge; high VIX = elevated risk premia, mean-reversion tendency.*
- **V002 — MOVE Index.** Cross-Asset / Volatility / R / Risk Mgmt / **A** / Siriwardane (2019) JF. Moderate with VIX (~0.5 normally, >0.8 in crises). *Bond-market stress; leads equity vol 1–2 weeks in crises.*
- **V004 — HY OAS.** Cross-Asset / Credit / R / Risk Mgmt / **A** / Gilchrist-Zakrajsek (2012) AER. 0.65–0.75 correlation with Intermediary Capital post-2008. Double-count gate with V027. *Credit-stress gauge; widening = risk-off.*
- **V005 — NFCI.** Cross-Asset / Financial conditions / R / Risk Mgmt / **A** / Brave-Butters (2012) Chicago Fed. *Composite financial conditions; negative = easy, positive = tight.*
- **V015 — BTC realized vol.** Crypto / Volatility / R / Risk Mgmt / **A** / Liu-Tsyvinski (2021) JF. *Vol regime; high realized vol = crash-prone, apply larger stops.*
- **V016 — BTC perp funding rate.** Crypto / Crowding / R / Risk Mgmt / **B** / Aloosh-Ouzan-Shahzad (2023) partial + practitioner. *Extreme positive = crowded longs; negative = shorts paying longs (contrarian bullish).*
- **V018 — BTC 3m basis.** Crypto / Carry/Crowding / R / Risk Mgmt / **B** / Practitioner + carry literature. *High basis = crowded long (bearish lean).*
- **V027 — Intermediary capital ratio.** Cross-Asset / Dealer constraints / R / Risk Mgmt / **A** / He-Kelly-Manela (2017) JFE; Adrian-Etula-Muir (2014) JF (replication). **Published Sharpe 0.6, decay haircut 40%, projected op Sharpe 0.36.** 0.65–0.75 correlation with V004 post-2008. Double-count gate: take more negative, not sum. *Dealer balance-sheet constraint leading indicator; z<-1σ tightens risk overlay one notch.*

#### Structural directional (S) — 9 variables

- **V003 — DXY (Dollar Index).** Cross-Asset / Currency / S / Directional / **A** / Verdelhan (2018) JF; BIS WP 1083 (replication on copper/tin). Moderate inverse with Gold (~-0.6), Brent (~-0.4). *Strong dollar = headwind for commodities, EM, risk assets.*
- **V006 — UST 2Y/10Y yields.** Rates / Yield curve / S / Structural / **A** / Campbell-Shiller (1991); Adrian-Crump-Moench (2013) JFE. *Term slope signals recession/expansion.*
- **V007 — Real yield / Breakevens.** Rates / Inflation expectations / S / Structural / **A** / D'Amico et al. (2018). High with Gold (~-0.84 historically) **but R² collapsed from 84% to 3–7% post-2022** due to central-bank buying. *Real yields drive gold/commodity valuation; regime-dependent.*
- **V008 — ACM Term Premium 10Y.** Rates / Term premium / S / Structural / **A** / Adrian-Crump-Moench (2013) JFE. *Duration-risk compensation; rising TP = tightening.*
- **V011 — Brent M1-M3 curve slope.** Commodities / Term structure / S / Structural / **A** / Gorton-Hayashi-Rouwenhorst (2013) JF; Koijen-Moskowitz-Pedersen-Vrugt (2018) (carry replication, Sharpe 0.74 avg across asset classes). Supplemented by V028. *Backwardation = supply tightness, contango = oversupply.*
- **V012 — BTC active addresses.** Crypto / Network activity / S / Structural / **A** / Liu-Tsyvinski (2021) JF; Cong-He-Li (2021) (replication). *Network usage proxy.*
- **V013 — BTC hash rate.** Crypto / Mining/Security / S / Structural / **A** / Cong-He-Li (2021). *Security proxy.*
- **V019 — MVRV / SOPR.** Crypto / On-chain valuation / S / Structural / **B** / Practitioner-dominant (limited peer-reviewed). *MVRV>3 historically preceded corrections; SOPR<1 = capitulation.*
- **V028 — Basis-momentum.** Commodities / Curve dynamics / S / Structural / **A** / Boons-Prado (2019) JF; Szymanowska et al. (2014) JF (complementary replication). **Published Sharpe 0.8, decay haircut 40%, projected op Sharpe 0.48.** Always used WITH static slope (V011), never alone. *Dynamic complement to static curve slope; catches curve-shape exhaustion.*

#### Tactical timing (T) — 6 variables

- **V009 — Time-series momentum (TSMOM).** All / Momentum / T / Timing / **A** / Moskowitz-Ooi-Pedersen (2012) JFE; Hurst-Ooi-Pedersen (2017) AQR (137 years, 67 markets replication). **Published Sharpe 0.9, decay haircut 40%, projected op Sharpe 0.54.** *Trend following across asset classes; positive autocorrelation at 1–12m horizons. SG CTA Trend Index delivered 0.61 Sharpe 2000–2024 (implementation-adjusted).*
- **V010 — Revision breadth.** Equities / Earnings / T / Timing / **A** / Gleason-Lee (2003); PGIM research (replication). *Analyst revisions contain information; Top-20% vs Bottom-20% revision-direction portfolios show >16% annual spread (practitioner) — subject to decay haircut.*
- **V014 — BTC exchange netflows.** Crypto / Flow / T / Timing / **A** / Aloosh-Ouzan-Shahzad (2023). *Net outflow = accumulation (bullish); net inflow = distribution.*
- **V017 — BTC ETF net flows.** Crypto / Institutional flow / T / Timing / **B** / No direct peer-reviewed; institutional flow literature. *Institutional demand proxy; flow streaks carry information.*
- **V026 — Residual momentum (FF5).** Equities / Factor-adjusted momentum / T / Timing / **A** / Blitz-Huij-Martens (2011) JEF; Asness-Moskowitz-Pedersen (2013) JF (replication). **Published Sharpe 0.7, decay haircut 40%, projected op Sharpe 0.42.** Moderate correlation with raw TSMOM by design. Replaces raw TSMOM for single stocks when they disagree. *Residualization strips factor-driven momentum, leaving alpha-momentum.*
- **V030 — Cross-asset lead-lag.** Cross-Asset / Lead-lag / T / Timing / **Provisional** / Lo-MacKinlay (1990) RFS; Asness-Moskowitz-Pedersen (2013). May overlap with TSMOM for the led asset. *BTC→ETH, NVDA→semis, Copper→ISM, MOVE→VIX, etc.*

#### Overlay (regime filter) — 3 variables

- **V029 — GEX (Gamma Exposure).** Equities / Microstructure / Overlay / Regime Filter / **Provisional** / Barbon-Buraschi (2021); practitioner research. *Positive GEX = dealer hedging is mean-reverting; negative GEX = pro-cyclical/trending.*
- **V031 — Correlation-regime signal quality.** Cross-Asset / Regime / Overlay / Regime Filter / **Provisional** / Kritzman et al. (2011) FAJ (absorption ratio). *High cross-asset correlation = crisis regime; other signals less reliable.*
- **V032 — Decision tree feature importance.** All / ML / Overlay / Regime Filter / **Ungraded** / Gu-Kelly-Xiu (2020) RFS. Meta-variable, not standalone. *Surfaces interaction effects hand-coded rules miss.*

#### Catalyst (C) — skipped in BNMA (only 2 variables)

- V020 News sentiment (Grade B, Tetlock 2007 / Garcia 2013) and V033 Calendar/seasonal (Ungraded, Lucca-Moench 2015 pre-FOMC drift) — excluded from main ranking because event-study effect size is not on the long-short Sharpe scale. Report separately in Stage F if relevant.

---

### Embedded Context — Known Literature Catalog (for Tier 2 replication augmentation)

Beyond each variable's primary citation listed above, the following replication and extension studies are known from Gerald's research cores. Use these in Stage A.2 as "already discovered" — do not invent additional replications without web-search-verifiable citations.

**Momentum / TSMOM / residual momentum:**
- Moskowitz-Ooi-Pedersen (2012) JFE — 58 futures markets, Sharpe ~1.0 diversified
- Jegadeesh-Titman (1993) — cross-sectional equity momentum 55–89 bps/month
- Daniel-Moskowitz (2016) JF — volatility-scaled momentum ~2x Sharpe; crash forecastable via vol state; worst month -88.5% Aug 1932
- Hurst-Ooi-Pedersen (2017) AQR — 137 years, 67 markets; positive Sharpe every decade every asset class; 2022 cal year +27.3%
- Blitz-Huij-Martens (2011) JEF — residual momentum
- Asness-Moskowitz-Pedersen (2013) JF — value and momentum everywhere
- Fieberg et al. (2023/2025) JFQA — CTREND factor, stable long-short even when classical momentum disappoints post-2017
- Han et al. (2024) — crypto TS momentum 28d lookback, 5d hold, Sharpe 1.51
- Sadaqat-Butt (2023) — 147 cryptocurrencies, stop-loss momentum (highest alpha vs benchmarks); conventional momentum -0.235 Sharpe due to crash risk

**Carry / term structure / basis-momentum:**
- Koijen-Moskowitz-Pedersen-Vrugt (2018) — carry avg Sharpe 0.74 across asset classes
- Gorton-Hayashi-Rouwenhorst (2013) JF — commodity carry; roll yield > spot price appreciation 1959–2004
- Boons-Prado (2019) JF — basis-momentum Sharpe 1.2–1.5 across 23 commodities; nearby returns ~18% ann
- Szymanowska-de Roon-Nijman-van den Goorbergh (2014) JF — anatomy of commodity futures risk premia
- Borri et al. (2025) — crypto carry Sharpe 6.45 (2020–2025) declining to negative 2025

**Credit / rates / yield curve:**
- Gilchrist-Zakrajsek (2012) AER — excess bond premium, 0.86 correlation with expected default frequency
- Adrian-Crump-Moench (2013) JFE — term premium; yield-curve inversion predicted 6 of 7 recessions since 1976
- D'Amico et al. (2018) — real yields TIPS decomposition
- Siriwardane (2019) JF — MOVE Index

**Volatility / risk overlays:**
- Whaley (2000) JD — VIX
- Brave-Butters (2012) — NFCI
- He-Kelly-Manela (2017) JFE — intermediary asset pricing
- Adrian-Etula-Muir (2014) JF — broker-dealer leverage factor (complementary)
- Verdelhan (2018) JF — DXY/FX
- Fassas-Hourvouliades (2018) — VIX term structure

**Sentiment / news / attention:**
- Tetlock (2007) JF — news sentiment
- Garcia (2013) — text sentiment
- Gu-Kurov (2020) — Twitter sentiment Sharpe 3.17 before costs (very decay-prone)
- Da-Engelberg-Gao (2011) — Google Trends SVI, short-horizon attention
- Farrell-O'Connor (2024) — F&G Index Granger-causes SPX/Nasdaq/Russell
- Caldara-Iacoviello Fed IFDP — Geopolitical Risk Index

**Crypto-specific:**
- Liu-Tsyvinski (2021) JF — common risk factors in crypto: market, size, momentum
- Cong-He-Li (2021) — on-chain fundamentals
- Aloosh-Ouzan-Shahzad (2023) — exchange flow signals
- Jaquart et al. (2022) — LSTM OOS Sharpe 3.23 (accuracy 52.9–54.1%, 57.5–59.5% on top 10% confidence)

**Earnings / revision / PEAD:**
- Gleason-Lee (2003) — revision breadth
- Martineau (2022) — PEAD arbitraged away in mega-cap
- Philadelphia Fed (2021) — text-based PEAD 8.01% annual drift

**Microstructure / GEX / ML:**
- Barbon-Buraschi (2021) — GEX/dealer hedging
- Lo-MacKinlay (1990) RFS — lead-lag
- Kritzman et al. (2011) FAJ — absorption ratio
- Gu-Kelly-Xiu (2020) RFS — neural nets OOS Sharpe 1.35–2.45 (long-short decile)
- Fischer-Krauss (2018) — LSTM Sharpe 5.8 pre-cost but vanished after 2010 post-costs
- Bailey-López de Prado (2015) — 888 Quantopian strategies, IS-OOS R² <0.025
- Gort et al. (2022) NeurIPS ICAIF — DRL overfitting detection
- Lucca-Moench (2015) JF — pre-FOMC drift

**Portfolio / sizing:**
- Burggraf et al. (2020) — HRP for crypto
- DeMiguel-Garlappi-Uppal (2009) — 1/N competitive with Markowitz
- Antonacci GEM (1974–2013) — CAGR 17.43%, Sharpe 0.87, max DD -22.72%

**Methodology:**
- McLean-Pontiff (2015) — anomalies decay 26% OOS, 58% post-publication
- Bailey-López de Prado (2014) — Deflated Sharpe Ratio

---

### Embedded Context — Un-registered Candidate Variables Known From Cores

These are explicitly outside the registry but plausibly relevant. Admit to Stage A.3 with citation; many will not survive the skeptical prior.

- **MVRV Z-Score** — Coin core practitioner; identifies cycle tops within 2 weeks historically. Correlates with V019. Likely redundant.
- **NVT Signal (90d smoothed)** — Ferretti-Santoro (2022) NVML variant, profit-to-max-drawdown 2.3.
- **Token unlock events** — 16,000+ events studied; ~90% negative price pressure regardless of size.
- **Global M2 money supply** — Fidelity Digital Assets; BTC elasticity 2.65, 60–70 day lag (Johansen cointegration).
- **Fear & Greed Index (<10 threshold)** — +48% 90-day avg return historically; n < 10 readings since 2018, very thin.
- **Whale accumulation / exchange whale ratio** — ML classifiers 68–73% 24–72h directional accuracy; sample specificity concerns.
- **Funding rate arbitrage (delta-neutral)** — ScienceDirect 2024, uncorrelated with directional strategies.
- **Pairs trading BTC-ETH cointegration** — IJSRA 2026 Sharpe 2.45 (16.34% ann ret, 8.45% vol); strongest at 5-min frequency.
- **200-DMA regime filter (equities)** — robust single regime filter for SPY/QQQ.
- **Short-period RSI (2–5 day) on S&P** — 42% invested; classic mean-reversion.
- **Price-to-sales (tech)** — best valuation lens for unprofitable/high-growth.
- **VIX term structure (backwardation = buy)** — Fassas-Hourvouliades 2018.
- **Gold/silver ratio** — >80 risk-off, <60 risk-on.
- **China PMI leading copper** — Grade A per core; "Dr. Copper" B+.
- **EIA inventory surprises (crude)** — weekly event-study.
- **OPEC+ production decisions** — event-driven, Grade A.
- **Dual momentum / Antonacci GEM** — practical portfolio strategy.
- **Market breadth (% constituents >200-DMA)** — SPY/QQQ regime.
- **Hierarchical Risk Parity (HRP)** — portfolio construction rather than signal.

---

### Scope

- **Universe (open with caps):**
  - **Tier 1 — Registered variables:** all 28 in the embedded registry above. Always included. Main ranking uses Grade A + Grade B; Provisional/Ungraded goes to Stage F.
  - **Tier 2 — Registry replications:** additional studies testing registered variables in independent samples, from the embedded literature catalog or (optionally) web-searched. Cap: ≤ 5 new replications per registered variable.
  - **Tier 3 — Un-registered candidate variables:** admit from the embedded candidate list above, or (optionally) from web search. Cap: ≤ 15 candidate variables total. Each must cite ≥ 1 peer-reviewed or high-quality working paper with a quantitative result.
  - **Web search budget (if available):** ≤ 3 searches per Tier 1 variable for replications; ≤ 10 searches total for Tier 3 candidate discovery. Without web search: rely entirely on the embedded literature catalog and candidate list.
- **Stratification:** four parallel BNMAs by Score_Component — **S**, **T**, **R**, **Overlay**. Skip C.
- **Main ranking filter:** Grade A + Grade B + admitted Tier 3 candidates. Provisional/Ungraded registry rows and unadmitted candidates go to Stage F.

### Exclusion-by-posterior (read carefully)

This prompt does NOT hard-gate under-evidenced variables. Instead:

- Priors are aggressively skeptical in inverse proportion to evidence strength (table below).
- Candidates with n_studies = 1 and wide SE will have posteriors dominated by the prior → `mu_k` shrinks toward zero → P(rank ∈ top 3) is tiny → they do not surface in main ranking.
- Report thresholds explicitly flag variables where the posterior cannot distinguish from zero (P(mu_k > 0) < 0.55) or rank CrI is near-uniform (rank_ci_width > 0.7 × group size).

Do not override this mechanism by manually rescuing variables that look intuitively interesting.

### Grade-tiered priors

| `mu_k` prior | Grade A | Grade B | Candidate (peer-reviewed) | Candidate (working paper) | Provisional/Ungraded (Stage F) |
|---|---|---|---|---|---|
| S / T group | N(0, 0.40) | N(0, 0.25) | N(0, 0.10) | N(0, 0.05) | not pooled |
| R group | N(0, 0.20) | N(0, 0.12) | N(0, 0.05) | N(0, 0.025) | not pooled |
| Overlay group | N(0, 0.20) | N(0, 0.12) | N(0, 0.05) | N(0, 0.025) | not pooled |
| Asset-class intercept `alpha_a` | N(0, 0.3) across tiers |
| Heterogeneity `tau_k` S/T | HalfNormal(0.25) |
| Heterogeneity `tau_k` R/Overlay | HalfNormal(0.15) |

Replication count, mechanism strength, independent information are already captured in the Grade. Do not loosen priors further on replication count.

---

### Stage A — Registry validation, replication augmentation, candidate discovery

**A.1 Validate registry (Tier 1).** For each Grade A/B registry row, use the embedded Source_Paper + Published_Sharpe fields as authoritative. Mark `registry_validation = PASS` unless you can demonstrate inconsistency from embedded context or web search.

**A.2 Replication discovery (Tier 2).** Use the embedded Literature Catalog as the primary replication source. For each Grade A/B variable, list additional replication studies from the catalog. If web search is available, run ≤ 3 targeted searches per variable for post-catalog replications. Cap 5 replications per variable.

**A.3 Candidate discovery (Tier 3).** Use the embedded Candidate Variables list as the primary candidate pool. If web search is available, supplement with ≤ 10 searches for recent additions. Require ≥ 1 peer-reviewed or working-paper citation per candidate. Cap 15 admitted total.

**A.4 Score_Component inference for candidates:**
- Slow/valuation/cross-sectional → S
- Price/flow/momentum/short-horizon forecast → T
- Volatility/stress/sizing → R
- Conditional filter that gates other signals → Overlay

Flag `score_component_inferred = TRUE`. Exclude ambiguous assignments to Stage F.

**A.5 Correlation inference for candidates.** List peers from the registry where economic reasoning indicates overlap. Flag `correlation_inferred = TRUE`. Required for marginal-contribution computation; admission without declared peers disallowed unless paper argues uncorrelatedness.

**A.6 SE imputation.** Where not reported: `se ≈ sqrt((1 + sharpe²/2) / n_months)`. Flag `se_imputed = TRUE`.

**Stage A output — print as markdown table:**
```
var_id | name | score_component | tier | grade | source_paper | asset_class |
study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months |
universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed |
registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag
```

**Fail-loud rules (Stage A):**
- Do not invent numerics. Verbal descriptions only → `extraction_flag = NUMERIC_MISSING`.
- No citation → `CITATION_MISSING`.
- No silent cap breaches.
- No ambiguous Score_Component assignments.

**STOP. Print Stage A summary (studies per variable, admitted candidates with inferred Score_Component, rejected candidates with reason, any registry-validation FAILs). Wait for user OK before Stage B.**

---

### Stage B — Network construction per Score_Component

For each group G ∈ {S, T, R, Overlay}:
1. Nodes = all variables in G (Tiers 1+2+3).
2. Edges = pairs tested head-to-head in a single study (expect 0–3).
3. Anchor to asset-class benchmark node.
4. Compile peer map from Correlation_w_Existing (registry) + correlation_peers (Tier 3 inferred).
5. State explicitly that cross-asset pooling within the group rests on common-scale + asset-class-intercept, not indirect evidence chains.

---

### Stage C — Hierarchical Bayesian model per group

Write a PyMC model per group:

```python
# For study i measuring variable k in asset class a:
#   y_i ~ Normal(theta_ik, se_i²)                   # observed, with study SE
#   theta_ik ~ Normal(mu_k + alpha_a, tau_k²)       # study-level random effect
#   mu_k ~ Normal(0, prior_sd_tier_grade_k)         # grade-tiered prior (see table)
#   alpha_a ~ Normal(0, 0.3)                         # asset-class intercept
#   tau_k ~ HalfNormal(prior_sd_hetero_group)       # 0.25 S/T, 0.15 R/Overlay
```

Fit NUTS, 4 chains, 2000 warmup + 2000 draws. Require R-hat < 1.01 and ESS > 400 for `mu_k`, `alpha_a`, `tau_k`. If not met, increase warmup → reparameterize (non-centered) → abort the group.

**If code execution is unavailable:** produce the model code anyway, plus a conjugate-normal analytical approximation (`mu_k | data ∝ Normal(posterior_mean, posterior_sd)` with `posterior_sd² = 1 / (1/prior_sd² + sum(1/se_i²))` and `posterior_mean = posterior_sd² × sum(y_i / se_i²)` under the simplifying assumption `alpha_a = tau_k = 0`). Mark every downstream numeric as "analytical approximation; full MCMC required for production use."

Install guidance (if user has code execution): `pip install pymc arviz --break-system-packages`.

---

### Stage D — Ranking, diagnostics, marginal contribution, exclusion flags

Per variable k from its trace:
- posterior mean, median, 5/95 percentile of `mu_k`
- `p_positive = P(mu_k > 0)`
- rank distribution within the group: `p_top3`, median rank, 5–95 CrI on rank, `rank_ci_width`
- **marginal contribution:** `p_beats_peers = P(mu_k > max over peer set)` where peers are absolute-correlation ≥ 0.5. If empty peer set → fall back to `p_rank1 = P(rank = 1)`
- `tau_k` posterior median
- post-decay Sharpe = posterior median × (1 − decay_haircut%/100). Use registry decay for Tiers 1+2; use 40% default for Tier 3 unless the paper reports its own OOS haircut.

**Exclusion flags:**
- `INDISTINGUISHABLE_FROM_ZERO` if `p_positive < 0.55`
- `RANK_UNSTABLE` if `rank_ci_width > 0.7 × group_size`
- `LOW_POWER_CANDIDATE` if Tier 3 AND n_studies ≤ 1 AND `p_top3 < 0.10`

Write one ranking table per group with columns:
```
var_id | name | tier | grade | asset_class | n_studies |
posterior_mean | ci95_low | ci95_high | p_positive |
p_top3 | median_rank | rank_ci_low | rank_ci_high | rank_ci_width |
tau_posterior_median | peers | p_beats_peers |
registry_published_sharpe | post_decay_sharpe |
divergence_flag | indistinguishable_flag | rank_unstable_flag | low_power_flag
```

**Final report.md structure (in this order):**

1. **Marginal-contribution flags (LEAD).** Variables with `p_beats_peers < 0.40` → demote/merge candidates (name + dominant peer). Tier 3 with `p_beats_peers > 0.80` vs registry peers → promotion candidates.
2. **Per-group ranking tables (four).** Exclusion-flagged variables at bottom with flags surfaced.
3. **Heterogeneity flags.** `tau_k` above threshold → "unreliable pool."
4. **Registry divergence flags.** `|registry_Sharpe − posterior_median| > 2 × se` → registry update candidate.
5. **Grade-rank consistency.** Grade A bottom 3 of group, Grade B top 3, Tier 3 top 3 → quarterly review flag.
6. **Cross-group summary.** Top 3 per group; overall top 5 by `p_top3`. Explicit cross-group-not-on-common-scale caveat.
7. **Prior sensitivity.** Re-run with uniformly-loose prior (N(0, 0.5) for S/T, N(0, 0.25) for R/Overlay, applied to all tiers). Variables moving ≥ 3 ranks → prior-dependent.
8. **Feed to 2026-10-14 audit.** V026 Residual Momentum, V027 Intermediary Capital, V028 Basis-Momentum — BNMA posterior, peer comparison, divergence from registry, ledger evidence (if available). GO/NO-GO per variable.
9. **Tier 3 graduation recommendations.** Candidates surviving the posterior (`p_positive > 0.70`, `p_beats_peers > 0.60`, passes heterogeneity) → recommend Grade B admission.
10. **Memory-ready insights.** 3–5 bullets suitable for framework memory update.

---

### Stage E — Reserved (skip)

---

### Stage F — Candidate pipeline

Merge into one output:
- Provisional/Ungraded registry rows (V029, V030, V031, V032, V033) plus V020.
- Tier 3 candidates flagged `LOW_POWER_CANDIDATE` in Stage D.
- Admitted Tier 3 candidates that failed `p_beats_peers` against registry peers but have independent information.

Per entry: name, citation, Score_Component (inferred or registered), peers, posterior summary if available, one-line verdict (`WATCH`, `NEEDS_MORE_EVIDENCE`, `PROMOTE_AT_NEXT_QUARTERLY`).

---

### Stage G — Optional SignalLedger consistency channel

If the user provides an out-of-sample signal ledger (trade log) with columns including decisive score legs and realized P&L, compute hit rate of each variable-driven signal and flag `OOS_DIVERGENCE` where pooled posterior sign contradicts OOS direction on ≥ 70% of deployments. Skip this stage entirely if no ledger is provided. Note explicitly that with small N the power is near zero — this is a consistency check, not a posterior update.

---

### Hard rules

- Every numeric claim in the final report must cite a ranking table row or a trace parameter. No freehand numbers.
- Do not collapse Score_Components onto one scale.
- Do not bypass exclusion-by-posterior. A Tier 3 candidate with wide CI must not be promoted.
- Do not exceed search caps. Report cap breaches for user decision.
- Every inferred field carries its `*_inferred = TRUE` flag through to the report.
- Any BNMA that fails to converge after reparameterization → report and abort that group.
- Marginal-contribution section leads the report.
- If running without code execution, mark all numerics "analytical approximation" and require full MCMC before any framework-change action.

---

### Deliverables

If the LLM has file-write access, write to a working directory:
- `stage_a.csv`, `stage_a_summary.md`, `candidates_rejected.csv`
- `network_{S,T,R,Overlay}.md`
- `model_{S,T,R,Overlay}.py`
- `trace_{S,T,R,Overlay}.nc`
- `ranking_{S,T,R,Overlay}.csv`
- `report.md` (primary deliverable)
- `candidate_pipeline.md`
- `ledger_divergence.md` (only if Stage G ran)

If file write is unavailable, output all content inline in the chat as labeled markdown sections.

End by printing:
1. Per-group top 3 with `p_top3` and `p_beats_peers`.
2. Any `INDISTINGUISHABLE_FROM_ZERO`, `RANK_UNSTABLE`, or `LOW_POWER_CANDIDATE` flags.
3. Tier 3 graduation candidates (for next registry admission).
4. GO/NO-GO for V026, V027, V028 against 2026-10-14 audit.

## END PROMPT BODY
