# Trade Recommendations -- 2026-04-20 (19:00 UTC+8) -- Cloud Edition

**Run type:** Cloud scheduled task
**Upstream files:** market-brief-2026-04-20.md + news-2026-04-20.md (both FOUND)
**Prior delta-check:** NO prior trade-rec found on Drive -- first cloud run


---

## 1. Upstream Synthesis

1. **market-brief [Regime]** -- Regime flipped from RISK-OFF/GEOPOLITICAL-CRISIS to RISK-ON/GEOPOLITICAL-FRAGILE on Apr 7 ceasefire; S&P at ATH (7,126), NDX at ATH (24,468), VIX 17.48 -- ceasefire described as "fragile."

2. **market-brief [FX]** -- DXY below 98 for 3rd consecutive weekly decline; EURUSD ~1.1765 (Apr 19 close, updated via web search); USDJPY ~159.06 -- near MoF intervention threshold; dollar structural weakness (Grade A) is core scoring driver for EURUSD.

3. **market-brief [Equity Scorecard]** -- 8 equity/ETF assets at |Sum|=3(T): NVDA, AAPL, AMZN, META, TSM, PLTR, SPY, QQQ -- all blocked by residual momentum MISSING (cloud staging). No equity position actionable today.

4. **market-brief [Data Quality]** -- Grade A MISSING: 5 variables (MOVE, VIX3M, IC z-score, BTC Active Addresses, BTC Hash Rate); Infrastructure MISSING: 2 (Residual Momentum, Basis-Momentum). All equity T-scores blocked.

5. **news [Geopolitics -- FLASH]** -- Strait of Hormuz open during truce Apr 20: crude -9.41% to $82.59, S&P +1.2%. Counter-signal: US Navy seized Iranian cargo ship Apr 19 -- ceasefire fragility confirmed in real time.

6. **news [Central Banks]** -- Fed on hold (3.50-3.75%), 1 cut median dot for 2026, timing H2. ECB considering 2 rate hikes on energy-driven inflation. BoJ on hold until June, then hike expected. Fed/ECB divergence = structural EUR tailwind.

7. **news [Earnings Pipeline]** -- TSLA + GOOGL Apr 22; INTC Apr 23; AAPL/AMZN/META Apr 29; NVDA May 20. AI capex scrutiny high -- "not yielding bottom-line results." C-scores for individual equities supported where earnings catalyst imminent.

8. **news [Crypto]** -- BTC $75,255 at 3rd test of $75K support; Fear & Greed 27; ETF outflows -$325.8M Apr 13; BTC/equity divergence widening. SEC-CFTC commodity classification = structural positive but not near-term score driver.

9. **Conflict: Oil narrative** -- News shows crude -9.41% on Hormuz opening (bearish oil); OPEC+ 206 kb/d cut effective May 1 (medium-term bullish oil). Resolution: short-term bearish on supply normalization outweighs medium-term cut -- Brent/WTI C=-1 appropriate today.

10. **Prior delta-check:** No prior trade-rec found on Drive -- first cloud run. Baseline = fresh.


---

## 2. Regime Read

**Label:** `RISK-ON / GEOPOLITICAL-FRAGILE`

| Watch Variable | Reading | Grade | Signal |
|---|---|---|---|
| VIX | 17.48 (Apr 17 close) | A | Below 20 threshold; equity bull intact; >20 = regime flip trigger |
| WTI | ~$82.59 (today -9.42%) | A | Hormuz normalization in progress; <$95 = benign; >$100 = RISK-OFF flip |
| BTC $75K support | $75,255 (Apr 19, -1.81%) | A | 3rd test -- hold = floor; break = $71.2K next level |

**Escalation flags:**
- Ceasefire crack signal: 10Y +2bp Monday pre-market on renewed US-Iran tensions (cargo seizure)
- 10-day window: ceasefire monitoring through ~2026-04-30
- No circuit breaker triggered (VIX <20, WTI <$100)


---

## 3. Recommendations Table

| Asset | Direction | Entry | Stop | Target | Size | Catalyst | Grade | Correlation | Risk-rule |
|---|---|---|---|---|---|---|---|---|---|
| EURUSD | LONG | ~1.1765 | 1.1670 | 1.2000 | 2% | ECB hawkish lean (2 hikes unpriced); USD safe-haven premium unwinding on Hormuz open; DXY structural weakness 3-wk decline | S=+1(A), T=N/A, C=+1, R=+1* | Standalone; no equity conflicts (all T-blocked) | <=2% position; post-entry heat 2% <= 8% |

*R=+1 conditional: IC z-score MISSING -- see Data Gaps. Observable proxies (HY OAS 2.85%, NFCI -0.47, VIX 17.48) all consistent with non-stressed intermediary conditions.


---

## 4. Theses Not Taken (|Sum|=2 near-misses)

**Gold (Sum=2):** S=+1 (safe-haven structural, A grade); C=0 (Hormuz open partially unwinds geopolitical premium, offset by dollar weakness); R=+1. C would need to flip to +1 to promote. Trigger: ceasefire breakdown => safe-haven flight => C=+1 => promote to outright long. No targeted search can close this gap today (C=0 is regime-dependent, not data-gap).

