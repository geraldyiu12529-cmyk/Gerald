"""Canonical HTML generator for trade-rec reports.
   Update the PER-RUN DATA section below for each new date, then run:
       python scripts/gen_trade_rec_html.py
"""
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# PER-RUN DATA — update these for every date
# ══════════════════════════════════════════════════════════════════════════════

TODAY      = "2026-04-22"
VERSION    = "v1 Local"
GEN_TIME   = "2026-04-22 20:30 UTC+8"
SUPERSEDES = "Local primary — cloud files absent from Drive at run time. "
STATUS_CLS = "ok"
STATUS_TXT = "OK"
MISS_COUNT = "0 (T3 fallbacks applied)"
V026_ST    = "ALL 12 LIVE \u2713"
V027_ST    = "z+1.65 \u2713"
MOVE_ST    = "STALE Apr-21"

# Executive summary cards: (label, val_text, val_css_class, sub_text)
# val_css_class: "ok" / "warn" / "bad" / ""
EXEC_PROMOTED = ("Promoted This Run",   "1 signal",  "ok",   "Brent P016 Long \u2014 commodity sleeve first ON this cycle")
EXEC_NEARMISS = ("Near-Miss / Blocked", "5 + 1",     "warn", "WTI, Silver, Copper, WDC, NVDA near-miss \u00b7 BTC gate-blocked")
EXEC_REGIME   = ("Regime",              "Risk-On / Geo-Binary", "", "Ceasefire EXTENDED \u00b7 Hormuz <10% \u00b7 Blockade intact")
EXEC_HEAT     = ("Heat (open+pending)", "~2.6%",     "",     "P009 SPY 1.86% open + P016 Brent 0.75% pending \u00b7 8% cap")

# ── Data Freshness Strip ───────────────────────────────────────────────────────
# (variable, reading, grade, pill_cls, age_note)
# pill_cls: "green"=LIVE A, "blue"=LIVE B, "yellow"=STALE, "red"=MISSING
FRESHNESS = [
    ("V026",      "12/12",    "A", "green",  "Apr-22 clean"),
    ("V027",      "+1.65",    "A", "green",  "fresh Apr-22"),
    ("V028",      "1/5 fresh","A", "yellow", "Brent T1; WTI/Gold/Ag/Cu T3 stale Apr-17"),
    ("Brent/WTI", "$94/$90",  "A", "green",  "Apr-22 staging (+6-9%)"),
    ("GSG/GSCI",  "31.75",    "A", "green",  "Apr-22 CONFIRMED ON"),
    ("SPY/QQQ",   "~$705/640","B", "blue",   "Apr-21 close"),
    ("EWJ",       "$90.19",   "B", "blue",   "Apr-22 brief"),
    ("DXY",       "98.242",   "A", "green",  "Apr-21"),
    ("DGS10",     "4.25%",    "A", "yellow", "1d stale Apr-21"),
    ("HY OAS",    "285bp",    "B", "yellow", "stale Apr-19"),
    ("NFCI",      "-0.47",    "A", "yellow", "12d stale Apr-10"),
    ("VIX",       "19.04",    "B", "blue",   "Apr-21"),
    ("MOVE",      "STALE",    "A", "yellow", "Apr-21 last; 67.90"),
    ("BTC",       "$76,000",  "B", "blue",   "Apr-22 ~4th test $75k"),
]

# ── V026 Residual Momentum (all tracked tickers) ──────────────────────────────
# (ticker, residual_pct_or_None, t_score, signal_note)
V026_RESIDUALS = [
    ("MU",    +15.63, "+1", "N040 near-miss — correlation gate (equity cluster Apr-22-30)"),
    ("INTC",  +13.89, "+1", "P013 OPEN — entry trigger Apr-23 AC beat"),
    ("WDC",   None,   "+1", "N045 near-miss — C=0 no near-term catalyst"),
    ("AAPL",  +4.68,  "+1", "P014 DEFERRED — price $266.17 below $271-274 entry zone"),
    ("AMZN",  None,   "0",  "Sum+2; timing Apr-29 earnings"),
    ("MSFT",  None,   "0",  "not individually scored this run"),
    ("META",  None,   "0",  "Sum+2; timing Apr-29 same-day FOMC"),
    ("PYPL",  None,   "0",  "not individually scored this run"),
    ("NVDA",  -1.00,  "0",  "N046 near-miss — residual -1.00% T=0; tech concentration"),
    ("GOOGL", -0.80,  "0",  "P015 CONTINGENT — earnings Apr-29 AC; entry Apr-30 morning"),
    ("TSLA",  -9.12,  "-1", "confirmed no-trade; earnings tonight"),
    ("PLTR",  -35.62, "-1", "Sum+2 only; factor crowding confirmed"),
    ("TSM",   None,   "—",  "not computed (data N/A this run)"),
    ("AVGO",  None,   "—",  "not computed (data N/A this run)"),
    ("BABA",  None,   "—",  "not computed (data N/A this run)"),
]

