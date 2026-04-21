---
name: System review execution — E1 + A1 + E4 (2026-04-17)
description: Execution pass on the three HIGH-impact proposals from system-review-2026-04-17.md; one live + seven patches ready; apply instructions in /mnt/Trade/patches/README.md
type: project
originSessionId: d8751fb2-f392-4cae-8f6e-ed9bb25ee98c
---
## Date
2026-04-17 (same-day execution following the inaugural system review)

## What was executed

**LIVE (no Gerald action required):**
1. **A1 scheduled task** — `positions-monitor-intraday-9am` created via `create_scheduled_task` MCP. Cron `0 9 * * 1-5`. Next fire Mon 2026-04-20 09:00 UTC+8. Self-contained task prompt includes 10-flag panel (F1–F10: stop buffer, stop hit, time-inv, earnings, catalyst, data, AH move, thesis var, portfolio heat, correlation gate), silent-when-OK fail-loud discipline, .pipeline-status.json integration.
2. **E4 helper script** — `/mnt/Trade/scripts/catalysts_cache.py` written and tested. Provides `write_catalysts`, `read_catalysts`, `latest_catalysts`, `filter_for_asset`, `filter_severity`, `to_markdown_table`. TRADE_DIR env-overridable. Validation strict by default.

**PATCHES READY (Gerald applies on Windows side — 6 files in `/mnt/Trade/patches/`):**
- `positions-monitor-SKILL.md` — install at `C:\Users\Lokis\Documents\Claude\skills\positions-monitor\SKILL.md` to enable on-demand phrases (the cron is already live).
- `E1-us-close-snapshot-prepend.md` — paste block at top of `C:\...\Scheduled\us-close-snapshot-730am-v2\SKILL.md`.
- `E1-workspace-tidy-prepend.md` — paste block at top of `C:\...\Scheduled\workspace-tidy-sunday-9pm\SKILL.md`.
- `E4-news-events-SKILL-patch.md` — append Section 4 to `C:\...\skills\news-events\SKILL.md` for cache write.
- `E4-market-brief-SKILL-patch.md` — replace §5 Catalyst calendar in brief SKILL.md for cache read.
- `E4-daily-trade-rec-SKILL-patch.md` — replace §5/§8 catalyst blocks in trade-rec SKILL.md for cache read.
- `README.md` — consolidated apply order + verification + rollback.

## Why execution was split live/patch

