# Weekly Regime Review — 2026-04-14 (18:00 UTC+8 = 06:00 ET Sun)

**Coverage window:** 2026-04-14 only (single-day). Workspace initialized 2026-04-14; no prior Mon/Wed/Fri briefs to aggregate. This is a **bootstrap + refresh edition** — incorporates today's web-search data closures and intra-day market moves atop the original bootstrap review. Next Sunday (2026-04-20) will be the first true 7-day aggregation.

**Upstream artifacts read:** `market-brief-2026-04-14.md` (v3), `trade-rec-2026-04-14.md` (v7), `us-close-snapshot-2026-04-14.md`, `news-events/news-2026-04-14.md`, `Memory.md` (current), `Risk Rules.md`, `Data Sources.md`.

---

## 1. Regime Label: Start-of-Week → End-of-Week

- **Start-of-week:** Baseline unknown — workspace initialized 2026-04-14.
- **End-of-week (2026-04-14):** *Energy-led reflation shock + hawkish repricing, softening at the margin.*
- **What moved it:** Hormuz blockade announced Apr-12 (Brent spiked +8.3% to ~$102) → CENTCOM scoped to Iran-bound traffic + both sides signalled willingness to talk → Brent pulled back below $100 ($98–99 intra-day Apr-14). Equities rebounded +1% (S&P 6,886). Grade-A variables doing the work: **Brent spot + M1–M3 deep backwardation** (F1–F2 ≈ −$9.6, ann. roll −110%, supply-shock confirmed; A), **10y UST 4.36%** (+4.2 bps on day; term-premium repricing; A), **BTC active addresses** −41% w/w (619k→364k; structural bearish signal blocking long promotion; A).

---

## 2. Primary Regime Variables — Weekly Path

Single observation available (workspace Day 1). Mon/Wed/Fri cells blank.

| Variable | Mon | Wed | Fri | Sun (2026-04-14) | Direction verdict |
|---|---|---|---|---|---|
| Brent spot + M1–M3 curve (A) | — | — | — | $98.05 spot (intra-day range $96.48–$98.68); M1–M3 **deep backwardation** (F1–F2 ≈ −$9.6, ann. roll −110%, lowest on record) | **Elevated, supply shock confirmed structurally.** Positioning crowded long → R−1 blocks entry. Curve shape matters more than spot retreat from $102. |
| 10y nominal / ACM term premium (A) | — | — | — | DGS10 4.359% (+4.2 bps); 2s10s +59 bps; DFII10 1.90%; ACM MISSING (Jan-2026 ~0.59%; Apr not posted) | **Rising nominal yields, positive slope.** Hawkish repricing intact; ACM gap prevents full calibration. |
| BTC trend + perp funding (A/B) | — | — | — | $74,414 (+5% vs prior $70.9k); perp funding **negative** (Binance, crowded short = contrarian-bullish); active addresses 364k (−41% w/w = structural S−1) | **Tactical T+1 / R+1, structural S−1.** Net: no directional edge. |

---

## 3. Thesis Survival Audit

No open positions. Watchlist review per Memory.md §5 and Risk Rules.md §3:

| Item | Direction | Trigger fired? | Invalidation tripped? | Time-to-invalidation clock | Recommendation |
|---|---|---|---|---|---|
| Copper long | Long | **No** — S+1 / T+1 / C 0 / R 0 = +2; no China demand catalyst on 2w calendar | No | Clock started 2026-04-14; no stale risk (0d) | **Hold on watchlist.** Cleanest S+T combo. Trigger = pullback to trend + supportive China PMI/IP surprise. |
| Oil (Brent/WTI) long | Long | **No** — extended; S+1 confirmed by backwardation but R−1 on crowded positioning; CENTCOM scoping tightened but did not release R | No | Clock started 2026-04-14; 0d | **Hold on watchlist.** Do-not-chase intact. EIA Apr-15 is symmetric risk — a build de-crowds, a draw re-loads. |
| ~~BTC short~~ | — | **REMOVED 2026-04-14 v5.** Funding negative (Binance, crowded short), exchange outflows −7.9k BTC (bullish), price reclaim $74.4k (+5%). Short thesis invalidated. Cannot flip long: S−1 on active-address collapse. | — | — | **Out of book.** No edge either direction. |

