---
name: positions-monitor
description: "Intraday watchdog — stop buffer, time-invalidation, earnings, catalyst, thesis variables, portfolio heat, correlation gate. Silent-when-OK. Use for 'check positions', 'monitor book', 'are my stops OK', 'portfolio heat', 'anything flashing'."
model: haiku
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Positions Monitor — Live Book Watchdog

Silent-when-OK. Writes `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` ONLY if flags fire. Create folder first: `mkdir -p {YYYY-MM-DD}`.

## Reads (and nothing else)
1. `framework/Memory.md` — §2 Open Positions, §7 Closed Trades
2. `pipeline/.pipeline-status.json` (if present)
3. Latest `*/us-close-snapshot-*.md` (date-folder convention; falls back to root `us-close-snapshot-*.md` if none)
4. `{today}/slack-digest-{today}.md` if present (cloud scheduled-agent POSITION-ALERTs, THESIS breaches, vol-band-violation flags). Invoke `/slack-ingest` if digest missing — the cloud agent fires 4x/day while local machine may be off, and its alerts must propagate into local flag panel.

Do NOT read framework/Methodology Prompt.md, framework/Risk Rules.md, cores, framework/Data Sources.md. Overrides startup protocol.

## Flag Panel

| Flag | Condition | Severity |
|---|---|---|
| F1 stop_buffer | distance_to_stop / ATR_14d < 2.0 | HIGH |
| F2 stop_hit | price ≤ stop (long) or ≥ stop (short) | CRITICAL |
| F3 time_inv | days_until_inv_date ≤ 7 | MED |
| F4 earnings | days_until_earnings ≤ 2 | HIGH |
| F5 catalyst | abs(days_until_catalyst) ≤ 1 | HIGH |
| F6 data | unable to price within 2 tries | MED |
| F7 ah_move | abs(overnight_pct) ≥ 3% (stock) or 1% (index/commodity) | HIGH |
| F8 thesis_var | thesis-invalidation variable breached kill level | CRITICAL |
| F9 portfolio_heat | total |entry−stop|/NAV > 6% | HIGH |
| F10 correlation_gate | pairwise |ρ_60d| > 0.7 | MED |
| F11 cot_crowding | commodity position: COT speculative net longs > 2σ above 52w average (search "COT report {commodity} latest") | MED |
| F12 vol_band | cloud scheduled agent flagged vol-band-violation in digest `[POSITION-ALERT]` (methodology stop tightened below 1h-RV band per ABDL 2001 / BPV 2016 Grade A) | HIGH |
| F13 cloud_alert | any other `[POSITION-ALERT]` from digest not already covered by F1–F12 | MED |

## Workflow — 8 steps

1. **Inventory** positions from `framework/Memory.md` §2
2. **Ingest slack digest** (`/slack-ingest` if missing) — parse `[POSITION-ALERT]` entries, match to open positions by ticker
3. **Price pull** — batched WebSearch per ticker
4. **Compute all 13 flags** (F12/F13 from digest alerts; F1–F11 from local data)
5. **If all green:** update `pipeline/.pipeline-status.json` with OK, exit silently
6. **If flags:** write `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` (`mkdir -p` first) with flag table + per-position detail. Cite digest `[POSITION-ALERT]` timestamps for F12/F13 so lineage back to cloud agent is explicit.
7. **Update** `pipeline/.pipeline-status.json`
8. **Escalate** CRITICAL flags to `/mnt/.auto-memory/`

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
- Cloud alert source: [digest timestamp if F12/F13 fired]
- **Recommended action:** [trim / tighten stop / hold / monitor]

## Regime / portfolio flags
[F9, F10]

## Cloud alerts (F12/F13)
[digest [POSITION-ALERT] entries with timestamps]

## Data gaps
[F6]

## Claude's read (1-3 sentences)
```

## Scope boundaries
- Read-only observer. Does NOT modify Memory.md or place orders.
- Does NOT duplicate weekly-regime-signal-review's ledger marks.
- Does NOT produce trade recommendations. For new entries, the full brief→rec pipeline runs.

## Triggers
**Scheduled:** `positions-monitor-intraday-9am` — Mon-Fri 09:00 UTC+8.
**On-demand:** "check positions", "monitor book", "are my stops OK", "portfolio heat", "anything flashing", "check the book", "positions check".
