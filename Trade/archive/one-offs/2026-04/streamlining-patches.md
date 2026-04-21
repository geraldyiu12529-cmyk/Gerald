# Streamlining Patches — Skill Overrides

**Created:** 2026-04-16
**Purpose:** Overrides for read-only skill instructions. Same pattern as `retrieval-monitoring-patches.md`.

Skills are read-only, so these patches modify skill behavior via CLAUDE.md.

---

## news-events: Step 1 — Drop Methodology Prompt (Change 1C)

**Override:** Do NOT read `/mnt/Trade/Methodology Prompt.md` in the news skill's Step 1. The news skill does not score or grade variables — it only needs the asset universe (hardcoded in Step 5: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC + ETFs) and the catalyst calendar (from Memory.md §6). The brief and trade-rec skills load the methodology.

Revised Step 1 read list:
1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
2. `/mnt/Trade/Memory.md` — open positions (§2), catalysts (§6)
2b. `/mnt/Trade/master-data-log.xlsx` — latest RegimeHistory row
3. `/mnt/Trade/news-events/README.md` — format spec, hotspot list, retention rules
4. Most recent prior news file

---

## news-events: Step 5 — Catalyst-Filtered Ticker Searches (Change 4)

**Override:** Replace the current Step 5 exhaustive ticker search with a filtered approach.

Before running any ticker searches: read the Catalysts section from Memory.md §6. Extract tickers with scheduled events in the next 48 hours. Call this the **active ticker list**.

Search strategy:

1. **Active tickers** (from the 48h catalyst list): run both targeted searches per ticker:
   - `{TICKER} earnings today` / `{TICKER} Q1 results today`
   - `{TICKER} news today`
2. **Universe catch-all** (for everything else — typically 1–2 searches total):
   - `tech earnings today` — catches any universe ticker with unscheduled news
   - `semiconductor earnings today` if TSM/NVDA/INTC/MU are in the active window
3. Do NOT run individual `{TICKER} news today` searches for tickers with no scheduled catalyst. On a typical day, 10 of 12 universe tickers have no material news. Running 20+ targeted searches for them produces empty results and wastes search budget.

Output rule: unchanged — only items that moved a market or inform a decision. Do not include companies outside the universe unless they directly affect a universe name.

---

## daily-trade-rec: Step 0 — Delta-Check Gate (Change 2)

**Override:** Insert a new Step 0 before Step 1 of the daily-trade-rec skill.

### Step 0 — Delta-check gate (runs before any other step)

Before loading any files, check whether today's run is necessary:

