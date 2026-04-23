#!/usr/bin/env python3
"""
Trading System — Claude Code Bootstrap
Run from your Trade/ directory:  python3 claude-code-migration/setup-claude-code.py
Creates .claude/ with all config, rules, and 11 skills. Does NOT touch existing files.
"""
import os, sys
from pathlib import Path

ROOT = Path('.')
CLAUDE_DIR = ROOT / '.claude'

def w(rel_path: str, content: str):
    """Write file, creating parent dirs. Skip if already exists."""
    p = CLAUDE_DIR / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        print(f"  SKIP (exists): .claude/{rel_path}")
        return
    p.write_text(content, encoding='utf-8')
    print(f"  WROTE: .claude/{rel_path}")

# ── Sanity check ──────────────────────────────────────────────
required = ['Methodology Prompt.md', 'Risk Rules.md', 'Memory.md', 'master-data-log.xlsx']
missing = [f for f in required if not (ROOT / f).exists()]
if missing:
    print(f"ERROR: Run this from your Trade/ directory. Missing: {missing}")
    sys.exit(1)

print("=== Trading System — Claude Code Bootstrap ===\n")

# ╔══════════════════════════════════════════════════════════════╗
# ║  1. CLAUDE.md — lean project instructions                   ║
# ╚══════════════════════════════════════════════════════════════╝
w('CLAUDE.md', r"""# Gerald's Trading Research System

Discretionary cross-asset + crypto trader using an evidence-graded 8-step methodology.
Timezone: UTC+8. "No trade" is always a valid output.

## Asset Universe (do not expand without permission)
Crypto: BTC, ETH. Equities: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC.
ETFs: QQQ, SPY, EWJ, EWY. Commodities: Brent, WTI, Gold, Silver, Copper, Palladium, Platinum.
FX: EURUSD, USDJPY.

## Authoritative Documents — load ONLY when a skill requires them
| Document | Authority over | Loaded by |
|---|---|---|
| `Methodology Prompt.md` | 8-step framework, evidence grades, scoring, Top-28 variables | brief, trade-rec, signal-review, quarterly-review |
| `Risk Rules.md` | Pre-entry checklist, sizing, stops, circuit breakers, correlation gate | trade-rec, trade-update, positions-monitor |
| `Data Sources.md` | Variable→source mapping, fail-loud rule, 4-tier retrieval | brief, preflight |
| `Coin core.md` / `Trad core.md` | Research evidence base | literature-review, quarterly-review ONLY |
| `Memory.md` | Open positions, watchlist, catalysts, closed trades | Most skills (see SKILL.md) |
| `Retention Policy.md` | File tiering, archival | workspace-tidy ONLY |
| `Excel-Sync-Protocol.md` | Column mappings for master-data-log.xlsx | brief, trade-rec, signal-review, trade-update |

**CRITICAL: Do NOT load all documents at session start. Each skill specifies its own reads. This is the primary token-saving mechanism.**

## Evidence Grade Discipline
- A = replicated, coherent mechanism, long history. B = regime-dependent. C = weak/anecdotal.
- Cite grades (A/B/C) on every signal reference.
- Never pad with Grade C unless explicitly asked. No stock-to-flow timing.
- Fail-loud on MISSING Grade A variables — never silently infer.

## Memory Protocol
- Update immediately — don't batch to end of session.
- Two systems: `Memory.md` (trader working state) + auto-memory (cross-session).
- Use absolute dates (YYYY-MM-DD), never relative.
- Memory.md §3/§4/§10 removed — regime/variable state lives in `master-data-log.xlsx`.

## Behavioral Rules
- Follow the 8-step methodology sequence exactly. Do not skip steps.
- Every sentence in a briefing must inform a decision or manage a risk. No padding.
- Do not present ungrounded assertions as evidence.
- Fail-loud on missing data — state what's missing and which score leg it blocks.

## Excel — sole structured store
- `master-data-log.xlsx`: 9 sheets (SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, NearMissLedger, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes).
- Read `Excel-Sync-Protocol.md` before any xlsx write. Use openpyxl.
- Append-only for SignalLedger rows. Never delete or overwrite existing signal data.

## Pipeline File Conventions
- Dated outputs at workspace root: `market-brief-YYYY-MM-DD.md`, `trade-rec-YYYY-MM-DD.md`, `report-YYYY-MM-DD-trade-rec.html`, `us-close-snapshot-YYYY-MM-DD.md`
- News: `news-events/news-YYYY-MM-DD.md`
- Scripts: `scripts/` (data_retrieval_engine.py, compute_audit_additions.py, pipeline_status.py, catalysts_cache.py, cache_manager.py, etc.)
- Cache: `.data-cache/` (persistent, staleness-classified per Data Sources.md)
- Pipeline state: `.pipeline-status.json`, `.pipeline-health.json`

## 2026-04-14 Audit Additions (Grade A, review due 2026-10-14)
Three variables added to the scoring pipeline:
1. **Residual momentum** (12m FF5-residualized) → single-stock T-input. Prefer over raw TSMOM when they disagree.
2. **Intermediary capital ratio** (NY Fed PD z-score) → cross-asset R-overlay. If z < −1σ, downgrade R by one notch. Don't double-count with HY OAS.
3. **Basis-momentum** (4w/12w F1–F2 slope change) → commodity S-input. Divergence-cap: if static slope = backwardation but basis-momentum flattening, cap S at 0.
""")

