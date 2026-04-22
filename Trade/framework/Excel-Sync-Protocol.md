# Excel Sync Protocol — master-data-log.xlsx

**Created:** 2026-04-15
**Purpose:** Defines how each daily skill/task writes structured data to the master-data-log workbook after completing its markdown output. This file is the single source of truth for sync behavior.

**Core rule:** The markdown output remains the human-readable presentation layer. The Excel workbook is the analytical layer. Both must be produced every run. If they diverge, Excel is source of truth for quantitative data.

---

## Workbook Location

`/mnt/Trade/master-data-log.xlsx`

## How to Open and Append

```python
from openpyxl import load_workbook
from datetime import date

wb = load_workbook('/mnt/Trade/master-data-log.xlsx')
ws = wb['SheetName']

# Find next empty row
next_row = ws.max_row + 1

# Check if today's row already exists (for same-day overwrites)
for row in range(2, ws.max_row + 1):
    if ws.cell(row=row, column=1).value == date.today():
        next_row = row  # overwrite
        break

# Write data...
ws.cell(row=next_row, column=1, value=date.today())
# ... more cells ...

wb.save('/mnt/Trade/master-data-log.xlsx')
```

**Important:** Always use `date` objects for the Date column, not strings. Use `None` for missing values, not "MISSING" or "N/A" — the DataQuality sheet tracks missingness separately.

---

## Per-Skill Sync Instructions

### 1. market-brief skill (Step 8 — after Memory.md update)

**Sheets to update:** DailyVariables, RegimeHistory, DataQuality, CatalystLog

**DailyVariables:** Append one row. Map every variable reading from the brief to the corresponding column. Use the column headers as the schema reference. Key column groups:
- Cross-asset risk: VIX, VIX3M, VIX/VIX3M, MOVE, DXY, HY_OAS, NFCI, Intermediary_Cap_Ratio, Intermediary_Cap_Z
- Rates: DGS2, DGS10, 2s10s (derived), DFII10, T10YIE, ACM_TP_10Y
- Equities: SPX, NDX, SPY, QQQ, EWJ, EWY + 12 single stocks + 12 residual momentum columns
- Commodities: Brent, WTI, Gold, Silver, Copper, Platinum, Palladium + 10 basis-momentum columns (4w/12w for each)
- FX: EURUSD, USDJPY
- Crypto: BTC, ETH, BTC_HashRate, BTC_ActiveAddr, BTC_ExchNetflow, BTC_ETF_Flow, BTC_PerpFunding, BTC_3mBasis, ETH_ETF_Flow, ETH_DailyTxns
- Meta: GradeA_Missing_Count, Source_Brief

If a same-day row exists from a prior version, overwrite it and note the version in Source_Brief.

**RegimeHistory:** Append one row:
- Date, Regime_Label (the one-line label from §1)
- Growth, Inflation, Policy, FinConditions, RiskOnOff (from regime snapshot)
- BTC_VolRegime, BTC_FundingBasis, BTC_Structural
- Watch_Var_1/2/3 (the three primary regime variables)
- Promoted_Signals (comma-separated IDs), NearMiss_Count
- Source_Brief

**DataQuality:** Append one row:
- Date, Total_GradeA_Vars (count from Data Sources.md), Missing_Count, Missing_Rate_Pct
- Missing_Variables (comma-separated names), Stale_Count, Stale_Variables
- Audit_ResidMom_Status / Audit_IntCap_Status / Audit_BasisMom_Status (LIVE/MISSING/STALE)
- Pipeline_Health (OPERATIONAL/DEGRADED/FAILED), Source_Brief, Notes

**CatalystLog:** For each NEW catalyst in the brief's §5 that doesn't already exist in the CatalystLog:
- Date_Added, Catalyst_Date, Event, Assets_Affected, Impact_Level, Expectation
- Outcome = PENDING, rest blank
For catalysts whose date has passed, update Outcome if known.

### 2. daily-trade-rec skill (Step 8.5 — HypoLedger append; Step 9.5 — SignalLedger/AuditAdditionLog/CatalystLog)

**Sheets to update:** HypoLedger (Step 8.5), SignalLedger, AuditAdditionLog, CatalystLog (Step 9.5)

**HypoLedger (Step 8.5):** For every FORMALLY PROMOTED signal (all pre-entry checklist items PASS), append one row — or update the existing row if this asset × direction × Rec_Date is a re-confirmation of a prior entry. This sheet is the system-efficacy ledger; it tracks rec-price performance independent of Gerald's execution decisions.

