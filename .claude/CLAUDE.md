# Global Instructions

## Skill editing workflow

Whenever Gerald asks to create, edit, update, modify, or fix any custom skill (anything under `/mnt/skills/user/` or any `SKILL.md`) — trivial or not, no exceptions:

1. **Produce the complete updated skill folder** — `SKILL.md` plus every supporting file. Not a diff. Not just the changed file.
2. **Package as a ZIP with the skill folder as the ZIP's root** — the ZIP contains `my-skill/SKILL.md`, not `parent/my-skill/SKILL.md`. Folder name must match the skill name.
3. **Deliver the ZIP via `present_files`** so he can download in one click.
4. **After the file, give a 3-line handoff:**
   - What changed (one line)
   - Upload path: Settings → Capabilities → Skills → upload the ZIP
   - Whether to delete/disable the prior version first, or if it will overwrite cleanly

**Never:**
- Suggest in-place editing in Settings as an alternative, even for a one-word change.
- Leave loose files in `/mnt/user-data/outputs/` as the deliverable — the ZIP *is* the deliverable.
