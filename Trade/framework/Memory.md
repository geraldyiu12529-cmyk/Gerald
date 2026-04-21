# Trade Memory — Working State

**Last updated:** 2026-04-20 17:07 UTC+8 (trade-update sync — 3 new off-methodology entries logged: AAVEUSDT short P006, TSLAUSDT short P007, CLUSDT long P008. All entered 2026-04-20. See §2 for detail.)
**Maintainer:** Gerald
**Local timezone:** UTC+8 (Asia). All scheduled-task cron expressions are evaluated in local time. All brief and trade-rec filenames use local date.

**Clock crosswalk (always write the correct one in the header of any output):**
- 20:00 UTC+8 = 08:00 ET = US pre-open
- 20:10 UTC+8 = 08:10 ET = US pre-open (news capture slot)
- 20:20 UTC+8 = 08:20 ET = US pre-open (trade rec slot)
- 07:30 UTC+8 = 19:30 ET previous day = US post-close (after-hours snapshot)
- 18:00 UTC+8 Sun = 06:00 ET Sun = weekly review slot

This file is the trader's working memory. Keep it operationally current — it should always reflect the latest known state of positions, regime, key variables, and watchlist. Use absolute dates (YYYY-MM-DD).

---

## 1. Asset Universe

**Crypto:** BTC, ETH (+ alt coins as specified per-session)
**Equities:** INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, AVGO, BABA, MSFT
**ETFs / Indices:** QQQ, SPY, EWJ, EWY
**Commodities / Metals:** Brent, WTI, Gold, Silver, Copper, Palladium, Platinum
**FX:** EURUSD, USDJPY

---

## 2. Open Positions

| Asset | Side | Size (USDT) | Entry date (UTC+8) | Entry price | Stop | Catalyst / Invalidation | Thesis |
|-------|------|-------------|---------------------|-------------|------|--------------------------|--------|
| AAVEUSDT (Binance Perp, Cross 1x) | **Short** | 404.85 | 2026-04-20 ≤15:03 | 90.580 | 95.000 | Stop hit | Off-methodology short. No Sum score. P006. |
| TSLAUSDT (Binance Perp, Cross 1x) | **Short** | 394.08 | 2026-04-20 ≤15:03 | 395.560 | 400.000 | TSLA Q1 earnings Apr-22 (catalyst risk for short) | Off-methodology short. No Sum score. P007. |
| CLUSDT (Bybit Perp, Cross 1x) | **Long** | 395.47 | 2026-04-20 ≤17:07 | 88.250 | 85.300 | Stop hit | Off-methodology long. No Sum score. P008. |

**Portfolio heat (est.): ~0.9%** (risk at stops: AAVE ~$19.7 + TSLA ~$4.4 + CL ~$13.2 = ~$37.3 USDT / ~$4,000 NAV). Within 8% cap.
**No methodology circuit breakers active.** All three are off-methodology positions.

---

*§3 (Regime State) and §4 (Key Variables) have been removed. Current regime and variable readings are now maintained exclusively in `master-data-log.xlsx` — see RegimeHistory (latest row) and DailyVariables (latest row). This eliminates dual-maintenance. Skills read from Excel at startup.*

---

## 5. Watchlist / Thesis Candidates

