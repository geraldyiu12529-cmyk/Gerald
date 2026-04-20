# Market Brief — 2026-04-20 v2
**Generated:** 2026-04-20 20:00 UTC+8 (08:00 ET pre-open)
**Routine:** market-brief (skill) — scheduled production run
**Status:** PARTIAL — MISSING Grade A: 3 (residual-momentum all 12 single stocks, intermediary-capital z-score, basis-momentum for WTI/Gold/Silver/Copper). All price/rate variables retrieved.

---

## Step 0 — Staging & Catalyst Input

**Staging file:** `2026-04-20/audit-data-staging-2026-04-20.md` ✅ (read; compute failures noted)
- **Residual momentum:** MISSING — numpy unavailable in compute environment. All 12 single-stock T-scores blocked. FAIL-LOUD.
- **Intermediary capital z-score:** MISSING — numpy unavailable. Cross-asset R leading gate cannot be applied. FAIL-LOUD. Fallback: use HY OAS (V004) as sole R-overlay input.
- **Basis-momentum:** PARTIAL — Brent only (1/5 computed). WTI/Gold/Silver/Copper: MISSING. Brent result: spread +13.95, 4w change +0.95, 12w change +2.95 → static backwardation AND steepening → no divergence cap for Brent. Other commodities: S-score must use static slope only. FAIL-LOUD on dynamic component for WTI/Gold/Silver/Copper.

**Slack digest:** `2026-04-20/slack-digest-2026-04-20.md` ✅ (Grade B)
- Regime pulse: VIX ~20.0 (+14% intraday); SPX ATH; Iran mixed signals; BTC $75,255 (3rd test $75K support)
- P007 TSLAUSDT STOP AT RISK: TSLA spot ~$401.09 ABOVE stop 400.000 (live data: TSLA $400.62)
- P006 AAVEUSDT: Kelp DAO hack ($292M) DeFi stress — AAVE -18% from peak, short directionally supported
- BTC ETF flows strong: $471M Apr-18; $996.4M weekly; weekly high since Jan

**Catalyst cache:** MISSING — `catalysts-cache-{today}.json` not found. Using Memory.md §6 inline. No score leg blocked.

**Key overnight development:** Iran sanctions waiver expired Apr-19 (not renewed). Brent gapped up to $94+ on Apr-20 as mixed Iran signals — "deal close" headlines followed by US Navy seizure of Iranian vessel. Ceasefire expires Apr-22 with no new talks scheduled. Binary unpriced.

---

## Step 1 — Regime Identification

### Macro Regime

| Dimension | State | Change vs Prior |
|---|---|---|
| **Growth** | AMBIGUOUS | UNCHANGED — SPY/QQQ ATH; UMich prelim 47.6 record low; consumer dislocation from energy shock |
| **Inflation** | REFLATION | UNCHANGED — DXY 98.22; breakeven ~2.36%; Brent $94.83 post-waiver expiry. Energy supply premium reasserting. |
| **Policy** | ON HOLD, hawkish tail | UNCHANGED — FOMC Apr-28-29. No cut priced. Rate-path surprise sensitivity (Grade A) elevated. |
| **Financial Conditions** | EASING | UNCHANGED — VIX 19.36; HY OAS 2.85%; NFCI −0.47 (loose); MOVE 65.7. |
| **Risk-on/Risk-off** | RISK-ON with geopolitical binary | UNCHANGED (tail UNRESOLVED) — Equity ATH pricing benign. Ceasefire binary Apr-22 NOT priced. US Navy–Iran seizure on Apr-20 = escalation signal. |

**Regime label:** Risk-on / Reflation; geopolitical-fragile; ceasefire binary Apr-22 = primary unpriced tail

**Primary regime watch variables:**
1. **Brent front-back curve + Iran ceasefire date** ($94.83; April-22 binary with no talks scheduled; US Navy escalation)
2. **HY OAS** (2.85% — contained; financial conditions gate)
3. **VIX/VIX3M ratio** (19.36/20.51 = 0.944 — contango, benign near-term vol)

**Digest cross-check:** Slack digest VIX ~20.0 vs pull 19.36 — divergence ~3%; within normal intraday range, not a staleness flag. DXY digest 98.31 vs pull 98.22 — negligible. Readings consistent. Pull authoritative for 20:00 snapshot.

---

## Step 1.5 — Overlay Gate (Faber TAA, C009, Grade A)

