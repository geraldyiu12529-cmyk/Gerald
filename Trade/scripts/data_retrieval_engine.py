#!/usr/bin/env python3
"""
Data Retrieval Engine — 4-tier fallback chain for all Grade A variables.

Tier 1: Direct HTTP (Yahoo Finance, CoinGecko, Blockchain.info, Kenneth French, NY Fed)
Tier 2: Web Search (multiple query patterns per variable, caller provides search function)
Tier 3: Persistent Cache (last known good, with staleness classification)
Tier 4: MISSING (fail-loud)

Every successful Tier 1 or Tier 2 retrieval automatically writes to the persistent cache.

Usage:
    from data_retrieval_engine import fetch, fetch_bulk, RetrievalResult

    # For single variables (brief / rec)
    result = fetch("VIX")
    result = fetch("HY_OAS", web_search_fn=my_web_search)

    # For bulk CSV data (audit-data-compute)
    result = fetch_bulk("ff5_factors.csv")
"""

import json
import re
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional

# Import sibling module
import sys
sys.path.insert(0, str(Path(__file__).parent))
from cache_manager import (
    write_cache, read_cache, write_bulk_cache, read_bulk_cache,
    copy_bulk_to_working, classify_staleness
)

HTTP_TIMEOUT = 15  # seconds per Tier 1 request
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


# ─── Result Types ────────────────────────────────────────────────────────────

@dataclass
class RetrievalResult:
    variable: str
    value: Any = None
    tier: int = 4  # 4 = MISSING
    source: str = "MISSING"
    staleness: str = "MISSING"
    timestamp: str = ""
    age_days: float = -1
    unit: str = ""
    error: str = ""
    attempts: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.tier < 4 and self.value is not None

    @property
    def is_stale(self) -> bool:
        return self.staleness.startswith("STALE")

    def brief_tag(self) -> str:
        """Return a tag for the brief output."""
        if self.staleness == "LIVE":
            return ""
        elif self.staleness == "STALE-OK":
            return f" (stale: {self.timestamp[:10]})"
        elif self.staleness == "STALE-WARN":
            return f" STALE-WARN — {self.timestamp[:10]}, {self.age_days:.0f}d old"
        else:
            return " MISSING"


@dataclass
class BulkRetrievalResult:
    filename: str
    file_path: Optional[Path] = None
    content: str = ""
    rows: int = 0
    tier: int = 4
    source: str = "MISSING"
    staleness: str = "MISSING"
    timestamp: str = ""
    age_days: float = -1
    error: str = ""
    attempts: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.tier < 4 and self.content != ""


# ─── Validation Ranges ───────────────────────────────────────────────────────

# Static baseline ranges — these define the "sane" universe for each variable.
# They're wide enough for normal market conditions but catch garbage data
# (e.g., a web search returning a year instead of a price).
VALIDATION_RANGES = {
    "VIX": (8, 90), "VIX3M": (8, 90), "MOVE": (40, 300),
    "DXY": (70, 130), "HY_OAS": (100, 2500),
    "DGS2": (0.0, 15.0), "DGS10": (0.0, 15.0), "2s10s": (-5.0, 5.0),
    "DFII10": (-3.0, 10.0), "T10YIE": (0.0, 8.0),
    "SPY": (100, 1500), "QQQ": (100, 1500), "SPX": (2000, 10000),
    "NDX": (5000, 30000),
    "NVDA": (10, 5000), "TSLA": (20, 3000), "AAPL": (50, 1000),
    "GOOGL": (30, 1000), "AMZN": (50, 1000), "META": (50, 3000),
    "TSM": (20, 500), "INTC": (5, 200), "MU": (10, 500),
    "PYPL": (10, 500), "PLTR": (5, 500), "WDC": (10, 500),
    "EWJ": (20, 200), "EWY": (20, 200),
    "Brent": (20, 200), "WTI": (20, 200),
    "Gold": (500, 10000), "Silver": (5, 200), "Copper": (1, 20),
    "Palladium": (100, 5000), "Platinum": (200, 5000),
    "EURUSD": (0.7, 1.5), "USDJPY": (70, 200),
    "GBPUSD": (0.8, 1.8), "AUDUSD": (0.4, 1.1),
    "BTC": (5000, 500000), "ETH": (500, 50000),
    "BTC_ActiveAddr": (100000, 2000000),
    "BTC_HashRate": (100, 2000),  # EH/s
    "NFCI": (-2.0, 5.0),
}

# Maximum single-day move as a fraction of the cached value.
# If a new reading deviates by more than this from the cached value,
# flag it as suspicious (but still accept if within static range).
# This catches stale data being served as fresh, and format changes
# returning a different variable's value.
MAX_DAILY_MOVE = {
    "VIX": 0.50,       # VIX can move 50% in a day (vol of vol)
    "MOVE": 0.30,
    "DXY": 0.05,       # Dollar index rarely moves >5% in a day
    "HY_OAS": 0.30,
    "SPY": 0.12, "QQQ": 0.15, "SPX": 0.12, "NDX": 0.15,
    "BTC": 0.25, "ETH": 0.30,  # Crypto can move 25-30%
    "Gold": 0.08, "Brent": 0.15, "WTI": 0.15,
    "EURUSD": 0.05, "USDJPY": 0.05,
    # Stocks can gap 15-20% on earnings
    "NVDA": 0.20, "TSLA": 0.20, "AAPL": 0.15, "GOOGL": 0.15,
    "AMZN": 0.15, "META": 0.20, "TSM": 0.20, "INTC": 0.25,
    "MU": 0.20, "PYPL": 0.20, "PLTR": 0.25, "WDC": 0.25,
}


