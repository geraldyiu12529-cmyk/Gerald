---
name: news-events
description: "Daily news, geopolitics, macro releases, corporate earnings, crypto regulatory, and flash-event capture for Gerald's trading workspace. Searches by category (not by named conflict), uses the hotspot list from news-events/README.md, and writes a structured file the trade-rec skill consumes downstream. Use this skill whenever the user asks for 'news capture', 'daily news', 'what happened today', 'overnight headlines', 'geopolitics update', 'econ calendar', 'flash events', or asks 'what moved markets'. Also use when the scheduled task `daily-news-events-810pm-v2` fires. Not for regime scoring or trade recommendations — use the market-brief or daily-trade-rec skills for those."
---

# Daily News & Events Capture

Produces the day's news and events log for Gerald's `/Trade/news-events/` directory. The output is a structured summary of geopolitics, macro data, economic calendar, corporate/tech, crypto/regulatory, central bank communications, credit events, flash events, and regime implications — consumed by the trade-rec skill as part of its upstream synthesis.

Local timezone is UTC+8. The canonical slot is 20:10 UTC+8 = 08:10 ET = US pre-open. Use today's local date in the filename. If the file already exists from an earlier run the same day, overwrite and bump the version tag in the title (`v2`, `v3`, …).

---

## Step 1 — Mandatory startup reads

