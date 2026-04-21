---
name: daily-trade-rec
description: "Pre-open trade recommendation — 8-step methodology + Risk Rules checklist + SignalLedger append + HTML report. Use for 'trade rec', 'trade recommendation', 'run the 8-step', 'score the book', 'tell me what to trade today'. Not for commentary — use market-brief or news-events."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily Trade Recommendation

Decision document, not commentary. Every section either promotes a trade or explains why it didn't. Local timezone UTC+8, canonical slot 20:20. Filename: `trade-rec-{YYYY-MM-DD}.md`.

---

## Step 0 — Delta-check gate

```python
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

trade_dir = Path('.')
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')

prior_recs = sorted(trade_dir.glob('trade-rec-*.md'))
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

upstream = [
    trade_dir / f'market-brief-{today}.md',
    trade_dir / f'news-events/news-{today}.md',
]
close_snaps = sorted(trade_dir.glob('us-close-snapshot-*.md'))
if close_snaps:
    upstream.append(close_snaps[-1])

changed = any(p.exists() and os.path.getmtime(p) > last_rec_mtime for p in upstream)
```

If `changed=False`: append no-change comment to rec file and exit. If True: proceed.

## Step 1 — Reads

**Framework:** Memory.md, Methodology Prompt.md, Risk Rules.md, master-data-log.xlsx (RegimeHistory latest row, DailyVariables latest row, SignalLedger OPEN rows for dedup).

**Upstream artifacts (today's date):**
- `market-brief-{today}.md` — regime, scorecard, levels, catalysts
- `news-events/news-{today}.md` — headlines, geopolitics, surprises
- `us-close-snapshot-{today}.md` (or most recent prior day)
- `weekly-review-{most-recent-Sunday}.md` — regime trajectory
- *(optional)* Latest `signal-review-*.md` §8 Escalation Flags

Missing framework file → stop. Missing upstream → log under Data Gaps, proceed.

## Step 2 — Upstream Synthesis

5–10 bullets, one per source file, naming the file and the single most decision-relevant fact. Conflicts called out with weighting rationale.

## Step 3 — Run 8-step methodology

For each scored asset, confirm/revise S, T, C, R, Sum. Brief does heavy lifting; this step checks C is scored and applies correlation gate.

**Audit additions:**
- Equity T (single-stock): prefer residual momentum over raw TSMOM. If they disagree, trust residual. MISSING → fail-loud §6.
- Commodity S: basis-momentum divergence-cap (static backwardation but flattening → cap S at 0). MISSING → note, score static slope.
- Cross-asset R: intermediary capital z < −1σ → downgrade R one notch. Don't double-count with HY OAS. MISSING → fail-loud §6.

**Catalyst (C) from shared cache:**
```python
import sys; sys.path.insert(0, 'scripts')
from catalysts_cache import read_catalysts, filter_for_asset, filter_severity
try:
    catalyst_cache = read_catalysts()
    catalysts_scoring = filter_severity(catalyst_cache, 'high')
    catalyst_cache_status = 'OK'
except FileNotFoundError:
    catalyst_cache = None; catalysts_scoring = []; catalyst_cache_status = 'MISSING'
```

|Sum| thresholds: ≥3 → candidate for entry. 2 → near-miss (enumerate missing leg). ≤1 → omit unless open position affected.

## Step 4 — Grade-A gap closure (optional)

If fail-loud MISSING rows AND the variable would flip a |Sum|=2 to +3, run targeted WebSearch. Common patterns:

| Gap | Search pattern | Unblocks |
|---|---|---|
| DGS2/DGS10/DFII10 | `"US 10 year yield" {date}` | rates, Gold S |
| Brent curve | `Brent crude M1 M3 futures curve {month}` | commodity S |
| BTC funding | `BTC funding rate {date} binance` | BTC R |
| Intermediary capital | `NY Fed primary dealer statistics {week}` | cross-asset R |
| Residual momentum | `Kenneth French 5-factor monthly {month}` | single-stock T |
| Basis-momentum | `Brent futures curve settlement {date}` | commodity S |

Re-score affected legs after closure.

## Step 5 — Pre-entry checklist (binding)

Every item must pass or no trade:
1. |Sum| ≥ 3 with C scored
2. Invalidation written, concrete, date-bounded
3. Correlation gate clean
4. Per-position risk ≤ 2% AND portfolio heat post-entry ≤ 8%
5. ATR stop set
6. Catalyst asymmetry stated (surprise vs confirmation)

## Step 6 — Write output

Path: `trade-rec-{YYYY-MM-DD}.md`. Section order:

```
# Trade Recommendations — YYYY-MM-DD (20:20 UTC+8) — vN

## 1. Upstream Synthesis
## 2. Regime Read
[Regime label + 3 watch variables. Signal-review escalation flags if any.]
## 3. Recommendations Table
| Asset | Direction | Entry | Stop | Target | Size | Catalyst | Grade | Correlation | Risk-rule |
[Empty table with "No actionable |Sum|≥3" if none clears checklist.]
## 4. Theses Not Taken (near-misses, |Sum|=2)
[Per candidate: asset, score legs, missing leg, specific trigger for promotion.]
## 5. Relative-Value Pairs
[Only if outright regime mixed AND valuation/carry/revisions rank cleanly.]
## 6. Data Gaps
(a) Upstream artifact coverage
(b) Audit-addition MISSING (separate for 2026-10-14 review visibility)
(c) Other Grade-A MISSING
## 7. Pre-Entry Checklist
[Walk items 1–6 if trade taken. "Not applied" if no candidate.]
## 8. Memory Updates Needed
[Concrete bullets. Include "Audit-addition contribution" bullet.]
```

## Step 7 — Apply Memory updates

Memory.md §5 (Watchlist), §2 (Open Positions if entry taken). Append to `memory-lessons.md`. Do not batch.

## Step 8 — Append to SignalLedger

Per `Excel-Sync-Protocol.md` §2. Promoted (P###, Type=Promoted, full score fields, Status=OPEN). Near-miss (N###, Type=Near-Miss, blocking leg, Status=OPEN). Dedup against existing OPEN rows. Append-only.

## Step 9.5 — Sync AuditAdditionLog + CatalystLog

Per `Excel-Sync-Protocol.md` §2.

## Step 10 — HTML report

If signal_count=0: compact report (summary, audit-additions panel, data gaps, scorecard table only).
If signal_count≥1: full report with Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`).

Full report sections: Executive Summary, Data Collected (incl. audit-additions sub-section), Analysis Methodology, Discussion, Results (score stacking with audit-addition annotations on blocked legs), Recommendations.

Charts: cross-asset risk dashboard, yield curve, real-yield decomposition, Brent curve, BTC addresses, score bars, score stacking, catalyst calendar, gap-closure doughnut, audit-addition status panel.

Path: `report-{YYYY-MM-DD}-trade-rec.html`. Single file, no external CSS.
