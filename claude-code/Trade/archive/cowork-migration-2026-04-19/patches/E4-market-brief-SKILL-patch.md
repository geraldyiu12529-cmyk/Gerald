# E4 Patch — market-brief SKILL.md (cache consumer)

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\market-brief\SKILL.md`

**Action:** Modify the catalyst-calendar section (currently §5 or equivalent) to READ the cache instead of restating the calendar. Remove the 12-row narrative catalyst table; replace with the helper-rendered table.

**Estimated savings:** ~2–4K tokens/run × 22 runs/month = ~44–88K tokens/month.

---

## Replace your current catalyst-calendar section with this

```markdown
## §5 — Catalyst calendar (next 30 days)

Read from the shared cache written by news-events:

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from catalysts_cache import read_catalysts, to_markdown_table, filter_severity

try:
    cache = read_catalysts()  # latest within 3 days
    # Show only severity >= med in the brief (critical/high/med, not low)
    visible = filter_severity(cache, 'med')
    cache_filtered = {**cache, 'catalysts': visible}
    table_md = to_markdown_table(cache_filtered, limit=15)
    cache_date = cache['date']
    cache_count = cache['count']
except FileNotFoundError:
    table_md = "_Catalyst cache missing — news-events may have failed. Falling back to inline extraction below._"
    cache_date = None
    cache_count = 0
```

Render in the brief as:
```markdown
**Catalyst window (next 30d, severity ≥ med, source: catalysts-cache-{cache_date}.json, {cache_count} total events):**

{table_md}
```

**Rules:**
- Do NOT re-narrate catalysts in prose that are already in the cache table.
- If the cache is missing (FileNotFoundError), fall back to pulling from
  the latest news-events file via existing extraction logic, AND flag this
  as a Data-Quality row in the Excel sync (`DataQuality` sheet:
  `catalysts_cache=MISSING`).
- The brief's regime-scoring step §4 should still read the full cache
  (not the filtered view) for Iran-binary / FOMC / earnings-cluster scoring
  inputs — use `read_catalysts()` directly where needed.
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\skills\market-brief\SKILL.md`.
2. Find the existing catalyst-calendar section (usually labelled §5 or "Catalyst calendar" or similar).
3. Replace the narrative-restatement block with the code block above.
4. Keep any surrounding context (section headers, introductory sentences) that aren't about restating the calendar itself.
5. Save.

## Verification

After next brief fire (2026-04-17 20:00 UTC+8):
- `market-brief-2026-04-17.md §5` renders the catalyst table via the helper.
- Footer cites `catalysts-cache-2026-04-17.json` as the source.
- Brief token count drops by ~2–4K vs. prior day.

If the cache isn't present (news-events failed earlier), brief falls back and flags Data Quality — no silent-carry-forward of yesterday's calendar.
