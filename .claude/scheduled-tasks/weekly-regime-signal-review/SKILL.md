---
name: weekly-regime-signal-review
description: Sunday weekly regime review + signal review (marks SignalLedger, hit rates, methodology)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

Run the weekly regime review and signal review.

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).

PIPELINE INTEGRITY PRE-CHECK (run before Phase 1):
Identify today's date and the 5 weekdays (Mon–Fri) in the most recently completed trading week. Check for `*/market-brief-{date}.md` files (glob; fall back to root `market-brief-{date}.md` for legacy runs) covering those 5 days. Also check .pipeline-status.json for consecutive failure counts across all tasks.

- If fewer than 4 of 5 daily briefs are present: output "PIPELINE INTEGRITY WARNING — only {n}/5 weekly briefs found. Proceeding but flagging low confidence." Add a ## Data Coverage section to the output noting missing days.
- If 0 or 1 briefs found: output "PIPELINE INTEGRITY FAIL — insufficient brief history ({n}/5). Weekly review aborted." STOP.
- If any task shows consecutive_failures >= 3: add a ## ⚠ Pipeline Health Alert section listing each failing task and its count.

Phase 1 — Regime review:
Read Memory.md, the latest `*/market-brief-*.md`, and all `*/news-*.md` from the past 7 days (glob across date folders, fall back to root for legacy runs). Write `{YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md` covering: regime trajectory for the week, key macro/geopolitical events, thesis validation for open positions, and distilled lessons. Condense memory-lessons.md (remove superseded entries, tighten surviving ones).
After Phase 1, pack §W into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`; upserts §W):
`python scripts/pack_daily.py --section W --source {YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md --status OK`

Phase 2 — Signal review:
/signal-review
Marks-to-market every hypothetical signal in the SignalLedger sheet of master-data-log.xlsx. Computes hit rates by asset class / score component / regime. Identifies methodology improvements. Writes `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` + `{YYYY-MM-DD}/report-{YYYY-MM-DD}-signal-review.html`. Updates PerformanceStats sheet.
After Phase 2, pack §S into the consolidated daily file (markdown only — the HTML report stays a separate file):
`python scripts/pack_daily.py --section S --source {YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md --status OK`

Then git add -A, commit with message "routine: weekly-regime-signal-review {today}", and push to origin main.