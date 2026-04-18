# Deep-Research Prompt — STOCKS Systematic Review with Replication Audit
## Cross-Sectional Single-Name Signals for US/Global Equities
**Prepared:** 2026-04-18
**Use:** Paste the block below `---PROMPT START---` into a deep-research LLM (ChatGPT Deep Research, Claude with web, Gemini Deep Research, Perplexity Pro).
**Expected output:** Ranked short-list of 5–7 cross-sectional candidate variables, research-grade — pre-execution.

---

## How to use this prompt

1. Paste the full block below into a deep-research LLM.
2. The full 32-variable framework is filled in — no placeholder step.
3. The prompt is STOCKS-ONLY. No index-directional, no commodity, no gold. Every candidate must be a **cross-sectional single-name signal** over a defined equity universe.
4. Research-grade: the requester has no specific ticker and no single-name trading infrastructure today. Infrastructure cost must be flagged, not auto-reject.
5. Let the research run fully — expect 5–15 minutes of tool calls.
6. After output: triage the ranked list, promote top 1–3 candidates into the candidate pipeline for the quarterly methodology review.

---

---PROMPT START---

# Role
You are a senior quantitative-finance research analyst running a structured systematic review with replication audit, modelled on PRISMA 2020 but adapted for empirical asset-pricing research. You will search published academic literature, working papers, and replication studies to identify **cross-sectional single-name equity signal candidates** that fill targeted gaps in an existing evidence-graded trading-variable framework. Every candidate must be deployable on a defined equity universe (e.g., S&P 500, Russell 1000, MSCI World Large Cap, CRSP common stocks). Your output must be decision-ready: each candidate must produce a concrete answer of the form "on universe X at today's close, signal Y ranks stocks to LONG_TOP_DECILE and SHORT_BOTTOM_DECILE (or LONG_ONLY_TOP_QUINTILE)."

# Task

Identify, evaluate, and rank **5–7 cross-sectional single-name equity signal candidates** that fill targeted gaps in the existing framework. Every candidate must be a **CROSS_SECTIONAL** signal that ranks individual stocks within a defined universe at a daily, weekly, or monthly frequency. Single-asset directional-timing or regime signals on indexes, commodities, or gold are OUT OF SCOPE — those belong to a separate INDEX prompt. The requester has no specific ticker or existing single-name trading infrastructure. The deliverable is research-grade: flag infrastructure cost explicitly but do not auto-reject candidates that require single-name execution.

## Mandatory coverage within the 5–7 candidates

- **≥1 Value candidate** (book-to-market refinements, earnings yield, intrinsic-value-based, residual-income, text-based value).
- **≥1 Quality candidate** (profitability, earnings quality, accruals-based, gross-profits, QMJ, operating-efficiency composites).
- **≥1 Defensive / BAB-family candidate** (low beta, low vol, BAB, idiosyncratic-vol, quality-defensive).
- **≥1 Modern-paradigm candidate** (ML / high-dim / NLP / alt-data — Gu-Kelly-Xiu, IPCA, deep-learning factor models, 10-K textual tone, satellite/card-data).
- **The 5–7 candidates must span at least 3 methodology paradigms** from {Classical-risk-premium, Option-implied, ML-or-Altdata, Structural-nowcasting, Behavioral-positioning}.
- **The 5–7 candidates must come from at least 4 distinct target gaps** (listed below).

# Context — existing framework (for overlap exclusion)

The requester operates a live trading framework with **32 evidence-graded variables across crypto and traditional assets**, organized into four groups: **S (Sentiment/Positioning)**, **T (Tactical Timing)**, **R (Regime/Risk)**, and **Overlay (regime gate)**. The framework is **overwhelmingly macro / index / crypto**. Only TWO variables currently touch single-name equities, and both are narrow. Below is the full registry. Do NOT duplicate any of these. Do NOT recommend a minor variant or re-parameterization unless you explicitly flag and justify the novelty.

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

## T — Tactical Timing (5 variables — **V010 and V026 are the only single-name touches**)

