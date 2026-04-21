# Routine → Output Map

Generated: 2026-04-19 (Claude Code, Trade/practical-liskov-278700 worktree).
Source of truth: `.claude/skills/{skill}/SKILL.md`. This map is a summary — always verify against the SKILL.md before changing wiring.

**2026-04-19 update — consolidated daily file.** Every producer routine also packs its output into the consolidated daily file under a canonical section anchor via `scripts/pack_daily.py`. Per-routine source files continue to be written for downstream skill-read compatibility. See §5 below for the section map and filename convention.

**2026-04-19 update — date-folder convention.** All dated outputs (producer source files, HTML reports, consolidated daily file) now live under `{YYYY-MM-DD}/` at workspace root — one folder per local UTC+8 date. The consolidated daily file is at `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`. Downstream skills glob across date folders (`*/market-brief-*.md`, `*/trade-rec-*.md`, etc.) with root fallback for legacy files. Skill SKILL.md files and scheduled-task wrappers were both updated.

---

## 1. Full map (10 skills)

| # | Routine | Primary output (write) | Secondary writes | Upstream reads | Model | Schedule |
|---|---|---|---|---|---|---|
| 1 | **market-brief** | `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md` | `master-data-log.xlsx` → DailyVariables, RegimeHistory, DataQuality, CatalystLog; framework/Memory.md §5/§6; `framework/memory-lessons.md` | framework/Memory.md §2/§5/§6; framework/Methodology Prompt.md; framework/Risk Rules.md; framework/Data Sources.md; master-data-log.xlsx (RegimeHistory, DailyVariables); `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` (root fallback); `.catalysts-cache/` (read); scripts: `data_retrieval_engine`, `catalysts_cache` | sonnet | Mon–Fri 20:00 UTC+8 |
| 2 | **news-events** | `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` | `.catalysts-cache/catalysts-cache-{YYYY-MM-DD}.json`; framework/Memory.md §6 | framework/Memory.md §2/§6; master-data-log.xlsx (RegimeHistory); `news-events/README.md`; prior `*/news-*.md` (glob); scripts: `catalysts_cache` | sonnet | Mon–Fri 20:10 UTC+8 |
| 3 | **daily-trade-rec** | `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` | `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html`; master-data-log.xlsx → SignalLedger, AuditAdditionLog, CatalystLog; framework/Memory.md §2/§5; `framework/memory-lessons.md` | framework/Memory.md; framework/Methodology Prompt.md; framework/Risk Rules.md; master-data-log.xlsx (RegimeHistory, DailyVariables, SignalLedger OPEN); `{today}/market-brief-{today}.md`; `{today}/news-{today}.md`; `*/us-close-snapshot-*.md` (latest; root fallback); `*/weekly-review-*.md` (latest-Sunday); `*/signal-review-*.md` (latest); scripts: `catalysts_cache` | opus | Mon–Fri 20:20 UTC+8 |
| 4 | **positions-monitor** | `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` (silent-when-OK — written only if flags fire) | `pipeline/.pipeline-status.json` (status); auto-memory (CRITICAL flags only) | framework/Memory.md §2/§7; `pipeline/.pipeline-status.json`; `*/us-close-snapshot-*.md` (latest; root fallback) | sonnet | Mon–Fri 09:00 UTC+8 |
| 5 | **pipeline-recovery** | (no markdown on healthy path) | `pipeline/.pipeline-status.json` (watchdog); framework/Memory.md System Alert block (CRITICAL only) | scripts: `pipeline_status`; `pipeline/audit-data-missing-tracker.md` | haiku | Daily 20:30 UTC+8 |
| 6 | **trade-update** | framework/Memory.md §2/§7 | master-data-log.xlsx → SignalLedger row update; `framework/memory-lessons.md`; auto-memory (repeated patterns only) | framework/Trade-Execution-Protocol.md; framework/Memory.md §2/§5/§7; master-data-log.xlsx (SignalLedger) | sonnet | Event-driven (on-demand only) |
| 7 | **signal-review** | `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` (+ `{YYYY-MM-DD}/report-{YYYY-MM-DD}-signal-review.html`) | master-data-log.xlsx → PerformanceStats, SignalLedger (status updates), VariableRegistry; `framework/memory-lessons.md` | master-data-log.xlsx (SignalLedger, RegimeHistory, PerformanceStats, AuditAdditionLog); framework/Methodology Prompt.md; framework/Memory.md §2/§5; `framework/memory-lessons.md`; prior `*/signal-review-*.md` | opus | Sun 18:00 UTC+8 |
| 8 | **literature-review** | `{YYYY-MM-DD}/literature-review-{YYYY-MM-DD}[-scope].md` | master-data-log.xlsx → VariableRegistry (Candidate rows) | framework/Methodology Prompt.md; framework/Trad core.md; framework/Coin core.md; framework/Data Sources.md; framework/Memory.md §9; `framework/memory-lessons.md`; master-data-log.xlsx; prior `*/quarterly-methodology-review-*.md`; recent `*/signal-review-*.md` | opus | Semi-annual (1st Sun of May/Nov) |
| 9 | **quarterly-methodology-review** | `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md` | master-data-log.xlsx → VariableRegistry; methodology change proposals | master-data-log.xlsx (SignalLedger, PerformanceStats, RegimeHistory, AuditAdditionLog); framework/Methodology Prompt.md; framework/Risk Rules.md; framework/Data Sources.md; framework/Trad core.md; framework/Coin core.md; framework/Memory.md §9; `framework/memory-lessons.md`; all `*/signal-review-*.md`; prior `*/quarterly-methodology-review-*.md` | opus | Quarterly |
| 10 | **system-review** | `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` (+ `.html`) | `patches/{skill}-patch.md` files (when skill-creator chain enabled) | (implicit — inventories all skills/tasks/files; does NOT edit) | opus | Semi-annual (1st Sun of May/Nov) |

