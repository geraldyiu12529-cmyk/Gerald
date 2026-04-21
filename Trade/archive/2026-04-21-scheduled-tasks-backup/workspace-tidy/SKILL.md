---
name: workspace-tidy
description: Sunday workspace tidy — retention policy, archive, diagnostics, cleanup log
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules, or protocol documents.

Apply the Retention Policy (read Retention Policy.md):
- Date-folder convention: dated outputs live under `{YYYY-MM-DD}/` (one folder per local date, UTC+8). Treat the entire folder as the retention unit — move the folder (not individual files) when it crosses a tier boundary.
- Move date folders aged 8+ days to `archive/YYYY-MM/{YYYY-MM-DD}/` (respecting Memory.md pinned files)
- Digest date folders aged 31+ days per the retention tiers
- Also sweep any legacy root-level dated files (`market-brief-*.md`, `news-*.md`, `trade-rec-*.md`, `us-close-snapshot-*.md`, etc.) that predate the folder convention — fold them into the corresponding `archive/YYYY-MM/{YYYY-MM-DD}/` bucket
- Never archive framework files: Methodology Prompt.md, Risk Rules.md, Data Sources.md, Coin core.md, Trad core.md, Memory.md, Retention Policy.md

Run workspace diagnostics:
1. Excel integrity — verify master-data-log.xlsx opens and has expected 10 sheets
2. Pipeline liveness — check .pipeline-status.json for any tasks with consecutive_failures > 0
3. Output continuity — confirm `*/market-brief-*.md`, `*/news-*.md`, and `*/trade-rec-*.md` exist for each of the past 5 weekdays (glob across date folders; fall back to root for any legacy runs still outside a date folder)
4. Cache health — check .data-cache/ for expired entries beyond staleness windows
5. Skill presence — confirm all 10 skill folders exist under .claude/skills/

Append a dated entry to archive/cleanup-log.md summarising: files archived, files digested, diagnostic results.

Then git add -A, commit with message "routine: workspace-tidy {today}", and push to origin main.