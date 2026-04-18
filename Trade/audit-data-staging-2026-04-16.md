# Audit-Addition Variable Staging — 2026-04-16

**Computed:** 2026-04-16 21:34 UTC+8
**Consumer:** daily-market-brief, daily-trade-rec
**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.

---

## 1. Residual Momentum (12m FF5-residualized) — Equity T-input

**Status:** 12 computed, 0 missing
**Source:** Kenneth French library (Tier 1) + Yahoo Finance monthly returns (Tier 1)
**Method:** Full FF5 OLS (24-month window)

| Ticker | Residual 12m (%) | T-Score | Raw TSMOM 12m (%) | Conflict? |
|--------|------------------|---------|-------------------|-----------|
| INTC | +38.48 | +1 | +80.89 | no |
| TSM | +21.59 | +1 | +81.06 | no |
| NVDA | +7.18 | +1 | +42.39 | no |
| TSLA | -14.98 | -1 | +41.01 | YES |
| AAPL | -9.34 | -1 | +11.40 | YES |
| GOOGL | +30.52 | +1 | +66.23 | no |
| AMZN | -5.93 | -1 | +2.27 | YES |
| META | -9.55 | -1 | +2.58 | YES |
| PYPL | -33.16 | -1 | -39.54 | no |
| PLTR | -57.17 | -1 | +61.46 | YES |
| MU | +89.52 | +1 | +177.99 | no |
| WDC | +94.78 | +1 | +204.13 | no |

## 2. Intermediary Capital Ratio — Cross-Asset R-overlay

**Status:** STALE-OK
- Current ratio: 0.1261
- Z-score vs 14-observation mean: +0.18
- Mean: 0.1258, Std: 0.0019
- R adjustment: +0
- Data: 14 observations through 2026-04-04
- Source: PD statistics cache (STALE-OK) (Tier 3)
- Double-counting gate: if HY OAS also flags stress, take the more negative of intermediary-capital and HY OAS, not the sum.

## 3. Basis-Momentum (4w / 12w F1-F2 change) — Commodity S-input

**Status:** 5 computed, 0 missing
**Source:** Yahoo Finance futures (Tier 1) + cache for historical spreads (Tier 3)

| Commodity | Spread (F1-F2) | 4w Change | 12w Change | Static Backwd? | Steepening? | Divergence Cap? |
|-----------|----------------|-----------|------------|----------------|-------------|-----------------|
| Brent | 4.7700 | +1.2700 | +1.2700 | Yes | Yes | No |
| WTI | 3.2700 | -3.7100 | -3.7100 | Yes | No | **YES** |
| Gold | -36.1000 | -16.1000 | -16.1000 | No | No | No |
| Silver | -0.5600 | -0.2700 | -0.2700 | No | No | No |
| Copper | -0.0590 | -0.1490 | -0.1490 | No | No | No |

---

*This file is overwritten each run. The brief and trade-rec should read it at startup and incorporate the values into their S/T/R scoring.*