# Market Brief — 2026-04-19 v1
**Generated:** 2026-04-19 ~20:00 UTC+8 (08:00 ET pre-open)
**Last trade:** Friday 2026-04-17 (Saturday–Sunday non-trading)
**Timezone:** UTC+8 · Local date 2026-04-19 (Sunday)
**Status:** PARTIAL — MISSING Grade A = 5 (see §DataQuality)

---

## Step 0 — Staging & Catalysts Input

**Staging file:** `audit-data-staging-2026-04-19.md` ✓ (Sunday weekend test run; Tier 3 cache active)
- Residual momentum: 12/12 computed — same Apr 2025–Mar 2026 window as Apr 17 (no live refresh on weekend)
- Intermediary capital z: **+0.18** (STALE-WARN — data through 2026-04-04; 15 days old, beyond 14-day window; no R adjustment)
- Basis-momentum: 5/5 computed from cache
  - **KEY CHANGE vs Apr 17:** WTI divergence cap (fired in Apr 17 staging, 4w −3.71) **NO LONGER fires** — Apr 19 shows WTI spread +$15.50 steepening (+7.22 4w/12w). Hormuz re-closure Saturday drove extreme backwardation. WTI S-score now uncapped.
  - Brent, WTI: static backwardation + steepening → no cap
  - Gold, Silver: contango → no cap
  - Copper: backwardation + steepening → no cap

**Catalysts cache:** Not written (news-events not run Sunday). Using Memory.md §6.

---

## Step 1 — Regime Identification

### Macro Regime

- **Growth: AMBIGUOUS** — VIX crashed to 17.94 (−44% in 3 weeks), SPY/QQQ at fresh records on ceasefire relief. Counter-signals: UMich prelim 47.6 (record low; 98% of respondents surveyed pre-ceasefire), tariff-pause expiry risk, war-disrupted supply chain. Signal mix is growth-positive on asset prices but demand-negative on sentiment.

- **Inflation: REFLATION building** — DXY 98.24 (below 100; 3rd consecutive weekly decline). 10Y breakeven ~2.38% (derived). Brent/WTI Friday close $86.52/$81.19 then rebounded to ~$96/$89-92 Saturday on Hormuz re-closure. Iran sanctions waiver expired **today** (Apr 19) — US not renewing. Energy supply risk premium is reasserting after brief Friday relief.

- **Policy: ON HOLD, hawkish tail risk** — FOMC Apr 28-29. No rate change priced. But energy-driven inflation + labor market uncertainty = asymmetric hawkish surprise risk if data deteriorates further. Rate-path surprise sensitivity (Grade A) is the key variable to watch at FOMC.

- **Financial Conditions: EASING** — VIX 17.94, HY OAS 2.95% (contained), DXY 98.24, intermediary capital z +0.18 (neutral → no R downgrade). NFCI **MISSING** (blocks FCI confirmation). Conditions are easy; event risk is elevated.

- **Risk-on/off: RISK-ON with acute binary event risk** — Three converging events: (1) Iran sanctions waiver expired today, (2) ceasefire expires Apr 22 with talks collapsed (Pakistan round failed Sunday), (3) FOMC Apr 28-29. Markets at records price a benign outcome. A ceasefire breakdown is a tail that is not priced.

**Regime label: Risk-on, reflation building; ceasefire-expiry binary (Apr 22) = primary unpriced tail**

**Three primary regime variables:**
1. Brent front-back curve (Hormuz open/closed binary → oil & inflation regime)
2. HY OAS (financial conditions gate; currently contained at 2.95%)
3. VIX term structure (FOMC positioning; Apr 28-29)

---

## Step 1.5 — Overlay Gate (Faber TAA, C009)

Read cadence: previous month-end close (March 31, 2026) vs. 10-month SMA. State holds through April.

| Sleeve | V# | Symbol | Mar 31 Close (est.) | 10m-SMA (est.) | Status |
|--------|----|--------|---------------------|----------------|--------|
| Equity | V033 | SPY | ~$665 | ~$610 | **ON** |
| Commodity | V034 | GSCI | — | — | **MISSING — treating as ON** |
| Crypto | V035 | BTC-USD | ~$67,300 | ~$80,000 | **OFF** |

**FAIL-LOUD: GSCI (V034) 10m-SMA state MISSING.** Cannot confirm commodity sleeve. Treating as ON pending Monday live computation.

