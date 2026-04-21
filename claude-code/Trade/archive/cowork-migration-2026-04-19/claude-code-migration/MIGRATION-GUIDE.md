# Trading System Migration: Cowork → Claude Code

**Date:** 2026-04-18 (updated)
**Status:** Ready for review

---

## 1. Feasibility Assessment

**Verdict: Fully feasible. Every Cowork feature has a direct Claude Code equivalent.**

| Cowork Feature | Claude Code Equivalent | Notes |
|---|---|---|
| Skills (SKILL.md) | `.claude/skills/<name>/SKILL.md` | 1:1 mapping. Same format, same invocation (`/skill-name`) |
| Scheduled Tasks | **Routines** (cloud) or Desktop Scheduled Tasks (local) | See §6 for detailed comparison |
| Auto-memory | `~/.claude/projects/<project>/memory/` | Same concept. 200-line MEMORY.md index, topic files. |
| CLAUDE.md | `.claude/CLAUDE.md` (project) + `~/.claude/CLAUDE.md` (user) | Richer scoping: project, user, local, managed, rules/ |
| WebSearch | WebSearch tool | Available in Claude Code |
| Bash/Python | Bash tool | Direct access, no sandbox mount issues |
| Read/Write/Edit | File tools | Direct filesystem — no `/mnt/Trade/` prefix needed |
| openpyxl/Excel | Via `Bash(python3 ...)` | Same. Pre-approve in settings.json |
| MCP servers | `.mcp.json` | Same protocol, different config location |
| Hooks (new) | `.claude/settings.json` hooks | **Bonus** — deterministic checks Cowork can't do |
| Path-scoped rules (new) | `.claude/rules/*.md` with `globs:` frontmatter | **Bonus** — load rules only for matching files |

**Key advantages of Claude Code over Cowork:**
1. **No read-only mount issue** — skills and files editable directly (the 6 blocked patches from system-review would apply instantly)
2. **Path-scoped rules** — evidence-grade rules only load when writing trading files, not for every session
3. **Hooks** — deterministic pre/post-tool checks (file validation, SignalLedger reminders) without burning LLM tokens
4. **Direct filesystem** — no `/mnt/Trade/` prefix, no sandbox mount complexity
5. **Model selection per task** — use Haiku for pipeline-recovery healthy path, Sonnet for news/monitor, Opus for trade-rec
6. **Routines** — cloud-hosted automation that runs without your machine being on

---

## 2. Token Optimization Analysis

### Current Estimated Monthly Burn: ~3.9M tokens

Breakdown:
- Daily pipeline (5 tasks × 22 days = 110 sessions): ~2.5M
- Weekly tasks (2 × 4 = 8 sessions): ~400K
- Positions monitor (22 sessions): ~200K
- Ad-hoc/interactive (~20 sessions): ~800K

### The Biggest Token Waste: Mandatory Startup Reads

Current CLAUDE.md forces EVERY session to read:
1. `Methodology Prompt.md` (13.7KB = ~3,400 tokens)
2. Latest market brief (~10KB = ~2,500 tokens)
3. `Memory.md` (17KB = ~4,250 tokens)
4. Auto-memory index (~5KB = ~1,250 tokens)

That's **~11,400 tokens per session** of mandatory reads. But 5 of 7 daily tasks don't need them all:
- `news-events` doesn't need Methodology Prompt or Risk Rules
- `pipeline-recovery` doesn't need ANY framework docs on healthy days
- `positions-monitor` doesn't need Methodology Prompt, cores, or Data Sources
- `us-close-snapshot` doesn't need cores
- `workspace-tidy` doesn't need ANY trading docs

**Savings from targeted reads: ~11,400 × 5 tasks × 22 days = ~1.25M tokens/month**

### Additional Savings

| Optimization | Mechanism | Estimated savings |
|---|---|---|
| Lean CLAUDE.md (55 lines vs current verbose) | Less context loaded per session | ~130K/month |
| Path-scoped rules (load only for matching files) | evidence-grades.md + risk-rules-summary.md | ~100K/month |
| Compressed skill instructions (20-40% shorter) | Less prompt per skill invocation | ~300K/month |
| Hooks for deterministic checks | File validation without LLM reasoning | ~60K/month |
| No redundant rule restatement in skills | Rules in CLAUDE.md/rules/, not repeated per skill | ~150K/month |

