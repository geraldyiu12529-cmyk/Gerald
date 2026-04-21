---
name: positions-monitor
description: Intraday positions watchdog — stop buffers, thesis variables, catalyst check
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

Ensure today's date folder exists before invoking the skill: `mkdir -p {YYYY-MM-DD}`.

/positions-monitor

After the skill completes, pack §G into the consolidated daily file:
- If `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` exists (flags fired):
  `python scripts/pack_daily.py --section G --source {YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md --status "flags"`
- If no file was written (silent-when-OK):
  `python scripts/pack_daily.py --section G --content "Silent — no flags fired at 09:00 check." --status SILENT`

(Creates `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md` if missing; upserts `## §G — Positions Monitor`.)

Then git add -A, commit with message "routine: positions-monitor {today}", and push to origin main. If the skill exited silently (no flags), the commit message should note "silent-OK".