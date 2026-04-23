---
name: apply-skill-patch
description: Apply skill-patch files sandbox-side to produce fully-patched SKILL.md outputs Gerald can save Windows-side. Reads patch files from `/mnt/Trade/patches/`, applies the before/after edits to the source SKILL.md at `/mnt/.claude/skills/<name>/SKILL.md`, runs the patch's verify checks, and writes output to `/mnt/Trade/skills-patched/<name>-SKILL-YYYY-MM-DD.md`. Use whenever Gerald says "apply the patches", "apply phase 3 patches", "produce the patched skills", "render the patches", "save the patched skills", "update my skills from patches", "build the post-patch files", "I need the patched skills to save to Windows", or "create the patched skills so I can save them". Also use when Gerald wants to preview what a patch will produce before running the PowerShell. NOT for writing new patches (skill-manager patch mode does that) — this skill CONSUMES existing patches.
model: haiku
---

# apply-skill-patch

Gerald's skills live at `C:\Users\Lokis\Documents\Claude\skills\<name>\SKILL.md` on Windows, mirrored **read-only** into the sandbox at `/mnt/.claude/skills/<name>/SKILL.md`. When a patch is authored (by `skill-manager`, the `system-review` chain, or by hand), the patch file at `/mnt/Trade/patches/` ships with a PowerShell apply block that modifies the Windows file in place. That flow works, but it asks Gerald to run PowerShell; sometimes he'd rather just save a finished file.

This skill produces that finished file. It reads the patch, reads the current SKILL.md sandbox-side, applies each edit, and writes the fully-patched output to `/mnt/Trade/skills-patched/`. Gerald can then open it, eyeball it, and drag it Windows-side to replace the existing SKILL.md. No PowerShell, no regex escaping, no anchor drift debugging at 11pm.

## When to use

| Gerald says | Do this |
|---|---|
| "apply the 5 phase 3 patches" / "produce all the patched skills" | Iterate over every `*-phase3-SKILL-patch.md` in `/mnt/Trade/patches/` |
| "apply the market-brief patch" / "render market-brief phase 3" | Single skill; match by filename substring |
| "preview what the signal-review patch will produce" | Single skill; note "preview" means don't overwrite an existing output file — append `-preview` suffix |
| "apply every patch in /mnt/Trade/patches/" | Every `*-SKILL-patch.md` (not just phase 3) |

If Gerald's phrasing is ambiguous (e.g., "apply the patches" with no qualifier after today's batch includes Phase 3 + E4 + RM1 + META-B5), list the candidates and ask which ones. Don't guess.

## Why this is not just "run the PowerShell"

The patch file's PowerShell block is authoritative for Windows-side application. This skill does NOT try to replace it. The two paths are complementary:

| Path | When to use |
|---|---|
| PowerShell apply (embedded in patch) | Gerald has terminal open Windows-side and wants in-place edit + backup |
| This skill | Gerald wants to eyeball the full patched file first, or deliver a file by drag-drop, or apply from sandbox without switching contexts |

Both paths produce byte-identical output when the patch is clean. This skill's value is that it *shows Gerald the finished file* before commitment.

## Authoritative scope — do not touch

This skill applies patches ONLY to the 11 trading skills: `market-brief`, `news-events`, `daily-trade-rec`, `pipeline-recovery`, `positions-monitor`, `signal-review`, `literature-review`, `quarterly-methodology-review`, `system-review`, `trade-update`, `consolidate-memory`. Refuse to touch utility skills (`docx`, `pdf`, `pptx`, `xlsx`, `schedule`, `setup-cowork`, `skill-creator`) — breaking them has downstream effects out of scope here. If Gerald explicitly insists, surface the scope line and require a second confirmation before proceeding.

## Workflow

### Step 1 — Identify the patches to apply

Read the user's phrasing. Enumerate the target patch files in `/mnt/Trade/patches/`. Common patterns:

- `*-phase3-SKILL-patch.md` → the 5 Phase 3 patches
- `<skill-name>-phase3-SKILL-patch.md` → single skill from Phase 3
- `E4-<skill>-SKILL-patch.md` → E4 batch (from system-review 2026-04-17)
- `META-B5-model-tiering-patch.md` → standalone meta patch

For each target patch file, the implied source SKILL.md is `/mnt/.claude/skills/<skill-name>/SKILL.md`, where `<skill-name>` is the first segment of the patch filename before `-phase3-` or `-SKILL-patch.md`. When in doubt, grep the patch file for `**Target file (Windows):**` — the Windows path's last two segments give you `<skill-name>\SKILL.md`.

### Step 2 — Read the patch, read the source

Read the patch file in full. Read the source SKILL.md in full. Do NOT truncate — the patch edits require exact-match anchors and a truncated read will mask drift.

### Step 3 — Parse the edit blocks

Each patch uses the convention established by `deployment-memo-2026-04-18.md` / the E4 / Phase 3 patches:

```
### Edit N — <short title>

**Anchor:**
```markdown
<exact string that must appear in source SKILL.md>
```

**Replace with:**
```markdown
<exact string to write in place of the anchor>
```
```

Some patches use `**Insert after anchor:**` or `**Prepend:**` variants. The pattern matters — if you see:

- **Replace with:** → overwrite the anchor string entirely with the replacement.
- **Insert after anchor:** → append the new content after the anchor string; the anchor stays.
- **Prepend:** → the patch has no anchor; prepend the content to the file.

