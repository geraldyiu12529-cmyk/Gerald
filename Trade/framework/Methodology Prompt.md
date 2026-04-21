# Methodology Prompt — Gerald's Cross-Asset + Crypto Trading Framework

This is the master document. It synthesizes the two research cores (`Trad core.md` for cross-asset/traditional and `Coin core.md` for BTC/crypto) into one operational methodology. Every session must follow it.

---

## 0. Asset Universe (fixed unless explicitly expanded)

**Crypto:** BTC, ETH (+ named alt coins when provided)
**Equities:** INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, AVGO, BABA, MSFT
**ETFs / Indices:** QQQ, SPY, EWJ, EWY
**Commodities / Metals:** Brent, WTI, Gold, Silver, Copper, Palladium, Platinum

Do not expand without being asked.

---

## 1. Evidence Grading

Every variable cited in analysis must carry an evidence grade:

- **Grade A** — Strong, replicated across samples/regions, coherent economic mechanism, long history. Examples: time-series momentum, carry, credit spreads, policy path surprises, BTC order imbalance, BTC realized vol / jumps, BTC active addresses.
- **Grade B** — Moderate. Works in most samples, regime-dependent, or thinner academic coverage. Examples: news sentiment, options skew, futures basis, MVRV/SOPR, exchange flows, stablecoin issuance.
- **Grade C** — Weak. Small samples, proxy-sensitive, narrative-heavy. Examples: stock-to-flow, halving cycle as timing tool, simple volume rules, pure seasonality.

**Rule:** Do not pad analysis with Grade C or below variables unless explicitly asked.

---

## 2. The 8-Step Methodology Sequence

Every trade thesis must pass through these steps in order. Skipping steps is not permitted.

### Step 1 — Regime Identification (Macro + Crypto)
- Growth: expansion / contraction / ambiguous
- Inflation: disinflation / reflation / stable
- Policy: easing / tightening / on hold; path surprise bias
- Financial conditions: easing / tightening (FCI, HY OAS, MOVE, DXY)
- Risk-on / risk-off cross-asset state
- For crypto: BTC realized-vol regime, funding/basis crowding, ETF flow direction

Output: one-line regime label + three primary regime variables being watched.

### Step 1.5 — Overlay Regime Gate (added 2026-04-18, meta-integration)

Binary sleeve-on / sleeve-off switch applied *after* regime identification, *before* structural scoring. Non-additive to Sum.

- **C009 Faber TAA (Grade A)** — Faber (2007) *J. Wealth Mgmt.* Rule: if sleeve price is below its 10-month simple moving average at the previous month-end close, the sleeve is gated OFF for the following month.
  - SPY/QQQ below 10m-SMA → equity sleeve OFF (new longs blocked on equity-sleeve assets)
  - GSCI (commodity aggregate) below 10m-SMA → commodity sleeve OFF
  - BTC-USD below 10m-SMA → crypto sleeve OFF
  - EFA (optional, for EWJ/EWY reads) below 10m-SMA → international-equity sleeve OFF

**Gating semantics.** Sleeve-OFF does NOT zero the Sum — it multiplies the post-Sum *position size* by 0 for that sleeve. A Sum +3 signal on a gated-off sleeve is preserved in the SignalLedger as a promoted signal with `Taken=NO` and `Block_Reason=OverlayGateOff` (or equivalent near-miss classification).

**Read cadence.** Overlay state flips only at end-of-month close. The daily pipeline reads the most recent month-end close against its 10m-SMA — do not recompute intraday. This mirrors the Faber rebalance discipline and avoids same-day execution confusion at monthly rolls.

**Output:** sleeve status per asset class (ON / OFF) written into the market-brief scorecard and every trade-rec's pre-entry checklist.

Evidence: meta-analysis 2026-04-18 PL-NMA rank 2/54, θ=+2.26; multi-review DEPLOY. Six-month live-review date **2026-10-14** (shared with V029–V035 meta-integration cohort).

### Step 2 — Structural Anchor per Asset
Score each candidate asset on its slow variables:
- Equities: valuation spread, profitability/quality, revision breadth
- Bonds: term premium, forward-rate factor, real yields, breakevens
- Commodities: inventories, curve slope, convenience yield, real rates, **basis-momentum (4w and 12w change in front-curve slope; Boons-Prado 2019 JF, Grade A)**
- BTC/ETH: active addresses, hash rate (BTC), transaction activity, MVRV regime

Score: +1 supportive / 0 mixed / -1 hostile.

