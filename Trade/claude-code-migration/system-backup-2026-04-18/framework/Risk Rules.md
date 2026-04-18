# Risk Rules — Policy Doc

**Last updated:** 2026-04-14
**Status:** Active. Binding on every trade.

This file promotes the sizing, heat, and stop rules from `Trad core.md` and `Coin core.md` into explicit policy. Reference at every entry. When a rule here conflicts with research prose in the cores, this file wins.

---

## 1. Position Sizing

- **Method:** Inverse-ATR volatility targeting with fractional-Kelly overlay.
  - Position $ = (Target Risk $) / (ATR × Multiplier).
  - ATR multiplier: 2–3× for trending assets (commodities, crypto); 1.5–2× for equities.
  - Source: `Trad core.md:203`.
- **Kelly fraction:** **Quarter-Kelly**, maximum 25% single-position cap.
  - Rationale: Full Kelly produces 40–60%+ drawdowns; quarter-Kelly is the professional consensus for crypto and is the right regime for current elevated VIX. Source: `Trad core.md:205`, `Coin core.md:53`.

## 2. Risk per Trade and Portfolio Heat

- **Single position risk at stop:** 0.5–2% of portfolio.
  - 0.5% for illiquid names: PLTR, palladium, platinum. Source: `Trad core.md:210`.
  - 1–2% for liquid names.
- **Total portfolio heat:** **6–8%** max (sum of all live position risks to stop). Source: `Trad core.md:209`.
- **Sector cap:** 25% max any single sector. Source: `Trad core.md:211`.
- **Crypto cap:** 5–15% of portfolio. Source: `Trad core.md:211`.

## 3. Stops and Exits

- **Stops:** ATR-based trailing at 2–3× ATR. Not fixed-percentage.
  - Evidence: 2–3× ATR reduces momentum strategy max DD from −49.8% to −11.4% (Han et al. 2016, via `Trad core.md:213`).
- **TP structure (crypto baseline):** TP1 at 1.5× ATR, TP2 at 3× ATR; at TP1 hit, move stop to breakeven. Source: `Coin core.md:57`.
- **Chandelier exit:** 3× ATR below highest high for crypto trend follows. Source: `Coin core.md:57`.
- **Time-to-invalidation:** Every thesis must also carry a date by which the setup must have moved in favor. A 4-week thesis that hasn't moved in 4 weeks is a failed thesis. Close and free the capital.

## 4. Drawdown Circuit Breakers

- At **−15% portfolio DD:** reduce gross exposure to 50%.
- At **−20% portfolio DD:** move to defensive (gold + cash overweight; no new risk-on entries).
- Source: `Trad core.md:214`.

## 5. Correlation / Concentration Gate (Step 6 overlay)

Before accepting a |sum|≥3 signal as a fresh trade, check:
- Does this thesis share its primary regime variable with any open position? (e.g., Copper long + Gold long + Silver long = one reflation/DXY-weak bet, not three.)
- If yes: treat as an **add** to the existing theme and size the combined bet to the sector cap, not the per-position cap.
- BTC and ETH momentum fire simultaneously ~80% of the time (`Trad core.md:199`) — never double-count these as independent.

## 6. Rebalancing Cadence

- **Hybrid threshold rebalance:** monitor daily, rebalance when 5% absolute drift or a signal change. Tighter 3% bands for crypto.
- Source: `Trad core.md:218`.

## 7. Pre-Entry Checklist (use every trade)

1. Methodology aggregate |sum| ≥ 3? (`Methodology Prompt.md:73`)
2. Invalidation written, concrete, date-bounded? (`Methodology Prompt.md:87`)
3. Correlation gate clean (Section 5 above)?
4. Per-position risk ≤ 2% AND portfolio heat post-entry ≤ 8%?
5. ATR stop set, not fixed %?
6. Catalyst scored and aligned (surprise vs confirmation dependency stated)?

If any answer is no: no trade.
