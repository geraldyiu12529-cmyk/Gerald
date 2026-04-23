# Phase 3 Patch — signal-review SKILL.md (meta-integration consumer)

**Source:** 2026-04-18 meta-integration deployment (`deployment-memo-2026-04-18.md`).
**Applies when:** 2026-04-25 shadow-mode review returns GO verdicts for V029, V033, V034, V035.
**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\signal-review\SKILL.md`
**Scope test:** edits total ~1.1 KB against the ~16 KB SKILL.md (~7%) → minimum-surface edit, NOT full rewrite.

## Summary

Phase 3 adds a new analytical dimension to the weekly mark-to-market aggregation: reading SignalLedger cols 33–36 (`overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`) and producing three new breakdowns in Step 4, one new section (§5B) in Step 6, and one new Escalation Flag in §8.

The point: track whether the overlay gate is earning its keep (does it actually protect returns when it blocks?) and whether V027 regime bucketing / BAB sleeve activation correlate with signal outcomes. This is the evidence base the 2026-10-14 six-month review will judge V029/V033/V034/V035 against.

No changes to mark-to-market logic, price fetch, or status assignment. New reads only. No new outputs to the Excel workbook beyond the existing PerformanceStats sheet (new summary tables appended per `Excel-Sync-Protocol.md §3`).

## SignalLedger cols read this skill consumes (positions 33–36, schema confirmed 2026-04-18)

| # | Col | Weekly aggregation |
|---|---|---|
| 33 | `overlay_gate_status` | parse sleeve states; group rows by sleeve; compute gate-ON vs gate-OFF outcomes |
| 34 | `v027_regime_bucket` | three-bucket grouping (expansion / neutral / contraction); win rate per bucket |
| 35 | `bab_sleeve_weight` | correlate weight > 0 vs weight = 0 with single-stock signal outcomes |
| 36 | `dealergamma_sleeve_weight` | record presence/absence; expected MISSING through 2026-07-01 |

Rows with `overlay_gate_status = 'MISSING'` (pre-Phase-3 or fail-loud fallback) are excluded from the overlay-specific breakdowns and counted in a separate "pre-Phase-3" pool for continuity.

## Before/after edits

### Edit 1 — Add Step 4 subsection: Overlay Gate + V027 + BAB analyses

**Anchor:**
```markdown
**Audit-Addition Variables:** For residual momentum, intermediary capital, and basis-momentum: count how many times each was present vs MISSING, how many times it was the blocking leg, and whether signals where it was present had better outcomes than signals where it was MISSING.

## Step 5 — Identify methodology improvement candidates
```

**Replace with:**
```markdown
**Audit-Addition Variables:** For residual momentum, intermediary capital, and basis-momentum: count how many times each was present vs MISSING, how many times it was the blocking leg, and whether signals where it was present had better outcomes than signals where it was MISSING.

**Meta-Integration Variables (Phase 3 addition — SignalLedger cols 33–36):**

*Overlay Gate Outcomes (V033/V034/V035).* Parse `overlay_gate_status` per row. Bucket every signal by whether its sleeve was ON or OFF at signal time. For overlay-OFF signals with Type='Promoted' / Taken='NO' / Block_Reason ∈ {'OverlayGateOff', 'OverlayStagingMissing'}: compute the *counterfactual* move from Price_at_Signal to current price, and classify as would-have-hit-target / would-have-hit-stop / expired. The key question: does the gate's OFF state systematically protect returns (hypothetical PnL worse on OFF sleeves than ON)? Or does it systematically block winners (OFF counterfactual wins > ON actual wins)? Update the "Overlay Gate Outcomes" table in the PerformanceStats sheet with columns: sleeve, gate_state, N_signals, counterfactual_win_rate, actual_win_rate (gate-ON population only), gate_protection_pp. Flag gate_protection_pp below −10pp as GATE-BLOCKING-WINNERS.