**Commodity S-score integration:** basis-momentum is a dynamic complement to static F1–F2 slope. Rule: if static slope and basis-momentum align (e.g., deep backwardation *and* steepening further), S can stay at +1; if they diverge (deep backwardation but flattening), cap S at 0 even when static slope alone would read +1. This catches curve-shape exhaustion that static slope misses.

### Step 3 — Tactical Confirmation
- Trend (1m / 3m / 12m; or BTC daily/weekly trend). **For single-stock equities (NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC), prefer residual momentum (12m return residualized against Fama-French 5-factor model; Blitz-Huij-Martens 2011 JEF, Asness-Moskowitz-Pedersen 2013 JF, Grade A) over raw TSMOM.** Raw TSMOM remains the T-input for indices/ETFs, commodities, and crypto.
- Revisions / surprise flow (equities) or funding/basis direction (crypto)
- Order flow / positioning (CFTC, ETF flows, BTC order imbalance)

Score: +1 / 0 / -1.

**Single-stock T-score integration:** residual momentum and raw TSMOM usually agree; when they conflict (stock is trending on market-beta/value loading, not idiosyncratic alpha), trust residual. Apply Daniel-Moskowitz (2016) volatility scaling — unscaled momentum crashes in correlation-1 regimes.

### Step 4 — Catalyst Map
Name the next 1–3 catalysts likely to reprice the asset (earnings, CPI, FOMC, OPEC, inventory release, ETF flows, on-chain unlock, policy announcement). State whether thesis depends on surprise vs. confirmation.

### Step 5 — Risk Overlay
- Realized vol / implied vol state
- Skew / risk reversals / MOVE / VIX
- Crowding: positioning, funding rate, open interest, ETF one-directional flow
- Liquidity: spreads, depth, cross-venue fragmentation
- **Intermediary capital capacity (NY Fed primary-dealer equity / total-capital ratio, z-score vs 3y rolling mean; Adrian-Etula-Muir 2014 JF 69(6) [primary anchor, re-confirmed per BNMA audit]; He-Kelly-Manela 2017 JFE [secondary], Grade A).** Weekly pull, ~1-week lag. Z < −1σ tightens the risk overlay by one notch across equities and commodities (downgrade R from +1 → 0, or 0 → −1); captures dealer balance-sheet constraint *before* HY OAS widens, so it's a leading — not confirmatory — R input. PL-NMA rank 4/54, θ=+1.71, P(top-5)=0.51; P(V027 > V004 HY OAS)=1.000 — V027 is the *leading* leg of the double-count gate.

Score: +1 favorable / 0 neutral / -1 crowded or crash-prone.

**Double-counting gate:** intermediary capital z-score correlates ~0.65–0.75 with HY OAS changes post-2008. If both flag stress simultaneously, count once (take the more negative of the two, not their sum). If intermediary z turns negative *before* HY OAS moves, that's the early-warning case — apply the notch. P(V027>V004)=1.000 in PL-NMA all-vs-all ranking: V027 is the dominant leg. When V027 fires, the V004 reading is confirmatory, not additive.

### Step 6 — Score Aggregation
Sum of Steps 2 + 3 + 4 + 5 (catalyst asymmetry scored +1/0/-1):

| Total | Action |
|-------|--------|
| +3 to +5 | Buy / Long |
| +1 to +2 | Hold / wait for confirmation |
| 0 to -2 | Sell / reduce |
| -3 to -5 | Short |

**Scorecard format requirement:** every brief's asset scorecard must include columns `S | T | C | R | Sum` where C is the catalyst score. Omitting C (as in the 2026-04-14 brief) understates/overstates the aggregate.

**Correlation gate:** before promoting a |sum|≥3 signal to an entry, check whether the thesis shares its primary regime variable with an existing position or with another simultaneous signal. Co-moving theses (e.g., Copper + Gold + Silver as one reflation/DXY-weak bet; BTC + ETH momentum firing ~80% together) must be sized to the combined sector/theme cap, not the per-position cap. See `Risk Rules.md §5`.

### Step 7 — Expression Choice
- **Outright long/short** when structural AND tactical signals align.
- **Relative value (long/short pair)** when valuation / carry / revisions rank assets clearly but outright regime is mixed.
- **No trade** when structural and tactical conflict, or thesis depends entirely on one event with poor asymmetry. "No trade" is always valid.

### Step 8 — Invalidation Criteria (explicit, written)
Specify the data points that would kill the thesis:
- Revision reversal
- Trend break on specific timeframe
- Spread widening past threshold
- Policy path repricing
- Inventory rebuild
- BTC funding flip / ETF flow reversal / hash drop
- Positioning flip

