# Data Retrieval Fallback Framework

**Created:** 2026-04-16
**Authority over:** All data retrieval across the daily pipeline — audit-data-compute, market-brief, news-events, daily-trade-rec. Supersedes single-source assumptions in `Data Sources.md`.
**Status:** ACTIVE — Phases 1-2 implemented (cache layer + retrieval engine with 36 Yahoo, 2 CoinGecko, 2 Blockchain Tier 1 sources, 19 Tier 2 query banks, 44 validation ranges, 60+ cached variables). Phase 3 (full skill integration via prompt patches) and Phase 4 (derived variable fallbacks) in progress.

---

## Problem Statement

The trading system has a single point of failure on every data source. Each Grade A variable maps to exactly one retrieval method. If that method fails — source is down, web search returns no match, API changes its format, rate limiting kicks in — the variable goes MISSING immediately. There is no retry, no alternative source, no cache. A single bad web-search result cascades into blank score legs across the entire book.

The audit-data-compute task is especially fragile: it expects pre-staged CSV files that are produced by web-search in the scheduled task prompt. If that web-search step fails, the Python script gets no input files, marks all three audit-addition variables MISSING, and the brief inherits three fail-loud caveats that block scoring on equities (T-leg), commodities (S-leg), and cross-asset risk (R-overlay).

The market-brief's own data pulls have the same problem at larger scale — ~30+ Grade A variables each pulled via a single web-search query with no fallback.

**Current MISSING cascade path:**
```
Web search fails for 1 variable
  → No retry attempted
    → MISSING printed in brief
      → Score leg left blank
        → |Sum| reduced, potentially blocking a valid signal
          → "No trade" output driven by data failure, not market evidence
```

This framework eliminates that cascade for every variable in the system.

---

## Architecture: The Retrieval Chain

Every variable retrieval follows a four-tier chain. The system moves to the next tier only when the current tier fails. Each tier has its own timeout, validation, and logging.

```
Tier 1: Direct HTTP (fastest, most deterministic)
  │ urllib.request to a stable API/CSV URL
  │ Timeout: 15s per source
  │ Validation: response code 200, parseable data, value in sane range
  │
  ├── fails → Tier 2
  │
Tier 2: Web Search (broader, handles URL changes)
  │ WebSearch tool with multiple query patterns
  │ Try up to 3 different query formulations
  │ Validation: extracted number matches expected units/range
  │
  ├── fails → Tier 3
  │
Tier 3: Persistent Cache (last known good value)
  │ Read from /mnt/Trade/.data-cache/{variable}.json
  │ Contains: value, timestamp, source_tier, source_name
  │ Apply staleness classification (see §3)
  │ Validation: cache exists, not expired per staleness tier
  │
  ├── fails (no cache or expired) → Tier 4
  │
Tier 4: MISSING (fail-loud, unchanged from current behavior)
  │ Print MISSING — [all attempted sources listed]
  │ Leave score leg blank
  │ Log to DataQuality sheet
```