# ╔══════════════════════════════════════════════════════════════╗
# ║  2. settings.json — permissions + hooks                      ║
# ╚══════════════════════════════════════════════════════════════╝
w('settings.json', r"""{
  "permissions": {
    "allow": [
      "Bash(python3 *)",
      "Bash(python *)",
      "Bash(pip install * --break-system-packages)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "WebSearch",
      "WebFetch"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(echo $TOOL_INPUT | python3 -c \"import sys,json; print(json.load(sys.stdin).get('file_path',''))\" 2>/dev/null); if echo \"$FILE\" | grep -qE 'trade-rec-.*\\.md$'; then echo 'Trade rec written — verify SignalLedger append in Step 8'; fi"
          }
        ]
      }
    ]
  }
}
""")

# ╔══════════════════════════════════════════════════════════════╗
# ║  3. Path-scoped rules                                       ║
# ╚══════════════════════════════════════════════════════════════╝
w('rules/evidence-grades.md', r"""---
globs: ["market-brief-*.md", "trade-rec-*.md", "signal-review-*.md", "weekly-review-*.md"]
---

# Evidence Grade Rules

When writing any trading analysis file:
- Cite evidence grades (A/B/C) on every variable and signal reference
- Grade A: replicated across samples, coherent economic mechanism, long history (momentum, carry, credit spreads, policy surprises, BTC order imbalance)
- Grade B: moderate, regime-dependent (news sentiment, options skew, MVRV/SOPR, exchange flows)
- Grade C: weak, narrative-heavy (stock-to-flow, halving cycles, seasonality)
- Never present Grade C as actionable without explicit qualification
- No stock-to-flow or halving-cycle timing — these are Grade C at best
- Fail-loud on MISSING Grade A: print `MISSING — [sources attempted]`, leave score leg blank
""")

w('rules/risk-rules-summary.md', r"""---
globs: ["trade-rec-*.md", "report-*-trade-rec.html"]
---

# Risk Rules — Pre-Entry Checklist (binding)

Full rules in `Risk Rules.md`. Summary for quick reference:

**Pre-entry — ALL must pass or no trade:**
1. |Sum| ≥ 3 with C scored (not blank)
2. Invalidation written, concrete, date-bounded
3. Correlation gate clean (shared regime variable = single theme, size to sector cap)
4. Per-position risk ≤ 2% AND post-entry portfolio heat ≤ 8%
5. ATR stop set (2–3× commodities/crypto, 1.5–2× equities)
6. Catalyst asymmetry stated (surprise vs confirmation dependent)

**Sizing:** Inverse-ATR with quarter-Kelly cap, max 25% single position.
**Heat limits:** 6–8% total, 25% sector cap, 5–15% crypto cap.
**Drawdown breakers:** −15% → 50% reduce; −20% → defensive (gold + cash).
**Correlation gate:** BTC + ETH ≈ one bet (~80% co-fire). Never double-count.
""")

# ╔══════════════════════════════════════════════════════════════╗
# ║  4. Skills                                                   ║
# ╚══════════════════════════════════════════════════════════════╝

