---
name: skill-manager skill deployed 2026-04-18
description: New meta-skill for managing 11 trading skills — backup/patch/scaffold/package modes; packaged as /mnt/Trade/skills-draft/skill-manager.zip for Windows-side install
type: project
originSessionId: d1d8a39d-8e5a-44c8-9824-32a8cc9ecb44
---
**Event.** 2026-04-18 same session as meta-analysis deployment. Gerald invoked `/skill-creator` asking for "recommend skill for me to save skill. it will allow me to update the current skill". After a three-question clarification (AskUserQuestion), Gerald chose all-three-modes / trading-skills-only / packaged-delivery.

**Artifact locations:**
- Source: `/mnt/Trade/skills-draft/skill-manager/` (SKILL.md + 4 scripts + 3 references + 1 asset)
- Package: `/mnt/Trade/skills-draft/skill-manager.zip` (18.4 KB, 10 files)
- Referenced test artifacts left on disk: `test-smoke/` scaffold, `positions-monitor-2026-04-18-patch*.md`, `skill-backups/2026-04-18/positions-monitor*/`. Sandbox rm blocked; Gerald can delete Windows-side.

**How to apply Windows-side.**
```powershell
$dest = "$env:USERPROFILE\Documents\Claude\skills\skill-manager"
$zip  = "$env:USERPROFILE\Documents\Trade\skills-draft\skill-manager.zip"
if (Test-Path $dest) { Write-Warning "already installed — skip or remove first" }
else { Expand-Archive -Path $zip -DestinationPath $dest; Write-Host "installed" }
```

**What the skill does.** Four modes triggered by phrase:
- **Backup** — mirrors a skill folder into `skill-backups/YYYY-MM-DD/<name>/` with a BACKUP_MANIFEST.md. Same-day collisions get `.2`, `.3` suffixes (never clobbers).
- **Patch** — reads the current skill, consumes an `edits.json` (Claude constructs in-memory from spoken instructions), auto-runs backup, emits a `<name>-<date>-patch.md` with summary + per-file edits + idempotent PowerShell apply + verify + rollback blocks. 20% byte-change threshold auto-promotes `edits` → `rewrite` mode.
- **Scaffold** — creates a new skill folder from `assets/skill-template.md`, auto-zips.
- **Package** — zips `skills-draft/<name>/` excluding dotfiles, `__pycache__`, `.pyc`, and `test_edits.json`.

**Scope enforcement.** Hardcoded allow-list of 11 trading skills in `scripts/_common.py:TRADING_SKILLS`. Out-of-scope targets fail-loud with exit 2 unless `--force` is passed.

**Why this skill exists.** Part B.5 on 2026-04-18 surfaced the read-only `/mnt/.claude/skills/` mount: any SKILL.md edit needs a patch file + PowerShell script built by hand. This skill encodes that pattern so future edits take one command instead of a hand-crafted workaround.

**How to apply:**
- When Gerald says "update [skill]" or "edit [skill]", invoke this skill, not skill-creator. skill-creator stays the tool for *creating* skills from scratch with the full iteration/eval workflow; skill-manager covers the lightweight edit workflow for already-deployed skills.
- The Python scripts auto-detect the mount root (tries `$SKILL_MANAGER_ROOT` env, then `/mnt`, then walks up from `__file__`) so they work identically in the Cowork sandbox (`/sessions/<id>/mnt/...`) and Windows-side (`/mnt/...`).
- Backup is the safety default: any patch run auto-takes a backup unless `--no-backup` is explicitly passed. The rollback block in every patch references that backup.
