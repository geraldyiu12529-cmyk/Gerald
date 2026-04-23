"""Canonical HTML generator v3 for trade-rec reports.
   Fixed 20-section template — ONLY update PER-RUN DATA block for each date.
   Sections, charts, and layout never change. Empty data = graceful empty state.
   Run: python scripts/gen_trade_rec_html.py
"""
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# PER-RUN DATA — update ONLY this block for each date.
# ══════════════════════════════════════════════════════════════════════════════

TODAY      = "2026-04-22"
VERSION    = "v1 Local"
GEN_TIME   = "2026-04-22 20:30 UTC+8"
SUPERSEDES = "Local primary — cloud files absent from Drive at run time."
STATUS_CLS = "ok"   # ok / warn / bad
STATUS_TXT = "OK"
MISS_COUNT = "0 (T3 fallbacks applied)"
V026_ST    = "ALL 12 LIVE"
V027_ST    = "z+1.65"

# ── Portfolio NAV ────────────────────────────────────────────────────────────
# Update this whenever Gerald deposits/withdraws or trade-update runs post-close.
# All notional sizes in RECS are computed as: risk_pct × PORT_NAV / stop_distance_pct
PORT_NAV      = 4300    # USDT
PORT_NAV_DATE = "2026-04-22"

REGIME_LABEL = "RISK-ON (FRAGILE) / GEOPOLITICAL-BINARY"
REGIME_SUB   = "CEASEFIRE EXTENDED  |  HORMUZ BLOCKED (<10% traffic)  |  TSLA earnings tonight AC"

# Executive summary cards: (label, val_text, val_css_class, sub_text)
EXEC_CARDS = [
    ("Promoted This Run",   "1 signal",            "ok",   "Brent P016 Long -- commodity sleeve first ON this cycle"),
    ("Near-Miss / Blocked", "5 near-miss + 1 gate","warn", "WTI | Silver | Copper | WDC | NVDA near-miss | BTC gate-blocked"),
    ("Regime",              REGIME_LABEL,           "",     REGIME_SUB),
    ("Portfolio Heat",      "~2.6%",                "",     f"~${round(2.6*PORT_NAV/100)} USDT at risk / ${PORT_NAV} NAV | P009+P010+P016 | 8% cap | room for INTC/GOOGL"),
]

# ── Open Positions ──────────────────────────────────────────────────────────
# Tuple: (ID, Asset, Side, entry_f, live_f, stop_f, tp1_f, tp2_f,
#         size_pct, size_usd_str, unreal_pct, flag_cls, flag_txt, time_stop)
# entry_f/live_f/stop_f/tp1_f/tp2_f are floats used for the range chart.
# flag_cls: "ok"=open-profit | "warn"=open-risk | "bad"=open-loss | "blue"=pending
# unreal_pct: float % (negative=loss, 0.0 if pending/not filled)
OPEN_POSITIONS = [
    # Tuple: (ID, Asset, Side, entry_f, live_f, stop_f, tp1_f, tp2_f,
    #         size_pct, size_usd_str, unreal_pct, flag_cls, flag_txt, time_stop,
    #         trail_activate_f, trail_pct)
    # trail_activate_f = entry + 1.5×ATR — price to move stop to breakeven (Rule 2)
    # trail_pct        = 3×ATR / trail_activate × 100 — chandelier callback % (Rule 3)
    ("P009","SPY",   "Long", 708.95, 705.00, 696.00, 720.0, 730.0,
     1.00, "$2,089", -0.56, "warn", "OPEN | below entry | stop buffer $9 (~1.3%)", "2026-05-13",
     718.7, 2.7),   # ATR=6.475; trail_activate=708.95+9.71; cb=19.43/718.7
    ("P010","EWJ",   "Long",  88.30,  90.19,  86.00,  95.0,  98.0,
     0.75, "$1,396", +2.14, "ok",   "OPEN | above entry | Nikkei record Apr-22",   "2026-06-30",
     90.0, 3.8),    # ATR=1.15; trail_activate=88.30+1.73; cb=3.45/90.0
    ("P016","Brent", "Long",  94.25,  94.19,  90.50,  98.0, 102.0,
     0.75, "~$859",   0.00, "blue", "PENDING | Gerald execution required",          "2026-05-22",
     97.1, 5.8),    # ATR=1.875; trail_activate=94.25+2.81; cb=5.625/97.1
]
TOTAL_HEAT = 2.6   # % of NAV at risk (open + pending)
HEAT_CAP   = 8.0   # % cap per Risk Rules

# ── Thesis Summary ────────────────────────────────────────────────────────────
# Writing standard (2026-04-22): each entry is a full analytical paragraph,
# 4–8 sentences minimum. Cover: position/status, mechanism behind each score
# leg (not just the value), the specific edge, primary invalidation + speed,
# and the exact next action. Numbers must be explained in context.
# Do NOT write terse one-liners — they provide no decision value at review time.
THESIS = {
    "P009": (
        "SPY is held long as the core equity sleeve position with a full three-factor edge (S+T+R, C=0). "
        "The structural case rests on the equity overlay gate being firmly ON — SPY trading ~$705, "
        "well above the estimated 10-month SMA of $650–680 (V033), confirming the regime is Risk-On. "
        "Momentum is constructive (T+1 via raw TSMOM), and intermediary capital (V027 z+1.65) is in "
        "expansion territory, which under Risk Rules §1.B authorizes full sizing — however, the position "
        "was deliberately half-sized at initiation because the Catalyst leg scores zero. There is no "
        "fresh event-driven tailwind; the edge is purely structural. Entry was averaged into across five "
        "tranches at $708.95; current price ~$705 leaves approximately $9 of buffer to the $696 hard stop "
        "(2× ATR ~$14). The primary near-term risk is TSLA Q1 earnings tonight — a sharp miss could "
        "pressure QQQ/SPX futures and bring the stop into focus. Secondary risk is FOMC Apr-28–29, "
        "where Warsh hawkish framing has injected a rate-regime tail. Hold unless SPY closes below $696 "
        "or the FOMC delivers a materially hawkish surprise. Time-stop: 2026-05-13."
    ),
    "P010": (
        "EWJ is a long in Japanese large-cap equities, held as an international equity sleeve position "
        "with two converging tailwinds. The primary structural driver (S+1) is USD weakness: DXY has "
        "fallen 3.9% from its April 9 peak to 98.24, compressing the dollar and boosting the relative "
        "purchasing power of yen-denominated assets when translated back for a USD investor — the same "
        "DXY-weak regime that underpins P009 SPY also favors international equity as a second expression. "
        "The momentum leg (T+1) is confirmed by the Nikkei printing a record high of 59,585 on April 22, "
        "and Japan's March trade surplus marked the seventh consecutive month of surplus, providing "
        "fundamental macro footing beneath the trend. The international equity overlay gate (EWJ $90.19 "
        "vs estimated 10-month SMA ~$78–82) is ON. Entry averaged $88.30 across three tranches; at "
        "$90.19 the position carries approximately $1.89 of unrealized gain. Stop is $86 (2× ATR ~$4.4). "
        "The primary risk is a DXY reversal — if the dollar strengthens sharply on hawkish Fed or "
        "safe-haven flow, both the S-variable and the FX translation unwind simultaneously. Time-stop: "
        "2026-06-30."
    ),
    "P016": (
        "Brent crude is the primary new promotion today — the commodity overlay gate (V034 GSG 31.75 "
        "vs. 10-month SMA 25.35, +24.8% above) confirmed ON for the first time this cycle, unblocking "
        "the commodity sleeve. Three independent structural factors stack the thesis: (1) the Hormuz "
        "Strait blockade — currently restricting less than 10% of normal traffic — is removing a "
        "significant share of seaborne crude supply from the global market, providing a persistent "
        "supply-shock bid; (2) the Brent futures curve shows fresh backwardation with basis-momentum "
        "T1 reading +13.95 and steepening, the only commodity with T1-grade fresh data in today's "
        "V028 run; and (3) USD structural weakness (DXY -3.9% from peak) provides an independent "
        "commodity S+1 tailwind. Intermediary capital expansion (V027 z+1.65) permits full sizing, "
        "but two risks drive a deliberate haircut to 0.75%: first, correlation exposure to P009/P010 "
        "which already express the DXY-weak macro theme; second, the Iran ceasefire binary — a deal "
        "materializing could send Brent down 10–15% instantly, and that outcome has symmetric "
        "probability at current visibility. Entry zone: $94.00–94.50 at-market or limit (Brent current "
        "$94.19). Stop: $90.50 (2× ATR ~$3.7). Targets: $98 / $102. Invalidation: Iran deal confirmed "
        "or Hormuz shipping >70% restored within 10 days. Time-stop: 2026-05-22."
    ),
    "P013": (
        "INTC is a contingent long in Intel, not yet entered — the position is pending an earnings-beat "
        "catalyst trigger tonight. The thesis is grounded in Intel's Terafab foundry ramp: the "
        "manufacturing-services buildout positions Intel to capture external semiconductor production "
        "demand independent of its legacy CPU business cycle, which has historically suffered from "
        "market-share attrition to AMD. What makes the setup compelling is the residual momentum signal "
        "(V026): INTC scores +13.89% on the T+1 residual basis — the highest residual reading in the "
        "entire scored universe. Residual momentum strips out market-wide and sector-wide factors, so "
        "+13.89% represents INTC-specific outperformance, not just semiconductor sector beta. The full "
        "score is Sum+4, the highest conviction score in the current book. A prior position (P004) in "
        "the same direction confirmed the thesis direction with a +2.09% return in 11 days. The entry "
        "plan: Intel reports Q1 after market close tonight (April 23). A confirmed beat triggers a "
        "limit-order entry in the $68–72 zone on the April 24 morning open. Current price $66.26 is "
        "below the zone — do not enter early. If earnings disappoint, the trade is abandoned. Stop "
        "and sizing will be set at entry confirmation."
    ),
    "P014": (
        "AAPL is a promoted long that is currently deferred — the setup is valid but price has not "
        "reached the entry zone, and methodology discipline prohibits chasing. The residual momentum "
        "score (V026) reads +4.68% on a T+1 basis, confirming stock-specific outperformance above "
        "market and sector factors, which gives T=+1. The macro and regime factors are supportive "
        "(S+T=+2), and Sum+3 clears the promotion threshold. The problem is price: AAPL closed at "
        "$266.17 on April 22, below the target entry zone of $271–274. Entering below $268 is "
        "prohibited — the entry zone was set at a level where the risk/reward and stop geometry make "
        "sense; entering lower compresses the reward leg while keeping the stop the same, degrading "
        "the trade's expected value. The action is to wait: if price recovers above $269 before "
        "April 30, the position can be entered. April 30 is a hard deadline — AAPL reports earnings "
        "on May 1, and no position will be initiated into a binary earnings event without an explicit "
        "catalyst thesis scored at C+1. If price fails to recover to $269 before April 30, the "
        "opportunity is abandoned for this cycle."
    ),
    "P015": (
        "GOOGL is a contingent long, not yet entered, pending the April 29 earnings event. The "
        "structural thesis (S+1) is AI-driven search monetization: Google's integration of AI "
        "Overviews and Gemini into core search positions it to defend and grow ad revenue per query "
        "even as the search interface evolves. The catalyst leg (C+1) is the pre-earnings setup: "
        "historically, 88% of Mega-Cap Tech names beat Q1 estimates in the prior four years, "
        "providing a statistically meaningful entry edge on the morning after a confirmed beat. "
        "The trend leg is the current weakness of the setup — residual momentum (V026) scores "
        "-0.80% (T=0), borderline but not positive, which is why this is a contingent entry "
        "rather than an immediate one. The plan is clear: if GOOGL beats Q1 earnings after market "
        "close on April 29, enter long on the April 30 morning open. Stop is set ~$317 (2× ATR "
        "below the April 30 open). One complicating factor is the FOMC meeting, which concludes "
        "April 29 — the same day as GOOGL earnings. A hawkish Fed surprise on the same evening "
        "could create a cross-current where even a solid earnings beat faces a rates-driven "
        "sell-off. Position size will be evaluated fresh at entry time to account for this "
        "compounded event risk. Time-stop: 2026-05-15."
    ),
}

