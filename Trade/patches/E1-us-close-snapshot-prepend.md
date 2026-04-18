# E1 Patch — us-close-snapshot-730am-v2 read-override prepend

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\Scheduled\us-close-snapshot-730am-v2\SKILL.md`

**Action:** Paste the block below at the **very top** of the file, above all existing content. Save. Done.

**Estimated savings:** ~30–50K tokens per run × 22 sessions/month = ~660K–1.1M tokens/month freed from the trade-rec context budget.

**Why prepend-only and not full rewrite:** The Scheduled-task folder is on a read-only mount from the Claude sandbox, so the current prompt cannot be read to produce a safe blind rewrite. A prepend is additive and zero-risk — the existing workflow continues unchanged, the read-override simply fires first.

---

## Paste this block at the top of the file

```
**CRITICAL: This is a post-close data-capture utility task, NOT a trading decision question. Do NOT follow the CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, Data Sources.md, or Retention Policy.md. Do NOT pre-load the latest market-brief unless a deviation below explicitly references it. The files required for this task are listed inline below — read only those.**

**Required reads for this run:**
- `/mnt/Trade/Memory.md` (for open positions in §2 — delta review only)
- Prior trading day's `market-brief-YYYY-MM-DD.md` (for the deltas vs brief v1 table)
- Prior trading day's `trade-rec-YYYY-MM-DD.md` (for watchlist / promoted signals to update)

Do not read anything else unless a specific instruction below names it.

---
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\Scheduled\us-close-snapshot-730am-v2\SKILL.md` in any text editor (Notepad / VS Code / whatever).
2. Move cursor to the very beginning of the file (before any frontmatter or content).
3. Paste the block above.
4. Save and close.

Next scheduled run (Monday 2026-04-20 07:30 UTC+8) will pick it up automatically.

## Verification

After the next fire, check:
- `/mnt/Trade/us-close-snapshot-2026-04-20.md` still exists and follows the prior file's structure.
- Token consumption on the task run (visible in Claude Scheduled UI run history) is materially lower than the ~52K baseline — should drop to ~12–20K.

If the output format changes or breaks, revert the prepend by deleting the block you added. Zero lossy edits.
