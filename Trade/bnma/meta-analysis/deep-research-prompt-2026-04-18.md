# Deep-Research Prompt — Systematic Review with Replication Audit
## Cross-Asset Risk Premia for Indexes, Stocks, Commodities, Gold
**Prepared:** 2026-04-18
**Use:** Paste the block below `---PROMPT START---` into any deep-research LLM (ChatGPT Deep Research, Claude with web, Gemini Deep Research, Perplexity Pro).
**Expected output:** Ranked short-list of 3–7 candidate variables with full extraction schema, replication audit, and registration recommendations.

---

## How to use this prompt

1. **Paste the full block below into a deep-research LLM.**
2. **The full 32-variable framework is now filled in** — no placeholder step required. The LLM has a complete map of what you own and what pattern of thinking produced it.
3. **The prompt deliberately demands a NEW PERSPECTIVE** — methodology diversification across classical academic factors, machine-learned / alt-data signals, structural / macro-nowcasting signals, and option-implied signals. The LLM is instructed to reject candidates that are simply more risk-premia-canon variants of what you already deploy.
4. **Let the research run fully** — systematic reviews are not one-shot; expect 5–15 minutes of tool calls.
5. **After output:** triage the ranked list, promote top 1–3 candidates into the candidate pipeline for the quarterly methodology review.

---

---PROMPT START---

# Role
You are a senior quantitative-finance research analyst running a structured systematic review with replication audit, modelled on PRISMA 2020 but adapted for empirical asset-pricing research. You will search published academic literature, working papers, and replication studies to identify tradeable variable candidates that fill specific coverage gaps in an existing trading framework. Your output must be decision-ready: each candidate must be rankable, registrable, and immediately implementable.

# Task

Identify, evaluate, and rank candidate academic papers or factor definitions that fill targeted gaps in an existing evidence-graded trading-variable framework. **The output must be split into TWO BUCKETS**, each with a minimum candidate count:

## INDEX BUCKET — priority, **4 candidates minimum**

Directional-timing, regime-gate, or sizing-scalar signals deployable on liquid indexes, commodities, and gold via **futures or ETFs** on the requester's existing execution rails. Each candidate must be able to produce a **buy / short / flat / sized** decision on a single tradeable instrument (S&P 500, NDX, Euro Stoxx 50, Nikkei, gold futures, Brent, copper, agricultural indexes, etc.) at today's close. **No single-name equity infrastructure required.** This bucket drives near-term deployment.

**Within the 4-minimum INDEX slots, coverage must include at least:**
- 1 candidate specifically for **US broad equity index** (SPX, NDX, or Russell 2000 directional/timing/VRP/option-implied/nowcast).
- 1 candidate specifically for **gold** (directional/carry/positioning construction).
- 2 further candidates that collectively cover at least two more of: (a) non-US equity index, (b) non-gold commodity, (c) bond/credit regime filter, (d) cross-asset carry applied to liquid-futures universe.

The 4 INDEX candidates must collectively cover **at least 3 distinct methodology paradigms** from {Classical-risk-premium, Option-implied, ML-or-Altdata, Structural-nowcasting, Behavioral-positioning}.

## STOCKS BUCKET — research, **3 candidates minimum**

Cross-sectional signals on single-name equities that the literature shows **materially shift the return distribution of individual stocks**. The requester has NO specific ticker in mind and is NOT looking to deploy today — the explicit goal is to **research which signals and variables impact the decision to trade single-name stocks**, so that any future single-name infrastructure buildout is prioritized evidence-first. Candidates in this bucket must still meet inclusion criteria (replicated, mechanism-grounded, etc.), but infrastructure requirements are flagged rather than disqualifying.

**Within the 3-minimum STOCKS slots, coverage must include at least:**
- 1 candidate from **Value OR Quality** (the two most foundational cross-sectional factor categories: Novy-Marx profitability, Asness-Frazzini-Pedersen QMJ, Fama-French value with monthly-updated price, Sloan accruals, etc.).
- 1 candidate from a **modern paradigm** — ML cross-sectional (Gu-Kelly-Xiu, Kelly-Pruitt-Su IPCA, Chen-Pelger-Zhu deep-learning), text/NLP (Loughran-McDonald, earnings-call NLP, LLM-based financial text), or alt-data firm-level.
- 1 further candidate from a third distinct STOCKS gap category (Defensive/BAB, fundamental cross-sectional not already covered, sentiment/attention firm-level).

The 3 STOCKS candidates must come from **3 distinct target gap categories** (no two stocks candidates in the same gap).

In both buckets: full extraction schema, replication evidence, implementability assessment, and executability check (defined in Step 4).

# Context — existing framework (for overlap exclusion)

The requester operates a live trading framework with **32 evidence-graded variables across crypto and traditional assets**, organized into four groups: **S (Sentiment/Positioning)**, **T (Tactical Timing)**, **R (Regime/Risk)**, and **Overlay (regime gate)**. Below is the full registry, with canonical citation and a one-line construction note. Do NOT duplicate any of these. Do NOT recommend a variable that is a minor variant, re-parameterization, or re-estimation of any of these unless you explicitly flag the novelty.

## S — Sentiment / Positioning (9 variables)

| ID | Name | Canonical source | Construction |
|---|---|---|---|
| V003 | DXY level and change | Bloomberg DXY | USD trade-weighted index, z-score of 3-month change |
| V006 | UST 2s10s yield curve slope | FRED DGS2, DGS10 | 10-year minus 2-year Treasury yield |
| V007 | Real yields and breakevens | FRED DFII10, T10YIE | 10-year TIPS yield and 10-year breakeven inflation |
| V008 | ACM Term Premium 10Y | Adrian-Crump-Moench (2013) | 10-year Treasury term premium, ACM model |
| V011 | Brent M1-M3 curve slope | ICE Brent futures | Front-month vs third-month price spread (backwardation/contango) |
| V012 | BTC active addresses | Glassnode | Daily unique active on-chain addresses |
| V013 | BTC hash rate | Glassnode | Network hash rate, 14-day EMA |
| V019 | MVRV / SOPR | Glassnode | Market-value-to-realized-value ratio, spent-output-profit-ratio |
| V028 | Commodity basis-momentum | **Boons & Prado (2019) JF** | Basis-momentum sort, commodity futures |

