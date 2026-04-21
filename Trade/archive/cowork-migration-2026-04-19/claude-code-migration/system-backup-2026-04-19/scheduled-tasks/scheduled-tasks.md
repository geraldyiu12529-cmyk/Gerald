# Scheduled Tasks — Snapshot 2026-04-19

All times local (UTC+8). 17 active tasks, enabled. Captured via `list_scheduled_tasks` on 2026-04-19.

## Daily (weekdays Mon–Fri)

| Time | Task ID | Cron | Purpose |
|------|---------|------|---------|
| 07:30 | `us-close-snapshot-730am-v2` | `30 7 * * 1-5` | US post-close delta snapshot — open positions mark + >1σ moves vs brief |
| 09:00 | `positions-monitor-intraday-9am` | `0 9 * * 1-5` | Intraday live-book watchdog — silent-when-OK |
| 19:00 | `preflight-audit-data-1945pm` | `0 19 * * 1-5` | Pre-pipeline source health + 3 audit-addition compute |
| 19:52 | `preflight-meta-additions-1952pm` | `52 19 * * 1-5` | SHADOW MODE — V029–V035 meta-integration compute (Phase 2) |
| 20:00 | `daily-market-brief-8pm-v2` | `0 20 * * 1-5` | Daily market brief — regime scorecard + S/T/C/R + Excel sync |
| 20:00 | `daily-news-events-810pm-v2` | `0 20 * * 1-5` | News & events capture — geopolitics, macro, earnings, catalysts cache |
| 21:00 | `daily-trade-recommendation-820pm-v2` | `0 21 * * 1-5` | Daily pre-open trade rec — 8-step + SignalLedger append |
| 22:00 | `pipeline-recovery-830pm` | `0 22 * * 1-5` | Post-pipeline health + recovery (Phase A triage, Phase B if unhealthy) |

## Weekly (Sunday)

| Time | Task ID | Cron | Purpose |
|------|---------|------|---------|
| 18:00 | `weekly-regime-signal-review-6pm` | `0 18 * * 0` | Merged weekly regime review + OOS signal-review (2 phases, single session) |
| 21:00 | `workspace-tidy-sunday-9pm` | `0 21 * * 0` | Archive per Retention Policy + memory consolidation + diagnostics |

## Monthly / Quarterly / Semi-annual

| When | Task ID | Cron / Fire | Purpose |
|------|---------|-------------|---------|
| 1st of May, Jun 19:00 (one-off window) | `monthly-bootstrap-review` | `0 19 1 5,6 *` | Bootstrap health check — May/Jun 2026 only, self-retires after Jul-1 |
| 1st of Jan, Apr, Jul, Oct 19:00 | `quarterly-methodology-review` | `0 19 1 1,4,7,10 *` | Quarterly meta-review — dimension audit + Top-28 reconciliation + variable pipeline |
| 1st of Jan, Jul 15:00 | `semi-annual-literature-review` | `0 15 1 1,7 *` | Academic factor scan — feeds quarterly's candidate pipeline |
| 1st Sunday of May, Nov 19:00 | `system-review-semi-annual` | `0 19 1-7 5,11 0` | Strategic architecture + efficiency audit; chains skill-creator for patches |

## One-time reviews

| Fire at | Task ID | Purpose |
|---------|---------|---------|
| 2026-04-25 10:00 | `meta-shadow-mode-review-2026-04-25` | 5-business-day review of V029–V035 shadow-mode output; recommends Phase 3 promotion if ≥80% LIVE |
| 2026-10-14 09:00 | `methodology-audit-6mo-review-2026-10-14` | 6mo live-monitoring review of 3 original audit-addition variables (first valued 2026-04-14/15) |
| 2026-10-14 09:30 | `methodology-audit-6mo-review-batch2-2026-10-14` | Batch-2 companion: 6mo review of V029–V035 meta-integration variables (added 2026-04-18) |

## Dependency chain (weekday pipeline)

```
07:30 us-close-snapshot
09:00 positions-monitor ────(silent unless flagged)
  │
19:00 preflight-audit-data ──► audit-data-staging-YYYY-MM-DD.md
19:52 preflight-meta-additions ─► meta-additions-staging-YYYY-MM-DD.md (SHADOW)
  │
20:00 daily-market-brief ──┐
20:00 daily-news-events ───┤
  │                        │
21:00 daily-trade-rec ◄────┘  (consumes brief + news + staging files)
  │
22:00 pipeline-recovery (skeleton files only if any upstream failed)
```

## Notes

- All cron expressions are in the agent's scheduler; `nextRunAt` / `lastRunAt` timestamps omitted from this snapshot (dynamic state).
- `jitterSeconds` adds randomized start delay to smooth load.
- Restore procedure: use `mcp__scheduled-tasks__create_scheduled_task` with each cron + description, or import via the `schedule` skill.
