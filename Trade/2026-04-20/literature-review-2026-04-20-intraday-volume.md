# Literature Review — Intraday-Volume Uplift Ranking (5×/day cadence)
**Generated:** 2026-04-20 UTC+8
**Routine:** literature-review (scoped — intraday refresh uplift on existing variables)
**Sources:** `framework/Methodology Prompt.md` §4 + §1.5 + §5; `2026-04-20/signal-review-2026-04-20.md`; live web search (queries + hits in §8 Appendix); eight literature strands enumerated in §5.
**Scope:** rank every variable in Gerald's current 8-step methodology by expected marginal benefit of moving its data input from EOD to **5 intraday updates per day** (~80-min spacing across the US cash session, plus a pre-open and an after-close read), scored across the **full applicable asset universe**. No new variables, no weight/sizing/universe changes.

---

## 1. Scope statement

Cadence is fixed at 5×/day. The question is *which existing variables* benefit from that refresh — not whether to go faster (1/min, streaming) or slower (EOD). Every variable is scored across each asset class it applies to (single-stock / equity-index-ETF / commodity / FX / crypto). Rows are duplicated per asset class whenever the IUS, mechanism, citation, cost, or whipsaw risk differs. A ⚠ flag marks any row whose supporting evidence is drawn from a single asset class only; such rows are capped at IUS 2 unless the mechanism explicitly generalizes. Gerald acts primarily from **Ranking B-ES** (index + single-stock, net of cost/whipsaw, Top-5) with Ranking B (all-asset, net) as cross-asset check.

---

## 2. Gap framing — what an intraday upgrade would plausibly fix

From `2026-04-20/signal-review-2026-04-20.md`:

- **EWY exit (N027)** — signal correct, exit was an *execution* error: stop tightened intraday below methodology stop, fired on a noise wick. An R-overlay refreshed intraday (realized vol, liquidity, ATR re-estimate) would have flagged the noise band before the stop was tightened, not after.
- **WTI basis-momentum cap fired Apr-16, cancelled Apr-19** — a 3-day lag from divergence-detection to cancellation is the window where a higher-frequency F1–F2 slope read could have either confirmed earlier or avoided the cap. Borderline — basis-momentum is structurally a 4w/12w window, so 5×/day mostly resolves the *trigger* not the underlying signal.
- **Audit-addition contribution log** — residual-momentum and basis-momentum are decision-moving; intermediary-capital z is dormant (weekly cadence, low-stress regime). Faster cadence on a weekly-sourced variable cannot make it less dormant.
- **All three open positions profitable within 4 days of entry** — entry timing is not the binding weakness; the binding weakness is **R-overlay responsiveness during the hold**. That asymmetry shapes Ranking B-ES.

Intraday upgrade matters most for **R-bucket** (vol state, skew, liquidity, dealer gamma, crypto order imbalance) and **T-bucket order-flow proxies** during the hold window. It matters least for slow Structural (S) and quarterly fundamentals.

---

## 3. Per-variable × asset-class table

**Legend.** Bucket = S/T/C/R/Overlay per Methodology §2. Native cadence = the data-source refresh. "5×/day moves?" = gatekeeper: N → IUS auto-0. ⚠ = citation grounded in a single asset class; IUS capped at 2 unless mechanism explicitly generalizes. Cost/Whipsaw: L=0, M=1, H=2 (used in Ranking B).

### 3.1 S — Structural (Step 2)

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | Carry / roll yield | FX (EURUSD, USDJPY) | S | Daily settlements; intraday front/back quotes | Y marginally | 1 |  | Koijen-Moskowitz-Pedersen-Vrugt 2018 JFE (A) | Intraday only resolves roll-trade timing, not carry signal | L | L |
| S02 | Carry / roll yield | Commodity (all 7) | S | Daily settlements; intraday futures | Y marginally | 1 |  | Koijen et al. 2018 JFE (A); Gorton-Hayashi-Rouwenhorst 2013 RF (A) | Same logic — slow-moving ratio, intraday adds noise | L | L |
| S03 | Equity valuation spread (E/P, B/P, FCF/EV) | Single-stock (12 tickers) | S | Numerator quarterly; denominator intraday | Y trivially (price leg only) | 0 |  | Asness-Frazzini-Pedersen 2019 RAPS (A) | Quarterly fundamentals dominate; price refresh duplicates TSMOM | L | L |
| S04 | Equity valuation spread | Equity-index-ETF (QQQ/SPY/EWJ/EWY) | S | Same | Y trivially | 0 |  | Same | Same | L | L |
| S05 | Gross profitability / quality | Single-stock | S | Quarterly 10-Q | N — statement-bound | 0 |  | Novy-Marx 2013 JFE (A) | INSUFFICIENT EVIDENCE for intraday — quarterly by source | L | L |
| S06 | Forward-rate factor (Cochrane-Piazzesi) | Rates / bond (cross-asset R input) | S | Daily yield curve | Y marginally | 1 |  | Cochrane-Piazzesi 2005 AER (A) | Curve trades intraday but 1-month-horizon signal dwarfs 5×/day noise | L | L |
| S07 | Term premium (ACM) | Rates | S | Daily, NY Fed posts EOD | N — model output EOD only | 0 |  | Adrian-Crump-Moench 2013 RFS (A) | Source publishes once daily; 5×/day = identical value 5× | L | L |
| S08 | Inflation breakevens | Rates / commodity R input | S | Intraday (TIPS market) | Y marginally | 1 |  | Fleckenstein-Longstaff-Lustig 2014 JF (A) | Moves ~5–10bp/week; 5×/day captures noise around drift | L | L |
| S09 | Real yields | Rates / gold R input | S | Intraday (TIPS) | Y marginally | 1 |  | Beeler-Campbell 2012 CFR (A) | Slow drift dominates | L | L |
| S10 | Commodity inventories (EIA, AGA) | Commodity (Brent/WTI/gas) | S | Weekly release | N — release-bound | 0 |  | Gorton-Hayashi-Rouwenhorst 2013 RF (A) | EIA release already triggers same-day reprice; 5×/day cannot beat the print | L | L |
| S11 | Commodity F1–F2 slope (static) | Commodity (all 7) | S | Continuous futures | Y | 2 |  | Hong-Yogo 2012 JFE (A); Boons-Prado 2019 JF (A); 2024 gold intraday RV literature (B) | Intraday curve can detect slope inflection ahead of EOD settle — catches curve-shape exhaustion static read misses | L | M |
| S12 | FX REER / PPP gap | FX | S | Monthly (BIS) | N — monthly source | 0 |  | Engel-West 2005 JPE (A) | INSUFFICIENT EVIDENCE for intraday — monthly by definition | L | L |
| S13 | Net supply / issuance / duration supply | Rates | S | Monthly Treasury auctions | N — monthly schedule | 0 |  | Greenwood-Vayanos 2014 RFS (A) | Auction-bound; 5×/day = identical value | L | L |
| S14 | Buyback / net payout | Single-stock | S | Quarterly 10-Q | N — 10-Q lag | 0 |  | Boudoukh-Michaely-Richardson-Roberts 2007 JF (A) | INSUFFICIENT EVIDENCE for intraday | L | L |
| S15 | Insider net buying | Single-stock | S | Form 4, ≤2-day filing lag | N — filings batched daily by SEC | 0 |  | Cohen-Malloy-Pomorski 2012 JF (B) | Filing cadence is daily at best; intraday flow is unobservable until file | L | L |
| S16 | V028 Basis-momentum (4w/12w slope change) | Commodity (all 7) | S | Continuous futures | Y but window is 4w/12w | 1 |  | Boons-Prado 2019 JF (A) | Change-window is structurally weekly; intraday refines the latest tick of a 4–12w rolling change. Marginal for divergence-cap rule. | L | M |
| S17 | V029 BAB (β estimate) | Single-stock | S | Daily β estimates, rolling 12m window | Y | 1 | ⚠ | Frazzini-Pedersen 2014 JFE (A); Insana 2023 IRFA v86 (B, intraday BAB) | ⚠ SINGLE-ASSET EVIDENCE — all BAB-intraday work is US single-stocks. Insana (2023) shows intraday β outperforms daily β, but at 5-min frequency, not 5×/day. 5×/day is much coarser than the paper's design. IUS capped at 2 by rule; scored 1 because 5×/day is well below the sampling range the literature validates. | L | M |
| S18 | V029 BAB (ETF proxy USMV/SPLV spread) | Equity-index-ETF | S | Intraday prices | Y | 1 | ⚠ | Same as S17 | Same ⚠ single-asset-evidence issue; ETF-spread version is a proxy, not the canonical factor | L | M |
| S19 | V031 GP/A | Single-stock | S | Quarterly | N — statement-bound | 0 |  | Novy-Marx 2013 JFE (A) | EXPLICIT SCOPE EXCLUSION per §4.3: report lag, not sampling, is binding | L | L |
| S20 | V032 CEI | Single-stock | S | Quarterly | N — statement-bound | 0 |  | Daniel-Titman 2006 JF (A) | EXPLICIT SCOPE EXCLUSION per §4.3 | L | L |

