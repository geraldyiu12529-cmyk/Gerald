"""Positions Monitor HTML Generator — v2.
Rich per-position context: background, thesis, S/T/C/R scores, invalidation checklist.
Fixed template. Update only the PER-RUN DATA block for each run.
Run from Trade/ directory: python scripts/gen_positions_html.py
Output: {TODAY}/positions-monitor-{TODAY}.html
"""
from pathlib import Path

# ════════════════════════════════════════════════════════════════════════════
# PER-RUN DATA — skill updates ONLY this block each run
# ════════════════════════════════════════════════════════════════════════════

TODAY       = "2026-04-23"
GEN_TIME    = "2026-04-23 09:00 UTC+8"
SNAPSHOT    = "2026-04-23/us-close-snapshot-2026-04-23.md"
PORT_NAV    = 4300
TOTAL_HEAT  = 3.09
HEAT_CAP    = 8.0
HEAT_CLS    = "ok"   # "ok" <4% | "warn" 4-6% | "bad" >6%

REGIME_LABEL = "RISK-ON / OIL-ELEVATED"
REGIME_SUB   = "CEASEFIRE EXTENDED | HORMUZ BLOCKED (BRENT >$100) | INTC earnings tonight AC"

# ── OPEN_POSITIONS ────────────────────────────────────────────────────────────
# Each entry is a dict. Field reference:
#   id, asset, side                         — identity
#   entry_f, live_f, stop_f, trail_activate_f, atr_f  — price floats
#   unrealized_pct                          — (live-entry)/entry×100
#   flag_cls  "ok"|"warn"|"bad"             — drives card accent color
#   size_pct (float), size_usd (str), time_stop (str)
#   sum (str)  e.g. "+3"
#   scores  list of (leg, value, rationale) — S/T/C/R current-state assessment
#   background  str — what this company/asset is; why it's in the universe
#   thesis  str — full analytical paragraph: current state, each score mechanism,
#                 primary risk with price level, exact next action
#   invalidation  list of (variable, kill_level, current_reading, status_cls)
#   entry_context  str — tranche fills, size rationale, ATR at entry
#   key_vars  str   — live V027, overlay gate, any position-specific variable readings
#   next_catalyst  str — most relevant upcoming event for THIS position specifically
#   recommendation str — HOLD / TRAIL STOP (+ exact breakeven) / EXIT / TIGHTEN STOP
#   development  dict — trade history since entry:
#     entries  list of (date, type, event, detail)
#       type: "fill"|"trim"|"stop"|"milestone"|"note"
#     thesis_evolution  str — how the thesis has played out vs. expectation