Scheduled tasks not mapped to a skill (utility routines):
- **us-close-snapshot** — writes `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md` (reads framework/Memory.md §2/§5/§6 + prior brief/rec; no framework doc loads)
- **preflight-audit-data** — writes `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` (reads `.data-cache/`; runs `scripts/compute_audit_additions.py`)
- **preflight-meta-additions** — writes `{YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md` (reads `.data-cache/`; runs `scripts/compute_meta_additions.py`)
- **weekly-regime-signal-review** — paired weekly-review + signal-review; writes `{YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md` and invokes signal-review skill
- **workspace-tidy** — enforces framework/Retention Policy.md (date-folder-aware); appends to `archive/cleanup-log.md`

---

## 2. Upstream/downstream link verification

Every read path declared in each SKILL.md was checked against the current filesystem:

| Link | Status | Notes |
|---|---|---|
| framework/Memory.md | ✅ live in framework/ | All 10 skills read |
| framework/Methodology Prompt.md | ✅ live in framework/ | 6 skills read (brief, rec, signal-review, lit-review, quarterly, brief) |
| framework/Risk Rules.md | ✅ live in framework/ | 4 skills read (brief, rec, trade-update via protocol, positions-monitor via protocol) |
| framework/Data Sources.md | ✅ live in framework/ | 3 skills read (brief, lit-review, quarterly) |
| framework/Coin core.md / framework/Trad core.md | ✅ live in framework/ | lit-review + quarterly only (per CLAUDE.md discipline) |
| framework/Excel-Sync-Protocol.md | ✅ live in framework/ | brief, rec, signal-review, trade-update read before xlsx writes |
| framework/Retention Policy.md | ✅ live in framework/ | workspace-tidy task only |
| framework/Trade-Execution-Protocol.md | ✅ live in framework/ | trade-update only |
| framework/memory-lessons.md | ✅ live in framework/ | brief, rec, signal-review append; lit-review, quarterly read |
| master-data-log.xlsx | ✅ live at root | 7 skills read or write |
| pipeline/audit-data-missing-tracker.md | ✅ live in pipeline/ | pipeline-recovery Step 4f |
| `{today}/audit-data-staging-{today}.md` | ✅ lives under today's date folder; legacy root copies remain for 2026-04-15, -16, -17 | Consumed by brief Step 2 and rec Step 3 (with root fallback) |
| news-events/README.md | ✅ live | news-events Step 1 |
| scripts/data_retrieval_engine.py | ✅ live | market-brief |
| scripts/catalysts_cache.py | ✅ live | news-events (write), brief + rec (read) |
| scripts/pipeline_status.py | ✅ live | pipeline-recovery |
| .catalysts-cache/ | ✅ live (contains 2026-04-17 snapshot) | Shared cache populated by news-events, consumed by brief + rec |
| .data-cache/ | ✅ live (80 variable JSON files + Tier-2 CSVs) | `data_retrieval_engine` |
| pipeline/.pipeline-status.json | ✅ live (62 lines, most-recent: 2026-04-19 brief PARTIAL) | pipeline-recovery, positions-monitor |

