---
name: setup-claude-code-routines
description: Reference guide: all 17 Claude Code trading routine configs for manual creation at claude.ai/code/routines
---


# Claude Code Routine Setup Guide — Gerald's Trading System

**Purpose:** Output the full configuration for all 17 trading routines so Gerald can create them at claude.ai/code/routines. Run this task, then copy-paste each config into the web UI.

**Repo:** https://github.com/geraldyiu12529-cmyk/Gerald (private, branch: main)
**Workspace subdirectory:** All content lives in `Trade/` inside the repo root. Every routine prompt begins with navigation to that directory.

---

## STEP 1 — Prerequisites (do these before creating any routines)

1. **GitHub repo settings:** Enable "Allow unrestricted branch pushes" so routines can push directly to `main` instead of creating `claude/*` branches. Without this, the daily pipeline chain breaks — each routine must see the prior routine's committed output.

2. **Create environment** at claude.ai/code → Environments → New:
   - Name: `trading-system-env`
   - Setup script: `pip install openpyxl requests pandas numpy`
   - Network: Trusted (required for WebSearch data pulls)
   - Leave API key fields blank unless you add FRED/Barchart keys later
   - Apply this environment to ALL routines below

3. **Plan tier check:** Max plan (15/day) or higher is required to run all 8 daily routines in the cloud. If on Pro (5/day cap), keep `us-close-snapshot`, `positions-monitor`, and `preflight-meta-additions` as local Desktop scheduled tasks and cloud-route only the core 5 daily routines.

4. **Cron timezone:** All cron expressions below are in your LOCAL time (UTC+8). The web UI scheduler uses local time — do not convert to UTC.

---

## STEP 2 — Create the 17 routines

### DAILY ROUTINES — Mon–Fri

---

#### Routine 1: us-close-snapshot-730am-v2
- **Model:** haiku
- **Cron (UTC+8 local):** `30 7 * * 1-5`
- **Prompt:**
```
CRITICAL: This is a utility task. Do NOT follow CLAUDE.md Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, or Data Sources.md. Only read Memory.md §2 Open Positions and the latest market-brief-*.md file.

cd Trade/

For each open position listed in Memory.md §2: pull US previous-day close price and any after-hours earnings reaction via WebSearch. Write us-close-snapshot-{TODAY}.md with mark-to-market values, any >1σ ATR moves flagged, and AH earnings notes. Update .pipeline-status.json with task completion status.

Then: git add -A && git commit -m "routine: us-close-snapshot {TODAY}" && git push origin HEAD:main
```

---

#### Routine 2: positions-monitor-intraday-9am
- **Model:** sonnet
- **Cron (UTC+8 local):** `0 9 * * 1-5`
- **Prompt:**
```
cd Trade/

Use the positions-monitor skill. Silent-when-OK — produce output only if position drift, stop breach, or watchlist trigger is detected. If all positions are within normal parameters, write a one-line OK status to .pipeline-status.json and exit. Do not write a dated output file on a silent run.

Commit only if there is something to commit (prevents empty-commit spam on silent-OK days):
git add -A && git diff --cached --quiet || (git commit -m "routine: positions-monitor {TODAY}" && git push origin HEAD:main)
```

---

#### Routine 3: preflight-audit-data-1945pm
- **Model:** sonnet
- **Cron (UTC+8 local):** `45 19 * * 1-5`
- **Prompt:**
```
CRITICAL: This is a data pipeline task. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, or Risk Rules.md. Only read Data Sources.md and .pipeline-health.json (if present).

cd Trade/

Phase 1 — source health check: Run `python scripts/pipeline_status.py` (or equivalent) to test connectivity for each data source in Data Sources.md. Write .pipeline-health.json with per-source availability, cache coverage, and any advisories.

Phase 2 — audit-addition compute: Run `python scripts/compute_audit_additions.py` to produce audit-data-staging-{TODAY}.md with:
  - Residual momentum (12m FF5-residualized) for all 12 equities — T-scores and raw TSMOM
  - Intermediary capital ratio (NY Fed PD z-score) — current ratio, z-score, R-adjustment
  - Basis-momentum (4w/12w F1-F2 change) for 5 commodities (Brent, WTI, Gold, Silver, Copper)

Use 4-tier retrieval per Data Sources.md: Tier 1 HTTP → Tier 2 WebSearch → Tier 3 cache → Tier 4 MISSING/fail-loud. If a variable fails all 4 tiers, mark as MISSING and state which score leg it blocks.

Phase 3 — tracker update: Append one row to audit-data-missing-tracker.md per the RM1 protocol: Date, ResidMom status, ResidMom_OK_stocks count, InterCap status, BasisMom status, BasisMom_OK_cmdty count, Notes.

Then: git add -A && git commit -m "routine: preflight-audit-data {TODAY}" && git push origin HEAD:main
```

