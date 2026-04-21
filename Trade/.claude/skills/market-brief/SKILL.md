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
3. `framework/Methodology Prompt.md` — 8-step framework, Top-33 variables, evidence grading
4. `master-data-log.xlsx` — latest row of `RegimeHistory` (prior regime) and `DailyVariables` (prior readings) via openpyxl
5. `framework/Data Sources.md` — variable-to-source mapping, fail-loud rule
6. `framework/Risk Rules.md` — scan for active circuit breaker or heat constraint

## Step 2 — Read audit-data staging

Check `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` (date-folder convention; fall back to root `audit-data-staging-{YYYY-MM-DD}.md` only if the folder form is absent). If present: extract residual momentum, intermediary capital z-score, basis-momentum values. If absent: mark all three MISSING (fail-loud).

## Step 2.5 — Read meta-additions staging

Check `{YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md`. If present: extract BAB beta scores (V029), DealerGamma/GEX regime (V030), GP/A readings (V031), CEI readings (V032), and sleeve ON/OFF state from prior month-end Overlay Gate computation (V033–V035). If absent: mark all five MISSING (fail-loud) — Step 1.5 Overlay Gate will require manual pull.

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

Tier 2-only variables (use WebSearch directly): BTC exchange netflows, ETF flows, perp funding, 3m basis, ETH ETF flows, stablecoin supply, revision breadth, CFTC positioning. **FX carry direction (V015, Grade A — context only, no scorecard rows):** G10 rate differential direction; carry-unwind = cross-asset risk-off signal. **FX real valuation (V016, Grade B/A — context only):** DXY vs PPP; extreme overvaluation = commodity/equity headwind.

Staleness: LIVE/STALE-OK display normally. STALE-WARN → warning flag on score leg. MISSING (Tier 4) → fail-loud, leave score leg blank.

## Step 4 — Score regime

Per Methodology Prompt §1: Growth, Inflation, Policy, Financial conditions, Risk-on/risk-off, BTC vol regime. One-line label + 3 primary watch variables. Compare against prior RegimeHistory row — call out changes.

**Digest cross-check:** if `{today}/slack-digest-{today}.md` contains recent `[REGIME]` entries (cloud scheduled agent fires 4x/day pulling Grade A variables VIX/MOVE/DXY/US10Y/CDX-HY/SPY), compare the most recent digest readings against this step's pull. Discrepancies >1σ flag a staleness issue on one side — note which. The digest's intraday readings are authoritative for the **last-observed** value of Grade A variables between market-brief runs; this step's pull is authoritative for the 20:00 UTC+8 canonical snapshot. Both are Grade A; neither dominates.

## Step 4.5 — Overlay Regime Gate (Faber TAA — V033–V035)

Read sleeve ON/OFF state from Step 2.5 meta-additions staging. If staging absent, compute manually from prior month-end close vs 10-month SMA pulled in Step 3:
- SPY or QQQ below 10m-SMA → equity sleeve OFF
- GSCI (or commodity aggregate proxy) below 10m-SMA → commodity sleeve OFF
- BTC-USD below 10m-SMA → crypto sleeve OFF
- EFA (or EWJ/EWY proxy) below 10m-SMA → international-equity sleeve OFF

Gate semantics (binding):
- Sleeve-OFF does NOT change Sum. It multiplies post-Sum position size by 0.
- A |Sum|≥3 signal on a gated-off sleeve = promoted signal, Taken=NO, Block_Reason=OverlayGateOff. Log it; do not suppress it.
- Gate flips only at month-end close. Do not recompute intraday.

Write sleeve status (ON/OFF) into the scorecard header.

Evidence: Faber (2007) J. Wealth Mgmt. — Grade A. Meta 2026-04-18 PL-NMA rank 2/54.

## Step 5 — Build asset scorecard

Score S|T|C|R|Sum per Methodology Steps 2–6 for every asset in universe.

**Audit-addition integration (binding):**
- Equity T (single-stock): use residual momentum from staging. If MISSING → T blank.
  SCORING RULE 1: score V026 (residual momentum) only on single-stock tickers — do NOT also score V009 (raw TSMOM). Co-scoring inflates the T-signal.
- Commodity S: use basis-momentum. Divergence-cap: static backwardation (+1) but basis-mom flattening → cap S at 0.
- Cross-asset R: intermediary capital z < −1σ → downgrade R one notch.
  SCORING RULE 2: if CDX HY also flagging stress simultaneously, count once — take the more negative of the two, not their sum.

**Meta-addition integration (binding — 2026-04-18):**
- Single-stock S: add V031 GP/A (gross profitability/assets — A, Novy-Marx 2013) from staging. If MISSING → leave S leg blank for that input, note in Data Gaps.
- Single-stock S: add V032 CEI (composite equity issuance — A, Daniel-Titman 2006; negative sign: high issuance = structural headwind) from staging.
- Independent factor sleeve V029 BAB (Betting-Against-Beta — A, Frazzini-Pedersen 2014): scored separately from staging, capped at 1/3 of V009 risk budget. Do NOT aggregate into spine S/T/C/R sizing. ETF proxy: USMV/SPLV spread.
- R-overlay modifier V030 DealerGamma (B — Barbon-Buraschi 2021; single-paper): short-gamma → widen R stop by one notch; long-gamma → tighten. Do not double-count with VIX when both flag stress.
  SCORING RULE 3: V029 BAB and V030 DealerGamma are independent sleeves, each capped at 1/3 V009 budget. Correlation gate still applies when BAB sleeve + spine V009 long on the same ticker.
- Overlay Gate: apply Step 4.5 result. Sleeve-OFF → post-Sum size × 0. Log as Taken=NO, Block_Reason=OverlayGateOff. Never suppress the signal.
  SCORING RULE 4: Overlay Gate is post-Sum × 0 for sizing. Non-additive to Sum. Never suppress the signal row.

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
3. **Asset Scorecard** — table: Asset|Sleeve|S|T|C|R|Sum|Gate|Notes. Flag |Sum|≥3. Gate column: ON → eligible; OFF → Taken=NO if |Sum|≥3. List promoted (|Sum|≥3, sleeve ON) and promoted-but-gated (|Sum|≥3, sleeve OFF) below the table.
4. **Watchlist Updates** — changes to framework/Memory.md §5.
5. **Catalyst Calendar** — from cache (Step 5.5).
6. **Variable Discovery Notes** — per Step 6.

## Step 8 — Update framework/Memory.md

§5 Watchlist, §6 Catalysts. Append one line to `framework/memory-lessons.md`. Do not batch.

## Step 9 — Sync to master-data-log.xlsx

Per `framework/Excel-Sync-Protocol.md` §1. Update sheets: DailyVariables, RegimeHistory, DataQuality, CatalystLog.
