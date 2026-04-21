#!/usr/bin/env python3
"""
Compute the three audit-addition variables and write results
to a staging file that the daily brief and trade-rec can consume.

Variables:
  1. Residual momentum (12m FF5-residualized) — single-stock T-input
  2. Intermediary capital ratio (NY Fed PD equity/total, z-score) — cross-asset R-overlay
  3. Basis-momentum (4w / 12w change in F1-F2 slope) — commodity S-input

Usage:
  python compute_audit_additions.py --output /path/to/staging-file.md

Data retrieval (2026-04-16 fallback framework):
  Source CSVs are fetched via the 4-tier retrieval chain:
    Tier 1: Direct HTTP (Kenneth French, Yahoo Finance, NY Fed, Barchart)
    Tier 2: Web search (scheduled task prompt)
    Tier 3: Persistent cache (./.data-cache/) — last known good
    Tier 4: MISSING (fail-loud)
  The data_retrieval_engine module handles the 4-tier fallback chain automatically.
  Even if ALL live sources fail, cached data produces valid (stale-flagged) output.

Derived variable fallbacks:
  Residual momentum:   FF5 (5-factor) → Market-model (1-factor SPY) → Cache
  Intermediary capital: NY Fed PD data → HY OAS directional proxy → Cache
  Basis-momentum:      Barchart curves → Web-search directional → Cache
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts dir to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

from data_retrieval_engine import fetch_bulk

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

SINGLE_STOCK_UNIVERSE = [
    "NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
    "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"
]

COMMODITY_UNIVERSE = ["Brent", "WTI", "Gold", "Silver", "Copper"]

DATA_DIR = Path(os.environ.get("AUDIT_DATA_DIR", "/tmp/audit-data"))
TODAY = datetime.now().strftime("%Y-%m-%d")


def _fetch_spy_monthly_returns():
    """
    Direct Yahoo Finance fetch for 14mo of SPY monthly returns (percent,
    matching the stock_returns.csv convention where values are divided by 100
    when read). Returns {YYYYMM: decimal_return} or None on failure.

    Used as a defensive fallback by the market-model residual path when
    stock_returns.csv is missing the SPY column.
    """
    import json
    import urllib.request
    try:
        url = ("https://query1.finance.yahoo.com/v8/finance/chart/SPY"
               "?range=14mo&interval=1mo")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["adjclose"][0]["adjclose"]

        returns = {}
        for i in range(1, len(closes)):
            if closes[i] is not None and closes[i-1] is not None and closes[i-1] != 0:
                d = datetime.fromtimestamp(timestamps[i]).strftime("%Y%m")
                # Stored as decimal (not percent) to match how the
                # market-model consumer divides parts[col] by 100.
                returns[d] = (closes[i] / closes[i-1] - 1)
        return returns if len(returns) >= 10 else None
    except Exception:
        return None


def compute_residual_momentum():
    """
    12-month residual momentum: regress each stock's excess returns on FF5
    factors over trailing 12 months, take cumulative residual.
    Returns dict of {ticker: {"residual_return": float, "t_score": int, "raw_tsmom_agrees": bool}}
    or None if data unavailable.
    """
    if not HAS_NUMPY:
        return None, "numpy not available for OLS computation"

    # Fetch FF5 factors via 4-tier retrieval chain
    ff5_result = fetch_bulk("ff5_factors.csv", dest_dir=str(DATA_DIR))
    stock_result = fetch_bulk("stock_returns.csv", dest_dir=str(DATA_DIR))

    if not ff5_result.ok:
        return None, f"FF5 factor file unavailable: {ff5_result.error or ff5_result.staleness}"
    if not stock_result.ok:
        return None, f"Stock returns file unavailable: {stock_result.error or stock_result.staleness}"

    try:
        # Parse FF5 factors from fetched content.
        # Canonical Kenneth French format: Date, Mkt-RF, SMB, HML, RMW, CMA, RF (7 cols).
        # Tolerate a 6-col file that omits RF (ETF-proxy or truncated export) by
        # synthesizing RF = 0 — at current rates RF is ~0.3-0.4%/month so the
        # residual-momentum accuracy cost is small, and this avoids failing the
        # whole primary path and silently falling through to the market-model
        # fallback whenever RF happens to be absent from the CSV.
        ff5_data = {}
        ff5_lines = ff5_result.content.split('\n')
        header_found = False
        header_fields = None
        for line in ff5_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            # Header detection: first non-blank line whose first field
            # contains 'date'/'month'/'yyyymm' (case-insensitive)
            if not header_found and len(parts) >= 6:
                first = parts[0].strip().lower()
                if any(h in first for h in ['date', 'month', 'yyyymm']):
                    header_fields = [p.strip().lower() for p in parts]
                    header_found = True
                    continue
            # Data row: require at least 6 columns (date + 5 factors).
            # If a 7th column is present, treat it as RF; otherwise RF=0.
            if len(parts) >= 6:
                try:
                    date_str = parts[0].strip()
                    mkt_rf = float(parts[1].strip()) / 100.0
                    smb   = float(parts[2].strip()) / 100.0
                    hml   = float(parts[3].strip()) / 100.0
                    rmw   = float(parts[4].strip()) / 100.0
                    cma   = float(parts[5].strip()) / 100.0
                    rf    = float(parts[6].strip()) / 100.0 if len(parts) >= 7 else 0.0
                    ff5_data[date_str] = [mkt_rf, smb, hml, rmw, cma, rf]
                except (ValueError, IndexError):
                    continue

        if len(ff5_data) < 10:
            return None, (f"Insufficient FF5 factor data: {len(ff5_data)} months "
                          f"(need at least 10; header={header_fields})")

        # Parse stock returns from fetched content
        stock_data = {}
        stock_lines = stock_result.content.split('\n')
        if not stock_lines:
            return None, "Empty stock returns file"
        header = [h.strip() for h in stock_lines[0].split(',')]
        date_col = 0
        ticker_cols = {}
        for i, h in enumerate(header):
            if h.upper() in [t.upper() for t in SINGLE_STOCK_UNIVERSE]:
                ticker_cols[h.upper()] = i

        for line in stock_lines[1:]:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            date_str = parts[0].strip()
            for ticker, col in ticker_cols.items():
                if col < len(parts):
                    try:
                        ret = float(parts[col].strip()) / 100.0
                        if ticker not in stock_data:
                            stock_data[ticker] = {}
                        stock_data[ticker][date_str] = ret
                    except ValueError:
                        continue

        # Use ALL available aligned months for regression (more dof = better residuals)
        # Then take last 12 months of residuals for the cumulative score.
        # Prior bug: using only 12 months gave 6 dof → near-zero residuals.
        all_ff5_dates = sorted(ff5_data.keys())
        all_stock_dates = set()
        for t in stock_data.values():
            all_stock_dates.update(t.keys())
        all_dates = [d for d in all_ff5_dates if d in all_stock_dates]
        if len(all_dates) < 12:
            return None, f"Only {len(all_dates)} months of aligned data (need at least 12)"
        n_months = len(all_dates)

        # Build factor matrix (n_months x 5)
        X = np.array([[ff5_data[d][i] for i in range(5)] for d in all_dates])
        rf = np.array([ff5_data[d][5] for d in all_dates])

        results = {}
        for ticker in SINGLE_STOCK_UNIVERSE:
            if ticker not in stock_data:
                results[ticker] = {"status": "MISSING", "reason": f"No return data for {ticker}"}
                continue

            # Get aligned stock returns
            y_raw = []
            valid = True
            for d in all_dates:
                if d in stock_data[ticker]:
                    y_raw.append(stock_data[ticker][d])
                else:
                    valid = False
                    break

            if not valid or len(y_raw) != n_months:
                results[ticker] = {"status": "MISSING", "reason": f"Incomplete 12m returns for {ticker}"}
                continue

            y = np.array(y_raw) - rf  # excess returns

            # OLS: y = X @ beta + residual
            X_with_const = np.column_stack([np.ones(n_months), X])
            try:
                beta, _, _, _ = np.linalg.lstsq(X_with_const, y, rcond=None)
                residuals = y - X_with_const @ beta
                # Use last 12 months of residuals for cumulative score
                cum_residual = float(np.sum(residuals[-12:]))
                raw_tsmom = float(np.sum(y_raw))

                # Score: positive residual = +1, negative = -1, near zero = 0
                if cum_residual > 0.02:  # >2% residual over 12m
                    t_score = 1
                elif cum_residual < -0.02:
                    t_score = -1
                else:
                    t_score = 0

                raw_agrees = (raw_tsmom > 0 and t_score >= 0) or (raw_tsmom < 0 and t_score <= 0) or t_score == 0

                results[ticker] = {
                    "status": "OK",
                    "residual_return_12m": round(cum_residual * 100, 2),
                    "t_score": t_score,
                    "raw_tsmom_12m": round(raw_tsmom * 100, 2),
                    "raw_agrees": raw_agrees,
                    "conflict": not raw_agrees
                }
            except Exception as e:
                results[ticker] = {"status": "MISSING", "reason": f"OLS failed: {e}"}

        return results, None

    except Exception as e:
        return None, f"Residual momentum computation error: {e}"


def compute_intermediary_capital():
    """
    NY Fed primary-dealer equity/total capital ratio, z-score vs 3-year rolling mean.
    Returns {"z_score": float, "r_adjustment": int, "raw_ratio": float} or None.
    """
    if not HAS_NUMPY:
        return None, "numpy not available for z-score computation"

    # Fetch PD statistics via 4-tier retrieval chain
    pd_result = fetch_bulk("pd_statistics.csv", dest_dir=str(DATA_DIR))

    if not pd_result.ok:
        return None, f"NY Fed PD statistics file unavailable: {pd_result.error or pd_result.staleness}"

    try:
        # Parse: expect columns Date, Equity, TotalCapital (or ratio directly)
        ratios = []
        dates = []
        pd_lines = pd_result.content.split('\n')
        if not pd_lines:
            return None, "Empty PD statistics file"

        header = [h.strip().lower() for h in pd_lines[0].split(',')]

        # Try to find relevant columns
        date_col = None
        ratio_col = None
        equity_col = None
        total_col = None

        for i, h in enumerate(header):
            if 'date' in h:
                date_col = i
            if 'ratio' in h or 'equity_total' in h:
                ratio_col = i
            if 'equity' in h and 'total' not in h:
                equity_col = i
            if 'total' in h:
                total_col = i

        for line in pd_lines[1:]:
            parts = line.strip().split(',')
            try:
                if ratio_col is not None and ratio_col < len(parts):
                    r = float(parts[ratio_col].strip())
                    ratios.append(r)
                    if date_col is not None and date_col < len(parts):
                        dates.append(parts[date_col].strip())
                elif equity_col is not None and total_col is not None:
                    eq = float(parts[equity_col].strip())
                    tot = float(parts[total_col].strip())
                    if tot > 0:
                        ratios.append(eq / tot)
                        if date_col is not None and date_col < len(parts):
                            dates.append(parts[date_col].strip())
            except (ValueError, IndexError):
                continue

        if len(ratios) < 13:  # Need at least ~3 years of weekly data (156 weeks) but be flexible
            # If we have at least some data, use what we have
            if len(ratios) < 4:
                return None, f"Insufficient PD data: {len(ratios)} observations (need at least 4 for z-score)"

        ratios_arr = np.array(ratios)
        current = ratios_arr[-1]

        # 3-year rolling mean and std (use all available if < 3 years)
        lookback = min(len(ratios_arr), 156)  # ~3 years of weekly data
        window = ratios_arr[-lookback:]
        mean = float(np.mean(window))
        std = float(np.std(window))

        if std < 1e-10:
            return None, "Zero variance in PD ratio — cannot compute z-score"

        z = float((current - mean) / std)

        # R adjustment: z < -1 => downgrade R by one notch
        r_adjustment = -1 if z < -1.0 else 0

        return {
            "status": "OK",
            "current_ratio": round(current, 4),
            "z_score": round(z, 2),
            "mean_3y": round(mean, 4),
            "std_3y": round(std, 4),
            "r_adjustment": r_adjustment,
            "latest_date": dates[-1] if dates else "unknown",
            "observations": len(ratios)
        }, None

    except Exception as e:
        return None, f"Intermediary capital computation error: {e}"


def compute_basis_momentum():
    """
    4-week and 12-week change in F1-F2 slope for each commodity.
    Returns dict of {commodity: {"slope_4w_change": float, "slope_12w_change": float,
    "divergence_cap": bool, "s_cap_at_zero": bool}}
    """
    # Fetch futures curves via 4-tier retrieval chain
    curves_result = fetch_bulk("futures_curves.csv", dest_dir=str(DATA_DIR))

    if not curves_result.ok:
        return None, f"Futures curves file unavailable: {curves_result.error or curves_result.staleness}"

    try:
        # Parse: expect columns Date, Commodity, F1, F2 (or F1_F2_spread)
        data = {}  # {commodity: [(date, spread), ...]}
        curves_lines = curves_result.content.split('\n')
        if not curves_lines:
            return None, "Empty futures curves file"

        header = [h.strip().lower() for h in curves_lines[0].split(',')]
        date_col = None
        commodity_col = None
        f1_col = None
        f2_col = None
        spread_col = None

        for i, h in enumerate(header):
            if 'date' in h:
                date_col = i
            if 'commodity' in h or 'asset' in h or 'name' in h:
                commodity_col = i
            if h in ['f1', 'front', 'cl1', 'front_month']:
                f1_col = i
            if h in ['f2', 'deferred', 'cl2', 'second_month']:
                f2_col = i
            if 'spread' in h or 'slope' in h:
                spread_col = i

        for line in curves_lines[1:]:
            parts = line.strip().split(',')
            try:
                date_str = parts[date_col].strip() if date_col is not None else ""
                commodity = parts[commodity_col].strip() if commodity_col is not None else ""

                if spread_col is not None:
                    spread = float(parts[spread_col].strip())
                elif f1_col is not None and f2_col is not None:
                    f1 = float(parts[f1_col].strip())
                    f2 = float(parts[f2_col].strip())
                    spread = f1 - f2  # Positive = backwardation
                else:
                    continue

                if commodity not in data:
                    data[commodity] = []
                data[commodity].append((date_str, spread))
            except (ValueError, IndexError):
                continue

        results = {}
        for commodity in COMMODITY_UNIVERSE:
            # Find matching key (case-insensitive)
            matched_key = None
            for k in data:
                if k.lower() == commodity.lower():
                    matched_key = k
                    break

            if matched_key is None or len(data[matched_key]) < 5:
                results[commodity] = {
                    "status": "MISSING",
                    "reason": f"Insufficient curve data for {commodity} ({len(data.get(matched_key, []))} days)"
                }
                continue

            series = data[matched_key]
            series.sort(key=lambda x: x[0])  # Sort by date

            current_spread = series[-1][1]

            # 4-week change (~20 trading days)
            idx_4w = max(0, len(series) - 20)
            spread_4w_ago = series[idx_4w][1]
            change_4w = current_spread - spread_4w_ago

            # 12-week change (~60 trading days)
            idx_12w = max(0, len(series) - 60)
            spread_12w_ago = series[idx_12w][1]
            change_12w = current_spread - spread_12w_ago

            # Static slope direction
            static_backwardation = current_spread > 0  # F1 > F2 = backwardation

            # Basis-momentum: is the curve steepening or flattening?
            steepening = change_4w > 0 and change_12w > 0  # Backwardation deepening
            flattening = change_4w < 0 or change_12w < 0  # Backwardation easing

            # Divergence-cap rule: if static slope = backwardation (+1) but basis-momentum
            # is flattening, cap S at 0
            divergence = static_backwardation and flattening
            s_cap = 0 if divergence else None  # None means no cap applied

            results[commodity] = {
                "status": "OK",
                "current_spread": round(current_spread, 4),
                "spread_4w_ago": round(spread_4w_ago, 4),
                "spread_12w_ago": round(spread_12w_ago, 4),
                "change_4w": round(change_4w, 4),
                "change_12w": round(change_12w, 4),
                "static_backwardation": static_backwardation,
                "steepening": steepening,
                "flattening": flattening,
                "divergence_cap": divergence,
                "s_cap_at_zero": divergence,
                "date_range": f"{series[0][0]} to {series[-1][0]}",
                "observations": len(series)
            }

        return results, None

    except Exception as e:
        return None, f"Basis-momentum computation error: {e}"


def _append_missing_tracker(residmom_primary_ok, residmom_fallback_ok,
                             residmom_ok_count, intermediary_ok,
                             basis_ok, basis_ok_count,
                             residmom_err, intermediary_err, basis_err,
                             tracker_path=None):
    if tracker_path is None:
        from pipeline_status import TRADE_DIR
        tracker_path = str(TRADE_DIR / "audit-data-missing-tracker.md")
    """
    Append a one-row uptime record to the tracker. Feeds the 2026-10-14
    audit-addition demote decision with a normalized denominator (days LIVE,
    not calendar days — see tracker header for normalization rule).

    States:
      residmom — LIVE (primary FF5 OK) / FALLBACK (market-model OK, partial
                  credit) / MISSING (both paths failed)
      intercap — LIVE / MISSING
      basismom — LIVE / MISSING

    Idempotent for a given TODAY: if a row for TODAY already exists, replace it
    rather than double-logging when the compute reruns mid-day.
    """
    from pathlib import Path as _Path

    path = _Path(tracker_path)
    if not path.exists():
        # Tracker file missing — create with header so the row has context.
        path.write_text(
            "# Audit-Addition Uptime Tracker\n\n"
            "Auto-generated. See ./audit-data-missing-tracker.md\n"
            "for the normalization rule used by the 2026-10-14 review.\n\n"
            "## Log\n\n"
            "| Date | ResidMom | ResidMom_OK_stocks | InterCap | BasisMom "
            "| BasisMom_OK_cmdty | Notes |\n"
            "|------|----------|---------------------|----------|----------"
            "|-------------------|-------|\n"
        )

    if residmom_primary_ok:
        rm_state = "LIVE"
    elif residmom_fallback_ok:
        rm_state = "FALLBACK"
    else:
        rm_state = "MISSING"

    ic_state = "LIVE" if intermediary_ok else "MISSING"
    bm_state = "LIVE" if basis_ok else "MISSING"

    notes = []
    if rm_state == "FALLBACK":
        notes.append("residmom-mktmodel-fallback")
    if rm_state == "MISSING" and residmom_err:
        notes.append(f"residmom-missing:{str(residmom_err)[:40]}")
    if ic_state == "MISSING" and intermediary_err:
        notes.append(f"intercap-missing:{str(intermediary_err)[:40]}")
    if bm_state == "MISSING" and basis_err:
        notes.append(f"basismom-missing:{str(basis_err)[:40]}")
    notes_str = "; ".join(notes) if notes else ""

    new_row = (
        f"| {TODAY} | {rm_state} | {residmom_ok_count}/12 | {ic_state} "
        f"| {bm_state} | {basis_ok_count}/5 | {notes_str} |"
    )

    content = path.read_text()
    lines = content.split("\n")
    # Replace same-date row if present (idempotent re-run safety)
    replaced = False
    for i, ln in enumerate(lines):
        if ln.startswith(f"| {TODAY} |"):
            lines[i] = new_row
            replaced = True
            break
    if not replaced:
        # Find the end of the file (after the last non-empty line)
        # and append the new row there. The table extends via append.
        # Strip trailing blank lines, append, keep one trailing newline.
        while lines and lines[-1].strip() == "":
            lines.pop()
        lines.append(new_row)
        lines.append("")

    path.write_text("\n".join(lines))
    print(f"  [tracker] {TODAY}: ResidMom={rm_state} "
          f"({residmom_ok_count}/12) InterCap={ic_state} "
          f"BasisMom={bm_state} ({basis_ok_count}/5)")


def write_staging_file(output_path, residual, residual_err, intermediary, intermediary_err,
                        basis, basis_err, residual_chain_attempts=None):
    """Write computed results to a markdown staging file for the brief/rec to consume.

    residual_chain_attempts: optional list of {path, status, error} dicts recording
    every path the residual-momentum computation tried. Rendered under the MISSING
    block so root cause is visible, not just the last path's error.
    """
    lines = []
    lines.append(f"# Audit-Addition Variable Staging — {TODAY}")
    lines.append(f"")
    lines.append(f"**Computed:** {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC+8")
    lines.append(f"**Consumer:** daily-market-brief, daily-trade-rec")
    lines.append(f"**Rule:** If a variable reads MISSING here, the brief/rec must fail-loud on that score leg.")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Section 1: Residual Momentum
    lines.append(f"## 1. Residual Momentum (12m FF5-residualized) — Equity T-input")
    lines.append(f"")
    if residual is None:
        lines.append(f"**Status: MISSING**")
        lines.append(f"**Reason:** {residual_err}")
        lines.append(f"**Impact:** All 12 single-stock T-scores blocked.")
        if residual_chain_attempts:
            lines.append(f"")
            lines.append(f"**Chain attempts (root-cause trace):**")
            for att in residual_chain_attempts:
                status_tag = "OK" if att.get("status") == "OK" else "FAILED"
                err = att.get("error") or ""
                lines.append(f"- `{att.get('path')}`: {status_tag}"
                             + (f" — {err}" if err else ""))
    else:
        ok_count = sum(1 for v in residual.values() if v.get("status") == "OK")
        missing_count = sum(1 for v in residual.values() if v.get("status") == "MISSING")
        lines.append(f"**Status:** {ok_count} computed, {missing_count} missing")
        lines.append(f"")
        lines.append(f"| Ticker | Residual 12m (%) | T-Score | Raw TSMOM 12m (%) | Conflict? |")
        lines.append(f"|--------|------------------|---------|-------------------|-----------|")
        for ticker in SINGLE_STOCK_UNIVERSE:
            if ticker in residual:
                v = residual[ticker]
                if v["status"] == "OK":
                    conflict = "YES" if v.get("conflict") else "no"
                    lines.append(f"| {ticker} | {v['residual_return_12m']:+.2f} | {v['t_score']:+d} | {v['raw_tsmom_12m']:+.2f} | {conflict} |")
                else:
                    lines.append(f"| {ticker} | MISSING | — | — | {v.get('reason', 'unknown')} |")
    lines.append(f"")

    # Section 2: Intermediary Capital
    lines.append(f"## 2. Intermediary Capital Ratio — Cross-Asset R-overlay")
    lines.append(f"")
    if intermediary is None:
        lines.append(f"**Status: MISSING**")
        lines.append(f"**Reason:** {intermediary_err}")
        lines.append(f"**Impact:** Cross-asset R-overlay leading gate cannot be applied.")
    else:
        z = intermediary["z_score"]
        adj = intermediary["r_adjustment"]
        lines.append(f"**Status: OK**")
        lines.append(f"- Current ratio: {intermediary['current_ratio']:.4f}")
        lines.append(f"- Z-score vs 3y mean: **{z:+.2f}**")
        lines.append(f"- 3y mean: {intermediary['mean_3y']:.4f}, std: {intermediary['std_3y']:.4f}")
        lines.append(f"- R adjustment: **{adj:+d}** {'(z < -1: DOWNGRADE R by one notch on equities/commodities/FX longs)' if adj < 0 else '(z >= -1: no adjustment)'}")
        lines.append(f"- Data: {intermediary['observations']} observations through {intermediary['latest_date']}")
        lines.append(f"- Double-counting gate: if HY OAS also flags stress, take the more negative of intermediary-capital and HY OAS, not the sum.")
    lines.append(f"")

    # Section 3: Basis-Momentum
    lines.append(f"## 3. Basis-Momentum (4w / 12w F1-F2 change) — Commodity S-input")
    lines.append(f"")
    if basis is None:
        lines.append(f"**Status: MISSING**")
        lines.append(f"**Reason:** {basis_err}")
        lines.append(f"**Impact:** Commodity S divergence-cap cannot fire.")
    else:
        ok_count = sum(1 for v in basis.values() if v.get("status") == "OK")
        missing_count = sum(1 for v in basis.values() if v.get("status") == "MISSING")
        lines.append(f"**Status:** {ok_count} computed, {missing_count} missing")
        lines.append(f"")
        lines.append(f"| Commodity | Spread (F1-F2) | 4w Change | 12w Change | Static Backwd? | Steepening? | Divergence Cap? |")
        lines.append(f"|-----------|----------------|-----------|------------|----------------|-------------|-----------------|")
        for commodity in COMMODITY_UNIVERSE:
            if commodity in basis:
                v = basis[commodity]
                if v["status"] == "OK":
                    div_flag = "**YES — cap S at 0**" if v["divergence_cap"] else "no"
                    lines.append(f"| {commodity} | {v['current_spread']:+.4f} | {v['change_4w']:+.4f} | {v['change_12w']:+.4f} | {'yes' if v['static_backwardation'] else 'no'} | {'yes' if v['steepening'] else 'no'} | {div_flag} |")
                else:
                    lines.append(f"| {commodity} | MISSING | — | — | — | — | {v.get('reason', 'unknown')} |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*This file is overwritten each run. The brief and trade-rec should read it at startup and incorporate the values into their S/T/R scoring.*")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    return output_path


def compute_residual_momentum_fallback_market_model():
    """
    Fallback: 1-factor market-model residual using SPY as the market proxy.
    Less precise than FF5 (R^2 ~0.5-0.7 vs 0.8-0.9) but produces non-zero
    residuals that correctly separate stock-specific from market-driven momentum.
    """
    if not HAS_NUMPY:
        return None, "numpy not available (market-model fallback)"

    # Fetch stock returns via 4-tier retrieval chain
    stock_result = fetch_bulk("stock_returns.csv", dest_dir=str(DATA_DIR))
    if not stock_result.ok:
        return None, f"Stock returns file unavailable (market-model fallback): {stock_result.error or stock_result.staleness}"

    try:
        # Parse stock returns from fetched content (same as primary)
        stock_data = {}
        stock_lines = stock_result.content.split('\n')
        if not stock_lines:
            return None, "Empty stock returns file (market-model fallback)"
        header = [h.strip() for h in stock_lines[0].split(',')]
        date_col = 0
        ticker_cols = {}
        spy_col = None
        for i, h in enumerate(header):
            upper = h.upper().strip()
            if upper in [t.upper() for t in SINGLE_STOCK_UNIVERSE]:
                ticker_cols[upper] = i
            if upper == "SPY":
                spy_col = i

        if spy_col is None:
            # Defensive fallback: fetch SPY monthly returns directly from Yahoo
            # so a missing SPY column in the cached CSV doesn't blackhole all
            # 12 single-stock T-scores. Logs a warning into stock_data["SPY"].
            spy_series = _fetch_spy_monthly_returns()
            if spy_series is None:
                return None, ("SPY column not found in stock returns and direct "
                              "Yahoo fallback also failed (needed for market-model)")
            stock_data["SPY"] = spy_series
            print("  Market-model: SPY absent from stock_returns.csv — "
                  "filled from direct Yahoo fetch as fallback.")
            # We still need to process the rest of the file for ticker returns.
            # Re-run the ticker loop below (spy_col stays None; we short-circuit
            # the SPY read path since we already filled stock_data["SPY"]).

        for line in stock_lines[1:]:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            date_str = parts[0].strip()
            # Read SPY only if the column exists; if it was filled by the
            # direct-Yahoo fallback above, skip this to avoid overwriting.
            if spy_col is not None:
                try:
                    spy_ret = float(parts[spy_col].strip()) / 100.0
                    if "SPY" not in stock_data:
                        stock_data["SPY"] = {}
                    stock_data["SPY"][date_str] = spy_ret
                except (ValueError, IndexError):
                    pass
            # Read stocks
            for ticker, col in ticker_cols.items():
                if col < len(parts):
                    try:
                        ret = float(parts[col].strip()) / 100.0
                        if ticker not in stock_data:
                            stock_data[ticker] = {}
                        stock_data[ticker][date_str] = ret
                    except ValueError:
                        continue

        if "SPY" not in stock_data or len(stock_data["SPY"]) < 12:
            return None, f"Insufficient SPY data for market model: {len(stock_data.get('SPY', {}))}"

        spy_dates = sorted(stock_data["SPY"].keys())
        results = {}

        for ticker in SINGLE_STOCK_UNIVERSE:
            if ticker not in stock_data:
                results[ticker] = {"status": "MISSING", "reason": f"No return data for {ticker}"}
                continue

            # Align dates
            aligned = [(d, stock_data[ticker].get(d), stock_data["SPY"][d])
                       for d in spy_dates if d in stock_data[ticker]]
            if len(aligned) < 12:
                results[ticker] = {"status": "MISSING",
                                   "reason": f"Insufficient aligned data for {ticker}: {len(aligned)} months"}
                continue

            y = np.array([a[1] for a in aligned])
            x = np.array([a[2] for a in aligned])

            # OLS: y = alpha + beta * SPY + residual
            X = np.column_stack([np.ones(len(x)), x])
            try:
                beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
                residuals = y - X @ beta
                cum_residual = float(np.sum(residuals[-12:]))
                raw_tsmom = float(np.sum([a[1] for a in aligned[-12:]]))

                if cum_residual > 0.02:
                    t_score = 1
                elif cum_residual < -0.02:
                    t_score = -1
                else:
                    t_score = 0

                raw_agrees = (raw_tsmom > 0 and t_score >= 0) or \
                             (raw_tsmom < 0 and t_score <= 0) or t_score == 0

                results[ticker] = {
                    "status": "OK",
                    "residual_return_12m": round(cum_residual * 100, 2),
                    "t_score": t_score,
                    "raw_tsmom_12m": round(raw_tsmom * 100, 2),
                    "raw_agrees": raw_agrees,
                    "conflict": not raw_agrees,
                    "model": "1-factor market model (fallback)"
                }
            except Exception as e:
                results[ticker] = {"status": "MISSING", "reason": f"Market-model OLS failed: {e}"}

        return results, None

    except Exception as e:
        return None, f"Market-model fallback error: {e}"


def _ensure_cache_csvs():
    """
    Pre-compute step: ensure working CSVs exist from persistent cache.
    Note: fetch_bulk() now handles the 4-tier chain automatically, so this
    is mainly for informational logging.
    """
    csv_status = {}
    for filename in ["ff5_factors.csv", "stock_returns.csv", "pd_statistics.csv", "futures_curves.csv"]:
        result = fetch_bulk(filename, dest_dir=str(DATA_DIR))
        csv_status[filename] = {
            "status": "OK" if result.ok else "MISSING",
            "source": result.source,
            "staleness": result.staleness,
            "age_days": result.age_days,
            "tier": result.tier
        }
        if result.ok:
            if result.staleness == "LIVE":
                print(f"  T{result.tier} ({result.source}): {filename}")
            else:
                print(f"  T{result.tier} ({result.staleness}, {result.age_days:.0f}d old): {filename}")
        else:
            print(f"  MISSING: {filename}")
    return csv_status


def _cache_successful_results(residual, intermediary, basis):
    """
    Write successful computation results to persistent cache for future fallback.
    """
    try:
        from cache_manager import write_cache, write_bulk_cache

        if residual:
            for ticker, data in residual.items():
                if data.get("status") == "OK":
                    write_cache(f"ResidMom_{ticker}", data["residual_return_12m"],
                               1, "compute_audit_additions",
                               "percent", f"t_score={data['t_score']}")

        if intermediary and intermediary.get("status") == "OK":
            write_cache("Intermediary_Cap_Z", intermediary["z_score"],
                       1, "compute_audit_additions", "z-score",
                       f"ratio={intermediary.get('current_ratio')}")
            write_cache("Intermediary_Cap_Ratio", intermediary.get("current_ratio", 0),
                       1, "compute_audit_additions", "ratio")

        if basis:
            for commodity, data in basis.items():
                if data.get("status") == "OK":
                    write_cache(f"BasisMom_{commodity}_4w", data["change_4w"],
                               1, "compute_audit_additions", "spread_change")
                    write_cache(f"BasisMom_{commodity}_12w", data["change_12w"],
                               1, "compute_audit_additions", "spread_change")

        # Also cache the raw CSV files if they exist in working dir
        for fn in ["ff5_factors.csv", "stock_returns.csv", "pd_statistics.csv", "futures_curves.csv"]:
            fpath = DATA_DIR / fn
            if fpath.exists():
                content = fpath.read_text()
                rows = len(content.strip().split('\n')) - 1
                if rows > 0:
                    write_bulk_cache(fn, content, 1, "audit_data_compute", rows)

    except ImportError:
        pass  # cache_manager not available, skip


def main():
    parser = argparse.ArgumentParser(description="Compute audit-addition variables")
    from pipeline_status import TRADE_DIR as _td
    parser.add_argument("--output", default=str(_td / f"audit-data-staging-{TODAY}.md"),
                        help="Output staging file path")
    args = parser.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)

    # === NEW: Ensure working CSVs from persistent cache if web search didn't produce them ===
    print("Checking data sources...")
    csv_status = _ensure_cache_csvs()

    # Compute residual momentum with fallback chain (handled by fetch_bulk's 4-tier chain)
    # chain_attempts records EVERY path's outcome so the staging file can show
    # root cause, not just the last-tried path's error. Added 2026-04-17
    # after a primary-path silent fall-through masked the real SPY defect.
    print("\nComputing residual momentum...")
    chain_attempts = []
    residual, residual_err = compute_residual_momentum()
    residual_source = "FF5 (5-factor)"
    chain_attempts.append({
        "path": "primary_ff5",
        "status": "OK" if residual is not None else "FAILED",
        "error": None if residual is not None else residual_err,
    })

    if residual is None:
        print(f"  Primary (FF5) failed: {residual_err}")
        print("  Trying fallback: 1-factor market model...")
        residual, residual_err = compute_residual_momentum_fallback_market_model()
        residual_source = "Market model (1-factor fallback)"
        chain_attempts.append({
            "path": "fallback_market_model",
            "status": "OK" if residual is not None else "FAILED",
            "error": None if residual is not None else residual_err,
        })
        if residual is None:
            print(f"  Fallback also failed: {residual_err}")
            residual_source = "MISSING"

    # Compute intermediary capital (fallback handled by fetch_bulk's 4-tier chain)
    print("\nComputing intermediary capital...")
    intermediary, intermediary_err = compute_intermediary_capital()
    if intermediary is None:
        print(f"  Failed: {intermediary_err}")

    # Compute basis-momentum (fallback handled by fetch_bulk's 4-tier chain)
    print("\nComputing basis-momentum...")
    basis, basis_err = compute_basis_momentum()
    if basis is None:
        print(f"  Failed: {basis_err}")

    # === NEW: Cache successful results for future fallback ===
    _cache_successful_results(residual, intermediary, basis)

    # Write staging file (now includes source info)
    output = write_staging_file(args.output, residual, residual_err,
                               intermediary, intermediary_err, basis, basis_err,
                               residual_chain_attempts=chain_attempts)
    print(f"\nStaging file written: {output}")

    # Summary
    r_status = "OK" if residual else "MISSING"
    i_status = "OK" if intermediary else "MISSING"
    b_status = "OK" if basis else "MISSING"
    print(f"\nResults:")
    print(f"  Residual momentum:   {r_status} (source: {residual_source})")
    print(f"  Intermediary capital: {i_status}")
    print(f"  Basis-momentum:      {b_status}")

    # === Append a single-row uptime record to the tracker ===
    # Feeds the 2026-10-14 audit-addition demote decision with a normalized
    # denominator (days LIVE, not calendar days). See the tracker header for
    # the normalization rule. Added 2026-04-17 after the residual-mom silent
    # fall-through made it clear calendar-day counting punishes good variables
    # for bad pipelines.
    try:
        _append_missing_tracker(
            residmom_primary_ok=(chain_attempts[0].get("status") == "OK"),
            residmom_fallback_ok=(len(chain_attempts) > 1 and
                                   chain_attempts[-1].get("status") == "OK"),
            residmom_ok_count=(sum(1 for v in (residual or {}).values()
                                    if v.get("status") == "OK")),
            intermediary_ok=(intermediary is not None),
            basis_ok=(basis is not None),
            basis_ok_count=(sum(1 for v in (basis or {}).values()
                                 if v.get("status") == "OK")),
            residmom_err=residual_err,
            intermediary_err=intermediary_err,
            basis_err=basis_err,
        )
    except Exception as e:
        print(f"  [tracker] append failed (non-fatal): {e}")

    # === NEW: Log retrieval stats ===
    try:
        from cache_manager import append_retrieval_log
        missing_vars = []
        if not residual: missing_vars.append("residual_momentum")
        if not intermediary: missing_vars.append("intermediary_capital")
        if not basis: missing_vars.append("basis_momentum")

        stale_vars = []
        for fn, info in csv_status.items():
            if info.get("source") == "persistent_cache":
                stale_vars.append({"name": fn, "staleness": info.get("staleness", "unknown")})

        append_retrieval_log(
            date=TODAY, task="audit-data-compute",
            variables_attempted=3, tier1_success=0, tier2_success=0,
            tier3_cache=len([s for s in csv_status.values()
                           if s.get("source") == "persistent_cache"]),
            tier4_missing=len(missing_vars),
            missing_vars=missing_vars, stale_vars=stale_vars
        )
    except ImportError:
        pass

    # Exit 0 even on MISSING — fail-loud is handled in the staging file, not here
    return 0


if __name__ == "__main__":
    sys.exit(main())
