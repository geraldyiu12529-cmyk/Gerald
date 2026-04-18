---
name: Literature review 2026-04-17 — news-events taxonomy (scope-limited)
description: Semi-annual lit review run with variable-promotion OUT of scope; produced peer-reviewed 12-category news taxonomy, non-overlap rule with market-brief, source hierarchy, noise filters
type: project
---

## What ran

On 2026-04-17 Gerald directed the semi-annual literature-review skill to run with a specific scope restriction: news-and-events taxonomy only, NOT variable promotion. The goal was to improve the `news-events` skill and formalize non-overlap with the `market-brief` skill.

**Why:** The two daily skills (brief at 20:00 UTC+8, news at 20:10) were producing overlapping content — calendar lists, actual-vs-expected data, price records — creating duplicate maintenance and unclear authority.

**How to apply:** Future semi-annual reviews that want to scope narrowly should cite this precedent — write a scope-limited review file with explicit "OUT of scope" statement and no VariableRegistry writes. Next full-scope review is planned ~2026-10-17.

## Output deliverable

- `/mnt/Trade/literature-review-2026-04-17-news-events.md` — 35-validation-point taxonomy document, 12 categories with effect-size evidence, 3-tier source hierarchy, 10-rule noise filter, 4-criterion political-communication filter, proposed diffs for README.md and SKILL.md flagged "Gerald sign-off PENDING"
- Memory.md §9 updated with 5 deferred candidate flags for future quarterly review
- memory-lessons.md one-line summary appended

## Key design decisions

- **Non-overlap rule (§2 of the review file):** market-brief owns STATE (levels, regime, scorecard, 2w catalyst calendar); news-events owns CHANGE (actual-vs-expected surprise deltas, events, 48h tactical cut, flash events).
- **Data-release rule:** news captures surprise delta only; brief captures the resulting variable level one day later.
- **Calendar split rule:** brief §5 owns 2w rolling; news §3 owns 48h tactical cut only, no duplication.
- **Political-communication 4-criterion filter:** credibility + implementation power + asset-exposure precision + prior follow-through; all four must pass to surface as signal.
- **Source hierarchy:** Tier 1 primary/official, Tier 2 Reuters/AP low-bias wire + Bloomberg left-center (use for numeric data), Tier 3 aggregator/retail (Yahoo/TradingView/CoinDesk/Seeking Alpha) — only when Tier 1/2 unavailable.

## Deferred candidates (not promoted, 5 total)

1. Daily GPR (Caldara-Iacoviello) as Grade B regime input
2. EO-density-per-week as policy-uncertainty proxy
3. LLM-based sentiment (NLP-infra-blocked)
4. BTC-ETF-flow direction as BTC T-input (currently crowding-filter only)
5. Caldara-Iacoviello TPU subindex

All flagged for next quarterly methodology review (2026-07-01).

## Sign-off flow

Gerald approved 2026-04-17 ("Execute"). Status:

- `/mnt/Trade/news-events/README.md` — **APPLIED 2026-04-17.** New §Format (9 sections), §Scope (non-overlap matrix), §Source Hierarchy (3 tiers), §Noise Filters (10 rules), §Political-Communication Filter (4 criteria) all inserted.
- `/mnt/.claude/skills/news-events/SKILL.md` — **BLOCKED** (read-only fuse mount — skills directory is plugin-managed, not writable in Cowork session). Approved patch text saved to `/mnt/Trade/news-events-skill-md-patch-2026-04-17.md` for manual application via skill-creator, direct Windows-side edit, or plugin update.

**How to apply SKILL.md changes outside Cowork:** either (a) edit the file directly from Windows at the path shown in the fuse mount (`C:\Users\Lokis\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\skills-plugin\...\news-events\SKILL.md`), (b) run the skill-creator skill in a future session that has write access, or (c) distribute via plugin update.

Both the taxonomy file `§10` and the dedicated patch file contain the exact insertion text.

## Next literature review

Full scope (including variable-promotion) targeted ~2026-10-17.
