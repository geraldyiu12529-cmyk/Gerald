# Pipeline Recovery Protocol

**Created:** 2026-04-16
**Authority over:** Task-level failure detection, consecutive failure tracking, and automated recovery across the daily pipeline. Complements the variable-level Data-Retrieval-Fallback-Framework.md (which handles individual data source failures).
**Status:** ACTIVE

---

## Problem Statement

The system has robust variable-level failure handling (4-tier retrieval with cache, fail-loud, DataQuality logging). What it lacks is task-level failure handling:

1. **No pipeline status tracking.** Each task is blind to whether upstream tasks completed or crashed. The trade rec's delta-check gate (Step 0) has a bug: when upstream files don't exist, `p.exists()` returns False, so `changed` evaluates to False — the skill silently carries forward the prior rec instead of aborting.

2. **No consecutive failure counter.** If the market brief crashes three days running, nothing escalates. The fourth day's trade rec aborts identically to the first.

3. **No recovery mechanism.** Detection without correction means the pipeline aborts more gracefully but nothing gets fixed. A brief that failed because of a transient web-search issue at 20:00 could succeed at 20:20 if retried — but nothing retries it.

---

## Architecture: `.pipeline-status.json`

A single file at `{TRADE_DIR}/pipeline/.pipeline-status.json` tracks task completion across the pipeline. Each task writes its own entry on completion (or failure). Downstream tasks read it before starting.

> **Path note (updated 2026-04-20):** The file lives at `pipeline/.pipeline-status.json` inside the workspace root, NOT at `{TRADE_DIR}/.pipeline-status.json`. All tasks must use `pipeline_status.PipelineStatus()` from `scripts/pipeline_status.py` rather than hardcoding the path. The `PipelineStatus` class resolves the correct location regardless of mount point (native Windows, Cowork, or env-var override).

```json
{
  "preflight": {
    "date": "2026-04-16",
    "status": "OK",
    "consecutive_failures": 0,
    "timestamp": "2026-04-16T19:52:00+08:00",
    "details": "All sources reachable. Cache coverage 45%."
  },
  "market-brief": {
    "date": "2026-04-16",
    "status": "OK",
    "consecutive_failures": 0,
    "timestamp": "2026-04-16T20:08:00+08:00",
    "missing_count": 1,
    "file": "2026-04-16/market-brief-2026-04-16.md"
  },
  "news-events": {
    "date": "2026-04-16",
    "status": "OK",
    "consecutive_failures": 0,
    "timestamp": "2026-04-16T20:15:00+08:00",
    "file": "2026-04-16/news-2026-04-16.md"
  },
  "trade-rec": {
    "date": "2026-04-16",
    "status": "OK",
    "consecutive_failures": 0,
    "timestamp": "2026-04-16T20:35:00+08:00",
    "signals_logged": 3,
    "file": "2026-04-16/trade-rec-2026-04-16.md"
  }
}
```

### Status values

| Status | Meaning |
|--------|---------|
| `OK` | Task completed successfully, output file written |
| `PARTIAL` | Task completed but with significant data gaps (>3 MISSING Grade A) |
| `ABORT` | Task aborted due to upstream integrity failure |
| `FAIL` | Task crashed or timed out (written by recovery task, not the failing task itself) |

### Consecutive failure tracking

Each task entry carries `consecutive_failures`. On successful completion, reset to 0. On any non-OK status, increment from the prior entry's value. This gives the recovery task a single number to check.

---

## Integrity Checks (task prompt prepends)

These go at the top of each scheduled task prompt. They run before the skill loads.

### `preflight-audit-data-1945pm`

The preflight runs first in the pipeline. Its integrity check is a self-check + recovery detection:

