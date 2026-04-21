# Phase 3 Patch — quarterly-methodology-review SKILL.md (meta-integration consumer)

**Source:** 2026-04-18 meta-integration deployment (`deployment-memo-2026-04-18.md`).
**Applies when:** 2026-04-25 shadow-mode review returns GO verdicts for V029, V033, V034, V035.
**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\quarterly-methodology-review\SKILL.md`
**Scope test:** edits total ~900 bytes against the ~14 KB SKILL.md (~6%) → minimum-surface edit, NOT full rewrite.

## Summary

Phase 3 extends the Step 3 Research Core Reconciliation loop and Step 4 Variable Candidate Pipeline to cover V029 / V033 / V034 / V035 (the four variables that received or will receive GO verdicts in the 2026-04-25 shadow review). V030 / V031 / V032 remain MISSING by design and get their own dedicated subsection for transparency.

Specifically:

1. **Step 3 loop extends from entries 1–28 to entries 1–35** (V029–V035 appended via the 2026-04-18 meta-integration).
2. **New dedicated subsection in Step 3** for the meta-integration cohort, mirroring the existing audit-addition subsection (residual momentum / intermediary capital / basis-momentum). Reads new SignalLedger cols 33–36 via `master-data-log.xlsx` and new PerformanceStats tables ("Overlay Gate Outcomes", "V027 Regime Bucket Conditioning", "BAB Sleeve Activation") produced by the signal-review Phase 3 patch.
3. **Step 4 pipeline extends** the tier taxonomy to track V030 / V031 / V032 explicitly as subscription-or-stub-blocked candidates with next-review markers.
4. **Step 9 auto-memory file** includes the Phase 3 cohort status in the quarterly review memory alongside the Batch-1 audit cohort.

No changes to Step 2 (Dimension Fitness Audit) because the new signal-review dimensions added in Phase 3 are themselves subject to quarterly fitness audit starting at the 2026-07-01 quarterly review — the first one with shadow-plus-live data to judge. Step 2 pickup happens automatically once this patch is applied.

## Before/after edits

### Edit 1 — Extend Step 3 range reference and add Phase 3 cohort subsection

**Anchor:**
```markdown
**For the three audit-addition variables specifically (residual momentum, intermediary capital, basis-momentum):**

4. Read the **AuditAdditionLog** sheet in `master-data-log.xlsx`. Count the entries. Are they contributing to scoring decisions? The 2026-10-14 review deadline is the hard gate — if they haven't contributed by then, they get demoted to Grade B.

5. Check the signal-review's §6 (Audit-Addition Variable Review) across all weekly reviews. Is there a pattern? Is one variable consistently blocking signals that would have won? Is another consistently contributing to winners?

**Output a reconciliation table:**
```

**Replace with:**
```markdown
**For the three audit-addition variables specifically (residual momentum, intermediary capital, basis-momentum):**

4. Read the **AuditAdditionLog** sheet in `master-data-log.xlsx`. Count the entries. Are they contributing to scoring decisions? The 2026-10-14 review deadline is the hard gate — if they haven't contributed by then, they get demoted to Grade B.

5. Check the signal-review's §6 (Audit-Addition Variable Review) across all weekly reviews. Is there a pattern? Is one variable consistently blocking signals that would have won? Is another consistently contributing to winners?

**For the meta-integration cohort V029 / V033 / V034 / V035 (Phase 3, added 2026-04-25):**

6. Read **SignalLedger cols 33–36** (`overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`) via openpyxl. Count rows by gate-ON vs gate-OFF per sleeve and by V027 bucket.

7. Read the three new **PerformanceStats** sub-tables produced by signal-review Phase 3: "Overlay Gate Outcomes", "V027 Regime Bucket Conditioning", "BAB Sleeve Activation". These give gate_protection_pp per sleeve, bucket-conditional win rates, and BAB activation win-rate splits.

8. Reconcile against the meta-analysis PL-NMA projections in `Methodology Prompt.md` — V029 post-decay Sharpe 0.4–0.8; V033–V035 Faber TAA as gate (no alpha, drawdown reduction instead, target: reduced max-DD on gated sleeves vs. un-gated counterfactual). Is realized behavior inside the projected range? Is the gate actually protecting drawdowns?

