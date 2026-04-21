# Literature Review Prompt — Intraday-Volume Uplift Ranking

**Output:** one scoped literature-review memo ranking every variable in Gerald's current methodology by the expected marginal benefit of moving its data input from end-of-day to **5 intraday updates per day** (roughly every ~80 minutes across the US cash session, plus a pre-open and an after-close read).

**Cadence assumption (fixed — do not debate):** 5 updates/day. Do not propose 1/min, 1/hour, or continuous streaming. All uplift estimates must be conditional on this exact refresh rate.

**Asset coverage — ALL assets by default.** Every variable must be scored across the **full asset universe** it applies to (equities single-stock, equity indices/ETFs, commodities, FX, crypto — per Methodology Prompt §0). Do not collapse to a single asset class. If the evidence, mechanism, or uplift is **materially different** across asset classes for the same variable, produce **one row per asset-class instance** (e.g., TSMOM-equity-index vs TSMOM-single-stock vs TSMOM-commodity vs TSMOM-crypto, scored separately). If the uplift is materially the same across all applicable assets, one row is fine — but the row must explicitly say "applies uniformly across [list]".

**If a variable's uplift claim is single-asset-only — SOUND OUT.** Any time the reviewer's IUS score, citation, or mechanism is grounded in evidence from *one* asset class only (e.g., a paper that only tested SPY, only tested BTC, only tested copper), this must be flagged with `⚠ SINGLE-ASSET EVIDENCE — [asset]` in the mechanism column, and the IUS capped at 2 unless the mechanism is explicitly argued to generalize. Do not silently extrapolate from one-asset evidence to a cross-asset uplift claim.

**Emphasis — indices and single stocks get the deepest treatment.** Gerald's methodology leans on single-stock and equity-index signals (12 single-stock tickers + QQQ/SPY/EWJ/EWY + single-stock sleeve factors V026/V029/V031/V032). The review must reflect this weighting:
- The per-variable table must break out **single-stock** and **equity-index/ETF** rows separately for every variable that applies to both (momentum, realized vol, skew, VRP, order flow, ETF flows, revisions, options IV, dealer gamma, etc.).
- The Literature Engagement section (§6) must prioritize the intraday-momentum, RV-microstructure, VPIN, options-IV, and dealer-gamma strands — these map directly onto the index+single-stock book.
- Commodity, FX, and crypto variables still get covered but with less depth and no separate single-ticker breakout unless the evidence demands it.
- Ranking A and Ranking B (see §5) must each produce a **dedicated Top-5 for the index+single-stock sleeve** in addition to the all-asset Top-3. Gerald acts primarily from the index+single-stock Top-5.

**Not in scope:** adding new variables, changing scoring weights, changing sizing, changing asset universe.

---

## Instructions to the reviewer

### Step 0 — Search online (mandatory — do not skip)

This review **must** be grounded in a live literature search, not in the reviewer's pre-existing memory. Do not answer from training knowledge alone. Before scoring any variable, execute the following using the WebSearch tool (and WebFetch where a specific paper PDF or abstract needs to be retrieved):

**Baseline searches — run all of these, record the queries used in an appendix:**

1. `"intraday momentum" SPY S&P OR index return predictability site:ssrn.com` — and same for 2023/2024/2025/2026 date filters
2. `"realized volatility" "sampling frequency" microstructure noise equity 5-minute hourly`
3. `VPIN "order flow toxicity" intraday prediction equity`
4. `"implied volatility" intraday skew risk-reversal prediction equity single-stock`
5. `"dealer gamma" OR GEX intraday hedging equity index SPY`
6. `"ETF flow" intraday creation redemption prediction equity`
7. `"earnings announcement" intraday drift PEAD high-frequency single-stock`
8. `"residual momentum" Fama-French intraday OR high-frequency single-stock`
9. `"betting against beta" OR BAB intraday frequency equity`
10. `"realized volatility" Bitcoin OR crypto intraday sampling frequency`
11. `Bitcoin "order imbalance" intraday return prediction`
12. `"funding rate" perpetual futures intraday crypto prediction`
13. `commodity futures intraday "realized volatility" OR "basis" prediction`
14. `FX "intraday momentum" OR "high-frequency" carry prediction`
15. `"intermediary capital" OR "dealer balance sheet" intraday sampling`
16. `"news sentiment" OR "text sentiment" intraday equity return high-frequency`
17. `"options volume" OR "put-call" intraday prediction equity single-stock`
18. `"limit order book" imbalance intraday return equity 2023 2024 2025`

