#!/usr/bin/env python3
"""
Persistent cache layer for the data retrieval pipeline.

Provides read/write/staleness classification for all Grade A variables.
Cache lives on persistent workspace storage (/mnt/Trade/.data-cache/),
NOT /tmp/ — survives session restarts.

Staleness tiers:
  LIVE        — fetched this run
  STALE-OK    — within staleness window, full scoring weight
  STALE-WARN  — 1-2x staleness window, score with caveat
  STALE-EXPIRED — >2x staleness window, treat as MISSING
"""

import json
import os
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path(os.environ.get(
    "DATA_CACHE_DIR",
    Path(__file__).resolve().parent.parent / ".data-cache"
))

# Staleness windows in days — how long a cached value remains decision-relevant.
# Varies by variable type: fast-moving (VIX) vs structural (ACM term premium).
STALENESS_WINDOWS = {
    # Cross-asset risk
    "VIX": 1, "VIX3M": 1, "VIX_VIX3M": 1, "MOVE": 1, "DXY": 1,
    "HY_OAS": 2, "NFCI": 7, "Intermediary_Cap_Ratio": 14, "Intermediary_Cap_Z": 14,

    # Rates
    "DGS2": 1, "DGS10": 1, "2s10s": 1, "DFII10": 1, "T10YIE": 1,
    "ACM_TP_10Y": 30, "Forward_Rate_Factor": 7,

    # Equities — prices
    "SPX": 1, "NDX": 1, "SPY": 1, "QQQ": 1, "EWJ": 1, "EWY": 1,
    "NVDA": 1, "TSLA": 1, "AAPL": 1, "GOOGL": 1, "AMZN": 1, "META": 1,
    "TSM": 1, "INTC": 1, "MU": 1, "PYPL": 1, "PLTR": 1, "WDC": 1,
    "Revision_Breadth": 7,

    # Equities — derived
    "FF5_Factors": 60,  # monthly factors, 12m regression barely changes
    "Stock_Returns": 30,  # monthly stock returns

    # Commodities — prices
    "Brent": 1, "WTI": 1, "Gold": 1, "Silver": 1, "Copper": 1,
    "Palladium": 1, "Platinum": 1,

    # Commodities — derived
    "Futures_Curves": 2,
    "BasisMom_Brent_4w": 5, "BasisMom_Brent_12w": 5,
    "BasisMom_WTI_4w": 5, "BasisMom_WTI_12w": 5,
    "BasisMom_Gold_4w": 5, "BasisMom_Gold_12w": 5,
    "BasisMom_Silver_4w": 5, "BasisMom_Silver_12w": 5,
    "BasisMom_Copper_4w": 5, "BasisMom_Copper_12w": 5,
    "EIA_Crude_Stocks": 7,

    # FX
    "EURUSD": 1, "USDJPY": 1, "GBPUSD": 1, "AUDUSD": 1,

    # Crypto — 24/7 market, tighter windows
    "BTC": 0.17,  # ~4 hours
    "ETH": 0.17,
    "BTC_RealizedVol": 2,
    "BTC_ActiveAddr": 2, "BTC_HashRate": 3,
    "BTC_ExchNetflow": 2, "BTC_ETF_Flow": 1,
    "BTC_PerpFunding": 1, "BTC_3mBasis": 2,
    "ETH_ETF_Flow": 1, "ETH_DailyTxns": 2,

    # Bulk data files
    "ff5_factors.csv": 60,
    "stock_returns.csv": 30,
    "pd_statistics.csv": 14,
    "futures_curves.csv": 2,
}

# Default staleness window for variables not in the map
DEFAULT_STALENESS_DAYS = 1


