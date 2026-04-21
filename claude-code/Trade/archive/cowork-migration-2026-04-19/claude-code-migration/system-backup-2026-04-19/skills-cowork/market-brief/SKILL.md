---
name: market-brief
description: "Produce the daily US pre-open market brief for Gerald's trading workspace. Pulls all Grade A variables via web search, scores the regime, builds the full asset scorecard with S|T|C|R|Sum columns, reads the audit-data staging file for the three audit-addition variables, and writes the markdown brief plus Excel sync. Use this skill whenever the user asks for a 'market brief', 'daily brief', 'pre-open brief', 'regime update', 'pull the numbers', 'refresh the brief', or asks 'what's the market doing'. Also use when the scheduled task `daily-market-brief-8pm-v2` fires. Not for trade recommendations — use the daily-trade-rec skill for those."
---

# Daily Market Brief

Produces the day's US pre-open market brief for Gerald's `/Trade/` workspace. The output is a regime snapshot, a full variable table with Grade A/B readings, and an asset scorecard — the evidence base that the trade-rec skill consumes 25 minutes later.

Local timezone is UTC+8. The canonical slot is 20:00 UTC+8 = 08:00 ET = US pre-open. Use today's local date in the filename. If the file already exists from an earlier run the same day, overwrite and bump the version tag in the title (`v2`, `v3`, …).

---

## Step 1 — Mandatory startup reads

1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
2. `/mnt/Trade/Methodology Prompt.md` — the 8-step framework, Top-28 variable list, evidence grading
3. `/mnt/Trade/Memory.md` — open positions, watchlist (§5), catalysts (§6). Skip §8 (now a pointer to memory-lessons.md — the brief never uses lessons operationally).
4. `/mnt/Trade/master-data-log.xlsx` — read the latest row of `RegimeHistory` (prior regime label, growth/inflation/policy/finconditions/riskonoff) and `DailyVariables` (prior variable readings) using openpyxl. These are the authoritative current-state sources.
5. `/mnt/Trade/Data Sources.md` — the variable-to-source mapping with fail-loud rule
6. `/mnt/Trade/Risk Rules.md` — quick scan for any active circuit breaker or heat constraint

If any framework file is missing, stop and surface the gap.

## Step 2 — Read the audit-data staging file