---

#### Routine 4: preflight-meta-additions-1952pm
- **Model:** sonnet
- **Cron (UTC+8 local):** `52 19 * * 1-5`
- **Prompt:**
```
cd Trade/

SHADOW MODE — V029–V035 meta-integration compute. Do NOT feed results into market-brief or trade-rec. This is a parallel monitoring run only.

Run `python scripts/compute_meta_additions.py` to produce meta-additions-staging-{TODAY}.md with shadow-mode scores for: V029 BAB (Betting Against Beta), V030 DealerGamma, V031 GP/A (Gross Profitability), V032 CEI (Composite Equity Issuance), V033–V035 Faber TAA (3-month, 10-month, cross-asset momentum). 

Log each variable's LIVE/MISSING status to AuditAdditionLog sheet of master-data-log.xlsx with Type=SHADOW.

Shadow mode remains active until the 2026-04-25 meta-shadow-mode-review GO/NO-GO. After a GO verdict, Phase 3 SKILL.md patches promote these to live scoring.

Then: git add -A && git commit -m "routine: preflight-meta-additions {TODAY}" && git push origin HEAD:main
```

---

#### Routine 5: daily-market-brief-8pm-v2
- **Model:** sonnet
- **Cron (UTC+8 local):** `0 20 * * 1-5`
- **Prompt:**
```
cd Trade/

Use the market-brief skill. Read audit-data-staging-{TODAY}.md first — if the file is missing, fail-loud and abort (do not produce a brief from stale data). The brief must incorporate all three audit-addition variable scores (residual-mom T-scores, intermediary-capital R-overlay, basis-momentum S-input) per the 2026-04-14 audit-addition rules in CLAUDE.md.

Then: git add -A && git commit -m "routine: market-brief {TODAY}" && git push origin HEAD:main
```

---

#### Routine 6: daily-news-events-8pm-v2
- **Model:** sonnet
- **Cron (UTC+8 local):** `0 20 * * 1-5`
- **Prompt:**
```
cd Trade/

Use the news-events skill. Capture geopolitics, macro surprises, earnings, and catalyst events for the day. Update the catalysts cache via scripts/catalysts_cache.py if new catalyst tags are identified.

Then: git add -A && git commit -m "routine: news-events {TODAY}" && git push origin HEAD:main
```

---

#### Routine 7: daily-trade-recommendation-820pm-v2
- **Model:** opus
- **Cron (UTC+8 local):** `0 21 * * 1-5`
- **Prompt:**
```
cd Trade/

INTEGRITY PRE-CHECK: Before running Step 0 delta-check, verify that market-brief-{TODAY}.md EXISTS as a non-empty file. If the file does not exist, abort and write a one-line failure note to .pipeline-status.json — do not fall through to the delta-check which would silently carry forward the prior rec.

Use the daily-trade-rec skill. This task touches live capital — follow the 8-step methodology in Methodology Prompt.md exactly. Do not skip steps. Fail-loud on any missing Grade A variable (state which leg it blocks). The SignalLedger append is append-only — never delete or overwrite existing rows.

Then: git add -A && git commit -m "routine: trade-rec {TODAY}" && git push origin HEAD:main
If Memory.md or .pipeline-status.json were updated but no new trade-rec was produced (delta-check triggered): still commit + push those updates.
```

---

#### Routine 8: pipeline-recovery-830pm
- **Model:** haiku
- **Cron (UTC+8 local):** `0 22 * * 1-5`
- **Prompt:**
```
cd Trade/

Use the pipeline-recovery skill. Phase A (fast triage, target <3K tokens): read .pipeline-status.json and check file sizes for today's expected outputs (market-brief, news, trade-rec, audit-data-staging). If all files present and above MIN_SIZES, log "healthy" to .pipeline-status.json and exit — no further work.

Phase B (recovery, runs only if Phase A flags unhealthy): produce cache-backed skeleton files for any missing output. Check audit-addition drift per RM1: read the last 3 rows of audit-data-missing-tracker.md; WARNING if any variable has ≥2 consecutive MISSING, CRITICAL (→ Memory.md alert) if ≥3. Excel sync check (read-only). Recovery-brief structural validation. Self-watchdog in_progress marker.

Commit + push only if files were created or Memory.md was updated:
git add -A && git commit -m "routine: pipeline-recovery {TODAY}" && git push origin HEAD:main
```