Columns (H_ID, Rec_Date, Rec_File, Asset, Direction, S, T, C, R, Sum, Entry_Price_Rec, Stop_Rec, TP1_Rec, TP2_Rec, Inv_Date, Size_Rec_%, Status, Hypo_Entry_Price, Hypo_Current_Price, Hypo_PnL_%, Actual_Taken, Actual_Entry, Actual_Exit, Actual_PnL_%, Note):
- `H_ID`: next sequential H### from max existing row
- `Entry_Price_Rec`: midpoint of the recommended entry zone (or limit price if stated precisely)
- `Hypo_Entry_Price`: same as `Entry_Price_Rec` at time of append
- `Hypo_Current_Price`: leave blank at append time — signal-review fills this weekly
- `Status`: `OPEN` (immediate entry) · `PENDING` (entry requires trigger: beat confirmation, gate resolution) · `VOIDED` (promoted then de-promoted same session) · `FLAGGED` (Sum≥3 identified but not formally promoted)
- `Actual_Taken`, `Actual_Entry`, `Actual_Exit`: blank at append; filled by trade-update or signal-review

Dedup rule: if asset × direction × Rec_Date already exists in HypoLedger, update the `Rec_File` field to reflect the latest version instead of adding a new row.
Do NOT add near-miss signals — those belong in SignalLedger (N### rows) only.

**SignalLedger (Step 9.5):** For each signal from today's rec (promoted or near-miss), append a row to SignalLedger:
- ID, Type ('Promoted' or 'Near-Miss'), Date, Asset, AssetClass, Direction
- S, T, C, R, Sum (as integers: 1, 0, -1)
- Entry_Price, ATR_Stop, Target_TP1, Target_TP2 (for promoted); leave blank for near-misses
- Invalidation, Inv_Date, VIX_at_Entry, Regime_Label (from the rec's §2)
- Blocking_Leg, Block_Reason (for near-misses; leave blank for promoted)
- Taken, Status (OPEN at log time)
- Exit columns all blank (filled by signal-review)
- Source_File, Notes

Same deduplication rule as the markdown ledger: if an asset has an OPEN row with identical S/T/C/R and same blocking leg, don't duplicate.

**AuditAdditionLog:** For each audit-addition variable that moved a scorecard leg:
- Date, Variable (name), Asset, Direction_of_Move (describe the change)
- Score_Leg_Before, Score_Leg_After, Impact_on_Sum
- Decision_Moving (YES/NO), Source_File

**CatalystLog:** Update outcomes for any catalysts that resolved since the last rec.

### 3. signal-review skill (Step 7 — after writing review file)

**Sheets to update:** SignalLedger (mark-to-market updates), **HypoLedger (mark-to-market + efficacy report)**, PerformanceStats (dimension 14)

**SignalLedger:** For each OPEN signal:
- Update Status if it should change (HIT_TARGET, HIT_STOP, EXPIRED, STILL_OPEN)
- Fill Exit_Price, Exit_Date, Days_to_Exit for closed signals
- Fill MAE_Pct, MFE_Pct for all signals with price history
- Fill Catalyst_Outcome for signals whose catalyst date has passed
- Fill Hypo_PnL_Pct for closed signals

Do NOT add new rows to SignalLedger — only update existing OPEN rows.

**HypoLedger:** For each row with Status = OPEN or PENDING:
- Fetch current price from latest brief/snapshot or WebSearch
- Update `Hypo_Current_Price` (the `Hypo_PnL_%` formula auto-recalculates)
- If `Stop_Rec` breached since last review → Status = `HIT_STOP`, `Hypo_Current_Price` = stop price
- If `TP1_Rec` breached → Status = `HIT_TARGET`, `Hypo_Current_Price` = TP1
- If today > `Inv_Date` and still OPEN → Status = `EXPIRED`, `Hypo_Current_Price` = current price
- For PENDING rows: if entry trigger confirmed → Status = `OPEN`, `Hypo_Entry_Price` = rec midpoint; if trigger failed (e.g. earnings miss for a contingent entry) → Status = `VOIDED`
- For rows where `Actual_Taken = YES` and `Actual_Exit` is still blank: cross-reference Memory.md §7 and fill `Actual_Exit` + `Actual_PnL_%`

**PerformanceStats (dimension 14):** Write the HypoLedger efficacy summary (hypo weighted avg PnL%, actual weighted avg PnL%, execution gap, early-exit cost) to the PerformanceStats sheet's dimension-14 block.

### 4. quarterly-methodology-review skill (Step 7.5 — after writing review file)

**Sheets to update:** VariableRegistry

For each variable assessment in the quarterly review:
- Update Last_Review_Date to today
- Update Next_Review_Date
- Append to Review_History
- Update Status if a promotion/demotion decision was made (with Gerald sign-off tracking in Notes)
- Update Decision_Moving_Count and OOS_Contribution based on ledger evidence

For variable candidates being promoted from the pipeline:
- Update Status (e.g., Candidate → Under Review, or Under Review → Provisionally Useful)
- Fill in any newly available screening criteria

### 5. literature-review skill (Step 8.5 — after writing review file)

**Sheets to update:** VariableRegistry

For each new variable candidate identified:
- Append a new row with the next sequential Var_ID (V034, V035, ...)
- Fill all known fields from the five-criteria screening
- Status = 'Candidate' (if 5/5 pass → 'Watchlist')
- Discovery_Date = today, Discovery_Source = 'Literature review YYYY-MM-DD'
- Fill Source_Paper, Intuition, Published_Sharpe, Decay_Haircut_Pct, Proj_Op_Sharpe

For rejected candidates: still add a row with Status = 'Rejected' and fill the failure reason in Notes. This prevents re-scanning.

### 6. news-events skill — Discovery sync only (no quantitative data sync)

The news-events skill doesn't produce quantitative time-series data. Its outputs are consumed by the market-brief and trade-rec, which handle the data sync.

**VariableRegistry (discovery only):** When a practitioner variable has been flagged in news files 3+ times across different weeks (per Variable-Discovery-Protocol.md §3C), append a Candidate row using the standardized template. Source_Type = 'C', Discovery_Source = the news file that prompted registration.

### 7. weekly-regime-review (Sunday) — No direct Excel sync

Produces the weekly review markdown. The regime state it establishes flows through the next week's market-briefs, which handle the sync.

---

## Variable Registry — Discovery System Protocol

The VariableRegistry sheet in master-data-log.xlsx implements the variable discovery and lifecycle system.

### Status Ladder

| Status | Meaning | Entry criteria | Exit criteria |
|--------|---------|----------------|---------------|
| Candidate | Plausible idea, not yet assessed | Any source: literature, market observation, practitioner | Classified and screened → Watchlist or Rejected |
| Watchlist | Weak or mixed evidence, worth tracking | Passes 3/5 criteria OR interesting mechanism | Monthly review: evidence improving → Under Review; still weak after 2 quarters → Rejected |
| Under Review | Being actively assessed with data | Passes 4/5 criteria AND data collection feasible | Data collected, pilot run → Provisionally Useful; fails pilot → Watchlist or Rejected |
| Provisionally Useful | Seems helpful but not fully trusted | Pilot shows positive results; N ≥ 30 signals | 6-month review: confirmed → Approved; not confirmed → Watchlist |
| Approved | Good enough for regular use | Confirmed via out-of-sample ledger evidence | Further confirmation → Grade A; evidence weakens → Provisionally Useful |
| Grade A | Strong evidence, repeated usefulness, core methodology | Multiple quarters of OOS confirmation, Gerald sign-off | Regime break or persistent underperformance → Approved (demotion) |
| Rejected | Failed screening or proved unhelpful | Failed criteria or no value after review period | Can re-enter as Candidate only if NEW evidence addresses the specific failure |
| Retired | Was useful but no longer | Regime change, factor decay, redundancy with better variable | Kept for audit trail; can re-enter if conditions change |

### Review Cadence (aligned with Variable-Discovery-Protocol.md)

| Cadence | Source | Action | Who |
|---------|--------|--------|-----|
| Daily | B (Market obs.) | Market-brief flags patterns in §6, trade-rec flags blocking patterns in §4/§8 | market-brief, daily-trade-rec skills |
| Daily | C (Practitioner) | News-events flags practitioner variables in §7 | news-events skill |
| Weekly | D (Repeated behavior) | Signal-review flags repeated patterns in §7B, cleans/validates week's Candidates | signal-review skill |
| Monthly | All | Bootstrap review assesses Watchlist variables | monthly-bootstrap-review task |
| Quarterly | All | Formal promote/demote/reject decisions. Variable pipeline assessment. Sole promotion gate. | quarterly-methodology-review skill |
| Semi-annual | A (Academic) | Deep academic literature scan using extended template and five-criteria screening | literature-review skill |

### Adding a New Variable (any skill)

**Authoritative reference:** See `Variable-Discovery-Protocol.md` for the full four-source discovery framework, per-skill responsibilities, and the standardized capture template.

When a skill discovers a potential new variable (from literature, market behavior, practitioner research, or repeated blocking pattern):

1. Open master-data-log.xlsx, go to VariableRegistry sheet
2. Find the next available Var_ID (check max existing ID + 1)
3. Fill in **all minimum required fields** from the standardized capture template (`Variable-Discovery-Protocol.md` §2):
   - Var_ID, Name, Definition, Asset_Class, Use_Type, Taxonomy, Horizon
   - Mechanism (must name a risk premium, behavioral bias, institutional constraint, or information asymmetry)
   - Source_Type (A/B/C/D), Discovery_Date, Discovery_Source
   - Initial_Evidence (Strong/Moderate/Weak/Anecdotal — be honest)
   - Independence_Check (which existing variables overlap, estimated correlation)
   - Implementability (data source, lag, cost)
   - Status = 'Candidate'
4. For Source A (academic) candidates, also fill the extended fields: Source_Paper, Published_Sharpe, Decay_Haircut_Pct, Proj_Op_Sharpe, Five_Criteria_Pass, Source_Hierarchy
5. Leave screening criteria blank if not yet assessed beyond initial discovery
6. Save the workbook

**Threshold for writing to the registry:** A single observation is logged in the skill's output file (brief §6, rec §4/§8, news §7, review §7B). Only write to the VariableRegistry when the observation has been seen 3+ times across different runs, or when the mechanism is well-grounded and the evidence is at least Moderate. The literature review writes on first identification (since the five-criteria screen is its own threshold).

The variable will be picked up in the next review cycle: weekly signal-review for cleanup/classification, monthly bootstrap for Watchlist assessment, quarterly for promotion decisions.

### Promotion Requires Gerald's Sign-Off

No variable moves from Provisionally Useful → Approved → Grade A without Gerald's explicit approval. The quarterly-methodology-review skill proposes promotions; Gerald confirms. The VariableRegistry Notes column tracks sign-off status.

---

## Relationship to Markdown Files (updated 2026-04-22)

As of 2026-04-16, structured data lives exclusively in Excel. The following markdown files have been **deleted** — Excel is the sole source of truth:

| Former markdown file | Excel sole owner | Notes |
|---|---|---|
| `hypo-ledger-2026.md` | **HypoLedger** (dedicated sheet, added 2026-04-22) | Promoted-signal efficacy ledger at rec prices; separate from SignalLedger. Hypo P&L, actual execution gap, stop-discipline delta, FLAGGED counterfactual. |
| `data-quality-scorecard.md` | DataQuality | Tiered fail-loud framework and daily MISSING log |
| `audit-data-missing-tracker.md` | DataQuality | Per-variable OK/MISSING daily log and running tally |
| Memory.md §3 (Regime State) | RegimeHistory | Latest row = current regime |
| Memory.md §4 (Key Variables) | DailyVariables | Latest row = current readings |
| Memory.md §10 (Audit-addition log) | AuditAdditionLog | Evidence base for 2026-10-14 review |

**Still maintained as narrative markdown (not duplicated in Excel):**

| Markdown file | Excel complement | Rule |
|---|---|---|
| Quarterly review §4 (Variable Pipeline) | VariableRegistry sheet | VariableRegistry is the authoritative registry. Quarterly review reads from and writes to it. |
| Literature review §4-5 (Candidates) | VariableRegistry sheet | Literature review appends candidates to the registry. |
| Briefs, recs, news, reviews | Various sheets | Narrative files remain the presentation layer. Excel accumulates their quantitative outputs. |

### Variable Discovery Flow (markdown → Excel)

Discovery observations are first logged in the skill's markdown output (brief §6, rec §4/§8, news §7, review §7B). These are the lightweight, low-threshold captures. Only when an observation meets the 3-occurrence threshold (or comes from the literature review's five-criteria screen) does it get written to the VariableRegistry sheet. See `Variable-Discovery-Protocol.md` for the full specification.
