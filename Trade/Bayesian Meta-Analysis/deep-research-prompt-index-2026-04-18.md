# Deep-Research Prompt — INDEX Systematic Review with Replication Audit
## Directional / Timing / Sizing Signals for Liquid Indexes, Commodities, and Gold
**Prepared:** 2026-04-18
**Use:** Paste the block below `---PROMPT START---` into a deep-research LLM (ChatGPT Deep Research, Claude with web, Gemini Deep Research, Perplexity Pro).
**Expected output:** Ranked short-list of 5–7 candidate variables, all deployable on existing futures/ETF execution rails.

---

## How to use this prompt

1. Paste the full block below into a deep-research LLM.
2. The full 32-variable framework is filled in — no placeholder step.
3. The prompt is INDEX-ONLY. No cross-sectional single-name signals permitted.
4. Let the research run fully — expect 5–15 minutes of tool calls.
5. After output: triage the ranked list, promote top 1–3 candidates into the candidate pipeline for the quarterly methodology review.

---

---PROMPT START---

# Role
You are a senior quantitative-finance research analyst running a structured systematic review with replication audit, modelled on PRISMA 2020 but adapted for empirical asset-pricing research. You will search published academic literature, working papers, and replication studies to identify tradeable directional/timing/sizing signal candidates for liquid indexes, commodities, and gold. Every candidate must be deployable on standard futures/ETF execution rails. Your output must be decision-ready: each candidate must produce a concrete executable answer on a named instrument at today's close.

# Task

Identify, evaluate, and rank **5–7 candidate academic papers or factor definitions** that fill targeted gaps in an existing evidence-graded trading-variable framework. Every candidate must be a **directional-timing, regime-gate, or sizing-scalar signal** deployable on liquid indexes, commodities, or gold via **futures or ETFs**. Each candidate must produce a **buy / short / flat / sized** decision on a single named tradeable instrument (S&P 500, NDX, Euro Stoxx 50, Nikkei 225, gold futures, Brent, copper, agricultural indexes, US Treasury futures, etc.) at today's close. Cross-sectional single-name signals are OUT OF SCOPE and will be rejected.

## Mandatory coverage within the 5–7 candidates

- **≥1 candidate for US broad equity index** (SPX, NDX, or Russell 2000 — directional, timing, VRP, option-implied, or macro-nowcast construction).
- **≥1 candidate for gold** (directional / carry / positioning construction — lease rate, real rates, inflation breakevens, central-bank flow, speculative CoT, gold-mining ratios, ETF holdings).
- **≥1 candidate for the variance / volatility risk premium on equity indexes** (may overlap with US broad equity mandate if SPX-VRP).
- **≥1 candidate for a non-gold commodity** (energy, metals, agriculturals — term-structure, hedging-pressure, inventory, convenience yield).
- **≥1 candidate from a non-US or cross-asset application** (non-US equity index, bond/credit, FX, cross-asset carry, cross-asset regime).
- **The 5–7 candidates must span at least 4 methodology paradigms** from {Classical-risk-premium, Option-implied, ML-or-Altdata, Structural-nowcasting, Behavioral-positioning}.

# Context — existing framework (for overlap exclusion)

The requester operates a live trading framework with **32 evidence-graded variables across crypto and traditional assets**, organized into four groups: **S (Sentiment/Positioning)**, **T (Tactical Timing)**, **R (Regime/Risk)**, and **Overlay (regime gate)**. Below is the full registry. Do NOT duplicate any of these. Do NOT recommend a minor variant or re-parameterization of any of these unless you explicitly flag and justify the novelty.

## S — Sentiment / Positioning (9 variables)

| ID | Name | Canonical source |
|---|---|---|
| V003 | DXY level and change | Bloomberg DXY |
| V006 | UST 2s10s yield curve slope | FRED DGS2, DGS10 |
| V007 | Real yields and breakevens | FRED DFII10, T10YIE |
| V008 | ACM Term Premium 10Y | Adrian-Crump-Moench (2013) |
| V011 | Brent M1-M3 curve slope | ICE Brent futures |
| V012 | BTC active addresses | Glassnode |
| V013 | BTC hash rate | Glassnode |
| V019 | MVRV / SOPR | Glassnode |
| V028 | Commodity basis-momentum | **Boons & Prado (2019) JF** |

## T — Tactical Timing (5 variables)

