---
name: semi-annual-system-review
description: Semi-annual strategic architecture + efficiency audit (first Sunday of May and November)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

If today is not a Sunday, exit silently without doing any work.

Ensure today's date folder exists before invoking the skill: `mkdir -p {YYYY-MM-DD}`.

/system-review

Runs the semi-annual strategic architecture and efficiency audit:
- Walks every skill, scheduled task, and workspace file
- Maps each to the research → trade → monitor → earn value chain
- Produces KEEP / MODIFY / MERGE / REMOVE verdicts using two tests: value (does it earn money) and efficiency (at minimum token cost)
- Identifies architecture gaps AND redundant token burn
- Ranks proposals by P&L impact or context-budget freed for the trade rec
- Output: `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` (+ `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.html`)

Then git add -A, commit with message "routine: system-review-semi-annual {today}", and push to origin main.