# ── Data Freshness Strip ──────────────────────────────────────────────────────
# (variable, reading, grade, pill_cls, age_note)
# pill_cls: green=LIVE-A | blue=LIVE-B | yellow=STALE | red=MISSING
FRESHNESS = [
    ("V026",      "12/12",      "A", "green",  "Apr-22 clean"),
    ("V027",      "+1.65",      "A", "green",  "fresh Apr-22"),
    ("V028",      "1/5 fresh",  "A", "yellow", "Brent T1; WTI/Gold/Ag/Cu T3 Apr-17"),
    ("Brent/WTI", "$94/$90",    "A", "green",  "Apr-22 staging (+6-9%)"),
    ("GSG/GSCI",  "31.75",      "A", "green",  "Apr-22 CONFIRMED ON"),
    ("SPY/QQQ",   "~$705/$640", "B", "blue",   "Apr-21 close"),
    ("EWJ",       "$90.19",     "B", "blue",   "Apr-22 brief"),
    ("DXY",       "98.242",     "A", "green",  "Apr-21"),
    ("DGS10",     "4.25%",      "A", "yellow", "1d stale Apr-21"),
    ("HY OAS",    "285bp",      "B", "yellow", "stale Apr-19"),
    ("NFCI",      "-0.47",      "A", "yellow", "12d stale Apr-10"),
    ("VIX",       "19.04",      "B", "blue",   "Apr-21"),
    ("MOVE",      "67.90",      "A", "yellow", "1d stale Apr-21"),
    ("BTC",       "~$76k",      "B", "blue",   "Apr-22 4th test $75k"),
]

# ── Overlay Gate ──────────────────────────────────────────────────────────────
# (Sleeve, Asset, Reading, pill_cls, gate_text)
GATE_ROWS = [
    ("Equity (V033)",    "SPY/QQQ", "ABOVE (~$705/$640 vs est. 10m-SMA $650-680)",          "green","ON"),
    ("Commodity (V034)", "GSG",     "31.75 vs 10m-SMA 25.35 -- ABOVE (CONFIRMED ON Apr-22)","green","ON -- FIRST TIME THIS CYCLE"),
    ("Crypto (V035)",    "BTC",     "$76,000 vs est. 10m-SMA ~$91.5k -- BELOW",             "red",  "OFF"),
    ("Intl Equity",      "EWJ/EFA", "$90.19 vs est. 10m-SMA ~$78-82 -- ABOVE",             "green","ON"),
]
GATE_NOTE = ("Next read: May-01 Faber monthly review. Commodity sleeve CONFIRMED ON first time this cycle -- "
             "Brent P016 promoted as primary; Silver/WTI/Copper correlation-gated. "
             "Crypto sleeve OFF: BTC needs >$91.5k at Apr-30 close.")

# ── Key Variables ─────────────────────────────────────────────────────────────
# (Variable, Reading, Grade, pill_cls, status_text, score_impact)
KEY_VARS = [
    ("VIX",               "19.04",             "B (BNMA)", "yellow","STALE Apr-21",          "R: borderline at 20; contango benign"),
    ("VIX3M",             "20.51",             "B (BNMA)", "gray",  "STALE Apr-18",          "VIX/VIX3M 0.93 = contango; no inversion stress"),
    ("MOVE",              "67.90",             "A",        "yellow","STALE Apr-21",           "R: +1 -- low bond vol; below 80 threshold"),
    ("HY OAS",            "285 bps",           "B (BNMA)", "yellow","STALE Apr-19",           "R: tight; non-stressed backdrop"),
    ("NFCI",              "-0.47",             "A",        "gray",  "STALE Apr-10 (12d)",     "Loose financial conditions"),
    ("IC z-score (V027)", "+1.65",             "A",        "green", "LIVE (Apr-22 fresh)",    "R: capital expansion; full sizing per Risk Rules ss1.B"),
    ("DGS10",             "4.25%",             "A",        "yellow","STALE 1d (Apr-21)",      "2s10s steepening; no inversion drag"),
    ("T10YIE",            "2.36%",             "A",        "yellow","STALE 1d (Apr-21)",      "Above 2% target; FOMC Apr-28 navigate"),
    ("DXY",               "98.242",            "A",        "green", "LIVE (Apr-21)",          "-3.9% from Apr-9 peak; USD structural weakness; Brent S+1"),
    ("SPY / QQQ",         "~$705 / $640",      "B",        "blue",  "Apr-21 close (1d lag)",  "P009 entry $708.95; ~$4 underwater; stop buffer $9"),
    ("EWJ",               "$90.19",            "A",        "blue",  "Apr-22 brief",           "P010 entry $88.30; +$1.89 unrealized; Nikkei record 59,585"),
    ("Brent / WTI",       "$94.19 / $90.16",   "A",        "green", "LIVE Apr-22 (+6-9%)",    "P016 entry zone $94-94.50; backwardation+steepening; Hormuz"),
    ("GSG (GSCI proxy)",  "31.75",             "A",        "green", "LIVE Apr-22 CONFIRMED ON","V034: 31.75 vs 10m-SMA 25.35 (+24.8%); commodity sleeve ON"),
    ("BTC",               "~$76,000",          "B",        "blue",  "Apr-22 approx.",         "4th test $75k; ETF +$412M Apr-21; sleeve OFF; crypto gate"),
]

# ── Audit Additions ───────────────────────────────────────────────────────────
# (ID, Variable, pill_cls, status_text, dm_pill_cls, dm_text)
AUDIT_ROWS = [
    ("V026","Residual momentum (FF5 12m) -- 12 tickers",
     "green","ALL 12 LIVE (no numpy failure Apr-22)",
     "green","YES -- TSLA/PLTR T=-1 via residual-over-raw; INTC/AAPL/MU/WDC T=+1; NVDA/GOOGL T=0"),
    ("V027","Intermediary capital z-score",
     "green","LIVE +1.65 (Apr-22 fresh)",
     "green","YES -- R=+1 Grade A; capital expansion; full sizing authorized (ss1.B); overridden 0.75% for P016 binary-downside"),
    ("V028","Basis-momentum (4w/12w)",
     "yellow","PARTIAL -- Brent LIVE T1 (Apr-22); WTI/Gold/Silver/Copper T3 STALE Apr-17 (5d limit)",
     "yellow","Brent S+1 CONFIRMED (backwd+13.95, steepening); others near-miss via static slope; infra failure action-logged"),
]
META_ROWS = [
    ("V029","BAB (USMV/SPLV)",           "gray","Not computed","NO"),
    ("V030","DealerGamma (Grade B)",      "gray","Not computed","NO"),
    ("V031","GP/A (Gross Profitability)", "gray","Not computed","NO"),
    ("V032","CEI (Composite Issuance)",   "gray","Not computed","NO"),
]

# ── V026 Residual Momentum ────────────────────────────────────────────────────
# (ticker, residual_pct_or_None, t_score, signal_note)
V026_RESIDUALS = [
    ("MU",    +15.63, "+1", "N040 near-miss -- correlation gate (equity cluster Apr-22-30)"),
    ("INTC",  +13.89, "+1", "P013 OPEN -- entry trigger Apr-23 AC beat"),
    ("WDC",     None, "+1", "N045 near-miss -- C=0 no near-term catalyst"),
    ("AAPL",  +4.68,  "+1", "P014 DEFERRED -- price $266.17 below $271-274 entry zone"),
    ("AMZN",    None,  "0", "Sum+2; timing Apr-29 earnings"),
    ("MSFT",    None,  "0", "not individually scored this run"),
    ("META",    None,  "0", "Sum+2; timing Apr-29 same-day FOMC"),
    ("PYPL",    None,  "0", "not individually scored this run"),
    ("NVDA",  -1.00,   "0", "N046 near-miss -- residual -1.00%; tech concentration"),
    ("GOOGL", -0.80,   "0", "P015 CONTINGENT -- earnings Apr-29 AC; entry Apr-30 morning"),
    ("TSLA",  -9.12,  "-1", "confirmed no-trade; earnings tonight"),
    ("PLTR",  -35.62, "-1", "Sum+2 only; factor crowding confirmed"),
    ("TSM",     None,  "?", "not computed (data N/A this run)"),
    ("AVGO",    None,  "?", "not computed (data N/A this run)"),
    ("BABA",    None,  "?", "not computed (data N/A this run)"),
]

# ── Score Chart Data ──────────────────────────────────────────────────────────
SCORE_LABELS = ["Brent P016","SPY P009","EWJ P010","INTC P013","GOOGL P015"]
SCORE_S = [1,1,1,1,1]; SCORE_T = [1,1,1,1,0]; SCORE_C = [0,0,0,1,1]; SCORE_R = [1,1,1,1,1]
NEAR_LABELS = ["WTI N042","Silver N043","Copper N044","WDC N045","NVDA N046","MU N040"]
NEAR_S = [1,1,1,1,1,1]; NEAR_T = [1,1,1,1,0,1]; NEAR_C = [0,0,0,0,1,0]; NEAR_R = [1,1,1,1,1,1]

# ── Factor Exposure ───────────────────────────────────────────────────────────
# (ID, asset, status, size_pct, S, T, C, R)
FACTOR_EXPOSURE = [
    ("P009","SPY",   "Open",            1.00, 1,1,0,1),
    ("P010","EWJ",   "Open",            0.75, 1,1,0,1),
    ("P016","Brent", "Pending (0.75%)", 0.75, 1,1,0,1),
    ("P013","INTC",  "Awaiting beat",   1.00, 1,1,1,1),
    ("P014","AAPL",  "Deferred",        0.75, 1,1,0,1),
    ("P015","GOOGL", "Contingent",      0.75, 1,0,1,1),
]

# ── Material Delta Box ────────────────────────────────────────────────────────
# Set DELTA_ITEMS = [] for v1 / no-material-change runs
DELTA_ITEMS = [
    '<span class="pill green">NEW P016</span> <b>Brent Long Sum+3</b> -- commodity sleeve CONFIRMED ON (GSG 31.75 > 10m-SMA 25.35). First commodity promotion this cycle. Entry $94.00-94.50, stop $90.50, size 0.75%.',
    '<span class="pill yellow">P015 DATE CORRECTED</span> <b>GOOGL earnings Apr-29 AC</b> (not Apr-22/23). Entry trigger shifts to Apr-30 morning. P015 contingent unchanged.',
    '<span class="pill blue">P014 AAPL DEFERRED</span> Price $266.17 below entry zone $271-274. Do not enter below $268. Hard time-stop Apr-30 still binding.',
]
DELTA_FOOT = ("BTC Sum+3 gate-blocked (crypto sleeve OFF; BTC $76k < $91.5k 10m-SMA) logged P017 Taken=NO. "
              "WTI/Silver/Copper near-miss -- correlation-gated behind Brent. "
              "V026 clean 12/12. V027 z+1.65 capital expansion = full sizing.")

# ── Recommendations ───────────────────────────────────────────────────────────
# RECS: new promotions this run
# (asset_html, dir_cls, entry, stop, target, size, catalyst, grade, sleeve, notional_usd)
# notional_usd = risk_pct × PORT_NAV / (stop_distance / entry_mid)
RECS = [
    # (asset_html, dir_cls, entry, stop, target, size, catalyst, grade, sleeve, notional_usd, trail_stop)
    # trail_stop: "$trail_activate (+BE% / +cb%)" — BE% = 1.5×ATR/entry (move-to-breakeven distance); cb% = 3×ATR/trail_activate (chandelier callback from HH)
    ("<b>Brent</b> <span class='pill green'>NEW P016</span>","green",
     "$94.00-94.50 (at-market/limit; last $94.19)","$90.50 (2x ATR ~$3.7)","$98 / $102",
     "0.75% (corr+binary haircut)",
     "C=0; structural: Hormuz blockade + backwardation steepening + DXY weak. Iran deal = invalidation.",
     "S+1(A), T+1(A), C0, R+1(A)","Commodity ON -- first cycle",
     813,              # 0.75% × $4,300 / (3.75/94.25) ≈ $813
     "~$97.1 (+3.0% BE / +5.8% cb)"),  # BE=1.5×1.875/94.25; cb=3×1.875/97.1
]
# RECS_CARRY: carry-over pending entries from prior recs
# (asset_label, entry_note, stop, target, size_note, catalyst_note, notional_usd, trail_stop)
RECS_CARRY = [
    ("<b>SPY</b> P009 OPEN",        "$708.95 avg (filled)",            "$696",      "~$720/$730","1.0% risk · ~$43 at stop",  "C=0; live ~$705 -- $9 stop buffer; watch TSLA tonight", 2089, "$718.7 (+1.4% BE / +2.7% cb)"),
    ("<b>EWJ</b> P010 OPEN",        "$88.30 avg (filled)",             "$86.00",    "~$95/$98",  "0.75% risk · ~$32 at stop", "C=0; Nikkei record Apr-22 +2.1% unrealized",            1396, "$90.0 (+1.9% BE / +3.8% cb)"),
    ("<b>INTC</b> P013 await beat", "$68-72 (after Apr-23 AC beat)",   "~$63-67",   "$75/$82",   "1.0% risk · ~$43 at stop",  "C+1: Apr-23 AC -- enter Apr-24 morning ONLY on beat",   602,  "est. at fill"),
    ("<b>AAPL</b> P014 deferred",   "DEFERRED ($266 < $271-274 zone)", "~$264-267", "$280/$290", "0.75% risk · ~$32 at stop", "Hard exit Apr-30; recover above $269 before",           543,  "est. at fill"),
    ("<b>GOOGL</b> P015 contingent","~$333-340 after Apr-29 beat",     "~$317",     "$355/$375", "0.75% risk · ~$32 at stop", "C+1: Apr-29 AC; enter Apr-30 morning on beat ONLY",     543,  "est. at fill"),
]
# RECS_BLOCKED: gate-blocked or near-miss Sum>=3
# (asset_html, dir_txt, entry, stop, target, size, catalyst, grade, sleeve)
RECS_BLOCKED = [
    ("<b>BTC</b> <span class='pill red'>P017 gate-blocked</span>","LONG",
     "--","--","--","Taken=NO",
     "Crypto sleeve OFF (BTC $76k < $91.5k 10m-SMA). Sum+3 (S+1/T+1/C+1/R0) blocked.",
     "S+1,T+1,C+1,R0 (+3)","Crypto OFF"),
    ("<b>WTI</b> <span class='pill yellow'>N042 near-miss</span>","LONG",
     "--","--","--","Taken=NO",
     "Correlation-gated behind Brent P016. V028 T3 STALE Apr-17.",
     "S+1,T+1,C0,R+1 (+3)","Commodity ON (near-miss)"),
    ("<b>Silver</b> <span class='pill yellow'>N043 near-miss</span>","LONG",
     "--","--","--","Taken=NO",
     "Gate-UNBLOCKED but correlation-gated behind Brent. Promote if Brent fills + sector cap room.",
     "S+1,T+1,C0,R+1 (+3)","Commodity ON (near-miss)"),
]
RECS_FOOTNOTE = (f"R=+1 via V027 z+1.65 (A) + HY OAS 285bp (B) + NFCI -0.47 (A) + VIX 19.04 (B) -- Grade A double confirmed.<br>"
                 f"Heat open+pending: P009 1.0% + P010 0.75% + P016 0.75% = 2.6% (~${round(2.6*PORT_NAV/100)} USDT / 32% of 8% cap). "
                 f"If P013+P014+P015 all fill: +2.5% additional = 5.1% total (~${round(5.1*PORT_NAV/100)} USDT, within cap).<br>"
                 f"<b>PORT_NAV: ${PORT_NAV} USDT ({PORT_NAV_DATE}).</b> Notionals = risk% &times; NAV &divide; stop-distance%.")

