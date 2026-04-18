---
name: Trade workspace layout
description: File locations for the methodology, research cores, working memory, and daily briefs
type: reference
---

All trading files live in `/mnt/Trade/`:

- `Methodology Prompt.md` — master 8-step framework, evidence grading, dashboard, top-25 variables, expression rules. Read first every session.
- `Trad core.md` — cross-asset factor literature review (equities, bonds, commodities, FX), ranked variables, decision framework.
- `Coin core.md` — BTC/crypto predictor families, long/short signal hierarchy, master variable table, research gaps.
- `Memory.md` — working memory: positions, watchlist, catalysts, closed trades. §3/§4/§10 removed (Excel only). §8 is a pointer to `memory-lessons.md`.
- `memory-lessons.md` — lessons & corrections log (split from Memory.md §8 on 2026-04-16). Trade-rec writes here; signal-review and weekly-regime-review read here.
- `market-brief-YYYY-MM-DD.md` — daily briefs. Read the most recent one at session start.

Session startup protocol (mandatory, from `/mnt/.claude/CLAUDE.md`):
1. Read `/mnt/.auto-memory/MEMORY.md` index + any relevant linked files.
2. Read `/mnt/Trade/Methodology Prompt.md`.
3. Read the latest `market-brief-*.md` in `/mnt/Trade/`.
4. Read `/mnt/Trade/Memory.md`.
