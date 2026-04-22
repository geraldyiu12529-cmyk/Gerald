---
name: news-events-daily
description: Daily news capture — 12-category taxonomy, catalysts cache, pipeline status update
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...`.

---

**Preflight-audit-data gate (run SECOND — abort if data not available):**

```bash
TODAY=$(date +%Y-%m-%d)
STAGING="$TODAY/audit-data-staging-$TODAY.md"
if [ ! -f "$STAGING" ] || [ $(wc -c < "$STAGING") -lt 500 ]; then
  echo "ABORT: preflight-audit-data not available ($STAGING missing or <500 bytes). News capture cannot run without upstream audit-data. Exiting cleanly — pipeline-recovery will handle."
  python -c "import json,pathlib,datetime; p=pathlib.Path('pipeline/.pipeline-status.json'); d=json.loads(p.read_text()) if p.exists() else {}; d.setdefault('news-events-daily',{}); d['news-events-daily'].update({'status':'BLOCKED','reason':'preflight-audit-data-missing','date':'$TODAY','timestamp':datetime.datetime.utcnow().isoformat()+'Z'}); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2))" || true
  exit 0
fi
```

---

Capture today's daily news, geopolitics, macro releases, corporate earnings, crypto regulatory, and flash events.

1. Do NOT follow CLAUDE.md §Session Startup Protocol in full. Read ONLY: `news-events/README.md` (for the 12-category taxonomy and hotspot list).
2. Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}`.
3. Load and run the `news-events` skill end-to-end for today's local date (UTC+8).
   - Search by category (not by named conflict). Use hotspot list from README.
   - Cover all 12 categories: macro releases, central bank, geopolitics, equity earnings, crypto regulatory, commodity supply, FX policy, flash events, credit/rates, sector rotation, analyst revisions, overnight Asia
   - Output: `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md`
   - Write `catalysts-cache-{YYYY-MM-DD}.json` (under `.catalysts-cache/`) if any time-sensitive catalysts found (for market-brief and trade-rec to consume)
4. After the news file is written, update pipeline/.pipeline-status.json:
   - status: OK if file exists and >200 bytes; FAIL otherwise
   - consecutive_failures: 0 on OK; increment from prior on non-OK
5. Pack into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`):
   `python scripts/pack_daily.py --section E --source {YYYY-MM-DD}/news-{YYYY-MM-DD}.md --status "{OK|FAIL}"`
   The per-day `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` source file is the canonical artifact — market-brief Step 5.5 and trade-rec read it directly.
6. Exit summary (one line):
   `News capture {YYYY-MM-DD} complete — {N} categories covered, {N} catalysts cached, status={OK|FAIL}, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §E`

Then git add -A, commit with message "routine: news-events {today}", and push to origin main.