---
name: methodology-sync
description: Audit all upstream/downstream skills and tasks against the current Methodology Prompt.md. Identifies stale grades, missing variables, outdated scoring rules, and incorrect Sharpe values. Outputs a gap report and optionally patches files.
---

**Workspace anchor (run FIRST):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd)"; exit 1; }
```

---

## Purpose

Ensure every skill and scheduled task reflects the current methodology state. Run this after any methodology update, or on-demand with `/methodology-sync`.

---

## STEP 0 — Load the source of truth

Read the following files in full:
- `framework/Methodology Prompt.md` — master methodology (all 8 steps, Top-33 variables, scoring rules, grade table)
- `framework/Risk Rules.md` — pre-entry checklist, heat limits, sizing rules

Extract and hold in context for comparison:
- Current evidence grade for each variable (A/B/C)
- Active scoring rules (double-count gates, sleeve interactions, Overlay Gate semantics)
- Active BNMA verdicts (DEPLOY / DEPLOY_CONDITIONAL / WATCH / EXCLUDE)
- PL-NMA ranks and θ values for V026–V035
- Stale-brief handling rule

---

## STEP 1 — Build the file inventory

Collect all SKILL.md paths to audit:

**Local skills** (glob `Trade/.claude/skills/*/SKILL.md`):
- market-brief, daily-trade-rec, news-events, signal-review, positions-monitor, trade-update, quarterly-methodology-review, system-review, pipeline-recovery, literature-review

**Scheduled tasks** (glob `~/.claude/scheduled-tasks/*/SKILL.md`):
- daily-market-brief-8pm, trade-rec-daily, cloud-market-brief, cloud-market-brief-6pm, cloud-trade-rec-7pm, cloud-news-events-630pm, news-events-daily, preflight-audit-data, preflight-meta-additions, us-close-snapshot, slack-ingest, positions-monitor, weekly-regime-signal-review, quarterly-methodology-review, semi-annual-literature-review, semi-annual-system-review, monthly-bootstrap-review, pipeline-recovery-daily, meta-shadow-review-2026-04-25, methodology-audit-6mo-review-2026-10-14, weekly-backup-sunday, workspace-tidy

Read each file. Do not skip any.

---

## STEP 2 — Apply the methodology compliance checklist

For each file read in Step 1, check ALL of the following. Record every gap as a finding.

### CHECK A — Grade downgrades (binding since 2026-04-18)
These five variables were downgraded A→B. Any file that cites them as Grade A is stale:

| Variable | Code | Correct grade |
|---|---|---|
| VIX | V001 | **B** |
| HY OAS / credit spreads | V004 | **B** |
| 2s10s yield curve | V006 | **B** |
| Real yields | V007 | **B** |
| ACM term premium | V008 | **B** |

Search pattern: `VIX.*\(A\)`, `HY OAS.*\(A\)`, `credit spread.*\(A\)`, `2s10s.*\(A\)`, `real yield.*\(A\)`, `term premium.*\(A\)`, `ACM.*\(A\)`.
Any hit where the variable is one of V001/V004/V006/V007/V008 = **GRADE-STALE**.

### CHECK B — New variables present (required in scoring skills)
For any skill that produces an asset scorecard or scores S/T/C/R, check that the following variables are referenced:

| Variable | Where required |
|---|---|
| V029 BAB (Betting-Against-Beta) | S-input for single-stock + ETF in brief, trade-rec, cloud-brief |
| V030 DealerGamma | R-overlay modifier in brief, trade-rec, cloud-brief |
| V031 GP/A (Gross Profitability) | S-input for single-stock in brief, trade-rec, cloud-brief |
| V032 CEI (Composite Equity Issuance) | S-input for single-stock in brief, trade-rec, cloud-brief |
| V033–V035 Faber TAA Overlay Gate | Step 1.5 in brief, trade-rec, cloud-brief |

If a scoring skill has no mention of BAB, DealerGamma, GP/A, CEI, or Faber TAA = **VAR-MISSING**.

### CHECK C — Scoring rules (double-count gates and sleeve caps)
Each scoring skill must contain ALL four of these interaction rules:

1. **V026/V009 gate:** "score V026 only" or "do not also score V009" on single-stock tickers — never both
2. **V027/V004 gate:** "count once" or "more negative" when both flag stress simultaneously
3. **Overlay Gate semantics:** "post-Sum × 0" or "sleeve-OFF" → `Taken=NO`, `Block_Reason=OverlayGateOff`, signal preserved in ledger
4. **V029/V030 sleeve caps:** "1/3 of V009 risk budget" or equivalent cap language

Missing any of these in a scoring skill = **RULE-MISSING**.

### CHECK D — V028 Sharpe value
Any file that cites `0.6–1.0` or `0.6-1.0` as the post-decay Sharpe for basis-momentum (V028) is stale.
Correct value: `0.35–0.47` (BNMA 4-run consensus).
Search for: `0\.6.*1\.0` near "basis-momentum" or "V028" = **SHARPE-STALE**.

### CHECK E — Workspace anchor present
Every scheduled task SKILL.md must contain a workspace anchor:
```
cd "$HOME/OneDrive/Desktop/T.system/Trade"
```
and a `pwd | grep -qE '/T[.]system/Trade$'` guard.
Missing = **ANCHOR-MISSING**.

### CHECK F — V027 citation correct
The primary anchor for intermediary capital ratio must be:
`Adrian-Etula-Muir 2014 JF` (not He-Kelly-Manela 2017 as the sole citation).
If V027 is cited as `He-Kelly-Manela 2017` only (AEM 2014 not present) = **CITATION-STALE**.

### CHECK G — Evidence sources listed
Skills that produce methodology-graded outputs (trade-rec, signal-review, quarterly-review) should reference `bnma/meta-analysis/` as an evidence source when citing V026–V035 BNMA verdicts. Missing = **SOURCE-MISSING** (low priority; note only).

---

## STEP 3 — Produce the gap report

Output a structured gap report in this format:

```
# Methodology Sync Report — {YYYY-MM-DD}
Source of truth: framework/Methodology Prompt.md (last known edit: 2026-04-21)