**Crypto sleeve OFF**: BTC March close ($67,300) is below estimated 10m-SMA (~$80,000; based on Jun 2025–Mar 2026 monthly average including Jan 2026 high ~$102,405 and Dec 2025 ~$88,445). Any BTC/ETH Sum ≥+3 signal: position size × 0, logged Taken=NO with Block_Reason=OverlayGateOff.

---

## Step 2–5 — Variable Table

### Cross-Asset Risk (Grade A)
| Variable | Value | Status | Notes |
|----------|-------|--------|-------|
| VIX | 17.94 | ✓ OK | Apr 17 close; 7-week low; −44% in 3 weeks |
| VIX3M | MISSING | ⚠ MISSING | Blocks VIX term-structure ratio |
| MOVE | 65.89 | ⚠ STALE | Carried from Apr 17 brief; Vol-compressed range |
| DXY | 98.24 | ✓ OK | Apr 17; 3rd consecutive weekly decline; below 100 |
| HY OAS | 2.95% | ✓ OK | FRED BAMLH0A0HYM2; Apr 2026 reading |
| **NFCI** | **MISSING** | ❌ **FAIL-LOUD** | Blocks FCI score leg |
| Intermediary Cap z | +0.18 | ⚠ STALE-WARN | Data through 2026-04-04 (15d); no R adj; z ≥ −1σ |

### Rates
| Variable | Value | Status | Notes |
|----------|-------|--------|-------|
| DGS2 | 3.78% | ✓ OK | Apr 17 close |
| DGS10 | 4.26% | ✓ OK | Apr 17 close |
| 2s10s | +0.48% | ✓ derived | Curve steepening; positive slope |
| DFII10 (real yield) | 1.88% | ✓ OK | Apr 17; compressing |
| T10YIE (breakeven) | ~2.38% | ✓ derived | DGS10 − DFII10; reflation building |
| **ACM TP 10Y** | **MISSING** | ❌ **FAIL-LOUD** | Monthly release; last known Jan 2026 ~0.59% |

### Equities
| Asset | Price | Source |
|-------|-------|--------|
| SPY | $710.75 | Apr 17 close — fresh record |
| QQQ | $648.85 | Apr 17 close — fresh record |
| EWJ | ~$90.19 | Apr 17 est. |
| EWY | ~$147.47 | Apr 17 est. |
| **Revision breadth** | **MISSING** | ❌ **FAIL-LOUD** | Zacks/IBES; blocks equity S-score confirmation |
| % above 200DMA | **MISSING** | ❌ **FAIL-LOUD** | StockCharts; blocks breadth |

#### Residual Momentum — Single-Stock (V026, staging 2026-04-19)
Window: Apr 2025–Mar 2026 (unchanged from Apr 17; weekend cache run)

| Ticker | Residual 12m% | T-Score (V026) | Raw TSMOM% | Conflict |
|--------|---------------|----------------|------------|---------|
| MU | +15.63% | **+1** | +178.44% | no |
| INTC | +13.89% | **+1** | +93.43% | no |
| AAPL | +4.68% | **+1** | +19.94% | no |
| WDC | +2.38% | **+1** | +209.72% | no |
| TSM | +1.00% | 0 | +78.52% | no |
| AMZN | +1.39% | 0 | +14.89% | no |
| META | +0.75% | 0 | +9.25% | no |
| NVDA | −1.00% | 0 | +53.55% | no |
| GOOGL | −0.80% | 0 | +64.84% | no |
| TSLA | −9.12% | **−1** | +36.03% | YES — use V026 (residual priority over raw) |
| PYPL | −5.25% | **−1** | −34.40% | no |
| PLTR | −35.62% | **−1** | +28.37% | YES — use V026 |

Rule applied: when V026 and V009 conflict on same single-stock ticker, score V026 only (Methodology §3, §Scoring rule 1).

