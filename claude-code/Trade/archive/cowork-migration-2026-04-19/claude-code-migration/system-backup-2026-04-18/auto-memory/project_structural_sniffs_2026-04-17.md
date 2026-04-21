---
name: STRUCTURAL_SNIFFS rubric enriched 2026-04-17
description: Pipeline rubric in pipeline_status.py extended with content-level sniffs for market-brief and trade-rec; user opted for sniffs-only scope
type: project
originSessionId: 40e8aaac-2f9b-473f-b3af-f13a2013c14b
---
On 2026-04-17, `STRUCTURAL_SNIFFS` in `/mnt/Trade/scripts/pipeline_status.py` was extended beyond title-line checks to include content-level sniffs:

- `market-brief-{date}.md`: now also requires `Regime\s+Snapshot` (§1 heading) and a `Grade` reference in the first 2KB
- `trade-rec-{date}.md`: now also requires `Upstream\s+Synthesis` (§1 heading) and a `Grade` reference in the first 2KB
- News, audit-staging, and HTML templates unchanged

Verified against 2026-04-14/15/16 briefs and trade-recs — all PASS, no false-fails. `fast_health_check()` returns `healthy: True`.

**Why:** User asked whether the proposed per-task "set KPI → self-review → improve" feedback loop was effective. Answer was no (self-grading bias, criteria drift, no ground truth) but the system already has 80% of what they wanted via `pipeline-recovery` Phase A against `MIN_SIZES`/`STRUCTURAL_SNIFFS`. The real gap was that sniffs checked structure only (titles), not content discipline (§1 heading present, evidence grades cited). This change closes that gap with a single source-of-truth rubric edit, no new skill, no SKILL.md edits.

**How to apply:** If a producer skill is ever rewritten to change §1 heading text or drop "Grade" notation, the sniff will fail-loud at pipeline-recovery 22:00. Update the regex here rather than loosening the check. For richer content checks (8 methodology steps, Risk Rules checklist complete, Grade A coverage), extend this same dict — do not build a separate self-review skill. User explicitly chose "sniffs only" scope on 2026-04-17; producer skills were not modified.
