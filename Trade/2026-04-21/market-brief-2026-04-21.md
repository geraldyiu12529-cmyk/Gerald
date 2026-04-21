# Market Brief — 2026-04-21 (20:00 UTC+8) [Local — Authoritative]

**Generated:** 2026-04-21 20:10 UTC+8 | **Version:** v1 | **Run type:** Local (20:00 slot — authoritative; cloud 18:00 run was supplementary)
**Grade A MISSING:** 1 (GSCI commodity sleeve gate V034 — 4th consecutive run)
**Grade A STALE FALLBACK (Tier-3, within window):** 4 (basis-momentum WTI/Gold/Silver/Copper — Apr 17 cached, 5d staleness window)
**Key Change vs Prior Brief (2026-04-20 v2):** T-scores resolved for all 12 single stocks (numpy failure cleared by preflight). New signals: AAPL +3 (T flip), INTC +4 (T flip), MU +3 (T flip), GOOGL +3 confirmed. IC z +1.65 and MOVE 67.90 both available (were MISSING). MISSING Grade A down to 1 (from 3).

---

## Step 1.5 — Overlay Gate Status (Faber TAA, V033–V035, Grade A)

Read cadence: prior month-end close (2026-03-31) vs 10-month SMA. Gate flips monthly.

| Sleeve | Index | Mar-31 Close vs 10m-SMA | State |
|--------|-------|--------------------------|-------|
| Equity | SPY/QQQ | $710+ at Mar-31 >> est. 10m-SMA ~$650–680 | **ON** |
| Commodity | GSCI | GSCI MISSING — no index data | **UNCERTAIN (tentative OFF)** |
| Crypto | BTC-USD | $76,454 (Apr 21) < est. 10m-SMA ~$80–85K | **OFF** |
| Intl Equity | EWJ/EFA | $90.19 (Apr 18) well above est. 10m-SMA ~$78–82 | **ON** |

Commodity sleeve gate unresolvable for the 4th consecutive local run. Silver Sum+3 remains gate-blocked. Brent is Sum+2 (below threshold regardless). Commodity longs on Copper/Gold are near-miss (Sum+2 or gate-blocked).

---

## Step 1 — Regime Snapshot

| Dimension | State | Key Reading |
|-----------|-------|-------------|
| Growth | Neutral-to-Positive | SPY $708.72, QQQ $646.79 (Apr 21 close); S&P 88% Q1 beat rate |
| Inflation | Moderating-to-Uncertain | T10YIE 2.36%; WTI $86.32, Brent $90.03; CPI next May 12 |
| Policy | Dovish lean fading | DGS10 4.25%; FOMC Apr 28–29; CME ≤1 cut priced for 2026 |
| Financial Conditions | Loose, tightening at margin | NFCI −0.47 (Apr 10, stale); HY OAS 285 bps (B); MOVE 67.90 (A) |
| Risk Sentiment | Risk-On, fragile | VIX 19.04 (B, near 20 threshold); Iran binary today; DXY 98.24 |
| BTC Vol Regime | Support-Hold | BTC $76,454 (4th test $75K support); hash rate 1,065 EH/s ✓ |

**Regime Label:** `RISK-ON / GEOPOLITICAL-BINARY — IRAN CEASEFIRE EXPIRED (APR-22 UTC+8)`

**Change vs prior:** No regime flip. Label sharpened: ceasefire was T-1 yesterday, now T-0 (expired). Iran re-closed Strait of Hormuz after US Navy seizure of Iranian cargo vessel Apr 19–20. VIX 19.04 = at the 20-threshold watch level. KelpDAO DeFi exploit ($292M, $195M Aave bad debt) is a crypto-specific tail risk; contained from cross-asset perspective.

**Primary watch variables (Apr 21–25):**
1. **WTI $88 / $95 (A):** Ceasefire binary resolution — hold <$90 = negotiation-hope priced; reclaim >$95 = risk-off flip across all assets. Currently $86.32 — below $88 watch.
2. **VIX 17 / 20 (B):** Sustain <19 = controlled; spike >20 = binary breakdown = R score headwind. Currently 19.04 — right at the pivot.
3. **BTC $75K / $71.2K (A):** 4th test of $75K support ongoing. Hold = floor confirmed; break = forced liquidation cascade + crypto divergence resolution.

---

## Step 2–5 — Key Variable Readings

