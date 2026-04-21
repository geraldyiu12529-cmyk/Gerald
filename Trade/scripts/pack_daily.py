#!/usr/bin/env python3
"""Pack same-day routine outputs into {YYYY-MM-DD}/daily-{YYYY-MM-DD}.md.

Each routine calls this helper after its skill completes. The helper:
  1. Creates the date folder if missing (mkdir -p {date}).
  2. Initialises {date}/daily-{date}.md with a header if it does not exist.
  3. Upserts the supplied content under a section anchor "## §X — {Title}".
  4. Re-runs on the same section are replaced (not appended), so same-day
     skill re-runs (e.g. brief v1 -> v2) refresh the section in-place.

Typical usage from a routine:
    python scripts/pack_daily.py --section D --source 2026-04-19/market-brief-2026-04-19.md
    python scripts/pack_daily.py --section H --title "Pipeline Recovery" --content "Healthy; no action."

Contract:
  --section {A..H}              canonical slot (see SECTION_TITLES)
  --title TEXT                  override default title
  --source PATH                 file to read; H1 stripped, rest inlined.
                                If the file does not exist, exit 0 silently
                                (nothing to pack — the skill produced nothing).
  --content TEXT                inline body (alternative to --source)
  --date YYYY-MM-DD             override today's date (for backfills)
  --status TEXT                 optional status tag shown in the section header
  --file-date YYYY-MM-DD        if --source uses a different date than --date
                                (rare; e.g. weekly review packing into Sunday file)

Default anchors (stable order in the daily file):
  A — US Close Snapshot               07:30 weekdays
  B — Preflight Audit Data            19:45 weekdays
  C — Preflight Meta-Additions        19:52 weekdays
  D — Market Brief                    20:00 weekdays
  E — News & Events                   20:10 weekdays
  F — Trade Recommendation            20:20 weekdays
  G — Positions Monitor               09:00 weekdays (silent-when-OK)
  H — Pipeline Recovery               22:00 weekdays (only on recovery action)
  W — Weekly Review                   Sunday
  S — Signal Review                   Sunday
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC8 = timezone(timedelta(hours=8))

SECTION_TITLES = {
    "A": "US Close Snapshot",
    "B": "Preflight — Audit Data Staging",
    "C": "Preflight — Meta-Additions Staging",
    "D": "Market Brief",
    "E": "News & Events",
    "F": "Trade Recommendation",
    "G": "Positions Monitor",
    "H": "Pipeline Recovery",
    "W": "Weekly Review",
    "S": "Signal Review",
}

SECTION_ORDER = ["A", "B", "C", "D", "E", "F", "G", "H", "W", "S"]


def today_str() -> str:
    return datetime.now(UTC8).strftime("%Y-%m-%d")


def now_hm() -> str:
    return datetime.now(UTC8).strftime("%H:%M UTC+8")


def strip_top_h1(text: str) -> str:
    return re.sub(r"^\s*#\s+[^\n]*\n+", "", text, count=1)


def init_daily(daily: Path, date_str: str) -> None:
    if daily.exists():
        return
    daily.write_text(
        f"# Daily Pipeline — {date_str} (UTC+8)\n\n"
        f"Consolidated output for all routines run this local date. "
        f"Per-routine source files (where applicable) live at workspace root.\n\n",
        encoding="utf-8",
    )


def upsert_section(
    daily: Path,
    section: str,
    title: str,
    body: str,
    source_name: str | None,
    status: str | None,
) -> None:
    anchor = f"## §{section} — {title}"
    meta_bits = [f"Packed: {now_hm()}"]
    if source_name:
        meta_bits.insert(0, f"Source: `{source_name}`")
    if status:
        meta_bits.append(f"Status: {status}")
    meta_line = " • ".join(meta_bits)

    new_section = f"{anchor}\n\n*{meta_line}*\n\n{body.strip()}\n\n"

    text = daily.read_text(encoding="utf-8")

    # Match from "## §X ..." up to the next "## §Y ..." or end of file.
    pattern = re.compile(
        r"^## §" + re.escape(section) + r" .*?(?=^## §|\Z)",
        re.DOTALL | re.MULTILINE,
    )

    m = pattern.search(text)
    if m:
        text = text[: m.start()] + new_section + text[m.end():]
    else:
        # Insert in canonical order: walk SECTION_ORDER and place before the
        # first section with a higher index that is already present.
        insert_idx: int | None = None
        target_idx = SECTION_ORDER.index(section) if section in SECTION_ORDER else 99
        for later in SECTION_ORDER[target_idx + 1:]:
            m2 = re.search(r"^## §" + re.escape(later) + r" ", text, re.MULTILINE)
            if m2:
                insert_idx = m2.start()
                break
        if insert_idx is not None:
            text = text[:insert_idx] + new_section + text[insert_idx:]
        else:
            text = text.rstrip() + "\n\n" + new_section

    daily.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True, choices=list(SECTION_TITLES.keys()))
    ap.add_argument("--title")
    ap.add_argument("--source")
    ap.add_argument("--content")
    ap.add_argument("--date")
    ap.add_argument("--file-date", dest="file_date")
    ap.add_argument("--status")
    args = ap.parse_args()

    date_str = args.date or today_str()
    date_folder = Path(date_str)
    date_folder.mkdir(parents=True, exist_ok=True)
    daily = date_folder / f"daily-{date_str}.md"
    title = args.title or SECTION_TITLES[args.section]

    if args.source:
        src = Path(args.source)
        if not src.exists():
            print(f"[pack_daily] source {src} not found; skipping §{args.section}.")
            return 0
        body = strip_top_h1(src.read_text(encoding="utf-8"))
        source_name = src.name
    elif args.content:
        body = args.content
        source_name = None
    else:
        print("[pack_daily] one of --source or --content is required", file=sys.stderr)
        return 2

    init_daily(daily, date_str)
    upsert_section(daily, args.section, title, body, source_name, args.status)
    print(f"[pack_daily] §{args.section} ({title}) -> {daily.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
