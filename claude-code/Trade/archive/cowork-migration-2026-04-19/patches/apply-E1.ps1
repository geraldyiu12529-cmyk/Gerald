# apply-E1.ps1
# Applies the two E1 read-override prepends to the scheduled-task SKILL.md files.
# Idempotent: safe to re-run. Creates a timestamped .bak before modifying.
#
# Usage:
#   Right-click -> Run with PowerShell
#   OR from a PowerShell prompt:  powershell -ExecutionPolicy Bypass -File .\apply-E1.ps1

$ErrorActionPreference = 'Stop'
$claudeRoot = Join-Path $env:USERPROFILE 'Documents\Claude'

function Apply-Prepend {
    param(
        [string]$Label,
        [string]$TargetFile,
        [string]$Marker,
        [string]$PrependText
    )

    if (-not (Test-Path $TargetFile)) {
        Write-Host "[$Label] FAILED — file not found: $TargetFile" -ForegroundColor Red
        return
    }

    $content = Get-Content $TargetFile -Raw
    if ($content -match [regex]::Escape($Marker)) {
        Write-Host "[$Label] SKIPPED — prepend already present in $TargetFile" -ForegroundColor Yellow
        return
    }

    $backup = "$TargetFile.bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $TargetFile $backup
    Set-Content -Path $TargetFile -Value ($PrependText + $content) -NoNewline -Encoding UTF8
    Write-Host "[$Label] APPLIED — prepend added; backup at $backup" -ForegroundColor Green
}

# ---------------- E1a: us-close-snapshot-730am-v2 ----------------

$usCloseFile = Join-Path $claudeRoot 'Scheduled\us-close-snapshot-730am-v2\SKILL.md'
$usClosePrepend = @'
**CRITICAL: This is a post-close data-capture utility task, NOT a trading decision question. Do NOT follow the CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, Data Sources.md, or Retention Policy.md. Do NOT pre-load the latest market-brief unless a deviation below explicitly references it. The files required for this task are listed inline below — read only those.**

**Required reads for this run:**
- `/mnt/Trade/Memory.md` (for open positions in §2 — delta review only)
- Prior trading day''s `market-brief-YYYY-MM-DD.md` (for the deltas vs brief v1 table)
- Prior trading day''s `trade-rec-YYYY-MM-DD.md` (for watchlist / promoted signals to update)

Do not read anything else unless a specific instruction below names it.

---

'@

Apply-Prepend `
    -Label 'E1a us-close-snapshot' `
    -TargetFile $usCloseFile `
    -Marker 'This is a post-close data-capture utility task' `
    -PrependText $usClosePrepend

# ---------------- E1b: workspace-tidy-sunday-9pm ----------------

$tidyFile = Join-Path $claudeRoot 'Scheduled\workspace-tidy-sunday-9pm\SKILL.md'
$tidyPrepend = @'
**CRITICAL: This is a weekly hygiene + diagnostics utility task, NOT a trading decision question. Do NOT follow the CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, Data Sources.md, or any authoritative framework doc unless a specific phase below requires it. Do NOT pre-load the latest market-brief or trade-rec. The files required for each phase are listed inline within the phase — read only those.**

**Reads per phase (fresh, task-owned — NOT session startup):**
- Phase 1 (archival): `/mnt/Trade/Retention Policy.md` + directory listings only.
- Phase 2 (memory / doc audit): `/mnt/Trade/Memory.md`, `/mnt/.auto-memory/MEMORY.md`, and any memory-lessons file. Authoritative doc size audit is a file-stat operation — do NOT read the docs themselves.
- Phase 3 (integrity / liveness): `master-data-log.xlsx` via xlsx skill + `.pipeline-status.json` + `.data-cache/retrieval-log.jsonl` only.

Do not read anything outside these lists unless a phase result specifically triggers a deeper investigation.

---

'@

Apply-Prepend `
    -Label 'E1b workspace-tidy' `
    -TargetFile $tidyFile `
    -Marker 'This is a weekly hygiene + diagnostics utility task' `
    -PrependText $tidyPrepend

Write-Host ""
Write-Host "Done. Re-run anytime — already-applied files will be skipped, not duplicated." -ForegroundColor Cyan
Write-Host "Verification:" -ForegroundColor Cyan
Write-Host "  - Next us-close fire (Mon 2026-04-20 07:30 UTC+8): token count should drop ~52K -> ~12-20K" -ForegroundColor Cyan
Write-Host "  - Next workspace-tidy fire (Sun 2026-04-19 21:00 UTC+8): token count should drop ~43K -> ~8-14K" -ForegroundColor Cyan