| ID | Name | Canonical source |
|---|---|---|
| V009 | Time-Series Momentum (cross-asset) | **Moskowitz, Ooi & Pedersen (2012) JFE** |
| **V010** | **Earnings revision breadth** | **I/B/E/S** |
| V014 | BTC exchange netflows | Glassnode |
| V017 | BTC ETF net flows | Bloomberg |
| **V026** | **Residual momentum (FF5-adjusted)** | **Blitz-Huij-Martens (2011)** |

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

## Structural characterization of the framework — STOCKS-relevant view

The framework is macro-heavy. Single-name cross-sectional coverage is near-zero. **Gaps below are mechanical — they are empty cells in the cross-sectional coverage matrix, not subjective claims.**

### Coverage Matrix — Factor Style × Single-Name Equity Coverage

| Factor style | Current coverage | Density |
|---|---|:---:|
| Momentum — price | V026 Residual Momentum (FF5-adjusted), Blitz-Huij-Martens 2011 | THIN |
| Momentum — earnings | V010 Earnings Revision Breadth (I/B/E/S) | THIN |
| **Value** — B/M, E/P, CF/P, intrinsic | **none** | **EMPTY** |
| **Quality** — profitability, accruals, earnings quality | **none** | **EMPTY** |
| **Size** — SMB, micro-cap | **none** | **EMPTY** |
| **Defensive / BAB / Low-vol** | **none** | **EMPTY** |
| **Investment / Asset Growth / Expected growth** | **none** | **EMPTY** |
| **Issuance / Buyback / Net Equity Issuance** | **none** | **EMPTY** |
| **Profitability** — GP/A, ROE, ROIC | **none** | **EMPTY** |
| **Short Interest / Stock-loan / Lending fee** | **none** | **EMPTY** |
| **Option-implied cross-section** — IVOL, skew, RNSkew, PIN | **none** | **EMPTY** |
| **Insider / Institutional holdings** — 13F, Form 4, ownership breadth | **none** | **EMPTY** |
| **NLP / Text** — 10-K tone, news sentiment, earnings-call tone | **none** | **EMPTY** |
| **Alt-data** — satellite, card, web-traffic, app-download | **none** | **EMPTY** |
| **ML / high-dim / neural** — GKX, IPCA, deep-learning | **none** | **EMPTY** |
| **Macro-linked betas** — CPI-beta, dollar-beta, oil-beta | **none** | **EMPTY** |

### Coverage Matrix — Methodology Paradigm × Single-Name Equity

| Paradigm | Current coverage |
|---|---|
| Reduced-form price / technical | V026 residual momentum |
| Reduced-form fundamental | V010 earnings-revision breadth |
| **Classical risk-premium (FF/HXZ/FF5/Q-factor)** | **none** |
| **Option-implied cross-section** | **none** |
| **ML / high-dim / deep-learning** | **none** |
| **NLP / text** | **none** |
| **Alt-data** | **none** |
| **Behavioral / limits-of-arbitrage** | **none** |

### Gaps derived mechanically — ranked by recovery value

1. **Value family × equities** — total empty row, highest priority in classical factors.
2. **Quality family × equities** — profitability, accruals, earnings quality all empty.
3. **Defensive / BAB / Low-vol family × equities** — empty, yet robustly replicated.
4. **Modern paradigm (ML/NLP/Alt-data) × equities** — entire row empty; next-decade-of-research is here.
5. **Option-implied cross-section** — IVOL, skew, RNSkew all empty.
6. **Short-interest / stock-loan / issuance** — documented negative-return anomalies, all absent.
7. **Insider / institutional holdings signals** — Form 4, 13F breadth, activist positioning, absent.
8. **Macro-linked cross-section (CPI-beta, inflation-beta, climate-beta)** — post-2020 literature active, absent.

**Your job is to push against this macro bias.** Candidates that merely replicate V010 or V026 will be rejected as duplicative regardless of citation quality.

# Target gaps (ranked — these feed ranking weights, not exclusion)

