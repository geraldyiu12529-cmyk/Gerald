---
name: daily-trade-rec
description: "Pre-open trade recommendation — 8-step methodology + Risk Rules checklist + SignalLedger append + HTML report. Use for 'trade rec', 'trade recommendation', 'run the 8-step', 'score the book', 'tell me what to trade today'. Not for commentary — use market-brief or news-events."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob mcp__fa60a538-6fb1-4c90-8c9b-8db7cba53dbc__search_files mcp__fa60a538-6fb1-4c90-8c9b-8db7cba53dbc__read_file_content mcp__fa60a538-6fb1-4c90-8c9b-8db7cba53dbc__list_recent_files
---

# Daily Trade Recommendation

Decision document, not commentary. Every section either promotes a trade or explains why it didn't. Local timezone UTC+8, canonical slot 20:20 ET pre-open. Output path: `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md`. Create the date folder first: `mkdir -p {YYYY-MM-DD}`.

**Pipeline position:** Runs after preflight (19:47) → news-events (20:00) → market-brief (20:08). Upstream artifacts must exist locally before this skill runs. Cloud versions (GDrive) are Grade B supplementary context read alongside — not substitutes.

---

## Step 0 — Delta-check gate

```python
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

trade_dir = Path('.')
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')

# Prior recs — new date-folder convention + legacy root fallback
prior_recs = sorted(
    list(trade_dir.glob('*/trade-rec-*.md')) + list(trade_dir.glob('trade-rec-*.md')),
    key=lambda p: os.path.getmtime(p)
)
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

# Glob for newest upstream files across ALL date folders — never hardcode today/.
# Handles date mismatches when cloud task (cloud-trade-rec-7pm) already wrote a
# trade-rec before the local brief ran, which would otherwise falsely skip the run.
def _newest(patterns):
    files = []
    for pat in patterns:
        files.extend(trade_dir.glob(pat))
    return max(files, key=lambda p: os.path.getmtime(p)) if files else None

briefs        = _newest([f'{today}/market-brief-{today}.md', '*/market-brief-*.md', 'market-brief-*.md'])
news_files    = _newest([f'{today}/news-{today}.md', '*/news-*.md', 'news-*.md'])
close_snaps   = _newest(['*/us-close-snapshot-*.md', 'us-close-snapshot-*.md'])

upstream = [f for f in [briefs, news_files, close_snaps] if f is not None]
changed  = any(os.path.getmtime(p) > last_rec_mtime for p in upstream)
```

If `changed=False`: append no-change comment to rec file and exit. If `True`: proceed.

---

## Step 1 — Reads

### 1a — Folder resolution (run first — never hardcode `{today}/`)

```python
from pathlib import Path; import os
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
trade_dir = Path('.')

def _newest(patterns):
    files = []
    for pat in patterns:
        files.extend(trade_dir.glob(pat))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None

brief_path        = _newest([f'{today}/market-brief-{today}.md', '*/market-brief-*.md', 'market-brief-*.md'])
news_path         = _newest([f'{today}/news-{today}.md', '*/news-*.md', 'news-*.md'])
digest_path       = _newest([f'{today}/slack-digest-{today}.md', '*/slack-digest-*.md'])
audit_path        = _newest([f'{today}/audit-data-staging-{today}.md', '*/audit-data-staging-*.md'])
meta_path         = _newest([f'{today}/meta-additions-staging-{today}.md', '*/meta-additions-staging-*.md'])
close_path        = _newest(['*/us-close-snapshot-*.md', 'us-close-snapshot-*.md'])
```

If `brief_path` is None → **stop**. Brief is a required upstream. Log under §6 Data Gaps and exit — do not proceed without it.

### 1b — Cloud data (Grade B — always read alongside local, never a substitute)

After local resolution, fetch cloud versions from Google Drive. These are produced by the 6pm/6:30pm cloud scheduled tasks and run ~2h before the local pipeline. They provide intraday context but are outranked by local Grade A pipeline files.

1. `search_files(query="market-brief {today}")` → pick most recent result → `read_file_content(file_id=<id>)` → hold as `cloud_brief` **(Grade B)**
2. `search_files(query="news {today}")` → pick most recent result → `read_file_content(file_id=<id>)` → hold as `cloud_news` **(Grade B)**

