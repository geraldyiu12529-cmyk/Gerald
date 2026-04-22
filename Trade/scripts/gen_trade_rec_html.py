"""Canonical HTML generator for trade-rec reports.
   Update the PER-RUN DATA section below for each new date, then run:
       python scripts/gen_trade_rec_html.py
"""
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# PER-RUN DATA — update these for every date
# ══════════════════════════════════════════════════════════════════════════════

TODAY      = "2026-04-21"
VERSION    = "v2 Local"
GEN_TIME   = "2026-04-21 20:20 UTC+8"
SUPERSEDES = "Supersedes cloud-7pm v1 (Grade B). "
STATUS_CLS = "ok"       # ok / warn / bad
STATUS_TXT = "OK"
MISS_COUNT = "1 (GSCI gate)"
V026_ST    = "ALL 12 LIVE ✓"
V027_ST    = "z+1.65 ✓"
MOVE_ST    = "67.90 ✓"

# Executive summary cards: (label, val_text, val_css_class, sub_text)
# val_css_class: "ok" / "warn" / "bad" / ""
EXEC_PROMOTED = ("Promoted This Run",   "5 signals", "ok",   "INTC +4 · AAPL +3 · GOOGL +3 · SPY · EWJ")
EXEC_NEARMISS = ("Near-Miss / Blocked", "4 + 1",     "warn", "MU, QQQ, NVDA, Copper · Silver gate-blocked")
EXEC_REGIME   = ("Regime",              "Risk-On / Geo-Binary", "", "Ceasefire EXPIRED · VIX 19.04 at threshold")
EXEC_HEAT     = ("Heat (if all filled)","4.58%",     "",     "≤ 8% cap · room for MU post-FOMC")

# ── Data Freshness Strip ───────────────────────────────────────────────────────
# (variable, reading, grade, pill_cls, age_note)
# pill_cls: "green"=LIVE A, "blue"=LIVE B, "yellow"=STALE, "red"=MISSING
FRESHNESS = [
    ("MOVE",    "67.90",   "A", "green",  "fresh Apr-21"),
    ("V027",    "+1.65",   "A", "green",  "fresh Apr-21"),
    ("V026",    "12/12",   "A", "green",  "Apr-21 19:48"),
    ("VIX",     "19.04",   "B", "blue",   "Apr-21"),
    ("DXY",     "98.242",  "A", "green",  "Apr-21"),
    ("HY OAS",  "285bp",   "B", "blue",   "Apr-19 OK"),
    ("DGS10",   "4.25%",   "A", "green",  "Apr-21"),
    ("SPY/QQQ", "$708/$646","A","green",  "Apr-21 close"),
    ("Brent/WTI","$90/$86","A", "green",  "Apr-21"),
    ("VIX3M",   "20.51",   "B", "yellow", "stale Apr-18"),
    ("NFCI",    "−0.47",   "A", "yellow", "11d stale Apr-10"),
    ("V028",    "Partial", "A", "yellow", "Brent only; others T3"),
    ("GSCI",    "MISSING", "A", "red",    "4th consecutive run"),
]

# ── V026 Residual Momentum (all tracked tickers) ──────────────────────────────
# (ticker, residual_pct_or_None, t_score, signal_note)
# residual_pct: None = computed but not individually reported / not computed
V026_RESIDUALS = [
    ("MU",    +15.63, "+1", "N040 near-miss (capacity gate)"),
    ("INTC",  +13.89, "+1", "P013 PROMOTED"),
    ("AAPL",  +4.68,  "+1", "P014 PROMOTED"),
    ("AMZN",  None,   "—",  "computed; not individually reported"),
    ("WDC",   None,   "—",  "computed; not individually reported"),
    ("MSFT",  None,   "—",  "computed; not individually reported"),
    ("META",  None,   "—",  "computed; not individually reported"),
    ("PYPL",  None,   "—",  "computed; not individually reported"),
    ("NVDA",  -1.00,  "0",  "N041 near-miss (tech concentration + T=0)"),
    ("GOOGL", -0.80,  "0",  "P015 — T=0; Sum+3 via C+1"),
    ("TSLA",  -9.12,  "-1", "confirmed no-trade"),
    ("PLTR",  -35.62, "-1", "downgraded from near-miss; factor crowding"),
    ("TSM",   None,   "—",  "not computed (data N/A this run)"),
    ("AVGO",  None,   "—",  "not computed (data N/A this run)"),
    ("BABA",  None,   "—",  "not computed (data N/A this run)"),
]

# ── Signal Age / Time-Decay ───────────────────────────────────────────────────
# (ID, asset, status, promoted_date, days_held, expiry_date, days_remaining, urgency_cls)
# urgency_cls: "ok" ≥20d / "warn" 10–19d / "bad" <10d
SIGNAL_AGE = [
    ("P008", "CLUSDT (WTI)", "Open — off-meth",  "2026-04-03", 18, "2026-05-03", 12, "warn"),
    ("P009", "SPY",           "Pending fill",      "2026-04-20",  1, "2026-05-13", 22, "ok"),
    ("P010", "EWJ",           "Pending fill",      "2026-04-21",  0, "2026-06-30", 70, "ok"),
    ("P013", "INTC",          "Awaiting Apr-23 beat","2026-04-21",0, "2026-06-23", 63, "ok"),
    ("P014", "AAPL",          "Pending fill",      "2026-04-21",  0, "2026-04-30",  9, "bad"),
    ("P015", "GOOGL",         "Contingent",        "2026-04-21",  0, "2026-05-15", 24, "ok"),
]

# ── Factor Exposure Aggregate ─────────────────────────────────────────────────
# (ID, asset, status, size_pct, S, T, C, R)
FACTOR_EXPOSURE = [
    ("P008", "CLUSDT",  "Open (off-meth)", 0.33, 1, 1, 1, 1),
    ("P009", "SPY",     "Pending",         1.00, 1, 1, 0, 1),
    ("P010", "EWJ",     "Pending",         0.75, 1, 1, 0, 1),
    ("P013", "INTC",    "Awaiting",        1.00, 1, 1, 1, 1),
    ("P014", "AAPL",    "Pending",         0.75, 1, 1, 0, 1),
    ("P015", "GOOGL",   "Contingent",      0.75, 1, 0, 1, 1),
]

# ── Regime Sensitivity Table ──────────────────────────────────────────────────
# Each scenario column: (header_text, header_cls)
SCENARIOS = [
    ("VIX → 28",          "warn"),
    ("FOMC +50bp",        "bad"),
    ("Iran Esc. +15%",    "warn"),
    ("Iran Deal −10%",    "ok"),
    ("SPY −5%",           "bad"),
]
# (ID, asset, [(impact_cls, short_label), ...])  — one tuple per SCENARIO column (same order)
SENSITIVITY = [
    ("P008", "CLUSDT Long", [
        ("warn", "Indirect — oil ≠ VIX"),
        ("bad",  "USD↑ → WTI pressure"),
        ("ok",   "THESIS ✓ WTI +15%"),
        ("bad",  "STOP HIT ~$85.30"),
        ("warn", "Risk-off corr."),
    ]),
    ("P009", "SPY Long", [
        ("bad",  "EXIT: VIX > 25"),
        ("bad",  "EXIT: primary risk"),
        ("warn", "Oil shock spillover"),
        ("ok",   "Risk-on boost"),
        ("bad",  "STOP $696 in range"),
    ]),
    ("P010", "EWJ Long", [
        ("warn", "Risk-off; BOJ caution"),
        ("bad",  "USD↑ JPY weak → EWJ↓"),
        ("warn", "Global risk-off"),
        ("ok",   "Risk-on; Nikkei↑"),
        ("bad",  "High SPY corr."),
    ]),
    ("P013", "INTC Long", [
        ("warn", "Tech selloff; stop buffer OK"),
        ("warn", "Sector rotation risk"),
        ("warn", "VIX indirect only"),
        ("ok",   "Thesis independent"),
        ("warn", "SPY corr; $63–67 stop"),
    ]),
    ("P014", "AAPL Long", [
        ("bad",  "EXIT: VIX + 9d window"),
        ("bad",  "Close early: FOMC+window"),
        ("warn", "Consumer sentiment indirect"),
        ("ok",   "Services thesis independent"),
        ("bad",  "STOP ~$264 if SPY $696"),
    ]),
    ("P015", "GOOGL Cont.", [
        ("warn", "May not enter if spike pre-Apr23"),
        ("warn", "FOMC risk post-entry; T=0"),
        ("warn", "Indirect only"),
        ("ok",   "AI/search independent"),
        ("warn", "SPY corr; stop $317"),
    ]),
]

