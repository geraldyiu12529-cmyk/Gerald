RESEARCH_MODE = SYSTEMATIC_REVIEW_WITH_REPLICATION_AUDIT; SCOPE = EQUITY_INDEX_AND_STOCK_GAP_FILL; BUCKETS = INDEX(3+) + STOCKS(3+); ASSET_CLASSES = EQUITY_INDEX + SINGLENAME_EQUITY; PARADIGM_MINS = OPTION_IMPLIED + ML_OR_TEXT + STRUCTURAL_NOWCASTING.

## 1. Executive Summary

The highest-value **INDEX** additions are: **(1) SPX variance risk premium / SVIX-style premium capture**, because it directly fills the missing variance-premium cell and is publicly implementable from options-implied volatility plus realized-volatility estimates, although recent replication audits force a downgrade from “easy Grade A” to **Grade B**; **(2) a real-time macro-surprise / nowcast gate** built around Scotti-style surprise aggregation plus ADS/GDPNow-type activity tracking, because it is genuinely orthogonal to your current yield-curve / real-yield / NFCI macro stack and is operationally near-immediate; and **(3) an SPX/SPY downside-skew demand scalar**, because it adds tail-demand asymmetry that your VIX-level and VIX-term-structure overlays do not capture. The highest-value **STOCKS** additions are: **(1) gross profitability**, the cleanest replicated quality/profitability sleeve; **(2) BAB / low-beta defensive equities**, which remains one of the stronger “defensive” stock constructions, though weaker than headline claims once overlap is controlled; and **(3) firm-level financial-text negativity** (Tetlock / Loughran-McDonald lineage), which is the best verified route into the missing NLP/text sleeve. Net result: three index candidates can enter an OOS ledger immediately or within weeks; the stock sleeve requires infrastructure but now has an evidence-first build order.

## 2. Search Log

### Search scope and process

**Databases / sources searched.** Tier-1 and Tier-2 journal pages, NBER, EconPapers, FRED, Philadelphia Fed, policyuncertainty.com, JKP Global Factor Data, Hou-Xue-Zhang replication materials, and Reuters / CBOE-adjacent market-data pages for current executability checks. Replication context was anchored to **McLean-Pontiff (2016)**, **Hou-Xue-Zhang (2020)**, and **Jensen-Kelly-Pedersen (2023)**.

**Keyword families actually run.** Variance risk premium, SVIX, skew, tail risk, implied correlation, dealer gamma, macro surprise, ADS, GDPNow, policy uncertainty, profitability, QMJ, BAB, textual tone, firm news sentiment, machine learning asset pricing, and IPCA. The screen emphasized 2000–present, with heavy weight on 2010+ publications and post-2015 replication or extension evidence.

**PRISMA-style flow for this review pass.**
- Records identified from search: **~50**
- Abstract / snippet screen: **~30**
- Full-text / official-page review: **17**
- Passed inclusion: **7 finalists + 4 partial / reserve candidates**
These counts are approximate because the review mixed journal pages, data pages, and replication databases in one pass.

### Replication databases consulted

- **McLean & Pontiff (2016)** for post-publication decay.
- **Hou, Xue, Zhang (2020)** for anomaly replication discipline.
- **Jensen, Kelly, Pedersen (2023)** and the **JKP Global Factor Data** documentation for broader replication context and factor mapping.
- **Goyal, Welch, Zafirov (2024)** for equity-premium-predictor re-audit, especially around SVIX / variance-premium claims.

### Seed-candidate disposition

| Seed candidate | Disposition | Reason |
|---|---:|---|
| Variance risk premium / SVIX | INCLUDED | Strong gap fit; public implementation feasible; replication survives but is less clean than headline claims |
| SPX skew / tail-risk demand | INCLUDED | Good orthogonality vs VIX level/curve; public proxies available |
| Dispersion / implied correlation | PARTIAL | Good literature, but near-term deployment needs richer options-surface infrastructure |
| Dealer gamma exposure | EXCLUDED | Public proxies exist, but reproducibility and stable nonproprietary construction are not yet strong enough |
| Macro surprise indices | INCLUDED | Strong structural-nowcasting fit, daily public data feasible |
| ADS / macro-nowcasting DFM | INCLUDED | Same as above; rolled into macro-nowcast composite |
| Leveraged-ETF / vol-target rebalances | EXCLUDED | More episodic price-pressure literature than stable, registrable close signal |
| EPU | INCLUDED (low confidence) | Valid behavioral/regime candidate, but current-data presentation is noisier than ideal |
| Gross profitability | INCLUDED | Best-supported quality/profitability sleeve |
| QMJ | PARTIAL | Strong paper, but too overlapping with profitability + BAB to make the final shortlist |
| BAB | INCLUDED | Strong defensive gap filler |
| Devil in HML’s Details | PARTIAL | Important value refinement, but classical-paradigm cap and weaker timing utility kept it out |
| Sloan accruals | EXCLUDED | Replication weakened in later anomaly audits |
| Loughran-McDonald text | INCLUDED | Publicly implementable NLP/text route |
| Tetlock firm-news sentiment | INCLUDED | Strong cross-sectional text-return evidence |
| Gu-Kelly-Xiu ML | PARTIAL | Important research area, but replication / registry-standard implementation remains less settled than the text sleeve |
| IPCA | PARTIAL | Elegant research candidate, but not strong enough for final shortlist under the inclusion bar |

