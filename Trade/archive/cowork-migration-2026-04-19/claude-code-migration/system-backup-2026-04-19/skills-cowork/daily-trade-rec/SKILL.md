---
name: daily-trade-rec
description: Produces Gerald's pre-open trade recommendation by synthesising the day's market brief, news capture, US close snapshot, and weekly regime review through the 8-step evidence-graded methodology and Risk Rules pre-entry checklist. Logs every promoted and near-miss signal to the SignalLedger sheet in `master-data-log.xlsx` for out-of-sample tracking. Also closes fail-loud Grade-A data gaps via web search when asked. Use when Gerald says "trade rec", "trade recommendation", "pre-open rec", "daily rec", "trade synthesis", "run the 8-step", "score the book", or "tell me what to trade today", even without naming the file. Also triggers on scheduled task `daily-trade-recommendation-820pm-v2`. Not for generic market commentary — use market-brief or news-events instead.
---

# Daily Trade Recommendation

Produces the day's pre-open trade rec for Gerald's `/Trade/` workspace. The output is a decision document, not commentary: every section either promotes a trade to entry or explains exactly why it didn't.

Local timezone is UTC+8. The canonical slot is 20:20 UTC+8 = 08:20 ET = US pre-open. Use today's local date in the filename. If the file already exists from an earlier run the same day, overwrite and bump the version tag in the title (`v2`, `v3`, …) so the lineage is auditable.

---

## Step 0 — Delta-check gate (runs before any other step)

Before loading any files, check whether today's run is necessary:

1. Find the most recent prior rec file: `trade-rec-*.md` in `/mnt/Trade/`.
2. Get the mtime of that rec file.
3. Check the mtime of the three upstream artifacts:
   - `market-brief-{today}.md` (today's date, local UTC+8)
   - `news-events/news-{today}.md` (today's date)
   - Most recent `us-close-snapshot-*.md`

```python
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

trade_dir = Path('/mnt/Trade')
utc8 = timezone(timedelta(hours=8))
today = datetime.now(utc8).strftime('%Y-%m-%d')

prior_recs = sorted(trade_dir.glob('trade-rec-*.md'))
last_rec_mtime = os.path.getmtime(prior_recs[-1]) if prior_recs else 0

upstream = [
    trade_dir / f'market-brief-{today}.md',
    trade_dir / f'news-events/news-{today}.md',
]
close_snaps = sorted(trade_dir.glob('us-close-snapshot-*.md'))
if close_snaps:
    upstream.append(close_snaps[-1])

changed = any(
    p.exists() and os.path.getmtime(p) > last_rec_mtime
    for p in upstream
)
```

- If `changed` is **False**: append one line to `/mnt/Trade/trade-rec-{today}.md`: `<!-- No-change revalidation {HH:MM} UTC+8: upstream artifacts unchanged since last rec. Scores carried forward. -->` — then print `Delta-check: no upstream changes detected. Carrying forward prior rec.` and **exit immediately. Do not execute Steps 1–10.**
- If `changed` is **True**: proceed to Step 1 normally.

This gate does not affect the first run of the day or any run following a new brief or news file.

---

## Step 1 — Mandatory startup reads (in order)

Before any analysis, read all of the following. The first four are framework; the next four are today's upstream evidence and must all be cross-checked.

**Framework:**
1. `/mnt/.auto-memory/MEMORY.md` — scan index, open any relevant memory files
2. `/mnt/Trade/Methodology Prompt.md` — the 8-step framework
3. `/mnt/Trade/Risk Rules.md` — binding pre-entry checklist and sizing policy
4. `/mnt/Trade/Memory.md` — open positions, watchlist, catalysts, lessons
5. `/mnt/Trade/master-data-log.xlsx` — read the latest row of `RegimeHistory` (regime label) and `DailyVariables` (current readings) using openpyxl. Also read all OPEN rows from `SignalLedger` for deduplication in Step 8.

**Today's upstream artifacts (all dated YYYY-MM-DD = today local):**
5. `/mnt/Trade/market-brief-{YYYY-MM-DD}.md` — produced by the 20:00 brief task. Pull regime label, scorecard, levels, catalyst calendar.
6. `/mnt/Trade/news-events/news-{YYYY-MM-DD}.md` — produced by the 20:10 news task. Pull overnight headlines, geopolitics, econ-calendar surprises.
7. `/mnt/Trade/us-close-snapshot-{YYYY-MM-DD}.md` (or most recent prior trading day if today is Mon) — post-close delta from the prior US session.
8. `/mnt/Trade/weekly-review-{most-recent-Sunday}.md` — week's regime trajectory and gating constraints.
9. *(optional)* Most recent `/mnt/Trade/signal-review-*.md` — read only the `## 8. Escalation Flags` section if it exists. If the section is present, carry the flags forward into the rec's §2 (Regime Read) as a one-line notice per flag.
10. **(Phase 3, post-2026-04-25)** `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` — produced by `preflight-meta-additions-1952pm` at 19:52. Extract `overlay_gate_status` (per-sleeve ON/OFF), `v027_regime_bucket`, `v029_bab_spread`. If missing, treat as fail-loud — Step 1.5 blocks ALL Phase-3-gated sleeves and logs Block_Reason=OverlayStagingMissing in Step 8.

If a framework file is missing, stop and surface the gap — do not fabricate the methodology. If an upstream artifact is missing, log it under "Data Gaps" in the output and proceed; do not silently skip. The reason these four upstream files are non-negotiable is that today's recommendation must be reproducible from named, dated source files; if you can't cite where a fact came from, it can't carry a Grade-A claim.

## Step 1.5 — Overlay Regime Gate (Phase 3, added 2026-04-25)

This step sits between Step 1 (reads) and Step 2 (synthesis). It is **non-additive to Sum** — it is a binary sleeve-on/sleeve-off switch that multiplies post-Sum position size by 0 for any gated-off sleeve. Authoritative: `Methodology Prompt.md §Step 1.5` and `Risk Rules.md §4.B, §7 item 7, §8`.

**Inputs (from the staging file read in Step 1 item 10):**

- `overlay_gate_status` — per-sleeve ON/OFF from V033/V034/V035 (Faber 10m-SMA at previous month-end close).
- `v027_regime_bucket` — expansion / neutral / contraction. Drives Risk Rules §1.B gross-exposure tier.
- `v029_bab_spread` — USMV − SPLV 12m. If spread > 0, BAB sleeve is active (long low-β / short high-β stocks); if ≤ 0, ANTI-BAB and the sleeve is flat this month.
- `v030_dealergamma` — expected MISSING until subscription confirmed; do not block on its absence.

**Sleeve mapping (asset class → sleeve):**

| Asset class | Gated by | Variables in scope |
|---|---|---|
| Equity (SPY, QQQ, individual stocks) | V033 SPY Faber gate | NVDA, TSLA, AAPL, GOOGL, AMZN, META, TSM, INTC, MU, PYPL, PLTR, WDC, SPY, QQQ |
| International equity | V033 EFA optional | EWJ, EWY |
| Commodity | V034 GSCI Faber gate | Brent, WTI, Gold, Silver, Copper, Palladium, Platinum |
| Crypto | V035 BTC-USD Faber gate | BTC, ETH |
| FX, rates | Not gated (no overlay applies) | EURUSD, USDJPY, DGS2, DGS10 |

**Gate-application logic (per asset under scoring):**

1. Identify the asset's sleeve from the table above.
2. If the sleeve is **ON**: proceed to Step 2 normally. Signal is entry-eligible.
3. If the sleeve is **OFF**: the asset is still scored through Steps 2–5 (S/T/C/R, Sum, invalidation, stop, target) because the ledger needs the full score record, but `Taken=NO` and `Block_Reason=OverlayGateOff` will be written in Step 8 regardless of |Sum|. The §3 Recommendations Table omits the row; the §4 Theses Not Taken section flags it.
4. If the sleeve status is `MISSING` (staging file absent or staging row missing for that sleeve): treat as **OFF** (fail-loud default). Block_Reason=OverlayStagingMissing.

**Gating is non-additive.** Do NOT reduce S/T/C/R or Sum because a sleeve is OFF. The Sum is what the methodology says it is; the overlay just prevents today's *execution* on that sleeve.

**V027 sizing tier (from v027_regime_bucket):**

- `expansion` → full inverse-ATR sizing (no tier adjustment)
- `neutral` → standard sizing
- `contraction` → halve gross exposure on all risk-asset sleeves (binds alongside quarter-Kelly; take the more restrictive)

The V027 tier is applied *after* Step 5 per-position sizing is computed. Record the tier in the §7 Pre-Entry Checklist (item 8) and in SignalLedger col 34.

**V029 BAB sleeve weight:**

- If `v029_bab_spread > 0` (BAB regime): BAB sleeve is active on single-stock longs; sleeve weight ≤ 1/3 of V009 (momentum) risk budget. Compute `bab_sleeve_weight` as the fraction of V009 budget allocated today. Correlation gate applies — a BAB sleeve leg and a V009 spine long on the same ticker size to the combined sector cap, not double-sized.
- If `v029_bab_spread ≤ 0` (ANTI-BAB): `bab_sleeve_weight = 0.0`.

**V030 DealerGamma sleeve weight:**

- Expected MISSING this cohort. If value is present, compute `dealergamma_sleeve_weight` analogously (≤ 1/3 V009 budget). Otherwise write `None` to col 36.

**Output of Step 1.5:** a one-paragraph gate panel written into the rec's §2 Regime Read, naming the sleeve status per class, the V027 bucket, and the BAB regime. This panel is read by positions-monitor via the output rec; see `positions-monitor-phase3-SKILL-patch.md`.

## Step 2 — Build the Upstream Synthesis block

Before scoring anything, produce 5–10 bullets — one per upstream source file — that name the file and the single most decision-relevant fact extracted from it. If two sources conflict, name the conflict and state which you are weighting and why. This block is the first section of the output and is the proof that today's call is grounded in the day's data, not in your memory of yesterday.

## Step 3 — Run the 8-step methodology against every asset in the brief

For each scored asset in the brief's scorecard, confirm or revise S, T, C, R and the aggregate Sum. The brief does the heavy lifting; your job is to (a) check the catalyst column (C) is scored — the methodology mandates it — and (b) apply the correlation gate before promoting anything to entry. If the brief omitted C on a row, score it here before using that row.

**2026-04-14 audit additions that feed into S/T/R (see `Methodology Prompt.md` reconciliation note and Top-25 entries 26–28):**
- **Equity T (single-stock only):** prefer residual momentum (12m FF5-residualized) over raw TSMOM for NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC. When they disagree, trust residual.
- **Commodity S:** incorporate basis-momentum (4w and 12w change in F1–F2 slope). Divergence-cap rule: if static slope reads +1 but basis-momentum is flattening the curve, cap S at 0.
- **Cross-asset R:** incorporate intermediary capital ratio (NY Fed primary-dealer equity-to-total z-score). If z < −1σ, downgrade R by one notch on equities, commodities, and FX longs. Do not double-count with HY OAS — if both flag stress, take the more negative signal, not their sum.

If any of the three audit-addition data rows are `MISSING`, fail loud in §6 Data Gaps of the output rec and do not infer the leg.

**Catalyst column (C) — read from shared cache, do NOT re-parse from news file (E4):**

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from catalysts_cache import read_catalysts, filter_for_asset, filter_severity

try:
    catalyst_cache = read_catalysts()  # latest within 3 days
    # For C scoring: only critical+high matter
    catalysts_scoring = filter_severity(catalyst_cache, 'high')
    catalyst_cache_status = 'OK'
except FileNotFoundError:
    # Fallback — parse catalysts inline from news-YYYY-MM-DD.md (prior logic).
    # Flag footer with 'catalysts_cache=MISSING — inline fallback'.
    catalyst_cache = None
    catalysts_scoring = []
    catalyst_cache_status = 'MISSING'
```

For each asset in the scorecard, pull its catalysts via `filter_for_asset(catalyst_cache, ticker)`. If any catalyst falls within 0–3 days AND severity ≥ high, set C = +1 (or −1 for `direction_hint='bearish_risk'`). Do NOT narrate the full calendar — reference `catalysts-cache-YYYY-MM-DD.json` in the score justification. The §5 pre-entry checklist row (Step 5, item 6 — "Catalyst asymmetry") and §8 narrative use `filter_for_asset` to extract only the rows relevant to the promoted ticker — no full-calendar restatement. Eliminates ~2–3K tokens/run of calendar duplication.

Aggregate Sum thresholds:

| |Sum| | Action |
|---|---|
| ≥ 3 | Candidate for entry — run the pre-entry checklist |
| 2 | Near-miss — enumerate the missing leg in §6 of the output |
| ≤ 1 | Not actionable — omit unless an open position is affected |

## Step 4 — Optional: web-search Grade-A gap closure

If the brief or US close snapshot lists fail-loud Grade-A `MISSING` rows AND the user asked for gap closure (or the missing variable is on a leg that would change a |Sum| = 2 candidate into +3), run a web-search pass to close them before finalising scores. Use WebSearch for human-readable sources; do not rely on FRED/CoinGlass direct fetches (egress-blocked).

Common closures and the search query that works:

| Gap | Search pattern that returns a number | Score leg it unblocks |
|---|---|---|
| DGS2 / DGS10 / DFII10 | `"US 10 year yield" {date}` / `"2-year Treasury yield" {date}` / `10-year TIPS real yield {month YYYY}` | rates block, 2s10s derived, real-yields → Gold S |
| Brent M1–M3 curve slope | `Brent crude M1 M3 futures curve {month YYYY} backwardation contango` | Brent/WTI S confirmation, R unchanged |
| BTC perp funding | `BTC funding rate {date} binance OKX` | BTC R (crowding direction) |
| BTC active addresses | `Bitcoin active addresses {month YYYY} blockchain.com` | BTC S (network usage) |
| META / EURUSD prices | `META stock price close {date}` / `EURUSD exchange rate {date}` | scorecard rows blocked by missing price |
| **Intermediary capital ratio (NY Fed PD equity/total, z-score)** | `NY Fed primary dealer statistics {week-ending-date}` / `"primary dealer" equity capital {month YYYY}` | cross-asset R-overlay leading gate per Methodology Prompt Step 5; do not double-count with HY OAS — take the more negative signal |
| **Residual momentum (equity single-stock)** | `Kenneth French 5-factor monthly {month YYYY}` (pull FF factors, compute residualized 12m return via rolling OLS on stock excess returns) | single-stock T-input per Step 3; applies to NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC. If raw TSMOM and residual conflict, trust residual. |
| **Basis-momentum (commodities)** | `Brent futures curve settlement {YYYY-MM-DD}` / `WTI CL1 CL2 CL3 futures prices {month YYYY}` — derive F1–F2 slope daily, take 4w / 12w change | commodity S-input per Step 2; divergence-cap rule — if static slope says +1 but basis-momentum shows the curve flattening, cap S at 0 |

Re-score affected legs after each closure. If a closed leg flips a watchlist thesis (e.g., funding negative invalidates a BTC short), update Memory §5 immediately — don't batch.

## Step 5 — Apply the binding pre-entry checklist

Only a candidate that clears **every** item below is eligible for the recommendations table. If any item fails, no trade on that candidate.

1. |Sum| ≥ 3 with C scored (not blank, not "—")
2. Invalidation written, concrete, and date-bounded
3. Correlation gate clean — does this share its primary regime variable with any open position or other simultaneous signal? If yes, treat as an add to that theme and size to the sector cap, not the per-position cap. Canonical example: Copper + Gold + Silver = one reflation/DXY-weak bet, sized once.
4. Per-position risk ≤ 2% AND post-entry portfolio heat ≤ 8%
5. ATR stop set (2–3× for commodities/crypto, 1.5–2× for equities), never fixed %
6. Catalyst asymmetry stated — surprise-dependent vs confirmation-dependent. Surprise-dependent catalysts carry positive convexity and are preferred; confirmation-dependent catalysts where the bar is elevated (e.g. an earnings print already discounted) carry poor asymmetry and usually fail the overall thesis even when scored C+1.
7. **Step 1.5 Overlay Gate status for this sleeve is ON** (Phase 3, added 2026-04-25). If OFF → position size × 0 → no trade regardless of Sum. Authoritative: `Risk Rules.md §7` item 7.
8. **V027 intermediary-capital sizing tier applied** (Phase 3, added 2026-04-25). If `v027_regime_bucket = contraction` (z < −1σ), the halved-gross-exposure rule is the binding constraint above quarter-Kelly. Authoritative: `Risk Rules.md §1.B` and `§7` item 8.

"No trade" is always a valid output. When evidence is mixed or a Grade-A input is `MISSING` on a leg that would decide the call, the correct answer is to say so and wait.

## Step 6 — Write the output file

Path: `/mnt/Trade/trade-rec-{YYYY-MM-DD}.md`. Overwrite if it exists; bump the version tag in the title. Use this exact section order and headings:

```
# Trade Recommendations — YYYY-MM-DD (20:20 UTC+8 = 08:20 ET US pre-open) — vN

## 1. Upstream Synthesis
[5–10 bullets, one per source file, naming the file and the single most decision-relevant fact. Conflicts called out explicitly.]

## 2. Regime Read
[One paragraph. Cite brief + weekly review. State the regime label and the three primary regime variables being watched.]
[If the latest signal review contained §8 Escalation Flags, append one line per flag here: "⚠ Signal-review flag: {FLAG-TYPE} — {summary}". These are informational — they don't block trades, but they should inform conviction sizing and thesis scrutiny.]

## 3. Recommendations Table
| Asset | Direction | Entry | Stop | Target | Size | Catalyst | Evidence Grade | Correlation check | Risk-rule check |

If no candidate clears the pre-entry checklist, leave the table empty (one row of "—") and write below it: "No actionable |Sum| ≥ 3 signals today. Pre-entry checklist Risk Rules §7 item 1 fails for every candidate."

## 4. Theses Not Taken (near-misses, |Sum| = 2)
[For each near-miss: name the asset, score legs, the one leg that's missing, and the specific trigger or data that would promote it to +3. One paragraph per candidate. If the missing leg is an audit-addition variable (residual momentum, intermediary capital, basis-momentum), say so explicitly — this is the evidence stream feeding the 2026-10-14 review.]

## 5. Relative-Value Pairs
[Only when the outright regime is mixed AND valuation/carry/revisions rank cleanly. If outright regime aligns across a theme, RV adds no edge — say so and skip.]

## 6. Data Gaps
[Three parts:
  (a) Upstream artifact coverage — name any of the four required artifacts that were missing.
  (b) Audit-addition Grade-A fail-loud rows still MISSING (residual momentum, intermediary capital z, basis-momentum). List each by name and which score leg on which asset it blocks. List these separately from (c) so the 2026-10-14 review can audit visibility.
  (c) Other Grade-A fail-loud rows still MISSING (post-closure if §4 ran). Name each and which score leg it blocks.]

## 7. Pre-Entry Checklist (binding)
[If a trade was taken: walk through items 1–8 with pass/fail (items 7 and 8 added 2026-04-25 Phase 3).
 If no trade: write "Not applied — no candidate cleared |Sum| ≥ 3 (item 1 fails)." and list items 1–8 for reference.
 If a candidate cleared items 1–6 but failed item 7 (sleeve OFF): write "Item 7 fail — sleeve gated OFF per Step 1.5. Logged as Promoted/Taken=NO in SignalLedger with Block_Reason=OverlayGateOff."]

## 8. Memory Updates Needed
[Bullet list: positions to log, watchlist changes, invalidated theses. Each item must be concrete enough to act on. Include a dedicated bullet "Audit-addition contribution" when any of the three audit-addition variables moved a scorecard leg into or out of entry range — note the variable, asset, and direction. These are written to the AuditAdditionLog sheet in Step 9.5. If none contributed, write "Audit-addition contribution: no entry today."]

---

Grades cited: A = replicated + coherent mechanism; B = regime-dependent. No Grade C padding. No stock-to-flow / halving-cycle timing.
```

## Step 7 — Apply Memory updates immediately (don't batch)

After writing the rec file, apply every change listed in §8 of the rec to `/mnt/Trade/Memory.md`:

- §5 (Watchlist): mark removals with strikethrough and a one-line reason; add new candidates if a thesis was promoted.
- §2 (Open Positions): add a row only if a |Sum| ≥ 3 candidate cleared the full checklist and an entry was actually taken.
- `/mnt/Trade/memory-lessons.md` (Lessons & Corrections): append one line summarising the slot, regime label, signal count, named near-misses, watchlist deltas, and the rec file path with version tag. Do NOT read this file at startup — write only. (Memory.md §8 is a pointer to this file.)

**Note:** Memory.md §3 (Regime State), §4 (Key Variables), and §10 (Audit-addition Contribution Log) have been removed. Regime and variable state is maintained in `master-data-log.xlsx` (RegimeHistory, DailyVariables sheets). Audit-addition contributions are written to the `AuditAdditionLog` sheet in Step 9.5 below. Do NOT recreate these Memory sections.

The "don't batch" rule exists because Memory is the bridge between sessions. A change you defer until later is a change that gets lost when the next scheduled run starts.

## Step 8 — Append signals to SignalLedger in master-data-log.xlsx (required, every run)

After writing the rec and applying Memory updates, append every qualifying signal to the **SignalLedger** sheet in `/mnt/Trade/master-data-log.xlsx` using openpyxl. This is the sole out-of-sample performance tracking system — it captures the signal, the scores, and the market price at recommendation time so the `signal-review` skill can later measure whether the system's calls were right.

The reason every run must do this: a performance record is only useful if it's complete. Skipping a day because "nothing happened" creates survivorship bias. Even a "no trade" day with five near-misses at |Sum| = 2 is valuable data.

Read `/mnt/Trade/Excel-Sync-Protocol.md` §2 (daily-trade-rec) for the authoritative column mapping. Key rules:

**For promoted signals** (|Sum| ≥ 3): append one row with ID (next sequential P###), Type='Promoted', Date, Asset, AssetClass, Direction, S/T/C/R/Sum, Entry_Price, ATR_Stop, Target_TP1, Target_TP2, Invalidation, Inv_Date, VIX_at_Entry, Regime_Label, Taken (check Memory.md §2), Status='OPEN'. Exit columns blank.

**For near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked): append one row with ID (next sequential N###), Type='Near-Miss', same score fields, Blocking_Leg, Block_Reason, Price_at_Signal, VIX_at_Signal, Status='OPEN'. Exit columns blank.

**Phase 3 meta-integration cols (positions 33–36, added 2026-04-25).** On every row — promoted AND near-miss — write:

| Col | Value source | Missing-value rule |
|---|---|---|
| 33 `overlay_gate_status` | `equity={ON\|OFF}\|commodity={ON\|OFF}\|crypto={ON\|OFF}` — from Step 1.5 gate panel | write `MISSING` string if staging absent |
| 34 `v027_regime_bucket` | `expansion`/`neutral`/`contraction` — from Step 1.5 | write `MISSING` if staging absent |
| 35 `bab_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V029 MISSING |
| 36 `dealergamma_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V030 MISSING (expected for this cohort) |

**Overlay-gated Sum +3 handling (per `Methodology Prompt.md §Step 1.5`).** A signal with |Sum| ≥ 3 on an overlay-OFF sleeve is logged as Type='Promoted', Taken='NO', Status='OPEN', Block_Reason='OverlayGateOff' (or 'OverlayStagingMissing' if fail-loud). This preserves the Sum arithmetic record for out-of-sample tracking while flagging why the trade wasn't executed. signal-review reads these rows to mark-to-market the overlay gate's hit rate separately from the Taken=YES population.

**Deduplication rule:** Read all OPEN rows first (done in Step 1). If an asset has an OPEN row with identical S/T/C/R and same blocking leg, skip. If any score changed, append a new row.

**Append-only rule:** Never delete or edit existing rows. If logged incorrectly, add a correction in the Notes column.

**Next ID tracking:** To find the next P### or N### ID, scan the ID column for the max existing number and increment.

---

## Step 9.5 — Sync to master-data-log.xlsx (MANDATORY)

After appending signals in Step 8, also update these sheets per `/mnt/Trade/Excel-Sync-Protocol.md