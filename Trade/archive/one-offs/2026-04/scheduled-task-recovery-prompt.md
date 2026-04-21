# Scheduled-Task Recovery — New-Session Handoff Prompt

Paste everything below (starting at the `===BEGIN PROMPT===` line) into a fresh Claude session. The prompt briefs the new session on the problem, tells it what to read before acting, and gives it the exact 14 recreations to perform.

---

===BEGIN PROMPT===

All 14 of my scheduled tasks are broken. The Claude desktop app shows "Task file not found or has unexpected format" on every task, and every run fails immediately.

**Root cause (already diagnosed, do not re-investigate from scratch — confirm with 2-3 tool calls and move on):** the task metadata is still registered in the Claude desktop app's DB (so `list_scheduled_tasks` returns all 14 tasks with intact crons and history), but the backing Windows folders at `C:\Users\Lokis\Documents\Claude\Scheduled\<taskId>\SKILL.md` are missing. Because the taskId is still registered in the DB, `create_scheduled_task` refuses with "already exists", and because the SKILL.md file doesn't exist, `update_scheduled_task` errors ENOENT. The sandbox cannot reach `C:\Users\Lokis\Documents\Claude\` directly.

**Recovery path I've already agreed to:** I will delete all 14 tasks in the Claude UI via the trash icon. Once deleted from the DB, the taskId conflict clears and you can call `create_scheduled_task` to recreate each one fresh. Run history is lost; everything else is rebuilt exactly.

---

## Before you do anything, read these files

These are the authoritative sources for how the pipeline works and what each task should do. Do NOT skim — each shapes one or more of the replacement prompts.

**Global framework (read in this order):**
1. `/mnt/.auto-memory/MEMORY.md` — index of persistent memories
2. `/mnt/.auto-memory/reference_pipeline.md` — full task-ID table, cron times, dependency chain, optimization changelog, known failure modes. **This is the spine.**
3. `/mnt/.claude/CLAUDE.md` — session startup protocol (Trade workspace rules)
4. `/mnt/Trade/Methodology Prompt.md` — 8-step framework the trading skills hang off
5. `/mnt/Trade/Risk Rules.md` — pre-entry checklist, circuit breakers
6. `/mnt/Trade/Data Sources.md` — variable-to-source mapping, fail-loud rule
7. `/mnt/Trade/Memory.md` — trader's working memory; §2 Open Positions and §6 Catalysts are load-bearing for multiple tasks
8. `/mnt/Trade/Retention Policy.md` — archival rules referenced by workspace-tidy
9. `/mnt/Trade/Pipeline-Recovery-Protocol.md` — task-level failure architecture and integrity check text per task

**Skill definitions (read every SKILL.md for the skills referenced below):**
- `/mnt/.claude/skills/market-brief/SKILL.md`
- `/mnt/.claude/skills/daily-trade-rec/SKILL.md`
- `/mnt/.claude/skills/news-events/SKILL.md`
- `/mnt/.claude/skills/positions-monitor/SKILL.md`
- `/mnt/.claude/skills/signal-review/SKILL.md`
- `/mnt/.claude/skills/pipeline-recovery/SKILL.md`
- `/mnt/.claude/skills/quarterly-methodology-review/SKILL.md`
- `/mnt/.claude/skills/literature-review/SKILL.md`
- `/mnt/.claude/skills/system-review/SKILL.md`
- `/mnt/.claude/skills/consolidate-memory/SKILL.md`
- `/mnt/.claude/skills/skill-creator/SKILL.md` (chained by system-review)

**Recent reports and outputs (so your prompts match the real current format):**
- Latest `/mnt/Trade/market-brief-*.md`
- Latest `/mnt/Trade/trade-rec-*.md` and `/mnt/Trade/report-*-trade-rec.html`
- Latest `/mnt/Trade/news-events/news-*.md` and `/mnt/Trade/news-events/README.md`
- Latest `/mnt/Trade/weekly-review-*.md` and `/mnt/Trade/signal-review-*.md`
- Latest `/mnt/Trade/us-close-snapshot-*.md`
- Latest `/mnt/Trade/audit-data-staging-*.md`

**Scripts the tasks reference (verify each exists before writing prompts that call them):**
- `/mnt/Trade/scripts/preflight_health_check.py`
- `/mnt/Trade/scripts/compute_audit_additions.py`
- `/mnt/Trade/scripts/data_retrieval_engine.py`
- `/mnt/Trade/scripts/pipeline_status.py`
- `/mnt/Trade/scripts/catalysts_cache.py`
- `/mnt/Trade/scripts/cache_manager.py`

**Data files referenced:**
- `/mnt/Trade/master-data-log.xlsx` — SignalLedger, DailyVariables, RegimeHistory, DataQuality, PerformanceStats sheets
- `/mnt/Trade/.pipeline-status.json`, `/mnt/Trade/.pipeline-health.json`
- `/mnt/Trade/.data-cache/` directory

After you've read these, run `list_scheduled_tasks` once to confirm current DB state. Then proceed.

---

## The 14 tasks to recreate

**Cron expressions are in LOCAL time (UTC+8), not UTC. All documented in `/mnt/.auto-memory/reference_pipeline.md` — cross-check before you fire the create calls.**

| # | taskId | cron / fireAt | Invokes | Hardening required |
|---|---|---|---|---|
| 1 | `daily-market-brief-8pm-v2` | `0 20 * * 1-5` | `market-brief` skill | Fail-loud on MISSING Grade A; write `.pipeline-status.json` |
| 2 | `daily-trade-recommendation-820pm-v2` | `0 21 * * 1-5` | `daily-trade-rec` skill | **Step 0 integrity pre-check:** brief must exist AND mtime ≤ 90 min, else abort. (Fixes the `p.exists()`-returns-False silently-carries-forward-prior-rec bug documented in reference_pipeline.md §Known failure modes.) |
| 3 | `daily-news-events-810pm-v2` | `0 20 * * 1-5` | `news-events` skill | Use `catalysts_cache.py` to write cache for downstream |
| 4 | `us-close-snapshot-730am-v2` | `30 7 * * 1-5` | Self-contained | **Read-override prepend:** skip CLAUDE.md startup protocol, skip Methodology Prompt / cores / protocol docs. Sections §1–§8 per reference_pipeline.md |
| 5 | `workspace-tidy-sunday-9pm` | `0 21 * * 0` | `consolidate-memory` + archive + diagnostics | **Read-override prepend** |
| 6 | `methodology-audit-6mo-review-2026-10-14` | fireAt `2026-10-14T09:00:00+08:00` | Self-contained (one-time) | KEEP/DEMOTE/REMOVE verdict on the 3 audit-addition variables (residual momentum, intermediary capital z-score, basis-momentum) |
| 7 | `quarterly-methodology-review` | `0 19 1 1,4,7,10 *` | `quarterly-methodology-review` skill | — |
| 8 | `monthly-bootstrap-review` | `0 19 1 5,6 *` | Self-contained | Bounded scope; active May/Jun 2026 only |
| 9 | `semi-annual-literature-review` | `0 15 1 1,7 *` | `literature-review` skill | Feeds quarterly review's candidate pipeline |
| 10 | `preflight-audit-data-1945pm` | `0 19 * * 1-5` | Self-contained (Phase 1 + Phase 2) | **Read-override prepend**; Phase 1 = `preflight_health_check.py` writes `.pipeline-health.json`; Phase 2 = `compute_audit_additions.py` writes `audit-data-staging-{YYYY-MM-DD}.md` |
| 11 | `weekly-regime-signal-review-6pm` | `0 18 * * 0` | Phase 1 self-contained + Phase 2 `signal-review` skill | Writes `weekly-review-*.md` then `signal-review-*.md` + HTML; updates SignalLedger/PerformanceStats |
| 12 | `pipeline-recovery-830pm` | `0 22 * * 1-5` | `pipeline-recovery` skill | **Phase A cheap guard:** target <3K tokens, ceiling 5K. Phase B only if Phase A flags |
| 13 | `system-review-semi-annual` | `0 19 1-7 5,11 0` | `system-review` skill + `skill-creator` chain | Writes patches to `/mnt/Trade/patches/` for any prompt edits (sandbox can't write to scheduled-task SKILL.md or ro skills mount) |
| 14 | `positions-monitor-intraday-9am` | `0 9 * * 1-5` | `positions-monitor` skill | **Silent-when-OK:** file written only if a trigger fires |

**Prompt-writing rules:**
- Skill-invocation tasks: keep the prompt short (5–15 lines). The skill carries the logic. Include date handling, version-tag-bump rule, `.pipeline-status.json` update where relevant, and a one-line exit summary.
- Self-contained tasks: spell out the read list, the action sequence, the output path, and the exit summary. If the task has a read-override, put the read-override at the very top as bold CRITICAL text.
- Every task ends with a one-line exit summary (makes pipeline-recovery's file sniff fast).
- Dates: use `{YYYY-MM-DD}` placeholder language — the running task will substitute the local date at fire time.

---

## Workflow

1. **Read the files listed above.** Do not skip this step — several tasks have non-obvious hardening (integrity pre-check, read-override, Phase A budget, silent-when-OK) documented in the authoritative files. If your prompts don't capture this, the pipeline regresses.

2. **Run `list_scheduled_tasks` once** to confirm current DB state matches the 14 taskIds above. Flag any drift.

3. **Wait for me to confirm "all deleted"** in the chat. I will delete the 14 tasks via the trash icon in the Claude UI (suggested order: rare → weekly → daily). Do not attempt to delete tasks yourself (no delete tool is exposed; the UI is the only way).

4. **When I say "all deleted":** call `list_scheduled_tasks` to confirm the DB is empty, then fire 14 `create_scheduled_task` calls in a single batched message. Cron/fireAt exactly as in the table. Description one-liner per task. Prompt per the rules above.

5. **Verify:**
   - `list_scheduled_tasks` returns 14 tasks with correct crons and `enabled: true`
   - Spot-check: ask me to click "Run now" on `positions-monitor-intraday-9am` (silent-when-OK, cheapest to run) and confirm the Instructions pane populates and the run completes without the "Task file not found" error
   - If that passes, the fix is complete; if not, investigate before mass-running the heavier tasks

6. **Update memory:** append a note to `/mnt/.auto-memory/project_system_state.md` recording the 2026-04-17 recovery event so future sessions know the current prompts are freshly reconstructed (not the originals).

---

## Things to NOT do

- Do not try to fix this from the sandbox side — it can't reach `C:\Users\Lokis\Documents\Claude\`.
- Do not call `update_scheduled_task` first (it will ENOENT); the DB-delete-then-create path is the only one that works.
- Do not batch the creates before I confirm deletions — taskId conflicts will burn half your calls.
- Do not shorten the prompts to the point that hardening is lost. The table above is the minimum; expand, don't contract.
- Do not change cron expressions or fireAt. The current timings are the result of optimization rounds documented in reference_pipeline.md §Optimization changelog.
- Do not add new tasks or merge tasks during recovery. This is a like-for-like restore. Architectural changes go through `system-review-semi-annual`, not a recovery.

===END PROMPT===

---

## Notes for Gerald (not part of the prompt)

- This prompt is self-contained — the new session doesn't need the current conversation's history.
- If the new session tries to shortcut the read step, push back with "read the files first" — the hardening details are non-obvious and will be lost otherwise.
- If the new session's `list_scheduled_tasks` shows fewer than 14 tasks before you've deleted anything, something else has changed on the DB side; investigate before proceeding.