OPEN_POSITIONS = [
    {
        "id": "P009", "asset": "SPY", "side": "Long",
        "entry_f": 708.95, "live_f": 708.40, "stop_f": 696.00,
        "trail_activate_f": 718.70, "atr_f": 6.475,
        "unrealized_pct": -0.08,
        "flag_cls": "warn",
        "size_pct": 1.00, "size_usd": "~$2,089", "time_stop": "2026-05-13",

        "sum": "+3",
        "scores": [
            ("S", "+1",
             "Equity overlay gate ON — SPY $708 is well above the estimated 10-month SMA ~$660–680 "
             "(V033 Faber). USD structural weakness (DXY −3.9% from Apr-9 peak to 98.41) adds a "
             "cross-asset risk-on tailwind that lifts all risk assets denominated in USD terms."),
            ("T", "+1",
             "Raw TSMOM: 12m return is firmly positive; 1m and 3m trend both intact. NDX printed a "
             "record close on Apr-22 (+1.73%). V036 PCTECH PC-composite is also confirming (Grade B "
             "supplementary T-input for index/ETF sleeve — supports but does not independently drive T)."),
            ("C",  "0",
             "No event-driven catalyst was scored at initiation — the edge is purely structural. "
             "C=0 is deliberate and is the direct reason the position was sized at half rather than full. "
             "A fresh catalyst (e.g., positive FOMC, macro surprise) could lift C to +1 and justify "
             "adding a second tranche."),
            ("R", "+1",
             "V027 intermediary capital z+1.65 = dealer balance-sheet expansion regime, which under "
             "Risk Rules §1.B authorizes full-size entries. V030 dealer gamma is estimated net-long "
             "at the $700 level, meaning dealers delta-hedge by selling into rallies and buying dips — "
             "this dampens intraday volatility and reduces crash-event probability at current price."),
        ],

        "background": (
            "SPY (SPDR S&P 500 ETF Trust) is the world's most liquid equity instrument (~$35–40B "
            "daily turnover), tracking the S&P 500 Index — 500 large US companies reconstituted "
            "quarterly by float-adjusted market cap. Top holdings: AAPL, MSFT, NVDA, AMZN, META "
            "(combined ~25%). SPY is in the portfolio not as a stock thesis but as the core equity "
            "sleeve expression: when the Faber regime gate (V033) is ON and structural + tactical "
            "signals align, SPY captures broad US equity risk premium with minimal execution cost "
            "and maximal liquidity. It provides exposure to the macro regime, not to any single "
            "company's fundamentals."
        ),

        "thesis": (
            "SPY is held long as the core equity sleeve with a three-factor structural edge (S+T+R, C=0). "
            "The structural case rests on the Faber overlay gate being firmly ON — SPY at $708 is "
            "significantly above the estimated 10-month SMA of $660–680, confirming a "
            "growth-expansionary macro regime. Momentum is constructive across 1m/3m/12m, with the "
            "NDX Apr-22 record close (+1.73%) providing the strongest near-term confirmation. "
            "Intermediary capital (V027 z+1.65) is in expansion territory, signaling dealer "
            "balance-sheet health — historically the strongest leading indicator for cross-asset "
            "risk appetite. The position was deliberately half-sized at 1.0% because C=0: without "
            "a fresh catalyst, the structural edge alone does not justify full deployment. Entry "
            "was averaged across five tranches at $708.95; the Apr-22 NDX surge rebuilt the stop "
            "buffer from $8 to $12.40. Primary near-term risk: INTC AC earnings tonight — a miss "
            "could pressure QQQ/SPX futures and narrow the buffer. Secondary risk: FOMC Apr-28–29, "
            "where Warsh hawkish framing has injected a rate-regime tail. Hold unless SPY closes "
            "below $696 or FOMC delivers a materially hawkish surprise."
        ),

        "invalidation": [
            ("VIX",           "> 25",          "18.92",            "ok"),
            ("HY OAS",        "> 4.50%",        "~3.8% (est.)",     "ok"),
            ("SPY close",     "< $696.00",      "$708.40",          "ok"),
            ("FOMC",          "hawkish shock",  "on hold / stable", "ok"),
        ],

        "entry_context": (
            "5 tranches — T1: $709.70 / T2: $709.56 / T3: $710.93 / T4: $710.90 (Apr-21 21:43–22:14 UTC+8) "
            "/ T5: $706.51 (Apr-22 05:05 UTC+8). Avg fill: $708.95. Risk: 1.0% NAV ($43 USDT). "
            "Half-size rationale: C=0 at entry (structural-only edge). ATR at entry: $6.475. "
            "Trail activates at $718.70 (entry + 1.5×ATR)."
        ),
        "key_vars": (
            "V027 intermediary capital z+1.65 (expansion — full-size authorized). "
            "V033 equity overlay gate ON. V036 PCTECH confirming (Grade B). "
            "V030 dealer gamma net-long at ~$700 (dampening intraday vol)."
        ),
        "next_catalyst": (
            "INTC AC tonight (Apr-23 ET) — miss could pressure QQQ/NDX futures overnight, "
            "narrowing the $12.40 stop buffer. FOMC Apr-28–29 is the primary macro catalyst "
            "for this position; any hawkish pivot scenario tests the $696 stop directly."
        ),
        "recommendation": "HOLD — stop buffer $12.40. No action. Monitor INTC AC and FOMC.",

        "development": {
            "entries": [
                ("Apr-21 21:43 UTC+8", "fill",      "T1 Fill @ $709.70",         "First tranche opened; avg $709.70"),
                ("Apr-21 21:45 UTC+8", "fill",      "T2 Fill @ $709.56",         "Avg moves to $709.63; position sizing on track"),
                ("Apr-21 22:00 UTC+8", "fill",      "T3 Fill @ $710.93",         "Avg rises to $710.06; slight push-up on momentum"),
                ("Apr-21 22:14 UTC+8", "fill",      "T4 Fill @ $710.90",         "Avg $710.27; 4/5 allocation — only missing T5 dip-fill"),
                ("Apr-22 05:05 UTC+8", "fill",      "T5 Fill @ $706.51",         "Final tranche catches pre-market dip; avg pulled to $708.95"),
                ("Apr-22 close",       "milestone", "NDX Record (+1.73%)",        "SPX/NDX records; SPY $708.40; stop buffer rebuilt $8→$12.40"),
            ],
            "thesis_evolution": (
                "Entered on structural-only edge (S+T+R, C=0) — deliberately half-sized because no catalyst "
                "was scored at entry. The five-tranche build averaged across the Apr-21 US session and Apr-22 "
                "pre-market, with T5 at $706.51 providing the best fill and pulling the avg down to $708.95. "
                "The thesis is progressing but not yet running: SPY closed Apr-22 at $708.40, nearly at parity "
                "with entry. The NDX record close (+1.73%) is the most meaningful development — it confirms the "
                "T-leg is holding and the buffer has expanded from $8 to $12.40. No stop moves have been made "
                "yet (trail activate at $718.70 not reached). Thesis evolution: structural signals intact, "
                "no catalyst edge added. Next milestone: close above $718.70 triggers Rule 2 (stop to breakeven $708.95)."
            ),
        },
    },

    {
        "id": "P010", "asset": "EWJ", "side": "Long",
        "entry_f": 88.30, "live_f": 87.40, "stop_f": 86.00,
        "trail_activate_f": 90.02, "atr_f": 1.15,
        "unrealized_pct": -1.02,
        "flag_cls": "warn",
        "size_pct": 0.75, "size_usd": "~$1,396", "time_stop": "2026-06-30",

        "sum": "+3",
        "scores": [
            ("S", "+1",
             "USD structural weakness (DXY −3.9% from Apr-9 peak) is the primary driver: EWJ is "
             "unhedged, so a falling dollar directly lifts the USD-translated NAV of yen assets "
             "independently of yen-denominated price change. International equity overlay gate ON — "
             "EWJ $90 well above estimated 10m-SMA ~$78–82 (EFA proxy)."),
            ("T", "+1",
             "Nikkei printed a record high 59,585 on Apr-22 (+0.4%). Japan's March trade surplus "
             "was the 7th consecutive monthly surplus, providing fundamental macro support under "
             "the trend. Raw TSMOM used (index/ETF sleeve rule — not single-stock residual)."),
            ("C",  "0",
             "No Japan-specific catalyst scored at entry. BOJ policy path is firmly on-hold; "
             "next BOJ meeting not a surprise vehicle in the current cycle. C=0 is consistent "
             "with the structural-only edge and contributes to the 0.75% sizing decision."),
            ("R", "+1",
             "V027 z+1.65 = cross-asset expansion regime applies. EWJ positioning is not crowded — "
             "it is not a consensus global-macro long in the current cycle. No elevated options "
             "skew or CFTC crowding flag."),
        ],

        "background": (
            "EWJ (iShares MSCI Japan ETF) tracks the MSCI Japan Index — ~240 large- and mid-cap "
            "Japanese companies, USD-denominated and unhedged. Top holdings: Toyota, Sony, "
            "Mitsubishi UFJ, Keyence, Shin-Etsu Chemical. Japan is the world's third-largest "
            "economy; its equity market is structurally different from the US — dominated by "
            "manufacturers, financials, and industrials rather than tech. The unhedged USD "
            "structure means the DXY direction is a first-order return driver: when the dollar "
            "weakens, EWJ rises in USD terms even if yen-denominated prices are flat. This makes "
            "EWJ a natural second expression of the DXY-weak thesis already in P009 SPY, but with "
            "genuinely different sector and factor exposure (no Magnificent Seven overlap)."
        ),

        "thesis": (
            "EWJ is held long as the international equity sleeve position with two converging "
            "tailwinds. The primary structural driver (S+1) is USD weakness: DXY at 98.41 is "
            "down 3.9% from its April 9 peak, directly translating into higher USD-equivalent "
            "returns from yen-denominated holdings. The same DXY-weak regime that underpins "
            "P009 SPY also makes EWJ a natural second sleeve expression with genuinely different "
            "sector exposure (no Mag7 overlap). The momentum leg (T+1) is confirmed by the Nikkei "
            "printing a record high on April 22 and Japan's seventh consecutive monthly trade "
            "surplus underpinning the macro trend. The position is currently below entry at $87.40 "
            "vs. $88.30 avg, leaving a critically thin stop buffer of $1.40 (~1.2× ATR). This is "
            "the most vulnerable position in the current book. The primary invalidation is a DXY "
            "reversal — if the dollar strengthens sharply on hawkish Fed or safe-haven flow, "
            "both the S-variable and the FX translation unwind simultaneously. An INTC earnings "
            "miss tonight could pressure broad indices including EWJ via risk-off correlation."
        ),

        "invalidation": [
            ("USDJPY",         "< 150 (yen spike)",    "~158–159",          "ok"),
            ("Nikkei",         "−5% single session",   "record +0.4%",      "ok"),
            ("BOJ emergency",  "≥ 50bp hike",          "on hold",           "ok"),
            ("EWJ stop",       "< $86.00",             "$87.40 (F1 thin)",  "warn"),
        ],

        "entry_context": (
            "3 tranches — T1: $88.48 / T2: $88.39 (Apr-21 21:47–22:13 UTC+8) / T3: $87.39 (Apr-22 05:08). "
            "Avg fill: $88.30. Risk: 0.75% NAV (~$32 USDT). "
            "Sizing haircut vs. full: correlation with P009 SPY (both express DXY-weak + equity-risk-on; "
            "combined sector cap per Risk Rules §5). ATR at entry: $1.15. Trail activates at $90.02."
        ),
        "key_vars": (
            "V027 z+1.65 (expansion). EFA proxy overlay gate ON (EWJ > 10m-SMA). "
            "USDJPY ~158.9 — yen not strengthening abnormally. "
            "F1 FIRED: buffer $1.40 = 1.2× ATR (< 2× ATR threshold)."
        ),
        "next_catalyst": (
            "INTC AC tonight — if a miss broadens to risk-off, the $1.40 buffer becomes critical "
            "overnight. Alert at EWJ < $87. BOJ next scheduled meeting; any emergency action = "
            "immediate exit regardless of price."
        ),
        "recommendation": "HOLD WITH CLOSE WATCH — F1 thin buffer fired. Alert if EWJ < $87. Ready to act on stop hit.",

        "development": {
            "entries": [
                ("Apr-21 21:47 UTC+8", "fill",  "T1 Fill @ $88.48",       "First tranche; avg $88.48"),
                ("Apr-21 22:13 UTC+8", "fill",  "T2 Fill @ $88.39",       "Avg $88.44; building into Nikkei momentum"),
                ("Apr-22 05:08 UTC+8", "fill",  "T3 Fill @ $87.39",       "Full 3-tranche build; avg pulled to $88.30 on pre-market dip"),
                ("Apr-22 close",       "note",  "F1 Buffer Alert — THIN", "EWJ $87.40 vs stop $86.00; buffer $1.40 ≈ 1.2× ATR — below 2× threshold"),
            ],
            "thesis_evolution": (
                "Entered on DXY-weakness + Nikkei momentum thesis, with P010 sized at 0.75% (haircut vs. full) "
                "due to correlation overlap with P009 SPY (both express DXY-weak + equity-risk-on). T3 at $87.39 "
                "brought the avg fill to $88.30, but the position immediately ran into pressure — EWJ closed at "
                "$87.40 on Apr-22, essentially flat from the T3 fill and $0.90 below the average entry. "
                "The DXY-weak structural thesis (primary S-driver) remains intact — DXY at 98.41 has not recovered "
                "and the Nikkei printed a record close. However, the position has not developed in our favour: "
                "price is sitting below entry and the stop buffer is critically thin (F1 fired). "
                "The position is in a hold-and-monitor state — no new adverse development, but no progress either. "
                "Needs EWJ to recover above $88.30 to become neutral; above $90.02 triggers Rule 2 trail."
            ),
        },
    },

    {
        "id": "P016", "asset": "Brent Crude", "side": "Long",
        "entry_f": 95.13, "live_f": 101.91, "stop_f": 90.50,
        "trail_activate_f": 97.94, "atr_f": 1.875,
        "unrealized_pct": +7.13,
        "flag_cls": "ok",
        "size_pct": 0.75, "size_usd": "~$859", "time_stop": "2026-05-22",

        "sum": "+3",
        "scores": [
            ("S", "+1",
             "Three structural factors stack: (1) Hormuz blockade restricting <10% of normal "
             "seaborne crude traffic = persistent supply shock, not a speculative crowding story; "
             "(2) Brent curve in backwardation with V028 basis-momentum steepening (T1 +13.95 — "
             "the only commodity with T1-grade fresh data in the Apr-22 run); (3) DXY structural "
             "weakness adds an independent commodity S-tailwind (commodities priced in USD benefit "
             "from dollar depreciation)."),
            ("T", "+1",
             "Price trend confirmed and accelerating: Brent +8.2% on Apr-22 to $101.91, breaching "
             "$100 for the first time this cycle. The 1m/3m momentum is strongly positive. "
             "Supply-shock narrative is driving the trend rather than speculative positioning, "
             "making it more durable."),
            ("C",  "0",
             "Iran ceasefire binary scored zero at entry: the outcome was symmetric — deal = "
             "Brent −10%, no deal = hold/higher. Cannot score a directional catalyst under those "
             "conditions. C=0 contributed to the 0.75% sizing haircut alongside the correlation "
             "concern."),
            ("R", "+1",
             "V027 z+1.65 = expansion regime. V034 GSG overlay gate CONFIRMED ON for the first "
             "time this cycle (GSG 31.75 > 10m-SMA 25.35, confirmed Apr-22). COT speculative "
             "positioning is not crowded — the trade is framed as a supply-shock, not a "
             "consensus-speculative long. No vol-band violation flagged."),
        ],

        "background": (
            "BZUSDT (Brent Crude Perpetual Futures, Bybit) tracks ICE Brent — the global benchmark "
            "crude oil price, referencing North Sea blend crude delivered at Sullom Voe. Brent "
            "prices ~80% of the world's internationally traded crude. The Strait of Hormuz — "
            "currently partially blockaded — is the world's most critical oil chokepoint: ~21 "
            "million barrels per day transited it in 2024 (~20% of global daily consumption). "
            "Any sustained reduction in Hormuz transit directly tightens the physical market and "
            "steepens the futures curve into backwardation. Brent is in the portfolio as the "
            "primary commodity sleeve expression: when V034 GSCI/GSG gate is ON and the thesis "
            "reaches Sum ≥ +3, Brent is the preferred vehicle over WTI (superior Bybit liquidity "
            "and more direct Hormuz/Middle East supply-shock read-through)."
        ),

        "thesis": (
            "Brent is the primary commodity sleeve position, entered Apr-22 after the Faber "
            "overlay gate (V034 GSG confirmed ON) unblocked the commodity sleeve for the first "
            "time this cycle. Three independent structural factors drive the +3 score: the Hormuz "
            "blockade is removing a persistent share of seaborne crude supply from the market "
            "(not a crowded speculative play — the COT report does not show >2σ speculative "
            "crowding); the Brent futures curve is in fresh backwardation with V028 basis-momentum "
            "steepening to T1 +13.95 (the single strongest commodity signal in the Apr-22 run); "
            "and DXY structural weakness adds an independent S-tailwind. Two risks drove a "
            "deliberate 0.75% haircut from full-size: correlation with P009/P010 (all three share "
            "the DXY-weak macro theme) and the Iran deal binary (confirmed deal = Brent likely "
            "−10–15% fast). Position is now running +7.1% to $101.91, having cleared the "
            "trail_activate level of $97.94. Mandatory Rule 2 (move stop to breakeven) is now "
            "triggered. The Hormuz thesis is validating in real-time: the breach of $100 with "
            "Iran still refusing to reopen shipping confirms the market is pricing structural "
            "supply disruption, not a temporary geopolitical spike."
        ),

        "invalidation": [
            ("Iran deal",       "Brent likely < $88",    "not confirmed",     "ok"),
            ("Hormuz re-open",  "> 70% normal traffic",  "< 10% currently",   "ok"),
            ("V034 gate",       "GSG < 10m-SMA",         "GSG 31.75 > 25.35", "ok"),
            ("Stop hit",        "< $90.50",              "$101.91 (+$11.41)", "ok"),
        ],

        "entry_context": (
            "Single fill: $95.13 (Bybit BZUSDT Perp, Apr-22 21:33 UTC+8). $0.63 above upper rec "
            "range $94.50. Original size 1,006.48 USDT; trimmed 147.21 USDT at $94.97 (22:27 UTC+8) "
            "— overexposure correction. Final size: 859.27 USDT. "
            "Risk: 0.75% NAV (~$32 USDT). ATR at entry: $1.875. Trail activates at $97.94."
        ),
        "key_vars": (
            "V034 GSG overlay gate CONFIRMED ON (31.75 > 10m-SMA 25.35). "
            "V028 basis-momentum T1 +13.95 (steepening — strongest commodity signal Apr-22). "
            "V027 z+1.65 (expansion). COT: not crowded. "
            "TRAIL RULE TRIGGERED: live $101.91 > trail_activate $97.94."
        ),
        "next_catalyst": (
            "Iran / Hormuz status: any confirmed deal or new shipping-attack escalation in "
            "next 24–48h directly reprices ±10% fast. Next EIA weekly crude inventory release. "
            "If Brent sustains >$100 into Apr-23 US session, chandelier stop continues to rise."
        ),
        "recommendation": (
            "ACTION REQUIRED — Move stop to breakeven $95.13 NOW (Rule 2 mandatory). "
            "Chandelier trail: stop = HH $101.91 − 3×ATR ≈ $96.28. Then trail as new HH forms."
        ),

        "development": {
            "entries": [
                ("Apr-22 21:33 UTC+8", "fill",      "Entry Fill @ $95.13",          "Size 1,006.48 USDT; $0.63 above $94.50 upper rec limit"),
                ("Apr-22 22:27 UTC+8", "trim",      "Trim −$147 USDT @ $94.97",     "Overexposure correction; trim below entry; final size 859.27 USDT (0.75% NAV)"),
                ("Apr-22 close",       "milestone", "Brent Breaks $100 → $101.91",  "+$6.78/bbl (+7.1% open P&L); Hormuz premium intact; Iran refuses to reopen"),
                ("Apr-22 close",       "stop",      "Rule 2 TRIGGERED",             "Live $101.91 > trail_activate $97.94; mandatory stop move to breakeven $95.13 required"),
            ],
            "thesis_evolution": (
                "Most dynamic position in the current book. Entered Apr-22 after the V034 GSG overlay gate "
                "confirmed ON for the first time this cycle, unblocking the commodity sleeve. The fill at $95.13 "
                "overshot the $94.50 upper limit by $0.63, triggering an immediate size correction: 147.21 USDT "
                "trimmed at $94.97 (below entry — costing ~$0.16/bbl vs. holding, but the discipline was correct). "
                "From there the thesis ran hard and fast: the ceasefire extension did NOT deliver the expected "
                "Brent deflation, because Iran refused to reopen Hormuz while US Navy intercepts resumed. "
                "Brent surged +8.2% in a single session, breaching $100 for the first time this cycle. "
                "This is the strongest thesis-validation print in the current book — every structural variable "
                "(Hormuz blockade, backwardation, DXY-weak) is active simultaneously. "
                "Rule 2 (mandatory stop to breakeven) is now triggered. The trim at entry was the only adverse "
                "development; everything since has been in our direction."
            ),
        },
    },
]

