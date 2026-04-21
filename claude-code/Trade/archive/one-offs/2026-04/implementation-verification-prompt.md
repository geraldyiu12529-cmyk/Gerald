# Implementation Verification & Completion Prompt

**Purpose:** Verify every system component from the architecture report is actually implemented. Fix anything that isn't. Run this prompt in a single session to close all gaps.

**Context:** The system architecture report (`system-architecture-report.html`) lists 10 problems as "Solved" or "Mitigated." An audit on 2026-04-16 found that while core scripts exist (`data_retrieval_engine.py`, `cache_manager.py`, `preflight_health_check.py`), several integration points are incomplete. This prompt walks through each gap, verifies it, and either confirms it's done or implements the fix.

---

## Instructions

Work through each checkpoint below IN ORDER. For each one:
1. Run the verification test exactly as written
2. If PASS → print "CHECKPOINT N: PASS" and move on
3. If FAIL → execute the fix steps, re-test, then move on
4. At the end, produce a summary table of all results

---

## CHECKPOINT 1: Design Doc Status Header

**What:** The `Data-Retrieval-Fallback-Framework.md` header still says "Status: DESIGN — pending Gerald's approval before implementation" but the core scripts are built and the cache is populated.

**Verify:**
```python
with open('/mnt/Trade/Data-Retrieval-Fallback-Framework.md') as f:
    header = f.read(500)
assert 'DESIGN' not in header or 'ACTIVE' in header, "FAIL: status header still says DESIGN"
```

**If FAIL — Fix:**
Open `/mnt/Trade/Data-Retrieval-Fallback-Framework.md`. Change line 5 from:
```
**Status:** DESIGN — pending Gerald's approval before implementation.
```
to:
```
**Status:** ACTIVE — Phases 1-2 implemented (cache layer + retrieval engine). Phase 3 (full skill integration) and Phase 4 (derived variable fallbacks) in progress.
```

---

## CHECKPOINT 2: Retrieval Engine — Tier 1 Live Fetch

**What:** `data_retrieval_engine.py` should be able to fetch all Yahoo Finance, CoinGecko, and Blockchain.info variables via Tier 1.

**Verify:**
```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from data_retrieval_engine import fetch, fetch_many

# Test one from each source
tests = {
    'Yahoo': 'VIX',
    'CoinGecko': 'BTC',
    'Blockchain': 'BTC_ActiveAddr',
}
for source, var in tests.items():
    r = fetch(var)
    assert r.tier == 1 and r.value is not None, f"FAIL: {var} ({source}) → tier={r.tier}, value={r.value}"
    print(f"  {source} ({var}): T{r.tier} = {r.value} [{r.staleness}]")
```

**If FAIL:** Debug the specific Tier 1 source. Check if the URL format changed. If a source is genuinely down, that's expected (Tier 2/3 catches it) — only FAIL if the code is broken, not if the source is temporarily unavailable.

---

## CHECKPOINT 3: Retrieval Engine — Cache Write-Through

**What:** Every successful Tier 1 or Tier 2 fetch must automatically write to the persistent cache at `/mnt/Trade/.data-cache/`.

**Verify:**
```python
import sys, json; sys.path.insert(0, '/mnt/Trade/scripts')
from data_retrieval_engine import fetch

r = fetch('Gold')
assert r.tier in (1, 2) and r.value is not None, "FAIL: Gold fetch failed"

# Check cache was written
cache_path = '/mnt/Trade/.data-cache/Gold.json'
with open(cache_path) as f:
    cached = json.load(f)
assert cached['value'] == r.value, f"FAIL: cache value {cached['value']} != fetched {r.value}"
print(f"  Gold: fetched={r.value}, cached={cached['value']} — write-through working")
```

**If FAIL:** Check `data_retrieval_engine.py` — the `write_cache()` call should be inside `fetch()` immediately after a successful Tier 1 or Tier 2 retrieval. If missing, add:
```python
write_cache(variable, value, tier, source_name, unit)
```
after each successful retrieval block.

---

## CHECKPOINT 4: Retrieval Engine — Tier 3 Cache Fallback

**What:** When Tier 1 has no source and no `web_search_fn` is provided, the engine should fall back to Tier 3 (cache) if a cached value exists within the staleness window.