```
**PIPELINE INTEGRITY SELF-CHECK + RECOVERY (run before anything else):**

1. Read `pipeline/.pipeline-status.json` (via `PipelineStatus()` from `scripts/pipeline_status.py`) if it exists.
2. Check yesterday's pipeline status:
   - If any task shows `consecutive_failures >= 3`, print:
     "⚠ CONSECUTIVE FAILURE ALERT: {task} has failed {N} consecutive days. Investigate."
   - If yesterday's market-brief status is FAIL/ABORT AND today's sources are healthy:
     Print: "Recovery opportunity: yesterday's brief failed but sources are now reachable."
     (The recovery task handles actual re-runs — preflight just flags the opportunity.)

3. After completing Phase 1 and Phase 2, before exiting:
   a. Verify `.pipeline-health.json` was written today (date matches today's local date)
   b. Verify `{today}/audit-data-staging-{today}.md` was written and is non-empty (with root fallback `audit-data-staging-{today}.md` for legacy runs)
   c. Write preflight status to `.pipeline-status.json`:
      ```python
      import json
      from pathlib import Path
      from datetime import datetime, timezone, timedelta
      utc8 = timezone(timedelta(hours=8))
      today = datetime.now(utc8).strftime('%Y-%m-%d')
      now_iso = datetime.now(utc8).isoformat()
      status_path = Path('/mnt/Trade/pipeline/.pipeline-status.json')
      status = json.loads(status_path.read_text()) if status_path.exists() else {}
      prev = status.get('preflight', {})
      health_ok = Path('/mnt/Trade/.pipeline-health.json').exists()
      staging_new = Path(f'/mnt/Trade/{today}/audit-data-staging-{today}.md')
      staging_legacy = Path(f'/mnt/Trade/audit-data-staging-{today}.md')
      staging_ok = staging_new.exists() or staging_legacy.exists()
      all_ok = health_ok and staging_ok
      consec = 0 if all_ok else (prev.get('consecutive_failures', 0) + 1) if prev.get('date') != today else prev.get('consecutive_failures', 0)
      status['preflight'] = {
          'date': today, 'status': 'OK' if all_ok else 'PARTIAL',
          'consecutive_failures': consec, 'timestamp': now_iso,
          'details': f"health.json={'OK' if health_ok else 'MISSING'}, staging={'OK' if staging_ok else 'MISSING'}"
      }
      status_path.write_text(json.dumps(status, indent=2))
      ```
   d. If either check fails, also append "INTEGRITY FAIL: [filename] not produced" to the final output summary.
```

### `daily-market-brief-8pm-v2`

The brief has no hard upstream dependency (it pulls its own data), so its integrity check is a status write on completion:

```
**PIPELINE STATUS WRITE (run after all steps complete):**

After writing the brief file and syncing to Excel, update `.pipeline-status.json`:

```python
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
now_iso = datetime.now(utc8).isoformat()
status_path = Path('/mnt/Trade/pipeline/.pipeline-status.json')
status = json.loads(status_path.read_text()) if status_path.exists() else {}
brief_new = Path(f'/mnt/Trade/{today}/market-brief-{today}.md')
brief_legacy = Path(f'/mnt/Trade/market-brief-{today}.md')
brief_path = brief_new if brief_new.exists() else brief_legacy
ok = brief_path.exists() and brief_path.stat().st_size > 500
prev = status.get('market-brief', {})
consec = 0 if ok else (prev.get('consecutive_failures', 0) + 1)
status['market-brief'] = {
    'date': today, 'status': 'OK' if ok else 'FAIL',
    'consecutive_failures': consec, 'timestamp': now_iso,
    'file': f'{today}/market-brief-{today}.md' if brief_new.exists() else f'market-brief-{today}.md'
}
status_path.write_text(json.dumps(status, indent=2))
```

If the brief has >3 MISSING Grade A variables, set status to `PARTIAL` instead of `OK`.
```

### `daily-news-events-810pm-v2`

Same pattern — status write on completion:

```
**PIPELINE STATUS WRITE (run after all steps complete):**

After writing the news file, update `.pipeline-status.json`:

```python
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
now_iso = datetime.now(utc8).isoformat()
status_path = Path('/mnt/Trade/pipeline/.pipeline-status.json')
status = json.loads(status_path.read_text()) if status_path.exists() else {}
news_new = Path(f'/mnt/Trade/{today}/news-{today}.md')
news_legacy = Path(f'/mnt/Trade/news-events/news-{today}.md')
news_path = news_new if news_new.exists() else news_legacy
ok = news_path.exists() and news_path.stat().st_size > 200
prev = status.get('news-events', {})
consec = 0 if ok else (prev.get('consecutive_failures', 0) + 1)
status['news-events'] = {
    'date': today, 'status': 'OK' if ok else 'FAIL',
    'consecutive_failures': consec, 'timestamp': now_iso,
    'file': f'{today}/news-{today}.md' if news_new.exists() else f'news-events/news-{today}.md'
}
status_path.write_text(json.dumps(status, indent=2))
```
```

### `daily-trade-recommendation-820pm-v2`