# ── PENDING_POSITIONS ─────────────────────────────────────────────────────────
# Same fields as OPEN_POSITIONS, plus:
#   entry_zone (str), est_trigger (str)
#   status_cls "blue"|"warn"|"bad", status_txt (str)
#   entry_criteria (str) — exact conditions both required to enter
#   thesis label changes to "why_we_want_this" (same key "thesis")

PENDING_POSITIONS = [
    {
        "id": "P013", "asset": "INTC", "side": "Long (pending)",
        "entry_zone": "$68–72", "est_trigger": "Apr-24 morning UTC+8",
        "status_cls": "blue", "status_txt": "ON DECK",
        "sum": "+4",
        "scores": [
            ("S", "+1",
             "V026 residual momentum +13.89% (Grade A, FF5-residualized) — stock outperforming "
             "its factor-predicted return on idiosyncratic alpha, not market beta. GP/A (V031) "
             "and CEI (V032) both supportive: gross profitability is recovering post-restructure "
             "and net issuance is minimal. Valuation at deep discount to TSMC/NVDA peers."),
            ("T", "+1",
             "V026 residual +13.89% confirms the T-leg (single-stock rule: use FF5-residualized "
             "momentum, not raw TSMOM). The idiosyncratic trend is driven by the Terafab foundry "
             "re-rating thesis, not broad-market beta — making it more robust to index sell-offs."),
            ("C", "+1",
             "Apr-23 AC earnings: Terafab 18A external customer reveal is the C+1 catalyst. "
             "The 88% historical beat rate for leading semis names with positive EPS revision "
             "supports pre-scoring C+1. C leg drops to 0 or −1 on miss or no foundry commentary."),
            ("R", "+1",
             "V027 z+1.65 = full-size authorized for this position. INTC options skew not "
             "extreme — no crowded short-squeeze setup, clean R-leg. Intermediary capital "
             "expansion regime is the most favorable R-state for initiating new entries."),
        ],

        "background": (
            "Intel Corporation (INTC) is the largest US semiconductor manufacturer by revenue, "
            "producing CPUs, data-center processors (Xeon), AI accelerators (Gaudi), and "
            "networking chips. Intel operates two distinct businesses: (1) Products — CPU design "
            "for PC (Core Ultra), server (Xeon), and AI (Gaudi 3), competing with AMD, NVIDIA, "
            "and Qualcomm; and (2) Intel Foundry Services (IFS) — contract chip manufacturing "
            "on Intel's own fabs under the Terafab 18A process node, directly competing with "
            "TSMC 2nm and Samsung 3nm for external customers. The IFS segment is the core thesis "
            "driver: 18A is Intel's first process node technologically competitive with TSMC 2nm, "
            "and winning external tape-outs (non-Intel chip production) would validate the foundry "
            "model and fundamentally re-rate the stock from a declining CPU company to a "
            "dual-revenue semiconductor platform. INTC is in the equity universe as a structural "
            "recovery play with high residual momentum and a binary catalyst."
        ),

        "thesis": (
            "INTC is a contingent long pending the Q1 earnings beat confirmation tonight. The "
            "structural case (S+1) rests on V026 residual momentum at +13.89% — one of the "
            "highest residual readings in the current equity universe — meaning the stock has "
            "been outperforming its Fama-French 5-factor predicted return on idiosyncratic alpha "
            "driven by the foundry re-rating narrative, not broad-market beta. This is the "
            "highest-confidence signal for single-name entries. The catalyst score (C+1) was "
            "pre-scored based on: (1) 88% historical beat rate for leading semis with positive "
            "EPS revisions; (2) Terafab 18A is at a milestoning moment — any external customer "
            "tape-out or production commitment revealed on the call transforms the IFS segment "
            "from a cost center to a validated revenue stream. The entry trigger is NOT the "
            "headline EPS beat alone. It requires positive Terafab/foundry commentary to confirm "
            "the structural narrative; without that, the Sum drops and the entry is canceled. "
            "Prior P004 trade (closed Apr-19 before earnings, +2.09%) was the structural read; "
            "this P013 is the confirmed-beat re-entry strategy."
        ),

        "invalidation": [
            ("Q1 revenue",       "< $12.37B",           "consensus ≥$12.37B",  "ok"),
            ("Terafab commentary","disappointing/absent","expected positive",   "ok"),
            ("DC-AI rev",        "miss vs $4.41B",       "est. $4.41B (Xeon)",  "ok"),
            ("Post-AC gap",      "gaps below $66",       "pre-earnings $68.50", "ok"),
        ],

        "entry_criteria": (
            "BOTH conditions required: (1) Q1 revenue ≥ $12.37B; "
            "(2) Positive Terafab / 18A external-customer commentary on the earnings call. "
            "Miss on either → cancel P013 in full. Do not chase a gap-up without foundry confirmation."
        ),
        "entry_context": "Not yet filled. Target entry Apr-24 morning UTC+8 at limit $68–72.",
        "key_vars": (
            "V026 residual momentum +13.89% (Grade A). V027 z+1.65 (full-size authorized). "
            "Planned size: 1.0% NAV (full — V027 expansion + Sum+4). ATR ~$5; stop = entry − 2×ATR."
        ),
        "next_catalyst": "Q1 earnings TONIGHT AC (Apr-23 ET). Entry decision: Apr-24 morning UTC+8.",
        "recommendation": (
            "WAIT. INTC reports tonight AC. Enter Apr-24 morning ONLY on beat + "
            "Terafab/foundry upside. Miss or weak DC-AI commentary → cancel P013 entirely."
        ),
    },

    {
        "id": "P014", "asset": "AAPL", "side": "Long (deferred)",
        "entry_zone": "$271–274", "est_trigger": "Hard stop 2026-04-30",
        "status_cls": "warn", "status_txt": "DEFERRED",
        "sum": "+3",
        "scores": [
            ("S", "+1",
             "V026 residual momentum +4.68% (Grade A, FF5-residualized). GP/A (V031): AAPL has "
             "the highest gross profitability among Mag7. CEI (V032) near-zero — Services-heavy "
             "model generates minimal net equity issuance, removing the usual large-cap issuance "
             "headwind. Valuation ~28× fwd P/E is premium but within historical band."),
            ("T", "+1",
             "V026 residual +4.68% confirms T-leg. Raw TSMOM also positive 12m. "
             "Tim Cook departure (Sept-1) introduced a temporary idiosyncratic discount; "
             "once the leadership transition is absorbed by the market, T-leg should remain "
             "supported by the Services revenue compounding story."),
            ("C",  "0",
             "No catalyst before the hard time-stop April 30. May 1 earnings are AFTER the "
             "time-stop — C cannot be scored before the event, and entering before May 1 "
             "with no informational edge is a Grade C approach. C=0 maintained."),
            ("R", "+1",
             "V027 z+1.65. No extreme crowding in CFTC positioning or ETF flows for AAPL. "
             "Dealer gamma positioning neutral — no crash-vol asymmetry at current price levels."),
        ],

        "background": (
            "Apple Inc. (AAPL) is the world's most valuable company by market cap (~$4T), "
            "designing consumer hardware (iPhone ~50% of revenue, Mac, iPad, Watch, Vision Pro), "
            "software (iOS, macOS, visionOS), and services (App Store, Apple Music, iCloud, "
            "Apple Pay, Apple Intelligence — AI features). The Services segment (~$26B/quarter, "
            "~75% gross margin) is the highest-margin business and the primary re-rating driver. "
            "Tim Cook announced his CEO retirement effective September 1, with COO John Ternus "
            "named as successor (Apr-21 announcement). This leadership transition is creating "
            "a near-term price overhang. Apple Intelligence (Apple's on-device AI system, "
            "announced at WWDC 2025) is the primary product catalyst for the next 12 months — "
            "upgrade supercycle tied to AI-capable iPhone hardware."
        ),

        "thesis": (
            "AAPL is a promoted long (Sum+3) that is currently deferred because the price "
            "($266.17 as of Apr-22) is below the entry zone ($271–274) and adjacent to the "
            "ATR stop (~$266.50). The structural case is intact: V026 residual +4.68%, "
            "highest GP/A in Mag7, minimal CEI, and V027 expansion regime all support entry. "
            "The deferral is purely mechanical — entering at $266 with a stop at $266.50 leaves "
            "essentially zero buffer and violates the 2× ATR buffer rule. The Tim Cook CEO "
            "transition announced Apr-21 (Sept-1 effective, John Ternus successor) is the proximate "
            "cause of the price overhang. If the market re-rates the Ternus succession as "
            "operationally neutral — Ternus is a hardware/product executive who designed every "
            "major Apple product of the last decade — recovery above $269 would restore adequate "
            "buffer and allow entry. Hard time-stop 2026-04-30 applies: May 1 earnings are too "
            "close to enter without the informational edge of the event outcome, and the position "
            "would have no time to develop before the catalyst binary."
        ),

        "invalidation": [
            ("AAPL price",    "< $264 (below ATR stop)", "$266.17 (deferred)",    "warn"),
            ("Recovery",      "> $269 (entry threshold)", "currently below",      "warn"),
            ("SPY",           "< $696",                  "$708.40 OK",            "ok"),
            ("Time-stop",     "after 2026-04-30",        "~7 days remaining",     "warn"),
        ],

        "entry_criteria": (
            "Price recovers above $269 (minimum 2× ATR buffer from stop ~$266.50) "
            "before 2026-04-30. Do not enter below $268. If not triggered by Apr-30 close → cancel."
        ),
        "entry_context": "Not yet filled. Deferred since Apr-22 when price missed entry zone.",
        "key_vars": "V026 residual +4.68% (Grade A). V027 z+1.65. Planned size: 0.75%. ATR ~$2.50.",
        "next_catalyst": "Apr-23 open: does AAPL recover above $269 on the broad market lift? If not by Apr-28, cancel is likely.",
        "recommendation": "DO NOT ENTER. Price $266.17 < $268 threshold. Reassess Apr-23 open. Cancel if not above $269 before Apr-30.",
    },

    {
        "id": "P015", "asset": "GOOGL", "side": "Long (waiting)",
        "entry_zone": "est. $333–340", "est_trigger": "Apr-30 morning UTC+8",
        "status_cls": "blue", "status_txt": "WAITING",
        "sum": "+3",
        "scores": [
            ("S", "+1",
             "V026 residual momentum (qualitative positive — GOOGL has outperformed on AI revenue "
             "monetization vs. consensus). Valuation ~22× fwd P/E is below Mag7 median (~25×) — "
             "the cheapest large-cap AI platform on earnings-adjusted multiples. GP/A (V031) "
             "best-in-class for internet platforms (~55% gross margin on advertising)."),
            ("T",  "0",
             "T=0 at last scoring (Apr-22): GOOGL's own 3m price action is flat-to-slightly "
             "negative vs. NDX despite the NDX record. The stock is lagging its index on "
             "pre-earnings uncertainty. T will be re-scored after the Apr-29 earnings reaction — "
             "a gap-up would confirm T+1 and raise confidence in the entry."),
            ("C", "+1",
             "Apr-29 AC earnings: Q1 2026 is the first clean quarter with AI monetization across "
             "Search (AI Overviews), Ads (Performance Max), and Cloud (Vertex AI) simultaneously. "
             "88% Mag7 beat rate × positive EPS revisions = C+1 pre-scored. C drops to 0/−1 "
             "on advertising revenue miss or negative AI commentary."),
            ("R", "+1",
             "V027 z+1.65. No extreme crowding — GOOGL is not a consensus-long among "
             "momentum funds at current positioning levels. Implied vol into earnings not "
             "elevated vs. historical (clean R without crash-risk asymmetry)."),
        ],

        "background": (
            "Alphabet Inc. (GOOGL) is the parent of Google — the world's dominant search engine "
            "(>90% market share), YouTube (2B+ monthly active users), Google Cloud (GCP, 3rd-largest "
            "cloud by revenue), DeepMind, and Waymo. GOOGL generates ~75% of revenue from "
            "advertising (Google Search + YouTube). The AI cycle is the primary re-rating driver: "
            "Google's Gemini models are integrated into Search (AI Overviews — replacing 10-blue-links "
            "with AI-generated answers + ads), Ads (Performance Max — AI-optimized campaign "
            "management), and Cloud (Vertex AI — enterprise model deployment platform). Q1 2026 "
            "is the first quarter where all three AI products have had a full quarter to contribute "
            "measurably to revenue. GOOGL also faces a regulatory tail risk (DOJ antitrust case "
            "on search monopoly), which is the primary reason the stock trades at a discount to "
            "Mag7 peers despite being one of the most profitable businesses ever built."
        ),

        "thesis": (
            "GOOGL is a promoted contingent long (Sum+3) waiting for the Apr-29 earnings beat "
            "confirmation. The structural case (S+1) rests on GOOGL being the cheapest large-cap "
            "AI platform at ~22× fwd P/E (vs. Mag7 median ~25×) with best-in-class gross "
            "profitability and V026 residual momentum tracking positively. The weight-bearing "
            "leg is C+1: Q1 2026 is the first clean quarter where AI Overviews in Search, "
            "Performance Max in Ads, and Vertex AI in Cloud can all show meaningful revenue "
            "contribution simultaneously. An advertising revenue beat (consensus ~$54B total "
            "revenue) with positive AI monetization commentary would confirm the C-leg thesis "
            "and trigger entry. The T=0 score reflects the stock's underperformance vs. NDX "
            "in the 3m window — this is a pre-earnings discount, not a structural trend break, "
            "and the Apr-29 earnings reaction will likely resolve it directionally. "
            "Key note: earnings date was corrected on Apr-22 from Apr-22/23 to Apr-29 AC "
            "(prior Memory.md date was wrong). Do not chase any pre-earnings gap."
        ),

        "invalidation": [
            ("Q1 advertising rev",  "miss vs ~$54B consensus", "consensus ~$54B",    "ok"),
            ("AI commentary",       "negative / absent",       "expected positive",  "ok"),
            ("Post-AC reaction",    "gap-down > 5%",           "TBD Apr-29",         "ok"),
            ("Time-stop",           "after 2026-05-15",        "~22 days remaining", "ok"),
        ],

        "entry_criteria": (
            "Q1 revenue beat vs. ~$54B consensus AND positive AI monetization commentary "
            "(Search AI Overviews revenue + Vertex AI cloud traction). "
            "Gap-up on Apr-30 open is the entry signal. Do not chase if gap > 5% at open."
        ),
        "entry_context": "Not yet filled. Earnings Apr-29 AC. Entry window: Apr-30 morning UTC+8.",
        "key_vars": "V026 residual positive (qualitative). V027 z+1.65. Planned size: 0.75%. ATR est. ~$8–10.",
        "next_catalyst": "Q1 earnings Apr-29 AC (5 days). No action before then. NDX record provides supportive pre-earnings backdrop.",
        "recommendation": "NO ACTION until Apr-30. Earnings Apr-29 AC. Enter Apr-30 morning on beat + AI monetization confirmation only.",
    },
]

