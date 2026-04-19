---
name: quarterly-methodology-review
description: Quarterly meta-review of the signal review system and trading methodology. Audits whether each analytical dimension is earning its keep, reconciles research cores against OOS ledger evidence, and manages the variable candidate pipeline. Use when the user asks to "review the methodology", "audit the system", "quarterly review", "meta-review", "is the system working", "are the analytics useful", "prune the review", "research reconciliation", "variable pipeline", "methodology fitness", or "review the review". Also triggers on scheduled task `quarterly-methodology-review`. NOT the weekly signal review (use signal-review) — this operates one level up, evaluating the signal review itself and the methodology it measures.
---

# Quarterly Methodology Review — Meta-Review & Research Reconciliation

This skill runs once per quarter (or on demand) to answer three questions the weekly signal review can't:

1. **Is the signal review asking the right questions?** — which analytical dimensions are producing actionable findings vs. burning context for nothing?
2. **Does the research still hold?** — where do the cores' claims diverge from what the ledger shows out of sample?
3. **What should we try next?** — which candidate variables or analyses have enough data to pilot?

The output is a dated review file, updates to the methodology prompt and skill files (pending Gerald's sign-off), and a research reconciliation log. Every change recommendation requires Gerald's explicit approval — this skill diagnoses and proposes, it never auto-adjusts.

---

## Step 1 — Read the inputs

Read these files in order. Each one feeds a specific part of the review:

**System state:**
1. `/mnt/.auto-memory/MEMORY.md` — scan index, open all project memories (especially `project_signal_review_enhancement_2026-04-15.md`, `project_methodology_audit_2026-04-14.md`, `project_performance_tracking.md`)
2. `/mnt/Trade/Memory.md` — §9 research questions
2b. `/mnt/Trade/memory-lessons.md` — the full lessons log (split from Memory.md §8). Read this for repeated blocking patterns and prior methodology notes.
3. `/mnt/Trade/master-data-log.xlsx` — read the **SignalLedger** sheet (all rows), **PerformanceStats** sheet (rolling statistics, interaction matrix, all summary tables), **RegimeHistory** (latest row = current regime), and **AuditAdditionLog** (audit-addition contribution history) using openpyxl. These are the sole structured data stores.

**Methodology:**
5. `/mnt/Trade/Methodology Prompt.md` — the master 8-step framework and Top-25 variables
6. `/mnt/Trade/Risk Rules.md` — binding pre-entry checklist and sizing policy
7. `/mnt/Trade/Data Sources.md` — variable-to-source mapping

**Research cores:**
8. `/mnt/Trade/Trad core.md` — cross-asset factor review
9. `/mnt/Trade/Coin core.md` — crypto predictor families

**Prior reviews:**
10. All `signal-review-*.md` files in `/mnt/Trade/` — read the Methodology Improvement Candidates (§7) from each. This is the cumulative record of what the weekly reviews have flagged.
11. The most recent `quarterly-methodology-review-*.md` if one exists — carry forward any pending actions.

If the ledger has fewer than 30 closed signals (promoted + near-miss), the review still runs but adds a banner at the top: "Early-stage review — statistical patterns below 30 signals are directional hypotheses, not evidence. Focus on system health checks rather than performance conclusions."

## Step 2 — Analytical Dimension Fitness Audit

This is the core of the meta-review. For each analytical dimension currently active in the signal review, assess whether it's earning its place in the weekly context budget.

**Dimensions to audit (as of 2026-04-15):**

*Original dimensions (from signal-review launch):*
1. Win rate by score component (S/T/C/R univariate)
2. Win rate by asset class
3. Win rate by regime label
4. Blocking leg distribution (near-miss)
5. Near-miss counterfactual (would-have-won vs would-have-lost)
6. Audit-addition variable contribution
7. Threshold sensitivity (|Sum| = 2 vs |Sum| = 3)

*Enhancement dimensions (added 2026-04-15):*
8. Score component interaction matrix (S×T, S×R, etc.)
9. Time-to-exit distribution
10. MAE/MFE analysis
11. Catalyst resolution tracking
12. VIX-at-entry conditioning
13. Near-miss counterfactual regression

**For each dimension, answer:**

- **Has it produced a finding that reached RECOMMEND status?** Check the PerformanceStats sheet and §6 of all weekly signal-review files. If yes, the dimension is validated — keep it.
- **Has it surfaced a pattern that changed how Gerald reads the weekly output?** This is softer — check Memory.md §8 for any lesson that references this dimension. Ask Gerald directly if unclear.
- **Is the sample size sufficient for this dimension to be statistically meaningful?** Some dimensions (interaction matrix, near-miss regression) need more data than others. If a dimension has been active for two quarters and still shows "insufficient data" or "sample too small" on most cells, it's not yet useful.
- **What's the context cost?** Estimate tokens: each summary table is ~200-400 tokens in the ledger, each review section is ~300-600 tokens. The full enhancement adds roughly 3,000-4,000 tokens to the weekly review's context. Is that cost justified by the findings?

**Classification:**
- **RETAIN** — producing or likely to produce actionable findings
- **DEMOTE to on-demand** — not currently useful at weekly cadence; compute only when Gerald asks or during quarterly reviews
- **RETIRE** — fundamentally doesn't work for this system; remove from the skill
- **PROMOTE** — showing enough value that it should inform scoring rules, not just diagnostics

Write a one-paragraph assessment for each dimension, then a summary table:

| # | Dimension | Status | Findings to date | Sample adequate? | Context cost (est. tokens) | Recommendation |
|---|-----------|--------|------------------|------------------|---------------------------|----------------|

## Step 3 — Research Core Reconciliation

This step cross-references the ledger's empirical findings against the claims in Trad core and Coin core. The purpose is to catch research assumptions that are breaking down in live markets — not to search for new papers (that's a separate activity).