**No broken links detected.** No routine references a framework doc or script that was moved into `archive/` during this cleanup.

---

## 3. Output file conventions

Since 2026-04-19, **all dated outputs live inside the date folder** `{YYYY-MM-DD}/` at workspace root. Every producer routine also packs its output into the consolidated daily file at `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md` via `scripts/pack_daily.py` (see §4).

- `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md` — **consolidated same-day view** (pack targets §A–§H + §W/§S); primary human-readable artifact
- `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md` — overwritten same-day with version bump (`v1`, `v2` in header); packed into §D
- `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` — rewritten fresh nightly; packed into §E
- `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` + `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html` — never digested (permanent audit trail); markdown packed into §F, HTML stays separate
- `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md` — normal Tier 1 → 2 → 3 lifecycle; packed into §A
- `{YYYY-MM-DD}/positions-monitor-{YYYY-MM-DD}.md` — conditional (silent-when-OK); packed into §G (inline "Silent" marker if no file)
- `{YYYY-MM-DD}/audit-data-staging-{YYYY-MM-DD}.md` — packed into §B
- `{YYYY-MM-DD}/meta-additions-staging-{YYYY-MM-DD}.md` — shadow compute; packed into §C

Periodic outputs (all inside the Sunday/quarterly/semi-annual date folder):
- `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` (+ `{YYYY-MM-DD}/report-{YYYY-MM-DD}-signal-review.html`) — Sunday
- `{YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md` — Sunday, never digested
- `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md` — quarterly, permanent
- `{YYYY-MM-DD}/literature-review-{YYYY-MM-DD}[-scope].md` — semi-annual, permanent
- `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` + `.html` — semi-annual, permanent

**Legacy root-level dated files** (`market-brief-YYYY-MM-DD.md` etc. produced before 2026-04-19) remain readable: downstream skills glob across both locations (`*/market-brief-*.md` plus root `market-brief-*.md`) and the workspace-tidy routine sweeps them into `archive/YYYY-MM/{YYYY-MM-DD}/` at Tier 2.

Structured store:
- `master-data-log.xlsx` — 10 sheets: SignalLedger, PerformanceStats, RegimeHistory, DailyVariables, AuditAdditionLog, DataQuality, VariableRegistry, MethodologyNotes, CatalystLog, README. Per `framework/Excel-Sync-Protocol.md`.

Caches (git-ignored / ephemeral):
- `.data-cache/` — persistent Tier-2 variable store (staleness-classified)
- `.catalysts-cache/catalysts-cache-{YYYY-MM-DD}.json` — 30-day forward catalyst window
- `pipeline/.pipeline-status.json`, `pipeline/.pipeline-health.json` — pipeline watchdog state

---

## 4. Consolidated daily file (2026-04-19+)

Every producer routine packs its output into a single same-day file:
`{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md`

**Canonical filename:** `daily-{YYYY-MM-DD}.md` (e.g. `2026-04-19/daily-2026-04-19.md`) inside the date folder at workspace root. Created lazily on first pack of the day; upserted thereafter.

**Section anchors** (stable order; helper keeps them sorted):

