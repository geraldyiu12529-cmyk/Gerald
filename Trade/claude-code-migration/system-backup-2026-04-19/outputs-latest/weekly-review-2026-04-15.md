# Weekly Regime Review — 2026-04-15 (18:00 UTC+8 = 06:00 ET)

**Coverage window:** 2026-04-14 to 2026-04-15 (2 days). Workspace initialized 2026-04-14; first audit-data-staging computed 2026-04-15. This is the second weekly review — still short-window. Next Sunday (2026-04-20) targets the first full 5-day aggregation.

**Upstream artifacts read:** `market-brief-2026-04-14.md` (v4), `trade-rec-2026-04-14.md` (v8), `us-close-snapshot-2026-04-14.md` (v2), `us-close-snapshot-2026-04-15.md`, `news-events/news-2026-04-14.md` (v2), `audit-data-staging-2026-04-15.md`, `weekly-review-2026-04-14.md` (bootstrap), `Memory.md`, `Risk Rules.md`, `Methodology Prompt.md`, `Data Sources.md`, `hypo-ledger-2026.md`.

---

## 1. Regime Label: Start-of-Week → End-of-Week

- **Start-of-week (2026-04-14):** *Energy-led reflation shock + hawkish repricing, softening at margin.*
- **End-of-week (2026-04-15):** **Post-shock reflation unwind → cautious risk-on.** Label shifted.

**Grade A variables that drove the shift:**

1. **Oil crash (A):** WTI settled $91.28 on Apr-14 (−8% d/d), Brent $94.79 (−4%). Apr-15 intraday range WTI $92–98, Brent $94–99 — extreme volatility. Iran peace-deal hopes + IEA "demand destruction" call eroded the energy-shock anchor. This is the sharpest single-day oil decline since the war began.
2. **Equities at pre-war highs (A):** S&P 500 6,967.38 (+1.18%), Nasdaq +1.96%. Five Mag7 names >1σ moves (META +4.1%, AMZN +3.8%, TSLA +3.8%, GOOGL +2.9%, NVDA +2.6%). VIX closed 18.59 — first sub-20 close since Iran conflict began.
3. **DXY breakdown (A):** 98.13, 7th consecutive loss, lowest since late-Feb pre-war. Accelerates metals (silver $79 breakout, gold steady at $4,761).
4. **BTC structural block persists (A):** Active addresses 364k (−41% w/w), S = −1 unchanged. BTC tactically firmer (~$75.9k intraday high, highest since Feb-5 crash) but structurally blocked.

**What changed vs. bootstrap review (Apr-14):** The "energy-led reflation shock" label no longer holds when WTI has crashed 8% and Brent broken below $95. The Hormuz blockade remains but is scoped to Iran-bound traffic; Islamabad peace talks ended without deal after 21 hours but both sides signaling willingness for a second round (ceasefire expires Apr-21). The regime anchor is shifting from supply-shock fear to post-shock normalization, with equities and VIX confirming risk-appetite recovery. "Cautious" qualifier reflects: deep backwardation in oil curve still structurally elevated, March PPI +3.3% y/y confirmed inflation pass-through, FOMC Apr-28 still a risk.

---

## 2. Primary Regime Variables — Weekly Path

Two observation points available (workspace Day 1 + Day 2 audit-staging + Apr-15 web-search).

| Variable | Mon (Apr-14 brief) | Mon (Apr-14 close) | Tue (Apr-15 intraday) | Direction verdict |
|---|---|---|---|---|
| **Brent spot + M1–M3 curve (A)** | $97.89 brief; M1–M3 deep backwardation (F1–F2 ≈ −$9.6) | **$94.79 settle** (−3.2%) | $94.43–99.41 intraday (extreme vol) | **Deteriorating.** Spot crashed through $95 support; basis-momentum still steepening per Apr-15 staging (4w +3.50, 12w +3.50, no divergence cap) — curve shape lagging spot collapse. Watch for flattening next week to confirm regime shift. |
| **10y nominal / ACM term premium (A)** | DGS10 4.34% (+3 bps); ACM MISSING | 4.34% (flat) | No new data | **Flat.** Rates absorbed PPI + oil shock without stress. Hawkish repricing intact but not intensifying. ACM Apr still MISSING (non-decision-moving). |
| **BTC trend + perp funding (A/B)** | $74,442; funding NEGATIVE (Binance, Apr-12); active addr 364k (S−1) | $75,900 intraday high | ~$74–76k range | **Marginally firmer.** Price reclaimed $76k intraday (highest since Feb-5 crash). Exchange netflows −7.9k BTC (bullish). ETF outflow −$325.8M (Grade B, conflicting). Structural S−1 unchanged. No directional edge. |