**New thesis candidates:** None promoted. Apr-13 BTC ETF net outflow −$325.8M (Grade B) conflicts with Grade A exchange-netflow (bullish) — reconciliation question carried forward but does not create a fresh entry thesis.

---

## 4. Methodology Adherence Check

| Metric | Count |
|---|---|
| Trade recs issued this week | 1 (`trade-rec-2026-04-14.md` v7) |
| |Sum| ≥ 3 signals fired | 0 |
| Trades entered | 0 |
| Entries below threshold | 0 |

**Adherence verdict: clean.** The rec correctly refused to force trades when all candidates sat at +2 or below. No Grade-C padding observed. No stock-to-flow / halving timing used. "No trade" correctly invoked per Methodology §7. The single-stock book went T-blank per the 2026-04-14 audit-addition binding rule (residual momentum replaces raw TSMOM for the 12-name universe) — this is the correct fail-loud reading, not an error.

**Below-threshold entries:** 0. No lesson required for §8.

---

## 5. Data-Gap Ledger (Fail-Loud)

Grade-A rows that printed MISSING during the coverage window, per Data Sources.md fail-loud rule:

| Row (Grade A) | Source | Status | Decision-moving? |
|---|---|---|---|
| **Intermediary capital ratio** (NY Fed PD equity/total, z-score 3y) | NY Fed primary dealer stats (weekly) | MISSING — 2026-04-14 audit-addition, first pull pending | Not today (no R-gated candidate at +2 that this would flip) |
| **Residual momentum** (12m FF5-residualized, single-stock) | Kenneth French library + rolling OLS | MISSING — first pull pending | **YES** — TSM and AMZN sit at S+1/C+1; positive residual would push to |Sum|=+3 and trigger entry consideration |
| **Basis-momentum** (4w/12w ΔF1–F2, commodities) | Derived from daily settles | MISSING — first pull pending | Not today (Brent already R−1 blocked; divergence-cap would only weaken the case further) |
| **ACM term premium 10Y** (April monthly) | NY Fed ACM CSV | MISSING — monthly not yet posted (latest Jan-2026 ~0.59%) | Not today |
| **BTC 3m basis** (Deribit) | Deribit public API / CME basis | MISSING — search inconclusive | Not today (BTC S−1 structural block regardless) |

**Closed during coverage window (2026-04-14):** DGS2 3.77%, DGS10 4.359%, DFII10 1.90%, 2s10s +59 bps, META $630.49, EURUSD ~1.1769, Brent M1–M3 deep backwardation, BTC funding negative (Binance), BTC active addresses 619k→364k.

**Priority unblocker for next week:** Residual momentum computation for NVDA/TSM/AMZN/META — this is the only MISSING row that could be decision-changing (would unblock single-stock T-scores and potentially promote TSM or AMZN to |Sum| ≥ 3). Requires Kenneth French monthly factor download + rolling 12m OLS; not a single-number web-search closure.

---

## 6. Outstanding Research Questions — Age Check

From Memory.md §9. All questions opened 2026-04-14 (age: 0 days; none >4 weeks).

| Question | Opened | Age | Disposition |
|---|---|---|---|
| BTC funding/OI/liquidation as standalone directional signal | 2026-04-14 | 0d | Carry forward; revisit when funding is routinely pulled |
| MVRV/SOPR/HODL waves as timing tools | 2026-04-14 | 0d | Carry forward; regime-context only |
| Post-ETF BTC factor stability | 2026-04-14 | 0d | Carry forward; monitor alpha decay |
| BTC flow-signal reconciliation (ETF outflow −$325.8M vs exchange outflow −7.9k BTC) | 2026-04-14 | 0d | **Escalate to next brief** — watch if ETF outflow extends into a 2–3 day streak; if so + address recovery → re-evaluate short thesis |
| Post-Hormuz M1–M3 curve evolution | 2026-04-14 | 0d | **Escalate to next brief** — #1 regime variable; need updated settles to assess whether backwardation is steepening or flattening (basis-momentum input) |