## 3. INDEX BUCKET — Ranked Table

| Rank | Candidate ID | Factor name | Paradigm | Grade | Deployability | Verdict at latest close |
|---|---|---|---|---|---|---|
| 1 | CAND-01 | SPX variance risk premium / SVIX-style premium capture | Option-implied | B | IMMEDIATE / NEAR | **FLAT** |
| 2 | CAND-02 | Real-time macro surprise / nowcast gate | Structural-nowcasting | B | IMMEDIATE / NEAR | **LONG, size 0.75** |
| 3 | CAND-03 | SPX/SPY downside-skew demand scalar | Option-implied | B/C | IMMEDIATE / NEAR | **LONG, size 0.75** |
| 4 | CAND-04 | U.S. economic policy uncertainty regime gate | Behavioral-positioning | C | IMMEDIATE | **FLAT / size 0.50** |

### CAND-01 — SPX variance risk premium / SVIX-style premium capture

- **Bucket:** INDEX
- **Signal type:** DIRECTIONAL_TIMING / SIZING_SCALAR
- **Primary citation:** Bollerslev, Tauchen, Zhou (2009), *Expected Stock Returns and Variance Risk Premia*, *RFS*; Martin (2017), *What Is the Expected Return on the Market?*, *QJE*.
- **Replication citations:** Bekaert & Hoerova (2014); Goyal, Welch, Zafirov (2024).
- **Asset-class coverage:** Equity index
- **Target gap filled:** Index gap #1, variance / volatility risk premium
- **Mechanism:** Options embed compensation investors pay to shed variance / crash exposure; when implied variance exceeds expected realized variance, the premium can proxy for required equity compensation.
- **Signal construction:**
  1. Compute 1-month model-free implied variance on SPX or use squared VIX as public proxy.
  2. Subtract forecast realized variance over matching horizon.
  3. Standardize versus trailing history.
  4. Long index when VRP is sufficiently positive; flat / underweight when near zero or negative.
- **Data requirements:** SPX options or VIX; daily SPX / SPY returns; public proxy feasible via CBOE/FRED.
- **Infrastructure required:** OPTIONS_CHAIN or public VIX proxy
- **Effect size (in-sample):** Original papers report meaningful predictive power.
- **Effect size (OOS):** Mixed-positive, weaker than headline.
- **Sharpe decay:** Present; enough to block Grade A, not enough to exclude.
- **Real-time implementability:** **HIGH** with proxy; **MEDIUM-HIGH** if full model-free variance is required
- **Executability check — INDEX:** Using a public proxy, SPY closed about **710.1** on April 17, 2026, while VIX fell to **17.94 on April 16** and **17.48 on April 17**. A rough 21-trading-day realized-vol estimate from FRED S&P 500 closes is about **19.8% annualized**, slightly above mid-April implied vol, so the plain IV-minus-RV proxy is **not currently positive**. **Recommendation at today’s close: FLAT on SPY**.
- **Correlation with V009 TSMOM:** **NOT_REPORTED**
- **Correlation with other candidates:** Moderate conceptual overlap with CAND-03 because both are option-implied; low overlap with existing VIX-level / curve variables because this is a **premium** construct, not a level/slope construct.
- **Recommended Grade:** **B**
- **Recommended group:** **S**
- **Methodology paradigm:** Option-implied
- **Confidence:** **MEDIUM**
- **Why it fills a gap:** Your framework has VIX level and curve-state overlays but no direct estimate of the compensation embedded in equity-volatility insurance. This is the cleanest missing index-premium cell.
- **Risk of adoption:** Public VIX proxies can mismeasure the full signal; replication audits show the premium is real but not bulletproof.
- **Deployability timeline:** **IMMEDIATE** with proxy; **NEAR** with a cleaner SPX-options implementation.

