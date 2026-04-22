---
name: weekly-backup-sunday
description: Weekly git backup — commit all changes and push to origin on Sunday at 10pm UTC+8
---

**Workspace anchor (run FIRST):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Weekly backup of the T.system/Trade workspace to git remote.

```bash
cd "$HOME/OneDrive/Desktop/T.system"
git add Trade/ --all
git status --short | head -20
CHANGED=$(git diff --cached --name-only | wc -l)
if [ "$CHANGED" -gt 0 ]; then
  git commit -m "backup: weekly $(date +%Y-%m-%d)"
  git push origin master
  echo "Backup committed and pushed — $CHANGED files"
else
  echo "No changes to backup"
fi
```

After backup: write a one-line status to `Trade/{YYYY-MM-DD}/backup-status-{YYYY-MM-DD}.md`:
- Date + time (UTC+8)
- Files committed (number or "no changes")
- Whether push succeeded or failed
- Last 5 git log --oneline lines

This is a safety net only. It does not replace the normal git commits made by individual tasks. If push fails due to auth: note the failure, do not retry, write the error to the backup-status file for manual review.