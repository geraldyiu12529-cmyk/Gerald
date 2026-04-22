# Trade Memory — Working State

**Last updated:** 2026-04-22 11:05 UTC+8 (trade-update: P009 SPY T5 added 699.45 USDT @ 706.51 (05:04 UTC+8); P010 EWJ T3 added 199.25 USDT @ 87.39 (05:07 UTC+8). Dip-buy adds, Asian session.)
**Maintainer:** Gerald
**Local timezone:** UTC+8 (Asia). All scheduled-task cron expressions are evaluated in local time. All brief and trade-rec filenames use local date.
**HTML Report Generator:** `scripts/gen_trade_rec_html.py` — canonical format locked 2026-04-21. Update `PER-RUN DATA` block and run `python scripts/gen_trade_rec_html.py`. Do not write HTML manually. Sections (in order): Data Freshness · Asset Universe · Delta · Exec Summary · Overlay Gate · Key Variables + V026 Full Table · Score Charts · Factor Exposure · Recommendations (Catalyst/Grade/Sleeve cols) · Signal Age · Checklists · Regime Sensitivity · Catalyst Cal · Closed-Trade Context · Near-Misses · Positions · Data Gap · Discussion.

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
| SPYUSDT (Bybit Perp) | **Long** | 2,089.08 | 2026-04-21 21:43 – 2026-04-22 05:05 | 708.95 (avg, 5 tranches) | 696.00 | VIX >25; SPY break $696; HY OAS >4.50%; FOMC Apr-28 hawkish → exit if SPY <$700; time-stop 2026-05-13 | Sum+3 (S+1/T+1/C0/R+1). Half-size 1.0% risk. V027 z+1.65 confirmed. T5 added 2026-04-22 05:05 @ 706.51. P009. |
| EWJUSDT (Bybit Perp) | **Long** | 1,396.05 | 2026-04-21 21:47 – 2026-04-22 05:08 | 88.30 (avg, 3 tranches) | 86.00 | USDJPY <150; Nikkei −5%; BOJ emergency ≥50bp; US-China escalation; time-stop 2026-06-30 | Sum+3 (S+1/T+1/C0/R+1). 0.75% risk (corr haircut vs SPY). Raw TSMOM. T3 added 2026-04-22 05:08 @ 87.39. P010. |