## Summary
Total files scanned: N
Files with gaps: N
Total findings: N (A=grade-stale, B=var-missing, C=rule-missing, D=sharpe-stale, E=anchor-missing, F=citation-stale, G=source-missing)

## Findings

### GRADE-STALE (A→B downgrades cited incorrectly)
| File | Line | Variable | Current text | Required fix |
|------|------|----------|--------------|--------------|

### VAR-MISSING (new V029–V035 variables absent from scoring skills)
| File | Missing variable | Required location in skill |
|------|-----------------|--------------------------|

### RULE-MISSING (scoring interaction rules absent)
| File | Missing rule | Required text |
|------|-------------|--------------|

### SHARPE-STALE (V028 post-decay Sharpe incorrect)
| File | Line | Current value | Correct value |
|------|------|---------------|---------------|

### ANCHOR-MISSING (workspace anchor absent)
| File | Fix |
|------|-----|

### CITATION-STALE (V027 primary anchor incorrect)
| File | Line | Current | Required |
|------|------|---------|---------|

### SOURCE-MISSING (bnma/meta-analysis/ not referenced) — low priority
| File | Note |
```

If a section has no findings, write `None — compliant.`

---

## STEP 4 — Patch or defer

For each finding, classify the urgency:

- **CRITICAL** (patch now without asking): ANCHOR-MISSING, SHARPE-STALE, CITATION-STALE
- **HIGH** (ask before patching): GRADE-STALE in scoring skills, VAR-MISSING in scoring skills, RULE-MISSING
- **LOW** (note only, defer): SOURCE-MISSING, VAR-MISSING in non-scoring skills (e.g. backup, workspace-tidy)

For CRITICAL findings: apply the fix inline, write the corrected file, note the change in the report.

For HIGH findings: list them clearly and ask Gerald to confirm before patching. Do not auto-patch.

For LOW findings: list them in the report. No action unless Gerald asks.

After patching CRITICAL items, note at end of report:
```
## Auto-patched (CRITICAL)
{list of file + change applied}
```

---

## STEP 5 — Commit

If any files were patched:
```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade"
git add -A
git commit -m "fix: methodology-sync patch — {summary of critical fixes}"
```

Then output:
```
Methodology sync complete — {N} files scanned, {N} gaps found, {N} auto-patched (CRITICAL), {N} pending Gerald confirmation (HIGH).
```

---

## Key methodology state as of 2026-04-21 (quick reference for this skill)

**Grade downgrades (A→B):** V001 VIX, V004 HY OAS, V006 2s10s, V007 real yields, V008 ACM term premium.

**New variables (2026-04-18 cohort, all scoring skills):**
- V029 BAB: S-input, single-stock+ETF, independent sleeve, cap 1/3 V009 budget, BNMA DEPLOY_CONDITIONAL
- V030 DealerGamma: R-overlay modifier, Grade B (1 paper), BNMA WATCH, must flag single-paper status
- V031 GP/A: S-input, single-stock, quarterly rebalance, BNMA DEPLOY
- V032 CEI: S-input, single-stock, negative sign, BNMA DEPLOY
- V033–V035 Faber TAA: Step 1.5 Overlay Gate only, non-additive to Sum, monthly flip at month-end close

**Scoring interaction rules (all four required in scoring skills):**
1. V026 only on single-stock (not V009+V026 together)
2. V027+V004 count once (more negative wins)
3. Overlay Gate: post-Sum × 0, sleeve-OFF → Taken=NO, Block_Reason=OverlayGateOff
4. V029+V030 each capped at 1/3 V009 risk budget

**V028 basis-momentum:** post-decay Sharpe 0.35–0.47 (BNMA 4-run). Not 0.6–1.0.

**V027 primary anchor:** Adrian-Etula-Muir 2014 JF 69(6) (He-Kelly-Manela 2017 JFE is secondary).

**Stale-brief fallback:** brief age < 36h → proceed with STALE labels; ≥ 36h → block new entries; no brief anywhere → HARD ABORT.

**Evidence sources:** `bnma/meta-analysis/BNMA-meta-analysis-2026-04-18.md` and `bnma/meta-analysis/PL-NMA-meta-analysis-2026-04-18.md` are authoritative for V026–V035 verdicts and rankings.
