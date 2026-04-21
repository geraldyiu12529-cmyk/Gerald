---
name: skill-manager
description: Meta-skill for managing Gerald's 11 custom trading skills. Handles three workflows — backup (snapshot a skill before editing), patch (generate an edit-list plus PowerShell apply script for an existing skill), and scaffold (create a new skill from a template). Works around the read-only `/mnt/.claude/skills/` mount by writing backups, patches, and new skill folders to `/mnt/Trade/` then packaging them for Windows-side install. Use whenever Gerald says "update [skill-name]", "edit a skill", "patch a skill", "backup a skill", "snapshot a skill before I change it", "save a skill", "create a new skill", "scaffold a skill", "package a skill", or "add a new skill to the trading workspace". Also use when Gerald says "I want to change [skill-name]" or asks to modify any of the 11 trading skills listed in `references/trading-skills.md`. Not for running an existing skill — use the skill directly in that case.
model: haiku
---

# Skill Manager

A meta-skill for managing Gerald's custom trading skills. Gerald's 11 trading skills live in `C:\Users\Lokis\Documents\Claude\skills\` on Windows, mirrored read-only into the sandbox at `/mnt/.claude/skills/`. This skill works around that read-only mount by writing all changes into `/mnt/Trade/` and packaging them for Windows-side apply.

The skill has three modes. Pick the right mode based on what Gerald asked for, then run the matching script.

---

## Scope

This skill operates only on the 11 custom trading skills listed in `references/trading-skills.md`. It will refuse to touch utility skills (`docx`, `pdf`, `pptx`, `xlsx`, `schedule`, `setup-cowork`, `skill-creator`, `consolidate-memory`) because those are maintained outside Gerald's trading workflow and breaking them could have downstream effects the skill can't reason about. If Gerald explicitly asks to operate outside the trading scope, surface this limit and get explicit confirmation before proceeding.

---

## Mode selection

| Trigger phrase from Gerald | Mode | Script |
|---|---|---|
| "back up [skill]", "snapshot [skill]", "save [skill] before I change it" | Backup | `scripts/backup_skill.py` |
| "update [skill]", "patch [skill]", "edit [skill]", "change [skill]" | Patch | `scripts/patch_skill.py` |
| "create a new skill", "scaffold a skill", "add a skill called X" | Scaffold | `scripts/scaffold_skill.py` |
| "package [skill]", "zip [skill]" | Package | `scripts/package_skill.py` |

If the ask is ambiguous ("save [skill]" could mean backup or package), ask Gerald which one. Don't guess.

**Safety default:** whenever Gerald asks to patch a skill, run Backup first without asking. The backup is cheap and the rollback path is worth the ~2s it takes. Announce the backup path in the final message so Gerald knows where to find it.

---

## Mode 1 — Backup

**When:** before any edit to an existing skill, or when Gerald wants a point-in-time snapshot.

**What it does:** copies the entire skill folder from `/mnt/.claude/skills/<name>/` (sandbox-readable) to `/mnt/Trade/skill-backups/YYYY-MM-DD/<name>/`. Preserves every file — SKILL.md, scripts, references, assets.

**Run:**

```bash
python /mnt/Trade/skills-draft/skill-manager/scripts/backup_skill.py <skill-name>
```

Or if this skill has been installed Windows-side, the script lives alongside this SKILL.md; call it with the relative path.

**Output:** `/mnt/Trade/skill-backups/YYYY-MM-DD/<skill-name>/` containing a mirror of the skill folder, plus a `BACKUP_MANIFEST.md` noting the date, source path, byte count per file, and any reason string Gerald supplied.

**If the backup directory for today already exists:** do not overwrite. Append a suffix: `<skill-name>.2`, `<skill-name>.3`, etc. This means Gerald can snapshot multiple times in a day and none of them clobber each other.

---

## Mode 2 — Patch

**When:** Gerald wants to change an existing skill. Because the Windows-side SKILL.md is authoritative and the sandbox copy is read-only, the skill cannot edit the live file — it must produce a patch that Gerald applies Windows-side.

**What it does:**
1. Reads the current SKILL.md (and any other files Gerald wants to edit) from `/mnt/.claude/skills/<name>/`.
2. Asks Gerald what the changes should be (in natural language; the skill translates to concrete edits).
3. Runs the backup script as a precondition.
4. Writes a patch file to `/mnt/Trade/patches/<skill-name>-<YYYY-MM-DD>-patch.md` containing:
   - **Summary** — one paragraph on what changes and why.
   - **Per-file edit list** — for each file touched, either (a) a set of before/after blocks for targeted edits, or (b) the full new content if the change is >20% of the file.
   - **PowerShell apply script** — inline, regex-based replacements. Idempotent where possible (checks whether the change is already applied).
   - **Verification block** — PowerShell snippet to grep for the expected strings after apply.
   - **Rollback** — PowerShell to revert by restoring from the backup folder.

**Run:**

```bash
python /mnt/Trade/skills-draft/skill-manager/scripts/patch_skill.py <skill-name> \
    --edits-file /path/to/edits.json
