---
name: pipeline-recovery
description: Pipeline health monitoring, integrity checking, and automated recovery for Gerald's daily trading pipeline. Use when the user asks to 'check the pipeline', 'is the pipeline healthy', 'recover the brief', 'fix the pipeline', 'what failed today', 'pipeline status', 'recovery check', 'why did the rec abort', 'check pipeline health', or 'run recovery'. Also triggers on scheduled task `pipeline-recovery-830pm`, and on informal phrasing like 'anything broken today?' or 'did everything run?' in a trading context. Not for running the actual brief, news, or trade rec — use those skills for production runs.
---

# Pipeline Recovery

Monitors task-level health across the daily trading pipeline, detects failures and consecutive outages, attempts minimal recovery from cached data, and escalates systemic issues to Memory.md. Complements the variable-level Data-Retrieval-Fallback-Framework (which handles individual data source failures) by operating one layer up — at the task level.

Core principle: detection without correction is a fancier abort message. This skill actually fixes things when it can, and clearly flags when it can't.

---

## When This Skill Runs

Two modes:

1. **Scheduled (22:00 UTC+8 Mon–Fri, task `pipeline-recovery-830pm`):** Fires after the full daily pipeline completes. Must be **cheap on healthy days** (target <3K tokens of work including output, <5K hard ceiling). On recovery days: <15K tokens.

2. **Interactive:** User asks about pipeline health, wants to manually trigger recovery, or wants to understand why something failed. Verbose diagnostic output — token cost is not a concern because the user initiated it.

---

## Architecture: two phases

Everything the skill does is split into a cheap **Phase A** (always runs) and an optional **Phase B** (only if Phase A finds a problem). The fast healthy path short-circuits after Phase A.

**Phase A — Fast triage.** Pure Python on local files: JSON load, file stat, 2KB header sniff. No Excel open, no subprocess, no web, no skill loads. Dominates the common case.

**Phase B — Recovery.** Runs only when Phase A flags a problem. Can do: cache-brief recovery, skeleton news, Excel sync integrity, Memory.md escalation, data-cache interrogation.

---

## Step 1 — Phase A: fast triage

Run this at the very top. It's a single Python block using the `pipeline_status` helper.

```python
import sys
sys.path.insert(0, '/mnt/Trade/scripts')
from pipeline_status import PipelineStatus

ps = PipelineStatus()
fast = ps.fast_health_check()
print(fast['summary'])
```

The `fast_health_check()` return carries everything Phase B might need:

| Key | Purpose |
|---|---|
| `healthy` | True iff all tasks are HEALTHY/NOT_YET AND no CRITICAL streaks AND status JSON loaded cleanly AND no prior recovery crash |
| `assessment` | Per-task: `state` (HEALTHY/PARTIAL/FAILED/NOT_YET), `consecutive_failures`, `files_valid`, `files_invalid` (with reasons), `status_entry` |
| `escalations` | List of tasks at WARNING (≥3) or CRITICAL (≥5) streaks |
| `self_healed` | True if `.pipeline-status.json` was corrupt and was moved aside |
| `prior_recovery_crash` | Non-None if recovery died mid-run on a prior day |
| `summary` | One-line human-readable status |

**File validity gate.** The helper doesn't just check existence — it enforces per-file minimum sizes and runs a 2KB structural sniff (regex for expected headings / key variable names). A brief of 50 bytes is FAILED, not HEALTHY. The thresholds live in `MIN_SIZES` and `STRUCTURAL_SNIFFS` in `pipeline_status.py` — single source of truth for the whole pipeline.

---

## Step 2 — Healthy fast exit

```python
if fast['healthy']:
    ps.clear_watchdog_healthy()
    print(fast['summary'])
    # End of scheduled run. No further work.
```

In scheduled mode: stop here. Do not produce additional prose, do not load any other skill, do not read Methodology Prompt / research cores / Memory.md. The one-line summary plus the `recovery` entry in `.pipeline-status.json` is the full output.

In interactive mode: continue to Step 6 to produce the verbose diagnostic even when healthy.

---

## Step 3 — Phase B entry: start watchdog

If Phase A reports unhealthy, open the watchdog marker before doing any recovery work:

```python
ps.start_watchdog()
actions = []         # list of recovery actions attempted
successes = 0        # recovered tasks
failures = 0         # recovery attempts that didn't produce a usable output
notes = []           # free-form findings
```

The watchdog writes `recovery.in_progress=True` to `.pipeline-status.json`. If the recovery task then crashes mid-run, tomorrow's preflight calls `ps.detect_prior_recovery_crash()` and sees the stale `in_progress` flag with yesterday's date — flagging that recovery itself died. Without this marker, a silent recovery-task crash would be indistinguishable from "recovery ran and everything was fine".

---

## Step 4 — Phase B recovery actions

Pull the assessment and walk the failed tasks in dependency order: preflight → brief → news → trade-rec. Each sub-step below writes its own status back through `ps`, appends to `actions`, and increments `successes` or `failures`.

