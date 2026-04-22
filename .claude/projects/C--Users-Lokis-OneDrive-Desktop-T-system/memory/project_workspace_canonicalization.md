---
name: Workspace Canonicalization (Trade vs cowork/Gerald/cloud-sync)
description: Canonical for Claude Code is T.system/Trade/. cowork/Gerald/cloud-sync/ is the renamed Cowork mirror — dormant, no active writes.
type: project
originSessionId: aea21653-0a12-4a50-b238-2a95c1b7aaff
---
Two trees live under `T.system/`:

- **`T.system/Trade/`** — canonical. All local sessions, local skills (`.claude/skills/*`), all 23 scheduled-tasks MCP tasks operate here. Single source of truth.
- **`cowork/Gerald/cloud-sync/`** — renamed from `cowork/Gerald/Trade/` on 2026-04-21 (Gerald's instruction). This is the old Cowork platform mirror. No active writes — all cloud tasks (cloud-market-brief-6pm, cloud-trade-rec-7pm, etc.) now anchor to `T.system/Trade/`. Retained as archive/reference only. Has its own nested .git repo.

**Why renamed:** Gerald confirmed nothing runs through cowork/Gerald/Trade — all 23 scheduled tasks have hard-abort guards anchoring to T.system/Trade/. The old name was misleading.

**How to apply:**
- Claude Code sessions operate only in `T.system/Trade/`. Never write to `cowork/Gerald/cloud-sync/`.
- Divergence between the two trees is expected and irrelevant — cloud-sync is a frozen snapshot (as of ~2026-04-20).
- If Cowork platform ever resumes writes, it would need to be reconfigured to the new folder name before any sync could occur.
- `.claude` directories: only two remain — `T.system/.claude` (root config) and `T.system/Trade/.claude` (workspace config). 21 stale git worktrees were pruned 2026-04-21.