For each of the 8 literature strands enumerated in §6, run at least **two additional targeted searches** to surface post-2023 evidence (the existing framework cites mostly 2014–2021 papers; the goal is to catch what's been published since).

**Search hygiene:**
- Prefer sources: `ssrn.com`, `nber.org`, Journal of Finance / JFE / RFS / JFQA / JoE, Review of Asset Pricing Studies, Journal of Empirical Finance, arXiv q-fin.
- Prefer post-2023 evidence when available; fall back to older canonical papers when no recent work exists.
- If a search returns no useful hits, record the null result in the appendix rather than pretending the query was never run.
- If a cited paper cannot be retrieved (paywall, dead link), mark the citation with `[unverified — abstract only]` and do not upgrade IUS beyond 2 on its strength.

**Web-search appendix requirement:** the memo must end with an appendix listing every query run, the number of hits, and the papers that materially influenced a scoring decision. Without this appendix the review is not complete.

**Fail-loud on evidence scarcity:** if the web search genuinely turns up no relevant post-2023 work for a given variable × asset-class cell, write `INSUFFICIENT ONLINE EVIDENCE — [queries attempted]` in the citation column and score IUS = 0 (not 1, not "TBD").

### Step 1 — Ground the universe

Read the full variable list from `framework/Methodology Prompt.md` §4 (the Top-33) plus the Step 1.5 overlay gate entries. Do not invent variables. The output must cover every one of these, grouped by score bucket:

- **S — Structural** (Step 2 inputs, incl. single-stock sleeve V026/V029/V031/V032 and commodity V028 basis-momentum)
- **T — Tactical** (Step 3 inputs: TSMOM, residual momentum V026, revisions, funding/basis direction, order flow)
- **C — Catalyst** (Step 4 — by construction event-driven; treat this bucket specially, see §4 below)
- **R — Risk Overlay** (Step 5: realized/implied vol, skew/MOVE/VIX, crowding/funding/OI/ETF flow, liquidity, V027 intermediary capital, V030 DealerGamma)
- **Overlay Gate** (Step 1.5: V033/V034/V035 C009 Faber) — monthly by construction; see §4

Also explicitly cover the BTC/ETH-specific Coin-core variables referenced in the Methodology Prompt §5 dashboard: order imbalance, realized vol + jumps, funding rate, futures basis, options IV/skew, ETF flows, stablecoin issuance, active addresses, hash rate, exchange netflows, MVRV/SOPR.

### Step 2 — The scoring rubric (uplift from 5×/day)

For each variable, assign an **Intraday Uplift Score (IUS)** on a 0–3 integer scale, justified by citation:

| IUS | Meaning |
|---|---|
| 3 | Strong academic evidence that intraday refresh (≤ hourly to sub-daily) materially improves signal-to-noise, timing, or information-ratio vs EOD, AND the variable's generating process has genuine intraday information content at the 5×/day cadence (i.e., not faster than the underlying data updates). |
| 2 | Moderate evidence of uplift — usually from related/adjacent literature (e.g., intraday momentum, VPIN, realized-vol microstructure) — and the data mechanically refreshes faster than once a day. |
| 1 | Weak / mixed evidence; variable refreshes intraday but published uplift is small, regime-dependent, or data-snooping-sensitive. |
| 0 | No uplift: the underlying economic signal is structurally slow (quarterly/weekly/monthly reporting lag) OR the academic evidence explicitly finds that EOD sampling dominates. Upsampling only adds noise or duplicates the EOD read. |

**Grade-A-only rule:** uplift claims must cite peer-reviewed or top-tier working-paper evidence. If the only support is anecdotal or narrative, score IUS = 1 maximum and mark the citation as Grade B/C per Gerald's evidence-grade discipline.

### Step 3 — Mandatory columns per variable (one row per variable × asset-class instance)

Produce one row per **variable × asset-class pair** in a table with these exact columns:

| # | Variable | Asset class (Single-stock / Equity-index-ETF / Commodity / FX / Crypto / All) | Bucket (S/T/C/R/Overlay) | Native data cadence | Does 5×/day actually change the observed value? (Y/N + why) | IUS 0–3 | Single-asset-evidence flag (⚠ or blank) | Primary citation(s) | One-line mechanism for the uplift | Implementation cost flag (Low / Med / High) | Risk of over-trading / whipsaw at 5×/day (Low/Med/High) |
|---|---|---|---|---|---|---|---|---|---|---|---|

**Row-duplication rule.** For every variable that applies to more than one asset class, produce separate rows when the IUS, mechanism, citations, cost, or whipsaw risk would differ. Use "All" in the asset-class column ONLY when the uplift is genuinely uniform across every asset it applies to — and state that explicitly in the mechanism column. Defaulting to "All" to save rows is not acceptable; the single-stock and equity-index rows are the ones Gerald cares about most and must never be collapsed into a commodity/FX/crypto aggregate.

The **"does 5×/day actually change the observed value"** column is the gatekeeper. If the answer is "N — the source only updates weekly (e.g., NY Fed PD ratio, CFTC)" or "N — monthly (Faber 10m-SMA, GP/A, CEI)", then IUS is automatically 0 regardless of the theoretical case. This is the filter that prevents fake precision.

The **single-asset-evidence flag** (⚠) must be set whenever the citation supporting the IUS is drawn from a single asset class (e.g., Gao-Han-Li-Zhou intraday momentum tested on SPY only). When flagged, IUS is capped at 2 unless the mechanism argument for generalization is explicit. See the "sound out" rule in the preamble.

### Step 4 — Special-case handling

Three buckets need explicit carve-outs:

1. **C — Catalyst (Step 4).** Catalysts are event-timestamped (earnings beat, FOMC dot-plot, CPI surprise). 5×/day does matter but only on event days. Score IUS 0–3 **conditional on event-day handling** and note in the mechanism column: "Uplift concentrated on T-0/T+0 of scheduled release; zero on other days."

2. **Overlay Gate (Step 1.5, V033–V035 Faber TAA).** The rule is explicitly month-end close vs 10m-SMA. Upsampling is forbidden by Faber's discipline. IUS = 0. Flag in the memo that 5×/day would violate the rule, not improve it.

3. **Quarterly fundamentals (V031 GP/A, V032 CEI).** Report lag is the binding constraint, not sampling frequency. IUS = 0. State explicitly.

### Step 5 — The ranking cuts required

After the per-variable table, produce **four sorted shortlists** — two all-asset views and two index+single-stock views:

**Ranking A (all assets) — Raw uplift, sort by IUS desc.** Answers Gerald's literal question across the full universe.

**Ranking B (all assets) — Uplift net of cost and whipsaw.** Sort by `IUS − 0.5·ImplementationCost − 0.5·WhipsawRisk`, using Low=0, Med=1, High=2. Corrects for the reality that some high-IUS variables (dealer gamma GEX subscription, high-frequency order-book data) are expensive or noisy at 5×/day cadence.

**Ranking A-ES (index + single-stock ONLY) — Raw uplift, filtered to rows where Asset class ∈ {Single-stock, Equity-index-ETF}, sort by IUS desc.** Top 5.

**Ranking B-ES (index + single-stock ONLY) — Uplift net of cost and whipsaw, same filter as A-ES, sort by the net score.** Top 5.

Gerald should act primarily from **Ranking B-ES** (the equity sleeve is where his book is concentrated), using Ranking B (all assets) as the cross-asset check. Ranking A and A-ES are shown for transparency, not action. State this hierarchy explicitly in the memo.

### Step 6 — Literature priors the reviewer must engage with

The review must explicitly address — cite, agree, or disagree — with the following strands of evidence. If a strand is judged irrelevant to a variable, say so; do not skip silently.

- **Intraday momentum (Gao-Han-Li-Zhou 2018, RFS; Zhang-Wang 2022 JBF follow-ups)** — first-half-hour and last-half-hour intraday return predictability. Relevant to T (TSMOM, residual momentum) on SPY/QQQ and single stocks.
- **Realized volatility microstructure (Andersen-Bollerslev-Diebold-Labys 2001; Bollerslev-Patton-Quaedvlieg 2016 JoE)** — realized-vol measures collapse noise with higher sampling, up to microstructure-noise limits. Relevant to R (realized vol), BTC realized vol + jumps.
- **VPIN / order-flow toxicity (Easley-López de Prado-O'Hara 2012 RFS)** — intraday flow imbalance as a leading indicator of volatility events. Relevant to R (liquidity, crowding) and BTC order imbalance.
- **Options-implied information (Cremers-Weinbaum 2010 JFQA; An-Ang-Bali-Cakici 2014 JF)** — intraday IV/skew updates carry return-predictive info on 1-day horizons. Relevant to R (skew, MOVE, VRP).
- **ETF flow intraday signal (Ben-David-Franzoni-Moussawi 2018 JF; crypto-ETF flow literature 2024–2025)** — daily-reported but intraday-inferrable via creation/redemption proxies. Relevant to crypto ETF flows and equity ETF positioning.
- **On-chain data frequency (Makarov-Schoar, Liu-Tsyvinski; Cong-Li-Wang crypto asset pricing series)** — which on-chain metrics (active addresses, exchange netflows, stablecoin issuance, MVRV) have genuine intraday information vs block-time aggregation noise.
- **Dealer gamma / GEX intraday (Barbon-Buraschi 2021; Ni-Pearson-Poteshman follow-ups)** — dealer-gamma estimates refresh intraday via options-volume; directly relevant to V030 at 5×/day.
- **CFTC / positioning (weekly Tuesday release)** — explicitly cite that no intraday uplift is possible; the variable is report-bound.

### Step 7 — Decision-grade deliverables

End the memo with a short, binding recommendation section:

1. **Top 5 variables from Ranking B-ES (index + single-stock)** — the primary action list, since that is where Gerald's book sits. For each, one sentence on the expected P&L channel (better timing of entries on |Sum|≥3 signals, tighter stop discipline, faster R-overlay updates, etc.).
2. **Top 3 variables from Ranking B (all assets, outside the equity sleeve)** — the cross-asset cross-check: any commodity/FX/crypto variable where the intraday uplift is large enough to matter despite the equity emphasis.
3. **Top 3 variables to explicitly NOT upsample** — where 5×/day would degrade, not improve, the signal (overlay gate, quarterly fundamentals, CFTC, etc.). Protects against the "more data = better" fallacy.
4. **Data-feed implications** — which upstream sources (polygon.io trades+quotes, CME settlement intraday, SqueezeMetrics GEX, Coin Metrics intraday) are implicated by the recommendations in 1 and 2. Keep to one paragraph.
5. **Six-month review gate** — propose a single metric to evaluate whether the upsample actually improved SignalLedger hit rate on the affected variables. Match the existing 2026-10-14 audit-addition review discipline.

### Step 8 — Discipline constraints

- Cite evidence grades (A/B/C) on every claim per `.claude/rules/evidence-grades.md`.
- Fail-loud on any variable where the literature is genuinely silent — write `INSUFFICIENT EVIDENCE — [sources searched]` and score IUS = 0, not 1.
- Do NOT recommend adding new variables; this is scoped to uplift on existing variables only.
- Do NOT propose changing the 8-step sequence or the Step 6 aggregation rule.
- Every sentence in the memo must either rank a variable, justify a ranking, or inform the recommendation. No padding.

---

## Expected output format

Write the output to `2026-MM-DD/literature-review-YYYY-MM-DD-intraday-volume.md` following the standard lit-review filename convention. Sections, in order:

1. Scope statement (2–3 lines; restate the 5×/day assumption).
2. Gap framing — which SignalLedger weaknesses an intraday upgrade would plausibly address (read recent `signal-review-*.md` files for this).
3. Per-variable table (§3 above) covering all Top-33 + overlay + BTC/ETH Coin-core variables.
4. Ranking A (raw IUS) and Ranking B (uplift net of cost/whipsaw).
5. Literature engagement section covering each of the eight strands in §6.
6. Decision-grade recommendation (§7).
7. Appendix — citation list with DOI or SSRN ID for every paper referenced.