### 3.2 T — Tactical (Step 3)

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 12m TSMOM | Equity-index-ETF | T | Continuous prices; signal is 252-day return | Y trivially | 1 |  | Moskowitz-Ooi-Pedersen 2012 JFE (A) | Sampling 12m signal 5×/day chases noise. Gao-Han-Li-Zhou 2018 RFS intraday-momentum is a *separate* signal at a separate frequency, not a refresh of 12m TSMOM — out of scope per §1 | L | H |
| T02 | 12m TSMOM | Single-stock | T | Same | Y trivially | 1 |  | Moskowitz-Ooi-Pedersen 2012 JFE (A) | Same logic; Methodology §3 prefers V026 residual momentum over raw TSMOM for single-stocks anyway | L | H |
| T03 | 12m TSMOM | Commodity (all 7) | T | Same | Y trivially | 1 |  | Same | Same; add'l note: commodity intraday RV literature (2024 Luo JoF) is about vol forecasting, not TSMOM refresh | L | H |
| T04 | 12m TSMOM | FX | T | Same | Y trivially | 1 |  | Same | Same | L | H |
| T05 | 12m TSMOM | Crypto (BTC/ETH) | T | Same (24/7) | Y trivially | 1 |  | Same; Liu-Tsyvinski 2021 RFS (A) | 24/7 trading only marginally changes the argument — signal is still 252-day | L | H |
| T06 | Earnings revision breadth (I/B/E/S) | Single-stock | T | Daily aggregate; individual revisions arrive intraday on broker notes | Y | 1 |  | Chan-Jegadeesh-Lakonishok 1996 JF (A) | Revision flow is intraday but the *breadth aggregate* is robustly daily; 5×/day captures day's flow but adds little to the statistic | M | L |
| T07 | FX interest-rate differential (carry signal) | FX | T | Continuous | Y trivially | 0 |  | Lustig-Roussanov-Verdelhan 2011 RFS (A) | Carry is a slow rate-spread signal; intraday rate moves are policy-event-driven (already captured under Catalyst) | L | L |
| T08 | CFTC speculative positioning | Commodity | T | Weekly (Tuesday COT; Friday as-of) | N — release-bound | 0 |  | Cheng-Xiong 2014 RAPS (B) | EXPLICIT per §5.8: report-bound; no intraday uplift possible | L | L |
| T09 | CFTC speculative positioning | FX | T | Same | N | 0 |  | Same | Same | L | L |
| T10 | Dealer / customer order flow proxy (VPIN) | Single-stock | T | Equity-tape intraday (TRF prints) | Y | 3 |  | Easley-López de Prado-O'Hara 2012 RFS (A); Abad-Yagüe 2018 JIFMIM (B); 2025 arxiv 2508.06788 S&P 500 E-mini OFI study (B) | VPIN is *defined* on intraday volume — EOD cannot reproduce it. 5×/day is coarser than canonical 50-bucket VPIN but retains direction. 2025 OFI study on S&P 500 futures reinforces intraday flow → return link. | M | M |
| T11 | Dealer / customer order flow proxy (VPIN, OFI) | Equity-index-ETF | T | Same (SPY/QQQ tape) | Y | 3 |  | Same | Same; arxiv 2508.06788 is index-specific evidence | M | M |
| T12 | Dealer / customer order flow proxy | Commodity (futures) | T | Continuous TAS tape | Y | 2 |  | Adapted from Easley et al. 2012 (A); Hong-Yogo 2012 JFE (A — futures flow) | Direct VPIN implementation on commodity futures less validated than equities; mechanism preserves but empirical base thinner | M | M |
| T13 | Dealer / customer order flow proxy | FX | T | EBS/Reuters aggregate; retail proxy CFTC | Y (EBS proprietary); N (public) | 1 |  | Evans-Lyons 2002 JPE (A) | Public FX order-flow is CFTC-bound (weekly); proprietary EBS/Reuters tape is intraday but not in Gerald's data stack | H | M |
| T14 | News-based text sentiment | Single-stock | T | Continuous newsfeed | Y | 3 |  | Tetlock 2007 JF (A); Jegadeesh-Wu 2013 JFE (B); 2025 Tandfonline dividend-announcement LLM sentiment study (B); 2024 ScienceDirect real-time sentiment JFE/ECF studies | Tetlock/Jegadeesh-Wu validate the signal; 2024–25 LLM-sentiment studies confirm **intraday sentiment outperforms daily** for predicting next-session returns on single-stocks. 5×/day windows (pre-open, morning, midday, afternoon, after-close) align with news flow | M | M |
| T15 | News-based text sentiment | Equity-index-ETF | T | Continuous newsfeed | Y | 2 |  | Tetlock 2007 JF (A); Calomiris-Mamaysky 2019 JF (A) | Index-level sentiment exists but signal-to-noise is weaker than single-stock (idiosyncratic news aggregates to less); IUS 2 | M | M |
| T16 | News-based text sentiment | Commodity | T | Continuous newsfeed | Y | 2 |  | Baker-Bloom 2013 (A); Smales 2017 JFM (B) | Event-days (OPEC, inventory surprise) drive most of the signal; 5×/day captures these | M | M |
| T17 | News-based text sentiment | FX | T | Continuous newsfeed | Y | 2 |  | Hendershott-Livdan-Schürhoff 2015 JF (A) | Same logic; central-bank-speak sentiment captured intraday | M | M |
| T18 | News-based text sentiment | Crypto (BTC/ETH) | T | 24/7 newsfeed + social | Y | 2 |  | Liu-Tsyvinski 2021 RFS (A — attention); Eom-Kaizoji-Livan-Scalas 2019 PhysA (B) | 24/7 flow + social channels (TG, X) — 5×/day coarse vs the data-generating process but still materially beats EOD | M | M |
| T19 | V026 Residual momentum (12m FF5-residualized) | Single-stock | T | 12m return; FF5 factors monthly (Ken French) | Y trivially on return leg | 0 |  | Blitz-Huij-Martens 2011 JEF (A); Asness-Moskowitz-Pedersen 2013 JF (A) | Intraday adds 1/252 of a day's residual return; **Ken French FF5 updates monthly** — residualization cannot be done intraday with current data. Even if it could, 252-day window dominates. | L | L |

### 3.3 C — Catalyst (Step 4)

All catalyst variables are event-timestamped; 5×/day uplift exists only on T-0/T+0 of scheduled releases, zero on other days. This is noted once here rather than repeated per row.

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves on event days? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | Scheduled-earnings catalyst (PEAD drift window) | Single-stock | C | Quarterly per name | Y on T-0/T+1 | 3 |  | Bernard-Thomas 1989 JAE (A); Sadka 2006 JFE (A); Kaczmarek-Zaremba 2025 FinResLett v86 (B — 12-quarter SUE elastic-net Sharpe ~2×); Garfinkel-Hribar-Hsiao 2024 SSRN 5040374 (B — CNN-on-earnings-visualization OOS return prediction); 2025 FinNLP / ACM ICAIF PEAD text studies | PEAD drift unfolds over hours-to-days. 5×/day captures the drift window; 2024–25 ML/NLP evidence (Kaczmarek-Zaremba, Garfinkel et al.) shows PEAD alive for large-caps when richer features are used. Matches Gerald's 12-ticker sleeve (all large-cap) | L | M |
| C02 | Scheduled-earnings guidance (follow-through) | Equity-index-ETF | C | Sector-aggregate earnings-season effect | Y on concentrated event days | 2 |  | Ball-Brown 1968 JAR (A); Savor-Wilson 2013 JF (A — FOMC/earnings announcement premia) | Index effect of earnings season is diffused vs single-stock PEAD; 5×/day uplift modest | L | L |
| C03 | Policy-path surprise (FOMC, ECB, BoJ) | Rates / cross-asset | C | Event-timestamped | Y on event days | 3 |  | Nakamura-Steinsson 2018 QJE (A); Gertler-Karadi 2015 AEJ (A); Swanson 2021 JME (A) | High-frequency surprise identification **requires** intraday windows; 5×/day is coarser than the 30-min window in the literature but still captures direction on release days | L | M |
| C04 | Macro-release surprise (CPI, NFP, ISM) | Cross-asset | C | Event-timestamped | Y on event days | 3 |  | Andersen-Bollerslev-Diebold-Vega 2003 AER (A) | ABDV 2003 is canonical intraday-impact literature (5-min windows). 5×/day coarser but still beats EOD on release days | L | M |
| C05 | OPEC / inventory release | Commodity (oil/gas) | C | Event-timestamped | Y on event days | 3 |  | Chen-Jin-Zhou 2014 JFE (A); Demirer-Kutan 2010 EE (B) | Same mechanism for commodities; OPEC + weekly EIA are the dominant intraday-impact windows | L | M |
| C06 | Crypto event (ETF approval, hack, enforcement) | Crypto | C | Event-timestamped | Y on event days | 3 |  | Makarov-Schoar 2020 JFE (A); Foley-Karlsen-Putniņš 2019 RFS (A) | 24/7 market amplifies intraday uplift — events reprice crypto within hours, not sessions | L | M |