# ── market-brief ──────────────────────────────────────────────
w('skills/market-brief/SKILL.md', r"""---
name: market-brief
description: "Daily US pre-open market brief — regime snapshot, variable table, S|T|C|R|Sum scorecard, Excel sync. Pulls Grade A variables via 4-tier retrieval engine. Use for 'market brief', 'daily brief', 'regime update', 'pull the numbers'. Not for trade recommendations."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily Market Brief

Produces the day's US pre-open market brief. Output: regime snapshot, full variable table with Grade A/B readings, asset scorecard. Consumed by trade-rec 25 minutes later.

Local timezone UTC+8. Canonical slot 20:00 UTC+8 = 08:00 ET. Filename: `market-brief-{YYYY-MM-DD}.md`. Overwrite same-day with version bump.

---

## Step 1 — Reads

1. `Memory.md` — §2 Open Positions, §5 Watchlist, §6 Catalysts. Skip §8.
2. `Methodology Prompt.md` — 8-step framework, Top-28 variables, evidence grading
3. `master-data-log.xlsx` — latest row of `RegimeHistory` (prior regime) and `DailyVariables` (prior readings) via openpyxl
4. `Data Sources.md` — variable-to-source mapping, fail-loud rule
5. `Risk Rules.md` — scan for active circuit breaker or heat constraint

## Step 2 — Read audit-data staging

Check `audit-data-staging-{YYYY-MM-DD}.md`. If present: extract residual momentum, intermediary capital z-score, basis-momentum values. If absent: mark all three MISSING (fail-loud).

## Step 3 — Pull Grade A variables (batch)

```python
import sys; sys.path.insert(0, 'scripts')
from data_retrieval_engine import fetch_many, format_retrieval_summary

variables = [
    'VIX', 'VIX3M', 'MOVE', 'DXY', 'HY_OAS', 'NFCI',
    'DGS2', 'DGS10', 'DFII10', 'T10YIE',
    'SPY', 'QQQ', 'EWJ', 'EWY',
    'NVDA', 'TSLA', 'AAPL', 'GOOGL', 'AMZN', 'META',
    'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL',
    'Brent', 'WTI', 'Gold', 'Silver', 'Copper', 'Palladium', 'Platinum',
    'EURUSD', 'USDJPY',
    'BTC', 'ETH', 'BTC_ActiveAddr', 'BTC_HashRate',
]
results = fetch_many(variables, web_search_fn=WebSearch)
```

Tier 2-only variables (use WebSearch directly): BTC exchange netflows, ETF flows, perp funding, 3m basis, ETH ETF flows, stablecoin supply, revision breadth, CFTC positioning.

Staleness: LIVE/STALE-OK display normally. STALE-WARN → warning flag on score leg. MISSING (Tier 4) → fail-loud, leave score leg blank.

## Step 4 — Score regime

Per Methodology Prompt §1: Growth, Inflation, Policy, Financial conditions, Risk-on/risk-off, BTC vol regime. One-line label + 3 primary watch variables. Compare against prior RegimeHistory row — call out changes.

## Step 5 — Build asset scorecard

Score S|T|C|R|Sum per Methodology Steps 2–6 for every asset in universe.

**Audit-addition integration (binding):**
- Equity T (single-stock): use residual momentum from staging. If MISSING → T blank.
- Commodity S: use basis-momentum. Divergence-cap: static backwardation (+1) but basis-mom flattening → cap S at 0.
- Cross-asset R: intermediary capital z < −1σ → downgrade R one notch. Don't double-count with HY OAS.

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

Path: `market-brief-{YYYY-MM-DD}.md`

Sections in order:
1. **Regime Snapshot** — table: Dimension|State|Change. Three watch variables.
2. **Key Variable Readings** — table: Bucket|Variable|Reading|Grade|Source. MISSING count + which legs blocked.
3. **Asset Scorecard** — table: Asset|S|T|C|R|Sum|Notes. Flag |Sum|≥3.
4. **Watchlist Updates** — changes to Memory.md §5.
5. **Catalyst Calendar** — from cache (Step 5.5).
6. **Variable Discovery Notes** — per Step 6.

## Step 8 — Update Memory.md

§5 Watchlist, §6 Catalysts. Append one line to `memory-lessons.md`. Do not batch.

## Step 9 — Sync to master-data-log.xlsx

Per `Excel-Sync-Protocol.md` §1. Update sheets: DailyVariables, RegimeHistory, DataQuality, CatalystLog.
""")

