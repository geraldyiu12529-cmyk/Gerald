# News & Events Log

Daily flash-news and geopolitics capture, written by the `daily-news-events-810pm-v2` scheduled task. Used alongside the daily market brief to explain regime shifts and catalyst repricing.

## Structure

- `news-YYYY-MM-DD.md` — full daily log (geopolitics, wars, macro releases, econ calendar, corporate/tech, crypto/regulatory, surprise events). Written fresh each night.
- `archive-summary.md` — rolling condensed summary of items older than 7 days. Lossy by design: only material items that still affect active regime or open positions survive. Everything else is dropped.

## Retention rule

News files follow the **master Retention Policy** in `../Retention Policy.md`. In short:

- **0–7 days:** full file lives at root (Tier 1)
- **8–30 days:** moved to `../archive/YYYY-MM/` by the Sunday workspace-tidy task (Tier 2)
- **31+ days:** originals deleted; content folded into the monthly digest at `../archive/YYYY-MM-digest.md` (Tier 3)

The workspace-tidy task owns the lifecycle — do not implement separate archival logic here. If a news item is still driving the current regime or tied to an open position in Memory.md, the tidy task's pin rule will protect it automatically.

## Format for daily files

Each `news-YYYY-MM-DD.md` uses these sections (omit any that have nothing):

1. **Geopolitics & political risk** — armed conflicts, sanctions, military/naval incidents, diplomatic breaks, territorial disputes, coups, regime changes, election crises, political instability. Search by category (sanctions, military, conflict, diplomatic crisis, territorial dispute, election crisis, regime change), not by named conflict — conflicts end, new ones begin. See **Current hotspots** below for active focus areas.
2. **Macro data releases today** — CPI, PPI, NFP, PCE, inflation/growth prints. **Actual vs. expected vs. prior ONLY — not levels.** Brief owns the level; this file owns the surprise delta.
3. **Economic calendar — next 48h cut** — upcoming releases and events. **48h window only**; the 2-week rolling list lives in the brief §5. News §3 carries only the next-48h tactical cut.
4. **Corporate / tech** — universe-relevant earnings, guidance changes, M&A, product launches (INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC). Capture EPS/rev/guide/margin + price reaction.
5. **Crypto & regulatory** — ETF flows, SEC/CFTC/FinCEN enforcement actions, exchange incidents, on-chain events, CLARITY/GENIUS policy moves
6. **Central bank & policy communications** — FOMC, ECB, BoJ, BoE, PBoC, RBA statements; Fed Chair speeches, testimony, dot-plot delta; Treasury/Commerce/USTR principal statements. Apply the 4-criterion political-communication filter below.
7. **Credit & sovereign events** — Moody's/S&P/Fitch rating actions, CDS widening, corporate defaults, distressed exchanges, bank stress regulatory actions.
8. **Flash / surprise events** — anything unscheduled that moved markets materially. Omit if none.
9. **Regime implications** — ≤3 lines max: which items above actually shift regime readings in Memory.md, and which are noise. Handoff surface to the brief.

Every item should cite source and be dated. No padding, no narrative. Items that did not move a market or inform a decision do not belong here.

## Current geopolitical hotspots

**Review this list monthly.** Remove entries when conflicts end or de-escalate below market-moving threshold; add new ones as they emerge. The daily news task should always search both the generic categories in §1 above AND these specific terms.

| Hotspot | Key search terms | Added | Status |
|---|---|---|---|
| Iran–US conflict | Iran, Hormuz, blockade, Iran sanctions, Iran diplomacy | 2026-04-14 | Active — naval blockade in effect |
| Russia–Ukraine war | Ukraine, Russia, Donbas, Black Sea, Ukraine ceasefire | 2026-04-14 | Active |
| US–China trade tensions | US China tariffs, tech export controls, Taiwan Strait, South China Sea | 2026-04-14 | Active |
| Middle East broader | Israel, Gaza, Houthi, Red Sea, Suez | 2026-04-14 | Active |

When a hotspot is removed, move it to a "Resolved" section below so there's a record. If a resolved conflict re-escalates, move it back.

## Scope — News vs Market Brief (non-overlap rule)