# ── FLAGS (unchanged tuple format) ────────────────────────────────────────────
FLAGS = [
    ("F1",  "Stop Buffer < 2×ATR",   "warn", "P010 EWJ thin — $1.40 / ~1.2× ATR"),
    ("F2",  "Stop Hit",              "ok",   "All clear"),
    ("F3",  "Time Inv ≤ 7 days",     "ok",   "Nearest: P016 2026-05-22 (~29 days)"),
    ("F4",  "Earnings ≤ 2 days",     "warn", "INTC tonight AC — P013 catalyst trigger"),
    ("F5",  "Catalyst ≤ 1 day",      "warn", "INTC AC within 24h"),
    ("F6",  "Data Missing",          "ok",   "All prices sourced from snapshot"),
    ("F7",  "AH Move ≥ 3%",         "ok",   "No large AH gaps on open positions"),
    ("F8",  "Thesis Variable Breach","ok",   "Brent >$100 = thesis validating, not breached"),
    ("F9",  "Portfolio Heat > 6%",   "ok",   "3.09% / 8% — headroom for 2 more positions"),
    ("F10", "Correlation |ρ| > 0.7", "warn", "P009+P016 share DXY-weak macro theme"),
    ("F11", "COT Crowding > 2σ",    "ok",   "Brent: supply-shock narrative, not crowded"),
    ("F12", "Vol Band (cloud)",      "ok",   "No cloud vol-band alerts in digest"),
    ("F13", "Cloud Alert",           "ok",   "No unmatched POSITION-ALERT in digest"),
]

