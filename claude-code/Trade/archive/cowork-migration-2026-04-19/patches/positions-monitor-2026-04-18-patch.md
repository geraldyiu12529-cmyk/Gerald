# Patch — positions-monitor — 2026-04-18

**Target:** `C:\Users\Lokis\Documents\Claude\skills\positions-monitor\`
**Backup:** `/sessions/upbeat-great-archimedes/mnt/Trade/skill-backups/2026-04-18/positions-monitor.2`

## Summary

Smoke test — add a demo `model:` line to positions-monitor to exercise patch_skill.py. Do NOT apply this Windows-side; it's for generating the patch file only.

## Per-file edits

### `SKILL.md` — mode: edits (change ratio: 0.3%)

**Edit 1** — Test insert before description

Before:
```
name: positions-monitor
description:
```

After:
```
name: positions-monitor
model: sonnet
description:
```

## PowerShell — apply

Copy this block into an elevated PowerShell session. It is idempotent where possible: a second run on already-patched files will be a no-op.

```powershell
$skillRoot = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor"
if (-not (Test-Path $skillRoot)) {
    Write-Error "skill folder not found: $skillRoot"; exit 1
}

# --- SKILL.md ---
$target = Join-Path $skillRoot 'SKILL.md'
if (-not (Test-Path $target)) { $targetDir = Split-Path $target -Parent; if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null } }
$content = Get-Content $target -Raw
# edit 1
$old = @'
name: positions-monitor
description:
'@
$new = @'
name: positions-monitor
model: sonnet
description:
'@
if ($content.Contains($old)) {
    $content = $content.Replace($old, $new)
    Write-Host 'applied edit 1 to SKILL.md'
} elseif ($content.Contains($new)) {
    Write-Host 'edit 1 on SKILL.md already applied — skipped'
} else {
    Write-Error 'edit 1 on SKILL.md: neither old nor new string matched — file drifted. Aborting.'; exit 1
}
Set-Content -Path $target -Value $content -NoNewline

Write-Host '`napply complete.'
```

## PowerShell — verify

```powershell
$skillRoot = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor"
# check edit 1 on SKILL.md
$target = Join-Path $skillRoot 'SKILL.md'
$content = Get-Content $target -Raw
$needle = @'
name: positions-monitor
model: sonnet
description:
'@
if ($content.Contains($needle)) { Write-Host 'OK — SKILL.md edit 1' } else { Write-Host 'FAIL — SKILL.md edit 1' }
```

## PowerShell — rollback

```powershell
$skillRoot = "$env:USERPROFILE\Documents\Claude\skills\positions-monitor"
$backup = "\sessions\upbeat-great-archimedes$env:USERPROFILE\Documents\Trade\skill-backups\2026-04-18\positions-monitor.2"
if (-not (Test-Path $backup)) { Write-Error "backup not found: $backup"; exit 1 }
Copy-Item -Path (Join-Path $backup '*') -Destination $skillRoot -Recurse -Force
Write-Host 'rollback complete.'
```

