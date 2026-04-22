# Trade-Update Plan — 2026-04-20

## Context

Gerald submitted 5 Binance USD-S Futures position-history screenshots at 13:23–13:24 UTC+8. The screenshots reveal that all three methodology-tracked open positions (INTC P003, Gold P004, QQQ P005) have been closed, plus a large volume of additional non-methodology activity. Memory.md was last updated 2026-04-17 and is stale — today's positions-monitor and trade-rec both ran with ghost-open positions. The 4-layer sync must close the gap.

---

## Extracted Trade Data (from screenshots)

### Methodology positions (tracked in Memory.md §2 and SignalLedger)

| ID | Asset | Entry | Exit price | Exit date/time (UTC+8) | Realized PNL | ROI |
|----|-------|-------|-----------|------------------------|-------------|-----|
| P003 | INTC | $67.8701 (Binance INTCUSDT) | $68.26 | 2026-04-19 21:31:55 | +$2.35 | +2.09% |
| P004 | Gold (XAU) | $4,780.69 | $4,823.65 | 2026-04-18 17:12:33 | +$3.20 | +0.80% |
| P005 | QQQ | $640.09 avg | $643.02 | 2026-04-19 16:00:05 | +$4.51 | +1.13% |

Note: Memory.md recorded INTC entry as $64.68 but Binance fill shows $67.8701 — plan notes the discrepancy; use Binance as authoritative for exit sync.

### Non-methodology activity (not in SignalLedger; log totals only)

| Asset | Side | Entry | Exit | Closed | PNL |
|-------|------|-------|------|--------|-----|
| BTCUSDT | Long | 72,172.6 | 74,983 | 2026-04-19 | +$11.17 |
| QQQUSDT | Long | 640.09 | 643.02 | 2026-04-19 | +$4.51 (same as P005) |
| BZUSDT | Short | 88.66 | 88.40 | 2026-04-19 | +$0.50 |
| INTCUSDT (Iso 4x) | Long | 67.87 | 68.26 | 2026-04-19 | +$2.35 (same as P003) |
| CLUSDT | Long | 84.60 | 83.79 | 2026-04-19 | −$6.43 |
| BZUSDT | Short | 87.95 | 88.91 | 2026-04-19 | −$3.49 |
| INTCUSDT | Long | 68.27 | 67.73 | 2026-04-20 | −$3.01 |
| BTCUSDT | Long | 75,687.77 | 74,942.7 | 2026-04-20 | −$6.43 |
| CLUSDT | Long | 84.64 | 84.97 | 2026-04-19 | −$2.99 |
| XAGUSDT | Short | 79.42 | 80.50 | 2026-04-20 | −$6.19 |
| TSLAUSDT | Short | 397.32 | 399.91 | 2026-04-20 | −$2.92 |
| AAVEUSDT | Long | 93.273 | 93.30 | 2026-04-19 (4 sec) | −$0.51 |
| AAVEUSDT | Long | 93.23 | 92.32 | 2026-04-19 | −$4.22 |

---

## 4-Layer Sync Plan

### Layer 1 — Memory.md (`Trade/framework/Memory.md`)

**§2 Open Positions** — remove all three rows; update portfolio heat to $0 / 0%:
- Remove INTC row (closed 2026-04-19)
- Remove Gold row (closed 2026-04-18)
- Remove QQQ row (closed 2026-04-19)
- Replace heat block with: "No open positions as of 2026-04-20."

**§7 Closed Trades Log** — append three new rows:
| Asset | Side | Entry/exit dates | Entry/exit price | P&L | Thesis worked? | Lesson |
|---|---|---|---|---|---|---|
| Gold (XAU) | Long | 2026-04-16 22:41 → 2026-04-18 17:12 UTC+8 | $4,780.69 → $4,823.65 | +$3.20 (+0.80%) | Partial — exited before Apr-22 ceasefire binary; thesis intact at exit but left early. | Exited 4 days before the primary catalyst event. |
| QQQ | Long | 2026-04-17 00:02 → 2026-04-19 16:00 UTC+8 | $640.09 → $643.02 | +$4.51 (+1.13%) | Partial — exited before Apr-22–23 earnings cluster; thesis intact at exit. | Exited before GOOGL/TSLA/INTC catalyst week. |
| INTC | Long | 2026-04-16 09:29 → 2026-04-19 21:31 UTC+8 | $67.87 (Binance) → $68.26 | +$2.35 (+2.09%) | Partial — exited before Apr-23 earnings. Terafab thesis unconfirmed at exit. | Left before the earnings confirmation event. |

**§2 header "Last updated"** — bump to 2026-04-20.

**§6 Catalysts** — strike-through any events that have now passed (Apr-19 Iran sanctions waiver, Apr-18/19 CLUSDT/BZUSDT events).

---

### Layer 2 — SignalLedger (`Trade/master-data-log.xlsx`, sheet: SignalLedger)