9. **V030 / V031 / V032 — explicit-MISSING tracking.** V030 DealerGamma stays MISSING until Gerald confirms a SqueezeMetrics or SpotGamma subscription; next decision point is 2026-07-01 (this review or the next). V031 GP/A and V032 CEI stay MISSING until the Phase 2b compute stubs land (Ken French GP fetcher / CRSP+Compustat CEI compute). For each MISSING variable, record: weeks_missing, blocker_reason, next_review_target. If any MISSING variable crosses 180 days (2026-10-14), it auto-flags for demotion review alongside the Batch-1 audit cohort.

**2026-10-14 shared review reminder.** V029 / V033–V035 share the 2026-10-14 six-month review date with V026–V028 (Batch-1 audit additions). The October quarterly review is the hard gate for the meta-integration cohort — formal GO/DOWNGRADE/RETIRE per variable based on OOS contribution evidence.

**Output a reconciliation table:**
```

### Edit 2 — Extend the reconciliation table header to note meta cohort

**Anchor:**
```markdown
**Output a reconciliation table:**

| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |
|----------|-------|---------------------|------------------------|-----------------|--------|

Actions: CONFIRMED (grade holds), WATCH (emerging concern), DOWNGRADE CANDIDATE (evidence against), UPGRADE CANDIDATE (evidence for), DATA GAP (can't assess).
```

**Replace with:**
```markdown
**Output a reconciliation table** (extended Phase 3 to entries 1–35; V029–V035 appended):

| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |
|----------|-------|---------------------|------------------------|-----------------|--------|

Actions: CONFIRMED (grade holds), WATCH (emerging concern), DOWNGRADE CANDIDATE (evidence against), UPGRADE CANDIDATE (evidence for), DATA GAP (can't assess), SUBSCRIPTION-BLOCKED (V030 only, until subscription live), STUB-BLOCKED (V031/V032 only, until Phase 2b compute implemented).
```

### Edit 3 — Extend Step 4 Tier 2 candidates with meta-integration stubs

**Anchor:**
```markdown
**Tier 2 candidates (need data collection infrastructure):**
- GEX (gamma exposure) as regime overlay — positive/negative GEX predicts mean-reversion vs trend-following
- Cross-asset lead-lag exploitation — BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX
- Correlation-regime signal quality — trailing 20d cross-asset correlation as quality filter
```

**Replace with:**
```markdown
**Tier 2 candidates (need data collection infrastructure):**
- GEX (gamma exposure) as regime overlay — positive/negative GEX predicts mean-reversion vs trend-following
- Cross-asset lead-lag exploitation — BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX
- Correlation-regime signal quality — trailing 20d cross-asset correlation as quality filter

**Meta-integration stubs (Phase 3, added 2026-04-25 — candidates pending data-pipeline implementation):**
- **V030 DealerGamma** — subscription-blocked. Recommended action per review: RENEW-BLOCK if Gerald has not confirmed subscription; PROMOTE-TO-LIVE if confirmed and one week of staging data available.
- **V031 GP/A (Novy-Marx 2013)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if Ken French GP-portfolio CSV fetcher landed; DEFER otherwise.
- **V032 CEI (Daniel-Titman 2006)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if CRSP+Compustat self-compute landed; DEFER otherwise.
```

### Edit 4 — Extend Step 9 auto-memory scope

**Anchor:**
```markdown
## Step 9 — Update auto-memory

Create or update the memory file for this review:
- File: `/mnt/.auto-memory/project_quarterly_review_{YYYY-MM-DD}.md`
- Content: key decisions made, dimensions retained/demoted, variable pipeline status, next review date
- Update `MEMORY.md` index with a pointer
```

**Replace with:**
```markdown
## Step 9 — Update auto-memory

Create or update the memory file for this review:
- File: `/mnt/.auto-memory/project_quarterly_review_{YYYY-MM-DD}.md`
- Content: key decisions made, dimensions retained/demoted, variable pipeline status, next review date
- **Phase 3 addition (2026-04-25):** include explicit status line for the meta-integration cohort — V029/V033/V034/V035 reconciliation verdicts, V030 subscription state, V031/V032 stub state, and shared-2026-10-14-review reminder
- Update `MEMORY.md` index with a pointer
```

## PowerShell apply block (idempotent)

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\quarterly-methodology-review\SKILL.md"
if (-not (Test-Path $path)) { Write-Error "SKILL.md not found at $path"; exit 1 }

$content = Get-Content $path -Raw

if ($content -match "meta-integration cohort V029 / V033 / V034 / V035") {
    Write-Host "quarterly-methodology-review Phase 3 patch already applied — skipping"
    exit 0
}

# --- Edit 1 — Insert meta-integration cohort subsection into Step 3 ---
$e1Anchor  = "5. Check the signal-review's §6 (Audit-Addition Variable Review) across all weekly reviews. Is there a pattern? Is one variable consistently blocking signals that would have won? Is another consistently contributing to winners?`r`n`r`n**Output a reconciliation table:**"
$e1Replace = @'
5. Check the signal-review's §6 (Audit-Addition Variable Review) across all weekly reviews. Is there a pattern? Is one variable consistently blocking signals that would have won? Is another consistently contributing to winners?

**For the meta-integration cohort V029 / V033 / V034 / V035 (Phase 3, added 2026-04-25):**

6. Read **SignalLedger cols 33–36** (`overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`) via openpyxl. Count rows by gate-ON vs gate-OFF per sleeve and by V027 bucket.

7. Read the three new **PerformanceStats** sub-tables produced by signal-review Phase 3: "Overlay Gate Outcomes", "V027 Regime Bucket Conditioning", "BAB Sleeve Activation". These give gate_protection_pp per sleeve, bucket-conditional win rates, and BAB activation win-rate splits.

8. Reconcile against the meta-analysis PL-NMA projections in `Methodology Prompt.md` — V029 post-decay Sharpe 0.4–0.8; V033–V035 Faber TAA as gate (no alpha, drawdown reduction instead, target: reduced max-DD on gated sleeves vs. un-gated counterfactual). Is realized behavior inside the projected range? Is the gate actually protecting drawdowns?

9. **V030 / V031 / V032 — explicit-MISSING tracking.** V030 DealerGamma stays MISSING until Gerald confirms a SqueezeMetrics or SpotGamma subscription; next decision point is 2026-07-01 (this review or the next). V031 GP/A and V032 CEI stay MISSING until the Phase 2b compute stubs land (Ken French GP fetcher / CRSP+Compustat CEI compute). For each MISSING variable, record: weeks_missing, blocker_reason, next_review_target. If any MISSING variable crosses 180 days (2026-10-14), it auto-flags for demotion review alongside the Batch-1 audit cohort.

**2026-10-14 shared review reminder.** V029 / V033–V035 share the 2026-10-14 six-month review date with V026–V028 (Batch-1 audit additions). The October quarterly review is the hard gate for the meta-integration cohort — formal GO/DOWNGRADE/RETIRE per variable based on OOS contribution evidence.

**Output a reconciliation table:**
'@
if (-not $content.Contains($e1Anchor)) { Write-Error "Edit 1 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e1Anchor, $e1Replace)

# --- Edit 2 — Extend reconciliation table note + action legend ---
$e2Anchor  = "**Output a reconciliation table:**`r`n`r`n| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |`r`n|----------|-------|---------------------|------------------------|-----------------|--------|`r`n`r`nActions: CONFIRMED (grade holds), WATCH (emerging concern), DOWNGRADE CANDIDATE (evidence against), UPGRADE CANDIDATE (evidence for), DATA GAP (can't assess)."
$e2Replace = @'
**Output a reconciliation table** (extended Phase 3 to entries 1–35; V029–V035 appended):

| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |
|----------|-------|---------------------|------------------------|-----------------|--------|

Actions: CONFIRMED (grade holds), WATCH (emerging concern), DOWNGRADE CANDIDATE (evidence against), UPGRADE CANDIDATE (evidence for), DATA GAP (can't assess), SUBSCRIPTION-BLOCKED (V030 only, until subscription live), STUB-BLOCKED (V031/V032 only, until Phase 2b compute implemented).
'@
if (-not $content.Contains($e2Anchor)) { Write-Error "Edit 2 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e2Anchor, $e2Replace)

# --- Edit 3 — Extend Step 4 Tier 2 candidates with V030/V031/V032 ---
$e3Anchor  = "**Tier 2 candidates (need data collection infrastructure):**`r`n- GEX (gamma exposure) as regime overlay — positive/negative GEX predicts mean-reversion vs trend-following`r`n- Cross-asset lead-lag exploitation — BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX`r`n- Correlation-regime signal quality — trailing 20d cross-asset correlation as quality filter"
$e3Replace = @'
**Tier 2 candidates (need data collection infrastructure):**
- GEX (gamma exposure) as regime overlay — positive/negative GEX predicts mean-reversion vs trend-following
- Cross-asset lead-lag exploitation — BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX
- Correlation-regime signal quality — trailing 20d cross-asset correlation as quality filter

**Meta-integration stubs (Phase 3, added 2026-04-25 — candidates pending data-pipeline implementation):**
- **V030 DealerGamma** — subscription-blocked. Recommended action per review: RENEW-BLOCK if Gerald has not confirmed subscription; PROMOTE-TO-LIVE if confirmed and one week of staging data available.
- **V031 GP/A (Novy-Marx 2013)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if Ken French GP-portfolio CSV fetcher landed; DEFER otherwise.
- **V032 CEI (Daniel-Titman 2006)** — stub-blocked. Recommended action: PROMOTE-TO-PHASE-2B if CRSP+Compustat self-compute landed; DEFER otherwise.
'@
if (-not $content.Contains($e3Anchor)) { Write-Error "Edit 3 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e3Anchor, $e3Replace)

# --- Edit 4 — Extend Step 9 auto-memory instructions ---
$e4Anchor  = "- Content: key decisions made, dimensions retained/demoted, variable pipeline status, next review date`r`n- Update ``MEMORY.md`` index with a pointer"
$e4Replace = @'
- Content: key decisions made, dimensions retained/demoted, variable pipeline status, next review date
- **Phase 3 addition (2026-04-25):** include explicit status line for the meta-integration cohort — V029/V033/V034/V035 reconciliation verdicts, V030 subscription state, V031/V032 stub state, and shared-2026-10-14-review reminder
- Update `MEMORY.md` index with a pointer
'@
if (-not $content.Contains($e4Anchor)) { Write-Error "Edit 4 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e4Anchor, $e4Replace)

# Backup + write
$backup = "$path.bak-phase3-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $path $backup
Set-Content $path $content -NoNewline
Write-Host "quarterly-methodology-review Phase 3 patch applied. Backup: $backup"
```

## Verify

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\quarterly-methodology-review\SKILL.md"
$c = Get-Content $path -Raw
$checks = @(
    @{ Name = "Meta-integration cohort block";        Pattern = "meta-integration cohort V029 / V033 / V034 / V035" },
    @{ Name = "SignalLedger cols 33–36 read";         Pattern = "SignalLedger cols 33–36" },
    @{ Name = "PerformanceStats sub-tables read";     Pattern = "Overlay Gate Outcomes"" }'?.substring(0,30) } # keep simple
)
# Simpler run
$patterns = @(
  "meta-integration cohort V029 / V033 / V034 / V035",
  "SignalLedger cols 33–36",
  "Overlay Gate Outcomes",
  "V030 DealerGamma",
  "SUBSCRIPTION-BLOCKED",
  "2026-10-14 shared review reminder"
)
foreach ($p in $patterns) {
    $found = $c -match [regex]::Escape($p)
    "{0,-48} {1}" -f $p, $(if ($found) { "OK" } else { "MISSING" })
}
```

Expected: all 6 checks `OK`.

## Rollback

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\quarterly-methodology-review\SKILL.md"
$backup = Get-ChildItem -Path "$path.bak-phase3-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Copy-Item $backup.FullName $path -Force
    Write-Host "Restored from $($backup.Name)"
} else {
    Write-Error "No pre-Phase-3 backup found — cannot auto-rollback"
}
```

## Sandbox note

First production fire of this patch is the **2026-07-01 quarterly review**, ~10 weeks post-apply. By then the SignalLedger will have accumulated shadow-plus-live signals with cols 33–36 populated. If signal-review Phase 3 is NOT applied simultaneously, Step 3 item 7 will find the three new PerformanceStats tables empty — the quarterly review still runs but flags DATA GAP for each. Apply both patches together when the 2026-04-25 review returns GO verdicts.