| ID | Name | Canonical source |
|---|---|---|
| V009 | Time-Series Momentum (cross-asset) | **Moskowitz, Ooi & Pedersen (2012) JFE** |
| V010 | Earnings revision breadth | I/B/E/S |
| V014 | BTC exchange netflows | Glassnode |
| V017 | BTC ETF net flows | Bloomberg |
| V026 | Residual momentum (FF5-adjusted) | Blitz-Huij-Martens (2011) |

## R — Regime / Risk (8 variables)

| ID | Name | Canonical source |
|---|---|---|
| V001 | VIX level | CBOE |
| V002 | MOVE Index | ICE |
| V004 | HY OAS / Excess Bond Premium | **Gilchrist & Zakrajšek (2012) AER** |
| V005 | Chicago Fed NFCI | FRB Chicago |
| V015 | BTC realized volatility | Kaiko / Glassnode |
| V016 | BTC perpetual funding rate | Binance / Bybit |
| V018 | BTC 3-month basis | CME / Deribit |
| V027 | Intermediary capital ratio | **Adrian-Etula-Muir (2014) JF** |

## Overlay — Regime gate (5 candidates)

| ID | Name | Canonical source |
|---|---|---|
| C009 | Faber 10-month TAA | **Faber (2007, 2013) JWM** |
| C011 | VIX futures term structure | CBOE VX curve |
| C005 | 200-day moving-average regime filter | — |
| C002 | VIX term structure slope | CBOE |
| C007 | Market breadth above 200-DMA | S&P 500 constituents |

## Structural characterization of the framework

Index-relevant coverage and gaps below the two coverage matrices. **Gaps are mechanical — they are empty cells in the matrices, not subjective claims.**

### Coverage Matrix — Factor Style × Asset Class (INDEX-relevant columns)

| Factor style | Eq Index | Bonds | Credit | Commodity | **Gold** | FX | Cross-asset |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Momentum / Trend | ✓ C-series | (✓) V009 | | ✓ V028, V009 | ✗ | (✓) V009 | ✓ V009 |
| **Value** | **✗** | **✗** | **✗** | **✗** | **✗** | **✗** | **✗** |
| **Carry** | **✗** | **✗** | **✗** | ✓ V011 | **✗** | **✗** | **✗** |
| Defensive / Vol level | ✓ V001, C011, C002 | ✓ V002 | ✗ | ✗ | ✗ | ✗ | |
| **Variance Risk Premium** | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |
| Macro / Regime | (✓) V005, V027 | ✓ V006, V007, V008 | ✓ V004 | (✓) V027 | (✓) V027 | ✓ V003 | (✓) V027 |
| Structural intermediary | ✓ V027 | ✓ V027 | ✓ V004 | ✓ V027 | ✓ V027 | | ✓ V027 |

### Coverage Matrix — Methodology Paradigm × Asset Class (INDEX-relevant columns)

| Paradigm | Eq Index | Bonds | Credit | Commodity | **Gold** | FX |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Reduced-form price / technical | ✓ | ✓ | | ✓ | ✗ | ✓ |
| Reduced-form derivative | ✓ C011, C002 | ✓ V002 | ✗ | ✗ | ✗ | ✗ |
| Structural (affine / intermediary) | (✓) V027 | ✓ V008, V027 | ✓ V004 | (✓) V027 | (✓) V027 | ✗ |
| **Option-implied premium** (skew, VRP, risk-reversal) | **✗** | **✗** | ✗ | ✗ | ✗ | ✗ |
| **Alt-data TradFi** (card, satellite, text) | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **ML / high-dim** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Macro-nowcasting (mixed-freq DFM)** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ |

### Gaps derived mechanically — ranked by recovery value

1. **Any-paradigm × Gold** — near-total empty row. Highest priority.
2. **Variance Risk Premium × all-asset-classes** — zero coverage. V001 and V002 are LEVELS not PREMIA.
3. **Option-implied premium paradigm × everything** — zero coverage. All option-derived variables (V001, V002, C002, C011) are static levels/slopes.
4. **Macro-nowcasting paradigm × everything** — zero coverage. V005 NFCI is a weighted composite, not a mixed-frequency factor model.
5. **Carry × equity / bond / FX / gold** — carry exists only in commodity (V011). Cross-asset carry premium undeployed.
6. **Commodity term-structure beyond basis-momentum and Brent slope** — hedging-pressure (CoT), inventory signals, curvature absent.
7. **Intermediary / flow on TradFi indexes** — dealer gamma, CTA positioning, vol-target-fund flows, leveraged-ETF rebalance flows, prime-broker indicators.
8. **Alt-data / ML / text for TradFi** — every signal uses end-of-day price or FRED macro data.