# ── news-events ───────────────────────────────────────────────
w('skills/news-events/SKILL.md', r"""---
name: news-events
description: "Daily news capture — geopolitics, macro, earnings, crypto, credit, flash events. Searches by category, writes structured file + catalysts cache for downstream brief/trade-rec. Use for 'news capture', 'daily news', 'what happened today', 'overnight headlines'. Not for regime scoring or trade recommendations."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Daily News & Events Capture

Produces structured news log for `news-events/news-{YYYY-MM-DD}.md`. Consumed by trade-rec upstream synthesis. Local timezone UTC+8, canonical slot 20:10.

---

## Step 1 — Reads

1. `Memory.md` — §2 Open Positions (what's live), §6 Catalysts (48h active tickers)
2. `master-data-log.xlsx` — latest RegimeHistory row via openpyxl
3. `news-events/README.md` — format spec, hotspot list, source hierarchy, noise filters, political-communication filter
4. Prior day's `news-{YYYY-MM-DD}.md` — for delta detection

Do NOT read Methodology Prompt, Risk Rules, or research cores. This skill does not score.

## Step 1.5 — Non-overlap check

This skill does NOT capture:
- Variable levels (VIX, DXY, rates, prices) — brief §2 owns these
- Regime labels or S/T/C/R scores — brief §1/§3
- 2-week catalyst list — brief §5. News carries 48h cut only.
- For data releases: capture **surprise delta** (actual vs expected vs prior) only, not levels.

## Step 2 — Geopolitics

Search by **category** (not named conflict). Trade/tariff/sanctions → Step 4.5 instead.

Generic searches: `sanctions today`, `military conflict today`, `diplomatic crisis today`, `territorial dispute today`, `election crisis today`, `regime change coup today`, `naval incident today`, `blockade embargo today`.

Hotspot-specific: from README.md hotspot table, run targeted search per active hotspot.

## Step 3 — Macro data releases

`US economic data releases today`, `CPI PPI NFP PCE release today`, `central bank rate decision today`. Report actual vs expected vs prior ONLY. Flag tier-1 prints.

## Step 4 — Economic calendar (48h only)

`US economic calendar this week` → table: Date/Time ET|Event|Impact|Notes. 48h window only.

## Step 4.5 — Central bank & policy communications

Searches: `{central bank} statement today`, `Fed Chair speech today`, `Treasury Secretary statement today`, `USTR statement today`, `executive order trade tariff today`.

Apply 4-criterion political-communication filter per README. Failing items tagged `⟨noise-probable⟩`.

For FOMC: rate, dot-plot delta, 2Y/10Y reaction, fed-funds-futures surprise bps.

## Step 5 — Corporate & tech (universe only)

Universe: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, SPY, QQQ, EWY, XLE.

**Catalyst-filtered strategy:**
1. Active tickers (from Memory §6 48h list): run `{TICKER} earnings today` + `{TICKER} news today`
2. Catch-all: `tech earnings today`, `semiconductor earnings today` if relevant
3. Do NOT run individual searches for tickers with no scheduled catalyst.

## Step 6 — Crypto & regulatory

`Bitcoin ETF flows today`, `Ethereum ETF flows today`, `crypto regulation news today`, `SEC crypto enforcement today`, `stablecoin regulation today`, `CLARITY Act`, `GENIUS Act`.

## Step 6.5 — Credit & sovereign

`Moody's rating action today`, `S&P Global rating action today`, `Fitch rating action today`, `sovereign credit downgrade today`, `corporate default today`, `CDS spread widening today`.

## Step 7 — Flash events

`market moving news today`, `surprise event markets today`, `exchange halt today`. Omit section if nothing qualifies.

## Step 8 — Write output

Path: `news-events/news-{YYYY-MM-DD}.md`

Sections: 1. Geopolitics & Political Risk | 2. Macro Data Releases (actual vs expected ONLY) | 3. Economic Calendar 48h | 4. Corporate & Tech | 5. Crypto & Regulatory | 6. Central Bank & Policy Communications | 7. Credit & Sovereign | 8. Flash Events (omit if none) | 9. Regime Implications (≤3 lines, signal vs noise handoff to brief)

Every item cites source + date. Apply 3-tier source hierarchy and 10-rule noise filter per README.

## Step 9 — Update Memory.md §6 Catalysts

Rescheduled events, new catalysts, expired catalysts. Do not batch.

## Step 10 — Write catalysts cache

```python
import sys; sys.path.insert(0, 'scripts')
from catalysts_cache import write_catalysts
write_catalysts('YYYY-MM-DD', catalysts_list, horizon_days=30)
```

Required fields per catalyst: `date`, `event`, `asset_impact`, `severity` (critical|high|med|low). Optional: `direction_hint`, `source`, `notes`. Append confirmation to news file tail.
""")

# ── daily-trade-rec ───────────────────────────────────────────
w('skills/daily-trade-rec/SKILL.md', r"""---
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
""")