# ── Closed-Trade Context ──────────────────────────────────────────────────────
# (section_label, asset_tag, [(ID, side, open_date, close_date, days, pnl, pnl_cls, exit_reason)])
CLOSED_CONTEXT = [
    ("INTC — prior pipeline history", "INTC", [
        ("P004", "Long", "2026-04-08", "2026-04-19", 11, "+2.09%", "ok",
         "Planned pre-earnings exit — avoided Apr-23 binary. Thesis direction validated. "
         "Entry validated Terafab foundry narrative."),
    ]),
    ("SPY — prior pipeline history", "SPY", [
        ("P005", "Long", "2026-03-28", "2026-04-19", 22, "+1.13%", "ok",
         "Correlation-freed slot after QQQ exit. Time-stop closure pre-FOMC positioning."),
    ]),
]
CLOSED_NOTE = ("GOOGL, AAPL, EWJ: first entries in this pipeline — no prior closed-trade history to reference. "
               "Full history: SignalLedger → PerformanceStats sheet.")

# ── Material Delta box (v2+) — leave DELTA_ITEMS empty for v1 ─────────────────
DELTA_ITEMS = [
    '<span class="pill green">NEW P013</span> <b>INTC Sum +4</b> — V026 residual +13.89% → T=+1 resolved. Entry after Apr-23 earnings beat.',
    '<span class="pill green">NEW P014</span> <b>AAPL Sum +3</b> — V026 residual +4.68% → T=+1 resolved. Immediate entry; hard exit Apr-30.',
    '<span class="pill blue">P015</span> <b>GOOGL Sum +3</b> — T=0 resolved (residual −0.80%). Entry after tonight\'s beat confirm.',
]
DELTA_FOOT = ("Also: PLTR downgraded (residual −35.62% → T=−1 → Sum+2, below threshold) · "
              "MOVE 67.90 + V027 z+1.65 now Grade A fresh (were MISSING in cloud) · "
              "All 12 V026 scores resolved (numpy failure cleared 19:48 UTC+8)")

# ── Overlay Gate ───────────────────────────────────────────────────────────────
# (Sleeve, Asset, Reading, pill_cls, gate_text)
GATE_ROWS = [
    ("Equity (V033)",    "SPY/QQQ",  "ABOVE (~$710 vs est. $650–680)",            "green", "ON"),
    ("Commodity (V034)", "GSCI",     "MISSING — 4th consecutive run",             "red",   "UNCERTAIN / effective OFF"),
    ("Crypto (V035)",    "BTC",      "$76,454 vs est. 10m-SMA ~$80–85K — BELOW", "red",   "OFF"),
    ("Intl Equity",      "EWJ/EFA",  "$90.19 vs est. 10m-SMA ~$78–82 — ABOVE",  "green", "ON"),
]
GATE_NOTE = ("Next read: Apr-30 month-end. Commodity sleeve blocked 4th consecutive run — "
             "Silver Sum+3 and Copper Sum+3 remain gate-blocked.")

# ── Key Variables ──────────────────────────────────────────────────────────────
# (Variable, Reading, Grade, pill_cls, status_text, score_impact)
KEY_VARS = [
    ("VIX",               "19.04",             "B (BNMA)", "yellow", "LIVE (at threshold)",    "R: +0 at 20 boundary; MOVE dominates"),
    ("VIX3M",             "20.51",             "B (BNMA)", "gray",   "STALE Apr-18",            "VIX/VIX3M 0.93 = contango benign"),
    ("MOVE",              "67.90",             "A",        "green",  "LIVE (fresh)",             "R: +1 — low bond vol; was MISSING in cloud"),
    ("HY OAS",            "285 bps",           "B (BNMA)", "green",  "LIVE",                     "R: tight, non-stressed"),
    ("NFCI",              "−0.47",             "A",        "gray",   "STALE Apr-10 (11d)",       "Loose conditions"),
    ("IC z-score (V027)", "+1.65",             "A",        "green",  "LIVE (fresh)",             "R: no notch (z > −1σ); was MISSING in cloud"),
    ("DGS10",             "4.25%",             "A",        "green",  "LIVE",                     "2s10s +0.54% steepening; no inversion drag"),
    ("T10YIE",            "2.36%",             "A",        "green",  "LIVE",                     "Above 2% Fed target; FOMC Apr-28 must navigate"),
    ("DXY",               "98.242",            "A",        "green",  "LIVE",                     "−3.9% from Apr-9 peak; USD structural weakness"),
    ("SPY / QQQ",         "$708.72 / $646.79", "A",        "green",  "LIVE (Apr-21 close)",      "P009 entry $710.14 within 0.2%"),
    ("EWJ",               "$90.19",            "A",        "gray",   "STALE Apr-18 (3d, OK)",    "Trend confirmed by Nikkei +1.21% Apr-21"),
    ("Brent / WTI",       "$90.03 / $86.32",   "A",        "green",  "LIVE",                     "Hormuz premium; P008 stop buffer $1.02"),
    ("Gold",              "$4,808",            "A",        "green",  "LIVE",                     "Sum+2; gate-blocked (commodity sleeve)"),
    ("BTC / ETH",         "$76,454 / $2,313",  "A / B",    "green",  "LIVE / STALE",             "4th test $75K; KelpDAO DeFi tail; sleeve OFF"),
]

# ── Audit Additions ────────────────────────────────────────────────────────────
# (ID, Variable, pill_cls, status_text, dm_pill_cls, dm_text)
AUDIT_ROWS = [
    ("V026", "Residual momentum (FF5 12m) — 12 tickers",
     "green", "ALL 12 LIVE — numpy failure cleared 19:48 UTC+8",
     "green", "YES — INTC T+1 (P013), AAPL T+1 (P014), PLTR T−1 (downgraded), TSLA T−1 confirmed"),
    ("V027", "Intermediary capital z-score",
     "green", "LIVE +1.65 — was MISSING in cloud",
     "green", "YES — R=+1 Grade A confirmed; full sizing per Risk Rules §1.B"),
    ("V028", "Basis-momentum (4w/12w)",
     "yellow","PARTIAL — Brent LIVE; WTI/Gold/Silver/Copper STALE T3 (Apr-17)",
     "gray",  "Brent S+1 confirmed; others scored static slope"),
]

# ── Meta Additions ─────────────────────────────────────────────────────────────
# (ID, Variable, pill_cls, status_text, dm_text)
META_ROWS = [
    ("V029", "BAB (USMV/SPLV)",           "gray", "Not computed", "NO"),
    ("V030", "DealerGamma (Grade B)",      "gray", "Not computed", "NO"),
    ("V031", "GP/A (Gross Profitability)", "gray", "Not computed", "NO"),
    ("V032", "CEI (Composite Issuance)",   "gray", "Not computed", "NO"),
]

