---
name: trade-update
description: "Event-driven 4-layer sync on trade execution events — entries, exits, stop moves, tranches, size changes. Use when 'I entered X', 'I bought X', 'stopped out of X', 'moved stop on X', 'trimmed X'. Not for placing trades or daily rec/brief."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# Trade Update

One event = four layers updated in order, no batching. Interactive only (no schedule).

## Step 1 — Reads
1. `framework/Trade-Execution-Protocol.md` — authoritative procedure
2. `framework/Memory.md` — §2 Open Positions, §5 Watchlist, §7 Closed Trades
3. `master-data-log.xlsx` → SignalLedger sheet (find rows to update)

## Step 2 — Classify event

| Phrase | Event type |
|---|---|
| entered/bought/filled/opened (promoted) | Fresh entry §A |
| entered/bought (near-miss/not in rec) | Ad-hoc promotion §C |
| added to/scaled into | Tranche add §B |
| stopped out/stop hit | Exit — stop §D |
| hit target/TP1/took profit | Exit — target §D |
| closed/cut/invalidated/time-stop | Exit — discretionary §D |
| moved stop/stop to breakeven/trailed | Adjustment — stop §E |
| trimmed/reduced/sized up | Adjustment — size §F |

## Step 3 — Fail-loud ambiguity check

Confirm all five: Asset, Side, Price, Time (UTC+8 absolute), SignalLedger linkage. If unclear, STOP and ask.

## Step 4 — Four layers, in order

**Layer 1 — framework/Memory.md:** §2 add/remove/edit row. §7 append for exits. Recompute portfolio heat. Update header timestamp.

**Layer 2 — SignalLedger (openpyxl):**
- Fresh entry: Taken=YES on today's Promoted row. Don't overwrite Entry_Price if set.
- Ad-hoc promotion: new P### row, cross-link N### in Notes.
- Tranche: update Notes, weighted-average Entry_Price.
- Exit: Status (HIT_STOP/HIT_TARGET/EXPIRED/DISCRETIONARY_CLOSE), Exit_Price, Exit_Date, Days_to_Exit, Hypo_PnL_Pct.
- Stop move: don't edit ATR_Stop, append to Notes.

**Layer 3 — framework/memory-lessons.md:** Append one factual line. Non-routine adjustments only.

**Layer 4 — auto-memory (conditional):** Only for repeated/novel patterns.

## Step 5 — Confirm

Report: event recorded, signal ID, new portfolio heat, follow-up if any.

## Reconciliation mode
Triggered by "reconcile the ledger": diff framework/Memory.md §2 vs SignalLedger OPEN rows, fix gaps oldest-first, save after each event.