**Your job is to push against these biases, not conform to them.** Candidates that are reduced-form price-based momentum or trend on TradFi assets will be rejected as duplicative regardless of citation quality.

# Target gaps (ranked — these feed ranking weights, not exclusion)

1. **Gold-specific directional signals.** Zero coverage currently.
2. **Variance / volatility risk premium on equity indexes.** Zero coverage; V001/V002 are LEVELS only.
3. **Option-implied directional signals on indexes.** Skew, risk-reversal, put-call parity, option-implied density, dealer gamma, dispersion.
4. **Macro-nowcasting / structural equity-index premium predictors.** Mixed-frequency DFM, macro surprise indices, real-time recession nowcasts.
5. **Cross-asset carry variants beyond KMPV 2018.** KMPV 2018 already on the radar — find *variants and refinements*.
6. **Commodity term-structure beyond basis-momentum and Brent slope.** Hedging-pressure (CoT), inventory, convenience yield dynamics across metals/grains/softs, curvature.
7. **Intermediary / flow signals on TradFi indexes.** Dealer gamma, CTA positioning proxies, vol-target-fund flows, leveraged-ETF rebalance flows.

# Must-evaluate seed candidates

For each seed below: locate the canonical source, apply inclusion/exclusion criteria, and either include in the final short-list OR exclude with explicit reason. Do NOT skip seeds silently.

- **Bollerslev-Tauchen-Zhou (2009) "Expected Stock Returns and Variance Risk Premia," RFS** — VRP on SPX.
- **Bekaert-Hoerova (2014) "The VIX, the variance premium and stock market volatility," JoE** — VRP decomposition.
- **Martin (2017) "What is the Expected Return on the Market?" QJE** — SVIX lower bound.
- **Garleanu-Pedersen-Poteshman (2009) "Demand-Based Option Pricing," RFS** — option-implied positioning.
- **Kelly-Jiang (2014) "Tail Risk and Asset Prices," RFS** — tail risk as factor.
- **Driessen-Maenhout-Vilkov (2009) "The Price of Correlation Risk," JF** — dispersion.
- **Hong-Yogo (2012) "What Does Futures Market Interest Tell Us," JFE** — CoT positioning.
- **Basu-Miffre (2013) "Capturing the Risk Premium of Commodity Futures," JBF** — hedging pressure.
- **Erb-Harvey (2013) "The Strategic and Tactical Value of Commodity Futures," FAJ** — gold + commodity framework.
- **Neely-Rapach-Tu-Zhou (2014) "Forecasting the Equity Risk Premium," MS** — combined technical + macro predictors.
- **Bańbura-Modugno (2014) "Maximum Likelihood Estimation of Factor Models on Data Sets with Arbitrary Pattern of Missing Data," JAE** — mixed-frequency DFM.
- **Aruoba-Diebold-Scotti (2009) ADS Index** — real-time business conditions.
- **Scotti (2016) "Surprise and Uncertainty Indexes," JME** — macro surprise as equity-premium signal.
- **Kolanovic-JPM (2017–present, public notes)** — dealer gamma exposure on SPX.
- **Barbon-Buraschi (2021) "Gamma Fragility," working paper** — gamma-fragility construction.
- **Tuzun (2013), Ivanov-Lenkey (2018), Bogousslavsky (2021) "End-of-Day Price Pressure"** — leveraged-ETF and vol-targeted-fund rebalance flows.
- **Koijen-Moskowitz-Pedersen-Vrugt (2018) "Carry," JFE** — already on the radar. Find per-asset VARIANTS only, not this paper.
- **Baker-Bloom-Davis (2016) "Measuring Economic Policy Uncertainty," QJE** — EPU.
- **Barro (2006) "Rare Disasters and Asset Markets," QJE** and successors — disaster-risk for gold.

# Methodology