### CAND-02 — Real-time macro surprise / nowcast gate

- **Bucket:** INDEX
- **Signal type:** REGIME_GATE / OVERLAY_COMBO
- **Primary citation:** Scotti (2016), *Surprise and Uncertainty Indexes*, *JME*; Aruoba, Diebold, Scotti (2009) / Philadelphia Fed ADS index.
- **Replication citations:** Institutional adoption of ADS / GDPNow / surprise-index style nowcasting as macro state trackers; the Philadelphia Fed and Atlanta Fed both maintain live nowcast systems.
- **Asset-class coverage:** Equity index
- **Target gap filled:** Index gap #3, macro-nowcasting / structural equity-premium predictors
- **Mechanism:** Equity-index returns respond not just to macro level, but to the **surprise component** of incoming data and real-time growth updates relative to priors.
- **Signal construction:**
  1. Standardize a daily U.S. surprise index.
  2. Combine with a high-frequency activity nowcast (ADS / GDPNow / equivalent).
  3. Trade long only when both are positive or when surprise is positive and activity is not recessionary.
  4. Use as a regime gate, not as a stand-alone forecast.
- **Data requirements:** Public macro-release calendar; Scotti/Citi-style surprise index; ADS page; GDPNow; manufacturing / claims / payroll updates.
- **Infrastructure required:** NONE_STANDARD_DATA
- **Effect size (in-sample):** Meaningful in paper and institutional practice, but more powerful as a gate / allocator than as an isolated equity-premium model.
- **Effect size (OOS):** Reasonable, with lower model-risk than many academic predictors because inputs are observable in real time.
- **Sharpe decay:** Not the key issue; this is mainly a **state filter**.
- **Real-time implementability:** **HIGH**
- **Executability check — INDEX:** Latest public nowcast-style evidence is positive enough for risk-on but not for maximum size: Atlanta Fed **GDPNow was 1.3% for 2026:Q1** on April 9, the Philadelphia Fed’s latest ADS vintage was updated April 16, and current U.S. surprise measures were modestly positive, around **9–12** in mid-April. **Recommendation: LONG SPY, size 0.75**.
- **Correlation with V009 TSMOM:** **NOT_REPORTED**
- **Correlation with other candidates:** Low with pure option-implied candidates; lower still with your existing yield-curve / real-yield / term-premium stack because this is a **mixed-frequency real-time** signal.
- **Recommended Grade:** **B**
- **Recommended group:** **Overlay**
- **Methodology paradigm:** Structural-nowcasting
- **Confidence:** **MEDIUM-HIGH**
- **Why it fills a gap:** This is the cleanest genuinely new macro method in the review: not another slow macro level, but a real-time update engine.
- **Risk of adoption:** Surprise signals can flip fast and whipsaw when the market is already pricing strong data.
- **Deployability timeline:** **IMMEDIATE**

### CAND-03 — SPX/SPY downside-skew demand scalar

- **Bucket:** INDEX
- **Signal type:** SIZING_SCALAR / REGIME_GATE
- **Primary citation:** Gârleanu, Pedersen, Poteshman (2009) and Kelly-Jiang (2014) on tail risk; operational public proxy via CBOE SKEW / 25-delta put-call skew.
- **Replication citations:** Tail-risk literature is broad, and Kelly-Jiang’s measure is strongly linked to aggregate returns; public skew proxies are widely used as practical tail-demand state variables.
- **Asset-class coverage:** Equity index
- **Target gap filled:** Index gap #2, option-implied directional / defensive signals
- **Mechanism:** Index downside skew prices the market’s willingness to overpay for crash protection; that price can be used as a defensive scalar or expected-return proxy.
- **Signal construction:**
  1. Use CBOE SKEW or 25-delta put IV minus 25-delta call IV.
  2. Z-score against a 1y or 3y history.
  3. High-and-rising skew = cut gross exposure; high-but-falling skew = allow longs, but not max size.
  4. Low skew = remove defensive haircut.
