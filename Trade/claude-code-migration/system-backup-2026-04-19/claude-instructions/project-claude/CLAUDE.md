# Gerald's Trading Research System

Discretionary cross-asset + crypto trader using an evidence-graded 8-step methodology.
Timezone: UTC+8. "No trade" is always a valid output.

## Asset Universe (do not expand without permission)
Crypto: BTC, ETH. Equities: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC.
ETFs: QQQ, SPY, EWJ, EWY. Commodities: Brent, WTI, Gold, Silver, Copper, Palladium, Platinum.
FX: EURUSD, USDJPY.

## Authoritative Documents — load ONLY when a skill requires them
| Document | Authority over | Loaded by |
|---|---|---|
| `Methodology Prompt.md` | 8-step framework, evidence grades, scoring, Top-28 variables | brief, trade-rec, signal-review, quarterly-review |
| `Risk Rules.md` | Pre-entry checklist, sizing, stops, circuit breakers, correlation gate | trade-rec, trade-update, positions-monitor |
| `Data Sources.md` | Variable→source mapping, fail-loud rule, 4-tier retrieval | brief, preflight |
| `Coin core.md` / `Trad core.md` | Research evidence base | literature-review, quarterly-review ONLY |
| `Memory.md` | Open positions, watchlist, catalysts, closed trades | Most skills (see SKILL.md) |
| `Retention Policy.md` | File tiering, archival | workspace-tidy ONLY |
| `Excel-Sync-Protocol.md` | Column mappings for master-data-log.xlsx | brief, trade-rec, signal-review, trade-update |

**CRITICAL: Do NOT load all documents at session start. Each skill specifies its own reads. This is the primary token-saving mechanism.**

## Evidence Grade Discipline
- A = replicated, coherent mechanism, long history. B = regime-dependent. C = weak/anecdotal.
- Cite grades (A/B/C) on every signal reference.
- Never pad with Grade C unless explicitly asked. No stock-to-flow timing.
- Fail-loud on MISSING Grade A variables — never silently infer.

## Memory Protocol
- Update immediately — don't batch to end of session.
- Two systems: `Memory.md` (trader working state) + auto-memory (cross-session).
- Use absolute dates (YYYY-MM-DD), never relative.
- Memory.md §3/§4/§10 removed — regime/variable state lives in `master-data-log.xlsx`.

## Behavioral Rules
- Follow the 8-step methodology sequence exactly. Do not skip steps.
- Every sentence in a briefing must inform a decision or manage a risk. No padding.
- Do not present ungrounded assertions as evidence.
- Fail-loud on missing data — state what's missing and which score leg it blocks.

## Excel — sole structured store
- `master-data-log.xlsx`: 9 sheets (SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, NearMissLedger, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes).
- Read `Excel-Sync-Protocol.md` before any xlsx write. Use openpyxl.
- Append-only for SignalLedger rows. Never delete or overwrite existing signal data.

## Pipeline File Conventions
- Dated outputs at workspace root: `market-brief-YYYY-MM-DD.md`, `trade-rec-YYYY-MM-DD.md`, `report-YYYY-MM-DD-trade-rec.html`, `us-close-snapshot-YYYY-MM-DD.md`
- News: `news-events/news-YYYY-MM-DD.md`
- Scripts: `scripts/` (data_retrieval_engine.py, compute_audit_additions.py, pipeline_status.py, catalysts_cache.py, cache_manager.py, etc.)
- Cache: `.data-cache/` (persistent, staleness-classified per Data Sources.md)
- Pipeline state: `.pipeline-status.json`, `.pipeline-health.json`

## 2026-04-14 Audit Additions (Grade A, review due 2026-10-14)
Three variables added to the scoring pipeline:
1. **Residual momentum** (12m FF5-residualized) → single-stock T-input. Prefer over raw TSMOM when they disagree.
2. **Intermediary capital ratio** (NY Fed PD z-score) → cross-asset R-overlay. If z < −1σ, downgrade R by one notch. Don't double-count with HY OAS.
3. **Basis-momentum** (4w/12w F1–F2 slope change) → commodity S-input. Divergence-cap: if static slope = backwardation but basis-momentum flattening, cap S at 0.