# ── Signal Age ────────────────────────────────────────────────────────────────
# (ID, asset, status, promoted_date, days_held, expiry_date, days_remaining, urgency_cls)
# urgency_cls: "ok">=20d | "warn"=10-19d | "bad"<10d
SIGNAL_AGE = [
    ("P009","SPY",   "OPEN -- filled Apr-21",       "2026-04-20", 2,"2026-05-13",21,"ok"),
    ("P010","EWJ",   "OPEN -- filled Apr-21",       "2026-04-21", 1,"2026-06-30",69,"ok"),
    ("P016","Brent", "PENDING -- Gerald execution", "2026-04-22", 0,"2026-05-22",30,"ok"),
    ("P013","INTC",  "Awaiting Apr-23 AC beat",     "2026-04-21", 1,"2026-06-23",62,"ok"),
    ("P014","AAPL",  "DEFERRED -- below zone",      "2026-04-21", 1,"2026-04-30", 8,"bad"),
    ("P015","GOOGL", "Contingent -- entry Apr-30",  "2026-04-21", 1,"2026-05-15",23,"ok"),
]

# ── Pre-Entry Checklists ──────────────────────────────────────────────────────
# list of (title, note_html, [(num, item, cls, icon, detail), ...])
# cls: "ok" / "warn" / "bad"
CHECKLISTS = [
    ("Brent Long (P016) -- New promotion today",
     "Commodity sleeve CONFIRMED ON for first time this cycle. "
     "Size haircut to 0.75% for Iran binary + TSLA tonight + FOMC Apr-28.",
     [(1,"|Sum|>=3 with C scored",                      "ok",  "PASS","Sum+3 (S+1/T+1/C0/R+1); C=0 explicitly scored (ceasefire binary symmetric)"),
      (2,"Invalidation written, concrete, date-bounded", "ok",  "PASS","Iran deal -> Brent <$88; Hormuz >70% within 10d; time-stop 2026-05-22"),
      (3,"Correlation gate clean",                       "ok",  "PASS","Primary commodity; WTI/Silver/Copper gated behind. Equity corr moderate only."),
      (4,"Per-position <=2% / heat <=8%",                "ok",  "PASS","0.75%; heat P009+P010+P016 = ~2.6% (well within 8% cap)"),
      (5,"ATR stop set",                                 "ok",  "PASS","Entry ~$94.25 avg; 2x ATR ~$3.7 -> stop $90.50"),
      (6,"Catalyst asymmetry stated",                    "warn","PARTIAL","C=0 -- structural only. Iran binary symmetric (-10-15% on deal). Size halved per SPY P009 C=0 precedent."),
      (7,"Overlay Gate clearance",                       "ok",  "PASS","Commodity sleeve CONFIRMED ON (V034 GSG 31.75 > 10m-SMA 25.35)"),
      (8,"Digest clearance",                             "ok",  "PASS","No unresolved POSITION-ALERT; no prior Brent position open"),
      (9,"V027 tier (R1.B)",                             "ok",  "PASS","z+1.65 = capital expansion; full sizing allowed; binary-downside overrides to 0.75%")]),
    ("INTC Long (P013) -- Awaiting Apr-23 AC beat",
     "WAIT FOR CONFIRMED BEAT (Apr-24 UTC+8 morning). Prior P004 closed Apr-19 to avoid this binary.",
     [(1,"|Sum|>=3 with C scored",                      "ok",  "PASS","Sum+4; C+1 (Terafab earnings Apr-23 AC pre-scored)"),
      (2,"Invalidation written, concrete, date-bounded", "ok",  "PASS","Q1 miss -> C=0/-1 -> no entry; time-stop 2026-06-23"),
      (3,"Correlation gate clean",                       "ok",  "PASS","Distinct foundry driver; equity heat within cap"),
      (4,"Per-position <=2% / heat <=8%",                "ok",  "PASS","1.0% planned; total ~3.5% if all open"),
      (5,"ATR stop set",                                 "ok",  "PASS","2x ATR ~$5 below fill; adjust at Apr-24 fill price"),
      (6,"Catalyst asymmetry stated",                    "ok",  "PASS","C+1: beat = thesis confirmed; miss = no entry. High asymmetry."),
      (7,"Overlay Gate clearance",                       "ok",  "PASS","Equity sleeve ON"),
      (8,"Digest clearance",                             "ok",  "PASS","No INTC POSITION-ALERT; P004 closed Apr-19")]),
]

# ── Regime Sensitivity ────────────────────────────────────────────────────────
# SCENARIOS: (header_text, header_cls)
SCENARIOS = [
    ("VIX -> 28",       "warn"),
    ("FOMC +50bp",      "bad"),
    ("Iran Deal -10%",  "bad"),
    ("Iran Esc. +15%",  "ok"),
    ("SPY -5%",         "bad"),
]
# SENSITIVITY: (ID, asset, [(impact_cls, short_label), ...]) -- one per SCENARIO
SENSITIVITY = [
    ("P009","SPY Long",[
        ("bad", "EXIT: VIX > 25"),
        ("bad", "EXIT: primary risk"),
        ("warn","Oil shock spillover"),
        ("ok",  "Risk-on boost"),
        ("bad", "STOP $696 in range"),
    ]),
    ("P010","EWJ Long",[
        ("warn","Risk-off; BOJ caution"),
        ("bad", "USD up JPY weak -> EWJ down"),
        ("warn","Global risk-off minor"),
        ("ok",  "Risk-on; Nikkei record"),
        ("bad", "High SPY corr."),
    ]),
    ("P016","Brent Long",[
        ("warn","Indirect; VIX != oil"),
        ("warn","USD up -> WTI soft pressure"),
        ("bad", "THESIS INVALIDATED: deal = -10-15%"),
        ("ok",  "Thesis confirmed: supply tighter"),
        ("warn","Risk-off; stop $90.50 OK"),
    ]),
    ("P013","INTC Await",[
        ("warn","Tech selloff; stop OK"),
        ("warn","Sector rotation risk"),
        ("warn","Indirect only"),
        ("ok",  "Foundry thesis independent"),
        ("warn","SPY corr; $63-67 stop"),
    ]),
    ("P015","GOOGL Cont.",[
        ("warn","May not enter if VIX spike"),
        ("warn","FOMC risk post-entry"),
        ("warn","Indirect only"),
        ("ok",  "AI/search independent"),
        ("warn","SPY corr; stop ~$317"),
    ]),
]

# ── Catalyst Calendar ─────────────────────────────────────────────────────────
# (date_html, event_html, assets, pill_cls, pill_text)
CATALYSTS = [
    ("<b>Apr-22 AC</b>", "<b>TSLA Q1 earnings</b>",          "QQQ, SPY P009 stress",  "red",   "HIGH -- delivery miss baked; guidance = key. P009 stop $696 at risk on miss"),
    ("<b>Apr-23 AC</b>", "<b>INTC Q1 earnings</b>",          "INTC, QQQ",             "red",   "HIGH -- P013 entry trigger; enter $68-72 Apr-24 morning on beat"),
    ("Apr-23 AC",        "AMZN Q1 earnings",                 "AMZN, QQQ",             "yellow","MED -- AWS read-through; AMZN Sum+2 potential +3 on beat"),
    ("<b>Apr-28-29</b>", "<b>FOMC</b>",                      "All positions",         "red",   "HIGH -- hawkish surprise = P009/P010 exit rule; Brent R-headwind"),
    ("<b>Apr-29 AC</b>", "<b>GOOGL Q1 earnings</b>",         "GOOGL P015 trigger",    "red",   "HIGH -- P015 entry trigger; enter $333-340 Apr-30 morning on beat"),
    ("Apr-29 AC",        "META earnings (same day FOMC)",    "META, QQQ",             "yellow","MED -- double-event risk"),
    ("<b>Apr-30</b>",    "<b>AAPL P014 hard time-stop</b>",  "AAPL",                  "red",   "HIGH -- exit regardless of P&amp;L before May-1 earnings"),
    ("<b>May-1</b>",     "<b>Faber overlay gate review</b>", "All sleeves",           "yellow","MED -- BTC needs >$91.5k at Apr-30 close for crypto sleeve ON"),
    ("May-12",           "April CPI",                        "All",                   "yellow","MED -- Hormuz inflation follow-through; Brent P016 R-confirmatory"),
    ("Ongoing",          "WTI $90/$95 threshold watch",      "Brent P016, R-base",    "yellow","MED -- WTI $90.16 live; deal = P016 invalidation"),
]
CAT_LABELS = ["Apr-22 TSLA","Apr-23 INTC","Apr-28-29 FOMC","Apr-29 GOOGL","Apr-30 AAPL","May-1 Gate","May-12 CPI"]
CAT_DATA   = [2,2,2,2,2,1,1]
CAT_COLORS = ["#f87171","#f87171","#f87171","#f87171","#f87171","#facc15","#facc15"]

# ── Near-Misses ───────────────────────────────────────────────────────────────
# (asset_html, sum_text, block_reason, trigger, id)
NEAR_MISSES = [
    ("WTI <span class='pill green' style='font-size:10px'>NEW</span>","+3",
     "Correlation-gated behind Brent P016 (sector cap 25%). V028 T3 STALE Apr-17.",
     "Brent clears OR fresh WTI basis-mom T1 with divergence cap test","N042"),
    ("Silver <span class='pill green' style='font-size:10px'>NEW</span>","+3",
     "Gate-UNBLOCKED but correlation-gated behind Brent (sector cap full).",
     "Brent fills + sector cap room, OR industrial C+1 catalyst","N043"),
    ("Copper <span class='pill green' style='font-size:10px'>NEW</span>","+3",
     "C=0 -- China PMI >50.5 needed. Commodity sleeve now ON.",
     "China Apr PMI print May-01 >50.5","N044"),
    ("WDC <span class='pill green' style='font-size:10px'>NEW</span>","+3",
     "C=0 -- no near-term catalyst. T+1 residual confirmed.",
     "Earnings catalyst or AI data-center news flow","N045"),
    ("NVDA","+3",
     "T=0 (residual -1.00%); tech concentration vs INTC/GOOGL",
     "Residual >+2% at next staging OR GOOGL Apr-29 AI read-through","N046"),
    ("MU","+3",
     "Correlation gate -- equity cluster Apr-22-30; post-FOMC window",
     "Post Apr-30 FOMC resolved + sector heat eases","N040"),
    ("BTC","+3",
     "OVERLAY GATE OFF (crypto sleeve; BTC $76k < $91.5k 10m-SMA)",
     "May-01 gate review; BTC >$91.5k at Apr-30 close (large gap)","P017 gate-blocked"),
]