Check for `/mnt/Trade/audit-data-staging-{YYYY-MM-DD}.md` (today's date). This file is produced by the `audit-data-compute-750pm` task at 19:50 — 10 minutes before this brief fires.

- If present: read it and extract the three audit-addition variable values (residual momentum, intermediary capital z-score, basis-momentum). These feed directly into the scorecard.
- If absent: mark all three as `MISSING — staging file not produced` in the variable table. This is correct fail-loud behavior.

## Step 2.5 — Read the meta-integration staging file (Phase 3, post-2026-04-25)

Check for `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` (today's date). This file is produced by the `preflight-meta-additions-1952pm` task at 19:52 — 8 minutes before this brief fires. It covers Phase 3 additions V029 (BAB proxy), V027 regime bucket, and V033/V034/V035 (Faber TAA overlay gates per sleeve). V030/V031/V032 remain MISSING by design (subscription / Phase 2b stub).

Extract:

- `overlay_gate_status` — the per-sleeve ON/OFF state from the V033/V034/V035 Faber table. Format as `equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF}` (and `international={ON|OFF}` if the optional EFA row is present).
- `v027_regime_bucket` — one of `expansion` (z > +0.5σ), `neutral` (−1σ ≤ z ≤ +0.5σ), `contraction` (z < −1σ). Source: today's V027 row in the staging file's reconciliation table.
- `v029_bab_spread` — the USMV − SPLV 12m spread percentage; sign tells BAB vs ANTI-BAB regime.

**Fail-loud rule.** If the staging file is absent, set `overlay_gate_status = "MISSING"`, `v027_regime_bucket = "MISSING"`, and log `meta_staging=MISSING` in the Step 9 DataQuality row. Do NOT carry forward yesterday's overlay state — overlay reads are end-of-month binary; a stale read is worse than no read. Downstream trade-rec Step 1.5 must block any Phase-3-gated sleeve if `overlay_gate_status = "MISSING"`.

**Read cadence reminder.** The overlay state flips only at end-of-month close (per `Methodology Prompt.md §Step 1.5`); intraday recompute is prohibited. The brief reads today's staging file and reports it verbatim.

## Step 3 — Pull all Grade A variables via the retrieval engine

Use the 4-tier data retrieval engine (`/mnt/Trade/scripts/data_retrieval_engine.py`) to fetch all Grade A variables. This replaces ad-hoc WebSearch calls with a resilient chain: Tier 1 (direct HTTP to Yahoo/CoinGecko/Blockchain.info) → Tier 2 (WebSearch with pre-built query bank) → Tier 3 (persistent cache with staleness classification) → Tier 4 (MISSING, fail-loud).

**Batch fetch all variables in one call:**

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from data_retrieval_engine import fetch_many, format_retrieval_summary, get_validation_warnings, analyze_retrieval_health, format_health_summary

# All Grade A variables in a single batch
variables = [
    # Cross-asset risk
    'VIX', 'VIX3M', 'MOVE', 'DXY', 'HY_OAS', 'NFCI',
    # Rates
    'DGS2', 'DGS10', 'DFII10', 'T10YIE',
    # Equities (indices + single stocks + ETFs)
    'SPY', 'QQQ', 'EWJ', 'EWY',
    'NVDA', 'TSLA', 'AAPL', 'GOOGL', 'AMZN', 'META',
    'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL',
    # Commodities
    'Brent', 'WTI', 'Gold', 'Silver', 'Copper', 'Palladium', 'Platinum',
    # FX
    'EURUSD', 'USDJPY',
    # Crypto
    'BTC', 'ETH', 'BTC_ActiveAddr', 'BTC_HashRate',
]

results = fetch_many(variables, web_search_fn=WebSearch)

# Variables that need WebSearch only (no Tier 1 source in the engine)
# These are automatically handled by Tier 2 when web_search_fn is provided:
# HY_OAS, NFCI, DFII10, T10YIE, BTC exchange netflows, BTC ETF flows,
# BTC funding, BTC 3m basis, ETH ETF flows, stablecoin supply
```

**Using the results:**
- `results['VIX'].value` → the number (e.g., 18.02)
- `results['VIX'].tier` → which tier provided it (1 = HTTP, 2 = WebSearch, 3 = cache, 4 = MISSING)
- `results['VIX'].staleness` → 'LIVE', 'STALE-OK', 'STALE-WARN', or 'STALE-EXPIRED'
- `results['VIX'].source` → e.g., 'Yahoo Finance API (^VIX)'

**For variables NOT in the engine's map** (BTC exchange netflows, BTC ETF flows, BTC perp funding, BTC 3m basis, ETH ETF flows, stablecoin supply, revision breadth, CFTC positioning):
Use WebSearch directly as before — these are Tier 2-only variables. The engine's query bank covers some; for others, use the search patterns from `Data Sources.md`.

**Staleness handling in the brief:**
- LIVE or STALE-OK: display normally (STALE-OK gets a `(stale: {date})` note)
- STALE-WARN: display with a warning flag, add caveat to the score leg
- MISSING (Tier 4): fail-loud as before — print `MISSING — [all sources attempted]`

**Retrieval summary for §7:**
```python
summary = format_retrieval_summary(results)
# Produces: "Grade A: 30 total — 24 LIVE (T1), 4 LIVE (T2), 1 STALE-OK, 1 MISSING"
```

**Fail-loud rule:** Any Grade A variable that reaches Tier 4 (MISSING) must print as `MISSING — [attempted sources listed]`. The asset's score leg stays blank rather than inferred. The engine exhausts all 4 tiers before declaring MISSING.

**Time budget:** The retrieval engine is faster than ad-hoc WebSearch because Tier 1 (direct HTTP) returns in 1–3 seconds per variable vs 5–10 seconds for WebSearch. Batch fetching 35+ variables takes ~30–60 seconds via Tier 1 alone. Prioritize Grade A over Grade B for any remaining manual WebSearch calls.

## Step 4 — Score the regime

Using the readings from Steps 2–3, produce the regime snapshot per Methodology Prompt §1:

- Growth: expansion / contraction / ambiguous
- Inflation: disinflation / reflation / stable
- Policy: easing / tightening / on hold; path surprise bias
- Financial conditions: easing / tightening
- Risk-on / risk-off cross-asset state
- BTC vol regime, funding/basis crowding, ETF flow direction

Output: one-line regime label + three primary regime variables being watched.

**Overlay gate line (Phase 3, added 2026-04-25):** append a dedicated line below the regime label:

```
Overlay gates (Step 1.5): equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF} — source: meta-additions-staging-{YYYY-MM-DD}.md (V033/V034/V035 Faber TAA)
V027 regime bucket: {expansion|neutral|contraction}  |  V029 BAB spread: {+X.XX%} ({BAB|ANTI-BAB})
```

If `overlay_gate_status = "MISSING"`, render `Overlay gates: MISSING — meta-additions-staging file not produced. Downstream trade-rec must block Phase-3-gated sleeves.` and continue — do NOT silently infer.

Compare against the prior regime label (from the latest row in `master-data-log.xlsx` RegimeHistory sheet, read in Step 1). If the label changed, call it out explicitly.

## Step 5 — Build the asset scorecard

For every asset in the universe (Methodology Prompt §0), score S | T | C | R | Sum per Steps 2–6 of the methodology.

**Audit-addition integration (binding):**
- **Equity T (single-stock only):** Use residual momentum from the staging file. If MISSING, leave T blank (fail-loud). Raw TSMOM remains authoritative for ETFs/indices, commodities, FX, crypto.
- **Commodity S:** Use basis-momentum from the staging file. Apply the divergence-cap: if static slope = backwardation (+1) but basis-momentum is flattening, cap S at 0. If MISSING, note it but still score static slope.
- **Cross-asset R:** Use intermediary capital z-score from the staging file. If z < −1σ, downgrade R by one notch on equities, commodities, FX longs. Do not double-count with HY OAS. If MISSING, note the fail-loud caveat.

**Catalyst column (C) is mandatory.** Do not omit it. Score +1 (favorable asymmetry), 0 (no near-term catalyst), or −1 (adverse catalyst). State whether the catalyst is surprise-dependent or confirmation-dependent.

Flag any asset reaching |Sum| ≥ 3 — the trade-rec will evaluate these for entry.

## Step 5.5 — Read catalysts cache (E4 shared cache)

Read the catalyst calendar from the shared cache written by `news-events` at 20:10 (10 minutes before this brief fires). Do NOT re-parse catalysts from the news file narrative — the cache is the authoritative view. Eliminates ~2–4K tokens/run of calendar restatement.

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from catalysts_cache import read_catalysts, to_markdown_table, filter_severity

try:
    cache = read_catalysts()  # latest within 3 days
    # Brief displays severity ≥ med (critical/high/med); 'low' stays in cache but not rendered
    visible = filter_severity(cache, 'med')
    cache_filtered = {**cache, 'catalysts': visible}
    table_md = to_markdown_table(cache_filtered, limit=15)
    cache_date = cache['date']
    cache_count = cache['count']
    cache_status = 'OK'
except FileNotFoundError:
    table_md = "_Catalyst cache missing — news-events may have failed. Inline fallback — pull catalyst list from the latest news-{date}.md file directly._"
    cache_date = None
    cache_count = 0
    cache_status = 'MISSING'
```

Render under §5 of the output (see Step 7 template) as:

```markdown
**Catalyst window (next 30d, severity ≥ med, source: catalysts-cache-{cache_date}.json, {cache_count} total events):**

{table_md}
```

**Rules:**
- Do NOT re-narrate catalysts in prose if they appear in the cache table.
- For regime-scoring pulls of full catalyst context (e.g. Iran-binary / FOMC / earnings-cluster), call `read_catalysts()` directly — that returns the full payload, not the filtered view.
- If `cache_status == 'MISSING'`, log `catalysts_cache=MISSING` in the Step 9 DataQuality sheet row so pipeline-recovery surfaces it.

## Step 6 — Variable Discovery Notes

At the end of the brief (after the scorecard, before Memory/Excel updates), add a section:

```
## 6. Variable Discovery Notes

[If nothing observed: "No new variable candidates observed today."]

[If something noticed:]
**Potential candidate:** {Name}
**Observation:** {What you saw, 1-2 sentences}
**Definition:** {Precise definition}
**Mechanism hypothesis:** {Why it might predict}
**Score component:** {S/T/C/R}
**Asset scope:** {Which assets}
**Evidence so far:** {Anecdotal / Weak — be honest}
```

If the observation has been seen 3+ times (check prior briefs), also write a Candidate row to the VariableRegistry sheet in `master-data-log.xlsx` per `Variable-Discovery-Protocol.md` §2.

Do NOT let discovery slow down the brief. This is a lightweight pass — if nothing stands out, write the no-candidate line and move on.

## Step 7 — Write the output file

Path: `/mnt/Trade/market-brief-{YYYY-MM-DD}.md`

Use this section order:

```
# Market Brief — YYYY-MM-DD HH:MM UTC+8 (HH:MM ET, US Pre-Open) — vN

[2–3 line summary of what changed vs prior version, new |Sum| ≥ 3 signals, and count of MISSING Grade A rows]

---

## 1. Regime Snapshot
[Table: Dimension | State | Change vs prior]
Primary regime variables watched: (1)…, (2)…, (3)…

---

## 2. Key Variable Readings
[Table: Bucket | Variable | Reading | Grade | Source / Date]
Grade A MISSING rows: [count] — [list each with which score leg it blocks]

---

## 3. Asset Scorecard
[Table: Asset | S | T | C | R | Sum | Notes]
Highlight any |Sum| ≥ 3 signals.

---

## 4. Watchlist Updates
[Changes to Memory.md §5 — new candidates, removed theses, trigger updates]

---

## 5. Catalyst Calendar (next 30d, from shared cache)
[Render `table_md` from Step 5.5 — the cache-sourced table. Include header line citing `catalysts-cache-{date}.json` and total event count. If cache_status='MISSING', render the fallback message and flag DataQuality in Step 9.]

---

## 6. Variable Discovery Notes
[Per Step 6]
```

## Step 8 — Update Memory.md (narrative sections only)

After writing the brief, apply changes to `/mnt/Trade/Memory.md`:

- §5 (Watchlist): update if any thesis was promoted/invalidated by new data
- §6 (Catalysts): refresh the rolling calendar
- `/mnt/Trade/memory-lessons.md` (Lessons): append one line: date, brief version, regime label, count of MISSING rows, any material delta vs prior brief. (Memory.m