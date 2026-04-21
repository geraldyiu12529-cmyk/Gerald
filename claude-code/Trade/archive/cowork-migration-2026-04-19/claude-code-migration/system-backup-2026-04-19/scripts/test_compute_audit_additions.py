#!/usr/bin/env python3
"""
Unit tests for compute_audit_additions.py

Tests cover:
  1. Residual momentum — OLS, scoring, conflict detection
  2. Intermediary capital — z-score, R adjustment threshold
  3. Basis-momentum — spread changes, divergence-cap logic
  4. Missing data handling — graceful MISSING for each variable
  5. Staging file output format
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import date, timedelta

# Patch DATA_DIR before importing
TEST_DIR = tempfile.mkdtemp(prefix="audit_test_")
os.environ["AUDIT_DATA_DIR_OVERRIDE"] = TEST_DIR

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compute_audit_additions as caa

# Override DATA_DIR
caa.DATA_DIR = Path(TEST_DIR)

PASSED = 0
FAILED = 0


def check(name, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ✅ {name}")
    else:
        FAILED += 1
        print(f"  ❌ {name} — {detail}")


def write_csv(filename, content):
    path = Path(TEST_DIR) / filename
    with open(path, 'w') as f:
        f.write(content)
    return path


def cleanup():
    for f in Path(TEST_DIR).glob("*"):
        f.unlink()


# ============================================================
print("\n=== Test Suite 1: Residual Momentum ===\n")
# ============================================================

# Test 1.1: Missing FF5 file
cleanup()
result, err = caa.compute_residual_momentum()
check("Missing FF5 file returns None", result is None)
check("Error mentions ff5_factors.csv", "ff5_factors" in str(err))

# Test 1.2: Missing stock file
cleanup()
write_csv("ff5_factors.csv", "Date,Mkt-RF,SMB,HML,RMW,CMA,RF\n" +
    "\n".join(f"2025{m:02d},{1.0},{0.5},{-0.3},{0.2},{0.1},{0.35}" for m in range(1, 13)))
result, err = caa.compute_residual_momentum()
check("Missing stock file returns None", result is None)
check("Error mentions stock_returns", "stock_returns" in str(err))

# Test 1.3: Successful computation with 12 months
cleanup()
ff5_rows = "\n".join(
    f"2025{m:02d},{1.0+m*0.1},{0.5-m*0.05},{-0.3+m*0.02},{0.2},{0.1},{0.35}"
    for m in range(1, 13)
)
write_csv("ff5_factors.csv", f"Date,Mkt-RF,SMB,HML,RMW,CMA,RF\n{ff5_rows}")

stock_rows = "\n".join(
    f"2025{m:02d}," + ",".join(str(round(2.0 + i*0.5 + m*0.1, 2)) for i in range(12))
    for m in range(1, 13)
)
write_csv("stock_returns.csv",
    "Date," + ",".join(caa.SINGLE_STOCK_UNIVERSE) + f"\n{stock_rows}")

result, err = caa.compute_residual_momentum()
check("12-month computation succeeds", result is not None and err is None)
check("All 12 tickers present", result is not None and len(result) == 12)
if result:
    ok_count = sum(1 for v in result.values() if v.get("status") == "OK")
    check("All tickers have OK status", ok_count == 12, f"got {ok_count}")
    # Check scoring
    for ticker, v in result.items():
        if v["status"] == "OK":
            check(f"{ticker} has t_score in [-1,0,+1]", v["t_score"] in [-1, 0, 1])
            check(f"{ticker} has conflict flag", "conflict" in v)
            break  # Just test one for structure

# Test 1.4: 10-month data correctly rejected (needs 12 minimum)
cleanup()
ff5_rows_10 = "\n".join(
    f"2025{m:02d},{1.0},{0.5},{-0.3},{0.2},{0.1},{0.35}"
    for m in range(3, 13)
)
write_csv("ff5_factors.csv", f"Date,Mkt-RF,SMB,HML,RMW,CMA,RF\n{ff5_rows_10}")
stock_rows_10 = "\n".join(
    f"2025{m:02d}," + ",".join(str(2.0 + i*0.5) for i in range(12))
    for m in range(3, 13)
)
write_csv("stock_returns.csv",
    "Date," + ",".join(caa.SINGLE_STOCK_UNIVERSE) + f"\n{stock_rows_10}")
result, err = caa.compute_residual_momentum()
check("10-month computation correctly rejected", result is None and err is not None,
     f"result={result}, err={err}")

# Test 1.5: 8-month data fails (below minimum)
cleanup()
ff5_rows_8 = "\n".join(
    f"2025{m:02d},{1.0},{0.5},{-0.3},{0.2},{0.1},{0.35}"
    for m in range(5, 13)
)
write_csv("ff5_factors.csv", f"Date,Mkt-RF,SMB,HML,RMW,CMA,RF\n{ff5_rows_8}")
result, err = caa.compute_residual_momentum()
check("8-month data returns MISSING", result is None)


# ============================================================
print("\n=== Test Suite 2: Intermediary Capital ===\n")
# ============================================================

# Test 2.1: Missing PD file
cleanup()
result, err = caa.compute_intermediary_capital()
check("Missing PD file returns None", result is None)

# Test 2.2: Normal z-score (no R adjustment)
cleanup()
import random
random.seed(42)
rows = []
d = date(2023, 1, 6)
for i in range(160):
    eq = 50.0 + random.gauss(0, 2.0)
    tot = 400.0 + random.gauss(0, 5.0)
    rows.append(f"{d.strftime('%Y-%m-%d')},{eq:.2f},{tot:.2f}")
    d += timedelta(days=7)
write_csv("pd_statistics.csv", "date,equity,total\n" + "\n".join(rows))

result, err = caa.compute_intermediary_capital()
check("Normal PD data computes OK", result is not None and result.get("status") == "OK")
if result and result.get("status") == "OK":
    check("Z-score is a number", isinstance(result["z_score"], (int, float)))
    check("R adjustment is 0 or -1", result["r_adjustment"] in [0, -1])

# Test 2.3: Stressed z-score triggers R downgrade
cleanup()
rows = []
d = date(2023, 1, 6)
for i in range(160):
    if i < 155:
        eq = 50.0 + random.gauss(0, 1.0)
        tot = 400.0 + random.gauss(0, 3.0)
    else:
        # Last 5 weeks: equity crashes
        eq = 35.0  # way below 3y mean
        tot = 400.0
    rows.append(f"{d.strftime('%Y-%m-%d')},{eq:.2f},{tot:.2f}")
    d += timedelta(days=7)
write_csv("pd_statistics.csv", "date,equity,total\n" + "\n".join(rows))

result, err = caa.compute_intermediary_capital()
check("Stressed PD computes OK", result is not None and result.get("status") == "OK")
if result and result.get("status") == "OK":
    check("Z-score is negative", result["z_score"] < 0, f"z={result['z_score']}")
    check("R adjustment is -1 (downgrade)", result["r_adjustment"] == -1,
         f"adj={result['r_adjustment']}, z={result['z_score']}")

# Test 2.4: Ratio column format
cleanup()
rows = "\n".join(f"2023-01-{6+i*7:02d},{0.120 + i*0.0005:.4f}" for i in range(20))
write_csv("pd_statistics.csv", "date,ratio\n" + rows)
result, err = caa.compute_intermediary_capital()
check("Ratio-column format works", result is not None and result.get("status") == "OK",
     f"err={err}")


# ============================================================
print("\n=== Test Suite 3: Basis-Momentum ===\n")
# ============================================================

# Test 3.1: Missing curves file
cleanup()
result, err = caa.compute_basis_momentum()
check("Missing curves file returns None", result is None)

# Test 3.2: Backwardation steepening (no divergence cap)
cleanup()
rows = []
d = date(2026, 1, 2)
for i in range(80):
    cd = d + timedelta(days=i)
    # Brent: deepening backwardation (F1 rising faster than F2)
    f1 = 92.0 + i * 0.15
    f2 = 83.0 + i * 0.05
    rows.append(f"{cd.strftime('%Y-%m-%d')},Brent,{f1:.2f},{f2:.2f}")
write_csv("futures_curves.csv", "date,commodity,f1,f2\n" + "\n".join(rows))

result, err = caa.compute_basis_momentum()
check("Steepening backwardation computes OK", result is not None)
if result and "Brent" in result and result["Brent"].get("status") == "OK":
    check("Brent static backwardation = True", result["Brent"]["static_backwardation"] == True)
    check("Brent steepening = True", result["Brent"]["steepening"] == True)
    check("Brent divergence cap = False", result["Brent"]["divergence_cap"] == False)
    check("Brent 4w change is positive", result["Brent"]["change_4w"] > 0)

# Test 3.3: Backwardation flattening → divergence cap fires
cleanup()
rows = []
d = date(2026, 1, 2)
for i in range(80):
    cd = d + timedelta(days=i)
    # Brent: backwardation but flattening (F2 catching up to F1)
    f1 = 100.0 - i * 0.02
    f2 = 85.0 + i * 0.08  # F2 rising faster → spread narrowing
    rows.append(f"{cd.strftime('%Y-%m-%d')},Brent,{f1:.2f},{f2:.2f}")
write_csv("futures_curves.csv", "date,commodity,f1,f2\n" + "\n".join(rows))

result, err = caa.compute_basis_momentum()
if result and "Brent" in result and result["Brent"].get("status") == "OK":
    # Spread starts at 15.0, narrows as F2 rises faster
    check("Flattening: divergence_cap = True", result["Brent"]["divergence_cap"] == True,
         f"4w={result['Brent']['change_4w']}, 12w={result['Brent']['change_12w']}")
    check("Flattening: s_cap_at_zero = True", result["Brent"]["s_cap_at_zero"] == True)

# Test 3.4: Contango (no backwardation) → no divergence cap
cleanup()
rows = []
d = date(2026, 1, 2)
for i in range(80):
    cd = d + timedelta(days=i)
    # Gold: contango (F2 > F1)
    f1 = 4750.0 + i * 0.5
    f2 = 4780.0 + i * 0.5
    rows.append(f"{cd.strftime('%Y-%m-%d')},Gold,{f1:.2f},{f2:.2f}")
write_csv("futures_curves.csv", "date,commodity,f1,f2\n" + "\n".join(rows))

result, err = caa.compute_basis_momentum()
if result and "Gold" in result and result["Gold"].get("status") == "OK":
    check("Contango: static_backwardation = False", result["Gold"]["static_backwardation"] == False)
    check("Contango: divergence_cap = False", result["Gold"]["divergence_cap"] == False)

# Test 3.5: Missing commodity in data
cleanup()
rows = []
d = date(2026, 1, 2)
for i in range(80):
    cd = d + timedelta(days=i)
    rows.append(f"{cd.strftime('%Y-%m-%d')},Brent,{98+i*0.1:.2f},{88+i*0.05:.2f}")
write_csv("futures_curves.csv", "date,commodity,f1,f2\n" + "\n".join(rows))

result, err = caa.compute_basis_momentum()
check("Partial commodity data: Brent OK", result is not None and result.get("Brent", {}).get("status") == "OK")
check("Missing WTI flagged", result is not None and result.get("WTI", {}).get("status") == "MISSING")


# ============================================================
print("\n=== Test Suite 4: Staging File Output ===\n")
# ============================================================

cleanup()
output_path = os.path.join(TEST_DIR, "test-staging.md")

# Write with all MISSING
caa.write_staging_file(output_path, None, "test error 1", None, "test error 2", None, "test error 3")
with open(output_path) as f:
    content = f.read()

check("Staging file created", os.path.exists(output_path))
check("Contains MISSING status for residual", "MISSING" in content and "test error 1" in content)
check("Contains MISSING status for intermediary", "test error 2" in content)
check("Contains MISSING status for basis", "test error 3" in content)
check("Contains consumer line", "daily-market-brief" in content)
check("Contains fail-loud rule", "fail-loud" in content.lower())


# ============================================================
print("\n=== Test Suite 5: Edge Cases ===\n")
# ============================================================

# Test 5.1: Empty CSV files
cleanup()
write_csv("ff5_factors.csv", "")
write_csv("stock_returns.csv", "")
result, err = caa.compute_residual_momentum()
check("Empty FF5 CSV handled gracefully", result is None)

cleanup()
write_csv("pd_statistics.csv", "date,equity,total\n")
result, err = caa.compute_intermediary_capital()
check("Empty PD CSV handled gracefully", result is None)

cleanup()
write_csv("futures_curves.csv", "date,commodity,f1,f2\n")
result, err = caa.compute_basis_momentum()
check("Empty futures CSV handled gracefully", result is not None)  # Returns dict with all MISSING


# ============================================================
# Summary
# ============================================================
print(f"\n{'='*50}")
print(f"RESULTS: {PASSED} passed, {FAILED} failed out of {PASSED+FAILED} tests")
print(f"{'='*50}")

# Cleanup
shutil.rmtree(TEST_DIR, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(1 if FAILED > 0 else 0)