# ── Recommendations ────────────────────────────────────────────────────────────
# (asset_html, dir_cls, entry, stop, target, size, catalyst, grade, sleeve)
RECS = [
    ("<b>INTC</b> <span class='pill green'>NEW P013</span>", "green",
     "$68–72 (after Apr-23 beat)", "~$63–67 (2× ATR ~$5)", "$75 / $82", "1.0% (full — V027 OK)",
     "C+1: beat = confirmed; miss = thesis invalidated. Earnings Apr-23 AC.",
     "S+1(A), T+1(A), C+1(A), R+1(A)", "Equity ON"),
    ("<b>AAPL</b> <span class='pill green'>NEW P014</span>", "green",
     "~$271–274 (immediate)", "~$264–267 (2× ATR ~$6.50)", "$280 / $290", "0.75% (corr. haircut vs SPY)",
     "C=0; structural momentum only. <b>Hard exit 2026-04-30</b> before May-1 earnings.",
     "S+1(A), T+1(A), C0, R+1(A)", "Equity ON"),
    ("<b>GOOGL</b> <span class='pill yellow'>P015 contingent</span>", "green",
     "~$333–340 (after Apr-23 beat)", "~$315–320 (2× ATR ~$9)", "$355 / $375", "0.75%",
     "C+1: Apr-23 beat = entry trigger. Do not chase gap; wait for price stability.",
     "S+1(A), T0, C+1(A), R+1(A)", "Equity ON"),
    ("<b>SPY</b> <span class='pill blue'>P009 reconfirmed</span>", "green",
     "$710.14 limit", "$696 (2× ATR ~$14)", "$720 / $730", "1.0% (half — FOMC tail)",
     "C=0; structural S+T+R edge. FOMC Apr-28-29 tail; ceasefire cross-asset risk.",
     "S+1(A), T+1(A), C0, R+1(B)*", "Equity ON"),
    ("<b>EWJ</b> <span class='pill blue'>P010 reconfirmed</span>", "green",
     "~$90.24", "$86.00 (2× ATR ~$4.4)", "$95 / $98", "0.75%",
     "C=0; USD structural weakness + Nikkei trend confirmation.",
     "S+1(A), T+1(A), C0, R+1(A)", "Intl Equity ON"),
]
RECS_BLOCKED = [
    ("<b>Silver</b> <span class='pill red'>P012 gate-blocked</span>", "LONG",
     "—", "—", "—", "Taken=NO",
     "Commodity sleeve UNCERTAIN/OFF — no commodity longs permitted.",
     "S+1, T+1, C0, R+1 (+3)", "Commodity OFF"),
]
RECS_FOOTNOTE = ("*R=+1 via MOVE 67.90 (A, fresh) + V027 z+1.65 (A, fresh) + HY OAS 285 (B) + NFCI −0.47 (A) — Grade A triple confirmed.<br>"
                 "Heat if all fill: P008 0.33% + SPY 1.0% + EWJ 0.75% + AAPL 0.75% + INTC 1.0% + GOOGL 0.75% = <b>4.58%</b> (57% of 8% cap).")

# ── Pre-Entry Checklists ───────────────────────────────────────────────────────
# list of (title, note_html, [(num, item, cls, icon, detail), ...])
CHECKLISTS = [
    ("INTC Long (P013) — entry after Apr-23 AC beat confirmed",
     "⚠ Entry approach: WAIT FOR CONFIRMED BEAT (Apr-24 UTC+8 morning). "
     "Prior P004 closed Apr-19 specifically to avoid this binary — maintain discipline.",
     [(1,"| Sum|≥3 with C scored",                     "ok",  "✅ PASS",         "Sum +4; C+1 (earnings Apr-23 AC pre-scored)"),
      (2,"Invalidation written, concrete, date-bounded","ok",  "✅ PASS",         "Q1 miss / Terafab miss → C=0/−1 → exit; time-stop 2026-06-23"),
      (3,"Correlation gate clean",                      "ok",  "✅ PASS",         "Distinct foundry driver vs SPY/AAPL; equity heat 3.83% under cap"),
      (4,"Per-position ≤2% / heat ≤8%",                "ok",  "✅ PASS",         "1.0%; heat 3.83% with all others"),
      (5,"ATR stop set",                                "ok",  "✅ PASS",         "2× ATR ~$5 below entry; adjust at fill price post-beat"),
      (6,"Catalyst asymmetry stated",                   "ok",  "✅ PASS",         "C+1: beat = thesis confirmed; miss = thesis invalidated. High asymmetry."),
      (7,"Overlay Gate clearance",                      "ok",  "✅ PASS",         "Equity sleeve ON"),
      (8,"Digest clearance",                            "ok",  "✅ PASS",         "P004 INTC closed Apr-19; no INTC POSITION-ALERT")]),
    ("AAPL Long (P014)",
     "",
     [(1,"| Sum|≥3 with C scored",                     "ok",  "✅ PASS",         "Sum +3; C=0 scored"),
      (2,"Invalidation written, concrete, date-bounded","ok",  "✅ PASS",         "Break $264 (2× ATR); SPY $696 break; <b>hard exit 2026-04-30</b>"),
      (3,"Correlation gate clean",                      "ok",  "✅ PASS",         "SPY corr ~0.65; combined equity 1.75%; distinct services/hardware driver"),
      (4,"Per-position ≤2% / heat ≤8%",                "ok",  "✅ PASS",         "0.75%"),
      (5,"ATR stop set",                                "ok",  "✅ PASS",         "~$273 entry; ATR ~$3.25; 2× = $6.50 → stop ~$266.50"),
      (6,"Catalyst asymmetry stated",                   "warn","⚠ PARTIAL",       "C=0; structural momentum only. 8-trading-day window before May-1 binary."),
      (7,"Overlay Gate clearance",                      "ok",  "✅ PASS",         "Equity sleeve ON"),
      (8,"Digest clearance",                            "ok",  "✅ PASS",         "No AAPL POSITION-ALERT")]),
    ("GOOGL Long (P015) — contingent on Apr-23 beat",
     "⚠ T=0 (not +1) — entry is C+1 driven. Do not chase post-earnings gap; "
     "wait for price stability before entering.",
     [(1,"| Sum|≥3 with C scored",                     "ok",  "✅ PASS (cond.)", "Sum +3; C+1 pre-earnings — falls to +2 on miss → no entry"),
      (2,"Invalidation written, concrete, date-bounded","ok",  "✅ PASS",         "Earnings miss → no entry; break 2× ATR from entry; time-stop 2026-05-15"),
      (3,"Correlation gate clean",                      "ok",  "✅ PASS",         "Tech concentration monitored; GOOGL AI-search driver distinct from AAPL/INTC"),
      (4,"Per-position ≤2% / heat ≤8%",                "ok",  "✅ PASS",         "0.75%; total heat 4.58% if all fill"),
      (5,"ATR stop set",                                "ok",  "✅ PASS",         "~$335 entry; ATR ~$9; 2× = $18 → stop ~$317"),
      (6,"Catalyst asymmetry stated",                   "ok",  "✅ PASS",         "88% Q1 beat rate + Mag7 +22.8% bar. Beat = entry confirmed."),
      (7,"Overlay Gate clearance",                      "ok",  "✅ PASS",         "Equity sleeve ON"),
      (8,"Digest clearance",                            "ok",  "✅ PASS",         "No GOOGL POSITION-ALERT")]),
]

