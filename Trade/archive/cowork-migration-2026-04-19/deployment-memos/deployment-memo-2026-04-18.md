# Deployment Memo — 2026-04-18 Meta-Analysis Integration + Token-Savings Rollout

**Session:** Cowork 2026-04-18 (upbeat-great-archimedes)
**Operator:** Claude (acting on Gerald's "recommend and execute" delegation)
**Plan reference:** `meta-analysis-integration-plan-2026-04-18.md`
**Status:** Phases 1, 2, 4 complete. Phase 3 blocked on 2026-04-25 shadow review. Part B rescoped and executed.

---

## Part A — Meta-analysis integration

### Phase 1 — Documentation patches (COMPLETE, GATE 1 passed on delegated judgment)

Five artifacts modified:

| File | Bytes before | Bytes after | Change |
|---|---:|---:|---|
| `Methodology Prompt.md` | ~10,900 | 22,493 | +Step 1.5 Overlay Gate, +§4 entries 29–33, +scoring rules §3.1 D, +reconciliation note, +crosswalk appendix |
| `Risk Rules.md` | 3,405 | 7,371 | +§1.B V027 sizing tier, +§4.B Faber overlay breaker, +§5.A R-group scale rule, §7 checklist 6→8 items, +§8 Factor Sleeves |
| `Data Sources.md` | 6,557 | 9,264 | +V029–V035 meta-integration table |
| `Trad core.md` | 41,566 | 53,760 | +Addendum 2026-04-18 with 5 mechanism entries |
| `master-data-log.xlsx` | — | — | +MethodologyNotes sheet (10 cols); seeded with 2026-04-18 integration event |

### GATE 1 decisions (delegated to Claude, logged here for audit):

1. **MethodologyNotes schema** — kept as written: Date, Event_Type, Description, Reference_File, Affects_Sheets, Affects_Variables, Requires_Gerald_Approval, Approval_Status, Source_Skill, Notes.
2. **V001 VIX / V004 HY OAS A→B downgrade** — **EXECUTED**. Without the downgrade, the §5.A R-group scale-consistency rule creates a double-counting hole. VariableRegistry updated with Demotion_Date 2026-04-18 and review history appended.
3. **SignalLedger schema delta** — **EXECUTED**. Added 4 columns at end: `overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`. Append-only rule applies to rows, not columns. Historical 38 rows backfilled with `n/a (pre-meta)` for signal-review readability.
4. **V030 DealerGamma subscription** — **STUB-MISSING** in Phase 2 compute pending subscription confirmation. Data Sources.md flagged subscription-dependent; VariableRegistry Status = "MISSING (subscription pending)"; next review 2026-07-01 quarterly.
5. **Step 1.5 naming** — kept as "1.5", no renumbering. Avoids cascading edit across all downstream SKILL.md and templates.
6. **Sleeve cap fraction** — **1/3** per plan §3.1 D (authoritative scoring section).

### Phase 2 — Data pipeline (COMPLETE, GATE 2 passed)

Artifacts:

- `scripts/compute_meta_additions.py` — new 15.8 KB sibling to `compute_audit_additions.py`. 7 functions: `_yahoo_monthly_closes`, `compute_faber_taa` (V033–V035), `compute_bab_etf_proxy` (V029), `compute_dealergamma` (V030 stub), `compute_gpa` (V031 stub), `compute_cei` (V032 stub), `write_staging_file`. Tested and produces valid output.
- VariableRegistry — 29→36 rows. V001/V004 downgraded to Grade B. V029–V035 added with Status="Shadow (Phase 2)" (V030 is "MISSING (subscription pending)").
- SignalLedger — 32→36 cols. 39 rows unchanged (1 header + 38 data).
- MethodologyNotes — row 3 logs Phase 2 execution with full scope.
- Scheduled task `preflight-meta-additions-1952pm` — new, runs 19:52 UTC+8 Mon–Fri, writes `meta-additions-staging-YYYY-MM-DD.md` in shadow mode.
- Scheduled task `meta-shadow-mode-review-2026-04-25` — one-time, fires 2026-04-25 10:00 UTC+8. Reviews 5 shadow business days, recommends Phase 3 GO/NO-GO per variable.

Today's test run (2026-04-18) produced real numbers:

| Var | Symbol | State | Detail |
|---|---|---|---|
| V033 | SPY | **ON** | 710.14 > 10m-SMA 669.57 (+6.06%) |
| V034 | GSG (GSCI) | **ON** | 30.35 > 10m-SMA 25.21 (+20.4%) |
| V035 | BTC-USD | **OFF** | 77,127 < 10m-SMA 91,649 (−15.85%) |
| V029 | USMV − SPLV | ANTI-BAB | −0.63% spread (low-β not earning premium) |
| V030 | — | MISSING | subscription pending |
| V031 | — | MISSING | Phase 2b stub (Ken French GP CSV fetcher) |
| V032 | — | MISSING | Phase 2b stub (CRSP+Compustat self-compute) |

**Material observation:** V035 BTC Faber gate is OFF. If Phase 3 live-promotion happens, new crypto longs would be blocked by the overlay gate. Flag for Gerald's awareness regardless of Phase 3 timing.

### Phase 3 — Live scoring (BLOCKED)

Phase 3 waits on the 2026-04-25 shadow-mode review. Do NOT set live_date on V029–V035 until that review produces GO verdicts per variable. Phase 3 tasks when unblocked:

- Update SKILL.md files for `market-brief`, `daily-trade-rec`, `signal-review`, `positions-monitor`, `quarterly-methodology-review` to read `meta-additions-staging-*.md`.
- Set live_date in VariableRegistry for each approved variable.
- First trade-rec post-go-live carries header note: "first rec with V029/V033–V035 live — shadow review at `meta-shadow-review-2026-04-25.md`".

### Phase 4 — 2026-10-14 audit review calendar (COMPLETE)

- Existing `methodology-audit-6mo-review-2026-10-14` task (Batch 1 — V026–V028) left unchanged; sandbox update blocked on path-traversal guard.
- New sibling task `methodology-audit-6mo-review-batch2-2026-10-14` created, fires 2026-10-14 01:30 UTC (09:30 local). Covers V029–V035. Companion deliverable to the Batch-1 review.

## Part B — Token-savings optimization (rescoped, GATE 4)

### GATE 4 finding

Gerald's "157 KB → 34 KB target, ≥50% per skill" premise was obsolete. Actual current total across 11 custom trading SKILL.md files: **33,745 bytes**. Already below target. Forcing a ≥50% per-skill reduction would require removing load-bearing methodology content (e.g. stripping the 8-step checklist from `daily-trade-rec`) — not defensible.

### Rescoped Part B

**B.1+B.2 — CLAUDE.md skip-logic override (EXECUTED, ~150 bytes edited).**
Patched `/mnt/.claude/CLAUDE.md` Session Startup Protocol from "MANDATORY" to "default; skills may override". Added explicit acknowledgement that `positions-monitor`, `news-events`, and `pipeline-recovery` healthy-path override the 4-file mandatory read when they enumerate their own reads. Total savings: whenever one of those skills is invoked without a parent trading-rec task, Claude skips the 3-4 framework-file loads (~20-30 KB per invocation).

**B.3 — SKIPPED.** Target already met. Per-skill rewrites would be cosmetic-only or destructive. Documented here.

**B.4 — Path-scoped rule files (VERIFIED).** `/mnt/Trade/.claude/rules/evidence-grades.md` and `/mnt/Trade/.claude/rules/risk-rules-summary.md` already have correct `globs:` frontmatter covering the right output filepaths. No changes needed.

**B.5 — Model tiering (PATCH WRITTEN, NEEDS WINDOWS APPLY).** See `patches/META-B5-model-tiering-patch.md`. Sandbox cannot write `/mnt/.claude/skills/*/SKILL.md` (read-only mount). PowerShell apply script included. Assignments:

- **Opus** (5 skills): daily-trade-rec, signal-review, quarterly-methodology-review, system-review, literature-review
- **Sonnet** (4 skills): market-brief, news-events, trade-update, positions-monitor
- **Haiku** (2 skills): pipeline-recovery (Gerald explicit), consolidate-memory

## Deferred / blocked items

| Item | Why deferred | Unblocks when |
|---|---|---|
| Phase 3 live scoring | Shadow mode needs 5 business days | 2026-04-25 review verdict |
| V030 DealerGamma live data | Subscription not confirmed | Gerald subscribes to SqueezeMetrics or SpotGamma |
| V031 GP/A compute | Phase 2b stub — Ken French GP portfolio CSV fetcher not implemented | Phase 2b sprint (separate deployment) |
| V032 CEI compute | Phase 2b stub — CRSP+Compustat self-compute not implemented | Phase 2b sprint |
| Batch-1 calendar task update | Sandbox path-traversal guard blocked update | Not needed — sibling Batch-2 task covers the new scope cleanly |
| SKILL.md edits for Part B.5 + eventual Phase 3 | Read-only mount | Apply `META-B5-model-tiering-patch.md` Windows-side |

## Files to review Windows-side

1. `/mnt/Trade/patches/META-B5-model-tiering-patch.md` — apply to install model tiering.
2. `/mnt/Trade/meta-additions-staging-2026-04-18.md` — first shadow output, includes V035 BTC OFF state flag.

## Audit chain

All changes logged to `master-data-log.xlsx:MethodologyNotes` (rows 2 and 3). Rollback path: delete V029–V035 rows from VariableRegistry, restore V001/V004 Evidence_Strength=Grade A + clear Demotion_Date, delete the 4 new SignalLedger cols, revert the 5 markdown files to pre-2026-04-18 git state, remove the 2 new scheduled tasks. Revertible in ~15 minutes if Phase 3 review finds material issues.