No questions >4 weeks. No disposition changes required.

---

## 7. Next Week's Catalyst Map

| Date | Event | Assets | Reprice risk | Note |
|---|---|---|---|---|
| **2026-04-15 (Tue)** | **EIA weekly crude inventories** (w/e Apr-10) | Brent, WTI, energy equities | **HIGH** | First full post-blockade print; governs oil de-crowding vs re-load. Prior week: +3.1M bbl build to 464.7M bbl. |
| 2026-04-15–16 | US Mar Retail Sales + Mar Industrial Production | SPY, QQQ, DXY | MED | Consumer/manufacturing read post-CPI shock |
| **2026-04-16 (Wed)** | **TSM Q1 earnings** (pre-mkt TW, 14:00 Taipei = 02:00 ET) | TSM, NVDA, QQQ, EWY | **HIGH** | Prelim $35.7B rev (+35% y/y); consensus $35.47B. Focus: N2 margin, Q2 guide, capex plan ($52–56B). Bar elevated — confirmation trade has poor asymmetry. |
| 2026-04-17 (Thu) | Monthly OpEx + UMich prelim sentiment | SPY, QQQ, DXY | MED | Positioning flush risk |
| 2026-04-23 (Wed) | AMZN earnings | AMZN, QQQ | MED | Retail + cloud read |
| **2026-04-28–29 (Mon–Tue)** | **FOMC** | All | **HIGH** | Statement + dots; path repricing risk. Rate 3.50–3.75%; April cut probability fading. |
| 2026-04-29 (Tue) | META earnings | META, QQQ | MED | Same-day FOMC — vol compression risk |
| 2026-05-12 (Mon) | April CPI | Rates, DXY, Gold, BTC | HIGH | Energy-shock follow-through (Mar: +0.9% m/m, +3.3% y/y) |

**Most likely to reprice the book next week:**

1. **EIA Apr-15** — directly informs Brent/WTI watchlist. A draw > 2M bbl re-loads the crowded long; a build > 3M bbl or neutral print + diplomacy progress de-crowds and could shift R from −1 toward 0 for oil longs. Also the first hard supply-demand read post-blockade escalation.
2. **TSM Apr-16 earnings** — if strong + residual momentum gets computed and lands positive, TSM could be the first |Sum| ≥ 3 signal in the book (S+1, T+1, C+1 = +3). Without residual momentum, T remains blank and the earnings are unactionable per audit-addition fail-loud.

---

## What I'll Watch Monday Open

**EIA Apr-15 inventory print** — tape-moving for Brent/WTI. If draw + diplomacy stalls → oil longs extend further into crowded territory (R stays −1). If build + diplomacy progress → de-crowding begins and watchlist becomes more interesting. **Brent intra-day range ($96.48–$98.68) vs $100 psychological barrier** — a sustained break back above $100 on the EIA print would re-tighten the geopolitical premium; a fade below $96 would signal the reflation impulse is peaking.

**TSM pre-market Apr-16 (02:00 ET)** — the Q2 guide and capex update matter more than the headline beat. If N2 margin guidance disappoints, the AI-capex narrative takes a hit across NVDA/QQQ. If capex is raised, it confirms structural demand and supports the S+1 score for TSM/NVDA/AMZN.

---

*Grades cited per Methodology: A = replicated, coherent mechanism; B = regime-dependent. No Grade C padding. No stock-to-flow / halving timing. Audit-addition contribution log (Memory §10) unchanged — no entries; first pulls pending. Coverage window = 1 day (bootstrap); first full-week review targets 2026-04-20.*