# ── Signal Age / Time-Decay ───────────────────────────────────────────────────
# (ID, asset, status, promoted_date, days_held, expiry_date, days_remaining, urgency_cls)
# urgency_cls: "ok" >=20d / "warn" 10-19d / "bad" <10d
SIGNAL_AGE = [
    ("P009", "SPY",    "OPEN — filled Apr-21",         "2026-04-20",  2, "2026-05-13", 21, "ok"),
    ("P010", "EWJ",    "OPEN — filled Apr-21",         "2026-04-21",  1, "2026-06-30", 69, "ok"),
    ("P016", "Brent",  "PENDING — Gerald execution",   "2026-04-22",  0, "2026-05-22", 30, "ok"),
    ("P013", "INTC",   "Awaiting Apr-23 AC beat",      "2026-04-21",  1, "2026-06-23", 62, "ok"),
    ("P014", "AAPL",   "DEFERRED — below entry zone",  "2026-04-21",  1, "2026-04-30",  8, "bad"),
    ("P015", "GOOGL",  "Contingent — entry Apr-30",    "2026-04-21",  1, "2026-05-15", 23, "ok"),
]

# ── Factor Exposure Aggregate ─────────────────────────────────────────────────
# (ID, asset, status, size_pct, S, T, C, R)
FACTOR_EXPOSURE = [
    ("P009", "SPY",    "Open",              1.00, 1, 1, 0, 1),
    ("P010", "EWJ",    "Open",              0.75, 1, 1, 0, 1),
    ("P016", "Brent",  "Pending (0.75%)",   0.75, 1, 1, 0, 1),
    ("P013", "INTC",   "Awaiting beat",     1.00, 1, 1, 1, 1),
    ("P014", "AAPL",   "Deferred",          0.75, 1, 1, 0, 1),
    ("P015", "GOOGL",  "Contingent",        0.75, 1, 0, 1, 1),
]

# ── Regime Sensitivity Table ──────────────────────────────────────────────────
# Each scenario column: (header_text, header_cls)
SCENARIOS = [
    ("VIX -> 28",          "warn"),
    ("FOMC +50bp",         "bad"),
    ("Iran Deal -10%",     "bad"),
    ("Iran Esc. +15%",     "ok"),
    ("SPY -5%",            "bad"),
]
# (ID, asset, [(impact_cls, short_label), ...])  — one tuple per SCENARIO column (same order)
SENSITIVITY = [
    ("P009", "SPY Long", [
        ("bad",  "EXIT: VIX > 25"),
        ("bad",  "EXIT: primary risk"),
        ("warn", "Oil shock spillover"),
        ("ok",   "Risk-on boost"),
        ("bad",  "STOP $696 in range ~$9 away"),
    ]),
    ("P010", "EWJ Long", [
        ("warn", "Risk-off; BOJ caution"),
        ("bad",  "USD up JPY weak -> EWJ down"),
        ("warn", "Global risk-off minor"),
        ("ok",   "Risk-on; Nikkei record"),
        ("bad",  "High SPY corr."),
    ]),
    ("P016", "Brent Long", [
        ("warn", "Indirect; VIX != oil"),
        ("warn", "USD up -> WTI soft pressure"),
        ("bad",  "THESIS INVALIDATED: deal = -10-15%"),
        ("ok",   "Thesis confirmed: supply tighter"),
        ("warn", "Risk-off corr; stop $90.50 OK"),
    ]),
    ("P013", "INTC Await", [
        ("warn", "Tech selloff; stop OK"),
        ("warn", "Sector rotation risk"),
        ("warn", "Indirect only"),
        ("ok",   "Foundry thesis independent"),
        ("warn", "SPY corr; $63-67 stop"),
    ]),
    ("P015", "GOOGL Cont.", [
        ("warn", "May not enter if VIX spike"),
        ("warn", "FOMC risk post-entry"),
        ("warn", "Indirect only"),
        ("ok",   "AI/search independent"),
        ("warn", "SPY corr; stop ~$317"),
    ]),
]

# ── Closed-Trade Context ──────────────────────────────────────────────────────
# (section_label, asset_tag, [(ID, side, open_date, close_date, days, pnl, pnl_cls, exit_reason)])
CLOSED_CONTEXT = [
    ("INTC — prior pipeline history", "INTC", [
        ("P004", "Long", "2026-04-08", "2026-04-19", 11, "+2.09%", "ok",
         "Planned pre-earnings exit — avoided Apr-23 binary. Thesis direction validated. Re-entering P013 after beat."),
    ]),
    ("Commodity sleeve — prior closed", "Brent/WTI", [
        ("P008", "Long (off-meth)", "2026-04-20", "2026-04-21", 1, "+0.19%", "ok",
         "Off-methodology WTI long, closed Apr-21 after P009/P010 opened. Tactical; not scored. "
         "Brent P016 is the first methodology-promoted commodity long."),
    ]),
]
CLOSED_NOTE = ("SPY, EWJ, Brent: first methodology entries for these assets — no prior closed history. "
               "Full history: SignalLedger -> PerformanceStats sheet.")

