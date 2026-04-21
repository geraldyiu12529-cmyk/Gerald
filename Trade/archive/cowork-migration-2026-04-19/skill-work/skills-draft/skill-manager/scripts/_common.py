"""Shared helpers for skill-manager scripts. Stdlib only."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def _find_mount_root() -> Path:
    """Locate the mount root containing both Trade/ and .claude/skills/.

    The Cowork sandbox exposes paths as /sessions/<id>/mnt/... when reached
    through Bash, but /mnt/... when Claude reads via its Read tool. Scripts
    called from either side need to work, so we auto-detect.

    Override by setting SKILL_MANAGER_ROOT to the absolute path that contains
    `Trade/` and `.claude/skills/` as direct children.
    """
    env = os.environ.get("SKILL_MANAGER_ROOT")
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    candidates.append(Path("/mnt"))
    # Walk upward from this file to find an ancestor that has mnt/Trade and
    # mnt/.claude/skills. This handles /sessions/<id>/mnt/... paths.
    here = Path(__file__).resolve()
    for ancestor in [here.parent, *here.parents]:
        candidates.append(ancestor / "mnt")
        candidates.append(ancestor)

    for c in candidates:
        if (c / "Trade").is_dir() and (c / ".claude" / "skills").is_dir():
            return c
    # Fall back to /mnt — scripts will fail loudly on first read if it's wrong.
    return Path("/mnt")


_ROOT = _find_mount_root()
SKILLS_DIR = _ROOT / ".claude" / "skills"
TRADE_DIR = _ROOT / "Trade"
BACKUPS_DIR = TRADE_DIR / "skill-backups"
PATCHES_DIR = TRADE_DIR / "patches"
DRAFTS_DIR = TRADE_DIR / "skills-draft"

# Allow-list: the 11 custom trading skills that skill-manager operates on.
# Model tier is informational — used by scaffold to pre-fill frontmatter when
# the target is an extension of an existing tier (not enforced here).
TRADING_SKILLS: dict[str, str] = {
    "market-brief": "sonnet",
    "news-events": "sonnet",
    "daily-trade-rec": "opus",
    "pipeline-recovery": "haiku",
    "positions-monitor": "sonnet",
    "signal-review": "opus",
    "quarterly-methodology-review": "opus",
    "literature-review": "opus",
    "system-review": "opus",
    "trade-update": "sonnet",
    "consolidate-memory": "haiku",
}


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def die(msg: str, code: int = 2) -> None:
    """Fail-loud on stderr with a non-zero exit. Never swallow errors."""
    print(f"skill-manager: {msg}", file=sys.stderr)
    sys.exit(code)


def require_in_scope(skill_name: str, allow_override: bool = False) -> None:
    """Refuse to operate on skills outside the trading allow-list."""
    if skill_name in TRADING_SKILLS:
        return
    if allow_override:
        print(
            f"skill-manager: WARNING — '{skill_name}' is outside the trading "
            "allow-list. Proceeding because --force was set.",
            file=sys.stderr,
        )
        return
    die(
        f"'{skill_name}' is not in the trading allow-list. Run with --force to "
        "override, or see references/trading-skills.md."
    )


def read_frontmatter(md_path: Path) -> tuple[dict[str, str], str]:
    """Parse a SKILL.md-style YAML frontmatter. Returns (fields, body).

    Minimal parser — no external deps. Handles: ---\nk: v\n---\n<body>.
    Multi-line values not supported (SKILL.md frontmatter is single-line
    per convention).
    """
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fields[k.strip()] = v.strip()
    body = "\n".join(lines[end + 1 :])
    return fields, body


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


SKIP_SUFFIXES = (".pyc",)
SKIP_NAMES_AT_ROOT = {"test_edits.json"}  # smoke-test leftovers


def iter_skill_files(skill_dir: Path):
    """Yield every file in the skill folder, skipping cruft.

    Skips: dot-files/dot-dirs, __pycache__, .pyc, and a small set of
    known test artifacts at the root. Intentionally strict — if the skill
    is supposed to ship a file, it should be in scripts/ references/ or
    assets/, not at the root.
    """
    for p in skill_dir.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(skill_dir)
        parts = rel.parts
        if any(part.startswith(".") for part in parts):
            continue
        if "__pycache__" in parts:
            continue
        if p.suffix in SKIP_SUFFIXES:
            continue
        if len(parts) == 1 and parts[0] in SKIP_NAMES_AT_ROOT:
            continue
        yield p, rel
