---
name: quarterly-methodology-review
description: Quarterly methodology review — variable pipeline, research core reconciliation, VariableRegistry update
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

Ensure today's date folder exists before invoking the skill: `mkdir -p {YYYY-MM-DD}`.

/quarterly-methodology-review

Runs the full quarterly meta-review:
- Audits whether each analytical dimension in the signal review is earning its keep
- Reconciles research cores (Coin core.md / Trad core.md) against out-of-sample ledger evidence in PerformanceStats sheet
- Manages the variable candidate pipeline (promote, hold, retire decisions)
- Updates VariableRegistry sheet in master-data-log.xlsx
- Writes `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md`

Then git add -A, commit with message "routine: quarterly-methodology-review {today}", and push to origin main.