# ── Material Delta box (v2+) — leave DELTA_ITEMS empty for v1 ─────────────────
DELTA_ITEMS = [
    '<span class="pill green">NEW P016</span> <b>Brent Long Sum +3</b> — commodity sleeve CONFIRMED ON (GSG 31.75 > 10m-SMA 25.35). First commodity promotion this cycle. Entry $94.00-94.50, stop $90.50, size 0.75%.',
    '<span class="pill yellow">P015 DATE CORRECTED</span> <b>GOOGL earnings Apr-29 AC</b> (not Apr-22/23). Entry trigger shifts to Apr-30 morning. P015 contingent status unchanged.',
    '<span class="pill blue">P014 AAPL DEFERRED</span> Price $266.17 below entry zone $271-274. Do not enter below $268. Hard time-stop Apr-30 still binding.',
]
DELTA_FOOT = ("Also: BTC Sum+3 gate-blocked (crypto sleeve OFF, BTC $76k < $91.5k 10m-SMA) logged as P017 Taken=NO. "
              "WTI/Silver/Copper near-miss — correlation-gated behind Brent (sector cap 25%). "
              "V026 clean 12/12 (no numpy fail). V027 z+1.65 capital expansion = full sizing.")

# ── Overlay Gate ───────────────────────────────────────────────────────────────
# (Sleeve, Asset, Reading, pill_cls, gate_text)
GATE_ROWS = [
    ("Equity (V033)",    "SPY/QQQ",  "ABOVE (~$705/$640 vs est. 10m-SMA $650-680)",           "green", "ON"),
    ("Commodity (V034)", "GSG",      "31.75 vs 10m-SMA 25.35 — ABOVE (CONFIRMED ON Apr-22)",  "green", "ON -- FIRST TIME THIS CYCLE"),
    ("Crypto (V035)",    "BTC",      "$76,000 vs est. 10m-SMA ~$91.5k -- BELOW",              "red",   "OFF"),
    ("Intl Equity",      "EWJ/EFA",  "$90.19 vs est. 10m-SMA ~$78-82 -- ABOVE",              "green", "ON"),
]
GATE_NOTE = ("Next read: May-01 Faber monthly review. Commodity sleeve CONFIRMED ON for first time this cycle "
             "-- Brent promoted as primary. Silver/WTI/Copper correlation-gated behind Brent. "
             "Crypto sleeve OFF: BTC needs >$91.5k at Apr-30 close (large gap).")

# ── Key Variables ──────────────────────────────────────────────────────────────
# (Variable, Reading, Grade, pill_cls, status_text, score_impact)
KEY_VARS = [
    ("VIX",               "19.04",             "B (BNMA)", "yellow", "STALE Apr-21",            "R: borderline at 20 threshold; benign"),
    ("VIX3M",             "20.51",             "B (BNMA)", "gray",   "STALE Apr-18",            "VIX/VIX3M contango; no inversion stress"),
    ("MOVE",              "67.90",             "A",        "yellow", "STALE Apr-21",             "R: +1 -- low bond vol; below 80 threshold"),
    ("HY OAS",            "285 bps",           "B (BNMA)", "yellow", "STALE Apr-19",             "R: tight; non-stressed backdrop"),
    ("NFCI",              "-0.47",             "A",        "gray",   "STALE Apr-10 (12d)",       "Loose conditions persisting"),
    ("IC z-score (V027)", "+1.65",             "A",        "green",  "LIVE (Apr-22 fresh)",      "R: capital expansion z>+0.5 = full sizing per §1.B"),
    ("DGS10",             "4.25%",             "A",        "yellow", "STALE 1d (Apr-21)",        "2s10s steepening; no inversion drag"),
    ("T10YIE",            "2.36%",             "A",        "yellow", "STALE 1d (Apr-21)",        "Above 2% target; FOMC Apr-28 navigate"),
    ("DXY",               "98.242",            "A",        "green",  "LIVE (Apr-21)",            "-3.9% from Apr-9 peak; USD structural weakness; Brent S+1"),
    ("SPY / QQQ",         "~$705 / $640",      "B",        "blue",   "Apr-21 close (1d)",        "P009 entry $708.95; ~$4 underwater; stop $696 buffer $9"),
    ("EWJ",               "$90.19",            "A",        "blue",   "Apr-22 brief",             "P010 entry $88.30; +$1.89 unrealized; Nikkei record 59,585"),
    ("Brent / WTI",       "$94.19 / $90.16",   "A",        "green",  "LIVE Apr-22 (+6-9%)",      "P016 entry zone $94-94.50; backwardation+steepening; Hormuz"),
    ("GSG (GSCI proxy)",  "31.75",             "A",        "green",  "LIVE Apr-22 (CONFIRMED ON)","V034 gate: 31.75 vs 10m-SMA 25.35 (+24.8%); sleeve ON"),
    ("BTC",               "~$76,000",          "B",        "blue",   "Apr-22 approx.",           "4th test $75k; ETF +$412M Apr-21; sleeve OFF; crypto gate"),
]

