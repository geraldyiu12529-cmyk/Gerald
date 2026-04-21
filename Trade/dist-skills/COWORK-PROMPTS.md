# Cowork Prompts — Slack Scheduled Updates Bundle

Four prompts to paste sequentially into Claude Cowork. Each creates one skill (or patches an existing one) using `/skill-creator`. Run them **in this order**: `slack-ingest` must exist before you patch the three skills that invoke it.

Channel name used throughout: `#trading-scheduled-updates`. If you want a different channel, find-and-replace before pasting.

---

## Prompt 1 — Create `slack-ingest` (NEW skill)

```
/skill-creator

Create a new skill named `slack-ingest`. Purpose: one-way pull of recent posts from a Slack channel into a local daily digest file, so downstream skills (market-brief, daily-trade-rec) can read what the cloud scheduled agent produced while the trader's machine was off.

Skill configuration:
- name: slack-ingest
- model: sonnet
- allowed-tools: Read Write Bash(python3 *) mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_search_channels mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_read_channel
- description: "Pull recent posts from the Slack #trading-scheduled-updates channel and write them to a local digest file for downstream consumption by market-brief and daily-trade-rec. Use for 'ingest slack', 'pull slack updates', 'sync slack'. Also auto-called as Step 0 of /market-brief and /daily-trade-rec."

Write the SKILL.md body exactly as follows:

---
# Slack Ingest

One-way pull: Slack scheduled-agent posts → local `{YYYY-MM-DD}/slack-digest-{date}.md`. Called at the start of the morning pipeline so cloud-produced context (intraday market/news/thesis updates) is folded into local trade decisions.

Local timezone UTC+8. Canonical channel name: `trading-scheduled-updates` (configurable; see Step 1).

## Step 1 — Resolve channel ID
Call `slack_search_channels(query="trading-scheduled-updates")` and pick the exact-name match. If no match: write a digest file with body `CHANNEL NOT FOUND — configure #trading-scheduled-updates and re-run.` and stop. Do not fail-loud silently.

## Step 2 — Pull last 24h of messages
Call `slack_read_channel(channel_id=<id>, limit=100, response_format="concise")`. Filter client-side:
- Keep messages within last 24h (UTC+8 day boundary).
- Drop bot system messages (channel_join, etc.).
- Preserve original author, timestamp, and full text.
If >100 messages in window, paginate via cursor.

## Step 3 — Categorize
Each message is expected to carry a leading tag from the cloud agent:
- `[REGIME]` — regime pulse
- `[NEWS]` — news capture
- `[THESIS]` — thesis-variable delta
- `[POSITION-ALERT]` — positions-monitor flag
- `[POSITION-STATE]` — **ignore here** (these are snapshots pushed up by /trade-update; no need to ingest back)
Untagged messages → "Unclassified".

## Step 4 — Write digest
Path: `{YYYY-MM-DD}/slack-digest-{YYYY-MM-DD}.md` using today in UTC+8. Create folder first: `mkdir -p {YYYY-MM-DD}`.
Sections: Regime Pulse, News, Thesis Variable Deltas, Position Alerts (surface at top if any), Unclassified.
If zero messages in window: write minimal file with body `No scheduled-update posts in last 24h window.` and exit.

## Step 5 — Report
One-line summary: `slack-digest written: N messages across {regime, news, thesis, alert} categories`. This skill is a data-pull, not commentary.

## Downstream contract
`/market-brief` Step 1 and `/daily-trade-rec` Step 1 read `{today}/slack-digest-{today}.md` if present. Treat the digest as **Grade B at best** — cloud agent synthesis, not primary source. Missing digest is not fail-loud.
---

Save as `.claude/skills/slack-ingest/SKILL.md`. Don't run evals — this is a utility data-pull skill with no subjective output. Just create the file and confirm.
```

---

## Prompt 2 — Patch `trade-update` (add Layer 5: Slack POSITION-STATE push)

```
/skill-creator

Update the existing `trade-update` skill to add a new Layer 5 that posts a POSITION STATE SNAPSHOT to Slack after every trade event. This gives a cloud-scheduled agent current position context on its next fire (the scheduled agent has no local file access, so it reads these snapshots from Slack).

If the skill doesn't exist yet, create it with the full content below. If it exists, ADD Layer 5 (content below) after Layer 4 and update the allowed-tools list.

Skill configuration:
- name: trade-update
- model: sonnet
- allowed-tools: Bash(python3 *) Read Write Edit Grep Glob mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_search_channels mcp__3707e784-0d34-4a07-887c-f348b3366436__slack_send_message
- description: "Event-driven 4-layer sync on trade execution events — entries, exits, stop moves, tranches, size changes. Use when 'I entered X', 'I bought X', 'stopped out of X', 'moved stop on X', 'trimmed X'. Not for placing trades or daily rec/brief."

Full SKILL.md body:

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
After Layers 1–4 complete, post an updated snapshot to `#trading-scheduled-updates` so the cloud scheduled agent has current position context on its next fire. Single message, not a thread.

1. Resolve channel: `slack_search_channels(query="trading-scheduled-updates")` → pick exact-name match. Not found → log missing, skip layer (do not fail the whole update).
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

3. Send: `slack_send_message(channel_id=<id>, message=<body>)`. Pull content from post-update state of Memory.md §2 §5 §7 — don't recompute from scratch.
4. If event was *Exit*: append one-line epitaph below table: `Exit: {asset} {HIT_STOP|HIT_TARGET|DISCRETIONARY} @ {price} — {hypo_pnl}`.

