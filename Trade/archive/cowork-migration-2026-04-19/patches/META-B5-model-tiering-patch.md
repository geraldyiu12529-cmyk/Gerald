# Part B.5 Model-Tiering Patch — 2026-04-18

**Source:** 2026-04-18 Part B deployment (see `deployment-memo-2026-04-18.md`).
**Action:** Add `model: <tier>` field to each custom trading SKILL.md frontmatter.
**Rollback:** Remove the added `model:` line; Claude falls back to default model.

Target directory (Windows-side): `C:\Users\Lokis\Documents\Claude\skills\<skill>\SKILL.md`

## Model assignment rationale

Three tiers based on Gerald's spec: Opus for reasoning-heavy synthesis, Sonnet for routine-with-judgment, Haiku for narrow fast paths. `positions-monitor` explicitly pinned to Sonnet (NOT Haiku) per Gerald's instruction.

| Skill | Tier | Why |
|---|---|---|
| daily-trade-rec | **opus** | 8-step synthesis, highest-stakes output, touches live capital |
| signal-review | **opus** | OOS methodology review, meta-reasoning on system performance |
| quarterly-methodology-review | **opus** | Meta-review of methodology fitness — hardest judgment call in the stack |
| system-review | **opus** | Strategic architecture audit, requires tradeoff reasoning |
| literature-review | **opus** | Academic factor evaluation, 5-criteria screens |
| market-brief | **sonnet** | Grade-A pulls + scorecard build; routine but regime calls need quality |
| news-events | **sonnet** | Categorized capture, catalyst tagging — quality/cost balanced |
| trade-update | **sonnet** | Memory sync across 4 layers — accuracy > speed |
| positions-monitor | **sonnet** | Gerald explicit: NOT Haiku. Reads live-book, flags drift. |
| pipeline-recovery | **haiku** | Gerald explicit: Haiku for healthy path. Silent-when-OK means most runs are trivial. Unhealthy path escalates to Memory.md which Gerald can read in fresh Opus session. |
| consolidate-memory | **haiku** | Utility — merging duplicates and pruning index, mechanical task |

## Frontmatter edits

For each skill, add one line after the `description:` line (and before the closing `---`). The position matters — keep it inside the frontmatter block.

### daily-trade-rec

**File:** `C:\Users\Lokis\Documents\Claude\skills\daily-trade-rec\SKILL.md`

**Current frontmatter:**
```yaml
---
name: daily-trade-rec
description: Produces Gerald's pre-open trade recommendation by synthesising...
---
```

**New frontmatter:**
```yaml
---
name: daily-trade-rec
description: Produces Gerald's pre-open trade recommendation by synthesising...
model: opus
---
```

### signal-review

**File:** `C:\Users\Lokis\Documents\Claude\skills\signal-review\SKILL.md`

Add `model: opus` after the `description:` line.

### quarterly-methodology-review

**File:** `C:\Users\Lokis\Documents\Claude\skills\quarterly-methodology-review\SKILL.md`

Add `model: opus` after the `description:` line.

### system-review

**File:** `C:\Users\Lokis\Documents\Claude\skills\system-review\SKILL.md`

Add `model: opus` after the `description:` line.

### literature-review

**File:** `C:\Users\Lokis\Documents\Claude\skills\literature-review\SKILL.md`

Add `model: opus` after the `description:` line.

### market-brief

**File:** `C:\Users\Lokis\Documents\Claude\skills\market-brief\SKILL.md`

Add `model: sonnet` after the `description:` line.

### news-events

**File:** `C:\Users\Lokis\Documents\Claude\skills\news-events\SKILL.md`

Add `model: sonnet` after the `description:` line.

### trade-update

**File:** `C:\Users\Lokis\Documents\Claude\skills\trade-update\SKILL.md`

Add `model: sonnet` after the `description:` line.

### positions-monitor

**File:** `C:\Users\Lokis\Documents\Claude\skills\positions-monitor\SKILL.md`

Add `model: sonnet` after the `description:` line.

### pipeline-recovery

**File:** `C:\Users\Lokis\Documents\Claude\skills\pipeline-recovery\SKILL.md`

Add `model: haiku` after the `description:` line.

### consolidate-memory

**File:** `C:\Users\Lokis\Documents\Claude\skills\consolidate-memory\SKILL.md`

Add `model: haiku` after the `description:` line.

## PowerShell apply script

Save as `apply-B5-model-tiering.ps1` in the same directory, then run from an elevated PowerShell:

```powershell
$skillRoot = "$env:USERPROFILE\Documents\Claude\skills"
$assignments = @{
    "daily-trade-rec"              = "opus"
    "signal-review"                = "opus"
    "quarterly-methodology-review" = "opus"
    "system-review"                = "opus"
    "literature-review"            = "opus"
    "market-brief"                 = "sonnet"
    "news-events"                  = "sonnet"
    "trade-update"                 = "sonnet"
    "positions-monitor"            = "sonnet"
    "pipeline-recovery"            = "haiku"
    "consolidate-memory"           = "haiku"
}
foreach ($skill in $assignments.Keys) {
    $path = Join-Path $skillRoot "$skill\SKILL.md"
    if (-not (Test-Path $path)) { Write-Warning "skip: $path not found"; continue }
    $content = Get-Content $path -Raw
    if ($content -match "(?m)^model:\s") {
        Write-Host "$skill — already has model field, skipping"
        continue
    }
    # Insert model line after the first 'description:' line in the frontmatter.
    # Frontmatter description may span multiple lines; we match a single-line description only.
    # For multi-line descriptions, insert before the closing '---' instead.
    $tier = $assignments[$skill]
    if ($content -match "(?ms)^---\r?\n.*?^description:.*?\r?\n(.*?)^---") {
        # Insert model: line before the closing ---
        $new = $content -replace "(?ms)^(---\r?\n.*?^description:[^\r\n]*(?:\r?\n(?!model:|---)[^\r\n]*)*\r?\n)", "`$1model: $tier`r`n"
        Set-Content $path $new -NoNewline
        Write-Host "$skill — set model: $tier"
    } else {
        Write-Warning "$skill — frontmatter not recognized, skipping"
    }
}
Write-Host "`nDone. Verify each SKILL.md has exactly one 'model:' line in frontmatter."
```

Verify with:

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\Claude\skills" -Filter SKILL.md -Recurse | ForEach-Object {
    $model = (Get-Content $_.FullName -First 15 | Select-String "^model:").Line
    "{0,-35} {1}" -f $_.Directory.Name, $model
}
```

## Rollback

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\Claude\skills" -Filter SKILL.md -Recurse | ForEach-Object {
    $c = Get-Content $_.FullName -Raw
    $c = $c -replace "(?m)^model:\s+\w+\r?\n", ""
    Set-Content $_.FullName $c -NoNewline
}
```

## Sandbox note

This patch file exists because the sandbox's `/mnt/.claude/skills/*/SKILL.md` paths are mounted read-only. `/mnt/.claude/CLAUDE.md` (global) was successfully patched in the same 2026-04-18 session for Part B.1+B.2 — the read-only restriction applies only to skill folders. Apply this patch Windows-side to complete Part B.5.
