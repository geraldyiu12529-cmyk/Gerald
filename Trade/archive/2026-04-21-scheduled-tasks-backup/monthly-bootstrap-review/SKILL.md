---
name: monthly-bootstrap-review
description: Bootstrap health check — verify all 16 routines firing (auto-disables after 2026-07-01)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

If today's date >= 2026-07-01: print "Auto-disable threshold reached. No action taken. Gerald: please pause this routine." and exit without doing any checks.

Bootstrap health check — verify all routines are firing and producing valid output.

Check git log for routine commits from the past 7 days. For each of the 16 routines, confirm at least one commit appeared in its expected window. Report any routine with no commits as MISSED.

Spot-check output quality: read the most recent `*/market-brief-*.md` (glob across date folders; fall back to root `market-brief-*.md` for legacy runs) and confirm it contains a regime label, a scorecard table, and at least 10 variable readings.

Check .pipeline-status.json for any task with consecutive_failures > 0.

If today's date >= 2026-07-01: print "Auto-disable threshold reached. No action taken. Gerald: please pause this routine." and exit without doing any checks.

Report status and any issues found.

Then git add -A, commit with message "routine: monthly-bootstrap-review {today}", and push to origin main.