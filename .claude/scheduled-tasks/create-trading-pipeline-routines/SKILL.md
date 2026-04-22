---
name: create-trading-pipeline-routines
description: One-time setup: create all 13 remaining Claude Code cloud routines for Gerald's trading pipeline
---

You are creating 13 Claude Code cloud routines for a trading pipeline. This is a one-time setup task.

## Preconditions — verify ALL before creating anything

1. GitHub repo https://github.com/geraldyiu12529-cmyk/Gerald has "Allow unrestricted branch pushes" enabled
2. A cloud environment named "trading-system-env" exists with: Network=Trusted, Setup script=`pip install openpyxl requests`
3. Account timezone is UTC+8 (Asia/Singapore)
4. Claude Code plan is Max or higher (required for 7 weekday routines)
5. Routine `preflight-audit-data` already exists — skip it, do NOT recreate it

If any precondition fails, STOP immediately and report what needs to be fixed. Do NOT proceed with partial setup.

## Spec reference

The authoritative spec is in Trade/claude-code-migration/MIGRATION-GUIDE.md §7 in the Gerald repo (branch: main). If any detail below conflicts with that file, the file wins.

## Common settings for all routines

- Repo: https://github.com/geraldyiu12529-cmyk/Gerald
- Branch: main
- Working directory: Trade/
- Environment: trading-system-env
- "Allow unrestricted branch pushes": enabled
- All prompts end with a git commit + push step

## Create these 13 routines in order. Verify each appears in /schedule list before creating the next.

### DAILY (Mon–Fri)

**1. us-close-snapshot**
- cron: `30 7 * * 1-5`
- model: Sonnet
- prompt: "cd Trade/. Read Memory.md §2 Open Positions and the previous day's market brief. For each open position, pull the latest US close price via WebSearch. Write us-close-snapshot-{today}.md with: mark-to-market per position, any >1σ ATR moves vs the brief's levels, after-hours earnings reactions. Update .pipeline-status.json. Git commit and push all changes."

**2. positions-monitor**
- cron: `0 9 * * 1-5`
- model: Haiku
- prompt: "cd Trade/. /positions-monitor then git commit and push any output files."

**3. market-brief**
- cron: `0 20 * * 1-5`
- model: Sonnet
- prompt: "cd Trade/. /market-brief then git commit and push all new/changed files."

**4. news-events**
- cron: `0 20 * * 1-5`
- model: Sonnet
- prompt: "cd Trade/. /news-events then git commit and push all new/changed files."

**5. trade-rec**
- cron: `0 21 * * 1-5`
- model: Opus
- prompt: "cd Trade/. /daily-trade-rec then git commit and push all new/changed files."

**6. pipeline-recovery**
- cron: `0 22 * * 1-5`
- model: Haiku
- prompt: "cd Trade/. /pipeline-recovery then git commit and push if any recovery files were created."

### WEEKLY (Sunday)

**7. weekly-review**
- cron: `0 18 * * 0`
- model: Opus
- prompt: "cd Trade/. Two phases in one session. Phase 1: Read Memory.md, latest market brief, all news files from this week. Write weekly-review-{today}.md with regime trajectory, week's key events, thesis validation, lessons. Condense memory-lessons.md entries. Phase 2: /signal-review. Git commit and push all changes."

**8. workspace-tidy**
- cron: `0 21 * * 0`
- model: Haiku
- prompt: "cd Trade/. CRITICAL: This is a utility task, NOT a trading question. Do NOT follow the CLAUDE.md Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, or protocol documents unless explicitly listed below. Apply Retention Policy.md. Move files aged 8+ days to archive/YYYY-MM/. Digest files aged 31+ days into monthly digest. Check Memory.md for pinned files before archiving. Run /consolidate-memory. Append to archive/cleanup-log.md. Run diagnostics: Excel integrity, pipeline liveness, output continuity, cache health, skill presence. Git commit and push all changes."

### INFREQUENT

**9. quarterly-review**
- cron: `0 19 1 1,4,7,10 *`
- model: Opus
- prompt: "cd Trade/. /quarterly-methodology-review then git commit and push all changes."

**10. bootstrap-review**
- cron: `0 19 1 5,6 *`
- model: Sonnet
- prompt: "cd Trade/. Health check: are all routines firing? Are skills producing valid output? Check git log for recent routine commits. Report status. Disable this routine after Jul 1 2026. Git commit and push."

**11. literature-review**
- cron: `0 15 1 1,7 *`
- model: Opus
- prompt: "cd Trade/. /literature-review then git commit and push all changes."

**12. system-review**
- cron: `0 19 1 5,11 *`
- model: Opus
- prompt: "cd Trade/. /system-review then git commit and push all changes."

**13. audit-variable-review**
- ONE-TIME fire: 2026-10-14T19:00:00+08:00
- model: Opus
- prompt: "cd Trade/. Six-month review of the 3 audit-addition variables (residual momentum, intermediary capital ratio, basis-momentum). Read AuditAdditionLog in master-data-log.xlsx. Per variable: count days LIVE, decision-moving contributions, contribution rate normalized by days LIVE. Verdict: KEEP at Grade A, DEMOTE to B, or REMOVE. Write methodology-audit-6mo-review-2026-10-14.md. Git commit and push."

## After all 13 are created

1. Run /schedule list and print the full output — confirm 14 routines total (13 above + preflight-audit-data)
2. Trigger ONE low-risk routine via "Run now" — use positions-monitor or workspace-tidy (not market-brief, news-events, or trade-rec — those must fire on schedule to preserve the parallel-run comparison window)
3. Report the resulting git commit SHA from the test run

## Error handling

If any routine fails to create: STOP and report the routine name + error. Do NOT silently skip.