1. **Value-family in equities.** B/M, earnings yield, cash-flow yield, residual-income, intrinsic-value, text-derived value.
2. **Quality-family in equities.** Profitability (GP/A), QMJ, Sloan accruals, earnings quality, Piotroski F-score, operating-efficiency composites.
3. **Defensive / BAB / Low-vol.** Beta-lower-than-one anomaly, low-vol anomaly, quality-defensive composites.
4. **Modern paradigm (ML / NLP / Alt-data).** Gu-Kelly-Xiu neural networks, IPCA (Kelly-Pruitt-Su), deep-learning factor models, 10-K textual tone, earnings-call tone, news sentiment, satellite/card/web-traffic data.
5. **Option-implied cross-section.** IVOL, skew, risk-neutral skew, put-call imbalance, Bali-Cakici-Whitelaw lottery/MAX.
6. **Short-interest / stock-loan / issuance.** Short-interest ratio, utilization, lending fee, net-equity-issuance anomaly, buyback anomaly.
7. **Insider / institutional holdings.** Form 4 insider buys, 13F breadth, active-ownership concentration, hedge-fund crowding.
8. **Macro-linked cross-section.** CPI-beta portfolios, inflation-beta, dollar-beta, climate-risk-beta.

# Must-evaluate seed candidates

For each seed below: locate the canonical source, apply inclusion/exclusion criteria, and either include in the final short-list OR exclude with explicit reason. Do NOT skip seeds silently.

## Classical risk-premium family

- **Fama-French (2015) "A Five-Factor Asset Pricing Model," JFE** — FF5 (market, size, value, profitability, investment).
- **Hou-Xue-Zhang (2015) "Digesting Anomalies: An Investment Approach," RFS** — Q-factor model.
- **Novy-Marx (2013) "The Other Side of Value: The Gross Profitability Premium," JFE** — GP/A.
- **Asness-Frazzini-Pedersen (2019) "Quality Minus Junk," RoF** — QMJ.
- **Frazzini-Pedersen (2014) "Betting Against Beta," JFE** — BAB.
- **Asness-Frazzini (2013) "The Devil in HML's Details," JoPM** — HML-Devil (timely B/M).
- **Piotroski (2000) "Value Investing: The Use of Historical Financial Statement Information," JAR** — F-score.
- **Sloan (1996) "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows?" AR** — accruals anomaly.

## Option-implied cross-section

- **Bali-Cakici-Whitelaw (2011) "Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns," JFE** — MAX.
- **Ang-Hodrick-Xing-Zhang (2006) "The Cross-Section of Volatility and Expected Returns," JF** — IVOL anomaly.
- **Conrad-Dittmar-Ghysels (2013) "Ex Ante Skewness and Expected Stock Returns," JF** — risk-neutral skew.
- **Cremers-Weinbaum (2010) "Deviations from Put-Call Parity and Stock Return Predictability," JFQA**.

## Modern paradigm — ML / NLP / Alt-data

- **Gu-Kelly-Xiu (2020) "Empirical Asset Pricing via Machine Learning," RFS** — neural-net benchmark.
- **Kelly-Pruitt-Su (2019) "Characteristics are Covariances: A Unified Model of Risk and Return," JFE** — IPCA.
- **Chen-Pelger-Zhu (2023) "Deep Learning in Asset Pricing," MS** — deep-factor model.
- **Loughran-McDonald (2011) "When is a Liability Not a Liability?" JF** — 10-K textual tone, LM dictionary.
- **Tetlock (2007) "Giving Content to Investor Sentiment," JF** — news sentiment cross-section.
- **Cohen-Malloy-Nguyen (2020) "Lazy Prices," JF** — 10-K changes / text similarity.
- **Froot-Kang-Ozik-Sadka (2017) "What Do Measures of Real-Time Corporate Sales Say About Earnings Surprises?" JFE** — alt-data / card.
- **Katona-Painter-Patatoukas-Zeng (2021, WP) "On the Capital Market Consequences of Alternative Data: Evidence from Outer Space"** — satellite.

## Short-interest / stock-loan / issuance / behavioral