### 4a. Preflight recovery

If `assessment['preflight']['state'] == 'FAILED'`:

1. Check connectivity with a simple HTTP ping sweep (same set the preflight's Phase 1 uses). Write a fresh `.pipeline-health.json`.
2. Try running the compute script:
   ```python
   import subprocess
   result = subprocess.run(
       ['python3', '/mnt/Trade/scripts/compute_audit_additions.py'],
       capture_output=True, text=True, timeout=120,
       cwd='/mnt/Trade/scripts'
   )
   ```
3. If the script fails because of missing CSVs, check `/mnt/Trade/.data-cache/` for cached inputs within the staleness window and copy them into the expected input location; retry.
4. Validate the produced staging file via `ps._check_files('preflight')`. If it passes, `ps.write_recovery('preflight', details='…')`, else `ps.write_fail('preflight', reason='…')`.

### 4b. Market-brief recovery

If `assessment['market-brief']['state'] == 'FAILED'`:

Full brief = ~40-60K tokens; a cache-brief = a few thousand. Always do the cache-brief.

1. Import the retrieval engine (it's already local to the sandbox — no web hit needed when cache-preferred):
   ```python
   sys.path.insert(0, '/mnt/Trade/scripts')
   from data_retrieval_engine import DataRetrievalEngine
   engine = DataRetrievalEngine(cache_dir='/mnt/Trade/.data-cache')
   results = engine.fetch_many(variables='grade_a', prefer_cache=True, skip_websearch=True)
   ```
2. Count how many Grade A variables you got. If `< 20`, recovery is not viable — `ps.write_fail('market-brief', reason='cache coverage {n}/20')` and move on.
3. If `≥ 20`: write the recovery brief to `/mnt/Trade/market-brief-{today}.md`, but only if no real file exists (never overwrite a real brief, even a malformed one — the assumption is that the real task's partial output is more informative than a synthetic replacement). Required sections:
   - `# Market Brief — {today} (RECOVERY — cache-only, not a full regime assessment)` header
   - Regime label pulled from the latest `RegimeHistory` row in `master-data-log.xlsx`
   - S|T|C|R scorecard block using whatever data is available, with `(recovery-pull, {staleness_tag})` on each reading
   - Footer disclosure: `⚠ Produced by pipeline-recovery. Stale readings flagged.`
4. Post-write validation:
   ```python
   from pipeline_status import validate_recovery_brief
   from pathlib import Path
   ok, missing_sections = validate_recovery_brief(
       Path(f'/mnt/Trade/market-brief-{ps.today}.md')
   )
   ```
   If `ok`, `ps.write_recovery('market-brief', details=f'{n}/57 Grade A from cache')`. If `missing_sections`, log it and `ps.write_fail('market-brief', reason=f'recovery-brief incomplete: {missing_sections}')` — don't pretend a broken file is a recovery.

### 4c. News events recovery

If `assessment['news-events']['state'] == 'FAILED'`:

News is supplementary — a missing news file degrades the C leg but doesn't block the trade rec. Write a skeleton to `/mnt/Trade/news-events/news-{today}.md` only if no file exists:

```markdown
# News & Events — {today} (RECOVERY SKELETON)

⚠ The news-events task failed. This skeleton was produced by pipeline-recovery.
No category searches were completed. Downstream tasks should proceed with C-leg data gaps.

## What this means for today's trade rec
- Catalyst scores (C column) will lack overnight news context
- Geopolitics, macro releases, and flash events were not captured
- The trade-rec skill should note "news capture unavailable" in §1 Upstream Synthesis
```

Validate size ≥ `MIN_SIZES['news-events/news-{date}.md']` and the `# News` header sniff after writing. On success: `ps.write_recovery('news-events', details='skeleton')`.

### 4d. Trade rec recovery

If `assessment['trade-rec']['state'] == 'FAILED'`:

Do **not** re-run the trade rec. By 22:00 the trading decision window is closing, and a full rerun costs ~50K tokens. Instead:

- If the brief now exists (original or just-recovered) and the trade rec aborted due to a missing brief: print `Trade rec was not re-run (too expensive, past decision window). Brief now available; next session can re-issue manually if needed.`
- If the trade rec was never attempted because of an upstream crash: same message.
- Do not write `PARTIAL` for trade-rec — leave it as `FAIL` so consecutive counting stays accurate and tomorrow's preflight sees the miss.

### 4e. Excel sync integrity (Phase B only)

Runs only if brief OR trade-rec is in FAILED state, OR any task shows `consecutive_failures >= 3`. Opens `master-data-log.xlsx` read-only:

```python
from pipeline_status import excel_sync_check
xlsx = excel_sync_check()
# xlsx['ok'] is True iff DailyVariables and RegimeHistory last rows are dated today
```

Three common outcomes:

- `xlsx['ok'] is True` → Excel was written today; markdown failure was the only issue.
- `xlsx['note']` contains `'locked by Excel'` → Gerald had the xlsx open when the task tried to write. Flag it: `actions.append('Excel sync likely blocked — xlsx was locked; Gerald may need to close master-data-log.xlsx and re-run the brief')`.
- `xlsx['ok'] is False` and no lock note → silent sync failure. Flag it for manual investigation.

Never attempt to re-sync Excel from the recovery task. Sync logic lives in the brief/trade-rec skills, and re-running them would be expensive. Just diagnose.

---

## Step 5 — Escalate consecutive failures

After all 4a-4e work is done, check escalations once more (streaks may have been reset by successful recoveries):

```python
ps_refreshed = PipelineStatus()  # re-read, since recoveries wrote new entries
escalations = ps_refreshed.get_escalations()
```

For each `level='CRITICAL'` (≥5 consecutive failures):

Append to `/mnt/Trade/Memory.md` under a `### System Alerts` heading (create if it doesn't exist):

```markdown
### System Alert — {today}
PIPELINE ALERT: `{task}` has failed {N} consecutive days.
Last status: {summary of status entry}
Files invalid: {list of file/reason tuples}
Possible causes: data source permanently changed, script bug, sandbox network issue, scheduled task disabled.
Action required: manual investigation in next interactive session.
```

Memory.md is loaded at the start of every session, so Gerald sees the alert on next interaction.

For `level='WARNING'` (3-4 consecutive): include in recovery output only, do not write to Memory.md. May resolve on its own.

---

## Step 6 — Close watchdog and emit summary

```python
ps.finish_watchdog(
    actions=actions,
    successes=successes,
    failures=failures,
    healthy=False,
    notes='; '.join(notes) if notes else '',
)
```

**Scheduled mode output:**

```
Pipeline Recovery — {today}
Phase A: unhealthy (see below)
Phase B actions:
  - {action 1}
  - {action 2}
Recoveries succeeded: {n}
Recoveries failed: {m}
Escalations: {list or "none"}
Status file updated.
```

**Interactive mode output (verbose):**

Produce a full diagnostic. Always include, regardless of health:

- `## Pipeline Status — {today}` header (from `ps.format_summary(verbose=True)`)
- Per-task block: state, consecutive_failures, files valid/invalid with reasons, last status entry
- If Phase B ran: list of every action attempted and its outcome
- Escalations section if any
- `## History` section with `consecutive_failures` for each task and the last 3 days of `recovery` entries (read from `.pipeline-status.json`)
- `## Source Health` from `.pipeline-health.json`: last-seen timestamp, cache coverage, advisories
- `## Recommendations` section if anything is off — concrete next steps (e.g., "close master-data-log.xlsx and re-run market-brief manually")

In interactive mode, also call `excel_sync_check()` unconditionally for the diagnostic — token cost doesn't matter here.

---

## Behavioral Notes

**Healthy-path token budget.** The scheduled-mode healthy path is target <3K, hard ceiling 5K. Concretely: one Python block, one line of stdout, one status write. Do NOT:
- Load Methodology Prompt.md, research cores, Risk Rules, Memory.md
- Call `excel_sync_check()` on healthy days
- Call `subprocess.run` on healthy days
- Do any web searches on healthy days
- Write a recovery brief or skeleton news on healthy days

**Recovery briefs are degraded by design.** A cache-brief with 20 stale readings is not equivalent to a full brief with 30 live readings. The recovery brief exists to give the trade rec *something* to consume rather than aborting entirely. The `(recovery-pull)` tags and RECOVERY header prevent it from being mistaken for a real brief. The `validate_recovery_brief()` gate refuses to let a broken recovery-brief masquerade as healthy.

**Never overwrite production files.** If a real brief/news/rec exists for today, recovery does not touch it — even if the file is malformed. A partial real output is usually better than a synthetic replacement.

**Consecutive failure counter resets on any success.** A single successful recovery (PARTIAL) resets the streak to 0. Prevents false escalations when a transient issue resolves itself.

**The 22:00 slot is deliberate.** Recovery runs 1 hour after trade-rec's scheduled 21:00 to absorb jitter (~450s max) and task runtime. Running earlier risks false-positive failure detection.

**Status JSON self-heal is one-way.** If `.pipeline-status.json` is corrupt at Phase A load time, the helper moves it aside as `.pipeline-status.json.corrupt` and starts fresh. This loses `consecutive_failures` history, which is a real cost, but is the only safe recovery — fabricating history is worse. The `self_healed` flag in the result surfaces this so Gerald sees it.

**Watchdog invariant.** Every invocation of this skill must call exactly one of `clear_watchdog_healthy()` or `finish_watchdog(...)` — the former for the fast exit, the latter for Phase B. Missing either means the `in_progress` flag lingers and tomorrow's preflight will report a false crash.

**Interactive triggers override healthy short-circuit.** When Gerald asks "is the pipeline healthy?", produce the verbose Step 6 output even when `fast['healthy']` is True. The short-circuit is a scheduled-mode optimization, not a user-facing behavior.