---

### WEEKLY ROUTINES — Sunday

---

#### Routine 9: weekly-regime-signal-review-6pm
- **Model:** opus
- **Cron (UTC+8 local):** `0 18 * * 0`
- **Prompt:**
```
cd Trade/

Phase 1 — weekly regime review: Read Memory.md, the latest market-brief-*.md, and all news-events/news-*.md files from the past 7 days. Write weekly-review-{TODAY}.md covering: regime trajectory vs prior week, key macro/geopolitical events, thesis validation for open positions, lessons. Condense any new entries in memory-lessons.md (deduplicate, sharpen wording, remove entries that have been absorbed into methodology).

Phase 2 — signal review: Use the signal-review skill. Produces signal-review-{TODAY}.md and report-{TODAY}-signal-review.html. Appends OOS performance metrics to PerformanceStats sheet of master-data-log.xlsx (append-only).

Then: git add -A && git commit -m "routine: weekly-review+signal-review {TODAY}" && git push origin HEAD:main
```

---

#### Routine 10: workspace-tidy-sunday-9pm
- **Model:** haiku
- **Cron (UTC+8 local):** `0 21 * * 0`
- **Prompt:**
```
CRITICAL: This is a utility task. Do NOT follow CLAUDE.md Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, or Data Sources.md.

cd Trade/

Apply Retention Policy.md: move files aged 8+ days to archive/YYYY-MM/; digest files aged 31+ days per the tiering rules. Respect Memory.md pinned files — do not move or delete anything pinned.

Run diagnostics and append to archive/cleanup-log.md:
- Excel integrity: verify master-data-log.xlsx opens and has 10 sheets (SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes, CatalystLog, README)
- Pipeline liveness: check .pipeline-status.json — last successful run for each of the 7 daily tasks
- Output continuity: are there dated output files for each weekday in the past 5 business days?
- Cache health: list .data-cache/ files with staleness classification per Data Sources.md
- Skill presence: verify .claude/skills/ contains 10 project-scope skills (no consolidate-memory)

Then: git add -A && git commit -m "routine: workspace-tidy {TODAY}" && git push origin HEAD:main
```

---

### QUARTERLY / SEMI-ANNUAL / MONTHLY

---

#### Routine 11: quarterly-methodology-review
- **Model:** opus
- **Cron (UTC+8 local):** `0 19 1 1,4,7,10 *`
- **Prompt:**
```
cd Trade/

Use the quarterly-methodology-review skill. This fires on the 1st of January, April, July, October. Review: Top-28 variable performance over the quarter, methodology dimension audit, variable pipeline (candidates from literature-review → promotion criteria), AuditAdditionLog trends, VariableRegistry reconciliation.

The 2026-10-14 methodology-audit-6mo-review-2026-10-14 one-time routine also feeds into this quarterly's October run — read its output if present.

Then: git add -A && git commit -m "routine: quarterly-methodology-review {TODAY}" && git push origin HEAD:main
```

---

#### Routine 12: semi-annual-literature-review
- **Model:** opus
- **Cron (UTC+8 local):** `0 15 1 1,7 *`
- **Prompt:**
```
cd Trade/

Use the literature-review skill. Fires 1st of January and July. Systematic academic factor scan: search recent papers (past 6 months) for new tradeable variables meeting 5-criteria screens (replication, mechanism, data availability, cost, orthogonality to existing Top-28). Output feeds the quarterly-methodology-review candidate pipeline.

Then: git add -A && git commit -m "routine: semi-annual-literature-review {TODAY}" && git push origin HEAD:main
```

---

