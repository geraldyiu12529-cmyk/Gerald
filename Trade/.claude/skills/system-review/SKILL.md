---
name: system-review
description: "Semi-annual architecture + efficiency audit. Maps skills/tasks/files to value chain, produces KEEP/MODIFY/MERGE/REMOVE verdicts. Two tests: value (does it earn money?) and efficiency (minimum token cost?). Use for 'system review', 'strategic review', 'audit architecture', 'optimize the system', 'reduce token burn'."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit Grep Glob
---

# System Review — Strategic Architecture + Efficiency Audit

Every skill, task, and file must pass: (1) Value — moves/protects money or produces actionable insight, AND (2) Efficiency — minimum token cost for the decision quality. Does NOT edit anything — produces ranked patch file for Gerald's review.

## Value chain buckets
1. Research (lit review, quarterly review, cores)
2. Rec-generation (brief, news, preflight, trade-rec)
3. Execution (trade-update, reactive)
4. Monitoring (positions-monitor)
5. Post-trade review (signal-review, weekly regime)
6. Infrastructure (workspace-tidy, pipeline-recovery, us-close)
7. Meta-review (this skill, quarterly-methodology)

## Seven phases

**Phase 1 — Inventory:** List all skills, scheduled tasks, workspace files, memory files. No interpretation.

**Phase 2 — Value-chain map:** Assign each process to a bucket. Identify gaps (empty buckets) and redundancies.

**Phase 3 — Per-process audit:** 6 questions each: (1) What decision does it inform? (2) When did it last change a trade? (3) Token cost per run? (4) Can same quality be achieved cheaper? (5) Does it duplicate another process? (6) Would removing it degrade decision quality?

**Phase 4 — Gap & redundancy analysis:** Architecture gaps, overlapping scopes, shared-artifact opportunities.

**Phase 5 — Ranked proposals:** ADD/REMOVE/MODIFY-scope/MODIFY-efficiency. Tagged HIGH/MEDIUM/LOW by P&L impact or tokens freed.

**Phase 6 — Self-audit:** What happened to prior cycle's proposals?

**Phase 7 — Output:** Patch file with concrete changes at `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` (+`.html`) — Gerald reviews. Create folder first: `mkdir -p {YYYY-MM-DD}`. If skill-creator chaining is enabled, write one patch per MODIFY target to `patches/`.

## Scope boundaries
Does NOT audit: methodology dimensions (quarterly-review), signal marking (signal-review), file retention (retention policy), pipeline failures (pipeline-recovery), variable pipeline (literature-review).