## T — Tactical Timing (5 variables)

| ID | Name | Canonical source | Construction |
|---|---|---|---|
| V009 | Time-Series Momentum (cross-asset) | **Moskowitz, Ooi & Pedersen (2012) JFE** | 12-month trailing excess return, sign-based entry, vol-scaled |
| V010 | Earnings revision breadth | I/B/E/S | Net % of analysts raising minus lowering EPS estimates |
| V014 | BTC exchange netflows | Glassnode | Net BTC flow onto exchanges (7-day) |
| V017 | BTC ETF net flows | Bloomberg | Daily net creations/redemptions across spot BTC ETFs |
| V026 | Residual momentum (FF5-adjusted) | Blitz-Huij-Martens (2011) | Cross-sectional momentum on Fama-French 5-factor residuals |

## R — Regime / Risk (8 variables)

| ID | Name | Canonical source | Construction |
|---|---|---|---|
| V001 | VIX level | CBOE | S&P 500 30-day implied volatility |
| V002 | MOVE Index | ICE | Treasury options 1-month implied volatility |
| V004 | HY OAS / Excess Bond Premium | **Gilchrist & Zakrajšek (2012) AER** | BBB-Treasury OAS spread and GZ-EBP decomposition |
| V005 | Chicago Fed NFCI | FRB Chicago | National Financial Conditions Index |
| V015 | BTC realized volatility | Kaiko / Glassnode | 30-day realized vol of BTC returns |
| V016 | BTC perpetual funding rate | Binance / Bybit aggregated | 8-hour funding rate, 7-day EMA |
| V018 | BTC 3-month basis | CME / Deribit | Annualized basis (3M futures vs spot) |
| V027 | Intermediary capital ratio | **Adrian-Etula-Muir (2014) JF** | Broker-dealer leverage state variable (AEM LMP anchor) |

## Overlay — Regime gate (5 candidate variables, none currently live)

| ID | Name | Canonical source | Construction |
|---|---|---|---|
| C009 | Faber 10-month TAA | **Faber (2007, 2013) JWM** | Long when price > 10-month SMA, else cash |
| C011 | VIX futures term structure | CBOE VX curve | VX1/VX2 contango vs backwardation regime |
| C005 | 200-day moving-average regime filter | — | Binary filter: index above/below 200-DMA |
| C002 | VIX term structure slope | CBOE | VX futures slope (different construct from C011 level) |
| C007 | Market breadth above 200-DMA | S&P 500 constituents | % of S&P 500 stocks trading above 200-DMA |

## Structural characterization of the framework (read this before searching)