| Asset | Direction | Trigger needed | Invalidation | Notes |
|-------|-----------|----------------|--------------|-------|
| ~~**EWY**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-15~~ | ~~See trade-rec-2026-04-15.md~~ | **EXECUTED 2026-04-15 22:36 → STOPPED 2026-04-16 21:55 UTC+8** at $145.39 via stop-market sell. Realized +$2.75 (+0.92%). Stop was too tight (2.08 units × ~$1.29 = ~$2.68 above entry). See §7 Closed Trades and §8 Lessons. |
| **TSM** | **Long** | C catalyst needed (post-earnings C=0) | Earnings miss on Q2; KOSPI <5800 | **T FLIPPED +1 (residual +21.59%). Sum +2 (S+1/T+1/C0/R0). Q1 BEAT but ADR −3% Apr-16 + another −3.13% Apr-17 = −4.4% cumulative sell-the-news. C=0 post-catalyst. De-prioritized watchlist.** |
| ~~**INTC**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-15 v3~~ | ~~See trade-rec-2026-04-15.md~~ | **EXECUTED 2026-04-16 09:29 UTC+8. CLOSED 2026-04-19 21:31 UTC+8** at $68.26 → +$2.35 (+2.09%). Exited before Apr-23 earnings. See §7. |
| Copper | Long | C catalyst needed (China PMI >50.5) | Trend break; China demand deterioration | Cleanest S+T combo in metals; Sum +2 |
| ~~**Gold**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-16 v2, reaffirmed v3~~ | ~~See trade-rec-2026-04-16.md~~ | **EXECUTED 2026-04-16 22:28 UTC+8. CLOSED 2026-04-18 17:12 UTC+8** at $4,823.65 → +$3.20 (+0.80%). Exited before Apr-22 ceasefire binary. See §7. |
| Silver | Long | 2nd day confirmation of $79+ breakout | Break below $75 | Sum +2 (S+1/T+1/C0/R0); breakout holding $79.915. Basis-mom MISSING — S from static slope only. Brief v2 2026-04-20. |
| WDC | Long | C catalyst needed; T recovery needed (residual mom blocked) | Trend break; earnings miss | Sum +1* (T BLOCKED — residual mom MISSING 2026-04-20). Price $372.52. Prior residual +94.78% but cannot confirm without staging. Brief v2 2026-04-20. |
| Brent | Long | Iran ceasefire binary resolves (Apr-22) — C could flip ±1 | Iran deal confirmed → Brent <$88; or thesis collapse | **Sum +2 (S+1/T0/C0/R+1).** Price $94.83 (up ~5–7% Apr-20 on US Navy seizure of Iranian vessel). Sanctions waiver expired Apr-19 (not renewed). T=0 (1m momentum mixed: recovered from $86 dip but below Mar highs; single-day gap-up ≠ confirmed trend). C=0 (Apr-22 binary: true symmetric — deal = oil −5–10%, no deal = +5–10%; cannot score directional). Basis-mom Brent: +0.95/+2.95 steepening, no divergence cap. Sum +2 → below threshold. Brief v2 2026-04-20. |
| **GOOGL** | **Long** | **Residual momentum recovery needed (T blocked); earnings Apr-22 = C+1** | Earnings miss; trend break; DXY >100; time inv. 2026-05-14 | **Sum +2* (T BLOCKED — residual mom MISSING, numpy failure 2026-04-20). S+1/C+1/R0 = +2 without T. If T recovers = +3 potential. Price $341.68. Earnings Apr-22 after close. Logged SignalLedger N024. Brief v2 2026-04-20.** |
| ~~Oil (WTI)~~ | ~~Long~~ | ~~Separated from Brent~~ | — | WTI Sum = 0 (S0/T0/C−1/R+1 = 0). **Basis-momentum divergence cap FIRES (2026-04-16 staging): static backwardation but 4w −3.71 = flattening → S capped at 0.** Brent-only thesis going forward. |
| **SPY** | **Long** | **|Sum|≥3 — PROMOTION CANDIDATE for trade-rec. FOMC Apr-28-29 timing risk.** | VIX >25; SPY break below 680; FOMC hawkish surprise | **Sum +3 (S+1/T+1/C0/R+1).** Price $710.14, VIX 19.36 / MOVE 65.70. QQQ correlation block LIFTED (QQQ closed Apr-19). C=0 (FOMC Apr-28 = upcoming risk; no favorable catalyst today). R=+1 (HY OAS 2.85%, NFCI −0.47, VIX<20; IC z MISSING). Brief v2 2026-04-20: confirmed active signal. |
| ~~**QQQ**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-16 v3~~ | ~~See trade-rec-2026-04-16.md~~ | **EXECUTED 2026-04-17 00:02 (tranche 1 $639.04) + 00:13 (tranche 2 $641.14) UTC+8. CLOSED 2026-04-19 16:00 UTC+8** at $643.02 → +$4.51 (+1.13%). Exited before Apr-22–23 earnings cluster. See §7. |
| BTC | **Long** | S improved −1→0; T+C building | S re-collapse <400k; funding positive flip | **Sum +2 (S0/T+1/C+1/R0).** Price $75,370 (3rd test $75K support). ActiveAddr 396,267 — CONFIRMED below 400k threshold (S=0 binding). ETF flows $471M Apr-18; $996M weekly (highest since Jan; Grade B). Funding most negative since 2023 = squeeze setup. Logged SignalLedger N032. Below threshold — monitor. Brief v2 2026-04-20. |
| ~~BTC Short~~ | ~~Short~~ | REMOVED 2026-04-14 v5 | — | Out of book. |