#### Routine 13: system-review-semi-annual
- **Model:** opus
- **Cron (UTC+8 local):** `0 19 1-7 5,11 0`
- **Prompt:**
```
cd Trade/

CRON GUARD: This routine should fire only on the FIRST Sunday of May and November. Today's date is {TODAY}. If day-of-month > 7 or month is not May or November, exit silently with no action (cron OR-semantics safeguard).

Use the system-review skill. Strategic architecture + efficiency audit: skill performance, token usage patterns, pipeline reliability, methodology fitness, any structural changes needed. Chain the skill-creator for patches if architectural changes are recommended.

Then: git add -A && git commit -m "routine: system-review {TODAY}" && git push origin HEAD:main
```
*Note: If the web UI cron fires under OR-semantics (every day 1–7 of May/Nov PLUS every Sunday of May/Nov), the in-prompt date guard above will catch and suppress misfires. Verify on first fire: expected 2026-05-03 19:00 UTC+8.*

---

#### Routine 14: monthly-bootstrap-review
- **Model:** sonnet
- **Cron (UTC+8 local):** `0 19 1 5,6 *`
- **Prompt:**
```
cd Trade/

Bootstrap health check — fires 1st of May and June 2026 only (auto-retires after).

If today's date >= 2026-07-01: print "auto-disable: bootstrap review window closed" and take no action. Gerald will disable this routine manually.

Otherwise: check whether all 17 routines have been firing correctly by reviewing git log for routine: commits over the past month. Report: which routines ran, which missed, any error patterns. Check that the 3-day parallel-run comparison (Cowork vs Claude Code) completed successfully. Note any remaining discrepancies for manual investigation.

Then: git add -A && git commit -m "routine: monthly-bootstrap-review {TODAY}" && git push origin HEAD:main
```

---

### ONE-TIME ROUTINES

---

#### Routine 15: meta-shadow-mode-review-2026-04-25
- **Model:** opus
- **Cron (UTC+8 local):** `0 10 25 4 *` — create this, then DISABLE immediately after it fires on 2026-04-25
- **Prompt:**
```
cd Trade/

One-time Phase 3 GO/NO-GO review for V029–V035 meta-integration variables.

Read all meta-additions-staging-*.md files from 2026-04-20 through 2026-04-24 (5 shadow-mode business days). For each of V029 BAB, V030 DealerGamma, V031 GP/A, V032 CEI, V033 Faber-3mo, V034 Faber-10mo, V035 Faber-cross:
- Contribution rate: how many days was the variable LIVE (not MISSING)?
- Decision-moving instances: how many times did it change a score leg?
- Verdict: PROMOTE to live (Phase 3 GO) if ≥80% LIVE and ≥1 decision-moving instance; HOLD in shadow if LIVE but not yet decision-moving; RETIRE if <50% LIVE.

Cross-check against deployment-memo-2026-04-18.md for each variable's expected behavior. Write meta-shadow-review-2026-04-25.md with per-variable verdict table and overall Phase 3 recommendation.

If overall verdict is GO: list the 5 Phase-3 SKILL.md patches (V029–V035) that must be applied. They are blocked in patches/ directory pending this review.

Then: git add -A && git commit -m "routine: meta-shadow-mode-review 2026-04-25" && git push origin HEAD:main
```
*After this fires on 2026-04-25, disable the routine in the web UI.*

---

#### Routine 16: methodology-audit-6mo-review-2026-10-14
- **Model:** opus
- **Cron (UTC+8 local):** `0 9 14 10 *` — create this, then DISABLE immediately after it fires on 2026-10-14
- **Prompt:**
```
cd Trade/

Six-month live-monitoring review of the 3 original audit-addition variables (first valued 2026-04-14/15). Review window: 2026-04-14 through 2026-10-13 (approximately 130 trading days).

Read:
- audit-data-missing-tracker.md — tally LIVE rows per variable (uptime denominator = LIVE rows only, per Methodology §Audit-Addition Review)
- AuditAdditionLog sheet of master-data-log.xlsx — decision-moving contributions
- The most recent quarterly-methodology-review output

For each variable (residual_momentum, intermediary_capital, basis_momentum):
- Days LIVE in review window (from tracker)
- Decision-moving contributions (from AuditAdditionLog)
- Contribution rate = decision_moving_rows / LIVE_rows (not calendar days)
- Uptime pct = LIVE_rows / total_rows (pipeline health signal)

Verdict per variable: KEEP Grade A (uptime ≥70%, contribution rate meets threshold) / DEMOTE to Grade B / REMOVE from pipeline.

Write methodology-audit-6mo-review-2026-10-14.md with full tables and verdict. This output feeds the October quarterly-methodology-review.

Then: git add -A && git commit -m "routine: methodology-audit-6mo-review 2026-10-14" && git push origin HEAD:main
```
*After this fires on 2026-10-14, disable the routine in the web UI.*

