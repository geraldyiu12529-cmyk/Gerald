# Trade Memory — Working State

**Last updated:** 2026-04-17 23:30 UTC+8 (trade-rec v1 — **no new entries**. All |Sum|≥3 candidates either open (INTC/Gold/QQQ) or correlation-blocked (SPY by QQQ). 10 near-misses logged to SignalLedger (GOOGL +2 T-block via residual, EWY +2 C, AMZN/META/NVDA T-block via residual, MU/WDC/Silver/Copper C-block, Brent +2 C-negative, BTC +2 upgraded S 0, PYPL −2 short). Residual momentum = today's decision-moving audit variable. Marks carry forward: INTC +8.10%, Gold +2.45%, QQQ +1.41%.)
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
**Equities:** INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC
**ETFs / Indices:** QQQ, SPY, EWJ, EWY
**Commodities / Metals:** Brent, WTI, Gold, Silver, Copper, Palladium, Platinum

---

## 2. Open Positions

| Asset | Side | Size | Entry date | Entry price | Stop / invalidation | Catalyst | Thesis (1 line) |
|-------|------|------|------------|-------------|---------------------|----------|------------------|
| **INTC** | Long | $49.78 USDT (~0.77 units @ $64.68) | 2026-04-16 09:29 UTC+8 | $64.68 (market fill) | $56 (2× ATR); earnings miss / Terafab delay / trend break <$55; time inv. 2026-05-13 | Q1 earnings 2026-04-23 (confirmation-dependent) | Terafab/foundry structural + residual +13.89% (confirmed 2026-04-17 staging v3, T=+1). **Sum +3 CONFIRMED.** **Current mark $69.92 (+8.10%, PNL +$4.03).** |
| **Gold (XAU)** | Long | $396.80 USDT (~0.0830 oz @ $4,780.69) | 2026-04-16 22:28 UTC+8 | $4,780.69 (trailing buy triggered ≤$4,798.34, 0.1% callback) | $4,640 (break <$4,640); DXY reversal >100; real yield spike >2.2%; time inv. 2026-05-14 | Iran ceasefire expiry Apr-21/22 (C+1 surprise-dependent) | DXY freefall + real-yield compression + contango deepening + oil crash boosts safe-haven bid. Sum +3 (S+1/T+1/C+1/R0). **Current mark $4,897.90 (+2.45%, PNL +$9.72).** |
| **QQQ** | Long | $396.85 USDT combined (tranche 1: $198.10 @ $639.04 trailing buy fill 2026-04-17 00:02; tranche 2: $198.75 @ $641.14 limit fill 2026-04-17 00:13) | 2026-04-17 00:02–00:13 UTC+8 | Avg ~$640.09 | Break below $600; VIX >25; time inv. 2026-05-14 | FOMC Apr-28–29; big tech earnings (GOOGL Apr-22, TSLA Apr-22, INTC Apr-23, AMZN Apr-23, META Apr-29) | Strongest NEW |Sum|≥3 signal — Sum +4. TSM AI validation + records + vol compression. **Current mark $649.13 (+1.41%, PNL +$5.60).** |

**Portfolio heat (recomputed v3):**
- INTC: $49.78 × (($69.92 − $56) / $69.92) ≈ $9.91 = 0.25% of $4,000
- Gold: $396.80 × (($4,897.90 − $4,640) / $4,897.90) ≈ $20.89 = 0.52% of $4,000
- QQQ: $396.85 × (($649.13 − $600) / $649.13) ≈ $30.04 = 0.75% of $4,000
- **Combined heat: ~1.52%.** Well within 8% cap. Equity correlation gate: INTC + QQQ combined ≈ 1.00% equity heat — within budget.

---

*§3 (Regime State) and §4 (Key Variables) have been removed. Current regime and variable readings are now maintained exclusively in `master-data-log.xlsx` — see RegimeHistory (latest row) and DailyVariables (latest row). This eliminates dual-maintenance. Skills read from Excel at startup.*

---

## 5. Watchlist / Thesis Candidates

| Asset | Direction | Trigger needed | Invalidation | Notes |
|-------|-----------|----------------|--------------|-------|
| ~~**EWY**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-15~~ | ~~See trade-rec-2026-04-15.md~~ | **EXECUTED 2026-04-15 22:36 → STOPPED 2026-04-16 21:55 UTC+8** at $145.39 via stop-market sell. Realized +$2.75 (+0.92%). Stop was too tight (2.08 units × ~$1.29 = ~$2.68 above entry). See §7 Closed Trades and §8 Lessons. |
| **TSM** | **Long** | C catalyst needed (post-earnings C=0) | Earnings miss on Q2; KOSPI <5800 | **T FLIPPED +1 (residual +21.59%). Sum +2 (S+1/T+1/C0/R0). Q1 BEAT but ADR −3% Apr-16 + another −3.13% Apr-17 = −4.4% cumulative sell-the-news. C=0 post-catalyst. De-prioritized watchlist.** |
| ~~**INTC**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-15 v3~~ | ~~See trade-rec-2026-04-15.md~~ | **EXECUTED 2026-04-16 09:29 UTC+8.** Market fill $64.68, $49.81 USDT (reduced size — price above entry zone). Now in §2 Open Positions. Earnings Apr-23. |
| Copper | Long | C catalyst needed (China PMI >50.5) | Trend break; China demand deterioration | Cleanest S+T combo in metals; Sum +2 |
| ~~**Gold**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-16 v2, reaffirmed v3~~ | ~~See trade-rec-2026-04-16.md~~ | **EXECUTED 2026-04-16 22:28 UTC+8.** Trailing buy filled $4,780.69, $396.80 USDT. Now in §2 Open Positions. Note: filled BELOW stated entry zone $4,800–$4,860 — trailing stop caught the dip, favorable entry. |
| Silver | Long | 2nd day confirmation of $79+ breakout | Break below $75 | Sum +2; breakout holding $79.67 |
| WDC | Long | C catalyst needed | Trend break; earnings miss | Sum +2 (S+1/T+1/C0/R0); residual +94.78% T=+1 (confirmed 2026-04-16 staging); post-earnings drift |
| Brent | Long | Iran talks collapse → C flips to +1 | Iran deal confirmed; Brent <$93 | **CAUTIONARY.** Sum +2 (S+1/T+1/C−1/R+1) but catalyst convexity against the thesis. Brent $86.65 (−9.67% intraday). **$5-of-$9 may be contract-roll artifact** in deeply backwardated market; genuine move ~−4% not trend-breaking. If US close confirms $86 print, T downgrades to 0 → Sum +1. Apr-19 Iran sanctions waiver expiry + Apr-21 ceasefire are the binary catalysts, both scored bearish-risk for oil longs. |
| **GOOGL** | **Long** | **DOWNGRADED to Sum +2 (v3 brief, confirmed rec v1 2026-04-17)** | Earnings miss; trend break; DXY >100; time inv. 2026-05-14 | **Sum +2 (S+1/T0/C+1/R0). Residual −0.80% → T=0 (near-zero; raw +64.84% entirely factor-driven). Downgraded from +3 ref. Earnings Apr-22 = C+1 but Sum ceiling is +2 without T. Price $336.90. Logged SignalLedger N024 (audit-addition decision-moving block). No longer |Sum|≥3 candidate.** |
| ~~Oil (WTI)~~ | ~~Long~~ | ~~Separated from Brent~~ | — | WTI Sum = 0 (S0/T0/C−1/R+1 = 0). **Basis-momentum divergence cap FIRES (2026-04-16 staging): static backwardation but 4w −3.71 = flattening → S capped at 0.** Brent-only thesis going forward. |
| **SPY** | **Long** | **|Sum|≥3 signal continuing — CORRELATION-BLOCKED (rec v1 2026-04-17)** | VIX >25; SPY break below 680 | **Sum +3 (S+1/T+1/C0/R+1).** Fresh record $710.82, VIX 17.92 / MOVE 65.89 vol compression deepening 3rd signal. FOMC Apr-28 risk. **Correlation-blocked by open QQQ per Risk Rules §5 (shares primary regime variable; QQQ is concentrated proxy already held). Not promotable independently.** |
| ~~**QQQ**~~ | ~~**Long**~~ | ~~PROMOTED 2026-04-16 v3~~ | ~~See trade-rec-2026-04-16.md~~ | **EXECUTED 2026-04-17 00:02 (tranche 1 $639.04) + 00:13 (tranche 2 $641.14) UTC+8.** Total ~$396.85 USDT, avg $640.09. Now in §2 Open Positions. |
| BTC | **Long** | S improved −1→0; T+C building | S re-collapse <400k; funding positive flip | **Sum +2 (S0/T+1/C+1/R0).** $77,775 (+2.70%). ETF flow alternating: +$411M Apr-14, +$186M Apr-15, **−$291M Apr-16 (reversal per close snapshot)**. Funding most negative since 2023 = squeeze setup. Address STALE-WARN 470k. Upgraded from Sum +1 on price/flow momentum. Logged SignalLedger N032. |
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
| 2026-04-29 | GOOGL Q1 earnings | GOOGL, QQQ | Ad revenue + cloud; could push Sum to +3. **Date corrected 2026-04-20 — confirmed Apr 29 (Alphabet IR abc.xyz), not Apr 22 as previously logged.** |
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
