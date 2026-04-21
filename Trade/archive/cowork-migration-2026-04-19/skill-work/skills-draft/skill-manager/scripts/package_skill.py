#!/usr/bin/env python3
"""Zip a skill folder from /mnt/Trade/skills-draft/<name>/ for Windows install.

Usage:
    python package_skill.py <skill-name> [--out <path>]

Prints the output zip path on stdout. Exits non-zero on error.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from _common import DRAFTS_DIR, die, iter_skill_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    src = DRAFTS_DIR / args.skill_name
    if not src.is_dir():
        die(f"draft folder not found: {src}")

    out_path = args.out or (DRAFTS_DIR / f"{args.skill_name}.zip")

    # Overwrite any prior zip — the draft is the source of truth.
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for abs_path, rel in iter_skill_files(src):
            # Put everything under <skill-name>/... so Expand-Archive creates
            # the target folder automatically.
            arcname = Path(args.skill_name) / rel
            zf.write(abs_path, arcname=str(arcname))

    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
