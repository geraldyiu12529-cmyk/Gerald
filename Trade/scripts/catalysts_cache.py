"""
catalysts_cache.py — Shared catalyst calendar artifact.

Purpose: E4 from system-review-2026-04-17.md. Eliminates 5-way duplication
of the catalyst calendar across news-events (§3), market-brief (§5),
trade-rec (§5/§8), weekly-review (§7), and Memory.md §6.

Write path: news-events at 20:10 UTC+8 calls write_catalysts() after
completing its category sweep.

Read path: market-brief and daily-trade-rec call read_catalysts() instead
of re-narrating the catalyst list. weekly-review and Memory sync can
optionally consume via latest_catalysts().

Schema is intentionally flat JSON for minimum-token read cost downstream.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


def _resolve_trade_dir() -> Path:
    if os.environ.get("TRADE_DIR"):
        return Path(os.environ["TRADE_DIR"])
    for candidate in [Path("/mnt/Trade"), Path(".")]:
        if (candidate / "Memory.md").exists():
            return candidate
    return Path("/mnt/Trade")

TRADE_DIR = _resolve_trade_dir()
CACHE_DIR = TRADE_DIR / ".catalysts-cache"
# Back-compat: also expose the cache at the root so brief/rec can find it
# via the same glob they use for news-YYYY-MM-DD.md.
ROOT_FILENAME_FMT = "catalysts-cache-{date}.json"

SEVERITY_ORDER = {"critical": 0, "high": 1, "med": 2, "low": 3}
VALID_DIRECTIONS = {"binary", "bullish_risk", "bearish_risk", "bullish_safe_haven", "bearish_safe_haven", "neutral"}


def _ensure_cache_dir() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_paths(date: str) -> tuple[Path, Path]:
    """Return (root_path, cache_dir_path). Both get written; either can be read."""
    fname = ROOT_FILENAME_FMT.format(date=date)
    return TRADE_DIR / fname, CACHE_DIR / fname


def _validate_catalyst(c: dict[str, Any]) -> list[str]:
    """Return list of validation errors; empty if OK."""
    errs: list[str] = []
    required = ("date", "event", "asset_impact", "severity")
    for k in required:
        if k not in c:
            errs.append(f"missing field: {k}")
    if "date" in c:
        try:
            datetime.strptime(c["date"], "%Y-%m-%d")
        except (ValueError, TypeError):
            errs.append(f"date must be YYYY-MM-DD, got {c['date']!r}")
    if "severity" in c and c["severity"] not in SEVERITY_ORDER:
        errs.append(f"severity must be one of {list(SEVERITY_ORDER)}, got {c['severity']!r}")
    if "direction_hint" in c and c["direction_hint"] not in VALID_DIRECTIONS:
        errs.append(f"direction_hint must be one of {VALID_DIRECTIONS}, got {c['direction_hint']!r}")
    if "asset_impact" in c and not isinstance(c["asset_impact"], list):
        errs.append("asset_impact must be a list of ticker strings")
    return errs


def write_catalysts(
    date: str,
    catalysts: list[dict[str, Any]],
    *,
    horizon_days: int = 30,
    generated_by: str = "news-events",
    strict: bool = True,
) -> Path:
    """
    Write the catalyst cache for `date`. Called by news-events at 20:10 UTC+8.

    Args:
        date: YYYY-MM-DD (the cache date, usually today).
        catalysts: list of dicts with fields {date, event, asset_impact,
                   severity, direction_hint?, source?, notes?}.
        horizon_days: how many days forward the list covers (metadata).
        generated_by: producer label.
        strict: raise on any validation error. Set False to warn-only.

    Returns:
        Path to the primary (root) cache file written.

    Raises:
        ValueError if `strict=True` and any catalyst fails validation.
    """
    _ensure_cache_dir()

    # Validate
    all_errs: list[str] = []
    for i, c in enumerate(catalysts):
        errs = _validate_catalyst(c)
        if errs:
            all_errs.extend(f"catalyst[{i}]: {e}" for e in errs)
    if all_errs:
        msg = f"catalysts validation failed:\n  - " + "\n  - ".join(all_errs)
        if strict:
            raise ValueError(msg)
        print(f"[catalysts_cache] WARN: {msg}")

    # Sort: severity asc (critical first), then date asc.
    catalysts_sorted = sorted(
        catalysts,
        key=lambda c: (SEVERITY_ORDER.get(c.get("severity", "low"), 3), c.get("date", "9999-99-99")),
    )

    payload = {
        "date": date,
        "generated_by": generated_by,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "horizon_days": horizon_days,
        "count": len(catalysts_sorted),
        "catalysts": catalysts_sorted,
    }

    root_path, cache_path = _cache_paths(date)
    for p in (root_path, cache_path):
        p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return root_path


def read_catalysts(date: str | None = None) -> dict[str, Any]:
    """
    Read the catalyst cache for `date`. If `date` is None, return latest.
    Called by market-brief and daily-trade-rec skills.

    Returns the full payload dict. Downstream producers access .catalysts.

    Raises:
        FileNotFoundError if no cache exists for the given date AND no fallback.
    """
    if date is not None:
        root_path, cache_path = _cache_paths(date)
        for p in (root_path, cache_path):
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"No catalysts cache for {date}; checked {root_path} and {cache_path}")

    return latest_catalysts()


def latest_catalysts(max_age_days: int = 3) -> dict[str, Any]:
    """
    Return the most recent catalyst cache (within max_age_days).
    Raises FileNotFoundError if nothing is fresh enough.
    """
    _ensure_cache_dir()
    today = datetime.now().date()
    # Check today → today-max_age_days
    for delta in range(max_age_days + 1):
        d = (today - timedelta(days=delta)).strftime("%Y-%m-%d")
        root_path, cache_path = _cache_paths(d)
        for p in (root_path, cache_path):
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError(
        f"No catalysts cache within {max_age_days} days of {today}. "
        f"news-events may have failed today; trade-rec should fall back to inline narrative."
    )


def filter_for_asset(payload: dict[str, Any], asset: str) -> list[dict[str, Any]]:
    """Return catalysts whose asset_impact list contains `asset` (case-insensitive)."""
    asset_u = asset.upper()
    return [
        c for c in payload.get("catalysts", [])
        if any(a.upper() == asset_u for a in c.get("asset_impact", []))
    ]


def filter_severity(payload: dict[str, Any], min_severity: str = "med") -> list[dict[str, Any]]:
    """Return catalysts with severity >= min_severity."""
    floor = SEVERITY_ORDER.get(min_severity, 2)
    return [c for c in payload.get("catalysts", []) if SEVERITY_ORDER.get(c.get("severity", "low"), 3) <= floor]


def to_markdown_table(payload: dict[str, Any], limit: int | None = None) -> str:
    """
    Render a compact markdown table. Replaces the 5-way duplicated calendar blocks.
    Used by brief, trade-rec, weekly-review for their catalyst section.
    """
    catalysts = payload.get("catalysts", [])
    if limit is not None:
        catalysts = catalysts[:limit]
    if not catalysts:
        return "_No catalysts in cache._"

    rows = [
        "| Date | Event | Assets | Severity | Direction |",
        "|---|---|---|---|---|",
    ]
    for c in catalysts:
        assets = ", ".join(c.get("asset_impact", []))
        direction = c.get("direction_hint", "—")
        rows.append(f"| {c['date']} | {c['event']} | {assets} | {c['severity']} | {direction} |")
    return "\n".join(rows)


# ---------- CLI helpers for ad-hoc / debugging ----------

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  catalysts_cache.py show [date]    # print latest or specific date")
        print("  catalysts_cache.py table [date]   # markdown table")
        print("  catalysts_cache.py asset <ticker> # filter latest by asset")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "show":
        d = sys.argv[2] if len(sys.argv) > 2 else None
        p = read_catalysts(d)
        print(json.dumps(p, indent=2))
    elif cmd == "table":
        d = sys.argv[2] if len(sys.argv) > 2 else None
        p = read_catalysts(d)
        print(to_markdown_table(p))
    elif cmd == "asset":
        if len(sys.argv) < 3:
            print("usage: catalysts_cache.py asset <ticker>")
            sys.exit(1)
        p = latest_catalysts()
        matches = filter_for_asset(p, sys.argv[2])
        print(json.dumps(matches, indent=2))
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)