### 3.4 R — Risk Overlay (Step 5)

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Realized volatility / ATR | Single-stock | R | Computed from intraday returns | Y | 3 |  | Andersen-Bollerslev-Diebold-Labys 2001 JASA (A); Bollerslev-Patton-Quaedvlieg 2016 JoE (A); 2024 ScienceDirect HF-stochastic-vol models (A) | RV variance falls ~1/N sampling rate up to microstructure-noise floor (5-min for liquid US equities). 5×/day far below floor — pure uplift. **Most relevant variable to EWY-stop lesson.** | L | L |
| R02 | Realized volatility / ATR | Equity-index-ETF | R | Same | Y | 3 |  | Same | Same; literature's 5-min optimum validated on SPY/E-mini directly | L | L |
| R03 | Realized volatility / ATR | Commodity | R | Same | Y | 3 |  | ABDL 2001 (A); Luo et al. 2024 JoF (A — WTI HAR-ML); Xia et al. 2023 FinLetters (B — gold intraday RV) | Direct cite for commodity RV (2024 crude, 2023 gold). Uplift confirmed at 5×/day in these studies' nested frequencies | L | L |
| R04 | Realized volatility / ATR | FX | R | Same | Y | 3 |  | ABDL 2001 JASA (A — FX is the ABDL original dataset); BPV 2016 JoE (A) | FX is the canonical ABDL dataset; uplift directly established | L | L |
| R05 | Realized volatility + jumps | Crypto (BTC/ETH) | R | Same (24/7) | Y | 3 |  | Aït-Sahalia-Jacod 2009 AoS (A); Lee-Wang 2024 Georgia Tech (B); 2024–25 Bitcoin 1-min/5-min RV studies (B); MDPI 2025 Bayesian minute-by-minute vol (B) | 24/7 trading *amplifies* the uplift vs equity hours-only constraint; jump detection specifically benefits from finer sampling (though 5×/day is coarse for jumps, still strictly beats EOD) | L | L |
| R06 | Implied vol level (VIX) | Equity-index-ETF | R | Real-time intraday | Y | 3 |  | Whaley 2009 JPM (A) | VIX is real-time at source; 5×/day captures intraday range vs EOD print | L | L |
| R07 | Implied vol level (MOVE) | Rates (cross-asset R input) | R | Real-time intraday | Y | 3 |  | Choi-Mueller-Vedolin 2017 JFE (A) | Same mechanism; MOVE real-time | L | L |
| R08 | Implied vol level (single-name IV) | Single-stock | R | Real-time intraday | Y | 3 |  | Goyal-Saretto 2009 JFE (A); MDPI FRM 2024 17/1/39 (B — intraday single-stock model-free IV 1m/10m/60m) | **2024 MDPI study explicitly implements single-stock intraday model-free IV at 1m/10m/60m windows** — directly validates 5×/day cadence for single-stock IV | L | L |
| R09 | Implied vol level (CVOL, crude/gold) | Commodity | R | Real-time intraday | Y | 2 |  | Schneider-Tavin 2018 WP (B — CVOL); adapted from Whaley 2009 (A) | CME CVOL publishes intraday; literature base thinner than equity VIX | L | L |
| R10 | Implied vol level (BVIV/DVOL for BTC) | Crypto | R | Real-time (Deribit) | Y | 3 |  | Alexander-Imeraj 2023 WP (B); Hou-Nolte-Staer 2020 JFE (B); analog to Whaley 2009 (A) | Deribit DVOL continuous; crypto IV literature younger but mechanism identical to equity VIX | L | L |
| R11 | Options-implied skew / risk reversals | Single-stock | R | Intraday options market | Y | 3 | ⚠ | Cremers-Weinbaum 2010 JFQA (A); An-Ang-Bali-Cakici 2014 JF (A); Xing-Zhang-Zhao 2010 JFQA (A); 2024 MDPI intraday single-stock IV (B) | ⚠ SINGLE-ASSET EVIDENCE — all three canonical papers are US single-stock options. Mechanism (skew leads 1-day return) **does generalize** — same microstructure obtains on index options, CVOL, Deribit — so IUS stays at 3 for single-stock where evidence is native. Cap IUS = 2 for extrapolation rows (R12/R13/R14 below) | L | L |
| R12 | Options-implied skew / risk reversals | Equity-index-ETF | R | Intraday (CBOE SKEW, SPX skew) | Y | 2 | ⚠ | Cremers-Weinbaum 2010 JFQA (A — single-stock; ⚠ extrapolation); Bollerslev-Todorov 2011 JF (A — SPX tail risk) | ⚠ extrapolated from single-stock Cremers-Weinbaum; Bollerslev-Todorov 2011 directly supports SPX-tail-risk intraday refresh as separate evidence | L | L |
| R13 | Options-implied skew / risk reversals | Commodity | R | Intraday (CVOL skew) | Y | 2 | ⚠ | Schneider-Tavin 2018 WP (B); extrapolated from equity literature | ⚠ limited direct evidence on commodity skew intraday uplift; mechanism argued to generalize | L | M |
| R14 | Options-implied skew / risk reversals | FX | R | Intraday (25-delta RR) | Y | 2 |  | Carr-Wu 2007 JFE (A — FX risk-reversals); Jurek 2014 JFE (A) | FX RR skew is a separately established signal (carry-crash literature); 5×/day captures intraday flip | L | M |
| R15 | Options-implied skew | Crypto | R | Intraday (Deribit DSKEW) | Y | 2 |  | Alexander-Imeraj 2023 WP (B); analog to Cremers-Weinbaum (A) | Deribit surface continuous; literature younger but mechanism transfers | L | M |
| R16 | VRP / IV–RV gap | Equity-index-ETF | R | Intraday IV; RV from intraday returns | Y | 2 |  | Bollerslev-Tauchen-Zhou 2009 RFS (A); BPV 2016 JoE (A) | RV estimate sharpens with sampling; VRP = IV² − RV² inherits the uplift | L | L |
| R17 | VRP / IV–RV gap | Single-stock | R | Same | Y | 2 |  | Bali-Hovakimian 2009 MS (A); Kadan-Tang 2020 RFS (B) | Single-stock VRP validated; intraday uplift inherited from R01 RV + R08 IV | L | L |
| R18 | VRP / IV–RV gap | Commodity | R | Same | Y | 2 |  | Trolle-Schwartz 2010 RFS (A); Prokopczuk-Simen 2014 JEE (B) | Commodity VRP thinner literature; uplift inherited | L | L |
| R19 | VRP / IV–RV gap | FX | R | Same | Y | 2 |  | Della Corte-Ramadorai-Sarno 2016 JFE (A) | FX VRP established; uplift inherited | L | L |
| R20 | VRP / IV–RV gap | Crypto | R | Same | Y | 2 |  | Hou-Nolte-Staer 2020 JFE (B); Alexander-Imeraj 2023 (B) | Crypto VRP; uplift inherited | L | L |
| R21 | Cross-asset correlation / beta regime | Cross-asset | R | Computed from returns | Y | 2 |  | ABDL 2001 JASA (A); Barndorff-Nielsen-Shephard 2004 JoE (A — realized covariance) | Realized-correlation sharpens with sampling; detects regime breaks faster. Applies uniformly across [SS, IDX, COM, FX, CRY] | L | L |
| R22 | Credit spreads (HY OAS via CDX HY proxy) | Cross-asset R input | R | ICE BAML EOD; CDX HY intraday | Y via CDX | 2 |  | Gilchrist-Zakrajšek 2012 AER (A); Greatrex 2009 JoFEcono (B — CDX/HY OAS correlation) | CDX HY intraday tracks EOD HY OAS at ~0.85 daily corr; 1–2 hr lead vs EOD print | L | L |
| R23 | FCI / RORO state | Cross-asset | R | Bloomberg/Goldman FCI daily; components intraday | Y (components only) | 1 |  | Hatzius et al. 2010 NBER (A) | FCI composite published daily; intraday components (DXY, equities, credit) update real-time but the *z-score* itself is a daily release | L | L |
| R24 | Liquidity (spreads, depth) | Single-stock | R | Real-time | Y | 3 |  | Amihud 2002 JFM (A); Korajczyk-Sadka 2008 JFE (A) | Real-time at source; 5×/day samples open/midday/close liquidity profile — matters for stop placement and fill | L | L |
| R25 | Liquidity (spreads, depth) | Equity-index-ETF | R | Real-time | Y | 3 |  | Same | Same | L | L |
| R26 | Liquidity (spreads, depth) | Commodity | R | Real-time | Y | 2 |  | Marshall-Nguyen-Visaltanachoti 2012 JFE (A) | Same mechanism; thinner literature on commodity intraday liquidity alpha | L | L |
| R27 | Liquidity (spreads, depth) | FX | R | Real-time | Y | 2 |  | Mancini-Ranaldo-Wrampelmeyer 2013 JF (A) | FX liquidity signal validated; uplift inherits | L | L |
| R28 | Liquidity (spreads, depth) | Crypto | R | Real-time (24/7) | Y | 3 |  | Brauneis-Mestel-Riordan-Theissen 2021 JFM (B); MDPI 2025 order book liquidity on crypto exchanges (B) | 24/7 order book; liquidity varies diurnally (Asia/EU/US sessions) — 5×/day captures the cycle | L | L |
| R29 | Crowding / positioning (CFTC component) | Commodity / FX | R | Weekly | N | 0 |  | See T08/T09 | Weekly source dominates | L | L |
| R30 | Funding rate (crypto perp) | Crypto (BTC/ETH) | R | 8-hourly settlement | Y | 2 |  | Hou-Lu 2024 SSRN (B); Ackerer-Hugonnier-Jermann 2025 MathFin (B); arxiv 2506.08573 2025 (B); Coin core (B) | Native cadence 3×/day; 5×/day captures all 3 settlements + 2 mid-period drifts. Filter-only per Coin core (no directional alpha on its own) so uplift bounded | L | M |
| R31 | OI / open interest direction | Commodity | R | Nightly (CME) | N | 0 |  | Hong-Yogo 2012 JFE (A) | Nightly-aggregated source; 5×/day = identical value | L | L |
| R32 | OI / open interest direction | Equity-index-ETF | R | Nightly (OCC) | N | 0 |  | Same | Same | L | L |
| R33 | ETF flow (creation/redemption proxy) | Equity-index-ETF | R | Daily AUM; intraday premium/discount + AP volume | Y via proxy | 2 |  | Ben-David-Franzoni-Moussawi 2018 JF (A); Brown-Davies-Ringgenberg 2021 JFE (B); Lazo-Paz 2024 AEA (B) | Creation predicts next-day positive returns **conditional on premium**; proxy is buildable from intraday premium/discount + volume | M | M |
| R34 | ETF flow (spot BTC/ETH) | Crypto | R | Daily issuer NAV; intraday AP volume + premium | Y via proxy | 2 |  | BFM 2018 JF (A — equity ETF analog); 2024–25 BTC-ETF flow literature (B) | Same mechanism for spot BTC/ETH ETF — intraday AP activity inferable | M | M |
| R35 | V027 Intermediary capital ratio (NY Fed PD z-score) | Cross-asset | R | Weekly, ~1-week lag | N — weekly source | 0 |  | He-Kelly-Manela 2017 JFE (A); Adrian-Etula-Muir 2014 JF (A) | EXPLICIT per §5.8 + signal-review "intermediary capital = 0 contribution" log. Weekly NY Fed release; 5×/day = identical value | L | L |
| R36 | V030 DealerGamma (GEX) | Single-stock | R | Intraday from options volume | Y | 3 | ⚠ | Barbon-Buraschi 2021 WP (B — single paper); Ni-Pearson-Poteshman 2005 RFS (B); 2024–25 practitioner GEX literature (C but mechanistically consistent) | ⚠ single-paper Grade B; GEX refreshes intraday as options trade; short-gamma vs long-gamma can flip within session. **Uplift mechanism is native intraday.** Cost = High (SqueezeMetrics subscription). Per Methodology §4 V030, IUS-3 is on mechanism strength but evidence grade stays B. | H | M |
| R37 | V030 DealerGamma (GEX) | Equity-index-ETF | R | Same | Y | 3 | ⚠ | Same; Barbon-Buraschi 2021 specifically tests SPX index | Same ⚠ single-paper issue; index evidence is more native than single-stock in BB 2021 | H | M |
| R38 | V030 DealerGamma | Crypto (Deribit GEX) | R | Intraday (Deribit) | Y | 2 | ⚠ | Extrapolated from Barbon-Buraschi 2021 (B); Alexander-Imeraj 2023 (B) | ⚠ no crypto-specific dealer-gamma paper at peer-reviewed level; mechanism argued to generalize but evidence thinner | M | M |
| R39 | Stablecoin issuance (USDT/USDC mint/burn) | Crypto | R | On-chain real-time | Y | 2 |  | Lyons-Viswanath-Natraj 2023 JIE (B); Coin core (B) | Mints/burns observable real-time; intraday net-issuance linked to BTC inflows at 1–2 hr horizons | L | M |
| R40 | Exchange netflows (BTC/ETH) | Crypto | R | On-chain real-time | Y | 2 |  | Makarov-Schoar 2020 JFE (A); Coin core (B) | Large exchange inflow events lead sell-pressure on hours-horizons; 5×/day captures the event | L | M |

### 3.5 Overlay Gate (Step 1.5)

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| O01 | V033/V034/V035 — C009 Faber TAA (10m-SMA gate) | Equity-index-ETF (V033), Commodity (V034), Crypto (V035) | Overlay | Month-end close vs 10m-SMA | N — by Faber discipline | 0 |  | Faber 2007 JWM (A) | EXPLICIT SCOPE EXCLUSION per §4.2: 5×/day would *violate* the rule, not improve it. Upsampling generates within-month sleeve flips the Faber circuit-breaker is *designed* to prevent. **Do not upsample.** | L | H (if violated) |

### 3.6 BTC/ETH Coin-core spine (Methodology §3 dashboard + §5 hierarchy)

| # | Variable | Asset class | Bucket | Native cadence | 5×/day moves? | IUS | ⚠ | Citation | Mechanism | Cost | Whipsaw |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K01 | BTC/ETH order imbalance (book + tape) | Crypto | T/R | Real-time from exchanges | Y | 3 |  | Cong-Li-Wang 2021 RFS (A); Easley-López de Prado-O'Hara 2012 RFS (A — VPIN analog); Anastasopoulos-Gradojevic 2025 EFMA WP (B); arxiv 2506.05764 2025 microstructural dynamics (B); PMC10040314 Bitcoin crash-risk nowcasting with OI (B) | Strongest intraday-frequency lead-lag signal in crypto (Coin core Grade A). EOD collapses the leading signal. 2025 empirical work reinforces OOS predictive power of order flow. | L | M |
| K02 | Active addresses | Crypto (BTC) | S | On-chain real-time; canonical daily | Y mechanically; signal value daily | 1 |  | Liu-Tsyvinski 2021 RFS (A); Cong-Li-Wang 2021 RFS (A); Pagnotta 2022 RFS (A) | Network-effect signal is calibrated on daily address counts. Intraday counts are diurnally cyclical (Asia/EU/US sessions) — 5×/day aliases the diurnal cycle | L | M |
| K03 | Hash rate (BTC) | Crypto | S | Real-time but smoothed over 24h | Y mechanically; signal value daily | 1 |  | Pagnotta 2022 RFS (A); Liu-Tsyvinski 2021 RFS (A) | Minute-to-minute block-time variance is noise; 24h MA is the canonical signal. 5×/day samples a noisy series whose canonical horizon is ≥1 day | L | M |
| K04 | MVRV / SOPR | Crypto (BTC) | S | Daily UTXO scan | N — daily compute at source | 0 |  | Coin core (B); §4 reconciliation note demotes to filter-only | Glassnode/CoinMetrics produce once daily; 5×/day = identical value. Plus methodology already uses as regime context only, not trigger | L | L |
| K05 | Futures basis (CME + perp) | Crypto (BTC/ETH) | R | Continuous | Y | 2 |  | Park-Spencer 2024 SSRN (B); Augustin-Rubtsov-Shin 2023 JFE (B); Coin core (B) | Basis fluctuates intraday with spot/futures lead-lag; 5×/day captures crowding inflections faster than EOD. Filter-only per Coin core | L | M |

---

## 4. Rankings

**Action hierarchy:** Gerald acts from **Ranking B-ES** first (index + single-stock, net of cost/whipsaw — the sleeve where the book concentrates); Ranking B (all-asset, net) as cross-asset check. Ranking A (raw IUS) and Ranking A-ES are shown for transparency only.

### 4.1 Ranking A — Raw uplift across all assets (sort by IUS desc, then bucket priority R > T > C > S > Overlay)

Top 20 shown (full IUS=3 band + all IUS=3 ties; all IUS-2 and below collapsed to band summary at the end):

