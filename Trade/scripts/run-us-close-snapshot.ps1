# US Close Snapshot — runs daily at 09:00 (07:30 UTC+8 = 19:30 ET prev day)
# Invoked by Windows Task Scheduler task "Trade\US-Close-Snapshot"

$tradeRoot = "C:\Users\Lokis\OneDrive\Desktop\T.system\Trade"
$logDir    = Join-Path $tradeRoot "scripts\logs"
$date      = (Get-Date).ToString("yyyy-MM-dd")
$logFile   = Join-Path $logDir "us-close-snapshot-$date.log"

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$prompt = @'
CRITICAL: This is a utility delta snapshot, NOT a trading question. Do NOT follow
CLAUDE.md §Session Startup Protocol. Do NOT read framework/Methodology Prompt.md, framework/Coin core.md,
framework/Trad core.md, framework/Risk Rules.md, framework/Data Sources.md, or any other authoritative doc unless explicitly listed below.

Produce the US post-close delta snapshot (07:30 UTC+8 = 19:30 ET previous day). Lean, deltas-only.

Reads (and only these):
- /mnt/Trade/framework/Memory.md §2 Open Positions, §5 Watchlist, §6 Upcoming Catalysts
- Yesterday's /mnt/Trade/market-brief-*.md (brief v1/final levels for delta comparison)
- Yesterday's /mnt/Trade/trade-rec-*.md (promoted entries + open-position marks) if present

Action sequence:
1. Web-search US cash-session close for every variable that moved >1sigma or changed materially
   vs yesterday's brief: SPX, NDX, Dow, each open position in Memory §2, each watchlist
   Sum>=2 name, Brent, Gold, BTC, BTC ETF flows, VIX, DXY.
2. Pull yesterday's US econ releases (actual vs expected vs prior) and any after-hours earnings
   in the universe (INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC).
3. Write /mnt/Trade/us-close-snapshot-{YYYY-MM-DD}.md with sections:
   §1 Close snapshot (>1sigma moves and material changes, tabled)
   §2 Open-position review (close vs entry, stop, status — intact / flagged / stopped)
   §3 Watchlist update
   §4 Regime delta (is brief regime label still current?)
   §5 Overnight watch (top-3 things to monitor before US pre-open)
4. Target <=500 words. Flat items go in a one-line "Flat vs brief" footer.
5. No fail-loud on variables already covered by brief — this is a delta file, not a brief.

Exit summary (one line):
US close snapshot {YYYY-MM-DD} complete — {N_moves} >1sigma moves, regime delta={none|soft|hard}, open-pos status={intact|flagged|stopped}
'@

Push-Location $tradeRoot
try {
    "[$date $(Get-Date -Format 'HH:mm:ss')] Starting US close snapshot" | Tee-Object -FilePath $logFile
    $output = $prompt | claude --print 2>&1
    $output | Tee-Object -FilePath $logFile -Append
    "[$date $(Get-Date -Format 'HH:mm:ss')] Done" | Tee-Object -FilePath $logFile -Append
} catch {
    "[$date $(Get-Date -Format 'HH:mm:ss')] ERROR: $_" | Tee-Object -FilePath $logFile -Append
} finally {
    Pop-Location
}