Cloud files missing or search returns no results → note under §6 Data Gaps (a), continue without. Never required.

### 1c — Slack digest

Use resolved `digest_path` (local). If None, invoke `/slack-ingest` now to produce it. Grade B optional — missing is non-fatal. Do not invoke GDrive for the digest; it is produced locally from Slack.

### 1d — Framework files (required)

- `framework/Memory.md` — §2 Open Positions, §5 Watchlist, §6 Catalysts
- `framework/Methodology Prompt.md` — 8-step framework, Top-33 variables, scoring rules, meta-integration additions
- `framework/Risk Rules.md` — pre-entry checklist, sizing, stops, correlation gate
- `master-data-log.xlsx` — RegimeHistory latest row (prior regime), DailyVariables latest row (prior readings), SignalLedger OPEN rows (dedup)

Missing framework file → stop.

### 1e — Upstream artifacts summary

| Source | Resolved path | Grade | Required |
|---|---|---|---|
| Local market brief | `brief_path` | A | **Yes — stop if None** |
| Local news | `news_path` | A | No — log gap |
| Local audit-data staging | `audit_path` | A | No — fail-loud per leg if None |
| Local meta-additions staging | `meta_path` | A | No — fail-loud per leg if None |
| Local slack digest | `digest_path` | B | No |
| Local us-close-snapshot | `close_path` | A | No — log gap |
| Local weekly review | `*/weekly-review-*.md` most recent Sunday | A | No |
| Local signal review §8 | latest `*/signal-review-*.md` | B | No |
| Cloud market brief | `cloud_brief` (GDrive) | **B** | No |
| Cloud news events | `cloud_news` (GDrive) | **B** | No |

---

## Step 2 — Upstream Synthesis

5–10 bullets, one per source file read. Each bullet names the file and the single most decision-relevant fact. Label grade inline: `(A)` for local pipeline files, `(B)` for cloud GDrive files and digest.

Where local Grade A and cloud Grade B readings conflict, local is authoritative. Call out the conflict explicitly and state the weighting rationale. Do not silently discard the discrepancy.

---

## Step 3 — Run 8-step methodology

For each asset in the universe, confirm/revise S, T, C, R, Sum. The market-brief does the heavy variable pull; this step applies the scoring rules, audit additions, meta-integration gates, and promotes signals.

### Step 1.5 — Overlay Gate (Faber TAA — binding, non-additive to Sum)

Read sleeve status from `brief_path` scorecard (market-brief computes the 10m SMA check):

- SPY/QQQ price < 10m-SMA at prior month-end → **equity sleeve OFF** (new longs blocked)
- GSCI < 10m-SMA → **commodity sleeve OFF**
- BTC < 10m-SMA → **crypto sleeve OFF**
- EFA < 10m-SMA → **international equity sleeve OFF** (EWJ, EWY)

Sleeve-OFF does NOT zero the Sum — it multiplies post-Sum position size by 0. A Sum +3 on a gated-off sleeve is logged to SignalLedger as `Taken=NO, Block_Reason=OverlayGateOff`. Record sleeve status in §3 Recommendations Table header.

### Audit additions (binding — 2026-04-14, review 2026-10-14)

Read `audit_path` for computed values:

- **Equity T (single-stock):** use residual momentum (12m FF5-residualized, V026). Prefer over raw TSMOM. When they conflict, trust residual (Blitz-Huij-Martens 2011, Grade A). `audit_path` None or value MISSING → fail-loud §6, leave T blank.
- **Commodity S:** use basis-momentum (4w/12w F1–F2 slope change, V028). Divergence-cap rule: static slope = backwardation but basis-momentum flattening → cap S at 0 regardless of static slope (Boons-Prado 2019, Grade A). `audit_path` None or MISSING → note in §6, score static slope only.
- **Cross-asset R:** intermediary capital z-score (V027). If z < −1σ → downgrade R one notch across equities, commodities, FX longs. Do not double-count with HY OAS — take the more negative, not the sum (He-Kelly-Manela 2017, Grade A). `audit_path` None or MISSING → fail-loud §6.