```

The `edits.json` format is described in `references/edits-schema.md`. In practice Claude constructs this in-memory from Gerald's spoken instructions rather than making Gerald hand-write JSON.

**Patch size policy:**
- If the concrete diff touches <20% of the file byte count, emit before/after blocks with exact-match `old_string` / `new_string` that PowerShell can regex-escape and replace.
- If the diff touches ≥20%, emit a full-file rewrite. Before/after is less readable than just showing the new file in that case.

This threshold is in `scripts/patch_skill.py` and can be tuned if Gerald finds the boundary wrong in practice.

---

## Mode 3 — Scaffold

**When:** Gerald wants a brand-new skill created and installed.

**What it does:**
1. Validates the skill name isn't already taken (would shadow an existing one).
2. Creates `/mnt/Trade/skills-draft/<skill-name>/` with `SKILL.md` from the template at `assets/skill-template.md`, plus empty `scripts/`, `references/`, `assets/` subdirectories.
3. If Gerald supplied an intent, pre-fills the SKILL.md frontmatter (name, description, model tier) and the top-level body outline.
4. Zips the folder to `/mnt/Trade/skills-draft/<skill-name>.zip` so Gerald can extract Windows-side into `C:\Users\Lokis\Documents\Claude\skills\<skill-name>\`.

**Run:**

```bash
python /mnt/Trade/skills-draft/skill-manager/scripts/scaffold_skill.py <skill-name> \
    --description "<one-line description>" \
    --model <opus|sonnet|haiku>
```

**After scaffold:** the skill is a stub. Follow up with skill-creator (or successive patch-mode runs) to flesh out the body, test cases, and helper scripts. Tell Gerald to run the "Install Windows-side" instruction block printed at the end.

---

## Mode 4 — Package

**When:** Gerald has finished scaffolding or editing a skill in `/mnt/Trade/skills-draft/<name>/` and wants a single zip he can save and move.

**What it does:** recursively zips `/mnt/Trade/skills-draft/<skill-name>/` into `/mnt/Trade/skills-draft/<skill-name>.zip`. Nothing fancy — but centralised so Gerald never has to remember the exact zip syntax and the skill doesn't accidentally include dot-files or IDE cruft.

**Run:**

```bash
python /mnt/Trade/skills-draft/skill-manager/scripts/package_skill.py <skill-name>
```

Output path is printed so it can be shared via a `computer://` link.

---

## Windows-side apply workflow

The apply workflow is the same for all three write modes (patch, scaffold, package). Gerald runs an elevated PowerShell and:

1. **Patch mode:** executes the script block at the bottom of the patch .md file. Validates with the verify block at the end.
2. **Scaffold/Package mode:** extracts the zip into `C:\Users\Lokis\Documents\Claude\skills\<skill-name>\`. Verifies the frontmatter via the snippet in `references/apply-workflow.md`.

See `references/apply-workflow.md` for copy-paste-ready command blocks.

---

## Output discipline

Every run of this skill produces exactly one deliverable file (the backup folder, patch .md, or .zip) in `/mnt/Trade/`. After the script succeeds, share the file with Gerald using a `computer://` link and a single-sentence summary of what's in it. Do not restate the full patch contents in chat — Gerald will read the file.

If the script fails, surface the stderr verbatim. Do not retry silently.

---

## Why this skill exists

Gerald has hit the read-only SKILL.md mount repeatedly — most recently on 2026-04-18 during the Part B.5 model-tiering deployment, where the fix required writing a patch file and a PowerShell apply script by hand. This skill encodes that pattern so future edits take one command instead of a hand-crafted workaround.

The scope is deliberately narrow: 11 skills, Gerald's workspace only. Generalising beyond that would re-introduce the failure modes that the scope was drawn to avoid.