1. `/mnt/.auto-memory/MEMORY.md` — scan index, open relevant memory files
2. `/mnt/Trade/Memory.md` — open positions (§2), catalysts (§6) — needed to judge what's noise vs signal
2b. `/mnt/Trade/master-data-log.xlsx` — read the latest row of **RegimeHistory** (current regime state) using openpyxl
3. `/mnt/Trade/news-events/README.md` — the format spec, current hotspot list, source hierarchy, noise filters, political-communication filter, and retention rules
4. The most recent prior news file (yesterday's `news-YYYY-MM-DD.md`) — for continuity and delta detection

Note: Methodology Prompt.md is not loaded by this skill. The news skill does not score or grade variables — it only needs the asset universe (hardcoded in Step 5) and the catalyst calendar (from Memory.md §6). The brief and trade-rec skills load the methodology.

If the README is missing, stop and surface the gap.

## Step 1.5 — Non-overlap check

Before searching, confirm what you will NOT capture because the market-brief owns it:

- Current variable levels (VIX, DXY, rates, prices) — brief §2 owns these
- Regime label and S/T/C/R scores — brief §1, §3
- 2-week rolling catalyst list — brief §5 (news §3 carries ONLY the 48h cut)
- Level milestones ("record high") mentioned without event-character — brief §2 carries the level; news surfaces the event-character only

For data releases, news captures the **surprise delta** (actual vs expected vs prior) only; the brief captures the resulting level the next day. Never restate a variable level in the news file.

See `news-events/README.md` §Scope — News vs Market Brief for the authoritative handoff matrix.

## Step 2 — Geopolitics & political risk search

Search by **category**, not by named conflict. Conflicts end, new ones begin. Trade/tariff/sanctions actions are **excluded** from this step — they belong to Step 4.5 (policy communications) as regulatory events, not geopolitical conflicts.

**Generic category searches (always run):**
- `sanctions today`
- `military conflict today`
- `diplomatic crisis today`
- `territorial dispute today`
- `election crisis today`
- `regime change coup today`
- `naval incident today`
- `blockade embargo today`

**Hotspot-specific searches (from README.md hotspot table):**
Read the hotspot table from `/mnt/Trade/news-events/README.md` and run a targeted search for each active hotspot using its key search terms.

**Rules:**
- Every item must cite source and date
- No padding, no narrative — only items that moved a market or inform a decision
- If a hotspot appears to have de-escalated or resolved, note it for the README update in Step 8

## Step 3 — Macro data releases

Search for today's economic data releases:
- `US economic data releases today`
- `CPI PPI NFP PCE release today` (if any major prints are expected)
- `central bank rate decision today`
- `Fed FOMC statement today` (if scheduled)
- `ECB BOJ BOE rate decision today` (if scheduled)

For each release found:
- Report **actual vs expected vs prior** ONLY — do NOT restate the level
- Note whether the print is inflationary/deflationary, above/below consensus
- Flag tier-1 prints (CPI, PPI, NFP, PCE, FOMC) explicitly

The brief owns the resulting variable level the next day. This step owns the surprise delta.

## Step 4 — Economic calendar (next 48h)

Search: `US economic calendar this week`

Build a table, **48h window only**:

| Date/Time (ET) | Event | Impact (High/Medium/Low) | Notes |

Include any rescheduled events. Compare against Memory.md §6 and flag changes.

The 2-week rolling list is owned by the brief §5; do not duplicate it here.

## Step 4.5 — Central bank & policy communications

Search:
- `{central bank} statement today` (Fed, ECB, BoJ, BoE, PBoC, RBA — as scheduled)
- `Fed Chair speech today`
- `Treasury Secretary statement today`
- `USTR statement today`
- `Congressional hearing on economy today`
- `executive order trade tariff today`

Apply the **4-criterion political-communication filter** (see README §Political-Communication Filter) before surfacing any political statement. Statements failing any one criterion are logged with `⟨noise-probable⟩` tag and do not drive regime repricing.

For FOMC decisions specifically, extract:
- Policy rate (actual vs prior)
- Dot-plot delta (median SEP shift)
- 2Y and 10Y yield reaction in the announcement window
- Fed-funds-futures surprise in bps (Kuttner 2001 identification)

For other principal statements (Treasury/USTR/WH), capture the specific asset/sector named and any implementation dates.

## Step 5 — Corporate & tech (universe only)

Search for earnings, guidance changes, M&A, and product launches for the asset universe: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC (and ETFs: SPY, QQQ, EWY, XLE).

**Catalyst-filtered search strategy:** Before running any ticker searches, read the Catalysts section from Memory.md §6. Extract tickers with scheduled events in the next 48 hours — call this the **active ticker list**.

1. **Active tickers** (from the 48h catalyst list): run both targeted searches per ticker:
   - `{TICKER} earnings today` / `{TICKER} Q1 results today`
   - `{TICKER} news today`
2. **Universe catch-all** (for everything else — typically 1–2 searches total):
   - `tech earnings today` — catches any universe ticker with unscheduled news
   - `semiconductor earnings today` if TSM/NVDA/INTC/MU are in the active window
3. Do NOT run individual `{TICKER} news today` searches for tickers with no scheduled catalyst. On a typical day, 10 of 12 universe tickers have no material news — targeted searches produce empty results and waste search budget.

For each earnings item found, capture EPS/rev/guide/margin + pre-market/intraday price reaction.

Do not include companies outside the universe unless they directly affect a universe name (e.g., a supplier to NVDA).

## Step 6 — Crypto & regulatory

Search:
- `Bitcoin ETF flows today`
- `Ethereum ETF flows today`
- `crypto regulation news today`
- `SEC crypto enforcement today`
- `Bitcoin exchange news today`
- `stablecoin regulation today`
- `CLARITY Act` / `GENIUS Act` (when markup or vote scheduled)

Cover: ETF flow data, SEC/CFTC/FinCEN enforcement actions, exchange incidents, on-chain events, and policy moves.

## Step 6.5 — Credit & sovereign events

Search:
- `Moody's rating action today`
- `S&P Global rating action today`
- `Fitch rating action today`
- `sovereign credit downgrade today`
- `corporate default today`
- `bank stress regulatory action today`
- `CDS spread widening today`

For each action, capture: issuer, old rating, new rating, outlook change, and any primary-market impact visible. Note pre-announcement drift if detectable (BIS WP 207 — spreads typically widen 30–60 days ahead of actual downgrade).

## Step 7 — Flash / surprise events

Search: `market moving news today`, `surprise event markets today`, `exchange halt today`, `circuit breaker equities today`

Capture anything unscheduled that moved markets materially. If nothing qualifies, omit this section entirely.

## Step 8 — Write the output file

Path: `/mnt/Trade/news-events/news-{YYYY-MM-DD}.md`

Use this format:

```
# News & Events — YYYY-MM-DD (vN)

**Local:** HH:MM UTC+8 (HH:MM ET, US pre-open) — scheduled daily news capture[, vN refresh].

---

## 1. Geopolitics & Political Risk
[Items with source citations — exclude trade/tariffs, those belong in §6]

## 2. Macro Data Releases Today (YYYY-MM-DD)
[Actual vs expected vs prior ONLY — NOT levels. Brief owns the level next day.]

## 3. Economic Calendar — Next 48h
[48h cut ONLY; 2-week list lives in brief §5]
[Table: Date/Time ET | Event | Impact | Notes]

## 4. Corporate & Tech (Universe Only)
[EPS/rev/guide/margin + price reaction, universe tickers only]

## 5. Crypto & Regulatory
[ETF flows, SEC/CFTC/FinCEN enforcement, on-chain, CLARITY/GENIUS progress]

## 6. Central Bank & Policy Communications
[FOMC, ECB, BoJ, BoE, Fed speeches, Treasury/USTR — apply 4-criterion filter]

## 7. Credit & Sovereign Events
[Rating actions, CDS widening, defaults, bank stress]

## 8. Flash / Surprise Events
[Omit if none]

## 9. Regime Implications
[≤3 lines max: which items above actually shift regime readings in Memory.md, and which are noise. Handoff surface to brief.]
```

## Step 9 — Update Memory.md §6 (Catalysts)

After writing the news file, check if any catalyst dates in Memory.md §6 need updating:
- Rescheduled events (update dates)
- New catalysts discovered (add to §6)
- Expired catalysts (mark as passed, note outcome)

Do not batch — update immediately.

## Step 10 — Write catalysts-cache-YYYY-MM-DD.json (E4 shared cache)

After completing Steps 1–9, write a machine-readable cache that brief, trade-rec, weekly-review, and Memory sync consume downstream. This is the **single writer**; all other producers read-and-render instead of re-parsing. Eliminates ~80–120K tokens/month of cross-file duplication.

**Helper:** `/mnt/Trade/scripts/catalysts_cache.py` (API: `write_catalysts`, `read_catalysts`, `filter_for_asset`, `filter_severity`, `to_markdown_table`).

**Process:**

1. Extract every dated catalyst within the next 30 days from the narrative (earnings, central-bank decisions, geopolitical expiries, data releases, nominations, regulatory deadlines, etc.).

2. For each, build a dict with required fields `date` (YYYY-MM-DD), `event` (short description), `asset_impact` (uppercase ticker list), `severity` (critical|high|med|low). Optional: `direction_hint` (binary|bullish_risk|bearish_risk|bullish_safe_haven|bearish_safe_haven|neutral), `source` (news-YYYY-MM-DD.md §N), `notes`.

3. Call the writer:

   ```python
   import sys; sys.path.insert(0, '/mnt/Trade/scripts')
   from catalysts_cache import write_catalysts
   write_catalysts('YYYY-MM-DD', catalysts_list, horizon_days=30)
   ```

   Writes both `/mnt/Trade/catalysts-cache-YYYY-MM-DD.json` (root, for globbing) and `/mnt/Trade/.catalysts-cache/catalysts-cache-YYYY-MM-DD.json` (stable cache dir).

4. Append one-line confirmation to the news file tail:
   `*Catalysts cache written: N events, severity breakdown [crit:X, high:Y, med:Z].*`

**Rules:**
- `strict=True` default — bad inputs raise. If validation fails, the news file still writes; log the error in the news tail as `**Catalysts cache FAILED: <reason>**` so downstream falls back to inline parsing.
- Only dated events. "Sometime this quarter" / "awaiting announcement" stays in narrative.
- Re-runs overwrite (authoritative view, not append-only log).
- Even if only 1 catalyst is datable, write the cache — downstream prefers empty-but-fresh over missing.

---

## Rules

- Every item must cite source and be dated. No padding, no narrative.
- Items that did not move a market or inform a decision do not belong here.
- Search by category, not by named conflict. The hotspot list supplements categories, not replaces them.
- Do not include companies outside the asset universe unless they directly affect a universe name.
- §9 (Regime Implications) is mandatory and must be ≤3 lines. Its job is to separate signal from noise for the downstream trade rec.
- Retention is owned by the master Retention Policy and the workspace-tidy task. Do not implement separate archival logic.
- If a geopolitical hotspot has resolved or de-escalated, note it so the README can be updated.
- Apply the **Tier 1/2/3 source hierarchy** per README §Source Hierarchy — prefer the highest tier that carries the fact. Do not cite Tier 3 when Tier 1/2 carries the same story (recycled-wire noise).
- Apply the **10-rule noise filter** per README §Noise Filters before surfacing any item.
- For political communications, apply the **4-criterion filter** per README §Political-Communication Filter. Items failing any criterion are tagged `⟨noise-probable⟩` and do not drive regime repricing.
- **Never restate a variable level** — the brief owns the level. News owns the surprise, the event-character, and the reaction.
- §2 is actual-vs-expected ONLY, not levels. §3 is the 48h cut ONLY, not the 2-week list.
