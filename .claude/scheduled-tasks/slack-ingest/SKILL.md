---
name: slack-ingest
description: Slack ingest 4×/day — pull #trading-scheduled-updates + GDrive pipeline files, save full local digest, post 5-paragraph plain-English summary to Slack (midnight, 8am, 12pm, 4pm UTC+8).
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...`.

---

Pull the last 24 hours of posts from Slack #trading-scheduled-updates AND today's cloud pipeline files from Google Drive. Extract ALL data. Save a comprehensive local digest. Post a 5-paragraph plain-English summary to Slack.

---
## PART A — Pull Cloud Pipeline Files (Google Drive)

Search Google Drive for today ({YYYY-MM-DD}) first, then yesterday as fallback. Use UTC+8 dates.

Files to retrieve:
1. `search_files(query="market-brief-{date}")` → `read_file_content(file_id=<id>)` → hold as `pipeline_brief`
2. `search_files(query="news-{date}")` → `read_file_content(file_id=<id>)` → hold as `pipeline_news`
3. `search_files(query="trade-rec-{date}")` → `read_file_content(file_id=<id>)` → hold as `pipeline_rec`

If not found for today → try yesterday. If neither → mark MISSING and continue.

**From `pipeline_brief` extract:**
- Regime label + change vs prior day
- Overlay gate status: SPY, QQQ, GSCI, BTC (ON or OFF, price vs 10m-SMA)
- Full variable table with all readings and directions (VIX, MOVE, DXY, US10Y, ACM term premium, CDX-HY, SPY vs 200d-MA, intermediary capital z-score)
- Crypto variables: BTC active addresses, BTC 3m basis, perp funding rate, ETF net flow
- Audit addition readings: V026 residual momentum (status + value), V027 intermediary capital (z-score + R adjustment), V028 basis-momentum (divergence-cap fired?)
- Per-asset S/T/C/R/Sum scorecard (all assets)
- Grade A data gaps listed

**From `pipeline_rec` extract:**
- Per-asset Sum scores and any promotions (N→P, or new P###)
- Pre-entry checklist: ALL PASS or FAILED (which rules)
- Any recommended positions: asset, direction, entry, stop, target, size %
- Risk budget: current heat %
- Any NO TRADE decisions and blocking reasons
- Near-misses (|Sum|=2): asset, missing leg, specific trigger needed

**From `pipeline_news` extract:**
- All items per category (geopolitics, macro, earnings, crypto, credit, flash)
- Catalyst calendar changes (next 48h additions or removals)

---
## PART B — Pull Slack #trading-scheduled-updates

Step 1 — Resolve channel:
Channel ID: C0AUCTQSC65 (#trading-scheduled-updates, private).
If the ID fails, re-resolve via slack_search_channels(query="trading-scheduled-updates", channel_types="public_channel,private_channel"). Exact-name match only.
If not found: post "CHANNEL NOT FOUND" and stop.

Step 2 — Pull last 24h:
`slack_read_channel(channel_id=<id>, limit=100, response_format="concise")`
Keep messages within last 24h (UTC+8 boundary). Drop bot join messages. Preserve author, timestamp, full text. Paginate if >100.

Step 3 — Categorize by tag:
| Tag | Priority | Content |
|-----|----------|---------|
| [POSITION-ALERT] | HIGHEST | stop buffer breach, thesis-breach, vol-band-violation |
| [ACTION-ITEMS] | HIGHEST | one concrete action per open position |
| [REGIME] | HIGH | VIX/MOVE/DXY/US10Y/CDX-HY/SPY numeric readings |
| [THESIS] | HIGH | thesis-variable delta for named position |
| [POTENTIAL-TRADES] | MED | watchlist candidates + intraday setups |
| [NEWS] | MED | any market news |
| [POSITION-STATE] | IGNORE | do not ingest back |
Untagged → Unclassified.

---
## METHODOLOGY FRAMEWORK (scoring reference — used to synthesise the Slack post)

### EVIDENCE GRADES
- Grade A = replicated, long history, coherent mechanism (momentum, carry, credit spreads, active addresses, term premium, intermediary capital)
- Grade B = moderate, regime-dependent (funding rate direction, options skew, MVRV/SOPR, exchange flows)
- Grade C = weak/anecdotal (stock-to-flow, halving cycles, pure seasonality) — never use as triggers
- Fail-loud on missing Grade A data — never silently infer

### STEP 1 — REGIME IDENTIFICATION
- Risk-On = macro supports buying; financial conditions loose; risk sentiment positive
- Risk-Off = macro deteriorating; financial conditions tightening; credit stress; VIX elevated
Key variables: VIX (B), MOVE (A), HY OAS (B), DXY (A), NFCI (A)

### STEP 1.5 — OVERLAY GATE (Faber TAA, Grade A, PL-NMA rank 2/54)
Monthly sleeve switch: SPY/QQQ, GSCI, BTC, EFA each vs 10m-SMA. If below → sleeve OFF → no new longs that sleeve. Sum still computed; position size = 0.

### STEP 2 — STRUCTURAL ANCHOR (S: +1/0/−1)
Equities: valuation spread, GP/A (V031 A), CEI (V032 A — high issuance = headwind), revision breadth, BAB (V029 A).
Commodities: inventory levels, curve slope, basis-momentum (V028 A — cap S at 0 if backwardation but basis-mom flattening).
BTC/ETH: active addresses, hash rate, MVRV (context only).

### STEP 3 — TACTICAL CONFIRMATION (T: +1/0/−1)
Single stocks: residual momentum V026 (A) — score V026 only, not V009.
ETFs/indices/commodities/crypto: raw 12m TSMOM V009 (A).

### STEP 4 — CATALYST MAP (C: +1/0/−1) — never blank.

### STEP 5 — RISK OVERLAY (R: +1/0/−1)
V027 intermediary capital z < −1σ → downgrade R one notch all longs (fires before CDX-HY).
Double-count gate: V027 + CDX-HY stress together → count once.
V030 DealerGamma (B): short-gamma → widen stops; long-gamma → tighten.

### SUM THRESHOLDS
|Sum| ≥ 3 → promoted. |Sum| = 2 → near-miss. |Sum| ≤ 1 → no trade.
Correlation gate: BTC+ETH ≈ one bet. Gold+Silver+Copper = one reflation theme.

---
## PART C — Post to #trading-scheduled-updates

Use slack_send_message (channel_id=C0AUCTQSC65, #trading-scheduled-updates, private; if the ID fails, re-resolve via slack_search_channels(query="trading-scheduled-updates", channel_types="public_channel,private_channel")). One message, five paragraphs. No tables. No headers. Plain text only. Each paragraph interprets the data in plain English — explain what it means, not just paste numbers. Write like you're explaining to a smart friend who doesn't follow markets daily. Keep each paragraph to 3–5 sentences max.

Format:
```
[DIGEST] {YYYY-MM-DD} {HH:MM} UTC+8

