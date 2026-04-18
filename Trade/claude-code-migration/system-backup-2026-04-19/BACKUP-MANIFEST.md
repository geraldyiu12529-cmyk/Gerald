# System Backup — 2026-04-19

Snapshot of Gerald's trading research system captured on 2026-04-19 (UTC+8).
Source root: `C:\Users\Lokis\OneDrive\Desktop\Trade\Trade\` (mounted at `/mnt/Trade/`).
Backup root: `C:\Users\Lokis\OneDrive\Desktop\Trade\Trade\claude-code-migration\system-backup-2026-04-19\`.

Previous snapshot: `system-backup-2026-04-18/` — preserved untouched for pre-migration audit trail.

## Scope

Captured the full architecture needed to reconstruct the system from cold storage: framework documents, all 18 installed skills, auto-memory, pipeline scripts + state, 17 scheduled-task definitions, CLAUDE.md instructions (global + project), most-recent dated producer outputs, master-data-log, news captures.

Not captured (deliberate): historical dated outputs (`market-brief-2026-04-14.md` etc. are in live `archive/`); Python `__pycache__/`; ephemeral session state under `/sessions/…/.claude/`; the prior `system-backup-2026-04-18/` folder.

## Contents

| Subfolder | Files | Bytes | What it holds |
|-----------|-------|-------|---------------|
| `framework/` | 13 | 256,771 | Authoritative docs — Methodology Prompt, Risk Rules, Data Sources, Coin core, Trad core, Memory, Retention Policy, Excel-Sync-Protocol, Pipeline-Recovery-Protocol, Trade-Execution-Protocol, Variable-Discovery-Protocol, Data-Retrieval-Fallback-Framework, memory-lessons |
| `skills-cowork/` | 218 | 3,859,503 | All 18 installed skills from `/mnt/.claude/skills/` (see skill inventory below) |
| `auto-memory/` | 17 | 60,790 | `/mnt/.auto-memory/` — MEMORY.md index + 16 memory files (user, feedback, project, reference) |
| `pipeline-config/` | 80 | 56,314 | `.pipeline-status.json`, `.pipeline-health.json`, `catalysts-cache-2026-04-17.json`, `.data-cache/` tree |
| `scripts/` | 10 | 211,362 | `data_retrieval_engine.py`, `compute_audit_additions.py`, `compute_meta_additions.py`, `cache_manager.py`, `catalysts_cache.py`, `pipeline_status.py`, `preflight_health_check.py`, `fetch_ff5_from_french_library.py`, + 2 test files |
| `news-events/` | 5 | 74,492 | `README.md` + last 4 daily captures (2026-04-14 → 2026-04-17) |
| `outputs-latest/` | 11 | 177,009 | Most-recent brief, trade-rec, us-close-snapshot, HTML report, weekly review, quarterly review, signal review, audit staging, positions monitor, audit-missing tracker, `master-data-log.xlsx` |
| `claude-instructions/` | 16 | 45,852 | Global `CLAUDE.md` (user-level) + project `.claude/` tree (CLAUDE.md, rules, settings.json, per-skill SKILL.md copies) |
| `scheduled-tasks/` | 2 | 9,315 | `scheduled-tasks.json` (machine-readable) + `scheduled-tasks.md` (human-readable with dependency graph) |
| **Total** | **372** | **~4.75 MB** | |

## Skill inventory (18 skills)

Production (scheduled): `market-brief`, `news-events`, `daily-trade-rec`, `pipeline-recovery`, `positions-monitor`, `signal-review`, `literature-review`, `quarterly-methodology-review`, `system-review`
On-demand (event-triggered): `trade-update`, `consolidate-memory`
Utility (file formats): `docx` (61 files), `pdf` (12), `pptx` (59), `xlsx` (54)
Meta: `schedule`, `setup-cowork`, `skill-creator` (18)

Most trading skills are single-file (just SKILL.md) — intentional, they're lean.

## Scheduled tasks inventory (17 tasks, all enabled)

Daily (Mon–Fri): `us-close-snapshot-730am-v2`, `positions-monitor-intraday-9am`, `preflight-audit-data-1945pm`, `preflight-meta-additions-1952pm`, `daily-market-brief-8pm-v2`, `daily-news-events-810pm-v2`, `daily-trade-recommendation-820pm-v2`, `pipeline-recovery-830pm`

Weekly (Sun): `weekly-regime-signal-review-6pm`, `workspace-tidy-sunday-9pm`

Monthly/Quarterly/Semi-annual: `monthly-bootstrap-review` (May/Jun 2026 only, auto-retires), `quarterly-methodology-review`, `semi-annual-literature-review`, `system-review-semi-annual`

One-time reviews: `meta-shadow-mode-review-2026-04-25`, `methodology-audit-6mo-review-2026-10-14`, `methodology-audit-6mo-review-batch2-2026-10-14`

Full cron + dependency graph in `scheduled-tasks/scheduled-tasks.md`.

## System state at capture

- Audit-addition variables (Grade A, review 2026-10-14): residual momentum, intermediary capital ratio, basis-momentum — all live since 2026-04-14/15.
- Meta-integration batch (V029–V035, Step 1.5, Part B): Phases 1+2+4 deployed 2026-04-18; Phase 3 promotion gated on `meta-shadow-mode-review-2026-04-25`.
- Last production run: 2026-04-17 (brief + trade-rec + news + us-close).
- Last weekly review: 2026-04-15 (signal-review + weekly regime review).
- Last quarterly methodology review: 2026-04-15.
- Last system review: 2026-04-17 (inaugural semi-annual; next 2026-10-04 → actually 1st Sun of May 2026-05-03 via `system-review-semi-annual`).
- Asset universe: BTC, ETH; INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC; QQQ, SPY, EWJ, EWY; Brent, WTI, Gold, Silver, Copper, Palladium, Platinum; EURUSD, USDJPY.

## Restore procedure (rough)

1. Copy `framework/` contents to `C:\...\Trade\` root (13 files, overwrite existing).
2. Copy `skills-cowork/*` to `%USERPROFILE%\.claude\skills\` (or wherever Cowork installs skills locally).
3. Copy `auto-memory/*` to `.auto-memory/` (will overwrite current memory index + files).
4. Copy `scripts/*` to `Trade\scripts\`.
5. Restore pipeline state from `pipeline-config/` to root (`.pipeline-status.json`, `.pipeline-health.json`).
6. Re-create scheduled tasks from `scheduled-tasks/scheduled-tasks.json` using `create_scheduled_task` (cron + description + enabled).
7. Copy `claude-instructions/CLAUDE.md.global` back to `%USERPROFILE%\.claude\CLAUDE.md`; `claude-instructions/project-claude/*` back to `Trade\.claude\`.
8. `outputs-latest/master-data-log.xlsx` is the structured store — verify SignalLedger integrity before appending new rows.
9. Validate by running `pipeline-recovery` skill (Phase A triage will surface any missing wiring).

## Integrity

Counts verified against live sources at capture time. See `/verification.txt` for sampled diffs.
