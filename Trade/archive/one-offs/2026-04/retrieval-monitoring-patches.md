# Retrieval Monitoring Layer — Skill Patches

Skills are read-only, so these patches override skill instructions via CLAUDE.md.

## Market-brief: Add §7 Data Pipeline Health (daily)

After writing §1–§6, add a **§7 Data Pipeline Health** section:

```python
import sys; sys.path.insert(0, "/mnt/Trade/scripts")
from data_retrieval_engine import analyze_retrieval_health, format_health_summary, get_validation_warnings

health = analyze_retrieval_health(lookback_days=7)
summary = format_health_summary(health, compact=True)
warnings = get_validation_warnings()
```

- Include `summary` in §7.
- If `warnings` non-empty: bullet each as "Warning: {variable}: moved {pct}% vs cached (max expected {max}%)".
- CRITICAL status: bold callout at brief header top. DEGRADED: note in header. NOMINAL: §7 alone suffices.

## Signal-review: Add §8 Retrieval Log Analysis (weekly)

After existing sections, add **§8 Retrieval Log Analysis**:

```python
from data_retrieval_engine import analyze_retrieval_health, format_health_summary
health = analyze_retrieval_health(lookback_days=7)
full_report = format_health_summary(health, compact=False)
```

- Include `full_report` in §8.
- If `chronic_missing` non-empty: recommend investigation/source replacement.
- If status != NOMINAL: recommendation paragraph (e.g., register FRED API key, add backup source).

## Validation warnings (applies to market-brief §7)

The retrieval engine validates every fetch with: (1) static range check (reject garbage), (2) cache-proximity check (flag moves > MAX_DAILY_MOVE). Warnings are advisory, not blocking. Include in brief §7 so Gerald can spot format changes or stale-data-served-as-fresh.
