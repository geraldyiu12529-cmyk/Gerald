---
name: pipeline-smoketest
description: One-shot health check — verifies all 20 scheduled tasks are registered + recent, all 11 skills are loadable, upstream files exist, downstream output paths land where expected. Read-only; writes nothing except a single report.
---

# Pipeline Smoke Test

Goal: in one pass, confirm every scheduled task and skill is wired correctly. Output one report file. Do not modify state.

Output: `{YYYY-MM-DD}/pipeline-smoketest-{YYYY-MM-DD}.md`. `mkdir -p {YYYY-MM-DD}` first.

## Step 1 — Workspace anchor check (hard-fail on cwd drift)

```bash
set -e
case "$(pwd)" in
  */Trade) echo "OK_pwd $(pwd)" ;;
  *) echo "FAIL_pwd: cwd is $(pwd), expected path ending in /Trade — ABORT"; exit 1 ;;
esac
test -f framework/Memory.md     && echo OK_framework || { echo FAIL_framework; exit 1; }
test -f master-data-log.xlsx    && echo OK_xlsx      || { echo FAIL_xlsx; exit 1; }
test -f scripts/pack_daily.py   && echo OK_scripts   || { echo FAIL_scripts; exit 1; }
test -f pipeline/.pipeline-status.json && echo OK_pipeline || { echo FAIL_pipeline; exit 1; }
test -d .claude/skills          && echo OK_skills_dir || { echo FAIL_skills_dir; exit 1; }
```

Any FAIL → workspace anchor is wrong. Stop and report. ALL subsequent Bash calls in this skill MUST use explicit paths relative to Trade root (never bare `2026-*/...` which break if a parallel Bash call resets cwd).

**Parallel Trade tree — expected, not a bug:** `cowork/Gerald/Trade/` (relative to repo root) is the **Anthropic Cowork platform workspace**, separate from canonical `T.system/Trade/`. It has its own git history and receives independent writes from claude.ai scheduled tasks. The marker file `cowork/Gerald/Trade/DO-NOT-EDIT-HERE.md` confirms this. Do NOT flag divergence between canonical Trade/ and cowork/Gerald/Trade/ as a failure — they are independent pipelines by design. Only flag if the marker is missing (→ unexpected third tree) or if canonical Trade/ is empty while cowork has content (→ possible misrouted writes).

## Step 2 — Skill inventory

List every `.claude/skills/*/SKILL.md`. For each: parse frontmatter (`name`, `description`, `allowed-tools`). Flag any with malformed YAML or missing `name`.

Expected 11 skills: daily-trade-rec, literature-review, market-brief, news-events, pipeline-recovery, positions-monitor, quarterly-methodology-review, signal-review, system-review, trade-update, test_write.

## Step 3 — Scheduled task inventory

Call `mcp__scheduled-tasks__list_scheduled_tasks`. For each task:
- `enabled` is true
- `lastRunAt` is within expected cadence (daily tasks: last 36h on a weekday; weekly: last 8d; monthly: last 35d). Flag stale.
- Cross-reference `taskId` against the expected 20 below.

Expected 20 tasks (group by cadence):

| Group | Tasks |
|---|---|
| Pre-open daily (weekdays) | preflight-audit-data, preflight-meta-additions, news-events-daily, daily-market-brief-8pm, trade-rec-daily, pipeline-recovery-daily |
| Intraday daily | positions-monitor (09:03 weekdays), us-close-snapshot (07:38 weekdays) |
| Cloud daily | cloud-market-brief-6pm, cloud-news-events-630pm, cloud-trade-rec-7pm |
| Sub-daily | slack-ingest (4×/day) |
| Weekly | weekly-regime-signal-review (Sun 18:00), workspace-tidy (Sun 21:03) |
| Quarterly+ | quarterly-methodology-review, semi-annual-literature-review, semi-annual-system-review |
| Bootstrap | monthly-bootstrap-review |
| One-time | meta-shadow-review-2026-04-25, methodology-audit-6mo-review-2026-10-14 |

Flag any registered task NOT in the list (orphan), and any expected task NOT registered (missing).

## Step 4 — Upstream → downstream chain check

