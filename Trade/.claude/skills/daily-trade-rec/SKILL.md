---
name: daily-trade-rec
description: "Pre-open trade recommendation — 8-step methodology + Risk Rules checklist + SignalLedger append + HTML report. Use for 'trade rec', 'trade recommendation', 'run the 8-step', 'score the book', 'tell me what to trade today'. Not for commentary — use market-brief or news-events."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily Trade Recommendation

Decision document, not commentary. Every section either promotes a trade or explains why it didn't. Local timezone UTC+8, canonical slot 20:20. Path: `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md`. Create the date folder first: `mkdir -p {YYYY-MM-DD}`.

---

## Step 0 — Delta-check gate

```python
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

trade_dir = Path('.')
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')

# Prior recs live under any past YYYY-MM-DD/ folder (new convention) or root (legacy).
prior_recs = sorted(list(trade_dir.glob('*/trade-rec-*.md')) + list(trade_dir.glob('trade-rec-*.md')))
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

upstream = [
    trade_dir / today / f'market-brief-{today}.md',
    trade_dir / today / f'news-{today}.md',
]
# latest us-close-snapshot under any date folder (new) or root (legacy)
close_snaps = sorted(list(trade_dir.glob('*/us-close-snapshot-*.md')) + list(trade_dir.glob('us-close-snapshot-*.md')))
if close_snaps:
    upstream.append(close_snaps[-1])

changed = any(p.exists() and os.path.getmtime(p) > last_rec_mtime for p in upstream)
```

If `changed=False`: append no-change comment to rec file and exit. If True: proceed.

## Step 1 — Reads

**Framework:** framework/Memory.md, framework/Methodology Prompt.md, framework/Risk Rules.md, master-data-log.xlsx (RegimeHistory latest row, DailyVariables latest row, SignalLedger OPEN rows for dedup).

**Upstream artifacts (today's date folder `{today}/`):**
- `{today}/market-brief-{today}.md` — regime, scorecard, levels, catalysts
- `{today}/news-{today}.md` — headlines, geopolitics, surprises
- `{today}/us-close-snapshot-{today}.md` (or most recent prior day under `*/us-close-snapshot-*.md`)
- `{most-recent-Sunday}/weekly-review-{most-recent-Sunday}.md` — regime trajectory
- *(optional)* Latest `*/signal-review-*.md` §8 Escalation Flags

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

Path: `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md`. Create folder first: `mkdir -p {YYYY-MM-DD}`. Section order:

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

framework/Memory.md §5 (Watchlist), §2 (Open Positions if entry taken). Append to `framework/memory-lessons.md`. Do not batch.

## Step 8 — Append to SignalLedger

Per `framework/Excel-Sync-Protocol.md` §2. Promoted (P###, Type=Promoted, full score fields, Status=OPEN). Near-miss (N###, Type=Near-Miss, blocking leg, Status=OPEN). Dedup against existing OPEN rows. Append-only.

## Step 9.5 — Sync AuditAdditionLog + CatalystLog

Per `framework/Excel-Sync-Protocol.md` §2.

## Step 10 — HTML report

**Canonical generator:** `scripts/gen_trade_rec_html.py` (v3, fixed 20-section template). Do **not** hand-craft HTML — edit only the PER-RUN DATA block at the top of the script, then run `python scripts/gen_trade_rec_html.py`. Output: `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html` (single file, inline CSS, Chart.js 4.4.0 via CDN). Sections, charts, layout never change — only data.

**Fixed 20 sections (never reorder, never rename):**
1. Data Freshness  · 2. Portfolio Dashboard (heat gauge + stop-buffer + position cards + price-range bars + pure-runner trade-mgmt panel)  · 3. Executive Summary  · 4. Overlay Gate (Faber TAA V033–V035)  · 5. Data Collected (KEY_VARS + Audit Additions + V026 residual bar+table + Meta Additions)  · 6. Score Analysis (promoted-stack + near-miss-stack + factor-radar + factor-tilt+breakdown table)  · 7. Material Change vs Prior Run  · 8. Recommendations (new + carry-over + gate-blocked rows)  · 9. Signal Age & Time-Decay  · 10. Thesis Summary  · 11. Pre-Entry Checklists  · 12. Regime Sensitivity  · 13. Catalyst Calendar  · 14. Near-Misses  · 15. Closed-Trade Context  · 16. Asset Universe  · 17. Data Gap Closure  · 18. Discussion  · 19. Memory Updates Applied  · 20. Sources.

**9 fixed Chart.js canvases:** `scoreBar`, `nearMissBar`, `factorRadar`, `residualBar`, `heatGauge`, `stopBuffer`, `catCal`, `gapDoughnut`, `signalAge`.

**PER-RUN DATA variables to populate** (top of `gen_trade_rec_html.py` — leave structures empty for graceful empty state, never delete a variable):
- *Header/status:* `TODAY`, `VERSION`, `GEN_TIME`, `SUPERSEDES`, `STATUS_CLS`/`STATUS_TXT`, `MISS_COUNT`, `V026_ST`, `V027_ST`, `REGIME_LABEL`, `REGIME_SUB`, `PORT_NAV`, `PORT_NAV_DATE`, `TOTAL_HEAT`, `HEAT_CAP`.
- *Positions/dashboard:* `OPEN_POSITIONS` (16-tuple: pid, asset, side, entry, live, stop, tp1, tp2, size_pct, size_usd, unreal, flag_cls, flag_txt, time_stop, trail_activate, trail_cb_pct), `EXEC_CARDS`, `THESIS` dict.
- *Variables/audit:* `FRESHNESS`, `GATE_ROWS`+`GATE_NOTE`, `KEY_VARS`, `AUDIT_ROWS`, `V026_RESIDUALS`, `META_ROWS`.
- *Scoring:* `SCORE_LABELS`/`SCORE_S`/`SCORE_T`/`SCORE_C`/`SCORE_R`, `NEAR_LABELS`/`NEAR_S`/`NEAR_T`/`NEAR_C`/`NEAR_R`, `FACTOR_EXPOSURE` (size-weighted bars auto-computed).
- *Recs/decisions:* `RECS` (with optional notional + trail), `RECS_CARRY`, `RECS_BLOCKED`, `RECS_FOOTNOTE`, `DELTA_ITEMS`+`DELTA_FOOT`, `SIGNAL_AGE`, `CHECKLISTS`, `SCENARIOS`+`SENSITIVITY`, `CATALYSTS`+`CAT_LABELS`/`CAT_DATA`/`CAT_COLORS`, `NEAR_MISSES`, `CLOSED_CONTEXT`+`CLOSED_NOTE`.
- *Coverage/footer:* `GAP_DATA` (LIVE,STALE,MISSING ints), `UPSTREAM`, `DISCUSSION`, `MEMORY_UPDATES`, `SOURCES_A`, `SOURCES_B`.

**Writing standards (binding, enforced by the generator's renderers):**
- `THESIS` entries — full analytical paragraph(s), **4–8 sentences minimum** per position. Cover position/status, mechanism behind each score leg, current invalidation, time-stop logic. Use `\n\n` to split into multiple paragraphs.
- `DISCUSSION` entries — substantive paragraphs of **5–10 sentences** with a bold header question/topic. Cover regime read, risk asymmetry, catalyst sequencing, what would flip the call.

**Empty-state behaviour:** all renderers handle `[]`/`{}` gracefully (e.g. "No new promotions", "No near-misses this run"). For zero-signal days do **not** revert to a custom compact report — just leave `RECS`, `THESIS` (for new entries), etc. empty; the 20 sections still render with empty-state cells.
