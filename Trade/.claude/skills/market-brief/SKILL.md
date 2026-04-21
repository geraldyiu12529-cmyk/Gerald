---
name: market-brief
description: "Daily US pre-open market brief — regime snapshot, variable table, S|T|C|R|Sum scorecard, Excel sync. Pulls Grade A variables via 4-tier retrieval engine. Use for 'market brief', 'daily brief', 'regime update', 'pull the numbers'. Not for trade recommendations."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily Market Brief

Produces the day's US pre-open market brief. Output: regime snapshot, full variable table with Grade A/B readings, asset scorecard. Consumed by trade-rec 25 minutes later.

Local timezone UTC+8. Canonical slot 20:00 UTC+8 = 08:00 ET. Path: `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md`. Create the date folder (`mkdir -p {YYYY-MM-DD}`) before writing. Overwrite same-day with version bump.

---

## Step 0 — Slack digest ingest

Before any other read, invoke `/slack-ingest` to pull the last 24h of scheduled-agent posts from `#trading-scheduled-updates` into `{today}/slack-digest-{today}.md`. Treat the digest as **Grade B optional context** — it informs the regime read and surfaces overnight news/alerts the cloud agent caught while the machine was off. Missing digest = proceed without, note under Data Gaps.

## Step 1 — Reads

1. `{today}/slack-digest-{today}.md` — cloud agent's overnight synthesis (Grade B). Optional.
2. `framework/Memory.md` — §2 Open Positions, §5 Watchlist, §6 Catalysts. Skip §8.
3. `framework/Methodology Prompt.md` — 8-step framework, Top-28 variables, evidence grading
4. `master-data-log.xlsx` — latest row of `RegimeHistory` (prior regime) and `DailyVariables` (prior readings) via openpyxl
5. `framework/Data Sources.md` — variable-to-source mapping, fail-loud rule
6. `framework/Risk Rules.md` — scan for active circuit breaker or heat constraint

## Step 2 — Read audit-data staging

Check `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` (date-folder convention; fall back to root `audit-data-staging-{YYYY-MM-DD}.md` only if the folder form is absent). If present: extract residual momentum, intermediary capital z-score, basis-momentum values. If absent: mark all three MISSING (fail-loud).

## Step 3 — Pull Grade A variables (batch)

```python
import sys; sys.path.insert(0, 'scripts')
from data_retrieval_engine import fetch_many, format_retrieval_summary

variables = [
    'VIX', 'VIX3M', 'MOVE', 'DXY', 'HY_OAS', 'NFCI',
    'DGS2', 'DGS10', 'DFII10', 'T10YIE',
    'SPY', 'QQQ', 'EWJ', 'EWY',
    'NVDA', 'TSLA', 'AAPL', 'GOOGL', 'AMZN', 'META',
    'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL', 'AVGO', 'BABA', 'MSFT',
    'Brent', 'WTI', 'Gold', 'Silver', 'Copper', 'Palladium', 'Platinum',
    'BTC', 'ETH', 'BTC_ActiveAddr', 'BTC_HashRate',
]
results = fetch_many(variables, web_search_fn=WebSearch)
```

Tier 2-only variables (use WebSearch directly): BTC exchange netflows, ETF flows, perp funding, 3m basis, ETH ETF flows, stablecoin supply, revision breadth, CFTC positioning.

Staleness: LIVE/STALE-OK display normally. STALE-WARN → warning flag on score leg. MISSING (Tier 4) → fail-loud, leave score leg blank.

## Step 4 — Score regime

Per Methodology Prompt §1: Growth, Inflation, Policy, Financial conditions, Risk-on/risk-off, BTC vol regime. One-line label + 3 primary watch variables. Compare against prior RegimeHistory row — call out changes.

**Digest cross-check:** if `{today}/slack-digest-{today}.md` contains recent `[REGIME]` entries (cloud scheduled agent fires 4x/day pulling Grade A variables VIX/MOVE/DXY/US10Y/CDX-HY/SPY), compare the most recent digest readings against this step's pull. Discrepancies >1σ flag a staleness issue on one side — note which. The digest's intraday readings are authoritative for the **last-observed** value of Grade A variables between market-brief runs; this step's pull is authoritative for the 20:00 UTC+8 canonical snapshot. Both are Grade A; neither dominates.

## Step 5 — Build asset scorecard

Score S|T|C|R|Sum per Methodology Steps 2–6 for every asset in universe.

**Audit-addition integration (binding):**
- Equity T (single-stock): use residual momentum from staging. If MISSING → T blank.
- Commodity S: use basis-momentum. Divergence-cap: static backwardation (+1) but basis-mom flattening → cap S at 0.
- Cross-asset R: intermediary capital z < −1σ → downgrade R one notch. Don't double-count with HY OAS.

C column mandatory: +1 (favorable), 0 (none), −1 (adverse). State surprise vs confirmation dependent.

## Step 5.5 — Catalyst cache (E4)

```python
import sys; sys.path.insert(0, 'scripts')
from catalysts_cache import read_catalysts, to_markdown_table, filter_severity
try:
    cache = read_catalysts()
    visible = filter_severity(cache, 'med')
    table_md = to_markdown_table({**cache, 'catalysts': visible}, limit=15)
    cache_status = 'OK'
except FileNotFoundError:
    table_md = "_Catalyst cache missing — inline fallback from news file._"
    cache_status = 'MISSING'
```

## Step 6 — Variable Discovery Notes

If a repeating observation is noticed (3+ times across briefs): write a Candidate row to VariableRegistry. Otherwise: "No new variable candidates observed today."

## Step 7 — Write output

Path: `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md`. Create the folder first: `mkdir -p {YYYY-MM-DD}`.

Sections in order:
1. **Regime Snapshot** — table: Dimension|State|Change. Three watch variables.
2. **Key Variable Readings** — table: Bucket|Variable|Reading|Grade|Source. MISSING count + which legs blocked.
3. **Asset Scorecard** — table: Asset|S|T|C|R|Sum|Notes. Flag |Sum|≥3.
4. **Watchlist Updates** — changes to framework/Memory.md §5.
5. **Catalyst Calendar** — from cache (Step 5.5).
6. **Variable Discovery Notes** — per Step 6.

## Step 8 — Update framework/Memory.md

§5 Watchlist, §6 Catalysts. Append one line to `framework/memory-lessons.md`. Do not batch.

## Step 9 — Sync to master-data-log.xlsx

Per `framework/Excel-Sync-Protocol.md` §1. Update sheets: DailyVariables, RegimeHistory, DataQuality, CatalystLog.
