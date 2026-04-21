---
name: slack-ingest
description: Slack ingest 4×/day — pull #trading-scheduled-updates into local slack-digest-{date}.md (midnight, 8am, 12pm, 4pm UTC+8)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

Pull the last 24 hours of posts from Slack #trading-scheduled-updates AND today's and yesterday's cloud market brief, news, and trade rec from Google Drive. Synthesize into a single structured digest posted back to #trading-scheduled-updates.

---
## PART A — Pull Cloud Pipeline Files (Google Drive)

For each of the following file patterns, search Google Drive for today ({YYYY-MM-DD}) first, then yesterday ({YYYY-MM-DD minus 1}) as fallback. Use UTC+8 dates.

Files to retrieve:
1. Market brief: filename contains "market-brief-{date}"
2. News: filename contains "news-{date}"
3. Trade rec: filename contains "trade-rec-{date}"

For each file:
- Use search_files(query="market-brief-{date}") (and news, trade-rec variants)
- If found: use read_file_content(file_id=<id>) to pull full text
- If not found for today, try yesterday's date
- If neither found: mark as MISSING — note in digest

---
## PART B — Pull Slack #trading-scheduled-updates

Step 1 — Resolve channel ID
slack_search_channels(query="trading-scheduled-updates"). Exact-name match only.
If not found: post "CHANNEL NOT FOUND" and stop.

Step 2 — Pull last 24h
slack_read_channel(channel_id=<id>, limit=100, response_format="concise")
- Keep messages within last 24h (UTC+8 boundary)
- Drop bot system/join messages
- Preserve author, timestamp, full text
- Paginate if >100 messages

Step 3 — Categorize Slack messages by tag
| Tag | Priority |
|---|---|
| [POSITION-ALERT] (stop buffer, thesis-breach, vol-band-violation) | HIGHEST |
| [ACTION-ITEMS] (one concrete action per open position) | HIGHEST |
| [REGIME] (VIX/MOVE/DXY/US10Y/CDX-HY/SPY readings) | HIGH |
| [THESIS] (thesis-variable delta for named position) | HIGH |
| [POTENTIAL-TRADES] (watchlist candidates + intraday setups) | MED |
| [NEWS] | MED |
| [POSITION-STATE] — IGNORE, do not ingest back | — |
Untagged → Unclassified.

---
## PART C — Post Digest to #trading-scheduled-updates

Use slack_send_message. Format:

[SLACK-DIGEST] {YYYY-MM-DD} | {N} Slack messages — {alert} POSITION-ALERTs, {action} ACTION-ITEMs, {regime} REGIME pulses, {news} NEWS, {trade} POTENTIAL-TRADEs

📄 PIPELINE FILES INGESTED
- Market Brief: {date found} ✓ | or MISSING
- News: {date found} ✓ | or MISSING
- Trade Rec: {date found} ✓ | or MISSING

⚠ POSITION ALERTS
{timestamp} | {ticker} | {sub-type} | {full text}
(or "None")

ACTION ITEMS
{timestamp} | {ticker}: {action} — {numbers/rationale}
(or "None")

REGIME PULSE (newest first — cross-check against market brief if available)
{timestamp} | VIX={x} MOVE={x} DXY={x} US10Y={x} CDX-HY={x} SPY={x} | {direction}
If market brief available: note any divergence >1σ from brief's canonical readings.

THESIS DELTAS
{list or "None"}

POTENTIAL TRADES
{timestamp} | {asset} {long|short}: trigger {x} | invalidation {y} | {why}
(or "None")

NEWS
{list or "None"}

NARRATIVE
5–7 sentences covering:
1. Regime status — most recent pulse vs market brief canonical reading; flag any flip or divergence
2. Trade rec alignment — does the cloud trade rec conflict with any open position alerts?
3. Position health — any under pressure or all clear
4. Strongest trade candidate from POTENTIAL-TRADES or trade rec if any
5. Pipeline gaps — which files were MISSING and what that blocks downstream

If zero Slack messages AND all files missing: post "[SLACK-DIGEST] No pipeline data in last 24h window — all sources empty."