# Phase 3 Patch — positions-monitor SKILL.md (meta-integration consumer)

**Source:** 2026-04-18 meta-integration deployment (`deployment-memo-2026-04-18.md`).
**Applies when:** 2026-04-25 shadow-mode review returns GO verdicts for V033, V034, V035. V029 and V030 do NOT directly affect positions-monitor (they're sleeve-weight inputs, not per-position triggers).
**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\positions-monitor\SKILL.md`
**Scope test:** edits total ~550 bytes against the ~3.5 KB SKILL.md (~16%) → right at threshold; staying with minimum-surface edits because the file has a tight flag-panel convention and adding one row + one read preserves it.

## Summary

Phase 3 adds one flag to the panel and one required read:

1. **New flag F11 `overlay_sleeve_off`** — CRITICAL severity. Fires when a live position's sleeve has flipped OFF between entry and today. A live position whose sleeve was ON when Gerald entered but flipped OFF at the next month-end close signals two things: (a) the drawdown circuit-breaker (Risk Rules §4.B) now argues against adding exposure to that sleeve, and (b) Gerald should review whether the thesis still holds given the sleeve's trend break. This is NOT an auto-close signal — Gerald decides — but it IS a flagged change of state.
2. **New required read of the meta-additions staging file** — needed to know today's overlay gate status. If the staging file is missing, the skill writes a MISSING flag but does NOT fall back to stale state (same fail-loud rule as market-brief and daily-trade-rec Phase 3 patches).

No changes to the silent-when-OK philosophy. No changes to the 7-step workflow beyond the new flag computation inside Step 3. No changes to Memory.md writes.

## Before/after edits

### Edit 1 — Add meta-additions-staging to required reads

**Anchor:**
```markdown
## REQUIRED READS (and nothing else unless triggered)
1. `/mnt/Trade/Memory.md` — §2 Open Positions, §3 Regime, §7 Closed Trades
2. `/mnt/Trade/.pipeline-status.json` (if present)
3. Latest `us-close-snapshot-YYYY-MM-DD.md` (today's 07:30 file if present)

Do NOT read the market brief, trade rec, core docs, Methodology Prompt, Risk Rules, or Data Sources. They are irrelevant at monitoring time. This skill explicitly overrides the CLAUDE.md §Session Startup Protocol for utility reasons.
```

**Replace with:**
```markdown
## REQUIRED READS (and nothing else unless triggered)
1. `/mnt/Trade/Memory.md` — §2 Open Positions, §3 Regime, §7 Closed Trades
2. `/mnt/Trade/.pipeline-status.json` (if present)
3. Latest `us-close-snapshot-YYYY-MM-DD.md` (today's 07:30 file if present)
4. **(Phase 3, post-2026-04-25)** Latest `/mnt/Trade/meta-additions-staging-YYYY-MM-DD.md` — read to evaluate flag F11 (overlay_sleeve_off). Extract today's per-sleeve `overlay_gate_status` (equity / commodity / crypto / international) and compare against the sleeve-at-entry recorded in Memory.md §2 Open Positions for each live row. If staging is missing, F11 fires for all positions with Severity=HIGH and `reason=OverlayStagingMissing`.

Do NOT read the market brief, trade rec, core docs, Methodology Prompt, Risk Rules, or Data Sources. They are irrelevant at monitoring time. This skill explicitly overrides the CLAUDE.md §Session Startup Protocol for utility reasons.
```

### Edit 2 — Add F11 to the flag panel table

**Anchor:**
```markdown
| F10 correlation_gate | two or more positions with pairwise \|ρ_60d\| > 0.7 loaded concurrently | MED |
```

**Replace with:**
```markdown
| F10 correlation_gate | two or more positions with pairwise \|ρ_60d\| > 0.7 loaded concurrently | MED |
| F11 overlay_sleeve_off | position's sleeve is gated OFF today AND was ON at entry (i.e., flipped since entry) — per Methodology Prompt §Step 1.5 / Risk Rules §4.B | CRITICAL |
```

### Edit 3 — Clarify F11 evaluation rules (add note after flag-panel table)

**Anchor:**
```markdown
| F11 overlay_sleeve_off | position's sleeve is gated OFF today AND was ON at entry (i.e., flipped since entry) — per Methodology Prompt §Step 1.5 / Risk Rules §4.B | CRITICAL |

## Workflow — 7 steps
```

**Replace with:**
```markdown
| F11 overlay_sleeve_off | position's sleeve is gated OFF today AND was ON at entry (i.e., flipped since entry) — per Methodology Prompt §Step 1.5 / Risk Rules §4.B | CRITICAL |

**F11 evaluation rules (Phase 3, added 2026-04-25):**

- Map each live position's asset → sleeve: equities/ETFs → equity sleeve (V033 SPY gate); EWJ/EWY → international equity (optional V033 EFA gate); commodities → commodity sleeve (V034 GSCI gate); BTC/ETH → crypto sleeve (V035 BTC-USD gate); FX and rates → not gated (F11 never fires).
- Retrieve the sleeve-status-at-entry from Memory.md §2 Notes (daily-trade-rec Phase 3 records this under the `overlay_at_entry` key; if missing on an older entry, treat as ON = prior-to-Phase-3 default).
- F11 fires only on transitions: ON-at-entry → OFF-today. A position that was entered when the sleeve was OFF (shouldn't happen post-Phase-3 because daily-trade-rec would have blocked it, but still possible for manual entries) is flagged under F8 thesis_var instead, not F11.
- Action recommendation for F11: "Sleeve overlay flipped OFF since entry — Gerald review thesis; do NOT auto-close. Consider trim or tighter stop per Risk Rules §4.B drawdown-gate interaction."
- MISSING staging → F11 fires on EVERY live position with Severity=HIGH and reason='OverlayStagingMissing' until the pipeline health is restored.

## Workflow — 7 steps
```

## PowerShell apply block (idempotent)

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor\SKILL.md"
if (-not (Test-Path $path)) { Write-Error "SKILL.md not found at $path"; exit 1 }

$content = Get-Content $path -Raw

if ($content -match "F11 overlay_sleeve_off") {
    Write-Host "positions-monitor Phase 3 patch already applied — skipping"
    exit 0
}

# --- Edit 1 — Add meta-additions-staging to required reads ---
$e1Anchor  = "3. Latest ``us-close-snapshot-YYYY-MM-DD.md`` (today's 07:30 file if present)`r`n`r`nDo NOT read the market brief"
$e1Replace = @'
3. Latest `us-close-snapshot-YYYY-MM-DD.md` (today's 07:30 file if present)
4. **(Phase 3, post-2026-04-25)** Latest `/mnt/Trade/meta-additions-staging-YYYY-MM-DD.md` — read to evaluate flag F11 (overlay_sleeve_off). Extract today's per-sleeve `overlay_gate_status` (equity / commodity / crypto / international) and compare against the sleeve-at-entry recorded in Memory.md §2 Open Positions for each live row. If staging is missing, F11 fires for all positions with Severity=HIGH and `reason=OverlayStagingMissing`.

Do NOT read the market brief
'@
if (-not $content.Contains($e1Anchor)) { Write-Error "Edit 1 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e1Anchor, $e1Replace)

# --- Edit 2 + 3 — Add F11 row + evaluation rules (combined anchor for atomicity) ---
$e23Anchor  = "| F10 correlation_gate | two or more positions with pairwise \|ρ_60d\| > 0.7 loaded concurrently | MED |`r`n`r`n## Workflow — 7 steps"
$e23Replace = @'
| F10 correlation_gate | two or more positions with pairwise \|ρ_60d\| > 0.7 loaded concurrently | MED |
| F11 overlay_sleeve_off | position's sleeve is gated OFF today AND was ON at entry (i.e., flipped since entry) — per Methodology Prompt §Step 1.5 / Risk Rules §4.B | CRITICAL |

**F11 evaluation rules (Phase 3, added 2026-04-25):**

- Map each live position's asset → sleeve: equities/ETFs → equity sleeve (V033 SPY gate); EWJ/EWY → international equity (optional V033 EFA gate); commodities → commodity sleeve (V034 GSCI gate); BTC/ETH → crypto sleeve (V035 BTC-USD gate); FX and rates → not gated (F11 never fires).
- Retrieve the sleeve-status-at-entry from Memory.md §2 Notes (daily-trade-rec Phase 3 records this under the `overlay_at_entry` key; if missing on an older entry, treat as ON = prior-to-Phase-3 default).
- F11 fires only on transitions: ON-at-entry → OFF-today. A position that was entered when the sleeve was OFF (shouldn't happen post-Phase-3 because daily-trade-rec would have blocked it, but still possible for manual entries) is flagged under F8 thesis_var instead, not F11.
- Action recommendation for F11: "Sleeve overlay flipped OFF since entry — Gerald review thesis; do NOT auto-close. Consider trim or tighter stop per Risk Rules §4.B drawdown-gate interaction."
- MISSING staging → F11 fires on EVERY live position with Severity=HIGH and reason='OverlayStagingMissing' until the pipeline health is restored.

## Workflow — 7 steps
'@
if (-not $content.Contains($e23Anchor)) { Write-Error "Edit 2/3 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e23Anchor, $e23Replace)

# Backup + write
$backup = "$path.bak-phase3-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $path $backup
Set-Content $path $content -NoNewline
Write-Host "positions-monitor Phase 3 patch applied. Backup: $backup"
```

## Verify

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor\SKILL.md"
$c = Get-Content $path -Raw
$checks = @(
    @{ Name = "Required read #4 (staging)";      Pattern = "meta-additions-staging-YYYY-MM-DD\.md" },
    @{ Name = "F11 flag row";                    Pattern = "F11 overlay_sleeve_off" },
    @{ Name = "F11 evaluation rules";            Pattern = "F11 evaluation rules \(Phase 3" },
    @{ Name = "Sleeve mapping rule";             Pattern = "V033 SPY gate" },
    @{ Name = "MISSING staging fail-loud rule";  Pattern = "OverlayStagingMissing" }
)
foreach ($chk in $checks) {
    $found = $c -match $chk.Pattern
    "{0,-32} {1}" -f $chk.Name, $(if ($found) { "OK" } else { "MISSING" })
}
```

Expected: all 5 checks `OK`. On the next `positions-monitor-intraday-9am` fire, the flag panel evaluates F11; on silent-OK days (no flags fired) no file is written — the change is invisible until a sleeve actually flips.

## Rollback

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor\SKILL.md"
$backup = Get-ChildItem -Path "$path.bak-phase3-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Copy-Item $backup.FullName $path -Force
    Write-Host "Restored from $($backup.Name)"
} else {
    Write-Error "No pre-Phase-3 backup found — cannot auto-rollback"
}
```

## Sandbox note

F11 depends on `overlay_at_entry` being recorded in Memory.md §2 Notes at entry time. The daily-trade-rec Phase 3 patch writes this on promotion, and the trade-update skill should write it on manual entries — that's a follow-on item NOT covered in this Phase 3 batch (it would touch the trade-update SKILL.md, which isn't in scope). If `overlay_at_entry` is missing for a live position when F11 runs, the default is ON (prior-to-Phase-3 positions) and F11 will not misfire. Flagged as a GATE question in the fresh-session outcome file for Gerald to decide whether trade-update needs its own Phase 3 patch.