This is the critical gate. The trade rec's skill has the delta-check bug described above, so the integrity check must run BEFORE the skill loads:

```
**PIPELINE INTEGRITY PRE-CHECK (mandatory, run before loading the skill):**

```python
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
now_iso = datetime.now(utc8).isoformat()
trade_dir = Path('/mnt/Trade')

def first_existing(*paths):
    for p in paths:
        if p.exists():
            return p
    return paths[0]  # return the canonical (date-folder) path even if missing, for reporting

brief   = first_existing(trade_dir / today / f'market-brief-{today}.md',   trade_dir / f'market-brief-{today}.md')
news    = first_existing(trade_dir / today / f'news-{today}.md',           trade_dir / f'news-events/news-{today}.md')
staging = first_existing(trade_dir / today / f'audit-data-staging-{today}.md', trade_dir / f'audit-data-staging-{today}.md')

missing = []
if not brief.exists():   missing.append(f'{today}/market-brief-{today}.md')
if not news.exists():    missing.append(f'{today}/news-{today}.md')
if not staging.exists(): missing.append(f'{today}/audit-data-staging-{today}.md')
```

**Decision logic:**

1. If `brief` is missing → **HARD ABORT.** The brief is the primary input; running the 8-step without it wastes ~50K tokens on degraded analysis.
   - Write abort status to `.pipeline-status.json` with incremented `consecutive_failures`
   - Output: `PIPELINE INTEGRITY FAIL — {missing files}. Trade rec aborted. Consecutive failures: {N}. Check upstream task logs.`
   - **Stop. Do not load the skill. Do not attempt to substitute yesterday's files.**

2. If `brief` exists but `news` or `staging` is missing → **WARN AND PROCEED.**
   - Output: `PIPELINE INTEGRITY WARNING — {missing files} missing. Proceeding with partial data.`
   - Load the skill normally. The missing files will surface in the rec's §6 Data Gaps.

3. If all three exist → proceed silently, load the skill.

**On completion** (after the skill finishes), write OK status to `.pipeline-status.json` with `consecutive_failures: 0`.

**Why the brief is the hard gate:** The trade rec skill consumes the brief as its primary evidence base — regime label, scorecard, variable readings, catalyst calendar. Without it, every score in Step 3 would be reconstructed from scratch using stale data, producing a rec that's both expensive and unreliable. News and staging are supplementary: missing news means weaker catalyst scoring (C leg), missing staging means fail-loud on audit additions — both degrade gracefully within the skill's existing §6 Data Gaps framework.
```

### `weekly-regime-signal-review-6pm`

The weekly review aggregates a week's worth of briefs. Its integrity check goes at the top of the Phase 1 prompt:

```
**PIPELINE INTEGRITY PRE-CHECK (mandatory, run before Phase 1):**

Identify today's date and the 5 weekdays (Mon–Fri) in the most recently completed trading week.
Check `/mnt/Trade/` for `{date}/market-brief-{date}.md` files (glob `*/market-brief-*.md`, fall back to root `market-brief-{date}.md` for legacy runs) covering those 5 days.

Also check `.pipeline-status.json` for consecutive failure counts across all tasks.

If fewer than 4 of the 5 daily briefs are present:
- Output: `PIPELINE INTEGRITY WARNING — only {n}/5 weekly briefs found. Regime aggregation may be incomplete. Proceeding with available data but flagging low confidence.`
- Proceed with Phase 1 but add a `## Data Coverage` section to the output noting which days are missing.

If 0 or 1 briefs are found:
- Output: `PIPELINE INTEGRITY FAIL — insufficient brief history for regime aggregation ({n}/5). Weekly review aborted.`
- **Stop.**

If any task in `.pipeline-status.json` shows `consecutive_failures >= 3`:
- Add an escalation section to the output: `## ⚠ Pipeline Health Alert` listing each failing task and its consecutive failure count.