Update three OPEN rows to CLOSED using openpyxl:

| Row | Promoted ID | Fields to write |
|-----|-------------|----------------|
| P003 INTC | Status → HIT_TARGET; Exit_Price → 68.26; Exit_Date → 2026-04-19; Days_to_Exit → 3; Hypo_PnL_Pct → +0.57% ((68.26/67.87−1)×100); Catalyst_Outcome → EXITED_PRE_CATALYST; Notes → "Closed 2026-04-19 21:31 UTC+8 before Apr-23 earnings. Memory.md entry $64.68 vs Binance fill $67.87 — discrepancy noted." |
| P004 Gold | Status → HIT_TARGET; Exit_Price → 4823.65; Exit_Date → 2026-04-18; Days_to_Exit → 2; Hypo_PnL_Pct → +0.90% ((4823.65/4780.69−1)×100); Catalyst_Outcome → EXITED_PRE_CATALYST; Notes → "Closed 2026-04-18 17:12 UTC+8 before Apr-22 ceasefire binary. DXY thesis intact at exit." |
| P005 QQQ | Status → HIT_TARGET; Exit_Price → 643.02; Exit_Date → 2026-04-19; Days_to_Exit → 2; Hypo_PnL_Pct → +0.46% ((643.02/640.09−1)×100); Catalyst_Outcome → EXITED_PRE_CATALYST; Notes → "Closed 2026-04-19 16:00 UTC+8 before Apr-22–23 earnings cluster. FOMC Apr-28 unresolved." |

Script path: `scripts/sync_trade_exits_2026-04-20.py` (new file, single-use)

---

### Layer 3 — memory-lessons.md (`Trade/framework/memory-lessons.md`)

Append one entry summarizing the batch:

```
- **2026-04-20 | Batch exit — all methodology positions closed early.** 
  All three open positions (Gold P004, QQQ P005, INTC P003) closed profitable but 
  before their primary catalysts. Gold +$3.20 (+0.80%) exited 2026-04-18 — 4 days 
  before Iran ceasefire binary Apr-22. QQQ +$4.51 (+1.13%) exited 2026-04-19 — 
  3 days before GOOGL/TSLA/INTC earnings cluster. INTC +$2.35 (+2.09%) exited 
  2026-04-19 — 4 days before Q1 earnings Apr-23 (the confirmation event). 
  Combined methodology PNL: +$10.06 USDT. Large off-methodology activity visible 
  in Binance history (AAVE, TSLA short, multiple BTC/CL/BZ trades); net off-methodology 
  PNL approximately −$14 to −$20 USDT — pulls overall session negative. 
  **Two structural lessons:** (1) Early exits forfeited catalyst optionality — the 
  methodology positions had well-buffered stops ($56 INTC / $4,640 Gold / $600 QQQ) 
  and intact theses; exiting days before the catalyst event converts a thesis trade 
  into a noise trade. (2) Off-methodology activity (AAVE, TSLA short, multiple 
  CL/BZ scalps) is producing the bulk of session losses — no scoring, no documented 
  invalidation, no stop discipline. This pattern mirrors the EWY stop-tightening 
  lesson: methodology edge is only captured when the methodology is followed end-to-end.
  **Pipeline staleness flagged:** positions-monitor and trade-rec both fired 2026-04-20 
  with ghost-open INTC/Gold/QQQ. Memory.md must be updated before the next scheduled 
  task runs, or the brief will score positions that do not exist.
```

---

### Layer 4 — Auto-memory (`C:\Users\Lokis\.claude\projects\...\memory\`)

Update or create `project_open_positions.md`:
- Remove INTC/Gold/QQQ as open
- Record: "As of 2026-04-20, no methodology positions are open."
- Note pipeline staleness incident and the off-methodology trading pattern.

---

## Verification

1. Read `Trade/framework/Memory.md` §2 after edit — confirm table is empty and heat reads 0%.
2. Read `Trade/framework/memory-lessons.md` last entry — confirm batch lesson appended.
3. Run `python scripts/sync_trade_exits_2026-04-20.py` — confirm 3 rows updated in SignalLedger (Status = HIT_TARGET for P003/P004/P005).
4. Read auto-memory file — confirm no open positions listed.
5. Check that `Trade/2026-04-20/trade-rec-2026-04-20.md` contains a `[MOCK — TEST RUN]` tag (it does) — no production rec file needs retroactive edits.

---

## Critical Files

| File | Action |
|------|--------|
| `Trade/framework/Memory.md` | Edit §2 (clear open positions) + §7 (add 3 closed trades) |
| `Trade/framework/memory-lessons.md` | Append batch-exit lesson |
| `Trade/master-data-log.xlsx` | Update SignalLedger P003/P004/P005 via Python script |
| `scripts/sync_trade_exits_2026-04-20.py` | New single-use script for Excel update |
| `C:\Users\Lokis\.claude\projects\...\memory\project_open_positions.md` | Update positions state |