For the most recent COMPLETED weekday (skip today if pre-open hasn't run), find that date's folder `{YYYY-MM-DD}/` and verify the file chain. Mark each ✓ / ✗ / N/A.

| # | Producer task | Expected file | Reads from (upstream) |
|---|---|---|---|
| 1 | preflight-audit-data | `{date}/audit-data-staging-{date}.md` | scripts/compute_audit_additions.py + caches |
| 2 | preflight-meta-additions | `{date}/meta-additions-staging-{date}.md` | scripts/compute_meta_additions.py |
| 3 | news-events-daily | `{date}/news-{date}.md` + `.catalysts-cache/catalysts-cache-{date}.json` | WebSearch |
| 4 | daily-market-brief-8pm | `{date}/market-brief-{date}.md` | news + staging files (#1, #2, #3) |
| 5 | cloud-market-brief-6pm | `{date}/cloud-market-brief-{date}.md` (or GDrive only) | independent cloud agent |
| 6 | cloud-news-events-630pm | `{date}/cloud-news-{date}.md` | independent |
| 7 | cloud-trade-rec-7pm | `{date}/cloud-trade-rec-{date}.md` | cloud brief + news (#5, #6) |
| 8 | trade-rec-daily | `{date}/trade-rec-{date}.md` + `{date}/report-{date}-trade-rec.html` | brief + news + staging + cloud (#1–#7) |
| 9 | pipeline-recovery-daily | `pipeline/.pipeline-status.json` updated; `{date}/pipeline-recovery-{date}.md` if recovery fired | reads #1–#8 status |
| 10 | positions-monitor | `{date}/positions-monitor-{date}.md` (silent-when-OK — absence is normal) | framework/Memory.md §2 + intraday data |
| 11 | us-close-snapshot | `{date-1}/us-close-snapshot-{date-1}.md` | reads close prices + open positions |
| 12 | slack-ingest | `{date}/slack-digest-{date}.md` | Slack channel |

Reverse-check for orphan outputs: list all files in `{date}/` and flag any whose pattern doesn't match a known producer.

**Authenticity checks** (catch mock/stub outputs that look real):
- Grep each dated `.md` for headers like `[MOCK`, `[TEST`, `TEST RUN`, `STUB`, `PLACEHOLDER`. Any hit → flag the file as non-production.
- For `news-{date}.md`: if the file claims `cache written` / `✅`, verify a real cache exists at `.catalysts-cache/catalysts-cache-{date}.json`. If the claim is in the markdown but no file exists, flag as **fabricated-confirmation** (Step 10 skipped, ✅ is model text).
- For `trade-rec-{date}.md`: verify companion `report-{date}-trade-rec.html` exists. Use explicit path `{date}/report-{date}-trade-rec.html`, not glob.
- Cross-tree divergence: if `cowork/Gerald/Trade/{date}/` exists, `diff -q` key files (news, trade-rec, catalysts cache) vs canonical. Divergent mtimes or content → report which tree has the real production run (later mtime + real content wins).

## Step 5 — Excel + framework write integrity

Open `master-data-log.xlsx` (read-only). Confirm 10 sheets exist: SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes, CatalystLog, README. For each sheet, report row count + max date. Flag if any append-only sheet (SignalLedger, AuditAdditionLog, CatalystLog) hasn't seen a write in >5 weekdays.

Verify `framework/Memory.md` has §2 Open Positions, §5 Watchlist, §6 Catalysts headers. Flag if missing.

## Step 6 — Cross-skill path consistency

Grep all `.claude/skills/*/SKILL.md` for: any absolute path (`C:\` or `/c/`), any reference to `claude-code/`, `Gerald/`, or `T.system\`. Should be zero — flag every hit. Skills must use relative paths only.

## Step 7 — Report

Write `{date}/pipeline-smoketest-{date}.md`:

```
# Pipeline Smoke Test — {date} (UTC+8)

## Workspace anchor
[Step 1 results]

## Skills (11 expected)
| Skill | SKILL.md | Frontmatter | Notes |
[Step 2 table]

## Scheduled tasks (20 expected)
| Task | Enabled | Last run | Stale? | Notes |
[Step 3 table — group by cadence]

## Pipeline chain — date checked: {checked-date}
| # | Producer → File | Status | Upstream OK | Notes |
[Step 4 chain — 12 rows]

## Orphan outputs in {checked-date}/
[Files in folder that don't match any producer pattern]

## Excel sheets
| Sheet | Rows | Max date | Stale? |
[Step 5 table]

## Path consistency
[Step 6 — list every absolute/wrong-prefix path hit, or "all clean"]

## Summary
- Pass: N
- Warn: N (stale > expected cadence)
- Fail: N
- Action items: [bulleted, by severity]
```

## Step 8 — Exit

One-line summary to stdout: `Smoketest {date} complete — pass={N}, warn={N}, fail={N}. Report: {date}/pipeline-smoketest-{date}.md`.

No git commit. This is diagnostic only.