| § | Title | Routine | Typical time (UTC+8) | Source file packed |
|---|---|---|---|---|
| A | US Close Snapshot | us-close-snapshot | 07:30 | `{date}/us-close-snapshot-{date}.md` |
| B | Preflight — Audit Data Staging | preflight-audit-data | 19:45 | `{date}/audit-data-staging-{date}.md` |
| C | Preflight — Meta-Additions Staging | preflight-meta-additions | 19:52 | `{date}/meta-additions-staging-{date}.md` |
| D | Market Brief | daily-market-brief-8pm | 20:00 | `{date}/market-brief-{date}.md` (v1→vN upserts in place) |
| E | News & Events | news-events-daily | 20:10 | `{date}/news-{date}.md` |
| F | Trade Recommendation | trade-rec-daily | 20:20 | `{date}/trade-rec-{date}.md` (markdown only; HTML report stays separate) |
| G | Positions Monitor | positions-monitor | 09:00 | `{date}/positions-monitor-{date}.md` if flags fired, else an inline "Silent" marker |
| H | Pipeline Recovery | pipeline-recovery-daily | 22:00 | inline one-liner — only on Phase B (recovery action); Phase A-only skips pack |
| W | Weekly Review | weekly-regime-signal-review | Sun 18:00 | `{date}/weekly-review-{date}.md` |
| S | Signal Review | weekly-regime-signal-review | Sun 18:00 | `{date}/signal-review-{date}.md` (markdown only; HTML report stays separate) |

**Helper:** `scripts/pack_daily.py` — accepts `--section`, `--source` (or `--content`), `--status`, optional `--title`/`--date`. Creates `{date}/` and `{date}/daily-{date}.md` if missing (with header `# Daily Pipeline — {date} (UTC+8)`); otherwise upserts the named section in-place (same-day re-runs replace the section rather than appending, so brief v1 → v2 refreshes §D cleanly).

**Why per-routine source files still exist.** Per-routine source files are the canonical artifact for downstream skills (the daily file is a convenience view, not the source of truth). Downstream skills read them directly via glob across date folders:
- `daily-trade-rec` skill reads `{today}/market-brief-{today}.md`, `{today}/news-{today}.md`, `*/us-close-snapshot-*.md` (latest), `*/weekly-review-*.md` (latest), `*/signal-review-*.md` (latest)
- `market-brief` skill reads `{today}/audit-data-staging-{today}.md`
- `trade-rec-daily` routine pre-check verifies `{today}/market-brief-{today}.md`, `{today}/news-{today}.md`, `{today}/audit-data-staging-{today}.md`
- `weekly-regime-signal-review` Phase 1 reads 5 `*/market-brief-*.md` + 7 `*/news-*.md` (root fallback for legacy pre-2026-04-19 files)

Retention Policy applies to the whole date folder: the folder moves to `archive/YYYY-MM/{YYYY-MM-DD}/` at Tier 2 (≥8 days), and digestable files inside it are removed at Tier 3 (≥31 days). See `framework/Retention Policy.md`.

**Not packed** (remain separate files):
- `report-{date}-trade-rec.html` — HTML audit trail, permanent
- `report-{date}-signal-review.html` — HTML audit trail, weekly
- `master-data-log.xlsx` — structured Excel store
- `pipeline/.pipeline-status.json`, `pipeline/.pipeline-health.json` — JSON state
- `.data-cache/`, `.catalysts-cache/` — caches
- `archive/cleanup-log.md` — workspace-tidy append log

---

## 5. Post-cleanup workspace layout

**Root:** framework docs, `{YYYY-MM-DD}/` date folders (one per local date with dated outputs), active project folders (bnma/, news-events/, scripts/, archive/), pipeline state files, `master-data-log.xlsx`. The `Bayesian Meta-Analysis/` folder was consolidated into `bnma/` on 2026-04-19 (byte-identical duplicates deleted; AI drafts moved to `archive/one-offs/2026-04/bnma-drafts/`). The `Research & Rationale/` holding folder was removed on 2026-04-20 (empty, no longer needed).

**`.claude/`:** CLAUDE.md, settings.json, `rules/` (evidence-grades, risk-rules-summary), `skills/` (10 installed skills, one SKILL.md each).

**`archive/`:**
- `2026-04/` + `weekly/` — empty (no Tier-2 files yet; earliest eligible 2026-04-22)
- `cowork-migration-2026-04-19/` — packaged Cowork artifacts (skills-packaged, patches, skill-work, .skill-stage, claude-code-migration, migration-prompts, deployment-memos)
- `outputs-superseded-2026-04/` — 18 obsolete audit/report/patch-note files
- `one-offs/2026-04/` — prompts and generalization docs
- `duplicates/` — byte-identical root copies quarantined
- `cleanup-log.md`, `memory-log-2026-W16.md`

See `archive/cleanup-log.md` for the full move list.
