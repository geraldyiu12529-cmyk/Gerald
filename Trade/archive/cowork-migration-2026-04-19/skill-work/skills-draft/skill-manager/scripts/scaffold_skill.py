#!/usr/bin/env python3
"""Scaffold a brand-new skill folder and package it.

Usage:
    python scaffold_skill.py <skill-name> --description "..." --model opus \
        [--title "Human title"] [--no-zip]

Creates /mnt/Trade/skills-draft/<skill-name>/ with a SKILL.md populated from
the template at assets/skill-template.md (token-substituted), plus empty
scripts/ references/ assets/ subdirectories. If --no-zip is not given,
zips the folder to /mnt/Trade/skills-draft/<skill-name>.zip.

Validates that the target name doesn't shadow an already-installed skill
(which would be ambiguous when Claude triggers).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _common import DRAFTS_DIR, SKILLS_DIR, die

VALID_MODELS = {"opus", "sonnet", "haiku"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name")
    ap.add_argument("--description", required=True)
    ap.add_argument("--model", required=True, choices=sorted(VALID_MODELS))
    ap.add_argument("--title", default=None)
    ap.add_argument("--no-zip", action="store_true")
    args = ap.parse_args()

    skill_name = args.skill_name
    # Name hygiene: lowercase, hyphens, no spaces.
    if not skill_name or any(c.isspace() for c in skill_name):
        die(f"invalid skill name: {skill_name!r}")
    if skill_name != skill_name.lower():
        die(f"skill name must be lowercase: {skill_name}")

    # Guard against shadowing existing skills.
    installed = SKILLS_DIR / skill_name
    if installed.exists():
        die(
            f"skill name '{skill_name}' already exists at {installed}. "
            "Pick a different name or back-up + patch the existing one instead."
        )

    draft_dir = DRAFTS_DIR / skill_name
    if draft_dir.exists():
        die(f"draft folder already exists: {draft_dir}. Remove it first.")

    # Load template.
    template_path = Path(__file__).parent.parent / "assets" / "skill-template.md"
    if not template_path.is_file():
        die(f"template not found: {template_path}")
    template = template_path.read_text(encoding="utf-8")

    title = args.title or skill_name.replace("-", " ").title()
    filled = (
        template.replace("{{SKILL_NAME}}", skill_name)
        .replace("{{ONE_LINE_DESCRIPTION}}", args.description)
        .replace("{{MODEL_TIER}}", args.model)
        .replace("{{SKILL_TITLE}}", title)
    )
    # Leave the trigger-phrase / step placeholders for the human to fill in.

    # Create the directory structure.
    draft_dir.mkdir(parents=True)
    (draft_dir / "scripts").mkdir()
    (draft_dir / "references").mkdir()
    (draft_dir / "assets").mkdir()
    (draft_dir / "SKILL.md").write_text(filled, encoding="utf-8")

    # Leave a README so empty subdirs are preserved in zip.
    for sub in ("scripts", "references", "assets"):
        (draft_dir / sub / ".gitkeep").write_text("", encoding="utf-8")

    # Package unless --no-zip.
    zip_path = DRAFTS_DIR / f"{skill_name}.zip"
    if not args.no_zip:
        pkg = Path(__file__).parent / "package_skill.py"
        proc = subprocess.run(
            [sys.executable, str(pkg), skill_name],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            die(f"package failed:\n{proc.stderr.strip()}")
        # package_skill.py prints the zip path
        zip_path = Path(proc.stdout.strip())

    # Print what was created for downstream consumption.
    print(str(draft_dir))
    if not args.no_zip:
        print(str(zip_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