- **Boehme-Danielsen-Sorescu (2006) "Short-Sale Constraints, Differences of Opinion, and Overvaluation," JFQA**.
- **Cohen-Diether-Malloy (2007) "Supply and Demand Shifts in the Shorting Market," JF** — utilization/fee.
- **Daniel-Titman (2006) "Market Reactions to Tangible and Intangible Information," JF** — net-equity-issuance.
- **Ikenberry-Lakonishok-Vermaelen (1995) "Market Underreaction to Open Market Share Repurchases," JFE** — buyback anomaly.

## Insider / institutional / holdings

- **Cohen-Malloy-Pomorski (2012) "Decoding Inside Information," JF** — Form 4 insider trades.

## Macro-linked cross-section

- **Boons-Duarte-de Roon-Szymanowska (2020) "Time-Varying Inflation Risk and Stock Returns," JFE** — inflation-beta portfolios.
- **Bolton-Kacperczyk (2021) "Do Investors Care About Carbon Risk?" JFE** — climate-beta.

# Methodology

## Step 1 — Search strategy
- **Tier 1 journals:** JF, JFE, RFS.
- **Tier 2 journals:** JFQA, RAPS, FAJ, JPM, Management Science, JOIM, JBF, Accounting Review, JAR.
- **Working papers:** NBER, SSRN top-downloaded in JEL G11, G12, G14, G17, M41.
- **Time range:** 1995–present, prioritize 2010+ and 2015+ replications. Pay particular attention to Jensen-Kelly-Pedersen 2023 "Is There a Replication Crisis in Finance?" as the replication benchmark.
- **Keyword sets:** [cross-section of expected stock returns] OR [profitability premium gross profits] OR [quality minus junk] OR [betting against beta low volatility] OR [machine learning asset pricing] OR [IPCA characteristics covariances] OR [10-K textual analysis sentiment] OR [short interest lending fee utilization] OR [Form 4 insider trading returns] OR [accruals earnings quality cross section] OR [inflation beta climate beta cross section] OR [alternative data satellite card earnings].

## Step 2 — Inclusion criteria (all must be met)
1. Peer-reviewed in a ranked journal OR NBER/SSRN working paper with ≥100 citations AND ≥1 independent replication.
2. Independently replicated (McLean-Pontiff 2016, Hou-Xue-Zhang 2020, Chen-Zimmermann 2022, Jensen-Kelly-Pedersen 2023 all count).
3. Mechanism-grounded — specific economic, behavioral, or informational channel.
4. Real-time implementable at daily or monthly frequency.
5. Cross-sectional in nature — produces a ranking over a defined equity universe.
6. Independent of V010 and V026. Correlation with V026 residual momentum must be below |0.5| in at least one published comparison, OR the paradigm/mechanism must be distinct.

## Step 3 — Exclusion criteria
- Pure factor-zoo mass-screening without mechanism.
- Factors failing Hou-Xue-Zhang 2020 OR Jensen-Kelly-Pedersen 2023 replication benchmarks.
- Proprietary non-public data with no vendor path.
- Forecast-of-fundamentals dependencies not independently published (raw sell-side target prices).
- In-sample Sharpe exceeds OOS Sharpe by >60%.
- **Index-directional, commodity, gold, or FX signals.** These belong to a separate INDEX prompt.
- Signals specific to a single country/decade without cross-sample validation (pre-1990 US-only, single-industry single-period).

## Step 4 — Extraction schema per candidate