### Meta-integration additions (binding — 2026-04-18, review 2026-10-14)

Read `meta_path` for computed values:

- **V029 BAB** (Betting-Against-Beta, Grade A): independent factor sleeve, single-stock + ETF structural S-input. Capped at 1/3 of V009 risk budget. Do NOT aggregate into spine sizing. ETF proxy: USMV/SPLV spread. MISSING → note §6.
- **V030 DealerGamma** (Grade B, single-paper): R-overlay modifier. Short-gamma regime → widen R stop one notch; long-gamma → tighten one notch. Flag single-paper status. Do not double-count with VIX. MISSING → note §6.
- **V031 GP/A** (Gross Profitability/Assets, Grade A): single-stock structural S-input. Quarterly-rebalance discipline; use most recent quarterly financials. MISSING → note §6.
- **V032 CEI** (Composite Equity Issuance, Grade A): single-stock structural S-input. Negative sign: high net issuance = structural headwind. Quarterly frequency. MISSING → note §6.
- **V033–V035 C009 Faber TAA**: already applied in Step 1.5 above. Non-additive to Sum.

### Scoring rules from 2026-04-18 meta-integration (binding)

1. **V009 + V026 on same single-stock ticker: score V026 only** — do not sum. Raw TSMOM stays as T for indices, ETFs, commodities, FX, crypto.
2. **V027 + V004 (HY OAS) both flagging stress: count once** — take the more-negative of the two. If V027 turns negative before HY OAS widens, apply V027 notch alone.
3. **Overlay Gate sleeve-off: position size × 0** regardless of Sum. Binding at execution.
4. **V029 BAB + V030 DealerGamma: independent sleeves, each capped at 1/3 of V009 risk budget.** Neither aggregates into spine sizing. Correlation gate still applies at position-sizing.

### Catalyst (C) from shared cache

```python
import sys; sys.path.insert(0, 'scripts')
from catalysts_cache import read_catalysts, filter_severity
try:
    catalyst_cache   = read_catalysts()
    catalysts_scoring = filter_severity(catalyst_cache, 'high')
    catalyst_cache_status = 'OK'
except FileNotFoundError:
    catalyst_cache = None; catalysts_scoring = []; catalyst_cache_status = 'MISSING'
```

### Score thresholds

|Sum| ≥ 3 → candidate for entry. |Sum| = 2 → near-miss (enumerate missing leg and specific trigger). |Sum| ≤ 1 → omit unless affects open position.

---

## Step 4 — Grade-A gap closure (optional)

If fail-loud MISSING rows AND closing the gap would flip a |Sum|=2 to ≥3, run targeted WebSearch:

| Gap | Search pattern | Unblocks |
|---|---|---|
| DGS2/DGS10/DFII10 | `"US 10 year yield" {date}` | rates, Gold S |
| Brent curve | `Brent crude M1 M3 futures curve {month}` | commodity S |
| BTC funding | `BTC funding rate {date} binance` | BTC R |
| Intermediary capital | `NY Fed primary dealer statistics {week}` | cross-asset R (V027) |
| Residual momentum | `Kenneth French 5-factor monthly {month}` | single-stock T (V026) |
| Basis-momentum | `Brent futures curve settlement {date}` | commodity S (V028) |
| BAB spread | `USMV SPLV spread {date}` | single-stock S (V029) |

Re-score affected legs after gap closure.

---

## Step 5 — Pre-entry checklist (binding — all must pass or no trade)

1. |Sum| ≥ 3 with C scored (not blank)
2. Invalidation written, concrete, date-bounded
3. Correlation gate clean — shared regime variable = single theme; size to sector cap, not per-position cap; BTC + ETH ≈ one bet (~80% co-fire)
4. Per-position risk ≤ 2% AND portfolio heat post-entry ≤ 8%
5. ATR stop set (2–3× commodities/crypto, 1.5–2× equities)
6. Catalyst asymmetry stated (surprise vs. confirmation dependent)
7. **Overlay Gate clearance:** confirm sleeve is ON for the asset class (Step 1.5 above). Sleeve OFF → block entry, log `Taken=NO, Block_Reason=OverlayGateOff`.
8. **Cloud digest clearance:** scan `digest_path` (local) and `cloud_brief`/`cloud_news` (GDrive Grade B) for unresolved `[POSITION-ALERT]` entries on any open position in the same sleeve or correlated asset. If vol-band-violation (F12) or thesis-breach alert exists and has not been addressed by a trade-update event → block new entries in that sleeve until the flagged position is re-evaluated. Prevents stacking risk while an open position is in a vol-widened state.

