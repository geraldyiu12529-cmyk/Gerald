# Claude Code — /schedule Prompts for All 16 Routines
# All times UTC+8 (Gerald's local timezone)
# Generated: 2026-04-19

---

## DAILY ROUTINES (Mon–Fri)

---

/schedule

Schedule this for every weekday at 7:30am

CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, or protocol documents.

Read ONLY: Memory.md §2 Open Positions and the latest market-brief-*.md.

For each open position, pull the US close price + any after-hours earnings reaction via WebSearch. Write us-close-snapshot-{today}.md with:
- Mark-to-market vs entry price and stop level
- Any moves >1σ ATR flagged
- After-hours earnings reactions if applicable

Update .pipeline-status.json entry for `us-close-snapshot`:
- status: OK if file written and >200 bytes, FAIL otherwise
- consecutive_failures: 0 on OK; increment from prior on non-OK

Exit summary (one line): `US close snapshot {YYYY-MM-DD} complete — {N} positions checked, {N} ATR alerts, status={OK|FAIL}`

Then git add -A, commit with message "routine: us-close-snapshot {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 9:00am

/positions-monitor

Then git add -A, commit with message "routine: positions-monitor {today}", and push to origin main. If the skill exited silently (no flags), the commit message should note "silent-OK".

---

/schedule

Schedule this for every weekday at 7:45pm

CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Memory.md, Risk Rules, or protocol documents.

Phase 1 — Pipeline health check:
Run scripts/preflight_health_check.py to test source connectivity and write .pipeline-health.json. Log any unreachable sources.

Check .pipeline-status.json for yesterday's entries:
- If any task shows consecutive_failures >= 3, print: "⚠ CONSECUTIVE FAILURE ALERT: {task} has failed {N} consecutive days. Investigate."
- If yesterday's market-brief status is FAIL/ABORT AND today's sources are healthy, print: "Recovery opportunity: yesterday's brief failed but sources are now reachable."

Phase 2 — Audit-addition compute:
Run scripts/compute_audit_additions.py to produce audit-data-staging-{today}.md. If compute fails, consult .data-cache/ for cached inputs within staleness windows per Data Sources.md §4-tier fallback and retry. Update audit-data-missing-tracker.md per RM1 protocol.

After both phases complete:
Verify .pipeline-health.json was written today. Verify audit-data-staging-{today}.md exists and is non-empty. Write preflight status to .pipeline-status.json (status: OK if both files written; PARTIAL if either missing). If either check fails, append "INTEGRITY FAIL: [filename] not produced" to the output summary.

Exit summary (one line): `Preflight {YYYY-MM-DD} complete — sources={OK|DEGRADED}, staging={OK|MISSING}, status={OK|PARTIAL|FAIL}`

Then git add -A, commit with message "routine: preflight-audit-data {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 7:52pm

CRITICAL: shadow mode only — do NOT feed results into market-brief or trade-rec.

Run scripts/compute_meta_additions.py to produce meta-additions-staging-{today}.md. The file covers seven shadow variables: V029 BAB (betting-against-beta), V030 DealerGamma, V031 GP/A (gross-profitability-to-assets), V032 CEI (composite equity issuance), V033–V035 Faber TAA signals.

For each variable, log status (RETRIEVED / MISSING / STALE) to AuditAdditionLog sheet in master-data-log.xlsx with Type=SHADOW. Do NOT promote to live scoring until the 2026-04-25 shadow review clears Phase 3.

If today's date >= 2026-04-25 and meta-shadow-review-2026-04-25.md contains PROMOTE verdicts for any variable, add a note: "Phase 3 GO/NO-GO complete — check meta-shadow-review-2026-04-25.md for live promotion instructions."

Exit summary (one line): `Meta-additions shadow {YYYY-MM-DD} — {N}/7 variables retrieved, {N} MISSING`

Then git add -A, commit with message "routine: preflight-meta-additions {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 8:00pm

Produce today's US pre-open market brief.

1. Follow CLAUDE.md §Session Startup Protocol (all four reads).
2. Load and run the `market-brief` skill end-to-end for today's local date (UTC+8).
   - Reads `audit-data-staging-{YYYY-MM-DD}.md` at Step 0
   - Reads `catalysts-cache-{YYYY-MM-DD}.json` at Step 5.5 if news wrote it
   - Pulls Grade A variables via data_retrieval_engine.fetch_many (4-tier fallback)
   - FAIL-LOUD on any MISSING Grade A variable — do NOT silently infer
   - Output: market-brief-{YYYY-MM-DD}.md (version tag v1 first run; v2/v3... on same-day re-runs)
   - Syncs DailyVariables, RegimeHistory, DataQuality, CatalystLog sheets in master-data-log.xlsx