# ── Catalyst Calendar ──────────────────────────────────────────────────────────
# (date_html, event_html, assets, pill_cls, pill_text)
CATALYSTS = [
    ("<b>Apr-23 ~01:00</b>", "<b>GOOGL Q1 earnings AC</b>",    "GOOGL, QQQ, NVDA",       "red",    "HIGH — P015 entry trigger"),
    ("<b>Apr-23 AC</b>",     "<b>INTC Q1 earnings</b>",         "INTC, QQQ",              "red",    "HIGH — P013 entry trigger (enter Apr-24)"),
    ("Apr-23 AC",            "AMZN Q1 earnings",                "AMZN, QQQ",              "yellow", "MED — AMZN +2 → potential +3"),
    ("Apr-24",               "UMich final April sentiment",     "SPY, DXY",               "yellow", "MED — prelim 47.6 record low"),
    ("<b>Apr-28–29</b>",     "<b>FOMC</b>",                     "All — SPY P009 primary", "red",    "HIGH — hawkish surprise = exit rule"),
    ("Apr-29",               "META earnings (same day FOMC)",   "META, QQQ",              "yellow", "MED — double-event risk"),
    ("<b>Apr-30</b>",        "<b>AAPL P014 hard time-stop</b>", "AAPL",                   "red",    "HIGH — exit regardless of P&amp;L"),
    ("May-1",                "AAPL Q1 earnings",                "AAPL",                   "gray",   "P014 must be closed before"),
    ("May-12",               "April CPI",                       "All",                    "yellow", "MED — Hormuz inflation follow-through"),
]
CAT_LABELS = ['Apr-23 GOOGL','Apr-23 INTC','Apr-23 AMZN','Apr-24 UMich','Apr-28-29 FOMC','Apr-30 AAPL stop','May-12 CPI']
CAT_DATA   = [2, 2, 1, 1, 2, 2, 1]
CAT_COLORS = ['#f87171','#f87171','#facc15','#facc15','#f87171','#f87171','#facc15']

# ── Near-Misses ────────────────────────────────────────────────────────────────
# (asset_html, sum_text, block_reason, trigger, id)
NEAR_MISSES = [
    ("MU <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "Correlation gate — equity sleeve at capacity during Apr-22–29 earnings+FOMC cluster",
     "Post-FOMC Apr-30+", "N040"),
    ("QQQ", "+3",
     "SPY preferred (correlation-blocked)",
     "Post earnings cluster Apr-30+", "N034"),
    ("NVDA <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "Tech concentration; T=0 (residual −1.00%)",
     "GOOGL beat + V026 residual >+2%", "N041"),
    ("Copper", "+3",
     "Commodity sleeve UNCERTAIN/OFF",
     "GSCI confirmed ON + China PMI >50.5", "N035"),
]

# ── Score chart data ───────────────────────────────────────────────────────────
SCORE_LABELS = ['INTC (P013)','AAPL (P014)','GOOGL (P015)','SPY (P009)','EWJ (P010)']
SCORE_S = [1,1,1,1,1]; SCORE_T = [1,1,0,1,1]; SCORE_C = [1,0,1,0,0]; SCORE_R = [1,1,1,1,1]
NEAR_LABELS = ['MU (N040)','QQQ (N034)','NVDA (N041)','Copper (N035)','Silver (P012)']
NEAR_S = [1,1,1,1,1]; NEAR_T = [1,1,0,1,1]; NEAR_C = [0,0,1,0,0]; NEAR_R = [1,1,1,1,1]

# ── Open Positions ─────────────────────────────────────────────────────────────
# (ID, Asset, Side, Entry, Stop, Live, Buffer, flag_cls, flag_text)
OPEN_POSITIONS = [
    ("P008","CLUSDT (WTI perp)","Short-term Long","$88.250","$85.300","$86.32", "~$1.02","warn","⚠ THIN — Iran binary watch"),
    ("P009","SPY",              "Long",           "$710.14","$696",   "$708.72","$12.72", "ok",  "OK — fill pending"),
    ("P010","EWJ",              "Long",           "~$90.24","$86.00", "$90.19", "~$4.19","ok",  "OK — fill pending"),
]

# ── Data Gap ───────────────────────────────────────────────────────────────────
GAP_DATA = [20, 4, 1]
UPSTREAM = [
    ("ok",  "Local market-brief 2026-04-21 v1 ✅ (A)"),
    ("ok",  "Local news 2026-04-21 ✅ (A)"),
    ("ok",  "Local audit-staging 2026-04-21 ✅ — V026 ALL 12, V027, V028 Brent"),
    ("ok",  "Cloud market-brief (GDrive) ✅ (B)"),
    ("ok",  "Cloud news (GDrive) ✅ (B)"),
    ("bad", "Cloud trade-rec: MISSING (not on Drive)"),
    ("ok",  "framework/Memory.md ✅ (updated 20:20)"),
    ("ok",  "SignalLedger: P010–P015, N040–N041 appended ✅"),
    ("ok",  "AuditAdditionLog: +8 V026/V027/MOVE entries ✅"),
]

# ── Discussion ─────────────────────────────────────────────────────────────────
DISCUSSION = [
    "<b>Why three new promotions today (INTC, AAPL, GOOGL)?</b> The numpy failure that blocked all single-stock T-scores for 3+ consecutive runs was cleared by the preflight at 19:48 UTC+8. This unlocked V026 residual momentum for all 12 tickers. INTC (+13.89%) and AAPL (+4.68%) both clear the +2% threshold for T=+1. GOOGL (−0.80%) resolves to T=0 — Sum+3 is still achieved via C+1 (earnings tonight) + S+1 + R+1. These are not new thesis discoveries; they are thesis confirmations unblocked by infrastructure recovery.",
    "<b>INTC is the highest conviction signal.</b> Sum+4 is rare — only the second time in this pipeline. The thesis is the Terafab foundry ramp (commercial validation, Q1 guidance $11.7–$12.7B). Prior P004 closed at +2.09% after 11 days. Entry AFTER the Apr-23 beat eliminates the pre-earnings binary gap risk while capturing the thesis activation. Do not enter pre-earnings.",
    "<b>AAPL has a hard time fence.</b> The residual momentum edge (+4.68%) and structural S+1 are valid, but C=0 means no catalyst amplification. The 8-day window (Apr-21 to Apr-30) is thin. The must-exit rule before May-1 earnings is non-negotiable — holding into May-1 with C=0 would be an off-methodology decision. If FOMC Apr-28-29 is hawkish and SPY breaks $696, the AAPL stop at ~$264–267 would likely be hit simultaneously.",
    "<b>V027 z+1.65 now Grade A fresh.</b> In the cloud-7pm run, R=+1 was proxy-only (HY OAS + NFCI + VIX). The local run adds MOVE 67.90 (A, fresh) and V027 z+1.65 (A, fresh). R is now backed by three independent Grade A inputs — the most confident R=+1 reading since the pipeline launched. Per Risk Rules §1.B, z > +0.5σ = full inverse-ATR sizing. INTC gets 1.0% (full); SPY stays half-size (FOMC tail, not R-related).",
    "<b>Iran ceasefire binary.</b> The two-week ceasefire expired today (Apr-21 UTC+8). Talks are in Islamabad; Iran is not participating in the US-led round. Hormuz at &lt;10% normal traffic. P008 (CL long, off-methodology) has a $1.02 buffer above the $85.30 stop — thin. The new equity entries have indirect Iran exposure through VIX; their ATR stops should survive a moderate oil move without being directly hit.",
]

# ── Memory Updates / Sources ───────────────────────────────────────────────────
MEMORY_UPDATES = [
    "Memory.md §5: Added INTC P013, AAPL P014, GOOGL P015, MU N040 (near-miss watchlist)",
    "Memory.md §5: GOOGL updated from T-blocked to T=0 resolved (−0.80%); PLTR downgraded to Sum+2",
    "Memory.md §6: Iran ceasefire status updated to EXPIRED Apr-21 UTC+8",
    "SignalLedger: P010 EWJ, P011 Gold (gate-blocked), P012 Silver (gate-blocked), P013 INTC, P014 AAPL, P015 GOOGL, N040 MU, N041 NVDA appended",
    "AuditAdditionLog: 8 entries for V026/V027/MOVE resolution impact",
    "pipeline/.pipeline-status.json: trade-rec updated to OK v2",
]
SOURCES_A = ("market-brief-2026-04-21.md v1 · news-2026-04-21.md · audit-data-staging-2026-04-21.md "
             "(V026 ALL 12, V027 z+1.65, V028 Brent) · framework/{Memory, Risk Rules, Methodology Prompt, Excel-Sync-Protocol}.md")