def _validate(variable: str, value: float) -> bool:
    """
    Two-layer validation:
    1. Static range check — reject values outside the sane universe.
    2. Dynamic cache-proximity check — if we have a recent cached value,
       flag (but accept) values that moved more than the max daily move.
       This catches format changes returning a wrong variable's value.

    Returns True if the value should be accepted.
    Logs a warning dict to _validation_warnings if the move is suspicious.
    """
    # Layer 1: Static range
    if variable in VALIDATION_RANGES:
        low, high = VALIDATION_RANGES[variable]
        # Dynamic range widening: if the cached value is near a boundary,
        # extend the boundary by 30% to avoid rejecting valid extreme moves
        cached = read_cache(variable)
        if cached and cached.get("value") is not None:
            cached_val = cached["value"]
            if isinstance(cached_val, (int, float)):
                # If cached value is within 20% of a boundary, widen that boundary
                if cached_val > high * 0.8:
                    high = cached_val * 1.5  # widen upper bound
                if cached_val < low * 1.2 and low > 0:
                    low = cached_val * 0.5   # widen lower bound

        if not (low <= value <= high):
            return False

    # Layer 2: Cache-proximity check (advisory, not blocking)
    if variable in MAX_DAILY_MOVE:
        cached = read_cache(variable)
        if cached and cached.get("value") is not None:
            cached_val = cached["value"]
            if isinstance(cached_val, (int, float)) and cached_val != 0:
                pct_move = abs(value - cached_val) / abs(cached_val)
                max_move = MAX_DAILY_MOVE[variable]
                if pct_move > max_move:
                    # Suspicious but not blocking — the value passed the static
                    # range check so it's plausibly real. Log for review.
                    _validation_warnings.append({
                        "variable": variable,
                        "new_value": value,
                        "cached_value": cached_val,
                        "pct_move": round(pct_move * 100, 1),
                        "max_expected": round(max_move * 100, 1),
                        "action": "ACCEPTED_WITH_WARNING"
                    })

    return True


# Collects suspicious moves during a retrieval run for inclusion in brief/log
_validation_warnings: list = []


def get_validation_warnings() -> list:
    """Get and clear validation warnings from the current run."""
    global _validation_warnings
    warnings = _validation_warnings.copy()
    _validation_warnings = []
    return warnings


# ─── Tier 1: Direct HTTP Sources ─────────────────────────────────────────────