# ════════════════════════════════════════════════════════════════════════════
# TEMPLATE — do not edit below this line
# ════════════════════════════════════════════════════════════════════════════

_CLS_COLOR = {"ok": "green", "warn": "yellow", "bad": "red", "blue": "blue"}
_SEV_MAP   = {
    "F1": "HIGH", "F2": "CRITICAL", "F3": "MED",  "F4": "HIGH",  "F5": "HIGH",
    "F6": "MED",  "F7": "HIGH",     "F8": "CRITICAL", "F9": "HIGH", "F10": "MED",
    "F11": "MED", "F12": "HIGH",    "F13": "MED",
}
_BORDER    = {"ok": "#4ade80", "warn": "#facc15", "bad": "#f87171", "blue": "#5b9bff"}
_REC_BG    = {"ok": "rgba(74,222,128,.07)", "warn": "rgba(250,204,21,.08)",
              "bad": "rgba(248,113,113,.10)", "blue": "rgba(91,155,255,.08)"}

CSS = """:root{--bg:#0f1115;--card:#171a21;--muted:#8a93a6;--fg:#e5e9f0;--accent:#5b9bff;
      --ok:#4ade80;--warn:#facc15;--bad:#f87171;--border:#262b35;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
     background:var(--bg);color:var(--fg);line-height:1.5}
.container{max-width:1300px;margin:0 auto;padding:28px 20px}
h1{font-size:24px;margin:0 0 4px}
h2{font-size:17px;margin:32px 0 12px;color:var(--accent);border-bottom:1px solid var(--border);
   padding-bottom:6px;letter-spacing:.02em}
.sub{color:var(--muted);font-size:13px;margin-bottom:12px}
.lbl{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:600}
.mute{color:var(--muted)}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px 18px}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:4px}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}
th{color:var(--muted);font-weight:500;background:#12151c}
tr:hover td{background:#1a1e27}
.pill{display:inline-block;padding:2px 9px;border-radius:10px;font-size:11px;font-weight:600}
.pill.green{background:rgba(74,222,128,.15);color:var(--ok)}
.pill.red{background:rgba(248,113,113,.15);color:var(--bad)}
.pill.yellow{background:rgba(250,204,21,.15);color:var(--warn)}
.pill.blue{background:rgba(91,155,255,.15);color:var(--accent)}
.pill.gray{background:#262b35;color:var(--muted)}
.ok{color:var(--ok)} .warn{color:var(--warn)} .bad{color:var(--bad)}
.status-bar{display:flex;align-items:center;gap:16px;padding:10px 16px;
            background:var(--card);border:1px solid var(--border);border-radius:8px;
            margin-bottom:16px;flex-wrap:wrap}
.range-bar{display:flex;width:100%;height:18px;border-radius:4px;overflow:hidden}
.heat-track{background:#12151c;border-radius:6px;overflow:hidden;height:8px;margin:4px 0 2px}
.heat-fill{height:100%;border-radius:6px}
.footer{color:var(--muted);font-size:12px;margin-top:28px;border-top:1px solid var(--border);
        padding-top:12px;line-height:1.8}
p{margin:0 0 0 0;line-height:1.68}
@media(max-width:900px){
  .grid-4{grid-template-columns:1fr 1fr}
  .pos-body-grid{grid-template-columns:1fr !important}
}"""


