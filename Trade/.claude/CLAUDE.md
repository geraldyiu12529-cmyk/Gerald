# Gerald's Trading Research System

Discretionary cross-asset + crypto trader using an evidence-graded 8-step methodology.
Timezone: UTC+8. "No trade" is always a valid output.

## Asset Universe (do not expand without permission)
Crypto: BTC, ETH. Equities: INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, AVGO, BABA, MSFT.
ETFs: QQQ, SPY, EWJ, EWY. Commodities: Brent, WTI, Gold, Silver, Copper, Palladium, Platinum.
FX: EURUSD, USDJPY.

## Authoritative Documents — load ONLY when a skill requires them
| Document | Authority over | Loaded by |
|---|---|---|
| `framework/Methodology Prompt.md` | 8-step framework, evidence grades, scoring, Top-28 variables | brief, trade-rec, signal-review, quarterly-review |
| `framework/Risk Rules.md` | Pre-entry checklist, sizing, stops, circuit breakers, correlation gate | trade-rec, trade-update, positions-monitor |
| `framework/Data Sources.md` | Variable→source mapping, fail-loud rule, 4-tier retrieval | brief, preflight |
| `framework/Coin core.md` / `framework/Trad core.md` | Research evidence base | literature-review, quarterly-review ONLY |
| `framework/Memory.md` | Open positions, watchlist, catalysts, closed trades | Most skills (see SKILL.md) |
| `framework/Retention Policy.md` | File tiering, archival | workspace-tidy ONLY |
| `framework/Excel-Sync-Protocol.md` | Column mappings for master-data-log.xlsx | brief, trade-rec, signal-review, trade-update |
| `bnma/meta-analysis/BNMA-meta-analysis-2026-04-18.md` | DEPLOY/WATCH/EXCLUDE verdicts, A→B grade downgrades for V001/V004/V006/V007/V008 | quarterly-review, literature-review, methodology-audit ONLY |
| `bnma/meta-analysis/PL-NMA-meta-analysis-2026-04-18.md` | PL-NMA 54-variable ranking (θ, P(top-k), pairwise dominance) | quarterly-review, literature-review, methodology-audit ONLY |

**CRITICAL: Do NOT load all documents at session start. Each skill specifies its own reads. This is the primary token-saving mechanism.**

## Evidence Grade Discipline
- A = replicated, coherent mechanism, long history. B = regime-dependent. C = weak/anecdotal.
- Cite grades (A/B/C) on every signal reference.
- Never pad with Grade C unless explicitly asked. No stock-to-flow timing.
- Fail-loud on MISSING Grade A variables — never silently infer.

## Memory Protocol
- Update immediately — don't batch to end of session.
- Two systems: `framework/Memory.md` (trader working state) + auto-memory (cross-session).
- Use absolute dates (YYYY-MM-DD), never relative.
- framework/Memory.md §3/§4/§10 removed — regime/variable state lives in `master-data-log.xlsx`.

## Behavioral Rules
- Follow the 8-step methodology sequence exactly. Do not skip steps.
- Every sentence in a briefing must inform a decision or manage a risk. No padding.
- Do not present ungrounded assertions as evidence.
- Fail-loud on missing data — state what's missing and which score leg it blocks.

## Excel — sole structured store
- `master-data-log.xlsx`: 10 sheets (SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes, CatalystLog, README).
- Read `framework/Excel-Sync-Protocol.md` before any xlsx write. Use openpyxl.
- Append-only for SignalLedger rows. Never delete or overwrite existing signal data.

## Pipeline File Conventions
- **Date-folder convention (effective 2026-04-19):** every dated output lives under `{YYYY-MM-DD}/` at workspace root, where the date is the local UTC+8 date the routine fired. One folder per local date, containing all artifacts produced for that date. Every scheduled task `mkdir -p {YYYY-MM-DD}` before writing.
- Daily outputs (all inside today's date folder):
  - `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` + `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html`
  - `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` (conditional — silent-when-OK)
  - `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md` (consolidated pack target from `scripts/pack_daily.py`)
- Periodic outputs (also inside today's date folder):
  - `{YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md`, `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` (+ `{YYYY-MM-DD}/report-{YYYY-MM-DD}-signal-review.html`)
  - `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md`
  - `{YYYY-MM-DD}/literature-review-{YYYY-MM-DD}[-scope].md`
  - `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` (+ `.html`)
- **Downstream reads** should glob across date folders — e.g. `*/market-brief-*.md`, `*/trade-rec-*.md` — and fall back to root-level `market-brief-*.md` etc. for legacy files produced before 2026-04-19.
- News taxonomy spec: `news-events/README.md` stays at root (it is the 12-category format reference, not a dated output).
- Scripts: `scripts/` (data_retrieval_engine.py, compute_audit_additions.py, pipeline_status.py, catalysts_cache.py, pack_daily.py, cache_manager.py, etc.)
- Cache: `.data-cache/` (persistent, staleness-classified per framework/Data Sources.md)
- Pipeline state: `pipeline/.pipeline-status.json`, `pipeline/.pipeline-health.json`

## 2026-04-14 Audit Additions (Grade A, review due 2026-10-14)
Three variables added to the scoring pipeline:
1. **Residual momentum** (12m FF5-residualized) → single-stock T-input. Prefer over raw TSMOM when they disagree.
2. **Intermediary capital ratio** (NY Fed PD z-score) → cross-asset R-overlay. If z < −1σ, downgrade R by one notch. Don't double-count with HY OAS.
3. **Basis-momentum** (4w/12w F1–F2 slope change) → commodity S-input. Divergence-cap: if static slope = backwardation but basis-momentum flattening, cap S at 0.
