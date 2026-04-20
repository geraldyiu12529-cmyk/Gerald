# Audit-Addition Uptime Tracker

**Purpose.** Feeds the 2026-10-14 six-month demote decision with a normalized
denominator: "residual-mom was LIVE X of Y review-window days," not raw
"decision-moving contributions out of calendar days."

**Normalization rule (Methodology §Audit-Addition Review).** Pipeline downtime
should not be charged against the variable. The demote test is:
    uptime_pct = LIVE_rows / total_rows for the variable in the review window
    decision_hit_pct = decision_moving_rows / LIVE_rows
Compute `decision_hit_pct` over LIVE rows only. If a variable has low uptime,
that's a pipeline issue, not a variable-quality issue — fix the pipeline first,
then re-measure over the NEXT window.

**Columns.**
- `Date` — absolute date (YYYY-MM-DD), append-only, one row per compute run
- `ResidMom` — `LIVE` (primary FF5 path OK) / `FALLBACK` (market-model fallback OK)
  / `MISSING` (both paths failed). Only `LIVE` counts toward uptime; fallback is
  a partial-credit state flagged but not counted as full uptime because residuals
  are directional, not FF5-grade.
- `ResidMom_OK_stocks` — count of single stocks with OK T-score (of 12)
- `InterCap` — `LIVE` / `MISSING`
- `BasisMom` — `LIVE` / `MISSING`
- `BasisMom_OK_cmdty` — count of commodities with computed basis-mom (of 5)
- `Notes` — short failure mode tag if any leg was MISSING

**How to use.**
- `quarterly-methodology-review` and the 2026-10-14 audit-addition review read
  this file and tally `LIVE_rows` per variable.
- `pipeline-recovery` watches for ≥2 consecutive MISSING rows per variable to
  flag pipeline drift early.

---

## Log

| Date | ResidMom | ResidMom_OK_stocks | InterCap | BasisMom | BasisMom_OK_cmdty | Notes |
|------|----------|---------------------|----------|----------|-------------------|-------|
| 2026-04-17 | LIVE | 12/12 | LIVE | LIVE | 5/5 |  |
| 2026-04-19 | LIVE | 12/12 | LIVE | LIVE | 5/5 | weekend-test; Tier 3 cache; InterCap STALE-WARN (data through 2026-04-04) |
| 2026-04-20 | MISSING | 0/12 | MISSING | LIVE | 1/5 | residmom-missing:numpy not available (market-model fallba; intercap-missing:numpy not available for z-score computat |