# ─── Bulk-CSV schema contracts ────────────────────────────────────────────────
# Added 2026-04-17 after the residual-momentum defect: the persistent cache held
# a stock_returns.csv without an SPY column. compute_audit_additions silently
# fell through to a fallback that then failed on the same missing column.
#
# Each contract lists REQUIRED case-insensitive column names. On write we refuse
# content that doesn't satisfy the contract (fail loud at the fetcher, not at
# the compute consumer). On read we recompute the signature from the current
# file and compare to the sidecar stamp — mismatch => return None so the caller
# re-fetches rather than serving stale incompatible shape.
BULK_CACHE_SCHEMAS = {
    "stock_returns.csv": {
        "required_cols": ["DATE", "SPY", "NVDA", "TSLA", "AAPL", "GOOGL",
                          "AMZN", "META", "TSM", "INTC", "MU", "PYPL",
                          "PLTR", "WDC"],
        "schema_version": 2,  # v1 had no SPY; v2 adds SPY for market-model fallback
    },
    "ff5_factors.csv": {
        # Date + 5 factors minimum. RF optional — the 2026-04-17 patch synthesizes
        # RF=0 when absent rather than failing.
        "required_cols": ["DATE", "Mkt-RF", "SMB", "HML", "RMW", "CMA"],
        "schema_version": 1,
    },
}
SCHEMA_CONTRACT_VERSION = 1  # bump if the CONTRACT framework itself changes


def _header_cols(content: str) -> list:
    """Return upper-case column names from the first line of a CSV string."""
    if not content:
        return []
    header = content.split("\n", 1)[0]
    return [c.strip().upper() for c in header.split(",") if c.strip()]


def _compute_schema_signature(filename: str, content: str) -> dict:
    """
    Compute the schema signature for a bulk CSV.

    Returns dict with:
      contract_version — bumps when the stamping framework itself changes
      schema_version   — bumps when the required columns for this file change
      header_cols      — list of normalized column names in the file
      cols_hash        — short hash over sorted(header_cols) for fast compare
      has_required     — bool, True iff every required col is present
      missing_cols     — list of required cols absent from header
    """
    import hashlib

    contract = BULK_CACHE_SCHEMAS.get(filename, {})
    required = [c.upper() for c in contract.get("required_cols", [])]
    cols = _header_cols(content)
    cols_set = set(cols)
    missing = [c for c in required if c not in cols_set]
    cols_hash = hashlib.sha1(
        ",".join(sorted(cols)).encode("utf-8")
    ).hexdigest()[:12]
    return {
        "contract_version": SCHEMA_CONTRACT_VERSION,
        "schema_version": contract.get("schema_version", 0),
        "header_cols": cols,
        "cols_hash": cols_hash,
        "has_required": not missing,
        "missing_cols": missing,
    }


class SchemaViolation(Exception):
    """Raised when write_bulk_cache is handed content that fails the contract."""
    pass


def _ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(variable: str) -> Path:
    """Get the cache file path for a variable."""
    # Sanitize variable name for filesystem
    safe_name = variable.replace("/", "_").replace("\\", "_").replace(" ", "_")
    if safe_name.endswith(".csv"):
        return CACHE_DIR / safe_name
    return CACHE_DIR / f"{safe_name}.json"


def _sidecar_path(csv_filename: str) -> Path:
    """Get the metadata sidecar path for a bulk CSV cache file."""
    return CACHE_DIR / f"{csv_filename}.meta.json"


def get_staleness_window(variable: str) -> float:
    """Get the staleness window in days for a variable."""
    return STALENESS_WINDOWS.get(variable, DEFAULT_STALENESS_DAYS)


def classify_staleness(variable: str, timestamp: str) -> str:
    """
    Classify a cached value's staleness.

    Args:
        variable: Variable name
        timestamp: ISO 8601 timestamp of when the value was fetched

    Returns:
        "LIVE", "STALE-OK", "STALE-WARN", or "STALE-EXPIRED"
    """
    try:
        cached_time = datetime.fromisoformat(timestamp)
    except (ValueError, TypeError):
        return "STALE-EXPIRED"

    now = datetime.now(cached_time.tzinfo) if cached_time.tzinfo else datetime.now()
    age = now - cached_time
    age_days = age.total_seconds() / 86400

    window = get_staleness_window(variable)

    # Just fetched (within last hour)
    if age_days < 0.042:  # ~1 hour
        return "LIVE"
    # Within staleness window
    elif age_days <= window:
        return "STALE-OK"
    # 1-2x staleness window
    elif age_days <= window * 2:
        return "STALE-WARN"
    # Beyond 2x staleness window
    else:
        return "STALE-EXPIRED"


