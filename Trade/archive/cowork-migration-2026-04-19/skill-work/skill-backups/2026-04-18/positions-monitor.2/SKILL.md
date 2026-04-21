---
name: positions-monitor
description: Intraday + on-demand watchdog over Gerald's live open positions. Checks stop buffer, time-to-invalidation, earnings windows, catalyst proximity, thesis-invalidation variables, portfolio heat, and correlation gate against Memory.md §2 Open Positions. Writes a dated flag report only when at least one trigger fires (silent-when-OK). Use when Gerald says "check positions", "monitor book", "how are my positions", "are my stops OK", "portfolio heat", "anything flashing", "check the book", "positions check", "watchlist my positions", or "what's flagging on my positions". Also fires from the scheduled task `positions-monitor-intraday-9am` (Mon-Fri 09:00 UTC+8). Not for placing trades (use trade-update), not for new-entry decisions (use daily-trade-rec), not for hypothetical ledger marks (use signal-review).
---

# positions-monitor — Live book watchdog

## Purpose
Close the zero-process Monitoring bucket gap identified in `system-review-2026-04-17.md`. Provides a fast, fail-loud check on open positions that is cheap to run (silent-when-OK) and unobtrusive when nothing is wrong.

## Fail-loud philosophy
- Writes `/mnt/Trade/positions-monitor-YYYY-MM-DD.md` ONLY IF at least one flag fires.
- All-green runs: update `.pipeline-status.json` with `{status: "OK", flags: []}` and exit. Console one-liner only.
- NEVER produce a "nothing flagged" narrative file. Silence is the signal.

## REQUIRED READS (and nothing else unless triggered)
1. `/mnt/Trade/Memory.md` — §2 Open Positions, §3 Regime, §7 Closed Trades
2. `/mnt/Trade/.pipeline-status.json` (if present)
3. Latest `us-close-snapshot-YYYY-MM-DD.md` (today's 07:30 file if present)

Do NOT read the market brief, trade rec, core docs, Methodology Prompt, Risk Rules, or Data Sources. They are irrelevant at monitoring time. This skill explicitly overrides the CLAUDE.md §Session Startup Protocol for utility reasons.

## The flag panel

For each open position compute the following and mark any that fire:

| Flag | Condition | Severity |
|---|---|---|
| F1 stop_buffer | distance_to_stop / ATR_14d < 2.0 | HIGH |
| F2 stop_hit | latest_price ≤ stop (LONG) or ≥ stop (SHORT) | CRITICAL |
| F3 time_inv | days_until_time_inv_date ≤ 7 | MED |
| F4 earnings | days_until_next_earnings ≤ 2 | HIGH |
| F5 catalyst | abs(days_until_named_catalyst) ≤ 1 | HIGH |
| F6 data | unable to price within 2 tries | MED |
| F7 ah_move | abs(overnight_pct) ≥ 3% (stock) or ≥ 1% (index/commodity) | HIGH |
| F8 thesis_var | thesis-invalidation variable breached its kill level | CRITICAL |
| F9 portfolio_heat | sum of \|entry−stop\|/NAV across all positions > 6% | HIGH |
| F10 correlation_gate | two or more positions with pairwise \|ρ_60d\| > 0.7 loaded concurrently | MED |

## Workflow — 7 steps

1. **Inventory** open positions from Memory.md §2.
2. **Price pull** — one batched web search per ticker.
3. **Flag panel** — compute all 10 flags.
4. **Decide** — silent OK vs. write file.
5. **Write output** (only if flags fired) following the template below.
6. **Update** `.pipeline-status.json` with status + flag list.
7. **Escalate** CRITICAL flags to `/mnt/.auto-memory/` escalation index.

## Output template (when flags fired)

```markdown
# Positions Monitor — YYYY-MM-DD (HH:MM UTC+8)

## Flag summary
| Position | Flags fired | Severity | Action suggested |
|---|---|---|---|

## Per-position detail
### [ticker] (entry $X, stop $Y, size $Z)
- Price (latest): $XX
- Distance to stop: $X.XX (Y.Yσ ATR)
- Time-to-invalidation: YYYY-MM-DD (N days)
- Next earnings: YYYY-MM-DD (N days)
- Thesis variable status: [green/flagged/breached]
- **Recommended action:** [trim / tighten stop / hold / monitor]

## Regime / portfolio flags
[F9, F10]

## Data gaps
[F6]

## Claude's read (1-3 sentences)
```

## Scope boundaries
- Read-only observer. Does NOT modify Memory.md or place orders.
- Does NOT duplicate weekly-regime-signal-review's ledger marks (hypotheticals vs. live book).
- Does NOT produce trade recommendations. For new entries, the full brief→rec pipeline runs.

## Triggers

**Scheduled:** `positions-monitor-intraday-9am` — Mon-Fri 09:00 UTC+8. Cron `0 9 * * 1-5`. Created 2026-04-17.

**On-demand phrases:** "check positions", "monitor book", "how are my positions", "are my stops OK", "portfolio heat", "anything flashing", "check the book", "positions check", "watchlist my positions", "what's flagging".

## Wall-clock target
~5–8 minutes end-to-end on a healthy day. All-green path is ~2–3 minutes.

## Why this skill exists
Before 2026-04-17, nothing in the pipeline watched for stop-breach, thesis-invalidation, or time-inv clock on live positions. Detection was entirely reactive (us-close-snapshot + Gerald's vigilance). EWY was stopped out 2026-04-16 on an over-tightened stop that was never cross-checked against the methodology's $133 level — the deviation surfaced only in post-mortem. This skill is the structural fix.
