# Streamlining Implementation — All 5 Optimisations
**Created:** 2026-04-16
**Scope:** Skill edits, new scheduled task, CLAUDE.md update, Memory.md restructure
**Goal:** Reduce repeated context loads and redundant operations without changing any methodology, scoring, or data rules.

---

## Overview of changes

| # | Change | Files touched | Token saving |
|---|--------|--------------|-------------|
| 1 | Session header task compiles daily context once | New task `session-header-compile-755pm`, new skill `session-header` | High — eliminates 3× repeated reads of Methodology Prompt + Memory.md |
| 2 | Delta-check gate enforced at skill entry | `daily-trade-rec/SKILL.md` Step 0 | High on unchanged days |
| 3 | Conditional HTML by signal count | `daily-trade-rec/SKILL.md` Step 10 | Medium — eliminates 10-chart render on flat days |
| 4 | News ticker filtering from §6 | `news-events/SKILL.md` Step 5 | Medium — cuts ~18 of 24 ticker searches on typical days |
| 5 | Lessons section separation | `Memory.md`, `news-events/SKILL.md`, `market-brief/SKILL.md`, `daily-trade-rec/SKILL.md`, `CLAUDE.md` | Medium/growing |

---

## Change 1 — Session header task

### 1A. Create new scheduled task `session-header-compile-755pm`

Create a new scheduled task with:
- **taskId:** `session-header-compile-755pm`
- **cronExpression:** `55 19 * * 1-5` (19:55 UTC+8, Mon–Fri, fires after `audit-data-compute-750pm` completes)
- **description:** `Compiles session-header-{YYYY-MM-DD}.md from authoritative sources once per day, before the brief/news/trade-rec pipeline runs. Eliminates triple-read of Methodology Prompt + Memory.md across the three daily skills.`
- **prompt:** (full prompt below)

```
You are the session-header compiler for Gerald's trading workspace.

Your sole job is to write a compact, accurate daily context file that the market-brief, news-events, and daily-trade-rec skills will read instead of re-loading the full source documents themselves.

## Step 1 — Read the authoritative sources

Read exactly these files (and no others):

1. `/mnt/Trade/Memory.md` — extract: §1 (Asset Universe), §2 (Open Positions table), §5 (Watchlist table), §6 (Catalyst table — next 14 days only)
2. `/mnt/Trade/master-data-log.xlsx` — read the latest row of RegimeHistory (regime label + growth/inflation/policy/finconditions/riskonoff + the three Watch_Var columns) and the latest row of DailyVariables (full variable readings, for context)
3. `/mnt/Trade/Risk Rules.md` — extract: §4 (Drawdown Circuit Breakers) and §5 (Correlation/Concentration Gate). Check whether any circuit breaker is currently active (portfolio DD exceeds −15% or −20% thresholds). If no open positions exist, write "No active circuit breakers."

Do NOT read Methodology Prompt.md, Data Sources.md, or the research cores. Those are loaded once by the market-brief skill and are too large for a header file.

## Step 2 — Write the session header

Path: `/mnt/Trade/session-header-{YYYY-MM-DD}.md` (use today's local date, UTC+8).

If a file already exists for today, overwrite it and bump the version tag in the title.

Use exactly this structure — no additions, no padding:

```markdown
# Session Header — {YYYY-MM-DD} (v{N})
*Compiled {HH:MM} UTC+8 by session-header-compile-755pm. Read this instead of loading Memory.md + Methodology Prompt.md startup sections.*

---

## Regime (latest row — RegimeHistory)
**Label:** {one-line regime label}
Growth: {state} | Inflation: {state} | Policy: {state} | FinCond: {state} | Risk: {state}
Watch: (1) {Watch_Var_1} (2) {Watch_Var_2} (3) {Watch_Var_3}

---

## Open Positions
{Copy §2 table from Memory.md verbatim. If no open positions, write "None."}

---

## Watchlist (active candidates only)
{Copy §5 table from Memory.md, but OMIT strikethrough rows — demoted/removed entries add noise. Active rows only.}

---

## Catalysts — Next 14 days
{Copy §6 table from Memory.md, rows with date ≤ today+14 only. Omit past catalysts.}

---

## Circuit Breakers
{Active circuit breakers from Risk Rules §4, or "None active." if portfolio DD is below threshold.}

---

## Prior variable readings (spot reference)
{One-line compact table: VIX | MOVE | HY_OAS | DXY | BTC | Brent | Gold — latest values from DailyVariables. Source dates in parentheses.}
```

## Step 3 — Done

Print the file path. No other output. Do not read any other files. Do not update Memory.md or Excel. This is a read-compile-write task only.
```

### 1B. Update `market-brief/SKILL.md` Step 1

Replace the current Step 1 (which reads Memory.md and Excel separately) with:

**Current Step 1 (remove):**
> 1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
> 2. `/mnt/Trade/Methodology Prompt.md` — the 8-step framework, Top-28 variable list, evidence grading
> 3. `/mnt/Trade/Memory.md` — open positions, watchlist (§5), catalysts (§6), lessons (§8)
> 4. `/mnt/Trade/master-data-log.xlsx` — read the latest row of `RegimeHistory` and `DailyVariables` using openpyxl.
> 5. `/mnt/Trade/Data Sources.md` — the variable-to-source mapping with fail-loud rule
> 6. `/mnt/Trade/Risk Rules.md` — quick scan for any active circuit breaker or heat constraint

**New Step 1 (replace with):**
> 1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
> 2. Check for `/mnt/Trade/session-header-{YYYY-MM-DD}.md` (today's date). If present, read it — this gives you regime label, open positions, watchlist, catalysts, and circuit breaker status in one compact file. **Skip reading Memory.md §1–§6 and the Excel RegimeHistory/DailyVariables latest rows; the header already compiled them.** If absent (session-header task didn't run), fall back: read Memory.md §2/§5/§6 and the Excel latest rows directly.
> 3. `/mnt/Trade/Methodology Prompt.md` — the 8-step framework, Top-28 variable list, evidence grading *(still mandatory — not compiled into the header)*
> 4. `/mnt/Trade/Data Sources.md` — the variable-to-source mapping with fail-loud rule
> 5. `/mnt/Trade/Risk Rules.md` §1–§3 — sizing rules and stops policy *(circuit breaker status already in header; read §1–§3 for sizing context)*

### 1C. Update `news-events/SKILL.md` Step 1

**Current Step 1 (remove):**
> 1. `/mnt/.auto-memory/MEMORY.md`
> 2. `/mnt/Trade/Methodology Prompt.md`
> 3. `/mnt/Trade/Memory.md` — open positions (§2), catalysts (§6)
> 3b. `/mnt/Trade/master-data-log.xlsx` — read latest RegimeHistory row
> 4. `/mnt/Trade/news-events/README.md`
> 5. Most recent prior news file