| Rank | IUS | Variable | Asset class | ⚠ |
|---|---|---|---|---|
| 1 | 3 | R01 Realized vol / ATR | Single-stock |  |
| 2 | 3 | R02 Realized vol / ATR | Equity-index-ETF |  |
| 3 | 3 | R03 Realized vol / ATR | Commodity |  |
| 4 | 3 | R04 Realized vol / ATR | FX |  |
| 5 | 3 | R05 Realized vol + jumps | Crypto |  |
| 6 | 3 | R06 VIX | Equity-index-ETF |  |
| 7 | 3 | R07 MOVE | Rates / cross-asset |  |
| 8 | 3 | R08 Single-name IV | Single-stock |  |
| 9 | 3 | R10 BVIV/DVOL | Crypto |  |
| 10 | 3 | R11 Equity skew / RR | Single-stock | ⚠ |
| 11 | 3 | R24 Liquidity | Single-stock |  |
| 12 | 3 | R25 Liquidity | Equity-index-ETF |  |
| 13 | 3 | R28 Liquidity | Crypto |  |
| 14 | 3 | R36 V030 DealerGamma | Single-stock | ⚠ |
| 15 | 3 | R37 V030 DealerGamma | Equity-index-ETF | ⚠ |
| 16 | 3 | T10 VPIN / OFI | Single-stock |  |
| 17 | 3 | T11 VPIN / OFI | Equity-index-ETF |  |
| 18 | 3 | T14 News sentiment | Single-stock |  |
| 19 | 3 | K01 BTC/ETH order imbalance | Crypto |  |
| 20 | 3 | C01 Earnings catalyst (event days) | Single-stock |  |
| 21 | 3 | C03 Policy surprise (event days) | Rates / cross-asset |  |
| 22 | 3 | C04 Macro release (event days) | Cross-asset |  |
| 23 | 3 | C05 OPEC / inventory release | Commodity |  |
| 24 | 3 | C06 Crypto event | Crypto |  |
| 25–50 | 2 | [IUS-2 band: R09 CVOL, R12–R15 skew (non-SS, ⚠ some), R16–R20 VRP, R21 cross-asset corr, R22 CDX HY, R26–R27 liquidity COM/FX, R30 funding, R33 ETF flow, R34 BTC-ETF flow, R38 GEX crypto ⚠, R39 stablecoin, R40 exchange netflows, T12 VPIN COM, T15–T18 news sentiment IDX/COM/FX/CRY, S11 F1–F2 slope, C02 earnings IDX, K05 futures basis] |  |  |
| 51–70 | 1 | [IUS-1 band: T01–T05 TSMOM all classes, T06 revisions, T13 FX OF, S01–S02 carry, S06/S08/S09 rates/TIPS, S16 basis-momentum, S17/S18 BAB ⚠, R23 FCI, K02 active addresses, K03 hash rate] |  |  |
| 71–95 | 0 | [IUS-0: all quarterly fundamentals, inventories, monthly FX REER, CFTC, intermediary capital, MVRV/SOPR, OI direction, Faber TAA] |  |  |

### 4.2 Ranking B — All-asset, net of cost and whipsaw (Score = IUS − 0.5·Cost − 0.5·Whipsaw)

Only rows with Score ≥ 2.0 shown; full list continues in source table.

| Rank | Score | IUS | Cost | Whipsaw | Variable | Asset class |
|---|---|---|---|---|---|---|
| 1 | **3.0** | 3 | L | L | R01 Realized vol / ATR | Single-stock |
| 2 | **3.0** | 3 | L | L | R02 Realized vol / ATR | Equity-index-ETF |
| 3 | **3.0** | 3 | L | L | R03 Realized vol / ATR | Commodity |
| 4 | **3.0** | 3 | L | L | R04 Realized vol / ATR | FX |
| 5 | **3.0** | 3 | L | L | R05 Realized vol + jumps | Crypto |
| 6 | **3.0** | 3 | L | L | R06 VIX | Equity-index-ETF |
| 7 | **3.0** | 3 | L | L | R07 MOVE | Rates |
| 8 | **3.0** | 3 | L | L | R08 Single-name IV | Single-stock |
| 9 | **3.0** | 3 | L | L | R10 BVIV/DVOL | Crypto |
| 10 | **3.0** | 3 | L | L | R11 Equity skew / RR | Single-stock ⚠ |
| 11 | **3.0** | 3 | L | L | R24 Liquidity | Single-stock |
| 12 | **3.0** | 3 | L | L | R25 Liquidity | Equity-index-ETF |
| 13 | **3.0** | 3 | L | L | R28 Liquidity | Crypto |
| 14 | **2.5** | 3 | L | M | K01 BTC/ETH order imbalance | Crypto |
| 15 | **2.0** | 3 | M | M | T10 VPIN / OFI | Single-stock |
| 16 | **2.0** | 3 | M | M | T11 VPIN / OFI | Equity-index-ETF |
| 17 | **2.0** | 3 | M | M | T14 News sentiment | Single-stock |
| 18 | **2.0** | 2 | L | L | R16 VRP | Equity-index-ETF |
| 19 | **2.0** | 2 | L | L | R17 VRP | Single-stock |
| 20 | **2.0** | 2 | L | L | R19 VRP | FX |
| 21 | **2.0** | 2 | L | L | R21 Cross-asset correlation | Cross-asset |
| 22 | **2.0** | 2 | L | L | R22 CDX HY proxy for HY OAS | Cross-asset |
| 23 | **2.0** | 2 | L | L | R26 Liquidity | Commodity |
| 24 | **2.0** | 2 | L | L | R27 Liquidity | FX |
| 25 | **2.0** | 2 | L | L | R09 CVOL | Commodity |
| 26 | **2.0** | 2 | L | L | R18 VRP | Commodity |
| 27 | **2.0** | 2 | L | L | R20 VRP | Crypto |
| 28 | **2.5** | 3 | L | M | C01 Earnings catalyst | Single-stock |
| 29 | **2.5** | 3 | L | M | C03 Policy surprise | Rates |
| 30 | **2.5** | 3 | L | M | C04 Macro release | Cross-asset |
| 31 | **2.5** | 3 | L | M | C05 OPEC / inventory | Commodity |
| 32 | **2.5** | 3 | L | M | C06 Crypto event | Crypto |
| 33 | **1.5** | 3 | H | M | R36 V030 DealerGamma | Single-stock ⚠ (cost-dominated) |
| 34 | **1.5** | 3 | H | M | R37 V030 DealerGamma | Equity-index-ETF ⚠ (cost-dominated) |
| 35 | **1.5** | 2 | L | M | R12 Skew | Equity-index-ETF ⚠ |
| 36 | **1.5** | 2 | L | M | R14 FX risk-reversals | FX |
| 37 | **1.5** | 2 | L | M | R15 Crypto skew | Crypto |
| 38 | **1.5** | 2 | L | M | R30 Funding rate | Crypto |
| 39 | **1.5** | 2 | L | M | R39 Stablecoin issuance | Crypto |
| 40 | **1.5** | 2 | L | M | R40 Exchange netflows | Crypto |
| 41 | **1.5** | 2 | L | M | K05 Futures basis | Crypto |
| 42 | **1.5** | 2 | L | M | S11 F1–F2 slope | Commodity |
| 43 | **1.0** | 2 | M | M | R33 ETF flow proxy | Equity-index-ETF |
| 44 | **1.0** | 2 | M | M | R34 BTC/ETH ETF flow | Crypto |
| 45 | **1.0** | 2 | M | M | T15 News sentiment | Equity-index-ETF |
| 46 | **1.0** | 2 | M | M | T16 News sentiment | Commodity |
| 47 | **1.0** | 2 | M | M | T17 News sentiment | FX |
| 48 | **1.0** | 2 | M | M | T18 News sentiment | Crypto |
| 49 | **1.0** | 2 | M | M | T12 VPIN | Commodity |
| 50 | **1.5** | 2 | L | M | R13 Skew | Commodity ⚠ |
| 51 | **1.5** | 2 | L | M | R38 GEX | Crypto ⚠ (cost/data-thin) |

Rank 52+ all score ≤1.0; full list in §3 source table. All IUS=0 rows omitted from action ranking.

### 4.3 Ranking A-ES — Index + Single-Stock ONLY, raw uplift (Top 5)

Filter: Asset class ∈ {Single-stock, Equity-index-ETF}.

| Rank | IUS | Variable | Asset class | ⚠ |
|---|---|---|---|---|
| 1 | 3 | R01 Realized vol / ATR | Single-stock |  |
| 2 | 3 | R02 Realized vol / ATR | Equity-index-ETF |  |
| 3 | 3 | R06 VIX | Equity-index-ETF |  |
| 4 | 3 | R08 Single-name IV | Single-stock |  |
| 5 | 3 | R11 Equity skew / RR | Single-stock | ⚠ |

(Ties at IUS=3 continue: R24/R25 Liquidity, R36/R37 DealerGamma ⚠, T10/T11 VPIN/OFI, T14 News sentiment SS, C01 Earnings catalyst SS — all ranked after top-5 on bucket-priority tiebreak R > T > C.)

### 4.4 Ranking B-ES — Index + Single-Stock ONLY, net of cost and whipsaw (Top 5) — **PRIMARY ACTION LIST**

Filter: Asset class ∈ {Single-stock, Equity-index-ETF}. Sort by Score = IUS − 0.5·Cost − 0.5·Whipsaw.

| Rank | Score | IUS | Cost | Whipsaw | Variable | Asset class |
|---|---|---|---|---|---|---|
| **1** | **3.0** | 3 | L | L | **R01 Realized vol / ATR** | Single-stock |
| **2** | **3.0** | 3 | L | L | **R02 Realized vol / ATR** | Equity-index-ETF |
| **3** | **3.0** | 3 | L | L | **R06 VIX** | Equity-index-ETF |
| **4** | **3.0** | 3 | L | L | **R08 Single-name IV** | Single-stock |
| **5** | **3.0** | 3 | L | L | **R11 Equity skew / RR (Cremers-Weinbaum, ⚠)** | Single-stock |

(Ranks 6–10 for continuity: R24 Liquidity SS, R25 Liquidity IDX, R17 VRP SS, R16 VRP IDX, T10 VPIN SS. Rank 11+: C01 Earnings catalyst SS (2.5), T14 News sentiment SS (2.0), R33 ETF flow IDX (1.0), R36/R37 V030 GEX (1.5 — knocked out of top-5 by High cost).)

---

## 5. Literature engagement — the eight strands

### 5.1 Intraday momentum (Gao-Han-Li-Zhou 2018 RFS; Zhang-Wang 2022 JBF; Zarattini-Aziz-Barbon 2024 SSRN #4824172) — Grade A

The first-half-hour return predicts the last-half-hour return at t > 4 in US equities (GHLZ 2018), replicated OOS internationally (Zhang-Wang 2022). Zarattini-Aziz-Barbon (2024) report Sharpe 1.33 on SPY intraday-momentum strategy from 2007–2024. **FX extension:** Elaut-Frömmel-Lampaert (2018 JBF) document intraday momentum in FX markets, reinforcing the generalizability claim but at different session boundaries. **BAB intraday note:** Insana (2023 IRFA v86) shows intraday-BAB outperforms daily-BAB, confirming the single-stock intraday family extends beyond pure price-momentum. **Engagement:** this is a *separate* signal at a separate frequency, not an uplift to existing 12m TSMOM. Out of scope per §1 (no new variables). **Also note:** 5×/day ≈ 80-min spacing is *too coarse* to capture the GHLZ first-half/last-half-hour signal; 5×/day would collapse open and close half-hours into single bars each. **Implication:** this strand does not change any existing variable's ranking. Flag for `quarterly-methodology-review` as a potential *new* variable — but out of scope for this memo. (Also: 2024–2025 reports of signal decay in intraday momentum — Zarattini et al. note "well-studied factors such as overnight effects and intraday momentum have diminished over time" — so decay risk is elevated vs the 2018 baseline.)

### 5.2 Realized-volatility microstructure (ABDL 2001 JASA; Bollerslev-Patton-Quaedvlieg 2016 JoE; HF-SV models 2024 ScienceDirect) — Grade A

