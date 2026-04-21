# Downstream Wiring for Cloud Agent v2 Data

The v2 scheduled agent emits new tagged content (per-position 1h-RV, single-name IV, 25d-RR, MOVE, CDX HY, BTC/ETH order imbalance, vol-band-violation POSITION-ALERTs). These edits make sure local skills actually consume that data rather than letting it sit in Slack.

## Changes applied

| Skill | Edit | Purpose |
|---|---|---|
| **positions-monitor** | Added read of `{today}/slack-digest-{today}.md` + auto-invoke `/slack-ingest` if missing | Cloud alerts fire while machine off; must surface next time monitor runs |
| **positions-monitor** | Added **F12 vol_band** (HIGH) — cloud flagged methodology stop tightened below 1h-RV band | Direct counterpart to v2 cloud agent's vol-band check; cites ABDL 2001 / BPV 2016 Grade A |
| **positions-monitor** | Added **F13 cloud_alert** (MED) — catchall for any other `[POSITION-ALERT]` not covered by F1–F12 | Prevents cloud intelligence from being silently dropped |
| **positions-monitor** | Workflow Step 2 now parses digest alerts, matches by ticker. Output cites digest timestamps for F12/F13 lineage | Audit trail back to cloud agent fire |
| **daily-trade-rec** | Added **Pre-Entry Checklist item 7 — Cloud digest clearance** | Blocks new entries in correlated sleeve if an open position has unresolved vol-band-violation or thesis-breach alert |
| **market-brief** | Step 4 "Digest cross-check" paragraph | When digest has recent `[REGIME]` readings, cross-validate against this step's own pull; discrepancies >1σ flag staleness on one side |

## What was intentionally NOT changed

- **slack-ingest**: already preserves full message text under tagged sections — the new v2 data (per-position vol, MOVE, CDX HY) flows through automatically as markdown text. No parsing logic needed.
- **trade-update**: one-way push only (Layer 5). Doesn't consume scheduled-agent output.
- **framework/Memory.md, Methodology Prompt, Data Sources**: unchanged — no new variables, only refresh-frequency changes.
- **master-data-log.xlsx**: intraday regime readings are NOT persisted to any new sheet. DailyVariables remains the daily EOD log. (If you later want a SlackIntradayLog sheet, that's a new audit step — not required for the decision loop.)

## Dataflow summary

```
[Cloud scheduled agent fires 08:03/12:07/16:04/00:06 UTC+8]
           ↓
    Posts tagged sections to #trading-scheduled-updates
           ↓
  [POSITION-STATE]           [REGIME] [NEWS] [THESIS] [POSITION-ALERT]
           ↑                              ↓
   trade-update Layer 5             slack-ingest (Step 0 of morning pipeline)
   pushes on every trade event             ↓
                              {today}/slack-digest-{today}.md
                                           ↓
                         ┌─────────────────┼─────────────────┐
                         ↓                 ↓                 ↓
                  market-brief       daily-trade-rec    positions-monitor
                  (Step 4 cross-     (Step 5 checklist   (F12/F13 flags;
                   check regime)      item 7)            auto-ingests if
                                                         digest missing)
```

## Data coverage check

| v2 cloud output | Consumed by | Status |
|---|---|---|
| `[REGIME]` with VIX/MOVE/DXY/US10Y/CDX-HY/SPY | market-brief Step 4 | ✅ cross-check rule added |
| `[REGIME]` per-position vol (1h-RV, IV, 25d-RR) | positions-monitor F12; daily-trade-rec item 7 | ✅ F12 + checklist |
| `[NEWS]` bullets | market-brief Step 1 read; trade-rec Step 2 upstream synthesis | ✅ existing digest read |
| `[THESIS]` per-position deltas | positions-monitor F13; daily-trade-rec item 7 | ✅ F13 + checklist |
| `[POSITION-ALERT]` any flag | positions-monitor F12/F13 | ✅ |
| `[POSITION-ALERT]` vol-band-violation specifically | positions-monitor F12 (HIGH) | ✅ dedicated flag |

Nothing the cloud agent produces is now silently dropped by local skills.

## Updated skill bundles

All `.skill` files in `dist-skills/` have been regenerated with these edits:

- `slack-ingest.skill`
- `trade-update.skill`
- `market-brief.skill`
- `daily-trade-rec.skill`
- `positions-monitor.skill` **(new in this pass)**

## Cowork install — additional prompt

Add this to `COWORK-PROMPTS.md` (or run it standalone after the first four):

```
/skill-creator

Update the existing `positions-monitor` skill: add slack-digest ingest to the read list, add two new flags (F12 vol_band HIGH, F13 cloud_alert MED) tied to cloud scheduled-agent POSITION-ALERTs, and update workflow to parse digest alerts in Step 2.

Skill configuration:
- name: positions-monitor
- model: sonnet
- allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
- description: "Intraday watchdog — stop buffer, time-invalidation, earnings, catalyst, thesis variables, portfolio heat, correlation gate. Silent-when-OK. Use for 'check positions', 'monitor book', 'are my stops OK', 'portfolio heat', 'anything flashing'."

Required changes relative to base:

**MODIFY Reads section** — add as item 4:
4. `{today}/slack-digest-{today}.md` if present (cloud scheduled-agent POSITION-ALERTs, THESIS breaches, vol-band-violation flags). Invoke `/slack-ingest` if digest missing — the cloud agent fires 4x/day while local machine may be off, and its alerts must propagate into local flag panel.

**ADD two rows to Flag Panel table** (after F11):
| F12 vol_band | cloud scheduled agent flagged vol-band-violation in digest `[POSITION-ALERT]` (methodology stop tightened below 1h-RV band per ABDL 2001 / BPV 2016 Grade A) | HIGH |
| F13 cloud_alert | any other `[POSITION-ALERT]` from digest not already covered by F1–F12 | MED |

**REPLACE Workflow** with:
1. Inventory positions from framework/Memory.md §2
2. Ingest slack digest (/slack-ingest if missing) — parse [POSITION-ALERT] entries, match to open positions by ticker
3. Price pull — batched WebSearch per ticker
4. Compute all 13 flags (F12/F13 from digest alerts; F1–F11 from local data)
5. If all green: update pipeline/.pipeline-status.json with OK, exit silently
6. If flags: write {YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md (mkdir -p first) with flag table + per-position detail. Cite digest POSITION-ALERT timestamps for F12/F13 so lineage back to cloud agent is explicit.
7. Update pipeline/.pipeline-status.json
8. Escalate CRITICAL flags to auto-memory

Save to `.claude/skills/positions-monitor/SKILL.md`. No evals needed.
```
