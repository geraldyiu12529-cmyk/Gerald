# E4 Patch — daily-trade-rec SKILL.md (cache consumer)

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\daily-trade-rec\SKILL.md`

**Action:** Modify the catalyst sections (§5 "Catalyst proximity" / §8 "Pre-entry checklist catalyst row") to READ the cache instead of re-extracting from the news file. Remove prose restatement of the calendar.

**Estimated savings:** ~2–3K tokens/run × 22 runs/month = ~44–66K tokens/month.

---

## Replace catalyst-consumption logic with this

```markdown
## Catalyst input (replaces prior re-extraction from news-YYYY-MM-DD.md)

Read from the shared cache written by news-events:

```python
import sys; sys.path.insert(0, '/mnt/Trade/scripts')
from catalysts_cache import read_catalysts, filter_for_asset, filter_severity

try:
    cache = read_catalysts()  # latest within 3 days
    catalysts_all = cache['catalysts']
    # For scoring: only critical+high matter for C component
    catalysts_scoring = filter_severity(cache, 'high')
except FileNotFoundError:
    # Fallback: parse catalysts inline from news-YYYY-MM-DD.md (existing logic).
    # Flag this run's output footer with "catalysts_cache=MISSING — inline fallback".
    catalysts_all = []
    catalysts_scoring = []
    cache = None
```

**Downstream use:**

1. **Step 3 scoring (C component):** For each asset in the universe, pull its
   catalysts via `filter_for_asset(cache, ticker)`. If any catalyst falls
   within 0–3 days of today AND severity ≥ high, set C-contribution = +1
   (or −1 for bearish_risk direction_hint). Do not narrate the calendar —
   reference the cache file by name in the score justification.

2. **Step 5 checklist (per promoted signal):** Use `filter_for_asset()` to
   extract the catalyst row(s) relevant to the ticker. Render ONLY those
   rows in the pre-entry checklist "Catalyst proximity" line, not a general
   calendar.

3. **Step 8 narrative:** Do NOT restate the full catalyst list. If a
   binary-type catalyst is within 48h for a promoted asset, write one
   sentence about it with the source reference
   (`catalysts-cache-YYYY-MM-DD.json`).
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\skills\daily-trade-rec\SKILL.md`.
2. Find the current §5 / §8 blocks that re-extract or restate catalysts.
3. Replace the re-extraction logic with the code/narrative blocks above.
4. Preserve the overall 8-step framework structure; only the catalyst IO changes.
5. Save.

## Verification

After next trade-rec fire (2026-04-17 21:00 UTC+8):
- `trade-rec-2026-04-17.md` references `catalysts-cache-2026-04-17.json` in its footer sources.
- §5 / §8 narrative is shorter (no full-calendar restatement).
- trade-rec token count drops by ~2–3K vs. prior day.

If cache is missing:
- Footer reads `catalysts_cache=MISSING — inline fallback`.
- Behavior matches pre-E4 state.
- Signal about a broken news-events pipeline surfaces immediately.
