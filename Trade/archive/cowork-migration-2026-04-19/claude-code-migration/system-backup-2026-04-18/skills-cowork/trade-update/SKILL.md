---
name: trade-update
description: On-demand skill that syncs Memory.md, master-data-log.xlsx (SignalLedger), memory-lessons.md, and auto-memory whenever Gerald reports a trade execution event — entries, exits, stop moves, tranche adds, size trims, or ad-hoc near-miss promotions. Use when the user says 'I entered X', 'I bought X', 'I sold X', 'filled X at $Y', 'opened X', 'added to X', 'scaled into X', 'stopped out of X', 'stop hit on X', 'hit target on X', 'TP1 on X', 'took profit on X', 'closed X', 'cut X', 'invalidated X', 'time-stop on X', 'moved stop on X to $Y', 'stop to breakeven', 'trailed stop on X', 'trimmed X', 'reduced X', or 'sized up X'. Also use for 'reconcile the ledger', 'sync memory and ledger', 'backlog update on trades', or 'log a trade after the fact'. Not for placing trades, the daily rec/brief, or weekly signal mark-to-market — use those skills/tasks instead.
---

# Trade Update

Executes the event-driven update sequence defined in `/mnt/Trade/Trade-Execution-Protocol.md` whenever Gerald reports a real-money fill, exit, or adjustment on a position. The planning pipeline (brief → news → trade-rec → signal-review) runs on a schedule; executions do not. This skill is the bridge.

