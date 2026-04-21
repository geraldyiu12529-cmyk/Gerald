---
name: Residual-momentum pipeline defect + fix (2026-04-17)
description: Two compounding defects caused all 12 single-stock T-scores to read INC on 2026-04-17; root cause + fix + implications for the 2026-10-14 audit demote decision.
type: project
originSessionId: 0dbee8fb-33f6-4afe-a752-3e76c01fcb9e
---
## The defect — 2026-04-17

Residual-momentum (Methodology §Step 3 equity T-input) read MISSING for all 12 single stocks. The staging file's surface error was "SPY column not found in stock returns (needed for market-model)" — the fallback path's message. But two compounding bugs were at play, and the surface error masked the upstream one.

**Bug 1 — primary FF5 path silently fell through.** `compute_residual_momentum()` in `scripts/compute_audit_additions.py` required `len(parts) >= 7` on every FF5 row (Date + 5 factors + RF). The cached `ff5_factors.csv` had only 6 columns (`date,Mkt-RF,SMB,HML,RMW,CMA` — no RF). So `ff5_data` stayed empty → primary failed with "Insufficient FF5 factor data: 0 months" → script silently promoted the market-model fallback.

**Bug 2 — fallback had no SPY to regress on.** `compute_residual_momentum_fallback_market_model()` required an SPY column in `stock_returns.csv`. The cached file had 13 columns (date + 12 single stocks), no SPY. `create_stock_returns_template()` in `fetch_ff5_from_french_library.py` had never included SPY in its header. So the fallback failed immediately on the SPY check — and because the primary had already failed silently, the whole variable read MISSING.

## The fix (this session, 2026-04-17)

1. **FF5 parser tolerates 6-col input.** `compute_audit_additions.py` now accepts 6-column FF5 files and synthesizes RF=0 (RF is ~0.3-0.4%/month, residual-momentum accuracy cost is small, avoids silent fall-through).
2. **SPY added to stock-returns pipeline.** `fetch_ff5_from_french_library.py` gained `fetch_stock_returns_from_yahoo()` which pulls 14mo of monthly returns for SPY + the 12 single stocks directly from Yahoo `/v8/finance/chart`, writes the working dir and the persistent cache. `create_stock_returns_template()` header also includes SPY. `main()` calls the Yahoo fetcher unconditionally (keeps cache fresh). `DATA_DIR` is now env-var-overridable (`AUDIT_DATA_DIR`) so tests and alt sessions don't collide with `/tmp/audit-data/` ownership.
3. **Market-model fallback defensive.** If `stock_returns.csv` is missing SPY at runtime, `compute_residual_momentum_fallback_market_model()` now fetches SPY monthly returns directly from Yahoo via `_fetch_spy_monthly_returns()` before giving up — belt-and-suspenders for days when the upstream fetcher didn't run.

## Prevention layers (six, all landed 2026-04-17)

After the fix, built out a defense-in-depth stack so the same defect class can't re-hide:

| # | Layer | File | Purpose |
|---|---|---|---|
| 1 | Schema canary | `scripts/preflight_health_check.py` — `_check_data_contract()` | Pre-flight check at 19:45 validates SPY + ≥6-col FF5. Flags SCHEMA VIOLATION in `.pipeline-health.json` advisories ahead of compute. |
| 2 | Chain-attempts surfacing | `scripts/compute_audit_additions.py` — `chain_attempts` list → `write_staging_file` | Staging file now renders every path's outcome under the MISSING block. Root cause visible, not just last-tried-path error. |
| 3 | Fail-loud write gate | `scripts/cache_manager.py` — `BULK_CACHE_SCHEMAS` + `SchemaViolation` | `write_bulk_cache` refuses stock_returns without SPY or FF5 with <6 cols. Fetcher fails at write site, not at compute consumer. |
| 4 | Read-time signature check | `scripts/cache_manager.py` — schema stamping in sidecar | Cache sidecar carries `cols_hash` + `schema_version`. `read_bulk_cache` recomputes and returns None on mismatch, forcing re-fetch rather than serving stale incompatible shape. |
| 5 | Regression test | `scripts/test_data_contract.py` | 26 checks across 4 test blocks (Yahoo fetcher shape, canary flag/pass, end-to-end residual compute, schema stamping). Run: `AUDIT_DATA_DIR=... python3 test_data_contract.py`. All 26 pass 2026-04-17. |
| 6 | Uptime tracker + drift detection | `audit-data-missing-tracker.md` + `compute_audit_additions._append_missing_tracker()` + RM1 patch for pipeline-recovery | Per-run LIVE/FALLBACK/MISSING state for each audit variable. RM1 (pending manual paste — skill mount ro) adds ≥2-day MISSING detection in pipeline-recovery Step 4f with Memory.md escalation at 3-day streak. |

Verified 2026-04-17: regenerated cache via new Yahoo fetcher, re-ran compute, staging file now populates all 12 single-stock T-scores. Test suite 26/26 green. Schema gate actively rejects bad content in-flight. Tracker seeded with today's LIVE row.

**Why:** This is Methodology §Step 3-binding. Raw TSMOM is explicitly not authoritative for single stocks — residual is the T-input. Without the fix every candidate like GOOGL (S+1/C+1/R0 = +2 without T) was blocked from |Sum|≥3 promotion by the fail-loud rule.

**How to apply:** If residual-mom reads MISSING again, first check whether `ff5_factors.csv` has ≥6 cols and `stock_returns.csv` has an SPY column. If either is off, the fetcher (`fetch_ff5_from_french_library.py`) didn't run or the French library returned truncated data. The market-model fallback will now auto-recover via Yahoo when SPY is absent.

## Downstream flag — denominator for the 2026-10-14 demote decision

The methodology note says residual-mom demotes to Grade B if "no decision-moving contribution by 2026-10-14." With this pipeline history:
- 2026-04-15: staging ran but 10-month window → near-zero residuals (unusable)
- 2026-04-16: clean
- 2026-04-17: MISSING (this defect)

Residual-mom was usable 1 day in 3, vs ~100% for intermediary capital and basis-momentum. Raw "decision-moving contributions" count is a flawed denominator if pipeline uptime is uneven — it would punish a good variable for a bad pipeline.

**Normalize the demote decision by opportunities observed.** Denominator = days the variable was actually LIVE (both cached files present, both parsers succeeded, regression produced non-zero residuals), not total review-window days. Track this in the audit-data-missing-tracker so the 2026-10-14 review has the normalized numerator/denominator ready.

Between now and 2026-10-14, the new Yahoo fetcher should keep denominator uptime ≥95%. If uptime still lags — that's the pipeline to fix, not a signal to demote the variable.