def write_cache(variable: str, value: Any, source_tier: int, source_name: str,
                unit: str = "", raw_snippet: str = "", timestamp: str = None):
    """
    Write a single variable value to the persistent cache.

    Args:
        variable: Variable name (e.g., "VIX", "DGS10")
        value: The value to cache (float, int, dict, etc.)
        source_tier: Which retrieval tier produced this (1, 2, 3)
        source_name: Human-readable source (e.g., "Yahoo Finance API")
        unit: Unit of measurement (e.g., "index", "percent", "USD")
        raw_snippet: Brief excerpt of raw response for audit
        timestamp: ISO 8601 timestamp; defaults to now
    """
    _ensure_cache_dir()

    if timestamp is None:
        timestamp = datetime.now().astimezone().isoformat()

    entry = {
        "variable": variable,
        "value": value,
        "unit": unit,
        "timestamp": timestamp,
        "source_tier": source_tier,
        "source_name": source_name,
        "staleness_window_days": get_staleness_window(variable),
        "raw_response_snippet": raw_snippet[:200] if raw_snippet else ""
    }

    path = _cache_path(variable)
    with open(path, 'w') as f:
        json.dump(entry, f, indent=2, default=str)

    # Update manifest
    _update_manifest(variable, timestamp, source_tier, source_name)


def read_cache(variable: str) -> Optional[dict]:
    """
    Read a cached value with staleness classification.

    Returns:
        dict with keys: variable, value, timestamp, source_tier, source_name,
        staleness, age_days — or None if no cache exists.
    """
    path = _cache_path(variable)
    if not path.exists():
        return None

    try:
        with open(path) as f:
            entry = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

    timestamp = entry.get("timestamp", "")
    staleness = classify_staleness(variable, timestamp)

    # If expired, return None (treat as MISSING)
    if staleness == "STALE-EXPIRED":
        return None

    # Compute age
    try:
        cached_time = datetime.fromisoformat(timestamp)
        now = datetime.now(cached_time.tzinfo) if cached_time.tzinfo else datetime.now()
        age_days = (now - cached_time).total_seconds() / 86400
    except (ValueError, TypeError):
        age_days = -1

    return {
        "variable": variable,
        "value": entry.get("value"),
        "unit": entry.get("unit", ""),
        "timestamp": timestamp,
        "source_tier": entry.get("source_tier", 3),
        "source_name": entry.get("source_name", "cache"),
        "staleness": staleness,
        "age_days": round(age_days, 2)
    }


def write_bulk_cache(filename: str, content: str, source_tier: int,
                     source_name: str, rows: int = 0, latest_date: str = "",
                     allow_schema_violation: bool = False):
    """
    Write a bulk CSV file to the persistent cache with metadata sidecar.

    Args:
        filename: CSV filename (e.g., "ff5_factors.csv")
        content: Full CSV content as string
        source_tier: Which retrieval tier produced this
        source_name: Human-readable source
        rows: Number of data rows (excluding header)
        latest_date: Most recent date in the data
        allow_schema_violation: If True, stamp the signature but don't refuse
            non-compliant content. Default False — a fetcher that produces a
            broken shape should fail loudly at the write site, not silently
            poison the cache for the compute consumer.

    Raises:
        SchemaViolation: when content violates the BULK_CACHE_SCHEMAS contract
            for this filename and allow_schema_violation=False.
    """
    _ensure_cache_dir()

    # ── Schema contract gate (added 2026-04-17) ──
    # Compute the signature BEFORE writing so a malformed fetch never lands
    # in cache. This is the belt for the suspenders that the compute-side
    # canary provides in preflight_health_check._check_data_contract().
    sig = _compute_schema_signature(filename, content)
    if filename in BULK_CACHE_SCHEMAS and not sig["has_required"] \
            and not allow_schema_violation:
        raise SchemaViolation(
            f"{filename} content missing required columns "
            f"{sig['missing_cols']}; refusing to pollute cache. "
            f"(Got header cols: {sig['header_cols'][:20]})"
        )

    # Write the CSV
    csv_path = CACHE_DIR / filename
    with open(csv_path, 'w') as f:
        f.write(content)

    # Write metadata sidecar
    timestamp = datetime.now().astimezone().isoformat()
    meta = {
        "file": filename,
        "rows": rows,
        "latest_date": latest_date,
        "timestamp": timestamp,
        "source_tier": source_tier,
        "source_name": source_name,
        "staleness_window_days": get_staleness_window(filename),
        "schema": sig,
    }

    sidecar = _sidecar_path(filename)
    with open(sidecar, 'w') as f:
        json.dump(meta, f, indent=2)

    _update_manifest(filename, timestamp, source_tier, source_name)


