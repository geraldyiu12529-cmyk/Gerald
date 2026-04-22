---
name: preflight-audit-data
description: Weekday preflight — pipeline health check + audit-addition compute
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Memory.md, Risk Rules, or protocol documents.

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).

Phase 1 — Pipeline health check:
Run scripts/preflight_health_check.py to test source connectivity and write .pipeline-health.json. Log any unreachable sources.

Check .pipeline-status.json for yesterday's entries:
- If any task shows consecutive_failures >= 3, print: "⚠ CONSECUTIVE FAILURE ALERT: {task} has failed {N} consecutive days. Investigate."
- If yesterday's market-brief status is FAIL/ABORT AND today's sources are healthy, print: "Recovery opportunity: yesterday's brief failed but sources are now reachable."

Phase 2 — Audit-addition compute:
Run scripts/compute_audit_additions.py to produce `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md`. If compute fails, consult .data-cache/ for cached inputs within staleness windows per Data Sources.md §4-tier fallback and retry. Update audit-data-missing-tracker.md per RM1 protocol.

(If the compute script writes to the legacy root path `audit-data-staging-{today}.md`, move it into `{YYYY-MM-DD}/` after the run so downstream skills find it at the canonical path.)

After both phases complete:
Verify .pipeline-health.json was written today. Verify `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` exists and is non-empty. Write preflight status to .pipeline-status.json (status: OK if both files written; PARTIAL if either missing). If either check fails, append "INTEGRITY FAIL: [filename] not produced" to the output summary.

Then pack into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`; upserts §B in-place):
`python scripts/pack_daily.py --section B --source {YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md --status "{OK|PARTIAL|FAIL}"`
The per-day `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` source file is the canonical artifact (market-brief Step 0 reads it).

Exit summary (one line): `Preflight {YYYY-MM-DD} complete — sources={OK|DEGRADED}, staging={OK|MISSING}, status={OK|PARTIAL|FAIL}, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §B`

Then git add -A, commit with message "routine: preflight-audit-data {today}", and push to origin main.