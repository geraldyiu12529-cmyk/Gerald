# Memory Index

- [User — Gerald trading profile](user_gerald.md) — discretionary cross-asset + crypto trader using evidence-graded methodology
- [Open Positions State](project_open_positions.md) — Current positions; updated each trade-update. As of 2026-04-21 19:00 UTC+8: P008 CL long open (off-meth, heat ~0.33%); P009 SPY + P010 EWJ pending fill (methodology promotions).
- [Workspace Canonicalization](project_workspace_canonicalization.md) — Canonical is `T.system/Trade/`. `cowork/Gerald/cloud-sync/` (renamed from Trade 2026-04-21) is dormant mirror. Only 2 `.claude` dirs remain; 21 worktrees pruned.
- [Feedback — Skill Editing Workflow](feedback_skill_editing_workflow.md) — Any skill edit: full folder → ZIP (folder as root) → present_files → 3-line handoff. Never diffs, never Settings.
- [Feedback — Evidence-grade discipline](feedback_evidence_grades.md) — cite A/B/C grades, never pad with Grade C, no stock-to-flow timing
- [Feedback — Trade execution events](feedback_trade_execution.md) — any entry/exit/adjustment must invoke trade-update skill and apply 4-layer protocol
- [Reference — Scheduled pipeline](reference_pipeline.md) — task IDs, cron times (UTC+8), dependency chain; migrated to Claude Code routines 2026-04-19
- [Reference — SKILL.md description character limit](reference_skill_description_limit.md) — Anthropic's 1024-char cap; descriptions preloaded every session
- [Reference — HTML Report Format](reference_html_report_format.md) — Canonical trade-rec HTML format locked 2026-04-21; use `scripts/gen_trade_rec_html.py`, never write HTML manually; 20-section order; analyst sections: freshness strip, V026 full table, factor exposure, signal age, regime sensitivity, closed-trade context
