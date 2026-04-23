---
name: Catalysts cache helper — API reference
description: catalysts_cache.py module at /mnt/Trade/scripts/ — eliminates 5-way catalyst duplication across news/brief/rec/weekly/Memory per E4 from system-review-2026-04-17.md
type: reference
originSessionId: d8751fb2-f392-4cae-8f6e-ed9bb25ee98c
---
## Location
`/mnt/Trade/scripts/catalysts_cache.py`

## Written by
`news-events` skill at 20:10 UTC+8 on a daily fire (after E4 news-events patch applied).

## Read by
- `market-brief` §5 (after E4 patch)
- `daily-trade-rec` §3 scoring + §5 checklist + §8 narrative (after E4 patch)
- `weekly-regime-signal-review` §7 (optional)
- `Memory.md` §6 sync (optional)
- Ad-hoc CLI: `python3 /mnt/Trade/scripts/catalysts_cache.py show|table|asset TICKER`

## API

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from catalysts_cache import (
    write_catalysts,   # news-events writes the cache after category sweep
    read_catalysts,    # brief/rec read by date (or latest)
    latest_catalysts,  # fallback: most recent within max_age_days
    filter_for_asset,  # per-ticker filter
    filter_severity,   # min-severity filter
    to_markdown_table, # compact rendering for brief/rec
)
```

### Write
```python
write_catalysts(date, catalysts, horizon_days=30, generated_by="news-events", strict=True)
```
Validates each catalyst against the schema (date, event, asset_impact, severity required; direction_hint in {binary, bullish_risk, bearish_risk, bullish_safe_haven, bearish_safe_haven, neutral}). Writes to BOTH `/mnt/Trade/catalysts-cache-YYYY-MM-DD.json` (root) and `/mnt/Trade/.catalysts-cache/catalysts-cache-YYYY-MM-DD.json`.

### Read
```python
payload = read_catalysts("2026-04-17")  # or read_catalysts() for latest
```
Raises FileNotFoundError if missing. Downstream convention: fall back to inline parsing + flag `catalysts_cache=MISSING` in DataQuality.

## Schema (per catalyst dict)
```python
{
  "date": "YYYY-MM-DD",                                            # required
  "event": "short description",                                    # required
  "asset_impact": ["TICKER1", "TICKER2"],                          # required, uppercase
  "severity": "critical|high|med|low",                             # required
  "direction_hint": "binary|bullish_risk|bearish_risk|...",        # optional
  "source": "news-YYYY-MM-DD.md §N",                               # optional
  "notes": "qualifier"                                              # optional
}
```

## Sorting
critical → high → med → low, then date ascending within each tier.

## Why
E4 proposal in `system-review-2026-04-17.md`. Catalyst calendar was duplicated 5 ways (brief §5, news §3, trade-rec §5/§8, weekly-review §7, Memory §6). Single-writer / multi-reader pattern saves ~80–120K tokens/month and eliminates a class of cross-file inconsistency.

## How to apply
- Helper script is live (tested with 5 events; sort/filter/validation/render all pass).
- Integration patches in `/mnt/Trade/patches/E4-*.md` pending Windows-side application to news-events, market-brief, daily-trade-rec SKILL.md.