**New audit-addition readings (first compute 2026-04-15):**

| Variable | Value | Score impact | Decision-moving? |
|---|---|---|---|
| **Intermediary capital z-score** | **+1.86** (ratio 0.140, above 3y mean 0.129) | R adjustment = +0; **EWY fail-loud caveat RESOLVED** | **YES** — EWY Sum = +3 now clean |
| **Residual momentum (FF5, 12 stocks)** | All 12 near 0.00% (approximate; 10m window, Apr2025–Jan2026 FF5 data) | T = 0 for all single stocks | **YES** — T-block lifted but T = 0 means TSM/AMZN/META stay at +2, not promoted |
| **Basis-momentum (5 commodities)** | Brent/Silver/Copper steepening (no cap); **WTI 4w flattening → divergence cap → S capped at 0**; **Gold 4w sharp flattening → divergence cap → S capped at 0** | WTI Sum +2 → +1; Gold Sum +2 → +1 | **YES** — WTI and Gold demoted; narrows near-miss roster |

---

## 3. Thesis Survival Audit

**No open positions.** Watchlist review per Memory.md §5:

| Item | Direction | Trigger fired? | Invalidation tripped? | Time-to-inv clock | Recommendation |
|---|---|---|---|---|---|
| **EWY long** | Long | **PARTIAL.** Fail-loud caveat resolved (intermediary capital z = +1.86 → R = 0 → Sum +3 clean). TSM earnings Apr-16 is the binary catalyst — not yet fired. | No | Started 2026-04-14; 1d elapsed | **PROMOTE TO ACTIVE SIGNAL.** Sum = +3 clean. Pre-entry checklist passes 5/6 (catalyst asymmetry cautionary). Awaits Gerald's decision + TSM earnings. |
| Copper long | Long | **No** — S+1/T+1/C0/R0 = +2. Basis-momentum steepening confirms S+1 (no divergence cap). | No | Started 2026-04-14; 1d | **Hold on watchlist.** Cleanest S+T in metals. Needs C catalyst (China PMI/IP). |
| Oil (Brent/WTI) long extended | Long | **No** — Brent S+1 (basis-momentum confirms), T+1, C+1 (EIA Apr-15), R−1 (crowded). **WTI demoted: basis-momentum flattening → S capped at 0 → Sum +1.** | **Partial — WTI thesis weakening.** WTI crashed −8% to $91.28; Brent broke below $95. Iran peace-deal momentum accelerating. | Started 2026-04-14; 1d | **Narrow to Brent only.** WTI divergence-cap fires. Do-not-chase intact. **Review for removal if Brent breaks $93 or curve flattens.** |
| Silver | Long (new) | **Not yet scored formally.** $79 breakout (+4.5%), DXY at 7-session low. S+1 (basis-momentum steepening), T+1, C+1 (gold sympathy), R−1 (crowded alongside gold). Sum +2. | n/a | Not yet on watchlist formally | **Add to watchlist** at Sum = +2, blocked by R−1. Correlation-gated with Copper. |
| ~~BTC~~ | — | Removed 2026-04-14. No edge either direction (S−1 blocks long). | — | — | Out of book. |

**New thesis candidates from audit-data:**
- **Gold demoted to Sum +1** (was +2): basis-momentum divergence cap fires. S capped at 0, T+1, C+1, R−1 = +1. Removed from near-miss roster.
- **WTI demoted to Sum +1** (was +2): same divergence-cap effect. Oil long thesis should narrow to Brent-only.

---

## 4. Methodology Adherence Check

| Metric | Count |
|---|---|
| Trade recs issued this week | 1 (`trade-rec-2026-04-14.md`, 8 versions due to Day-1 bootstrap — 1 logical rec) |
| |Sum| ≥ 3 signals fired | 1 (EWY at +3; flagged v4 brief, fail-loud blocked promotion through v8 rec) |
| Trades entered | 0 |
| Below-threshold entries | 0 |
| Forced trades | 0 |