# ── pipeline-recovery ─────────────────────────────────────────
w('skills/pipeline-recovery/SKILL.md', r"""---
name: pipeline-recovery
description: "Pipeline health monitoring + recovery. Phase A: fast triage (<3K tokens). Phase B: recovery only if unhealthy. Use for 'check the pipeline', 'is the pipeline healthy', 'fix the pipeline', 'what failed today', 'pipeline status'."
model: haiku
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# Pipeline Recovery

Two-phase: Phase A (cheap triage via JSON + file stats) → Phase B (recovery if unhealthy). Token target: healthy <3K, recovery <15K.

## Step 1 — Phase A: fast triage

```python
import sys; sys.path.insert(0, 'scripts')
from pipeline_status import PipelineStatus
ps = PipelineStatus()
fast = ps.fast_health_check()
print(fast['summary'])
```

Returns: `healthy`, `assessment` (per-task state/streak/validity), `escalations`, `self_healed`, `prior_recovery_crash`.

## Step 2 — Healthy fast exit

If `fast['healthy']`: `ps.clear_watchdog_healthy()`, print summary, stop. In scheduled mode: no further work (no Methodology, no Memory, no Excel). Interactive mode: continue to Step 6.

## Step 3 — Phase B entry

`ps.start_watchdog()` — marks recovery in-progress for crash detection.

## Step 4 — Recovery actions (dependency order)

**4a. Preflight:** HTTP ping sweep, retry compute script, check cache fallback, validate staging file.
**4b. Market-brief:** Cache-brief if ≥20 Grade A from cache. Never overwrite real file. Validate via `validate_recovery_brief()`.
**4c. News-events:** Skeleton file if no file exists. Degrades C-leg but doesn't block trade-rec.
**4d. Trade-rec:** Do NOT re-run (past decision window, too expensive). Leave as FAIL.
**4e. Excel sync:** Read-only diagnostic. Never re-sync from recovery.

## Step 5 — Escalate consecutive failures

CRITICAL (≥5): append System Alert to Memory.md. WARNING (3-4): recovery output only.

## Step 6 — Close watchdog

`ps.finish_watchdog(actions, successes, failures, healthy=False, notes)`. Interactive mode: full diagnostic with per-task blocks, history, source health, recommendations.

## Rules
- Healthy path: NO reads of Methodology, cores, Memory, Risk Rules
- Never overwrite production files
- Consecutive counter resets on any success
- 22:00 slot absorbs jitter from 21:00 trade-rec
- Watchdog invariant: every invocation calls exactly one of `clear_watchdog_healthy()` or `finish_watchdog()`
""")

# ── positions-monitor ─────────────────────────────────────────
w('skills/positions-monitor/SKILL.md', r"""---
name: positions-monitor
description: "Intraday watchdog — stop buffer, time-invalidation, earnings, catalyst, thesis variables, portfolio heat, correlation gate. Silent-when-OK. Use for 'check positions', 'monitor book', 'are my stops OK', 'portfolio heat', 'anything flashing'."
model: haiku
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Positions Monitor — Live Book Watchdog

Silent-when-OK. Writes `positions-monitor-YYYY-MM-DD.md` ONLY if flags fire.

## Reads (and nothing else)
1. `Memory.md` — §2 Open Positions, §7 Closed Trades
2. `.pipeline-status.json` (if present)
3. Latest `us-close-snapshot-*.md`

Do NOT read Methodology Prompt, Risk Rules, cores, Data Sources. Overrides startup protocol.

## Flag Panel

| Flag | Condition | Severity |
|---|---|---|
| F1 stop_buffer | distance_to_stop / ATR_14d < 2.0 | HIGH |
| F2 stop_hit | price ≤ stop (long) or ≥ stop (short) | CRITICAL |
| F3 time_inv | days_until_inv_date ≤ 7 | MED |
| F4 earnings | days_until_earnings ≤ 2 | HIGH |
| F5 catalyst | abs(days_until_catalyst) ≤ 1 | HIGH |
| F6 data | unable to price within 2 tries | MED |
| F7 ah_move | abs(overnight_pct) ≥ 3% (stock) or 1% (index/commodity) | HIGH |
| F8 thesis_var | thesis-invalidation variable breached kill level | CRITICAL |
| F9 portfolio_heat | total |entry−stop|/NAV > 6% | HIGH |
| F10 correlation_gate | pairwise |ρ_60d| > 0.7 | MED |

## Workflow
1. Inventory positions from Memory.md §2
2. Price pull — batched WebSearch per ticker
3. Compute all 10 flags
4. If all green: update `.pipeline-status.json` with OK, exit silently
5. If flags: write `positions-monitor-YYYY-MM-DD.md` with flag table + per-position detail
6. Update `.pipeline-status.json`
7. Escalate CRITICAL flags to auto-memory

## Scope
Read-only observer. Does NOT modify Memory.md, place orders, produce trade recs, or mark signals.
""")

