# Market Brief — 2026-04-20 v1
**[MOCK — TEST RUN 2026-04-20]**
**Generated:** 2026-04-20 20:00 UTC+8 (08:00 ET pre-open)
**Routine:** market-brief (skill)
**Status:** PARTIAL — MISSING Grade A: 2 (NFCI, ACM term premium). All others computed.

---

## Step 0 — Staging & Catalysts Input

**Staging file:** `2026-04-20/audit-data-staging-2026-04-20.md` ✅
- Residual momentum: 14/14 computed — window Apr 2025–Mar 2026 (3-day-old cache, within 7d window)
- Intermediary capital z: **+1.38** (healthy; no R downgrade)
- Basis-momentum: 5/5 computed — **no divergence caps firing** (WTI cap cancelled; all steepening)

**Catalysts cache:** `.catalysts-cache/catalysts-cache-2026-04-17.json` (3 days old; stale flag suppressed — weekend + Good Friday)

**Key overnight development (Apr-19–20 weekend):** Iran sanctions waiver expired Apr-19 (not renewed). Brent backwardation deepening. Ceasefire expiry Apr-22 — no new talks scheduled.

---

## Step 1 — Regime Identification

### Macro Regime
- **Growth: AMBIGUOUS** — SPY/QQQ at records; UMich prelim 47.6 (record low); FOMC Apr-28-29 asymmetric hawkish risk if CPI re-accelerates on energy.
- **Inflation: REFLATION** — DXY 98.24; 10Y breakeven ~2.40% (derived); Brent re-bid post-sanctions waiver expiry (~$87–90 range). Energy supply premium reasserting.
- **Policy: ON HOLD, hawkish tail** — FOMC Apr-28-29. No cut priced. Rate-path surprise sensitivity (Grade A) elevated.
- **Financial Conditions: EASING** — VIX 17.94; HY OAS 2.95%; DXY 98.24; intermediary capital z +1.38. NFCI **MISSING** — blocks FCI confirmation.
- **Risk-on/off: RISK-ON with binary tail** — Ceasefire expires Apr-22 (no talks scheduled). FOMC Apr-28-29. Markets at records price benign. Tail is NOT priced.

**Regime label: Risk-on, reflation; ceasefire-expiry binary (Apr-22) = primary unpriced tail**

**Primary regime variables:**
1. Brent front-back curve (Hormuz/ceasefire → oil & inflation regime)
2. HY OAS (financial conditions gate; 2.95% = contained)
3. VIX term structure (FOMC Apr-28-29 positioning)

---

## Step 1.5 — Overlay Gate (Faber TAA, C009)
- Reading: Mar-31 month-end close vs. 10-month SMA — **ALL ABOVE SMA**. Overlay = **RISK-ON** (holds through April).
- Next update: Apr-30 month-end.

---

## Step 2 — Variable Table (Top-28, abbreviated)

| # | Variable | Value | Grade | S | T | C | R | Notes |
|---|----------|-------|-------|---|---|---|---|-------|
| 1 | Equity momentum (SPY 12m) | +24.1% | A | +1 | — | — | — | Above threshold |
| 2 | Bond-equity carry (DY vs 10Y) | 1.43% vs 4.28% | A | — | — | — | −1 | Equity expensive vs bonds |
| 3 | Credit spread (HY OAS) | 2.95% | A | — | — | — | +1 | Contained; risk-on |
| 4 | DXY trend | 98.24 (below 100) | A | +1 | — | — | — | Bearish USD = commodity tailwind |
| 5 | VIX level | 17.94 | A | — | — | +1 | — | Vol compression = regime extension signal |
| 6 | Gold momentum | +2.45% (5d mark) | A | +1 | +1 | — | — | DXY + real yield compression |
| 7 | Brent basis-momentum | Backwardation + steepening | A | +1 | — | — | — | Cap cancelled post-Hormuz |
| 8 | BTC 30d momentum | +5.2% | B | 0 | +1 | +1 | — | Funding negative (crowding filter) |
| 9 | Residual momentum — INTC | +14.10% | A | — | +1 | — | — | Key open position |
| 10 | Intermediary capital z | +1.38 | A | — | — | — | 0 | No R downgrade |
| … | (remaining 18 per Methodology Prompt.md) | — | — | — | — | — | — | See master-data-log.xlsx DailyVariables |

**MISSING — Grade A:**
- NFCI (Chicago Fed) — blocks FCI step confirmation. Latest reading from 2026-04-10 (10 days old). Using stale value −0.12 with STALE-WARN flag.
- ACM term premium 10Y — Apr-2026 not yet posted (monthly; last Jan-2026 ~0.59%).

---

## Step 3 — S|T|C|R|Sum Scorecard (open positions)

| Asset | S | T | C | R | Sum | Status |
|-------|---|---|---|---|-----|--------|
| **INTC** (open long) | +1 | **+1** | +1 | 0 | **+3** | HOLD — earnings Apr-23 confirmation catalyst |
| **Gold** (open long) | +1 | +1 | +1 | 0 | **+3** | HOLD — ceasefire expiry Apr-22 = binary tail; thesis intact |
| **QQQ** (open long) | +1 | +1 | +1 | +1 | **+4** | HOLD — strongest signal; vol compression extending; FOMC Apr-28 risk |
| SPY (watchlist) | +1 | +1 | 0 | +1 | +3 | CORRELATION-BLOCKED by QQQ |
| BTC (watchlist) | 0 | +1 | +1 | 0 | +2 | Below threshold — monitor |
| TSM (watchlist) | +1 | +1 | 0 | 0 | +2 | C=0 post-earnings; de-prioritized |
| Copper (watchlist) | +1 | +1 | 0 | 0 | +2 | C needed (China PMI >50.5) |
| GOOGL (watchlist) | +1 | 0 | +1 | 0 | +2 | T=0 (residual −0.50%); earnings Apr-22 could flip C→+1 but Sum ceiling +2 without T |

---

## Step 4 — Data Quality

| Item | Status |
|------|--------|
| Grade A variables available | 26/28 |
| NFCI | MISSING (STALE 10d — using stale; no score leg blocked for open positions) |
| ACM term premium | MISSING (monthly; Jan-2026 value used as estimate) |
| Residual momentum cache | STALE-WARN 3d (within 7d window — acceptable) |
| Catalysts cache | STALE 3d (weekend + Good Friday — suppressed) |

**Brief verdict: PARTIAL — 2 Grade A missing. No open position score blocked.**

---

## Step 5 — Risk Overlay

Open portfolio heat: **~1.52%** (vs 8% cap). All three positions have:
- ATR stops set and documented
- Time invalidations (May-13 / May-14)
- Catalyst asymmetry stated

**No circuit breakers triggered.** Correlation gate: INTC + QQQ = 1.00% equity heat (within sector cap).

---

## Summary for trade-rec handoff
- Regime: Risk-on, reflation. Primary tail: ceasefire Apr-22.
- Open positions: INTC (+3 HOLD), Gold (+3 HOLD), QQQ (+4 HOLD).
- Watchlist: BTC +2, TSM +2, Copper +2, GOOGL +2 (none promotable today).
- New candidate watch: None — no new |Sum|≥3 signals in universe scan.
- Data gaps: NFCI (stale), ACM term premium (monthly). Neither blocks open position thesis.
