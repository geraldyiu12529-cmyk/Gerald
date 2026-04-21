#!/usr/bin/env python3
"""Generate a patch file for an existing trading skill.

Usage:
    python patch_skill.py <skill-name> --edits-file <path-to-edits.json>
                           [--no-backup] [--force] [--out-dir <dir>]

Reads the current files from /mnt/.claude/skills/<skill-name>/, applies the
edit spec in-memory (to validate), runs backup_skill.py as a precondition,
and writes a patch .md to /mnt/Trade/patches/<skill-name>-<date>-patch.md.

The patch .md contains everything Gerald needs to apply the change on
Windows: a summary, per-file diffs or full rewrites, a PowerShell apply
script block, a verification block, and a rollback block.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import (
    BACKUPS_DIR,
    PATCHES_DIR,
    SKILLS_DIR,
    TRADE_DIR,
    die,
    ensure_parent,
    require_in_scope,
    today_str,
)

PATCH_VS_REWRITE_THRESHOLD = 0.20  # 20% byte change → prefer rewrite


def _ps_escape(s: str) -> str:
    """Escape a string for safe embedding in a PowerShell here-string.

    Here-strings delimited by @'...'@ are literal — no interpolation — so
    we only need to guard against the closing '@ sequence.
    """
    return s.replace("'@", "'+\"@\"+'@")


def _rel(path: str) -> Path:
    p = Path(path)
    if p.is_absolute() or ".." in p.parts:
        die(f"edits.json path must be relative and not traverse: {path}")
    return p


def _validate_edit_spec(spec: dict[str, Any], skill_root: Path) -> dict[str, Any]:
    """Read the target file, validate all old_strings match, compute diff ratio.

    Returns an enriched spec with:
      - `current_content`: str — file on disk (empty string if mode=rewrite and
        file is new)
      - `final_content`: str — what the file will look like after applying
      - `change_ratio`: float — |len(final - current)| / max(1, len(current))
      - `effective_mode`: str — "edits" or "rewrite" after auto-promotion
    """
    path = _rel(spec["path"])
    abs_path = skill_root / path
    mode = spec.get("mode", "edits")
    current = abs_path.read_text(encoding="utf-8") if abs_path.is_file() else ""

    if mode == "rewrite":
        final = spec["new_content"]
    elif mode == "edits":
        final = current
        for i, edit in enumerate(spec.get("edits", [])):
            old = edit["old_string"]
            new = edit["new_string"]
            count = final.count(old)
            if count == 0:
                die(
                    f"edit #{i} on {path}: old_string not found. File may have "
                    f"changed since the edits.json was written. Aborting.\n"
                    f"  old_string (first 120 chars): {old[:120]!r}"
                )
            if count > 1:
                die(
                    f"edit #{i} on {path}: old_string is ambiguous "
                    f"(appears {count} times). Make it more specific."
                )
            final = final.replace(old, new, 1)
    else:
        die(f"unknown edit mode: {mode}")

    change = abs(len(final) - len(current))
    denom = max(1, len(current))
    ratio = change / denom

    effective_mode = mode
    if mode == "edits" and ratio >= PATCH_VS_REWRITE_THRESHOLD:
        effective_mode = "rewrite"

    return {
        **spec,
        "current_content": current,
        "final_content": final,
        "change_ratio": ratio,
        "effective_mode": effective_mode,
    }


def _render_patch(
    skill_name: str,
    summary: str,
    validated: list[dict[str, Any]],
    backup_dir: Path | None,
) -> str:
    """Compose the patch .md from validated edit specs."""
    date = today_str()
    out: list[str] = []
    out.append(f"# Patch — {skill_name} — {date}")
    out.append("")
    out.append(f"**Target:** `C:\\Users\\Lokis\\Documents\\Claude\\skills\\{skill_name}\\`")
    if backup_dir:
        try:
            rel = backup_dir.relative_to(TRADE_DIR)
            out.append(
                f"**Backup:** `$env:USERPROFILE\\Documents\\Trade\\"
                f"{str(rel).replace('/', chr(92))}`"
            )
        except ValueError:
            out.append(f"**Backup:** `{backup_dir}`")
    else:
        out.append("**Backup:** skipped (--no-backup)")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(summary)
    out.append("")
    out.append("## Per-file edits")
    out.append("")

    for spec in validated:
        path = spec["path"]
        mode = spec["effective_mode"]
        ratio = spec["change_ratio"]
        out.append(f"### `{path}` — mode: {mode} (change ratio: {ratio:.1%})")
        out.append("")

        if mode == "edits":
            for i, edit in enumerate(spec.get("edits", [])):
                reason = edit.get("reason", "")
                out.append(f"**Edit {i + 1}** — {reason}" if reason else f"**Edit {i + 1}**")
                out.append("")
                out.append("Before:")
                out.append("```")
                out.append(edit["old_string"])
                out.append("```")
                out.append("")
                out.append("After:")
                out.append("```")
                out.append(edit["new_string"])
                out.append("```")
                out.append("")
        else:
            out.append("Full file rewrite. New content:")
            out.append("")
            out.append("```")
            out.append(spec["final_content"])
            out.append("```")
            out.append("")

    out.append("## PowerShell — apply")
    out.append("")
    out.append(
        "Copy this block into an elevated PowerShell session. It is idempotent "
        "where possible: a second run on already-patched files will be a no-op."
    )
    out.append("")
    out.append("```powershell")
    out.append(f"$skillRoot = \"$env:USERPROFILE\\Documents\\Claude\\skills\\{skill_name}\"")
    out.append("if (-not (Test-Path $skillRoot)) {")
    out.append(f"    Write-Error \"skill folder not found: $skillRoot\"; exit 1")
    out.append("}")
    out.append("")

    for spec in validated:
        rel = spec["path"].replace("/", "\\")
        out.append(f"# --- {rel} ---")
        out.append(f"$target = Join-Path $skillRoot '{rel}'")
        out.append(
            "if (-not (Test-Path $target)) { "
            "$targetDir = Split-Path $target -Parent; "
            "if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null } "
            "}"
        )
        if spec["effective_mode"] == "edits":
            out.append("$content = Get-Content $target -Raw")
            for i, edit in enumerate(spec.get("edits", [])):
                old_esc = _ps_escape(edit["old_string"])
                new_esc = _ps_escape(edit["new_string"])
                out.append(f"# edit {i + 1}")
                out.append(f"$old = @'\n{old_esc}\n'@")
                out.append(f"$new = @'\n{new_esc}\n'@")
                out.append("if ($content.Contains($old)) {")
                out.append("    $content = $content.Replace($old, $new)")
                out.append(f"    Write-Host 'applied edit {i + 1} to {rel}'")
                out.append("} elseif ($content.Contains($new)) {")
                out.append(f"    Write-Host 'edit {i + 1} on {rel} already applied — skipped'")
                out.append("} else {")
                out.append(
                    f"    Write-Error 'edit {i + 1} on {rel}: neither old nor new string matched — file drifted. Aborting.'; exit 1"
                )
                out.append("}")
            out.append("Set-Content -Path $target -Value $content -NoNewline")
        else:
            new_esc = _ps_escape(spec["final_content"])
            out.append(f"$new = @'\n{new_esc}\n'@")
            out.append("Set-Content -Path $target -Value $new -NoNewline")
            out.append(f"Write-Host 'rewrote {rel}'")
        out.append("")

    out.append("Write-Host '`napply complete.'")
    out.append("```")
    out.append("")

    out.append("## PowerShell — verify")
    out.append("")
    out.append("```powershell")
    out.append(f"$skillRoot = \"$env:USERPROFILE\\Documents\\Claude\\skills\\{skill_name}\"")
    for spec in validated:
        rel = spec["path"].replace("/", "\\")
        if spec["effective_mode"] == "edits":
            for i, edit in enumerate(spec.get("edits", [])):
                new_esc = _ps_escape(edit["new_string"])
                out.append(f"# check edit {i + 1} on {rel}")
                out.append(f"$target = Join-Path $skillRoot '{rel}'")
                out.append("$content = Get-Content $target -Raw")
                out.append(f"$needle = @'\n{new_esc}\n'@")
                out.append(
                    "if ($content.Contains($needle)) { "
                    f"Write-Host 'OK — {rel} edit {i + 1}' "
                    "} else { "
                    f"Write-Host 'FAIL — {rel} edit {i + 1}' "
                    "}"
                )
        else:
            out.append(f"# rewrite verification on {rel}")
            out.append(f"$target = Join-Path $skillRoot '{rel}'")
            out.append("if (Test-Path $target) { Write-Host 'OK — " + rel + " exists' } else { Write-Host 'FAIL — " + rel + " missing' }")
    out.append("```")
    out.append("")

    out.append("## PowerShell — rollback")
    out.append("")
    if backup_dir:
        # Translate sandbox backup path to a Windows-relative path. The Trade
        # folder on Windows is at $env:USERPROFILE\Documents\Trade (or wherever
        # Gerald mounts it as the Cowork directory). Compute the path relative
        # to the Trade dir so the Windows script doesn't need to know the
        # sandbox-specific prefix.
        try:
            rel_from_trade = backup_dir.relative_to(TRADE_DIR)
            win_backup_rel = str(rel_from_trade).replace("/", "\\")
        except ValueError:
            # Backup isn't under TRADE_DIR — shouldn't happen in normal flow.
            win_backup_rel = str(backup_dir).replace("/", "\\")
        out.append("```powershell")
        out.append(f"$skillRoot = \"$env:USERPROFILE\\Documents\\Claude\\skills\\{skill_name}\"")
        out.append(
            "# If your Trade folder lives somewhere else, edit $tradeRoot accordingly."
        )
        out.append("$tradeRoot = \"$env:USERPROFILE\\Documents\\Trade\"")
        out.append(f"$backup = Join-Path $tradeRoot '{win_backup_rel}'")
        out.append("if (-not (Test-Path $backup)) { Write-Error \"backup not found: $backup\"; exit 1 }")
        out.append(
            "Copy-Item -Path (Join-Path $backup '*') -Destination $skillRoot -Recurse -Force"
        )
        out.append("Write-Host 'rollback complete.'")
        out.append("```")
    else:
        out.append("(No backup was taken for this patch. Manual rollback required.)")
    out.append("")

    return "\n".join(out) + "\n"


def _run_backup(skill_name: str) -> Path:
    """Invoke backup_skill.py as a subprocess and return the backup dir."""
    script = Path(__file__).parent / "backup_skill.py"
    proc = subprocess.run(
        [sys.executable, str(script), skill_name, "--reason", "pre-patch auto-snapshot"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        die(f"backup failed:\n{proc.stderr.strip()}")
    backup_path = Path(proc.stdout.strip())
    if not backup_path.is_dir():
        die(f"backup script returned non-directory: {backup_path}")
    return backup_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name")
    ap.add_argument("--edits-file", required=True, type=Path)
    ap.add_argument("--no-backup", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out-dir", type=Path, default=PATCHES_DIR)
    args = ap.parse_args()

    skill_name = args.skill_name
    require_in_scope(skill_name, allow_override=args.force)

    skill_root = SKILLS_DIR / skill_name
    if not skill_root.is_dir():
        die(f"skill folder not found: {skill_root}")

    if not args.edits_file.is_file():
        die(f"edits file not found: {args.edits_file}")
    spec = json.loads(args.edits_file.read_text(encoding="utf-8"))
    if spec.get("skill_name") != skill_name:
        die(f"edits.json skill_name mismatch: {spec.get('skill_name')} vs {skill_name}")

    validated = [_validate_edit_spec(f, skill_root) for f in spec.get("files", [])]

    backup_dir: Path | None = None
    if not args.no_backup:
        backup_dir = _run_backup(skill_name)

    patch_md = _render_patch(
        skill_name=skill_name,
        summary=spec.get("summary", ""),
        validated=validated,
        backup_dir=backup_dir,
    )

    out_path = args.out_dir / f"{skill_name}-{today_str()}-patch.md"
    ensure_parent(out_path)
    # Same-day collision: suffix -v2, -v3, ...
    if out_path.exists():
        i = 2
        while True:
            candidate = args.out_dir / f"{skill_name}-{today_str()}-patch-v{i}.md"
            if not candidate.exists():
                out_path = candidate
                break
            i += 1
    out_path.write_text(patch_md, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