3. After the brief file is written, update .pipeline-status.json:
   - status: OK if file exists and >500 bytes and <=3 MISSING Grade A; PARTIAL if >3 MISSING; FAIL if write failed
   - consecutive_failures: 0 on OK; increment from prior on non-OK
4. Exit summary (one line, required for pipeline-recovery sniff):
   `Market brief {YYYY-MM-DD} v{N} complete — regime={label}, MISSING Grade A={count}, status={OK|PARTIAL|FAIL}`

Then git add -A, commit with message "routine: market-brief {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 8:00pm

Capture today's daily news, geopolitics, macro releases, corporate earnings, crypto regulatory, and flash events.

1. Do NOT follow CLAUDE.md §Session Startup Protocol in full. Read ONLY: news-events/README.md (for the 12-category taxonomy and hotspot list).
2. Load and run the `news-events` skill end-to-end for today's local date (UTC+8).
   - Search by category (not by named conflict). Use hotspot list from README.
   - Cover all 12 categories: macro releases, central bank, geopolitics, equity earnings, crypto regulatory, commodity supply, FX policy, flash events, credit/rates, sector rotation, analyst revisions, overnight Asia
   - Output: news-events/news-{YYYY-MM-DD}.md
   - Write catalysts-cache-{YYYY-MM-DD}.json if any time-sensitive catalysts found (for market-brief and trade-rec to consume)
3. After the news file is written, update .pipeline-status.json:
   - status: OK if file exists and >200 bytes; FAIL otherwise
   - consecutive_failures: 0 on OK; increment from prior on non-OK
4. Exit summary (one line):
   `News capture {YYYY-MM-DD} complete — {N} categories covered, {N} catalysts cached, status={OK|FAIL}`

Then git add -A, commit with message "routine: news-events {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 9:00pm

Produce today's pre-open trade recommendation.

PIPELINE INTEGRITY PRE-CHECK (run before loading the skill):

```python
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
trade_dir = Path('.')
brief   = trade_dir / f'market-brief-{today}.md'
news    = trade_dir / f'news-events/news-{today}.md'
staging = trade_dir / f'audit-data-staging-{today}.md'
missing = []
if not brief.exists():   missing.append(f'market-brief-{today}.md')
if not news.exists():    missing.append(f'news-events/news-{today}.md')
if not staging.exists(): missing.append(f'audit-data-staging-{today}.md')
```

- If brief is MISSING → HARD ABORT. Write abort status to .pipeline-status.json with incremented consecutive_failures. Output: "PIPELINE INTEGRITY FAIL — {missing files}. Trade rec aborted. Consecutive failures: {N}." Stop. Do not load the skill.
- If brief exists but news or staging is missing → WARN AND PROCEED. Output: "PIPELINE INTEGRITY WARNING — {missing files} missing. Proceeding with partial data." Load the skill normally.
- If all three exist → proceed silently.

1. Follow CLAUDE.md §Session Startup Protocol (all four reads).
2. Load and run the `daily-trade-rec` skill end-to-end for today's local date (UTC+8).
   - Synthesises market-brief, news-events, us-close-snapshot, and weekly-review through the 8-step evidence-graded methodology
   - Applies Risk Rules pre-entry checklist before promoting any signal
   - Logs all promoted signals and near-misses to SignalLedger in master-data-log.xlsx (append-only — never rewrite existing rows)
   - Output: trade-rec-{YYYY-MM-DD}.md + report-{YYYY-MM-DD}-trade-rec.html
3. If the delta-check (Step 0) flags "no material change since prior rec", still commit any Memory.md or .pipeline-status.json updates that occurred.
4. On completion, update .pipeline-status.json:
   - status: OK on successful write; ABORT if pre-check aborted; FAIL if skill crashed
   - consecutive_failures: 0 on OK; increment on non-OK
5. Exit summary (one line):
   `Trade rec {YYYY-MM-DD} complete — signals={N promoted, N near-miss}, status={OK|ABORT|FAIL}`

Then git add -A, commit with message "routine: trade-rec {today}", and push to origin main.

---

/schedule

Schedule this for every weekday at 10:00pm

Run the pipeline-recovery skill to check today's pipeline health and recover from any upstream failures.

