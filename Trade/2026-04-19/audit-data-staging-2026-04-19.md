# Audit-Addition Variable Staging — 2026-04-19

**Computed:** 2026-04-19 01:45 UTC+8 (Sunday — weekend test run, markets closed)
**Data window:** 12-month cumulative Apr 2025–Mar 2026 (unchanged from 2026-04-17)
**Source:** Persistent cache (`Trade/.data-cache/`) — Tier 3 fallback active (weekend, no live market)
**Consumer:** daily-market-brief, daily-trade-rec
**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.

---

## 1. Residual Momentum (12m FF5-residualized) — Equity T-input

**Status:** 12 computed, 0 missing
**Method:** Market-model fallback (FF5 factors available only through 2025-12; Jan–Mar 2026 estimated via SPY beta regression)
**Note:** Weekend run — same 12-month window as 2026-04-17 (Apr 2025–Mar 2026). Values unchanged.

| Ticker | Residual 12m (%) | T-Score | Raw TSMOM 12m (%) | Conflict? |
|--------|------------------|---------|-------------------|-----------|
| NVDA   | -1.00            | +0      | +53.55            | no        |
| TSLA   | -9.12            | -1      | +36.03            | YES       |
| AAPL   | +4.68            | +1      | +19.94            | no        |
| GOOGL  | -0.80            | +0      | +64.84            | no        |
| AMZN   | +1.39            | +0      | +14.89            | no        |
| META   | +0.75            | +0      | +9.25             | no        |
| TSM    | +1.00            | +0      | +78.52            | no        |
| INTC   | +13.89           | +1      | +93.43            | no        |
| MU     | +15.63           | +1      | +178.44           | no        |
| PYPL   | -5.25            | -1      | -34.40            | no        |
| PLTR   | -35.62           | -1      | +28.37            | YES       |
| WDC    | +2.38            | +1      | +209.72           | no        |

## 2. Intermediary Capital Ratio — Cross-Asset R-overlay

**Status: STALE-WARN** (data through 2026-04-04; Thursday 2026-04-17 NY Fed update may add week ending 2026-04-11 — next live run will refresh)
- Current ratio: 0.1261
- Z-score vs 3y mean: **+0.18**
- 3y mean: 0.1258, std: 0.0018
- R adjustment: **+0** (z ≥ −1σ: no adjustment)
- Data: 14 observations through 2026-04-04
- Double-counting gate: if HY OAS also flags stress, take the more negative; do not sum.

## 3. Basis-Momentum (4w / 12w F1-F2 change) — Commodity S-input

**Status:** 5 computed, 0 missing
**Note:** Brent/WTI April data — curve structure confirmed steep backwardation via WebSearch. WTI F1-F2 spread ~$15.50 (steeper than Apr 17 +$8.28). 4w and 12w change values carried from cache pending next weekday live compute. Gold/Silver/Copper from cached values.

| Commodity | Spread (F1-F2) | 4w Change | 12w Change | Static Backwd? | Steepening? | Divergence Cap? |
|-----------|----------------|-----------|------------|----------------|-------------|-----------------|
| Brent     | +5.00          | +3.50     | +3.50      | yes            | yes         | no              |
| WTI       | +15.50         | +7.22     | +7.22      | yes            | yes         | no              |
| Gold      | -25.00         | -20.00    | -20.00     | no             | no          | no              |
| Silver    | -0.39          | -0.29     | -0.29      | no             | no          | no              |
| Copper    | +0.11          | +0.09     | +0.09      | yes            | yes         | no              |

---

**Pipeline test note:** This is the first Claude Code routine test run (2026-04-19, Sunday). Cowork scheduled tasks remain active during parallel-run period. Primary purpose of this run: verify git commit + push workflow end-to-end.

*This file is overwritten each run. The brief and trade-rec should read it at startup and incorporate the values into their S/T/R scoring.*
