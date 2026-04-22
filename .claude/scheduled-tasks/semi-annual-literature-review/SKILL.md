---
name: semi-annual-literature-review
description: Semi-annual academic finance literature scan for new tradeable variables
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

Ensure today's date folder exists before invoking the skill: `mkdir -p {YYYY-MM-DD}`.

/literature-review

Runs the semi-annual academic finance literature scan:
- Searches working papers and journals for new tradeable factors meeting the 5 inclusion criteria (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable)
- Assesses candidates against Gerald's framework gaps
- Writes structured candidate proposals for the variable pipeline
- Output: `{YYYY-MM-DD}/literature-review-{YYYY-MM-DD}.md` (scope-suffixed variants permitted per the skill)

Then git add -A, commit with message "routine: semi-annual-literature-review {today}", and push to origin main.