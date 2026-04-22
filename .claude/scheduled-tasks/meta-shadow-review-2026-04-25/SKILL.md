---
name: meta-shadow-review-2026-04-25
description: One-time Phase 3 GO/NO-GO review for V029–V035 shadow variables (fires 2026-04-25)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).

Read all `*/meta-additions-staging-*.md` files from 2026-04-20 to 2026-04-24 (5 shadow-run days; glob across date folders, fall back to root path `meta-additions-staging-*.md` for legacy runs).

For each of V029–V035 (BAB, DealerGamma, GP/A, CEI, Faber TAA V033–V035):
- Report: days retrieved successfully, contribution rate, any instance where the variable was decision-moving in the shadow analysis
- Verdict: PROMOTE to live scoring (Phase 3 GO) / HOLD in shadow for another review cycle / RETIRE

Cross-check against the 2026-04-18 deployment memo in Methodology Prompt.md for the original promotion criteria.

Write `{YYYY-MM-DD}/meta-shadow-review-2026-04-25.md` (today's date folder, file name retains the fixed 2026-04-25 anchor for downstream consumers) with per-variable verdict table and narrative justification.

If any variable earns PROMOTE: note that Phase 3 SKILL.md edits in patches/ must now be applied (market-brief, news-events, daily-trade-rec). Gerald must authorize explicitly before applying.

Then git add -A, commit with message "routine: meta-shadow-mode-review 2026-04-25", and push to origin main.