# ── Closed-Trade Context ──────────────────────────────────────────────────────
# (section_label, asset_tag, [(ID, side, open_date, close_date, days, pnl, pnl_cls, exit_reason)])
CLOSED_CONTEXT = [
    ("INTC -- prior pipeline history","INTC",[
        ("P004","Long","2026-04-08","2026-04-19",11,"+2.09%","ok",
         "Planned pre-earnings exit -- avoided Apr-23 binary. Thesis direction validated. Re-entering P013 after beat."),
    ]),
    ("Commodity sleeve -- prior closed","Brent/WTI",[
        ("P008","Long (off-meth)","2026-04-20","2026-04-21",1,"+0.19%","ok",
         "Off-methodology WTI long; closed Apr-21 after P009/P010 opened. Not scored. "
         "Brent P016 is the first methodology-promoted commodity long."),
    ]),
]
CLOSED_NOTE = ("SPY, EWJ, Brent: first methodology entries -- no prior closed history. "
               "Full history: SignalLedger -> PerformanceStats sheet.")

# ── Data Gap ──────────────────────────────────────────────────────────────────
GAP_DATA = [18, 5, 0]   # Grade A: [LIVE, STALE, MISSING]
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
    ("ok",  "HypoLedger: H013 Brent P016 inserted (PENDING)"),
]

# ── Discussion ────────────────────────────────────────────────────────────────
# Writing standard (2026-04-22): each entry is a substantive paragraph,
# 5–10 sentences, with a bold header question/topic. Cover min: primary
# promotion rationale, sizing haircut factors, gate/regime change consequences,
# live event risk scenarios mapped to each position with price levels, all
# pending entry triggers with exact conditions, portfolio heat + regime label.
# Frame each item as "why is the obvious interpretation incomplete?" — not a
# recap of what the scorecard already shows.
DISCUSSION = [
    (
        "<b>Why Brent Long despite the ceasefire extension?</b> "
        "It is worth being precise about what the ceasefire extension actually changes. "
        "The extension removes the immediate 24-hour re-escalation trigger — that is good for equities and reduces VIX-spike risk. "
        "What it does NOT change is the Hormuz Strait blockade, which remains in force at less than 10% of normal traffic throughput. "
        "Brent's current price level is not primarily a war-risk premium — it is a physical supply shortage premium. "
        "The tonnage that cannot move through Hormuz has to re-route via the Cape of Good Hope (adding ~14 days and meaningful freight cost), "
        "or it simply does not reach buyers. That supply displacement is structural and does not resolve with a ceasefire. "
        "The scenario that invalidates the thesis is not a ceasefire pause; it is a full Iran nuclear deal followed by Hormuz reopening — "
        "a significantly higher political bar. The 'frozen conflict with blockade intact' scenario is precisely the Brent-bullish case. "
        "C is scored at 0 (not +1) because the binary outcome is symmetric: a deal materializes = Brent -10 to -15% fast; "
        "blockade persists = Brent +10% or more. That symmetric uncertainty is why there is no catalyst credit — "
        "and it is already reflected in the 0.75% size haircut rather than the standard 1.5%."
    ),
    (
        "<b>Why 0.75% and not more?</b> "
        "This sizing decision is the most consequential judgment call in today's rec and deserves explicit treatment. "
        "V027 intermediary capital at z+1.65 authorizes full sizing under Risk Rules §1.B — so the methodology ceiling is 1.5%. "
        "Four factors independently argued for a haircut, and their combined weight drove the position to half-size. "
        "First, the Iran ceasefire binary: a deal could produce a -10 to -15% drawdown in Brent within hours, "
        "and at 1.5% position size that would consume nearly the entire annual risk budget for a single commodity slot. "
        "Second, correlation exposure: P009 SPY and P010 EWJ are both DXY-weak expressions in the equity sleeve — "
        "adding a commodity position that also benefits from USD weakness means three positions sharing the same macro factor; "
        "a DXY reversal would hurt all three simultaneously. "
        "Third, TSLA earnings tonight introduce cross-asset tail risk — a miss could pressure QQQ/SPX futures, "
        "trigger risk-off, and impact Brent through VIX expansion. "
        "Fourth, FOMC Apr-28-29 is six days out with hawkish optionality (Warsh framing). "
        "The SPY P009 precedent — also C=0, also half-sized — is directly applicable. "
        "This is a structural-edge position with acknowledged binary downside, not a momentum chase; sizing should reflect that."
    ),
    (
        "<b>Commodity sleeve ON for the first time this cycle — what changes.</b> "
        "V034 (GSG GSCI proxy) reading 31.75 against an estimated 10-month SMA of 25.35 represents a 24.8% premium — "
        "a decisive gate-ON confirmation, not a borderline reading. This matters because the overlay gate is the system's "
        "primary defense against promoting commodity trades in secular downtrend regimes. For the past several months, "
        "every commodity Sum+3 signal — Brent, WTI, Silver, Copper — was blocked by this gate regardless of its score. "
        "Today that block is lifted. The direct consequences: Brent P016 is promoted as primary (freshest basis-momentum data, T1 grade). "
        "Silver (N043) and WTI (N042) are unblocked but remain near-misses today due to correlation gating behind Brent — "
        "the sector cap of 25% commodity exposure prevents stacking correlated commodity longs. "
        "Copper (N044) remains blocked on C (needs China PMI > 50.5). "
        "The next gate review is May-01 Faber monthly close — if GSG slips below the 10-month SMA, the sleeve gates back OFF "
        "and all commodity positions revert to gate-blocked status at that point."
    ),
    (
        "<b>TSLA earnings tonight are the live portfolio stress test.</b> "
        "The delivery miss (358k vs. 372k guidance) is already market knowledge — that news is baked into the pre-earnings price. "
        "What the market does not yet know are: FSD and Robotaxi guidance quality, gross margin trajectory, "
        "and whether management gives forward-year confidence or signals further demand softness. "
        "The playbook for each scenario: a guidance beat or margin surprise drives QQQ/SPX futures higher overnight, "
        "P009 SPY's ~$9 buffer to the $696 stop widens, and P010 EWJ gets sympathy support through Nikkei futures. "
        "A guidance miss or margin disappointment drives risk-off: QQQ could gap -2% or more, "
        "bringing P009's stop into live focus by morning. Brent is indirectly exposed — "
        "a VIX spike from TSLA risk-off would suppress risk-on sentiment broadly, "
        "though Brent's primary driver (Hormuz supply) is largely independent. "
        "The stop at $90.50 provides ~$3.70 of buffer from $94.19; that buffer is unlikely to be tested by TSLA alone "
        "unless risk-off is severe enough to produce broad commodity liquidation. "
        "INTC P013 is directly at stake: an INTC earnings beat tonight opens the $68-72 entry window; a miss closes it."
    ),
    (
        "<b>Pending entries and what has to happen for each.</b> "
        "Three positions are promoted but not yet entered, each with a specific trigger. "
        "INTC P013 (Sum+4) requires a confirmed beat in Intel's Q1 earnings tonight (April 23 AC). "
        "If beat confirmed: enter long in the $68-72 limit zone on the April 24 morning open — not before, not at market. "
        "The entry zone represents the post-earnings pop range consistent with thesis price geometry; "
        "chasing above $72 on gap-up would compress the risk/reward unacceptably. "
        "AAPL P014 (Sum+3) is deferred because price is at $266.17, below the $271-274 entry zone. "
        "Do not enter below $268. The trade has a hard time-stop of April 30 because AAPL reports May 1 — "
        "if price has not recovered to the entry zone by April 30, the opportunity expires for this cycle. "
        "GOOGL P015 (Sum+3) is a cleaner situation: the trigger is an April 29 AC earnings beat, "
        "with entry on the April 30 morning open. Note that FOMC also concludes April 29 — "
        "a hawkish surprise on the same day could create cross-currents that require sizing judgment at entry time. "
        "None of these three are actionable today."
    ),
    (
        "<b>Portfolio heat and regime context.</b> "
        "Current portfolio heat across all open positions: approximately 2.6% total risk after adding Brent P016 at 0.75%. "
        "That is well within the 8% heat cap, leaving meaningful capacity for INTC P013 (contingent), "
        "and still-deferred AAPL and GOOGL entries. "
        "The regime label — Risk-On (FRAGILE) / Geopolitical-Binary — reflects a market that is directionally constructive "
        "but operating with elevated tail risk on two independent axes: the Iran binary (commodity supply shock) "
        "and the FOMC rate path (earnings multiple compression risk). "
        "FRAGILE is an internal label indicating that the Risk-On read is real but not robust — "
        "a single negative macro surprise could flip the regime. "
        "The correct posture under FRAGILE is: honor the trend, size conservatively on new entries, "
        "keep stops tight, and do not stack correlated positions. That is exactly what today's rec does. "
        "The primary regime-flip watch variable for the next 48 hours is WTI at the $90/$95 threshold: "
        "above $95 begins to function as a tax on growth, creating R headwinds across all sleeves simultaneously."
    ),
]

# ── Memory Updates ────────────────────────────────────────────────────────────
MEMORY_UPDATES = [
    "Memory.md ss5: Added Brent P016 PROMOTED; Silver GATE-UNBLOCKED near-miss",
    "Memory.md ss5: P015 GOOGL earnings date CORRECTED to Apr-29 AC; P014 AAPL DEFERRED",
    "Memory.md ss5: P011 Gold SUPERSEDED (Sum dropped +3 to +2)",
    "Memory.md ss6: Added WTI $90/$95 threshold watch; Apr-29 GOOGL; May-01 Faber review",
    "SignalLedger: P016 Brent, P017 BTC gate-blocked, N042-N046 appended (65 rows total)",
    "HypoLedger: H013 Brent P016 inserted (PENDING status, entry 94.25, stop 90.50)",
    "memory-lessons.md: appended 2026-04-22 lesson entry",
    "pipeline/.pipeline-status.json: trade-rec OK; consecutive_failures=0",
]
SOURCES_A = ("market-brief-2026-04-22.md v1 (A) | news-2026-04-22.md (A) | audit-data-staging-2026-04-22.md "
             "(V026 12/12, V027 z+1.65, V028 Brent T1) | framework/{Memory, Risk Rules, Methodology Prompt}.md")
SOURCES_B = ("us-close-snapshot-2026-04-22.md (B) | slack-digest-2026-04-22-0923.md (B) | "
             "[cloud-market-brief, cloud-news, cloud-trade-rec all MISSING from Drive]")