If no concrete invalidation exists → thesis is narrative, not research-backed → no trade.

---

## 3. Minimal Dashboard (check every session)

**Cross-asset:** VIX, MOVE, HY OAS, DXY, Gold, cross-asset correlation, FCI
**Equities:** Valuation spread, revision breadth, profitability basket, 1m/3m/12m trend, breadth
**Bonds:** 2s10s, forward-rate factor, ACM term premium, breakevens, real yields, credit spreads, rate-option skew
**Commodities:** Front-back curve, inventory change, China/global demand, real rates, trend
**Crypto (BTC/ETH):** Price trend, realized vol & jumps, order imbalance proxy, funding rate, futures basis, options IV/skew, ETF flows, stablecoin issuance, active addresses, hash rate, exchange netflows, MVRV/SOPR (regime context only)

---

## 4. Top-31 Variables to Monitor (ranked, from Trad core + audit + meta-integration)

*(V015 FX carry and V016 FX PPP removed 2026-04-21 — FX not in trading universe. Numbering resequenced.)*

1. 12-month time-series momentum (A)
2. Carry / roll yield (A)
3. Credit spreads / excess bond premium (A)
4. Financial conditions / RORO (A)
5. Policy-path surprise sensitivity (A)
6. Equity valuation spread (A)
7. Earnings revision breadth (A)
8. Gross profitability / quality (A)
9. Yield-curve forward-rate factor (A)
10. Term premium (A)
11. Inflation breakevens (A)
12. Real yields (A)
13. Commodity inventories (A)
14. Commodity front-back curve slope (A)
15. CFTC speculative positioning (B)
16. Dealer/customer order flow proxy (B public / A proprietary)
17. Options-implied skew / risk reversals (B)
18. Variance risk premium / IV-RV gap (B)
19. News-based text sentiment (B)
20. Cross-asset correlation / beta regime (A as filter)
21. Net supply / issuance / duration supply (A in rates)
22. Buyback / net payout signal (B)
23. Insider net buying (B)
26. **Residual momentum (equities, 12m FF5-residualized) — A** — Blitz-Huij-Martens (2011) JEF 18(3), 506–521; Asness-Moskowitz-Pedersen (2013) JF 68(3), 929–985. Single-stock T-input; see Step 3. Post-decay projected Sharpe 0.6–0.9. **BNMA verdict: DEPLOY_CONDITIONAL — operationally subsumed by V009 (p_beats_peers 0.009–0.053 across 4 runs).** PL-NMA rank 53/54, P(V009>V026)=1.000. Use as sleeve-only input: V026 scores the single-stock T leg but receives zero independent sizing allocation vs. V009. Six-month review 2026-10-14 may result in demotion to T-overlay only.
27. **Intermediary capital ratio (NY Fed primary-dealer equity/total, z-score) — A** — He-Kelly-Manela (2017) JFE 124(2), 264–279; Adrian-Etula-Muir (2014) JF 69(6), 2557–2596. Cross-asset R-overlay input; see Step 5. Post-decay projected Sharpe 0.4–0.7.
28. **Basis-momentum (commodities, 4w/12w change in front-curve slope) — A** — Boons-Prado (2019) JF 74(1), 239–279. Commodity S-input; see Step 2. Post-decay projected Sharpe 0.35–0.47 (BNMA 4-run consensus; P4 posterior 0.39–0.47). PL-NMA rank 10/54, θ=+1.30, P(top-5)=0.13. P(V028>V011)=0.887 — basis-momentum edges Brent slope; size V028 ≥ V011.
29. **V029 BAB — Betting-Against-Beta — A** (review 2026-10-14) — Frazzini, A., & Pedersen, L. (2014). *Betting Against Beta.* JFE 111(1), 1–25. Step 2 — single-stock + ETF sleeve. Long low-β / short high-β. Independent factor sleeve, capped at 1/3 of V009's risk budget. ETF proxy: USMV/SPLV spread (tactical); canonical AQR BAB / Ken French library for grading. BNMA verdict: DEPLOY_CONDITIONAL — 4-paper support, robust primary+S2. PL-NMA rank 6/54, θ=+1.60, P(top-5)=0.38.
30. **V030 DealerGamma — options dealer gamma positioning — B** (single-paper; second replication required before Grade A; review 2026-10-14) — Barbon, A., & Buraschi, A. (2021). *Gamma Fragility.* Working Paper. Step 5 — single-stock + index R-overlay. Short-gamma dealer regimes amplify intraday vol (widen R stop); long-gamma damps it (tighten). Source: SqueezeMetrics GEX (subscription-dependent) → SpotGamma → MISSING. Independent factor sleeve, capped at 1/3 of V009's risk budget. BNMA verdict: WATCH — 1 paper, pending second replication. PL-NMA rank 5/54 primary (rank 2 S2); θ=+1.68. Flag single-paper status in every trade rec that references it.
31. **V031 GP/A — Gross Profitability / Assets — A** (review 2026-10-14) — Novy-Marx, R. (2013). *The Other Side of Value: The Gross Profitability Premium.* JFE 108(1), 1–28. Step 2 — single-stock. Canonical Fama-French 5F component. JKP-tangency implementation intended when HMLDevil/QMJ later promoted. Monthly rebalance of ranked basket from quarterly financials. Meta 2026-04-18 PL-NMA rank 15, θ=+0.63.
32. **V032 CEI — Composite Equity Issuance — A** (review 2026-10-14) — Daniel, K., & Titman, S. (2006). *Market Reactions to Tangible and Intangible Information.* JF 61(4), 1605–1643. Step 2 — single-stock. Negative sign: high net issuance is a structural headwind signal. Self-compute from CRSP + Compustat (quarterly, with reporting lag). BNMA verdict: DEPLOY — 2-paper support, robust primary+S2. PL-NMA rank 7/54, θ=+1.33.
33. **V033/V034/V035 C009 Faber TAA — 10-month SMA sleeve gate — A** (review 2026-10-14) — Faber, M. (2007). *A Quantitative Approach to Tactical Asset Allocation.* J. Wealth Mgmt. **Step 1.5 Overlay Gate only — non-additive to Sum.** Three asset instantiations: V033 SPY, V034 GSCI, V035 BTC. Monthly Yahoo closes → Stooq → MISSING. Drawdown circuit-breaker, not alpha sizer. Meta 2026-04-18 PL-NMA rank 2/54 primary (rank 18 S2 — artefact from small Overlay peer-set in S2 spec; does not change DEPLOY verdict), θ=+2.26; multi-review DEPLOY.

