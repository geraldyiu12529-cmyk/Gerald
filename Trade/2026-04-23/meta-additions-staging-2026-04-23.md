# Meta-Integration Variable Staging (V029-V035) — 2026-04-23

**Computed:** 2026-04-23 19:36 UTC+8
**Consumer:** SHADOW MODE — brief/rec do not consume this file until Phase 3 live_date set.
**Reference:** `meta-analysis-integration-plan-2026-04-18.md`, `framework/Methodology Prompt.md §Step 1.5`, `framework/Risk Rules.md §1.B, §4.B, §5.A, §8`.

---

## V033-V035 C009 Faber TAA Overlay Gate (Step 1.5)

Overlay state flips only at end-of-month (Risk Rules §4.B). State below uses LAST COMPLETED month-end close.

| Var | Sleeve | Symbol | Month-End Date | Close | 10m-SMA | Distance % | **Gate State** |
|-----|--------|--------|----------------|-------|---------|-----------:|---------------:|
| V033_SPY | equity | SPY | 2026-04-01 | 711.21 | 669.67 | +6.20% | **ON** |
| V034_GSCI | commodity | GSG | 2026-04-01 | 32.12 | 25.39 | +26.51% | **ON** |
| V035_BTC | crypto | BTC-USD | 2026-04-01 | 76352.77 | 91571.34 | -16.62% | **OFF** |

**Sleeve-gate rule.** If `OFF`, position size × 0 on that sleeve (Step 1.5 Overlay Gate). Non-additive to Sum.

## V029 BAB (Betting-Against-Beta)

- Proxy: ETF (USMV - SPLV 12m)
- USMV 12m total return: **+2.20%**
- SPLV 12m total return: **+1.74%**
- Spread (USMV - SPLV): **+0.47%**  ->  **PRO-BAB**
- *Tactical proxy only. Canonical AQR BAB factor deferred to Phase 2b.*

**Sleeve rule.** V029 sleeve capped at 1/3 of V009 risk budget (Risk Rules §8). Correlation gate applies on same-ticker BAB leg + V009 spine long.

## V030 DealerGamma

**Status: MISSING** — Subscription pending — SqueezeMetrics / SpotGamma not confirmed as of 2026-04-18 GATE 1
- Grade: B (single-paper Baltussen-Da-Lammers-Martens 2021 JFE; corrected 2026-04-22)
- Sources attempted: SqueezeMetrics GEX (paid), SpotGamma daily composite (paid)
- Next review: 2026-07-01 quarterly methodology review

## V031 GP/A (Gross Profitability / Assets)

**Status: MISSING** — Phase 2 stub — Ken French GP portfolio CSV fetcher not yet implemented
- Grade: A (Novy-Marx 2013)
- Cadence: Quarterly data, monthly portfolio rebalance

## V032 CEI (Composite Equity Issuance)

**Status: MISSING** — Phase 2 stub — scripts/compute_cei.py self-compute not yet implemented
- Grade: A (Daniel-Titman 2006)
- Cadence: Quarterly

---

*Shadow mode: this file is NOT consumed by brief or trade-rec. Phase 3 sets live_date on V029-V035 in VariableRegistry and updates brief/rec SKILL.md to read this file.*