---

## 6. Upcoming Catalysts (rolling 2 weeks)

| Date | Event | Assets affected | Expectation |
|------|-------|-----------------|-------------|
| ~~2026-04-15~~ | ~~EIA weekly crude inventories 10:30 ET~~ | ~~Brent, WTI~~ | **OCCURRED — crude −0.9 Mb (vs +0.154 expected), gasoline −1.6 Mb, distillates −3.1 Mb. Across-the-board draws on first blockade week.** |
| ~~2026-04-15~~ | ~~Goldman Sachs BTC ETF filing~~ | ~~BTC~~ | **OCCURRED — +$411.5M ETF inflows** |
| ~~2026-04-16~~ | ~~TSM Q1 earnings (02:00 ET)~~ | ~~TSM, NVDA, QQQ, EWY~~ | **OCCURRED — BEAT on all metrics. But TSM −3% on Apr-16 (sell-the-news confirmed). EWY likely dragged −1% to −2%.** |
| 2026-04-17 | Monthly options expiry; UMich prelim | SPY/QQQ, DXY | **TODAY.** Positioning flush; sentiment read post-tariff-pause |
| 2026-04-16 | Israel-Lebanon 10-day ceasefire begins | Brent, Gold, VIX | Incremental de-escalation signal; Trump announced 5pm ET Apr-16 |
| 2026-04-19 | Iran oil sanctions waiver expires | Brent, WTI, Iran | Escalation risk if not renewed |
| 2026-04-22 | **Iran ceasefire expires** (corrected from Apr-21) | Brent, WTI, Gold, VIX, all | Binary: no date set for next US-Iran talks; Pakistan FM visiting Tehran; 3 nuclear sticking points unresolved |
| 2026-04-24 | UMich final April sentiment (10am ET) | SPY/QQQ, DXY | Prelim was 47.6 record low; 98% surveyed pre-ceasefire — potential partial recovery |
| 2026-04-21 | Advance Retail Sales March | SPY, QQQ, consumer | Demand-side read post-energy shock |
| 2026-04-22 | TSLA Q1 earnings (after close) | TSLA, QQQ | Consensus EPS $0.38, rev $22.6B |
| 2026-04-22 | GOOGL Q1 earnings | GOOGL, QQQ | Ad revenue + cloud; could push Sum to +3 |
| 2026-04-23 | **INTC Q1 earnings (after close)** | **INTC, QQQ** | **Sum = +3 catalyst.** Guided rev $11.7–$12.7B; Terafab validation |
| 2026-04-23 | AMZN earnings | AMZN, QQQ | Retail/cloud read |
| 2026-04-28–29 | FOMC | All | Statement + dots; path repricing risk |
| 2026-04-29 | META earnings | META, QQQ | Same-day as FOMC; ad rev vs GOOGL |
| 2026-05-12 | April CPI release | Rates, DXY, Gold, BTC | Inflation follow-through post-energy shock |
| 2026-05-14–15 | Xi–Trump summit (Beijing) | US-China tariffs, DXY, EWY | Trade deal / "Board of Trade" mechanism; tariff de-escalation potential |

---

## 7. Closed Trades Log