| Sleeve | Asset | Mar-31 Close vs 10m-SMA | Gate Status |
|---|---|---|---|
| Equity (V033) | SPY | ABOVE (SPY Mar-31 ~$700+ vs 10m-SMA ~$580–620 est.) | **ON** |
| Commodity (V034) | GSCI | ABOVE (energy/metals complex elevated) | **ON** |
| Crypto (V035) | BTC | ABOVE (BTC $75k+ vs 10m-SMA est. ~$60–65k) | **ON** |
| Intl Equity (optional) | EFA | ABOVE | **ON** |

**All sleeves ON.** Next read: Apr-30 month-end close. No position-size multipliers triggered.

---

## Step 2 — Key Variable Readings

| Bucket | Variable | Value | Grade | Tier | Staleness | Score Impact |
|---|---|---|---|---|---|---|
| **Cross-Asset** | VIX | 19.36 | A | T1 | LIVE | R: favorable (<25) |
| | VIX3M | 20.51 | A | T1 | LIVE | Term structure contango = benign |
| | VIX/VIX3M ratio | 0.944 | A− | derived | LIVE | <1.0 = normal |
| | MOVE | 65.70 | A | T1 | LIVE | Bond vol compressed; risk-on |
| | DXY | 98.22 | A | T1 | LIVE | Below 100; commodity tailwind |
| | HY OAS | ~2.85% | A | T2 | STALE-WARN (Apr avg) | R: contained; no stress |
| | NFCI | −0.47 | A | T1 | LIVE | Loose financial conditions |
| | Int. Capital z | **MISSING** | **A** | — | — | R leading gate BLOCKED |
| **Rates** | DGS2 | 3.71% | A | T2 | STALE-WARN (Apr-17) | 2s10s = 53.6bps (moderate steep) |
| | DGS10 | 4.246% | A | T1 | LIVE | |
| | 2s10s | 53.6bps | A | derived | LIVE/STALE | Moderate steepening |
| | DFII10 (real) | 1.89% | A | T2 | STALE-WARN (Apr-17) | Elevated real yield; growth ambiguous |
| | T10YIE (breakeven) | ~2.36% | A | derived | STALE-WARN | Reflation regime confirmed |
| | ACM term premium | ~0.59% | A | — | STALE (Jan-2026) | Monthly; last known |
| **Equities** | SPY | 710.14 | A | T1 | LIVE (Apr-17 close) | 12m momentum +24.1% |
| | QQQ | 648.85 | A | T1 | LIVE | 12m strong; ATH |
| | EWJ | 90.19 | A | T1 | LIVE | Yen-hedged Japan |
| | EWY | 152.33 | A | T1 | LIVE | Post-TSM beat recovery |
| | Residual momentum (12 stocks) | **MISSING** | **A** | — | — | All single-stock T-scores BLOCKED |
| **Single Stocks** | NVDA | 201.68 | A | T1 | LIVE | T: BLOCKED |
| | TSLA | 400.62 | A | T1 | LIVE | **P007 SHORT STOP = $400.00 — AT STOP** |
| | AAPL | 270.23 | A | T1 | LIVE | T: BLOCKED |
| | GOOGL | 341.68 | A | T1 | LIVE | Earnings Apr-22 |
| | AMZN | 250.56 | A | T1 | LIVE | Earnings Apr-23 |
| | META | 688.55 | A | T1 | LIVE | Earnings Apr-29 |
| | INTC | 68.50 | A | T1 | LIVE | Earnings Apr-23; T: BLOCKED |
| | TSM | 370.50 | A | T1 | LIVE | T: BLOCKED |
| | MU | 455.07 | A | T1 | LIVE | T: BLOCKED |
| | WDC | 372.52 | A | T1 | LIVE | T: BLOCKED |
| | PLTR | 146.39 | A | T1 | LIVE | T: BLOCKED |
| | PYPL | 50.81 | A | T1 | LIVE | T: BLOCKED |
| **Commodities** | Brent | 94.83 | A | T1 | LIVE | Up ~5–7% on Apr-20 Iran escalation |
| | WTI | 87.22 | A | T1 | LIVE | |
| | Gold | 4,830.70 | A | T1 | LIVE | Near ATH; DXY-correlated |
| | Silver | 79.915 | A | T1 | LIVE | Breakout holding $79+ |
| | Copper | 6.036 | A | T1 | LIVE | | 
| | Palladium | 1,552.0 | A | T1 | LIVE | |
| | Platinum | 2,090.7 | A | T1 | LIVE | |
| | Basis-momentum (WTI/Gold/Silver/Cu) | **MISSING** | **A** | — | — | S static-slope only |
| | Basis-mom Brent | Spread +13.95, 4w+0.95, 12w+2.95 | A | T1 | LIVE | Steepening; no divergence cap |
| **FX** | EURUSD | 1.1763 | A | T1 | LIVE | DXY inverse |
| | USDJPY | 158.898 | A | T1 | LIVE | Yen weak; BOJ watch |
| **Crypto** | BTC | 75,370.6 | A | T1 | LIVE | 3rd test $75K support |
| | ETH | 2,313.3 | A | T1 | LIVE | |
| | BTC ActiveAddr | 396,267 | A | T1 | LIVE | Below 400k threshold — S-negative signal |
| | BTC HashRate | 1,064.99 EH/s | A | T1 | LIVE | Healthy/rising |