**Silver (Sum=2):** S=+1 (industrial+precious dual demand); C=0 (no scheduled catalyst); R=+1. Trigger: industrial data surprise or Gold breakout pulls Silver along. Monitor.

**Copper (Sum=2):** S=+1 (China recovery, industrial demand); C=0 (no specific catalyst); R=+1. Trigger: China PMI beat or fiscal stimulus announcement => C=+1.

**EWJ (Sum=2, T-blocked):** S=+1 (USDJPY 159 = export tailwind); C=0 (no specific near-term catalyst); R=+1. T-blocked (residual momentum MISSING). Promotion requires: T resolved + C catalyst identified.

**Equities/ETFs (Sum=3(T) blocked):** NVDA, AAPL, AMZN, META, TSM, PLTR, SPY, QQQ -- all pass S/C/R checks but T leg blocked by residual momentum MISSING in cloud staging. Promotion: restore staging file in local run.


---

## 5. Relative-Value Pairs

Regime is directionally mixed: equities at ATH (risk-on) while crude -9.4% (commodity bust), BTC in fear (crypto cautious). No clean outright regime for RV pair construction today.

Potential pair on resolution: **Long EURUSD / monitor USDJPY short** -- both are USD-weakness expressions but with different mechanics (EUR: ECB/Fed divergence; JPY: BoJ intervention risk). Not structured as a pair trade due to MoF intervention making USDJPY timing uncertain. Flag for monitoring if USDJPY stays >158 post 2026-04-20.


---

## 6. Data Gaps

**(a) Upstream artifact coverage:**
- market-brief-2026-04-20.md: FOUND (created 2026-04-20T10:40:43Z)
- news-2026-04-20.md: FOUND (created 2026-04-20T11:00:51Z)
- Prior trade rec: NOT FOUND on Drive -- first cloud run; no delta-check available

**(b) Audit-addition MISSING (2026-04-14 review visibility):**
- **Equity T -- Residual Momentum: MISSING** -- cloud run, no staging file. All 8 equity/ETF |Sum|>=3 assets blocked. Fail-loud: no equity position taken.
- **Commodity S -- Basis-Momentum: MISSING** -- cloud run, no staging file. Divergence-cap not applied to Brent/WTI.
- **Cross-asset R -- Intermediary Capital z-score: MISSING** -- NY Fed PD data not web-accessible; confirmed Apr 20 2026 search. Fail-loud: R=+1 for EURUSD is conditional on IC not being stressed. Observable proxies (HY OAS 2.85%, NFCI -0.47, VIX 17.48) all non-stressed -- downgrade risk assessed as low but not confirmed.

**(c) Other Grade-A MISSING:**
- VIX3M: no public source confirmed
- MOVE (bond vol): no specific Apr 17/20 value retrieved
- BTC Active Addresses: BitInfoCharts/CryptoQuant not web-accessible
- BTC Hash Rate: no specific value retrieved


---

## 7. Pre-Entry Checklist (EURUSD Long)

1. **|Sum| >= 3 with C scored:** PASS -- Sum=3; C=+1 (Hormuz USD unwind + ECB hawkish divergence). Note: IC z-score MISSING => R=+1 conditional.

2. **Invalidation -- concrete, date-bounded:**
 - Price: EURUSD breaks below 1.1670 (stop; ~95 pips = 1.5x ATR)
 - Fundamental: ceasefire collapses (US-Iran cargo seizure escalates) => USD safe-haven bid => EURUSD reversal
 - Date-bound: Ceasefire 10-day window through ~2026-04-30; full reassessment if WTI reclaims $100
 - PASS

3. **Correlation gate:** EURUSD standalone FX trade; all equity positions T-blocked (no entry); no shared regime variable creating double-exposure. PASS

4. **Per-position risk <= 2% / portfolio heat <= 8%:** No open positions (Memory.md confirmed). New EURUSD = 2% max. Post-entry heat: 2% <= 8%. PASS

5. **ATR stop set:** Entry ~1.1765; Daily ATR ~65 pips (elevated, macro news flow). Stop: 1.1670 (~95 pips = 1.5x ATR). Target: 1.2000 (round number resistance). R:R ~1:2.5. PASS

6. **Catalyst asymmetry:**
 - Downside tail: US-Iran cargo seizure (Apr 19 announced) => ceasefire fragility => USD safe-haven bid (partially priced in)
 - Upside surprise: ECB 2 hike scenario (not fully priced) -- EUR structural appreciation; DXY 3 weekly declines = trend confirmation
 - Net: Asymmetric to upside. ECB/Fed divergence is structural and multi-week; ceasefire tail risk is event-specific and shorter-dated. PASS

**All 6 checklist items: PASS (with IC z-score MISSING noted as conditional risk).**


---

**Sources: market-brief-2026-04-20.md (Google Drive), news-2026-04-20.md (Google Drive), TradingEconomics, Chicago Fed/FRED, BlockchainMagazine, CNBC, NY Fed PD Statistics (searched; no specific Apr 2026 IC z-score found), poundsterlinglive.com (EURUSD Apr 19: 1.1765).**