**New Step 1 (replace with):**
> 1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
> 2. Check for `/mnt/Trade/session-header-{YYYY-MM-DD}.md`. If present, read it — this gives you regime label, positions, watchlist, and catalysts. **Do not separately load Memory.md §2/§6 or the Excel RegimeHistory row.** If absent, fall back to reading Memory.md §2/§6 and the Excel latest RegimeHistory row directly.
> 3. `/mnt/Trade/news-events/README.md` — format spec, hotspot list, retention rules *(still mandatory)*
> 4. Most recent prior news file (yesterday's `news-YYYY-MM-DD.md`)

Note: Methodology Prompt.md is **removed** from the news skill startup entirely. The news skill does not score or grade variables — it only needs the asset universe (in the header under §1) and the catalyst calendar (in the header under Catalysts). The asset universe is stable and its 6 tickers fit in one line; the header provides it.

### 1D. Update `daily-trade-rec/SKILL.md` Step 1

**Current Step 1 framework reads (remove lines 1–5):**
> 1. `/mnt/.auto-memory/MEMORY.md`
> 2. `/mnt/Trade/Methodology Prompt.md`
> 3. `/mnt/Trade/Risk Rules.md`
> 4. `/mnt/Trade/Memory.md`
> 5. `/mnt/Trade/master-data-log.xlsx` — RegimeHistory + DailyVariables latest rows + OPEN SignalLedger rows

**New Step 1 framework reads (replace with):**
> 1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
> 2. Check for `/mnt/Trade/session-header-{YYYY-MM-DD}.md`. If present, read it — regime, positions, watchlist, catalysts, circuit breakers in one file. **Skip separate Memory.md §2/§5/§6 and the Excel RegimeHistory/DailyVariables latest rows.** If absent, fall back.
> 3. `/mnt/Trade/Methodology Prompt.md` — 8-step framework *(still mandatory)*
> 4. `/mnt/Trade/Risk Rules.md` — binding pre-entry checklist and sizing policy *(still mandatory)*
> 5. `/mnt/Trade/master-data-log.xlsx` — read **only** OPEN rows from `SignalLedger` (for deduplication in Step 8). *(RegimeHistory and DailyVariables latest rows now come from the session header.)*

### 1E. Update `CLAUDE.md` Session Startup Protocol

Add one line to the startup protocol (after step 1):

> 1b. Check for `/mnt/Trade/session-header-{YYYY-MM-DD}.md`. If present, read it in place of Memory.md §1–§6 and the Excel RegimeHistory/DailyVariables latest rows. If absent, read those sources directly as before.

---

## Change 2 — Delta-check gate enforced in trade-rec skill

### Update `daily-trade-rec/SKILL.md` — add Step 0 before Step 1

Insert a new **Step 0 — Delta-check gate** as the very first step of the skill:

```
## Step 0 — Delta-check gate (runs before any other step)

Before loading any files, check whether today's run is necessary:

1. Find the most recent prior rec file: `trade-rec-{YYYY-MM-DD}.md` (prior trading day or same day vN-1).
2. Get the mtime (file modification time) of that rec file.
3. Check the mtime of the three upstream artifacts:
   - `market-brief-{YYYY-MM-DD}.md` (today)
   - `news-events/news-{YYYY-MM-DD}.md` (today)
   - `us-close-snapshot-{YYYY-MM-DD}.md` (today) or most recent prior-day snapshot

```python
import os
from pathlib import Path

trade_dir = Path('/mnt/Trade')
today = '{YYYY-MM-DD}'  # replace with actual local date

# Find last rec
prior_recs = sorted(trade_dir.glob('trade-rec-*.md'))
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

# Check upstream artifact mtimes
upstream = [
    trade_dir / f'market-brief-{today}.md',
    trade_dir / f'news-events/news-{today}.md',
]
# Also check most recent us-close snapshot
close_snaps = sorted(trade_dir.glob('us-close-snapshot-*.md'))
if close_snaps:
    upstream.append(close_snaps[-1])

changed = any(
    p.exists() and os.path.getmtime(p) > last_rec_mtime
    for p in upstream
)
```

4. If `changed` is **False** (no upstream file is newer than the last rec):
   - Write one line to `/mnt/Trade/trade-rec-{YYYY-MM-DD}.md` (append, do not overwrite):
     `<!-- No-change revalidation {HH:MM} UTC+8: upstream artifacts unchanged since last rec. Scores carried forward. -->`
   - Print: `Delta-check: no upstream changes detected. Carrying forward prior rec. No full rerun needed.`
   - **Exit immediately. Do not execute Steps 1–10.**

5. If `changed` is **True**: proceed to Step 1 normally.

**Rationale:** The pipeline produces multiple rec versions per day when upstream artifacts update. On sessions where Gerald re-runs the task manually and nothing has changed, this gate eliminates an unnecessary full context load. It does not affect the first run of the day or any run following a new brief or news file.
```

---

## Change 3 — Conditional HTML output

### Update `daily-trade-rec/SKILL.md` Step 10

Replace the current Step 10 (unconditional full HTML) with a tiered version:

**Replace current Step 10 header with:**

```
## Step 10 — HTML report (tiered by signal count)

Before rendering, count the number of assets with |Sum| ≥ 2 across today's scorecard (near-misses + promoted signals combined). Call this `signal_count`.

**If `signal_count` ≥ 1 (active signal day):** Produce the full HTML report as currently specified — all 10+ charts, full section order (Executive Summary, Data Collected with audit-addition sub-section, Analysis Methodology, Discussion, Results with annotated score stacking, Recommendations, outstanding gaps).

**If `signal_count` = 0 (flat day — all assets at |Sum| ≤ 1):** Produce a compact HTML report:
- Path: same `/mnt/Trade/report-{YYYY-MM-DD}-trade-rec.html`
- Required sections only:
  1. Executive Summary (no-trade verdict, regime label, material changes vs prior, next 48h catalysts)
  2. **Audit additions status panel** (mandatory regardless of signal count — three status indicators: residual momentum / intermediary capital / basis-momentum showing OK / MISSING / contributed-today)
  3. Data Gaps — Grade A MISSING rows with (a)/(b)/(c) split
  4. Regime + scorecard table (text, no charts)
- **Omit:** all Chart.js charts, score stacking charts, time-series sparklines, gap-closure doughnut, BTC address chart, yield curve chart. These add rendering overhead without decision value when no signal is near actionable.
- **Why:** On a flat day the HTML is an audit record, not a decision aid. The audit-addition panel is always kept because visibility of MISSING data is the point of that section regardless of signal count.
```

---

## Change 4 — News ticker filtering from §6

### Update `news-events/SKILL.md` Step 5

Replace the current Step 5 with:

```
## Step 5 — Corporate & tech (universe only)

**Before running any ticker searches:** read the Catalysts section from the session header (or Memory.md §6 if the header is absent). Extract tickers with scheduled events in the next 48 hours. Call this the **active ticker list**.

```python
# Example logic — read from session header or Memory §6
# active_tickers = tickers that have a catalyst row with date within next 48h
# e.g., on Apr-16: ['TSM'] (TSM Q1 earnings 02:00 ET)
```

**Search strategy:**

1. **Active tickers** (from the 48h catalyst list): run both targeted searches per ticker:
   - `{TICKER} earnings today` / `{TICKER} Q1 results today`
   - `{TICKER} news today`

2. **Universe catch-all** (for everything else — typically 1–2 searches total):
   - `tech earnings today` — catches any universe ticker with unscheduled news
   - `semiconductor earnings today` if TSM/NVDA/INTC/MU are in the active window

3. **Do NOT run** individual `{TICKER} news today` searches for the 8–10 tickers with no scheduled catalyst. On a typical day, 10 of 12 universe tickers have no material news. Running 20+ targeted searches for them produces empty results and wastes search budget.

**Output rule:** still the same — only items that moved a market or inform a decision. Do not include companies outside the universe unless they directly affect a universe name.
```

---

## Change 5 — Lessons section separation

### 5A. Split Memory.md §8 into a separate file

Create `/mnt/Trade/memory-lessons.md` by cutting §8 from Memory.md and pasting it there verbatim. Then replace §8 in Memory.md with a one-line pointer:

In Memory.md, replace the entire §8 block with:
```markdown
## 8. Lessons & Corrections

*Moved to `/mnt/Trade/memory-lessons.md` to keep daily startup reads lean. Read that file for the full lesson log. The weekly-regime-review task writes new condensed entries directly to `memory-lessons.md`.*
```

### 5B. Update `market-brief/SKILL.md` — remove §8 from startup read

In the new Step 1 (after Change 1 is applied), remove any reference to loading Memory.md §8 or lessons. The brief never uses lessons operationally — it uses §2 (positions), §5 (watchlist), §6 (catalysts) only. The session header provides all three. No change needed if Change 1 is applied first (the header already omits §8).

### 5C. Update `daily-trade-rec/SKILL.md` — remove §8 from startup read

Same as 5B. The trade-rec references Memory.md §8 only when *writing* a new lesson entry (Step 7). The write target changes to `memory-lessons.md`. Update Step 7 line:

**Current:**
> §8 (Lessons & Corrections): append one line summarising the slot...

**New:**
> `/mnt/Trade/memory-lessons.md` (Lessons & Corrections): append one line summarising the slot, regime label, signal count, named near-misses, watchlist deltas, and the rec file path with version tag. Do NOT read this file at startup — write only.

### 5D. Update `news-events/SKILL.md` — no change needed

The news skill never reads Memory.md §8. No change.

### 5E. Update `signal-review/SKILL.md` — add memory-lessons.md to Step 1

The signal review is the one downstream skill that legitimately reads historical lessons (to look for repeated patterns). Update its Step 1:

Add after the current Memory.md read:
> 3b. `/mnt/Trade/memory-lessons.md` — the full lessons log. Read this (not Memory.md §8, which is now a pointer only) when looking for repeated blocking patterns or prior methodology notes.

### 5F. Update `weekly-regime-review-sunday-6pm-v2` scheduled task description

Update the task description to note that the Memory §8 condensation step now writes to `memory-lessons.md`, not Memory.md §8.

Update the task prompt to:
- Read verbose entries from `memory-lessons.md` (not Memory.md §8)
- Write condensed summary to `memory-lessons.md`
- Archive originals to `archive/memory-log-YYYY-WNN.md` (unchanged)

---

## Implementation order

Apply changes in this sequence to avoid dependency issues:

1. **Change 5A first** — split Memory.md. Self-contained file operation, no skill dependencies.
2. **Change 1** — create session header task + update all three daily skill Step 1s + CLAUDE.md. Do these together in one pass.
3. **Change 2** — add Step 0 to trade-rec skill.
4. **Change 3** — update trade-rec Step 10.
5. **Change 4** — update news-events Step 5.
6. **Changes 5B–5F** — update skill references to memory-lessons.md. Apply after Change 1 is live so the session header already handles the startup load reduction.

---

## What does NOT change

- Methodology Prompt.md — unchanged, still loaded by market-brief and trade-rec
- Risk Rules.md — unchanged, still loaded by trade-rec
- Data Sources.md — unchanged, still loaded by market-brief
- All scoring rules, evidence grades, pre-entry checklist — unchanged
- Excel sync protocol — unchanged
- Fail-loud rules for Grade A MISSING variables — unchanged
- SignalLedger append-only rule — unchanged
- Audit-addition panel in HTML — always present regardless of signal count (Change 3 explicitly preserves this)
- 2026-10-14 review gate — unchanged

---

## Verification after implementation

After applying all changes, run a dry-pass check:

1. Confirm `session-header-{today}.md` is produced at 19:55 and contains all five sections with no empty blocks.
2. Run the market-brief manually and confirm it reads the session header, not Memory.md §5/§6 separately.
3. Run the trade-rec with no upstream changes since the last rec and confirm Step 0 exits cleanly with the no-change one-liner.
4. Run the news skill on a day where only one ticker is in the 48h catalyst window and confirm it runs ≤4 ticker searches (not 24).
5. Confirm `memory-lessons.md` exists and Memory.md §8 contains only the pointer line.
6. Confirm the weekly-regime-review task writes to `memory-lessons.md`, not Memory.md §8.
