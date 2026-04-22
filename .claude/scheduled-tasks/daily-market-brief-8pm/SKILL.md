---
name: daily-market-brief-8pm
description: Daily US pre-open market brief — runs every weekday at 8pm local time (UTC+8)
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
  echo "ABORT: preflight-audit-data not available ($STAGING missing or <500 bytes). Market brief cannot run without upstream audit-data. Exiting cleanly — pipeline-recovery will handle."
  # Update pipeline/.pipeline-status.json with status=BLOCKED, reason=preflight-audit-data-missing
  python -c "import json,pathlib,datetime; p=pathlib.Path('pipeline/.pipeline-status.json'); d=json.loads(p.read_text()) if p.exists() else {}; d.setdefault('daily-market-brief-8pm',{}); d['daily-market-brief-8pm'].update({'status':'BLOCKED','reason':'preflight-audit-data-missing','date':'$TODAY','timestamp':datetime.datetime.utcnow().isoformat()+'Z'}); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2))" || true
  exit 0
fi
```

---

Produce today's US pre-open market brief.

1. Follow CLAUDE.md §Session Startup Protocol (all four reads).
2. Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).
3. Load and run the `market-brief` skill end-to-end for today's local date (UTC+8).
   - Reads `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` at Step 2 (date-folder convention; falls back to root if absent)
   - Reads `catalysts-cache-{YYYY-MM-DD}.json` at Step 5.5 if news wrote it
   - Pulls Grade A variables via data_retrieval_engine.fetch_many (4-tier fallback)
   - FAIL-LOUD on any MISSING Grade A variable — do NOT silently infer
   - Output: `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md` (version tag v1 first run; v2/v3... on same-day re-runs)
   - Syncs DailyVariables, RegimeHistory, DataQuality, CatalystLog sheets in master-data-log.xlsx
4. After the brief file is written, update pipeline/.pipeline-status.json per
   the write pattern in framework/Pipeline-Recovery-Protocol.md §daily-market-brief-8pm-v2.
   OK if file ≥500 bytes and ≤3 MISSING Grade A. PARTIAL if >3 MISSING. FAIL if write failed.
   consecutive_failures: 0 on OK; increment from prior on non-OK.
5. Pack into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`; same-day v1→v2 re-runs replace §D in-place):
   `python scripts/pack_daily.py --section D --source {YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md --status "{OK|PARTIAL|FAIL} v{N}"`
   The per-day `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md` source file is the canonical artifact — trade-rec's integrity pre-check and the weekly review read it directly.
6. Exit summary (one line, required for pipeline-recovery sniff):
   `Market brief {YYYY-MM-DD} v{N} complete — regime={label}, MISSING Grade A={count}, status={OK|PARTIAL|FAIL}, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §D`

Then git add -A, commit with message "routine: market-brief {today}", and push to origin main.