def _http_get(url: str, timeout: int = HTTP_TIMEOUT) -> Optional[str]:
    """Simple HTTP GET with error handling."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


def _tier1_yahoo(ticker: str) -> Optional[dict]:
    """
    Fetch a quote from Yahoo Finance chart API.
    Returns {"price": float, "timestamp": str, "raw": str} or None.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1d"
    raw = _http_get(url)
    if raw is None:
        return None

    try:
        data = json.loads(raw)
        meta = data["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice") or meta.get("previousClose")
        if price is None:
            return None
        ts = meta.get("regularMarketTime", 0)
        timestamp = datetime.fromtimestamp(ts).astimezone().isoformat() if ts else ""
        return {"price": float(price), "timestamp": timestamp, "raw": raw[:200]}
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def _tier1_coingecko(coin_id: str) -> Optional[dict]:
    """
    Fetch price from CoinGecko free API.
    Returns {"price": float, "timestamp": str, "raw": str} or None.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    raw = _http_get(url)
    if raw is None:
        return None

    try:
        data = json.loads(raw)
        price = data[coin_id]["usd"]
        return {
            "price": float(price),
            "timestamp": datetime.now().astimezone().isoformat(),
            "raw": raw[:200]
        }
    except (KeyError, TypeError, ValueError):
        return None


def _tier1_blockchain_info(chart_name: str) -> Optional[dict]:
    """
    Fetch BTC metric from Blockchain.info API.
    Returns {"value": float, "timestamp": str, "raw": str} or None.
    """
    url = f"https://api.blockchain.info/charts/{chart_name}?timespan=1days&format=json"
    raw = _http_get(url)
    if raw is None:
        return None

    try:
        data = json.loads(raw)
        values = data.get("values", [])
        if not values:
            return None
        latest = values[-1]
        value = float(latest["y"])

        # Unit conversion: blockchain.info reports hash-rate in TH/s,
        # but we track in EH/s (divide by 1e6)
        if chart_name == "hash-rate" and value > 1e6:
            value = value / 1e6  # TH/s → EH/s

        return {
            "value": value,
            "timestamp": datetime.fromtimestamp(latest["x"]).astimezone().isoformat(),
            "raw": raw[:200]
        }
    except (KeyError, IndexError, TypeError, ValueError):
        return None


# Yahoo Finance ticker mapping for Tier 1
YAHOO_TICKERS = {
    "VIX": "^VIX", "VIX3M": "^VIX3M", "MOVE": "^MOVE", "DXY": "DX-Y.NYB",
    "SPX": "^GSPC", "NDX": "^NDX",
    "SPY": "SPY", "QQQ": "QQQ", "EWJ": "EWJ", "EWY": "EWY",
    "NVDA": "NVDA", "TSLA": "TSLA", "AAPL": "AAPL", "GOOGL": "GOOGL",
    "AMZN": "AMZN", "META": "META", "TSM": "TSM", "INTC": "INTC",
    "MU": "MU", "PYPL": "PYPL", "PLTR": "PLTR", "WDC": "WDC",
    "Brent": "BZ=F", "WTI": "CL=F",
    "Gold": "GC=F", "Silver": "SI=F", "Copper": "HG=F",
    "Palladium": "PA=F", "Platinum": "PL=F",
    "EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X", "AUDUSD": "AUDUSD=X",
    "DGS10": "^TNX",  # 10Y yield proxy via Yahoo
    "BTC": "BTC-USD", "ETH": "ETH-USD",
}

# CoinGecko mapping
COINGECKO_IDS = {"BTC": "bitcoin", "ETH": "ethereum"}

# Blockchain.info mapping
BLOCKCHAIN_CHARTS = {
    "BTC_ActiveAddr": "n-unique-addresses",
    "BTC_HashRate": "hash-rate",
}


def _try_tier1(variable: str) -> Optional[RetrievalResult]:
    """
    Attempt Tier 1 direct HTTP retrieval.
    Returns RetrievalResult with tier=1 on success, None on failure.
    """
    result = RetrievalResult(variable=variable)

    # Try Yahoo Finance
    if variable in YAHOO_TICKERS:
        ticker = YAHOO_TICKERS[variable]
        data = _tier1_yahoo(ticker)
        if data and _validate(variable, data["price"]):
            result.value = data["price"]
            result.tier = 1
            result.source = f"Yahoo Finance API ({ticker})"
            result.staleness = "LIVE"
            result.timestamp = data.get("timestamp", datetime.now().astimezone().isoformat())
            result.unit = _get_unit(variable)
            # Write to cache
            write_cache(variable, result.value, 1, result.source,
                       result.unit, data.get("raw", ""), result.timestamp)
            return result

    # Try CoinGecko (for crypto, as alternative or primary)
    if variable in COINGECKO_IDS:
        data = _tier1_coingecko(COINGECKO_IDS[variable])
        if data and _validate(variable, data["price"]):
            result.value = data["price"]
            result.tier = 1
            result.source = f"CoinGecko API ({COINGECKO_IDS[variable]})"
            result.staleness = "LIVE"
            result.timestamp = data.get("timestamp", datetime.now().astimezone().isoformat())
            result.unit = "USD"
            write_cache(variable, result.value, 1, result.source,
                       result.unit, data.get("raw", ""), result.timestamp)
            return result

    # Try Blockchain.info
    if variable in BLOCKCHAIN_CHARTS:
        data = _tier1_blockchain_info(BLOCKCHAIN_CHARTS[variable])
        if data and _validate(variable, data["value"]):
            result.value = data["value"]
            result.tier = 1
            result.source = f"Blockchain.info ({BLOCKCHAIN_CHARTS[variable]})"
            result.staleness = "LIVE"
            result.timestamp = data.get("timestamp", datetime.now().astimezone().isoformat())
            result.unit = _get_unit(variable)
            write_cache(variable, result.value, 1, result.source,
                       result.unit, data.get("raw", ""), result.timestamp)
            return result

    # Try Chicago Fed for NFCI (FRED is blocked from sandbox)
    if variable == "NFCI":
        data = _tier1_chicago_fed_nfci()
        if data and _validate(variable, data["value"]):
            result.value = data["value"]
            result.tier = 1
            result.source = "Chicago Fed NFCI page (scrape)"
            result.staleness = "LIVE"
            result.timestamp = data.get("timestamp", datetime.now().astimezone().isoformat())
            result.unit = "index"
            write_cache(variable, result.value, 1, result.source,
                       result.unit, data.get("raw", ""), result.timestamp)
            return result

    return None  # No Tier 1 source available


def _tier1_chicago_fed_nfci() -> Optional[dict]:
    """
    Scrape NFCI value from Chicago Fed current-data page.
    The page contains a sentence like: "NFCI decreased to –0.47 in the week ending April 10."
    Returns {"value": float, "timestamp": str, "raw": str} or None.
    """
    import re as _re
    url = "https://www.chicagofed.org/research/data/nfci/current-data"
    raw = _http_get(url, timeout=15)
    if raw is None:
        return None

    try:
        # Pattern 1: "NFCI decreased/increased to –0.47 in the week ending ..."
        # The page uses en-dash (–) or minus (-) before the value
        match = _re.search(
            r'NFCI\s+(?:decreased|increased|was unchanged)\s+to\s+[–\-]?(\d+\.\d+)',
            raw
        )
        if match:
            # Check if there's a negative sign before the number
            # Get a wider context to check for the sign
            start = max(0, match.start() - 5)
            context = raw[start:match.end()]
            value = float(match.group(1))
            if '–' in context[context.rfind('to'):] or '-' in context[context.rfind('to'):]:
                # Check if the dash is right before the number (negative sign)
                pre_number = raw[match.start():match.start() + match.group(0).index(match.group(1))]
                if '–' in pre_number.split('to')[-1] or '-' in pre_number.split('to')[-1]:
                    value = -value

            # Extract date context — always produce ISO timestamp for cache compatibility
            timestamp = datetime.now().astimezone().isoformat()
            date_match = _re.search(
                r'week ending\s+(\w+)\s+(\d+)',
                raw[match.start():match.start() + 200]
            )
            if date_match:
                try:
                    month_str, day_str = date_match.group(1), date_match.group(2)
                    year = datetime.now().year
                    parsed = datetime.strptime(f"{month_str} {day_str} {year}", "%B %d %Y")
                    timestamp = parsed.astimezone().isoformat()
                except (ValueError, TypeError):
                    pass  # keep the now() timestamp

            return {"value": value, "timestamp": timestamp, "raw": raw[match.start():match.start()+200]}

        # Pattern 2: fallback — look for "NFCI" near a decimal like -0.47
        match2 = _re.search(r'NFCI[^.]{0,80}?([–\-]?\d+\.\d{2})', raw)
        if match2:
            val_str = match2.group(1).replace('–', '-')
            value = float(val_str)
            if VALIDATION_RANGES["NFCI"][0] <= value <= VALIDATION_RANGES["NFCI"][1]:
                return {
                    "value": value,
                    "timestamp": datetime.now().astimezone().isoformat(),
                    "raw": raw[match2.start():match2.start()+200]
                }

        return None
    except Exception:
        return None


# ─── Tier 2: Web Search Query Bank ──────────────────────────────────────────

TIER2_QUERIES = {
    "VIX": ["VIX close today CBOE", "CBOE volatility index VIX latest",
            "VIX index value site:yahoo.com"],
    "VIX3M": ["VIX3M index close today", "CBOE VIX 3 month index"],
    "MOVE": ["MOVE index bond volatility today", "ICE BofA MOVE index latest"],
    "DXY": ["US dollar index DXY close today", "DXY dollar index latest value"],
    "HY_OAS": ["high yield OAS spread FRED BAMLH0A0HYM2 latest",
               "ICE BofA high yield option adjusted spread today",
               "high yield credit spread basis points current"],
    "NFCI": ["Chicago Fed NFCI index value this week",
             "NFCI National Financial Conditions Index latest weekly reading",
             "site:chicagofed.org NFCI current data"],
    "DGS2": ["US 2 year treasury yield today", "2 year treasury note yield close"],
    "DGS10": ["US 10 year treasury yield today", "10 year treasury note yield close"],
    "DFII10": ["10 year TIPS real yield DFII10", "real yield 10 year inflation protected"],
    "T10YIE": ["10 year breakeven inflation T10YIE", "breakeven inflation rate 10 year"],
    "ACM_TP_10Y": ["ACM term premium 10 year NY Fed", "term premium 10 year estimate"],
    "Revision_Breadth": ["earnings revisions breadth S&P 500", "analyst estimate revisions this week"],
    "EIA_Crude_Stocks": ["EIA weekly petroleum status crude inventory",
                         "US crude oil inventory change this week"],
    "BTC_ExchNetflow": ["Bitcoin exchange netflows CryptoQuant", "BTC exchange inflows outflows"],
    "BTC_ETF_Flow": ["Bitcoin ETF net flows today Farside", "spot Bitcoin ETF flows daily"],
    "BTC_PerpFunding": ["Bitcoin perpetual funding rate", "BTC funding rate Binance"],
    "BTC_3mBasis": ["Bitcoin futures basis 3 month annualized", "BTC CME futures premium spot"],
    "ETH_ETF_Flow": ["Ethereum ETF net flows today", "spot Ether ETF daily flows"],
    "BTC_RealizedVol": ["Bitcoin 30 day realized volatility", "BTC realized vol"],
    # Equity prices — generated dynamically in _get_tier2_queries()
    # Commodity prices — generated dynamically
    # FX — generated dynamically
}


def _get_tier2_queries(variable: str) -> list:
    """Get web search queries for a variable, including dynamically generated ones."""
    if variable in TIER2_QUERIES:
        return TIER2_QUERIES[variable]

    # Dynamic generation for common patterns
    if variable in ["SPY", "QQQ", "EWJ", "EWY", "SPX", "NDX"]:
        return [f"{variable} close price today", f"{variable} ETF price",
                f"{variable} stock market close"]
    if variable in ["NVDA", "TSLA", "AAPL", "GOOGL", "AMZN", "META",
                    "TSM", "INTC", "MU", "PYPL", "PLTR", "WDC"]:
        return [f"{variable} stock price close today", f"{variable} share price",
                f"{variable} stock quote"]
    if variable in ["Brent", "WTI"]:
        return [f"{variable} crude oil price today", f"{variable} oil price per barrel"]
    if variable in ["Gold", "Silver", "Copper", "Palladium", "Platinum"]:
        return [f"{variable} price today per ounce", f"{variable} spot price",
                f"{variable} commodity price"]
    if variable in ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD"]:
        return [f"{variable} exchange rate today", f"{variable} forex rate"]
    if variable in ["BTC", "ETH"]:
        return [f"{'Bitcoin' if variable == 'BTC' else 'Ethereum'} price USD today",
                f"{variable} crypto price"]

    return [f"{variable} latest value", f"{variable} current reading"]


def _extract_number_from_text(text: str, variable: str) -> Optional[float]:
    """
    Try to extract a numeric value from web search result text.
    Handles various formats: 18.59, 4,523.50, $18.59, 18.59%, etc.
    """
    if not text:
        return None

    # Clean up common patterns
    text = text.replace(",", "").replace("$", "").replace("%", "")

    # Find all numbers in the text
    numbers = re.findall(r'-?\d+\.?\d*', text)
    if not numbers:
        return None

    # For variables with known ranges, find the first number in range
    if variable in VALIDATION_RANGES:
        low, high = VALIDATION_RANGES[variable]
        for n in numbers:
            try:
                val = float(n)
                if low <= val <= high:
                    return val
            except ValueError:
                continue

    # Fallback: return the first reasonable number
    try:
        return float(numbers[0])
    except ValueError:
        return None


def _try_tier2(variable: str, web_search_fn: Optional[Callable] = None) -> Optional[RetrievalResult]:
    """
    Attempt Tier 2 web search retrieval.
    web_search_fn should accept a query string and return search result text.
    Returns RetrievalResult with tier=2 on success, None on failure.
    """
    if web_search_fn is None:
        return None

    queries = _get_tier2_queries(variable)
    result = RetrievalResult(variable=variable)

    for i, query in enumerate(queries):
        try:
            search_result = web_search_fn(query)
            if search_result:
                value = _extract_number_from_text(str(search_result), variable)
                if value is not None and _validate(variable, value):
                    result.value = value
                    result.tier = 2
                    result.source = f"WebSearch ({query})"
                    result.staleness = "LIVE"
                    result.timestamp = datetime.now().astimezone().isoformat()
                    result.unit = _get_unit(variable)
                    # Write to cache
                    write_cache(variable, result.value, 2, result.source,
                               result.unit, str(search_result)[:200], result.timestamp)
                    return result
                else:
                    result.attempts.append({
                        "tier": 2, "query": query, "status": "no_valid_number",
                        "extracted": value
                    })
            else:
                result.attempts.append({"tier": 2, "query": query, "status": "empty_result"})
        except Exception as e:
            result.attempts.append({"tier": 2, "query": query, "status": f"error: {e}"})

    return None


def _try_tier3(variable: str) -> Optional[RetrievalResult]:
    """
    Attempt Tier 3 cache retrieval.
    Returns RetrievalResult with tier=3 on success, None if no cache or expired.
    """
    cached = read_cache(variable)
    if cached is None:
        return None

    result = RetrievalResult(
        variable=variable,
        value=cached["value"],
        tier=3,
        source=f"Cache (originally: {cached['source_name']})",
        staleness=cached["staleness"],
        timestamp=cached["timestamp"],
        age_days=cached["age_days"],
        unit=cached.get("unit", "")
    )
    return result


# ─── Main Fetch Interface ────────────────────────────────────────────────────

def fetch(variable: str, web_search_fn: Optional[Callable] = None,
          skip_tier1: bool = False) -> RetrievalResult:
    """
    Fetch a variable value through the 4-tier chain.

    Args:
        variable: Variable name (e.g., "VIX", "HY_OAS")
        web_search_fn: Callable for Tier 2 web search.
                       Signature: fn(query: str) -> str (search result text)
        skip_tier1: If True, skip direct HTTP (e.g., when preflight says source is down)

    Returns:
        RetrievalResult with the best available value and metadata.
    """
    result = RetrievalResult(variable=variable)
    start = time.time()

    # Tier 1: Direct HTTP
    if not skip_tier1:
        t1 = _try_tier1(variable)
        if t1 is not None and t1.ok:
            t1.attempts = [{"tier": 1, "status": "OK", "source": t1.source}]
            return t1
        if t1:
            result.attempts.extend(t1.attempts)
        result.attempts.append({"tier": 1, "status": "no_source" if t1 is None else "failed"})

    # Tier 2: Web Search
    t2 = _try_tier2(variable, web_search_fn)
    if t2 is not None and t2.ok:
        t2.attempts = result.attempts + [{"tier": 2, "status": "OK", "source": t2.source}]
        return t2
    if t2:
        result.attempts.extend(t2.attempts)
    result.attempts.append({"tier": 2, "status": "no_fn" if web_search_fn is None else "failed"})

    # Tier 3: Cache
    t3 = _try_tier3(variable)
    if t3 is not None:
        t3.attempts = result.attempts + [{"tier": 3, "status": "OK",
                                          "staleness": t3.staleness}]
        return t3
    result.attempts.append({"tier": 3, "status": "no_cache"})

    # Tier 4: MISSING
    result.tier = 4
    result.source = "MISSING"
    result.staleness = "MISSING"
    result.error = f"All tiers failed for {variable}"
    result.attempts.append({"tier": 4, "status": "MISSING"})
    return result


def fetch_many(variables: list, web_search_fn: Optional[Callable] = None,
               skip_tier1_for: list = None) -> dict:
    """
    Fetch multiple variables. Returns {variable: RetrievalResult}.
    """
    skip = set(skip_tier1_for or [])
    results = {}
    for var in variables:
        results[var] = fetch(var, web_search_fn, skip_tier1=(var in skip))
    return results


def fetch_bulk(filename: str, fetch_fn: Optional[Callable] = None,
               dest_dir: str = "/tmp/audit-data") -> BulkRetrievalResult:
    """
    Fetch a bulk CSV file through the retrieval chain.

    Args:
        filename: CSV filename (e.g., "ff5_factors.csv")
        fetch_fn: Optional callable that produces the CSV content (Tier 1).
                  Signature: fn() -> str (CSV content) or None
        dest_dir: Working directory to write the CSV

    Returns:
        BulkRetrievalResult with file_path pointing to usable CSV.
    """
    result = BulkRetrievalResult(filename=filename)

    # Tier 1: Direct fetch via provided function
    if fetch_fn is not None:
        try:
            content = fetch_fn()
            if content and len(content.strip().split('\n')) > 1:
                rows = len(content.strip().split('\n')) - 1
                # Write to persistent cache
                write_bulk_cache(filename, content, 1, "direct_fetch", rows)
                # Write to working dir
                dest = Path(dest_dir)
                dest.mkdir(parents=True, exist_ok=True)
                dest_path = dest / filename
                with open(dest_path, 'w') as f:
                    f.write(content)
                result.file_path = dest_path
                result.content = content
                result.rows = rows
                result.tier = 1
                result.source = "direct_fetch"
                result.staleness = "LIVE"
                result.timestamp = datetime.now().astimezone().isoformat()
                return result
        except Exception as e:
            result.attempts.append({"tier": 1, "status": f"error: {e}"})

    # Check working dir first (may have been placed by current run's web search)
    working_path = Path(dest_dir) / filename
    if working_path.exists():
        try:
            content = working_path.read_text()
            rows = len(content.strip().split('\n')) - 1
            if rows > 0:
                # Also cache it
                write_bulk_cache(filename, content, 1, "working_dir", rows)
                result.file_path = working_path
                result.content = content
                result.rows = rows
                result.tier = 1
                result.source = "working_dir"
                result.staleness = "LIVE"
                result.timestamp = datetime.now().astimezone().isoformat()
                return result
        except Exception:
            pass

    # Tier 3: Persistent cache
    cached = read_bulk_cache(filename)
    if cached is not None:
        # Copy to working dir
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        dest_path = dest / filename
        with open(dest_path, 'w') as f:
            f.write(cached["content"])

        result.file_path = dest_path
        result.content = cached["content"]
        result.rows = cached["rows"]
        result.tier = 3
        result.source = f"cache (originally: {cached['source_name']})"
        result.staleness = cached["staleness"]
        result.timestamp = cached["timestamp"]
        result.age_days = cached["age_days"]
        return result

    # Tier 4: MISSING
    result.tier = 4
    result.source = "MISSING"
    result.staleness = "MISSING"
    result.error = f"No data available for {filename}"
    return result


# ─── Utility Functions ───────────────────────────────────────────────────────

def _get_unit(variable: str) -> str:
    """Get the unit of measurement for a variable."""
    units = {
        "VIX": "index", "VIX3M": "index", "MOVE": "index", "DXY": "index",
        "HY_OAS": "bps", "NFCI": "index",
        "DGS2": "percent", "DGS10": "percent", "DFII10": "percent",
        "T10YIE": "percent", "ACM_TP_10Y": "percent", "2s10s": "percent",
        "BTC": "USD", "ETH": "USD",
        "Gold": "USD/oz", "Silver": "USD/oz", "Copper": "USD/lb",
        "Brent": "USD/bbl", "WTI": "USD/bbl",
        "BTC_ActiveAddr": "addresses", "BTC_HashRate": "EH/s",
    }
    return units.get(variable, "")


def format_retrieval_summary(results: dict) -> str:
    """
    Format a retrieval summary for inclusion in briefs/recs.

    Args:
        results: dict of {variable: RetrievalResult}

    Returns:
        Markdown-formatted summary string.
    """
    t1 = sum(1 for r in results.values() if r.tier == 1)
    t2 = sum(1 for r in results.values() if r.tier == 2)
    t3 = sum(1 for r in results.values() if r.tier == 3)
    t4 = sum(1 for r in results.values() if r.tier == 4)
    total = len(results)

    lines = [f"**Data retrieval:** {total} variables — "
             f"{t1} direct (T1), {t2} web search (T2), "
             f"{t3} cache (T3), {t4} MISSING (T4)"]

    stale = [(v, r) for v, r in results.items() if r.staleness.startswith("STALE")]
    if stale:
        stale_items = [f"{v} ({r.staleness}, {r.age_days:.0f}d)" for v, r in stale]
        lines.append(f"**Stale readings:** {', '.join(stale_items)}")

    missing = [v for v, r in results.items() if r.tier == 4]
    if missing:
        lines.append(f"**MISSING (fail-loud):** {', '.join(missing)}")

    return "\n".join(lines)


# ─── Preflight Health Check ──────────────────────────────────────────────────

def preflight_check() -> dict:
    """
    Quick connectivity test to key data sources.
    Returns a dict with source availability and advisory messages.
    """
    sources = {}

    # Yahoo Finance
    try:
        resp = _http_get("https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=1d&interval=1d",
                         timeout=8)
        sources["yahoo"] = resp is not None
    except Exception:
        sources["yahoo"] = False

    # CoinGecko
    try:
        resp = _http_get("https://api.coingecko.com/api/v3/ping", timeout=8)
        sources["coingecko"] = resp is not None
    except Exception:
        sources["coingecko"] = False

    # Blockchain.info
    try:
        resp = _http_get("https://api.blockchain.info/charts/market-price?timespan=1days&format=json",
                         timeout=8)
        sources["blockchain"] = resp is not None
    except Exception:
        sources["blockchain"] = False

    # Kenneth French
    try:
        resp = _http_get("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
                         timeout=8)
        sources["french_library"] = resp is not None
    except Exception:
        sources["french_library"] = False

    # NY Fed
    try:
        resp = _http_get("https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics",
                         timeout=8)
        sources["nyfed"] = resp is not None
    except Exception:
        sources["nyfed"] = False

    # Chicago Fed (NFCI)
    try:
        resp = _http_get("https://www.chicagofed.org/research/data/nfci/current-data",
                         timeout=8)
        sources["chicago_fed"] = resp is not None
    except Exception:
        sources["chicago_fed"] = False

    # Cache coverage
    from cache_manager import get_cache_coverage
    coverage = get_cache_coverage()

    # Build advisory
    advisories = []
    down_sources = [k for k, v in sources.items() if not v]
    if down_sources:
        advisories.append(f"Sources down: {', '.join(down_sources)} — will use Tier 2/3 fallback")
    if coverage["coverage_pct"] < 50:
        advisories.append(f"Cache coverage low ({coverage['coverage_pct']}%) — "
                         f"MISSING risk elevated if web search also fails")

    return {
        "timestamp": datetime.now().astimezone().isoformat(),
        "sources": sources,
        "cache_coverage": f"{coverage['cached']}/{coverage['total']} variables cached",
        "cache_coverage_pct": coverage["coverage_pct"],
        "predicted_missing": len(coverage["missing_variables"]) if not all(sources.values()) else 0,
        "advisories": advisories,
        "skip_tier1_for": _sources_to_variables(down_sources)
    }


def _sources_to_variables(down_sources: list) -> list:
    """Map down sources to variables that should skip Tier 1."""
    skip = []
    if "yahoo" in down_sources:
        skip.extend(YAHOO_TICKERS.keys())
    if "coingecko" in down_sources:
        skip.extend(COINGECKO_IDS.keys())
    if "blockchain" in down_sources:
        skip.extend(BLOCKCHAIN_CHARTS.keys())
    return skip


def write_preflight_status(status: dict, output_path: str = None):
    if output_path is None:
        from pipeline_status import TRADE_DIR
        output_path = str(TRADE_DIR / "pipeline" / ".pipeline-health.json")
    """Write preflight status to a JSON file for downstream tasks."""
    with open(output_path, 'w') as f:
        json.dump(status, f, indent=2)


# ─── Tier Degradation Detection ─────────────────────────────────────────────

def analyze_retrieval_health(lookback_days: int = 7) -> dict:
    """
    Analyze the retrieval log for tier degradation patterns.

    Reads retrieval-log.jsonl, computes tier distribution over the lookback
    window, compares the most recent day vs the window average, and flags
    alerts when:
      - T1 success rate drops >15 pp below the window average
      - T3 cache usage rises >15 pp above the window average
      - T4 MISSING count exceeds 3 in any single run
      - Any variable has been MISSING on 3+ days in the window

    Returns a dict with:
      {
        "window_days": int,
        "runs_analyzed": int,
        "avg_tier_pct": {"t1": float, "t2": float, "t3": float, "t4": float},
        "latest_tier_pct": {"t1": float, "t2": float, "t3": float, "t4": float},
        "chronic_missing": [{"variable": str, "days_missing": int}],
        "alerts": [str],
        "status": "NOMINAL" | "DEGRADED" | "CRITICAL"
      }
    """
    from cache_manager import CACHE_DIR
    log_path = CACHE_DIR / "retrieval-log.jsonl"

    if not log_path.exists():
        return {
            "window_days": lookback_days,
            "runs_analyzed": 0,
            "avg_tier_pct": {},
            "latest_tier_pct": {},
            "chronic_missing": [],
            "alerts": ["No retrieval log found — first run pending"],
            "status": "NOMINAL"
        }

    # Parse log entries within the lookback window
    entries = []
    cutoff = datetime.now().astimezone() - timedelta(days=lookback_days)
    try:
        with open(log_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    # Parse timestamp
                    ts_str = entry.get("timestamp", entry.get("date", ""))
                    if "T" in ts_str:
                        ts = datetime.fromisoformat(ts_str)
                    else:
                        ts = datetime.strptime(ts_str[:10], "%Y-%m-%d").astimezone()
                    if ts >= cutoff:
                        entry["_parsed_ts"] = ts
                        entries.append(entry)
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception:
        return {
            "window_days": lookback_days,
            "runs_analyzed": 0,
            "avg_tier_pct": {},
            "latest_tier_pct": {},
            "chronic_missing": [],
            "alerts": ["Error reading retrieval log"],
            "status": "NOMINAL"
        }

    if not entries:
        return {
            "window_days": lookback_days,
            "runs_analyzed": 0,
            "avg_tier_pct": {},
            "latest_tier_pct": {},
            "chronic_missing": [],
            "alerts": [f"No retrieval log entries in the past {lookback_days} days"],
            "status": "NOMINAL"
        }

    # Sort by timestamp
    entries.sort(key=lambda e: e["_parsed_ts"])

    # Compute tier percentages per run
    def _tier_pcts(e):
        total = e.get("variables_attempted", 1) or 1
        return {
            "t1": e.get("tier1_success", 0) / total * 100,
            "t2": e.get("tier2_success", 0) / total * 100,
            "t3": e.get("tier3_cache_used", 0) / total * 100,
            "t4": e.get("tier4_missing", 0) / total * 100,
        }

    run_pcts = [_tier_pcts(e) for e in entries]

    # Window average
    n = len(run_pcts)
    avg_pct = {
        "t1": sum(r["t1"] for r in run_pcts) / n,
        "t2": sum(r["t2"] for r in run_pcts) / n,
        "t3": sum(r["t3"] for r in run_pcts) / n,
        "t4": sum(r["t4"] for r in run_pcts) / n,
    }

    # Latest run
    latest_pct = run_pcts[-1]
    latest_entry = entries[-1]

    # Chronic MISSING: variables MISSING on 3+ days in the window
    missing_counter = {}
    for e in entries:
        date_key = e.get("date", e.get("timestamp", ""))[:10]
        for var in e.get("missing_variables", []):
            if var not in missing_counter:
                missing_counter[var] = set()
            missing_counter[var].add(date_key)
    chronic_missing = [
        {"variable": var, "days_missing": len(dates)}
        for var, dates in sorted(missing_counter.items())
        if len(dates) >= 3
    ]

    # Alerts
    alerts = []

    # Alert 1: T1 rate drop
    t1_drop = avg_pct["t1"] - latest_pct["t1"]
    if t1_drop > 15:
        alerts.append(
            f"T1 direct success rate dropped: {latest_pct['t1']:.0f}% vs "
            f"{avg_pct['t1']:.0f}% avg (−{t1_drop:.0f}pp)"
        )

    # Alert 2: T3 cache rise
    t3_rise = latest_pct["t3"] - avg_pct["t3"]
    if t3_rise > 15:
        alerts.append(
            f"Cache dependency rising: T3 at {latest_pct['t3']:.0f}% vs "
            f"{avg_pct['t3']:.0f}% avg (+{t3_rise:.0f}pp)"
        )

    # Alert 3: High MISSING in latest run
    latest_missing_count = latest_entry.get("tier4_missing", 0)
    if latest_missing_count > 3:
        missing_vars = latest_entry.get("missing_variables", [])
        alerts.append(
            f"High MISSING count: {latest_missing_count} variables "
            f"({', '.join(missing_vars[:5])})"
        )

    # Alert 4: Chronic MISSING
    for cm in chronic_missing:
        alerts.append(
            f"Chronic MISSING: {cm['variable']} missing on "
            f"{cm['days_missing']}/{lookback_days} days"
        )

    # Status classification
    if latest_missing_count > 5 or len(chronic_missing) > 3:
        status = "CRITICAL"
    elif alerts:
        status = "DEGRADED"
    else:
        status = "NOMINAL"

    return {
        "window_days": lookback_days,
        "runs_analyzed": n,
        "avg_tier_pct": {k: round(v, 1) for k, v in avg_pct.items()},
        "latest_tier_pct": {k: round(v, 1) for k, v in latest_pct.items()},
        "chronic_missing": chronic_missing,
        "alerts": alerts,
        "status": status
    }


def format_health_summary(health: dict, compact: bool = True) -> str:
    """
    Format the retrieval health analysis into a markdown snippet
    for inclusion in the daily brief or weekly review.

    Args:
        health: Output from analyze_retrieval_health()
        compact: If True, produce a 2-3 line summary (for daily brief).
                 If False, produce a full section (for weekly review).
    """
    if health["runs_analyzed"] == 0:
        return f"**Retrieval health:** {health['alerts'][0] if health['alerts'] else 'No data yet'}"

    status_emoji = {"NOMINAL": "OK", "DEGRADED": "WARN", "CRITICAL": "ALERT"}
    status_tag = status_emoji.get(health["status"], health["status"])
    avg = health["avg_tier_pct"]
    latest = health["latest_tier_pct"]

    if compact:
        # 2-3 line summary for daily brief
        line1 = (f"**Retrieval health ({status_tag}):** "
                 f"T1 {latest['t1']:.0f}% / T2 {latest['t2']:.0f}% / "
                 f"T3 {latest['t3']:.0f}% / T4 {latest['t4']:.0f}% "
                 f"(7d avg: T1 {avg['t1']:.0f}%)")
        if health["alerts"]:
            line1 += f"\n  Alerts: {'; '.join(health['alerts'][:2])}"
        return line1

    # Full section for weekly review
    lines = [
        f"### Retrieval Health — {health['status']}",
        f"",
        f"Window: {health['window_days']} days, {health['runs_analyzed']} runs analyzed",
        f"",
        f"| Tier | Latest | 7d Avg |",
        f"|------|--------|--------|",
        f"| T1 Direct | {latest['t1']:.1f}% | {avg['t1']:.1f}% |",
        f"| T2 WebSearch | {latest['t2']:.1f}% | {avg['t2']:.1f}% |",
        f"| T3 Cache | {latest['t3']:.1f}% | {avg['t3']:.1f}% |",
        f"| T4 MISSING | {latest['t4']:.1f}% | {avg['t4']:.1f}% |",
    ]

    if health["chronic_missing"]:
        lines.append("")
        lines.append("**Chronic MISSING variables:**")
        for cm in health["chronic_missing"]:
            lines.append(f"- {cm['variable']}: missing {cm['days_missing']}/{health['window_days']}d")

    if health["alerts"]:
        lines.append("")
        lines.append("**Alerts:**")
        for a in health["alerts"]:
            lines.append(f"- {a}")

    return "\n".join(lines)


if __name__ == "__main__":
    """Quick self-test: run preflight check and attempt a few Tier 1 fetches."""
    print("=== Data Retrieval Engine Self-Test ===\n")

    # Preflight
    print("Running preflight check...")
    status = preflight_check()
    for source, available in status["sources"].items():
        mark = "OK" if available else "DOWN"
        print(f"  {source:20s} {mark}")
    print(f"  Cache coverage: {status['cache_coverage']}")
    for adv in status["advisories"]:
        print(f"  Advisory: {adv}")

    # Test a few Tier 1 fetches
    print("\nTier 1 fetch tests:")
    test_vars = ["VIX", "BTC", "Gold", "BTC_ActiveAddr", "SPY"]
    for var in test_vars:
        result = fetch(var)
        if result.ok:
            print(f"  {var:20s} = {result.value:>12} | T{result.tier} | {result.source}")
        else:
            print(f"  {var:20s} = MISSING | {result.error}")