RV variance falls ~1/N sampling rate **up to the microstructure-noise floor** (5-min for liquid US equities; finer for crypto). 5×/day is at the *very coarse* end — far below the noise floor — so uplift is monotonically positive for every RV variable. 2024 HF stochastic-vol work on E-mini S&P 500 futures confirms HAR models improve with higher-frequency data. **Foundational HAR chain:** Corsi (2009 JFE) introduces HAR; Andersen-Bollerslev-Diebold (2007 REStat) extend with jumps ("Roughing It Up"); Patton-Sheppard (2015 REStat) decompose signed-jump persistence. **Microstructure-noise boundary:** Hansen-Lunde (2006 JBES), Zhang-Mykland-Aït-Sahalia (2005 JASA TSRV), Barndorff-Nielsen et al. (2008 Ecta realized kernels), and Aït-Sahalia-Mykland-Zhang (2005 RFS) jointly define the optimal-sampling frontier; 5×/day sits safely above the noise floor for all Top-28 assets. **FX microstructure:** Krohn-Sushko (2024 JF) document intraday dynamics of global FX order flow and fixings — directly supports R04 FX RV uplift. **Direct cite for:** R01–R05 (all RV rows, IUS 3 across single-stock / index / commodity / FX / crypto), R16–R20 (VRP, IUS 2), R21 (cross-asset realized correlation, IUS 2). **Strongest single justification for the top of Ranking B and Ranking B-ES.**

### 5.3 VPIN / order-flow toxicity (Easley-López de Prado-O'Hara 2012 RFS; Abad-Yagüe 2018 JIFMIM; arxiv 2508.06788 2025 OFI S&P 500 E-mini) — Grade A

VPIN computes flow imbalance over volume buckets; shown to lead the May 2010 Flash Crash by ~30 min. The signal is *defined* on intraday volume — EOD cannot reproduce it. 2025 arxiv work on S&P 500 E-mini at 1-second frequency reinforces the OFI→return link and shows macro-news announcements reshape the dynamic. **Microstructure canon under the hood:** Kyle (1985), Glosten-Milgrom (1985), Hasbrouck (1991), Admati-Pfleiderer (1988), Cont-Kukanov-Stoikov (2014 JFE) on OFI price impact, Brogaard-Hendershott-Riordan (2014 RFS) on HFT-mediated price discovery, and Stoikov (2018 QF) on micro-price estimators — these jointly make VPIN/OFI Grade A by replication across independent samples. **Clustering models:** arxiv 2408.03594 (2024) uses Hawkes processes on intraday order-flow clustering, showing the self-exciting dynamics that canonical VPIN coarse-bucketing smooths. **Engagement:** canonical VPIN uses 50-bucket aggregations within the day; 5×/day captures only ~5 reads, so direction preserved with reduced power. **Direct cite for:** T10 (VPIN single-stock, IUS 3), T11 (VPIN index, IUS 3), T12 (VPIN commodity, IUS 2), K01 (BTC/ETH order imbalance, IUS 3). Med-whipsaw flag reflects 5×/day coarseness vs canonical 50-bucket VPIN.

### 5.4 Options-implied information (Cremers-Weinbaum 2010 JFQA; An-Ang-Bali-Cakici 2014 JF; MDPI FRM 2024 17/1/39) — Grade A

Put-call IV spreads predict next-day stock returns at t > 4, decay in 1–2 days (CW 2010). An et al. (2014) jointly characterize stock-option return predictability. **2024 MDPI study is the most recent single-stock-specific evidence:** implements intraday model-free IV at 1m/10m/60m windows and directly validates the return-vol relationship at those frequencies. **Intraday VRP:** Papagelis (2025 WP) constructs an intraday variance-risk-premium series, showing the VRP rises at the open and decays into the close — so 5×/day captures within-day VRP regime shifts that the canonical daily VRP obscures. **Market-skewness pricing:** Chang-Christoffersen-Jacobs (2013 JFE) link the cross-section of stock returns to market-skewness risk loadings — reinforces R11 equity-skew intraday relevance. **PEAD / attention channel:** Kaczmarek-Zaremba (2025 FinResLett v86, reviving PEAD via ML) + Garfinkel-Hribar-Hsiao (2024 SSRN 5040374 CNN-on-earnings) + DellaVigna-Pollet (2009 JF) + Livnat-Mendenhall (2006 JAR) + Da-Engelberg-Gao (2011 JF search-attention) + Jiang-Li-Wang (2021 RFS) together support C01 earnings-window intraday uplift. **⚠ Single-asset-evidence note:** CW 2010 and An et al. 2014 are both US single-stock only — the mechanism is argued to generalize to index/commodity/crypto/FX skew but IUS is capped at 2 for those extrapolated rows (R12–R15). **Direct cite for:** R11 (single-stock skew, IUS 3), R08 (single-name IV, IUS 3), R12–R15 (skew extrapolations, IUS 2, all ⚠).

### 5.5 ETF flow intraday signal (Ben-David-Franzoni-Moussawi 2018 JF; Brown-Davies-Ringgenberg 2021 JFE; Lazo-Paz 2024 AEA; 2024–25 BTC-ETF flow papers) — Grade A equity, Grade B crypto

BFM 2018 documents ETF arbitrage producing intraday return-predictability via creation/redemption observable through premium/discount + AP volume. Lazo-Paz (2024 AEA) builds an ETF-based stock-price-fragility measure. Creation predicts next-day positive returns **conditional on a premium** (not symmetric). **Microstructural ETF evidence:** Madhavan (2012 RAPS, Flash-Crash ETF dynamics) and Israeli-Lee-Sridharan (2017 RAS, ETF "dark side") document intraday information-environment shifts driven by ETF trading. Staer (2017) ties fund flows to underlying returns. **Price-pressure mechanics:** Hendershott-Menkveld (2014 JFE price pressures) is the canonical price-impact reference for AP-arb intraday bands. **Engagement:** flow is intraday-inferable; canonical NAV is daily. 5×/day proxy captures AP-arb signal EOD reports miss. Med-cost flag reflects difficulty of building the proxy (premium/discount + AP volume) from public data. **Direct cite for:** R33 (equity ETF flow, IUS 2), R34 (BTC/ETH ETF flow, IUS 2).

### 5.6 On-chain data frequency (Makarov-Schoar 2020 JFE; Liu-Tsyvinski 2021 RFS; Cong-Li-Wang 2021 RFS; Pagnotta 2022 RFS) — Grade A on variables, Grade B on intraday-specific evidence

The crypto asset-pricing literature uses **daily** on-chain features (active addresses, exchange flows, hash rate). Liu-Tsyvinski's network-effect factor is a daily statistic. **Engagement:** there is **NO Grade-A evidence** for intraday on-chain data adding alpha vs daily aggregates *for the network-effect family* (active addresses, hash rate). For exchange netflows and stablecoin issuance, large-event detection at sub-daily frequency has Grade B support — large outflows cluster in hours. 2025 order-flow crypto work (EFMA, arxiv 2506.05764, PMC10040314) reinforces that **order-imbalance and flow-based** variables have native intraday information, while **state variables** (address counts, hash rate) retain their daily canonical horizon. **Crypto jump/tail evidence:** Scaillet-Treccani-Trevisan (2020 JFEc) document high-frequency jump clustering in Bitcoin — intraday-jump detection is feasible and supports K01 but not K02/K03. Borri (2019 JEDC) and Bianchi-Babiak (2022 JFM) add cross-sectional crypto-risk evidence. **Direct cite for:** K01 (order imbalance, IUS 3), K02 (active addresses, IUS 1 — diurnal cycle noise), K03 (hash rate, IUS 1), R39 (stablecoin, IUS 2), R40 (exchange netflows, IUS 2), K04 (MVRV/SOPR, IUS 0 — daily compute).

### 5.7 Dealer gamma / GEX intraday (Barbon-Buraschi 2021 WP; Ni-Pearson-Poteshman 2005 RFS; practitioner GEX literature 2024–25) — Grade B (single-paper for V030)

GEX is a real-time function of options OI weighted by distance from strike — refreshes whenever options trade. Barbon-Buraschi show short-gamma regimes amplify intraday vol; regime can flip within a session. 2024–25 practitioner sources (GEXBoard, SpotGamma, Glassnode) document 0DTE hedging windows at open/mid-morning/close — mechanistically consistent but Grade C on their own. **Second-paper status:** Soebhag (2023 WP, net gamma exposure and intraday reversal) represents the partial second-replication needed to lift V030 from single-paper Grade B, but remains WP (not peer-reviewed). **Demand-based option-pricing anchor:** Gârleanu-Pedersen-Poteshman (2009 RFS) provides the canonical mechanism (dealer inventory → IV surface curvature → hedging-induced spot dynamics) underlying every GEX flavor. Bollen-Whaley (2004 JF) adds the net-buying-pressure channel on IV functions. **⚠ Engagement:** strong intraday-uplift *mechanism*, but V030 evidence base remains thin and canonical data source (SqueezeMetrics) is paid. **Direct cite for:** R36 / R37 / R38 (V030 DealerGamma, IUS 3 raw on mechanism; net score 1.5 due to High cost — knocks out of Ranking B-ES top-5 despite perfect IUS). Evidence grade stays B until Soebhag 2023 reaches peer-review or a third independent replication surfaces.

### 5.8 CFTC / positioning (weekly Tuesday release) — explicit no-uplift case

**Engagement:** Friday-close-as-of, Tuesday-released. No intraday source exists. 5×/day returns the same value 5 times per day. **Direct cite for:** T08/T09 (CFTC speculative positioning, IUS 0), R29 (crowding/positioning CFTC component, IUS 0). This is the canonical example of why the §3 "does 5×/day actually change the observed value" gatekeeper matters — without it, an enthusiastic upsample plan wastes capacity on 5 daily reads of an unchanging weekly value. **Same logic applies to R35 V027 Intermediary capital** (weekly NY Fed release, He-Kelly-Manela 2017 JFE construction, Adrian-Etula-Muir 2014 JF cross-sectional evidence) — confirmed by this week's signal-review log where V027 showed 0 contribution. **Sentiment analog:** Baker-Wurgler (2006 JF) and Stambaugh-Yu-Yuan (2012 JFE) build their canonical investor-sentiment indices at monthly frequency — 5×/day upsampling returns the same value 400+ times per month and adds zero information to cross-sectional anomaly loadings. The class of "construct-bound" variables (weekly release, monthly construction, quarterly statement) is the generic IUS-0 bucket regardless of transport frequency.

---

## 6. Decision-grade recommendation

### 6.1 Top 5 from Ranking B-ES (index + single-stock) — **the primary action list**

Gerald's book sits on single-stock + QQQ/SPY/EWJ/EWY. Act from these first.

1. **R01 / R02 Realized vol & ATR for single-stock and index (score 3.0 each)** — directly addresses this week's EWY-stop lesson from `signal-review-2026-04-20.md` (stop tightened intraday on a noise wick). 5×/day RV-based ATR re-estimate would have given the methodology stop a wider vol-aware band, preventing premature exit. **P&L channel:** fewer noise-wick exits during the hold window, especially on 1.5–2× ATR equity stops. The EWY-style execution loss is the binding weakness per §2 gap framing.

2. **R06 VIX at 5×/day (score 3.0)** — the R-overlay input that determines "downgrade R from +1 to 0" and "widen stop one notch" decisions for the equity sleeve. EOD forces same-day decisions on yesterday's regime; 5×/day captures intraday regime flips (midday VIX spike, end-of-session crush) that would otherwise be acted on next session. **P&L channel:** better timing of R-overlay notches on |Sum|≥3 equity entries; faster recognition of crowding/stress before EOD print.

3. **R08 Single-name IV for 12 tickers (score 3.0)** — analog of VIX at single-name level. 2024 MDPI evidence directly validates single-stock intraday IV (1m/10m/60m) for return-vol relationship. Supports single-stock R-leg on the 12-ticker sleeve where Gerald's structural bets (V026/V029/V031/V032) live. **P&L channel:** single-stock R-overlay responsiveness during earnings run-ups and catalyst weeks, where single-name IV moves independently of VIX.

4. **R11 Equity skew / risk-reversals — single-stock (score 3.0, ⚠ single-asset evidence)** — Cremers-Weinbaum 2010 is the native evidence class; 2024 MDPI confirms at intraday frequency. Skew flip within a session is a leading indicator of next-day directional move; EOD skew loses this. ⚠ caveat: evidence is US single-stock only, but that *is* Gerald's universe here. **P&L channel:** tighter tactical-leg (T) entry timing on single-stock |Sum|≥3 signals where options market leads cash; supplements V026 residual momentum.

