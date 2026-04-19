---
name: System state — current architecture and key dates
description: Consolidated state of the trading workspace — architecture decisions, audit-addition timeline, upcoming review dates, and operational status
type: project
originSessionId: fa7d637e-e782-4f14-9161-6cd76456528d
---
## Architecture (established 2026-04-14 through 2026-04-16)

- Workspace created 2026-04-14 with methodology, research cores, and Memory.md
- Excel (`master-data-log.xlsx`) is sole structured data store (9 sheets). Markdown deleted for hypo-ledger, data-quality-scorecard, audit-data-missing-tracker, and Memory.md §3/§4/§10.
- 4-tier data retrieval fallback (HTTP → WebSearch → Cache → MISSING) with persistent cache at `/mnt/Trade/.data-cache/`. FRED blocked from sandbox.
- Variable discovery protocol: 4 sources (academic, market obs, practitioner, repeated behavior). Quarterly review = sole promotion gate.
- 6 skills installed, 11 active scheduled tasks (4 disabled after consolidation), 40 unit tests passing.
- **2026-04-16 pipeline optimization:** Merged preflight+audit-data into one task; merged weekly regime+signal review into one task. Saves ~2 session startups/day + 1/week (~35-40K tokens each). 4 old tasks disabled but kept for rollback.

## Audit-Addition Variables (added 2026-04-14)

Three Grade A additions from peer-reviewed audit:
1. **Residual momentum** (Blitz-Huij-Martens 2011) — equity T-input. Projected post-decay Sharpe 0.6–0.9.
2. **Intermediary capital ratio** (He-Kelly-Manela 2017) — cross-asset R-overlay. Projected post-decay Sharpe 0.4–0.7.
3. **Basis-momentum** (Boons-Prado 2019) — commodity S-input. Projected post-decay Sharpe 0.6–1.0. Early-CONFIRMED (2 divergence caps decision-moving as of 2026-04-15).

**6-month review due 2026-10-14** (one-time task `methodology-audit-6mo-review-2026-10-14`). If no decision-moving contribution, demote to Grade B.

## Key Dates

- **2026-07-01:** First quarterly methodology review (Q3) + first semi-annual literature review. Expect ~60-90 closed signals.
- **2026-10-01:** Q4 review — must include formal GO/NO-GO for audit additions.
- **2026-10-14:** Hard deadline for audit-addition keep/demote decision.

## Signal Review Enhancements (2026-04-15)

13 analytical dimensions total (7 original + 6 added): score interactions, time-to-exit, MAE/MFE, catalyst resolution, VIX conditioning, near-miss regression. Archival at 80 rows.

## Inaugural Review Results (2026-04-15)

All 13 dimensions RETAIN. 0 change proposals. Basis-momentum early-CONFIRMED. 5 variable candidates (GEX, lead-lag, correlation-regime, decision tree, calendar) all DEFER pending data. Statistics unreliable below ~30 signals.

## Scheduled-Task Recovery Event (2026-04-17)

**All 14 scheduled tasks recreated from scratch.** Pre-existing DB metadata was orphaned (Windows-side `C:\Users\Lokis\Documents\Claude\Scheduled\<taskId>\SKILL.md` files missing while DB entries persisted), causing every task to fail with "Task file not found or has unexpected format." Sandbox cannot reach the Windows path, so recovery path: Gerald deleted all 14 tasks via the UI trash icon to clear taskId conflicts, then the sandbox fired 14 `create_scheduled_task` calls in one batched message.

**Integrity preserved:** cron expressions, fireAt timestamps, descriptions, and hardening (trade-rec integrity pre-check, preflight self-check, pipeline-recovery Phase A budget, positions-monitor silent-when-OK, us-close-snapshot/workspace-tidy read-overrides, system-review skill-creator chain) are exact reconstructions of the documented originals — validated against `/mnt/Trade/scheduled-task-recovery-prompt.md`, `/mnt/Trade/Pipeline-Recovery-Protocol.md`, `reference_pipeline.md`, and the skill SKILL.md files.

**Lost:** run history on every task. All `consecutive_failures` counters reset to absent (treated as 0 on next run).

**Implication for future sessions:** the 14 task prompts are freshly reconstructed as of 2026-04-17 and may diverge subtly from the originals in areas not documented in the authoritative files. If a task's behavior seems off, cross-check the prompt against this event and the authoritative docs rather than assuming stable ground truth from prior runs.
