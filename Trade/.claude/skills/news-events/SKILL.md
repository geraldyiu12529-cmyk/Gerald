---
name: news-events
description: "Daily news capture — geopolitics, macro, earnings, crypto, credit, flash events. Searches by category, writes structured file + catalysts cache for downstream brief/trade-rec. Use for 'news capture', 'daily news', 'what happened today', 'overnight headlines'. Not for regime scoring or trade recommendations."
model: haiku
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily News & Events Capture

Produces structured news log at `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` (create folder: `mkdir -p {YYYY-MM-DD}`). Consumed by trade-rec upstream synthesis. Local timezone UTC+8, canonical slot 20:10. `news-events/README.md` (format spec) stays in `news-events/`.

---

## Step 1 — Reads

1. `framework/Memory.md` — §2 Open Positions (what's live), §6 Catalysts (48h active tickers)
2. `master-data-log.xlsx` — latest RegimeHistory row via openpyxl
3. `news-events/README.md` — format spec, hotspot list, source hierarchy, noise filters, political-communication filter
4. Prior day's `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` — for delta detection

Do NOT read framework/Methodology Prompt.md, framework/Risk Rules.md, or research cores. This skill does not score.

## Step 1.5 — Non-overlap check

This skill does NOT capture:
- Variable levels (VIX, DXY, rates, prices) — brief §2 owns these
- Regime labels or S/T/C/R scores — brief §1/§3
- 2-week catalyst list — brief §5. News carries 48h cut only.
- For data releases: capture **surprise delta** (actual vs expected vs prior) only, not levels.

## Step 2 — Geopolitics

Search by **category** (not named conflict). Trade/tariff/sanctions → Step 4.5 instead.

Generic searches: `sanctions today`, `military conflict today`, `diplomatic crisis today`, `territorial dispute today`, `election crisis today`, `regime change coup today`, `naval incident today`, `blockade embargo today`.

Hotspot-specific: from README.md hotspot table, run targeted search per active hotspot.

## Step 3 — Macro data releases

`US economic data releases today`, `CPI PPI NFP PCE release today`, `central bank rate decision today`. Report actual vs expected vs prior ONLY. Flag tier-1 prints.

## Step 4 — Economic calendar (48h only)

`US economic calendar this week` → table: Date/Time ET|Event|Impact|Notes. 48h window only.

## Step 4.5 — Central bank & policy communications

Searches: `{central bank} statement today`, `Fed Chair speech today`, `Treasury Secretary statement today`, `USTR statement today`, `executive order trade tariff today`.

Apply 4-criterion political-communication filter per README. Failing items tagged `⟨noise-probable⟩`.

For FOMC: rate, dot-plot delta, 2Y/10Y reaction, fed-funds-futures surprise bps.

## Step 5 — Corporate & tech (universe only)

Universe: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, AVGO, BABA, MSFT, SPY, QQQ, EWY, XLE.

**Catalyst-filtered strategy:**
1. Active tickers (from framework/Memory.md §6 48h list): run `{TICKER} earnings today` + `{TICKER} news today`
2. Catch-all: `tech earnings today`, `semiconductor earnings today` if relevant
3. Do NOT run individual searches for tickers with no scheduled catalyst.

## Step 6 — Crypto & regulatory

`Bitcoin ETF flows today`, `Ethereum ETF flows today`, `crypto regulation news today`, `SEC crypto enforcement today`, `stablecoin regulation today`, `CLARITY Act`, `GENIUS Act`.

## Step 6.5 — Credit & sovereign

`Moody's rating action today`, `S&P Global rating action today`, `Fitch rating action today`, `sovereign credit downgrade today`, `corporate default today`, `CDS spread widening today`.

## Step 7 — Flash events

`market moving news today`, `surprise event markets today`, `exchange halt today`. Omit section if nothing qualifies.

## Step 8 — Write output

Path: `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md`. Create the folder first: `mkdir -p {YYYY-MM-DD}`.

Sections: 1. Geopolitics & Political Risk | 2. Macro Data Releases (actual vs expected ONLY) | 3. Economic Calendar 48h | 4. Corporate & Tech | 5. Crypto & Regulatory | 6. Central Bank & Policy Communications | 7. Credit & Sovereign | 8. Flash Events (omit if none) | 9. Regime Implications (≤3 lines, signal vs noise handoff to brief)

Every item cites source + date. Apply 3-tier source hierarchy and 10-rule noise filter per README.

## Step 9 — Update framework/Memory.md §6 Catalysts

Rescheduled events, new catalysts, expired catalysts. Do not batch.

## Step 10 — Write catalysts cache

```python
import sys; sys.path.insert(0, 'scripts')
from catalysts_cache import write_catalysts
write_catalysts('YYYY-MM-DD', catalysts_list, horizon_days=30)
```

Required fields per catalyst: `date`, `event`, `asset_impact`, `severity` (critical|high|med|low). Optional: `direction_hint`, `source`, `notes`. Append confirmation to news file tail.