If a patch uses a variant you've never seen, read the surrounding context — the patch author usually explains the semantics in prose before the code fence.

### Step 4 — Apply each edit in order

For each edit:

1. Check the anchor appears **exactly once** in the current working copy. If zero times → anchor drifted, fail loud. If more than once → the anchor isn't unique, fail loud (would need human judgment to pick the right occurrence).
2. Apply the replacement using plain string replace. Do not use regex — the patch author chose exact anchors for a reason.
3. After each edit, sanity-check that the post-patch marker mentioned in the patch's PowerShell `-match` check now appears in the working copy. This catches cases where the anchor matched but the replacement body was wrong.

If any edit fails, abort the whole patch — do NOT write a partial output file. Report which edit failed and which anchor.

### Step 5 — Run the patch's verify checks

Every well-formed patch includes a Verify block — a PowerShell snippet with a list of `@{ Name = ...; Pattern = ... }` checks. Ignore the PowerShell wrapping; extract each Pattern and verify it appears in the patched working copy. Report each check as OK / MISSING.

For patches without an explicit Verify block, fall back to checking that every "Replace with" body's distinctive first line appears in the output.

### Step 6 — Write the output file

Write to `/mnt/Trade/skills-patched/<skill-name>-SKILL-<YYYY-MM-DD>.md`. Use today's date from the session environment.

If the output file already exists for today, append a suffix: `<name>-SKILL-<date>.2.md`, `.3.md`, etc. This lets Gerald apply-preview-revise without clobbering earlier iterations.

### Step 7 — Write a run report

Write a compact run report to `/mnt/Trade/skills-patched/apply-report-<YYYY-MM-DD>.md` listing, for each patch applied:

- Patch file path
- Source SKILL.md path
- Output path
- Edits applied (count + summary)
- Verify checks (OK / MISSING)
- Any warnings (e.g., "market-brief and daily-trade-rec Phase 3 depend on each other — apply together or neither")

If the report already exists for today, append to it rather than overwrite. Gerald may apply patches in batches.

### Step 8 — Present the outputs

Give Gerald one `computer://` link per output file, plus one for the run report. Do NOT recap the patch contents in prose — Gerald can open the file. Lead with the run report link if multiple patches were applied.

## Dependency warnings

Certain patches are known to depend on each other. If Gerald applies one without the other, flag it in the run report:

| If you apply | Also apply | Why |
|---|---|---|
| `market-brief-phase3` | `daily-trade-rec-phase3` | The rec's Step 1.5 consumes the brief's `Meta_Staging_Status` field. Applying rec without brief → staging reads fail. |
| `daily-trade-rec-phase3` | `signal-review-phase3` | Rec writes SignalLedger cols 33-36; signal-review reads them. Missing signal-review → the new cols accumulate un-analyzed. |

Phase 3 patches as a bundle should only apply after the 2026-04-25 shadow review returns GO verdicts for V029/V033/V034/V035. This skill does NOT enforce that gate — it's a *file producer*, not a *deployment controller*. If Gerald applies pre-gate, surface a notice in the run report but proceed.

## Failure modes and what to do

| Failure | Reason | Action |
|---|---|---|
| Anchor appears zero times | Source SKILL.md has drifted since patch was authored | Abort, report `ANCHOR_DRIFT: edit N, anchor fragment = "<first 40 chars>"`. Do NOT attempt fuzzy match. |
| Anchor appears >1 times | Patch author chose a non-unique anchor | Abort, report `ANCHOR_AMBIGUOUS: edit N, N occurrences`. Escalate to `skill-manager` to re-author with a longer anchor. |
| Source SKILL.md doesn't exist | Skill was renamed or removed | Abort, report `SOURCE_MISSING: <path>`. |
| Post-patch marker from verify block doesn't appear after all edits applied | Replacement body has a subtle typo (the anchor matched but the new content is wrong) | Abort, report `VERIFY_FAIL: check "<check name>", pattern "<pattern>"`. |
| Output directory unwritable | Sandbox mount issue | Abort, report the error verbatim. |

Fail loud on all of these — do NOT silently produce a partial output.

## Idempotence

Running the skill twice in one day with the same patch produces `<name>-SKILL-<date>.md` the first time and `<name>-SKILL-<date>.2.md` the second (etc.). This is deliberate — if Gerald ran once, spot-checked, then asked you to rerun, he wants a fresh output rather than trusting that nothing changed upstream.

If Gerald wants to force-overwrite (e.g., post-review cleanup), he'll say "overwrite the output" — then skip the suffix logic. Otherwise default to suffixing.

## Implementation note

The Python script `scripts/apply_patch.py` exists as an optional fallback for when a patch has many edits and you want deterministic string operations rather than doing them in Claude's head. For simple patches (≤5 edits), applying inline is fine; for larger patches or bulk runs, call the script. The script takes `--patch-file` and `--source-skill` args, writes to stdout, and exits non-zero on any failure. See the script's docstring.

## Scope guard — what this skill does NOT do

- Does NOT install skills Windows-side. Gerald copies the output file manually.
- Does NOT run the patch's PowerShell block. Separate workflow.
- Does NOT mutate the source SKILL.md sandbox-side (the mount is read-only anyway).
- Does NOT write patches. That's `skill-manager` Mode 2.
- Does NOT enforce Phase 3 GO-gate. Produces files regardless; flags it in the report.
- Does NOT reformat or "clean up" the source SKILL.md beyond the patch's literal edits. If the source has inconsistent heading levels or trailing whitespace, that's preserved.
