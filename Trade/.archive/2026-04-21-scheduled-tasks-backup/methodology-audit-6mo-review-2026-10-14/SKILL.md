---
name: methodology-audit-6mo-review-2026-10-14
description: One-time 6-month keep/demote review for residual-mom, intermediary capital ratio, basis-momentum (fires 2026-10-14)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

Six-month keep/demote review for the 3 audit-addition variables added 2026-04-14:
1. Residual momentum (12m FF5-residualized) — T-input for single stocks
2. Intermediary capital ratio (NY Fed PD z-score) — R-overlay cross-asset
3. Basis-momentum (4w/12w F1–F2 slope change) — S-input for commodities

For each variable:
- Read AuditAdditionLog sheet in master-data-log.xlsx for all entries since 2026-04-14
- Read audit-data-missing-tracker.md for MISSING rates
- Compute: days LIVE, number of decision-moving contributions, contribution rate normalized by days LIVE
- Verdict: KEEP at Grade A / DEMOTE to Grade B / REMOVE from pipeline

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).

Read `*/methodology-audit-6mo-review-2026-10-14.md` (glob; fall back to root) for any pre-written decision criteria.

Write `{YYYY-MM-DD}/methodology-audit-6mo-review-2026-10-14-DECISION.md` with per-variable verdict, supporting evidence, and any required updates to Methodology Prompt.md, Data Sources.md, or SKILL.md files.

Then git add -A, commit with message "routine: methodology-audit-6mo-review 2026-10-14", and push to origin main.