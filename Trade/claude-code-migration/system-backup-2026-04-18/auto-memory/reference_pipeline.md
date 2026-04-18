---
name: Scheduled pipeline — task IDs, timing, and dependencies
description: The daily and weekly scheduled task chain with IDs, cron times (UTC+8), dependency order, and known failure modes
type: reference
---
## Daily pipeline (Mon–Fri, all times UTC+8 local)

| Order | Time | Task ID | Produces | Depends on |
|---|---|---|---|---|
| 1 | 07:30 | `us-close-snapshot-730am-v2` | `us-close-snapshot-YYYY-MM-DD.md` | Nothing (post US close) |
| 2 | 19:45 | `preflight-audit-data-1945pm` | `.pipeline-health.json` + `audit-data-staging-YYYY-MM-DD.md` | Phase 1: tests connectivity, checks cache. Phase 2: 4-tier retrieval for audit-addition variables. Includes read-override (skips Methodology Prompt, Memory.md, etc.) |
| 3 | 20:00 | `daily-market-brief-8pm-v2` | `market-brief-YYYY-MM-DD.md` + `.pipeline-status.json` update | Reads audit-data staging file |
| 4 | 20:00 | `daily-news-events-810pm-v2` | `news-events/news-YYYY-MM-DD.md` + `.pipeline-status.json` update | Web access for news search (fires concurrently with brief) |
| 5 | 21:00 | `daily-trade-recommendation-820pm-v2` | `trade-rec-YYYY-MM-DD.md` + `report-YYYY-MM-DD-trade-rec.html` + SignalLedger append + `.pipeline-status.json` update | All of the above + loads `daily-trade-rec` skill. Hard-aborts if brief missing. |
| 6 | 22:00 | `pipeline-recovery-830pm` | Recovery briefs/news skeletons if upstream failed + `.pipeline-status.json` update + Memory.md alerts for consecutive failures ≥5 | Reads `.pipeline-status.json` written by tasks 2-5. Loads `pipeline-recovery` skill. |

## Weekly pipeline (Sunday, UTC+8 local)

| Order | Time | Task ID | Produces |
|---|---|---|---|
| 1 | 18:00 | `weekly-regime-signal-review-6pm` | Phase 1: `weekly-review-YYYY-MM-DD.md` + memory-lessons condensation. Phase 2: `signal-review-YYYY-MM-DD.md` + `report-YYYY-MM-DD-signal-review.html` + SignalLedger/PerformanceStats updates |
| 2 | 21:00 | `workspace-tidy-sunday-9pm` | Archive moves + cleanup log + diagnostics |

## Disabled tasks (kept for rollback)

| Task ID | Replaced by | Disabled date |
|---|---|---|
| `preflight-health-check-1945pm` | `preflight-audit-data-1945pm` | 2026-04-16 |
| `audit-data-compute-750pm` | `preflight-audit-data-1945pm` | 2026-04-16 |
| `weekly-regime-review-sunday-6pm-v2` | `weekly-regime-signal-review-6pm` | 2026-04-16 |
| `weekly-signal-review` | `weekly-regime-signal-review-6pm` | 2026-04-16 |

## One-time

| Fire date | Task ID | Purpose |
|---|---|---|
| 2026-10-14 | `methodology-audit-6mo-review-2026-10-14` | Keep/demote decision for 3 audit-addition variables |

## Monthly (temporary)

| Schedule | Task ID | Purpose |
|---|---|---|
| 19:00, 1st of May & Jun | `monthly-bootstrap-review` | Bootstrap health check; auto-disables after Jul 1 |

## Semi-annual

| Schedule | Task ID | Purpose |
|---|---|---|
| 15:00, 1st of Jan & Jul | `semi-annual-literature-review` | Systematic academic lit scan for new tradeable variables; feeds quarterly review's candidate pipeline |

## Quarterly

| Schedule | Task ID | Purpose |
|---|---|---|
| 19:00, 1st of Jan/Apr/Jul/Oct | `quarterly-methodology-review` | Meta-review of signal review dimensions + research reconciliation + variable pipeline |

## Known failure modes

