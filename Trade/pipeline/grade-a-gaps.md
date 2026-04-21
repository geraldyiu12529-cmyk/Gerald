# Grade A Data Gaps — Chronic Missing Tracker

**Purpose:** Track Grade A variables that have never been successfully retrieved in the live pipeline. Unlike the audit-addition uptime tracker (which tracks the three 2026-04-14 variables), this file tracks the broader Top-28 retrieval failures that recur across multiple briefs.

**Read by:** pipeline-recovery (Phase B), market-brief (fail-loud gate), quarterly-methodology-review.

**Update rule:** Append a row each time a gap status changes (resolved, newly failing, source changed). Do not delete rows — mark as RESOLVED with date.

---

## Active Gaps

| Variable | Grade | Role | Failure mode | First seen missing | Attempts | Status | Next action |
|----------|-------|------|-------------|-------------------|----------|--------|-------------|
| **NFCI** | A | Financial conditions gate (R-leg) | Chicago Fed API returns 403 in bash env; web search returns stale releases | 2026-04-14 | Tier 1 fail → Tier 2 partial → Tier 3 stale fallback | **CHRONIC** — Tier 3 stale value used (−0.12 from 2026-04-10). Not blocking any open position score but blocks FCI confirmation. | Try Chicago Fed FRED endpoint `NFCI` via `fred.stlouisfed.org/graph/fredgraph.csv?id=NFCI` (weekly; Fridays). Add as Tier 1 FRED fallback in data_retrieval_engine.py. |
| **ACM term premium 10Y** | A | Policy surprise sensitivity (R-leg refinement) | NY Fed posts monthly; Jan-2026 is latest available as of Apr-2026 | 2026-04-14 | Monthly cadence — no more recent data exists | **STRUCTURAL** — monthly release means 30-day gaps are expected. Jan-2026 ~0.59% used as estimate. | Accept monthly cadence. Document in Data Sources.md that ACM is monthly-refresh-only. No pipeline fix needed; remove from MISSING count in brief when within 30d of last release. |
| **BTC 3m basis (Deribit)** | A | Crypto crowding / futures premium (C-leg crypto) | Deribit API undocumented in bash; web search returns inconsistent format | 2026-04-14 | Tier 1 fail → Tier 2 format mismatch → Tier 3 MISSING | **CHRONIC** — blocks crypto basis confirmation. BTC Sum never reaches +3 partly due to S=0 but this gap also prevents C confirmation via basis. | Test Deribit v2 REST endpoint: `https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd`. For basis: `BTC-25JUL25` vs spot; compute (futures−spot)/spot annualized. Add Tier 1 Deribit fetch in data_retrieval_engine.py. |
| **Revision Breadth** | A | Earnings revision momentum (T-leg, single stocks) | Search queries return analyst report paywalls; no free structured source identified | 2026-04-17 | Tier 2 search fails → Tier 4 MISSING | **CHRONIC** — blocks systematic revision scoring for single stocks. Currently replaced by residual momentum (audit-addition) which is a superior T-input anyway. | Evaluate whether Revision Breadth is still needed given residual momentum coverage. If residual momentum is decision-moving for T-leg in ≥50% of scored assets at 2026-07-01 quarterly review, consider retiring Revision Breadth from Top-28 (Grade B or C). Flag at quarterly review. |
| **Pct Above 200DMA** | A | Trend breadth (S-leg regime confirmation) | Finviz screener blocked in bash; Yahoo Finance screener requires JS | 2026-04-17 | Tier 1 fail → Tier 2 blocked → Tier 4 MISSING | **CHRONIC** — trend breadth gap. Without it, S-leg regime confirmation is missing one of its three inputs (VIX/HY OAS available; breadth missing). | Try `finviz.com/groups.ashx?g=sector&o=perf52w` via basic HTTP. Alternative: compute from Yahoo Finance bulk download of SPX constituents (weekly cron, store in .data-cache). |

---

## Resolved Gaps

| Variable | Grade | Resolution date | How resolved |
|----------|-------|----------------|--------------|
| DGS2 (2Y Treasury) | A | 2026-04-14 | FRED direct HTTP fetch working |
| DGS10 (10Y Treasury) | A | 2026-04-14 | FRED direct HTTP fetch working |
| DFII10 (10Y TIPS real yield) | A | 2026-04-14 | FRED direct HTTP fetch working |
| Brent M1–M3 basis | A | 2026-04-14 | CME Group web search pattern found |
| BTC funding rate | A | 2026-04-14 | Binance API Tier 1 working |
| BTC active addresses | A | 2026-04-14 | Blockchain.info API working (STALE-WARN cadence normal) |
| Intermediary capital z | A | 2026-04-15 | NY Fed PD data fetch via web search working |
| Residual momentum | A | 2026-04-15 | Kenneth French FF5 library fetch working |
| Basis-momentum (5 commodities) | A | 2026-04-15 | CME Group fetch for all 5 working |

---

## ACM Cadence Note (structural — not a pipeline bug)

ACM term premium is monthly. When `age_days ≤ 30` since last release, do NOT count it as MISSING in the brief's Grade A gap count. The pipeline status note `missing_grade_a_count` should subtract ACM when it is within the expected monthly window. This prevents ACM from inflating the PARTIAL count 29 out of every 30 days.

**Action for market-brief skill:** in the DataQuality section, distinguish between:
- `MISSING — source failure` (real gap, counts toward MISSING tally)
- `MISSING — monthly cadence, N days since last release` (structural, does NOT count toward tally)