**For each of the Top-25 variables in Methodology Prompt.md (entries 1-28):**

1. **Is this variable being scored in the daily pipeline?** Check Data Sources.md and the recent trade-rec files. If a Grade A variable isn't being scored (e.g., always MISSING), that's a data pipeline issue, not a methodology issue — flag it separately.

2. **Does the ledger evidence support the variable's grade?** Compare the variable's contribution to signal outcomes:
   - If a Grade A variable's score leg shows no win-rate differential between +1 and −1 after 60+ signals, that's a red flag for the grade assignment.
   - If a Grade B variable consistently appears in winning signals, it may deserve promotion.
   - Reference the specific academic paper cited in the cores and note whether the market conditions that paper tested are similar to current conditions.

3. **Has the market regime shifted in a way that undermines the variable?** The classic example from the Trad core: real yields had R² = 84% with gold prices 2005-2021 but collapsed to 3-7% post-2022 due to central bank buying. Look for similar regime breaks in other variables.

**For the three audit-addition variables specifically (residual momentum, intermediary capital, basis-momentum):**

4. Read the **AuditAdditionLog** sheet in `master-data-log.xlsx`. Count the entries. Are they contributing to scoring decisions? The 2026-10-14 review deadline is the hard gate — if they haven't contributed by then, they get demoted to Grade B.

5. Check the signal-review's §6 (Audit-Addition Variable Review) across all weekly reviews. Is there a pattern? Is one variable consistently blocking signals that would have won? Is another consistently contributing to winners?

**For the meta-integration cohort V029 / V033 / V034 / V035 (Phase 3, added 2026-04-25):**

6. Read **SignalLedger cols 33–36** (`overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`) via openpyxl. Count rows by gate-ON vs gate-OFF per sleeve and by V027 bucket.

7. Read the three new **PerformanceStats** sub-tables produced by signal-review Phase 3: "Overlay Gate Outcomes", "V027 Regime Bucket Conditioning", "BAB Sleeve Activation". These give gate_protection_pp per sleeve, bucket-conditional win rates, and BAB activation win-rate splits.

8. Reconcile against the meta-analysis PL-NMA projections in `Methodology Prompt.md` — V029 post-decay Sharpe 0.4–0.8; V033–V035 Faber TAA as gate (no alpha, drawdown reduction instead, target: reduced max-DD on gated sleeves vs. un-gated counterfactual). Is realized behavior inside the projected range? Is the gate actually protecting drawdowns?

9. **V030 / V031 / V032 — explicit-MISSING tracking.** V030 DealerGamma stays MISSING until Gerald confirms a SqueezeMetrics or SpotGamma subscription; next decision point is 2026-07-01 (this review or the next). V031 GP/A and V032 CEI stay MISSING until the Phase 2b compute stubs land (Ken French GP fetcher / CRSP+Compustat CEI compute). For each MISSING variable, record: weeks_missing, blocker_reason, next_review_target. If any MISSING variable crosses 180 days (2026-10-14), it auto-flags for demotion review alongside the Batch-1 audit cohort.

**2026-10-14 shared review reminder.** V029 / V033–V035 share the 2026-10-14 six-month review date with V026–V028 (Batch-1 audit additions). The October quarterly review is the hard gate for the meta-integration cohort — formal GO/DOWNGRADE/RETIRE per variable based on OOS contribution evidence.

**Output a reconciliation table** (extended Phase 3 to entries 1–35; V029–V035 appended):

| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |
|----------|-------|---------------------|------------------------|-----------------|--------|