/pipeline-recovery

The skill runs in two phases:
- Phase A: fast triage (<3K tokens). Reads .pipeline-status.json, checks file sizes against MIN_SIZES, runs structural sniff on brief and trade-rec. If all healthy, print "Pipeline healthy. No recovery needed." and EXIT — do NOT write any files.
- Phase B: recovery (only if Phase A finds failures). Attempts cache-brief from Tier 3 data if market-brief failed. Writes news skeleton if news-events failed. Flags .recovery-pending if trade-rec aborted and brief was just recovered. Escalates to Memory.md §7 if consecutive_failures >= 5 for any task.

Commit + push ONLY if Phase B created or modified files. If Phase A was clean, no commit needed.

Exit summary (one line):
`Pipeline recovery {YYYY-MM-DD} — phase={A-only|A+B}, status={healthy|recovered|unrecoverable}`

---

## WEEKLY ROUTINES (Sunday)

---

/schedule

Schedule this for every Sunday at 6:00pm

Run the weekly regime review and signal review.

PIPELINE INTEGRITY PRE-CHECK (run before Phase 1):
Identify today's date and the 5 weekdays (Mon–Fri) in the most recently completed trading week. Check for market-brief-{date}.md files covering those 5 days. Also check .pipeline-status.json for consecutive failure counts across all tasks.

- If fewer than 4 of 5 daily briefs are present: output "PIPELINE INTEGRITY WARNING — only {n}/5 weekly briefs found. Proceeding but flagging low confidence." Add a ## Data Coverage section to the output noting missing days.
- If 0 or 1 briefs found: output "PIPELINE INTEGRITY FAIL — insufficient brief history ({n}/5). Weekly review aborted." STOP.
- If any task shows consecutive_failures >= 3: add a ## ⚠ Pipeline Health Alert section listing each failing task and its count.

Phase 1 — Regime review:
Read Memory.md, the latest market-brief-*.md, and all news-events/news-*.md from the past 7 days. Write weekly-review-{today}.md covering: regime trajectory for the week, key macro/geopolitical events, thesis validation for open positions, and distilled lessons. Condense memory-lessons.md (remove superseded entries, tighten surviving ones).

Phase 2 — Signal review:
/signal-review
Marks-to-market every hypothetical signal in the SignalLedger sheet of master-data-log.xlsx. Computes hit rates by asset class / score component / regime. Identifies methodology improvements. Writes signal-review-{today}.md + report-{today}-signal-review.html. Updates PerformanceStats sheet.

Then git add -A, commit with message "routine: weekly-regime-signal-review {today}", and push to origin main.

---

/schedule

Schedule this for every Sunday at 9:00pm

CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules, or protocol documents.

Apply the Retention Policy (read Retention Policy.md):
- Move files aged 8+ days to archive/YYYY-MM/ (respecting Memory.md pinned files)
- Digest files aged 31+ days per the retention tiers
- Never archive framework files: Methodology Prompt.md, Risk Rules.md, Data Sources.md, Coin core.md, Trad core.md, Memory.md, Retention Policy.md

Run workspace diagnostics:
1. Excel integrity — verify master-data-log.xlsx opens and has expected 10 sheets
2. Pipeline liveness — check .pipeline-status.json for any tasks with consecutive_failures > 0
3. Output continuity — confirm market-brief, news, and trade-rec files exist for each of the past 5 weekdays
4. Cache health — check .data-cache/ for expired entries beyond staleness windows
5. Skill presence — confirm all 12 skill folders exist under .claude/skills/

Append a dated entry to archive/cleanup-log.md summarising: files archived, files digested, diagnostic results.

Then git add -A, commit with message "routine: workspace-tidy {today}", and push to origin main.

---

## QUARTERLY

---

/schedule

Schedule this for 7:00pm on the 1st of January, April, July, and October

/quarterly-methodology-review

Runs the full quarterly meta-review:
- Audits whether each analytical dimension in the signal review is earning its keep
- Reconciles research cores (Coin core.md / Trad core.md) against out-of-sample ledger evidence in PerformanceStats sheet
- Manages the variable candidate pipeline (promote, hold, retire decisions)
- Updates VariableRegistry sheet in master-data-log.xlsx
- Writes quarterly-methodology-review-{today}.md

Then git add -A, commit with message "routine: quarterly-methodology-review {today}", and push to origin main.

---

## SEMI-ANNUAL

---

/schedule

Schedule this for 3:00pm on the 1st of January and July

