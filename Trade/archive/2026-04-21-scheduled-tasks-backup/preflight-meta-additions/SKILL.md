---
name: preflight-meta-additions
description: Shadow compute for V029–V035 meta-addition variables (BAB, DealerGamma, GP/A, CEI, Faber TAA)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

CRITICAL: shadow mode only — do NOT feed results into market-brief or trade-rec.

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}`.

Run scripts/compute_meta_additions.py to produce `{YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md`. The file covers seven shadow variables: V029 BAB (betting-against-beta), V030 DealerGamma, V031 GP/A (gross-profitability-to-assets), V032 CEI (composite equity issuance), V033–V035 Faber TAA signals.

(If the compute script writes to the legacy root path `meta-additions-staging-{today}.md`, move it into `{YYYY-MM-DD}/` after the run so downstream skills find it at the canonical path.)

For each variable, log status (RETRIEVED / MISSING / STALE) to AuditAdditionLog sheet in master-data-log.xlsx with Type=SHADOW. Do NOT promote to live scoring until the 2026-04-25 shadow review clears Phase 3.

If today's date >= 2026-04-25 and `*/meta-shadow-review-2026-04-25.md` (glob) contains PROMOTE verdicts for any variable, add a note: "Phase 3 GO/NO-GO complete — check meta-shadow-review-2026-04-25.md for live promotion instructions."

Then pack into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`; upserts §C in-place):
`python scripts/pack_daily.py --section C --source {YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md --status "{N}/7 retrieved"`

Exit summary (one line): `Meta-additions shadow {YYYY-MM-DD} — {N}/7 variables retrieved, {N} MISSING, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §C`

Then git add -A, commit with message "routine: preflight-meta-additions {today}", and push to origin main.