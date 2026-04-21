---
name: us-close-snapshot
description: Daily US post-close delta snapshot — >1σ moves, open-position review, overnight watch (Mon–Fri 07:30 UTC+8)
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

**CRITICAL: This is a utility delta snapshot, NOT a trading question. Do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules, Data Sources, or any other authoritative doc unless explicitly listed below.**

Produce the US post-close delta snapshot. Lean, deltas-only.

Ensure today's date folder exists: `mkdir -p {YYYY-MM-DD}` (all dated outputs live under `{YYYY-MM-DD}/`).

**Reads (and only these):**
- Memory.md §2 Open Positions, §5 Watchlist, §6 Upcoming Catalysts
- Yesterday's `*/market-brief-*.md` (brief v1/final levels for Δ comparison; glob the most recent under any date folder, fall back to root `market-brief-*.md` for legacy runs)
- Yesterday's `*/trade-rec-*.md` (promoted entries + open-position marks) if present — same glob + fallback

**Action sequence:**
1. Web-search US cash-session close for every variable that moved >1σ or changed materially vs yesterday's brief: SPX, NDX, Dow, each open position in Memory §2, each watchlist Sum≥2 name, Brent, Gold, BTC, BTC ETF flows, VIX, DXY.
2. Pull yesterday's US econ releases (actual vs expected vs prior) and any after-hours earnings in the universe (INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC).
3. Write `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md` (use today's date) with sections:
   §1 Close snapshot (>1σ moves and material changes, tabled)
   §2 Open-position review (close vs entry, stop, status — intact / flagged / stopped)
   §3 Watchlist update
   §4 Regime delta (is brief regime label still current?)
   §5 Overnight watch (top-3 things to monitor before US pre-open)
4. Target ≤500 words. Flat items go in a one-line "Flat vs brief" footer.
5. No fail-loud on variables already covered by brief — this is a delta file, not a brief.
6. Pack into the consolidated daily file (writes `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`; upserts §A in-place if it exists):
   `python scripts/pack_daily.py --section A --source {YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md --status "delta={none|soft|hard}"`
   The per-day `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md` source file is the canonical artifact (downstream brief/rec reads it).

Exit summary (one line):
`US close snapshot {YYYY-MM-DD} complete — {N_moves} >1σ moves, regime delta={none|soft|hard}, open-pos status={intact|flagged|stopped}, packed={YYYY-MM-DD}/daily-{YYYY-MM-DD}.md §A`

Then git add -A, commit with message "routine: us-close-snapshot {today}", and push to origin main.