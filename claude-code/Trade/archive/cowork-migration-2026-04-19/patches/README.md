# System-Review Execution Patches — 2026-04-17

All artifacts required to complete E1, A1, E4 from `system-review-2026-04-17.md`.
Created during the execute pass on 2026-04-17 evening.

## INSTALLABLE `.skill` PACKAGES (new, 2026-04-17 ~21:50 UTC+8)

Four `.skill` files are now available in this directory as an alternative to
manual SKILL.md edits. Install each through the Cowork app (Skills → Install
from file) — one click replaces the multi-paste workflow described below.

| File | What it installs | Replaces |
|---|---|---|
| `positions-monitor.skill` | New skill, closes Monitoring bucket gap | Manual copy of `positions-monitor-SKILL.md` |
| `news-events.skill` | Existing news-events + E4 Step 10 cache writer | `E4-news-events-SKILL-patch.md` |
| `market-brief.skill` | Existing market-brief + E4 Step 5.5 cache reader | `E4-market-brief-SKILL-patch.md` |
| `daily-trade-rec.skill` | Existing daily-trade-rec + E4 cache-consumer block | `E4-daily-trade-rec-SKILL-patch.md` |
| `../system-review.skill` | Existing system-review minus `consolidate-memory` references (2026-04-17 follow-up) | `remove-consolidate-memory-skill.md` edits 2A/2B |

The .md patch files are retained as authoritative diff documentation and
rollback references. Either path (install .skill or paste .md) produces the
same final SKILL.md on disk.

**E1 still requires manual paste** — us-close-snapshot and workspace-tidy
are scheduled tasks (not skills), so the prepend blocks must be pasted into
`C:\Users\Lokis\Documents\Claude\Scheduled\*\SKILL.md` directly.


## Execution status (updated 2026-04-17 evening, post-install verification)

Sandbox grep of `/mnt/.claude/skills/` confirms same-day install of most items.

| Proposal | Status | Evidence / Next step |
|---|---|---|
| **A1** — positions-monitor scheduled task | ✅ **LIVE** | cron `0 9 * * 1-5`, next fire Mon 2026-04-20 09:00 UTC+8 |
| **A1** — positions-monitor user skill | ✅ **INSTALLED** | `/mnt/.claude/skills/positions-monitor/SKILL.md` present (92 lines) |
| **E4** — catalysts_cache helper script | ✅ **LIVE** | `/mnt/Trade/scripts/catalysts_cache.py` (tested) |
| **E4** — news-events writer integration | ✅ **INSTALLED** | `news-events/SKILL.md` contains `catalysts_cache` ref |
| **E4** — market-brief reader integration | ✅ **INSTALLED** | `market-brief/SKILL.md` contains `catalysts_cache` ref |
| **E4** — daily-trade-rec reader integration | ✅ **INSTALLED** | `daily-trade-rec/SKILL.md` contains `catalysts_cache` ref |
| **Follow-up** — system-review.skill (drop consolidate-memory refs) | ✅ **INSTALLED** | `system-review/SKILL.md` no longer references `consolidate-memory` |
| **Follow-up** — delete `consolidate-memory` skill folder | ✅ **DONE** (2026-04-17 15:27 UTC+8) | Folder deleted via File Explorer; skills dir count 18 → 17 confirmed |
| **E1** — us-close read-override prepend | ✅ **DONE** (2026-04-17 evening, via `apply-E1.bat`) | Verify token-drop on next fire Mon 2026-04-20 07:30 UTC+8 |
| **E1** — workspace-tidy read-override prepend | ✅ **DONE** (2026-04-17 evening, via `apply-E1.bat`) | Verify token-drop on next fire Sun 2026-04-19 21:00 UTC+8 |

**Net:** 10 of 10 applied. All that remains is passive verification via the next scheduled fires (Sun 21:00 workspace-tidy, Mon 07:30 us-close). If token-burn drops into the projected ranges, the system-review's efficiency proposals are fully landed.

## New patch — RM1 (2026-04-17 evening, residual-mom pipeline fix follow-up)

| File | What it installs | Status |
|---|---|---|
| `RM1-pipeline-recovery-SKILL-patch.md` | Adds Step 4f "Audit-addition variable drift check" + Step 5 CRITICAL escalation to Memory.md. Detects ≥2 consecutive MISSING rows in `audit-data-missing-tracker.md` per audit-addition variable. | ⬜ Pending manual paste into `pipeline-recovery\SKILL.md` |

**Why:** Phase A's task-level health check sees whether a file was written,
not whether its contents are usable. 2026-04-17 was a content failure
(staging file written, all 12 T-scores MISSING) that pipeline-recovery
couldn't see. With today's tracker plumbing the per-run LIVE/MISSING state
is now queryable; RM1 makes pipeline-recovery read it and escalate
drift ≥3 days to Memory.md.