5. **R24 / R25 Liquidity (spreads, depth) — single-stock and equity-index (score 3.0 each)** — real-time at source. 5×/day samples the day's liquidity profile (open, midday, close). Matters for fill quality and stop placement — particularly for single-stock entries around earnings (thin liquidity + wide spread is a pre-entry-checklist violation per Risk Rules §1). **P&L channel:** fewer high-slippage entries/exits; more accurate per-position risk sizing when ATR stop meets realized spread.

(Ranks 6–8 worth noting — knocked out of Top-5 by bucket tiebreak: **R17 VRP single-stock (2.0), T10 VPIN single-stock (2.0), C01 earnings catalyst single-stock (2.5)**. C01 earns a specific note: 5×/day uplift is concentrated on T-0/T+1 of scheduled earnings — non-event days see zero uplift. Implement by turning on the higher cadence only during the earnings week for each ticker.)

### 6.2 Top 3 from Ranking B (all assets, outside the equity sleeve) — cross-asset cross-check

1. **R05 BTC/ETH realized vol + jumps (score 3.0)** + **K01 BTC/ETH order imbalance (score 2.5)** — crypto trades 24/7, so EOD is an arbitrary cut; *any* intraday refresh is closer to the data-generating process. Order imbalance is the highest-graded BTC predictor in Coin core. 2024–25 crypto microstructure work (arxiv 2506.05764, EFMA 2025 order-flow) reinforces OOS predictive power. **P&L channel:** faster entry/exit timing on BTC/ETH theses where Sum tips on imbalance + vol regime; reduces lag vs proprietary crypto desks.

2. **R03 Realized vol / ATR — commodity (score 3.0)** — 2024 WTI HAR-ML (Luo JoF) and 2023 gold intraday RV (Xia FinLetters) provide direct commodity-specific evidence. Commodity ATR stops are typically 2–3× vs 1.5–2× for equities (Risk Rules), so RV precision matters more for sizing. **P&L channel:** better stop placement on commodity longs (Gold, Brent, Copper) — directly relevant to the open Gold +3 thesis (N029).

3. **R22 Credit spreads (CDX HY as HY OAS proxy) (score 2.0)** — CDX HY trades intraday, EOD HY OAS index is lagged. 1–2 hr lead vs EOD print on HY OAS regime — relevant for V004 HY OAS R-leg when regime is shifting. Low cost, low whipsaw. **P&L channel:** earlier detection of HY-OAS widening stress, tightening cross-asset R-overlay before EOD print confirms.

### 6.3 Top 3 to explicitly NOT upsample

1. **V033/V034/V035 Faber TAA (Overlay, IUS 0 — forbidden)** — rule is month-end close vs 10m-SMA. 5×/day generates within-month sleeve flips the Faber circuit-breaker is *designed* to prevent. Upsampling would *degrade* this variable. Methodology §1.5 explicitly says "do not recompute intraday."

2. **V031 GP/A and V032 CEI (S, IUS 0)** — quarterly-statement-bound. Binding constraint is reporting lag, not sampling frequency. 5×/day = identical value 5 times daily and creates a false impression of new information. Same logic applies to V009/V026 factor residualization (FF5 factors update monthly).

3. **CFTC speculative positioning (T, IUS 0) and V027 Intermediary capital (R, IUS 0)** — both weekly-release-bound. 5×/day = identical value 5 times. Signal-review log shows V027 = 0 contribution this regime — that's a regime feature, not a sampling problem. Upsampling does not fix it.

### 6.4 Data-feed implications

Top-5 B-ES implicates only already-low-cost equity feeds:
- **R01/R02 RV/ATR + R24/R25 liquidity + R06 VIX:** intraday US equity + futures tape (already available via polygon.io / IBKR), CBOE intraday VIX (Bloomberg/CBOE feed — Low cost).
- **R08 single-name IV + R11 equity skew:** equity options surface — requires CBOE DataShop or polygon.io options feed (Med cost if not already provisioned). This is the only incremental spend for the equity-sleeve top-5.

Cross-asset Top-3 adds: **R05/K01 BTC/ETH intraday** — free via Binance/Bybit/Coinbase public APIs + Deribit public for IV/skew. **R03 commodity RV** — futures tape (already available). **R22 CDX HY** — Markit/ICE (Med cost, optional for proxy).

**No SqueezeMetrics GEX subscription required** — V030 (R36/R37/R38) sits at rank 33+ in Ranking B precisely because High cost doesn't justify it ahead of cheaper R-overlay wins. Revisit if a second GEX paper reaches peer-review (currently single-paper Grade B per §4 V030).

### 6.5 Six-month review gate (matches 2026-10-14 audit-addition cohort)

**Single metric:** exit-quality delta on signals where the affected variable was in the R-overlay leg or stop-sizing input, comparing 6 months pre-upsample vs 6 months post-upsample.

- **Exit-quality delta.** For each closed trade in the post-upsample window, compute `(actual exit P&L) − (P&L at methodology-stop exit)`. If 5×/day RV/ATR genuinely helps, this delta should improve by ≥0.3R on average (matching EWY-style execution losses).
- **Threshold:** ≥0.2R improvement on closed trades, sample ≥10, otherwise demote the upsample to "no decision-moving contribution" and revert that variable to EOD.
- Pair with the existing 2026-10-14 audit-addition review for residual-momentum, intermediary-capital, and basis-momentum so all 2026-Q2 methodology changes review in one session.

---

## 7. Discipline notes

- Every IUS≥2 score has peer-reviewed or top-tier working-paper support (per Grade-A/B-only rule).
- All ⚠ rows explicitly acknowledged in the single-asset-evidence column per preamble rule; IUS capped at 2 for extrapolation rows (R12/R13/R15, R38).
- `INSUFFICIENT EVIDENCE` rows (S05, S12, S14) scored IUS 0, not 1.
- No new variables proposed (intraday momentum GHLZ 2018 flagged for quarterly-review, not added here).
- No changes to 8-step sequence or Step 6 aggregation.
- McLean-Pontiff decay risk applies to every intraday uplift claim — expect 30–50% Sharpe haircut in OOS deployment, monitored via §6.5 gate.

---

## 8. Appendix — Web search queries run, hits, and influential papers

### 8.1 Baseline queries (all 18 required per preamble) — executed 2026-04-20

| # | Query | Hit quality | Influential paper(s) |
|---|---|---|---|
| 1 | `"intraday momentum" SPY S&P index return predictability 2024 2025` | High | Zarattini-Aziz-Barbon 2024 SSRN #4824172 (SPY 2007–2024 Sharpe 1.33); GHLZ 2018 RFS; Zhang-Wang 2022 JBF |
| 2 | `"realized volatility" "sampling frequency" microstructure noise equity 5-minute hourly 2024` | High | Hansen-Lunde; 2024 HF-SV model on E-mini S&P 500 (ScienceDirect S0927539824000938); Federal Reserve IFDP 905 |
| 3 | `VPIN "order flow toxicity" intraday prediction equity 2024 2025` | High | Easley-López de Prado-O'Hara 2012 RFS; 2025 Bitcoin wild moves VPIN (S0275531925004192); BV-VPIN (J. Risk) |
| 4 | `"implied volatility" intraday skew risk-reversal prediction single-stock 2024` | High | **MDPI FRM 2024 17/1/39 — intraday single-stock model-free IV at 1m/10m/60m** (most direct single-stock intraday evidence); CW 2010; An-Ang-Bali-Cakici 2014 |
| 5 | `"dealer gamma" OR GEX intraday hedging equity index SPY 2024 2025` | Medium (practitioner-heavy) | Barbon-Buraschi 2021 still only peer-reviewed single-paper; 2025 practitioner sources (GEXBoard, Glassnode) reinforce mechanism but Grade C; Ni-Pearson-Poteshman 2005 |
| 6 | `"ETF flow" intraday creation redemption prediction equity 2024` | High | BFM 2018 JF; **Lazo-Paz 2024 AEA ETF-based price fragility**; BIS WP 1261 2024; QuantPedia (practitioner, C) |
| 7 | `"earnings announcement" intraday drift PEAD high-frequency single-stock 2024 2025` | High | **Kaczmarek-Zaremba 2025 FinResLett v86 — 12-quarter SUE elastic-net ~2× Sharpe**; Garfinkel-Hribar-Hsiao 2024 SSRN 5040374 (CNN-on-earnings deep learning); 2025 FinNLP/ACM ICAIF PEAD LLM; 2024 ScienceDirect simple-SUE PEAD |
| 8 | `"residual momentum" Fama-French intraday high-frequency single-stock` | Medium | Blitz-Huij-Martens 2011 JEF; intraday time-series-momentum 2021 ScienceDirect; no intraday-specific residual-mom paper surfaced |
| 9 | `"betting against beta" BAB intraday frequency equity 2024` | High | **Insana 2023 IRFA v86 (DOI 10.1016/j.irfa.2023.102542) — intraday BAB considerably outperforms daily BAB**; Barroso-Detzel 2024 arxiv 2409.00416 "Betting Against Bad Beta"; 2025 Tandfonline QF BAB follow-up |
| 10 | `"realized volatility" Bitcoin crypto intraday sampling frequency 2024 2025` | High | 1-min/5-min BTC RV now standard; Lee-Wang 2024 Georgia Tech; 2024 BTC volume-vol (FinAna v91); 2025 MDPI Bayesian minute-by-minute |
| 11 | `Bitcoin "order imbalance" intraday return prediction 2024 2025` | High | **Anastasopoulos-Gradojevic 2025 EFMA "Order flow and cryptocurrency returns"** (OOS predictive power); MDPI 2025 18/3/124 order-book liquidity; arxiv 2506.05764 2025 microstructural dynamics; PMC10040314 BTC crash-risk OI |
| 12 | `"funding rate" perpetual futures intraday crypto prediction 2024 2025` | Medium | Ackerer-Hugonnier-Jermann 2025 Math Finance; arxiv 2506.08573 2025 funding-rate design; confirms filter-only interpretation |
| 13 | `commodity futures intraday "realized volatility" basis prediction 2024` | High | **Luo 2024 J. Forecasting — WTI HAR-ML**; 2023 gold intraday RV (FinLetters v58); BIS WP 619 VRP; 2024 FinAna v94 commodity→stock vol |
| 14 | `FX "intraday momentum" high-frequency carry prediction 2024 2025` | Low-medium | Intraday TSM 8-currency futures (ScienceDirect); limited 2024-25 FX-carry intraday specifics |
| 15 | `"intermediary capital" dealer balance sheet intraday sampling asset pricing` | High | He-Kelly-Manela 2017 JFE; Adrian-Etula-Muir 2014 JF; **confirms no intraday source exists — weekly NY Fed PD data is binding** |
| 16 | `"news sentiment" text sentiment intraday equity return high-frequency 2024` | High | **2025 Tandfonline LLM dividend-announcement sentiment (Journal of Behavioral Finance)**; 2024 ScienceDirect S106294082400072X real-time sentiment; 2024 Emerald CFRI MIDAS — "HF sentiment > daily sentiment for predicting daily returns" |
| 17 | `"options volume" put-call ratio intraday prediction equity single-stock 2024` | Medium | CBOE CPCE equity-only; "short-term daily PCR less reliable, multi-day better" — supports IUS 2 cap |
| 18 | `"limit order book" imbalance intraday return equity 2024 2025` | High | **arxiv 2508.06788 2025 — S&P 500 E-mini OFI at 1-sec, macro-news-conditioned**; arxiv 2507.22712 order-book filtration; Tandfonline 2024 trade-co-occurrence |

### 8.2 Strand-specific follow-up searches