def pill(txt, cls):
    c = _CLS_COLOR.get(cls, "gray")
    return f'<span class="pill {c}">{txt}</span>'


def score_cls(v):
    try:
        n = int(str(v).replace("+", ""))
        return "ok" if n > 0 else ("bad" if n < 0 else "mute")
    except Exception:
        return "mute"


def score_table(scores, sum_val):
    rows = ""
    for leg, val, rationale in scores:
        sc = score_cls(val)
        rows += (
            f'<tr style="border-bottom:1px solid #1e2330">'
            f'<td style="font-weight:700;font-size:13px;color:#b5bccc;padding:5px 10px 5px 0;'
            f'white-space:nowrap;width:16px">{leg}</td>'
            f'<td style="padding:5px 12px 5px 0;width:26px">'
            f'<span class="{sc}" style="font-weight:800;font-size:15px">{val}</span></td>'
            f'<td style="padding:5px 0;font-size:11px;color:#a8b2c4;line-height:1.55">{rationale}</td>'
            f'</tr>'
        )
    sc_sum = score_cls(sum_val)
    rows += (
        f'<tr><td style="font-weight:700;font-size:13px;color:#b5bccc;padding:7px 10px 4px 0">'
        f'Sum</td>'
        f'<td style="padding:7px 12px 4px 0">'
        f'<span class="{sc_sum}" style="font-weight:900;font-size:18px">{sum_val}</span></td>'
        f'<td></td></tr>'
    )
    return f'<table style="width:100%;border-collapse:collapse">{rows}</table>'


def inv_chips(items):
    out = ""
    for var, kill, current, scls in items:
        icon   = "✓" if scls == "ok" else ("⚠" if scls == "warn" else "✗")
        bg     = ("rgba(74,222,128,.10)" if scls == "ok" else
                  "rgba(250,204,21,.13)" if scls == "warn" else "rgba(248,113,113,.13)")
        col    = "#4ade80" if scls == "ok" else ("#facc15" if scls == "warn" else "#f87171")
        out += (
            f'<div style="display:inline-block;padding:6px 10px;border-radius:6px;'
            f'background:{bg};margin:3px 4px 3px 0;font-size:11px;line-height:1.5;'
            f'vertical-align:top">'
            f'<div style="color:{col};font-weight:700">{icon} {var}</div>'
            f'<div style="color:#8a93a6">Kill: {kill}</div>'
            f'<div style="color:#c8d0de">Now: {current}</div>'
            f'</div>'
        )
    return out


def range_bar(entry_f, live_f, stop_f, trail_f):
    hi   = max(trail_f, live_f, entry_f) * 1.018
    span = (hi - stop_f) or 1.0

    def pct(v):
        return max(0.0, min(100.0, (v - stop_f) / span * 100))

    ep = pct(entry_f)
    tp = pct(trail_f)
    lp = pct(live_f)
    live_col = "#4ade80" if live_f >= trail_f else ("#facc15" if live_f >= entry_f else "#f87171")

    def fmt(v):
        return f"${v:,.2f}"

    return (
        f'<div style="position:relative;margin:10px 0 44px">'
        f'<div class="range-bar">'
        f'<div style="width:{ep:.1f}%;background:rgba(248,113,113,.22)"></div>'
        f'<div style="width:{max(0.0,tp-ep):.1f}%;background:rgba(250,204,21,.20)"></div>'
        f'<div style="flex:1;background:rgba(74,222,128,.18)"></div>'
        f'</div>'
        f'<div style="position:absolute;top:0;left:{lp:.1f}%;height:18px;width:3px;'
        f'background:{live_col};transform:translateX(-50%);border-radius:1px"></div>'
        f'<div style="position:relative;height:38px;margin-top:4px;font-size:10px;color:#8a93a6">'
        f'<span style="position:absolute;left:0;line-height:1.4;color:#f87171">'
        f'STOP<br>{fmt(stop_f)}</span>'
        f'<span style="position:absolute;left:{ep:.1f}%;transform:translateX(-50%);'
        f'text-align:center;line-height:1.4">ENTRY<br>{fmt(entry_f)}</span>'
        f'<span style="position:absolute;left:{tp:.1f}%;transform:translateX(-50%);'
        f'text-align:center;line-height:1.4">TRAIL↑<br>{fmt(trail_f)}</span>'
        f'<span style="position:absolute;left:{lp:.1f}%;transform:translateX(-50%);'
        f'text-align:center;line-height:1.4;color:{live_col};font-weight:700">'
        f'▲LIVE<br>{fmt(live_f)}</span>'
        f'</div></div>'
    )


