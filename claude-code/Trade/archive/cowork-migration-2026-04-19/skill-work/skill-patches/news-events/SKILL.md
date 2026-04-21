---
name: news-events
description: "Daily news, geopolitics, macro releases, corporate earnings, crypto regulatory, and flash-event capture for Gerald's trading workspace. Searches by category (not by named conflict), uses the hotspot list from news-events/README.md, and writes a structured file the trade-rec skill consumes downstream. Use this skill whenever the user asks for 'news capture', 'daily news', 'what happened today', 'overnight headlines', 'geopolitics update', 'econ calendar', 'flash events', or asks 'what moved markets'. Also use when the scheduled task `daily-news-events-810pm-v2` fires. Not for regime scoring or trade recommendations — use the market-brief or daily-trade-rec skills for those."
---

# Daily News & Events Capture

Produces the day's news and events log for Gerald's `/Trade/news-events/` directory. The output is a structured summary of geopolitics, macro data, economic calendar, corporate/tech, crypto/regulatory, flash events, and regime implications — consumed by the trade-rec skill as part of its upstream synthesis.

Local timezone is UTC+8. The canonical slot is 20:10 UTC+8 = 08:10 ET = US pre-open. Use today's local date in the filename. If the file already exists from an earlier run the same day, overwrite and bump the version tag in the title (`v2`, `v3`, …).

---

## Step 1 — Mandatory startup reads

1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
2. `/mnt/Trade/Memory.md` — open positions (§2), catalysts (§6) — needed to judge what's noise vs signal
2b. `/mnt/Trade/master-data-log.xlsx` — read the latest row of **RegimeHistory** (current regime state) using openpyxl
3. `/mnt/Trade/news-events/README.md` — the format spec, current hotspot list, and retention rules
4. The most recent prior news file (yesterday's `news-YYYY-MM-DD.md`) — for continuity and delta detection

Note: Methodology Prompt.md is not loaded by this skill. The news skill does not score or grade variables — it only needs the asset universe (hardcoded in Step 5) and the catalyst calendar (from Memory.md §6). The brief and trade-rec skills load the methodology.

If the README is missing, stop and surface the gap.

## Step 2 — Geopolitics & political risk search

Search by **category**, not by named conflict. Conflicts end, new ones begin.

**Generic category searches (always run):**
- `sanctions today`
- `military conflict today`
- `diplomatic crisis today`
- `trade war tariffs today`
- `territorial dispute today`
- `election crisis today`
- `regime change coup today`
- `naval incident today`
- `blockade embargo today`

**Hotspot-specific searches (from README.md hotspot table):**
Read the hotspot table from `/mnt/Trade/news-events/README.md` and run a targeted search for each active hotspot using its key search terms.

**Rules:**
- Every item must cite source and date
- No padding, no narrative — only items that moved a market or inform a decision
- If a hotspot appears to have de-escalated or resolved, note it for the README update in Step 8

## Step 3 — Macro data releases

Search for today's economic data releases:
- `US economic data releases today`
- `CPI PPI NFP PCE release today` (if any major prints are expected)
- `central bank rate decision today`
- `Fed FOMC statement today` (if scheduled)
- `ECB BOJ BOE rate decision today` (if scheduled)

For each release found:
- Report **actual vs expected vs prior**
- Note whether the print is inflationary/deflationary, above/below consensus
- Flag tier-1 prints (CPI, PPI, NFP, PCE, FOMC) explicitly

## Step 4 — Economic calendar (next 48h)

Search: `US economic calendar this week`

Build a table:

| Date/Time (ET) | Event | Impact (High/Medium/Low) | Notes |

Include any rescheduled events. Compare against Memory.md §6 and flag changes.

## Step 5 — Corporate & tech (universe only)

Search for earnings, guidance changes, M&A, and product launches for the asset universe: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC (and ETFs: SPY, QQQ, EWY, XLE).

**Catalyst-filtered search strategy:** Before running any ticker searches, read the Catalysts section from Memory.md §6. Extract tickers with scheduled events in the next 48 hours — call this the **active ticker list**.

1. **Active tickers** (from the 48h catalyst list): run both targeted searches per ticker:
   - `{TICKER} earnings today` / `{TICKER} Q1 results today`
   - `{TICKER} news today`
2. **Universe catch-all** (for everything else — typically 1–2 searches total):
   - `tech earnings today` — catches any universe ticker with unscheduled news
   - `semiconductor earnings today` if TSM/NVDA/INTC/MU are in the active window
3. Do NOT run individual `{TICKER} news today` searches for tickers with no scheduled catalyst. On a typical day, 10 of 12 universe tickers have no material news — targeted searches produce empty results and waste search budget.

Do not include companies outside the universe unless they directly affect a universe name (e.g., a supplier to NVDA).

## Step 6 — Crypto & regulatory

Search:
- `Bitcoin ETF flows today`
- `Ethereum ETF flows today`
- `crypto regulation news today`
- `SEC crypto enforcement today`
- `Bitcoin exchange news today`
- `stablecoin regulation today`

Cover: ETF flow data, enforcement actions, exchange incidents, on-chain events, and policy moves.

## Step 7 — Flash / surprise events

Search: `market moving news today`, `surprise event markets today`

Capture anything unscheduled that moved markets materially. If nothing qualifies, omit this section entirely.

## Step 8 — Write the output file

Path: `/mnt/Trade/news-events/news-{YYYY-MM-DD}.md`

Use this format:

```
# News & Events — YYYY-MM-DD (vN)

**Local:** HH:MM UTC+8 (HH:MM ET, US pre-open) — scheduled daily news capture[, vN refresh].

---

## 1. Geopolitics & Political Risk
[Items with source citations]

## 2. Macro Data Releases Today (YYYY-MM-DD)
[Actual vs expected vs prior, with source citations]

## 3. Economic Calendar — Next 48h
[Table: Date/Time ET | Event | Impact | Notes]

## 4. Corporate & Tech (Universe Only)
[Universe-relevant items only, with source citations]

## 5. Crypto & Regulatory
[ETF flows, enforcement, on-chain, policy, with source citations]

## 6. Flash / Surprise Events
[Omit if none]

## 7. Regime Implications
[2–3 lines max: which items above actually shift regime readings in Memory.md, and which are noise]
```

## Step 9 — Update Memory.md §6 (Catalysts)

After writing the news file, check if any catalyst dates in Memory.md §6 need updating:
- Rescheduled events (update dates)
- New catalysts discovered (add to §6)
- Expired catalysts (mark as passed, note outcome)

Do not batch — update immediately.

---

## Rules

- Every item must cite source and be dated. No padding, no narrative.
- Items that did not move a market or inform a decision do not belong here.
- Search by category, not by named conflict. The hotspot list supplements categories, not replaces them.
- Do not include companies outside the asset universe unless they directly affect a universe name.
- §7 (Regime Implications) is mandatory and must be ≤3 lines. Its job is to separate signal from noise for the downstream trade rec.
- Retention is owned by the master Retention Policy and the workspace-tidy task. Do not implement separate archival logic.
- If a geopolitical hotspot has resolved or de-escalated, note it so the README can be updated.