# ── signal-review ─────────────────────────────────────────────
w('skills/signal-review/SKILL.md', r"""---
name: signal-review
description: "Weekly OOS performance review — marks SignalLedger to market, computes hit rates by asset/component/regime, identifies methodology improvements. Use for 'review signals', 'check performance', 'signal review', 'OOS performance', 'how are the recs doing'."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Signal Review — Weekly Performance & Methodology Feedback

OOS record: signals logged at rec time with market price, review measures what happened after. Changes feed methodology improvement through Gerald's sign-off only — never auto-adjust.

## Step 1 — Reads

1. `master-data-log.xlsx` — SignalLedger (all rows), RegimeHistory (latest), PerformanceStats (prior stats), AuditAdditionLog
2. `Methodology Prompt.md` — score component definitions
3. `Memory.md` — §2 open positions, §5 watchlist
4. `memory-lessons.md` — full lessons log
5. Latest `signal-review-*.md` — carry forward pending observations

If SignalLedger empty: stop with message.

## Step 2 — Expire stale signals, fetch prices

**2a. Date-based expiry (no price needed):** Near-misses past Inv_Date → EXPIRED. Promoted past Inv_Date + never taken → EXPIRED.

**2b. Price fetch (remaining OPEN):** Priority: Taken=YES first, then other Promoted, Near-Miss last. Sources: latest brief/snapshot, then WebSearch. Defer Near-Miss fetches if rate-limited.

## Step 3 — Update statuses

**Promoted:** HIT_TARGET (price reached TP1), HIT_STOP (breached ATR stop), EXPIRED (past inv date), STILL_OPEN. Calculate Hypo P&L %.

**Near-Miss:** WOULD_HIT_TARGET, WOULD_HIT_STOP, EXPIRED, STILL_OPEN. Calculate Hypothetical Move %.

## Step 4 — Compute rolling statistics (13 dimensions)

Update **PerformanceStats** sheet:

1. Win rate by score component (S/T/C/R univariate)
2. Win rate by asset class (Crypto/Equities/ETFs/Commodities)
3. Win rate by regime label
4. Blocking leg breakdown (which component most often blocks)
5. Average hypo P&L (promoted) and move (near-miss)
6. Best/worst individual signals
7. **Score interaction matrix** (S×T, S×R, T×R, etc.) — 3×3 contingency, flag >15pp differential as SYNERGY/CONFLICT
8. **Time-to-exit distribution** — ≤5d, 6–14d, 15–28d, >28d buckets with win rate per bucket
9. **MAE/MFE analysis** — worst/best close before exit
10. **Catalyst resolution** — did C=+1 events resolve as expected?
11. **VIX-at-entry conditioning** — win rate when VIX>25 vs <20 vs between
12. **Near-miss counterfactual regression** — would promoting near-misses have improved overall stats?
13. **Audit-addition variable contribution** — did residual-mom/intermediary-cap/basis-mom move any score leg into/out of entry?

## Step 5 — Escalation flags

Check for: SCORE-LEG-COLLAPSE (component stops predicting), DATA-SOURCE-DEGRADATION (rising MISSING rate), GATE-TOO-AGGRESSIVE (too many viable signals blocked), AUDIT-ADDITION-STALL (no contribution across review window).

## Step 6 — Methodology improvement candidates

Surface 1–3 concrete proposals from the statistical evidence. Each: observation, hypothesis, proposed change, required evidence threshold, Gerald sign-off required.

## Step 7 — Write output

Path: `signal-review-{YYYY-MM-DD}.md` + update PerformanceStats sheet + VariableRegistry maintenance.

## Step 8 — Update Memory.md

Append to `memory-lessons.md`: date, signal count, win rates, escalation flags, improvement candidates.
""")

# ── trade-update ──────────────────────────────────────────────
w('skills/trade-update/SKILL.md', r"""---
name: trade-update
description: "Event-driven 4-layer sync on trade execution events — entries, exits, stop moves, tranches, size changes. Use when 'I entered X', 'I bought X', 'stopped out of X', 'moved stop on X', 'trimmed X'. Not for placing trades or daily rec/brief."
model: sonnet
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# Trade Update

One event = four layers updated in order, no batching. Interactive only (no schedule).

## Step 1 — Reads
1. `Trade-Execution-Protocol.md` — authoritative procedure
2. `Memory.md` — §2 Open Positions, §5 Watchlist, §7 Closed Trades
3. `master-data-log.xlsx` → SignalLedger sheet (find rows to update)

## Step 2 — Classify event

| Phrase | Event type |
|---|---|
| entered/bought/filled/opened (promoted) | Fresh entry §A |
| entered/bought (near-miss/not in rec) | Ad-hoc promotion §C |
| added to/scaled into | Tranche add §B |
| stopped out/stop hit | Exit — stop §D |
| hit target/TP1/took profit | Exit — target §D |
| closed/cut/invalidated/time-stop | Exit — discretionary §D |
| moved stop/stop to breakeven/trailed | Adjustment — stop §E |
| trimmed/reduced/sized up | Adjustment — size §F |

## Step 3 — Fail-loud ambiguity check

Confirm all five: Asset, Side, Price, Time (UTC+8 absolute), SignalLedger linkage. If unclear, STOP and ask.

## Step 4 — Four layers, in order

**Layer 1 — Memory.md:** §2 add/remove/edit row. §7 append for exits. Recompute portfolio heat. Update header timestamp.

**Layer 2 — SignalLedger (openpyxl):**
- Fresh entry: Taken=YES on today's Promoted row. Don't overwrite Entry_Price if set.
- Ad-hoc promotion: new P### row, cross-link N### in Notes.
- Tranche: update Notes, weighted-average Entry_Price.
- Exit: Status (HIT_STOP/HIT_TARGET/EXPIRED/DISCRETIONARY_CLOSE), Exit_Price, Exit_Date, Days_to_Exit, Hypo_PnL_Pct.
- Stop move: don't edit ATR_Stop, append to Notes.

**Layer 3 — memory-lessons.md:** Append one factual line. Non-routine adjustments only.

**Layer 4 — auto-memory (conditional):** Only for repeated/novel patterns.

## Step 5 — Confirm

Report: event recorded, signal ID, new portfolio heat, follow-up if any.

## Reconciliation mode
Triggered by "reconcile the ledger": diff Memory §2 vs SignalLedger OPEN rows, fix gaps oldest-first, save after each event.
""")