**Verify:**
```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from data_retrieval_engine import fetch

# HY_OAS has no Tier 1 (FRED blocked). Fetch without web_search_fn.
# First, seed cache if empty by doing a manual write
from cache_manager import write_cache, read_cache
existing = read_cache('HY_OAS')
if not existing:
    # Seed with a plausible value so we can test the fallback
    write_cache('HY_OAS', 350.0, staleness_window_days=2, source_tier=2, source_name='test_seed', unit='bps')
    print("  Seeded HY_OAS cache for testing")

r = fetch('HY_OAS')  # No web_search_fn
if r.tier == 3:
    print(f"  HY_OAS: T3 cache fallback working — value={r.value}, staleness={r.staleness}")
elif r.tier == 1:
    print(f"  HY_OAS: T1 unexpectedly worked — FRED may be unblocked. value={r.value}")
elif r.tier == 4:
    print("  FAIL: HY_OAS went to MISSING despite cache being seeded")
    print(f"  Attempts: {r.attempts}")
```

**If FAIL:** The `fetch()` function's Tier 3 block likely isn't reading the cache correctly. Check that it calls `read_cache(variable)` and checks the staleness classification. The cache read should happen AFTER Tier 1 and Tier 2 fail, BEFORE declaring MISSING.

---

## CHECKPOINT 5: compute_audit_additions.py — Retrieval Engine Integration

**What:** The audit-data compute script should use `data_retrieval_engine.fetch()` and `fetch_bulk()` instead of ad-hoc file reads from `/tmp/`. This is the Phase 3 integration point.

**Verify:**
```python
with open('/mnt/Trade/scripts/compute_audit_additions.py') as f:
    content = f.read()

uses_retrieval = 'data_retrieval_engine' in content or 'from data_retrieval_engine' in content
uses_cache = 'cache_manager' in content or 'from cache_manager' in content
print(f"  Uses retrieval engine: {'YES' if uses_retrieval else 'NO'}")
print(f"  Uses cache manager: {'YES' if uses_cache else 'YES' if uses_cache else 'NO'}")

if not uses_retrieval:
    print("  FAIL: compute_audit_additions.py does not import data_retrieval_engine")
    print("  This script still relies on pre-staged CSV files from /tmp/")
```

**If FAIL — Fix:**
This is the most impactful integration. Modify `compute_audit_additions.py` to:

1. At the top, add:
```python
import sys; sys.path.insert(0, str(Path(__file__).parent))
from data_retrieval_engine import fetch_bulk
from cache_manager import read_bulk_cache
```

2. Replace the current CSV-loading blocks with retrieval-engine calls. For each bulk data source:
   - **FF5 factors:** Replace `pd.read_csv('/tmp/audit-data/ff5_monthly.csv')` (or similar) with:
     ```python
     ff5_result = fetch_bulk('ff5_factors.csv', web_search_fn=web_search_fn)
     if ff5_result.tier <= 3:
         ff5_df = ff5_result.value  # DataFrame or path
     ```
   - **Stock returns:** Replace Yahoo CSV reads with `fetch_many()` for each ticker.
   - **PD statistics:** Replace with `fetch_bulk('pd_statistics.csv')`.
   - **Futures curves:** Replace with `fetch_bulk('futures_curves.csv')`.

3. Each data block should have the pattern:
```python
result = fetch_bulk(filename, web_search_fn=web_search_fn)
if result.tier == 4:  # MISSING
    # Use cache_manager fallback
    cached = read_bulk_cache(filename)
    if cached is not None:
        # Use cached data with staleness tag
    else:
        # Mark as MISSING, log to attempts
```

4. The script's output staging file (`audit-data-staging-*.md`) should now include source tier and staleness for each variable.

---

## CHECKPOINT 6: HY OAS Proxy for Intermediary Capital

**What:** When NY Fed PD data is unavailable, the system should use HY OAS weekly change as a directional substitute for the intermediary capital signal (per Fallback Framework §7).

**Verify:**
```python
with open('/mnt/Trade/scripts/compute_audit_additions.py') as f:
    content = f.read().lower()

has_proxy = 'hy_oas' in content and ('proxy' in content or 'fallback' in content or 'directional' in content)
print(f"  HY OAS directional proxy for intermediary capital: {'IMPLEMENTED' if has_proxy else 'NOT IMPLEMENTED'}")
```

**If FAIL — Fix:**
In `compute_audit_additions.py`, in the intermediary capital computation section, add after the primary NY Fed fetch fails:

```python
# Fallback: HY OAS directional proxy
# If intermediary capital data unavailable but HY OAS is available,
# use HY OAS weekly change as directional substitute (corr ~0.65-0.75)
if intermediary_z is None:
    hy_oas_result = fetch('HY_OAS', web_search_fn=web_search_fn)
    hy_oas_cached = read_cache('HY_OAS')  # For weekly change calc
    if hy_oas_result.value is not None and hy_oas_cached is not None:
        # If HY OAS widened >25bp in past week AND intermediary is cached (even stale)
        cached_intermediary = read_cache('Intermediary_Cap_Z')
        hy_weekly_change = hy_oas_result.value - hy_oas_cached.get('value', hy_oas_result.value)
        if hy_weekly_change > 25 and cached_intermediary:
            intermediary_z = cached_intermediary.get('value', None)
            intermediary_source = 'HY_OAS_proxy + stale_cache'
            print(f"  Intermediary capital: using HY OAS proxy (widened {hy_weekly_change:.0f}bp)")
```

---

## CHECKPOINT 7: DataQuality Sheet — Tier Tracking Columns

**What:** The DataQuality sheet should have columns for T1_Count, T2_Count, T3_Cache_Count, T4_Missing_Count, Retrieval_Time_Sec, and Cache_Coverage_Pct (per Fallback Framework §9).

**Verify:**
```python
from openpyxl import load_workbook
wb = load_workbook('/mnt/Trade/master-data-log.xlsx', read_only=True)
ws = wb['DataQuality']
headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
wb.close()

required = ['T1_Count', 'T2_Count', 'T3_Cache_Count', 'T4_Missing_Count', 'Retrieval_Time_Sec', 'Cache_Coverage_Pct']
missing = [col for col in required if col not in headers]
if missing:
    print(f"  FAIL: DataQuality missing columns: {missing}")
else:
    print(f"  PASS: All tier tracking columns present")
```

**If FAIL — Fix:**
```python
from openpyxl import load_workbook
wb = load_workbook('/mnt/Trade/master-data-log.xlsx')
ws = wb['DataQuality']

# Find last column
last_col = ws.max_column
new_cols = ['T1_Count', 'T2_Count', 'T3_Cache_Count', 'T4_Missing_Count', 'Retrieval_Time_Sec', 'Cache_Coverage_Pct']
for i, col_name in enumerate(new_cols):
    # Check if it already exists
    existing = [ws.cell(1, c).value for c in range(1, last_col + 1)]
    if col_name not in existing:
        ws.cell(1, last_col + 1 + i, value=col_name)

wb.save('/mnt/Trade/master-data-log.xlsx')
print("  Added tier tracking columns to DataQuality sheet")
```

---

## CHECKPOINT 8: Market-Brief Skill Integration

**What:** The market-brief skill should use the retrieval engine for data pulls (Phase 3 of the Fallback Framework). Skills are read-only, so this is enforced via CLAUDE.md patches and `retrieval-monitoring-patches.md`.

**Verify:**
```python
import os

# Check that the retrieval-monitoring-patches.md exists and is referenced in CLAUDE.md
patches_exists = os.path.exists('/mnt/Trade/retrieval-monitoring-patches.md')
with open('/mnt/.claude/CLAUDE.md') as f:
    claude_md = f.read()
patches_referenced = 'retrieval-monitoring-patches' in claude_md

print(f"  retrieval-monitoring-patches.md exists: {patches_exists}")
print(f"  Referenced in CLAUDE.md: {patches_referenced}")

if patches_exists and patches_referenced:
    print("  PASS: Monitoring patches are in place (skill will use them at runtime)")
else:
    print("  FAIL: Patches missing or not referenced")
```

**If FAIL:** The `retrieval-monitoring-patches.md` file already exists. If not referenced in CLAUDE.md, add to the "Mandatory Protocols" section:
```
- **Retrieval Monitoring:** Read `retrieval-monitoring-patches.md`. Market-brief adds §7 health section; signal-review adds §8 retrieval log.
```

**NOTE:** Full integration where the market-brief's WebSearch calls are replaced by `data_retrieval_engine.fetch()` calls requires the skill itself to execute Python code inline. Currently, skills use ad-hoc WebSearch calls in the prompt. True integration means the skill prompt instructs Claude to call `fetch()` for each variable instead of WebSearch directly. This is a PROMPT-LEVEL change in the skill's instructions, which can be made via the skill-patches directory at `/mnt/Trade/skill-patches/`.

Verify the skill patches directory:
```python
import os
patches_dir = '/mnt/Trade/skill-patches'
if os.path.isdir(patches_dir):
    files = os.listdir(patches_dir)
    print(f"  Skill patches dir: {len(files)} files — {files[:5]}")
    # Check if market-brief patch instructs using retrieval engine
    for f in files:
        if 'market' in f.lower() or 'brief' in f.lower():
            with open(os.path.join(patches_dir, f)) as fh:
                if 'data_retrieval_engine' in fh.read() or 'fetch(' in fh.read():
                    print(f"    {f}: references retrieval engine")
                else:
                    print(f"    {f}: does NOT reference retrieval engine — needs update")
else:
    print("  FAIL: skill-patches directory does not exist")
```

