# Phase 3 Patch — market-brief SKILL.md (meta-integration consumer)

**Source:** 2026-04-18 meta-integration deployment (`deployment-memo-2026-04-18.md`, `meta-analysis-integration-plan-2026-04-18.md`).
**Applies when:** 2026-04-25 shadow-mode review (`meta-shadow-review-2026-04-25.md`) returns GO verdicts for V029, V033, V034, V035. V030/V031/V032 remain MISSING and are NOT consumed by this patch.
**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\market-brief\SKILL.md`
**Scope test:** edits total ~700 bytes against the 13.8 KB SKILL.md (~5%) → minimum-surface edit, NOT full rewrite.

## Summary

Phase 3 wires three behaviors into `market-brief`:

1. **Read the meta-integration staging file.** `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` is produced by the 19:52 `preflight-meta-additions-1952pm` task, 8 minutes before the brief fires. The brief extracts the V033/V034/V035 Faber overlay gate state per sleeve, V029 BAB proxy spread, and V027 regime bucket.
2. **Surface overlay gate state in the regime block.** The Step 4 regime snapshot adds a dedicated line `Overlay gates: equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF}` so downstream consumers (trade-rec Step 1.5) read it without reparsing.
3. **Fail-loud on missing staging.** If the staging file is absent, the brief prints `Overlay gates: MISSING — meta-additions-staging file not produced` and flags `meta_staging=MISSING` in the DataQuality sheet. It does NOT fall back to prior-day state; the overlay read is binary and stale reads are prohibited (per `Methodology Prompt.md §Step 1.5` read-cadence rule).

No changes to scorecard columns. Overlay is non-additive to Sum; the |Sum|≥3 promotion logic is untouched. The brief is the authoritative reader of the staging file; the trade-rec consumes the overlay state from the brief's regime block OR re-reads the staging file directly (see companion patch `daily-trade-rec-phase3-SKILL-patch.md`).

## Before/after edits

### Edit 1 — Add Step 2.5 (new subsection after existing Step 2)

**Anchor (find exact text):**
```markdown
- If absent: mark all three as `MISSING — staging file not produced` in the variable table. This is correct fail-loud behavior.

## Step 3 — Pull all Grade A variables via the retrieval engine
```

**Replace with:**
```markdown
- If absent: mark all three as `MISSING — staging file not produced` in the variable table. This is correct fail-loud behavior.

## Step 2.5 — Read the meta-integration staging file (Phase 3, post-2026-04-25)