# ── literature-review ─────────────────────────────────────────
w('skills/literature-review/SKILL.md', r"""---
name: literature-review
description: "Semi-annual academic finance lit scan for new tradeable variables. Five inclusion criteria, McLean-Pontiff decay projection, integration assessment. Use for 'literature review', 'lit review', 'new variables', 'academic scan', 'factor scan'. Scope-limited runs allowed."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Literature Review — Semi-Annual Variable Discovery

Systematic scan for new variables that could strengthen the framework. Runs semi-annually or on demand. Most papers won't clear the bar — value is in systematic coverage.

## Step 1 — Reads

1. `Methodology Prompt.md` — current Top-28 variables, framework gaps
2. `Trad core.md` — cross-asset factors already covered
3. `Coin core.md` — crypto predictors already covered
4. `Data Sources.md` — current variable-to-source mapping
5. `Memory.md` — §9 research questions
6. `memory-lessons.md` — repeated patterns
7. `master-data-log.xlsx` — RegimeHistory, AuditAdditionLog, PerformanceStats
8. Latest `quarterly-methodology-review-*.md` — variable candidate pipeline
9. Recent `signal-review-*.md` files — §7 improvement candidates

## Step 2 — Identify framework gaps

Analyze: scoring gaps (which S/T/C/R components fail to discriminate?), asset class gaps, regime gaps, temporal gaps, Memory §9 open questions. Produce 3–7 gap list before searching.

## Step 3 — Systematic search

By category: cross-asset factors, commodities, equities, risk/volatility, crypto, microstructure, macro/rates, gap-directed. Use WebSearch for SSRN, NBER, JF, JFE, RFS, working papers.

## Step 4 — Five-criteria screening

Each candidate must pass ALL:
1. Peer-reviewed or credible working paper
2. Replicated across samples/geographies
3. Coherent economic mechanism
4. Independent (not redundant with existing Top-28)
5. Real-time implementable with available data

## Step 5 — McLean-Pontiff decay projection

Published Sharpe → projected operational Sharpe (apply 26% OOS decay + 58% post-publication decay as upper bound).

## Step 6 — Integration assessment

Per candidate: component feed (S/T/C/R), asset scope, double-counting gates, data source, implementation complexity, review window.

## Step 7 — Write output + VariableRegistry sync

Output: structured review file. Sync Candidate rows to VariableRegistry in master-data-log.xlsx.
""")

# ── quarterly-methodology-review ──────────────────────────────
w('skills/quarterly-methodology-review/SKILL.md', r"""---
name: quarterly-methodology-review
description: "Quarterly meta-review — analytical dimension fitness audit, research core reconciliation, variable candidate pipeline management. Use for 'quarterly review', 'review the methodology', 'audit the system', 'is the system working'. Operates above weekly signal-review."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Quarterly Methodology Review

Three questions the weekly review can't answer: (1) Is the signal review asking the right questions? (2) Does the research still hold? (3) What should we try next? Every change proposal requires Gerald's sign-off.

## Step 1 — Reads

1. `master-data-log.xlsx` — SignalLedger (all), PerformanceStats, RegimeHistory, AuditAdditionLog
2. `Methodology Prompt.md` — Top-28 variables, 8-step framework
3. `Risk Rules.md` — binding constraints
4. `Data Sources.md` — variable-to-source mapping
5. `Trad core.md` + `Coin core.md` — research evidence
6. `Memory.md` — §9 research questions
7. `memory-lessons.md` — full lessons log
8. All `signal-review-*.md` files — §7 improvement candidates
9. Prior `quarterly-methodology-review-*.md` — pending actions

If <30 closed signals: add "Early-stage review" banner.

## Step 2 — Analytical dimension fitness audit

13 dimensions (7 original + 6 from 2026-04-15): win rate by component, by asset class, by regime, blocking leg, average P&L, best/worst, interaction matrix, time-to-exit, MAE/MFE, catalyst resolution, VIX conditioning, near-miss regression, audit-addition contribution.

Each rated: RETAIN / DEMOTE / RETIRE / PROMOTE.

## Step 3 — Research core reconciliation

Cross-check Top-28 claims against ledger evidence. Flag divergences (research says predictive, ledger says not, or vice versa).

## Step 4 — Variable candidate pipeline

Tier 2 (promising, need more data) and Tier 3 (speculative). Advance, hold, or remove candidates.

## Step 5 — Methodology change proposals

QR-prefixed proposals. All require Gerald sign-off.

## Step 6 — Context budget assessment

Weekly review token cost. Are any dimensions burning context for zero insight?

## Output
Dated review file + VariableRegistry updates + methodology change proposals.
""")

