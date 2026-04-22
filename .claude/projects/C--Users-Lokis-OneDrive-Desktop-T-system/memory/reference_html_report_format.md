# Reference — HTML Report Format (Trade Rec)

**Locked:** 2026-04-21
**Generator:** `scripts/gen_trade_rec_html.py` (canonical — never write HTML manually)
**Output path:** `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html`

## How to generate

1. Update the `# ═══ PER-RUN DATA` block at the top of `scripts/gen_trade_rec_html.py`
2. Run: `python scripts/gen_trade_rec_html.py`
3. HTML is written automatically — no manual editing

## Canonical section order (do not reorder)

1. Header + sub (version, status, V026/V027/MOVE)
2. **Data Freshness strip** — scrollable tiles, traffic-light: green=LIVE A, blue=LIVE B, yellow=STALE, red=MISSING
3. **Asset Universe** — static pill grid by asset class (equity/ETF/commodity/crypto)
4. **Material Delta box** — v2+ only; empty `DELTA_ITEMS=[]` for v1
5. **Executive Summary** — grid-4 cards (promoted, near-miss, regime, heat)
6. **Overlay Gate** — Faber TAA sleeve table
7. **Data Collected — Key Variables**
   - Audit Additions (V026/V027/V028)
   - **V026 Residual Momentum — Full Equity Universe** — all 15 tickers, inline bar, ±2% boundary
   - Meta Additions (V029–V032)
8. **Score Stacking** — Chart.js stacked bar (promoted + near-miss)
9. **Factor Exposure Aggregate** — size-weighted S/T/C/R bars + per-position table; auto-computed
10. **Recommendations** — columns: Asset | Dir | Entry | Stop | Target | Size | Catalyst | Grade (S+1(A)...) | Sleeve
11. **Signal Age & Time-Decay** — countdown bars, urgency color (red<10d, yellow<20d, green≥20d)
12. **Pre-Entry Checklists** — 8-item table per promoted signal
13. **Regime Sensitivity — Stress Test** — positions × scenarios matrix, color-coded cells
14. **Catalyst Calendar** — Chart.js priority bar + table
15. **Closed-Trade Context** — prior pipeline history per asset; empty list = "first entry" note
16. Near-Misses
17. Open Positions (all)
18. Data Gap Closure — Grade A doughnut + upstream coverage list
19. Discussion — 4–6 analyst narrative paragraphs
20. Memory Updates Applied
21. Footer (sources A + B, version, time)

## CSS / JS dependencies

- Chart.js 4.4.0 CDN: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`
- CSS variables: `--bg:#0f1115; --card:#171a21; --muted:#8a93a6; --fg:#e5e9f0; --accent:#5b9bff; --green:#4ade80; --red:#f87171; --yellow:#facc15; --border:#262b35;`
- All CSS inline — no external stylesheets

## Charts

- `scoreBar` — stacked horizontal bar (promoted signals S/T/C/R)
- `nearMissBar` — stacked horizontal bar (near-miss S/T/C/R)
- `catCal` — vertical bar (catalyst priority by date)
- `gapDoughnut` — doughnut (Grade A LIVE / STALE / MISSING)

## Analyst sections added 2026-04-21

- **Data Freshness strip**: operational decision — can I trust today's scores before reading anything?
- **V026 full table**: who's approaching the ±2% T-threshold next run?
- **Factor Exposure Aggregate**: is the portfolio momentum-heavy, catalyst-light, R-confirmed?
- **Signal Age**: how much time pressure on each open/pending signal?
- **Regime Sensitivity**: which positions cascade-exit simultaneously under each stress scenario?
- **Closed-Trade Context**: does current thesis have a prior track record in this pipeline?

## Reference in SKILL.md

daily-trade-rec SKILL.md Step 10 is the authoritative instruction for populating and running the generator each trade-rec run.