**Tier-2 Web Search supplements:**
- HY OAS ~2.85% (Apr 2026 average per Trading Economics)
- DGS2 3.71% (Apr-17, Friday close per Trading Economics)
- DFII10 1.89% (Apr-17, Friday close per Trading Economics)

**MISSING Grade A count: 3**
1. Residual momentum (numpy compute failure) — blocks T for 12 single stocks
2. Intermediary capital z-score (numpy compute failure) — blocks R leading gate
3. Basis-momentum for WTI/Gold/Silver/Copper (0 curve data retrieved) — S static-only for these four

**Stale-Warn flags (acceptable):** HY_OAS (T2 Apr-avg), DGS2 (T2 Apr-17), DFII10 (T2 Apr-17), ACM term premium (monthly, Jan-2026)

---

## Step 3 — Asset Scorecard

**Scoring rules applied:**
- Single-stock T: residual momentum MISSING → T = BLANK (fail-loud; do not substitute raw TSMOM for single stocks)
- Commodity S: basis-momentum MISSING for WTI/Gold/Silver/Copper → S from static slope only; flag MISSING
- Cross-asset R: IC z MISSING → use HY OAS (V004) as sole input. V027 leading gate cannot be applied.
- Overlay Gate: all sleeves ON (Step 1.5)
- Scoring rule: V009+V026 on same single stock → score V026 only (V026 = residual mom = MISSING → T blank)