| Field | Description |
|---|---|
| **Candidate ID** | CAND-01, CAND-02, etc. |
| **Signal type** | CROSS_SECTIONAL (all candidates in this prompt). |
| **Factor name** | Human-readable |
| **Primary citation** | Author(s) (year) "Title," Journal, Volume(Issue): pages. DOI if available. |
| **Replication citations** | Independent replications. |
| **Universe** | S&P 500 / Russell 1000 / Russell 2000 / Russell 3000 / MSCI World Large Cap / CRSP common stocks NYSE-AMEX-NASDAQ / other. Specify. |
| **Portfolio construction** | Quintile / decile / long-short / long-only top-quintile. Weighting (equal, value, rank-weighted). Rebalance frequency. |
| **Target gap filled** | Which of the 8 gaps |
| **Mechanism** | 1–2 sentences — specify economic, behavioral, or informational channel. |
| **Signal construction** | Exact formula/procedure in 3–8 lines. No pseudo-code. |
| **Data requirements** | Inputs, frequency, vendor/source, cost. Specify Compustat / CRSP / I/B/E/S / Option Metrics / Ravenpack / Markit / Alt-data vendor. |
| **Infrastructure required** | SINGLE_NAME_UNIVERSE (all candidates) + one of: FUNDAMENTALS_FEED / OPTIONS_CHAIN / STOCK_LOAN_FEED / NLP_TEXT_FEED / ALT_DATA_FEED / NONE_STANDARD_DATA. |
| **Effect size (in-sample)** | Spread long-minus-short: Sharpe, t-stat, monthly alpha vs FF3/FF5/Q5. Exact numbers. |
| **Effect size (OOS)** | Post-publication OOS Sharpe. "NO_OOS_EVIDENCE" if none. |
| **Sharpe decay** | In-sample minus OOS. Flag >60%. Reference Jensen-Kelly-Pedersen 2023 if applicable. |
| **Real-time implementability** | HIGH / MEDIUM / LOW. Flag point-in-time (PIT) data availability if fundamental. |
| **Executability check** | "On universe [X] at today's close, this signal ranks to LONG_TOP_DECILE [sector/region characteristics] and SHORT_BOTTOM_DECILE [sector/region characteristics]." Concrete description of top/bottom portfolios expected today, not a historical backtest. |
| **Correlation with V026 Residual Momentum** | Cite or "NOT_REPORTED." |
| **Correlation with V010 Earnings Revision Breadth** | Cite or "NOT_REPORTED." |
| **Correlation with other candidates in this short-list** | Flag \|ρ\| > 0.5 pairs. |
| **Capacity / crowding** | AUM estimate, crowding indicators. Smart-beta AUM flag if applicable. |
| **Recommended Grade** | A / B / C |
| **Recommended group** | S / T / R / Overlay. (Most cross-sectional signals enter T. Flag if Overlay or S is more appropriate.) |
| **Methodology paradigm** | Classical-risk-premium / Option-implied / ML-or-Altdata / Structural-nowcasting / Behavioral-positioning |
| **Confidence** | HIGH / MEDIUM / LOW |
| **Why it fills a gap** | 2–3 sentences referencing specific empty cells in the cross-sectional matrices above. |
| **Risk of adoption** | 1–2 sentences on crowding, post-publication decay, regime dependence (value drawdown 2017–2020), data fragility. |
| **Infrastructure cost** | ESTIMATED_LOW (<$5K/yr) / MEDIUM ($5K–$50K/yr) / HIGH (>$50K/yr). Research-grade — flag cost, do not auto-reject. |
| **Deployability timeline** | IMMEDIATE (≤4 weeks, paper-trade) / NEAR (4–12 weeks) / MEDIUM (3–12 months) / LONG (>12 months). |

## Step 5 — Ranking

**Hard bucket minimum:** 5–7 candidates, all CROSS_SECTIONAL, spanning ≥3 paradigms and ≥4 target gaps. Mandatory slots: Value (≥1), Quality (≥1), Defensive/BAB (≥1), Modern-paradigm ML/NLP/Alt-data (≥1).

**Ranking weights:**
- 30% — Grade A/B likelihood and replication strength (Jensen-Kelly-Pedersen 2023 survivor)
- 25% — Gap priority (earlier gap outranks later)
- 15% — Orthogonality to existing V010 / V026 and to other short-listed candidates
- 10% — Post-publication OOS preservation (lower Sharpe decay preferred)
- 10% — Paradigm diversification bonus (modern-paradigm slot underweight-corrected)
- 5% — Infrastructure cost (LOW preferred but not auto-reject)
- 5% — Executability check concreteness

**Tie-break:** if two candidates match on weighted score, prefer the one that covers a mandatory slot not yet filled.

## Step 6 — Deliverable structure