**Adherence verdict: clean.** The rec correctly refused to promote EWY when intermediary capital was MISSING — correct fail-loud application. After the audit-data-staging resolved the caveat (Apr-15), EWY became a clean +3 signal but no new trade-rec has run yet to formally promote it. No Grade C padding. No stock-to-flow / halving timing. "No trade" correctly invoked. The v1–v8 version churn reflects workspace bootstrap (multiple ad-hoc runs on Day 1); the P1 delta-check gate implemented Apr-15 should eliminate this going forward.

**Violations:** 0.

---

## 5. Data-Gap Ledger (Fail-Loud)

Grade A rows that printed MISSING during the coverage window:

| Row (Grade A) | Status start-of-week | Status end-of-week | Closed by |
|---|---|---|---|
| **Intermediary capital ratio** | MISSING | **CLOSED: z = +1.86** | `audit-data-staging-2026-04-15.md` |
| **Residual momentum (FF5, 12 stocks)** | MISSING | **CLOSED: all ~0.00%** (approximate; web-search-derived returns, 10m window) | `audit-data-staging-2026-04-15.md` |
| **Basis-momentum (5 commodities)** | MISSING | **CLOSED: all 5 computed** (Brent/Silver/Copper steepening; WTI/Gold divergence cap fires) | `audit-data-staging-2026-04-15.md` |
| **ACM term premium 10Y (Apr)** | MISSING | **STILL MISSING** — monthly not yet posted; latest Jan-2026 ~0.59% | NY Fed has not published April data |
| **BTC 3m basis (Deribit)** | MISSING | **STILL MISSING** — search inconclusive | Deribit data not reliably web-sourced |

**Net: 3 of 5 Grade A MISSING rows closed this week.** The remaining 2 (ACM, BTC 3m basis) are not decision-moving for any current signal.

**Data quality caveat on residual momentum:** All residuals near zero using a 10-month FF5 window. Plausible but low-confidence. Accuracy improves when Kenneth French publishes Feb–Mar 2026 factors. Treat T = 0 as directionally correct but provisional.

---

## 6. Audit-Addition Status

**All three audit-addition variables produced their first non-MISSING values on 2026-04-15.** Contributions to Memory §10 (audit-addition contribution log):

| Variable | Asset | Contribution | Decision-moving? |
|---|---|---|---|
| **Intermediary capital ratio** | EWY (cross-asset R-overlay) | z = +1.86 → R adjustment +0; **resolved fail-loud caveat blocking EWY promotion** | **YES** — EWY Sum = +3 now clean |
| **Residual momentum** | All 12 single stocks | All T = 0; **lifted T-block but did not promote any stock** (TSM/AMZN/META stay +2) | **YES** — resolved T-blank; revealed flat idiosyncratic alpha |
| **Basis-momentum** | WTI, Gold | Divergence cap fired → **S capped at 0**; WTI Sum +2 → +1; Gold Sum +2 → +1 | **YES** — narrowed near-miss roster |
| **Basis-momentum** | Brent, Silver, Copper | Steepening confirmed → no divergence cap; S unchanged +1 | No — confirmatory |

**All three variables contributed to scorecard changes within 1 day of going live.** Evidence for the 2026-10-14 six-month review is accumulating. First entries appended to Memory §10.

---

## 7. Next Week Preview

### Catalysts

