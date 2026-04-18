---
name: Trade execution events must invoke the trade-update skill
description: Every real-money entry, exit, or adjustment is event-driven and must run the 4-layer protocol — never batch, never skip the ledger, never guess ambiguity
type: feedback
---

When Gerald reports a trade execution in natural language (entry, exit, stop move, tranche add, size trim, or ad-hoc near-miss promotion), invoke the `trade-update` skill. It reads `/mnt/Trade/Trade-Execution-Protocol.md` and applies the four-layer update in order: Memory.md → master-data-log.xlsx (SignalLedger) → memory-lessons.md → auto-memory (conditional).

**Why:** A 2026-04-17 linkage audit found the SignalLedger out of sync with Memory.md across three positions (EWY closed but Status=OPEN, Gold taken but Taken=None, QQQ promoted ad-hoc with no ledger row). The scheduled skills (daily-trade-rec, signal-review) only handle rec-time appends and weekly hypothetical mark-to-market — neither covers event-driven fills. Without a dedicated skill and protocol, the out-of-sample evidence base that feeds the weekly signal-review, the quarterly methodology review, and the 2026-10-14 audit-addition decision silently degrades with every unlogged execution.

**How to apply:**
- Any message matching the protocol's trigger-phrase table (`I entered`, `stopped out`, `hit target`, `moved stop to`, `added to`, `trimmed`, etc.) routes through the trade-update skill, not through ad-hoc edits.
- Fail loud on the five ambiguity axes (asset, side, price, time, signal-ID linkage) — never guess which P### or N### row the event maps to.
- Do NOT overwrite `Entry_Price` on Taken=YES rows with the actual fill — that column is the signal-time price the performance system relies on. Write the actual fill to Notes and to a secondary `Entry_Price` only if blank.
- Do NOT edit `ATR_Stop` when Gerald moves a stop — it preserves the signal-time plan. Append the new stop level to Notes.
- Ad-hoc promotions of near-misses get a **new** P### Promoted row on the execution date, and the superseded N### row is cross-linked via Notes without changing its Status.
- Reconciliation mode (diff §2 vs OPEN rows, fix both directions) is only for backlog; normal events process one at a time.
- Do not run the 8-step methodology, refresh the brief, or mark anything to market inside this skill — those are owned by other skills and tasks.