The core principle: **one execution event = four layers updated, in order, with no batching**. Memory.md first (it is the trader's canonical working state), then SignalLedger (the analytical record), then memory-lessons.md (the narrative log), then auto-memory (only if the event reveals a cross-session pattern).

---

## When This Skill Runs

Only interactively. There is no scheduled trigger. Gerald reports the event in natural language; the skill:

1. Parses the event type from the trigger phrase.
2. Fails loud if anything is ambiguous (which asset? which signal ID? what fill price?).
3. Reads the protocol, Memory.md, and SignalLedger to establish what should change.
4. Writes every layer before returning control.

If the user is reporting several events at once ("I got stopped on EWY and added to Gold"), treat them as separate events and process them one at a time — do not batch writes across events.

---

## Step 1 — Read the protocol and current state

Always read these three first:

```
Read /mnt/Trade/Trade-Execution-Protocol.md      # the authoritative procedure
Read /mnt/Trade/Memory.md                         # §2 Open Positions, §5 Watchlist, §7 Closed Trades Log
Read /mnt/Trade/master-data-log.xlsx → SignalLedger sheet  # find the row(s) to update
```

Use openpyxl for the xlsx read:

```python
from openpyxl import load_workbook
wb = load_workbook('/mnt/Trade/master-data-log.xlsx', data_only=False)
sl = wb['SignalLedger']
headers = [c.value for c in sl[1]]
rows = [{headers[i]: c.value for i, c in enumerate(r)} for r in sl.iter_rows(min_row=2)]
```

Do NOT skip these reads even if the event feels obvious. The protocol is the spec; drifting from it silently corrupts the performance record that feeds the 2026-10-14 audit review.

---

## Step 2 — Classify the event

Map the trigger phrase to the event type in the protocol:

| Phrase class | Event type | Protocol section |
|---|---|---|
| "I entered / bought / filled / opened" (asset is on today's promoted list) | Entry — fresh | §A |
| "I entered / bought / filled" (asset is a near-miss or not in today's rec) | Entry — ad-hoc promotion | §C |
| "added to / scaled into / second tranche" | Entry — tranche add | §B |
| "stopped out / stop hit" | Exit — stop | §D |
| "hit target / TP1 / took profit" | Exit — target | §D |
| "closed / cut / invalidated / time-stop" | Exit — discretionary / time | §D |
| "moved stop / stop to breakeven / trailed stop" | Adjustment — stop | §E |
| "trimmed / reduced / sized up" (without a new tranche price) | Adjustment — size | §F |

If the phrase does not cleanly map, ask the user which event type applies. Do not guess.

---

## Step 3 — Fail-loud ambiguity check

Before writing anything, confirm all five of these are unambiguous:

1. **Asset** — exact ticker or contract (QQQ vs QQEW, Gold futures GC vs GLD ETF).
2. **Side** — long or short.
3. **Price** — actual fill price (for entries/exits) or new stop level (for adjustments).
4. **Time** — the execution timestamp in UTC+8. If the user gave a relative time ("an hour ago"), convert to absolute.
5. **SignalLedger linkage** — for exits and adjustments, which signal ID (P### or N###) the event refers to. For entries, whether the asset is on today's promoted list, a near-miss, or net new.

If any of the five is unclear, STOP and ask. Never guess. The protocol is explicit: a silent wrong update corrupts the out-of-sample evidence base.

Helpful clarifying questions:
- "Which signal ID does this refer to — P00X (the {Date} {Sum}/5 entry) or something else?"
- "Was this the first tranche or an add to the existing position opened on {Date}?"
- "What was the actual fill price? I'll write that into Notes and preserve the original signal-time price in Entry_Price so the performance stats stay comparable."
- "Is this the Gold futures (GC1!) signal or the GLD ETF? There are two open Gold rows in the ledger."

---

## Step 4 — Apply the four layers, in order

Follow the protocol section that matches the event type. Every event touches these four layers in exactly this order. Do not reorder.

### Layer 1 — Memory.md

Edit `/mnt/Trade/Memory.md` in place. Touch the right sections:
- **Entries**: append a new row to §2 Open Positions; strike through and annotate the §5 Watchlist row if one exists.
- **Exits**: remove the row from §2; append a full-accounting row to §7 Closed Trades Log (entry/exit dates and prices, realized $ and %, thesis-worked verdict, one-line lesson).
- **Stop / size adjustments**: edit the §2 row in place (Stop cell with `(trailed YYYY-MM-DD)` tag, or Size cell).
- **Portfolio heat**: recompute the portfolio-heat line under §2 after any entry, exit, size change, or stop move.
- **Header**: update the "Last updated" timestamp on every write.

### Layer 2 — SignalLedger (master-data-log.xlsx)

Open the workbook with openpyxl, edit the relevant row, save.

| Event | Action on the ledger |
|---|---|
| Fresh entry (promoted) | Find today's Promoted row for the asset. `Taken=YES`. Write actual fill into Notes. Do NOT overwrite `Entry_Price` if already set — that is the signal-time price. If blank, write actual fill. `Status=OPEN`. |
| Ad-hoc promotion | Append a **new Promoted row** with next P### ID. Type=Promoted, Date=execution date, same S/T/C/R/Sum as the near-miss, Taken=YES, Status=OPEN, Entry_Price=actual fill, Notes=`promoted ad-hoc from near-miss {N###} — {reason}`. Then cross-link: on the superseded N### row, append to Notes `superseded by P### promoted ad-hoc {YYYY-MM-DD}`. Do NOT change N###'s Status. |
| Tranche add | No new row. Update the existing Taken=YES row's Notes. If Entry_Price was the first tranche, change it to the weighted-average fill and preserve the original first-tranche price in Notes. |
| Exit | Find the OPEN row. Set `Status` (HIT_STOP / HIT_TARGET / EXPIRED / DISCRETIONARY_CLOSE), write `Exit_Price`, `Exit_Date` (ISO date), `Days_to_Exit` (calendar days), `Hypo_PnL_Pct` (exit/entry − 1 for long, × 100; reverse for short). Leave MAE_Pct and MFE_Pct blank — signal-review fills those Sunday. |
| Stop move | Do NOT edit `ATR_Stop` (it preserves the signal-time plan). Append to Notes: `stop moved to ${new} {YYYY-MM-DD} — {reason}`. |
| Size change | Notes: `size {trimmed/added} to ${new} {YYYY-MM-DD} — {reason}`. |

Save the workbook: `wb.save('/mnt/Trade/master-data-log.xlsx')`.

If multiple OPEN rows exist for the same asset (e.g., two Gold signals), the user must disambiguate by signal ID — the protocol's fail-loud rule applies.

### Layer 3 — memory-lessons.md

Append one line to `/mnt/Trade/memory-lessons.md`. Keep it factual and terse. The exact format depends on event type (see protocol §A–§F), but every entry begins with `YYYY-MM-DD HH:MM UTC+8:` and names the asset, the event, the price(s), and the driving reason.

For ad-hoc promotions write two lines: the promotion reason, then the fill.

For adjustments, only append if non-routine (breakeven-after-TP1 is routine and does not need a line; tightening below the methodology stop is non-routine and does).

### Layer 4 — auto-memory (conditional)

Only write here if the event reveals a repeated or first-of-its-kind pattern that should carry across sessions. Not every execution generates one. Examples that warrant an auto-memory entry:

- First time a stop was tightened below the methodology ATR stop — write a feedback_* memory capturing the rule and the reason.
- First observed case of a near-miss being correctly promoted ad-hoc with a clear C-leg trigger — write a project_* memory with the pattern.
- Repeated time-stop invalidations on the same asset class — write a feedback_* memory flagging the pattern so next week's regime review picks it up.

Format: standalone file in `/mnt/.auto-memory/` with frontmatter (name, description, type), plus a one-line pointer in `/mnt/.auto-memory/MEMORY.md`. Keep the `**Why:**` and `**How to apply:**` lines for feedback and project types.

---

## Step 5 — Confirm and report

After all four layers are written (or three, if no auto-memory entry was warranted), return a brief confirmation to the user that names:

1. What event was recorded.
2. Which signal ID(s) it mapped to.
3. What the new portfolio heat is.
4. Any follow-up the user should be aware of (e.g., "EWY stop to breakeven also freed 0.4% of portfolio heat — you now have room for one more entry under the 6% cap").

Do not re-summarize the full protocol or list every file you touched. Gerald can diff the files if he wants.

---

## Reconciliation mode

If the user asks to "reconcile the ledger", "sync memory and ledger", or "fix the backlog", run protocol §Backlog / reconciliation events:

1. Diff Memory.md §2 against SignalLedger OPEN rows.
2. For each §2 row with no Taken=YES counterpart: classify (fresh / tranche / ad-hoc) and apply §A / §B / §C.
3. For each Taken=YES OPEN row not in §2: it was closed without being logged — reconstruct the exit from Memory.md §7 and apply §D.
4. Log the reconciliation in memory-lessons.md with the date and the count of rows fixed.

Reconciliation mode is the only time this skill writes multiple events in one session. Even then, process them in a deterministic order (oldest first) and save the workbook after each event, not at the end.

---

## What this skill deliberately does NOT do

- Does **not** run the 8-step methodology. If you are reporting an execution, the decision has been made. Use `daily-trade-rec` for fresh decisions.
- Does **not** refresh the brief or trade-rec. Those run on schedule.
- Does **not** mark signals to market on price movement alone. That is `signal-review`'s job, weekly.
- Does **not** promote watchlist rows to OPEN without an explicit user-reported fill. The user must say "I entered" or equivalent.
- Does **not** touch `RegimeHistory`, `DailyVariables`, `DataQuality`, `CatalystLog`, `AuditAdditionLog`, `PerformanceStats`, or `VariableRegistry`. Those are owned by the scheduled skills.
- Does **not** place orders or move money. Gerald executes every trade himself; this skill only records what he did.

---

## Error handling

- **SignalLedger row not found**: fail loud. Ask the user for the signal ID or to confirm the asset. Do NOT create a speculative row.
- **Memory.md §2 row missing for an exit**: fail loud. The position may have been opened in a session that did not run the protocol — offer to run reconciliation mode.
- **openpyxl save error**: retry once with `data_only=False`. If still failing, report the error, leave Memory.md and memory-lessons.md unchanged, and ask the user to inspect the xlsx manually. Do not apply a partial update.
- **Asset has two matching OPEN rows**: fail loud. Ask the user for the signal ID. The protocol is explicit about this case.

---

## Changelog

- 2026-04-17: Initial skill. Created to close the gap between event-driven executions and the scheduled planning pipeline. Invokes `Trade-Execution-Protocol.md` as the authoritative procedure.
