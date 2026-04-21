# Audit-Addition Variable Staging — 2026-04-21

**Computed:** 2026-04-21 19:48 UTC+8
**Consumer:** daily-market-brief, daily-trade-rec
**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.

---

## 1. Residual Momentum (12m FF5-residualized) — Equity T-input

**Status:** 12 computed, 0 missing

| Ticker | Residual 12m (%) | T-Score | Raw TSMOM 12m (%) | Conflict? |
|--------|------------------|---------|-------------------|-----------|
| NVDA | -1.00 | +0 | +53.55 | no |
| TSLA | -9.12 | -1 | +36.03 | YES |
| AAPL | +4.68 | +1 | +19.94 | no |
| GOOGL | -0.80 | +0 | +64.84 | no |
| AMZN | +1.39 | +0 | +14.89 | no |
| META | +0.75 | +0 | +9.25 | no |
| TSM | +1.00 | +0 | +78.52 | no |
| INTC | +13.89 | +1 | +93.43 | no |
| MU | +15.63 | +1 | +178.44 | no |
| PYPL | -5.25 | -1 | -34.40 | no |
| PLTR | -35.62 | -1 | +28.37 | YES |
| WDC | +2.38 | +1 | +209.72 | no |

## 2. Intermediary Capital Ratio — Cross-Asset R-overlay

**Status: OK**
- Current ratio: 0.1295
- Z-score vs 3y mean: **+1.65**
- 3y mean: 0.1247, std: 0.0029
- R adjustment: **+0** (z >= -1: no adjustment)
- Data: 20 observations through 2023-01-139
- Double-counting gate: if HY OAS also flags stress, take the more negative of intermediary-capital and HY OAS, not the sum.

## 3. Basis-Momentum (4w / 12w F1-F2 change) — Commodity S-input

**Status:** 1 computed, 4 missing

| Commodity | Spread (F1-F2) | 4w Change | 12w Change | Static Backwd? | Steepening? | Divergence Cap? |
|-----------|----------------|-----------|------------|----------------|-------------|-----------------|
| Brent | +13.9500 | +0.9500 | +2.9500 | yes | yes | no |
| WTI | MISSING | — | — | — | — | Insufficient curve data for WTI (0 days) |
| Gold | MISSING | — | — | — | — | Insufficient curve data for Gold (0 days) |
| Silver | MISSING | — | — | — | — | Insufficient curve data for Silver (0 days) |
| Copper | MISSING | — | — | — | — | Insufficient curve data for Copper (0 days) |

---

*This file is overwritten each run. The brief and trade-rec should read it at startup and incorporate the values into their S/T/R scoring.*