def read_bulk_cache(filename: str) -> Optional[dict]:
    """
    Read a bulk CSV cache file with staleness check.

    Returns:
        dict with keys: file_path (Path), content (str), rows, latest_date,
        timestamp, staleness, age_days — or None if no cache or expired.
    """
    csv_path = CACHE_DIR / filename
    sidecar = _sidecar_path(filename)

    if not csv_path.exists() or not sidecar.exists():
        return None

    try:
        with open(sidecar) as f:
            meta = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

    timestamp = meta.get("timestamp", "")
    staleness = classify_staleness(filename, timestamp)

    if staleness == "STALE-EXPIRED":
        return None

    try:
        with open(csv_path) as f:
            content = f.read()
    except IOError:
        return None

    # ── Schema signature verification (added 2026-04-17) ──
    # Recompute signature from the file currently on disk and compare to the
    # sidecar stamp. Three failure modes trigger a re-fetch (return None):
    #   (a) sidecar predates stamping and has no schema block
    #   (b) required columns are missing from the current file
    #   (c) the file's column hash doesn't match the stamp — shape drifted
    #       between write and read, or the stamp is stale
    # This is the layer that would have prevented the 2026-04-17 silent
    # fall-through: an old no-SPY cache from a previous schema version would
    # have been refused on read and re-hydrated from Tier 1 (Yahoo).
    if filename in BULK_CACHE_SCHEMAS:
        stamped = meta.get("schema")
        live_sig = _compute_schema_signature(filename, content)
        if not stamped:
            # Pre-stamping cache — don't trust it; force re-fetch.
            return None
        expected_schema_version = BULK_CACHE_SCHEMAS[filename]["schema_version"]
        if stamped.get("schema_version", -1) != expected_schema_version:
            return None
        if not live_sig["has_required"]:
            return None
        if stamped.get("cols_hash") != live_sig["cols_hash"]:
            return None

    try:
        cached_time = datetime.fromisoformat(timestamp)
        now = datetime.now(cached_time.tzinfo) if cached_time.tzinfo else datetime.now()
        age_days = (now - cached_time).total_seconds() / 86400
    except (ValueError, TypeError):
        age_days = -1

    return {
        "file_path": csv_path,
        "content": content,
        "rows": meta.get("rows", 0),
        "latest_date": meta.get("latest_date", ""),
        "timestamp": timestamp,
        "source_tier": meta.get("source_tier", 3),
        "source_name": meta.get("source_name", "cache"),
        "staleness": staleness,
        "age_days": round(age_days, 2),
        "schema": meta.get("schema", {}),
    }


def copy_bulk_to_working(filename: str, dest_dir: str = "/tmp/audit-data") -> Optional[Path]:
    """
    Copy a cached bulk CSV to the working directory for compute scripts.

    Returns the destination path, or None if no cache available.
    """
    cached = read_bulk_cache(filename)
    if cached is None:
        return None

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    dest_path = dest / filename

    with open(dest_path, 'w') as f:
        f.write(cached["content"])

    return dest_path


def _update_manifest(variable: str, timestamp: str, source_tier: int, source_name: str):
    """Update the manifest index with a cache entry."""
    manifest_path = CACHE_DIR / "manifest.json"

    manifest = {}
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
        except (json.JSONDecodeError, IOError):
            manifest = {}

    manifest[variable] = {
        "timestamp": timestamp,
        "source_tier": source_tier,
        "source_name": source_name,
        "staleness_window_days": get_staleness_window(variable)
    }

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