**MISSING Grade A: 1** — GSCI commodity sleeve gate (V034). Commodity sleeve defaults to UNCERTAIN; no commodity positions can be taken until gate confirmed.
**STALE FALLBACK Tier-3:** Basis-momentum WTI/Gold/Silver/Copper (Apr 17, within 5-day staleness window). Used in S-scoring with STALE notation.

### Cross-Asset Risk & Financial Conditions

| Variable | Reading | Grade | Freshness | Score Impact |
|----------|---------|-------|-----------|--------------|
| VIX | 19.04 | B (BNMA) | Fresh (Apr 21 16:45) | R: +0 — at threshold; not decisively non-stressed |
| VIX3M | 20.51 | B (BNMA) | STALE (Apr 18) | VIX/VIX3M ≈ 0.93 = contango = normal |
| MOVE | 67.90 | A | Fresh (Apr 21 04:30) | R: +1 — low bond vol = loose FCI |
| HY OAS | 285 bps | B (BNMA) | Fresh (Apr 21 17:02) | R: +1 — tight, non-stressed (V027 > V004 gate: V027 dominates) |
| NFCI | −0.47 | A | STALE (Apr 10, 11d) | R: +1 context — loose; last available weekly print |
| IC ratio z-score (V027) | +1.65 | A | Fresh (Apr 21 19:48) | R adjustment: **+0** — z > −1σ, no downgrade; dealers well-capitalized |

**Double-count gate (V027 vs V004):** Both available. V027 +1.65 = positive (no stress). V004 HY OAS 285 bps = tight (no stress). No conflict. V027 is leading indicator — no R notch.

### Rates

| Variable | Reading | Grade | Freshness |
|----------|---------|-------|-----------|
| DGS10 | 4.25% | A | Fresh (Apr 21 02:59) |
| DGS2 | ~3.71% (derived from 2s10s) | A | Implied |
| 2s10s | +0.54% | B (BNMA) | Fresh (Apr 21 17:02) |
| T10YIE (breakeven) | 2.36% | A | Fresh (Apr 21 17:02) |
| DFII10 (real yield) | 1.89% | B (BNMA) | Fresh (Apr 21 17:02) |

Notes: Curve steepening (+0.54%) = no inversion drag. Real yield 1.89% — elevated but compressing from peak. Breakeven 2.36% = above Fed 2% target; FOMC Apr 28 must navigate energy-driven inflation overshoot risk from Hormuz.

### Equities & ETFs

| Variable | Reading | Grade | Freshness |
|----------|---------|-------|-----------|
| SPY | $708.72 | A | Fresh (Apr 21 04:00, US Apr 20 close) |
| QQQ | $646.79 | A | Fresh (Apr 21 04:00) |
| EWJ | $90.19 | A | STALE (Apr 18, 3d) — trend direction intact |
| EWY | $152.33 | A | STALE (Apr 18, 3d) |

### FX

| Variable | Reading | Grade | Freshness | Context |
|----------|---------|-------|-----------|---------|
| DXY | 98.242 | A | Fresh (Apr 21 16:50) | −3.9% from Apr 9 peak ~102 |
| USDJPY | 158.898 | A | Borderline (Apr 20 20:10) | BOJ 0.75%; yen carry intact |
| EURUSD | 1.1763 | A | Borderline (Apr 20 20:09) | Context only — FX not trading |

### Commodities

| Variable | Reading | Grade | Freshness |
|----------|---------|-------|-----------|
| WTI | $86.32 | A | Fresh (Apr 21 16:50) |
| Brent | $90.03 | A | Fresh (Apr 21 16:49) |
| EIA Crude Draw | −0.913 Mb | A | Fresh (Apr 21 17:03) |
| EIA Crude Stocks | 463.8 Mb | A | Fresh (Apr 21 17:03) |
| Gold | $4,808.50 | A | Fresh (Apr 21 16:50) |
| Silver | $79.065 | A | Fresh (Apr 21 16:50) |
| Copper | $6.035/lb | A | Fresh (Apr 21 16:50) |
| Palladium | $1,552 | A | Borderline (Apr 20) |
| Platinum | $2,090.7 | A | Borderline (Apr 20) |

### Crypto

| Variable | Reading | Grade | Freshness |
|----------|---------|-------|-----------|
| BTC | $76,454 | A | Fresh (Apr 21 17:03) |
| ETH | $2,313.3 | B | STALE (Apr 20 20:10, ~22h, 4h window) |
| BTC Active Addresses | 396,267 | A | Borderline (Apr 19, 2d/2d window) |
| BTC Hash Rate | 1,065 EH/s | A | Fresh (Apr 19, 2d/3d window) |
| BTC ETF Flow | +$412M | B | Fresh (Apr 21 17:03) |
| KelpDAO exploit | −$292M rsETH | B | Apr 20 — contained; Aave $195M bad debt |