### Projected Monthly Burn: ~1.9–2.2M tokens (~44–51% reduction)

With model tiering (Haiku/Sonnet/Opus), **cost reduction could reach 55–65%**.

### Model Tiering Recommendations

| Task | Recommended Model | Rationale |
|---|---|---|
| pipeline-recovery (healthy) | Haiku | <3K tokens, pure JSON/file-stat check |
| positions-monitor (green) | Haiku | Price lookup + 10 boolean flags |
| us-close-snapshot | Sonnet | Position marking + delta detection |
| news-events | Sonnet | Web search + structured extraction |
| market-brief | Sonnet | Data pull + scoring (formulaic) |
| daily-trade-rec | Opus | Synthesis, judgment, HTML generation |
| signal-review | Opus | Statistical analysis, methodology feedback |
| quarterly-methodology-review | Opus | Deep analytical reasoning |
| system-review | Opus | Architecture judgment |
| workspace-tidy | Haiku | File moves + retention policy application |

---

## 3. Directory Structure

Copy the `.claude/` folder from this migration directory to your Trade workspace root:

```
Trade/                              ← your workspace root (also a GitHub repo for routines)
├── .claude/
│   ├── CLAUDE.md                   ← project instructions (55 lines, lean)
│   ├── settings.json               ← hooks, permissions
│   ├── rules/
│   │   ├── evidence-grades.md      ← loads only for trading output files
│   │   └── risk-rules-summary.md   ← loads only for trade-rec files
│   └── skills/
│       ├── market-brief/SKILL.md
│       ├── news-events/SKILL.md
│       ├── daily-trade-rec/SKILL.md
│       ├── pipeline-recovery/SKILL.md
│       ├── positions-monitor/SKILL.md
│       ├── signal-review/SKILL.md
│       ├── trade-update/SKILL.md
│       ├── literature-review/SKILL.md
│       ├── quarterly-methodology-review/SKILL.md
│       ├── system-review/SKILL.md
│       └── consolidate-memory/SKILL.md
├── Methodology Prompt.md           ← committed to repo
├── Risk Rules.md                   ← committed to repo
├── Data Sources.md                 ← committed to repo
├── Memory.md                       ← committed to repo (routines push updates back)
├── Coin core.md                    ← committed to repo
├── Trad core.md                    ← committed to repo
├── Retention Policy.md             ← committed to repo
├── Excel-Sync-Protocol.md          ← committed to repo
├── Trade-Execution-Protocol.md     ← committed to repo
├── master-data-log.xlsx            ← committed to repo (routines push updates back)
├── memory-lessons.md               ← committed to repo
├── scripts/                        ← committed to repo
│   ├── compute_audit_additions.py
│   ├── data_retrieval_engine.py
│   ├── pipeline_status.py
│   ├── catalysts_cache.py
│   ├── cache_manager.py
│   └── ...
├── news-events/                    ← committed to repo
├── .data-cache/                    ← .gitignore (rebuilt each run)
├── .pipeline-status.json           ← committed to repo
├── .pipeline-health.json           ← committed to repo
└── archive/                        ← committed to repo
```

---

## 4. Path Changes Required

All skill files use **relative paths** (e.g., `Memory.md` instead of `/mnt/Trade/Memory.md`). Claude Code runs from the project root, so relative paths resolve correctly.

**In Python scripts:** Change `'/mnt/Trade/'` references to `'.'` or use `Path('.')`. The scripts already support `DATA_DIR` environment variable — set it in settings.json if needed.

**One-time sed command for scripts:**
```bash
cd Trade
find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} +
```

---

## 5. Installation & Setup

### Step 1 — Install Claude Code

**Windows (PowerShell):**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Verify:**
```bash
claude --version
claude doctor    # full diagnostics
```

### Step 2 — Copy `.claude/` to your Trade folder

Copy the entire `.claude/` directory from `claude-code-migration/` into your Trade workspace root. Skills, rules, settings, and CLAUDE.md are all auto-discovered — no registration needed.

Or run the setup script: `python3 claude-code-migration/setup-claude-code.py`

### Step 3 — Fix script paths

Python scripts currently reference `/mnt/Trade/`. Run this one-time fix:
```bash
cd Trade
find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} +
```

### Step 4 — Initialize GitHub repo (required for routines)

Routines clone from GitHub on each run. Your Trade folder must be a GitHub repo:

```bash
cd Trade
git init
echo ".data-cache/" > .gitignore
git add -A
git commit -m "Initial trading system commit"
git remote add origin https://github.com/YOUR_USERNAME/trading-system.git
git push -u origin main
```

**Important:** This repo should be **private** — it contains your trading methodology and memory files.

### Step 5 — Launch and verify

```bash
cd Trade
claude
```

Inside the session, run:
- `/help` — confirms all 11 skills are discovered
- `/status` — shows model and account
- `/memory` — shows loaded CLAUDE.md and memory files
- `/context` — shows token budget usage

### Step 6 — Run the bootstrap verification prompt (paste this in):

```
Verify my trading system setup:
1. Check that .claude/CLAUDE.md exists and read it
2. List all skills in .claude/skills/ and confirm each has a SKILL.md
3. Confirm these framework files exist: Methodology Prompt.md, Risk Rules.md, Data Sources.md, Memory.md, Coin core.md, Trad core.md, Retention Policy.md, Excel-Sync-Protocol.md, Trade-Execution-Protocol.md
4. Confirm master-data-log.xlsx exists and has 9 sheets
5. Confirm scripts/ has: compute_audit_additions.py, data_retrieval_engine.py, pipeline_status.py, catalysts_cache.py, cache_manager.py
6. Run: python3 scripts/test_data_contract.py — all 26 tests should pass
7. Check .data-cache/ and news-events/README.md exist
8. Report any missing files
```

---

## 6. Automation: Routines vs Desktop Scheduled Tasks

Claude Code offers **two** ways to run tasks on a schedule. Your pipeline can use either or a mix of both.

### Comparison

| Feature | Routines (cloud) | Desktop Scheduled Tasks (local) |
|---|---|---|
| **Where it runs** | Anthropic cloud VM | Your local machine |
| **Requires machine on?** | No | Yes (Desktop app must be open) |
| **File access** | Fresh git clone per run | Full local filesystem |
| **State persistence** | Must commit + push changes back to repo | Files persist naturally |
| **Minimum interval** | 1 hour | 1 minute |
| **Jitter** | Up to 10% of period (max 15 min) | Minimal |
| **Catch-up on missed runs** | Fires once when available, no multi-catch-up | One catch-up within 7 days |
| **Skills access** | Committed `.claude/skills/` only | All local + user-level skills |
| **MCP servers** | Configured connectors only | Your machine's full MCP setup |
| **Network access** | Configurable (None/Trusted/Custom/Full) | Full local network |
| **Daily run limit** | Pro: 5, Max: 15, Team/Enterprise: 25 | Unlimited |
| **Trigger types** | Cron schedule, API webhook, GitHub events | Cron schedule only |
| **How to create** | Web UI, CLI (`/schedule`), or Desktop app | Desktop app GUI only |
| **Where configs live** | Cloud (claude.ai account) | `~/.claude/scheduled-tasks/` |

### Recommendation for This Pipeline

**Use routines for the daily pipeline** — they're more reliable (no dependency on your machine being on) and your tasks all run at ≥1 hour intervals. The tradeoff is that routines need a GitHub repo, and file changes must be committed + pushed back.

**Use desktop scheduled tasks for ad-hoc or sub-hourly tasks** — positions-monitor at 09:00 could use either, but if you ever want more frequent monitoring, desktop tasks allow it.

**Hybrid approach (recommended):**
- **Routines:** market-brief, news-events, trade-rec, pipeline-recovery, weekly-review, workspace-tidy, quarterly/semi-annual tasks
- **Desktop tasks:** positions-monitor, us-close-snapshot (convenient for morning check when machine is on)
- **Interactive only:** trade-update (event-driven, never scheduled)

### How Routines Handle File State

Routines get a **fresh git clone** each run. To persist changes:

1. The routine reads the latest state from the repo (Memory.md, master-data-log.xlsx, etc.)
2. The routine writes output files (market-brief, trade-rec, etc.) and updates Memory.md / Excel
3. The routine commits changes and pushes to a branch (default: `claude/routine-name`)
4. You can configure routines to push directly to `main` by enabling "Allow unrestricted branch pushes" for the repo

**For this pipeline:** Enable unrestricted branch pushes so each routine's changes (Memory.md updates, new briefs, SignalLedger appends) are immediately visible to the next routine in the chain.

### Cron Syntax for Routines