### Commodities
| Asset | Price | Status | Notes |
|-------|-------|--------|-------|
| Brent M1 | $86.52 | ⚠ POST-CLOSE NOTE | Apr 17 close; −13% on Hormuz declared open. **Saturday: rebounded ~$96 as Hormuz re-closed. Monday open is first traded read.** |
| WTI M1 | $81.19 | ⚠ POST-CLOSE NOTE | Apr 17 close. Saturday: ~$89-92 in futures. |
| Gold | $4,867.39 | ✓ OK | Apr 17 close; +1.65% |
| Silver | $79.60 | ✓ OK | Apr 17 close; +1.52% |
| Copper | ~$6.07/lb | ⚠ STALE | Apr 15 close; within 1-week staleness window |
| EIA crude stocks | −0.9 Mb crude | ⚠ STALE | Apr 15 release; draws across gasoline (−1.6 Mb) + distillates (−3.1 Mb) |
| Palladium | MISSING | — | Not pulled |
| Platinum | MISSING | — | Not pulled |

#### Basis-Momentum (V028, from staging 2026-04-19)
| Commodity | F1–F2 Spread | 4w Change | 12w Change | Backw'd? | Steepen? | Cap? |
|-----------|-------------|-----------|------------|----------|----------|------|
| Brent | +5.00 | +3.50 | +3.50 | yes | yes | **NO** |
| WTI | +15.50 | +7.22 | +7.22 | yes | yes | **NO** ← reversal from Apr 17 |
| Gold | −25.00 | −20.00 | −20.00 | no | no | NO |
| Silver | −0.39 | −0.29 | −0.29 | no | no | NO |
| Copper | +0.11 | +0.09 | +0.09 | yes | yes | **NO** |

**WTI cap reversal note:** Apr 17 staging showed 4w change −3.71 (cap FIRED; S capped at 0). Apr 19 staging shows +7.22 (cap no longer fires). Hormuz re-closure Saturday drove rapid curve steepening. Treat with caution — this oscillation reflects event-driven noise, not slow structural change. Flag for signal-review.

### FX
| Pair | Rate | Grade | Notes |
|------|------|-------|-------|
| EURUSD | 1.17975 | A | Apr 17 close; DXY weak below 100 |
| USDJPY | ~158.9 | B+ | Apr 16/17; JPY structurally weak despite DXY soft |

### Crypto
| Variable | Value | Grade | Status |
|----------|-------|-------|--------|
| BTC | $77,319 | A | Apr 18 (Saturday) |
| ETH | $2,424.73 | A | Apr 18 (Saturday) |
| BTC hash rate | 968.88 EH/s | A | Apr 17 — healthy, high |
| BTC active addresses | ~470k | A | ⚠ STALE-WARN (carry from prior staging) |
| BTC exchange netflow | MISSING | A | Not pulled today |
| BTC realized vol | ~65% ann. (est.) | A | Derived est. from 18-day OHLC; elevated; HIGH regime |
| **BTC 3m basis** | **MISSING** | A | ❌ **FAIL-LOUD** — blocks basis/crowding confirmation |
| BTC perp funding | Negative (most neg since 2023) | B | ⚠ STALE (Apr 17); squeeze setup |
| BTC ETF flows | ~+$284M (BlackRock Apr 18) | B | Partial; aggregate net unknown |
| ETH ETF flows | MISSING | B | Not pulled |
| Stablecoin supply | MISSING | B | DefiLlama |
| MVRV/SOPR | MISSING | B | Context only; not assessed |

---

## Step 6 — Asset Scorecards (S | T | C | R | Sum)

**Scoring rules applied:**
- V026 vs V009 same-ticker: V026 wins (§Scoring rule 1)
- V027 (IntCap z +0.18) and V004 (HY OAS 2.95%): neither in stress; double-count gate not triggered
- Step 1.5 crypto sleeve OFF: Sum preserved in SignalLedger; position size × 0
- V029 BAB / V031 GP-A / V032 CEI: not scored (Phase 2 pending; MISSING source data)
- V030 DealerGamma: MISSING (subscription-dependent)

### Open Positions
| Asset | S | T | C | R | Sum | Overlay | Action |
|-------|---|---|---|---|-----|---------|--------|
| **INTC** | +1 | +1 | +1 | 0 | **+3** | ON ✓ | HOLD. Earnings Apr 23 = binary. Guided rev $11.7–$12.7B; Terafab/foundry validation = thesis confirmation event. |
| **Gold** | +1 | +1 | +1 | 0 | **+3** | ON ✓ | HOLD. Apr 22 ceasefire expiry = C+1 surprise-dependent. Sanctions waiver expired today (Apr 19). No talks renewal = oil/gold upside. Invalidation: ceasefire renewed AND DXY >100. |
| **QQQ** | +1 | +1 | 0 | +1 | **+3** | ON ✓ | HOLD. FOMC Apr 28-29 = primary risk. Stop $600. Big tech earnings window: GOOGL Apr 22, TSLA Apr 22, INTC Apr 23, AMZN Apr 23, META Apr 29. |