---

## Audit-Addition Variable Status (V026–V028, Grade A)

*Source: audit-data-staging-2026-04-21.md, computed 19:48 UTC+8*

### V026 — Residual Momentum (FF5-residualized, 12m) — ALL COMPUTED ✓

| Ticker | Residual 12m | T-Score | Raw TSMOM 12m | Conflict? |
|--------|-------------|---------|---------------|-----------|
| NVDA | −1.00% | **0** | +53.55% | No |
| TSLA | −9.12% | **−1** | +36.03% | **YES** — trust residual |
| AAPL | +4.68% | **+1** | +19.94% | No |
| GOOGL | −0.80% | **0** | +64.84% | No |
| AMZN | +1.39% | **0** | +14.89% | No |
| META | +0.75% | **0** | +9.25% | No |
| TSM | +1.00% | **0** | +78.52% | No |
| INTC | +13.89% | **+1** | +93.43% | No |
| MU | +15.63% | **+1** | +178.44% | No |
| PYPL | −5.25% | **−1** | −34.40% | No |
| PLTR | −35.62% | **−1** | +28.37% | **YES** — trust residual |
| WDC | +2.38% | **+1** | +209.72% | No |

T-score threshold: >+2% → +1; between −2% and +2% → 0; <−2% → −1. Conflicts resolved by trusting residual (Blitz-Huij-Martens 2011, Grade A).

### V027 — Intermediary Capital Z-Score — +1.65 ✓

- Ratio: 0.1295 | 3y mean: 0.1247 | std: 0.0029 | Z: **+1.65**
- R adjustment: **+0** (z > −1σ threshold). Dealers well-capitalized. No notch.
- Double-count gate with HY OAS: both non-stressed; V027 dominates as leading indicator.

### V028 — Basis-Momentum (Commodity S-input)

| Commodity | Static Slope | 4w Δ | 12w Δ | Freshness | Steepening? | Divergence Cap? | S Impact |
|-----------|-------------|------|-------|-----------|-------------|-----------------|----------|
| Brent | Backwd +13.95 | **+0.95** | **+2.95** | Fresh (Apr 21) | YES | No | S+1 maintained |
| WTI | Backwd | **+6.98** | **+6.98** | STALE T3 (Apr 17) | YES | No | S+1 conditional (stale) |
| Gold | Contango | **−20.0** | **−20.0** | STALE T3 (Apr 17) | Further contango | N/A | No cap; S scored on fundamentals |
| Silver | Near-flat | **−0.29** | **−0.29** | STALE T3 (Apr 17) | Flat | No | S unchanged |
| Copper | Near-flat | **+0.09** | **+0.09** | STALE T3 (Apr 17) | Flat | No | S unchanged |

WTI/Gold/Silver/Copper: compute_audit_additions.py failed (insufficient curve data in futures_curves.csv). Values above are Tier-3 fallback from Apr 17 cache (within 5-day staleness window). Fail-loud: audit staging marked these MISSING; treated here as STALE FALLBACK.

---

## Step 6 — Asset Scorecard (S | T | C | R | Sum)

**Scoring rules (binding):** V026 only for single-stock T (no sum with V009); V027 double-count gate with V004; overlay gate multiplies post-Sum position size by 0 for gated sleeves.

**R baseline for this run:** +1 (MOVE 67.90 = A, low; HY OAS 285 bps = tight; IC z +1.65 = no notch; VIX 19.04 = borderline but R = +1 given MOVE + HY OAS dominance). Exception: BTC R=0 (crypto sleeve OFF + DeFi tail).

