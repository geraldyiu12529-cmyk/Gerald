# E4 Patch — news-events SKILL.md (cache writer)

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\news-events\SKILL.md`
(or wherever the user-skill mount is rooted on Windows — the same directory `/mnt/.claude/skills/news-events/` mirrors from the sandbox side.)

**Action:** Insert the new Section 4 below, after the existing catalyst-collection narrative section. Do NOT remove any existing sections — this is additive.

**Why:** E4 from system-review-2026-04-17.md. Currently the catalyst calendar is duplicated 5 ways across news / brief / trade-rec / weekly-review / Memory. news-events is the natural owner (it already collects them). Writing a machine-readable cache lets the downstream producers read-and-render instead of re-narrating.

**Estimated savings:** ~80–120K tokens/month across brief + trade-rec + weekly-review combined.

---

## Add this section near the end of news-events SKILL.md, before "Triggers"

```markdown
## Section 4 — Write catalysts-cache-YYYY-MM-DD.json (NEW, E4)

After completing the category sweep and writing news-YYYY-MM-DD.md, extract
all dated catalysts from the narrative into a structured cache that brief,
trade-rec, weekly-review, and Memory sync consume downstream.

**Helper script:** `/mnt/Trade/scripts/catalysts_cache.py`
(implements write_catalysts, read_catalysts, filter_for_asset, to_markdown_table)

**Process:**

1. Extract from the news file each event with a known or estimable date
   within the next 30 days (earnings, central-bank decisions, geopolitical
   expiries, data releases, nominations, regulatory deadlines, etc.).

2. For each, build a dict:
   ```python
   {
     "date": "YYYY-MM-DD",                 # required
     "event": "short description",         # required
     "asset_impact": ["TICKER1", ...],     # required; uppercase
     "severity": "critical|high|med|low",  # required
     "direction_hint": "binary|bullish_risk|bearish_risk|bullish_safe_haven|bearish_safe_haven|neutral",
     "source": "news-YYYY-MM-DD.md §N",   # optional but recommended
     "notes": "any qualifier"             # optional
   }
   ```

3. Call the writer:
   ```python
   import sys; sys.path.insert(0, '/mnt/Trade/scripts')
   from catalysts_cache import write_catalysts
   write_catalysts('YYYY-MM-DD', catalysts_list, horizon_days=30)
   ```
   This writes both `/mnt/Trade/catalysts-cache-YYYY-MM-DD.json` (root, for
   easy globbing) and `/mnt/Trade/.catalysts-cache/catalysts-cache-YYYY-MM-DD.json`
   (stable cache dir).

4. Include a one-line confirmation in the news file tail:
   `*Catalysts cache written: N events, severity breakdown [crit:X, high:Y, med:Z].*`

**Rules:**
- strict=True by default. Bad inputs raise — fail-loud. If validation fails,
  the news file still writes (the cache is secondary), but the error is
  logged to the news file tail as `**Catalysts cache FAILED: <reason>**` so
  downstream producers know to fall back to inline parsing.
- Scope: only dated events. Do NOT include "sometime this quarter" or
  "awaiting announcement" items — those belong in the narrative.
- Re-runs on the same date overwrite (authoritative). The cache is a view,
  not an append-only log.

**Minimum viable output:** Even if only 1 catalyst is datable, write the
cache — downstream prefers an empty-but-fresh cache to a missing one.
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\skills\news-events\SKILL.md` in any text editor.
2. Scroll to just before the "Triggers" or final section.
3. Paste the section above.
4. Save.

Next news-events run (today 20:10 UTC+8) will begin writing the cache. Brief and trade-rec changes (see separate patches) will consume it from the next run onwards.

## Verification

After the next news-events fire, check:
- `/mnt/Trade/catalysts-cache-2026-04-17.json` exists.
- Opening it shows a sorted list with at least Iran ceasefire, FOMC, INTC earnings, GOOGL earnings.
- `python3 /mnt/Trade/scripts/catalysts_cache.py show` prints the payload.
- `python3 /mnt/Trade/scripts/catalysts_cache.py table` renders a markdown table.