# ── Audit Additions ────────────────────────────────────────────────────────────
# (ID, Variable, pill_cls, status_text, dm_pill_cls, dm_text)
AUDIT_ROWS = [
    ("V026", "Residual momentum (FF5 12m) -- 12 tickers",
     "green", "ALL 12 LIVE (no numpy failure Apr-22)",
     "green", "YES -- TSLA/PLTR T=-1 via residual-over-raw; INTC/AAPL/MU/WDC T=+1; NVDA/GOOGL T=0"),
    ("V027", "Intermediary capital z-score",
     "green", "LIVE +1.65 (Apr-22 fresh)",
     "green", "YES -- R=+1 Grade A; capital expansion regime; full sizing authorized (§1.B); overridden to 0.75% for P016 binary-downside"),
    ("V028", "Basis-momentum (4w/12w)",
     "yellow","PARTIAL -- Brent LIVE T1 (Apr-22); WTI/Gold/Silver/Copper T3 STALE Apr-17 (5d limit)",
     "yellow","Brent S+1 CONFIRMED (backwardation+13.95, steepening); others near-miss scored static slope; infrastructure persistent failure action-logged"),
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
    ("<b>Brent</b> <span class='pill green'>NEW P016</span>", "green",
     "$94.00-94.50 (at-market/limit; last known $94.19)", "$90.50 (2x ATR ~$3.7)", "$98 / $102", "0.75% (corr+binary haircut)",
     "C=0; structural: Hormuz blockade + backwardation steepening + DXY weak. Iran deal = invalidation.",
     "S+1(A), T+1(A), C0, R+1(A)", "Commodity ON -- first cycle"),
]
# carry-over pending (not new promotions today)
RECS_CARRY = [
    ("<b>SPY</b> P009 OPEN", "$708.95 avg (filled)", "$696", "~$720/$730", "1.0% open", "C=0; stop $696 ~$9 buffer"),
    ("<b>EWJ</b> P010 OPEN", "$88.30 avg (filled)",  "$86.00", "~$95/$98", "0.75% open", "C=0; Nikkei record Apr-22 +2.1% unrealized"),
    ("<b>INTC</b> P013 await", "$68-72 (after Apr-23 beat)", "~$63-67", "$75/$82", "1.0% planned", "C+1: Apr-23 AC earnings trigger"),
    ("<b>AAPL</b> P014 deferred", "DEFERRED ($266 < $271-274 zone)", "~$264-267", "$280/$290", "0.75% if entry", "Hard exit Apr-30"),
    ("<b>GOOGL</b> P015 contingent", "~$333-340 after Apr-29 beat", "~$317", "$355/$375", "0.75% planned", "C+1: Apr-29 AC; entry Apr-30 morning"),
]
RECS_BLOCKED = [
    ("<b>BTC</b> <span class='pill red'>P017 gate-blocked</span>", "LONG",
     "--", "--", "--", "Taken=NO",
     "Crypto sleeve OFF (BTC $76k < $91.5k 10m-SMA). Sum+3 (S+1/T+1/C+1/R0) blocked.",
     "S+1, T+1, C+1, R0 (+3)", "Crypto OFF"),
    ("<b>WTI</b> <span class='pill yellow'>N042 near-miss</span>", "LONG",
     "--", "--", "--", "Taken=NO",
     "Correlation-gated behind Brent. V028 T3 STALE (Apr-17). Basis-mom flat divergence.",
     "S+1, T+1, C0, R+1 (+3)", "Commodity ON (near-miss)"),
    ("<b>Silver</b> <span class='pill yellow'>N043 near-miss</span>", "LONG",
     "--", "--", "--", "Taken=NO",
     "Gate-UNBLOCKED but correlation-gated behind Brent (sector cap 25%). Promote if Brent fills + room.",
     "S+1, T+1, C0, R+1 (+3)", "Commodity ON (near-miss)"),
]
RECS_FOOTNOTE = ("R=+1 via V027 z+1.65 (A) + HY OAS 285bp (B) + NFCI -0.47 (A) + VIX 19.04 (B) -- Grade A double confirmed.<br>"
                 "Heat with open+pending: P009 1.0% + P010 0.75% + P016 0.75% (pending) = 2.6% (32% of 8% cap). "
                 "If P013+P014+P015 all fill: +2.5% additional = 5.1% total (within cap).")