| Asset | S | T | C | R | Sum | Status | Sleeve | Note |
|-------|---|---|---|---|-----|--------|--------|------|
| **INTC** | +1 | +1 | +1 | +1 | **+4** | **PROMOTED — NEW** | Equity ON | Residual +13.89%; earnings Apr-23 AC (Terafab validation = C+1); re-entry after P004 closed Apr-19 |
| **GOOGL** | +1 | 0 | +1 | +1 | **+3** | **PROMOTED** (entry contingent) | Equity ON | Residual −0.80% (T=0 resolved); C+1 pre-earnings (88% beat rate); entry after beat confirmed Apr-23 |
| **AAPL** | +1 | +1 | 0 | +1 | **+3** | **PROMOTED — NEW** | Equity ON | Residual +4.68%; no near-term catalyst (May 1 earnings); correlation gate vs SPY required in trade-rec |
| **SPY** | +1 | +1 | 0 | +1 | **+3** | **ACTIVE — P009 fill pending** | Equity ON | Entry $710.14, stop $696 (2×ATR), target $720–730, time-stop 2026-05-13 |
| **EWJ** | +1 | +1 | 0 | +1 | **+3** | **ACTIVE — P010 fill pending** | Intl Equity ON | Entry ~$90.24, stop $86.00 (2×ATR), target $95–98, time-stop 2026-06-30 |
| MU | +1 | +1 | 0 | +1 | **+3** | **New watch candidate** | Equity ON | Residual +15.63%; DRAM cycle; earnings June; check correlation gate vs SPY/QQQ |
| Silver | +1 | +1 | 0 | +1 | **+3** | **GATE-BLOCKED** | Commodity UNCERTAIN | P012 Taken=NO (OverlayGateOff); GSCI gate unresolvable; basis-mom flat (no divergence cap) |
| QQQ | +1 | +1 | 0 | +1 | **+3** | Near-miss | Equity ON | Correlation-blocked (SPY is primary equity position — same theme); log near-miss |
| NVDA | +1 | 0 | +1 | +1 | **+3** | Near-miss | Equity ON | GOOGL earnings read-through C+1; residual −1% T=0; correlation gate vs SPY needed |
| Copper | +1 | +1 | 0 | +1 | **+3** | Near-miss | Commodity UNCERTAIN | Commodity sleeve gate blocks; China PMI needed for C+1 |
| Brent | +1 | 0 | 0 | +1 | **+2** | Watchlist | Commodity UNCERTAIN | Apr-22 binary C=0; T=0 (short-term trend mixed post-seizure spike) |
| Gold | +1 | 0 | 0 | +1 | **+2** | Watchlist | Commodity UNCERTAIN | DXY weak, real yield compressing; C=0 post-ceasefire binary |
| BTC | 0 | +1 | +1 | 0 | **+2** | Watchlist | Crypto OFF | Active addr 396,267 < 400K → S=0; funding most negative since 2023 → squeeze setup; sleeve OFF |
| TSM | +1 | 0 | 0 | +1 | **+2** | Watchlist | Equity ON | T resolved to 0 (+1.00%); C=0 post-Q1 earnings (sell-the-news) |
| WDC | +1 | +1 | 0 | +1 | **+2** | Watchlist | Equity ON | Residual +2.38% (borderline +1); C=0 pending catalyst |
| META | +1 | 0 | 0 | +1 | **+2** | Watchlist | Equity ON | Residual +0.75%; earnings Apr-29 same-day as FOMC |
| AMZN | +1 | 0 | 0 | +1 | **+2** | Watchlist | Equity ON | Residual +1.39%; earnings Apr-23 |
| EWY | +1 | 0 | 0 | +1 | **+2** | Watchlist | Intl Equity ON | T stale (price Apr 18); below threshold |
| PLTR | +1 | −1 | +1 | +1 | **+2** | Watchlist | Equity ON | Residual −35.62% (T=−1; conflict with raw TSMOM — trust residual) |
| WTI | 0 | 0 | −1 | +1 | **0** | No trade | Commodity UNCERTAIN | Basis-mom stale; C=−1 (ceasefire deal = oil down sharply) |
| TSLA | +1 | −1 | −1 | +1 | **0** | No trade | Equity ON | Residual −9.12% (T=−1; conflict with raw TSMOM — trust residual); C=−1 (earnings Apr-22 binary; P007 closed) |
| ETH | 0 | +1 | 0 | 0 | **+1** | No trade | Crypto OFF | Stale price; sleeve OFF; KelpDAO DeFi contagion risk |
| PYPL | 0 | −1 | 0 | +1 | **0** | No trade | Equity ON | Residual −5.25%; S=0 (no structural edge) |

**Promoted signals this run:**
1. INTC +4 (NEW — T resolved to +1 with earnings catalyst)
2. GOOGL +3 (confirmed — T resolved, entry contingent on earnings beat Apr-23)
3. AAPL +3 (NEW — T resolved to +1; correlation gate check required)
4. SPY +3 (continuing — P009 fill pending)
5. EWJ +3 (continuing — P010 fill pending)