## Step 1 — Search strategy
- **Tier 1 journals:** JF, JFE, RFS.
- **Tier 2 journals:** JFQA, RAPS, FAJ, JPM, Management Science, JOIM, JBF.
- **Working papers:** NBER, SSRN top-downloaded in JEL G11, G12, G13, G14, G17.
- **Time range:** 2000–present, prioritize 2010+ and 2015+ replications.
- **Keyword sets:** [variance risk premium equity index] OR [dealer gamma option hedging] OR [skew risk reversal directional] OR [macro surprise equity premium] OR [mixed frequency factor model equity] OR [carry asset pricing] OR [gold lease rate real rates] OR [commodity hedging pressure futures] OR [CTA positioning flows].

## Step 2 — Inclusion criteria (all must be met)
1. Peer-reviewed in a ranked journal OR NBER/SSRN working paper with ≥100 citations AND ≥1 independent replication.
2. Independently replicated (McLean-Pontiff 2016, Hou-Xue-Zhang 2020, Jensen-Kelly-Pedersen 2023 count).
3. Mechanism-grounded — specific economic or behavioral channel.
4. Real-time implementable at daily or monthly frequency.
5. Independent of V009, V027, V028, V004, C009 and the rest of the 32-variable registry. Correlation with V009 must be below |0.5| in at least one published comparison, OR the paradigm/mechanism must be distinct.

## Step 3 — Exclusion criteria
- Pure factor-zoo mass-screening without mechanism.
- Factors failing Hou-Xue-Zhang 2020 OR Jensen-Kelly-Pedersen 2023.
- Proprietary non-public data requirements.
- Forecast-of-fundamentals dependencies (FY2 EPS estimates).
- In-sample Sharpe exceeds OOS Sharpe by >60%.
- **Cross-sectional single-name signals.** These belong to a separate STOCKS prompt, not this one.
- Signals specific to a single country/decade without cross-sample validation.

## Step 4 — Extraction schema per candidate

| Field | Description |
|---|---|
| **Candidate ID** | CAND-01, CAND-02, etc. |
| **Signal type** | DIRECTIONAL_TIMING / REGIME_GATE / SIZING_SCALAR / OVERLAY_COMBO. (No CROSS_SECTIONAL — those are out of scope.) |
| **Factor name** | Human-readable |
| **Primary citation** | Author(s) (year) "Title," Journal, Volume(Issue): pages. DOI if available. |
| **Replication citations** | Independent replications. |
| **Asset coverage** | Equity index (specify which) / bonds / credit / commodity (specify which) / gold / FX / cross-asset |
| **Target gap filled** | Which of the 7 gaps |
| **Mechanism** | 1–2 sentences |
| **Signal construction** | Exact formula/procedure in 3–8 lines. No pseudo-code. |
| **Data requirements** | Inputs, frequency, vendor/source, cost |
| **Infrastructure required** | FUTURES_ETF_ONLY / OPTIONS_CHAIN / ALT_DATA_FEED / NONE_STANDARD_DATA |
| **Effect size (in-sample)** | Sharpe, t-stat, alpha with exact numbers. |
| **Effect size (OOS)** | Post-publication OOS Sharpe. "NO_OOS_EVIDENCE" if none. |
| **Sharpe decay** | In-sample minus OOS. Flag >60%. |
| **Real-time implementability** | HIGH / MEDIUM / LOW |
| **Executability check** | "If deployed at today's close on [named instrument], this signal recommends: [LONG / SHORT / FLAT / SIZE_SCALAR=x]." Concrete answer required, not historical backtest. |
| **Correlation with V009 TSMOM** | Cite or "NOT_REPORTED." |
| **Correlation with other candidates in this short-list** | Flag \|ρ\| > 0.5 pairs. |
| **Recommended Grade** | A / B / C |
| **Recommended group** | S / T / R / Overlay |
| **Methodology paradigm** | Classical-risk-premium / Option-implied / ML-or-Altdata / Structural-nowcasting / Behavioral-positioning |
| **Confidence** | HIGH / MEDIUM / LOW |
| **Why it fills a gap** | 2–3 sentences referencing specific empty cells in the matrices above. |
| **Risk of adoption** | 1–2 sentences on regime dependence, capacity, crowding, data fragility. |
| **Deployability timeline** | IMMEDIATE (≤4 weeks) / NEAR (4–12 weeks) / MEDIUM (3–12 months) / LONG (>12 months) |

## Step 5 — Ranking