**Why:** Sandbox mount for `/mnt/.claude/skills/` is `dr-x` (read-only). Windows `C:\Users\Lokis\Documents\Claude\Scheduled\` is not reachable from the sandbox. `update_scheduled_task` MCP does not return current prompt text, so blind rewrite of us-close / workspace-tidy prompts would risk losing Phase 2/3 diagnostic logic. The pragmatic path is: execute what the MCP safely allows (new scheduled task creation), and deliver the rest as minimally-invasive prepend/replace patches that are zero-risk for Gerald to apply manually.

**How to apply:** Open `/mnt/Trade/patches/README.md` for full apply order, exact file paths, and verification checks.

## Expected token savings (aligned with system-review efficiency tally)

| Proposal | Monthly tokens saved |
|---|---|
| E1 (us-close + workspace-tidy read-overrides) | +780K to +1,300K |
| E4 (shared catalysts cache) | +80K to +120K |
| A1 (positions-monitor new burn) | −220K |
| **Net freed for trade-rec context** | **+640K to +1,200K** |

Monthly burn projected to drop from ~3.94M → ~2.7–3.3M.

## Verification plan once Gerald applies E1 patches

1. **Next us-close fire (Mon 2026-04-20 07:30 UTC+8):** run token count drops from ~52K → ~12–20K. Output `us-close-snapshot-2026-04-20.md` retains prior structure.
2. **Next workspace-tidy fire (Sun 2026-04-19 21:00 UTC+8):** run token count drops from ~43K → ~8–14K. Archival + diagnostics still complete per Retention Policy.
3. **Next news-events fire (Fri 2026-04-17 20:10 UTC+8, if E4 applied before then):** `catalysts-cache-2026-04-17.json` exists at root + `.catalysts-cache/`. News file footer contains `Catalysts cache written: N events`.
4. **A1 first scheduled fire (Mon 2026-04-20 09:00 UTC+8):** either silent OK (written to `.pipeline-status.json`) or `positions-monitor-2026-04-20.md` if any flag fires on INTC/Gold/QQQ.

## Closes six of nine system-review proposals

- **E1 done (patches)** → biggest boilerplate leak addressed.
- **E2 (apply six blocked patch files) — still pending.** Separate from this execution pass; Gerald must visit each one. Workspace-tidy should now surface them more visibly once E1 tightens that task.
- **E3 (trim brief flat rows) — still pending.** Not in this execution scope.
- **E4 done (patches + live helper).**
- **A1 done (live cron + patch for skill).**
- **A2 (trade-update pre-entry compliance check) — still pending.**
- **A3 (N-month audit-review template) — still pending.**
- **S1, S2 — still pending.**

## Apply status snapshot

- 2 of 9 live from MCP: A1 cron + E4 helper script.
- 6 of 9 patch-ready: A1 skill, E1×2, E4×3, system-review.skill (consolidate-memory cleanup).
- 1 of 9 structural (no patch needed): S2 requires design.

## Apply status snapshot — 2026-04-17 evening (post-install verification)

Sandbox grep of `/mnt/.claude/skills/` confirms Gerald applied most patches same day:

- ✅ `positions-monitor/SKILL.md` present (92 lines) — A1 skill installed.
- ✅ `news-events/SKILL.md` contains `catalysts_cache` ref — E4 news-events applied.
- ✅ `market-brief/SKILL.md` contains `catalysts_cache` ref — E4 market-brief applied.
- ✅ `daily-trade-rec/SKILL.md` contains `catalysts_cache` ref — E4 daily-trade-rec applied.
- ✅ `system-review/SKILL.md` no longer references `consolidate-memory` — system-review.skill installed.
- 🟡 `consolidate-memory/` folder still present in `/mnt/.claude/skills/` — Gerald to delete manually (instructions in `patches/remove-consolidate-memory-skill.md`).
- 🟡 E1 us-close-snapshot prepend — NOT verifiable from sandbox (scheduled-tasks dir not mounted). Still pending.
- 🟡 E1 workspace-tidy prepend — NOT verifiable from sandbox. Still pending.

Net: 5 of 8 Windows-side items confirmed applied the day they were produced. Only the two E1 scheduled-task prepends and the `consolidate-memory` folder delete remained open at that point. E1 verification will be automatic via token-count drop on Mon 2026-04-20 07:30 (us-close) and Sun 2026-04-19 21:00 (workspace-tidy) fires.

## Apply status snapshot — 2026-04-17 ~15:27 UTC+8 (final)

All three remaining Windows-side items closed during this session:

- ✅ **E1 us-close + workspace-tidy prepends** applied via `/mnt/Trade/patches/apply-E1.bat` (double-click PS1 launcher). Script is idempotent (marker check), makes timestamped `.bak-YYYYMMDD-HHMMSS` copies before modifying, reports APPLIED/SKIPPED/FAILED per task with color. Still awaiting passive verification: next fires are Sun 2026-04-19 21:00 (tidy) and Mon 2026-04-20 07:30 (us-close); token-drop from ~43K→8–14K and ~52K→12–20K respectively will confirm.
- ✅ **`consolidate-memory` folder deleted** via File Explorer guided through computer-use. Path: `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\skills-plugin\{60747006-…}\{69749f53-…}\skills\consolidate-memory`. Gerald pressed Delete after I selected the folder. Skills dir count confirmed 18 → 17 post-screenshot.

**Net: 10 of 10 system-review execution items now applied.** System-review proposals E1, A1, E4, plus the consolidate-memory cleanup, are all landed. Next checkpoint is the semi-annual `system-review-semi-annual` task (Sun 2026-05-03 19:00 UTC+8) which will re-audit the full architecture.

## Residual risk / watch items

- **Plugin re-sync**: the `consolidate-memory` folder sits inside a plugin-managed AppData bundle. If Claude Code pushes a plugin update that re-syncs the default skills list, the folder could reappear. If that happens, the root cause is an Anthropic-side default — resolution is thumbs-down feedback rather than another local delete.
- **E1 rollback**: timestamped `.bak-*` files are sitting next to the two Scheduled SKILL.md files. Remove them after the first successful post-E1 fires confirm nothing regressed.

## Addendum — 2026-04-17 ~21:50 UTC+8 — .skill packages produced

Four of the six patch-ready items are now also available as installable `.skill`
bundles (zip files containing the full SKILL.md) in `/mnt/Trade/patches/`:

- `positions-monitor.skill` — new skill, A1 gap closure
- `news-events.skill` — existing + E4 Step 10 cache writer
- `market-brief.skill` — existing + E4 Step 5.5 cache reader + §5 template update
- `daily-trade-rec.skill` — existing + E4 Step 3 cache-consumer block

Installing via Cowork app (Skills → Install from file) is the one-click path.
The .md patches remain authoritative for diff review and rollback. Either path
produces the same final SKILL.md on disk.

E1 still requires manual paste (scheduled tasks, not skills).


## Addendum — 2026-04-17 (later): skill↔task coverage audit + consolidate-memory removal

Coverage audit confirmed every production skill has a live scheduled runner; every daily/weekly output has a downstream consumer. No scheduling gaps.

Two drift patches applied sandbox-side to `/mnt/.claude/CLAUDE.md`:
- Skills list refreshed from stale "5 installed" + non-existent `preflight-check` to current 4-category breakdown (9 production + 1 on-demand + 4 utility + 3 meta).
- Pipeline table rewritten to match current crons (news 20:00 not 20:10, trade-rec 21:00 not 20:25, preflight 19:45 merged, positions-monitor / quarterly / semi-annual rows added, pointer to `reference_pipeline.md` as authoritative source).

Gerald: "there is no consolidate-memory skill. remove." Removed references from `CLAUDE.md` (on-demand line now lists only `trade-update`). Auto-memory grep confirmed clean.

`system-review.skill` bundle now in `/mnt/Trade/` — drops `consolidate-memory` from Infrastructure bucket list (line 37) and scope-boundary bullet (line 186). Install via Cowork Skills → Install from file. Folder deletion of `C:\...\.claude\skills\consolidate-memory\` instructions saved to `/mnt/Trade/patches/remove-consolidate-memory-skill.md`.


## How to apply
1. Open `/mnt/Trade/patches/README.md` for the full apply order.
2. Apply E1 first (zero-risk prepends, biggest saving).
3. Apply A1 skill + E4 three patches in any order.
4. After each next fire, verify via the checks in this memory and in the README.