**Portfolio heat (est.): ~1.86%** (P009 SPY ~$38.2 + P010 EWJ ~$36.4 = ~$74.6 USDT at risk / ~$4,000 NAV). Within 8% cap.
**No methodology circuit breakers active.** P009/P010 are methodology-promoted.

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
| Silver | Long | Commodity sleeve gate must confirm ON at local 20:20 brief | Break below $75 | **Sum +3 (S+1/T+1/C0/R+1) — GATE-BLOCKED (P012, Taken=NO, OverlayGateOff tentative).** Commodity sleeve OFF in cloud brief (GSCI MISSING). Basis-mom MISSING for Silver — S from static slope only. If local 20:20 confirms commodity sleeve ON → re-enters pre-entry checklist. Cloud-7pm rec 2026-04-21. |
| WDC | Long | C catalyst needed; T recovery needed (residual mom blocked) | Trend break; earnings miss | Sum +1* (T BLOCKED — residual mom MISSING 2026-04-20). Price $372.52. Prior residual +94.78% but cannot confirm without staging. Brief v2 2026-04-20. |
| Brent | Long | Iran ceasefire binary resolves (Apr-22) — C could flip ±1 | Iran deal confirmed → Brent <$88; or thesis collapse | **Sum +2 (S+1/T0/C0/R+1).** Price $94.83 (up ~5–7% Apr-20 on US Navy seizure of Iranian vessel). Sanctions waiver expired Apr-19 (not renewed). T=0 (1m momentum mixed: recovered from $86 dip but below Mar highs; single-day gap-up ≠ confirmed trend). C=0 (Apr-22 binary: true symmetric — deal = oil −5–10%, no deal = +5–10%; cannot score directional). Basis-mom Brent: +0.95/+2.95 steepening, no divergence cap. Sum +2 → below threshold. Brief v2 2026-04-20. |
| **GOOGL** | **Long** | **PROMOTED P015 — entry after Apr-23 UTC+8 beat confirmation (~$333–340 limit)** | Earnings miss → C drops → Sum <3 → no entry; break below 2× ATR from entry; time-stop 2026-05-15 | **Sum +3 confirmed (S+1/T=0/C+1/R+1). T resolved to 0 (residual −0.80%, within ±2% range). C+1 scored pre-earnings (88% Q1 beat rate + Mag7 +22.8% bar). Earnings tonight Apr-23 01:00 UTC+8. Entry after beat confirmation — do not chase gap. Size 0.75%. ATR stop ~$317 (2× ATR ~$9 from ~$335 entry). Target $355/$375. Logged P015. Local trade-rec-2026-04-21 v2.** |
| ~~Oil (WTI)~~ | ~~Long~~ | ~~Separated from Brent~~ | — | WTI Sum = 0 (S0/T0/C−1/R+1 = 0). **Basis-momentum divergence cap FIRES (2026-04-16 staging): static backwardation but 4w −3.71 = flattening → S capped at 0.** Brent-only thesis going forward. |
| ~~**SPY**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-20 v3, re-confirmed 2026-04-21 v2 local~~ | ~~VIX >25; SPY break $696; HY OAS >4.50%~~ | **EXECUTED 2026-04-21 21:43–22:14 UTC+8.** Avg fill 710.17 (4 tranches: 709.70/709.56/710.93/710.90). Total 1,391.96 USDT. Stop 696.00. See Open Positions P009. |
| ~~**EWJ**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-21 v2 local (P010)~~ | ~~USDJPY <150; Nikkei −5%; BOJ emergency ≥50bp~~ | **EXECUTED 2026-04-21 21:47–22:13 UTC+8.** Avg fill 88.44 (2 tranches: 88.48 market/88.39 market). Total 1,198.57 USDT. Entry ~2% below rec estimate 90.24. Stop 86.00. See Open Positions P010. |
| **INTC** | **Long** | **PROMOTED P013 — entry after Apr-23 AC beat confirmed (~$68–72 limit, Apr-24 UTC+8 morning)** | Q1 miss / Terafab milestone miss → C=0/−1 → exit thesis; break below ATR stop; time-stop 2026-06-23 | **Sum +4 (S+1/T+1/C+1/R+1). V026 residual +13.89% (A) — T=+1 resolved.** Earnings Apr-23 AC. C+1 for Terafab foundry validation. Size 1.0% (full — V027 z +1.65 = capital expansion regime). ATR stop 2× ATR ~$5 below entry. Target $75/$82. Prior P004 closed Apr-19 before earnings; this is a confirmed-beat re-entry strategy. Logged P013. Local trade-rec-2026-04-21 v2. |
| **AAPL** | **Long** | **PROMOTED P014 — entry now (~$271–274 limit or at-market)** | Break below $264 (2× ATR ~$6.50); SPY break $696; FOMC Apr-28 hawkish; hard exit 2026-04-30 before May 1 earnings | **Sum +3 (S+1/T+1/C=0/R+1). V026 residual +4.68% (A) — T=+1 resolved.** C=0 (no near-term catalyst; edge is structural momentum). Size 0.75% (correlation haircut vs SPY). Time-stop 2026-04-30 binding — MUST exit before May 1 earnings binary. ATR stop ~$266.50. Target $280/$290. Logged P014. Local trade-rec-2026-04-21 v2. |
| ~~**QQQ**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-16 v3~~ | ~~See trade-rec-2026-04-16.md~~ | **EXECUTED 2026-04-17 00:02 (tranche 1 $639.04) + 00:13 (tranche 2 $641.14) UTC+8. CLOSED 2026-04-19 16:00 UTC+8** at $643.02 → +$4.51 (+1.13%). Exited before Apr-22–23 earnings cluster. See §7. |
| BTC | **Long** | S improved −1→0; T+C building | S re-collapse <400k; funding positive flip | **Sum +2 (S0/T+1/C+1/R0).** Price $76,454 (4th test $75K support). ActiveAddr 396,267 — CONFIRMED below 400k threshold (S=0 binding). ETF flows +$412M Apr-21 (B). Funding most negative since 2023 = squeeze setup. KelpDAO exploit $292M Apr-20 = DeFi tail (contained; BTC/ETH bid intact). Crypto sleeve OFF. Logged N032. Brief local v1 2026-04-21. |
| MU | Long | Correlation gate clears (post-Apr-23 week); C=0 (June earnings) | Trend break; DRAM cycle reversal | **Sum +3 (S+1/T+1/C0/R+1). V026 residual +15.63% (A).** T=+1 resolved. Size: deferred to post-FOMC (Apr-30+) — equity sleeve at capacity during Apr-22–29 earnings cluster. Logged N036 near-miss. Local trade-rec-2026-04-21 v2. |
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
| 2026-04-22 | **Iran ceasefire EXPIRED Apr-21 UTC+8. Talks in Pakistan; Iran non-participating. Hormuz <10% traffic.** | Brent, WTI, Gold, VIX, ALL | WTI $86.32, Brent $90.03. Deal → oil −10–15%; no deal → oil +10–15%. P008 stop buffer thin ($1.02 above $85.30). |
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
| **CLUSDT P008** | Long | Opened 2026-04-20 16:20 / Closed 2026-04-21 23:10 UTC+8 | 88.250 → 88.52 (avg close) | **+$0.79 realized (+0.19% ROI, 4.53 CL)** | N/A — off-methodology (no Sum score) | Off-methodology long, discretionary close 1 day after entry. Small profit; exit tactical as P009/P010 now open. |
| **AAVEUSDT P006** | Short | Opened 2026-04-20 04:27:37 / Closed 2026-04-21 16:22:10 UTC+8 | 90.580 → 93.035 | **−$11.15 realized (−2.79% ROI, ~4.4 AAVE)** | No — off-methodology short. Price moved against the short. Thesis was undocumented. | Off-methodology short held ~36h against rising AAVE price. Stop at 95.000 was never hit — discretionary close. Loss exceeds the prior methodology session gain. |
| **TSLAUSDT P007** | Short | Opened 2026-04-20 08:08:45 / Closed 2026-04-20 20:49:22 UTC+8 | 395.560 → 400.045 | **−$4.60 realized (−1.17% ROI, ~0.99 TSLA)** | No — off-methodology short. Closed before TSLA earnings Apr-22 binary. | Closed same day, discretionary exit before earnings. Stop at 400.000 was within 1.12% — extremely tight on a volatile stock into earnings. Correct to close before the Apr-22 binary catalyst. |
| **Off-methodology batch** | Mixed | 2026-04-13 to 2026-04-20 UTC+8 | Various | **Net approx. −$22 USDT** (batch: BTCUSDT Long −$6.43, INTCUSDT Long −$3.01, XAGUSDT Short −$6.19, TSLAUSDT Short −$2.92, AAVEUSDT Long −$4.22, AAVEUSDT Short −$0.51, BZUSDT Short +$0.50) | No — none were methodology-scored. No documented invalidations, no ATR stops, many held <24h. | Off-methodology activity is generating the bulk of session losses. All profitable closed positions in this session are methodology-tracked ones. |

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