def get_cache_coverage() -> dict:
    """
    Get a summary of cache coverage — how many Grade A variables have valid caches.

    Returns:
        dict with total, cached, expired, missing counts and lists.
    """
    all_vars = [k for k in STALENESS_WINDOWS.keys() if not k.endswith(".csv")]
    cached = []
    expired = []
    missing = []

    for var in all_vars:
        result = read_cache(var)
        if result is not None:
            cached.append({"variable": var, "staleness": result["staleness"],
                          "age_days": result["age_days"]})
        else:
            # Check if there's an expired cache file
            path = _cache_path(var)
            if path.exists():
                expired.append(var)
            else:
                missing.append(var)

    return {
        "total": len(all_vars),
        "cached": len(cached),
        "expired": len(expired),
        "missing": len(missing),
        "cached_details": cached,
        "expired_variables": expired,
        "missing_variables": missing,
        "coverage_pct": round(len(cached) / max(len(all_vars), 1) * 100, 1)
    }


def append_retrieval_log(date: str, task: str, variables_attempted: int,
                         tier1_success: int, tier2_success: int,
                         tier3_cache: int, tier4_missing: int,
                         missing_vars: list, stale_vars: list,
                         retrieval_time_sec: float = 0):
    """
    Append a retrieval summary to the JSONL log.
    """
    _ensure_cache_dir()
    log_path = CACHE_DIR / "retrieval-log.jsonl"

    entry = {
        "date": date,
        "task": task,
        "variables_attempted": variables_attempted,
        "tier1_success": tier1_success,
        "tier2_success": tier2_success,
        "tier3_cache_used": tier3_cache,
        "tier4_missing": tier4_missing,
        "missing_variables": missing_vars,
        "stale_variables": stale_vars,
        "total_retrieval_time_sec": round(retrieval_time_sec, 1),
        "timestamp": datetime.now().astimezone().isoformat()
    }

    with open(log_path, 'a') as f:
        f.write(json.dumps(entry) + "\n")


# --- Convenience functions for the pipeline ---

def ensure_working_csvs(dest_dir: str = "/tmp/audit-data") -> dict:
    """
    Ensure all bulk CSV files needed by compute_audit_additions.py exist
    in the working directory. Copies from persistent cache if available.

    Returns dict of {filename: {"status": "OK"/"MISSING", "source": ..., "staleness": ...}}
    """
    required_files = ["ff5_factors.csv", "stock_returns.csv",
                      "pd_statistics.csv", "futures_curves.csv"]
    results = {}

    for filename in required_files:
        dest_path = Path(dest_dir) / filename
        if dest_path.exists():
            # Already in working dir (placed by current run's web search)
            results[filename] = {"status": "OK", "source": "working_dir", "staleness": "LIVE"}
        else:
            # Try to copy from persistent cache
            cached_path = copy_bulk_to_working(filename, dest_dir)
            if cached_path:
                cached = read_bulk_cache(filename)
                results[filename] = {
                    "status": "OK",
                    "source": "persistent_cache",
                    "staleness": cached["staleness"] if cached else "unknown",
                    "age_days": cached["age_days"] if cached else -1
                }
            else:
                results[filename] = {"status": "MISSING", "source": "none", "staleness": "n/a"}

    return results


if __name__ == "__main__":
    """Quick self-test and cache status report."""
    print("=== Cache Manager Status ===")
    print(f"Cache dir: {CACHE_DIR}")
    print(f"Exists: {CACHE_DIR.exists()}")
    print()

    coverage = get_cache_coverage()
    print(f"Cache coverage: {coverage['cached']}/{coverage['total']} "
          f"({coverage['coverage_pct']}%)")
    print(f"  Expired: {coverage['expired']}")
    print(f"  No cache: {len(coverage['missing_variables'])}")

    if coverage['cached_details']:
        print("\nCached variables:")
        for c in sorted(coverage['cached_details'], key=lambda x: x['variable']):
            print(f"  {c['variable']:25s} {c['staleness']:12s} ({c['age_days']:.1f}d old)")

    # Check bulk caches
    print("\nBulk CSV caches:")
    for fn in ["ff5_factors.csv", "stock_returns.csv", "pd_statistics.csv", "futures_curves.csv"]:
        result = read_bulk_cache(fn)
        if result:
            print(f"  {fn:25s} {result['staleness']:12s} ({result['age_days']:.1f}d old, {result['rows']} rows)")
        else:
            print(f"  {fn:25s} NOT CACHED")