**Near-miss signals (Sum+3, blocked):**
- MU +3 (new candidate, not yet in watchlist — add to §5)
- Silver +3 (gate-blocked, commodity sleeve uncertain)
- QQQ +3 (correlation-blocked by SPY)
- NVDA +3 (correlation gate check; GOOGL read-through C only until GOOGL confirms)
- Copper +3 (commodity sleeve gate blocks)

---

## Step 4 — Catalyst Map (Next 48h Priority)

| Date | Event | Assets | C Impact | Thesis Dependency |
|------|-------|--------|----------|-------------------|
| **Apr-22 AC (~01:00 UTC+8 Apr-23)** | **GOOGL Q1 earnings** | GOOGL, NVDA, QQQ | C+1 if beat | Entry trigger: beat → confirm GOOGL sum +3; read-through to NVDA C+1 |
| **Apr-22 (US daytime, Apr-22 UTC+8 AM)** | **Iran ceasefire resolution** | Brent, WTI, Gold, VIX, ALL | C±1 | Binary: deal = Brent −5–10%; no-deal = +5–10%; Hormuz re-closure = global risk-off |
| **Apr-22 AC** | **TSLA Q1 earnings** | TSLA | C already scored −1 | P007 closed. No position. If TSLA drops post-miss → T=−1 strengthens short thesis but not actionable vs methodology. |
| **Apr-23 AC** | **INTC Q1 earnings** | INTC, QQQ | C+1 if Terafab validates | Primary thesis trigger for INTC +4. Entry before earnings carries earnings-gap risk. |
| **Apr-23** | **AMZN Q1 earnings** | AMZN, QQQ | C+1 potential | Sum+2 currently → beat + positive cloud read-through could push C+1 → Sum+3 next run. |
| **Apr-28–29** | **FOMC statement** | All | Depends on tone | Primary invalidation risk for SPY P009. Hawkish surprise (>2 cuts removed) → exit into print if SPY <$700. |

---

## Step 5 — Risk Overlay Summary

- **Vol state:** VIX 19.04 (B, at threshold); MOVE 67.90 (A, low bond vol). Condition: MOVE suggests loose FCI despite VIX near 20. R = +1 baseline.
- **Credit:** HY OAS 285 bps (B, tight). V027 IC z +1.65 dominates as leading indicator (PL-NMA P(V027>V004)=1.000). No double-count applied. Both non-stressed.
- **IC capacity:** V027 z +1.65 = dealers well-capitalized. No R notch. Positive condition for liquidity provision.
- **Crypto tail:** KelpDAO exploit $292M (Apr 20); $195M Aave bad debt; $5.1B stablecoin frozen. Contained from cross-asset perspective. BTC +$76K resilient. ETH watch.
- **Geopolitical:** Hormuz closure = supply shock. Brent $90 + WTI $86 = within prior-brief ranges. VIX 19.04 = market is pricing Iran risk without panic.
- **Earnings anomaly (Grade B context):** S&P 88% beat rate but avg +0.2% price response (vs historical +1.0%). "Sell the news" environment. Entry timing around earnings beats is important — consider entering AFTER confirmed beat, not before.

**Portfolio heat (pre-new-entries):**
- P008 CL Long (off-meth): ~0.33%
- P009 SPY (pending): 1.0% risk
- P010 EWJ (pending): 0.75% risk
- Total: ~2.08% heat. Cap = 8%. Room: ~5.92% for new positions.

---

## Step 7 — Position Status

### Active Positions

| ID | Asset | Side | Entry | Stop | Heat % | Status |
|----|-------|------|-------|------|--------|--------|
| P008 | CLUSDT Perp | Long | $88.250 | $85.300 | ~0.33% | Off-methodology. CL = WTI perp. WTI $86.32 = between entry and stop. Watch: if WTI holds >$85, thesis intact (Hormuz premium). |
| P009 | SPY | Long | $710.14 | $696 | 1.0% | Fill pending — promoted Apr-20 v3, re-confirmed cloud Apr-21 18:00 and local 20:00. |
| P010 | EWJ | Long | ~$90.24 | $86.00 | 0.75% | Fill pending — promoted cloud Apr-21 18:00 and local 20:00 re-confirmed. Nikkei +1.21% Apr-21. |

**P008 Risk Note:** WTI $86.32 is $1.02 above the CL stop proxy ($85.30). If Iran ceasefire fails and WTI spikes >$95, P008 benefits. If Iran deal and WTI drops to $80 range, P008 stop hit. Off-methodology; tolerance as-is.

