# Trade Execution Protocol

**Created:** 2026-04-17
**Status:** Active. Binding on every trade execution event.
**Authority:** This file is authoritative for the *update sequence* triggered by an execution event. It does not override `Risk Rules.md` (policy) or `Methodology Prompt.md` (decision framework). When in doubt about *whether* to take a trade, read those. When in doubt about *how to record* a trade that has already happened, read this.

The planning pipeline (brief → news → rec → signal-review) is scheduled daily/weekly. Executions are **event-driven** — they happen when you get filled, not at 20:20 UTC+8. This protocol is what keeps `Memory.md`, `master-data-log.xlsx`, and `memory-lessons.md` in sync with your actual book between scheduled runs.

The protocol is invoked by the `trade-update` skill whenever you report an execution event. Follow it exactly. Do not batch updates — apply every layer before moving on.

---

## Event types covered

| Event | Trigger phrases |
|---|---|
| **Entry (fresh)** | "I entered X", "I bought X", "filled X at $Y", "opened X" |
| **Entry (tranche add)** | "added to X", "second tranche", "scaled into X" |
| **Exit — stop** | "stopped out of X", "stop hit on X", "X got stopped" |
| **Exit — target** | "hit target on X", "TP1 on X", "took profit on X" |
| **Exit — time / discretionary / invalidation** | "closed X", "cut X", "invalidated X", "time-stop on X" |
| **Adjustment — stop** | "moved stop on X to $Y", "stop to breakeven on X", "trailed stop on X" |
| **Adjustment — size** | "trimmed X", "reduced X by half", "sized up X" |
| **Near-miss promoted ad-hoc** | Asset not on today's promoted list but executed anyway (e.g., near-miss with the blocking leg resolved intraday, or a correlation-gate deferral that cleared). |

---

## Universal rule: **fail-loud on ambiguity**

If the user reports an execution and:
- the asset name is ambiguous (e.g. "the gold trade" when there are two Gold signals),
- the direction is not clear,
- the price is missing,
- or there is **no matching OPEN signal in the SignalLedger** for an exit event,

