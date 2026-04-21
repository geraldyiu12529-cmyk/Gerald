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
4. **(Phase 3, post-2026-04-25)** Latest `/mnt/Trade/meta-additions-staging-YYYY-MM-DD.md` — read to evaluate flag F11 (overlay_sleeve_off). Extract today's per-sleeve `overlay_gate_status` (equity / commodity / crypto / international) and compare against the sleeve-at-entry recorded in Memory.md §2 Open Positions for each live row. If staging is missing, F11 fires for all positions with Severity=HIGH and `reason=OverlayStagingMissing`.

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
| F11 overlay_sleeve_off | position's sleeve is gated OFF today AND was ON at entry (i.e., flipped since entry) — per Methodology Prompt §Step 1.5 / Risk Rules §4.B | CRITICAL |

**F11 evaluation rules (Phase 3, added 2026-04-25):**

- Map each live position's asset → sleeve: equities/ETFs → equity sleeve (V033 SPY gate); EWJ/EWY → international equity (optional V033 EFA gate); commodities → commodity sleeve (V034 GSCI gate); BTC/ETH → crypto sleeve (V035 BTC-USD gate); FX and rates → not gated (F11 never fires).
- Retrieve the sleeve-status-at-entry from Memory.md §2 Notes (daily-trade-rec Phase 3 records this under the `overlay_at_entry` key; if missing on an older entry, treat as ON = prior-to-Phase-3 default).
- F11 fires only on transitions: ON-at-entry → OFF-today. A position that was entered when the sleeve was OFF (shouldn't happen post-Phase-3 because daily-trade-rec would have blocked it, but still possible for manual entries) is flagged under F8 thesis_var instead, not F11.
- Action recommendation for F11: "Sleeve overlay flipped OFF since entry — Gerald review thesis; do NOT auto-close. Consider trim or tighter stop per Risk Rules §4.B drawdown-gate interaction."
- MISSING staging → F11 fires on EVERY live position with Severity=HIGH and reason='OverlayStagingMissing' until the pipeline health is restored.

## Workflow — 7 steps

1. **Inventory** open positions from Memory.md §2.
2. **Price pull** — one batched web search per ticker.
3. **Flag panel** — compute all 10 flags.
4. **Decide** — silent OK vs. write file.
5. **Write output** (only if flags fired) following the template below.
6. **Update** `.pipeline-status.json` with status + flag list.
7. **Escalate** CRITICAL flags to 