# ══════════════════════════════════════════════════════════════════════════════
# STATIC DATA — update only when asset universe changes
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
FACTOR_WS = round(sum(r[3]*r[4] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WT = round(sum(r[3]*r[5] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WC = round(sum(r[3]*r[6] for r in FACTOR_EXPOSURE) / _fe_total, 3)
FACTOR_WR = round(sum(r[3]*r[7] for r in FACTOR_EXPOSURE) / _fe_total, 3)


# ══════════════════════════════════════════════════════════════════════════════
# HTML GENERATORS — never edit below this line for routine runs
# ══════════════════════════════════════════════════════════════════════════════

def pill(cls, text):
    return f'<span class="pill {cls}">{text}</span>'

def card(label, value, val_cls, sub):
    vc = f' style="color:var(--{val_cls})"' if val_cls in ("ok","warn","bad") else ""
    return (f'<div class="card">'
            f'<div class="lbl">{label}</div>'
            f'<div class="val"{vc}>{value}</div>'
            f'<div class="mute" style="font-size:12px;margin-top:4px">{sub}</div>'
            f'</div>')

def section(title, content, anchor=""):
    anch = f' id="{anchor}"' if anchor else ""
    return f'<section{anch}>\n<h2>{title}</h2>\n{content}\n</section>\n'


# §1 Freshness Strip
def freshness_html():
    items = []
    for var, reading, grade, cls, note in FRESHNESS:
        dot_c = {"green":"#4ade80","blue":"#5b9bff","yellow":"#facc15","red":"#f87171"}.get(cls,"#8a93a6")
        dot   = {"green":"●","blue":"●","yellow":"◐","red":"○"}.get(cls,"●")
        items.append(
            f'<div class="fresh-item">'
            f'<div class="fresh-var">{var}</div>'
            f'<div class="fresh-val"><span style="color:{dot_c}">{dot}</span> {reading}'
            f'<span class="fresh-grade"> {grade}</span></div>'
            f'<div class="fresh-note">{note}</div>'
            f'</div>'
        )
    return '<div class="fresh-strip">' + "".join(items) + '</div>'


# §2 Portfolio Dashboard
def pos_range_html():
    """CSS price-range bar for each open position."""
    if not OPEN_POSITIONS:
        return '<div class="mute">No open positions.</div>'
    out = []
    for row in OPEN_POSITIONS:
        pid, asset, side, entry, live, stop, tp1, tp2 = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        unreal = row[10]; flag_cls = row[11]
        trail_activate = row[14] if len(row) > 14 else None
        trail_pct_val  = row[15] if len(row) > 15 else None
        total = tp2 - stop
        if total <= 0:
            continue
        def pct(p):
            return max(0.0, min(100.0, (p - stop) / total * 100))
        ep = pct(entry); lp = pct(live); t1p = pct(tp1)
        tap = pct(trail_activate) if trail_activate and trail_activate > stop else None
        pnl_positive = live >= entry
        pnl_col = "#4ade80" if pnl_positive else "#f87171"
        flag_col = {"ok":"#4ade80","warn":"#facc15","bad":"#f87171","blue":"#5b9bff"}.get(flag_cls,"#8a93a6")
        # segment widths — trail_activate splits the upside zone into pre-trail (amber) and chandelier (green tint)
        w_risk = ep
        w_pnl  = abs(lp - ep)
        if tap and tap > lp:
            w_pre_trail  = max(0, tap - lp)
            w_chan        = max(0, t1p - tap)
            trail_segs = (
                f'<div style="width:{w_pre_trail:.1f}%;background:rgba(250,204,21,.08);border-right:2px solid #facc1566" title="Await trail activate: {live} \u2192 {trail_activate}"></div>'
                f'<div style="width:{w_chan:.1f}%;background:rgba(74,222,128,.08);border-right:2px dashed #4ade8055" title="Chandelier zone: {trail_activate} \u2192 TP1 {tp1}"></div>'
            )
        else:
            trail_segs = f'<div style="width:{max(0, t1p-lp):.1f}%;background:rgba(91,155,255,.12);border-right:2px dashed #5b9bff44" title="Upside to TP1: {live} \u2192 {tp1}"></div>'
        w_tp2 = max(0, 100 - t1p)
        bar = (
            f'<div class="range-bar">'
            f'<div style="width:{w_risk:.1f}%;background:rgba(248,113,113,.18);border-right:2px solid #f87171" title="Risk zone: stop {stop} to entry {entry}"></div>'
            f'<div style="width:{w_pnl:.1f}%;background:{pnl_col}30;border-right:2px solid {pnl_col}" title="P&L: entry {entry} to live {live}"></div>'
            + trail_segs +
            f'<div style="width:{w_tp2:.1f}%;background:rgba(91,155,255,.05)" title="Upside to TP2: {tp1} to {tp2}"></div>'
            f'</div>'
        )
        trail_lbl = ""
        if tap:
            trail_lbl = f'<span style="left:{tap:.1f}%;transform:translateX(-50%);color:#facc15;font-weight:700" title="Rule 2: move stop to breakeven when this level prints">Trail&#9733;<br>{trail_activate}</span>'
        labels = (
            f'<div class="range-labels">'
            f'<span style="left:0%">Stop<br>{stop}</span>'
            f'<span style="left:{ep:.1f}%;transform:translateX(-50%)">Entry<br>{entry}</span>'
            f'<span style="left:{lp:.1f}%;transform:translateX(-50%);color:{pnl_col};font-weight:600">Live<br>{live}</span>'
            + trail_lbl +
            f'<span style="left:{t1p:.1f}%;transform:translateX(-50%)">TP1<br>{tp1}</span>'
            f'<span style="right:0">TP2<br>{tp2}</span>'
            f'</div>'
        )
        unreal_str = f'{unreal:+.2f}%' if unreal != 0 else '--'
        header = (
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
            f'<span style="font-weight:600;font-size:13px">{pid} &mdash; {asset}</span>'
            f'<span style="font-size:12px;color:{pnl_col};font-weight:600">{unreal_str} unrealized</span>'
            f'<span style="font-size:11px;color:{flag_col}">{row[12]}</span>'
            f'</div>'
        )
        out.append(f'<div style="margin-bottom:20px">{header}{bar}{labels}</div>')
    return "\n".join(out)

def positions_cards_html():
    if not OPEN_POSITIONS:
        return '<div class="mute">No open positions this session.</div>'
    cards = ""
    for row in OPEN_POSITIONS:
        pid, asset, side = row[0], row[1], row[2]
        entry, live, stop = row[3], row[4], row[5]
        tp1, tp2 = row[6], row[7]
        size_pct, size_usd, unreal = row[8], row[9], row[10]
        flag_cls, flag_txt, tstop = row[11], row[12], row[13]
        trail_act = row[14] if len(row) > 14 else None
        trail_cb  = row[15] if len(row) > 15 else None
        buf = round((live - stop) / entry * 100, 2) if flag_cls != "blue" else None
        pnl_col = "#4ade80" if unreal >= 0 else "#f87171"
        flag_col = {"ok":"#4ade80","warn":"#facc15","bad":"#f87171","blue":"#5b9bff"}.get(flag_cls,"#8a93a6")
        trail_row = ""
        if trail_act:
            be_pct = (trail_act - entry) / entry * 100  # 1.5×ATR as % of entry
            trail_row = (
                f'<tr><td class="mute">Trail&#9733; activate (1.5&times;ATR)</td>'
                f'<td style="text-align:right;color:#facc15;font-weight:600">{trail_act} &nbsp;<span style="color:#8a93a6;font-weight:400">(+{be_pct:.2f}% from entry &rarr; BE)</span></td></tr>'
                f'<tr><td class="mute">Chandelier cb% (3&times;ATR)</td>'
                f'<td style="text-align:right;color:#5b9bff">{trail_cb:.1f}% from HH</td></tr>'
            )
        cards += (
            f'<div class="card pos-card">'
            f'<div style="display:flex;justify-content:space-between">'
            f'<span class="lbl">{pid} &mdash; {side}</span>'
            f'<span class="pill {"green" if flag_cls=="ok" else "yellow" if flag_cls=="warn" else "red" if flag_cls=="bad" else "blue"}" style="font-size:10px">{flag_cls.upper()}</span>'
            f'</div>'
            f'<div style="font-size:15px;font-weight:700;margin:4px 0">{asset}</div>'
            f'<div style="font-size:22px;font-weight:700;color:{pnl_col}">{unreal:+.2f}%</div>'
            f'<div class="mute" style="font-size:11px">Unrealized P&amp;L</div>'
            f'<table style="margin-top:8px;font-size:12px"><tbody>'
            f'<tr><td class="mute">Entry</td><td style="text-align:right">{entry}</td></tr>'
            f'<tr><td class="mute">Live (last known)</td><td style="text-align:right">{live}</td></tr>'
            f'<tr><td class="mute">Stop (Rule 1)</td><td style="text-align:right;color:#f87171">{stop}</td></tr>'
            f'<tr><td class="mute">Buffer to stop</td><td style="text-align:right;color:{"#4ade80" if buf and buf>5 else "#facc15" if buf and buf>2 else "#f87171"}">{f"{buf:.2f}%" if buf is not None else "--"}</td></tr>'
            + trail_row +
            f'<tr><td class="mute">TP1 / TP2</td><td style="text-align:right">{tp1} / {tp2}</td></tr>'
            f'<tr><td class="mute">Size</td><td style="text-align:right">{size_pct:.2f}% risk &middot; {size_usd} notional &middot; <span style="color:#5b9bff">~${round(size_pct/100*PORT_NAV):,} risk$</span></td></tr>'
            f'<tr><td class="mute">Time-stop</td><td style="text-align:right">{tstop}</td></tr>'
            f'</tbody></table>'
            f'<div style="margin-top:8px;font-size:11px;color:{flag_col}">{flag_txt}</div>'
            f'</div>'
        )
    return f'<div class="pos-grid">{cards}</div>'

def heat_gauge_section():
    return (
        f'<div class="card" style="text-align:center">'
        f'<div class="lbl">Portfolio Heat</div>'
        f'<div class="chart-wrap" style="height:160px"><canvas id="heatGauge"></canvas></div>'
        f'<div style="font-size:20px;font-weight:700;margin-top:4px">{TOTAL_HEAT}% / {HEAT_CAP}%</div>'
        f'<div class="mute" style="font-size:12px">{TOTAL_HEAT/HEAT_CAP*100:.0f}% of cap used</div>'
        f'<div class="mute" style="font-size:12px;margin-top:4px">'
        f'~${round(TOTAL_HEAT*PORT_NAV/100):,} USDT at risk &nbsp;|&nbsp; NAV ${PORT_NAV:,} ({PORT_NAV_DATE})'
        f'</div>'
        f'</div>'
    )

def stop_buffer_section():
    return (
        f'<div class="card">'
        f'<div class="lbl">Stop Buffer (% of entry) &mdash; Open positions only</div>'
        f'<div class="chart-wrap" style="height:160px"><canvas id="stopBuffer"></canvas></div>'
        f'<div class="mute" style="font-size:11px;margin-top:4px">'
        f'<span style="color:#4ade80">&#9632;</span> &gt;5% safe &nbsp;'
        f'<span style="color:#facc15">&#9632;</span> 2-5% monitor &nbsp;'
        f'<span style="color:#f87171">&#9632;</span> &lt;2% urgent</div>'
        f'</div>'
    )


# §3 Exec Summary
def exec_summary_html():
    return ('<div class="grid grid-4">'
            + "".join(card(*c) for c in EXEC_CARDS)
            + '</div>')


# §4 Overlay Gate
def gate_html():
    rows = "".join(
        f'<tr><td>{sl}</td><td>{a}</td><td>{rd}</td><td>{pill(cls,txt)}</td></tr>\n'
        for sl, a, rd, cls, txt in GATE_ROWS
    )
    return (f'<table><tr><th>Sleeve</th><th>Asset</th><th>vs 10m-SMA</th><th>Gate</th></tr>\n'
            f'{rows}</table>'
            f'<div class="mute" style="font-size:12px;margin-top:6px">{GATE_NOTE}</div>')


# §5 Data & Variables
def vars_html():
    rows = "".join(
        f'<tr><td>{v}</td><td>{r}</td><td>{g}</td><td>{pill(cls,st)}</td><td>{imp}</td></tr>\n'
        for v,r,g,cls,st,imp in KEY_VARS
    )
    return (f'<table><tr><th>Variable</th><th>Reading</th><th>Grade</th>'
            f'<th>Status</th><th>Score Impact</th></tr>\n{rows}</table>')

def audit_html():
    rows = "".join(
        f'<tr><td>{vid}</td><td>{var}</td><td>{pill(sc,st)}</td><td>{pill(dc,dt)}</td></tr>\n'
        for vid,var,sc,st,dc,dt in AUDIT_ROWS
    )
    return (f'<h3>Audit Additions (binding 2026-04-14 | review 2026-10-14)</h3>'
            f'<table><tr><th>ID</th><th>Variable</th><th>Status</th><th>Decision-Moving?</th></tr>\n'
            f'{rows}</table>')

def v026_bar_section():
    return (f'<h3>V026 Residual Momentum &mdash; Full Equity Universe (FF5 12m)</h3>'
            f'<div class="chart-wrap" style="height:280px"><canvas id="residualBar"></canvas></div>')

def v026_table_html():
    rows = ""
    for ticker, resid, t_score, note in V026_RESIDUALS:
        if resid is not None:
            bar_pct = max(0, min(100, (resid + 40) / 80 * 100))
            bc = "#4ade80" if resid > 2 else "#f87171" if resid < -2 else "#facc15"
            resid_html = (
                f'<span style="font-weight:600;color:{bc}">{resid:+.2f}%</span>'
                f'<div style="display:inline-block;width:60px;height:6px;background:#262b35;border-radius:3px;margin-left:8px;vertical-align:middle">'
                f'<div style="width:{bar_pct:.0f}%;height:100%;background:{bc};border-radius:3px"></div></div>'
            )
            tc = "#4ade80" if t_score=="+1" else "#f87171" if t_score=="-1" else "#facc15"
            t_html = f'<span style="font-weight:600;color:{tc}">{t_score}</span>'
        else:
            resid_html = '<span class="mute">--</span>'
            tc = "#8a93a6"
            t_html = f'<span class="mute">{t_score}</span>'
        rows += f'<tr><td><b>{ticker}</b></td><td>{resid_html}</td><td>{t_html}</td><td style="font-size:12px;color:#8a93a6">{note}</td></tr>\n'
    return (f'<table><tr><th>Ticker</th><th>Residual % (FF5 12m)</th><th>T</th><th>Signal Note</th></tr>\n'
            f'{rows}</table>'
            f'<div class="mute" style="font-size:11px;margin-top:4px">Threshold: T=+1 if &gt;+2% | T=0 if within &plusmn;2% | T=&minus;1 if &lt;&minus;2%</div>')

def meta_html():
    rows = "".join(
        f'<tr><td>{vid}</td><td>{var}</td><td>{pill(sc,st)}</td><td>{dm}</td></tr>\n'
        for vid,var,sc,st,dm in META_ROWS
    )
    return (f'<h3>Meta Additions (binding 2026-04-18)</h3>'
            f'<table><tr><th>ID</th><th>Variable</th><th>Status</th><th>Decision-Moving?</th></tr>\n'
            f'{rows}</table>')


# §6 Score Analysis
def score_charts_html():
    return (
        f'<div class="grid grid-3">'
        f'<div class="card"><h3 style="margin-top:0">Promoted |Sum|&ge;3 &mdash; S/T/C/R</h3>'
        f'<div class="chart-wrap"><canvas id="scoreBar"></canvas></div></div>'
        f'<div class="card"><h3 style="margin-top:0">Near-Miss |Sum|=3 (blocked)</h3>'
        f'<div class="chart-wrap"><canvas id="nearMissBar"></canvas></div></div>'
        f'<div class="card"><h3 style="margin-top:0">Factor Radar &mdash; Portfolio Weighted</h3>'
        f'<div class="chart-wrap"><canvas id="factorRadar"></canvas></div></div>'
        f'</div>'
    )

def factor_table_html():
    def bar(val, color):
        pct = int(val * 100)
        return (f'<div style="display:flex;align-items:center;gap:8px">'
                f'<div style="flex:1;height:8px;background:#262b35;border-radius:4px">'
                f'<div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div></div>'
                f'<span style="font-size:12px;color:{color};width:36px">{val:.2f}</span></div>')
    pos_rows = ""
    for pid, asset, status, size, S, T, C, R in FACTOR_EXPOSURE:
        pos_rows += (f'<tr><td>{pid}</td><td>{asset}</td>'
                     f'<td style="color:#8a93a6;font-size:12px">{status}</td>'
                     f'<td>{size:.2f}%</td>'
                     f'<td style="color:#4ade80">{S}</td>'
                     f'<td style="color:#5b9bff">{T}</td>'
                     f'<td style="color:#facc15">{C}</td>'
                     f'<td style="color:#a78bfa">{R}</td></tr>\n')
    pos_rows += (f'<tr style="background:#1a1e27;font-weight:600">'
                 f'<td colspan="3">Portfolio weighted avg ({_fe_total:.2f}% heat)</td><td></td>'
                 f'<td style="color:#4ade80">{FACTOR_WS:.2f}</td>'
                 f'<td style="color:#5b9bff">{FACTOR_WT:.2f}</td>'
                 f'<td style="color:#facc15">{FACTOR_WC:.2f}</td>'
                 f'<td style="color:#a78bfa">{FACTOR_WR:.2f}</td></tr>\n')
    tilt = []
    if FACTOR_WS > 0.9: tilt.append("signal-heavy")
    if FACTOR_WT < 0.6: tilt.append('<span style="color:#facc15">trend-light (C=0 dominant)</span>')
    if FACTOR_WC < 0.3: tilt.append('<span style="color:#facc15">catalyst-light</span>')
    if FACTOR_WR > 0.9: tilt.append("strong risk backdrop (R Grade A triple)")
    bars_html = (
        f'<div style="padding:4px 0">'
        f'<div style="margin:5px 0"><span style="display:inline-block;width:90px;font-size:12px;color:#8a93a6">S (Signal)</span>{bar(FACTOR_WS,"#4ade80")}</div>'
        f'<div style="margin:5px 0"><span style="display:inline-block;width:90px;font-size:12px;color:#8a93a6">T (Trend)</span>{bar(FACTOR_WT,"#5b9bff")}</div>'
        f'<div style="margin:5px 0"><span style="display:inline-block;width:90px;font-size:12px;color:#8a93a6">C (Catalyst)</span>{bar(FACTOR_WC,"#facc15")}</div>'
        f'<div style="margin:5px 0"><span style="display:inline-block;width:90px;font-size:12px;color:#8a93a6">R (Risk)</span>{bar(FACTOR_WR,"#a78bfa")}</div>'
        f'</div>'
    )
    return (
        f'<div class="grid grid-2" style="margin-top:12px">'
        f'<div class="card"><h3 style="margin-top:0">Factor Tilt (size-weighted)</h3>'
        f'{bars_html}'
        f'<div style="font-size:12px;color:#8a93a6;margin-top:8px">Bias: {" | ".join(tilt) if tilt else "balanced"}</div>'
        f'</div>'
        f'<div class="card"><h3 style="margin-top:0">Position Breakdown</h3>'
        f'<table style="margin-top:0">'
        f'<tr><th>ID</th><th>Asset</th><th>Status</th><th>Size%</th>'
        f'<th style="color:#4ade80">S</th><th style="color:#5b9bff">T</th>'
        f'<th style="color:#facc15">C</th><th style="color:#a78bfa">R</th></tr>\n'
        f'{pos_rows}</table></div></div>'
    )


# §7 Delta Box
def delta_html():
    if not DELTA_ITEMS:
        return ''
    cols = "".join(f'<div>{item}</div>' for item in DELTA_ITEMS)
    foot = (f'<div class="mute" style="margin-top:10px;font-size:13px">{DELTA_FOOT}</div>'
            if DELTA_FOOT else "")
    return (f'<div class="delta-box">'
            f'<h3>&#9889; Material change vs prior run</h3>'
            f'<div class="grid grid-3" style="margin-top:8px">{cols}</div>'
            f'{foot}</div>')


# §2b Trade Management — Pure Runner Panel
def trade_mgmt_html():
    """Pure runner trade management: three binding rules per open position."""
    if not OPEN_POSITIONS:
        return '<div class="mute">No open positions.</div>'
    rationale = (
        '<div style="background:rgba(91,155,255,.04);border:1px solid rgba(91,155,255,.2);'
        'border-radius:6px;padding:8px 12px;margin-bottom:10px;font-size:12px;color:#8a93a6">'
        '<b style="color:#5b9bff">Exit Architecture &mdash; Pure Runner (Grade A, binding all assets)</b> &nbsp;&middot;&nbsp; '
        'No partial exits. Returns are power-law distributed: top ~10% of trades drive all cumulative P&amp;L. '
        'Partial exits truncate the right tail. Academic TF (Hurst/Ooi/Pedersen 2017, 137yr&times;67 mkts) uses '
        'trailing stops with no partial exits. Win rate 35&ndash;40% is only viable if outlier winners run to full extension.'
        '</div>'
    )
    rows = ""
    for row in OPEN_POSITIONS:
        pid, asset = row[0], row[1]
        entry, stop = row[3], row[5]
        flag_cls = row[11]
        trail_act = row[14] if len(row) > 14 else None
        trail_cb  = row[15] if len(row) > 15 else None
        is_pending = flag_cls == "blue"
        r1 = f'Hold stop at <span style="color:#f87171;font-weight:600">{stop}</span>'
        if trail_act:
            r2 = f'Move stop &rarr; <span style="color:#facc15;font-weight:700">{entry}</span> (breakeven) when price &ge; <span style="color:#facc15;font-weight:700">{trail_act}</span>'
            r3 = f'Highest high &minus; <span style="color:#5b9bff;font-weight:700">{trail_cb:.1f}%</span> callback from each new high'
        else:
            r2 = 'Calc at fill: entry + 1.5&times;ATR'
            r3 = 'Calc at fill: 3&times;ATR / trail_activate &times; 100'
        status_badge = '<span class="pill blue" style="font-size:10px">PENDING</span>' if is_pending else ''
        rows += (
            f'<tr>'
            f'<td><b>{pid}</b> {status_badge}<br><span class="mute" style="font-size:11px">{asset}</span></td>'
            f'<td style="font-size:12px">{r1}</td>'
            f'<td style="font-size:12px">{r2}</td>'
            f'<td style="font-size:12px">{r3}</td>'
            f'</tr>\n'
        )
    return (
        rationale +
        f'<table><tr>'
        f'<th>Position</th>'
        f'<th>Rule 1 &mdash; Hold stop</th>'
        f'<th>Rule 2 &mdash; Breakeven trigger &#9733; <span style="color:#facc15">mandatory</span></th>'
        f'<th>Rule 3 &mdash; Chandelier trail</th>'
        f'</tr>\n{rows}</table>'
        f'<div class="mute" style="font-size:11px;margin-top:6px">'
        f'&#9733; = mandatory action at that price. No partial exit &mdash; full size retained. '
        f'Chandelier fires if price retraces &gt;trail_cb% from highest high after activation. '
        f'Once chandelier stop rises above entry naturally (&asymp;+3&times;ATR HH), it supersedes the breakeven rule.</div>'
    )


# §8 Recommendations
def recs_html():
    hdr = ('<tr><th>Asset</th><th>Dir</th><th>Entry</th><th>Stop</th>'
           '<th style="color:#facc15">Trail&#9733;</th>'
           '<th>Target</th><th>Enter (USDT)</th><th>Catalyst</th><th>Grade</th><th>Sleeve</th></tr>')
    rows = ""
    if RECS:
        for rec in RECS:
            asset, dir_cls, entry, stop, target, size, catalyst, grade, sleeve = rec[:9]
            notional = rec[9] if len(rec) > 9 else None
            trail    = rec[10] if len(rec) > 10 else "--"
            if notional:
                size_cell = (f'<span style="font-size:15px;font-weight:700;color:#4ade80">~${notional:,} USDT</span>'
                             f'<br><span style="color:#8a93a6;font-size:11px">{size}</span>')
            else:
                size_cell = size
            rows += (f'<tr style="background:rgba(74,222,128,.04)">'
                     f'<td>{asset}</td><td>{pill(dir_cls,"LONG")}</td>'
                     f'<td>{entry}</td><td>{stop}</td>'
                     f'<td style="color:#facc15;font-size:12px;font-weight:600">{trail}</td>'
                     f'<td>{target}</td><td>{size_cell}</td>'
                     f'<td style="font-size:12px">{catalyst}</td>'
                     f'<td style="font-size:12px;color:#b5bccc">{grade}</td>'
                     f'<td style="font-size:12px">{sleeve}</td></tr>\n')
    else:
        rows += f'<tr><td colspan="10" class="mute" style="text-align:center;padding:16px">No new promotions this run.</td></tr>\n'
    if RECS_CARRY:
        rows += f'<tr><td colspan="10" style="background:#12151c;color:#8a93a6;font-size:11px;padding:5px 10px;letter-spacing:.04em">CARRY-OVER PENDING (previously promoted)</td></tr>\n'
        for rec in RECS_CARRY:
            a_c, e_c, s_c, t_c, sz_c, cat_c = rec[:6]
            notional_c = rec[6] if len(rec) > 6 else None
            trail_c    = rec[7] if len(rec) > 7 else "--"
            if notional_c:
                sz_html = (f'<span style="font-size:14px;font-weight:700;color:#5b9bff">~${notional_c:,} USDT</span>'
                           f'<br><span style="color:#8a93a6;font-size:11px">{sz_c}</span>')
            else:
                sz_html = f'<span style="font-size:12px">{sz_c}</span>'
            rows += (f'<tr style="opacity:0.8"><td>{a_c}</td><td>{pill("blue","--")}</td>'
                     f'<td style="font-size:12px">{e_c}</td><td style="font-size:12px">{s_c}</td>'
                     f'<td style="color:#facc15;font-size:12px">{trail_c}</td>'
                     f'<td style="font-size:12px">{t_c}</td><td>{sz_html}</td>'
                     f'<td style="font-size:12px">{cat_c}</td><td></td><td></td></tr>\n')
    if RECS_BLOCKED:
        rows += f'<tr><td colspan="10" style="background:#12151c;color:#f87171;font-size:11px;padding:5px 10px;letter-spacing:.04em">GATE-BLOCKED / NEAR-MISS (Sum&ge;3 but blocked)</td></tr>\n'
        for asset, dir_txt, entry, stop, target, size, catalyst, grade, sleeve in RECS_BLOCKED:
            rows += (f'<tr style="opacity:0.55"><td>{asset}</td><td>{dir_txt}</td>'
                     f'<td>{entry}</td><td>{stop}</td><td class="mute">--</td>'
                     f'<td>{target}</td><td>{size}</td>'
                     f'<td style="font-size:12px">{catalyst}</td>'
                     f'<td style="font-size:12px;color:#b5bccc">{grade}</td>'
                     f'<td style="font-size:12px">{sleeve}</td></tr>\n')
    return (f'<table>\n{hdr}\n{rows}</table>\n'
            f'<div class="mute" style="font-size:12px;margin-top:6px">'
            f'&#9733; Trail = breakeven trigger price (+chandelier callback%). Move stop to entry the moment this level prints. No partial exit &mdash; full size retained.<br>'
            f'{RECS_FOOTNOTE}</div>')


# §9 Signal Age
def signal_age_html():
    rows = ""
    for sid, asset, status, prom, days, expiry, rem, urgency in SIGNAL_AGE:
        bar_pct = min(100, int(rem / 90 * 100))
        bc = {"ok":"#4ade80","warn":"#facc15","bad":"#f87171"}.get(urgency,"#8a93a6")
        countdown = (f'<span style="font-weight:600;color:{bc}">{rem}d</span>'
                     f'<div style="display:inline-block;width:60px;height:6px;background:#262b35;border-radius:3px;margin-left:8px;vertical-align:middle">'
                     f'<div style="width:{bar_pct}%;height:100%;background:{bc};border-radius:3px"></div></div>')
        rows += (f'<tr><td>{sid}</td><td><b>{asset}</b></td>'
                 f'<td style="font-size:12px;color:#8a93a6">{status}</td>'
                 f'<td>{prom}</td><td class="mute">{days}d</td>'
                 f'<td>{expiry}</td><td>{countdown}</td></tr>\n')
    return (f'<div class="grid grid-2">'
            f'<div class="card"><h3 style="margin-top:0">Signal Age Timeline</h3>'
            f'<div class="chart-wrap"><canvas id="signalAge"></canvas></div>'
            f'<div class="mute" style="font-size:11px;margin-top:4px">'
            f'<span style="color:#4ade80">&#9632;</span> &ge;20d OK &nbsp;'
            f'<span style="color:#facc15">&#9632;</span> 10-19d monitor &nbsp;'
            f'<span style="color:#f87171">&#9632;</span> &lt;10d urgent</div>'
            f'</div>'
            f'<div class="card"><h3 style="margin-top:0">Signal Age Detail</h3>'
            f'<table style="margin-top:0">'
            f'<tr><th>ID</th><th>Asset</th><th>Status</th><th>Promoted</th><th>Age</th><th>Expiry</th><th>Remaining</th></tr>\n'
            f'{rows}</table></div></div>')


# §10 Thesis Summary
def thesis_html():
    if not THESIS:
        return '<div class="mute">No thesis entries.</div>'
    items = ""
    for sid, text in THESIS.items():
        # Split on double-newlines for multi-paragraph theses; fall back to single paragraph
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            paragraphs = [text]
        paras_html = "".join(
            f'<p style="font-size:13px;line-height:1.7;margin:0 0 8px 0">{p}</p>'
            for p in paragraphs
        )
        items += (f'<div class="card" style="margin-bottom:8px">'
                  f'<div class="lbl">{sid}</div>'
                  f'<div style="margin-top:6px">{paras_html}</div>'
                  f'</div>')
    return items


# §11 Checklists
def checklists_html():
    if not CHECKLISTS:
        return '<div class="mute">No pre-entry checklists this run.</div>'
    out = ""
    for title, note, rows in CHECKLISTS:
        out += f'<h3>{title}</h3>\n'
        if note:
            out += f'<div class="mute" style="font-size:12px;margin-bottom:8px">{note}</div>\n'
        out += '<table><tr><th>#</th><th>Item</th><th>Status</th><th>Detail</th></tr>\n'
        for num, item, cls, icon, detail in rows:
            cls_map = {"ok":"color:var(--ok)","warn":"color:var(--warn)","bad":"color:var(--bad)"}
            out += (f'<tr><td style="color:#8a93a6">{num}</td><td>{item}</td>'
                    f'<td style="{cls_map.get(cls,"")};font-weight:600">{icon}</td>'
                    f'<td style="font-size:12px">{detail}</td></tr>\n')
        out += '</table>\n'
    return out


# §12 Regime Sensitivity
def sensitivity_html():
    if not SENSITIVITY:
        return '<div class="mute">No sensitivity data this run.</div>'
    hdr_cells = "".join(
        f'<th style="color:{"var(--ok)" if c=="ok" else "var(--warn)" if c=="warn" else "var(--bad)"}">{h}</th>'
        for h, c in SCENARIOS
    )
    rows = ""
    for sid, asset, impacts in SENSITIVITY:
        cells = ""
        for ic, it in impacts:
            bg = {"ok":"rgba(74,222,128,.06)","warn":"rgba(250,204,21,.06)","bad":"rgba(248,113,113,.08)"}.get(ic,"")
            tc = {"ok":"#4ade80","warn":"#facc15","bad":"#f87171"}.get(ic,"var(--fg)")
            cells += f'<td style="font-size:12px;background:{bg};color:{tc}">{it}</td>'
        rows += f'<tr><td><b>{sid}</b> <span class="mute" style="font-size:12px">{asset}</span></td>{cells}</tr>\n'
    return (f'<div style="overflow-x:auto">'
            f'<table style="min-width:750px"><tr><th>Position</th>{hdr_cells}</tr>\n{rows}</table></div>'
            f'<div class="mute" style="font-size:12px;margin-top:4px">'
            f'<span style="color:#4ade80">&#9632;</span> neutral/positive &nbsp;'
            f'<span style="color:#facc15">&#9632;</span> monitor/indirect &nbsp;'
            f'<span style="color:#f87171">&#9632;</span> direct stop/exit risk</div>')


# §13 Catalyst Calendar
def catalyst_html():
    rows = "".join(
        f'<tr><td>{dt}</td><td>{ev}</td><td>{assets}</td><td>{pill(cls,ptxt)}</td></tr>\n'
        for dt, ev, assets, cls, ptxt in CATALYSTS
    )
    return (f'<div class="chart-wrap" style="height:180px"><canvas id="catCal"></canvas></div>\n'
            f'<table style="margin-top:10px">'
            f'<tr><th>Date</th><th>Event</th><th>Assets</th><th>Priority</th></tr>\n'
            f'{rows}</table>')


# §14 Near-Misses
def near_miss_html():
    if not NEAR_MISSES:
        return '<div class="mute">No near-misses this run.</div>'
    rows = "".join(
        f'<tr><td>{a}</td><td style="color:var(--accent);font-weight:700">{sv}</td>'
        f'<td style="font-size:12px">{blk}</td><td style="font-size:12px">{trig}</td><td>{nid}</td></tr>\n'
        for a, sv, blk, trig, nid in NEAR_MISSES
    )
    return (f'<table><tr><th>Asset</th><th>Sum</th><th>Block Reason</th>'
            f'<th>Promotion Trigger</th><th>ID</th></tr>\n{rows}</table>')


# §15 Closed Trade Context
def closed_context_html():
    if not CLOSED_CONTEXT:
        return '<div class="mute">No closed-trade context this run.</div>'
    out = ""
    for section_label, asset_tag, trades in CLOSED_CONTEXT:
        out += f'<h3>{section_label}</h3>\n'
        if not trades:
            out += f'<div class="mute">No prior closed trades for {asset_tag}.</div>\n'
            continue
        out += ('<table><tr><th>ID</th><th>Side</th><th>Opened</th><th>Closed</th>'
                '<th>Hold</th><th>P&amp;L</th><th>Exit Reason</th></tr>\n')
        for tid, side, opened, closed, days, pnl, pnl_cls, reason in trades:
            pc = {"ok":"var(--ok)","warn":"var(--warn)","bad":"var(--bad)"}.get(pnl_cls,"")
            out += (f'<tr><td>{tid}</td><td>{side}</td><td>{opened}</td><td>{closed}</td>'
                    f'<td>{days}d</td><td style="color:{pc};font-weight:600">{pnl}</td>'
                    f'<td style="font-size:12px">{reason}</td></tr>\n')
        out += '</table>\n'
    if CLOSED_NOTE:
        out += f'<div class="mute" style="font-size:12px;margin-top:6px">{CLOSED_NOTE}</div>\n'
    return out


# §16 Asset Universe
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
    return '<div class="card">' + "\n".join(parts) + '</div>'


# §17 Data Gap
def gap_html():
    ul = "".join(
        f'<li style="color:{"var(--ok)" if cls=="ok" else "var(--warn)" if cls=="warn" else "var(--bad)"}">{txt}</li>'
        for cls, txt in UPSTREAM
    )
    return (f'<div class="grid grid-2">'
            f'<div class="card"><h3 style="margin-top:0">Grade A Coverage</h3>'
            f'<div class="chart-wrap" style="height:200px"><canvas id="gapDoughnut"></canvas></div>'
            f'<div class="mute" style="font-size:12px;text-align:center;margin-top:4px">'
            f'LIVE {GAP_DATA[0]} | STALE {GAP_DATA[1]} | MISSING {GAP_DATA[2]}</div></div>'
            f'<div class="card"><h3 style="margin-top:0">Upstream Artifact Coverage</h3>'
            f'<ul style="font-size:12px">{ul}</ul></div></div>')


# §18 Discussion
def discussion_html():
    return '<div class="card">' + "".join(f'<p>{p}</p>' for p in DISCUSSION) + '</div>'


# §19 Memory Updates
def memory_html():
    return ('<ul style="font-size:13px">'
            + "".join(f'<li>{u}</li>' for u in MEMORY_UPDATES)
            + '</ul>')


# ── Chart.js Data ─────────────────────────────────────────────────────────────
def chartjs_html():
    def ja(lst): return "[" + ",".join(str(x) for x in lst) + "]"
    def js(lst): return "[" + ",".join(f"'{x}'" for x in lst) + "]"
    def jq(lst): return "[" + ",".join(f'"{x}"' for x in lst) + "]"

    # Signal Age chart
    sa_labels = [f"{s[0]} {s[1]}" for s in SIGNAL_AGE]
    sa_data   = [s[6] for s in SIGNAL_AGE]
    sa_urg    = [s[7] for s in SIGNAL_AGE]
    sa_bg  = ['"rgba(74,222,128,.3)"' if u=="ok" else '"rgba(250,204,21,.3)"' if u=="warn" else '"rgba(248,113,113,.3)"' for u in sa_urg]
    sa_bd  = ['"#4ade80"' if u=="ok" else '"#facc15"' if u=="warn" else '"#f87171"' for u in sa_urg]

    # V026 residual chart
    v_data = [(r[0], r[1]) for r in V026_RESIDUALS if r[1] is not None]
    vl = [t[0] for t in v_data]; vv = [t[1] for t in v_data]
    v_bg = ['"rgba(74,222,128,.3)"' if v>2 else '"rgba(248,113,113,.3)"' if v<-2 else '"rgba(250,204,21,.3)"' for v in vv]
    v_bd = ['"#4ade80"' if v>2 else '"#f87171"' if v<-2 else '"#facc15"' for v in vv]

    # Stop buffer (open positions only; flag_cls != blue)
    open_p = [p for p in OPEN_POSITIONS if p[11] != "blue"]
    sb_labels = [f"{p[0]} {p[1]}" for p in open_p]
    sb_data   = [round((p[4]-p[5])/p[3]*100, 2) for p in open_p]
    sb_bg = ['"rgba(74,222,128,.3)"' if b>5 else '"rgba(250,204,21,.3)"' if b>2 else '"rgba(248,113,113,.3)"' for b in sb_data]
    sb_bd = ['"#4ade80"' if b>5 else '"#facc15"' if b>2 else '"#f87171"' for b in sb_data]

    ws, wt, wc, wr = FACTOR_WS, FACTOR_WT, FACTOR_WC, FACTOR_WR
    heat_used = TOTAL_HEAT; heat_avail = round(HEAT_CAP - TOTAL_HEAT, 2)

    return f'''<script>
const DS = (lbl,data,bg,bd) => ({{label:lbl,data,backgroundColor:bg,borderColor:bd,borderWidth:1}});
const hBar = {{
  indexAxis:'y',responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{display:false}}}},
  scales:{{
    x:{{ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}}}},
    y:{{ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}
  }}
}};
const stackedHBar = {{
  indexAxis:'y',responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{labels:{{color:'#e5e9f0'}}}}}},
  scales:{{
    x:{{stacked:true,min:0,max:4,ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}}}},
    y:{{stacked:true,ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}
  }}
}};

// 1. Score stacking -- promoted
new Chart(document.getElementById('scoreBar'),{{
  type:'bar',
  data:{{labels:{js(SCORE_LABELS)},datasets:[
    DS('S',{ja(SCORE_S)},'#4ade80','#4ade80'),
    DS('T',{ja(SCORE_T)},'#5b9bff','#5b9bff'),
    DS('C',{ja(SCORE_C)},'#facc15','#facc15'),
    DS('R',{ja(SCORE_R)},'#a78bfa','#a78bfa')
  ]}},options:stackedHBar
}});

// 2. Score stacking -- near-miss
new Chart(document.getElementById('nearMissBar'),{{
  type:'bar',
  data:{{labels:{js(NEAR_LABELS)},datasets:[
    DS('S',{ja(NEAR_S)},'#4ade80','#4ade80'),
    DS('T',{ja(NEAR_T)},'#5b9bff','#5b9bff'),
    DS('C',{ja(NEAR_C)},'#facc15','#facc15'),
    DS('R',{ja(NEAR_R)},'#a78bfa','#a78bfa')
  ]}},options:stackedHBar
}});

// 3. Factor Radar
new Chart(document.getElementById('factorRadar'),{{
  type:'radar',
  data:{{
    labels:['S (Signal)','T (Trend)','C (Catalyst)','R (Risk)'],
    datasets:[{{
      label:'Portfolio Weighted',
      data:[{ws},{wt},{wc},{wr}],
      backgroundColor:'rgba(91,155,255,.15)',
      borderColor:'#5b9bff',
      pointBackgroundColor:'#5b9bff',
      borderWidth:2
    }}]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    scales:{{r:{{
      beginAtZero:true,max:1,
      ticks:{{color:'#8a93a6',stepSize:0.25,backdropColor:'transparent'}},
      grid:{{color:'#262b35'}},
      pointLabels:{{color:'#e5e9f0',font:{{size:12}}}},
      angleLines:{{color:'#262b35'}}
    }}}},
    plugins:{{legend:{{labels:{{color:'#e5e9f0'}}}}}}
  }}
}});

// 4. V026 Residual Momentum bar
new Chart(document.getElementById('residualBar'),{{
  type:'bar',
  data:{{
    labels:{js(vl)},
    datasets:[{{
      label:'V026 Residual % (FF5 12m)',
      data:{ja(vv)},
      backgroundColor:[{",".join(v_bg)}],
      borderColor:[{",".join(v_bd)}],
      borderWidth:1
    }}]
  }},
  options:{{
    indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{min:-42,max:20,ticks:{{color:'#8a93a6',callback:v=>v+'%'}},grid:{{color:'#262b35'}},
          title:{{display:true,text:'Residual % (FF5 12m)',color:'#8a93a6'}}}},
      y:{{ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}
    }}
  }}
}});

// 5. Portfolio heat gauge
new Chart(document.getElementById('heatGauge'),{{
  type:'doughnut',
  data:{{
    labels:['Heat Used ({heat_used}%)','Available ({heat_avail}%)'],
    datasets:[{{
      data:[{heat_used},{heat_avail}],
      backgroundColor:['rgba(91,155,255,.7)','rgba(38,43,53,.9)'],
      borderColor:['#5b9bff','#262b35'],
      borderWidth:2
    }}]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    cutout:'65%',
    plugins:{{legend:{{labels:{{color:'#e5e9f0',font:{{size:11}}}}}}}}
  }}
}});

// 6. Stop buffer chart
new Chart(document.getElementById('stopBuffer'),{{
  type:'bar',
  data:{{
    labels:{js(sb_labels)},
    datasets:[{{
      label:'Stop Buffer % of Entry',
      data:{ja(sb_data)},
      backgroundColor:[{",".join(sb_bg)}],
      borderColor:[{",".join(sb_bd)}],
      borderWidth:1
    }}]
  }},
  options:{{
    indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{min:0,ticks:{{color:'#8a93a6',callback:v=>v+'%'}},grid:{{color:'#262b35'}},
          title:{{display:true,text:'Buffer to Stop (% of entry)',color:'#8a93a6'}}}},
      y:{{ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}
    }}
  }}
}});

// 7. Catalyst calendar
new Chart(document.getElementById('catCal'),{{
  type:'bar',
  data:{{
    labels:{js(CAT_LABELS)},
    datasets:[{{
      label:'Priority (1=MED 2=HIGH)',
      data:{ja(CAT_DATA)},
      backgroundColor:{jq(CAT_COLORS)},
      borderColor:'#262b35',borderWidth:1
    }}]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{ticks:{{color:'#8a93a6'}},grid:{{color:'#262b35'}}}},
      y:{{min:0,max:3,ticks:{{color:'#8a93a6',stepSize:1}},grid:{{color:'#262b35'}}}}
    }}
  }}
}});

// 8. Data gap doughnut
new Chart(document.getElementById('gapDoughnut'),{{
  type:'doughnut',
  data:{{
    labels:['Grade A LIVE','Grade A STALE','Grade A MISSING'],
    datasets:[{{
      data:{ja(GAP_DATA)},
      backgroundColor:['#4ade80','#facc15','#f87171'],
      borderColor:'#171a21',borderWidth:2
    }}]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    cutout:'50%',
    plugins:{{legend:{{labels:{{color:'#e5e9f0'}}}}}}
  }}
}});

// 9. Signal age chart
new Chart(document.getElementById('signalAge'),{{
  type:'bar',
  data:{{
    labels:{js(sa_labels)},
    datasets:[{{
      label:'Days Remaining',
      data:{ja(sa_data)},
      backgroundColor:[{",".join(sa_bg)}],
      borderColor:[{",".join(sa_bd)}],
      borderWidth:1
    }}]
  }},
  options:{{
    indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{min:0,ticks:{{color:'#8a93a6',callback:v=>v+'d'}},grid:{{color:'#262b35'}}}},
      y:{{ticks:{{color:'#e5e9f0'}},grid:{{color:'#262b35'}}}}
    }}
  }}
}});
</script>'''


# ══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE — fixed 20-section order, never changes
# ══════════════════════════════════════════════════════════════════════════════

out_path = Path(f"{TODAY}/report-{TODAY}-trade-rec.html")

css = """
:root{--bg:#0f1115;--card:#171a21;--muted:#8a93a6;--fg:#e5e9f0;--accent:#5b9bff;
      --ok:#4ade80;--warn:#facc15;--bad:#f87171;--border:#262b35;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
     background:var(--bg);color:var(--fg);line-height:1.5}
.container{max-width:1240px;margin:0 auto;padding:28px 20px}
h1{font-size:24px;margin:0 0 4px}
h2{font-size:17px;margin:32px 0 10px;color:var(--accent);border-bottom:1px solid var(--border);
   padding-bottom:6px;letter-spacing:.02em}
h3{font-size:14px;margin:16px 0 8px;color:#b5bccc}
section{margin-bottom:6px}
.sub{color:var(--muted);font-size:13px;margin-bottom:12px}
.mute{color:var(--muted)}
.lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.val{font-size:20px;margin-top:4px}
/* Grids */
.grid{display:grid;gap:12px}
.grid-2{grid-template-columns:1fr 1fr}
.grid-3{grid-template-columns:repeat(3,1fr)}
.grid-4{grid-template-columns:repeat(4,1fr)}
/* Card */
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
/* Positions */
.pos-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.pos-card{}
/* Table */
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}
th{color:var(--muted);font-weight:500;background:#12151c}
tr:hover td{background:#1a1e27}
/* Pills */
.pill{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:500}
.pill.green{background:rgba(74,222,128,.15);color:var(--ok)}
.pill.red{background:rgba(248,113,113,.15);color:var(--bad)}
.pill.yellow{background:rgba(250,204,21,.15);color:var(--warn)}
.pill.blue{background:rgba(91,155,255,.15);color:var(--accent)}
.pill.gray{background:#262b35;color:var(--muted)}
.pill.purple{background:rgba(167,139,250,.15);color:#a78bfa}
/* Charts */
.chart-wrap{position:relative;height:260px}
/* Colors */
.ok{color:var(--ok)} .warn{color:var(--warn)} .bad{color:var(--bad)}
/* Freshness strip */
.fresh-strip{display:flex;gap:8px;overflow-x:auto;padding:2px 0 10px 0;
             scrollbar-width:thin;scrollbar-color:#262b35 transparent}
.fresh-item{background:var(--card);border:1px solid var(--border);border-radius:8px;
            padding:8px 10px;min-width:110px;flex:0 0 auto}
.fresh-var{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.fresh-val{font-size:14px;font-weight:600;margin:2px 0}
.fresh-grade{font-size:10px;font-weight:400;color:var(--muted)}
.fresh-note{font-size:10px;color:var(--muted)}
/* Position range */
.range-bar{display:flex;width:100%;height:20px;border-radius:4px;overflow:hidden;font-size:0;margin-bottom:4px}
.range-labels{position:relative;height:32px;font-size:10px;color:#8a93a6;margin-bottom:8px}
.range-labels span{position:absolute;white-space:nowrap;line-height:1.3}
/* Delta */
.delta-box{background:#0d1a2e;border:1px solid #1f6feb;border-radius:8px;padding:14px 18px;margin-bottom:18px}
.delta-box h3{color:#79c0ff;margin-top:0}
/* Status bar */
.status-bar{display:flex;align-items:center;gap:12px;padding:10px 16px;
            background:var(--card);border:1px solid var(--border);border-radius:8px;
            margin-bottom:16px;flex-wrap:wrap}
.status-bar .regime{font-size:13px;font-weight:600;color:var(--fg)}
.status-bar .regime-sub{font-size:12px;color:var(--muted)}
/* Footer */
.footer{color:var(--muted);font-size:12px;margin-top:24px;border-top:1px solid var(--border);
        padding-top:12px;line-height:1.8}
ul{margin:6px 0;padding-left:20px}
li{margin:3px 0}
p{margin:0 0 12px;line-height:1.65}
@media(max-width:800px){.grid-4{grid-template-columns:1fr 1fr}.grid-3{grid-template-columns:1fr}.grid-2{grid-template-columns:1fr}}
"""

STATUS_ICON = {"ok":"&#9679;","warn":"&#9651;","bad":"&#9888;"}.get(STATUS_CLS,"&#9679;")
STATUS_COLOR = {"ok":"var(--ok)","warn":"var(--warn)","bad":"var(--bad)"}.get(STATUS_CLS,"var(--fg)")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Trade Rec &mdash; {TODAY} {VERSION}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>{css}</style>
</head>
<body>
<div class="container">

<!-- HEADER -->
<h1>Trade Recommendation &mdash; {TODAY} <span class="pill blue">{VERSION}</span>
    <span class="pill {"green" if STATUS_CLS=="ok" else "yellow" if STATUS_CLS=="warn" else "red"}"
          style="font-size:13px;vertical-align:middle">{STATUS_ICON} {STATUS_TXT}</span></h1>
<div class="sub">Generated {GEN_TIME} &mdash; {SUPERSEDES}
  Miss: {MISS_COUNT} &nbsp;&middot;&nbsp; V026 {V026_ST} &nbsp;&middot;&nbsp; V027 {V027_ST}</div>

<!-- STATUS BAR -->
<div class="status-bar">
  <div>
    <div class="regime">{REGIME_LABEL}</div>
    <div class="regime-sub">{REGIME_SUB}</div>
  </div>
  <div style="flex:1"></div>
  <div style="font-size:12px;color:var(--muted)">Heat <span style="color:var(--accent);font-weight:600">{TOTAL_HEAT}% / {HEAT_CAP}%</span></div>
  <div style="font-size:12px;color:var(--muted)">Positions <span style="font-weight:600;color:var(--fg)">{len(OPEN_POSITIONS)}</span></div>
</div>

{section("1. Data Freshness", freshness_html(), "s1")}

<!-- §2 PORTFOLIO DASHBOARD -->
<section id="s2">
<h2>2. Portfolio Dashboard</h2>
<div class="grid grid-2" style="margin-bottom:12px">
  {heat_gauge_section()}
  {stop_buffer_section()}
</div>
{positions_cards_html()}
<h3>Price Level Range &mdash; Stop / Entry / Live / Trail&#9733; / Targets</h3>
<div class="card">{pos_range_html()}</div>
<h3>Pure Runner Trade Management &mdash; Three Binding Rules</h3>
<div class="card">{trade_mgmt_html()}</div>
</section>

{section("3. Executive Summary", exec_summary_html(), "s3")}

{section("4. Overlay Gate &mdash; Faber TAA (V033-V035)", gate_html(), "s4")}

<!-- §5 DATA & VARIABLES -->
<section id="s5">
<h2>5. Data Collected &mdash; Key Variables</h2>
{vars_html()}
{audit_html()}
{v026_bar_section()}
{v026_table_html()}
{meta_html()}
</section>

<!-- §6 SCORE ANALYSIS -->
<section id="s6">
<h2>6. Score Analysis</h2>
{score_charts_html()}
{factor_table_html()}
</section>

<!-- §7 DELTA -->
<section id="s7">
<h2>7. Material Change vs Prior Run</h2>
{delta_html() or '<div class="mute">No material changes from prior run (v1 run).</div>'}
</section>

{section("8. Recommendations", recs_html(), "s8")}

{section("9. Signal Age &amp; Time-Decay", signal_age_html(), "s9")}

<!-- §10 THESIS -->
<section id="s10">
<h2>10. Thesis Summary</h2>
{thesis_html()}
</section>

{section("11. Pre-Entry Checklists", checklists_html(), "s11")}

{section("12. Regime Sensitivity &mdash; Stress Test", sensitivity_html(), "s12")}

{section("13. Catalyst Calendar (rolling 2 weeks)", catalyst_html(), "s13")}

{section("14. Near-Misses (|Sum|&ge;3 not promoted)", near_miss_html(), "s14")}

{section("15. Closed-Trade Context", closed_context_html(), "s15")}

{section("16. Asset Universe", universe_html(), "s16")}

{section("17. Data Gap Closure", gap_html(), "s17")}

{section("18. Discussion", discussion_html(), "s18")}

<!-- §19 MEMORY UPDATES -->
<section id="s19">
<h2>19. Memory Updates Applied</h2>
{memory_html()}
</section>

<!-- §20 SOURCES & FOOTER -->
<section id="s20">
<h2>20. Sources</h2>
<div class="footer">
<b>Sources (local A):</b> {SOURCES_A}<br>
<b>Sources (cloud B):</b> {SOURCES_B}<br>
<br>
{VERSION} Authoritative &mdash; generated {GEN_TIME}<br>
Template: gen_trade_rec_html.py v3 &mdash; 20-section fixed layout | 9 charts | sections never change, only PER-RUN DATA
</div>
</section>

</div>
{chartjs_html()}
</body>
</html>"""

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")
print(f"HTML written: {out_path}  ({out_path.stat().st_size:,} bytes)")