**Related files already live (no patch needed):**
- `scripts/cache_manager.py` — schema stamping on bulk CSV writes + read-time signature verification
- `scripts/compute_audit_additions.py` — FF5 6-col tolerance, chain_attempts tracking, tracker-append
- `scripts/fetch_ff5_from_french_library.py` — Yahoo SPY+stocks fetcher, env-var-configurable DATA_DIR
- `scripts/preflight_health_check.py` — schema canary (`_check_data_contract`)
- `scripts/test_data_contract.py` — 26-test regression suite (all passing 2026-04-17)
- `audit-data-missing-tracker.md` — new uptime tracker feeding 2026-10-14 demote review

RM1 is the one remaining item that needs SKILL.md surgery, so it's a patch.

## One-click E1 launcher

`apply-E1.bat` (double-click) runs `apply-E1.ps1`, which:
- Locates `%USERPROFILE%\Documents\Claude\Scheduled\{task}\SKILL.md` for both tasks.
- Checks whether the prepend is already present (idempotent — safe to re-run).
- Makes a timestamped `.bak-YYYYMMDD-HHMMSS` backup of the original before modifying.
- Prepends the E1 block using UTF-8, no trailing newline.
- Reports `APPLIED` / `SKIPPED` / `FAILED` per task with colors.

Rollback = delete the prepend block at the top of the target file, or restore the `.bak-*` copy.

## Why six of eight are patches vs. live

The sandbox mount for `/sessions/gallant-vibrant-bardeen/mnt/.claude/skills/`
is `dr-x` (read-only). The Windows filesystem path
`C:\Users\Lokis\Documents\Claude\Scheduled\` is also not reachable from
the sandbox. The MCP can:
- Create new scheduled tasks (done for A1's cron).
- Update scheduled task prompts (but only by full replacement — the MCP does
  not return current prompt text, so a blind rewrite risks losing logic).

Therefore the chosen approach is:
- **A1 cron:** created directly (no existing logic to preserve).
- **A1 skill, E1, E4 SKILL patches:** delivered as minimally-invasive
  prepend/replace patches Gerald applies via a Windows text editor. This
  path is zero-risk — no existing logic is overwritten blindly.

## Apply order (suggested)

If Gerald applies in this order, each change is independently verifiable
before the next starts:

### 1. E1 — fastest win, lowest risk

```
open  C:\Users\Lokis\Documents\Claude\Scheduled\us-close-snapshot-730am-v2\SKILL.md
paste block from E1-us-close-snapshot-prepend.md at the top
save

open  C:\Users\Lokis\Documents\Claude\Scheduled\workspace-tidy-sunday-9pm\SKILL.md
paste block from E1-workspace-tidy-prepend.md at the top
save
```

**Verify after next fires:** us-close run token count drops from ~52K → ~12–20K;
workspace-tidy run drops from ~43K → ~8–14K. ~900K–1.3M tokens/month freed.

### 2. A1 — install user skill

```
create directory  C:\Users\Lokis\Documents\Claude\skills\positions-monitor\
copy  positions-monitor-SKILL.md  →  C:\Users\Lokis\Documents\Claude\skills\positions-monitor\SKILL.md
```

**Scheduled version is already live** — fires Mon 2026-04-20 09:00 UTC+8. The
skill file enables on-demand invocation via phrases like "check positions",
"monitor book", "portfolio heat".

### 3. E4 — catalysts cache integration

Helper script is already live and tested at `/mnt/Trade/scripts/catalysts_cache.py`.
Three SKILL.md edits remain:

```
open  C:\Users\Lokis\Documents\Claude\skills\news-events\SKILL.md
append Section 4 from E4-news-events-SKILL-patch.md
save

open  C:\Users\Lokis\Documents\Claude\skills\market-brief\SKILL.md
replace §5 Catalyst calendar with block from E4-market-brief-SKILL-patch.md
save

open  C:\Users\Lokis\Documents\Claude\skills\daily-trade-rec\SKILL.md
replace §5 / §8 catalyst handling with block from E4-daily-trade-rec-SKILL-patch.md
save
```

**Verify after next pipeline run:** news-2026-04-18 footer contains "Catalysts
cache written: N events"; `catalysts-cache-2026-04-18.json` exists; brief and
trade-rec reference it in their sources. ~80–120K tokens/month freed.

## Rollback

All three proposals are pure prepends or clearly-demarcated block replacements.
To roll back any change:
- E1: delete the prepend block at the top of the target task file.
- A1 skill: delete the skill directory.
- A1 cron: disable via `mcp__scheduled-tasks__update_scheduled_task` with `enabled: false`.
- E4: delete the added Section 4 from news-events; revert the brief/rec blocks to their prior narrative.

## Expected cumulative effect

| Source | Tokens/month saved |
|---|---|
| E1 (us-close + workspace-tidy) | +780K–1,300K |
| E4 (shared catalysts cache) | +80K–120K |
| A1 (positions-monitor new burn) | −220K |
| **Net freed for trade-rec context budget** | **+640K to +1,200K** |

Aligned with the system-review's efficiency-HIGH tally. Monthly burn projected
to drop from ~3.94M → ~2.7–3.3M.