### Watchlist Updates

| Asset | Prior Status | Update |
|-------|-------------|--------|
| GOOGL | Sum +3† (T blocked) | T resolved to 0. Sum +3 confirmed. Entry after earnings beat Apr-23. |
| AAPL | Not in watchlist | NEW — Sum +3. Add. Correlation gate vs SPY check in trade-rec. |
| INTC | Sum +1* (T blocked) | T resolved to +1. Sum +4. STRONG signal. Earnings Apr-23 AC. |
| MU | Not in watchlist | NEW — Sum +3. Add. Correlation gate check vs SPY/QQQ. |
| TSM | Sum +2 (T blocked) | T resolved to 0. Sum +2. Unchanged below threshold. |
| Silver | Gate-blocked | Unchanged. Commodity sleeve still UNCERTAIN. |
| Brent | Sum +2 | Unchanged. Apr-22 binary pending. |
| BTC | Sum +2 | Unchanged. 4th test $75K. |

---

## Regime & Structural Notes

**Iran Ceasefire (CRITICAL):** Ceasefire expired. As of this brief, no extension confirmed. Key asymmetry: Hormuz closure = global supply shock → oil +10–15%, equities −3–5%, gold +3–5%, VIX spike >25. Hormuz reopens = oil −10%, equities +2–3%, rates down slightly. The market (Brent $90, VIX 19) is pricing partial closure risk — not full crisis. SPY P009 thesis survives a moderate oil move; invalidation = VIX >25 + SPY <$696.

**GOOGL Earnings (CATALYST TONIGHT):** 88% Q1 beat rate. Mag7 blended EPS growth +22.8% bar. The "sell-the-news" anomaly (avg +0.2% response on beats) is a risk. GOOGL C=+1 scored pre-event means the score assumes the beat. If beat + positive cloud commentary = GOOGL +3 entry Apr-23. If miss = C=0 or C=−1, score falls to +2 or +1 = no entry.

**INTC Earnings (Apr-23):** Terafab/foundry validation is the structural thesis. Q1 rev guidance $11.7–$12.7B. If INTC beats AND Terafab milestones confirmed, S+1/T+1/C+1/R+1 = +4 is the strongest signal in today's scorecard. Entry risk: holding through earnings carries gap risk. Prior P004 was closed Apr-19 specifically to avoid this. Decision point for trade-rec: enter before earnings (takes gap risk) or after (misses pre-announcement drift but confirms thesis).

**T-Score Resolution — Key Change:** All 12 residual momentum scores now available for the first time since numpy failure on Apr-19. Notable updates: TSLA residual −9.12% (T=−1, conflict with raw TSMOM: raw +36%, but trust residual — market-beta driven, not idiosyncratic alpha). PLTR residual −35.62% (T=−1; extreme negative idiosyncratic despite positive raw trend = factor crowding warning). AAPL and INTC new promotions.

**Earnings Anomaly (Grade B):** S&P 88% beat rate with +0.2% avg price response (vs +1.0% historical) = "buy the rumor, sell the news" in full effect. Implication: don't size aggressively into pre-announcement drift. Prefer confirmed-beat entries (day-after) for GOOGL, INTC, AMZN.

**BOJ / EWJ:** BOJ rate unchanged 0.75%; JGB purchase reduction continues. USDJPY 158.90 = yen carry intact. EWJ structural S+1 from JPY carry compression; if BOJ pivots (not expected before June), EWJ stop $86 provides buffer. Nikkei +1.21% Apr-21 (fresh print).

---

## Data Quality Summary

| Category | Count | Details |
|----------|-------|---------|
| Grade A variables total | ~25 primary | Per Data Sources.md |
| Grade A MISSING (strict) | **1** | GSCI commodity sleeve gate (V034) |
| Grade A STALE FALLBACK | **4** | Basis-mom WTI/Gold/Silver/Copper (Tier-3, Apr 17, within 5d window) |
| Grade B STALE | 2 | VIX3M (Apr 18, 3d), ETH price (Apr 20, 22h vs 4h window) |
| Audit additions status | V026: LIVE ✓, V027: LIVE ✓, V028: BRENT LIVE / WTI-Copper-Gold-Silver STALE T3 |
| Pipeline health | **OPERATIONAL** |

---

*Source: .data-cache/ (84 files), audit-data-staging-2026-04-21.md (19:48 UTC+8), news-2026-04-21.md, framework/Memory.md (16:22 UTC+8)*
