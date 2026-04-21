---
name: trade-rec-daily
description: Daily pre-open trade recommendation — pipeline integrity check + 8-step methodology
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

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
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
trade_dir = Path('.')
brief   = trade_dir / today / f'market-brief-{today}.md'
news    = trade_dir / today / f'news-{today}.md'
staging = trade_dir / today / f'audit-data-staging-{today}.md'
missing = []
if not brief.exists():   missing.append(f'{today}/market-brief-{today}.md')
if not news.exists():    missing.append(f'{today}/news-{today}.md')
if not staging.exists(): missing.append(f'{today}/audit-data-staging-{today}.md')
```

- If brief is MISSING → HARD ABORT. Write abort status to pipeline/.pipeline-status.json with incremented consecutive_failures. Output: "PIPELINE INTEGRITY FAIL — {missing files}. Trade rec aborted. Consecutive failures: {N}." Stop. Do not load the skill.
- If brief exists but news or staging is missing → WARN AND PROCEED. Output: "PIPELINE INTEGRITY WARNING — {missing files} missing. Proceeding with partial data." Load the skill normally.
- If all three exist → proceed silently.

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