**R-score rationale (all positions):** VIX 17.94 (favorable), HY OAS 2.95% (contained), intermediary capital z +0.18 STALE-WARN (no downgrade — z ≥ −1σ). R = 0 for INTC/Gold; R = +1 for QQQ (vol compression + contained spreads). NFCI MISSING does not independently force R change; defaults to current read. Double-count gate: z=+0.18 and HY OAS 2.95% are NOT simultaneously flagging stress — no double-count issue.

### Near-Misses (SignalLedger candidates)
| Asset | S | T | C | R | Sum | Block |
|-------|---|---|---|---|-----|-------|
| SPY | +1 | +1 | 0 | +1 | +3 | Correlation-blocked by open QQQ (same primary regime variable, Risk Rules §5) |
| BTC | 0 | +1 | +1 | 0 | +2 | Overlay gate OFF (V035; crypto sleeve off until Apr-end evaluation) |

**SPY C-score = 0:** FOMC Apr 28-29 is neutral-to-risky, not a confirmed positive catalyst. No near-term positive surprise expected before FOMC.

**BTC S-score = 0:** Active addresses STALE-WARN (470k — prior staging; below the 600k+ level that would signal expansion). BTC 3m basis MISSING blocks crowding confirmation. Hash rate 968.88 EH/s is healthy (positive structural signal) but insufficient alone for S=+1 vs. the address/on-chain data gap.

### Watchlist (Sum = +2, catalyst pending)
| Asset | S | T | C | R | Sum | Trigger |
|-------|---|---|---|---|-----|---------|
| Brent | +1 | 0 | 0 | +1 | **+2** | T=0: extreme intraday volatility (−13%/+13% in 48h) = trend signal destroyed. C=0: Apr 22 binary is contested asymmetry (ceasefire fail = C+1; renewal = C−1). Trigger: Monday open price direction + Hormuz status. |
| WTI | +1 | 0 | 0 | +1 | **+2** | Same T/C issue as Brent. Basis-momentum cap reversal adds uncertainty. |
| Silver | 0 | +1 | +1 | 0 | **+2** | S=0: contango, basis-momentum flat — no structural curve support. T=+1: price trend above $79. Trigger: 2nd consecutive close ≥$79. |
| Copper | +1 | +1 | 0 | 0 | **+2** | C trigger: China PMI >50.5. No near-term China data release. |
| GOOGL | +1 | 0 | +1 | 0 | **+2** | T=0: residual −0.80% (near-zero; raw TSMOM +64.84% entirely factor-driven). C=+1: earnings Apr 22. If beat → T could flip to +1 via revised residual (next staging), pushing Sum to +3. |
| AAPL | +1 | +1 | 0 | 0 | **+2** | C trigger: earnings not until late April/May. Structural + residual momentum +4.68% confirmed. Hold on watchlist. |
| MU | +1 | +1 | 0 | 0 | **+2** | Residual +15.63% = strongest equity T-signal after INTC. C trigger needed. Earnings not imminent. |
| WDC | +1 | +1 | 0 | 0 | **+2** | Residual +2.38% → T=+1. C trigger needed. Sum +2 pending catalyst. |

### Short Watch / Structural Headwinds
| Asset | Key Signal | Note |
|-------|-----------|------|
| TSLA | Residual −9.12% → T=−1 | Raw TSMOM +36% is factor-driven; use V026 per rules. S and C not assessed today. |
| PLTR | Residual −35.62% → T=−1 | Raw TSMOM +28.37% conflict. Strongest short-side T signal in universe. S/C not assessed today. |
| PYPL | Residual −5.25% → T=−1 | Consistent with raw TSMOM −34.40%. No long thesis. |

---

## Step 4 — Catalyst Map (Next 2 Weeks)