---

### Scoring rule additions — 2026-04-18 meta-integration (binding)

These four rules resolve double-counting and sleeve interaction for the meta-integrated variable set. They sit above the Step 6 aggregate sum.

1. **V009 (TSMOM) and V026 (Residual momentum) on the same single-stock ticker: score V026 only — do not sum.** This makes explicit the existing mandate restriction (see Step 3). Meta 2026-04-18 flagged V026 as peer-dominated by V009 in all 4 BNMA runs; co-scoring inflates T-signal on factor-driven names. Six-month review will decide whether to keep V026 at all.
2. **V027 (Intermediary capital z-score) and V004 (HY OAS) simultaneously flagging stress: count once — take the more-negative of the two, not their sum.** Extends the existing Step 5 double-counting gate. If V027 turns negative *before* V004 widens (the leading-indicator case), the notch applies on V027 alone; when V004 catches up later, do not double-adjust.
3. **Step 1.5 Overlay Gate sleeve-off: post-Sum position size × 0 for that sleeve regardless of Sum.** The gate is non-additive to Sum but binding on execution. A Sum +3 signal on a gated-off sleeve is logged as a promoted signal with `Taken=NO` and `Block_Reason=OverlayGateOff`.
4. **V029 BAB and V030 DealerGamma are independent factor sleeves, each capped at 1/3 of V009's risk budget.** Neither aggregates into the spine (V009/V027/V028) sizing. Correlation gate still applies: a BAB sleeve and a spine V009 long on the same ticker must be sized to the combined sector cap, not double-sized.

---

### Reconciliation note — MVRV and funding rate

`Coin core.md:9, 107-109` ranks MVRV Z-Score and funding rate as top on-chain/derivatives predictors (B+). This Prompt deliberately demotes both to "regime context / crowding filter only" (not entry triggers) because:
1. Post-ETF institutional sample is short; older MVRV/funding alpha may be sample-specific. See `Coin core.md:96` on market-maturation alpha decay (carry Sharpe 6.45 → negative in 5 years).
2. McLean & Pontiff 2015 — documented anomalies decay 26% OOS and 58% post-publication (`Trad core.md:94, 255`).
3. Funding rate has "no correlation with directional strategies" in its own study (`Coin core.md:41`) — consistent with use as a filter, not a direction predictor.