| Asset | Side | Entry / exit dates | Entry / exit price | P&L | Thesis worked? | Lesson |
|-------|------|--------------------|--------------------|-----|----------------|--------|
| **EWY** | Long | Opened 2026-04-15 22:38:58 / Closed 2026-04-16 21:55:12 UTC+8 | $144.10 → $145.39 (avg close) | **+$2.75 realized (+0.92% ROI, 2.08 units)** | Partial — TSM beat validated the AI/semi read-through, but the "sell-the-news" drag on TSM ADR −3% pulled EWY lower intraday and tripped a tight stop before the thesis could play out. Exited in profit by luck of tranche stop-market fill above entry. | **Stop too tight relative to intraday noise post-TSM.** Methodology stop was $133 (2× ATR = ~7.7% below entry). Actual protective stop used was near $145.39, i.e. ~0.9% above entry — effectively a "move-stop-to-break-even" that tripped on normal post-catalyst chop. Lesson: if protective stop is tightened intraday, size to that tighter stop and document the reason, or keep the methodology stop and accept the risk. A 0.9% stop on a Sum+3 equity thesis throws away the edge. |
| **Gold (XAU)** | Long | Opened 2026-04-16 22:41:00 / Closed 2026-04-18 17:12:33 UTC+8 | $4,780.69 → $4,823.65 (avg close) | **+$3.20 realized (+0.80% ROI, 0.083 oz)** | Partial — DXY freefall + real-yield compression thesis was intact; ceasefire binary (Apr-22) had not resolved. Exited 4 days before the primary catalyst event. | Exited before the catalyst that the position was sized for. Stop at $4,640 had 5.4% buffer; thesis unbroken. Off-methodology decisions drove early exit. |
| **QQQ** | Long | Opened 2026-04-17 00:02–00:13 / Closed 2026-04-19 16:00:05 UTC+8 | $640.09 avg → $643.02 (avg close) | **+$4.51 realized (+1.13% ROI, 0.62 units combined)** | Partial — vol compression + AI capex cycle thesis intact; earnings cluster (GOOGL/TSLA Apr-22, INTC Apr-23) had not occurred. Exited 3 days before the catalyst week. | Exited before GOOGL/TSLA/INTC earnings cluster that was the primary Sum +4 thesis catalyst. Stop at $600 had 7.5% buffer. |
| **INTC** | Long | Opened 2026-04-16 09:29:59 / Closed 2026-04-19 21:31:55 UTC+8 | $67.8701 (Binance INTCUSDT) → $68.26 | **+$2.35 realized (+2.09% ROI, Isolated 4x)** | Partial — Terafab/foundry structural thesis intact; Q1 earnings Apr-23 (confirmation catalyst) had not occurred. | Exited 4 days before the earnings confirmation event. Note: Memory.md entry logged $64.68 (rec model price); Binance fill was $67.8701 — entry-price discrepancy flagged for methodology audit. |
| **Off-methodology batch** | Mixed | 2026-04-13 to 2026-04-20 UTC+8 | Various | **Net approx. −$14 to −$20 USDT** (13 positions: BTCUSDT×2, CLUSDT×2, BZUSDT×2, XAGUSDT, TSLAUSDT, AAVEUSDT×2, INTCUSDT×1 repeat-entry) | No — none were methodology-scored. No documented invalidations, no ATR stops, many held <24h. | Off-methodology activity is generating the bulk of session losses. All profitable positions in this batch are the methodology-tracked ones. |

---

## 8. Lessons & Corrections

*Moved to `/mnt/Trade/framework/memory-lessons.md` to keep daily startup reads lean. Read that file for the full lesson log. The weekly-regime-review task writes new condensed entries directly to `framework/memory-lessons.md`.*

## 9. Outstanding Research Questions

- BTC funding / open-interest / liquidation as standalone directional signal — evidence is thinner than practitioner usage implies. Treat as crowding filter, not return predictor.
- MVRV / SOPR / HODL waves — regime-context only until more peer-reviewed return-timing evidence exists.
- Post-ETF BTC factor stability — older BTC studies may be sample-specific; monitor whether momentum/attention signals decay in the institutional era.
- **Grade A data gaps still open as of 2026-04-14 v5 (fail-loud):**
  - ACM term premium 10Y (NY Fed) — Apr-2026 monthly not yet posted; latest is Jan-2026 ~0.59%
  - BTC 3m basis (Deribit) — search inconclusive; blocks crypto basis/crowding confirmation
  - *(Closed 2026-04-14 v4/v5: DGS2 3.77%, DGS10 4.359%, DFII10 1.90%, Brent M1–M3 deep backwardation, BTC funding negative Binance, BTC active addresses 619k→364k, META $630.49, EURUSD ~1.1769)*