*V027 Regime Bucket Conditioning.* Group signals by `v027_regime_bucket`. Compute win rate, average P&L, and average days-to-exit per bucket (expansion / neutral / contraction / MISSING). The key question: does the V027 sizing tier (Risk Rules §1.B) correctly downsize in contraction regimes? Compare realized P&L in contraction-bucket Taken=YES signals against the halved-gross-exposure expectation. Update the "V027 Regime Bucket Conditioning" table in PerformanceStats with: bucket, N_signals, win_rate, avg_pnl_pct, avg_days_to_exit, avg_bab_sleeve_weight, avg_dealergamma_sleeve_weight.

*BAB Sleeve Activation.* Split single-stock signals on `bab_sleeve_weight > 0` vs `= 0`. Compute win rate for each split. The key question: when V029 signals BAB-on (USMV − SPLV spread > 0), do our long single-stock signals on low-β names outperform? Require N ≥ 10 per split before drawing conclusions. Update the "BAB Sleeve Activation" table in PerformanceStats.

*DealerGamma* remains MISSING across this cohort (V030 subscription pending — expected MISSING until at least 2026-07-01). Count MISSING rows for audit completeness; no outcome analysis possible until subscription is live.

## Step 5 — Identify methodology improvement candidates
```

### Edit 2 — Add §5B to Step 6 output template

**Anchor:**
```markdown
## 5. Audit-Addition Variable Review
[For residual momentum, intermediary capital, basis-momentum: present vs MISSING counts, blocking-leg frequency, outcome differential. Feeds the 2026-10-14 six-month review.]

## 6. Methodology Improvement Candidates
```

**Replace with:**
```markdown
## 5. Audit-Addition Variable Review
[For residual momentum, intermediary capital, basis-momentum: present vs MISSING counts, blocking-leg frequency, outcome differential. Feeds the 2026-10-14 six-month review.]

## 5B. Meta-Integration Variable Review (Phase 3, added 2026-04-25)
[Four sub-sections:
 (a) Overlay Gate Outcomes — per-sleeve gate-ON vs gate-OFF counts, counterfactual vs actual win rates, gate_protection_pp. Flag GATE-BLOCKING-WINNERS if any sleeve shows protection_pp < −10.
 (b) V027 Regime Bucket Conditioning — win rate, avg P&L, avg days-to-exit across expansion / neutral / contraction.
 (c) BAB Sleeve Activation — win rate split by bab_sleeve_weight > 0 vs = 0 on single-stock signals.
 (d) DealerGamma — MISSING count only; no outcome analysis until V030 subscription live.
 Feeds the 2026-10-14 six-month meta-integration review (shared cohort with V026–V028 Batch-1).]

## 6. Methodology Improvement Candidates
```

### Edit 3 — Add new Escalation Flag to §8

**Anchor:**
```markdown
- **AUDIT-ADDITION-STALL:** Any audit-addition variable has 0 decision-moving contributions and > 90 days elapsed since 2026-04-14 → name variable, days elapsed.

Format: `**{FLAG-TYPE}** — {variable/component}: {metric} (N = {sample size})`
```

**Replace with:**
```markdown
- **AUDIT-ADDITION-STALL:** Any audit-addition variable has 0 decision-moving contributions and > 90 days elapsed since 2026-04-14 → name variable, days elapsed.
- **OVERLAY-GATE-BLOCKING-WINNERS** *(Phase 3, added 2026-04-25)*: Any sleeve shows counterfactual_win_rate (gate-OFF) exceeding actual_win_rate (gate-ON) by > 10pp with N ≥ 10 gate-OFF signals → name sleeve, both rates, N.
- **OVERLAY-STAGING-MISSING-PERSISTENT** *(Phase 3, added 2026-04-25)*: `overlay_gate_status = 'MISSING'` in ≥ 3 of last 5 daily trade-recs → staging pipeline health issue; check `preflight-meta-additions-1952pm` task.