---

## Step 6 — Write output

Path: `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md`. Create folder first: `mkdir -p {YYYY-MM-DD}`. Version-bump if same-day rerun.

```
# Trade Recommendations — YYYY-MM-DD (20:20 UTC+8) — vN

## 1. Upstream Synthesis
[Bullets per Step 2. Grade labels (A)/(B) on each. Conflict notes.]

## 2. Regime Read
[Regime label + 3 watch variables. Overlay Gate sleeve status per asset class.
 Signal-review §8 escalation flags if any.]

## 3. Recommendations Table
| Asset | Direction | Entry | Stop | Target | Size | Catalyst | Grade | Sleeve | Correlation | Risk-rule |
[Empty table with "No actionable |Sum|≥3" if none clears checklist.]

## 4. Theses Not Taken (near-misses, |Sum|=2)
[Per candidate: asset, score legs (S/T/C/R), missing leg, specific trigger for promotion.]

## 5. Relative-Value Pairs
[Only if outright regime mixed AND valuation/carry/revisions rank cleanly.]

## 6. Data Gaps
(a) Upstream artifact coverage — local and cloud
(b) Audit-addition MISSING (V026/V027/V028 — separate for 2026-10-14 review visibility)
(c) Meta-integration MISSING (V029–V032)
(d) Other Grade-A MISSING

## 7. Pre-Entry Checklist
[Walk items 1–8 if trade taken. "Not applied — no candidate" if none.]

## 8. Memory Updates Needed
[Concrete bullets. Include "Audit-addition contribution" bullet and "Meta-addition contribution" bullet.]
```

---

## Step 7 — Apply Memory updates

`framework/Memory.md` §5 (Watchlist) and §2 (Open Positions if entry taken). Append one factual line to `framework/memory-lessons.md`. Do not batch — update immediately after writing the rec file.

---

## Step 8 — Append to SignalLedger

Per `framework/Excel-Sync-Protocol.md` §2. Append-only — never overwrite existing rows.

- **Promoted signal** (P###): Type=Promoted, full S/T/C/R score fields, Entry_Price, ATR_Stop, Target_TP1/TP2, Invalidation, Inv_Date, VIX_at_Entry, Regime_Label, Taken=YES/NO, Status=OPEN. If Overlay Gate blocked: Taken=NO, Block_Reason=OverlayGateOff.
- **Near-miss** (N###): Type=Near-Miss, blocking leg, Block_Reason=missing leg name, Status=OPEN.
- Dedup against existing OPEN rows (same asset + same S/T/C/R + same blocking leg = skip).

---

## Step 9.5 — Sync AuditAdditionLog + CatalystLog

Per `framework/Excel-Sync-Protocol.md` §2.

**AuditAdditionLog:** For each V026/V027/V028/V029–V032 variable that moved a scorecard leg today:
- Date, Variable, Asset, Direction_of_Move, Score_Leg_Before, Score_Leg_After, Impact_on_Sum, Decision_Moving (YES/NO), Source_File

**CatalystLog:** Update Outcome for any catalysts whose date has passed since the last rec.

---

## Step 10 — HTML report

Path: `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html`. Single file, no external CSS.

**If signal_count = 0:** compact report — executive summary, overlay gate status panel, audit-additions panel, meta-additions panel, data gaps, scorecard table.

**If signal_count ≥ 1:** full report with Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`).

Full report sections: Executive Summary | Data Collected (audit-additions + meta-additions sub-sections) | Analysis Methodology | Discussion | Results (score stacking with V026–V032 annotations on blocked legs) | Recommendations.

Charts: cross-asset risk dashboard, yield curve, real-yield decomposition, Brent curve, BTC on-chain, score bars, score stacking, catalyst calendar, gap-closure doughnut, audit-addition status panel, overlay gate status panel.
