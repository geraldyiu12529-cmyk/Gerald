# Audit-Addition Variable Staging — 2026-04-15

**Computed:** 2026-04-15 22:12 UTC+8
**Consumer:** daily-market-brief, daily-trade-rec
**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.

---

## 1. Residual Momentum (12m FF5-residualized) — Equity T-input

**Status:** 12 computed, 0 missing

| Ticker | Residual 12m (%) | T-Score | Raw TSMOM 12m (%) | Conflict? |
|--------|------------------|---------|-------------------|-----------|
| NVDA | -30.67 | -1 | +94.90 | YES |
| TSLA | -44.21 | -1 | +88.30 | YES |
| AAPL | -3.89 | -1 | +46.00 | YES |
| GOOGL | -0.20 | +0 | +63.30 | no |
| AMZN | -7.20 | -1 | +55.00 | YES |
| META | -25.25 | -1 | +60.40 | YES |
| TSM | -19.78 | -1 | +75.10 | YES |
| INTC | +42.33 | +1 | +2.40 | no |
| MU | +1.44 | +0 | +50.80 | no |
| PYPL | -47.46 | -1 | +5.10 | YES |
| PLTR | -100.26 | -1 | +217.30 | YES |
| WDC | +20.62 | +1 | +125.30 | no |

## 2. Intermediary Capital Ratio — Cross-Asset R-overlay

**Status: OK**
- Current ratio: 0.1261
- Z-score vs 3y mean: **+0.18**
- 3y mean: 0.1258, std: 0.0018
- R adjustment: **+0** (z >= -1: no adjustment)
- Data: 14 observations through 2026-04-04
- Double-counting gate: if HY OAS also flags stress, take the more negative of intermediary-capital and HY OAS, not the sum.

## 3. Basis-Momentum (4w / 12w F1-F2 change) — Commodity S-input

**Status:** 5 computed, 0 missing

| Commodity | Spread (F1-F2) | 4w Change | 12w Change | Static Backwd? | Steepening? | Divergence Cap? |
|-----------|----------------|-----------|------------|----------------|-------------|-----------------|
| Brent | +5.5500 | +3.9500 | +4.0500 | yes | yes | no |
| WTI | +8.0000 | +6.6000 | +6.7000 | yes | yes | no |
| Gold | -25.0000 | -19.0000 | -20.0000 | no | no | no |
| Silver | -0.4000 | -0.2800 | -0.3000 | no | no | no |
| Copper | +0.1100 | +0.0800 | +0.0900 | yes | yes | no |

---

*This file is overwritten each run. The brief and trade-rec should read it at startup and incorporate the values into their S/T/R scoring.*