Actions: CONFIRMED (grade holds), WATCH (emerging concern), DOWNGRADE CANDIDATE (evidence against), UPGRADE CANDIDATE (evidence for), DATA GAP (can't assess), SUBSCRIPTION-BLOCKED (V030 only, until subscription live), STUB-BLOCKED (V031/V032 only, until Phase 2b compute implemented).

## Step 4 — Variable Candidate Pipeline

Review variables that were identified as potential additions but haven't been implemented yet. As of 2026-04-15, the candidate pipeline includes:

**Tier 2 candidates (need data collection infrastructure):**
- GEX (gamma exposure) as regime overlay — positive/negative GEX predicts mean-reversion vs trend-following
- Cross-asset lead-lag exploitation — BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX
- Correlation-regime signal quality — trailing 20d cross-asset correlation as quality filter

**Meta-integration stubs (Phase 3, added 2026-04-25 — candidates pending data-pipeline implementation):**
- **V030 DealerGamma** — subscription-blocked. Recommended action per review: RENEW-BLOCK if Gerald has not confirmed subscription; PROMOTE-TO-LIVE if confirmed and one week of staging data available.
- **V031 GP/A (Novy-Marx 2013)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if Ken French GP-portfolio CSV fetcher landed; DEFER otherwise.
- **V032 CEI (Daniel-Titman 2006)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if CRSP+Compustat self-compute landed; DEFER otherwise.

**Tier 3 candidates (need 60+ closed signals):**
- Decision tree feature importance — shallow tree to surface non-obvious interaction effects
- Calendar/seasonal effects — day-of-week, OpEx proximity, FOMC week patterns

**For each candidate, assess:**

1. **Does the ledger now have enough data to pilot this?** Check signal count. Decision tree needs 50+; correlation-regime needs 30+; GEX and lead-lag can start immediately with retroactive tagging.

2. **Has any weekly review finding pointed toward this candidate?** If the interaction matrix or near-miss regression surfaced a pattern that this candidate would explain, that's evidence for promotion.

3. **What's the implementation cost?** New columns in the ledger? New data source? New computation in the review skill? Estimate the effort and context budget impact.

4. **Recommendation:** PILOT (add to next week's review on trial basis), DEFER (not enough data yet), REJECT (evidence suggests it won't help), NEEDS RESEARCH (worth investigating but unclear implementation).

**Output:**

| Candidate | Data ready? | Weekly review evidence? | Impl. cost | Recommendation |
|-----------|-------------|------------------------|------------|----------------|

## Step 5 — Methodology Change Proposals

Consolidate all RECOMMEND-status items from:
- Weekly signal review §7 (Methodology Improvement Candidates)
- Step 2 dimension audit (PROMOTE or RETIRE recommendations)
- Step 3 research reconciliation (DOWNGRADE or UPGRADE candidates)
- Step 4 variable pipeline (PILOT recommendations)

For each proposed change, write a structured recommendation:

```
### Change ID: QR-{YYYY}-{NN}

**Proposed change:** [one sentence]
**Evidence:** [cite specific signals, win rates, sample sizes from the ledger]
**Risk:** [what could go wrong; overfitting risk; McLean-Pontiff decay concern]
**Impact:** [which assets/legs are affected; estimated improvement]
**Reversibility:** [can this be unwound easily if it doesn't work?]
**Status:** RECOMMEND / MONITOR / REJECT
**Gerald sign-off:** PENDING
```

## Step 6 — Write the review file

Path: `/mnt/Trade/quarterly-methodology-review-{YYYY-MM-DD}.md`. Use this structure:

```
# Quarterly Methodology Review — YYYY-MM-DD

## 1. Review Summary
[One paragraph: ledger size, period covered, key headline findings. Is the system healthy? Are the analytics earning their keep?]

## 2. Analytical Dimension Fitness Audit
[Summary table + one paragraph per dimension. Retain/Demote/Retire/Promote decisions.]

## 3. Research Core Reconciliation
[Reconciliation table + commentary on any variables where the grade is under pressure. Special section on the three audit-addition variables with reference to the 2026-10-14 deadline.]

## 4. Variable Candidate Pipeline
[Pipeline table + rationale for each recommendation.]

## 5. Methodology Change Proposals
[Structured recommendations per the template above. Number sequentially QR-{YYYY}-01, QR-{YYYY}-02, etc.]

## 6. Context Budget Assessment
[Current token estimate for the weekly review cycle: ledger + review file + HTML report. Is it growing unsustainably? Are the archival tiers working? Specific recommendations for trimming if needed.]

## 7. Action Items for Next Quarter
[Bulleted list of what to monitor, what to implement, and what's due. Include the next quarterly review date.]

---

Review covers: {date range}. Closed signals: {N}. Open signals: {N}. Ledger health: {OK / NEEDS ARCHIVAL / OVERSIZED}.
```

## Step 7 — Apply changes (with sign-off tracking)

After writing the review file:

1. **Record change proposals** in the quarterly review output file (§5). All QR-prefixed proposals with `Gerald sign-off: PENDING` are written to the review file only — no separate persistent change log.

2. **Update `/mnt/Trade/memory-lessons.md`** with a one-line summary: `YYYY-MM-DD quarterly methodology review: N dimensions audited, N retained / N demoted / N retired. N variable candidates assessed. N change proposals (RECOMMEND: N, MONITOR: N). File: quarterly-methodology-review-YYYY-MM-DD.md.` (Memory.md §8 is a pointer to this file.)

3. **Update Memory.md §9** with any new research questions surfaced by the reconciliation.

4. **If any dimension was classified as DEMOTE or RETIRE:** Do NOT modify the signal-review skill directly. Instead, add a note to the review file §5 with the exact skill edit required, and mark it `Gerald sign-off: PENDING`. Gerald will apply it manually or ask Claude to do so in a future session.

5. **If any variable candidate was classified as PILOT:** Same approach — describe the exact ledger column additions and skill modifications needed, but don't apply without sign-off.

## Step 7.5 — Sync to master-data-log.xlsx (MANDATORY)

After applying changes above, update the **VariableRegistry** sheet in `master-data-log.xlsx` using openpyxl. Read `Excel-Sync-Protocol.md` §4 (quarterly-methodology-review) for the authoritative column mapping.

For each variable assessment in this review:
- Update `Last_Review_Date` to today
- Update `Next_Review_Date`
- Append to `Review_History`
- Update `Status` if a promotion/demotion decision was made (with Gerald sign-off tracking in Notes)
- Update `Decision_Moving_Count` and `OOS_Contribution` based on SignalLedger evidence

For variable candidates being promoted from the pipeline:
- Update Status (e.g., Candidate → Under Review, or Under Review → Provisionally Useful)
- Fill in any newly available screening criteria

## Step 8 — HTML report

Produce a single-file HTML report at `/mnt/Trade/report-{YYYY-MM-DD}-quarterly-review.html`. Use Chart.js via CDN (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`).

**Required charts:**

- **Dimension fitness scorecard** (horizontal bar or radar chart: each dimension rated on a 0-3 scale for findings produced, sample adequacy, and context efficiency)
- **Research core reconciliation heatmap** (Top-25 variables: rows = variables, columns = grade supported / regime concern / data gap; color-coded)
- **Audit-addition contribution timeline** (sparkline or bar chart: count of contribution log entries per week for each of the three audit additions, with the 2026-10-14 deadline marked)
- **Cumulative P&L curve** (carried from weekly review, but with quarterly trend annotation)
- **Variable candidate pipeline funnel** (visual showing how many candidates are at each stage: idea → data ready → piloting → active → retired)
- **Context budget breakdown** (stacked bar: tokens consumed by each section of the weekly review, with a budget ceiling line)
- **Methodology change log timeline** (horizontal Gantt-style: each change proposal from PENDING to signed-off or rejected, over time)

If this is the first quarterly review (no prior review exists), add a setup banner: "First quarterly review — establishing baselines. All assessments are initial readings, not trend conclusions."

## Step 9 — Update auto-memory

Create or update the memory file for this review:
- File: `/mnt/.auto-memory/project_quarterly_review_{YYYY-MM-DD}.md`
- Content: key decisions made, dimensions retained/demoted, variable pipeline status, next review date
- **Phase 3 addition (2026-04-25):** include explicit status line for the meta-integration cohort — V029/V033/V034/V035 reconciliation verdicts, V030 subscription state, V031/V032 stub state, and shared-2026-10-14-review reminder
- Update `MEMORY.md` index with a pointer

---

## Discipline rules

- Every change requires Gerald's sign-off. This skill proposes, never executes methodology changes.
- Sample size caveats on everything. A quarterly review with 40 signals is more useful than no review, but less useful than one with 120.
- The purpose is to keep the system sharp, not to add complexity. If a quarterly review consistently produces more RETAIN than DEMOTE decisions, that's a sign the system is well-calibrated. If it consistently produces DEMOTE or RETIRE, that's a sign the enhancement process is over-building.
- Research reconciliation should be conservative. A variable that underperforms for one quarter in a specific regime isn't necessarily broken — it might just be regime-inappropriate right now. Look for persistent patterns across multiple regimes and quarters before recommending grade changes.
- The 2026-10-14 audit-addition review is a hard deadline. The quarterly review closest to that date (likely early October) must include a formal GO/NO-GO recommendation for each of the three additions.
