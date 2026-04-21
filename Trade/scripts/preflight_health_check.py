#!/usr/bin/env python3
"""
Pre-flight health check for the data pipeline.

Runs 5 minutes before the main pipeline starts (19:45 UTC+8).
Tests connectivity to key data sources, checks cache coverage,
and writes a status file for downstream tasks to read.

If a source is flagged as down, the audit-data-compute task
skips Tier 1 for that source (saving timeout delays) and goes
straight to Tier 2.

Output: ./pipeline/.pipeline-health.json
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pipeline_status import TRADE_DIR as _TRADE_DIR
OUTPUT_PATH = str(_TRADE_DIR / "pipeline" / ".pipeline-health.json")

# Derive cache dir from cache_manager so tests and prod agree on path.
try:
    from cache_manager import CACHE_DIR as DATA_CACHE_DIR  # type: ignore
except ImportError:
    DATA_CACHE_DIR = _TRADE_DIR / ".data-cache"


def _check_data_contract() -> list:
    """
    Validate the shape of cached bulk CSVs before compute consumes them.

    Catches the 2026-04-17 failure mode: an older cache had stock_returns.csv
    without an SPY column and ff5_factors.csv with only 6 cols (no RF). The
    compute script then silently fell through to a fallback path that
    itself failed, blocking all 12 single-stock T-scores.

    Returns a list of human-readable issue strings. Empty list = all OK.
    """
    issues = []

    # stock_returns.csv — must contain SPY
    stock_path = DATA_CACHE_DIR / "stock_returns.csv"
    if stock_path.exists():
        try:
            header = stock_path.read_text().split("\n", 1)[0]
            cols = [c.strip().upper() for c in header.split(",")]
            if "SPY" not in cols:
                issues.append(
                    "stock_returns.csv missing SPY column (market-model "
                    "regressor required by compute_audit_additions)"
                )
            stock_tickers = {"NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
                             "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"}
            missing_stocks = stock_tickers - set(cols)
            if missing_stocks:
                issues.append(
                    f"stock_returns.csv missing single-stock columns: "
                    f"{sorted(missing_stocks)}"
                )
        except Exception as e:
            issues.append(f"stock_returns.csv read error: {e}")
    else:
        issues.append("stock_returns.csv absent from cache")

    # ff5_factors.csv — must have ≥6 columns (Date + 5 factors; RF optional)
    ff5_path = DATA_CACHE_DIR / "ff5_factors.csv"
    if ff5_path.exists():
        try:
            header = ff5_path.read_text().split("\n", 1)[0]
            n_cols = len([c for c in header.split(",") if c.strip()])
            if n_cols < 6:
                issues.append(
                    f"ff5_factors.csv has {n_cols} cols, need ≥6 "
                    f"(Date + 5 factors)"
                )
        except Exception as e:
            issues.append(f"ff5_factors.csv read error: {e}")
    else:
        issues.append("ff5_factors.csv absent from cache")

    return issues


def check_source(name: str, url: str, timeout: int = 8) -> dict:
    """Test connectivity to a data source. Returns status dict."""
    import urllib.request
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            size = len(resp.read())
            elapsed = time.time() - start
            return {
                "available": True,
                "response_time_ms": round(elapsed * 1000),
                "response_size": size
            }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "available": False,
            "error": str(e)[:100],
            "response_time_ms": round(elapsed * 1000)
        }


def run_preflight() -> dict:
    """Run all preflight checks and return status dict."""
    print("=== Pre-Flight Health Check ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC+8\n")

    # Check all data sources
    sources = {
        "yahoo_finance": {
            "url": "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=1d&interval=1d",
            "variables_affected": ["VIX", "MOVE", "DXY", "All equity prices",
                                   "Commodities", "FX", "BTC/ETH (backup)"]
        },
        "coingecko": {
            "url": "https://api.coingecko.com/api/v3/ping",
            "variables_affected": ["BTC", "ETH"]
        },
        "blockchain_info": {
            "url": "https://api.blockchain.info/charts/market-price?timespan=1days&format=json",
            "variables_affected": ["BTC_ActiveAddr", "BTC_HashRate"]
        },
        "kenneth_french": {
            "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
            "variables_affected": ["FF5_Factors", "Residual_Momentum"]
        },
        "ny_fed": {
            "url": "https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics",
            "variables_affected": ["Intermediary_Capital"]
        },
        "barchart": {
            "url": "https://www.barchart.com/futures/quotes/CLK26/overview",
            "variables_affected": ["Futures_Curves", "Basis_Momentum"]
        },
        "chicago_fed": {
            "url": "https://www.chicagofed.org/research/data/nfci/current-data",
            "variables_affected": ["NFCI"]
        }
    }

    source_results = {}
    for name, config in sources.items():
        result = check_source(name, config["url"])
        source_results[name] = {
            **result,
            "variables_affected": config["variables_affected"]
        }
        status = "OK" if result["available"] else "DOWN"
        ms = result["response_time_ms"]
        print(f"  {name:20s} {status:4s} ({ms}ms)")

    # Check cache coverage
    cache_info = {"coverage_pct": 0, "cached": 0, "total": 0, "missing_variables": []}
    try:
        from cache_manager import get_cache_coverage
        cache_info = get_cache_coverage()
        print(f"\n  Cache coverage: {cache_info['cached']}/{cache_info['total']} "
              f"({cache_info['coverage_pct']}%)")
        if cache_info['missing_variables']:
            print(f"  No cache for: {', '.join(cache_info['missing_variables'][:10])}")
    except ImportError:
        print("\n  Cache: unavailable (cache_manager not found)")

    # ── Schema canary ──
    # Added 2026-04-17 after the all-stocks-INC defect. The compute script
    # assumes (a) stock_returns.csv has an SPY column (market-model regressor),
    # and (b) ff5_factors.csv has ≥6 cols (Date + 5 factors, RF optional).
    # If the persistent cache violates either, compute will fail-loud downstream;
    # catch it here so the advisory fires BEFORE the brief/rec consume MISSING.
    schema_issues = _check_data_contract()
    if schema_issues:
        print("\n  Schema canary — DATA CONTRACT VIOLATIONS:")
        for issue in schema_issues:
            print(f"    ✗ {issue}")
    else:
        print("\n  Schema canary — OK (stock_returns has SPY, ff5 has ≥6 cols)")

    # Build skip list — variables whose Tier 1 source is down
    skip_tier1 = []
    variable_to_source = {
        "yahoo_finance": ["VIX", "VIX3M", "MOVE", "DXY", "DGS10",
                          "SPY", "QQQ", "SPX", "NDX", "EWJ", "EWY",
                          "NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
                          "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC",
                          "Brent", "WTI", "Gold", "Silver", "Copper",
                          "Palladium", "Platinum",
                          "EURUSD", "USDJPY", "GBPUSD", "AUDUSD",
                          "BTC", "ETH"],
        "coingecko": ["BTC", "ETH"],
        "blockchain_info": ["BTC_ActiveAddr", "BTC_HashRate"],
    }

    for source_name, vars_list in variable_to_source.items():
        if not source_results.get(source_name, {}).get("available", False):
            skip_tier1.extend(vars_list)
    skip_tier1 = list(set(skip_tier1))  # deduplicate

    # Build advisories
    advisories = []
    down_sources = [k for k, v in source_results.items() if not v["available"]]
    if down_sources:
        advisories.append(f"Sources down: {', '.join(down_sources)} — Tier 2/3 fallback active")
    if cache_info.get("coverage_pct", 0) < 50:
        advisories.append(f"Cache coverage low ({cache_info.get('coverage_pct', 0)}%) — "
                         f"MISSING risk elevated")
    # Schema-canary advisories are BLOCKING — they surface at the top of the
    # advisory list so the trade-rec can see them and refuse to promote
    # decisions that depend on the violated contract.
    if schema_issues:
        for issue in schema_issues:
            advisories.insert(0, f"SCHEMA VIOLATION — {issue}")
    if not down_sources and not schema_issues and cache_info.get("coverage_pct", 0) > 80:
        advisories.append("All systems nominal — high cache coverage")

    # Predict MISSING count
    predicted_missing = 0
    if down_sources:
        # Variables affected by down sources that have no cache
        uncovered = set(skip_tier1) & set(cache_info.get("missing_variables", []))
        predicted_missing = len(uncovered)
        if uncovered:
            advisories.append(f"Predicted MISSING (no cache + source down): "
                             f"{', '.join(sorted(uncovered))}")

    # Compose output
    status = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "sources": {k: {"available": v["available"],
                        "response_time_ms": v["response_time_ms"]}
                    for k, v in source_results.items()},
        "cache_coverage": f"{cache_info.get('cached', 0)}/{cache_info.get('total', 0)} variables",
        "cache_coverage_pct": cache_info.get("coverage_pct", 0),
        "schema_issues": schema_issues,
        "schema_ok": len(schema_issues) == 0,
        "predicted_missing": predicted_missing,
        "skip_tier1_for": skip_tier1,
        "advisories": advisories
    }

    # Write status file
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(status, f, indent=2)
    print(f"\n  Status written to: {OUTPUT_PATH}")

    if advisories:
        print("\n  Advisories:")
        for a in advisories:
            print(f"    → {a}")

    return status


def read_preflight_status() -> dict:
    """
    Read the latest preflight status. Called by downstream tasks.
    Returns the status dict, or empty dict with a warning if not available.
    """
    try:
        with open(OUTPUT_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "timestamp": "",
            "sources": {},
            "skip_tier1_for": [],
            "advisories": ["Preflight status not available — running without source hints"]
        }


if __name__ == "__main__":
    status = run_preflight()
    all_up = all(s["available"] for s in status["sources"].values())
    print(f"\n{'='*40}")
    print(f"Result: {'ALL SYSTEMS GO' if all_up else 'DEGRADED — fallbacks active'}")
    sys.exit(0)