# ── Pre-Entry Checklists ───────────────────────────────────────────────────────
# list of (title, note_html, [(num, item, cls, icon, detail), ...])
CHECKLISTS = [
    ("Brent Long (P016) -- New promotion today",
     "Commodity sleeve CONFIRMED ON for first time this cycle. "
     "Size haircut to 0.75% acknowledges Iran ceasefire binary + TSLA earnings cross-asset risk + FOMC Apr-28 tail.",
     [(1,"|Sum|>=3 with C scored",                      "ok",   "PASS",     "Sum +3 (S+1/T+1/C0/R+1); C explicitly scored at 0 (ceasefire binary symmetric)"),
      (2,"Invalidation written, concrete, date-bounded", "ok",   "PASS",     "Iran deal -> Brent <$88; Hormuz >70% normal within 10d; time-stop 2026-05-22"),
      (3,"Correlation gate clean",                       "ok",   "PASS",     "Primary commodity; WTI/Silver/Copper gated behind. Equity book corr moderate only."),
      (4,"Per-position <=2% / heat <=8%",                "ok",   "PASS",     "0.75%; heat P009+P010+P016 = ~2.6% (well within 8% cap)"),
      (5,"ATR stop set",                                 "ok",   "PASS",     "Entry ~$94.25 avg; 2x ATR ~$3.7 -> stop $90.50"),
      (6,"Catalyst asymmetry stated",                    "warn", "PARTIAL",  "C=0 -- structural edge only. Iran binary is symmetric (-10-15% on deal). Same PARTIAL as SPY P009 precedent 2026-04-20. Size halved."),
      (7,"Overlay Gate clearance",                       "ok",   "PASS",     "Commodity sleeve CONFIRMED ON (V034 GSG 31.75 > 10m-SMA 25.35)"),
      (8,"Digest clearance",                             "ok",   "PASS",     "No unresolved POSITION-ALERT in slack-digest; no prior Brent position open"),
      (9,"V027 tier applied",                            "ok",   "PASS (R1.B)", "z+1.65 = capital expansion; full sizing allowed; binary-downside haircut overrides to 0.75%")]),
    ("INTC Long (P013) -- Awaiting Apr-23 beat",
     "WAIT FOR CONFIRMED BEAT (Apr-24 UTC+8 morning). Prior P004 closed Apr-19 to avoid this binary.",
     [(1,"|Sum|>=3 with C scored",                      "ok",   "PASS",     "Sum +4; C+1 (Terafab earnings Apr-23 AC pre-scored)"),
      (2,"Invalidation written, concrete, date-bounded", "ok",   "PASS",     "Q1 miss -> C=0/-1 -> no entry; time-stop 2026-06-23"),
      (3,"Correlation gate clean",                       "ok",   "PASS",     "Distinct foundry driver; equity heat within cap"),
      (4,"Per-position <=2% / heat <=8%",                "ok",   "PASS",     "1.0% planned; total ~3.5% if all open"),
      (5,"ATR stop set",                                 "ok",   "PASS",     "2x ATR ~$5 below fill; adjust at Apr-24 fill price"),
      (6,"Catalyst asymmetry stated",                    "ok",   "PASS",     "C+1: beat = thesis confirmed; miss = no entry. High asymmetry."),
      (7,"Overlay Gate clearance",                       "ok",   "PASS",     "Equity sleeve ON"),
      (8,"Digest clearance",                             "ok",   "PASS",     "No INTC POSITION-ALERT; P004 closed Apr-19")]),
]

# ── Catalyst Calendar ──────────────────────────────────────────────────────────
# (date_html, event_html, assets, pill_cls, pill_text)
CATALYSTS = [
    ("<b>Apr-22 AC</b>",    "<b>TSLA Q1 earnings</b>",          "QQQ, SPY (P009 stress)", "red",    "HIGH -- delivery miss baked; guidance = key. P009 stop $696 at risk on miss"),
    ("<b>Apr-23 AC</b>",    "<b>INTC Q1 earnings</b>",          "INTC, QQQ",              "red",    "HIGH -- P013 entry trigger; enter $68-72 Apr-24 morning on beat"),
    ("Apr-23 AC",           "AMZN Q1 earnings",                 "AMZN, QQQ",              "yellow", "MED -- AWS read-through; AMZN Sum+2 potential +3 on beat"),
    ("<b>Apr-28-29</b>",    "<b>FOMC</b>",                      "All positions",          "red",    "HIGH -- hawkish surprise = P009/P010 exit rule; Brent P016 R-headwind"),
    ("Apr-29 AC",           "GOOGL Q1 earnings",                "GOOGL (P015 trigger)",   "red",    "HIGH -- P015 entry trigger; enter $333-340 Apr-30 morning on beat"),
    ("Apr-29 AC",           "META earnings (same day FOMC)",    "META, QQQ",              "yellow", "MED -- double-event risk"),
    ("Apr-29 AC",           "AMZN earnings",                    "AMZN, QQQ",              "yellow", "MED -- capex + AWS trajectory"),
    ("<b>Apr-30</b>",       "<b>AAPL P014 hard time-stop</b>",  "AAPL",                   "red",    "HIGH -- exit regardless of P&amp;L before May-1 earnings"),
    ("<b>May-1</b>",        "<b>Faber overlay gate review</b>", "All sleeves",            "yellow", "MED -- BTC needs >$91.5k at Apr-30 close for crypto sleeve ON"),
    ("May-12",              "April CPI",                        "All",                    "yellow", "MED -- Hormuz inflation follow-through; Brent P016 R-confirmatory"),
    ("Ongoing",             "WTI $90/$95 threshold watch",      "Brent P016, R-baseline", "yellow", "MED -- WTI $90.16 live; >$95 = R headwind; deal = P016 invalidation"),
]
CAT_LABELS = ['Apr-22 TSLA','Apr-23 INTC','Apr-28-29 FOMC','Apr-29 GOOGL','Apr-30 AAPL stop','May-1 Gate','May-12 CPI']
CAT_DATA   = [2, 2, 2, 2, 2, 1, 1]
CAT_COLORS = ['#f87171','#f87171','#f87171','#f87171','#f87171','#facc15','#facc15']