Format: `**{FLAG-TYPE}** — {variable/component}: {metric} (N = {sample size})`
```

## PowerShell apply block (idempotent)

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\signal-review\SKILL.md"
if (-not (Test-Path $path)) { Write-Error "SKILL.md not found at $path"; exit 1 }

$content = Get-Content $path -Raw

if ($content -match "Meta-Integration Variables \(Phase 3 addition") {
    Write-Host "signal-review Phase 3 patch already applied — skipping"
    exit 0
}

# --- Edit 1 — Add Step 4 meta-integration analysis block ---
$e1Anchor  = "**Audit-Addition Variables:** For residual momentum, intermediary capital, and basis-momentum: count how many times each was present vs MISSING, how many times it was the blocking leg, and whether signals where it was present had better outcomes than signals where it was MISSING.`r`n`r`n## Step 5 — Identify methodology improvement candidates"
$e1Replace = @'
**Audit-Addition Variables:** For residual momentum, intermediary capital, and basis-momentum: count how many times each was present vs MISSING, how many times it was the blocking leg, and whether signals where it was present had better outcomes than signals where it was MISSING.

**Meta-Integration Variables (Phase 3 addition — SignalLedger cols 33–36):**

*Overlay Gate Outcomes (V033/V034/V035).* Parse `overlay_gate_status` per row. Bucket every signal by whether its sleeve was ON or OFF at signal time. For overlay-OFF signals with Type='Promoted' / Taken='NO' / Block_Reason ∈ {'OverlayGateOff', 'OverlayStagingMissing'}: compute the *counterfactual* move from Price_at_Signal to current price, and classify as would-have-hit-target / would-have-hit-stop / expired. The key question: does the gate's OFF state systematically protect returns (hypothetical PnL worse on OFF sleeves than ON)? Or does it systematically block winners (OFF counterfactual wins > ON actual wins)? Update the "Overlay Gate Outcomes" table in the PerformanceStats sheet with columns: sleeve, gate_state, N_signals, counterfactual_win_rate, actual_win_rate (gate-ON population only), gate_protection_pp. Flag gate_protection_pp below −10pp as GATE-BLOCKING-WINNERS.

*V027 Regime Bucket Conditioning.* Group signals by `v027_regime_bucket`. Compute win rate, average P&L, and average days-to-exit per bucket (expansion / neutral / contraction / MISSING). The key question: does the V027 sizing tier (Risk Rules §1.B) correctly downsize in contraction regimes? Compare realized P&L in contraction-bucket Taken=YES signals against the halved-gross-exposure expectation. Update the "V027 Regime Bucket Conditioning" table in PerformanceStats with: bucket, N_signals, win_rate, avg_pnl_pct, avg_days_to_exit, avg_bab_sleeve_weight, avg_dealergamma_sleeve_weight.

*BAB Sleeve Activation.* Split single-stock signals on `bab_sleeve_weight > 0` vs `= 0`. Compute win rate for each split. The key question: when V029 signals BAB-on (USMV − SPLV spread > 0), do our long single-stock signals on low-β names outperform? Require N ≥ 10 per split before drawing conclusions. Update the "BAB Sleeve Activation" table in PerformanceStats.

*DealerGamma* remains MISSING across this cohort (V030 subscription pending — expected MISSING until at least 2026-07-01). Count MISSING rows for audit completeness; no outcome analysis possible until subscription is live.

## Step 5 — Identify methodology improvement candidates
'@
if (-not $content.Contains($e1Anchor)) { Write-Error "Edit 1 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e1Anchor, $e1Replace)

# --- Edit 2 — Insert §5B into Step 6 output template ---
$e2Anchor  = "## 5. Audit-Addition Variable Review`r`n[For residual momentum, intermediary capital, basis-momentum: present vs MISSING counts, blocking-leg frequency, outcome differential. Feeds the 2026-10-14 six-month review.]`r`n`r`n## 6. Methodology Improvement Candidates"
$e2Replace = @'
## 5. Audit-Addition Variable Review
[For residual momentum, intermediary capital, basis-momentum: present vs MISSING counts, blocking-leg frequency, outcome differential. Feeds the 2026-10-14 six-month review.]

## 5B. Meta-Integration Variable Review (Phase 3, added 2026-04-25)
[Four sub-sections:
 (a) Overlay Gate Outcomes — per-sleeve gate-ON vs gate-OFF counts, counterfactual vs actual win rates, gate_protection_pp. Flag GATE-BLOCKING-WINNERS if any sleeve shows protection_pp < −10.
 (b) V027 Regime Bucket Conditioning — win rate, avg P&L, avg days-to-exit across expansion / neutral / contraction.
 (c) BAB Sleeve Activation — win rate split by bab_sleeve_weight > 0 vs = 0 on single-stock signals.
 (d) DealerGamma — MISSING count only; no outcome analysis until V030 subscription live.
 Feeds the 2026-10-14 six-month meta-integration review (shared cohort with V026–V028 Batch-1).]

## 6. Methodology Improvement Candidates
'@
if (-not $content.Contains($e2Anchor)) { Write-Error "Edit 2 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e2Anchor, $e2Replace)

# --- Edit 3 — Add new flags to §8 Escalation Flags ---
$e3Anchor  = "- **AUDIT-ADDITION-STALL:** Any audit-addition variable has 0 decision-moving contributions and > 90 days elapsed since 2026-04-14 → name variable, days elapsed.`r`n`r`nFormat:"
$e3Replace = @'
- **AUDIT-ADDITION-STALL:** Any audit-addition variable has 0 decision-moving contributions and > 90 days elapsed since 2026-04-14 → name variable, days elapsed.
- **OVERLAY-GATE-BLOCKING-WINNERS** *(Phase 3, added 2026-04-25)*: Any sleeve shows counterfactual_win_rate (gate-OFF) exceeding actual_win_rate (gate-ON) by > 10pp with N ≥ 10 gate-OFF signals → name sleeve, both rates, N.
- **OVERLAY-STAGING-MISSING-PERSISTENT** *(Phase 3, added 2026-04-25)*: `overlay_gate_status = 'MISSING'` in ≥ 3 of last 5 daily trade-recs → staging pipeline health issue; check `preflight-meta-additions-1952pm` task.

Format:
'@
if (-not $content.Contains($e3Anchor)) { Write-Error "Edit 3 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e3Anchor, $e3Replace)

# Backup + write
$backup = "$path.bak-phase3-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $path $backup
Set-Content $path $content -NoNewline
Write-Host "signal-review Phase 3 patch applied. Backup: $backup"
```