| Date | Event | Assets | Expectation / Asymmetry |
|------|-------|--------|------------------------|
| **2026-04-19 (TODAY)** | Iran oil sanctions waiver expires; US not renewing (Bessent) | Brent, WTI, Gold, VIX | Already announced Apr 15. Monday open = first price response. Bullish oil/gold if Hormuz remains closed; partial catalyst if markets priced this in. |
| **2026-04-22 (Tue)** | Iran ceasefire expires. Talks collapsed Sunday (Pakistan round). | Brent, WTI, Gold, VIX, ALL | **BINARY, HIGH IMPACT.** No deal = Hormuz closure risk → Brent $100+, Gold surge, VIX spike, equity sell-off. Deal = Hormuz open → oil relief, Gold retreat, equity stabilization. Not priced. Mediators (Pakistan/Egypt/Turkey) continuing. |
| **2026-04-22 (Tue)** | GOOGL Q1 earnings (after close) | GOOGL, QQQ | Ad revenue + cloud beat could flip GOOGL T-score, pushing Sum to +3. Positive QQQ tail. |
| **2026-04-22 (Tue)** | TSLA Q1 earnings (after close) | TSLA, QQQ | Consensus EPS $0.38, rev $22.6B. Structural T=−1 (residual). May not drive thesis. |
| **2026-04-23 (Wed)** | **INTC Q1 earnings (after close)** | **INTC (open position)** | Guided rev $11.7–$12.7B. Terafab/foundry validation = Sum +3 confirmation catalyst. Beat → target TP1/TP2. Miss → reassess stop. |
| 2026-04-23 (Wed) | AMZN Q1 earnings | AMZN, QQQ | Cloud/retail read. Not in active scorecard (T=0 residual). |
| 2026-04-24 (Thu) | UMich final April sentiment | SPY/QQQ, DXY | Prelim 47.6 (record low; 98% pre-ceasefire). Potential partial recovery — positive QQQ tail if sentiment improves. |
| **2026-04-28–29 (Tue-Wed)** | **FOMC** | **ALL** | No rate change expected. Risk: hawkish surprise on energy/war inflation. Primary QQQ invalidation risk. SPY stop $680; QQQ stop $600. |
| 2026-04-29 (Wed) | META earnings (same day as FOMC) | META, QQQ | T=0 (residual +0.75%); ad rev + FOMC compounded event risk. |
| 2026-05-12 | April CPI | Rates, DXY, Gold, BTC | Inflation follow-through post-energy shock. |
| 2026-05-14–15 | Xi–Trump summit (Beijing) | US-China tariffs, EWY, DXY | Trade deal/tariff de-escalation potential. EWY watchlist catalyst. |

---

## Step 5 — Risk Overlay Summary

| Factor | Reading | Grade | R Impact | Notes |
|--------|---------|-------|----------|-------|
| VIX | 17.94 | A | Favorable | 7-week low; compressed |
| MOVE | 65.89 | A | Favorable | Low vol in rates |
| HY OAS | 2.95% | A | Neutral/Favorable | Contained; no stress |
| NFCI | **MISSING** | A | Unknown | Blocks FCI gate |
| Intermediary cap z | +0.18 STALE | A | **+0** adj | z ≥ −1σ; no notch. STALE-WARN. |
| DealerGamma (V030) | **MISSING** | B | Unknown | Subscription-dependent. Not assessed. |
| Double-count gate | z=+0.18 / HY OAS 2.95% | — | Not triggered | Neither in stress simultaneously |
| Crowding — BTC | Funding most-negative since 2023 | B | Squeeze setup | Not a directional signal (Methodology §Reconciliation) |
| Crowding — Oil | Hormuz binary dominant | — | Event-driven | Positioning data not available |

**Primary tail risk:** Ceasefire breakdown Apr 22 with Hormuz closure → Brent $100+, VIX spike >25 (QQQ stop triggered), Gold surge. This tail is NOT priced at current VIX 17.94. Portfolio heat ~1.52% combined (well within 8% cap). INTC + QQQ equity heat ~1.00% (within equity cap).

---

## Step 7 — Expression (No New Entries)

Three open positions confirmed (Sum ≥ +3, overlay ON, not correlation-blocked):
- **INTC Long** — confirmed at Sum +3. Earnings Apr 23 = binary catalyst.
- **Gold Long** — confirmed at Sum +3. Apr 22 ceasefire = primary catalyst.
- **QQQ Long** — confirmed at Sum +3. FOMC Apr 28-29 = primary risk; stop $600.