- **Data requirements:** Public SKEW or SPY options skew; daily frequency; low cost.
- **Infrastructure required:** OPTIONS_CHAIN or public SKEW feed
- **Effect size (in-sample):** Supportive but not as clean as VRP.
- **Effect size (OOS):** Partial / operational rather than pristine. Better as a risk scalar than a naked directional predictor.
- **Sharpe decay:** Unknown in clean standalone form.
- **Real-time implementability:** **HIGH**
- **Executability check — INDEX:** CBOE SKEW was about **141.82** on April 17, 2026, above the year-ago **130.02**, while SPY 25-delta put IV exceeded call IV by roughly **3.8 vol points**. However, one-month put-call skew had fallen sharply from March stress levels. **Recommendation: LONG SPY, size 0.75**.
- **Correlation with V009 TSMOM:** **NOT_REPORTED**
- **Correlation with other candidates:** Moderate overlap with CAND-01 because both use option markets; low overlap with VIX-curve slope because skew is about **asymmetry**, not term structure.
- **Recommended Grade:** **B/C**
- **Recommended group:** **R / Overlay**
- **Methodology paradigm:** Option-implied
- **Confidence:** **MEDIUM**
- **Why it fills a gap:** This is the missing crash-asymmetry cell. Your current overlay stack sees “how much vol” and “what vol curve shape,” but not “how much people are paying for the left tail specifically.”
- **Risk of adoption:** Tail hedging can remain expensive for long periods; timing with skew alone is weak.
- **Deployability timeline:** **IMMEDIATE**

### CAND-04 — U.S. economic policy uncertainty regime gate

- **Bucket:** INDEX
- **Signal type:** REGIME_GATE
- **Primary citation:** Baker, Bloom, Davis (2016), *QJE*.
- **Replication citations:** Later work finds nonlinearity and regime dependence; the series remains maintained and widely used.
- **Asset-class coverage:** Equity index
- **Target gap filled:** Index gap #6, sentiment / attention / policy uncertainty
- **Mechanism:** Elevated policy uncertainty raises discount rates, widens tails, and reduces confidence in fundamental mapping.
- **Signal construction:**
  1. Use monthly or daily U.S. EPU.
  2. Apply a nonlinear threshold: only the upper tail matters.
  3. Use elevated EPU to haircut new long risk rather than to force outright shorts.
- **Data requirements:** Public EPU series; daily and monthly variants are available.
- **Infrastructure required:** NONE_STANDARD_DATA
- **Effect size (in-sample):** Real but regime-dependent.
- **Effect size (OOS):** Modest; better as overlay than core predictor.
- **Sharpe decay:** Likely material.
- **Real-time implementability:** **HIGH**
- **Executability check — INDEX:** Monthly U.S. EPU was about **260.1 in March 2026**, and Federal Reserve Governor Waller referred on April 17 to policy-uncertainty indexes having risen to elevated levels. **Recommendation: FLAT for new incremental SPY risk, or size 0.50 inside a broader long stack.**
- **Correlation with V009 TSMOM:** **NOT_REPORTED**
- **Correlation with other candidates:** Moderate overlap with your broader risk regime variables, but not a duplicate because it is text/news-policy specific.
- **Recommended Grade:** **C**
- **Recommended group:** **Overlay**
- **Methodology paradigm:** Behavioral-positioning
- **Confidence:** **LOW-MEDIUM**
- **Why it fills a gap:** It gives the framework a policy-news attention channel that is currently absent.
- **Risk of adoption:** Data presentation can be noisy; high uncertainty does not always mean negative next-month returns.
- **Deployability timeline:** **IMMEDIATE**

## 4. STOCKS BUCKET — Ranked Table

| Rank | Candidate ID | Factor name | Paradigm | Grade | Deployability | Research verdict |
|---|---|---|---|---|---|---|
| 1 | CAND-05 | Gross profitability | Classical risk premium | A | MEDIUM | Build first |
| 2 | CAND-06 | Betting Against Beta (BAB) | Classical risk premium | B | MEDIUM | Build second |
| 3 | CAND-07 | Firm-level financial-text negativity | ML-or-Text | B | MEDIUM / LONG | Build third |

### CAND-05 — Gross profitability

- **Bucket:** STOCKS
- **Signal type:** CROSS_SECTIONAL
- **Primary citation:** Novy-Marx (2013), *The Other Side of Value: The Gross Profitability Premium*, *JFE*.
- **Replication citations:** Fama-French (2015) effectively embed profitability into the five-factor model; later replication-oriented work finds profitability among the more durable characteristic families.
- **Asset-class coverage:** Single-name equity
- **Target gap filled:** Stocks gap #2, quality / profitability
- **Mechanism:** More profitable firms appear underpriced relative to persistent earnings power; profitability proxies quality and capital allocation discipline.
- **Signal construction:**
  1. Gross profits = revenue minus cost of goods sold.
  2. Divide by total assets.
  3. Rank within a large liquid universe.
  4. Long top decile / short bottom decile, monthly or quarterly rebalance after filing lag.