The news file and the market brief run 10 minutes apart and must own disjoint jobscopes:

| Question | Owner |
|----------|-------|
| "What is the current level of X?" | market-brief |
| "What regime are we in?" | market-brief |
| "What's the S/T/C/R score for each asset?" | market-brief |
| "What is the rolling 2-week catalyst list?" | market-brief §5 |
| "What was released in the last 24h, and was it a surprise?" | news §2 (actual vs expected ONLY) |
| "What geopolitical / regulatory / corporate event occurred?" | news §1, §4, §5, §6, §7 |
| "What are the next 48h events?" | news §3 (48h cut of brief §5) |
| "Which items reprice the regime?" | news §9 (Regime Implications, ≤3 lines) |

For data releases: news captures the surprise delta (actual vs expected vs prior) only; the brief captures the resulting level the next day. For level milestones ("record high"): news owns the event-character, brief owns the level. Never restate a variable level in news — the brief owns it.

See `/mnt/Trade/literature-review-2026-04-17-news-events.md` §2 for the full handoff rule.

## Source Hierarchy

Three tiers, per taxonomy §4:

- **Tier 1 (primary/official):** FederalReserve.gov, BLS, BEA, Census, SEC, CFTC, FinCEN, USTR, OFAC, EIA, company IR, SEC EDGAR, Moody's/S&P/Fitch press releases, Blockchain.info, CoinGlass, CryptoQuant, White House press releases, C-SPAN, verified WH X account.
- **Tier 2 (wire/professional):** Reuters, AP (low bias, foundation wires), Bloomberg terminal (left-center bias per MBFC 2024; use for numeric data, de-prefer for political framing), FT, WSJ, Al Jazeera (MENA), France 24 (EU), Euronews.
- **Tier 3 (aggregator/retail):** Yahoo Finance, TradingView, CoinDesk, CoinPedia, CoinTelegraph, Seeking Alpha, GuruFocus, MarketWatch, TheStreet, Investing.com, Fortune, X/Twitter. USE ONLY when Tier 1/2 is unavailable; corroborate unverified social posts with Tier 1/2 within 15–30 min before surfacing.

**Rule:** log one source per story at the highest available tier. Do not cite Tier 3 when Tier 1/2 carries the same fact — that is recycled-wire noise.

## Noise Filters (10 rules)

Items that look news-like but do NOT inform a decision and must NOT enter the daily file:

1. **No analyst chatter without recommendation change.** Reiterations and price-target nudges fail the filter (Loh-Stulz NBER 14971, 2009).
2. **No recycled wire.** One source per story at the highest tier; AP/Reuters are the foundation wires.
3. **No sensational political threat without implementation history.** Log with ⟨noise-probable⟩ tag; do not drive regime repricing.
4. **No anonymous speculation.** Require named reporter or on-record source.
5. **No price-action-as-news.** Brief owns the level; restating it here is double-count.
6. **No non-power-holder political commentary on equity markets.** Must pass §Political-Communication Filter.
7. **No Grade-C crypto price-prediction headlines.** "Analyst says BTC could hit $X" — no mechanism, rejected.
8. **No unverified X/Twitter.** Require Tier 1/2 corroboration within 15–30 min.
9. **Flag Bloomberg for left-center framing on political stories.** Prefer AP/Reuters for neutral political framing; use Bloomberg for numeric/data speed.
10. **No hotspot restatement.** If Memory.md §6 already carries a catalyst entry, the news file notes the delta since last update only — not the full history.

## Political-Communication 4-Criterion Filter

A statement enters the news file as a signal only if **all four** pass:

1. **Credibility** — speaker has publicly spoken on this policy before with follow-through ≥ 50% of the time.
2. **Implementation power** — speaker directly controls (or votes on) the mentioned lever.
3. **Asset-exposure precision** — statement names a specific asset class, sector, or rate/price.
4. **Prior follow-through** — at least one prior similar statement has resulted in action within 30 days.

If a statement fails any one of these, log it with ⟨noise-probable⟩ tag; do not treat as a regime-repricing signal. See `/mnt/Trade/literature-review-2026-04-17-news-events.md` §3.9 for evidence and case examples.
