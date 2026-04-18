---
name: pipeline-recovery
description: "Pipeline health monitoring + recovery. Phase A: fast triage (<3K tokens). Phase B: recovery only if unhealthy. Use for 'check the pipeline', 'is the pipeline healthy', 'fix the pipeline', 'what failed today', 'pipeline status'."
model: haiku
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# Pipeline Recovery

Two-phase: Phase A (cheap triage via JSON + file stats) → Phase B (recovery if unhealthy). Token target: healthy <3K, recovery <15K.

## Step 1 — Phase A: fast triage

```python
import sys; sys.path.insert(0, 'scripts')
from pipeline_status import PipelineStatus
ps = PipelineStatus()
fast = ps.fast_health_check()
print(fast['summary'])
```

Returns: `healthy`, `assessment` (per-task state/streak/validity), `escalations`, `self_healed`, `prior_recovery_crash`.

## Step 2 — Healthy fast exit

If `fast['healthy']`: `ps.clear_watchdog_healthy()`, print summary, stop. In scheduled mode: no further work (no Methodology, no Memory, no Excel). Interactive mode: continue to Step 6.

## Step 3 — Phase B entry

`ps.start_watchdog()` — marks recovery in-progress for crash detection.

## Step 4 — Recovery actions (dependency order)

**4a. Preflight:** HTTP ping sweep, retry compute script, check cache fallback, validate staging file.
**4b. Market-brief:** Cache-brief if ≥20 Grade A from cache. Never overwrite real file. Validate via `validate_recovery_brief()`.
**4c. News-events:** Skeleton file if no file exists. Degrades C-leg but doesn't block trade-rec.
**4d. Trade-rec:** Do NOT re-run (past decision window, too expensive). Leave as FAIL.
**4e. Excel sync:** Read-only diagnostic. Never re-sync from recovery.
**4f. Audit-addition variable drift check (Phase B only):** Read `audit-data-missing-tracker.md`, parse the last 3 markdown-table rows (lines starting with `| 202`). For each of the three audit-addition variables (residual_momentum → col `residmom`, intermediary_capital → col `intercap`, basis_momentum → col `basismom`), count consecutive trailing MISSING entries. Build a `drift_flags` list: WARNING if streak ≥ 2, CRITICAL if streak ≥ 3. Append each flag to the `notes` block. If any flag is CRITICAL, proceed to Step 5 drift escalation. (# RM1 applied 2026-04-19)

## Step 5 — Escalate consecutive failures

CRITICAL (≥5 task failures): append System Alert to Memory.md. WARNING (3–4 task failures): recovery output only.
Drift CRITICAL (≥3 consecutive MISSING for any audit-addition variable from 4f): append a `### System Alert — {today}` block to `Memory.md` stating `AUDIT-ADDITION DRIFT: {variable} has been MISSING for {N} consecutive compute runs` and directing Gerald to inspect `audit-data-staging-{today}.md` chain_attempts block. Guard: do not append if identical alert already present. Drift WARNING (streak = 2): log to notes only, no Memory.md write.

## Step 6 — Close watchdog

`ps.finish_watchdog(actions, successes, failures, healthy=False, notes)`. Interactive mode: full diagnostic with per-task blocks, history, source health, recommendations.

## Rules
- Healthy path: NO reads of Methodology, cores, Memory, Risk Rules
- Never overwrite production files
- Consecutive counter resets on any success
- 22:00 slot absorbs jitter from 21:00 trade-rec
- Watchdog invariant: every invocation calls exactly one of `clear_watchdog_healthy()` or `finish_watchdog()`