- **Audit-data compute produces all MISSING:** Mitigated by 4-tier fallback framework (2026-04-16). Persistent cache at `/mnt/Trade/.data-cache/`. Market-model (1-factor) fallback for residual momentum. Only a multi-day outage exceeding staleness windows produces true MISSING.
- **FRED API blocked from sandbox:** Confirmed 2026-04-16. FRED variables rely on Tier 2 web search as primary, with cache as backup.
- **Task-level crash/timeout:** Mitigated by pipeline-recovery-830pm task (2026-04-16). Detects failures via `.pipeline-status.json`, produces cache-briefs and skeleton news files. Consecutive failures ≥5 escalate to Memory.md for manual investigation.
- **Trade rec delta-check bug:** Step 0 conflates "file missing" with "file unchanged" — `p.exists()` returning False makes `changed = False`, silently carrying forward prior rec. Mitigated by integrity pre-check prepend in task prompt (checks file existence before delta-check runs).

## Optimization changelog

- **2026-04-15:** Signal-review offset from 18:00 → 18:30 to eliminate co-scheduling race with regime review.
- **2026-04-16:** Merged preflight + audit-data into single task (`preflight-audit-data-1945pm`). Saves 1 session startup (~35-40K system prompt tokens/day). Eliminates jitter-based ordering risk between the two tasks. Merged task includes read-override to skip unnecessary startup reads (Methodology Prompt, Memory.md, Risk Rules, etc.).
- **2026-04-16:** Merged weekly regime review + signal review into single task (`weekly-regime-signal-review-6pm`). Saves 1 session startup (~35-40K tokens/week). Guarantees regime review completes before signal review starts (previously relied on 30-min cron gap). Eliminates the race condition fix from 2026-04-15.
- **2026-04-17:** Hardened `pipeline-recovery-830pm`. Recovery skill now splits into Phase A (fast triage, target <3K tokens, ~0.4ms Python on healthy days — file stat + 2KB header sniff + JSON load only) and Phase B (recovery, runs only when unhealthy). New failure modes covered: truncated/corrupt output files (per-file MIN_SIZES + structural sniff), corrupt `.pipeline-status.json` (self-heal — moves to `.corrupt` backup, rebuilds from file evidence), Excel sync drift (read-only `excel_sync_check`, Phase B only), recovery-brief structural validation (refuses to mark incomplete recovery as PARTIAL), recovery-task self-watchdog (in_progress marker detects recovery crashes). Size gates now single-source-of-truth in `pipeline_status.MIN_SIZES`. Trade-rec integrity check now validity-gated, not just existence. Helper script at `/mnt/Trade/scripts/pipeline_status.py`; bundle at `/mnt/Trade/pipeline-recovery.skill`. Sandbox verified all 9 scenarios pass; deployed helper dry-ran clean against live `.pipeline-status.json`.

## Monitoring

- DataQuality sheet in `master-data-log.xlsx` tracks daily MISSING rates with tier distribution (T1/T2/T3/T4).
- Retrieval log at `/mnt/Trade/.data-cache/retrieval-log.jsonl` records per-run fetch statistics.
- Preflight health check (Phase 1 of `preflight-audit-data-1945pm`) tests source connectivity and writes `.pipeline-health.json`.
- `.pipeline-status.json` tracks task-level completion, consecutive failure counts, and recovery actions. Written by each task on completion; read by downstream tasks and recovery task.
- `Pipeline-Recovery-Protocol.md` documents the full task-level failure architecture, integrity check text for each task prompt, and recovery logic.

## Future optimization (requires manual prompt access)

- **us-close-snapshot-730am-v2** and **workspace-tidy-sunday-9pm**: add read-override instructions to skip unnecessary startup reads. Requires editing task prompts on the Windows filesystem (Claude cannot read/write `C:\Users\Lokis\Documents\Claude\Scheduled\` from sandbox). Prepend to each task prompt: `**CRITICAL: This is a utility task, NOT a trading question. Do NOT follow the CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, or protocol documents unless explicitly listed below.**` Estimated savings: ~30-50K tokens per task per run.