def dev_section(dev):
    """Render the Trade Development timeline + thesis evolution paragraph."""
    if not dev:
        return ""
    _TYPE_COL = {
        "fill":      ("#5b9bff", "●", "Fill"),
        "trim":      ("#fb923c", "◆", "Trim"),
        "stop":      ("#f87171", "▲", "Stop"),
        "milestone": ("#4ade80", "★", "Milestone"),
        "note":      ("#8a93a6", "◉", "Note"),
    }
    rows = ""
    for date, typ, event, detail in dev.get("entries", []):
        col, icon, label = _TYPE_COL.get(typ, ("#8a93a6", "●", typ.title()))
        rows += (
            f'<tr style="border-bottom:1px solid #1b2030">'
            f'<td style="white-space:nowrap;padding:5px 12px 5px 0;font-size:11px;color:#6b748a">{date}</td>'
            f'<td style="padding:5px 10px 5px 0;white-space:nowrap">'
            f'<span style="color:{col};font-size:11px;font-weight:700">{icon}&nbsp;{label}</span></td>'
            f'<td style="padding:5px 10px 5px 0;font-size:12px;color:#c8d0de;font-weight:600">{event}</td>'
            f'<td style="padding:5px 0;font-size:11px;color:#8a93a6">{detail}</td>'
            f'</tr>'
        )
    evo = dev.get("thesis_evolution", "")
    return (
        f'<div style="margin:18px 0 6px">'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:8px">Trade Development</div>'
        f'<table style="width:100%;border-collapse:collapse;margin-bottom:12px">'
        f'<thead><tr>'
        f'<th style="font-size:10px;color:#6b748a;font-weight:500;padding:4px 12px 4px 0;background:transparent">Date</th>'
        f'<th style="font-size:10px;color:#6b748a;font-weight:500;padding:4px 10px 4px 0;background:transparent">Type</th>'
        f'<th style="font-size:10px;color:#6b748a;font-weight:500;padding:4px 10px 4px 0;background:transparent">Event</th>'
        f'<th style="font-size:10px;color:#6b748a;font-weight:500;padding:4px 0;background:transparent">Detail</th>'
        f'</tr></thead>'
        f'<tbody>{rows}</tbody>'
        f'</table>'
        f'<div style="background:#12151c;border-left:3px solid #2d3548;border-radius:0 6px 6px 0;'
        f'padding:10px 13px">'
        f'<div style="font-size:10px;color:#6b748a;font-weight:600;letter-spacing:.06em;'
        f'text-transform:uppercase;margin-bottom:5px">Thesis Evolution</div>'
        f'<p style="font-size:11px;color:#9ba5bc;line-height:1.70;margin:0">{evo}</p>'
        f'</div>'
        f'</div>'
    )


def open_card(pos):
    pid     = pos["id"];       asset   = pos["asset"];      side    = pos["side"]
    fcls    = pos["flag_cls"]; entry_f = pos["entry_f"];    live_f  = pos["live_f"]
    stop_f  = pos["stop_f"];   trail_f = pos["trail_activate_f"]; atr_f = pos["atr_f"]
    up      = pos["unrealized_pct"]
    spct    = pos["size_pct"]; susd    = pos["size_usd"];   tstop   = pos["time_stop"]

    sign   = "+" if up >= 0 else ""
    ucls   = "ok" if up >= 0 else ("bad" if up < -1.5 else "warn")
    bcol   = _BORDER.get(fcls, "#262b35")
    rbg    = _REC_BG.get(fcls, "rgba(91,155,255,.08)")

    bar_h   = range_bar(entry_f, live_f, stop_f, trail_f)
    scores_h = score_table(pos["scores"], pos["sum"])
    chips_h  = inv_chips(pos["invalidation"])
    dev_h    = dev_section(pos.get("development"))

    return (
        f'<div class="card" style="border-left:4px solid {bcol};margin-bottom:22px">\n'

        # Header
        f'<div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:2px">\n'
        f'<div><span class="lbl">{pid}</span>\n'
        f'<div style="font-size:22px;font-weight:700;margin-top:2px">{asset} '
        f'<span style="font-size:14px;color:#8a93a6;font-weight:400">{side}</span></div>\n'
        f'<div style="font-size:11px;color:#8a93a6;margin-top:1px">'
        f'ATR&nbsp;{atr_f:.3f} &nbsp;·&nbsp; '
        f'Risk&nbsp;{spct:.2f}%&nbsp;({susd})</div></div>\n'
        f'<div style="text-align:right">{pill("OPEN", fcls)}<br>'
        f'<span class="{ucls}" style="font-size:17px;font-weight:700">{sign}{up:.2f}%</span><br>'
        f'<span style="font-size:11px;color:#8a93a6">unrealized</span></div></div>\n'

        # Range bar
        + bar_h +

        # Two-column body
        f'<div class="pos-body-grid" style="display:grid;grid-template-columns:1.6fr 1fr;'
        f'gap:22px;margin-bottom:16px">\n'

        # Left — background + thesis
        f'<div>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Background</div>\n'
        f'<p style="font-size:12px;color:#8a93a6;line-height:1.68;margin-bottom:14px">'
        f'{pos["background"]}</p>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Thesis</div>\n'
        f'<p style="font-size:12px;color:#c8d0de;line-height:1.72">{pos["thesis"]}</p>\n'
        f'</div>\n'

        # Right — scores + key vars + entry context
        f'<div>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:7px">Score (S / T / C / R)</div>\n'
        + scores_h +
        f'<div class="lbl" style="color:#5b9bff;margin:14px 0 5px">Key Variables</div>\n'
        f'<p style="font-size:11px;color:#8a93a6;line-height:1.60;margin-bottom:12px">'
        f'{pos["key_vars"]}</p>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:5px">Entry Context</div>\n'
        f'<p style="font-size:11px;color:#8a93a6;line-height:1.60;font-family:monospace">'
        f'{pos["entry_context"]}</p>\n'
        f'</div></div>\n'

        # Invalidation checklist
        f'<div style="margin-bottom:14px">\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Invalidation Checklist</div>\n'
        f'<div>{chips_h}</div></div>\n'

        # Trade development timeline
        + dev_h +

        # Recommendation + catalyst
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">\n'
        f'<div style="background:{rbg};border:1px solid {bcol}50;border-radius:7px;'
        f'padding:10px 13px">\n'
        f'<div class="lbl" style="color:{bcol};margin-bottom:4px">Recommendation</div>\n'
        f'<div style="font-size:12px;color:#e5e9f0;line-height:1.65">'
        f'{pos["recommendation"]}</div></div>\n'
        f'<div style="background:#12151c;border:1px solid #262b35;border-radius:7px;'
        f'padding:10px 13px">\n'
        f'<div class="lbl" style="color:#8a93a6;margin-bottom:4px">Next Catalyst</div>\n'
        f'<div style="font-size:12px;color:#b0b8cc;line-height:1.65">'
        f'{pos["next_catalyst"]}</div></div></div>\n'

        f'<div style="margin-top:10px;font-size:11px;color:#8a93a6">'
        f'Time-stop: {tstop}</div>\n'
        f'</div>'
    )


def pending_card(pos):
    pid    = pos["id"];        asset  = pos["asset"];        side   = pos["side"]
    scls   = pos["status_cls"]; stxt  = pos["status_txt"]
    ezone  = pos["entry_zone"]; trig  = pos["est_trigger"]
    bcol   = _BORDER.get(scls, "#262b35")
    rbg    = _REC_BG.get(scls, "rgba(91,155,255,.08)")

    scores_h = score_table(pos["scores"], pos["sum"])
    chips_h  = inv_chips(pos["invalidation"])

    return (
        f'<div class="card" style="border-left:4px solid {bcol};margin-bottom:22px">\n'

        # Header
        f'<div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:12px">\n'
        f'<div><span class="lbl">{pid}</span>\n'
        f'<div style="font-size:22px;font-weight:700;margin-top:2px">{asset} '
        f'<span style="font-size:14px;color:#8a93a6;font-weight:400">{side}</span></div></div>\n'
        f'<div style="text-align:right">{pill(stxt, scls)}<br>'
        f'<span style="font-size:12px;color:#8a93a6">Entry zone: {ezone}</span><br>'
        f'<span style="font-size:11px;color:#8a93a6">Est. trigger: {trig}</span></div></div>\n'

        # Entry criteria
        f'<div style="background:#12151c;border:1px solid {bcol}55;border-radius:7px;'
        f'padding:10px 14px;margin-bottom:16px">\n'
        f'<div class="lbl" style="color:{bcol};margin-bottom:4px">Entry Criteria</div>\n'
        f'<div style="font-size:12px;color:#e5e9f0;line-height:1.65">'
        f'{pos["entry_criteria"]}</div></div>\n'

        # Two-column: background+thesis | scores
        f'<div class="pos-body-grid" style="display:grid;grid-template-columns:1.6fr 1fr;'
        f'gap:22px;margin-bottom:16px">\n'
        f'<div>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Background</div>\n'
        f'<p style="font-size:12px;color:#8a93a6;line-height:1.68;margin-bottom:14px">'
        f'{pos["background"]}</p>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Why We Want This</div>\n'
        f'<p style="font-size:12px;color:#c8d0de;line-height:1.72">{pos["thesis"]}</p>\n'
        f'</div>\n'
        f'<div>\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:7px">Score (S / T / C / R)</div>\n'
        + scores_h +
        f'<div class="lbl" style="color:#5b9bff;margin:14px 0 5px">Key Variables</div>\n'
        f'<p style="font-size:11px;color:#8a93a6;line-height:1.60;margin-bottom:12px">'
        f'{pos["key_vars"]}</p>\n'
        f'</div></div>\n'

        # Invalidation
        f'<div style="margin-bottom:14px">\n'
        f'<div class="lbl" style="color:#5b9bff;margin-bottom:6px">Entry Invalidation</div>\n'
        f'<div>{chips_h}</div></div>\n'

        # Recommendation + catalyst
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">\n'
        f'<div style="background:{rbg};border:1px solid {bcol}50;border-radius:7px;'
        f'padding:10px 13px">\n'
        f'<div class="lbl" style="color:{bcol};margin-bottom:4px">Recommendation</div>\n'
        f'<div style="font-size:12px;color:#e5e9f0;line-height:1.65">'
        f'{pos["recommendation"]}</div></div>\n'
        f'<div style="background:#12151c;border:1px solid #262b35;border-radius:7px;'
        f'padding:10px 13px">\n'
        f'<div class="lbl" style="color:#8a93a6;margin-bottom:4px">Next Catalyst</div>\n'
        f'<div style="font-size:12px;color:#b0b8cc;line-height:1.65">'
        f'{pos["next_catalyst"]}</div></div></div>\n'
        f'</div>'
    )


