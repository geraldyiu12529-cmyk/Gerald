#!/usr/bin/env python3
"""
Fetch Fama-French 5-factor monthly returns from Kenneth French's data library.
Falls back to ETF-proxy factors if the direct download fails.

Output: /tmp/audit-data/ff5_factors.csv
        /tmp/audit-data/stock_returns.csv (from Yahoo Finance via web search)

This script is designed to be called by the audit-data-compute-750pm scheduled
task BEFORE compute_audit_additions.py runs.

ETF Proxy Mapping (fallback):
  Mkt-RF  → SPY total return - 3m T-bill rate
  SMB     → IWM - SPY  (small vs large)
  HML     → IWD - IWF  (value vs growth, Russell 1000 variants)
  RMW     → QUAL - SPY (quality factor minus market)
  CMA     → VLUE - SPY (value/conservative minus market, approximate)

The proxy approach sacrifices precision but ensures the pipeline never goes
fully inert due to French library publication lag. The compute script's OLS
will produce slightly noisier residuals, but non-zero residuals are better
than the current all-zeros output.
"""

import os
import sys
import csv
import io
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(os.environ.get("AUDIT_DATA_DIR", "/tmp/audit-data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Kenneth French library direct download URL for FF5 monthly
FF5_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"

SINGLE_STOCK_UNIVERSE = [
    "NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
    "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"
]


def try_download_french_library():
    """
    Attempt to download FF5 factors directly from Kenneth French's website.
    The file is a ZIP containing a CSV with monthly and annual returns.
    Returns True if successful, False otherwise.
    """
    try:
        import urllib.request
        print("Attempting direct download from Kenneth French library...")

        req = urllib.request.Request(FF5_URL, headers={
            'User-Agent': 'Mozilla/5.0 (research tool)'
        })

        with urllib.request.urlopen(req, timeout=30) as response:
            zip_data = response.read()

        # Extract CSV from ZIP
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            csv_filename = z.namelist()[0]  # Usually one file
            csv_data = z.read(csv_filename).decode('utf-8')

        # Parse the Kenneth French format:
        # First section is monthly data, separated by blank line from annual
        lines = csv_data.split('\n')
        monthly_data = []
        in_monthly = False
        header_written = False

        for line in lines:
            line = line.strip()
            if not line:
                if in_monthly and monthly_data:
                    break  # End of monthly section
                continue

            # Look for the start of monthly data (6-digit date like 196307)
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 7:
                try:
                    date_str = parts[0]
                    if len(date_str) == 6 and date_str.isdigit():
                        in_monthly = True
                        if not header_written:
                            monthly_data.append("Date,Mkt-RF,SMB,HML,RMW,CMA,RF")
                            header_written = True
                        # Keep only data from 2024 onwards (for 12m window)
                        year = int(date_str[:4])
                        if year >= 2024:
                            monthly_data.append(line)
                except (ValueError, IndexError):
                    continue

        if len(monthly_data) > 6:  # At least 6 months of data
            output_path = DATA_DIR / "ff5_factors.csv"
            with open(output_path, 'w') as f:
                f.write('\n'.join(monthly_data))
            print(f"FF5 factors written: {output_path} ({len(monthly_data)-1} months)")
            return True
        else:
            print(f"Insufficient monthly data extracted: {len(monthly_data)-1} rows")
            return False

    except Exception as e:
        print(f"Direct download failed: {e}")
        return False


def build_etf_proxy_factors(stock_returns_data):
    """
    Build approximate FF5 factor returns from ETF proxies via Yahoo Finance.
    This is a fallback when the French library is unavailable or stale.

    ETF Proxy Mapping:
      Mkt-RF  → SPY total return - 0 (approximate; RF is small)
      SMB     → IWM - SPY (small vs large)
      HML     → IWD - IWF (value vs growth, Russell 1000 variants)
      RMW     → QUAL - SPY (quality factor minus market)
      CMA     → VLUE - SPY (value/conservative minus market, approximate)

    The proxy factors will be noisier than true FF5 factors, but the key
    property we need — that the OLS residual separates stock-specific
    momentum from factor-driven momentum — is preserved approximately.

    Returns CSV content string on success, or None if insufficient data.
    """
    import urllib.request
    import json

    print("Building ETF-proxy factor approximation via Yahoo Finance...")

    etf_tickers = ["SPY", "IWM", "IWD", "IWF"]  # QUAL and VLUE often have less history
    monthly_returns = {}

    for ticker in etf_tickers:
        try:
            # Fetch 14 months of daily data, convert to monthly
            url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                   f"?range=14mo&interval=1mo")
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            result = data["chart"]["result"][0]
            timestamps = result["timestamp"]
            closes = result["indicators"]["adjclose"][0]["adjclose"]

            # Compute monthly returns
            returns = {}
            for i in range(1, len(closes)):
                if closes[i] is not None and closes[i-1] is not None and closes[i-1] != 0:
                    from datetime import datetime as dt
                    date_str = dt.fromtimestamp(timestamps[i]).strftime("%Y%m")
                    ret = (closes[i] / closes[i-1] - 1) * 100  # in percent
                    returns[date_str] = ret

            monthly_returns[ticker] = returns
            print(f"  {ticker}: {len(returns)} months of returns")

        except Exception as e:
            print(f"  {ticker}: FAILED — {e}")
            continue

    if "SPY" not in monthly_returns or len(monthly_returns["SPY"]) < 10:
        print("  Insufficient SPY data for proxy construction")
        return None

    # Build factor CSV
    # All dates where SPY has data
    all_dates = sorted(monthly_returns["SPY"].keys())
    lines = ["Date,Mkt-RF,SMB,HML,RMW,CMA,RF"]

    for date in all_dates:
        spy = monthly_returns["SPY"].get(date)
        if spy is None:
            continue

        mkt_rf = spy  # Approximate: RF is small (~0.3-0.4% monthly at current rates)
        smb = (monthly_returns.get("IWM", {}).get(date, 0) -
               monthly_returns["SPY"].get(date, 0)) if "IWM" in monthly_returns else 0
        hml = (monthly_returns.get("IWD", {}).get(date, 0) -
               monthly_returns.get("IWF", {}).get(date, 0)) if ("IWD" in monthly_returns and
                                                                   "IWF" in monthly_returns) else 0
        rmw = 0  # QUAL not always available; set to 0 (drops to ~3 factor model)
        cma = 0  # VLUE not always available; set to 0

        rf = 0.04  # ~0.4% monthly at ~5% annualized (approximate)
        lines.append(f"{date},{mkt_rf:.4f},{smb:.4f},{hml:.4f},{rmw:.4f},{cma:.4f},{rf:.4f}")

    if len(lines) < 8:  # Need at least 7 months of data
        print(f"  Only {len(lines)-1} months of proxy data — insufficient")
        return None

    csv_content = "\n".join(lines)
    output_path = DATA_DIR / "ff5_factors.csv"
    with open(output_path, 'w') as f:
        f.write(csv_content)
    print(f"  ETF proxy factors written: {output_path} ({len(lines)-1} months)")
    print(f"  Note: RMW and CMA set to 0 — effectively a 3-factor model (Mkt, SMB, HML)")

    # Also cache to persistent storage
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from cache_manager import write_bulk_cache
        write_bulk_cache("ff5_factors.csv", csv_content, 2,
                        "ETF proxy (Yahoo Finance)", len(lines)-1,
                        all_dates[-1] if all_dates else "")
    except ImportError:
        pass

    return csv_content


def create_stock_returns_template():
    """
    Create a stock_returns.csv template that the scheduled task populates
    via web search. Each row is YYYYMM format with monthly returns in percent.

    Always includes SPY as the first ticker column — the market-model
    fallback in compute_audit_additions.py requires a market regressor,
    and omitting SPY here was the 2026-04-17 defect that blocked all 12
    single-stock T-scores for the day.
    """
    output_path = DATA_DIR / "stock_returns_template.csv"
    tickers = ["SPY"] + list(SINGLE_STOCK_UNIVERSE)
    header = "Date," + ",".join(tickers)

    # Generate date range: last 14 months
    now = datetime.now()
    dates = []
    for i in range(14, 0, -1):
        d = now - timedelta(days=30 * i)
        dates.append(d.strftime("%Y%m"))

    lines = [header]
    for d in dates:
        lines.append(d + "," + ",".join([""] * len(tickers)))

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Stock returns template written: {output_path}")
    return output_path


def fetch_stock_returns_from_yahoo():
    """
    Direct Yahoo Finance monthly-return fetch for the 12 single stocks + SPY.
    Writes /tmp/audit-data/stock_returns.csv with SPY as the market regressor.

    Why this function exists: the scheduled audit-data task previously relied
    on web-search hydration to populate stock_returns.csv, which (a) was
    flaky, and (b) had no mechanism to ensure SPY — required by the
    market-model fallback in compute_audit_additions — was actually included.
    Fetching directly from Yahoo Finance /v8 chart API with interval=1mo
    gives us deterministic, always-complete monthly returns for the full
    universe plus SPY.

    Returns CSV content string on success, or None if insufficient data.
    """
    import urllib.request
    import json

    print("Fetching monthly stock returns (+ SPY) from Yahoo Finance...")

    tickers = ["SPY"] + list(SINGLE_STOCK_UNIVERSE)
    monthly_returns = {}  # {ticker: {YYYYMM: return_pct}}

    for ticker in tickers:
        try:
            url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                   f"?range=14mo&interval=1mo")
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            result = data["chart"]["result"][0]
            timestamps = result["timestamp"]
            closes = result["indicators"]["adjclose"][0]["adjclose"]

            returns = {}
            for i in range(1, len(closes)):
                if closes[i] is not None and closes[i-1] is not None and closes[i-1] != 0:
                    from datetime import datetime as dt
                    date_str = dt.fromtimestamp(timestamps[i]).strftime("%Y%m")
                    ret = (closes[i] / closes[i-1] - 1) * 100  # in percent
                    returns[date_str] = ret

            monthly_returns[ticker] = returns
            print(f"  {ticker:6s}: {len(returns)} months")
        except Exception as e:
            print(f"  {ticker:6s}: FAILED — {e}")
            continue

    if "SPY" not in monthly_returns or len(monthly_returns["SPY"]) < 10:
        print("  Insufficient SPY data — cannot write stock_returns.csv")
        return None

    # Union of all dates where at least SPY has a return, sorted ascending
    all_dates = sorted(monthly_returns["SPY"].keys())

    # Only keep dates where SPY + at least one single stock has data
    header_tickers = [t for t in tickers
                      if t in monthly_returns and len(monthly_returns[t]) > 0]
    lines = ["Date," + ",".join(header_tickers)]
    for d in all_dates:
        row_vals = []
        for t in header_tickers:
            v = monthly_returns.get(t, {}).get(d)
            row_vals.append(f"{v:.6f}" if v is not None else "")
        lines.append(f"{d}," + ",".join(row_vals))

    csv_content = "\n".join(lines)
    output_path = DATA_DIR / "stock_returns.csv"
    with open(output_path, 'w') as f:
        f.write(csv_content)
    print(f"  Stock returns written: {output_path} "
          f"({len(lines)-1} months, {len(header_tickers)} tickers incl. SPY)")

    # Cache to persistent storage so compute_audit_additions picks it up
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from cache_manager import write_bulk_cache
        write_bulk_cache("stock_returns.csv", csv_content, 1,
                        "Yahoo Finance monthly", len(lines)-1,
                        all_dates[-1] if all_dates else "")
    except ImportError:
        pass

    return csv_content


