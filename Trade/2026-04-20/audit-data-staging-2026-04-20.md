# Audit-Addition Variable Staging — 2026-04-20

**Computed:** 2026-04-20 20:03 UTC+8
**Consumer:** daily-market-brief, daily-trade-rec
**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.

---

## 1. Residual Momentum (12m FF5-residualized) — Equity T-input

**Status: MISSING**
**Reason:** numpy not available (market-model fallback)
**Impact:** All 12 single-stock T-scores blocked.

**Chain attempts (root-cause trace):**
- `primary_ff5`: FAILED — numpy not available for OLS computation
- `fallback_market_model`: FAILED — numpy not available (market-model fallback)

## 2. Intermediary Capital Ratio — Cross-Asset R-overlay

**Status: MISSING**
**Reason:** numpy not available for z-score computation
**Impact:** Cross-asset R-overlay leading gate cannot be applied.

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