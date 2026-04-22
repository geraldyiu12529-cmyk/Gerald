---
name: trade-rec-daily
description: Daily pre-open trade recommendation — pipeline integrity check + 8-step methodology
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

Produce today's pre-open trade recommendation.

CLOUD INGEST (run before pre-check — pulls the 3 cloud routines from Google Drive into today's date folder):

```
Use mcp__fa60a538-6fb1-4c90-8c9b-8db7cba53dbc__search_files in folder `T.system-cloud` for:
  - market-brief-{today}.md   → save to {today}/cloud-market-brief-{today}.md
  - news-{today}.md           → save to {today}/cloud-news-{today}.md
  - trade-rec-{today}.md      → save to {today}/cloud-trade-rec-{today}.md
Read each with read_file_content and write locally. If any is missing, log "CLOUD MISSING: {name}" and proceed — not fail-loud (cloud is supplementary).
```

These three cloud files are Grade B supplementary inputs (cloud-agent synthesis); the local artifacts remain primary.

PIPELINE INTEGRITY PRE-CHECK (run before loading the skill):

```python
import json, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
trade_dir = Path('.')

# Today-specific paths
brief_today   = trade_dir / today / f'market-brief-{today}.md'
news_today    = trade_dir / today / f'news-{today}.md'
staging_today = trade_dir / today / f'audit-data-staging-{today}.md'

# Fallback: find most recent brief in ANY date folder (last 7 days)
def _newest_glob(patterns):
    files = []
    for pat in patterns:
        files.extend(trade_dir.glob(pat))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None

brief_fallback = _newest_glob(['*/market-brief-*.md', 'market-brief-*.md'])
brief_staleness = None
if brief_fallback and not brief_today.exists():
    mtime = brief_fallback.stat().st_mtime
    age_hours = (datetime.now().timestamp() - mtime) / 3600
    brief_staleness = f"STALE {age_hours:.0f}h — using {brief_fallback}"

missing = []
if not news_today.exists():    missing.append(f'{today}/news-{today}.md')
if not staging_today.exists(): missing.append(f'{today}/audit-data-staging-{today}.md')
```

- If `brief_today` exists → proceed silently.
- If `brief_today` is MISSING but `brief_fallback` exists → **WARN AND PROCEED** with stale brief. Output: "PIPELINE INTEGRITY WARNING — today's market-brief missing. Using {brief_staleness}. Skill will label all brief-derived variables STALE." Load the skill with brief_path = brief_fallback.
- If `brief_today` is MISSING AND `brief_fallback` is None (no brief in workspace at all) → **HARD ABORT**. Write abort to pipeline/.pipeline-status.json. Output: "PIPELINE INTEGRITY FAIL — no market-brief found anywhere. Trade rec aborted. Run /market-brief manually." Stop.
- If brief exists (today or fallback) but news or staging is missing → note gaps, proceed.

**Rationale:** The original hard-abort on missing today-brief caused silent failures when the 8pm brief task ran slightly late or was in recovery. A stale brief (e.g., yesterday's) is better than no trade rec — all variables will be labeled STALE and the rec will note the data age.

1. Follow CLAUDE.md §Session Startup Protocol (all four reads).
2. Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}`.
3. Load and run the `daily-trade-rec` skill end-to-end for today's local date (UTC+8).
   - Synthesises market-brief, news-events, us-close-snapshot, weekly-review, AND the 3 cloud files (`cloud-market-brief-{today}.md`, `cloud-news-{today}.md`, `cloud-trade-rec-{today}.md`) through the 8-step evidence-graded methodology. Cloud files are Grade B context — cite disagreements with local primary sources.
   - Applies Risk Rules pre-entry checklist before promoting any signal
   - Logs all promoted signals and near-misses to SignalLedger in master-data-log.xlsx (append-only — never rewrite existing rows)
   - Output: `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` + `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html`
4. If the delta-check (Step 0) flags "no material change since prior rec", still commit any framework/Memory.md or pipeline/.pipeline-status.json updates that occurred.
5. On completion, update pipeline/.pipeline-status.json:
   - status: OK on successful write; ABORT if pre-check aborted; FAIL if skill crashed
   - consecutive_failures: 0 on OK; increment on non-OK
6. Pack into the consolidated daily file (markdown only — the HTML report stays separate):
   `python scripts/pack_daily.py --section F --source {YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md --status "{OK|ABORT|FAIL}"`
   The `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` source file is the canonical artifact (permanent per Retention Policy).
7. Exit summary (one line):
   `Trade rec {YYYY-MM-DD} complete — signals={N promoted, N near-miss}, cloud_ingested={3|partial|0}, status={OK|ABORT|FAIL}, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §F`

Then git add -A, commit with message "routine: trade-rec {today}", and push to origin main.