No promotable new |Sum|≥+3 signals:
- SPY +3 → correlation-blocked by QQQ
- BTC/ETH → overlay gate OFF

No shorts: TSLA/PLTR/PYPL have T=−1 but full S/C/R scoring not completed today. Not promotable without full scorecard. Flag for trade-rec session.

---

## Step 8 — Invalidation Criteria (Open Positions)

**INTC (long $64.68, stop $56):**
- Earnings miss: Q1 rev <$11.7B or Terafab/foundry delay guidance → immediate exit
- Trend break below $55 (below stop)
- Time invalidation: 2026-05-13

**Gold (long $4,780.69, stop <$4,640):**
- Ceasefire renewed AND DXY reversal above 100
- Real yield spike above 2.2%
- Break below $4,640
- Time invalidation: 2026-05-14

**QQQ (long avg $640.09, stop <$600):**
- VIX close above 25
- Break below $600
- FOMC hawkish surprise: rate hike signal or hawkish dots revision
- Time invalidation: 2026-05-14

---

## §6 — Variable Discovery Flags

**1. WTI basis-momentum rapid oscillation (flag for signal-review):**
Apr 17 staging: 4w change −3.71 → divergence cap FIRED (S capped at 0).
Apr 19 staging: 4w change +7.22 → cap reversed.
This 48-hour oscillation reflects the Hormuz open/close binary event, not slow structural basis-momentum change. The Boons-Prado (2019) variable is designed for secular slope changes, not intraday geopolitical dislocations. **Flag: assess whether event-driven basis reversals should be excluded from cap-rule computation during active conflict regimes.** Low-threshold observation (first time); will log to variable discovery if it recurs.

**2. Oil T-score fragility in binary event regimes (flag for methodology note):**
Brent moved −13%/+13% in 48 hours around the Hormuz announcement. TSMOM (Grade A) is not designed for one-day binary event dislocations — trend reading becomes unreliable. In active conflict regimes where supply shocks are the primary variable, C (catalyst) carries more weight than T. **This is a second observation of this pattern (first: Apr 17 brief). Approaching 3-occurrence threshold for VariableRegistry flagging.** Note in §9 of next trade-rec.

---

## §DataQuality — Grade A MISSING Summary

| Variable | Blocking | Workaround |
|----------|---------|------------|
| NFCI | FCI score leg | HY OAS 2.95% (OK) + VIX 17.94 (OK) partially substitute |
| ACM TP 10Y | Term-premium rate leg | Last known Jan 2026 ~0.59%; informational only |
| BTC 3m basis | Crypto basis/crowding | Perp funding STALE-WARN (negative, squeeze setup) as partial substitute |
| Revision breadth | Equity S-score confirmation | Residual momentum V026 (all 12 computed) partially substitutes |
| % above 200DMA | Breadth signal | SPY/QQQ at fresh records implies broad participation but not confirmed |

**MISSING Grade A count: 5 → Status: PARTIAL**
(>3 MISSING; pipeline status PARTIAL per Recovery Protocol thresholds)

**STALE-WARN (within or near staleness window, usable):**
- Intermediary capital z +0.18 (15 days; window 14 days — borderline)
- MOVE 65.89 (1 day carry from Apr 17 brief)
- BTC active addresses ~470k (>1 day; trend context only)
- BTC perp funding (STALE from Apr 17; direction unchanged)
- Copper ~$6.07/lb (2 days; within 1-week window)
- EIA crude stocks (4 days; within 7-day window)

---

## Open Position Marks (carry forward from Memory.md — updated at next live session)

| Asset | Side | Entry | Stop | Mark (Apr 17/18 est.) | P&L est. |
|-------|------|-------|------|----------------------|----------|
| INTC | Long | $64.68 | $56 | ~$69.92 | +~8.1% |
| Gold | Long | $4,780.69 | $4,640 | $4,867.39 | +~1.8% |
| QQQ | Long | $640.09 avg | $600 | $648.85 | +~1.4% |

Portfolio heat: ~1.52% combined (within 8% cap). Equity correlation (INTC + QQQ): ~1.00% (within equity cap).

---

*Exit summary: Market brief 2026-04-19 v1 complete — regime=Risk-on/reflation-building/ceasefire-expiry-binary, MISSING Grade A=5, status=PARTIAL*
