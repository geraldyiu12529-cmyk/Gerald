# Claude Code Bootstrap Prompt

Paste this into your first Claude Code session after installing. Run from your `Trade/` directory.

---

## Option A — If `.claude/` folder doesn't exist yet

```
Run python3 claude-code-migration/setup-claude-code.py to bootstrap my trading system. Then fix script paths: find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} + . After that, verify: list all skills in .claude/skills/, confirm framework files exist (Methodology Prompt.md, Risk Rules.md, Data Sources.md, Memory.md, master-data-log.xlsx), and run python3 scripts/test_data_contract.py.
```

## Option B — If `.claude/` folder already exists (setup script already ran)

```
Fix script paths: find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} + . Then verify my trading system: list all 11 skills in .claude/skills/ and confirm each has a SKILL.md. Confirm framework files exist: Methodology Prompt.md, Risk Rules.md, Data Sources.md, Memory.md, Coin core.md, Trad core.md, Excel-Sync-Protocol.md, Trade-Execution-Protocol.md, Retention Policy.md. Confirm master-data-log.xlsx exists. Confirm scripts/ has: compute_audit_additions.py, data_retrieval_engine.py, pipeline_status.py, catalysts_cache.py, cache_manager.py. Run python3 scripts/test_data_contract.py. Check .data-cache/ and news-events/README.md exist. Report any issues.
```

---

## After verification — create routines

Go to [claude.ai/code/routines](https://claude.ai/code/routines) (or use `/schedule` in Claude Code CLI).

### One-time setup first:

1. **Create a cloud environment:**
   - Network: Trusted (allows web search)
   - Setup script: `pip install openpyxl requests`
   - Environment variables: any API keys your scripts need

2. **Add your Trade repo:**
   - Point to your GitHub private repo
   - Enable "Allow unrestricted branch pushes" so routines can push to main

### Then create these 14 routines:

#### Daily (Mon–Fri)

| Name | Cron | Model | Prompt |
|---|---|---|---|
| us-close-snapshot | `30 7 * * 1-5` | Sonnet | `Read Memory.md §2 Open Positions and the previous day's market brief. For each open position, pull the latest US close price via WebSearch. Write us-close-snapshot-{today}.md with: mark-to-market per position, any >1σ ATR moves vs the brief's levels, after-hours earnings reactions. Update .pipeline-status.json. Git commit and push all changes.` |
| positions-monitor | `0 9 * * 1-5` | Haiku | `/positions-monitor` then git commit and push any output files. |
| preflight-audit-data | `45 19 * * 1-5` | Sonnet | `Run scripts/compute_audit_additions.py to produce audit-data-staging-{today}.md. If the script fails, check .data-cache/ for cached inputs within staleness windows and retry. Write .pipeline-health.json with connectivity status. Update .pipeline-status.json. Git commit and push all changes.` |
| market-brief | `0 20 * * 1-5` | Sonnet | `/market-brief` then git commit and push all new/changed files. |
| news-events | `0 20 * * 1-5` | Sonnet | `/news-events` then git commit and push all new/changed files. |
| trade-rec | `0 21 * * 1-5` | Opus | `/daily-trade-rec` then git commit and push all new/changed files. |
| pipeline-recovery | `0 22 * * 1-5` | Haiku | `/pipeline-recovery` then git commit and push if any recovery files were created. |

#### Weekly (Sunday)

| Name | Cron | Model | Prompt |
|---|---|---|---|
| weekly-review | `0 18 * * 0` | Opus | `Two phases in one session. Phase 1: Read Memory.md, latest market brief, all news files from this week. Write weekly-review-{today}.md with regime trajectory, week's key events, thesis validation, lessons. Condense memory-lessons.md entries. Phase 2: /signal-review. Git commit and push all changes.` |
| workspace-tidy | `0 21 * * 0` | Haiku | `Apply Retention Policy.md. Move files aged 8+ days to archive/YYYY-MM/. Digest files aged 31+ days into monthly digest. Check Memory.md for pinned files before archiving. Run /consolidate-memory. Append to archive/cleanup-log.md. Run diagnostics: Excel integrity, pipeline liveness, output continuity, cache health, skill presence. Git commit and push all changes.` |

#### Quarterly / Semi-Annual / One-Time

| Name | Cron | Model | Prompt |
|---|---|---|---|
| quarterly-review | `0 19 1 1,4,7,10 *` | Opus | `/quarterly-methodology-review` then git commit and push all changes. |
| bootstrap-review | `0 19 1 5,6 *` | Sonnet | `Health check: are all routines firing? Are skills producing valid output? Check git log for recent routine commits. Report status. Disable this routine after Jul 1. Git commit and push.` |
| literature-review | `0 15 1 1,7 *` | Opus | `/literature-review` then git commit and push all changes. |
| system-review | `0 19 1 5,11 *` | Opus | `/system-review` then git commit and push all changes. |
| audit-variable-review | One-time: 2026-10-14 | Opus | `Six-month review of the 3 audit-addition variables. Read AuditAdditionLog in master-data-log.xlsx. Per variable: count days LIVE, decision-moving contributions, contribution rate normalized by days LIVE. Verdict: KEEP at Grade A, DEMOTE to B, or REMOVE. Write methodology-audit-6mo-review-2026-10-14.md. Git commit and push.` |

### Plan requirement

Your daily pipeline has 7 weekday routines. Pro plan allows 5/day — you need **Max plan** (15/day) or higher. Alternatively, move positions-monitor + pipeline-recovery to desktop scheduled tasks (they're cheap Haiku tasks anyway).
