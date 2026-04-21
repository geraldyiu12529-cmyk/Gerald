# edits.json schema

`patch_skill.py` consumes an `edits.json` that describes the changes to make to a skill folder. In practice Claude writes this file in-memory from Gerald's spoken instructions — Gerald does not hand-author it — but the schema is documented here so the pipeline is auditable.

## Top-level

```json
{
  "skill_name": "daily-trade-rec",
  "summary": "One-paragraph reason this patch exists.",
  "files": [ ...edit specs... ]
}
```

- `skill_name` — must be in the trading allow-list (`references/trading-skills.md`).
- `summary` — prose for the top of the generated patch file.
- `files` — array of per-file edit specs.

## Per-file edit spec

Two shapes, chosen by `mode`:

### Mode `"edits"` — targeted before/after blocks

```json
{
  "path": "SKILL.md",
  "mode": "edits",
  "edits": [
    {
      "old_string": "model: sonnet",
      "new_string": "model: haiku",
      "reason": "Demote to Haiku — routine healthy-path work"
    }
  ]
}
```

- `path` — relative to the skill folder root (e.g. `SKILL.md`, `scripts/foo.py`).
- `edits` — one or more substitutions. Each `old_string` must match the current file exactly and uniquely. If it doesn't match, `patch_skill.py` fails loudly with the mismatch and does not emit a patch.
- `reason` — optional per-edit note that appears in the patch summary.

### Mode `"rewrite"` — full-file replacement

```json
{
  "path": "SKILL.md",
  "mode": "rewrite",
  "new_content": "---\nname: ...\n---\n\n# ...\n"
}
```

Use when the diff is >20% of the file or when the edit is structural (reordering sections, etc.). `patch_skill.py` auto-promotes `edits` → `rewrite` if the cumulative change exceeds the threshold.

## Patch size policy

The 20% threshold is in `scripts/patch_skill.py` (`PATCH_VS_REWRITE_THRESHOLD`). Tune if the boundary feels wrong. Rationale: below ~20% byte change, before/after blocks are the most readable format; above ~20%, the before/after blocks become harder to review than the full new file.

## Example

A minimal, valid edits file that bumps one SKILL.md's model tier:

```json
{
  "skill_name": "positions-monitor",
  "summary": "Demote positions-monitor from Sonnet to Haiku for intraday silent-when-OK runs; preserve Sonnet for fresh-context escalations (not in this patch).",
  "files": [
    {
      "path": "SKILL.md",
      "mode": "edits",
      "edits": [
        {
          "old_string": "model: sonnet",
          "new_string": "model: haiku",
          "reason": "Healthy-path is mechanical; escalation path is out of scope here."
        }
      ]
    }
  ]
}
```