| Date | Event | Assets | Reprice risk |
|---|---|---|---|
| **2026-04-15 (Tue)** | **EIA weekly crude inventories** (10:30 ET; w/e Apr-10) | Brent, WTI | **HIGH** — first post-blockade print. Prior: +3.1M bbl build. Draw = stabilizes; build = accelerates oil downside. |
| **2026-04-16 (Wed)** | **TSM Q1 earnings** (02:00 ET) | TSM, NVDA, QQQ, **EWY** | **HIGHEST** — binary for EWY Sum = +3 entry. Prelim $35.71B at high end of guide. Focus: N2 margin, Q2 guide, capex. |
| 2026-04-17 (Thu) | Monthly OpEx + UMich prelim sentiment | SPY, QQQ, DXY | MED — positioning flush |
| **2026-04-21 (Mon)** | **Iran ceasefire expires** | Brent, WTI, Gold, DXY | **HIGH** — if no new round of talks or extension, Hormuz risk reprices. Possible new talks this week per NBC/CNBC. |
| 2026-04-21 (Mon) | Advance Retail Sales (March, rescheduled) | SPY, QQQ, consumer | MED — demand-side read |
| 2026-04-22 (Tue) | TSLA + GOOGL Q1 earnings | TSLA, GOOGL, QQQ | MED–HIGH |
| 2026-04-23 (Wed) | INTC + AMZN earnings | INTC, AMZN, QQQ | MED–HIGH |
| **2026-04-28–29** | **FOMC** | All | **HIGH** — path repricing; rate 3.50–3.75%; April cut probability fading |
| 2026-04-29 (Tue) | META earnings (same-day FOMC) | META, QQQ | MED–HIGH |

### Regime variables to watch

1. **Brent M1–M3 curve post-EIA** — does deep backwardation flatten as spot collapses? Basis-momentum still says steepening, but spot is diverging. A curve flattening confirmation would complete the regime shift from "reflation shock" to "post-shock unwind."
2. **Iran ceasefire deadline Apr-21** — if talks resume and ceasefire extends, oil de-crowding accelerates (R−1 could ease). If ceasefire lapses without deal, Hormuz risk reprices and oil spikes.
3. **TSM earnings Apr-16** — binary for EWY. A miss or weak Q2 guide invalidates C+1 and drops Sum to +2.
4. **BTC active addresses** — need recovery toward 500k+ to reopen the BTC discussion. Unchanged at 364k.

### Priority unblockers

1. **Gerald's decision on EWY** — signal is clean at +3, checklist passes (catalyst asymmetry cautionary). TSM earnings Apr-16 is the decision event. This is the first clean |Sum| ≥ 3 in workspace history.
2. **Oil watchlist narrowing** — WTI divergence-cap demotes it; Brent holds but R−1 persists. If EIA prints a build AND Iran talks resume, oil long thesis should be reviewed for formal removal.
3. **ACM term premium April monthly** — not decision-moving but calibrates rates overlay. Expected mid-to-late April.

---

## Updated Scorecard (incorporating audit-data-staging 2026-04-15 + Apr-15 market data)

| Asset | S | T | C | R | Sum | Change vs Apr-14 | State |
|---|---|---|---|---|---|---|---|
| **EWY** | +1 | +1 | +1 | 0 | **+3** | **R-overlay confirmed** (was conditional) | **CLEAN SIGNAL — first in workspace** |
| Copper | +1 | +1 | 0 | 0 | **+2** | Basis-momentum confirms S+1 | Watchlist — cleanest metals |
| Brent | +1 | +1 | +1 | −1 | **+2** | Basis-momentum steepening confirms S+1; spot crashed to $94.79 | Extended; do not chase; review if <$93 |
| Silver | +1 | +1 | +1 | −1 | **+2** | Basis-momentum steepening; $79 breakout | Crowded; correlation-gated |
| QQQ | 0 | +1 | +1 | 0 | **+2** | Unchanged | Catalyst-dense |
| TSM | +1 | **0** | +1 | 0 | **+2** | **T-block lifted** — residual mom ~0 | Earnings Apr-16 |
| AMZN | +1 | **0** | +1 | 0 | **+2** | T-block lifted | Earnings Apr-23 |
| META | +1 | **0** | +1 | 0 | **+2** | T-block lifted | Earnings Apr-29 + FOMC |
| **WTI** | **0** | +1 | +1 | −1 | **+1** | **S demoted** by basis-momentum divergence cap | **Demoted from near-miss** |
| **Gold** | **0** | +1 | +1 | −1 | **+1** | **S demoted** by basis-momentum divergence cap | **Demoted from near-miss** |
| BTC | −1 | +1 | 0 | +1 | **+1** | Unchanged | No edge; S−1 blocks |
| ETH | 0 | +1 | 0 | 0 | **+1** | Unchanged | Hold/watch |

---

*Grades cited per Methodology: A = replicated, coherent mechanism; B = regime-dependent. No Grade C padding. No stock-to-flow / halving timing. Coverage window = 2 days (short-window). First full 5-day review targets 2026-04-20.*