Use MVRV and funding as crowding/regime signals and size overlays, never as the sole trigger for direction.

### Reconciliation note — 2026-04-14 methodology audit additions

Three Grade A variables added to the scoring framework after peer-reviewed audit (see `auto-memory/project_methodology_audit_2026-04-14.md` and this Prompt's Top-25 entries 26–28):

1. **Residual momentum** refines equity T-scores only; raw TSMOM remains authoritative for indices/commodities/crypto. When residual and raw conflict on a single stock, trust residual.
2. **Intermediary capital ratio** is a leading cross-asset R-overlay. Do not double-count with HY OAS — take the more negative signal, not the sum.
3. **Basis-momentum** supplements (does not replace) static F1–F2 slope in commodity S-scores. When they diverge, cap S at 0.

All three carry McLean-Pontiff decay risk (30–50% Sharpe haircut vs. published). Fail-loud if the data is `MISSING` — same rule as existing Grade A variables per `Data Sources.md`. Six-month live-monitoring review: if no decision-moving contribution by 2026-10-14, demote to Grade B and drop from the binding scorecard inputs.

### Reconciliation note — 2026-04-18 meta-analysis integration additions

Five new variables entered the framework after the 2026-04-18 meta-analysis (see `meta-analysis-integration-plan-2026-04-18.md`). V029 BAB, V031 GP/A, V032 CEI, and V033–V035 C009 Faber TAA enter at Grade A. V030 DealerGamma enters at Grade B pending a second independent replication. All five share a 2026-10-14 six-month review date with the 2026-04-14 audit cohort.

1. **V029 BAB** is a single-stock + ETF Structural-sleeve input. Treat as an **independent factor sleeve**, capped at 1/3 of V009's risk budget. Do NOT aggregate into the V009/V027/V028 spine sizing. ETF-proxy implementation (USMV/SPLV spread) is adequate for tactical use; canonical BAB is required for grading reviews.
2. **V030 DealerGamma** is a Risk-Overlay modifier. Short-gamma regime → widen the R stop by one notch; long-gamma → tighten by one notch. Flag single-paper status at the 2026-07-01 quarterly and in every trade rec referencing it.
3. **V031 GP/A** and **V032 CEI** are single-stock Structural inputs. Both are quarterly-frequency factors with real-statement reporting lag; replicate the equal-weight quarterly-rebalance discipline rather than daily rescore.
4. **V033–V035 C009 Faber TAA** is Step 1.5 Overlay Gate only — **non-additive to Sum**. Sleeve flips read from the previous month-end close against its 10m-SMA; do not recompute intraday. See §Step 1.5 for full gating semantics.
5. **Bucket interaction with V026**: BAB, GP/A, CEI run on the single-stock equity sleeve alongside V026 (Residual momentum). When V026 and a meta-factor fire on the same ticker, score each separately — they isolate different drivers (V026 = residual alpha; BAB = low-β premium; GP/A = profitability; CEI = issuance headwind). Correlation gate applies at position-sizing time.
6. **V030 DealerGamma double-count gate**: do not double-count with V001 VIX when both flag stress. Take the more-negative read.

All five meta additions obey the fail-loud rule on MISSING pulls. Post-decay projections per meta PL-NMA: V029 Sharpe 0.4–0.8, V030 0.4–0.7, V031 0.3–0.5, V032 0.4–0.6, V033–V035 as gate (no alpha, drawdown reduction instead).

### Reconciliation note — 2026-04-18 BNMA grade downgrades (binding)

The BNMA 4-paper cross-run audit (2026-04-18) found evidence inconsistency or regime-sensitivity in five previously Grade A macro variables. All five are **downgraded A→B** effective immediately. They remain in the scorecard but carry the lower grade until a future audit reverses the call.

| Variable | Code | Previous | New | BNMA finding |
|---|---|---|---|---|
| VIX | V001 | A | **B** | Regime-sensitive; predictive only in specific vol-regime clusters |
| HY OAS / credit spreads | V004 | A | **B** | Correlates 0.65–0.75 with V027 post-2008; loses independent signal in high-V027-correlation windows |
| 2s10s yield curve | V006 | A | **B** | Lead-lag structure unstable across rate cycles; inversion signal inconsistent post-QE |
| Real yields | V007 | A | **B** | Cross-asset correlation with equity E/P varies by inflation regime; not unconditionally Grade A |
| ACM term premium | V008 | A | **B** | Methodology-sensitive (ACM vs. Kim-Wright diverge post-2020); 1-model dependency |

**How to apply:** In scorecards, mark these variables as **(B)** not **(A)**. When one of these fires against a Grade A variable pointing the other way, treat the Grade B reading as confirmatory context, not an independent signal leg. Do not double-count V004 with V027 (existing gate still applies).

---

### Appendix — Meta-analysis group ↔ Gerald bucket crosswalk (added 2026-04-18)

The SignalLedger, trade-rec scorecards, and every downstream reviewer tool use Gerald's S/T/C/R bucket codes. The 2026-04-18 meta-analysis uses a different group taxonomy. **Do NOT rename** Gerald's bucket codes. When citing meta-analysis ranks or posteriors, use this crosswalk:

| Meta-analysis group | Gerald bucket | Notes |
|---|---|---|
| Meta **S** (Sentiment / slow structural) | Gerald **S (Structural)** | Step 2 input |
| Meta **T** (Tactical / momentum) | Gerald **T (Tactical)** | Step 3 input |
| Meta **R** (Regime / macro conditions) | Gerald **R (Risk Overlay)** | Step 5 input |
| Meta **Overlay** (gates) | Gerald **Overlay Gate** | **New Step 1.5, non-additive** |
| Meta **Stocks** (cross-sectional equity factors) | Gerald **S (Structural), single-stock sleeve** | Step 2 input on single-stock universe |

When a meta-analysis posterior is cited in analysis or in the deployment memo, disclose which group the variable sits in so bucket attribution is not ambiguous at signal-review time.

## 5. BTC-Specific Long/Short Signal Hierarchy (from Coin core)

**Strongest longs (A/B):** positive time-series momentum, buy-side order imbalance, rising active addresses/hash rate, supportive ETF/stablecoin events, early-stage attention rising from low base.

**Strongest shorts (A/B):** trend breakdown, sell-side imbalance + widening spreads, rising realized vol + jumps, negative events (hacks, enforcement, bans), exchange inflows + stressed leverage, overheated positive funding (crowding signal).

**Mixed / caution (B/C):** funding rate direction alone, open interest alone, futures basis direction alone, search attention at extremes, MVRV/SOPR as trigger (use only as regime context), stock-to-flow / halving narratives.

---

## 6. Directional Expression Rules

- **Buy/sell outright** is for when structural + tactical + regime align.
- **Long/short relative value** is usually stronger than outright for valuation, carry, term structure, revisions — these rank better than they forecast.
- **Trend and event surprise** signals are more useful for outright direction.
- In commodities and crypto, combine directional signal with volatility filter — carry and momentum are crash-prone without a vol overlay.

---

## 7. What NOT to Do

- Do not pad briefings with Grade C variables unasked.
- Do not use stock-to-flow or halving-cycle narratives as timing tools.
- Do not present ungrounded assertions as evidence.
- Do not expand the trading universe without permission.
- Do not skip session startup reads.
- Do not force a trade when evidence is mixed. "No trade" is an output.
- Do not reproduce long passages from the research cores — cite, don't quote at length.

---

## 8. Output Discipline

Every sentence in a briefing must either (a) inform a decision or (b) manage a risk. No padding, no narrative prose, no recaps of what the user already knows. Cite evidence grades (A/B/C) when referencing signals.

---

## Source Documents

- `Trad core.md` — cross-asset factor review, decision framework, ranked variables, top-25 monitor list, one-page framework.
- `Coin core.md` — BTC predictor families, long/short signal hierarchy, master variable table, research gaps.
- `Risk Rules.md` — binding sizing, heat, stop, and correlation-gate policy. Reference at every entry.
- `Data Sources.md` — explicit Grade A/B variable → source mapping with fail-loud rule.
- `bnma/meta-analysis/BNMA-meta-analysis-2026-04-18.md` — highest-evidence synthesis: 4-paper cross-run MCMC analysis; DEPLOY/WATCH/EXCLUDE verdicts per variable; V001/V004/V006/V007/V008 A→B downgrades; primary evidence basis for Top-33 entries V026–V035.
- `bnma/meta-analysis/PL-NMA-meta-analysis-2026-04-18.md` — Plackett-Luce NMA all-vs-all ranking of 54 variables across 12 papers (Bradley-Terry model); provides θ (log-odds), P(top-k), and pairwise dominance probabilities cited in Top-33 entries.

All live in `/Trade/framework/` (or `/Trade/bnma/meta-analysis/` for the BNMA files) and should be consulted directly when a variable's definition, evidence, or direction is uncertain.