def flag_row(flag):
    fid, name, scls, txt = flag
    sev     = _SEV_MAP.get(fid, "MED")
    sev_cls = "bad" if sev == "CRITICAL" else ("warn" if sev == "HIGH" else "mute")
    fired   = scls != "ok"
    id_col  = "#f87171" if scls == "bad" else ("#facc15" if scls == "warn" else "#8a93a6")
    return (
        f'<tr><td style="font-weight:700;color:{id_col}">{fid}</td>'
        f'<td>{name}</td>'
        f'<td><span class="{sev_cls}">{sev}</span></td>'
        f'<td>{pill("FIRED" if fired else "OK", scls)}</td>'
        f'<td style="font-size:12px">{txt}</td></tr>'
    )


# ── Derived counts ─────────────────────────────────────────────────────────────
flags_fired     = sum(1 for f in FLAGS if f[2] != "ok")
open_profit     = sum(1 for p in OPEN_POSITIONS if p["unrealized_pct"] >= 0)
open_risk       = sum(1 for p in OPEN_POSITIONS if p["unrealized_pct"] < 0)
pending_active  = sum(1 for p in PENDING_POSITIONS if p["status_cls"] != "bad")
heat_used_pct   = round(TOTAL_HEAT / HEAT_CAP * 100)
heat_bar_col    = "#4ade80" if heat_used_pct < 50 else ("#facc15" if heat_used_pct < 75 else "#f87171")
flags_cls       = "ok" if flags_fired == 0 else "warn"
flags_txt       = ", ".join(f[0] for f in FLAGS if f[2] != "ok") or "All clear"

open_cards_html    = "\n".join(open_card(p)    for p in OPEN_POSITIONS)
pending_cards_html = "\n".join(pending_card(p) for p in PENDING_POSITIONS)
flag_rows_html     = "\n".join(flag_row(f)     for f in FLAGS)

# ── Page ───────────────────────────────────────────────────────────────────────
PAGE = (
    f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    f'<meta charset="UTF-8">\n'
    f'<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
    f'<title>Positions Monitor &mdash; {TODAY}</title>\n'
    f'<style>{CSS}</style>\n'
    f'</head>\n<body>\n<div class="container">\n'

    f'<h1>Positions Monitor</h1>\n'
    f'<p class="sub">Generated {GEN_TIME} &nbsp;|&nbsp; Source: {SNAPSHOT} '
    f'&nbsp;|&nbsp; NAV ${PORT_NAV:,}</p>\n'

    # Status bar
    f'<div class="status-bar">\n'
    f'<div style="flex:1">\n'
    f'<div style="font-size:13px;font-weight:700">{REGIME_LABEL}</div>\n'
    f'<div style="font-size:12px;color:var(--muted)">{REGIME_SUB}</div>\n'
    f'</div>\n'
    f'<div style="text-align:right;min-width:140px">\n'
    f'<div class="lbl">Portfolio Heat</div>\n'
    f'<div style="font-size:18px;font-weight:700" class="{HEAT_CLS}">{TOTAL_HEAT:.2f}%</div>\n'
    f'<div class="heat-track" style="width:140px">'
    f'<div class="heat-fill" style="width:{heat_used_pct}%;background:{heat_bar_col}"></div>'
    f'</div>\n'
    f'<div style="font-size:10px;color:var(--muted)">{TOTAL_HEAT:.2f}% / {HEAT_CAP}% cap</div>\n'
    f'</div>\n'
    f'<div style="text-align:right;min-width:100px">\n'
    f'<div class="lbl">Flags</div>\n'
    f'<div style="font-size:18px;font-weight:700" class="{flags_cls}">{flags_fired} fired</div>\n'
    f'<div style="font-size:11px;color:var(--muted)">{flags_txt}</div>\n'
    f'</div></div>\n'

    # Exec cards
    f'<div class="grid-4" style="margin-bottom:4px">\n'
    f'<div class="card"><div class="lbl">Open Positions</div>'
    f'<div style="font-size:26px;font-weight:700;margin-top:4px">{len(OPEN_POSITIONS)}</div>'
    f'<div style="font-size:12px;color:var(--muted);margin-top:4px">'
    f'<span class="ok">{open_profit} in profit</span>'
    f' &nbsp; <span class="warn">{open_risk} at risk</span></div></div>\n'
    f'<div class="card"><div class="lbl">Pending Triggers</div>'
    f'<div style="font-size:26px;font-weight:700;margin-top:4px">{pending_active}</div>'
    f'<div style="font-size:12px;color:var(--muted);margin-top:4px">'
    f'{" · ".join(p["asset"] for p in PENDING_POSITIONS if p["status_cls"] != "bad")}'
    f'</div></div>\n'
    f'<div class="card"><div class="lbl">Heat Used</div>'
    f'<div style="font-size:26px;font-weight:700;margin-top:4px" class="{HEAT_CLS}">'
    f'{TOTAL_HEAT:.2f}%</div>'
    f'<div style="font-size:12px;color:var(--muted);margin-top:4px">'
    f'{HEAT_CAP - TOTAL_HEAT:.2f}% headroom to cap</div></div>\n'
    f'<div class="card"><div class="lbl">Flags Fired</div>'
    f'<div style="font-size:26px;font-weight:700;margin-top:4px" class="{flags_cls}">'
    f'{flags_fired}&thinsp;<span style="font-size:14px;color:var(--muted)">/ {len(FLAGS)}</span>'
    f'</div>'
    f'<div style="font-size:12px;color:var(--muted);margin-top:4px">{flags_txt}</div>'
    f'</div></div>\n'

    # Open positions
    f'<h2>Open Positions ({len(OPEN_POSITIONS)})</h2>\n'
    + open_cards_html + "\n"

    # Pending positions
    + f'<h2>Pending Positions ({len(PENDING_POSITIONS)})</h2>\n'
    + pending_cards_html + "\n"

    # Flag panel
    + f'<h2>Flag Panel</h2>\n'
    f'<table>\n'
    f'<thead><tr><th>Flag</th><th>Condition</th><th>Severity</th>'
    f'<th>Status</th><th>Detail</th></tr></thead>\n'
    f'<tbody>{flag_rows_html}</tbody>\n'
    f'</table>\n'

    # Footer
    f'<div class="footer">'
    f'Positions Monitor v2 &nbsp;|&nbsp; {TODAY} &nbsp;|&nbsp; Source: {SNAPSHOT}<br>'
    f'Read-only observer — does not modify Memory.md, place orders, or produce trade recommendations.<br>'
    f'Full thesis: <code>report-{TODAY}-trade-rec.html</code> &nbsp;|&nbsp; '
    f'Positions state: <code>framework/Memory.md §2</code>'
    f'</div>\n'

    f'</div>\n</body>\n</html>'
)

out      = Path(TODAY)
out.mkdir(exist_ok=True)
out_path = out / f"positions-monitor-{TODAY}.html"
out_path.write_text(PAGE, encoding="utf-8")
print(f"Written: {out_path}")