Check for `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` (today's date). This file is produced by the `preflight-meta-additions-1952pm` task at 19:52 — 8 minutes before this brief fires. It covers Phase 3 additions V029 (BAB proxy), V027 regime bucket, and V033/V034/V035 (Faber TAA overlay gates per sleeve). V030/V031/V032 remain MISSING by design (subscription / Phase 2b stub).

Extract:

- `overlay_gate_status` — the per-sleeve ON/OFF state from the V033/V034/V035 Faber table. Format as `equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF}` (and `international={ON|OFF}` if the optional EFA row is present).
- `v027_regime_bucket` — one of `expansion` (z > +0.5σ), `neutral` (−1σ ≤ z ≤ +0.5σ), `contraction` (z < −1σ). Source: today's V027 row in the staging file's reconciliation table.
- `v029_bab_spread` — the USMV − SPLV 12m spread percentage; sign tells BAB vs ANTI-BAB regime.

**Fail-loud rule.** If the staging file is absent, set `overlay_gate_status = "MISSING"`, `v027_regime_bucket = "MISSING"`, and log `meta_staging=MISSING` in the Step 9 DataQuality row. Do NOT carry forward yesterday's overlay state — overlay reads are end-of-month binary; a stale read is worse than no read. Downstream trade-rec Step 1.5 must block any Phase-3-gated sleeve if `overlay_gate_status = "MISSING"`.

**Read cadence reminder.** The overlay state flips only at end-of-month close (per `Methodology Prompt.md §Step 1.5`); intraday recompute is prohibited. The brief reads today's staging file and reports it verbatim.

## Step 3 — Pull all Grade A variables via the retrieval engine
```

### Edit 2 — Extend Step 4 regime snapshot output to include overlay gate line

**Anchor (find exact text):**
```markdown
Output: one-line regime label + three primary regime variables being watched.

Compare against the prior regime label (from the latest row in `master-data-log.xlsx` RegimeHistory sheet, read in Step 1). If the label changed, call it out explicitly.
```

**Replace with:**
```markdown
Output: one-line regime label + three primary regime variables being watched.

**Overlay gate line (Phase 3, added 2026-04-25):** append a dedicated line below the regime label:

```
Overlay gates (Step 1.5): equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF} — source: meta-additions-staging-{YYYY-MM-DD}.md (V033/V034/V035 Faber TAA)
V027 regime bucket: {expansion|neutral|contraction}  |  V029 BAB spread: {+X.XX%} ({BAB|ANTI-BAB})
```

If `overlay_gate_status = "MISSING"`, render `Overlay gates: MISSING — meta-additions-staging file not produced. Downstream trade-rec must block Phase-3-gated sleeves.` and continue — do NOT silently infer.

Compare against the prior regime label (from the latest row in `master-data-log.xlsx` RegimeHistory sheet, read in Step 1). If the label changed, call it out explicitly.
```

### Edit 3 — Extend Step 9 DataQuality row to log meta-staging status

**Anchor (find exact text):**
```markdown
3. **DataQuality** — append one row: Date, Total_GradeA_Vars, Missing_Count, Missing_Rate_Pct, Missing_Variables, Stale_Count, Stale_Variables, Audit_ResidMom_Status / Audit_IntCap_Status / Audit_BasisMom_Status (LIVE/MISSING/STALE), Pipeline_Health, Source_Brief, Notes.
```

**Replace with:**
```markdown
3. **DataQuality** — append one row: Date, Total_GradeA_Vars, Missing_Count, Missing_Rate_Pct, Missing_Variables, Stale_Count, Stale_Variables, Audit_ResidMom_Status / Audit_IntCap_Status / Audit_BasisMom_Status (LIVE/MISSING/STALE), **Meta_Staging_Status (OK/MISSING) — from Step 2.5**, Pipeline_Health, Source_Brief, Notes.
```

## PowerShell apply block (idempotent)

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\market-brief\SKILL.md"
if (-not (Test-Path $path)) { Write-Error "SKILL.md not found at $path"; exit 1 }

$content = Get-Content $path -Raw

# Idempotence — unique marker only present after patch
if ($content -match "Step 2\.5 — Read the meta-integration staging file \(Phase 3") {
    Write-Host "market-brief Phase 3 patch already applied — skipping"
    exit 0
}

# Edit 1 — Insert Step 2.5 before Step 3
$edit1Anchor  = "- If absent: mark all three as ``MISSING — staging file not produced`` in the variable table. This is correct fail-loud behavior.`r`n`r`n## Step 3 — Pull all Grade A variables via the retrieval engine"
$edit1Replace = @'
- If absent: mark all three as `MISSING — staging file not produced` in the variable table. This is correct fail-loud behavior.

## Step 2.5 — Read the meta-integration staging file (Phase 3, post-2026-04-25)

Check for `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` (today's date). This file is produced by the `preflight-meta-additions-1952pm` task at 19:52 — 8 minutes before this brief fires. It covers Phase 3 additions V029 (BAB proxy), V027 regime bucket, and V033/V034/V035 (Faber TAA overlay gates per sleeve). V030/V031/V032 remain MISSING by design (subscription / Phase 2b stub).

Extract:

- `overlay_gate_status` — the per-sleeve ON/OFF state from the V033/V034/V035 Faber table. Format as `equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF}` (and `international={ON|OFF}` if the optional EFA row is present).
- `v027_regime_bucket` — one of `expansion` (z > +0.5σ), `neutral` (−1σ ≤ z ≤ +0.5σ), `contraction` (z < −1σ). Source: today's V027 row in the staging file's reconciliation table.
- `v029_bab_spread` — the USMV − SPLV 12m spread percentage; sign tells BAB vs ANTI-BAB regime.

**Fail-loud rule.** If the staging file is absent, set `overlay_gate_status = "MISSING"`, `v027_regime_bucket = "MISSING"`, and log `meta_staging=MISSING` in the Step 9 DataQuality row. Do NOT carry forward yesterday's overlay state — overlay reads are end-of-month binary; a stale read is worse than no read. Downstream trade-rec Step 1.5 must block any Phase-3-gated sleeve if `overlay_gate_status = "MISSING"`.

**Read cadence reminder.** The overlay state flips only at end-of-month close (per `Methodology Prompt.md §Step 1.5`); intraday recompute is prohibited. The brief reads today's staging file and reports it verbatim.

## Step 3 — Pull all Grade A variables via the retrieval engine
'@
if (-not $content.Contains($edit1Anchor)) { Write-Error "Edit 1 anchor not found — aborting (SKILL.md drifted from snapshot)"; exit 1 }
$content = $content.Replace($edit1Anchor, $edit1Replace)

# Edit 2 — Extend Step 4 regime snapshot output
$edit2Anchor  = "Output: one-line regime label + three primary regime variables being watched.`r`n`r`nCompare against the prior regime label"
$edit2Replace = @'
Output: one-line regime label + three primary regime variables being watched.

**Overlay gate line (Phase 3, added 2026-04-25):** append a dedicated line below the regime label:

```
Overlay gates (Step 1.5): equity={ON|OFF}, commodity={ON|OFF}, crypto={ON|OFF} — source: meta-additions-staging-{YYYY-MM-DD}.md (V033/V034/V035 Faber TAA)
V027 regime bucket: {expansion|neutral|contraction}  |  V029 BAB spread: {+X.XX%} ({BAB|ANTI-BAB})
```

If `overlay_gate_status = "MISSING"`, render `Overlay gates: MISSING — meta-additions-staging file not produced. Downstream trade-rec must block Phase-3-gated sleeves.` and continue — do NOT silently infer.

Compare against the prior regime label
'@
if (-not $content.Contains($edit2Anchor)) { Write-Error "Edit 2 anchor not found — aborting"; exit 1 }
$content = $content.Replace($edit2Anchor, $edit2Replace)

# Edit 3 — Extend DataQuality row schema in Step 9
$edit3Anchor  = "Audit_ResidMom_Status / Audit_IntCap_Status / Audit_BasisMom_Status (LIVE/MISSING/STALE), Pipeline_Health"
$edit3Replace = "Audit_ResidMom_Status / Audit_IntCap_Status / Audit_BasisMom_Status (LIVE/MISSING/STALE), **Meta_Staging_Status (OK/MISSING) — from Step 2.5**, Pipeline_Health"
if (-not $content.Contains($edit3Anchor)) { Write-Error "Edit 3 anchor not found — aborting"; exit 1 }
$content = $content.Replace($edit3Anchor, $edit3Replace)

# Backup then write
$backup = "$path.bak-phase3-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $path $backup
Set-Content $path $content -NoNewline
Write-Host "market-brief Phase 3 patch applied. Backup: $backup"
```