1. Find the most recent prior rec file: `trade-rec-*.md` in `/mnt/Trade/`.
2. Get the mtime (file modification time) of that rec file.
3. Check the mtime of the three upstream artifacts:
   - `market-brief-{today}.md` (today's date, local UTC+8)
   - `news-events/news-{today}.md` (today's date)
   - Most recent `us-close-snapshot-*.md`

```python
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

trade_dir = Path('/mnt/Trade')
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')

# Find last rec
prior_recs = sorted(trade_dir.glob('trade-rec-*.md'))
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

# Check upstream artifact mtimes
upstream = [
    trade_dir / f'market-brief-{today}.md',
    trade_dir / f'news-events/news-{today}.md',
]
close_snaps = sorted(trade_dir.glob('us-close-snapshot-*.md'))
if close_snaps:
    upstream.append(close_snaps[-1])

changed = any(
    p.exists() and os.path.getmtime(p) > last_rec_mtime
    for p in upstream
)
```

- If `changed` is **False** (no upstream file is newer than the last rec):
  - Append one line to `/mnt/Trade/trade-rec-{today}.md`: `<!-- No-change revalidation {HH:MM} UTC+8: upstream artifacts unchanged since last rec. Scores carried forward. -->`
  - Print: `Delta-check: no upstream changes detected. Carrying forward prior rec. No full rerun needed.`
  - **Exit immediately. Do not execute Steps 1–10.**
- If `changed` is **True**: proceed to Step 1 normally.

This gate does not affect the first run of the day or any run following a new brief or news file.

---

## daily-trade-rec: Step 7 — Write to memory-lessons.md (Change 5C)

**Override:** In Step 7, the line that currently says:

> §8 (Lessons & Corrections): append one line summarising the slot...

Replace with:

> `/mnt/Trade/memory-lessons.md` (Lessons & Corrections): append one line summarising the slot, regime label, signal count, named near-misses, watchlist deltas, and the rec file path with version tag. Do NOT read this file at startup — write only.

---

## daily-trade-rec: Step 10 — Conditional HTML by Signal Count (Change 3)

**Override:** Replace the unconditional full HTML render in Step 10 with a tiered version.

Before rendering, count the number of assets with |Sum| ≥ 2 across today's scorecard (near-misses + promoted signals combined). Call this `signal_count`.

**If `signal_count` ≥ 1** (active signal day):
Produce the full HTML report as currently specified — all charts, full section order (Executive Summary, Data Collected with audit-addition sub-section, Analysis Methodology, Discussion, Results with annotated score stacking, Recommendations, outstanding gaps).

**If `signal_count` = 0** (flat day — all assets at |Sum| ≤ 1):
Produce a compact HTML report:

- Path: same `/mnt/Trade/report-{YYYY-MM-DD}-trade-rec.html`
- Required sections only:
  1. Executive Summary (no-trade verdict, regime label, material changes vs prior, next 48h catalysts)
  2. Audit additions status panel (mandatory regardless of signal count — three status indicators: residual momentum / intermediary capital / basis-momentum showing OK / MISSING / contributed-today)
  3. Data Gaps — Grade A MISSING rows with (a)/(b)/(c) split
  4. Regime + scorecard table (text, no charts)
- Omit: all Chart.js charts, score stacking charts, time-series sparklines, gap-closure doughnut, BTC address chart, yield curve chart.

Why: On a flat day the HTML is an audit record, not a decision aid. The audit-addition panel is always kept because visibility of MISSING data is the point regardless of signal count.

---

## signal-review: Step 1 — Read memory-lessons.md (Change 5E)

**Override:** Add to the signal-review Step 1 read list, after the Memory.md read:

> 4b. `/mnt/Trade/memory-lessons.md` — the full lessons log. Read this (not Memory.md §8, which is now a pointer) when looking for repeated blocking patterns or prior methodology notes.

---

## market-brief: Step 1 & Step 9 — memory-lessons.md redirect (Change 5B)

**Override:** The market-brief's Step 1 references "lessons (§8)" in the Memory.md read. Skip reading §8 — the brief never uses lessons operationally. It uses §2 (positions), §5 (watchlist), §6 (catalysts) only.

The market-brief's Step 9 writes a one-line lesson entry to "§8 (Lessons)". Redirect this write to `/mnt/Trade/memory-lessons.md` instead. Append the line there.

---

## quarterly-methodology-review: Step 1 & Step 8 — memory-lessons.md redirect (Change 5)

**Override:** The quarterly review's Step 1 reads "§8 lessons" — redirect to `/mnt/Trade/memory-lessons.md`. The quarterly review's Step 8 writes "Update Memory.md §8 with a one-line summary" — redirect that write to `/mnt/Trade/memory-lessons.md`.

---

## literature-review: Step 1 & final step — memory-lessons.md redirect (Change 5)

**Override:** The literature review's Step 1 reads "§8 lessons" — redirect to `/mnt/Trade/memory-lessons.md`. The literature review's final step writes "Update Memory.md §8 with a one-line summary" — redirect that write to `/mnt/Trade/memory-lessons.md`.

---

## weekly-regime-review: §8 Condensation Target (Change 5F)

**Override:** The weekly regime review's Memory §8 condensation step now targets `/mnt/Trade/memory-lessons.md`, not Memory.md §8. Specifically:

- **Read** verbose entries from `/mnt/Trade/memory-lessons.md`
- **Write** the condensed weekly summary to `/mnt/Trade/memory-lessons.md`
- **Archive** originals to `archive/memory-log-YYYY-WNN.md` (unchanged)
- Memory.md §8 is now a one-line pointer — do not write to it.