- **Data requirements:** CRSP + Compustat or equivalent; monthly ranking; filing-lag discipline.
- **Infrastructure required:** SINGLE_NAME_UNIVERSE
- **Effect size (in-sample):** Strong in original study.
- **Effect size (OOS):** Relatively durable versus many other accounting anomalies.
- **Sharpe decay:** Manageable; not enough to overturn inclusion.
- **Real-time implementability:** **MEDIUM** because of filing lags, but straightforward once data engineering exists
- **Executability check — STOCKS:** On a **500-stock U.S. universe**, **long top decile / short bottom decile**, monthly rebalance, minimum **25–50 names per side**, moderate turnover, strict lagging of accounting data.
- **Correlation with V009 / V026:** **NOT_REPORTED** specifically; conceptually orthogonal to trend and residual momentum.
- **Correlation with other candidates:** High conceptual overlap with QMJ, hence QMJ was not separately shortlisted.
- **Recommended Grade:** **A**
- **Recommended group:** **Cross-sectional equity sleeve**
- **Methodology paradigm:** Classical-risk-premium
- **Confidence:** **HIGH**
- **Why it fills a gap:** This is the cleanest missing stock-quality sleeve and the most defensible first build after momentum.
- **Risk of adoption:** Crowding and stale accounting data can compress spreads.
- **Deployability timeline:** **MEDIUM**
- **Infrastructure-cost estimate:** Requires CRSP/Compustat-style data, portfolio-construction stack, and lag-safe accounting joins; this is not trivial retail infrastructure and usually means institutional or academic-style data licensing plus **4–8 weeks** engineering.

### CAND-06 — Betting Against Beta (BAB)

- **Bucket:** STOCKS
- **Signal type:** CROSS_SECTIONAL / DEFENSIVE
- **Primary citation:** Frazzini, Pedersen (2014), *Betting Against Beta*, *JFE*.
- **Replication citations:** Strong literature recognition, but later work shows overlap with quality can absorb part of the headline alpha. A recent study reports the beta anomaly becomes much weaker after augmenting with QMJ.
- **Asset-class coverage:** Single-name equity
- **Target gap filled:** Stocks gap #3, defensive / low-vol / BAB
- **Mechanism:** Constrained investors overpay for high-beta assets; low-beta assets become relatively underpriced.
- **Signal construction:**
  1. Estimate beta to market on rolling window.
  2. Rank universe by beta.
  3. Go long low-beta sleeve, short high-beta sleeve, optionally leverage to beta-neutralize.
  4. Rebalance monthly.
- **Data requirements:** Daily returns, robust beta estimation, portfolio leverage and beta-neutralization logic.
- **Infrastructure required:** SINGLE_NAME_UNIVERSE
- **Effect size (in-sample):** Strong in original paper.
- **Effect size (OOS):** Positive but less isolated once overlap with quality is controlled.
- **Sharpe decay:** Meaningful; enough to keep it at **B**, not **A**.
- **Real-time implementability:** **MEDIUM**
- **Executability check — STOCKS:** On a **500-stock liquid U.S. universe**, **long bottom beta decile / short top beta decile**, monthly rebalance, minimum **30 names per side**, turnover moderate, beta-neutralize at portfolio level.
- **Correlation with V009 / V026:** **NOT_REPORTED** specifically
- **Correlation with other candidates:** Material overlap with QMJ / profitability-defense composites; this is why QMJ was left out of the final set.
- **Recommended Grade:** **B**
- **Recommended group:** **Cross-sectional equity sleeve**
- **Methodology paradigm:** Classical-risk-premium
- **Confidence:** **MEDIUM**
- **Why it fills a gap:** It fills the missing defensive / low-risk sleeve without duplicating stock momentum.
- **Risk of adoption:** Can require leverage or beta balancing that is operationally messy for small accounts; alpha may be partly a quality proxy.
- **Deployability timeline:** **MEDIUM**
- **Infrastructure-cost estimate:** Same data stack as profitability plus beta-estimation / risk model; **4–8 weeks** engineering, plus live borrow / shorting / leverage rules.

### CAND-07 — Firm-level financial-text negativity

