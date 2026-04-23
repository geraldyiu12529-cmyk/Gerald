# Windows-side apply workflow

All outputs from `skill-manager` land in `/mnt/Trade/` (or the user's mounted Trade folder). This document is the Windows-side procedure for each mode.

## Patch mode

1. Open the patch file: `C:\...\Trade\patches\<skill-name>-<YYYY-MM-DD>-patch.md`.
2. Skim the **Summary** and **Per-file edit list** sections to confirm the changes are what you approved.
3. Open an elevated PowerShell.
4. Copy the **PowerShell apply script** block (bottom of the patch file) into the PowerShell session. Run.
5. Run the **Verification block** (immediately after the apply block in the patch file). All lines should print `OK`. If any print `FAIL`, stop and either re-run or roll back.
6. Keep the backup folder until the next successful run confirms the change is working.

### Rollback

Each patch file has a **Rollback** block. It restores from the backup folder created in the same session. Paste into PowerShell to revert.

## Scaffold / Package mode

1. The skill produces `C:\...\Trade\skills-draft\<skill-name>.zip`.
2. In PowerShell:

```powershell
$dest = "$env:USERPROFILE\Documents\Claude\skills\<skill-name>"
$zip  = "$env:USERPROFILE\Documents\Trade\skills-draft\<skill-name>.zip"

if (Test-Path $dest) {
    Write-Warning "$dest already exists. Back up or remove it first."
} else {
    Expand-Archive -Path $zip -DestinationPath $dest
    Write-Host "installed at $dest"
}
```

3. Verify the frontmatter:

```powershell
Get-Content "$env:USERPROFILE\Documents\Claude\skills\<skill-name>\SKILL.md" -First 10
```

4. Restart any Claude session that needs the new skill to pick it up.

## Backup mode

No Windows-side action needed. The backup lives in `C:\...\Trade\skill-backups\YYYY-MM-DD\<skill-name>\` and can be referenced directly if a rollback is needed.