## Verify

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\market-brief\SKILL.md"
$c = Get-Content $path -Raw
$checks = @(
    @{ Name = "Step 2.5 header";           Pattern = "Step 2\.5 — Read the meta-integration staging file" },
    @{ Name = "Overlay gate line anchor";  Pattern = "Overlay gates \(Step 1\.5\)" },
    @{ Name = "DataQuality meta col";      Pattern = "Meta_Staging_Status \(OK/MISSING\)" },
    @{ Name = "Fail-loud rule";            Pattern = "overlay reads are end-of-month binary" }
)
foreach ($chk in $checks) {
    $found = $c -match $chk.Pattern
    "{0,-30} {1}" -f $chk.Name, $(if ($found) { "OK" } else { "MISSING" })
}
```

Expected: all 4 checks `OK`. After applying, the next brief fire (`daily-market-brief-8pm-v2`) should surface overlay gate state in §1 Regime Snapshot.

## Rollback

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\market-brief\SKILL.md"
# Restore most recent backup
$backup = Get-ChildItem -Path "$path.bak-phase3-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Copy-Item $backup.FullName $path -Force
    Write-Host "Restored from $($backup.Name)"
} else {
    Write-Error "No pre-Phase-3 backup found — cannot auto-rollback"
}
```

## Sandbox note

Patch written in Cowork sandbox 2026-04-18 against the in-mount snapshot of SKILL.md. Apply must happen Windows-side because `/mnt/.claude/skills/*/SKILL.md` is mounted read-only in the sandbox. If Gerald chooses to extract the shipped `skill-manager.zip` (from `/mnt/Trade/skills-draft/skill-manager.zip`) before applying, this patch is compatible with skill-manager's patch-mode consumption (summary + edits + PowerShell all match the format).