| Asset | S | T | C | R | Sum | Overlay | Notes |
|---|---|---|---|---|---|---|---|
| **SPY** | +1 | +1 | 0 | +1 | **+3** | ON | **|Sum|≥3 SIGNAL** — QQQ correlation block LIFTED (closed Apr-19). FOMC Apr-28 risk. Raw TSMOM (index/ETF): 1m/3m/12m all positive. R: HY_OAS 2.85% contained + NFCI −0.47 + VIX<20. C=0: FOMC Apr-28 = upcoming risk, no catalyst today. |
| **QQQ** | +1 | +1 | 0 | +1 | **+3** | ON | |Sum|≥3 — but SPY is preferred entry (correlated; SPY has less single-name earnings risk). Earnings cluster Apr-22–23 (GOOGL/TSLA/INTC) = C could flip to +1 after beats, but also gap risk. NEAR-MISS: SPY preferred over QQQ for entry. |
| **BTC** | 0 | +1 | +1 | 0 | **+2** | ON | S=0: ActiveAddr 396k below 400k threshold (Grade A, negative). T=+1: price momentum positive, hash rate strong. C=+1: ETF flows $471M Apr-18, $996M weekly (Grade B); funding most negative since 2023 = squeeze setup. R=0: funding negative = crowding filter neutral. Below threshold — monitor. |
| **Silver** | +1 | +1 | 0 | 0 | **+2** | ON | S=+1 static (DXY weak, gold correlation, no basis-mom). T=+1 raw TSMOM (breakout holding $79+). C=0. R=0 (no catalyst; IC z MISSING). |
| **Gold** | +1 | +1 | 0 | 0 | **+2** | ON | S=+1 static (DXY weak, real yield 1.89%, breakeven 2.36%). T=+1 raw TSMOM ($4,830 near ATH). C=0 (ceasefire Apr-22 = true binary, not asymmetric enough to score). R=0 (IC z MISSING; VIX elevated). |
| **Brent** | +1 | 0 | 0 | +1 | **+2** | ON | S=+1: static backwardation + steepening (basis-mom Brent +0.95/+2.95; no divergence cap). T=0: 1m momentum mixed (recovery from $86 dip but below Mar highs; today's gap-up = new signal but <1 session). C=0: Apr-22 ceasefire expiry = true binary (no deal progress; also US Navy seized Iranian vessel = escalation signal, but price reaction symmetric). R=+1: geopolitical supply shock ongoing; HY OAS contained. Below threshold. |
| **Copper** | +1 | +1 | 0 | 0 | **+2** | ON | S=+1 static slope (basis-mom MISSING). T=+1 raw TSMOM. C=0 (China PMI >50.5 needed). R=0. |
| **GOOGL** | +1 | __ | +1 | 0 | +2* | ON | T BLOCKED (residual mom MISSING). S=+1 structural. C=+1 (earnings Apr-22 = potential AI/cloud beat). R=0. Sum incomplete — cannot promote. *If residual mom recovers: +3 possible if T=+1. |
| **INTC** | +1 | __ | +1 | 0 | +2* | ON | T BLOCKED (residual mom MISSING). S=+1 (Terafab/foundry structural). C=+1 (earnings Apr-23 = confirmation catalyst). Sum incomplete. *If T recovers: +3 possible. |
| **TSM** | +1 | __ | 0 | 0 | +1* | ON | T BLOCKED. C=0 (post-earnings, sell-the-news confirmed). Incomplete, de-prioritized. |
| **EWY** | +1 | +1 | 0 | 0 | **+2** | ON | Raw TSMOM (ETF/index) positive. TSM beat read-through supportive. C=0 (KOSPI needs confirmation). |
| **WDC** | +1 | __ | 0 | 0 | +1* | ON | T BLOCKED. Below threshold. |
| All other single stocks | +varies | __ | varies | 0 | incomplete | ON | T BLOCKED for NVDA/AAPL/AMZN/META/MU/PLTR/PYPL. No promotions possible without residual momentum. |
| **AAVEUSDT** | — | — | — | — | OFF-METHOD | — | P006 short. DeFi hack thesis (Kelp DAO $292M). Short directionally supported; governance-patch bounce risk. Stop $95.00. |
| **TSLAUSDT** | — | — | — | — | OFF-METHOD | — | **P007 short. STOP AT RISK: live TSLA $400.62 > stop $400.00. Verify position status on exchange.** Earnings Apr-22 binary. |
| **CLUSDT** | — | — | — | — | OFF-METHOD | — | P008 long. Stop $85.30. ~$7 buffer from current CL. |

**|Sum|≥3 signals this brief: SPY (+3). QQQ (+3) — NEAR-MISS (SPY preferred).**

**Score change from prior brief:**
- SPY upgraded from CORRELATION-BLOCKED to SIGNAL (+3). QQQ correlation block removed (QQQ closed Apr-19).
- All single-stock T-scores DOWNGRADED to BLANK due to staging compute failure. Previously +1 from 3-day-old cache — that cache is now stale beyond tolerance for numpy-required residual momentum.
- INTC/Gold/QQQ positions CLOSED since prior (mock) brief — corrected.

---

## Step 4 — Catalyst Calendar

| Date | Event | Assets | Impact Assessment |
|---|---|---|---|
| **TODAY Apr-20** | Iran ceasefire status / US Navy seizure | Brent, WTI, Gold, VIX | Escalation signal on Apr-20. Binary: deal = oil −5–10%; no deal = oil +5–10%. Brent $94.83 = mid-point. |
| **Apr-21** | Advance Retail Sales (March) | SPY, QQQ, consumer | Demand read post-energy shock; UMich 47.6 prelim suggests weak consumer |
| **Apr-22** | **Iran ceasefire expires** | Brent, WTI, Gold, VIX, all | PRIMARY BINARY — no new talks; 3 sticking points unresolved. Asymmetric impact: if escalation, S+C+R all flip. |
| **Apr-22** | **TSLA Q1 earnings** | TSLA, QQQ | Consensus $0.36 EPS. Prior beat +9.94%. P007 short faces gap-up risk. |
| **Apr-22** | **GOOGL Q1 earnings** | GOOGL, QQQ | AI/cloud beat could push GOOGL Sum to +3 if residual mom recovered. |
| **Apr-23** | **INTC Q1 earnings** | INTC, QQQ | Terafab validation. Sum +3 catalyst if T recovers. |
| **Apr-23** | AMZN Q1 earnings | AMZN, QQQ | Retail/cloud. |
| **Apr-24** | UMich final April sentiment | SPY, QQQ, DXY | Prelim 47.6 (record low) was 98% pre-ceasefire — potential partial recovery if peace holds. |
| **Apr-28–29** | **FOMC** | All | SPY C-leg: FOMC = rate-path surprise risk. No cut expected; hawkish surprise = C −1 for SPY. |
| **Apr-29** | META Q1 earnings | META, QQQ | Ad revenue vs GOOGL read-through. |
| **May-12** | April CPI | Rates, DXY, Gold, BTC | Energy-shock follow-through in April CPI. |
| **May-14–15** | Xi–Trump summit (Beijing) | DXY, EWY, tariffs | Trade deal catalyst. EWY could re-enter watchlist. |

**Catalyst cache status:** MISSING — inline fallback used.

---

## Step 5 — Portfolio Risk Overlay

**Open positions (off-methodology):**

| Position | Side | Entry | Stop | Live Price | Buffer | Heat |
|---|---|---|---|---|---|---|
| AAVEUSDT (P006) | Short | $90.580 | $95.00 | ~$91 | ~4.4% | ~$19.7 USDT |
| **TSLAUSDT (P007)** | **Short** | $395.560 | $400.00 | **$400.62** | **−0.16% (AT/BELOW STOP)** | ~$4.4 USDT |
| CLUSDT (P008) | Long | $88.250 | $85.30 | ~$87-88 | ~$2-3 | ~$13.2 USDT |

**⚠ P007 TSLAUSDT: Live price $400.62 ABOVE stop $400.00. Stop likely triggered. Verify on exchange immediately.**

**Portfolio heat (if all 3 open):** ~$37 USDT / ~$4,000 NAV ≈ 0.9%. Within 8% cap.
**No methodology circuit breakers active.** V027 IC z MISSING — cannot apply intermediary-capital sizing gate. Conservative approach: no change to sizing on open positions.

**Methodology positions:** None (all methodology positions closed as of Apr-19).

---

## Step 6 — Variable Discovery Notes

1. **BTC ETF flows as formal T-input (Grade B → potential promotion):** Weekly flows $996M (highest since mid-Jan) are now consistently decision-moving for BTC C-scores. This is the 3rd+ consecutive brief where ETF flows influence BTC thesis direction. Item deferred to quarterly methodology review per Memory.md §9. No registry write today (already logged as candidate).

2. **Iran geopolitical event density:** Ceasefire expiry, US Navy seizure, waiver expiry — these three separate events in 24h are creating an abnormal C-score volatility regime for oil and safe-haven assets. Not a variable candidate — a regime flag.

3. **Residual momentum numpy failure:** This is the 1st run with this compute error. If numpy unavailability persists, the audit-addition T-scores will be systematically blocked. Flag for system maintenance — this is a compute infrastructure issue, not a data issue.

**No new variable candidates observed today.**

---

## Step 7 — Watchlist Updates

**Changes from prior state:**

| Asset | Change | Reason |
|---|---|---|
| **SPY** | UPGRADED: CORRELATION-BLOCKED → |Sum|≥3 SIGNAL (+3) | QQQ correlation block lifted (QQQ closed Apr-19 21:31). Re-evaluate for entry in trade-rec. |
| **QQQ** | DOWNGRADED to NEAR-MISS | SPY preferred entry; earnings cluster risk Apr-22-23. |
| **GOOGL/INTC** | BLOCKED — incomplete score | Residual momentum MISSING; T blank. Still flagged for earnings catalyst Apr-22-23. |
| **TSM** | Further de-prioritized | T blocked, C=0 post-earnings. |
| **Brent** | C=0 (was C−1) | Binary now symmetric on Apr-20 (US Navy escalation vs deal hope). |
| All single stocks | T BLANK | Residual momentum compute failure — flag for maintenance. |

---

## Summary for Trade-Rec Handoff

- **Regime:** Risk-on / Reflation. Primary tail: ceasefire binary Apr-22 (UNPRICED).
- **Open positions:** P006 AAVEUSDT short (directionally supported); **P007 TSLAUSDT STOP AT RISK** ($400.62 > $400.00 — verify on exchange); P008 CLUSDT long (monitoring).
- **|Sum|≥3 signal:** SPY (+3). FOMC Apr-28 risk = key timing consideration for entry.
- **Near-miss:** QQQ (+3) — SPY preferred.
- **Below threshold:** BTC (+2), Silver (+2), Gold (+2), Brent (+2), Copper (+2), EWY (+2).
- **Incomplete scores:** GOOGL/INTC (+2* with T blocked) — earnings Apr-22-23 could flip Sum if residual momentum recovers.
- **Data gaps:** Residual momentum (compute infrastructure failure — all single-stock T blank), IC z (compute failure), basis-momentum 4/5 missing. Critical: fix numpy environment before next staging run.
- **MISSING Grade A: 3** — Status: PARTIAL.