- ~~Watchlist reconciliation pending: BTC short thesis contradicted by today's tape.~~ **RESOLVED 2026-04-14 v5:** BTC short formally removed from watchlist (funding negative + netflow outflow + price reclaim invalidate short; S−1 address collapse blocks long).
- BTC flow-signal reconciliation (new 2026-04-14 v7): news-2026-04-14 reports Apr-13 US spot BTC ETFs net outflow −$325.8M (Grade B) vs. Apr-09/10 exchange netflow −7,900 BTC (Grade A, bullish). These two flow reads point opposite directions; weight Grade A exchange-netflow but watch whether the ETF outflow extends into a streak over the next 2–3 sessions — a multi-day ETF outflow streak with negative funding would strengthen a fresh short-direction case if S were to flip via address recovery.
- **2026-04-14 audit-addition gaps — ALL CLOSED 2026-04-15:**
  - ~~Intermediary capital ratio~~ → **CLOSED** z = +1.86 (ratio 0.140, above 3y mean 0.129); R adjustment = +0; resolved EWY fail-loud caveat
  - ~~Residual momentum~~ → **CLOSED** all 12 near 0.00% (approximate, 10m window); T = 0 for all single stocks; T-block lifted but no promotions
  - ~~Basis-momentum~~ → **CLOSED** 5/5 computed; WTI/Gold divergence cap fires (S capped at 0); Brent/Silver/Copper steepening (no cap)
- **Six-month live-monitoring review for 2026-04-14 audit additions due 2026-10-14.** Criteria: demote to Grade B if no decision-moving contribution observed across any scored asset in the live monitoring window. A one-time scheduled task (`methodology-audit-6mo-review-2026-10-14`) will fire on that date to run the review.
- **2026-04-15 quarterly review surfaced:** Top-25 variables #6-8 (equity valuation spread, revision breadth, profitability) and #16-20, #23-25 (FX PPP, order flow, skew, VRP, supply, buyback, insider) are not systematically scored in the pipeline — they inform narrative judgment only. This is acceptable for a discretionary framework but creates reconciliation gaps. Monitor whether the Q3 review can link any of these to signal outcomes.
- **Quarterly methodology review skill created 2026-04-15.** Meta-review running one level above the weekly signal review: audits analytical dimension fitness (RETAIN/DEMOTE/RETIRE/PROMOTE), reconciles research cores vs OOS evidence, manages variable candidate pipeline (GEX, lead-lag, correlation-regime, decision tree, calendar). Scheduled task `quarterly-methodology-review` fires 1st of Jan/Apr/Jul/Oct at 19:00 UTC+8. First run 2026-07-01. The Q4 review (2026-10-01) must include formal GO/NO-GO for the three audit-addition variables ahead of the 2026-10-14 deadline.
- **2026-04-17 literature review (news-events taxonomy, scope-limited) surfaced 5 deferred variable candidates for future quarterly review consideration (NOT promoted, per scope directive):**
  1. **Daily GPR (Caldara-Iacoviello Fed IFDP)** — Grade B regime-input candidate; paper has index coverage, real-time implementable. Defer until quarterly review.
  2. **Executive-order density per week** — policy-uncertainty proxy under high-EO cadence regime; needs sample before promotion consideration.
  3. **LLM-based sentiment (vs Loughran-McDonald dictionary)** — requires NLP infrastructure; defer indefinitely until infra choice.
  4. **BTC-ETF-flow direction as formal T-input for BTC** — currently treated as crowding filter; post-ETF institutional sample may now justify reclassification. Quarterly review can assess.
  5. **Caldara-Iacoviello TPU (trade-policy uncertainty) subindex** — dedicated policy-uncertainty read separable from geopolitics; reviewable against Baker-Bloom-Davis EPU overlap.
- **2026-04-17 literature review also identified news-events/market-brief jobscope overlap** — three HIGH-severity gaps (calendar double-count, data-release double-count, political-communication filter absent). Proposed diffs to news-events/README.md and news-events/SKILL.md drafted with "Gerald sign-off PENDING" — no production edits applied. File: `literature-review-2026-04-17-news-events.md`. Next full-scope (including variable promotion) literature review: ~2026-10-17.

*§10 (Audit-addition Contribution Log) has been removed. All audit-addition contribution tracking is now maintained exclusively in the `AuditAdditionLog` sheet of `master-data-log.xlsx`. The 2026-10-14 review reads from Excel. Historical entries (2026-04-15 through removal date) were migrated to Excel before deletion.*