def main():
    print("=== FF5 Factor Data Fetch ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Output dir: {DATA_DIR}")
    print()

    # Step 1: Try direct download from Kenneth French
    success = try_download_french_library()

    if success:
        print("\n✓ FF5 factors fetched from Kenneth French library")
        # Verify and cache the data
        ff5_path = DATA_DIR / "ff5_factors.csv"
        with open(ff5_path) as f:
            content = f.read()
            lines = content.strip().split('\n')
            print(f"  Rows: {len(lines)-1}")
            if len(lines) > 1:
                last_line = lines[-1].strip().split(',')
                print(f"  Latest month: {last_line[0]}")
                # Cache to persistent storage
                try:
                    sys.path.insert(0, str(Path(__file__).parent))
                    from cache_manager import write_bulk_cache
                    write_bulk_cache("ff5_factors.csv", content, 1,
                                    "Kenneth French library", len(lines)-1,
                                    last_line[0])
                    print("  Cached to persistent storage")
                except ImportError:
                    pass
    else:
        print("\n✗ French library download failed")

        # Tier 3: try persistent cache before ETF proxy
        cached_ok = False
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from cache_manager import read_bulk_cache, copy_bulk_to_working
            cached = read_bulk_cache("ff5_factors.csv")
            if cached:
                copy_bulk_to_working("ff5_factors.csv", str(DATA_DIR))
                print(f"  ✓ Using cached FF5 factors ({cached['staleness']}, "
                      f"{cached['age_days']:.0f}d old, {cached['rows']} rows)")
                cached_ok = True
        except ImportError:
            pass

        if not cached_ok:
            print("  No cached FF5 data available")
            print("  Falling back to ETF proxy factors...")
            proxy = build_etf_proxy_factors(None)
            if proxy:
                print("  ✓ ETF proxy factors built")
            else:
                print("  ✗ ETF proxy also unavailable")
                print("  → Residual momentum will remain MISSING")
                print("  → Single-stock T-scores will be blocked")
                print()
                print("  MANUAL FIX: Download FF5 CSV from:")
                print(f"  {FF5_URL}")
                print(f"  Extract and place at: {DATA_DIR / 'ff5_factors.csv'}")

    # Step 2: Fetch stock returns from Yahoo (12 single stocks + SPY).
    # SPY is required by the market-model fallback in compute_audit_additions;
    # omitting it previously caused the 2026-04-17 all-stocks-INC defect.
    # Always run this so the cache stays fresh, not just when the file is missing.
    print("\n--- Stock returns ---")
    stock_path = DATA_DIR / "stock_returns.csv"
    stock_content = fetch_stock_returns_from_yahoo()
    if stock_content is None:
        # Last-resort: don't overwrite a pre-existing file with a template
        if not stock_path.exists():
            print("  Yahoo fetch failed and no existing file — writing template")
            create_stock_returns_template()
        else:
            print("  Yahoo fetch failed — leaving existing stock_returns.csv in place")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
