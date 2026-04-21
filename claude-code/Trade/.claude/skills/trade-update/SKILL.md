---
name: trade-update
description: "Event-driven 4-layer sync on trade execution events — entries, exits, stop moves, tranches, size changes. Use when 'I entered X', 'I bought X', 'stopped out of X', 'moved stop on X', 'trimmed X'. Not for placing trades or daily rec/brief."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_search_channels mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_send_message
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

**Layer 5 — Slack POSITION STATE SNAPSHOT (every event):**
After Layers 1–4 complete, post an updated snapshot to `#trading-scheduled-updates` so the cloud scheduled agent has current position context on its next fire. This is a single message, not a thread.

1. Resolve channel: `slack_search_channels(query="trading-scheduled-updates")` → pick exact-name match. Not found → log missing in rec, skip layer (do not fail the whole update).
2. Compose message. Lead tag `[POSITION-STATE]`. Compact format — this is machine-read by the cloud agent:

```
[POSITION-STATE] {YYYY-MM-DD HH:MM UTC+8}

Open positions (N):
| Sig | Asset | Side | Entry | Stop | Target | ATR | Size% | Thesis | Invalidation |
|-----|-------|------|-------|------|--------|-----|-------|--------|--------------|
| P001 | ... | long | ... | ... | ... | ... | 1.5% | ... | ... |

Portfolio heat: X.X%  |  Sector exposure: {tech X%, crypto Y%, ...}
Circuit breaker: {none | reduced | defensive}
Watchlist promotions since last snapshot: [tickers or "none"]
Last closed trade: {asset, exit type, hypo_pnl or "none this week"}
```

3. Send: `slack_send_message(channel_id=<id>, message=<body>)`. Pull content directly from the post-update state of `framework/Memory.md §2 §5 §7` — don't recompute from scratch.
4. If the event type was *Exit*: append a one-line epitaph below the table: `Exit: {asset} {HIT_STOP|HIT_TARGET|DISCRETIONARY} @ {price} — {hypo_pnl}`.

Purpose: cloud scheduled agent reads the most recent `[POSITION-STATE]` message on each fire (8am / 12pm / 4pm / 12am UTC+8) so it can produce position-aware intraday updates without local file access.

## Step 5 — Confirm

Report: event recorded, signal ID, new portfolio heat, Slack POSITION-STATE posted (y/n + link), follow-up if any.

## Reconciliation mode
Triggered by "reconcile the ledger": diff framework/Memory.md §2 vs SignalLedger OPEN rows, fix gaps oldest-first, save after each event.