# ── Near-Misses ────────────────────────────────────────────────────────────────
# (asset_html, sum_text, block_reason, trigger, id)
NEAR_MISSES = [
    ("WTI <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "Correlation-gated behind Brent P016 (sector cap 25%). V028 T3 STALE Apr-17.",
     "Brent correlation clears OR fresh WTI basis-mom T1 with divergence cap test", "N042"),
    ("Silver <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "Correlation-gated behind Brent (gate-UNBLOCKED but sector cap full). Basis-mom T3 STALE.",
     "Brent fills + sector cap has room, OR industrial C+1 catalyst", "N043"),
    ("Copper <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "C=0 -- China PMI >50.5 needed. Commodity sleeve now ON.",
     "China Apr PMI print May-01 >50.5", "N044"),
    ("WDC <span class='pill green' style='font-size:10px'>NEW</span>", "+3",
     "C=0 -- no near-term catalyst. T+1 residual but blocking.",
     "Earnings catalyst or AI data-center news flow", "N045"),
    ("NVDA", "+3",
     "T=0 (residual -1.00%); tech concentration vs INTC/GOOGL",
     "Residual >+2% at next staging OR GOOGL Apr-29 AI read-through", "N046"),
    ("MU", "+3",
     "Correlation gate -- equity cluster Apr-22-30; post-FOMC window",
     "Post Apr-30 FOMC resolved + sector heat eases", "N040"),
    ("BTC", "+3",
     "OVERLAY GATE OFF (crypto sleeve; BTC $76k < $91.5k 10m-SMA)",
     "May-01 gate review; needs BTC >$91.5k at Apr-30 close", "P017 gate-blocked"),
]

# ── Score chart data ───────────────────────────────────────────────────────────
SCORE_LABELS = ['Brent P016','SPY P009','EWJ P010','INTC P013','GOOGL P015']
SCORE_S = [1,1,1,1,1]; SCORE_T = [1,1,1,1,0]; SCORE_C = [0,0,0,1,1]; SCORE_R = [1,1,1,1,1]
NEAR_LABELS = ['WTI N042','Silver N043','Copper N044','WDC N045','NVDA N046','MU N040']
NEAR_S = [1,1,1,1,1,1]; NEAR_T = [1,1,1,1,0,1]; NEAR_C = [0,0,0,0,1,0]; NEAR_R = [1,1,1,1,1,1]

# ── Open Positions ─────────────────────────────────────────────────────────────
# (ID, Asset, Side, Entry, Stop, Live, Buffer, UnrealizedPnL, SizeUSDT, flag_cls, flag_text)
# NOTE: Live = last known price from brief/staging; update with each US-close snapshot
OPEN_POSITIONS = [
    ("P009","SPY (SPYUSDT perp)","Long","$708.95 avg (5T)","$696.00","~$705 (Apr-21 close)","~$9 (~1.3%)","~-$4/sh (-0.56%)","$2,089","warn","OPEN -- below entry; within stop buffer"),
    ("P010","EWJ (EWJUSDT perp)","Long","$88.30 avg (3T)","$86.00","~$90.19 (Apr-22 brief)","~$4.19 (~4.7%)","~+$1.89 (+2.14%)","$1,396","ok","OPEN -- above entry; Nikkei record Apr-22"),
    ("P016","Brent (BZUSDT/BZ=F)","Long","$94.00-94.50 zone","$90.50","~$94.19 (Apr-22 staging)","~$3.69 (~3.9%)","--","0.75% (~$30)","blue","PENDING -- Gerald execution required"),
]

