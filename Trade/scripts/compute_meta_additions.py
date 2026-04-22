#!/usr/bin/env python3
"""
Compute the meta-integration variables (V029-V035) added 2026-04-18.

Writes results to a *sibling* staging file (not the audit-data-staging file
consumed by brief/rec). The sibling file is the shadow-mode ledger — brief/rec
do not consume it until Phase 3 live_date is set on V029-V035.

Variables:
  V029 BAB           — ETF proxy (USMV/SPLV daily spread) as tactical input;
                        canonical AQR monthly for grading (Phase 2b).
  V030 DealerGamma   — Grade B, subscription-required data (SqueezeMetrics /
                        SpotGamma). MISSING stub until Gerald confirms.
  V031 GP/A          — MISSING stub. Needs Ken French GP portfolio CSV; slow-
                        moving (quarterly). Deferred to Phase 2b.
  V032 CEI           — MISSING stub. Needs CRSP+Compustat self-compute;
                        deferred to Phase 2b (scripts/compute_cei.py).
  V033 C009 Faber SPY  — Monthly close vs 10m-SMA, equity sleeve gate.
  V034 C009 Faber GSCI — Monthly close vs 10m-SMA, commodity sleeve gate.
  V035 C009 Faber BTC  — Monthly close vs 10m-SMA, crypto sleeve gate.

Usage:
  python compute_meta_additions.py [--output /path/to/staging-file.md]

Fail-loud discipline:
  Every Grade A row must print LIVE value OR MISSING with chain-attempt trace.
  Grade B V030 prints MISSING (subscription pending) — not fail-loud yet
  because the row is explicitly flagged subscription-pending in framework/Data Sources.md.
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

TODAY = datetime.now().strftime("%Y-%m-%d")

# Faber TAA tickers (Yahoo symbols)
FABER_TICKERS = {
    "V033_SPY":  {"symbol": "SPY",     "sleeve": "equity",    "desc": "SPY 10m-SMA"},
    "V034_GSCI": {"symbol": "GSG",     "sleeve": "commodity", "desc": "GSG 10m-SMA (GSCI proxy)"},
    "V035_BTC":  {"symbol": "BTC-USD", "sleeve": "crypto",    "desc": "BTC-USD 10m-SMA"},
}

# BAB ETF proxy
BAB_PROXY = {"long": "USMV", "short": "SPLV"}


def _yahoo_monthly_closes(symbol, range_str="18mo"):
    """
    Fetch Yahoo Finance monthly-bar adjusted closes. Returns list of
    (YYYY-MM-DD, close) tuples sorted ascending, or (None, error_str).
    14 months is the minimum for a trailing 10m-SMA computed at the
    previous month-end; 18mo is default for safety margin.
    """
    try:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
               f"?range={range_str}&interval=1mo")
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        adjclose = result["indicators"]["adjclose"][0]["adjclose"]
        series = []
        for t, c in zip(timestamps, adjclose):
            if c is None:
                continue
            d = datetime.fromtimestamp(t).strftime("%Y-%m-%d")
            series.append((d, float(c)))
        if len(series) < 11:
            return None, f"insufficient monthly bars for {symbol}: {len(series)}"
        return series, None
    except Exception as e:
        return None, f"Yahoo fetch failed for {symbol}: {e}"


# -------------------- V033-V035 Faber TAA --------------------

def compute_faber_taa():
    """
    Faber 10m-SMA overlay gate for SPY, GSCI (GSG proxy), BTC-USD.
    Read state at last month-end close — intraday recompute prohibited
    (Risk Rules §4.B).

    Returns dict of {var_id: {status, sleeve, current_close, sma_10m,
    gate_state, month_end_date}}
    """
    results = {}
    for var_id, meta in FABER_TICKERS.items():
        series, err = _yahoo_monthly_closes(meta["symbol"], range_str="18mo")
        if series is None:
            results[var_id] = {
                "status": "MISSING",
                "sleeve": meta["sleeve"],
                "symbol": meta["symbol"],
                "reason": err,
                "sources_attempted": [f"Yahoo Finance {meta['symbol']} (14mo monthly)"],
            }
            continue

        # Use the LAST COMPLETED month-end close (not the partial current month)
        # Current month bar will be incomplete until the calendar flips.
        # Risk Rules §4.B: "state flips only at end-of-month".
        # Defensive: drop the final bar if its timestamp is in the current month.
        current_month = datetime.now().strftime("%Y-%m")
        if series and series[-1][0].startswith(current_month):
            eligible = series[:-1]
        else:
            eligible = series

        if len(eligible) < 10:
            results[var_id] = {
                "status": "MISSING",
                "sleeve": meta["sleeve"],
                "symbol": meta["symbol"],
                "reason": f"insufficient completed-month bars: {len(eligible)}",
            }
            continue

        last10 = eligible[-10:]
        sma_10m = sum(c for _, c in last10) / 10.0
        current_close = eligible[-1][1]
        month_end_date = eligible[-1][0]
        gate_state = "ON" if current_close > sma_10m else "OFF"
        distance_pct = (current_close / sma_10m - 1.0) * 100.0

        results[var_id] = {
            "status": "OK",
            "sleeve": meta["sleeve"],
            "symbol": meta["symbol"],
            "current_close": round(current_close, 2),
            "sma_10m": round(sma_10m, 2),
            "gate_state": gate_state,
            "distance_pct": round(distance_pct, 2),
            "month_end_date": month_end_date,
            "n_bars": len(eligible),
        }
    return results


# -------------------- V029 BAB (ETF proxy) --------------------

def compute_bab_etf_proxy():
    """
    BAB tactical proxy: 12-month total-return spread between USMV (low-vol,
    low-β) and SPLV (low-vol). Not the canonical AQR BAB factor — this is a
    daily ETF spread used as a fast regime indicator. Canonical BAB (AQR
    monthly) deferred to Phase 2b.

    Returns {status, usmv_12m_pct, splv_12m_pct, spread_pct, direction}.
    """
    usmv_series, e1 = _yahoo_monthly_closes(BAB_PROXY["long"], range_str="14mo")
    splv_series, e2 = _yahoo_monthly_closes(BAB_PROXY["short"], range_str="14mo")

    if usmv_series is None or splv_series is None:
        return {
            "status": "MISSING",
            "reason": f"ETF proxy fetch failed: USMV={e1}; SPLV={e2}",
            "sources_attempted": ["Yahoo Finance USMV monthly", "Yahoo Finance SPLV monthly"],
        }

    # 12-month return = (last_close / 12mo_ago_close) - 1
    if len(usmv_series) < 13 or len(splv_series) < 13:
        return {
            "status": "MISSING",
            "reason": f"insufficient history: USMV={len(usmv_series)} SPLV={len(splv_series)}",
        }

    usmv_r = (usmv_series[-1][1] / usmv_series[-13][1] - 1.0) * 100.0
    splv_r = (splv_series[-1][1] / splv_series[-13][1] - 1.0) * 100.0
    spread = usmv_r - splv_r

    # Direction: positive spread → low-β (USMV) outperforming low-vol-only (SPLV),
    # consistent with BAB long low-β. Negative → high-β regime favor.
    direction = "PRO-BAB" if spread > 0 else "ANTI-BAB"

    return {
        "status": "OK",
        "proxy_type": "ETF (USMV - SPLV 12m)",
        "usmv_12m_pct": round(usmv_r, 2),
        "splv_12m_pct": round(splv_r, 2),
        "spread_pct": round(spread, 2),
        "direction": direction,
        "note": "Tactical proxy only. Canonical AQR BAB factor deferred to Phase 2b.",
    }


# -------------------- V030 DealerGamma --------------------

def compute_dealergamma():
    """
    DealerGamma requires paid data (SqueezeMetrics GEX or SpotGamma composite).
    Until Gerald confirms subscription, this returns MISSING with explicit
    subscription-pending reason (not fail-loud panic — documented policy).
    """
    return {
        "status": "MISSING",
        "reason": "Subscription pending — SqueezeMetrics / SpotGamma not confirmed as of 2026-04-18 GATE 1",
        "sources_attempted": [
            "SqueezeMetrics GEX (paid)",
            "SpotGamma daily composite (paid)",
        ],
        "grade": "B (single-paper Baltussen-Da-Lammers-Martens 2021 JFE; corrected 2026-04-22)",
        "next_review": "2026-07-01 quarterly methodology review",
    }


# -------------------- V031 GP/A --------------------

def compute_gpa():
    """
    GP/A stub. Full implementation requires Ken French GP monthly portfolio
    return CSV OR Compustat financial-statement pull. Phase 2 ships the row
    wired and MISSING; Phase 2b implements the actual compute.
    """
    return {
        "status": "MISSING",
        "reason": "Phase 2 stub — Ken French GP portfolio CSV fetcher not yet implemented",
        "sources_attempted": [
            "Ken French data library (Phase 2b TODO)",
            "Compustat self-compute (Phase 2b TODO)",
        ],
        "grade": "A (Novy-Marx 2013)",
        "cadence": "Quarterly data, monthly portfolio rebalance",
    }


# -------------------- V032 CEI --------------------

def compute_cei():
    """
    CEI stub. Full implementation requires CRSP + Compustat self-compute
    (scripts/compute_cei.py — deferred to Phase 2b).
    """
    return {
        "status": "MISSING",
        "reason": "Phase 2 stub — scripts/compute_cei.py self-compute not yet implemented",
        "sources_attempted": [
            "Self-compute from CRSP + Compustat (Phase 2b TODO)",
        ],
        "grade": "A (Daniel-Titman 2006)",
        "cadence": "Quarterly",
    }


# -------------------- Staging file writer --------------------

def write_staging_file(output_path, faber, bab, dealer, gpa, cei):
    lines = []
    lines.append(f"# Meta-Integration Variable Staging (V029-V035) — {TODAY}")
    lines.append(f"")
    lines.append(f"**Computed:** {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC+8")
    lines.append(f"**Consumer:** SHADOW MODE — brief/rec do not consume this file until Phase 3 live_date set.")
    lines.append(f"**Reference:** `meta-analysis-integration-plan-2026-04-18.md`, `framework/Methodology Prompt.md §Step 1.5`, `framework/Risk Rules.md §1.B, §4.B, §5.A, §8`.")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # V033-V035 Faber TAA
    lines.append(f"## V033-V035 C009 Faber TAA Overlay Gate (Step 1.5)")
    lines.append(f"")
    lines.append(f"Overlay state flips only at end-of-month (Risk Rules §4.B). State below uses LAST COMPLETED month-end close.")
    lines.append(f"")
    lines.append(f"| Var | Sleeve | Symbol | Month-End Date | Close | 10m-SMA | Distance % | **Gate State** |")
    lines.append(f"|-----|--------|--------|----------------|-------|---------|-----------:|---------------:|")
    for var_id, meta in FABER_TICKERS.items():
        v = faber.get(var_id, {})
        if v.get("status") == "OK":
            state_emoji = "**ON**" if v["gate_state"] == "ON" else "**OFF**"
            lines.append(f"| {var_id} | {v['sleeve']} | {v['symbol']} | {v['month_end_date']} "
                         f"| {v['current_close']:.2f} | {v['sma_10m']:.2f} "
                         f"| {v['distance_pct']:+.2f}% | {state_emoji} |")
        else:
            lines.append(f"| {var_id} | {meta['sleeve']} | {meta['symbol']} | MISSING | — | — | — | **MISSING** — {v.get('reason','?')} |")
    lines.append(f"")
    lines.append(f"**Sleeve-gate rule.** If `OFF`, position size × 0 on that sleeve (Step 1.5 Overlay Gate). Non-additive to Sum.")
    lines.append(f"")

    # V029 BAB
    lines.append(f"## V029 BAB (Betting-Against-Beta)")
    lines.append(f"")
    if bab.get("status") == "OK":
        lines.append(f"- Proxy: {bab['proxy_type']}")
        lines.append(f"- USMV 12m total return: **{bab['usmv_12m_pct']:+.2f}%**")
        lines.append(f"- SPLV 12m total return: **{bab['splv_12m_pct']:+.2f}%**")
        lines.append(f"- Spread (USMV - SPLV): **{bab['spread_pct']:+.2f}%**  ->  **{bab['direction']}**")
        lines.append(f"- *{bab['note']}*")
    else:
        lines.append(f"**Status: MISSING** — {bab.get('reason','?')}")
        for src in bab.get('sources_attempted', []):
            lines.append(f"- attempted: {src}")
    lines.append(f"")
    lines.append(f"**Sleeve rule.** V029 sleeve capped at 1/3 of V009 risk budget (Risk Rules §8). Correlation gate applies on same-ticker BAB leg + V009 spine long.")
    lines.append(f"")

    # V030 DealerGamma
    lines.append(f"## V030 DealerGamma")
    lines.append(f"")
    lines.append(f"**Status: {dealer['status']}** — {dealer['reason']}")
    lines.append(f"- Grade: {dealer['grade']}")
    lines.append(f"- Sources attempted: {', '.join(dealer['sources_attempted'])}")
    lines.append(f"- Next review: {dealer['next_review']}")
    lines.append(f"")

    # V031 GP/A
    lines.append(f"## V031 GP/A (Gross Profitability / Assets)")
    lines.append(f"")
    lines.append(f"**Status: {gpa['status']}** — {gpa['reason']}")
    lines.append(f"- Grade: {gpa['grade']}")
    lines.append(f"- Cadence: {gpa['cadence']}")
    lines.append(f"")

    # V032 CEI
    lines.append(f"## V032 CEI (Composite Equity Issuance)")
    lines.append(f"")
    lines.append(f"**Status: {cei['status']}** — {cei['reason']}")
    lines.append(f"- Grade: {cei['grade']}")
    lines.append(f"- Cadence: {cei['cadence']}")
    lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Shadow mode: this file is NOT consumed by brief or trade-rec. "
                 f"Phase 3 sets live_date on V029-V035 in VariableRegistry and updates "
                 f"brief/rec SKILL.md to read this file.*")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return output_path


# -------------------- Main --------------------

def main():
    parser = argparse.ArgumentParser(description="Compute meta-integration variables V029-V035")
    default_output = f"meta-additions-staging-{TODAY}.md"
    parser.add_argument("--output", default=default_output, help="Output staging file path")
    args = parser.parse_args()

    print("Meta-integration compute starting...")

    print("\n[V033-V035] Faber TAA...")
    faber = compute_faber_taa()
    for var_id, v in faber.items():
        if v["status"] == "OK":
            print(f"  {var_id} {v['symbol']} ({v['sleeve']}): {v['gate_state']} "
                  f"(close {v['current_close']:.2f} vs 10m-SMA {v['sma_10m']:.2f})")
        else:
            print(f"  {var_id} {v.get('symbol','?')}: MISSING — {v.get('reason','?')}")

    print("\n[V029] BAB ETF proxy...")
    bab = compute_bab_etf_proxy()
    if bab["status"] == "OK":
        print(f"  USMV {bab['usmv_12m_pct']:+.2f}% - SPLV {bab['splv_12m_pct']:+.2f}% "
              f"= {bab['spread_pct']:+.2f}% ({bab['direction']})")
    else:
        print(f"  MISSING — {bab['reason']}")

    print("\n[V030] DealerGamma...")
    dealer = compute_dealergamma()
    print(f"  {dealer['status']}: {dealer['reason']}")

    print("\n[V031] GP/A...")
    gpa = compute_gpa()
    print(f"  {gpa['status']}: {gpa['reason']}")

    print("\n[V032] CEI...")
    cei = compute_cei()
    print(f"  {cei['status']}: {cei['reason']}")

    output = write_staging_file(args.output, faber, bab, dealer, gpa, cei)
    print(f"\nStaging file written: {output}")

    # Exit 0 — fail-loud is in the file, not via exit code
    return 0


if __name__ == "__main__":
    sys.exit(main())
