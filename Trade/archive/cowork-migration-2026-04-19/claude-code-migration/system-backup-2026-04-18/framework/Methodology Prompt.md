# Methodology Prompt — Gerald's Cross-Asset + Crypto Trading Framework

This is the master document. It synthesizes the two research cores (`Trad core.md` for cross-asset/traditional and `Coin core.md` for BTC/crypto) into one operational methodology. Every session must follow it.

---

## 0. Asset Universe (fixed unless explicitly expanded)

**Crypto:** BTC, ETH (+ named alt coins when provided)
**Equities:** INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC
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

### Step 2 — Structural Anchor per Asset
Score each candidate asset on its slow variables:
- Equities: valuation spread, profitability/quality, revision breadth
- Bonds: term premium, forward-rate factor, real yields, breakevens
- Commodities: inventories, curve slope, convenience yield, real rates, **basis-momentum (4w and 12w change in front-curve slope; Boons-Prado 2019 JF, Grade A)**
- FX: carry, REER/PPP gap
- BTC/ETH: active addresses, hash rate (BTC), transaction activity, MVRV regime

Score: +1 supportive / 0 mixed / -1 hostile.

**Commodity S-score integration:** basis-momentum is a dynamic complement to static F1–F2 slope. Rule: if static slope and basis-momentum align (e.g., deep backwardation *and* steepening further), S can stay at +1; if they diverge (deep backwardation but flattening), cap S at 0 even when static slope alone would read +1. This catches curve-shape exhaustion that static slope misses.

### Step 3 — Tactical Confirmation
- Trend (1m / 3m / 12m; or BTC daily/weekly trend). **For single-stock equities (NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC), prefer residual momentum (12m return residualized against Fama-French 5-factor model; Blitz-Huij-Martens 2011 JEF, Asness-Moskowitz-Pedersen 2013 JF, Grade A) over raw TSMOM.** Raw TSMOM remains the T-input for indices/ETFs, commodities, FX, and crypto.
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
- **Intermediary capital capacity (NY Fed primary-dealer equity / total-capital ratio, z-score vs 3y rolling mean; He-Kelly-Manela 2017 JFE, Grade A).** Weekly pull, ~1-week lag. Z < −1σ tightens the risk overlay by one notch across equities, commodities, and FX longs (downgrade R from +1 → 0, or 0 → −1); captures dealer balance-sheet constraint *before* HY OAS widens, so it's a leading — not confirmatory — R input.

Score: +1 favorable / 0 neutral / -1 crowded or crash-prone.

**Double-counting gate:** intermediary capital z-score correlates ~0.65–0.75 with HY OAS changes post-2008. If both flag stress simultaneously, count once (take the more negative of the two, not their sum). If intermediary z turns negative *before* HY OAS moves, that's the early-warning case — apply the notch.

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
**FX:** Carry, REER/PPP gap, trend, CFTC positioning, risk reversals
**Crypto (BTC/ETH):** Price trend, realized vol & jumps, order imbalance proxy, funding rate, futures basis, options IV/skew, ETF flows, stablecoin issuance, active addresses, hash rate, exchange netflows, MVRV/SOPR (regime context only)

---

## 4. Top-25 Variables to Monitor (ranked, from Trad core)

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
15. FX interest-rate differential (A)
16. FX real valuation / PPP gap (B at short horizons, A at long)
17. CFTC speculative positioning (B)
18. Dealer/customer order flow proxy (B public / A proprietary)
19. Options-implied skew / risk reversals (B)
20. Variance risk premium / IV-RV gap (B)
21. News-based text sentiment (B)
22. Cross-asset correlation / beta regime (A as filter)
23. Net supply / issuance / duration supply (A in rates)
24. Buyback / net payout signal (B)
25. Insider net buying (B)
26. **Residual momentum (equities, 12m FF5-residualized) — A** — Blitz-Huij-Martens (2011) JEF 18(3), 506–521; Asness-Moskowitz-Pedersen (2013) JF 68(3), 929–985. Single-stock T-input; see Step 3. Post-decay projected Sharpe 0.6–0.9.
27. **Intermediary capital ratio (NY Fed primary-dealer equity/total, z-score) — A** — He-Kelly-Manela (2017) JFE 124(2), 264–279; Adrian-Etula-Muir (2014) JF 69(6), 2557–2596. Cross-asset R-overlay input; see Step 5. Post-decay projected Sharpe 0.4–0.7.
28. **Basis-momentum (commodities, 4w/12w change in front-curve slope) — A** — Boons-Prado (2019) JF 74(1), 239–279. Commodity S-input; see Step 2. Post-decay projected Sharpe 0.6–1.0.

---

### Reconciliation note — MVRV and funding rate

`Coin core.md:9, 107-109` ranks MVRV Z-Score and funding rate as top on-chain/derivatives predictors (B+). This Prompt deliberately demotes both to "regime context / crowding filter only" (not entry triggers) because:
1. Post-ETF institutional sample is short; older MVRV/funding alpha may be sample-specific. See `Coin core.md:96` on market-maturation alpha decay (carry Sharpe 6.45 → negative in 5 years).
2. McLean & Pontiff 2015 — documented anomalies decay 26% OOS and 58% post-publication (`Trad core.md:94, 255`).
3. Funding rate has "no correlation with directional strategies" in its own study (`Coin core.md:41`) — consistent with use as a filter, not a direction predictor.

Use MVRV and funding as crowding/regime signals and size overlays, never as the sole trigger for direction.

### Reconciliation note — 2026-04-14 methodology audit additions

Three Grade A variables added to the scoring framework after peer-reviewed audit (see `auto-memory/project_methodology_audit_2026-04-14.md` and this Prompt's Top-25 entries 26–28):

1. **Residual momentum** refines equity T-scores only; raw TSMOM remains authoritative for indices/commodities/FX/crypto. When residual and raw conflict on a single stock, trust residual.
2. **Intermediary capital ratio** is a leading cross-asset R-overlay. Do not double-count with HY OAS — take the more negative signal, not the sum.
3. **Basis-momentum** supplements (does not replace) static F1–F2 slope in commodity S-scores. When they diverge, cap S at 0.

All three carry McLean-Pontiff decay risk (30–50% Sharpe haircut vs. published). Fail-loud if the data is `MISSING` — same rule as existing Grade A variables per `Data Sources.md`. Six-month live-monitoring review: if no decision-moving contribution by 2026-10-14, demote to Grade B and drop from the binding scorecard inputs.

## 5. BTC-Specific Long/Short Signal Hierarchy (from Coin core)

**Strongest longs (A/B):** positive time-series momentum, buy-side order imbalance, rising active addresses/hash rate, supportive ETF/stablecoin events, early-stage attention rising from low base.

**Strongest shorts (A/B):** trend breakdown, sell-side imbalance + widening spreads, rising realized vol + jumps, negative events (hacks, enforcement, bans), exchange inflows + stressed leverage, overheated positive funding (crowding signal).

**Mixed / caution (B/C):** funding rate direction alone, open interest alone, futures basis direction alone, search attention at extremes, MVRV/SOPR as trigger (use only as regime context), stock-to-flow / halving narratives.

---

## 6. Directional Expression Rules

- **Buy/sell outright** is for when structural + tactical + regime align.
- **Long/short relative value** is usually stronger than outright for valuation, carry, term structure, revisions — these rank better than they forecast.
- **Trend and event surprise** signals are more useful for outright direction.
- In FX, commodities, and crypto, combine directional signal with volatility filter — carry and momentum are crash-prone without a vol overlay.

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

All live in `/Trade/` and should be consulted directly when a variable's definition, evidence, or direction is uncertain.
