# Trading skills — scope of skill-manager

This file is the allow-list. `skill-manager` only operates on skills in this list. Other skills in `/mnt/.claude/skills/` (utility skills like docx/pdf/pptx/xlsx, meta-skills like skill-creator/setup-cowork/schedule, consolidate-memory) are explicitly out of scope.

## Production (scheduled, scorecard/brief pipeline)

| Skill | Role | Model tier |
|---|---|---|
| market-brief | 20:00 pre-open regime + scorecard | sonnet |
| news-events | 20:10 categorised news + catalyst tagging | sonnet |
| daily-trade-rec | 21:00 8-step synthesis, ledger append | opus |
| pipeline-recovery | 22:00 skeleton/recovery fallback | haiku |
| positions-monitor | 09:00 intraday watchdog, silent-when-OK | sonnet |
| signal-review | Sun 18:00 weekly OOS mark-to-market | opus |
| quarterly-methodology-review | Quarterly meta-review of the methodology | opus |
| literature-review | Semi-annual academic factor scan | opus |
| system-review | Semi-annual strategic architecture audit | opus |

## On-demand (event-triggered)

| Skill | Role | Model tier |
|---|---|---|
| trade-update | Any entry/exit/adjust — 4-layer memory sync | sonnet |

## Reference data for scripts

```python
TRADING_SKILLS = {
    "market-brief": "sonnet",
    "news-events": "sonnet",
    "daily-trade-rec": "opus",
    "pipeline-recovery": "haiku",
    "positions-monitor": "sonnet",
    "signal-review": "opus",
    "quarterly-methodology-review": "opus",
    "literature-review": "opus",
    "system-review": "opus",
    "trade-update": "sonnet",
    "consolidate-memory": "haiku",  # included: Gerald uses it within the trading workflow
}
```

Note: `consolidate-memory` is included as a trading-adjacent utility because it's part of the memory-consolidation leg of the Sunday tidy pipeline. Remove from the allow-list if Gerald wants pure trading-only scope.