/literature-review

Runs the semi-annual academic finance literature scan:
- Searches working papers and journals for new tradeable factors meeting the 5 inclusion criteria (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable)
- Assesses candidates against Gerald's framework gaps
- Writes structured candidate proposals for the variable pipeline
- Output: literature-review-{today}.md

Then git add -A, commit with message "routine: semi-annual-literature-review {today}", and push to origin main.

---

/schedule

Schedule this for 7:00pm on the first Sunday of May and November
(Cron: 0 19 1-7 5,11 0 — verify AND vs OR semantics on first fire. If OR-semantics misfire, add in-prompt guard: "If today is not Sunday, exit silently.")

/system-review

Runs the semi-annual strategic architecture and efficiency audit:
- Walks every skill, scheduled task, and workspace file
- Maps each to the research → trade → monitor → earn value chain
- Produces KEEP / MODIFY / MERGE / REMOVE verdicts using two tests: value (does it earn money) and efficiency (at minimum token cost)
- Identifies architecture gaps AND redundant token burn
- Ranks proposals by P&L impact or context-budget freed for the trade rec
- Output: system-review-{today}.md

Then git add -A, commit with message "routine: system-review-semi-annual {today}", and push to origin main.

---

## TEMPORARY / ONE-TIME

---

/schedule

Schedule this for 7:00pm on the 1st of May and June (auto-disable after July 1 2026)

Bootstrap health check — verify all routines are firing and producing valid output.

Check git log for routine commits from the past 7 days. For each of the 16 routines, confirm at least one commit appeared in its expected window. Report any routine with no commits as MISSED.

Spot-check output quality: read the most recent market-brief-*.md and confirm it contains a regime label, a scorecard table, and at least 10 variable readings.

Check .pipeline-status.json for any task with consecutive_failures > 0.

If today's date >= 2026-07-01: print "Auto-disable threshold reached. No action taken. Gerald: please pause this routine." and exit without doing any checks.

Report status and any issues found.

Then git add -A, commit with message "routine: monthly-bootstrap-review {today}", and push to origin main.

---

/schedule

Schedule this as a one-time task firing on 2026-04-25 at 10:00am (then disable)
(Cron: 0 10 25 4 * — pause or delete after it fires)

Read all meta-additions-staging-*.md files from 2026-04-20 to 2026-04-24 (5 shadow-run days).

For each of V029–V035 (BAB, DealerGamma, GP/A, CEI, Faber TAA V033–V035):
- Report: days retrieved successfully, contribution rate, any instance where the variable was decision-moving in the shadow analysis
- Verdict: PROMOTE to live scoring (Phase 3 GO) / HOLD in shadow for another review cycle / RETIRE

Cross-check against the 2026-04-18 deployment memo in Methodology Prompt.md for the original promotion criteria.

Write meta-shadow-review-2026-04-25.md with per-variable verdict table and narrative justification.

If any variable earns PROMOTE: note that Phase 3 SKILL.md edits in patches/ must now be applied (market-brief, news-events, daily-trade-rec). Gerald must authorize explicitly before applying.

Then git add -A, commit with message "routine: meta-shadow-mode-review 2026-04-25", and push to origin main.

---

/schedule

Schedule this as a one-time task firing on 2026-10-14 at 10:00am (then disable)
(Cron: 0 10 14 10 * — pause or delete after it fires)

Six-month keep/demote review for the 3 audit-addition variables added 2026-04-14:
1. Residual momentum (12m FF5-residualized) — T-input for single stocks
2. Intermediary capital ratio (NY Fed PD z-score) — R-overlay cross-asset
3. Basis-momentum (4w/12w F1–F2 slope change) — S-input for commodities

For each variable:
- Read AuditAdditionLog sheet in master-data-log.xlsx for all entries since 2026-04-14
- Read audit-data-missing-tracker.md for MISSING rates
- Compute: days LIVE, number of decision-moving contributions, contribution rate normalized by days LIVE
- Verdict: KEEP at Grade A / DEMOTE to Grade B / REMOVE from pipeline

Read methodology-audit-6mo-review-2026-10-14.md for any pre-written decision criteria.

Write methodology-audit-6mo-review-2026-10-14-DECISION.md with per-variable verdict, supporting evidence, and any required updates to Methodology Prompt.md, Data Sources.md, or SKILL.md files.

Then git add -A, commit with message "routine: methodology-audit-6mo-review 2026-10-14", and push to origin main.