---

#### Routine 17: methodology-audit-6mo-review-batch2-2026-10-14
- **Model:** opus
- **Cron (UTC+8 local):** `30 9 14 10 *` — fires 30 minutes after Routine 16 on the same day
- **Prompt:**
```
cd Trade/

Batch-2 companion to methodology-audit-6mo-review-2026-10-14 (runs 30 min later). Reviews V029–V035 meta-integration variables added 2026-04-18 (approximately 6 months of shadow + live data).

Read:
- All meta-additions-staging-*.md files from 2026-04-18 through 2026-10-13
- AuditAdditionLog sheet (Type=SHADOW pre-GO, Type=LIVE post-GO)
- meta-shadow-review-2026-04-25.md (the Phase 3 GO/NO-GO decision)

For each of V029–V035:
- Shadow period uptime (pre-2026-04-25 GO date)
- Live period uptime (post-GO, if promoted)
- Decision-moving contributions in live period
- Verdict: KEEP Grade A / DEMOTE to B / REMOVE

Write methodology-audit-6mo-review-batch2-2026-10-14.md.

Then: git add -A && git commit -m "routine: methodology-audit-6mo-review-batch2 2026-10-14" && git push origin HEAD:main
```
*After this fires on 2026-10-14, disable the routine in the web UI.*

---

## STEP 3 — Verify one routine end-to-end

After creating all 17 routines, test `preflight-audit-data-1945pm` first (lowest risk):

1. Click **Run now** in the web UI
2. Watch the session — confirm it clones the repo, runs the compute, writes audit-data-staging-{TODAY}.md and .pipeline-health.json, commits, and pushes to main
3. On your local machine: `git pull origin main` and verify the new files appear
4. If any step fails, investigate before activating the remaining routines

## STEP 4 — Parallel-run period (3 business days)

Keep Cowork scheduled tasks enabled. Each day, compare Cowork vs Claude Code outputs. Expected: identical or near-identical. Discrepancies → stop and investigate before Cowork cutover (~2026-04-24).

## Summary table

| # | Task ID | Model | Cron (UTC+8) | Type |
|---|---------|-------|--------------|------|
| 1 | us-close-snapshot-730am-v2 | haiku | `30 7 * * 1-5` | daily |
| 2 | positions-monitor-intraday-9am | sonnet | `0 9 * * 1-5` | daily |
| 3 | preflight-audit-data-1945pm | sonnet | `45 19 * * 1-5` | daily |
| 4 | preflight-meta-additions-1952pm | sonnet | `52 19 * * 1-5` | daily |
| 5 | daily-market-brief-8pm-v2 | sonnet | `0 20 * * 1-5` | daily |
| 6 | daily-news-events-8pm-v2 | sonnet | `0 20 * * 1-5` | daily |
| 7 | daily-trade-recommendation-820pm-v2 | opus | `0 21 * * 1-5` | daily |
| 8 | pipeline-recovery-830pm | haiku | `0 22 * * 1-5` | daily |
| 9 | weekly-regime-signal-review-6pm | opus | `0 18 * * 0` | weekly |
| 10 | workspace-tidy-sunday-9pm | haiku | `0 21 * * 0` | weekly |
| 11 | quarterly-methodology-review | opus | `0 19 1 1,4,7,10 *` | quarterly |
| 12 | semi-annual-literature-review | opus | `0 15 1 1,7 *` | semi-annual |
| 13 | system-review-semi-annual | opus | `0 19 1-7 5,11 0` | semi-annual |
| 14 | monthly-bootstrap-review | sonnet | `0 19 1 5,6 *` | monthly (temp) |
| 15 | meta-shadow-mode-review-2026-04-25 | opus | `0 10 25 4 *` (one-time, disable after) | one-time |
| 16 | methodology-audit-6mo-review-2026-10-14 | opus | `0 9 14 10 *` (one-time, disable after) | one-time |
| 17 | methodology-audit-6mo-review-batch2-2026-10-14 | opus | `30 9 14 10 *` (one-time, disable after) | one-time |