# ── Data Gap ───────────────────────────────────────────────────────────────────
GAP_DATA = [18, 5, 0]  # Grade A: LIVE, STALE, MISSING
UPSTREAM = [
    ("ok",  "Local market-brief 2026-04-22 v1 (A) -- 22k bytes, all 20 variables"),
    ("ok",  "Local news 2026-04-22 (A) -- 12/12 categories"),
    ("ok",  "Local audit-staging 2026-04-22 (A) -- V026 12/12, V027 z+1.65, V028 Brent T1"),
    ("ok",  "us-close-snapshot-2026-04-22 (B) -- Apr-21 19:30 ET"),
    ("warn","Cloud market-brief 2026-04-22: MISSING (Drive empty at run time) -- local primary used"),
    ("warn","Cloud news 2026-04-22: MISSING (Drive empty at run time)"),
    ("warn","Cloud trade-rec 2026-04-22: MISSING (Drive empty)"),
    ("ok",  "framework/Memory.md updated 20:35 UTC+8"),
    ("ok",  "SignalLedger: P016, P017, N042-N046 appended"),
    ("ok",  "HypoLedger: H013 Brent P016 inserted"),
]

# ── Discussion ─────────────────────────────────────────────────────────────────
DISCUSSION = [
    "<b>Why Brent Long despite ceasefire extension?</b> The ceasefire extension removes the immediate re-escalation binary (good for risk-on equities), but the Hormuz naval blockade REMAINS in force — &lt;10% normal traffic. Brent is not priced on 'war risk premium' alone; it is priced on physical supply shortage from the blockade. The invalidation event is an Iran DEAL + Hormuz reopening, not just a ceasefire pause. The 'frozen conflict with blockade intact' scenario (Al Jazeera scenario b) is exactly the Brent-bullish case. C was scored 0 precisely because the ceasefire binary is symmetric: deal = -10-15%, frozen = +10%; that asymmetry is already in the 0.75% size haircut.",
    "<b>Why is Brent sized at 0.75% rather than 1.0% or 1.5%?</b> Four simultaneous haircut reasons: (1) Iran ceasefire binary downside (-10-15% if deal — sharp, fast); (2) correlation with open equity book (P009 SPY, P010 EWJ share DXY-weak + real-yield direction with Brent); (3) TSLA earnings tonight = cross-asset tail that could pressure all risk assets; (4) FOMC Apr-28 hawkish tail. V027 z+1.65 allows full sizing per Risk Rules §1.B but the binary-downside logic overrides — same PARTIAL treatment as SPY P009 C=0 precedent (2026-04-20 v3).",
    "<b>Commodity sleeve now CONFIRMED ON for the first time this cycle.</b> V034 GSG 31.75 vs 10m-SMA 25.35 — a 25% premium over the SMA. This is not marginal. The sleeve was UNCERTAIN for 4+ consecutive runs because GSCI data was missing; today's brief provided fresh GSG data. This unblocks Brent P016, Silver (N043), WTI (N042), and Copper (N044) — all of which had Sum+3 scores blocked by the commodity gate. Brent is the primary promotion; the others are near-miss due to correlation gating.",
    "<b>TSLA earnings tonight (Apr-22 AC) are the primary portfolio stress test.</b> Delivery miss (358k vs 372k) is baked in. Market focus is on FSD/Robotaxi guidance and margins. A beat on guidance lifts QQQ/SPX futures — supportive for P009 SPY (stop buffer $9) and P010 EWJ. A miss on guidance increases risk-off pressure and tests the P009 $696 stop. Brent is indirectly exposed via VIX; the $90.50 stop has ~$3.7 buffer from $94.19 entry.",
    "<b>Pending entries this week.</b> P013 INTC: wait for Apr-23 beat confirmation; enter $68-72 Apr-24 morning only. P014 AAPL: deferred (price $266 below $271-274 entry zone); reassess if recovery above $269 before Apr-30. P015 GOOGL: earnings date corrected to Apr-29 AC; entry Apr-30 morning on beat. None of these are actionable today — do not anticipate.",
]

# ── Memory Updates / Sources ───────────────────────────────────────────────────
MEMORY_UPDATES = [
    "Memory.md §5: Added Brent P016 PROMOTED; Silver GATE-UNBLOCKED near-miss",
    "Memory.md §5: P015 GOOGL earnings date CORRECTED to Apr-29 AC; P014 AAPL DEFERRED",
    "Memory.md §5: P011 Gold SUPERSEDED (Sum dropped +3 to +2, T=0)",
    "Memory.md §6: Added WTI $90/$95 threshold watch; Apr-29 GOOGL; May-01 Faber review",
    "SignalLedger: P016 Brent, P017 BTC gate-blocked, N042-N046 appended (65 rows total)",
    "HypoLedger: H013 Brent P016 inserted (PENDING status, entry 94.25, stop 90.50)",
    "memory-lessons.md: appended 2026-04-22 lesson entry (commodity sleeve first ON; Brent 0.75% haircut; V026 12/12 clean)",
    "pipeline/.pipeline-status.json: trade-rec OK; consecutive_failures=0",
]
SOURCES_A = ("market-brief-2026-04-22.md v1 (A) · news-2026-04-22.md (A) · audit-data-staging-2026-04-22.md "
             "(V026 12/12, V027 z+1.65, V028 Brent T1) · framework/{Memory, Risk Rules, Methodology Prompt}.md")