- **Bucket:** STOCKS
- **Signal type:** CROSS_SECTIONAL / NLP-TEXT
- **Primary citation:** Tetlock, Saar-Tsechansky, Macskassy (2008), *More Than Words*, *JF*.
- **Replication citations:** Loughran-McDonald (2011) show generic dictionaries misclassify financial language and provide a finance-specific lexicon tied to 10-K returns and related market outcomes; later text literature continues to find predictive content in financial text.
- **Asset-class coverage:** Single-name equity
- **Target gap filled:** Stocks gap #5, text / NLP sentiment
- **Mechanism:** Investors underreact to negative qualitative information, especially when text contains fundamentals-relevant adverse information.
- **Signal construction:**
  1. Ingest firm news and/or 10-K / 10-Q / earnings-call text.
  2. Compute finance-specific negativity score using Loughran-McDonald or upgraded NLP model.
  3. Neutralize for size / industry / momentum if desired.
  4. Short most negative decile or long positive-minus-negative baskets on short horizon.
- **Data requirements:** Either public EDGAR text or paid news feed; NLP parsing; event timestamps.
- **Infrastructure required:** ALT_DATA_FEED if news-based; SINGLE_NAME_UNIVERSE if filing-based only
- **Effect size (in-sample):** Strong in canonical papers.
- **Effect size (OOS):** Survives conceptually, but implementation details matter materially.
- **Sharpe decay:** Moderate; signal quality depends heavily on text source and timestamp accuracy.
- **Real-time implementability:** **MEDIUM** for filing text; **LOW-MEDIUM** for full news feed unless paid data is available
- **Executability check — STOCKS:** On a **500-stock U.S. universe**, either **short the most negative decile after text events** or **long top-quintile / short bottom-quintile tone baskets**, weekly or event-driven rebalance, minimum **40 names per side**, turnover high if news-based and lower if filing-based.
- **Correlation with V010 / V026:** Likely moderate with earnings revisions and residual momentum, but **NOT_REPORTED** in a clean apples-to-apples form.
- **Correlation with other candidates:** Low with profitability and BAB; this is the cleanest nonclassical stock addition in the review.
- **Recommended Grade:** **B**
- **Recommended group:** **Cross-sectional equity sleeve**
- **Methodology paradigm:** ML-or-Text
- **Confidence:** **MEDIUM**
- **Why it fills a gap:** This is the most defensible path into the stock NLP sleeve without requiring black-box ML on day one.
- **Risk of adoption:** Timestamp errors, headline duplication, and vendor-specific text coverage can destroy live signal quality.
- **Deployability timeline:** **MEDIUM** for EDGAR-only; **LONG** for full news-based system
- **Infrastructure-cost estimate:**
  - **EDGAR / filings version:** low data cost, meaningful engineering, **4–8 weeks**
  - **News-feed version:** commercial feed plus NLP/event-time stack, likely **8–16 weeks**

## 5. DUAL_USE BUCKET — Ranked Table

**No candidate admitted.** I considered dispersion / implied correlation and broader attention / uncertainty aggregators, but neither cleared both the current-executability standard for the **INDEX** bucket and the replication / implementation bar for a clean **DUAL_USE** admission.

## 6. Gap Coverage Matrix

| Gap | Covered by | Status |
|---|---|---|
| Index variance / volatility risk premium | CAND-01 | COVERED |
| Index option-implied directional / defensive | CAND-03 | COVERED |
| Index macro-nowcasting / structural premium predictors | CAND-02 | COVERED |
| Index intermediary / flow / positioning | — | **NO_QUALIFYING_CANDIDATE** |
| Index dispersion / implied correlation | Reserve only | **PARTIAL** |
| Index sentiment / attention / policy uncertainty | CAND-04 | COVERED |
| Index valuation timing | — | **NO_QUALIFYING_CANDIDATE** |
| Stock value | Reserve only | **PARTIAL / NOT SHORTLISTED** |
| Stock quality / profitability | CAND-05 | COVERED |
| Stock defensive / low-vol / BAB | CAND-06 | COVERED |
| Stock ML / latent-factor models | — | **NO_QUALIFYING_CANDIDATE (this pass)** |
| Stock text / NLP | CAND-07 | COVERED |
| Stock attention / behavioral | Reserve only | PARTIAL |

## 7. Paradigm Diversification Check

Final shortlist count by paradigm:

- **Option-implied / variance-structure:** 2
- **Structural-nowcasting:** 1
- **Behavioral / attention / positioning:** 1
- **Classical academic risk premium:** 2
- **ML-or-Text / alternative-data:** 1

The final shortlist spans **five paradigms**, comfortably exceeding the required minimum of three, while respecting the cap of **no more than two candidates from the same paradigm**.