Market: {One paragraph — what is the market doing right now and why does it matter? State the regime (Risk-On/Off/Neutral), explain what the key variables are telling you in plain terms (e.g. "Fear is elevated but easing" not "VIX = 22"), and say whether conditions favour adding risk or staying cautious.}

Event: {One paragraph — what is the single most important thing that happened in the last 24h? Explain what it is, why it matters for the portfolio, and what to watch for next. No raw headlines — interpret the impact.}

Notable: {One paragraph — anything else worth knowing: a data gap blocking a decision, a sleeve gate that just flipped, unusual vol, a near-miss trade, or carry stress building. If nothing: "Nothing unusual to flag — conditions are within normal range."}

Trades: {One paragraph — how are the open positions doing? For each position, say whether it's on track or under pressure, whether the stop is still comfortable, and if there's any catalyst coming that could force a decision. Write as a narrative, not a list.} — or "No open positions currently."

Rec: {One paragraph — if there is a new trade recommendation, explain what it is, why the evidence supports it in plain terms, and what would make you exit. If no new rec, explain what's closest to triggering and what specific thing needs to happen to get there.}
```

If POSITION-ALERT exists: prepend `⚠ ALERT: {ticker} — {sub-type}: {one sentence on what happened and what action is needed}` as the very first line.
If Slack fails: retry once, then stop.

---
## SAVE DIGEST TO LOCAL FILE

Write the complete extracted data (Parts A + B in full) to:
`{YYYY-MM-DD}/slack-digest-{YYYY-MM-DD}-{HH}{MM}.md`

If a file for today already exists, append below a `---` divider with a `## {HH:MM} UTC+8 refresh` heading. Do not overwrite prior runs.

---
## ZERO-DATA FALLBACK

If zero Slack messages AND all pipeline files missing: post "[DIGEST] {YYYY-MM-DD} — No pipeline data in last 24h window." and write the same to the local file.