STOP. Ask the user which signal ID (P### or N###) the execution refers to, or which price was filled. Never guess. A silent wrong update corrupts the performance record that feeds the 2026-10-14 audit review.

---

## The four layers that must be updated (in order)

Every execution event touches these four layers. The order matters — Memory.md is the canonical working state, so it is updated first; SignalLedger is the analytical record; memory-lessons.md is the narrative audit trail; auto-memory is the cross-session hint.

1. **`Memory.md`** (trader working state) — §2 Open Positions, §5 Watchlist, §7 Closed Trades Log
2. **`master-data-log.xlsx` → SignalLedger sheet** (analytical record)
3. **`memory-lessons.md`** (narrative lesson log, write-only)
4. **`.auto-memory/`** (only if the event reveals a repeated pattern — not every execution)

---

## Sequence per event type

### A. Entry — fresh (signal already promoted in today's rec)

1. **Memory.md §2** — append a new row: Asset | Side | Size | Entry date (YYYY-MM-DD HH:MM UTC+8) | Entry price (actual fill) | Stop / invalidation | Catalyst | Thesis (one line citing Sum score and components).
2. **Memory.md §5** — find the watchlist row for the asset, strike through with `~~`, and append `**EXECUTED YYYY-MM-DD HH:MM UTC+8.** [actual fill details]. Now in §2 Open Positions.`
3. **Memory.md** recompute "Portfolio heat" line under §2 using all open positions.
4. **SignalLedger** — find the asset's today-dated `Promoted` row. Set `Taken=YES`. Write the **actual** fill price into the `Notes` column (do not overwrite the originally-recommended `Entry_Price` — that is the signal-time price the performance system needs). If `Entry_Price` is blank, write the actual fill into it. Leave `Status=OPEN`.
5. **memory-lessons.md** — append one line: `YYYY-MM-DD HH:MM UTC+8: Entered {Asset} {Side} at ${price}, size ${USDT}, stop ${stop}, per {trade-rec file} v{N}.`
6. Memory.md header — update the "Last updated" line.

### B. Entry — tranche add to an existing position

1. **Memory.md §2** — update the existing row in place: add the new tranche details to the Size/Entry-price cell (e.g., `tranche 1: ... ; tranche 2: ...`). Update avg entry price.
2. **Memory.md** portfolio heat — recompute.
3. **SignalLedger** — do NOT add a new row. Update the Notes column on the asset's Taken=YES row with the tranche details. If `Entry_Price` was the first tranche, change it to the weighted-average fill and note the original first-tranche price in Notes.
4. **memory-lessons.md** — append one line naming the tranche, price, and combined size.
5. Memory.md header — update.

### C. Entry — ad-hoc promotion (the QQQ case)

Asset was a **near-miss** in the latest rec (Type=Near-Miss in SignalLedger, Taken=None) but you executed anyway because the blocking condition cleared intraday.

1. Ask the user: what changed to promote this? (correlation gate cleared / C-leg confirmed / data gap closed). Write that reason into the new row's Notes and also into the memory-lessons entry — this is evidence for the signal-review's near-miss counterfactual analysis.
2. **Memory.md §2** — append new row as in §A.
3. **Memory.md §5** — find the watchlist row, strike through, log the promotion + execution.
4. **SignalLedger** — append a **new Promoted row** with the next P### ID. Type=Promoted, Date=execution date (not the original near-miss date), same score components (S/T/C/R/Sum), Taken=YES, Status=OPEN, Entry_Price=actual fill, Notes=`promoted ad-hoc from near-miss {N###} — {reason}`.
5. **SignalLedger** — find the superseded Near-Miss row {N###}, append to its Notes column: `superseded by P### promoted ad-hoc {YYYY-MM-DD}`. Do NOT change its Status — signal-review will still mark it to market, and cross-linking via Notes prevents the stats from double-counting while preserving the original near-miss record.
6. **memory-lessons.md** — append two lines: the promotion reason, then the fill.
7. Memory.md header — update.

### D. Exit — stop hit / target hit / discretionary close / time invalidation

1. **Memory.md §2** — remove the position's row from §2.
2. **Memory.md §5** — if a watchlist row exists for the asset, update it to reflect the close and any re-entry conditions.
3. **Memory.md §7 (Closed Trades Log)** — append a row: Asset | Side | Entry/exit dates | Entry/exit prices | P&L (realized $ and %) | Thesis worked? (partial/yes/no — honest) | Lesson (one-sentence takeaway).
4. **Memory.md** portfolio heat — recompute.
5. **SignalLedger** — find the OPEN P### row for the asset. Set `Status=HIT_STOP` / `HIT_TARGET` / `EXPIRED` / `DISCRETIONARY_CLOSE`. Write `Exit_Price`, `Exit_Date` (ISO date), `Days_to_Exit` (calendar days from Date to Exit_Date), `Hypo_PnL_Pct` (same formula the signal-review uses — exit/entry − 1 for long, × 100). Leave `MAE_Pct` / `MFE_Pct` blank — signal-review will fill these Sunday from intraday price history.
6. **memory-lessons.md** — append one line: `YYYY-MM-DD: {Asset} closed {reason} at ${exit}, realized {±$X} ({±Y%}), {N} days held. Lesson: {one sentence or 'none'}.`
7. Memory.md header — update.
8. If the exit produced a methodology lesson (e.g., "stop was too tight", "time-invalidation fired before the catalyst"), ALSO write a feedback entry in `.auto-memory/feedback_*.md` so it carries across sessions. Not every exit generates an auto-memory entry — only repeated or first-of-its-kind mistakes.

### E. Adjustment — stop move

1. **Memory.md §2** — edit the row in place: update the "Stop / invalidation" cell with the new stop and a `(trailed YYYY-MM-DD)` tag.
2. **Memory.md** portfolio heat — recompute using the new stop.
3. **SignalLedger** — do NOT edit `ATR_Stop` (it preserves the signal-time plan). Append to Notes: `stop moved to ${new} {YYYY-MM-DD} — {reason: breakeven / trail / tighten / loosen}`.
4. **memory-lessons.md** — append if the adjustment is non-routine (breakeven after TP1 is routine; tightening below the methodology stop is non-routine and worth logging).
5. Memory.md header — update.

### F. Adjustment — size (trim / add, but see §B for new-tranche entries)

1. **Memory.md §2** — update Size cell. Update portfolio heat.
2. **SignalLedger** — Notes column: `size {trimmed/added} to ${new} {YYYY-MM-DD} — {reason}`.
3. **memory-lessons.md** — append if the reason is methodology-relevant.
4. Memory.md header — update.

---

## Backlog / reconciliation events

When the SignalLedger falls out of sync with Memory.md (e.g., because executions happened during sessions that didn't invoke this protocol), run a reconciliation pass:

1. Diff Memory.md §2 against SignalLedger OPEN rows.
2. For each row in §2 that has no Taken=YES counterpart: fix per §A / §B / §C.
3. For each Taken=YES OPEN row in the ledger that is not in §2: it was closed without being logged — reconstruct the exit from Memory.md §7 and apply §D.
4. Log the reconciliation in memory-lessons.md with the date and the count of rows fixed.

---

## What this protocol deliberately does NOT do

- It does **not** run the 8-step methodology. If you're reporting an execution, the decision has been made.
- It does **not** refresh the brief or trade-rec. Those run on schedule.
- It does **not** mark signals to market on price movement alone — that is signal-review's job, weekly.
- It does **not** promote watchlist rows to OPEN without an explicit user-reported fill.
- It does **not** touch `RegimeHistory`, `DailyVariables`, `DataQuality`, `CatalystLog`, `AuditAdditionLog`, `PerformanceStats`, or `VariableRegistry`. Those are owned by the scheduled skills.

---

## Why each layer matters

- **Memory.md** is the trader's working state — the bridge between sessions. If you come back tomorrow and Memory.md is wrong, every skill that reads it at startup is wrong.
- **SignalLedger** is the out-of-sample evidence base that the weekly signal-review, quarterly methodology review, and 2026-10-14 audit-addition decision all read from. A Taken=None row that was actually taken, or a Status=OPEN row that was actually closed, silently corrupts hit rates, MAE/MFE, time-to-exit, and VIX-at-entry conditioning.
- **memory-lessons.md** is the narrative audit trail. Weekly regime review reads it to spot repeated patterns.
- **auto-memory** carries lessons across Claude sessions. Without this layer, the same mistake gets re-learned every week.

---

## Changelog

- 2026-04-17: Initial protocol. Created in response to a linkage audit that found SignalLedger out of sync with Memory.md across 3 positions (EWY closed, Gold taken-flag missing, QQQ promoted ad-hoc with no ledger row).