1. **Executive Summary** (one paragraph). Top 3 candidates named with one-line rationale. Which cross-sectional gaps close. Expected time-to-paper-trade. Infrastructure cost range.
2. **Search Log.** Journals, keywords, PRISMA-style flow counts. Seed Disposition Table for all ~25 seeds (INCLUDED / EXCLUDED / PARTIAL + reason).
3. **Ranked Candidate Table.** Full extraction schema (Step 4) for each candidate, top-ranked first.
4. **Gap Coverage Matrix.** 8 × N_candidates showing which gap each fills. Flag uncovered gaps explicitly.
5. **Paradigm Diversification Check.** Paradigm count; confirm ≥3 paradigms represented.
6. **Mandatory-slot Check.** Confirm Value, Quality, Defensive/BAB, Modern-paradigm slots each filled.
7. **Correlation / Orthogonality Analysis.** Reported correlation with V010 / V026. Flag \|ρ\| > 0.5 pairs within short-list.
8. **Replication-Audit Summary.** Per candidate: who replicated, when, OOS window, Sharpe preserved, caveats. Explicitly reference Jensen-Kelly-Pedersen 2023 status (survivor / not-tested / flagged).
9. **Infrastructure & Data Summary.** Per candidate: what vendor feed is required, point-in-time caveats, estimated annual cost, whether vendor supplies daily PIT fundamentals or accounting lag must be managed.
10. **Registration Recommendations.** Per top candidate: registry ID (V029, V030, V031 sequential), Grade, group (S/T/R/Overlay), OOS tracking period, universe to paper-trade over.
11. **Gaps Still Unfilled.** Explicit "NO_QUALIFYING_CANDIDATE" where applicable.
12. **Suggested Next Steps.** Which candidate(s) enter OOS paper-trade ledger within 4–12 weeks. Which need further evidence. Whether a dedicated sub-review is warranted (e.g., "dedicated ML asset-pricing deep-dive," "dedicated textual-NLP review"). Flag infrastructure build requirements.

# Hard rules

- No uncited claims.
- No invented citations.
- No factor-zoo laundering.
- No duplication with V010 or V026 — flag variants explicitly.
- No Grade-A claim without independent replication passing Jensen-Kelly-Pedersen 2023 OR Hou-Xue-Zhang 2020.
- No overconfident OOS claims — use "NO_OOS_EVIDENCE" where unknown.
- Respect confidence flags — LOW stays LOW.
- Fail loud on gaps — "NO_QUALIFYING_CANDIDATE" per gap as needed.
- No silent seed skipping — every seed in the Seed Disposition Table with reason.
- **No index-directional, commodity, gold, or FX signals.** These are out of scope for this prompt.
- **Every candidate must be CROSS_SECTIONAL.** Long-short or long-only top-quintile/decile. No market-timing, no single-asset directional.
- Every candidate must produce a concrete Executability Check description of today's long and short portfolio characteristics.
- **Print this header before your output:**
  `RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = STOCKS_ONLY_CROSS_SECTIONAL; MIN_CANDIDATES = 5-7; MANDATES = VALUE + QUALITY + DEFENSIVE_BAB + MODERN_PARADIGM_ML_NLP_ALTDATA; PARADIGM_MIN = 3_OF_5; TARGET_GAP_MIN = 4_OF_8.`

# Output expectations

- Length: 2,500–5,000 words.
- Tone: analytical, skeptical, concrete. No marketing language.
- Format: as specified in Step 6. Use tables where schema calls for them.
- Citations: inline parenthetical + full reference list.

---PROMPT END---

---

## Post-research actions

1. Triage the ranked table. Reject LOW confidence or high-overlap candidates. Sanity-check against Jensen-Kelly-Pedersen 2023 survivor list.
2. Verify top 3. Independently confirm primary citation + replication citation for each.
3. Register. Promote 1–3 to candidate pipeline. Assign V029+ IDs.
4. Paper-trade. Add to OOS SignalLedger for 12–18 months of hypothetical cross-sectional tracking before infrastructure build.
5. Infrastructure decision. Only after 12+ months of OOS evidence should single-name execution infrastructure (single-stock brokerage, options account, data feeds, rebalance automation) be scoped.
6. Re-BNMA cadence: late 2027 / early 2028 once 2–3 new candidates have 12+ months of OOS evidence.