## Verify

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\signal-review\SKILL.md"
$c = Get-Content $path -Raw
$checks = @(
    @{ Name = "Step 4 meta-integration block";        Pattern = "Meta-Integration Variables \(Phase 3 addition" },
    @{ Name = "Overlay Gate Outcomes table";          Pattern = "Overlay Gate Outcomes \(V033/V034/V035\)" },
    @{ Name = "V027 Regime Bucket Conditioning";      Pattern = "V027 Regime Bucket Conditioning" },
    @{ Name = "BAB Sleeve Activation";                Pattern = "BAB Sleeve Activation" },
    @{ Name = "§5B output template";                  Pattern = "## 5B\. Meta-Integration Variable Review" },
    @{ Name = "OVERLAY-GATE-BLOCKING-WINNERS flag";   Pattern = "OVERLAY-GATE-BLOCKING-WINNERS" },
    @{ Name = "OVERLAY-STAGING-MISSING-PERSISTENT";   Pattern = "OVERLAY-STAGING-MISSING-PERSISTENT" }
)
foreach ($chk in $checks) {
    $found = $c -match $chk.Pattern
    "{0,-40} {1}" -f $chk.Name, $(if ($found) { "OK" } else { "MISSING" })
}
```

Expected: all 7 checks `OK`.

## Rollback

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\signal-review\SKILL.md"
$backup = Get-ChildItem -Path "$path.bak-phase3-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Copy-Item $backup.FullName $path -Force
    Write-Host "Restored from $($backup.Name)"
} else {
    Write-Error "No pre-Phase-3 backup found — cannot auto-rollback"
}
```

## Sandbox note

Read-only mount applies; see the market-brief patch for context. `Excel-Sync-Protocol.md §3` may need a sibling update to enumerate the three new PerformanceStats sub-tables ("Overlay Gate Outcomes", "V027 Regime Bucket Conditioning", "BAB Sleeve Activation") — tracked as a GATE question in the fresh-session outcome file.
