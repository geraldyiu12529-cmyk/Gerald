---
name: quarterly-methodology-review
description: "Quarterly meta-review — analytical dimension fitness audit, research core reconciliation, variable candidate pipeline management. Use for 'quarterly review', 'review the methodology', 'audit the system', 'is the system working'. Operates above weekly signal-review."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Quarterly Methodology Review

Three questions the weekly review can't answer: (1) Is the signal review asking the right questions? (2) Does the research still hold? (3) What should we try next? Every change proposal requires Gerald's sign-off.

## Step 1 — Reads

1. `master-data-log.xlsx` — SignalLedger (all), PerformanceStats, RegimeHistory, AuditAdditionLog
2. `framework/Methodology Prompt.md` — Top-28 variables, 8-step framework
3. `framework/Risk Rules.md` — binding constraints
4. `framework/Data Sources.md` — variable-to-source mapping
5. `framework/Trad core.md` + `framework/Coin core.md` — research evidence
6. `framework/Memory.md` — §9 research questions
7. `framework/memory-lessons.md` — full lessons log
8. All `*/signal-review-*.md` files (date-folder convention) — §7 improvement candidates
9. Prior `*/quarterly-methodology-review-*.md` — pending actions

If <30 closed signals: add "Early-stage review" banner.

## Step 2 — Analytical dimension fitness audit

13 dimensions (7 original + 6 from 2026-04-15): win rate by component, by asset class, by regime, blocking leg, average P&L, best/worst, interaction matrix, time-to-exit, MAE/MFE, catalyst resolution, VIX conditioning, near-miss regression, audit-addition contribution.

Each rated: RETAIN / DEMOTE / RETIRE / PROMOTE.

## Step 3 — Research core reconciliation

Cross-check Top-28 claims against ledger evidence. Flag divergences (research says predictive, ledger says not, or vice versa).

## Step 4 — Variable candidate pipeline

Tier 2 (promising, need more data) and Tier 3 (speculative). Advance, hold, or remove candidates.

## Step 5 — Methodology change proposals

QR-prefixed proposals. All require Gerald sign-off.

## Step 6 — Context budget assessment

Weekly review token cost. Are any dimensions burning context for zero insight?

## Output
Dated review file at `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md` (create folder first: `mkdir -p {YYYY-MM-DD}`) + VariableRegistry updates + methodology change proposals.
