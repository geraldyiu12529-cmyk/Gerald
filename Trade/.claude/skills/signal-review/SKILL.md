---
name: signal-review
description: "Weekly OOS performance review — marks SignalLedger to market, computes hit rates by asset/component/regime, identifies methodology improvements. Use for 'review signals', 'check performance', 'signal review', 'OOS performance', 'how are the recs doing'."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Signal Review — Weekly Performance & Methodology Feedback

OOS record: signals logged at rec time with market price, review measures what happened after. Changes feed methodology improvement through Gerald's sign-off only — never auto-adjust.

## Step 1 — Reads

1. `master-data-log.xlsx` — SignalLedger (all rows), RegimeHistory (latest), PerformanceStats (prior stats), AuditAdditionLog
2. `framework/Methodology Prompt.md` — score component definitions
3. `framework/Memory.md` — §2 open positions, §5 watchlist
4. `framework/memory-lessons.md` — full lessons log
5. Latest `*/signal-review-*.md` (date-folder convention; any prior dates) — carry forward pending observations

If SignalLedger empty: stop with message.

## Step 2 — Expire stale signals, fetch prices

**2a. Date-based expiry (no price needed):** Near-misses past Inv_Date → EXPIRED. Promoted past Inv_Date + never taken → EXPIRED.

**2b. Price fetch (remaining OPEN):** Priority: Taken=YES first, then other Promoted, Near-Miss last. Sources: latest brief/snapshot, then WebSearch. Defer Near-Miss fetches if rate-limited.

## Step 3 — Update statuses

**Promoted:** HIT_TARGET (price reached TP1), HIT_STOP (breached ATR stop), EXPIRED (past inv date), STILL_OPEN. Calculate Hypo P&L %.

**Near-Miss:** WOULD_HIT_TARGET, WOULD_HIT_STOP, EXPIRED, STILL_OPEN. Calculate Hypothetical Move %.

## Step 4 — Compute rolling statistics (13 dimensions)

Update **PerformanceStats** sheet:

1. Win rate by score component (S/T/C/R univariate)
2. Win rate by asset class (Crypto/Equities/ETFs/Commodities)
3. Win rate by regime label
4. Blocking leg breakdown (which component most often blocks)
5. Average hypo P&L (promoted) and move (near-miss)
6. Best/worst individual signals
7. **Score interaction matrix** (S×T, S×R, T×R, etc.) — 3×3 contingency, flag >15pp differential as SYNERGY/CONFLICT
8. **Time-to-exit distribution** — ≤5d, 6–14d, 15–28d, >28d buckets with win rate per bucket
9. **MAE/MFE analysis** — worst/best close before exit
10. **Catalyst resolution** — did C=+1 events resolve as expected?
11. **VIX-at-entry conditioning** — win rate when VIX>25 vs <20 vs between
12. **Near-miss counterfactual regression** — would promoting near-misses have improved overall stats?
13. **Audit-addition variable contribution** — did residual-mom/intermediary-cap/basis-mom move any score leg into/out of entry?

## Step 5 — Escalation flags

Check for: SCORE-LEG-COLLAPSE (component stops predicting), DATA-SOURCE-DEGRADATION (rising MISSING rate), GATE-TOO-AGGRESSIVE (too many viable signals blocked), AUDIT-ADDITION-STALL (no contribution across review window).

## Step 6 — Methodology improvement candidates

Surface 1–3 concrete proposals from the statistical evidence. Each: observation, hypothesis, proposed change, required evidence threshold, Gerald sign-off required.

## Step 7 — Write output

Path: `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` (create folder first: `mkdir -p {YYYY-MM-DD}`) + update PerformanceStats sheet + VariableRegistry maintenance.

## Step 8 — Update framework/Memory.md

Append to `framework/memory-lessons.md`: date, signal count, win rates, escalation flags, improvement candidates.