## 8. Overlap / Correlation Analysis

- **CAND-01 vs existing VIX stack:** related, but not duplicative. VIX level and VIX-curve slope tell you about fear and term structure; VRP / SVIX tells you about the **premium paid for variance insurance**.
- **CAND-03 vs existing VIX stack:** also related, but skew is about **left-tail asymmetry**, not total vol or term structure.
- **CAND-02 vs existing macro variables:** the strongest orthogonality in the review. Your current macro set is level/state-heavy; this one is **mixed-frequency real-time updating**.
- **CAND-05 vs CAND-06:** manageable overlap, but both belong to the classical equity-factor family. BAB loses some incremental distinctiveness once quality is controlled.
- **CAND-05 vs QMJ reserve candidate:** high overlap; shortlist **gross profitability**, not both.
- **CAND-07 vs V010 earnings revisions:** probably some overlap around information diffusion, but text negativity is a different modality and earlier in the chain.
- **Reported correlations with V009 / V010 / V026:** mostly **NOT_REPORTED** in the literature in directly comparable form. No shortlisted candidate produced a documented |ρ| > 0.5 with the exact existing variables.

## 9. Replication-Audit Summary

**CAND-01 (VRP / SVIX).** The family is real enough to include, but not clean enough for Grade A. BTZ and Martin established the concept; Bekaert-Hoerova strengthened decomposition; Goyal-Welch-Zafirov’s later audit is the critical humility check, showing that SVIX/VIX-style signals remain interesting but are not as universally significant as early readings suggested. This is why it ranks first on **gap value**, not on certainty.

**CAND-02 (macro surprise / nowcast).** This signal family survives because it is less a fragile anomaly and more a disciplined state-updating framework. Scotti’s surprise index is real-time by construction, ADS is institutionally maintained, and GDPNow provides a parallel public nowcast benchmark. The weakness is not replication failure; it is that the exact composite specification is a design choice.

**CAND-03 (skew / tail demand).** Tail-risk papers are credible, but live-trading implementation often slides from elegant theory into rough public proxy. That is why I am keeping the candidate only as a sizing scalar / regime tool. The literature supports tail-risk pricing; the operational question is how faithful SKEW or 25-delta skew is to the academic object.

**CAND-04 (EPU).** EPU is well established as an uncertainty measure and clearly mechanism-grounded, but market-timing power is nonlinear and unstable. It survives here as a low-confidence overlay, not as a core alpha engine.

**CAND-05 (gross profitability).** This is the cleanest stock candidate in the review. It migrated from anomaly to mainstream via the Fama-French profitability term, and later factor-replication work generally treats profitability as one of the sturdier families. It is the rare candidate that remains strong after the audit layer.

**CAND-06 (BAB).** BAB is robust enough to keep, but not robust enough to present without caveats. The original paper is strong; later work shows part of the apparent beta anomaly may be subsumed by quality. That still leaves BAB as a useful defensive sleeve, but it lowers confidence.

**CAND-07 (financial-text negativity).** The text sleeve is more robust than the ML sleeve in this pass because its mechanism is intuitive and replicated across filing and news contexts. The signal is real, but implementation quality matters enormously. This is not a “download one sentiment score and trade it” factor.

## 10. Registration Recommendations

### Top INDEX candidates

- **V029 — SPX variance risk premium / SVIX proxy**
  - **Grade:** B
  - **Group:** S
  - **Rationale:** Best direct fill for the missing equity-index variance-premium cell.
  - **OOS tracking period before live capital:** **3–6 months** weekly and monthly tracking.
  - **Named instrument:** **SPY** (execution) and **SPX/VIX** (signal inputs).

- **V030 — Real-time macro surprise / nowcast gate**
  - **Grade:** B
  - **Group:** Overlay
  - **Rationale:** Highest orthogonality to current macro stack; public and operational now.
  - **OOS tracking period:** **2–3 months** is sufficient because data is live and observable.
  - **Named instrument:** **SPY** or **ES**.

- **V031 — SPX/SPY downside-skew scalar**
  - **Grade:** B/C
  - **Group:** R / Overlay
  - **Rationale:** Adds crash-asymmetry pricing missing from current overlay stack.
  - **OOS tracking period:** **3–6 months**.
  - **Named instrument:** **SPY**.

- **V032 — U.S. EPU gate**
  - **Grade:** C
  - **Group:** Overlay
  - **Rationale:** Useful defensive guardrail, but not a core signal.
  - **OOS tracking period:** **6 months** minimum.
  - **Named instrument:** **SPY**.