**Hard bucket minimum:** 5–7 candidates, each IMMEDIATE or NEAR deployability, Infrastructure = FUTURES_ETF_ONLY / OPTIONS_CHAIN / NONE_STANDARD_DATA. Collectively cover ≥4 asset classes and ≥4 paradigms. Mandatory slots: US broad equity (≥1), gold (≥1), equity-index VRP (≥1), non-gold commodity (≥1), non-US or cross-asset (≥1).

**Ranking weights:**
- 35% — Grade A/B likelihood and replication strength
- 25% — Gap priority (earlier gap outranks later)
- 15% — Orthogonality to existing framework
- 10% — Deployability timeline (IMMEDIATE > NEAR > MEDIUM > LONG)
- 10% — Paradigm diversification bonus (empty-row paradigms preferred)
- 5% — Executability check strength

**Tie-break:** if two candidates match on weighted score, prefer the one that covers a mandatory slot not yet filled.

## Step 6 — Deliverable structure

1. **Executive Summary** (one paragraph). Top 3 candidates named with one-line rationale. Cumulative framework impact. Expected time-to-deployment.
2. **Search Log.** Journals, keywords, PRISMA-style flow counts. Seed Disposition Table for all ~19 seeds (INCLUDED / EXCLUDED / PARTIAL + reason).
3. **Ranked Candidate Table.** Full extraction schema (Step 4) for each candidate, top-ranked first.
4. **Gap Coverage Matrix.** 7 × N_candidates showing which gap each fills. Flag uncovered gaps explicitly.
5. **Paradigm Diversification Check.** Paradigm count; confirm ≥4 paradigms represented.
6. **Asset Coverage Check.** Confirm mandatory slots (US equity, gold, VRP, non-gold commodity, non-US/cross-asset) filled.
7. **Correlation / Orthogonality Analysis.** Reported correlation with V009/V027/V028. Flag \|ρ\| > 0.5 pairs within short-list.
8. **Replication-Audit Summary.** Per candidate: who replicated, when, OOS window, Sharpe preserved, caveats.
9. **Registration Recommendations.** Per top candidate: registry ID (V029, V030, V031 sequential), Grade, group (S/T/R/Overlay), OOS tracking period, named instrument to track.
10. **Gaps Still Unfilled.** Explicit "NO_QUALIFYING_CANDIDATE" where applicable.
11. **Suggested Next Steps.** Which candidate(s) enter OOS ledger within 4 weeks. Which need further evidence. Whether a dedicated sub-review is warranted (e.g., "dedicated gold deep-dive," "dealer-gamma construction review").

# Hard rules

- No uncited claims.
- No invented citations.
- No factor-zoo laundering.
- No duplication with existing framework — flag variants explicitly.
- No Grade-A claim without independent replication.
- No overconfident OOS claims — use "NO_OOS_EVIDENCE" where unknown.
- Respect confidence flags — LOW stays LOW.
- Fail loud on gaps — "NO_QUALIFYING_CANDIDATE" per gap as needed.
- No silent seed skipping — every seed in the Seed Disposition Table with reason.
- **No cross-sectional single-name signals.** These are out of scope for this prompt.
- Every candidate must produce a concrete Executability Check answer on a named liquid instrument at today's close.
- **Print this header before your output:**
  `RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = INDEX_ONLY; MIN_CANDIDATES = 5-7; MANDATES = US_BROAD_EQUITY + GOLD + EQUITY_INDEX_VRP + NON_GOLD_COMMODITY + NON_US_OR_CROSS_ASSET; PARADIGM_MIN = 4_OF_5.`

# Output expectations

- Length: 2,500–5,000 words.
- Tone: analytical, skeptical, concrete. No marketing language.
- Format: as specified in Step 6. Use tables where schema calls for them.
- Citations: inline parenthetical + full reference list.

---PROMPT END---

---

## Post-research actions

1. Triage the ranked table. Reject LOW confidence or high-overlap candidates.
2. Verify top 3. Independently confirm primary citation + replication citation for each.
3. Register. Promote 1–3 to candidate pipeline. Assign V029+ IDs.
4. Add to OOS SignalLedger for 12–18 months of hypothetical tracking before live deployment.
5. Re-BNMA cadence: late 2027 / early 2028 once 2–3 new candidates have 12+ months of OOS evidence.
