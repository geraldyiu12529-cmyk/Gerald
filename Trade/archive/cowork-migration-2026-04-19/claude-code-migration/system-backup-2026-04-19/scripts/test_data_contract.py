#!/usr/bin/env python3
"""
Data-contract regression test for the audit-data pipeline.

Guards against the 2026-04-17 failure mode: the Yahoo fetcher drifting from
the shape compute_audit_additions expects (missing SPY column, wrong FF5
column count, etc.) without any test catching it until live trading.

Run manually:   python3 test_data_contract.py
Run in CI:      any non-zero exit means the data contract is broken.
Wire into quarterly-methodology-review so drift is caught at each audit.

Checks:
  A. Yahoo fetcher output includes SPY and all 12 single stocks in the header.
  B. Yahoo fetcher produces >= 12 months of rows (need 12 for residual window).
  C. Schema canary flags a bad CSV (missing SPY) and passes a good one.
  D. compute_audit_additions.compute_residual_momentum() succeeds end-to-end
     when given a healthy 6-col FF5 + stock_returns with SPY.
"""

import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

PASSED = FAILED = 0


def check(name, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"  PASS  {name}")
    else:
        FAILED += 1
        print(f"  FAIL  {name}  —  {detail}")


def _isolated_env():
    """Fresh temp dirs for cache + working, isolated from prod."""
    root = Path(tempfile.mkdtemp(prefix="data_contract_"))
    (root / "cache").mkdir()
    (root / "work").mkdir()
    return root


# ─── Test A: Yahoo fetcher output shape ──────────────────────────────────────
print("\n== Test A: Yahoo fetcher produces expected shape ==")
try:
    import fetch_ff5_from_french_library as fetcher

    # Redirect its DATA_DIR to a scratch location
    scratch = _isolated_env()
    fetcher.DATA_DIR = scratch / "work"

    # Also isolate cache_manager so we don't pollute prod cache
    import cache_manager as cm
    cm.CACHE_DIR = scratch / "cache"
    cm.MANIFEST_PATH = cm.CACHE_DIR / "manifest.json"

    csv = fetcher.fetch_stock_returns_from_yahoo()
    check("Yahoo fetcher returned content", csv is not None and len(csv) > 100,
          f"got {type(csv).__name__}, len={len(csv) if csv else 0}")

    if csv:
        header = csv.split("\n", 1)[0]
        cols = [c.strip().upper() for c in header.split(",")]
        check("Header includes SPY", "SPY" in cols, f"header={header}")
        for t in ["NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
                  "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"]:
            check(f"Header includes {t}", t in cols)
        rows = csv.strip().split("\n")[1:]
        check("At least 12 months of rows", len(rows) >= 12,
              f"got {len(rows)} rows")
except Exception as e:
    check("Yahoo fetcher runs without error", False, str(e))

# ─── Test B: schema canary behavior ─────────────────────────────────────────
print("\n== Test B: schema canary flags / passes correctly ==")
try:
    import preflight_health_check as phc

    # Bad cache: stock_returns missing SPY, FF5 too narrow
    bad = Path(tempfile.mkdtemp(prefix="bad_cache_"))
    (bad / "stock_returns.csv").write_text(
        "Date,NVDA,TSLA,AAPL\n202501,1,2,3\n"
    )
    (bad / "ff5_factors.csv").write_text("Date,Mkt-RF,SMB\n202501,1,2\n")
    phc.DATA_CACHE_DIR = bad
    bad_issues = phc._check_data_contract()
    check("Canary flags missing SPY",
          any("SPY" in i for i in bad_issues), str(bad_issues))
    check("Canary flags narrow FF5",
          any("ff5" in i.lower() and "need ≥6" in i for i in bad_issues),
          str(bad_issues))

    # Good cache
    good = Path(tempfile.mkdtemp(prefix="good_cache_"))
    good_tickers = ["SPY", "NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
                    "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"]
    (good / "stock_returns.csv").write_text(
        "Date," + ",".join(good_tickers) + "\n"
        "202501," + ",".join(["1"] * 13) + "\n"
    )
    (good / "ff5_factors.csv").write_text(
        "Date,Mkt-RF,SMB,HML,RMW,CMA\n202501,1,2,3,4,5\n"
    )
    phc.DATA_CACHE_DIR = good
    good_issues = phc._check_data_contract()
    check("Canary passes a healthy cache", good_issues == [],
          f"issues={good_issues}")
except Exception as e:
    check("Schema-canary runs", False, str(e))