Standard 5-field cron: `minute hour day-of-month month day-of-week`

Times are interpreted in **your local timezone** (UTC+8 for you).

Examples:
```
0 20 * * 1-5     # Weekdays at 20:00 (market-brief)
0 21 * * 1-5     # Weekdays at 21:00 (trade-rec)
0 18 * * 0       # Sunday at 18:00 (weekly-review)
0 19 1 1,4,7,10 *  # 1st of Jan/Apr/Jul/Oct at 19:00 (quarterly)
0 15 1 1,7 *     # 1st of Jan/Jul at 15:00 (literature-review)
```

Minimum interval: 1 hour. Jitter: up to ~6 minutes on hourly schedules.

---

## 7. Creating Routines

### Method 1: Web UI (recommended for initial setup)

1. Go to [claude.ai/code/routines](https://claude.ai/code/routines)
2. Click **New routine**
3. Fill in: Name, Prompt, Model, Repository, Environment, Trigger
4. Save and test with **Run now**

### Method 2: CLI

In any Claude Code session:
```
/schedule
```
Claude walks you through creation conversationally. Use `/schedule list` to view, `/schedule update` to modify, `/schedule run <name>` to test.

### Method 3: Desktop app

Click **Schedule** → **New task** → **New remote task** (for routines) or **New local task** (for desktop scheduled tasks).

### Cloud Environment Setup

Create one shared environment for all trading routines:

| Setting | Value |
|---|---|
| **Network access** | Trusted (allows web search for variable pulls) |
| **Setup script** | `pip install openpyxl requests` |
| **Environment variables** | Any API keys your scripts need |

### Routine Definitions

#### Daily Routines (Mon–Fri)

| # | Name | Cron (UTC+8) | Model | Prompt |
|---|---|---|---|---|
| 1 | `us-close-snapshot` | `30 7 * * 1-5` | Sonnet | `Read Memory.md §2 Open Positions and the previous day's market brief. For each open position, pull the latest US close price via WebSearch. Write us-close-snapshot-{today}.md with: mark-to-market per position, any >1σ ATR moves vs the brief's levels, after-hours earnings reactions. Update .pipeline-status.json. Git commit and push all changes.` |
| 2 | `positions-monitor` | `0 9 * * 1-5` | Haiku | `/positions-monitor` then git commit and push any output files. |
| 3 | `preflight-audit-data` | `45 19 * * 1-5` | Sonnet | `Run scripts/compute_audit_additions.py to produce audit-data-staging-{today}.md. If the script fails, check .data-cache/ for cached inputs within staleness windows and retry. Write .pipeline-health.json with connectivity status. Update .pipeline-status.json. Git commit and push all changes.` |
| 4 | `market-brief` | `0 20 * * 1-5` | Sonnet | `/market-brief` then git commit and push all new/changed files. |
| 5 | `news-events` | `0 20 * * 1-5` | Sonnet | `/news-events` then git commit and push all new/changed files. |
| 6 | `trade-rec` | `0 21 * * 1-5` | Opus | `/daily-trade-rec` then git commit and push all new/changed files. |
| 7 | `pipeline-recovery` | `0 22 * * 1-5` | Haiku | `/pipeline-recovery` then git commit and push if any recovery files were created. |

#### Weekly Routines (Sunday)

| # | Name | Cron (UTC+8) | Model | Prompt |
|---|---|---|---|---|
| 8 | `weekly-review` | `0 18 * * 0` | Opus | `Two phases in one session. Phase 1: Read Memory.md, latest market brief, all news files from this week. Write weekly-review-{today}.md with regime trajectory, week's key events, thesis validation, lessons. Condense memory-lessons.md entries. Phase 2: /signal-review. Git commit and push all changes.` |
| 9 | `workspace-tidy` | `0 21 * * 0` | Haiku | `Apply Retention Policy.md. Move files aged 8+ days to archive/YYYY-MM/. Digest files aged 31+ days into monthly digest. Check Memory.md for pinned files before archiving. Run /consolidate-memory. Append to archive/cleanup-log.md. Run diagnostics: Excel integrity, pipeline liveness, output continuity, cache health, skill presence. Git commit and push all changes.` |

#### Quarterly / Semi-Annual / One-Time

| # | Name | Cron (UTC+8) | Model | Prompt |
|---|---|---|---|---|
| 10 | `quarterly-review` | `0 19 1 1,4,7,10 *` | Opus | `/quarterly-methodology-review` then git commit and push all changes. |
| 11 | `bootstrap-review` | `0 19 1 5,6 *` | Sonnet | `Health check: are all routines firing? Are skills producing valid output? Check git log for recent routine commits. Report status. Disable this routine after Jul 1. Git commit and push.` |
| 12 | `literature-review` | `0 15 1 1,7 *` | Opus | `/literature-review` then git commit and push all changes. |
| 13 | `system-review` | `0 19 1 5,11 *` | Opus | `/system-review` then git commit and push all changes. |
| 14 | `audit-variable-review` | One-time: 2026-10-14 | Opus | `Six-month review of the 3 audit-addition variables. Read AuditAdditionLog in master-data-log.xlsx. Per variable: count days LIVE, decision-moving contributions, contribution rate normalized by days LIVE. Verdict: KEEP at Grade A, DEMOTE to B, or REMOVE. Write methodology-audit-6mo-review-2026-10-14.md. Git commit and push.` |

### API Triggers (bonus)

Each routine gets a unique HTTPS endpoint for manual/external triggering:

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_XXXXX/fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Manual trigger: flash crash detected"}'
```

Useful for: emergency pipeline runs, position checks triggered by price alerts, manual re-runs after failures.

---

## 8. Auto-Memory Migration

Claude Code's auto-memory lives at `~/.claude/projects/<project-hash>/memory/`. The format is identical to Cowork's `.auto-memory/`.

**To find your project hash:** Launch `claude` from your Trade directory, then run `/memory`. It shows the memory directory path including the hash.

**Migration steps:**
1. Launch Claude Code from Trade folder: `cd Trade && claude`
2. Run `/memory` to see the auto-memory path (e.g., `~/.claude/projects/-Users-gerald-Trade/memory/`)
3. Copy all `.auto-memory/*.md` files to that directory
4. Claude Code will manage the directory going forward

**Important:** Always launch Claude Code from the same `Trade/` directory. The project hash is derived from the working directory path — launching from a different path creates a separate memory scope.

**Note for routines:** Routines run in cloud VMs and do NOT access your local `~/.claude/` auto-memory. Memory for routines comes from files committed to the repo (Memory.md, memory-lessons.md). The auto-memory path is for interactive Claude Code sessions only.

---

## 9. Key Differences to Be Aware Of

1. **No `/mnt/Trade/` prefix** — Claude Code runs from project root. All paths are relative.
2. **Skills invoked with `/`** — type `/market-brief` in Claude Code to invoke.
3. **Routines run in the cloud** — they clone your GitHub repo each run. Changes must be committed and pushed back. No local file persistence between routine runs.
4. **Git commit/push in routine prompts** — every routine prompt should end with a git commit + push instruction so changes propagate to the next routine in the chain.
5. **Hooks are new** — The settings.json includes a PostToolUse hook that reminds about SignalLedger append when writing trade-rec files. Add more hooks as needed.
6. **Path-scoped rules** — evidence-grades.md and risk-rules-summary.md only load when Claude is working on matching files (market-brief, trade-rec, signal-review, etc.).
7. **No computer-use** — Claude Code doesn't have Cowork's computer-use MCP. Not needed for this system.
8. **`allowed-tools` in skills** — Pre-approves tools so Claude doesn't ask for permission each time.
9. **Direct file access (local sessions)** — No sandbox isolation. Files created by Claude Code appear directly in your filesystem.
10. **Daily routine limits** — Pro: 5/day, Max: 15/day, Team/Enterprise: 25/day. Your daily pipeline has 7 weekday routines, so you need at least a Max plan or split some to desktop tasks.
11. **Routine jitter** — runs may start up to ~6 min late on hourly schedules. The 1-hour gap between brief (20:00) and trade-rec (21:00) accommodates this.

---

## 10. Migration Checklist (step by step)

**Phase 1 — Install & configure (10 min)**
- [ ] Install Claude Code: `irm https://claude.ai/install.ps1 | iex` (Windows) or `curl -fsSL https://claude.ai/install.sh | bash` (Mac/Linux)
- [ ] Verify: `claude --version` and `claude doctor`
- [ ] Copy `.claude/` folder from `claude-code-migration/` to `Trade/` root (or run `setup-claude-code.py`)
- [ ] Fix script paths: `cd Trade && find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} +`

**Phase 2 — Initialize GitHub repo (10 min)**
- [ ] `cd Trade && git init`
- [ ] Create `.gitignore` with `.data-cache/` and any secrets
- [ ] `git add -A && git commit -m "Trading system initial commit"`
- [ ] Create private repo on GitHub
- [ ] `git remote add origin <url> && git push -u origin main`

**Phase 3 — Verify setup (5 min)**
- [ ] Launch: `cd Trade && claude`
- [ ] Run `/help` — confirm all 11 skills listed
- [ ] Run the bootstrap verification prompt from §5 Step 6
- [ ] Fix any issues reported

**Phase 4 — Migrate memory (5 min)**
- [ ] Run `/memory` to find auto-memory path
- [ ] Copy `.auto-memory/*.md` files to that path (see §8)

**Phase 5 — Test skills manually (30 min)**
- [ ] Run `/market-brief` — check output file and master-data-log.xlsx
- [ ] Run `/news-events` — check news file and catalysts cache
- [ ] Run `/daily-trade-rec` — check rec, HTML report, SignalLedger
- [ ] Run `/positions-monitor` — check silent-when-OK or flag report
- [ ] Run `/pipeline-recovery` — check healthy fast-exit

**Phase 6 — Create routines (20 min)**
- [ ] Go to [claude.ai/code/routines](https://claude.ai/code/routines)
- [ ] Create cloud environment (Trusted network, `pip install openpyxl requests`)
- [ ] Add your Trade repo (enable unrestricted branch pushes)
- [ ] Create all 14 routines per §7 table
- [ ] Click **Run now** on one routine to verify it works end-to-end
- [ ] Check that it committed + pushed changes to the repo

**Phase 7 — Parallel run & cutover (3–5 days)**
- [ ] Keep Cowork tasks enabled alongside Claude Code routines for 1–2 days
- [ ] Monitor first routine run end-to-end (check run history at claude.ai/code/routines)
- [ ] Compare outputs (brief, news, rec) between Cowork and Claude Code
- [ ] After 3 successful days: disable Cowork scheduled tasks
- [ ] Keep Cowork skills as rollback for 2 weeks, then clean up

---

## 11. Rollback Plan

If Claude Code doesn't work as expected:
1. The `.claude/` folder doesn't affect Cowork — both can coexist
2. Cowork scheduled tasks remain active until you disable them
3. All workspace files (Memory.md, master-data-log.xlsx, etc.) are shared — both systems read/write the same files
4. To roll back: simply disable routines (pause or delete at claude.ai/code/routines) and re-enable Cowork scheduled tasks
5. Git history preserves every routine's changes — easy to inspect and revert

---

## 12. Routine Limits & Plan Requirements

| Plan | Routines/day | Enough for this pipeline? |
|---|---|---|
| Pro | 5 | No — 7 weekday routines alone exceeds cap |
| Max | 15 | Yes — 7 weekday + 2 weekly + infrequent quarterly = fits |
| Team/Enterprise | 25 | Yes with headroom |

**If on Pro plan:** Use desktop scheduled tasks for the 2 cheapest routines (positions-monitor, pipeline-recovery) and cloud routines for the other 5.

---

## Appendix: Skill Size Comparison

| Skill | Cowork (KB) | Claude Code (KB) | Reduction |
|---|---|---|---|
| daily-trade-rec | 24.3 | ~10.5 | -57% |
| signal-review | 20.1 | ~6.5 | -68% |
| literature-review | 17.9 | ~5.0 | -72% |
| quarterly-methodology-review | 17.4 | ~5.5 | -68% |
| pipeline-recovery | 15.4 | ~4.5 | -71% |
| market-brief | 14.2 | ~6.5 | -54% |
| system-review | 14.9 | ~5.0 | -66% |
| news-events | 13.6 | ~7.0 | -49% |
| trade-update | 12.3 | ~5.0 | -59% |
| positions-monitor | 4.9 | ~3.0 | -39% |
| consolidate-memory | 1.9 | ~0.8 | -58% |
| **Total** | **156.9** | **~59.3** | **-62%** |

The 62% reduction in skill instruction size translates directly to fewer tokens loaded per skill invocation. Combined with targeted reads (no unnecessary framework file loading) and path-scoped rules, this produces the estimated 44–51% total token reduction.