**If the skill patch doesn't reference the retrieval engine:** Update the market-brief skill patch to instruct Claude to use the retrieval engine. Add this block to the market-brief skill patch, in the data-pull step:

```markdown
### Data Retrieval Override (replaces ad-hoc WebSearch)

For ALL Grade A variable pulls in Steps 3–5, use the retrieval engine instead of direct WebSearch:

\```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from data_retrieval_engine import fetch_many

# Batch-fetch all Grade A variables
variables = ['VIX', 'VIX3M', 'MOVE', 'DXY', 'HY_OAS', 'NFCI', 
             'DGS2', 'DGS10', 'DFII10', 'T10YIE',
             'SPY', 'QQQ', 'NVDA', 'TSLA', 'AAPL', 'GOOGL', 'AMZN', 'META',
             'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL', 'EWJ', 'EWY',
             'Brent', 'WTI', 'Gold', 'Silver', 'Copper', 'Palladium', 'Platinum',
             'BTC', 'ETH', 'EURUSD', 'USDJPY']

results = fetch_many(variables, web_search_fn=WebSearch)

# Use results dict for scoring
for var, result in results.items():
    # result.value, result.tier, result.staleness available
    pass
\```

Variables that need WebSearch (not in the engine's Tier 1 map) will automatically fall through to Tier 2 using the engine's query bank. Variables with no web_search_fn will use Tier 3 cache. Only after all tiers fail will MISSING be declared.

After all fetches complete, generate the retrieval summary:
\```python
from data_retrieval_engine import format_retrieval_summary
summary = format_retrieval_summary(results)
# Include in §7 Data Pipeline Health
\```
```

---

## CHECKPOINT 9: Streamlining Patches — Delta-Check Gate

**What:** The daily-trade-rec should have a Step 0 delta-check gate that skips full reruns when upstream files haven't changed.

**Verify:**
```python
with open('/mnt/Trade/streamlining-patches.md') as f:
    content = f.read()

has_delta = 'delta-check' in content.lower() or 'Delta-Check' in content
with open('/mnt/.claude/CLAUDE.md') as f:
    claude_md = f.read()
claude_refs = 'streamlining-patches' in claude_md

print(f"  Delta-check gate in streamlining-patches.md: {'YES' if has_delta else 'NO'}")
print(f"  streamlining-patches.md referenced in CLAUDE.md: {'YES' if claude_refs else 'NO'}")
```

**If both YES:** PASS — the delta-check gate is defined and will be applied at runtime.

---

## CHECKPOINT 10: memory-lessons.md Redirect

**What:** All skills should write lessons to `/mnt/Trade/memory-lessons.md` instead of Memory.md §8.

**Verify:**
```python
import os
exists = os.path.exists('/mnt/Trade/memory-lessons.md')
print(f"  memory-lessons.md exists: {exists}")
if exists:
    with open('/mnt/Trade/memory-lessons.md') as f:
        lines = f.readlines()
    print(f"  memory-lessons.md: {len(lines)} lines")
```

**If exists and has content:** PASS — the file is live and being written to.

---

## FINAL SUMMARY

After running all checkpoints, produce a summary table:

```
| # | Checkpoint | Status | Action Taken |
|---|-----------|--------|-------------|
| 1 | Design doc status header | ? | ? |
| 2 | Tier 1 live fetch | ? | ? |
| 3 | Cache write-through | ? | ? |
| 4 | Tier 3 cache fallback | ? | ? |
| 5 | compute_audit integration | ? | ? |
| 6 | HY OAS proxy fallback | ? | ? |
| 7 | DataQuality tier columns | ? | ? |
| 8 | Market-brief skill integration | ? | ? |
| 9 | Delta-check gate | ? | ? |
| 10 | memory-lessons redirect | ? | ? |
```

Then update the architecture report's problems table:
- Any checkpoint that was already PASS → confirm "Solved" label
- Any checkpoint that was FAIL and is now fixed → change to "Solved"  
- Any checkpoint that was FAIL and could NOT be fixed in this session → change to "In Progress" with a note on what remains

Finally, write the updated statuses to a brief log file at `/mnt/Trade/implementation-audit-log.md` with today's date.