# ─── Test C: residual-momentum end-to-end with healthy inputs ───────────────
print("\n== Test C: compute_residual_momentum end-to-end ==")
try:
    # Fresh isolated env
    e2e = _isolated_env()
    os.environ["AUDIT_DATA_DIR"] = str(e2e / "work")

    # Isolate cache BEFORE (re)importing so fetch_bulk doesn't hit prod
    import cache_manager as cm
    cm.CACHE_DIR = e2e / "cache"
    cm.MANIFEST_PATH = cm.CACHE_DIR / "manifest.json"

    import importlib
    import data_retrieval_engine as dre
    importlib.reload(dre)
    import compute_audit_additions as caa
    importlib.reload(caa)
    caa.DATA_DIR = e2e / "work"

    # Healthy 24mo FF5 (6-col, no RF — exercises the tolerance)
    ff5_lines = ["Date,Mkt-RF,SMB,HML,RMW,CMA"]
    for y in (2024, 2025):
        for m in range(1, 13):
            ff5_lines.append(f"{y}{m:02d},{(m-6)*0.4},0.2,-0.1,0.1,0.05")
    (e2e / "work" / "ff5_factors.csv").write_text("\n".join(ff5_lines))

    # Healthy 24mo stock returns with SPY
    tickers = ["SPY"] + list(caa.SINGLE_STOCK_UNIVERSE)
    sr_lines = ["Date," + ",".join(tickers)]
    for y in (2024, 2025):
        for m in range(1, 13):
            row = [f"{(m-6)*0.3 + (i*0.05):.3f}" for i in range(len(tickers))]
            sr_lines.append(f"{y}{m:02d}," + ",".join(row))
    (e2e / "work" / "stock_returns.csv").write_text("\n".join(sr_lines))

    result, err = caa.compute_residual_momentum()
    check("Primary FF5 path succeeds on healthy inputs",
          result is not None and err is None, f"err={err}")
    if result:
        ok = sum(1 for v in result.values() if v.get("status") == "OK")
        check("All 12 single stocks produce OK", ok == 12, f"got {ok}/12")

except Exception as e:
    import traceback
    check("End-to-end runs without exception", False,
          f"{e}\n{traceback.format_exc()}")

# ─── Test D: cache-schema stamping ──────────────────────────────────────────
print("\n== Test D: cache-schema stamping enforces contract ==")
try:
    import importlib
    import cache_manager as cm
    importlib.reload(cm)

    # Fresh isolated cache dir
    stamp_env = Path(tempfile.mkdtemp(prefix="schema_stamp_"))
    cm.CACHE_DIR = stamp_env
    cm.MANIFEST_PATH = cm.CACHE_DIR / "manifest.json"

    # D1: write refuses bad stock_returns (no SPY)
    bad = "Date,NVDA,TSLA,AAPL\n202501,1,2,3\n"
    try:
        cm.write_bulk_cache("stock_returns.csv", bad, 1, "bad-test")
        check("Write rejects stock_returns missing SPY", False,
              "no SchemaViolation raised")
    except cm.SchemaViolation as e:
        check("Write rejects stock_returns missing SPY",
              "SPY" in str(e).upper(), f"got: {e}")

    # D2: write accepts good stock_returns and stamps signature
    tickers = ["SPY", "NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
               "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"]
    good = ("Date," + ",".join(tickers) + "\n"
            + "\n".join(f"2025{m:02d}," + ",".join(["1"]*13)
                        for m in range(1, 13)) + "\n")
    cm.write_bulk_cache("stock_returns.csv", good, 1, "good-test",
                        rows=12, latest_date="202512")
    meta_path = cm.CACHE_DIR / "stock_returns.csv.meta.json"
    import json as _j
    meta = _j.loads(meta_path.read_text())
    check("Sidecar has schema block", "schema" in meta,
          f"meta keys={list(meta.keys())}")
    check("Schema.has_required=True",
          meta.get("schema", {}).get("has_required") is True,
          str(meta.get("schema")))

    # D3: read returns the stamped cache
    got = cm.read_bulk_cache("stock_returns.csv")
    check("Read accepts stamped cache", got is not None,
          "read returned None")

    # D4: drift detection — clobber file with an incompatible shape without
    # re-stamping; read should refuse and return None.
    (cm.CACHE_DIR / "stock_returns.csv").write_text(
        "Date,FOO,BAR\n202501,1,2\n"
    )
    got2 = cm.read_bulk_cache("stock_returns.csv")
    check("Read refuses drifted shape (stamp mismatch)", got2 is None,
          f"got: {got2}")

    # D5: FF5 allow_schema_violation=True path (future-proofing for RF-less files)
    ff5_stamp_env = Path(tempfile.mkdtemp(prefix="ff5_stamp_"))
    cm.CACHE_DIR = ff5_stamp_env
    ff5_good = "Date,Mkt-RF,SMB,HML,RMW,CMA\n202501,1,2,3,4,5\n"
    cm.write_bulk_cache("ff5_factors.csv", ff5_good, 1, "ff5-test",
                        rows=1, latest_date="202501")
    got_ff5 = cm.read_bulk_cache("ff5_factors.csv")
    check("FF5 6-col cache reads back OK", got_ff5 is not None,
          "6-col FF5 rejected (should be allowed)")

except Exception as e:
    import traceback
    check("Cache-stamping runs without exception", False,
          f"{e}\n{traceback.format_exc()}")

# ─── Summary ────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"RESULTS: {PASSED} passed, {FAILED} failed")
print(f"{'='*50}")
sys.exit(0 if FAILED == 0 else 1)