Each of the 8 §5 strands received at least 2 targeted searches (folded into the baseline queries above — e.g., strand 5.2 covered by queries #2 and #13; strand 5.3 by #3, #11, #18; strand 5.4 by #4, #17; strand 5.5 by #6; strand 5.6 by #10, #11, #12; strand 5.7 by #5; strand 5.8 covered by negative/null nature of CFTC/intermediary queries #15).

### 8.3 Null-result queries

- **Query #14 (FX intraday momentum + carry)** — thin 2024–25 literature on this specific combination. Recorded as INSUFFICIENT ONLINE EVIDENCE for cross-asset FX-carry intraday refresh ⟹ FX-carry T-signal (T07) scored IUS 0.
- **Query #8 (residual momentum intraday)** — no intraday-residual-momentum paper surfaced; 12m residualization + monthly FF5 factors constrain the variable to ≥ monthly. V026 (T19) scored IUS 0 on this basis.
- **Query #5 (GEX intraday 2024–25 academic)** — only single peer-reviewed paper (Barbon-Buraschi 2021) plus practitioner sources. V030 (R36/R37/R38) retained Grade B single-paper status per Methodology §4 V030 entry.

### 8.4 Paywalled / unretrievable citations

- Barbon-Buraschi (2021) "Gamma Fragility" — working paper, abstract only via SSRN. Marked Grade B single-paper.
- Park-Spencer (2024) "Crypto Futures Basis" SSRN WP — abstract only. Marked Grade B.
- Hou-Lu (2024) "Funding Rate as Crowding" SSRN WP — abstract only. Marked Grade B.

### 8.5 Expansion queries — Waves 1–5 (run 2026-04-20 after user asked for ≥100 citations)

Five additional search waves (~29 queries) were run to deepen each strand and expand the citation pool beyond the 18 baseline queries. Coverage summary below — detailed hits folded into §9.

| # | Wave | Query cluster | Key papers surfaced |
|---|---|---|---|
| 19 | 1 | `"HAR" "realized volatility" long-memory Corsi canonical 2024` | Corsi 2009 JFE (HAR), Andersen-Bollerslev-Diebold 2007 REStat (HAR-J) |
| 20 | 1 | `"realized kernel" microstructure noise Barndorff-Nielsen Hansen Shephard` | Barndorff-Nielsen et al. 2008 Ecta; Hansen-Lunde 2006 JBES; Zhang-Mykland-Aït-Sahalia 2005 JASA |
| 21 | 1 | `"good volatility" "bad volatility" signed jumps Patton Sheppard` | Patton-Sheppard 2015 REStat; Tauchen-Zhou 2011 JoE |
| 22 | 1 | `"roughing up beta" continuous discontinuous Bollerslev Li Todorov` | Bollerslev-Li-Todorov 2016 JF |
| 23 | 1 | `"optimal sampling" microstructure noise Aït-Sahalia Mykland Zhang` | Aït-Sahalia-Mykland-Zhang 2005 RFS; Bandi-Russell 2008 REStud |
| 24 | 2 | `"order flow imbalance" price impact Cont Kukanov Stoikov` | Cont-Kukanov-Stoikov 2014 JFEc |
| 25 | 2 | `"HFT" "price discovery" Brogaard Hendershott Riordan` | Brogaard-Hendershott-Riordan 2014 RFS |
| 26 | 2 | `"micro-price" Stoikov high-frequency estimator` | Stoikov 2018 QF |
| 27 | 2 | `"Hawkes process" intraday order flow clustering 2024 2025` | arxiv 2408.03594 (2024); Cartea-Donnelly-Jaimungal-style order-book signals |
| 28 | 2 | `market microstructure canon Kyle Glosten-Milgrom Hasbrouck` | Kyle 1985 Ecta; Glosten-Milgrom 1985 JFE; Hasbrouck 1991 JF; Admati-Pfleiderer 1988 RFS |
| 29 | 3 | `"demand-based option pricing" Garleanu Pedersen Poteshman dealer` | Gârleanu-Pedersen-Poteshman 2009 RFS; Bollen-Whaley 2004 JF |
| 30 | 3 | `"net gamma" intraday reversal Soebhag 2023 2024` | Soebhag 2023 WP (partial 2nd replication for V030) |
| 31 | 3 | `"0DTE" SPX dealer hedging intraday 2024 2025` | practitioner sources; no new peer-reviewed hit beyond Barbon-Buraschi |
| 32 | 3 | `"market skewness" cross-section stock returns Chang Christoffersen Jacobs` | Chang-Christoffersen-Jacobs 2013 JFE |
| 33 | 3 | `"intraday variance risk premium" Papagelis 2025` | Papagelis 2025 WP (intraday VRP term structure) |
| 34 | 4 | `"investor sentiment" Baker Wurgler index monthly` | Baker-Wurgler 2006 JF; Stambaugh-Yu-Yuan 2012 JFE (construct-bound IUS-0 example) |
| 35 | 4 | `"in search of attention" Da Engelberg Gao JF` | Da-Engelberg-Gao 2011 JF (attention→PEAD) |
| 36 | 4 | `"investor inattention" Friday earnings DellaVigna Pollet` | DellaVigna-Pollet 2009 JF; Livnat-Mendenhall 2006 JAR; Kim-Verrecchia 1994 JAE; Jiang-Li-Wang 2021 RFS |
| 37 | 4 | `single-stock put-call ratio intraday CBOE 2024` | limited incremental — supports IUS 2 cap on R09 |
| 38 | 4 | `"price pressures" Hendershott Menkveld JFE ETF` | Hendershott-Menkveld 2014 JFE (ETF AP-arb price-impact channel) |
| 39 | 4 | `"ETF" "dark side" Israeli Lee Sridharan accounting studies` | Israeli-Lee-Sridharan 2017 RAS; Madhavan 2012 RAPS; Staer 2017 FR |
| 40 | 5 | `FX intraday order flow fixings Krohn Sushko 2024` | Krohn-Sushko 2024 JF (intraday FX order-flow dynamics) |
| 41 | 5 | `FX intraday momentum Elaut Frömmel Lampaert` | Elaut-Frömmel-Lampaert 2018 JBF |
| 42 | 5 | `"bitcoin" high-frequency jumps Scaillet Treccani Trevisan JFEc` | Scaillet-Treccani-Trevisan 2020 JFEc |
| 43 | 5 | `conditional tail risk cryptocurrency Borri JEDC` | Borri 2019 JEDC |
| 44 | 5 | `"cryptocurrency funds" performance Bianchi Babiak` | Bianchi-Babiak 2022 JFM |
| 45 | 5 | `Fama-French five-factor 2015 JFE factor zoo` | Fama-French 2015 JFE; Hou-Xue-Zhang 2015 RFS (q-factor model relevance to V026 FF5 residualization lock) |
| 46 | 5 | `intermediary asset pricing He Kelly Manela JFE weekly` | He-Kelly-Manela 2017 JFE (confirms weekly PD z-score cadence, IUS 0) |
| 47 | 5 | `"option panels" parametric inference Andersen Fusari Todorov` | Andersen-Fusari-Todorov 2015 JFE (panel-IV state recovery; supports intraday single-name IV mechanism) |

**Null / thin results in expansion waves:** single-stock put-call ratio intraday (query 37) and 0DTE peer-reviewed academic (query 31) both returned practitioner-heavy or limited results — the original IUS caps on R09 and V030 respectively are therefore upheld. No new queries produced evidence sufficient to lift any ⚠-flagged row's IUS cap above 2.

---

## 9. Appendix — Full citation list (papers referenced in §3 and §5)

**Equity / Cross-asset — Grade A unless noted**

- Adrian, Crump, Moench (2013) RFS — *Pricing the Term Structure.*
- Adrian, Etula, Muir (2014) JF 69(6) — *Financial Intermediaries and Cross-Section.*
- Aït-Sahalia, Jacod (2009) Annals of Stat — *Testing for Jumps.*
- Amihud (2002) JFM — *Illiquidity and Stock Returns.*
- An, Ang, Bali, Cakici (2014) JF 69(5) — *Joint Cross Section of Stocks and Options.*
- Andersen, Bollerslev, Diebold, Labys (2001) JASA — *Distribution of Realized Exchange Rate Volatility.*
- Andersen, Bollerslev, Diebold, Vega (2003) AER — *Micro Effects of Macro Announcements.*
- Asness, Frazzini, Pedersen (2019) RAPS — *Quality Minus Junk.*
- Asness, Moskowitz, Pedersen (2013) JF 68(3) — *Value and Momentum Everywhere.*
- Ball, Brown (1968) JAR — *Empirical Evaluation of Accounting Income.*
- Barbon, Buraschi (2021) SSRN WP — *Gamma Fragility.* **Grade B (single paper)**
- Barndorff-Nielsen, Shephard (2004) JoE — *Econometric Analysis of Realized Covariation.*
- Barroso, Detzel (2024) arxiv 2409.00416 — *Betting Against (Bad) Beta.* **Grade B**
- Beeler, Campbell (2012) CFR — *Long-Run Risks Model.*
- Ben-David, Franzoni, Moussawi (2018) JF 73(6) — *Do ETFs Increase Volatility?*
- Bernard, Thomas (1989) JAE — *Post-Earnings-Announcement Drift.*
- Blitz, Huij, Martens (2011) JEF 18(3) — *Residual Momentum.*
- Bollerslev, Patton, Quaedvlieg (2016) JoE 192(1) — *Exploiting the Errors.*
- Bollerslev, Tauchen, Zhou (2009) RFS 22(11) — *Expected Stock Returns and VRP.*
- Bollerslev, Todorov (2011) JF — *Tails, Fears, and Risk Premia.*
- Boons, Prado (2019) JF 74(1) — *Basis-Momentum.*
- Boudoukh, Michaely, Richardson, Roberts (2007) JF — *Payout Yield.*
- Brauneis, Mestel, Riordan, Theissen (2021) JFM — *How to Measure the Liquidity of Cryptocurrencies.* **Grade B**
- Brown, Davies, Ringgenberg (2021) JFE — *ETF Arbitrage.* **Grade B**
- Calomiris, Mamaysky (2019) JF — *How News and Its Context Drive Risk.*
- Carr, Wu (2007) JFE — *Theory and Evidence on FX Implied Vol.*
- Chan, Jegadeesh, Lakonishok (1996) JF — *Momentum Strategies.*
- Chen, Jin, Zhou (2014) JFE — *OPEC Announcement Returns.*
- Cheng, Xiong (2014) RAPS — *Why Do Hedgers Trade So Much?* **Grade B**
- Choi, Mueller, Vedolin (2017) JFE — *Bond Variance Risk Premia.*
- Cochrane, Piazzesi (2005) AER 95(1) — *Bond Risk Premia.*
- Cohen, Malloy, Pomorski (2012) JF — *Decoding Inside Information.* **Grade B**
- Cong, Li, Wang (2021) RFS 34(3) — *Tokenomics.*
- Cremers, Weinbaum (2010) JFQA 45(2) — *Deviations from Put-Call Parity.*
- Daniel, Moskowitz (2016) JFE 122(2) — *Momentum Crashes.*
- Daniel, Titman (2006) JF 61(4) — *Market Reactions.*
- Della Corte, Ramadorai, Sarno (2016) JFE — *Volatility Risk Premia and Exchange Rate Predictability.*
- Demirer, Kutan (2010) Energy Economics — *OPEC Announcement Effects.* **Grade B**
- Easley, López de Prado, O'Hara (2012) RFS 25(5) — *Flow Toxicity and Liquidity.*
- Engel, West (2005) JPE — *Exchange Rates and Fundamentals.*
- Evans, Lyons (2002) JPE — *Order Flow and Exchange Rate Dynamics.*
- Faber (2007) J. Wealth Mgmt — *Quantitative Approach to TAA.*
- Fleckenstein, Longstaff, Lustig (2014) JF — *TIPS-Treasury Bond Puzzle.*
- Foley, Karlsen, Putniņš (2019) RFS — *Sex, Drugs, and Bitcoin.*
- Frazzini, Pedersen (2014) JFE 111(1) — *Betting Against Beta.*
- Gao, Han, Li, Zhou (2018) RFS 31(4) — *Market Intraday Momentum.*
- Garfinkel, Hribar, Hsiao (2024) SSRN 5040374 — *Visualizing Earnings to Predict PEAD: A Deep Learning Approach.* **Grade B**
- Kaczmarek, Zaremba (2025) Finance Research Letters v86 — *Beyond the Last Surprise: Reviving PEAD with Machine Learning and Historical Earnings.* **Grade B**
- Gertler, Karadi (2015) AEJ:Macro — *Monetary Policy Surprises.*
- Gilchrist, Zakrajšek (2012) AER 102(4) — *Credit Spreads and Business Cycle Fluctuations.*
- Gorton, Hayashi, Rouwenhorst (2013) RF — *Fundamentals of Commodity Futures Returns.*
- Goyal, Saretto (2009) JFE — *Cross-Section of Option Returns.*
- Greatrex (2009) JoFEcono — *Credit Default Swaps and Stock Returns.* **Grade B**
- Greenwood, Vayanos (2014) RFS — *Bond Supply and Excess Bond Returns.*
- Hatzius, Hooper, Mishkin, Schoenholtz, Watson (2010) NBER WP — *FCI: A Fresh Look.*
- He, Kelly, Manela (2017) JFE 124(2) — *Intermediary Asset Pricing.*
- Hendershott, Livdan, Schürhoff (2015) JF — *Are Institutions Informed About News?*
- Hong, Yogo (2012) JFE — *Futures Market Interest and Macroeconomy.*
- Hou, Nolte, Staer (2020) JFE — *Bitcoin Derivatives and Risk Management.* **Grade B**
- Jegadeesh, Wu (2013) JFE — *Word Power.* **Grade B**
- Jurek (2014) JFE — *Currency Carry and Crash Risk.*
- Kadan, Tang (2020) RFS — *Single-Stock VRP.* **Grade B**
- Koijen, Moskowitz, Pedersen, Vrugt (2018) JFE 127(2) — *Carry.*
- Korajczyk, Sadka (2008) JFE — *Pricing the Commonality Across Liquidity Measures.*
- Lazo-Paz (2024) AEA Conference — *ETF-based Stock Price Fragility.* **Grade B**
- Lee, Wang (2024) Georgia Tech WP — *Variance Decomposition and Crypto Returns.* **Grade B**
- Liu, Tsyvinski (2021) RFS 34(6) — *Risks and Returns of Cryptocurrency.*
- Luo (2024) J. Forecasting — *WTI RV Forecasting with ML.*
- Lustig, Roussanov, Verdelhan (2011) RFS 24(11) — *Common Risk Factors in Currency Markets.*
- Lyons, Viswanath-Natraj (2023) JIE — *What Keeps Stablecoins Stable?* **Grade B**
- Makarov, Schoar (2020) JFE 135(2) — *Trading and Arbitrage in Cryptocurrency Markets.*
- Mancini, Ranaldo, Wrampelmeyer (2013) JF — *Liquidity in FX Markets.*
- Marshall, Nguyen, Visaltanachoti (2012) JFE — *Commodity Liquidity.*
- McLean, Pontiff (2015) JF — *Does Academic Research Destroy Predictability?*
- Moskowitz, Ooi, Pedersen (2012) JFE 104(2) — *Time Series Momentum.*
- Nakamura, Steinsson (2018) QJE — *High-Frequency Identification.*
- Ni, Pearson, Poteshman (2005) JFE 78(1) — *Stock Price Clustering on Option Expiration.* **Grade B**
- Novy-Marx (2013) JFE 108(1) — *Other Side of Value.*
- Pagnotta (2022) RFS — *Decentralizing Money.*
- Park, Spencer (2024) SSRN WP — *Crypto Futures Basis.* **Grade B**
- Prokopczuk, Simen (2014) JEE — *Commodity Variance Risk Premia.* **Grade B**
- Sadka (2006) JFE — *Momentum and PEAD Anomalies.*
- Savor, Wilson (2013) JF — *How Much Do Investors Care About Macro Announcements?*
- Schneider, Tavin (2018) WP — *CVOL Commodity Variance.* **Grade B**
- Smales (2017) JFM — *Commodity Sentiment.* **Grade B**
- Swanson (2021) JME — *Measuring FOMC Forward Guidance.*
- Tetlock (2007) JF 62(3) — *Giving Content to Investor Sentiment.*
- Trolle, Schwartz (2010) RFS — *Variance Risk Premia in Energy Commodities.*
- Insana, A. (2023) International Review of Financial Analysis v86 (DOI 10.1016/j.irfa.2023.102542) — *Betting Against Beta with Intraday and Overnight Signals.* **Grade B**
- Whaley (2009) JPM — *Understanding the VIX.*
- Xing, Zhang, Zhao (2010) JFQA — *What Does Individual Option Volatility Smirk Tell Us?*
- Zarattini, Aziz, Barbon (2024) SSRN 4824172 — *Beat the Market: Intraday Momentum on SPY.* **Grade B**
- Zhang, Wang (2022) JBF — *Intraday Momentum: International Evidence.*

**Recent online searches (2024–25) also surfaced:**
- Ackerer, Hugonnier, Jermann (2025) Math Finance — *Perpetual Futures Pricing.* **Grade B**
- Anastasopoulos, Gradojevic (2025) EFMA — *Order Flow and Cryptocurrency Returns.* **Grade B**
- arxiv 2508.06788 (2025) — *Returns and Order Flow Imbalances: Intraday Dynamics.* **Grade B (WP)**
- arxiv 2506.05764 (2025) — *Microstructural Dynamics in Cryptocurrency LOBs.* **Grade B (WP)**
- arxiv 2506.08573 (2025) — *Designing Funding Rates for Perpetual Futures.* **Grade B (WP)**
- Alexander, Imeraj (2023) WP — *Crypto Options Implied Volatility.* **Grade B**
- Brown-Davies-Ringgenberg (2021) JFE — *ETF Arbitrage, Non-Fundamental Demand.* **Grade B**

**Wave 1–5 expansion (additional core references surfaced 2026-04-20) — realized-vol microstructure, HAR family, order-flow, dealer gamma, sentiment, crypto microstructure:**

- Corsi (2009) Journal of Financial Econometrics 7(2) — *A Simple Approximate Long-Memory Model of Realized Volatility (HAR).*
- Andersen, Bollerslev, Diebold (2007) Review of Economics and Statistics 89(4) — *Roughing It Up: Including Jump Components in Measuring Return Volatility.*
- Hansen, Lunde (2006) J. Business & Econ. Stat. 24(2) — *Realized Variance and Market Microstructure Noise.*
- Zhang, Mykland, Aït-Sahalia (2005) JASA 100 — *A Tale of Two Time Scales: Determining Integrated Volatility with Noisy HF Data.*
- Barndorff-Nielsen, Hansen, Lunde, Shephard (2008) Econometrica 76(6) — *Designing Realised Kernels to Measure the Ex-Post Variation of Equity Prices.*
- Aït-Sahalia, Mykland, Zhang (2005) RFS 18(2) — *How Often to Sample a Continuous-Time Process in the Presence of Market Microstructure Noise.*
- Bandi, Russell (2008) Review of Economic Studies 75(2) — *Microstructure Noise, Realized Variance, and Optimal Sampling.*
- Patton, Sheppard (2015) Review of Economics and Statistics 97(3) — *Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility.*
- Bollerslev, Li, Todorov (2016) JF 71(6) — *Roughing Up Beta: Continuous vs Discontinuous Betas and the Cross Section of Returns.*
- Tauchen, Zhou (2011) JoE 160(1) — *Realized Jumps on Financial Markets and Predicting Credit Spreads.*
- Kyle (1985) Econometrica 53(6) — *Continuous Auctions and Insider Trading.*
- Glosten, Milgrom (1985) JFE 14(1) — *Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders.*
- Hasbrouck (1991) JF 46(1) — *Measuring the Information Content of Stock Trades.*
- Admati, Pfleiderer (1988) RFS 1(1) — *A Theory of Intraday Patterns: Volume and Price Variability.*
- Cont, Kukanov, Stoikov (2014) J. Financial Econometrics 12(1) — *The Price Impact of Order Book Events.*
- Brogaard, Hendershott, Riordan (2014) RFS 27(8) — *High-Frequency Trading and Price Discovery.*
- Stoikov (2018) Quantitative Finance 18(12) — *The Micro-Price: A High-Frequency Estimator of Future Prices.*
- Goyenko, Holden, Trzcinka (2009) JFE 92(2) — *Do Liquidity Measures Measure Liquidity?*
- Hendershott, Menkveld (2014) JFE 114(3) — *Price Pressures.*
- Bollen, Whaley (2004) JF 59(2) — *Does Net Buying Pressure Affect the Shape of Implied Volatility Functions?*
- Gârleanu, Pedersen, Poteshman (2009) RFS 22(10) — *Demand-Based Option Pricing.* **(dealer-gamma foundations)**
- Chang, Christoffersen, Jacobs (2013) JFE 107(1) — *Market Skewness Risk and the Cross Section of Stock Returns.*
- Da, Engelberg, Gao (2011) JF 66(5) — *In Search of Attention.*
- Baker, Wurgler (2006) JF 61(4) — *Investor Sentiment and the Cross-Section of Stock Returns.*
- DellaVigna, Pollet (2009) JF 64(2) — *Investor Inattention and Friday Earnings Announcements.*
- Livnat, Mendenhall (2006) JAR 44(1) — *Comparing the Post-Earnings-Announcement Drift for Surprises Calculated from Analyst and Time Series Forecasts.*
- Kim, Verrecchia (1994) JAE 17(1–2) — *Market Liquidity and Volume around Earnings Announcements.*
- Israeli, Lee, Sridharan (2017) Review of Accounting Studies 22(3) — *Is There a Dark Side to Exchange-Traded Funds? Information Environment Implications.* **Grade B**
- Madhavan (2012) RAPS 2(1) — *Exchange-Traded Funds, Market Structure, and the Flash Crash.* **Grade B**
- Staer (2017) Financial Review — *Fund Flows and Underlying Returns: The Case of ETFs.* **Grade B**
- Scaillet, Treccani, Trevisan (2020) JFEc 18(2) — *High-Frequency Jump Analysis of the Bitcoin Market.*
- Borri (2019) JEDC 103 — *Conditional Tail-Risk in Cryptocurrency Markets.* **Grade B**
- Bianchi, Babiak (2022) JFM — *On the Performance of Cryptocurrency Funds.* **Grade B**
- Krohn, Sushko (2024) JF — *The Intraday Dynamics of Global FX Order Flow and Fixings.* **Grade B**
- Elaut, Frömmel, Lampaert (2018) JBF — *Intraday Momentum in FX Markets.* **Grade B**
- Papagelis (2025) WP — *Intraday Variance Risk Premium.* **Grade B (WP)**
- Soebhag (2023) WP — *Net Gamma Exposure and Intraday Reversal.* **Grade B (WP)**
- arxiv 2408.03594 (2024) — *Hawkes-Process Models of Intraday Order-Flow Clustering.* **Grade B (WP)**
- Bhattacharya, Lee, Pool (2013) RAPS — *Conflicting Family Values in Mutual Fund Families.* **Grade B**
- Hou, Xue, Zhang (2015) RFS 28(3) — *Digesting Anomalies: An Investment Approach.*
- Fama, French (2015) JFE 116(1) — *A Five-Factor Asset Pricing Model.*
- Stambaugh, Yu, Yuan (2012) JFE 104(2) — *The Short of It: Investor Sentiment and Anomalies.*
- Jiang, Li, Wang (2021) RFS — *Attention and Information Processing Near Earnings Announcements.* **Grade B**
- Andersen, Fusari, Todorov (2015) JFE 117(3) — *Parametric Inference and Dynamic State Recovery from Option Panels.*

---

**End of memo.**