Purpose: cloud scheduled agent reads the most recent `[POSITION-STATE]` message on each fire (8am / 12pm / 4pm / 12am UTC+8) so it can produce position-aware intraday updates without local file access.

## Step 5 — Confirm
Report: event recorded, signal ID, new portfolio heat, Slack POSITION-STATE posted (y/n + link), follow-up if any.

## Reconciliation mode
Triggered by "reconcile the ledger": diff framework/Memory.md §2 vs SignalLedger OPEN rows, fix gaps oldest-first, save after each event.
---

Save to `.claude/skills/trade-update/SKILL.md`. No evals needed.
```

---

## Prompt 3 — Patch `market-brief` (add Step 0: auto-ingest Slack)

```
/skill-creator

Update the existing `market-brief` skill: insert a new **Step 0 — Slack digest ingest** that invokes `/slack-ingest` before any other read, and add the digest as the first item in Step 1 reads. This ensures overnight cloud-agent posts inform the regime read.

If the skill already exists, apply the minimal change. If not, create it with the full content below.

Skill configuration:
- name: market-brief
- model: sonnet
- allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
- description: "Daily US pre-open market brief — regime snapshot, variable table, S|T|C|R|Sum scorecard, Excel sync. Pulls Grade A variables via 4-tier retrieval engine. Use for 'market brief', 'daily brief', 'regime update', 'pull the numbers'. Not for trade recommendations."

Required change (relative to base version):

**INSERT at top, before Step 1:**

## Step 0 — Slack digest ingest
Before any other read, invoke `/slack-ingest` to pull the last 24h of scheduled-agent posts from `#trading-scheduled-updates` into `{today}/slack-digest-{today}.md`. Treat the digest as **Grade B optional context** — it informs the regime read and surfaces overnight news/alerts the cloud agent caught while the machine was off. Missing digest = proceed without, note under Data Gaps.

**MODIFY Step 1 reads** — add as item 1 (shift others down):
1. `{today}/slack-digest-{today}.md` — cloud agent's overnight synthesis (Grade B). Optional.
2. `framework/Memory.md` — §2 Open Positions, §5 Watchlist, §6 Catalysts. Skip §8.
3. `framework/Methodology Prompt.md` — 8-step framework, Top-28 variables, evidence grading
4. `master-data-log.xlsx` — latest row of `RegimeHistory` (prior regime) and `DailyVariables` (prior readings) via openpyxl
5. `framework/Data Sources.md` — variable-to-source mapping, fail-loud rule
6. `framework/Risk Rules.md` — scan for active circuit breaker or heat constraint

Leave everything else (Steps 2-9) unchanged. Save the patched file to `.claude/skills/market-brief/SKILL.md`. No evals needed.
```

---

## Prompt 4 — Patch `daily-trade-rec` (add Slack digest to Step 1 reads)

```
/skill-creator

Update the existing `daily-trade-rec` skill: add Slack digest ingest as the first item in Step 1 reads, with fallback to invoke `/slack-ingest` if the digest wasn't produced by a prior `/market-brief` run.

Skill configuration:
- name: daily-trade-rec
- model: opus
- allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
- description: "Pre-open trade recommendation — 8-step methodology + Risk Rules checklist + SignalLedger append + HTML report. Use for 'trade rec', 'trade recommendation', 'run the 8-step', 'score the book', 'tell me what to trade today'. Not for commentary — use market-brief or news-events."

Required change — replace Step 1 "Reads" section with:

## Step 1 — Reads

**Slack digest (first):** If `/market-brief` ran today, `{today}/slack-digest-{today}.md` already exists. If not (direct trade-rec invocation without brief), invoke `/slack-ingest` now to produce it. Treat as **Grade B optional context** — cloud agent synthesis, not primary source. Missing digest is not fail-loud.

**Framework:** framework/Memory.md, framework/Methodology Prompt.md, framework/Risk Rules.md, master-data-log.xlsx (RegimeHistory latest row, DailyVariables latest row, SignalLedger OPEN rows for dedup).

**Upstream artifacts (today's date folder `{today}/`):**
- `{today}/slack-digest-{today}.md` — overnight cloud-agent synthesis (Grade B, optional)
- `{today}/market-brief-{today}.md` — regime, scorecard, levels, catalysts
- `{today}/news-{today}.md` — headlines, geopolitics, surprises
- `{today}/us-close-snapshot-{today}.md` (or most recent prior day under `*/us-close-snapshot-*.md`)
- `{most-recent-Sunday}/weekly-review-{most-recent-Sunday}.md` — regime trajectory
- *(optional)* Latest `*/signal-review-*.md` §8 Escalation Flags

Missing framework file → stop. Missing upstream → log under Data Gaps, proceed.

Leave Step 0 (delta-check gate), Steps 2-10, and the HTML report section unchanged. Save to `.claude/skills/daily-trade-rec/SKILL.md`. No evals needed.
```

---

## Post-install checklist

After running all four prompts in Cowork:

1. Create the Slack channel `#trading-scheduled-updates` if it doesn't exist.
2. Verify Slack MCP is connected in the Cowork workspace.
3. Run `/slack-ingest` manually once to confirm channel resolution works.
4. Test `/trade-update` with a dummy event to confirm Layer 5 posts reach Slack.
5. Register the cloud scheduled agent via `/schedule` (4x/day at 08:03, 12:07, 16:04, 00:06 UTC+8) with the self-contained prompt from the earlier discussion.