SOURCES_B = "us-close-snapshot-2026-04-22.md (B) · slack-digest-2026-04-22-0923.md (B) · [cloud files all MISSING from Drive]"


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
        rows += (f'<tr style="background:rgba(74,222,128,.04)">'
                 f'<td>{asset}</td><td>{pill(dir_cls,"LONG")}</td>'
                 f'<td>{entry}</td><td>{stop}</td><td>{target}</td><td>{size}</td>'
                 f'<td style="font-size:12px">{catalyst}</td>'
                 f'<td style="font-size:12px;color:#b5bccc">{grade}</td>'
                 f'<td style="font-size:12px">{sleeve}</td></tr>\n')
    # Carry-over pending entries (not new promotions)
    if RECS_CARRY:
        rows += f'<tr><td colspan="9" style="background:#12151c;color:#8a93a6;font-size:11px;padding:5px 10px;letter-spacing:.04em">CARRY-OVER PENDING (previously promoted; not new today)</td></tr>\n'
        for rec in RECS_CARRY:
            asset_c, entry_c, stop_c, target_c, size_c, cat_c = rec
            rows += (f'<tr style="opacity:0.8"><td>{asset_c}</td><td>{pill("blue","—")}</td>'
                     f'<td style="font-size:12px">{entry_c}</td><td style="font-size:12px">{stop_c}</td>'
                     f'<td style="font-size:12px">{target_c}</td><td style="font-size:12px">{size_c}</td>'
                     f'<td style="font-size:12px">{cat_c}</td><td></td><td></td></tr>\n')
    # Blocked
    if RECS_BLOCKED:
        rows += f'<tr><td colspan="9" style="background:#12151c;color:#f87171;font-size:11px;padding:5px 10px;letter-spacing:.04em">GATE-BLOCKED / NEAR-MISS (Sum>=3 but blocked)</td></tr>\n'
        for asset, dir_txt, entry, stop, target, size, catalyst, grade, sleeve in RECS_BLOCKED:
            rows += (f'<tr style="opacity:0.55"><td>{asset}</td><td>{dir_txt}</td>'
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
    # summary cards
    total_heat = sum(0 for _ in OPEN_POSITIONS)  # placeholder; heat shown in exec card
    card_rows = ""
    for pid, asset, side, entry, stop, live, buf, pnl, size, fcls, ftxt in OPEN_POSITIONS:
        pnl_color = "var(--green)" if "+" in pnl else "var(--red)" if "-" in pnl else "var(--accent)"
        flag_cls_map = {"ok": "green", "warn": "yellow", "bad": "red", "blue": "blue"}
        pill_cls = flag_cls_map.get(fcls, "gray")
        card_rows += (
            f'<div class="card" style="min-width:220px">'
            f'<div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em">{pid} &mdash; {asset}</div>'
            f'<div style="font-size:16px;font-weight:600;margin:4px 0;color:{pnl_color}">{pnl}</div>'
            f'<div style="font-size:12px;color:var(--muted)">Entry {entry}</div>'
            f'<div style="font-size:12px;color:var(--muted)">Live {live} &middot; Stop {stop} &middot; Buffer {buf}</div>'
            f'<div style="margin-top:6px"><span class="pill {pill_cls}" style="font-size:10px">{ftxt}</span></div>'
            f'</div>\n'
        )
    cards = f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">{card_rows}</div>'

    # detail table
    rows = "".join(
        f'<tr><td>{pid}</td><td><b>{asset}</b></td><td style="color:var(--green)">{side}</td>'
        f'<td>{entry}</td><td>{stop}</td><td>{live}</td>'
        f'<td style="font-weight:600">{buf}</td>'
        f'<td style="font-weight:600;color:{"var(--green)" if "+" in pnl else "var(--red)" if "-" in pnl else "var(--accent)"}">{pnl}</td>'
        f'<td>{size}</td><td class="{fcls}" style="font-size:12px">{ftxt}</td></tr>\n'
        for pid, asset, side, entry, stop, live, buf, pnl, size, fcls, ftxt in OPEN_POSITIONS
    )
    table = (f'<table>\n<tr><th>ID</th><th>Asset</th><th>Side</th>'
             f'<th>Entry</th><th>Stop</th><th>Last Known Price</th>'
             f'<th>Buffer to Stop</th><th>Unrealized P&amp;L</th>'
             f'<th>Size</th><th>Status</th></tr>\n'
             f'{rows}</table>'
             f'<div class="mute" style="font-size:11px;margin-top:5px">'
             f'Live prices = last known from brief/staging. Update with each US-close snapshot.</div>')
    return cards + table


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

<h2>Open Positions (all)</h2>
{positions_html()}

<h2>Recommendations</h2>
{recs_html()}

<h2>Signal Age &amp; Time-Decay</h2>
{signal_age_html()}

<h2>Factor Exposure Aggregate</h2>
{factor_exposure_html()}

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
