"""Generate HTML report for trade-rec."""
import sys, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')
src = Path(f"{today}/trade-rec-{today}.md")
out = Path(f"{today}/report-{today}-trade-rec.html")

md = src.read_text(encoding="utf-8")

# Pull header fields
gen_line = next((l for l in md.splitlines() if l.startswith("**Generated:")), "")
status_line = next((l for l in md.splitlines() if l.startswith("**Status:")), "")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trade Rec {today} (v2 Local Authoritative)</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px;margin:0 auto;padding:20px;background:#0f1117;color:#e1e4e8}}
h1{{color:#58a6ff;border-bottom:2px solid #21262d;padding-bottom:10px}}
h2{{color:#79c0ff;margin-top:28px}}
h3{{color:#d2a8ff}}
table{{border-collapse:collapse;width:100%;margin:14px 0;font-size:.88em}}
th{{background:#161b22;color:#8b949e;text-align:left;padding:8px 10px;border:1px solid #30363d}}
td{{padding:7px 10px;border:1px solid #21262d}}
tr:hover{{background:#161b22}}
.sum4{{color:#3fb950;font-weight:bold}}
.sum3{{color:#58a6ff;font-weight:bold}}
.sum2{{color:#e3b341}}
.neg{{color:#f85149}}
.badge{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:.8em;font-weight:600;margin-left:6px}}
.new{{background:#0d3d0d;color:#3fb950;border:1px solid #238636}}
.pend{{background:#2d2000;color:#e3b341;border:1px solid #d29922}}
.blk{{background:#2d0d0d;color:#f85149;border:1px solid #da3633}}
.conf{{background:#1a1a2d;color:#79c0ff;border:1px solid #1f6feb}}
.warn{{background:#2d2000;border-left:4px solid #d29922;padding:8px 12px;margin:10px 0;border-radius:4px}}
.info{{background:#0d1117;border-left:4px solid #1f6feb;padding:8px 12px;margin:10px 0;border-radius:4px}}
.delta{{background:#0d1a2e;border:1px solid #1f6feb;border-radius:6px;padding:12px 16px;margin:12px 0}}
.regime{{background:#1a1a2d;padding:10px 16px;border-radius:6px;border-left:4px solid #58a6ff;font-family:monospace;font-size:1.05em;color:#79c0ff;margin:12px 0}}
code{{background:#161b22;padding:1px 6px;border-radius:4px;font-family:monospace;color:#a5d6ff}}
.meta{{color:#8b949e;font-size:.9em;margin-top:-8px;margin-bottom:20px}}
</style>
</head>
<body>
<h1>Trade Recommendations — {today}</h1>
<div class="meta">
  <strong>v2 — Local Authoritative</strong> &nbsp;|&nbsp; Generated: 2026-04-21 20:20 UTC+8 &nbsp;|&nbsp;
  Supersedes: v1 cloud-7pm (Grade B) &nbsp;|&nbsp;
  <span style="color:#3fb950">5 Promoted</span> &nbsp;|&nbsp;
  <span style="color:#f85149">1 Gate-Blocked</span> &nbsp;|&nbsp;
  <span style="color:#e3b341">4 Near-Miss + 1 Downgraded</span>
</div>

<h2>&#9889; Delta vs Cloud-7pm v1 — MATERIAL CHANGE</h2>
<div class="delta">
<ul>
<li>&#x1F195; <strong>INTC Sum +4</strong> — T resolved to +1 (V026 residual +13.89%). Was T-blocked. <strong>NEW PROMOTION P013.</strong></li>
<li>&#x1F195; <strong>AAPL Sum +3</strong> — T resolved to +1 (V026 residual +4.68%). Was T-blocked. <strong>NEW PROMOTION P014.</strong></li>
<li>&#x1F504; <strong>GOOGL Sum +3</strong> — T resolved to 0 (−0.80%). Sum confirmed +3 via C+1. Entry after tonight's beat. <strong>P015.</strong></li>
<li>&#x2B07; <strong>PLTR downgraded</strong> — residual −35.62% → T=−1 → Sum +2. Removed from near-miss.</li>
<li>&#x2705; MOVE 67.90 (A, fresh) + V027 z +1.65 (A, fresh) — R now Grade A confirmed.</li>
<li>&#x2705; All 12 V026 residual momentum scores computed (numpy failure cleared at 19:48 UTC+8).</li>
</ul>
</div>

<h2>Regime</h2>
<div class="regime">RISK-ON / GEOPOLITICAL-BINARY &#8212; IRAN CEASEFIRE EXPIRED (APR-22 UTC+8)</div>
<table>
<tr><th>Dimension</th><th>State</th><th>Reading</th></tr>
<tr><td>Growth</td><td>Neutral-to-Positive</td><td>SPY $708.72, QQQ $646.79 (Apr-21 close); 88% Q1 EPS beat rate</td></tr>
<tr><td>Inflation</td><td>Mod-to-Uncertain</td><td>T10YIE 2.36%; WTI $86.32, Brent $90.03; CPI May 12</td></tr>
<tr><td>Policy</td><td>Dovish lean fading</td><td>DGS10 4.25%; FOMC Apr 28-29; CME &le;1 cut priced 2026</td></tr>
<tr><td>FCI</td><td>Loose, tightening</td><td>NFCI -0.47; HY OAS 285 bps (B); <strong>MOVE 67.90 (A,fresh)</strong>; IC z +1.65 (A,fresh)</td></tr>
<tr><td>Risk Sentiment</td><td>Risk-On, fragile</td><td>VIX 19.04 (B, at threshold); DXY 98.242; Nikkei +1.21% Apr-21</td></tr>
<tr><td>BTC Regime</td><td>Support-Hold</td><td>BTC $76,454 — 4th test $75K; Hash 1,065 EH/s</td></tr>
</table>

<h2>Overlay Gate (Faber TAA C009)</h2>
<table>
<tr><th>Sleeve</th><th>State</th><th>Effect</th></tr>
<tr style="background:#0d2d0d"><td>Equity</td><td><strong>ON</strong></td><td>New longs permitted</td></tr>
<tr style="background:#2d0d0d"><td>Commodity</td><td><strong>UNCERTAIN / effective OFF</strong></td><td>GSCI MISSING 4th run — no commodity longs</td></tr>
<tr style="background:#2d0d0d"><td>Crypto</td><td><strong>OFF</strong></td><td>BTC &lt; est. 10m-SMA</td></tr>
<tr style="background:#0d2d0d"><td>Intl Equity</td><td><strong>ON</strong></td><td>New intl equity longs permitted</td></tr>
</table>

<h2>Promoted Signals</h2>
<table>
<tr><th>Asset</th><th>Dir</th><th>Entry</th><th>Stop</th><th>Target</th><th>Risk%</th><th>S|T|C|R|Sum</th><th>Status</th></tr>
<tr style="background:#0d2d0d">
  <td><strong>INTC</strong> <span class="badge new">NEW P013</span></td>
  <td>LONG</td><td>$68-72 (post-beat)</td><td>~$63-67 (2xATR)</td><td>$75/$82</td><td>1.0%</td>
  <td><span class="sum4">+1|+1|+1|+1|+4</span></td><td>Pending Apr-23 AC beat</td>
</tr>
<tr style="background:#0d2d0d">
  <td><strong>AAPL</strong> <span class="badge new">NEW P014</span></td>
  <td>LONG</td><td>~$271-274 (immediate)</td><td>~$264-267 (2xATR)</td><td>$280/$290</td><td>0.75%</td>
  <td><span class="sum3">+1|+1|0|+1|+3</span></td><td>&#x26A0; Hard exit 2026-04-30</td>
</tr>
<tr style="background:#0d2d0d">
  <td><strong>GOOGL</strong> <span class="badge pend">P015 CONTINGENT</span></td>
  <td>LONG</td><td>~$333-340 (post-beat)</td><td>~$315-320 (2xATR)</td><td>$355/$375</td><td>0.75%</td>
  <td><span class="sum3">+1|0|+1|+1|+3</span></td><td>Pending Apr-23 UTC+8 beat confirm</td>
</tr>
<tr style="background:#0d2d0d">
  <td><strong>SPY</strong> <span class="badge conf">P009 RECONFIRMED</span></td>
  <td>LONG</td><td>$710.14 limit</td><td>$696 (2xATR)</td><td>$720/$730</td><td>1.0%</td>
  <td><span class="sum3">+1|+1|0|+1|+3</span></td><td>Fill pending</td>
</tr>
<tr style="background:#0d2d0d">
  <td><strong>EWJ</strong> <span class="badge conf">P010 RECONFIRMED</span></td>
  <td>LONG</td><td>~$90.24</td><td>$86.00 (2xATR)</td><td>$95/$98</td><td>0.75%</td>
  <td><span class="sum3">+1|+1|0|+1|+3</span></td><td>Fill pending</td>
</tr>
<tr style="background:#2d0d0d">
  <td><strong>Silver</strong> <span class="badge blk">P012 GATE-BLOCKED</span></td>
  <td>LONG</td><td>-</td><td>-</td><td>-</td><td>Taken=NO</td>
  <td><span class="sum3">+1|+1|0|+1|+3</span></td><td>Commodity UNCERTAIN/OFF</td>
</tr>
</table>

<div class="info">Portfolio heat if all filled: P008 0.33% + SPY 1.0% + EWJ 0.75% + AAPL 0.75% + INTC 1.0% + GOOGL 0.75% = <strong>4.58%</strong> (57% of 8% cap)</div>

<h2>Pre-Entry Checklist Highlights</h2>
<div class="warn"><strong>INTC P013:</strong> WAIT for confirmed beat Apr-23 AC. Enter Apr-24 UTC+8 morning. Prior P004 closed Apr-19 to avoid this binary — maintain discipline.</div>
<div class="warn"><strong>AAPL P014:</strong> Hard time-stop 2026-04-30. MUST exit before May 1 earnings. C=0 structural-only edge. 8-trading-day window.</div>
<div class="warn"><strong>GOOGL P015:</strong> Do not chase post-earnings gap. Wait for price stability. T=0 (not +1) — entry on C+1 confirmation, not momentum.</div>

<h2>Near-Misses</h2>
<table>
<tr><th>Asset</th><th>Sum</th><th>Block Reason</th><th>Trigger</th><th>ID</th></tr>
<tr style="background:#1a1a0d"><td>MU <span class="badge new">NEW</span></td><td><span class="sum3">+3</span></td><td>Correlation gate — equity sleeve at capacity</td><td>Post-FOMC Apr-30+</td><td>N036</td></tr>
<tr style="background:#1a1a0d"><td>QQQ</td><td><span class="sum3">+3</span></td><td>SPY preferred (corr-blocked)</td><td>Post earnings cluster Apr-30+</td><td>N034</td></tr>
<tr style="background:#1a1a0d"><td>NVDA <span class="badge new">NEW</span></td><td><span class="sum3">+3</span></td><td>Tech concentration; T=0</td><td>GOOGL beat tonight &#8594; C reinforced; V026 residual &gt;+2%</td><td>N037</td></tr>
<tr style="background:#1a1a0d"><td>Copper</td><td><span class="sum3">+3</span></td><td>Commodity sleeve UNCERTAIN/OFF</td><td>GSCI confirmed ON + China PMI &gt;50.5</td><td>N035</td></tr>
</table>
<table>
<tr><th>Downgraded</th><th>Prior</th><th>Now</th><th>Reason</th></tr>
<tr><td>PLTR</td><td>Near-miss Sum+3† (T-blocked)</td><td><span class="sum2">Sum +2</span></td><td>V026 residual -35.62% → T=-1. Factor crowding. Below threshold.</td></tr>
</table>

<h2>Catalyst Calendar</h2>
<table>
<tr><th>Date (UTC+8)</th><th>Event</th><th>Assets</th><th>Significance</th></tr>
<tr><td><strong>Apr-23 ~01:00</strong></td><td><strong>GOOGL Q1 earn. (AC)</strong></td><td>GOOGL,QQQ,NVDA</td><td>P015 entry trigger</td></tr>
<tr><td><strong>Apr-23 AC</strong></td><td><strong>INTC Q1 earn.</strong></td><td>INTC,QQQ</td><td>P013 entry trigger (enter Apr-24 morning)</td></tr>
<tr><td>Apr-23 AC</td><td>AMZN Q1 earn.</td><td>AMZN,QQQ</td><td>AMZN +2 → potential +3</td></tr>
<tr><td>Apr-24</td><td>UMich final April</td><td>SPY,DXY</td><td>Prelim 47.6 record low</td></tr>
<tr><td><strong>Apr-28-29</strong></td><td><strong>FOMC</strong></td><td>All</td><td>SPY P009 primary risk; hawkish surprise = exit rule</td></tr>
<tr><td><strong>Apr-30</strong></td><td><strong>AAPL P014 time-stop</strong></td><td>AAPL</td><td>Exit regardless of P&amp;L</td></tr>
<tr><td>May-12</td><td>April CPI</td><td>All</td><td>Hormuz inflation follow-through</td></tr>
</table>

<h2>Data Quality</h2>
<table>
<tr><th>Category</th><th>Status</th></tr>
<tr><td>Grade A MISSING</td><td>1 (GSCI commodity sleeve gate — 4th consecutive run)</td></tr>
<tr><td>V026 Residual Momentum</td><td><span style="color:#3fb950">ALL 12 LIVE ✓</span> (numpy failure cleared 19:48 UTC+8)</td></tr>
<tr><td>V027 IC z-score</td><td><span style="color:#3fb950">+1.65 LIVE ✓</span> — no R notch; full sizing</td></tr>
<tr><td>MOVE</td><td><span style="color:#3fb950">67.90 LIVE ✓</span> (A, low bond vol)</td></tr>
<tr><td>V028 Basis-Momentum</td><td>Brent LIVE; WTI/Gold/Silver/Copper STALE T3 (Apr-17)</td></tr>
<tr><td>Cloud Ingest</td><td>2/3 (market-brief + news; trade-rec not found on Drive)</td></tr>
</table>

<hr style="border-color:#21262d;margin-top:30px">
<div style="color:#8b949e;font-size:.82em;margin-top:12px">
Local authoritative v2 — supersedes cloud-7pm v1 (Grade B) — generated 2026-04-21 20:20 UTC+8
</div>
</body>
</html>"""

with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML written: {out}")