# ── system-review ─────────────────────────────────────────────
w('skills/system-review/SKILL.md', r"""---
name: system-review
description: "Semi-annual architecture + efficiency audit. Maps skills/tasks/files to value chain, produces KEEP/MODIFY/MERGE/REMOVE verdicts. Two tests: value (does it earn money?) and efficiency (minimum token cost?). Use for 'system review', 'strategic review', 'audit architecture', 'optimize the system', 'reduce token burn'."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# System Review — Strategic Architecture + Efficiency Audit

Every skill, task, and file must pass: (1) Value — moves/protects money or produces actionable insight, AND (2) Efficiency — minimum token cost for the decision quality. Does NOT edit anything — produces ranked patch file for Gerald's review.

## Value chain buckets
1. Research (lit review, quarterly review, cores)
2. Rec-generation (brief, news, preflight, trade-rec)
3. Execution (trade-update, reactive)
4. Monitoring (positions-monitor)
5. Post-trade review (signal-review, weekly regime)
6. Infrastructure (workspace-tidy, pipeline-recovery, us-close)
7. Meta-review (this skill, quarterly-methodology)

## Seven phases

**Phase 1 — Inventory:** List all skills, scheduled tasks, workspace files, memory files. No interpretation.

**Phase 2 — Value-chain map:** Assign each process to a bucket. Identify gaps (empty buckets) and redundancies.

**Phase 3 — Per-process audit:** 6 questions each: (1) What decision does it inform? (2) When did it last change a trade? (3) Token cost per run? (4) Can same quality be achieved cheaper? (5) Does it duplicate another process? (6) Would removing it degrade decision quality?

**Phase 4 — Gap & redundancy analysis:** Architecture gaps, overlapping scopes, shared-artifact opportunities.

**Phase 5 — Ranked proposals:** ADD/REMOVE/MODIFY-scope/MODIFY-efficiency. Tagged HIGH/MEDIUM/LOW by P&L impact or tokens freed.

**Phase 6 — Self-audit:** What happened to prior cycle's proposals?

**Phase 7 — Output:** Patch file with concrete changes, Gerald reviews. If skill-creator chaining is enabled, write one patch per MODIFY target to `patches/`.

## Scope boundaries
Does NOT audit: methodology dimensions (quarterly-review), signal marking (signal-review), file retention (retention policy), pipeline failures (pipeline-recovery), variable pipeline (literature-review).
""")

# ── consolidate-memory ────────────────────────────────────────
w('skills/consolidate-memory/SKILL.md', r"""---
name: consolidate-memory
description: "Reflective pass over memory files — merge duplicates, fix stale facts, prune index."
model: haiku
allowed-tools: Read Write Edit Grep Glob
---

# Memory Consolidation

## Phase 1 — Take stock
List memory directory, read index (MEMORY.md), skim each topic file. Note overlaps, stale entries, thin files.

## Phase 2 — Consolidate
- Separate durable (preferences, style, relationships) from dated (specific deadlines, one-off tasks)
- Merge overlapping files, keep richer path
- Convert relative dates to absolute
- Drop what's easy to re-derive from files/tools

## Phase 3 — Tidy index
Keep MEMORY.md under 200 lines / 25KB. One line per entry, <150 chars: `- [Title](file.md) — hook`.
""")

# ── Done ──────────────────────────────────────────────────────
print(f"\n=== Done. Created .claude/ structure ===")
print(f"  Config:  CLAUDE.md, settings.json")
print(f"  Rules:   rules/evidence-grades.md, rules/risk-rules-summary.md")
print(f"  Skills:  11 skills in skills/*/SKILL.md")
print(f"\nNext steps:")
print(f"  1. Fix script paths:  find scripts/ -name '*.py' -exec sed -i 's|/mnt/Trade/|./|g' {{}} +")
print(f"  2. Launch Claude Code: claude")
print(f"  3. Verify:  /help  (should list all 11 skills)")
print(f"  4. Create scheduled tasks via Desktop app (see MIGRATION-GUIDE.md §6)")