This characterization uses a four-dimensional cross-tab — **Factor Style × Asset Class × Economic Mechanism × Methodology Paradigm** — derived from the practitioner factor-taxonomy literature (Ang 2014, Ilmanen 2022, Asness-Moskowitz-Pedersen 2013, plus Cochrane's 2011 AFA presidential address for the mechanism layer). Gaps below are mechanical — they are empty cells in the matrices, not subjective claims.

### Classification of each variable

| ID | Factor style | Asset class | Economic mechanism | Methodology paradigm |
|---|---|---|---|---|
| V001 | Defensive / Vol level | Equity index | Risk compensation (variance) | Reduced-form option-implied level |
| V002 | Defensive / Vol level | Bonds | Risk compensation (variance) | Reduced-form option-implied level |
| V003 | Macro / FX | FX (USD) | Funding / safe-haven demand | Reduced-form macro level |
| V004 | Credit / Defensive | Credit | Intermediary constraint + default premium | Structural decomposition (Gilchrist-Zakrajšek) |
| V005 | Macro regime composite | Composite | Aggregate financial conditions | Reduced-form weighted index |
| V006 | Macro / term | Bonds | Business-cycle predictor | Reduced-form yield-curve spread |
| V007 | Macro / real rates | Bonds | Real-rate + breakeven inflation | Reduced-form (TIPS-extracted) |
| V008 | Macro / term | Bonds | Bond risk premium | Structural affine term-structure (ACM) |
| V009 | Momentum / Trend | Cross-asset | Behavioral (underreaction/disposition) | Reduced-form price-based |
| V010 | Momentum (fundamental) | Equity (single-name) | Analyst-info diffusion / anchoring | Reduced-form fundamental |
| V011 | Carry (curve) | Commodity (energy) | Convenience yield / storage theory | Structural-adjacent term-structure |
| V012 | Sentiment / network | Crypto | Attention / network effect | Alt-data (on-chain) |
| V013 | Sentiment / network | Crypto | Miner commitment / supply | Alt-data (on-chain) |
| V014 | Positioning / flow | Crypto | Order-flow / intent-to-sell | Alt-data (on-chain) |
| V015 | Vol (realized) | Crypto | Vol regime | Reduced-form realized |
| V016 | Carry (vol-like) | Crypto | Leverage demand / futures basis | Reduced-form derivative |
| V017 | Flow | Crypto | Institutional demand / liquidity | Reduced-form flow |
| V018 | Carry | Crypto | Futures-spot arbitrage | Reduced-form derivative |
| V019 | Valuation (mean-reversion) | Crypto | Behavioral / positioning | Alt-data (on-chain) |
| V026 | Momentum (residual) | Equity (single-name) | Behavioral (underreaction) | Reduced-form cross-sectional |
| V027 | Structural regime | Cross-asset | Intermediary constraint / slow-moving capital | Structural (Adrian-Etula-Muir) |
| V028 | Momentum × term-structure | Commodity | Convenience yield × momentum | Reduced-form term-structure |
| C009 | Trend | Equity index | Regime / drawdown avoidance | Reduced-form technical |
| C011 | Vol term | Equity index | Hedging demand | Reduced-form option curve |
| C005 | Trend | Equity index | Regime | Reduced-form technical |
| C002 | Vol term | Equity index | Risk-aversion | Reduced-form option curve |
| C007 | Trend breadth | Equity index | Participation breadth | Reduced-form technical |

### Coverage matrix 1 — Factor Style × Asset Class

(✓ = covered; ✗ = empty cell; (✓) = covered only via cross-asset variable, no asset-specific construction)

| Factor style | Eq Index | Eq Single | Bonds | Credit | Commodity | **Gold** | FX | Crypto |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Momentum / Trend | ✓ C-series | ✓ V026 | (✓) V009 | ✗ | ✓ V028, V009 | ✗ | (✓) V009 | (✓) V009 |
| **Value** | **✗** | **✗** | **✗** | **✗** | **✗** | **✗** | **✗** | (V019 is behavioral, not valuation) |
| **Carry** | **✗** | **✗** | **✗** | **✗** | ✓ V011 | **✗** | **✗** | ✓ V016, V018 |
| Defensive / Vol level | ✓ V001, C011, C002 | ✗ | ✓ V002 | ✗ | ✗ | ✗ | ✗ | ✓ V015 |
| **Variance Risk Premium** | **✗** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Quality / Profitability** | **✗** | **✗** | n/a | n/a | n/a | n/a | n/a | n/a |
| **Low-Vol / BAB** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Macro / Regime | (✓) V005, V027 | (✓) V027 | ✓ V006, V007, V008 | ✓ V004 | (✓) V027 | (✓) V027 | ✓ V003 | (✓) V027 |
| Sentiment / Attention | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ V012, V013, V019 |
| Flow / Positioning | ✗ | ✓ V010 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ V014, V017 |

### Coverage matrix 2 — Methodology Paradigm × Asset Class

| Paradigm | Eq Index | Eq Single | Bonds | Credit | Commodity | **Gold** | FX | Crypto |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Reduced-form price / technical | ✓ | ✓ | ✓ | | ✓ | ✗ | ✓ | ✓ |
| Reduced-form fundamental | ✗ | ✓ V010 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Reduced-form derivative | ✓ C011, C002 | ✗ | ✓ V002 | ✗ | ✗ | ✗ | ✗ | ✓ V016, V017, V018 |
| Structural (affine / DSGE / intermediary) | (✓) V027 | (✓) V027 | ✓ V008, V027 | ✓ V004 | (✓) V027 | (✓) V027 | ✗ | (✓) V027 |
| **Option-implied premium** (skew, VRP, risk-reversal) | **✗** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Alt-data / on-chain / card / satellite** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ V012, V013, V014, V019 |
| **ML / high-dim (Gu-Kelly-Xiu style)** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Text / NLP sentiment** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Macro-nowcasting (mixed-freq DFM, Bańbura-Modugno)** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

### Gaps derived mechanically from empty cells — ranked by recovery value

1. **Any-paradigm × Gold** — near-total empty row. Gold is touched only by cross-asset V009 and V027. No gold-specific construction exists. (Priority #1 for new candidates.)
2. **Value × all-asset-classes** — the entire Value factor row is empty across every asset. The framework lacks a value premium entirely.
3. **Variance Risk Premium × all-asset-classes** — zero coverage. V001 and V002 are LEVELS, not PREMIA.
4. **Option-implied premium paradigm × everything** — zero coverage. All option-derived variables (V001, V002, C002, C011) are static levels/slopes, not premium-capture constructs.
5. **Quality and Low-Vol / BAB × equities** — zero coverage of the two best-documented equity cross-sectional anomalies.
6. **Alt-data × TradFi** — alt-data is 100% crypto. No text sentiment on equities, no card/transaction data, no satellite, no flow-of-funds alt-data for TradFi.
7. **ML / high-dim paradigm** — zero coverage. Every variable in the framework is a hand-specified linear construct.
8. **Macro-nowcasting paradigm** — zero coverage. V005 NFCI is a weighted composite, not a mixed-frequency factor model.
9. **Carry × equity / bond / FX / gold** — carry exists only in commodity (V011) and crypto (V016, V018). The cross-asset carry premium is undeployed.
10. **Sentiment × TradFi equity** — zero coverage. Attention, news sentiment, EPU, retail-attention — all absent.

### What the empty cells reveal about the current construction approach

The pattern of gaps is not random. Four systematic biases are visible:

- **Paradigm bias:** 24 of 27 variables (89%) are reduced-form. Structural appears only in V008, V027, V004. Option-implied, alt-data-TradFi, ML, text, and macro-nowcasting are all zero.
- **Factor bias:** Momentum/Trend (6 variables), Macro regime (7 variables), and crypto constructs (8 variables) together = 21 of 27. Value, Quality, Low-Vol, VRP = zero.
- **Asset bias:** Crypto has 8 variables; single-name equity has 2 (V010, V026); gold has 0.
- **Information-source bias:** Every signal uses either end-of-day price data, macro series from FRED, or on-chain data. No text, no survey, no satellite, no card, no option-density.

**Your job is to push against these biases, not conform to them.** Candidates that are reduced-form price-based momentum or trend on TradFi assets will be rejected as duplicative regardless of citation quality.

# NEW-PERSPECTIVE MANDATE (the single most important instruction in this prompt)

The requester's current 32-variable framework is **methodologically narrow**: reduced-form, linear, end-of-day structured data, evenly split between rates/credit and crypto. Another paper from the same methodological tradition (another cross-sectional momentum tweak, another credit-spread decomposition, another on-chain metric) is NOT what is being requested.

**Your candidate short-list MUST span at least three of the following five methodological paradigms. If it does not, you have failed the task.**

1. **Classical academic risk premium** (e.g., carry, value, quality, defensive) — ONE candidate maximum in this bucket. The requester already has the canonical reference (KMPV 2018) for carry; a second carry-variant candidate is allowed only if the construction differs materially.
2. **Option-implied / variance-structure signals** (variance risk premium, skew, risk reversal, option-implied tail metric, dispersion, put-call parity deviation). AT LEAST ONE CANDIDATE REQUIRED.
3. **Machine-learned / alternative-data signals** (text-based news sentiment, earnings-call transcript sentiment, satellite data, transaction/card data, neural-net portfolios-from-fundamentals in the Gu-Kelly-Xiu 2020 tradition, large-language-model financial applications). AT LEAST ONE CANDIDATE REQUIRED.
4. **Structural / macro-nowcasting signals** (mixed-frequency factor models like Bańbura-Modugno, Stock-Watson factor-extraction for equity-premium prediction, disaster-risk pricing models, production-network propagation, recession nowcasts). AT LEAST ONE CANDIDATE REQUIRED.
5. **Behavioral / attention / positioning microstructure** (retail-attention, Google Trends, Reddit/X sentiment, dealer gamma exposure, option dealer positioning, systematic-macro CTA positioning, hedge-fund crowding signals).

Additional hard constraints for the methodology-diversification goal:

- **INDEX BUCKET minimum: 4 candidates** — directional-timing, regime-gate, or sizing-scalar signals deployable on futures/ETF rails. These are priority. No bucket shortfall is acceptable without explicit "no qualifying candidate" justification.
- **STOCKS BUCKET minimum: 3 candidates** — cross-sectional single-name signals. Research-grade. Infrastructure-cost flagged.
- **DUAL_USE BUCKET: 0–1 candidate maximum.** Dual-use slots are now tightly capped so index and stocks candidates are not crowded out.
- **At least ONE INDEX candidate must specifically target gold directional signals.** Gold is the most uncovered asset in the current framework. Lease rates, real rates, inflation breakevens, central-bank buying, speculative CoT positioning, gold-mining equity ratios, ETF holdings changes.
- **At least ONE INDEX candidate must specifically target US broad equity index (SPX, NDX, or Russell 2000).** This is independent of the gold mandate — the two must be different candidates. Do not let a gold candidate satisfy the US equity mandate.
- **At least ONE INDEX candidate must specifically target the variance / volatility risk premium for equity indexes.** The framework has vol *levels* (V001, V002) but no vol *premium*. This candidate may overlap with the US broad-equity-index mandate if construction is SPX-VRP.
- **At least ONE STOCKS candidate must be from Value OR Quality cross-sectional factor categories.** These are the two most-replicated cross-sectional equity factors outside momentum.
- **At least ONE STOCKS candidate must be from a modern paradigm** (ML cross-sectional, text/NLP, or alt-data firm-level).
- **At least ONE candidate must be from the ML-or-Altdata or Text/NLP paradigm.** Can satisfy either bucket — preferably STOCKS (satisfies the modern-paradigm STOCKS mandate) or INDEX (if macro-data ML or index-level alt-data).
- **At least ONE candidate must be from the Option-implied premium paradigm** (VRP, skew, risk-reversal, dispersion, dealer gamma). Naturally satisfies INDEX bucket.
- **At least ONE candidate must be from the Structural-nowcasting paradigm** (mixed-frequency DFM, macro-surprise-index-based, structural-model equity-premium). Naturally satisfies INDEX bucket.
- **At most TWO candidates may share a methodology paradigm.** Spread the paradigms across the final ranked list.

# Target gaps (coverage priorities, ranked — these feed ranking weights, not exclusion)

Target gaps are annotated by BUCKET — INDEX-tagged gaps drive 60% of ranking weight, STOCKS-tagged gaps drive 30%, dual-use gaps (can hit either bucket depending on construction) drive 10%. Within each ranked gap, higher position = higher priority.

## INDEX BUCKET gaps (priority)

1. **Gold-specific directional signals — INDEX.** Zero coverage currently. Lease rate, real rates, inflation breakevens, central-bank buying, speculative CoT positioning, gold ETF holdings dynamics, gold-mining vs gold ratio.
2. **Variance / volatility risk premium on equity indexes — INDEX.** Zero coverage; V001 and V002 are LEVELS only. IV-minus-RV on SPX, term-structure VRP, cross-section of index VRP.
3. **Option-implied directional signals on indexes — INDEX.** Skew, risk-reversal, put-call parity deviation, option-implied density, dealer gamma exposure, dispersion (index vs single-name implied vol).
4. **Macro-nowcasting / structural equity-index premium predictors — INDEX.** Mixed-frequency dynamic factor models (Bańbura-Modugno), macro surprise indices (Citi, Bloomberg), real-time recession nowcasts, GDP nowcast error as equity-premium signal.
5. **Cross-asset carry — INDEX.** KMPV 2018 is already on the radar. Look for *variants and refinements* — per-asset carry constructions on gold, equity indexes, commodities that differ materially from KMPV 2018's diversified-carry approach.
6. **Commodity term-structure beyond basis-momentum and Brent slope — INDEX.** Hedging-pressure (CoT), inventory-based storage-theory signals, convenience-yield dynamics across commodities (metals, grains, softs), commodity curvature (not just slope).
7. **Intermediary / flow signals on TradFi indexes — INDEX.** Dealer gamma, CTA positioning proxies, systematic-vol-target-fund flows, leveraged-ETF rebalance flows, prime-broker flow-of-funds indicators.

## STOCKS BUCKET gaps (research)

8. **Value — cross-sectional equities — STOCKS.** Book-to-market, earnings yield, CAPE decomposition at stock level, value composites (Asness-Frazzini 2013 "Devil in HML's Detail").
9. **Quality / Profitability — cross-sectional equities — STOCKS.** Novy-Marx (2013) profitability, Asness-Frazzini-Pedersen (2019) quality-minus-junk, Sloan (1996) accruals, Fama-French 5-factor Q/I.
10. **Defensive / Low-Vol / BAB — cross-sectional equities — STOCKS.** Frazzini-Pedersen (2014) betting-against-beta, low-volatility anomaly, idiosyncratic vol (Ang-Hodrick-Xing-Zhang 2006, Hou-Loh 2016).
11. **Machine-learned cross-sectional stock signals — STOCKS.** Gu-Kelly-Xiu (2020) ML portfolios, Kelly-Pruitt-Su (2019) IPCA, Chen-Pelger-Zhu (2023) deep-learning asset pricing.
12. **Text / NLP sentiment on single-names — STOCKS.** 10-K tone (Loughran-McDonald), earnings-call linguistic features, news sentiment (Tetlock 2007 and successors), LLM-based financial-text signals (post-2023 literature).

## Dual-use gaps (index OR stocks depending on construction)

13. **Alt-data on TradFi (non-crypto alt-data).** Card/transaction data, satellite imagery, shipping, jobs postings, credit/debit data. Can target indexes (aggregate-level) or stocks (firm-level).
14. **Sentiment / attention beyond options.** Google Trends, Reddit/X, retail-attention, EPU (Baker-Bloom-Davis 2016). Indexes (aggregate EPU) or stocks (firm-level attention).

# Must-evaluate seed candidates (not endorsements — specific constructions to evaluate explicitly before inventing from scratch)

For each seed candidate below: locate the canonical source, apply the inclusion/exclusion criteria, and either include in the final short-list OR exclude with explicit reason. Do NOT skip seeds silently. If a seed is excluded, state which criterion it failed.

## Seeds for INDEX BUCKET

- **Dealer gamma exposure on SPX** — Kolanovic-JPM (public notes, 2017–present), Barbon-Buraschi (2021 "Gamma Fragility"), SpotGamma / SqueezeMetrics methodology. Evaluate as a directional-timing or sizing signal.
- **Macro surprise indices** — Citigroup Economic Surprise Index (Scotti 2016 SSRN), Bloomberg ECO SURPRISE, Econoday. Evaluate as equity-index directional.
- **SPX risk-reversal and skew** — Garleanu-Pedersen-Poteshman (2009) "Demand-Based Option Pricing," Kelly-Jiang (2014) "Tail Risk." Evaluate as directional/defensive.
- **Dispersion (index vs single-name vol)** — Driessen-Maenhout-Vilkov (2009), Herskovic et al. (2016) on common idiosyncratic vol. Evaluate as sizing or regime.
- **CFTC non-commercial positioning — E-mini, gold, oil, copper** — Hong-Yogo (2012) "Futures Market Interest," Basu-Miffre (2013) hedging-pressure. Evaluate as sentiment/positioning.
- **Variance risk premium, SPX** — Bollerslev-Tauchen-Zhou (2009), Bekaert-Hoerova (2014), Martin (2017) SVIX. Evaluate as directional/timing on SPX.
- **Gold lease rate minus real yield** — Erb-Harvey (2013) commodity framework + Barro (2006) disaster-risk for gold link. Evaluate as gold-specific directional.
- **Macro-nowcasting DFM** — Bańbura-Modugno (2014) mixed-frequency, Aruoba-Diebold-Scotti (2009) ADS index. Evaluate as equity-index directional.
- **Leveraged-ETF and vol-targeted-fund rebalance flows** — Tuzun (2013), Ivanov-Lenkey (2018), Bogousslavsky (2021) "End-of-Day Price Pressure." Evaluate as sizing/flow.

## Seeds for STOCKS BUCKET

- **Novy-Marx (2013) "The Other Side of Value"** — gross profitability. Evaluate as quality/profitability.
- **Asness-Frazzini-Pedersen (2019) "Quality Minus Junk"** — composite quality. Evaluate as stocks-quality.
- **Frazzini-Pedersen (2014) "Betting Against Beta"** — BAB factor. Evaluate as defensive/low-vol.
- **Asness-Frazzini (2013) "The Devil in HML's Details"** — value refinement (monthly-updated price). Evaluate as cross-sectional value.
- **Loughran-McDonald (2011, 2016) 10-K textual tone** — negative-word lexicon. Evaluate as NLP sentiment on single-names.
- **Gu-Kelly-Xiu (2020) "Empirical Asset Pricing via Machine Learning"** — ML portfolios from 94 characteristics. Evaluate as ML-cross-sectional.
- **Kelly-Pruitt-Su (2019) IPCA** — instrumented PCA. Evaluate as latent-factor cross-sectional.
- **Chen-Pelger-Zhu (2023) "Deep Learning in Asset Pricing"** — deep-net cross-sectional. Evaluate as ML-cross-sectional.
- **Sloan (1996) accruals anomaly** — earnings quality. Evaluate as fundamental cross-sectional.

## Seeds for dual-use bucket

- **Baker-Bloom-Davis (2016) EPU** — Economic Policy Uncertainty. Index-level (aggregate EPU) and stocks-level (firm-level EPU).
- **Scotti (2016) Surprise and Uncertainty Indexes** — macro nowcast errors. Index-level.
- **Retail attention — Google Trends** — Da-Engelberg-Gao (2011) SVI. Stock-level and index-level applications.
- **Tetlock (2007) "Giving Content to Investor Sentiment"** — WSJ text. Aggregate or firm-level.

---

# Methodology — follow this sequence

## Step 1 — Search strategy (pre-register this before searching)
- **Target journals (Tier 1):** Journal of Finance (JF), Journal of Financial Economics (JFE), Review of Financial Studies (RFS).
- **Target journals (Tier 2):** Journal of Financial and Quantitative Analysis (JFQA), Review of Asset Pricing Studies (RAPS), Financial Analysts Journal (FAJ), Journal of Portfolio Management (JPM), Management Science.
- **Working paper archives:** NBER, SSRN top-downloaded in relevant JEL codes (G11, G12, G13, G14, G17), CEPR.
- **Time range:** 2000–present, with citation-weighted priority on 2010+ publications and 2015+ replications.
- **Keyword sets (run combinations):** [carry AND "asset pricing"] OR [value AND cross-asset] OR [variance risk premium] OR [betting against beta] OR [low volatility anomaly] OR [commodity term structure] OR [gold AND (lease rate OR real rates OR positioning)] OR [tactical asset allocation AND equity index] OR [factor zoo AND replication].

## Step 2 — Apply inclusion criteria (ALL must be met)
1. **Peer-reviewed in a ranked journal** OR NBER/SSRN working paper with ≥100 citations AND at least one independent replication attempt.
2. **Independently replicated** at least once in a peer-reviewed follow-up (own-author replications do not count; Hou-Xue-Zhang 2020, McLean-Pontiff 2016, and Jensen-Kelly-Pedersen 2023 factor-replication papers are acceptable replication evidence).
3. **Mechanism-grounded** — the paper provides a specific economic or behavioral channel (discount rate, limits to arbitrage, intermediary constraints, information asymmetry, institutional flow). "The factor works empirically" alone does NOT qualify.
4. **Real-time implementable at daily or monthly frequency** — all inputs publicly observable at end-of-period with no look-ahead. Flag any signal requiring quarterly fundamental data as lower priority.
5. **Independent of existing framework variables** — not methodologically identical to V009/V027/V028/V004/C009 or the [EXISTING_FRAMEWORK_VARIABLES] list. Correlation with V009 (TSMOM) must be below |0.5| in at least one published comparison.

## Step 3 — Apply exclusion criteria (ANY triggers exclusion)
- Pure "factor zoo" mass-screening papers with no mechanism (Harvey-Liu-Zhu 2016 is cited AS a zoo audit, not recommended as a candidate).
- Factors failing replication in Hou-Xue-Zhang 2020 OR Jensen-Kelly-Pedersen 2023.
- Signals requiring proprietary, non-public data.
- Signals requiring forecasts of future fundamentals (FY2 EPS estimates, sell-side price targets).
- Signals where the published in-sample Sharpe exceeds the OOS Sharpe by more than 60% (suggests publication bias or p-hacking).
- Factors specific to a single country or decade without cross-sample validation.

## Step 4 — Extract the following schema for each candidate that passes Steps 2–3

| Field | Description |
|---|---|
| **Candidate ID** | Assign a temporary ID: CAND-01, CAND-02, etc. |
| **Bucket** | **INDEX** / **STOCKS** / **DUAL_USE** — which bucket this candidate serves. Dual-use candidates must specify which bucket they primarily serve and what the secondary application is. |
| **Signal type** | **DIRECTIONAL_TIMING** (produces long/short/flat on a single named instrument) / **CROSS_SECTIONAL** (produces a ranking/portfolio across a universe, long-top vs short-bottom) / **REGIME_GATE** (binary on/off filter for entire book) / **SIZING_SCALAR** (continuous scalar modifying gross exposure) / **OVERLAY_COMBO** (combination of regime gate + sizing). This classification is load-bearing — INDEX-bucket candidates must be one of DIRECTIONAL_TIMING / REGIME_GATE / SIZING_SCALAR; STOCKS-bucket candidates are almost always CROSS_SECTIONAL. |
| **Factor name** | Human-readable factor name |
| **Primary citation** | Author(s) (year) "Title," Journal, Volume(Issue): pages. DOI if available. |
| **Replication citations** | List all independent replications with citations. |
| **Asset-class coverage** | Which of: equity index / single-name equity / commodity / gold / bond / currency |
| **Target gap filled** | Which of the 14 gap categories (see Target Gaps section); state which bucket the gap serves. |
| **Mechanism** | 1–2 sentence economic channel |
| **Signal construction** | Exact formula/procedure in 3–8 lines. No pseudo-code — be concrete. |
| **Data requirements** | What inputs, what frequency, what vendor/source, any cost |
| **Infrastructure required** | **FUTURES_ETF_ONLY** (trades on standard futures/ETF rails) / **SINGLE_NAME_UNIVERSE** (needs Russell 1000 / S&P 1500 / CRSP single-name data feed and portfolio construction for ~100–500 names) / **OPTIONS_CHAIN** (needs live options chain data + options execution) / **ALT_DATA_FEED** (requires paid vendor feed — name the vendor) / **NONE_STANDARD_DATA** (all inputs available from FRED / Bloomberg / standard end-of-day). Be explicit — this determines near-term deployability. |
| **Effect size (in-sample)** | Sharpe, t-stat, alpha, whatever the paper reports. Cite exact numbers. |
| **Effect size (OOS)** | Post-publication OOS Sharpe from independent replication. If none, flag "NO_OOS_EVIDENCE." |
| **Sharpe decay** | In-sample Sharpe minus OOS Sharpe. Flag if >60% decay. |
| **Real-time implementability** | HIGH (daily close, public data) / MEDIUM (monthly, public data) / LOW (quarterly or restricted) |
| **Executability check — INDEX candidates** | For a named instrument (SPX or equivalent): "If deployed at today's close, this signal recommends: [LONG / SHORT / FLAT / SIZE_SCALAR=x]." Must be a concrete answer using the signal's exact construction, not a backtested historical. If the candidate cannot produce a concrete executable answer, downgrade Bucket to STOCKS or DUAL_USE and explain. |
| **Executability check — STOCKS candidates** | "If applied to a 500-stock universe at today's close, this signal recommends: [long decile construction / rank aggregate]." State required universe, rebalance cadence, expected turnover, and minimum positions to express. |
| **Correlation with V009 TSMOM** | If reported in any paper, cite. Otherwise "NOT_REPORTED." |
| **Correlation with other candidates** | If two candidates in the short-list have |correlation| > 0.5, flag and recommend one over the other. |
| **Recommended Grade** | A / B / C using the requester's evidence framework: A = replicated, Tier 1 journal, OOS survives; B = one strong paper + one replication OR Tier 2 journal; C = working paper or weak replication |
| **Recommended group** | S (Sentiment/Positioning) / T (Tactical Timing) / R (Regime/Risk) / Overlay. For STOCKS candidates, also indicate whether this is a new group (e.g., "Cross-sectional equity sleeve"). |
| **Methodology paradigm** | Classical-risk-premium / Option-implied / ML-or-Altdata / Structural-nowcasting / Behavioral-positioning. Used to enforce paradigm diversification in ranking. |
| **Confidence** | HIGH / MEDIUM / LOW — YOUR confidence in the candidate surviving real-world deployment |
| **Why it fills a gap** | 2–3 sentences on why this specifically adds information not already in the framework — reference the empty cell(s) in the Factor × Asset or Paradigm × Asset matrix it fills. |
| **Risk of adoption** | 1–2 sentences on what could go wrong (regime dependence, capacity, crowding, data fragility, infrastructure cost) |
| **Deployability timeline** | IMMEDIATE (can run on existing rails within 4 weeks) / NEAR (4–12 weeks incl data integration) / MEDIUM (3–12 months incl infrastructure build) / LONG (>12 months — ML/alt-data pipeline required) |

## Step 5 — Rank the full candidate pool by expected decision value

**Bucket-coverage enforcement (HARD):**
- **INDEX BUCKET:** minimum 4 candidates, each IMMEDIATE or NEAR deployability and Infrastructure = FUTURES_ETF_ONLY / OPTIONS_CHAIN / NONE_STANDARD_DATA. Must collectively cover ≥3 methodology paradigms and include at least one each for (a) US broad equity index, (b) gold, (c) equity-index VRP (may overlap with (a)).
- **STOCKS BUCKET:** minimum 3 candidates, each with explicit infrastructure flag for SINGLE_NAME_UNIVERSE. Must include ≥1 from Value/Quality AND ≥1 from a modern paradigm (ML / NLP / alt-data).
- **DUAL_USE BUCKET:** 0–1 candidate only.
- If you cannot produce the bucket minimums from the qualifying pool, state so explicitly and recommend what sub-gap is structurally un-fillable.

**Ranking weights (within each bucket):**
- 35% — Grade A/B likelihood and replication strength
- 25% — Gap priority (earlier-listed target gap in the bucket outranks later)
- 15% — Orthogonality to existing framework (measured by reported correlation with V009, V027, V028 — or by paradigm/mechanism distinctness if no correlation reported)
- 10% — Deployability timeline (IMMEDIATE > NEAR > MEDIUM > LONG)
- 10% — Paradigm diversification: bonus if the candidate is in a paradigm row that is empty or near-empty in the Paradigm × Asset matrix (option-implied premium, alt-data TradFi, ML, text, macro-nowcasting). Each paradigm bonus only applies once in the final ranked list.
- 5% — Executability check strength (concrete directional/cross-sectional answer beats a hedged "it depends")

**Cross-bucket weight allocation for the final ranked list:**
- Top 7–8 candidates overall, with INDEX bucket receiving ≥50% of slots (minimum 4 of 7–8), STOCKS bucket receiving ~37–40% (minimum 3 of 7–8), DUAL_USE 0–1.
- Within INDEX bucket, the 4 candidates must collectively cover **at least 3 different asset classes** from (US broad equity index / non-US equity index / gold / commodities ex-gold / bonds / FX / cross-asset). US broad equity and gold are guaranteed slots. No two INDEX candidates may share BOTH the same asset class AND the same paradigm.
- Within STOCKS bucket, the 3 candidates must come from **3 different target gap categories** from (Value, Quality, Defensive/BAB, ML-cross-sectional, Text/NLP, Fundamental-cross-sectional). ≥1 must be Value or Quality; ≥1 must be a modern paradigm (ML/NLP/alt-data).

## Step 6 — Produce the deliverable in this exact structure

### 1. Executive Summary (one paragraph)
Top 3 INDEX-bucket candidates named with one-line rationale each, and top 2 STOCKS-bucket candidates named with one-line rationale each. State cumulative framework impact and expected time-to-deployment.

### 2. Search Log
- Journals searched, keyword combinations run, number of papers screened at each stage (PRISMA-style flow).
- Date range of search.
- Replication databases consulted.
- Seed-candidate disposition table: for each of the ~20 seed candidates in the "Must-evaluate seed candidates" section, state INCLUDED / EXCLUDED / PARTIAL, with reason if excluded.

### 3. INDEX BUCKET — Ranked Table (3+ candidates)
Full extraction schema (from Step 4) for each candidate. Order top-ranked first. Each row ends with the Executability Check as a concrete directional answer.

### 4. STOCKS BUCKET — Ranked Table (2+ candidates)
Full extraction schema (from Step 4) for each candidate. Order top-ranked first. Include infrastructure-cost estimate (ballpark: "requires CRSP + Compustat + portfolio optimizer, ~$X annual data cost + 2–4 weeks engineering").

### 5. DUAL_USE BUCKET — Ranked Table (0–2 candidates, optional)
Same schema. State which bucket primary vs secondary.

### 6. Gap Coverage Matrix
A 14 × N_candidates table showing which of the 14 target gaps each candidate fills. Flag uncovered gaps explicitly with "NO_QUALIFYING_CANDIDATE."

### 7. Paradigm Diversification Check
Count candidates by paradigm: Classical-risk-premium / Option-implied / ML-or-Altdata / Structural-nowcasting / Behavioral-positioning. Confirm ≥3 paradigms are represented in the final short-list. If not, state why.

### 8. Overlap / Correlation Analysis
For each candidate, state reported correlation with V009/V027/V028 where known. Flag pairs of candidates with |ρ| > 0.5 and recommend one over the other.

### 9. Replication-Audit Summary
For each candidate, a single paragraph on replication status: who replicated, when, what OOS window, what Sharpe preserved, what caveats.

### 10. Registration Recommendations

**For each INDEX-bucket top candidate:** proposed registry ID (V029, V030, V031 — assign sequentially), Grade, group (S / T / R / Overlay), rationale for Grade assignment, suggested OOS tracking period before promotion to live capital, specific named instrument to track against (e.g., "track on SPX via ES futures; rebalance monthly").

**For each STOCKS-bucket top candidate:** proposed candidate pipeline ID (PIPE-01, PIPE-02), Grade, rationale, infrastructure buildout order-of-magnitude cost, and whether this candidate is promising enough to justify the build-out now or should wait for evidence-stacking with other candidates.

### 11. Gaps Still Unfilled
If any of the 14 target gaps has no qualifying candidate in either bucket, say so explicitly. Do not invent a candidate to fill it. Rank the unfilled gaps by structural priority — which are worth a second systematic review in a later cycle.

### 12. Suggested Next Steps
- Which INDEX-bucket candidate(s) should enter the OOS tracking ledger IMMEDIATELY (next 4 weeks).
- Which STOCKS-bucket candidate(s) should enter the candidate pipeline for further evidence stacking.
- Which candidate(s) need further evidence before entry and what evidence would resolve uncertainty.
- Whether a follow-up systematic review is needed for a specific sub-gap (e.g., "dedicated gold-specific deep-dive," "LLM/NLP stock-signal scan").

# Hard rules (do not violate)

- **No uncited claims.** Every factual assertion about a paper must include the citation.
- **No invented citations.** If you cannot verify a paper exists and says what you claim, omit it.
- **No factor-zoo laundering.** Do not include a factor whose replication status is unknown or failed.
- **No duplication with existing framework.** If a candidate is a variant of V009/V027/V028/V004/C009, say so and exclude — unless it offers a materially distinct construction (e.g., vol-targeted vs plain TSMOM is borderline — flag and explain).
- **No Grade-A claim without independent replication.** Grade A requires at least one independent replication in a peer-reviewed venue.
- **No overconfident OOS claims.** If post-publication OOS is unknown, state "NO_OOS_EVIDENCE" — do not back out an OOS Sharpe from a theoretical model.
- **Respect confidence flags.** Mark LOW confidence candidates as LOW — do not upgrade to HIGH for the sake of ranking.
- **Fail loud on gaps.** If the literature has no qualifying answer for Target Gap #N, say "NO_QUALIFYING_CANDIDATE" for that gap — do not fabricate.
- **No silent seed skipping.** Every seed candidate in the "Must-evaluate seed candidates" section must appear in the Seed Disposition Table with INCLUDED / EXCLUDED / PARTIAL and a reason.
- **No bucket shortfall without declaration.** If you cannot hit INDEX≥3 or STOCKS≥2, say so explicitly with sub-gap analysis showing which parts of the literature failed the criteria.
- **No cross-sectional signal in the INDEX bucket.** A cross-sectional portfolio signal (rank 500 stocks, long-top short-bottom) is NOT an index directional signal. If a candidate is fundamentally cross-sectional, it goes in STOCKS bucket.
- **Every INDEX candidate must produce a concrete Executability Check answer** on a named liquid instrument at today's close. No hedged "conditional on regime" non-answers.
- **Print this header before your output:**
  `RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = INDEX_STOCKS_GAP_FILL; BUCKETS = INDEX(4+) + STOCKS(3+) + DUAL_USE(0-1); MANDATES = US_BROAD_EQUITY + GOLD + EQUITY_INDEX_VRP + STOCKS_VALUE_OR_QUALITY + STOCKS_MODERN_PARADIGM; PARADIGM_MINS = OPTION_IMPLIED + ML_OR_TEXT + STRUCTURAL_NOWCASTING.`

# Output expectations
- Length: 3,000–6,000 words. Depth beats breadth.
- Tone: analytical, skeptical, concrete. No marketing language.
- Format: structured as specified in Step 6. Use tables where the schema calls for them.
- Citations: inline parenthetical + full reference list at the end.
- If tool use is available (web search, academic databases), use it aggressively. If not, work from training knowledge and flag confidence accordingly.

---PROMPT END---

---

## Post-research actions (for the requester, not the LLM)

After the deep-research output lands:

1. **Triage:** Review the ranked table. Reject any candidate where confidence is LOW or where overlap with V009/V027/V028 is high.
2. **Verify top 3:** Independently confirm the primary citation and at least one replication citation for each top candidate. Do not skip this — LLMs sometimes hallucinate journal issues or replication follow-ups.
3. **Register:** Promote 1–3 candidates to the candidate pipeline (see quarterly-methodology-review skill). Assign V029+ IDs.
4. **OOS ledger:** Add hypothetical signals for each new candidate to the SignalLedger sheet in `master-data-log.xlsx` for 12–18 months of OOS tracking before live deployment.
5. **Re-BNMA cadence:** Once 2–3 new Grade A candidates have 12+ months of OOS evidence, run a follow-up BNMA (target: late 2027 or early 2028) including the original 4 papers plus the new evidence stream.

## Why this sequence beats running another BNMA now

BNMA pools effect sizes on variables you already own. The gap is that you do not yet have variables for carry, value, VRP, defensive, commodity term-structure, or gold. You cannot pool what does not exist. A systematic review is a discovery tool; BNMA is a synthesis tool. Discovery precedes synthesis. Running another BNMA in April 2026 with 4 more papers on V009/V027/V028 would give you tighter posteriors on what you already know — it would not give you a variable for gold.