**Key principle:** Tier 3 (cache) means that a *temporary* source outage never produces MISSING. Only a *persistent* outage (lasting longer than the variable's staleness window) triggers fail-loud. This is the single biggest reliability improvement in the framework.

**Cache writes happen on every successful Tier 1 or Tier 2 retrieval.** The cache is always being refreshed. It's not a separate step — it's a side effect of success.

---

## 1. Sandbox Network Capabilities (Tested 2026-04-16)

Before designing source redundancy, I tested what the sandbox can actually reach via direct HTTP:

| Source | Direct HTTP | Notes |
|--------|-------------|-------|
| Yahoo Finance (chart API) | **YES** | `query1.finance.yahoo.com` — returns JSON, parseable |
| CoinGecko API | **YES** | Free, no key, rate-limited to 10-30 calls/min |
| Kenneth French library | **YES** | ZIP download works, already implemented in `fetch_ff5_from_french_library.py` |
| NY Fed website | **YES** | HTML response, needs parsing for CSV links |
| Blockchain.info API | **YES** | JSON, free, BTC metrics |
| Barchart | **YES** | HTML, needs parsing for futures data |
| FRED API | **NO** | Timeouts consistently — blocked or rate-limited from sandbox |
| FRED CSV endpoint | **NO** | Same timeout issue |

**Implication:** FRED data (HY OAS, DGS2, DGS10, DFII10, T10YIE, NFCI) cannot use direct HTTP as Tier 1. For these variables, Tier 1 is web search and Tier 2 is an alternative direct source (e.g., Yahoo Finance for yields, Treasury.gov for rates).

---

## 2. Source Redundancy Map — All Grade A Variables

### Cross-Asset Risk

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **VIX** | Yahoo Finance API (`^VIX`) | WebSearch `"VIX close today CBOE"` | Cache | 1 trading day |
| **VIX3M / VIX term structure** | Yahoo Finance API (`^VIX3M`) | WebSearch `"VIX3M index close"` | Cache | 1 trading day |
| **MOVE** | Yahoo Finance API (`^MOVE`) | WebSearch `"MOVE index bond volatility today"` | Cache | 1 trading day |
| **DXY** | Yahoo Finance API (`DX-Y.NYB`) | WebSearch `"US dollar index DXY close today"` | Cache | 1 trading day |
| **HY OAS** | WebSearch `"high yield OAS FRED BAMLH0A0HYM2 latest"` | WebSearch `"ICE BofA high yield spread today"` → WebSearch `"high yield credit spread basis points"` | Cache | 2 trading days (moves slowly) |
| **NFCI** | WebSearch `"Chicago Fed National Financial Conditions Index latest"` | WebSearch `"NFCI weekly release"` | Cache | 7 days (weekly release) |
| **Intermediary capital** | NY Fed direct HTTP → parse CSV link | WebSearch `"NY Fed primary dealer statistics equity capital"` | Cache | 14 days (weekly data, structural, slow-moving) |

### Rates

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **2Y UST** | Yahoo Finance API (`2YY=F` or `^IRX` proxy) | WebSearch `"US 2 year treasury yield today"` → WebSearch `"2 year note yield close"` | Cache | 1 trading day |
| **10Y UST** | Yahoo Finance API (`^TNX`) | WebSearch `"US 10 year treasury yield today"` | Cache | 1 trading day |
| **2s10s** | Derived (10Y - 2Y, computed locally) | WebSearch `"2s10s yield curve spread"` | Cache | 1 trading day |
| **10Y real yield** | WebSearch `"10 year TIPS real yield DFII10"` | WebSearch `"real yield 10 year inflation protected"` | Cache | 1 trading day |
| **10Y breakeven** | WebSearch `"10 year breakeven inflation T10YIE"` | Derived (10Y nominal − 10Y real, if both available) | Cache | 1 trading day |
| **ACM term premium** | NY Fed direct HTTP (monthly CSV) | WebSearch `"ACM term premium 10 year NY Fed"` | Cache | 30 days (monthly, structural) |

### Equities

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **Index/stock closes** (all 12 + ETFs) | Yahoo Finance API (`{TICKER}`) | WebSearch `"{TICKER} stock price close today"` | Cache | 1 trading day |
| **Fama-French 5-factor** | Kenneth French ZIP download (direct HTTP) | ETF proxy computation (SPY/IWM/IWD/IWF/QUAL) | Cache | 60 days (monthly factors, used for 12m regression — stale factor data still produces valid residuals) |
| **Residual momentum** | Derived from FF5 + stock returns (compute_audit_additions.py) | Single-factor market-model residual (SPY beta only — less precise but non-zero) | Cache | 30 days (monthly signal, changes slowly) |
| **Revision breadth** | WebSearch `"earnings revisions breadth S&P 500"` | WebSearch `"analyst estimate revisions this week"` | Cache | 7 days (weekly aggregated metric) |

### Commodities

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **Brent / WTI** | Yahoo Finance API (`BZ=F` / `CL=F`) | WebSearch `"Brent crude oil price today"` | Cache | 1 trading day |
| **Gold / Silver / Copper** | Yahoo Finance API (`GC=F` / `SI=F` / `HG=F`) | WebSearch `"{metal} price today"` | Cache | 1 trading day |
| **Palladium / Platinum** | Yahoo Finance API (`PA=F` / `PL=F`) | WebSearch `"{metal} price today"` | Cache | 1 trading day |
| **Futures curves (F1-F2)** | Barchart direct HTTP (parse settlement table) | WebSearch `"{commodity} futures curve contango backwardation"` | Cache | 2 trading days |
| **Basis-momentum** | Derived from curves (compute_audit_additions.py) | Derived from Barchart-scraped curves (alternative parse) | Cache | 5 trading days (4w/12w change; a few days staleness barely moves the delta) |
| **EIA crude stocks** | WebSearch `"EIA weekly petroleum status report crude"` | WebSearch `"US crude oil inventories weekly"` | Cache | 7 days (weekly release) |

### FX

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **EUR/USD, USD/JPY** | Yahoo Finance API (`EURUSD=X`, `JPY=X`) | WebSearch `"EURUSD exchange rate today"` | Cache | 1 trading day |

### Crypto

| Variable | Tier 1 | Tier 2 | Tier 3 (Cache) | Staleness Window |
|----------|--------|--------|-----------------|------------------|
| **BTC / ETH spot** | CoinGecko API (direct HTTP) | Yahoo Finance API (`BTC-USD`, `ETH-USD`) → WebSearch `"Bitcoin price today"` | Cache | 4 hours (24/7 market) |
| **BTC active addresses** | Blockchain.info API (direct HTTP) | WebSearch `"Bitcoin active addresses blockchain"` | Cache | 2 days |
| **BTC hash rate** | Blockchain.info API (direct HTTP) | WebSearch `"Bitcoin hash rate today"` | Cache | 3 days (changes slowly) |
| **BTC exchange netflows** | WebSearch `"Bitcoin exchange netflows CryptoQuant"` | WebSearch `"BTC exchange inflows outflows"` | Cache | 2 days |
| **BTC ETF flows** | WebSearch `"Bitcoin ETF net flows today Farside"` | WebSearch `"spot Bitcoin ETF flows daily"` | Cache | 1 trading day |
| **BTC perp funding** | WebSearch `"Bitcoin perpetual funding rate"` | WebSearch `"BTC funding rate Binance"` | Cache | 1 day |
| **BTC 3m basis** | WebSearch `"Bitcoin futures basis 3 month annualized"` | WebSearch `"BTC CME futures premium spot"` | Cache | 2 days |
| **ETH ETF flows** | WebSearch `"Ethereum ETF net flows"` | WebSearch `"spot Ether ETF daily flows"` | Cache | 1 trading day |

---

## 3. Staleness Classification

When a value comes from cache (Tier 3), it carries a staleness tag. The staleness window varies by variable type because different variables have different information half-lives.

| Staleness Tier | Age | Treatment in Brief | Treatment in Scoring |
|----------------|-----|--------------------|--------------------|
| **LIVE** | Fetched this run (Tier 1 or 2) | No flag | Full weight |
| **STALE-OK** | Within staleness window | Flag as `(stale: {date})` | Full weight — data is still decision-relevant |
| **STALE-WARN** | 1-2× staleness window | Flag as `STALE-WARN — {date}, {N} days old` | Score the leg but add a ⚠ caveat |
| **STALE-EXPIRED** | >2× staleness window | Treat as MISSING | Fail-loud, score leg blank |

**Examples:**
- VIX from 1 day ago (staleness window = 1 trading day): STALE-OK. Yesterday's VIX is still useful for today's regime assessment.
- VIX from 4 days ago: STALE-EXPIRED. A 4-day-old VIX is meaningless for pre-open decisions.
- ACM term premium from 20 days ago (staleness window = 30 days): STALE-OK. It's a monthly structural variable.
- FF5 factors from 45 days ago (staleness window = 60 days): STALE-OK. The 12-month OLS regression barely changes with one stale month.

**Why this matters:** Under the current system, if the French library is down for one day, residual momentum goes MISSING and all 12 single-stock T-scores are blocked. Under this framework, the cached monthly factors are STALE-OK (well within the 60-day window) and the compute runs normally. Only a 2+ month outage would trigger MISSING.

---

## 4. Cache Implementation

### Location and Format

```
/mnt/Trade/.data-cache/
  ├── manifest.json          # Index: variable → latest cache entry
  ├── VIX.json
  ├── MOVE.json
  ├── DXY.json
  ├── HY_OAS.json
  ├── DGS2.json
  ├── DGS10.json
  ├── ...
  ├── ff5_factors.csv        # Bulk cache for multi-row data
  ├── stock_returns.csv
  ├── pd_statistics.csv
  └── futures_curves.csv
```

### Single-Variable Cache Format

```json
{
  "variable": "VIX",
  "value": 18.59,
  "unit": "index",
  "timestamp": "2026-04-15T20:05:00+08:00",
  "source_tier": 1,
  "source_name": "Yahoo Finance API",
  "staleness_window_days": 1,
  "raw_response_snippet": "regularMarketPrice: 18.59"
}
```

### Bulk Cache (CSV files)

For multi-row data (FF5 factors, stock returns, futures curves, PD statistics), the cache stores the full CSV alongside a metadata sidecar:

```json
{
  "file": "ff5_factors.csv",
  "rows": 24,
  "latest_date": "202603",
  "timestamp": "2026-04-15T19:52:00+08:00",
  "source_tier": 1,
  "source_name": "Kenneth French library direct download",
  "staleness_window_days": 60
}
```

### Cache Write Rules

1. **Every successful Tier 1 or Tier 2 retrieval writes to cache.** This is automatic, not optional.
2. **Cache is on the persistent workspace** (`/mnt/Trade/.data-cache/`), not `/tmp/`. The current `/tmp/audit-data/` directory is ephemeral — it gets wiped between sessions. This is a critical fix: right now, every session starts with empty staging files.
3. **Cache is append-aware for bulk files.** If today's FF5 download has one new month, append it to the cached CSV rather than replacing the entire file.
4. **Cache never overwrites with worse data.** If Tier 1 returns 5 rows but cache has 24 rows, keep the cache and append only new rows.

### Cache Read Rules

1. Read the variable's `.json` file (or bulk CSV + sidecar).
2. Compute age: `now - timestamp`.
3. Classify staleness per §3 table.
4. If STALE-EXPIRED, treat as MISSING (do not return cached value).
5. If STALE-OK or STALE-WARN, return the value with the staleness tag.

---

## 5. Retrieval Engine Design

A single Python module (`scripts/data_retrieval_engine.py`) that all pipeline tasks use. This replaces ad-hoc web-search calls scattered across skill prompts.

### Core Interface

```python
class RetrievalResult:
    variable: str          # e.g. "VIX"
    value: Any             # float, dict, or DataFrame
    tier: int              # 1, 2, 3, or 4 (MISSING)
    source: str            # e.g. "Yahoo Finance API"
    staleness: str         # "LIVE", "STALE-OK", "STALE-WARN", "STALE-EXPIRED"
    timestamp: datetime    # when this value was produced at source
    attempts: list[dict]   # log of every tier attempted, with errors

def fetch(variable: str, web_search_fn=None) -> RetrievalResult:
    """
    Attempt to retrieve a variable through the 4-tier chain.
    web_search_fn: callable that takes a query string and returns
                   search results (bridges to Claude's WebSearch tool).
    """
```

### Tier 1 Dispatcher

```python
TIER1_SOURCES = {
    # Yahoo Finance direct HTTP
    "VIX":    {"method": "yahoo", "ticker": "^VIX"},
    "VIX3M":  {"method": "yahoo", "ticker": "^VIX3M"},
    "MOVE":   {"method": "yahoo", "ticker": "^MOVE"},
    "DXY":    {"method": "yahoo", "ticker": "DX-Y.NYB"},
    "SPY":    {"method": "yahoo", "ticker": "SPY"},
    # ... all equity/commodity/FX tickers ...

    # CoinGecko direct HTTP
    "BTC":    {"method": "coingecko", "id": "bitcoin"},
    "ETH":    {"method": "coingecko", "id": "ethereum"},

    # Blockchain.info direct HTTP
    "BTC_ActiveAddr": {"method": "blockchain_info", "chart": "n-unique-addresses"},
    "BTC_HashRate":   {"method": "blockchain_info", "chart": "hash-rate"},

    # Kenneth French direct HTTP
    "FF5_Factors": {"method": "french_library"},

    # NY Fed direct HTTP (parse for CSV download link)
    "Intermediary_Capital": {"method": "nyfed_pd"},

    # No Tier 1 available (FRED blocked from sandbox)
    "HY_OAS":  None,
    "NFCI":    None,
    "DGS2":    None,   # but Yahoo ^IRX / ^TYX are approximate alternatives
    "DGS10":   None,   # Yahoo ^TNX available as Tier 1 proxy
    "DFII10":  None,
    "T10YIE":  None,
}
```

### Tier 2 Query Bank

Each variable gets 2-3 pre-written web search queries, tried in order:

```python
TIER2_QUERIES = {
    "VIX": [
        "VIX close today CBOE",
        "CBOE volatility index VIX latest",
        "VIX index value site:yahoo.com"
    ],
    "HY_OAS": [
        "high yield OAS spread FRED BAMLH0A0HYM2 latest",
        "ICE BofA high yield option adjusted spread today",
        "high yield credit spread basis points current"
    ],
    "DGS10": [
        "US 10 year treasury yield today",
        "10 year treasury note yield close",
        "DGS10 FRED latest value"
    ],
    # ... every Grade A variable ...
}
```

### Validation Layer

Every retrieved value passes a sanity check before being accepted:

```python
VALIDATION_RANGES = {
    "VIX":      (8, 90),       # VIX below 8 or above 90 is suspect
    "MOVE":     (40, 300),
    "DXY":      (70, 130),
    "HY_OAS":   (200, 2500),   # basis points
    "DGS10":    (0.0, 15.0),   # percent
    "DGS2":     (0.0, 15.0),
    "BTC":      (5000, 500000), # USD
    "Gold":     (500, 10000),
    # ...
}
```

If a value falls outside its range, the retrieval is rejected and the next tier is tried. This catches garbage data from malformed web-search extractions.

### Cross-Validation (Optional, for Critical Variables)

For the three variables that most frequently drive trading decisions (VIX, DXY, 10Y yield), if Tier 1 and Tier 2 both return values, compare them. If they diverge by more than a threshold (e.g., >5% relative), flag a data quality warning. Use the Tier 1 value (more deterministic) but log the discrepancy.

---

## 6. Pipeline Integration

### Audit-Data-Compute Task (19:50)

**Current flow:**
```
Scheduled task prompt does web searches → writes CSVs to /tmp/audit-data/
  → runs compute_audit_additions.py → writes staging .md
```

**New flow:**
```
Scheduled task invokes data_retrieval_engine for each bulk source:
  FF5 factors:        French library (T1) → ETF proxy compute (T2) → cache (T3)
  Stock returns:       Yahoo Finance batch (T1) → WebSearch per ticker (T2) → cache (T3)
  PD statistics:       NY Fed direct (T1) → WebSearch (T2) → cache (T3)
  Futures curves:      Barchart parse (T1) → WebSearch per commodity (T2) → cache (T3)

Each successful retrieval → write to /mnt/Trade/.data-cache/ AND /tmp/audit-data/
  → runs compute_audit_additions.py (unchanged)
  → writes staging .md
  → staging .md now includes source tier + staleness for each variable
```

**Critical change:** CSVs are cached on persistent storage, not just `/tmp/`. If the scheduled task fails entirely (Claude timeout, sandbox crash), the next run finds valid cached CSVs and the compute script can still produce results from stale-but-usable data.

### Market-Brief Skill (20:00)

**Current flow:**
```
WebSearch for each Grade A variable (single query per variable)
  → if search fails, mark MISSING
```

**New flow:**
```
For each Grade A variable:
  Call data_retrieval_engine.fetch(variable, web_search_fn=WebSearch)
    → Tier 1 (direct HTTP where available)
    → Tier 2 (web search with 2-3 query patterns)
    → Tier 3 (cache with staleness tag)
    → Tier 4 (MISSING, fail-loud)

Report in the brief:
  - LIVE readings: display normally
  - STALE-OK readings: display with (stale: {date}) note
  - STALE-WARN readings: display with ⚠ flag, add caveat to score leg
  - MISSING readings: fail-loud as today
```

**The brief's DataQuality sync now includes source tier distribution:**
```
Grade A: 28 total — 22 LIVE (T1), 4 LIVE (T2), 1 STALE-OK, 1 MISSING
```

This gives you a running record of retrieval reliability. If Tier 2 usage is climbing, a source is degrading and you can investigate before it cascades to MISSING.

### Trade-Rec Skill (20:25)

No change to the trade-rec's own data retrieval — it consumes the brief and staging file. But the rec should now read and propagate staleness tags from the brief. If a score leg is based on a STALE-WARN value, the rec should note that in the pre-entry checklist as a data quality caveat (similar to current fail-loud, but less severe).

---

## 7. Derived Variable Fallback (Audit Additions)

The three audit-addition variables are *derived* — they're computed from upstream data, not fetched directly. They need their own fallback logic beyond source redundancy.

### Residual Momentum

```
Primary compute:   Full FF5 OLS (5-factor residual)
  ↓ FF5 data unavailable
Fallback compute:  Market-model residual (1-factor, SPY-only beta)
  ↓ SPY data also unavailable
Cache:             Last month's residual scores (staleness window: 30 days)
  ↓ cache expired
MISSING:           All 12 single-stock T-scores blocked
```

**Implementation:** The market-model fallback (`build_etf_proxy_factors` in `fetch_ff5_from_french_library.py`) is currently a stub returning `None`. Implement it: fetch SPY monthly returns via Yahoo Finance API, run a 1-factor regression, compute residuals. The residuals will be noisier (R-squared ~0.5-0.7 vs ~0.8-0.9 for FF5) but non-zero residuals that correctly separate stock-specific from market-driven momentum are far better than MISSING.

### Intermediary Capital

```
Primary compute:   NY Fed PD data → z-score vs 3y rolling mean
  ↓ NY Fed data unavailable
Fallback proxy:    HY OAS weekly change as directional substitute
                   (corr ~0.65-0.75 with intermediary capital post-2008)
  ↓ HY OAS also unavailable
Cache:             Last week's z-score (staleness window: 14 days)
  ↓ cache expired
MISSING:           Cross-asset R-overlay leading gate cannot fire
```

**Note:** The HY OAS proxy is explicitly a directional substitute, not a replacement. If intermediary capital z < -1σ (stress), the R downgrade fires. The proxy rule: if HY OAS widened >25bp in the past week AND intermediary capital is cached (even stale), apply the downgrade. This catches the leading-indicator property even when the precise z-score is unavailable.

### Basis-Momentum

```
Primary compute:   Barchart futures curves → F1-F2 slope → 4w/12w change
  ↓ Barchart unavailable
Fallback compute:  WebSearch "{commodity} futures contango backwardation"
                   → extract directional signal (steepening/flattening)
                   even without precise basis-momentum numbers
  ↓ WebSearch also fails
Cache:             Last week's basis-momentum (staleness window: 5 trading days)
  ↓ cache expired
Score rule:        Static F1-F2 slope only (no divergence-cap applied).
                   Note in brief: "Basis-momentum MISSING — divergence-cap inactive."
```

**Key insight:** Basis-momentum's divergence-cap is a safety check (it prevents a false +1 S-score when curve shape is exhausting). When basis-momentum is missing, the correct fallback is to use static slope WITHOUT the cap, not to block the entire S-score. This is less conservative than fail-loud MISSING but reflects the fact that basis-momentum is a refinement on top of static slope, not a standalone signal.

---

## 8. Pre-Flight Health Check (New Task)

Add a lightweight task that runs 5 minutes before the pipeline starts, testing source availability without pulling full data.

**Schedule:** 19:45 UTC+8 Mon-Fri (5 min before audit-data-compute)

**What it does:**
1. HTTP HEAD request to Yahoo Finance, CoinGecko, Kenneth French, NY Fed, Blockchain.info
2. WebSearch `"VIX close today"` as a canary query (if this returns nothing, web search is broken)
3. Check `/mnt/Trade/.data-cache/manifest.json` — are cached values available if live sources fail?
4. Write a one-line status to `/mnt/Trade/.pipeline-health.json`:

```json
{
  "timestamp": "2026-04-16T19:45:00+08:00",
  "yahoo": true,
  "coingecko": true,
  "french": true,
  "nyfed": false,
  "blockchain": true,
  "web_search": true,
  "cache_coverage": "27/30 variables cached",
  "predicted_missing": 0,
  "advisory": "NY Fed unreachable — intermediary capital will use cache (STALE-OK, 3 days old)"
}
```

The audit-data-compute task reads this file at startup. If a source is flagged as down, it skips Tier 1 for that source (saving timeout delays) and goes straight to Tier 2. This cuts wasted time from ~15s per timed-out source to zero.

---

## 9. Post-Run Diagnostics and Alerting

### Per-Run Log

Every pipeline run writes a retrieval log to `/mnt/Trade/.data-cache/retrieval-log.jsonl` (append-only):

```json
{
  "date": "2026-04-16",
  "task": "market-brief",
  "variables_attempted": 30,
  "tier1_success": 22,
  "tier2_success": 5,
  "tier3_cache_used": 2,
  "tier4_missing": 1,
  "missing_variables": ["NFCI"],
  "stale_variables": [{"name": "ACM_TP", "age_days": 18, "status": "STALE-OK"}],
  "total_retrieval_time_sec": 45,
  "slowest_variable": {"name": "HY_OAS", "time_sec": 12, "tier": 2}
}
```

### DataQuality Sheet Enhancement

The current DataQuality sheet tracks Missing_Count and Missing_Variables. Extend it with:

| New Column | Description |
|-----------|-------------|
| T1_Count | Variables successfully retrieved via Tier 1 |
| T2_Count | Variables successfully retrieved via Tier 2 |
| T3_Cache_Count | Variables served from cache |
| T4_Missing_Count | True MISSING (replaces current Missing_Count) |
| Stale_Count | Variables in STALE-OK or STALE-WARN state |
| Retrieval_Time_Sec | Total time spent on data retrieval |
| Cache_Coverage_Pct | % of Grade A variables with valid cache entries |

**Trend detection:** If `T2_Count` rises above 5 for three consecutive days, a source is degrading. If `T3_Cache_Count` rises above 3, multiple sources are failing. The weekly signal-review should check these trends and flag them.

### Weekly Health Summary

The weekly signal-review already reviews data quality. Add a subsection:

```
### Data Retrieval Health (Week of YYYY-MM-DD)
- Average MISSING rate: X% (down from Y%)
- Tier distribution: T1 avg {N}, T2 avg {N}, T3 avg {N}, T4 avg {N}
- Chronic T2 dependence (>3 days this week): [list variables]
- Source degradation alerts: [any source that failed >50% of attempts]
- Cache saves this week: {N} variables would have been MISSING without cache
```

---

## 10. Implementation Plan

### Phase 1 — Cache Layer (Highest Impact, Lowest Risk)
**Estimated effort:** 1 session

1. Create `/mnt/Trade/.data-cache/` directory structure
2. Write `scripts/cache_manager.py` — read/write/staleness logic
3. Modify `compute_audit_additions.py` to write successful fetches to persistent cache
4. Modify the audit-data-compute scheduled task to read cache as fallback when web-search fails
5. Seed the cache with today's data

**Why first:** This alone eliminates most MISSING events. Yesterday's data is almost always better than no data.

### Phase 2 — Retrieval Engine + Tier 1 Direct HTTP
**Estimated effort:** 1-2 sessions

1. Write `scripts/data_retrieval_engine.py` with the Tier 1-4 chain
2. Implement Yahoo Finance, CoinGecko, Blockchain.info, French library, NY Fed parsers
3. Implement the validation layer (range checks, sanity filters)
4. Wire into the audit-data-compute task
5. Test with all Grade A variables

### Phase 3 — Brief Integration + Tier 2 Query Bank
**Estimated effort:** 1 session

1. Build the Tier 2 query bank (2-3 queries per variable)
2. Update market-brief skill to use the retrieval engine instead of ad-hoc web searches
3. Add staleness tags to brief output format
4. Update DataQuality sync with new columns

### Phase 4 — Derived Variable Fallbacks
**Estimated effort:** 1 session

1. Implement the market-model residual fallback for residual momentum
2. Implement the HY OAS directional proxy for intermediary capital
3. Implement the directional basis-momentum fallback
4. Update `compute_audit_additions.py` with fallback compute paths

### Phase 5 — Pre-Flight Check + Diagnostics
**Estimated effort:** 1 session

1. Create the pre-flight health check task
2. Implement the retrieval log (JSONL append)
3. Extend the DataQuality sheet schema
4. Add the weekly health summary to signal-review

---

## 11. Expected Impact

### Before This Framework

| Scenario | MISSING Count | Score Legs Blocked |
|----------|--------------|-------------------|
| Normal day, all sources up | 0-2 | 0-2 |
| One source down (e.g., Yahoo) | 8-12 | 5-8 (all equities + FX + some commodities) |
| Two sources down | 15-20 | 10-15 (most of the book) |
| Audit-compute web-search fails | +3 on top of above | T (all 12 stocks), S (5 commodities), R (cross-asset) |

### After This Framework

| Scenario | MISSING Count | Score Legs Blocked |
|----------|--------------|-------------------|
| Normal day, all sources up | 0 | 0 |
| One source down (e.g., Yahoo) | 0 (Tier 2 catches all) | 0 |
| Two sources down | 0-1 (cache catches rest) | 0-1 |
| All sources down for 1 day | 0-2 (cache STALE-OK for most) | 0-1 |
| All sources down for 1 week | 5-10 (slow variables still OK, fast variables expire) | 3-6 |
| Audit-compute web-search fails | 0 (cache provides CSVs, compute runs on cached data) | 0 |

**The cache layer alone (Phase 1) reduces expected MISSING from the current 3-5 per day to near zero for any single-day outage.** The full framework makes the system resilient against multi-day outages for most variables.

---

## 12. Monitoring Layer

Three monitoring mechanisms detect degradation before it causes MISSING events.

### 12.1 Dynamic Validation (per-fetch)

Every value passes two-layer validation in `data_retrieval_engine._validate()`:

1. **Static range check** — rejects values outside the sane universe (e.g., VIX outside 8–90). Ranges widen dynamically if the cached value is near a boundary (within 20% → extends by 50%), preventing rejection of valid extreme moves.
2. **Cache-proximity check** — if a new reading deviates from the cached value by more than `MAX_DAILY_MOVE[variable]` (e.g., >50% for VIX, >5% for DXY), it's flagged as suspicious but still accepted. Warnings accumulate in `_validation_warnings` and are surfaced via `get_validation_warnings()`.

This catches: stale data served as fresh, format changes returning a different variable's value, unit mismatches.

### 12.2 Tier Degradation Detection (per-run + lookback)

`data_retrieval_engine.analyze_retrieval_health(lookback_days=7)` reads `retrieval-log.jsonl` and computes:

- **Tier distribution** — latest run vs 7-day average for T1/T2/T3/T4 percentages
- **Alert thresholds:**
  - T1 success rate drops >15 pp below average → alert
  - T3 cache dependency rises >15 pp above average → alert
  - T4 MISSING >3 in any single run → alert
  - Any variable MISSING on 3+ days in the window → chronic MISSING alert
- **Status classification:** NOMINAL / DEGRADED / CRITICAL

`format_health_summary(health, compact=True/False)` renders the analysis as a markdown snippet for the brief (compact) or weekly review (full table).

### 12.3 Skill Integration

- **Daily market-brief (§7):** Compact health summary (2-3 lines) + any validation warnings. CRITICAL status triggers a bold callout in the brief header.
- **Weekly signal-review (§8):** Full health report with tier distribution table, chronic MISSING list, and remediation recommendations.

Both skill patches are defined in `CLAUDE.md` § "Retrieval Monitoring Layer" (since skill files are read-only).

### 12.4 Retrieval Log

Every pipeline run appends to `/mnt/Trade/.data-cache/retrieval-log.jsonl` via `cache_manager.append_retrieval_log()`. Each entry records: date, task name, variables attempted, per-tier success counts, MISSING variable list, stale variable list, retrieval time.

The log is the foundation for all degradation detection. If it grows large (>1000 entries), the weekly signal-review should truncate entries older than 90 days.

---

## 13. What This Does NOT Cover

- **Data correctness.** This framework ensures data is *available*, not that it's *right*. A source that returns stale or erroneous values (e.g., Yahoo showing yesterday's close as today's) is partially covered by the cache-proximity validation check (§12.1) but full semantic correctness is a separate problem.
- **New variable onboarding.** When a variable is promoted from the pipeline to Grade A, someone must add it to the source redundancy map, validation ranges, and cache configuration. Add this as a step in the quarterly review's promotion checklist.
- **Cost.** All sources in this framework are free. If FRED access is needed for precision (as opposed to Yahoo/web-search proxies for yields), a free FRED API key ($0, but requires registration) would restore Tier 1 for all FRED series.