Only if 4 or 5 briefs confirmed: proceed with Phase 1 normally.
```

---

## Recovery Task: `pipeline-recovery-830pm`

A new lightweight scheduled task that runs 5 minutes after the trade rec slot. Its sole purpose: detect failures in today's pipeline and attempt recovery.

**Schedule:** 20:30 UTC+8 Mon–Fri (5 min after trade rec)
**Expected runtime:** <60 seconds if pipeline is healthy; 2–5 minutes if recovery needed

### Logic:

```
1. Read .pipeline-status.json
2. For each task, check today's status:

   CASE: market-brief status is FAIL or no entry for today
   → The brief task crashed or timed out.
   → Recovery: attempt to produce a minimal "cache-brief" from cached data:
     a. Read .pipeline-health.json for source status
     b. Run data_retrieval_engine.fetch_many() for Grade A variables (cache-only mode: skip Tier 1/2, use Tier 3 only)
     c. If ≥20 variables available from cache: write `{today}/market-brief-{today}-recovery.md` with STALE tags on every reading
     d. If <20 variables: recovery not viable, leave as FAIL
   → Update status to PARTIAL if recovery succeeded

   CASE: news-events status is FAIL or no entry for today
   → News is supplementary. Write a skeleton `{today}/news-{today}-recovery.md` with "NEWS CAPTURE FAILED — no category searches completed. Trade rec should proceed with C-leg gaps."
   → Update status to PARTIAL

   CASE: trade-rec status is ABORT and brief now exists (recovery produced one)
   → The trade rec aborted because the brief was missing, but recovery just produced one.
   → DO NOT re-run the trade rec automatically (too expensive, too late in the window).
   → Instead: write a flag file .recovery-pending that the next day's preflight will notice.
   → Print: "Recovery produced a brief. Trade rec was not re-run. Tomorrow's preflight will flag this."

   CASE: consecutive_failures >= 5 for any task
   → This is a systemic failure, not a transient issue.
   → Write to Memory.md §7 (System Alerts): "PIPELINE ALERT {date}: {task} has failed {N} consecutive days. Manual investigation required."
   → This ensures Gerald sees it in the next interactive session.

3. If nothing failed today: print "Pipeline healthy. No recovery needed." and exit.
```

### Why 20:30?

The recovery task runs after all daily tasks have completed (preflight 19:45 → brief 20:00 → news 20:10 → trade rec 20:25). By 20:30, the status file reflects the full pipeline. Running earlier would miss trade-rec failures; running later serves no purpose since the trading window is closing.

### Why not just retry the failed task?

Retry is expensive (~40-60K tokens for a full brief) and may hit the same failure. The cache-brief recovery is cheap (<5K tokens) and produces a "good enough" result for the trade rec to consume. If the underlying data source issue persists, the next day's preflight will flag it, and the retrieval engine's cache layer ensures the cache-brief has reasonably fresh data.

---

## Interaction with Existing Systems

| Existing mechanism | What it handles | Gap this protocol fills |
|---|---|---|
| 4-tier retrieval + cache | Variable-level source failures | Task-level crash/timeout failures |
| Fail-loud in briefs | Missing individual variables | Missing entire upstream files |
| `.pipeline-health.json` | Source connectivity before pipeline runs | Whether tasks actually completed |
| DataQuality sheet | MISSING variable counts per day | Consecutive failure trends |
| Delta-check gate (Step 0) | Whether upstream changed since last rec | **Bug fix:** distinguishes "file missing" from "file unchanged" |
| Weekly signal review | Data quality trends over the week | Pipeline health alerts for consecutive failures |

---

## Implementation Checklist

1. [ ] Paste preflight integrity text into `preflight-audit-data-1945pm` task prompt
2. [ ] Paste brief status write text into `daily-market-brief-8pm-v2` task prompt (at end)
3. [ ] Paste news status write text into `daily-news-events-810pm-v2` task prompt (at end)
4. [ ] Paste trade-rec integrity text into `daily-trade-recommendation-820pm-v2` task prompt (at top)
5. [ ] Paste weekly review integrity text into `weekly-regime-signal-review-6pm` task prompt (at top)
6. [ ] Create `pipeline-recovery-830pm` scheduled task
7. [ ] Seed `.pipeline-status.json` with initial state

---

## What This Does NOT Cover

- **Skill-level bugs.** If the market-brief skill has a logic error that produces a valid but wrong brief, the pipeline status shows OK. Data correctness is a separate problem (partially covered by the validation layer in Data-Retrieval-Fallback-Framework.md §12.1).
- **Timeout recovery.** If a task times out mid-execution, it can't write its own FAIL status (it's dead). The recovery task infers failure from the absence of a status entry for today. This has a 5-minute detection gap (between the expected completion time and recovery task fire).
- **Weekend pipeline.** Only Mon–Fri tasks are covered. The weekly review (Sunday) has its own integrity check but no recovery task.