### Top STOCKS candidates

- **PIPE-01 — Gross profitability sleeve**
  - **Grade:** A
  - **Rationale:** Strong enough to justify buildout now.
  - **Infrastructure estimate:** accounting database + lag-safe joins + cross-sectional backtest stack.
  - **Buildout:** justified now.

- **PIPE-02 — BAB / defensive sleeve**
  - **Grade:** B
  - **Rationale:** Good second sleeve, but should be tested jointly against profitability / quality overlap.
  - **Infrastructure estimate:** same as PIPE-01 plus beta-neutralization and borrow logic.
  - **Buildout:** justified after PIPE-01.

- **PIPE-03 — Financial-text negativity sleeve**
  - **Grade:** B
  - **Rationale:** Strong enough to justify a research build, especially via filing text first.
  - **Infrastructure estimate:** EDGAR ingest first, news-feed later.
  - **Buildout:** justified, but in stages.

## 11. Gaps Still Unfilled

Ranked by importance:

1. **Index intermediary / dealer-positioning / gamma / systematic-flow signals** — important, but public nonproprietary replication still too weak for admission.
2. **Stock ML / latent-factor models** — important research frontier, but this pass did not find a candidate that was both sufficiently replicated and registry-ready.
3. **Stock value** — not rejected on theory grounds; it lost on shortlist design because the classical bucket was already filled by stronger first-build sleeves.
4. **Index dispersion / implied correlation** — academically credible, but operationally heavier than the near-term index candidates.
5. **Index valuation timing** — still low priority; timing evidence is weaker than premium, skew, and nowcast alternatives.

## 12. Suggested Next Steps

Enter **V029, V030, and V031** into the **index OOS tracking ledger immediately**. For live tracking, do not force a composite score yet; first log each one independently against SPY / ES so you can see whether the newer paradigms actually add orthogonal information to the existing stack.

For stocks, start the candidate pipeline in this order: **PIPE-01 gross profitability**, **PIPE-02 BAB**, then **PIPE-03 filing-based text negativity**. That sequence maximizes evidence strength first and engineering complexity second.

The follow-up reviews most worth commissioning are: **(1) an equity-index option-implied deep dive** focused on VRP vs skew vs implied correlation; **(2) a stock NLP / LLM signal scan** focused on the difference between cheap filing-text implementations and expensive real-time news; and **(3) a dealer-positioning public-data feasibility scan**, because that is the most important missing index gap that this review could not honestly clear.

---

## References

Aruoba, S. B., Diebold, F. X., and Scotti, C. (2009). *Real-Time Measurement of Business Conditions.*

Asness, C., and Frazzini, A. (2013). *The Devil in HML’s Details.*

Asness, C., Frazzini, A., and Pedersen, L. H. (2019). *Quality Minus Junk.*

Baker, S. R., Bloom, N., and Davis, S. J. (2016). *Measuring Economic Policy Uncertainty.*

Bekaert, G., and Hoerova, M. (2014). *The VIX, the Variance Premium and Stock Market Volatility.*

Bollerslev, T., Tauchen, G., and Zhou, H. (2009). *Expected Stock Returns and Variance Risk Premia.*

Frazzini, A., and Pedersen, L. H. (2014). *Betting Against Beta.*

Gârleanu, N., Pedersen, L. H., and Poteshman, A. (2009). option-demand / directional-pressure literature.

Goyal, A., Welch, I., and Zafirov, A. (2024). *A Comprehensive 2022 Look at the Empirical Performance of Equity Premium Prediction.*

Hou, K., Xue, C., and Zhang, L. (2020). *Replicating Anomalies.*

Jensen, T. I., Kelly, B. T., and Pedersen, L. H. (2023). *Is There a Replication Crisis in Finance?*

Kelly, B., and Jiang, H. (2014). *Tail Risk and Asset Prices.*

Loughran, T., and McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.*

Martin, I. (2017). *What Is the Expected Return on the Market?*

McLean, R. D., and Pontiff, J. (2016). *Does Academic Research Destroy Stock Return Predictability?*

Novy-Marx, R. (2013). *The Other Side of Value: The Gross Profitability Premium.*

Scotti, C. (2016). *Surprise and Uncertainty Indexes: Real-Time Aggregation of Real-Activity Macro-Surprises.*

Tetlock, P. C., Saar-Tsechansky, M., and Macskassy, S. (2008). *More Than Words: Quantifying Language to Measure Firms’ Fundamentals.*
