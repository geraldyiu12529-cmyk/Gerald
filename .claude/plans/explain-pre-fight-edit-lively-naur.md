# Plan: Evaluate preflight-audit-data vs preflight-meta-additions

## Context

Two scheduled tasks both fire nightly before the main pipeline. The question is whether they
are distinct enough to justify separate tasks, or whether one should be merged, simplified, or
deleted. This is an architectural efficiency review — no user-facing output changes needed.

---

## What each task does

### preflight-audit-data (19:45 UTC+8)
**Location:** `/c/Users/Lokis/.claude/scheduled-tasks/preflight-audit-data/SKILL.md`
**Script:** `scripts/compute_audit_additions.py`

- **Phase 1:** HTTP ping sweep of 7 data sources → writes `.pipeline-health.json`
- **Phase 2:** 4-tier retrieval of 3 Grade A audit-addition variables:
  1. Residual momentum (12m FF5-residualized) → equity T-input
  2. Intermediary capital ratio (NY Fed PD z-score) → cross-asset R-overlay
  3. Basis-momentum (4w/12w F1–F2 slope) → commodity S-input
- Writes `{YYYY-MM-DD}/audit-data-staging-{date}.md`
- Writes `.pipeline-status.json` with OK/PARTIAL/FAIL
- Packs §B of `daily-{date}.md`
- **LIVE:** market-brief Step 0 consumes `audit-data-staging` directly. Failure here = broken brief + broken trade-rec.

### preflight-meta-additions (19:52 UTC+8)
**Location:** `/c/Users/Lokis/.claude/scheduled-tasks/preflight-meta-additions/SKILL.md`
**Script:** `scripts/compute_meta_additions.py`

- Computes 7 shadow variables V029–V035 (BAB, DealerGamma, GP/A, CEI, Faber TAA)
- Writes `{YYYY-MM-DD}/meta-additions-staging-{date}.md`
- Logs status to `master-data-log.xlsx` AuditAdditionLog sheet (Type=SHADOW)
- Packs §C of `daily-{date}.md`
- **SHADOW MODE ONLY:** explicitly blocked from feeding market-brief or trade-rec until 2026-04-25 shadow review decides Phase 3 GO/NO-GO per variable.

---

## Are they the same thing?

No. They have fundamentally different roles:

| Dimension | preflight-audit-data | preflight-meta-additions |
|---|---|---|
| Variables | V027/V028/V003 (3 Grade A, live) | V029–V035 (7 candidates, shadow) |
| Downstream consumers | market-brief, trade-rec (LIVE) | None until Phase 3 |
| Failure consequence | Pipeline FAIL → bad trade rec | No downstream impact |
| Status written | pipeline-status.json (triggers recovery) | Not written to pipeline-status |
| Lifecycle | Permanent (unless demoted Oct 2026) | Temporary: retires or merges Apr 2026 |
| Purpose | Data reliability gate | Shadow validation window |

---

## Verdict: LEAVE SEPARATE (with a future merge path)

**Justification:**

1. **Failure isolation is architecturally critical.** If meta-additions compute fails (e.g. Yahoo fetch error on BAB), that must never pollute the live pipeline-status.json that drives recovery logic. Merging them collapses this boundary.

2. **The shadow/live distinction is intentional and load-bearing.** The entire point of preflight-meta-additions is that it runs in parallel to the live pipeline without touching it. This is the Phase 2 → Phase 3 gate mechanism. Merging defeats the purpose.

3. **The task is self-expiring.** After 2026-04-25 shadow review:
   - **GO verdict per variable:** that variable's compute migrates into `compute_audit_additions.py` + audit-data task. `preflight-meta-additions` shrinks or retires.
   - **NO-GO verdict:** the shadow task retires cleanly with no surgery on the live task.
   - Keeping them separate makes both outcomes simple to execute.

4. **No meaningful duplication exists today.** Phase 1 (health check) runs only in audit-data; meta-additions does not re-run it. The two Python scripts are distinct. The 7-minute gap is intentional dependency ordering. There is nothing to collapse.

5. **Token / compute cost is negligible.** Each task is a short compute-only run (~2K tokens). The overhead of two tasks vs one is irrelevant compared to the architectural clarity gained.

---

## What to do now: Nothing

Both tasks are correctly scoped and correctly isolated. No merge, no delete, no restructure.

**One future action to schedule (post-2026-04-25):**

After the shadow review on 2026-04-25:
- For each GO variable: move its compute function from `compute_meta_additions.py` into `compute_audit_additions.py`, extend `audit-data-staging` format to include it, update market-brief Step 0 to read and score it.
- Once all GO/NO-GO decisions are applied, retire or archive `preflight-meta-additions` task.
- If all 7 are NO-GO: delete `compute_meta_additions.py` and the scheduled task.

This plan requires no code changes today. The architecture is correct as-is.

---

## Verification (if any future merge/retire is executed)

1. Run `preflight-audit-data` manually → confirm `audit-data-staging-{date}.md` written and non-empty
2. Run `market-brief` → confirm audit additions appear in S/T/C/R scoring
3. Confirm `.pipeline-status.json` shows `preflight: OK`
4. Confirm `meta-additions-staging-{date}.md` is either absent (retired) or present (shadow still active)
5. Check `master-data-log.xlsx` AuditAdditionLog — no SHADOW rows written after retire
