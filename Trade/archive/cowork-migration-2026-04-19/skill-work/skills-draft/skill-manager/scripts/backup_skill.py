#!/usr/bin/env python3
"""Backup an existing trading skill before editing.

Usage:
    python backup_skill.py <skill-name> [--reason "why"] [--force]

Source: /mnt/.claude/skills/<skill-name>/  (sandbox-readable copy of the
        Windows-side skill folder)
Dest:   /mnt/Trade/skill-backups/YYYY-MM-DD/<skill-name>/

Writes a BACKUP_MANIFEST.md alongside the mirror. Same-day collisions get
a numeric suffix (.2, .3, ...) — never clobber an earlier backup.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from _common import (
    BACKUPS_DIR,
    SKILLS_DIR,
    die,
    iter_skill_files,
    require_in_scope,
    today_str,
)


def unique_dest(parent: Path, skill_name: str) -> Path:
    candidate = parent / skill_name
    if not candidate.exists():
        return candidate
    i = 2
    while True:
        candidate = parent / f"{skill_name}.{i}"
        if not candidate.exists():
            return candidate
        i += 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name")
    ap.add_argument("--reason", default="", help="Free-text reason for the snapshot")
    ap.add_argument("--force", action="store_true", help="Allow out-of-scope skills")
    args = ap.parse_args()

    skill_name = args.skill_name
    require_in_scope(skill_name, allow_override=args.force)

    src = SKILLS_DIR / skill_name
    if not src.is_dir():
        die(f"source skill folder not found: {src}")

    today_dir = BACKUPS_DIR / today_str()
    today_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_dest(today_dir, skill_name)
    dest.mkdir(parents=True)

    file_list: list[tuple[Path, int]] = []
    for abs_path, rel in iter_skill_files(src):
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(abs_path, out)
        file_list.append((rel, abs_path.stat().st_size))

    manifest = dest / "BACKUP_MANIFEST.md"
    total_bytes = sum(b for _, b in file_list)
    lines = [
        f"# Backup manifest — {skill_name}",
        "",
        f"- **Date:** {today_str()}",
        f"- **Source:** {src}",
        f"- **Dest:** {dest}",
        f"- **Files:** {len(file_list)}",
        f"- **Total bytes:** {total_bytes:,}",
    ]
    if args.reason:
        lines += ["", f"**Reason:** {args.reason}"]
    lines += ["", "## File list", ""]
    for rel, size in sorted(file_list):
        lines.append(f"- `{rel}` — {size:,} bytes")
    lines.append("")
    manifest.write_text("\n".join(lines), encoding="utf-8")

    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
