---
name: slack-ingest
description: "Pull recent posts from the Slack #trading-scheduled-updates channel and write them to a local digest file for downstream consumption by market-brief, daily-trade-rec, and positions-monitor. Use for 'ingest slack', 'pull slack updates', 'sync slack'. Also auto-called as Step 0 of /market-brief, /daily-trade-rec, and /positions-monitor."
allowed-tools: Read Write Bash(python3 *) mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_search_channels mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_read_channel
metadata:
  model: sonnet
---
# Slack Ingest
One-way pull: Slack scheduled-agent posts → local `{YYYY-MM-DD}/slack-digest-{date}.md`. The cloud agent fires 4x/day while the local machine may be off — this skill is what brings those intraday observations (regime pulses, position alerts, thesis breaches) into the local pipeline.
Local timezone UTC+8. Canonical channel name: `trading-scheduled-updates`.
---
## Step 1 — Resolve channel ID
```
slack_search_channels(query="trading-scheduled-updates")
```
Pick the exact-name match. If no match: write a digest file with body `CHANNEL NOT FOUND — configure #trading-scheduled-updates and re-run.` and stop.
## Step 2 — Pull last 24h of messages
```
slack_read_channel(channel_id=<id>, limit=100, response_format="concise")
```
Filter client-side:
- Keep messages with timestamps within the last 24h (UTC+8 day boundary is fine; cloud agent timestamps are UTC).
- Drop bot system messages (channel_join, etc.).
- Preserve original author, timestamp, and full text.
If >100 messages in the window, paginate via cursor.
## Step 3 — Categorize
Each message carries a leading tag from the cloud agent:
| Tag | Meaning | Priority |
|---|---|---|
| `[POSITION-ALERT]` | Stop buffer, thesis breach, vol-band-violation — requires local action | **HIGHEST** |
| `[ACTION-ITEMS]` | One concrete action per open position (synthesized by cloud agent) | **HIGHEST** |
| `[REGIME]` | Intraday regime pulse — VIX/MOVE/DXY/US10Y/CDX-HY/SPY readings | HIGH |
| `[THESIS]` | Thesis-variable delta for a named open position | HIGH |
| `[POTENTIAL-TRADES]` | Watchlist candidates + intraday setups flagged by cloud agent | MED |
| `[NEWS]` | News capture | MED |
| `[POSITION-STATE]` | Snapshots YOU pushed up — **ignore, do not ingest back** | — |
Untagged messages go under "Unclassified".
**For `[POSITION-ALERT]` messages:** extract and preserve:
- Ticker symbol (match against open positions)
- Alert sub-type if present: `vol-band-violation`, `thesis-breach`, `stop-buffer`, `catalyst-proximity`
- Timestamp (positions-monitor cites this for F12/F13 lineage)
**For `[REGIME]` messages:** extract and preserve the specific variable readings (VIX, MOVE, DXY, US10Y, CDX-HY, SPY values and direction) — market-brief Step 4 compares these against its own pull to detect staleness.
## Step 4 — Write digest
Path: `{YYYY-MM-DD}/slack-digest-{YYYY-MM-DD}.md` where `{YYYY-MM-DD}` is today in UTC+8. Create folder first: `mkdir -p {YYYY-MM-DD}`.
```markdown
# Slack Digest — {date} (ingested {ingest-time-utc+8})
Source channel: #trading-scheduled-updates
Window: last 24h ending {ingest-time}
Messages: {N} total ({alert-count} alerts, {regime-count} regime pulses)
## ⚠ Position Alerts [POSITION-ALERT]
[Surface FIRST if any exist — these gate new trade entries and trigger F12/F13 in positions-monitor.
 Format per alert: `{timestamp} | {ticker} | {sub-type} | {full message text}`
 If none: "No position alerts in window."]
## Action Items [ACTION-ITEMS]
[One action item per open position as synthesized by the cloud agent.
 Format: `{timestamp} | {ticker}: {action verb} — {numbers/rationale}`
 If none: "No action items in window."]
## Regime Pulse [REGIME]
[REGIME-tagged messages, newest first.
 Format: `{timestamp} | VIX={x} MOVE={x} DXY={x} US10Y={x} CDX-HY={x} SPY={x} | {direction/label}`
 Preserve numeric readings verbatim — market-brief Step 4 uses these for cross-check.]
## Thesis Variable Deltas [THESIS]
[THESIS-tagged messages, newest first.]
## News [NEWS]
[NEWS-tagged messages.]
## Potential Trades [POTENTIAL-TRADES]
[Watchlist candidates + intraday setups flagged by cloud agent.
 Format: `{timestamp} | {asset} {long|short}: trigger {x} | invalidation {y} | {why now}`
 If none: "No potential trades flagged in window."]
## Unclassified
[Messages without known tags.]
## Narrative Summary
[3–5 sentence synthesis written by Claude after reviewing all sections above. Cover:
 1. Regime status — what the most recent pulse says about market conditions and any flip since prior fire.
 2. Position health — whether any open positions are under pressure (alert or action-item driven); if all clear, say so.
 3. Opportunity read — whether any potential trade candidates are worth elevating to the next local session; note the strongest one if any.
 4. Any data gaps or anomalies (missing Grade A data, no POSITION-STATE in 72h, etc.).
 Keep it decision-focused. No padding. No repeating numbers already in the sections above — synthesize, don't restate.]
```
If zero messages in window: write a minimal file with body `No scheduled-update posts in last 24h window.` and exit.
## Step 5 — Report
One-line summary: `slack-digest written: N messages — {alert-count} POSITION-ALERTs, {action-count} ACTION-ITEMs, {regime-count} REGIME pulses, {news-count} NEWS, {trade-count} POTENTIAL-TRADEs`. Then output the Narrative Summary from the digest on the next line so the caller sees the key read at a glance.
---
## Downstream contract
Three skills consume `{today}/slack-digest-{today}.md`:
| Skill | What it reads | Treatment |
|---|---|---|
| `/market-brief` Step 4 | `[REGIME]` entries — compares numeric readings against its own Grade A pull | Digest = authoritative for last-observed value between runs; brief = authoritative for 20:00 canonical snapshot. Discrepancy >1σ → staleness flag. |
| `/daily-trade-rec` Step 5 item 7 | `[POSITION-ALERT]` entries — gates new entries in the same sleeve | Unresolved vol-band-violation or thesis-breach → blocks new sleeve entries until re-evaluated via trade-update. |
| `/positions-monitor` Step 2 | `[POSITION-ALERT]` entries — drives F12 (vol_band) and F13 (cloud_alert) flags | Timestamps cited in flag output for lineage back to cloud agent. |
All three treat a missing digest as non-fatal (Grade B optional context) — but invoke `/slack-ingest` proactively so the digest is present before their reads.