SOURCES_B = "cloud-market-brief-2026-04-21.md · cloud-news-2026-04-21.md · [cloud-trade-rec MISSING]"


# ══════════════════════════════════════════════════════════════════════════════
# STATIC DATA — update only when CLAUDE.md asset universe changes
# ══════════════════════════════════════════════════════════════════════════════

UNIVERSE = {
    "Equities":    ["INTC","TSM","NVDA","TSLA","AAPL","GOOGL","AMZN","META","PYPL","PLTR","MU","WDC","AVGO","BABA","MSFT"],
    "ETFs":        ["QQQ","SPY","EWJ","EWY"],
    "Commodities": ["Brent","WTI","Gold","Silver","Copper","Palladium","Platinum"],
    "Crypto":      ["BTC","ETH"],
}
UNIVERSE_COLORS = {
    "Equities":    ("rgba(91,155,255,.15)",  "#5b9bff"),
    "ETFs":        ("rgba(74,222,128,.15)",  "#4ade80"),
    "Commodities": ("rgba(250,204,21,.15)",  "#facc15"),
    "Crypto":      ("rgba(248,113,113,.15)", "#f87171"),
}


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTED VALUES
# ══════════════════════════════════════════════════════════════════════════════

_fe_total = sum(r[3] for r in FACTOR_EXPOSURE)
FACTOR_WS = round(sum(r[3] * r[4] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WT = round(sum(r[3] * r[5] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WC = round(sum(r[3] * r[6] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WR = round(sum(r[3] * r[7] for r in FACTOR_EXPOSURE) / _fe_total, 3)


# ══════════════════════════════════════════════════════════════════════════════
# HTML GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def pill(cls, text):
    return f'<span class="pill {cls}">{text}</span>'


def universe_html():
    parts = []
    for cat, tickers in UNIVERSE.items():
        bg, fg = UNIVERSE_COLORS[cat]
        chips = " ".join(
            f'<span style="display:inline-block;margin:2px 3px;padding:2px 8px;border-radius:8px;'
            f'font-size:12px;font-weight:500;background:{bg};color:{fg}">{t}</span>'
            for t in tickers
        )
        parts.append(
            f'<div style="margin-bottom:7px">'
            f'<span style="display:inline-block;min-width:110px;font-size:11px;font-weight:600;'
            f'color:#8a93a6;text-transform:uppercase;letter-spacing:.05em;vertical-align:middle">{cat}</span>'
            f'{chips}</div>'
        )
    return "\n".join(parts)


def freshness_strip_html():
    items = []
    for var, reading, grade, cls, note in FRESHNESS:
        dot = {"green": "●", "blue": "●", "yellow": "◐", "red": "○"}.get(cls, "●")
        dot_color = {"green": "#4ade80", "blue": "#5b9bff", "yellow": "#facc15", "red": "#f87171"}.get(cls, "#8a93a6")
        items.append(
            f'<div style="background:#171a21;border:1px solid #262b35;border-radius:8px;'
            f'padding:8px 10px;min-width:120px;flex:0 0 auto">'
            f'<div style="font-size:11px;color:#8a93a6;text-transform:uppercase;letter-spacing:.04em">{var}</div>'
            f'<div style="font-size:14px;font-weight:600;margin:2px 0">'
            f'<span style="color:{dot_color}">{dot}</span> {reading}'
            f'<span style="font-size:10px;font-weight:400;color:#8a93a6;margin-left:4px">{grade}</span></div>'
            f'<div style="font-size:10px;color:#8a93a6">{note}</div>'
            f'</div>'
        )
    return (
        f'<div style="display:flex;gap:8px;overflow-x:auto;padding:2px 0 10px 0;'
        f'scrollbar-width:thin;scrollbar-color:#262b35 transparent">'
        + "".join(items) + '</div>'
    )


def delta_html():
    if not DELTA_ITEMS:
        return ""
    cols = "".join(f'<div>{item}</div>' for item in DELTA_ITEMS)
    foot = (f'<div style="margin-top:10px;font-size:13px;color:var(--muted)">{DELTA_FOOT}</div>'
            if DELTA_FOOT else "")
    return (f'<div class="delta-box">\n'
            f'<h3>&#9889; Material change vs cloud-7pm v1</h3>\n'
            f'<div class="grid grid-3" style="margin-top:8px">{cols}</div>\n'
            f'{foot}\n</div>')


def gate_html():
    rows = "".join(
        f'<tr><td>{sl}</td><td>{as_}</td><td>{rd}</td><td>{pill(cls, txt)}</td></tr>\n'
        for sl, as_, rd, cls, txt in GATE_ROWS
    )
    return (f'<table>\n<tr><th>Sleeve</th><th>Asset</th><th>vs 10m-SMA</th><th>Gate</th></tr>\n'
            f'{rows}</table>\n'
            f'<div class="mute" style="font-size:12px;margin-top:6px">{GATE_NOTE}</div>')


def vars_html():
    rows = "".join(
        f'<tr><td>{v}</td><td>{r}</td><td>{g}</td><td>{pill(cls, st)}</td><td>{imp}</td></tr>\n'
        for v, r, g, cls, st, imp in KEY_VARS
    )
    return (f'<table>\n<tr><th>Variable</th><th>Reading</th><th>Grade</th>'
            f'<th>Status</th><th>Score Impact</th></tr>\n{rows}</table>')


def audit_html():
    rows = "".join(
        f'<tr><td>{vid}</td><td>{var}</td><td>{pill(scls, st)}</td><td>{pill(dcls, dt)}</td></tr>\n'
        for vid, var, scls, st, dcls, dt in AUDIT_ROWS
    )
    return (f'<table>\n<tr><th>ID</th><th>Variable</th><th>Status</th><th>Decision-Moving?</th></tr>\n'
            f'{rows}</table>')


def v026_table_html():
    rows = ""
    for ticker, resid, t_score, note in V026_RESIDUALS:
        if resid is not None:
            # visual bar: map [-40, +40] → [0, 100]% width; center at 50%
            bar_pct = max(0, min(100, (resid + 40) / 80 * 100))
            bar_color = "#4ade80" if resid > 2 else "#f87171" if resid < -2 else "#facc15"
            resid_html = (
                f'<span style="font-weight:600;color:{bar_color}">{resid:+.2f}%</span>'
                f'<div style="display:inline-block;width:60px;height:6px;background:#262b35;'
                f'border-radius:3px;margin-left:8px;vertical-align:middle">'
                f'<div style="width:{bar_pct:.0f}%;height:100%;background:{bar_color};border-radius:3px"></div></div>'
            )
            t_color = "#4ade80" if t_score == "+1" else "#f87171" if t_score == "-1" else "#facc15"
            t_html = f'<span style="font-weight:600;color:{t_color}">{t_score}</span>'
        else:
            resid_html = '<span style="color:#8a93a6">—</span>'
            t_html = '<span style="color:#8a93a6">—</span>'
        rows += f'<tr><td><b>{ticker}</b></td><td>{resid_html}</td><td>{t_html}</td><td style="font-size:12px;color:#8a93a6">{note}</td></tr>\n'
    return (
        f'<div style="font-size:12px;color:#8a93a6;margin-bottom:6px">'
        f'Threshold: <span style="color:#4ade80">T=+1 if &gt;+2%</span> &nbsp;|&nbsp; '
        f'<span style="color:#facc15">T=0 if within ±2%</span> &nbsp;|&nbsp; '
        f'<span style="color:#f87171">T=−1 if &lt;−2%</span> &nbsp;|&nbsp; '
        f'12-ticker subset (TSM/AVGO/BABA excluded — data N/A)</div>'
        f'<table>\n<tr><th>Ticker</th><th>Residual % (FF5 12m)</th><th>T-Score</th><th>Signal Note</th></tr>\n'
        f'{rows}</table>'
    )


def meta_html():
    rows = "".join(
        f'<tr><td>{vid}</td><td>{var}</td><td>{pill(scls, st)}</td><td>{dm}</td></tr>\n'
        for vid, var, scls, st, dm in META_ROWS
    )
    return (f'<table>\n<tr><th>ID</th><th>Variable</th><th>Status</th><th>Decision-Moving?</th></tr>\n'
            f'{rows}</table>')


def score_charts_html():
    return ('<div class="grid grid-2">\n'
            '<div class="card"><h3 style="margin-top:0">Promoted |Sum| &#8805; 3 &mdash; S/T/C/R breakdown</h3>\n'
            '<div class="chart-wrap"><canvas id="scoreBar"></canvas></div></div>\n'
            '<div class="card"><h3 style="margin-top:0">Near-Misses |Sum| = 3 (blocked)</h3>\n'
            '<div class="chart-wrap"><canvas id="nearMissBar"></canvas></div></div>\n'
            '</div>')


def factor_exposure_html():
    def bar(val, color):
        pct = int(val * 100)
        return (f'<div style="display:flex;align-items:center;gap:8px">'
                f'<div style="flex:1;height:8px;background:#262b35;border-radius:4px">'
                f'<div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div></div>'
                f'<span style="font-size:12px;color:{color};width:36px">{val:.2f}</span></div>')

    # table of individual positions
    pos_rows = ""
    for pid, asset, status, size, S, T, C, R in FACTOR_EXPOSURE:
        pos_rows += (f'<tr>'
                     f'<td>{pid}</td><td>{asset}</td><td style="color:#8a93a6;font-size:12px">{status}</td>'
                     f'<td>{size:.2f}%</td>'
                     f'<td style="color:#4ade80">{S}</td>'
                     f'<td style="color:#5b9bff">{T}</td>'
                     f'<td style="color:#facc15">{C}</td>'
                     f'<td style="color:#a78bfa">{R}</td>'
                     f'</tr>\n')
    # weighted aggregate row
    pos_rows += (f'<tr style="background:#1a1e27;font-weight:600">'
                 f'<td colspan="3">Portfolio weighted avg (size={_fe_total:.2f}% heat)</td>'
                 f'<td></td>'
                 f'<td style="color:#4ade80">{FACTOR_WS:.2f}</td>'
                 f'<td style="color:#5b9bff">{FACTOR_WT:.2f}</td>'
                 f'<td style="color:#facc15">{FACTOR_WC:.2f}</td>'
                 f'<td style="color:#a78bfa">{FACTOR_WR:.2f}</td>'
                 f'</tr>\n')

    # interpretation
    bias = []
    if FACTOR_WS > 0.9: bias.append("signal-heavy (all S=1)")
    if FACTOR_WT > 0.8: bias.append("trend-favorable")
    elif FACTOR_WT < 0.6: bias.append("trend-light")
    if FACTOR_WC < 0.5: bias.append('<span style="color:#facc15">catalyst-light (most C=0)</span>')
    if FACTOR_WR > 0.9: bias.append("strong risk backdrop (R Grade A triple)")
    bias_str = " · ".join(bias) if bias else "balanced"

    # mini factor bar chart (inline, no canvas)
    bars_html = (
        f'<div style="padding:4px 0">'
        f'<div style="margin:6px 0"><span style="display:inline-block;width:80px;font-size:12px;color:#8a93a6">S (Signal)</span>{bar(FACTOR_WS,"#4ade80")}</div>'
        f'<div style="margin:6px 0"><span style="display:inline-block;width:80px;font-size:12px;color:#8a93a6">T (Trend)</span>{bar(FACTOR_WT,"#5b9bff")}</div>'
        f'<div style="margin:6px 0"><span style="display:inline-block;width:80px;font-size:12px;color:#8a93a6">C (Catalyst)</span>{bar(FACTOR_WC,"#facc15")}</div>'
        f'<div style="margin:6px 0"><span style="display:inline-block;width:80px;font-size:12px;color:#8a93a6">R (Risk)</span>{bar(FACTOR_WR,"#a78bfa")}</div>'
        f'</div>'
    )

    return (
        f'<div class="grid grid-2">\n'
        f'<div class="card">\n'
        f'<h3 style="margin-top:0">Factor Tilt (size-weighted)</h3>\n'
        f'{bars_html}'
        f'<div style="font-size:12px;color:#8a93a6;margin-top:8px">Portfolio bias: {bias_str}</div>'
        f'</div>\n'
        f'<div class="card">\n'
        f'<h3 style="margin-top:0">Position Breakdown</h3>\n'
        f'<table style="margin-top:0">\n'
        f'<tr><th>ID</th><th>Asset</th><th>Status</th><th>Size%</th>'
        f'<th style="color:#4ade80">S</th><th style="color:#5b9bff">T</th>'
        f'<th style="color:#facc15">C</th><th style="color:#a78bfa">R</th></tr>\n'
        f'{pos_rows}</table>\n'
        f'</div>\n</div>'
    )


def recs_html():
    header = ('<tr><th>Asset</th><th>Dir</th><th>Entry</th><th>Stop</th><th>Target</th>'
              '<th>Size</th><th>Catalyst</th><th>Grade</th><th>Sleeve</th></tr>')
    rows = ""
    for asset, dir_cls, entry, stop, target, size, catalyst, grade, sleeve in RECS:
        rows += (f'<tr><td>{asset}</td><td>{pill(dir_cls,"LONG")}</td>'
                 f'<td>{entry}</td><td>{stop}</td><td>{target}</td><td>{size}</td>'
                 f'<td style="font-size:12px">{catalyst}</td>'
                 f'<td style="font-size:12px;color:#b5bccc">{grade}</td>'
                 f'<td style="font-size:12px">{sleeve}</td></tr>\n')
    for asset, dir_txt, entry, stop, target, size, catalyst, grade, sleeve in RECS_BLOCKED:
        rows += (f'<tr style="opacity:0.6"><td>{asset}</td><td>{dir_txt}</td>'
                 f'<td>{entry}</td><td>{stop}</td><td>{target}</td><td>{size}</td>'
                 f'<td style="font-size:12px">{catalyst}</td>'
                 f'<td style="font-size:12px;color:#b5bccc">{grade}</td>'
                 f'<td style="font-size:12px">{sleeve}</td></tr>\n')
    return (f'<table>\n{header}\n{rows}</table>\n'
            f'<div class="mute" style="font-size:12px;margin-top:6px">{RECS_FOOTNOTE}</div>')


def signal_age_html():
    rows = ""
    for sid, asset, status, prom, days, expiry, days_rem, urgency in SIGNAL_AGE:
        # progress bar: days_remaining / 90 days max
        bar_pct = min(100, int(days_rem / 90 * 100))
        bar_color = {"ok": "#4ade80", "warn": "#facc15", "bad": "#f87171"}.get(urgency, "#8a93a6")
        countdown = (
            f'<span style="font-weight:600;color:{bar_color}">{days_rem}d</span>'
            f'<div style="display:inline-block;width:70px;height:6px;background:#262b35;'
            f'border-radius:3px;margin-left:8px;vertical-align:middle">'
            f'<div style="width:{bar_pct}%;height:100%;background:{bar_color};border-radius:3px"></div></div>'
        )
        rows += (f'<tr><td>{sid}</td><td><b>{asset}</b></td>'
                 f'<td style="font-size:12px;color:#8a93a6">{status}</td>'
                 f'<td>{prom}</td><td style="color:#8a93a6">{days}d</td>'
                 f'<td>{expiry}</td><td>{countdown}</td></tr>\n')
    return (f'<table>\n'
            f'<tr><th>ID</th><th>Asset</th><th>Status</th><th>Promoted</th>'
            f'<th>Age</th><th>Expiry / Hard Stop</th><th>Days Remaining</th></tr>\n'
            f'{rows}</table>\n'
            f'<div class="mute" style="font-size:12px;margin-top:4px">'
            f'<span style="color:#f87171">■</span> &lt;10d urgent &nbsp;'
            f'<span style="color:#facc15">■</span> 10–19d monitor &nbsp;'
            f'<span style="color:#4ade80">■</span> ≥20d OK</div>')


def checklists_html():
    out = ""
    for title, note, rows in CHECKLISTS:
        out += f'<h3>{title}</h3>\n'
        out += '<table>\n<tr><th>#</th><th>Item</th><th>Status</th><th>Detail</th></tr>\n'
        for num, item, cls, icon, detail in rows:
            out += f'<tr><td>{num}</td><td>{item}</td><td class="{cls}">{icon}</td><td>{detail}</td></tr>\n'
        out += '</table>\n'
        if note:
            out += f'<div class="mute" style="font-size:12px;margin-top:4px">{note}</div>\n'
    return out


def sensitivity_html():
    # header
    hdr_cells = "".join(
        f'<th class="sens-{cls}">{hdr}</th>'
        for hdr, cls in SCENARIOS
    )
    header = f'<tr><th>Position</th>{hdr_cells}</tr>'

    rows = ""
    for sid, asset, impacts in SENSITIVITY:
        cells = ""
        for imp_cls, imp_txt in impacts:
            cell_bg = {"ok": "rgba(74,222,128,.07)", "warn": "rgba(250,204,21,.07)",
                       "bad": "rgba(248,113,113,.09)"}.get(imp_cls, "")
            text_color = {"ok": "#4ade80", "warn": "#facc15", "bad": "#f87171"}.get(imp_cls, "var(--fg)")
            cells += (f'<td style="font-size:12px;background:{cell_bg};color:{text_color}">'
                      f'{imp_txt}</td>')
        rows += f'<tr><td><b>{sid}</b> <span style="color:#8a93a6;font-size:12px">{asset}</span></td>{cells}</tr>\n'

    return (f'<div style="overflow-x:auto">\n'
            f'<table style="min-width:800px">\n{header}\n{rows}</table>\n</div>\n'
            f'<div class="mute" style="font-size:12px;margin-top:4px">'
            f'Read: <span style="color:#4ade80">■ neutral/positive</span> &nbsp;'
            f'<span style="color:#facc15">■ monitor / indirect risk</span> &nbsp;'
            f'<span style="color:#f87171">■ direct stop/exit risk</span></div>')


def catalyst_table_html():
    rows = "".join(
        f'<tr><td>{dt}</td><td>{ev}</td><td>{assets}</td><td>{pill(cls, ptxt)}</td></tr>\n'
        for dt, ev, assets, cls, ptxt in CATALYSTS
    )
    return (f'<div class="chart-wrap" style="height:190px"><canvas id="catCal"></canvas></div>\n'
            f'<table style="margin-top:10px">\n'
            f'<tr><th>Date</th><th>Event</th><th>Assets</th><th>Priority</th></tr>\n'
            f'{rows}</table>')


def closed_context_html():
    out = ""
    for section_label, asset_tag, trades in CLOSED_CONTEXT:
        out += f'<h3>{section_label}</h3>\n'
        if not trades:
            out += f'<div class="mute" style="font-size:13px">No prior closed trades in pipeline for {asset_tag}.</div>\n'
            continue
        out += ('<table>\n<tr><th>ID</th><th>Side</th><th>Opened</th><th>Closed</th>'
                '<th>Hold</th><th>P&amp;L</th><th>Exit Reason</th></tr>\n')
        for tid, side, opened, closed, days, pnl, pnl_cls, reason in trades:
            out += (f'<tr><td>{tid}</td><td>{side}</td><td>{opened}</td><td>{closed}</td>'
                    f'<td>{days}d</td><td class="{pnl_cls}"><b>{pnl}</b></td>'
                    f'<td style="font-size:12px">{reason}</td></tr>\n')
        out += '</table>\n'
    if CLOSED_NOTE:
        out += f'<div class="mute" style="font-size:12px;margin-top:6px">{CLOSED_NOTE}</div>\n'
    return out


def near_miss_table_html():
    rows = "".join(
        f'<tr><td>{asset}</td>'
        f'<td><span style="color:var(--accent);font-weight:bold">{sv}</span></td>'
        f'<td style="font-size:12px">{blk}</td>'
        f'<td style="font-size:12px">{trig}</td>'
        f'<td>{nid}</td></tr>\n'
        for asset, sv, blk, trig, nid in NEAR_MISSES
    )
    return (f'<table>\n<tr><th>Asset</th><th>Sum</th><th>Block Reason</th>'
            f'<th>Trigger to Promote</th><th>ID</th></tr>\n{rows}</table>')


def positions_html():
    rows = "".join(
        f'<tr><td>{pid}</td><td>{asset}</td><td>{side}</td>'
        f'<td>{entry}</td><td>{stop}</td><td>{live}</td><td>{buf}</td>'
        f'<td class="{fcls}">{ftxt}</td></tr>\n'
        for pid, asset, side, entry, stop, live, buf, fcls, ftxt in OPEN_POSITIONS
    )
    return (f'<table>\n<tr><th>ID</th><th>Asset</th><th>Side</th>'
            f'<th>Entry</th><th>Stop</th><th>Live</th><th>Buffer</th><th>Flag</th></tr>\n'
            f'{rows}</table>')


def gap_html():
    ul = "".join(f'<li class="{cls}">{txt}</li>' for cls, txt in UPSTREAM)
    return (f'<div class="grid grid-2">\n'
            f'<div class="card"><h3 style="margin-top:0">Grade A Coverage</h3>'
            f'<div class="chart-wrap"><canvas id="gapDoughnut"></canvas></div></div>\n'
            f'<div class="card"><h3 style="margin-top:0">Upstream Artifact Coverage</h3>'
            f'<ul>{ul}</ul></div>\n</div>')


def discussion_html():
    return '<div class="card">' + "".join(f'<p>{p}</p>' for p in DISCUSSION) + '</div>'


def memory_html():
    return '<ul>' + "".join(f'<li>{u}</li>' for u in MEMORY_UPDATES) + '</ul>'


def chartjs_html():
    def ja(lst):   return "[" + ",".join(str(x) for x in lst) + "]"
    def js(lst):   return "[" + ",".join(f"'{x}'" for x in lst) + "]"
    def jq(lst):   return "[" + ",".join(f'"{x}"' for x in lst) + "]"

    return f'''<script>
const cfg = {{
  indexAxis:'y', responsive:true, maintainAspectRatio:false,
  plugins:{{legend:{{labels:{{color:'#e5e9f0'}}}}}},
  scales:{{x:{{ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}}}},
           y:{{ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}}}
}};

new Chart(document.getElementById('scoreBar'),{{
  type:'bar',
  data:{{labels:{js(SCORE_LABELS)},datasets:[
    {{label:'S',data:{ja(SCORE_S)},backgroundColor:'#4ade80'}},
    {{label:'T',data:{ja(SCORE_T)},backgroundColor:'#5b9bff'}},
    {{label:'C',data:{ja(SCORE_C)},backgroundColor:'#facc15'}},
    {{label:'R',data:{ja(SCORE_R)},backgroundColor:'#a78bfa'}}]}},
  options:{{...cfg,scales:{{...cfg.scales,
    x:{{...cfg.scales.x,stacked:true,min:0,max:4}},
    y:{{...cfg.scales.y,stacked:true}}}}}}
}});

new Chart(document.getElementById('nearMissBar'),{{
  type:'bar',
  data:{{labels:{js(NEAR_LABELS)},datasets:[
    {{label:'S',data:{ja(NEAR_S)},backgroundColor:'#4ade80'}},
    {{label:'T',data:{ja(NEAR_T)},backgroundColor:'#5b9bff'}},
    {{label:'C',data:{ja(NEAR_C)},backgroundColor:'#facc15'}},
    {{label:'R',data:{ja(NEAR_R)},backgroundColor:'#a78bfa'}}]}},
  options:{{...cfg,scales:{{...cfg.scales,
    x:{{...cfg.scales.x,stacked:true,min:0,max:4}},
    y:{{...cfg.scales.y,stacked:true}}}}}}
}});

new Chart(document.getElementById('catCal'),{{
  type:'bar',
  data:{{labels:{js(CAT_LABELS)},datasets:[{{
    label:'Priority (1=MED 2=HIGH 3=CRITICAL)',
    data:{ja(CAT_DATA)},
    backgroundColor:{jq(CAT_COLORS)}}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}}}},
    scales:{{x:{{ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}}}},
             y:{{ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}},min:0,max:3}}}}}}
}});

new Chart(document.getElementById('gapDoughnut'),{{
  type:'doughnut',
  data:{{labels:['Grade A LIVE','Grade A STALE','Grade A MISSING'],
        datasets:[{{data:{ja(GAP_DATA)},
          backgroundColor:['#4ade80','#facc15','#f87171'],
          borderColor:'#171a21',borderWidth:2}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{labels:{{color:'#e5e9f0'}}}}}}}}
}});
</script>'''


# ══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE
# ══════════════════════════════════════════════════════════════════════════════

out_path = Path(f"{TODAY}/report-{TODAY}-trade-rec.html")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trade Rec &mdash; {TODAY} {VERSION}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root {{--bg:#0f1115;--card:#171a21;--muted:#8a93a6;--fg:#e5e9f0;--accent:#5b9bff;--green:#4ade80;--red:#f87171;--yellow:#facc15;--border:#262b35;}}
*{{box-sizing:border-box}} body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.5}}
.container{{max-width:1180px;margin:0 auto;padding:32px 24px}}
h1{{font-size:26px;margin:0 0 4px}}
h2{{font-size:18px;margin:28px 0 10px;color:var(--accent);border-bottom:1px solid var(--border);padding-bottom:6px}}
h3{{font-size:15px;margin:18px 0 8px;color:#b5bccc}}
.sub{{color:var(--muted);font-size:13px;margin-bottom:14px}}
.grid{{display:grid;gap:12px}} .grid-2{{grid-template-columns:1fr 1fr}} .grid-3{{grid-template-columns:1fr 1fr 1fr}} .grid-4{{grid-template-columns:repeat(4,1fr)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 16px}}
.card .label{{color:var(--muted);font-size:12px;letter-spacing:.04em;text-transform:uppercase}}
.card .val{{font-size:20px;margin-top:4px}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px}}
th,td{{padding:8px 10px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}}
th{{color:var(--muted);font-weight:500;background:#12151c}}
tr:hover td{{background:#1a1e27}}
.pill{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:500}}
.pill.green{{background:rgba(74,222,128,.15);color:var(--green)}}
.pill.red{{background:rgba(248,113,113,.15);color:var(--red)}}
.pill.yellow{{background:rgba(250,204,21,.15);color:var(--yellow)}}
.pill.blue{{background:rgba(91,155,255,.15);color:var(--accent)}}
.pill.gray{{background:#262b35;color:var(--muted)}}
.pill.purple{{background:rgba(167,139,250,.15);color:#a78bfa}}
.chart-wrap{{position:relative;height:260px}}
.ok{{color:var(--green)}} .warn{{color:var(--yellow)}} .bad{{color:var(--red)}} .mute{{color:var(--muted)}}
.footer{{color:var(--muted);font-size:12px;margin-top:24px;border-top:1px solid var(--border);padding-top:12px}}
ul{{margin:6px 0;padding-left:20px}} li{{margin:3px 0}}
.delta-box{{background:#0d1a2e;border:1px solid #1f6feb;border-radius:8px;padding:14px 18px;margin-bottom:18px}}
.delta-box h3{{color:#79c0ff;margin-top:0}}
.universe-box{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 16px;margin-bottom:6px}}
.sens-ok{{color:var(--green)}} .sens-warn{{color:var(--yellow)}} .sens-bad{{color:var(--red)}}
</style>
</head>
<body>
<div class="container">

<h1>Trade Recommendation &mdash; {TODAY} <span class="pill blue">{VERSION}</span></h1>
<div class="sub">Generated {GEN_TIME} &mdash; production run. {SUPERSEDES}Status: <span class="{STATUS_CLS}">{STATUS_TXT}</span> &mdash; Grade A MISSING: {MISS_COUNT}. &nbsp; V026 {V026_ST} &nbsp;&middot;&nbsp; V027 {V027_ST} &nbsp;&middot;&nbsp; MOVE {MOVE_ST}</div>

<h2>Data Freshness</h2>
{freshness_strip_html()}

<h2>Asset Universe</h2>
<div class="universe-box">
{universe_html()}
</div>

{delta_html()}

<h2>Executive Summary</h2>
<div class="grid grid-4">
  <div class="card"><div class="label">{EXEC_PROMOTED[0]}</div><div class="val {EXEC_PROMOTED[2]}">{EXEC_PROMOTED[1]}</div><div class="mute" style="font-size:12px;margin-top:4px">{EXEC_PROMOTED[3]}</div></div>
  <div class="card"><div class="label">{EXEC_NEARMISS[0]}</div><div class="val {EXEC_NEARMISS[2]}">{EXEC_NEARMISS[1]}</div><div class="mute" style="font-size:12px;margin-top:4px">{EXEC_NEARMISS[3]}</div></div>
  <div class="card"><div class="label">{EXEC_REGIME[0]}</div><div class="val">{EXEC_REGIME[1]}</div><div class="mute" style="font-size:12px;margin-top:4px">{EXEC_REGIME[3]}</div></div>
  <div class="card"><div class="label">{EXEC_HEAT[0]}</div><div class="val">{EXEC_HEAT[1]}</div><div class="mute" style="font-size:12px;margin-top:4px">{EXEC_HEAT[3]}</div></div>
</div>

<h2>Overlay Gate &mdash; Faber TAA (C009)</h2>
{gate_html()}

<h2>Data Collected &mdash; Key Variables</h2>
{vars_html()}

<h3>Audit Additions (2026-04-14 binding, 2026-10-14 review)</h3>
{audit_html()}

<h3>V026 Residual Momentum &mdash; Full Equity Universe</h3>
{v026_table_html()}

<h3>Meta Additions (2026-04-18 binding)</h3>
{meta_html()}

<h2>Score Stacking &mdash; Top Theses</h2>
{score_charts_html()}

<h2>Factor Exposure Aggregate</h2>
{factor_exposure_html()}

<h2>Recommendations</h2>
{recs_html()}

<h2>Signal Age &amp; Time-Decay</h2>
{signal_age_html()}

<h2>Pre-Entry Checklists</h2>
{checklists_html()}

<h2>Regime Sensitivity &mdash; Stress Test</h2>
{sensitivity_html()}

<h2>Catalyst Calendar (rolling 2 weeks)</h2>
{catalyst_table_html()}

<h2>Closed-Trade Context &mdash; Analyst Reference</h2>
{closed_context_html()}

<h2>Near-Misses</h2>
{near_miss_table_html()}

<h2>Open Positions (all)</h2>
{positions_html()}

<h2>Data Gap Closure</h2>
{gap_html()}

<h2>Discussion</h2>
{discussion_html()}

<h2>Memory Updates Applied</h2>
{memory_html()}

<div class="footer">
Sources (local A): {SOURCES_A}<br>
Sources (cloud B): {SOURCES_B}<br>
{VERSION} Authoritative &mdash; generated {GEN_TIME}
</div>
</div>

{chartjs_html()}
</body>
</html>"""

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")
print(f"HTML written: {out_path}")
