---
name: cloud-news-events-630pm
description: Cloud daily news capture — 6:30pm local (UTC+8), uploads to Google Drive + Slack notify
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` â that is a separate Cowork platform workspace.

---

Capture today's daily news (cloud edition — no local filesystem).

Today's local date = today in UTC+8. Use that as {YYYY-MM-DD}.

NO PREFLIGHT. NO pipeline-status write. NO git ops. NO pack_daily.

1. Run the `news-events` skill logic end-to-end using web search. Cover the full 12-category taxonomy:
   macro releases, central bank, geopolitics, equity earnings, crypto regulatory, commodity supply, FX policy, flash events, credit/rates, sector rotation, analyst revisions, overnight Asia.
   - Search by category (not by named conflict). Use the standard hotspot list.
   - Flag time-sensitive catalysts with asset / direction / date.
   - Output as markdown, canonical structure from the skill.

2. Write to `/tmp/news-{YYYY-MM-DD}.md`.

3. Upload to Google Drive using `mcp__fa60a538-6fb1-4c90-8c9b-8db7cba53dbc__create_file`:
   - filename: `news-{YYYY-MM-DD}.md`
   - Folder: `T.system-cloud` at Drive root (search first with `search_files`; create if missing).
   - Capture webViewLink.

4. Slack message to `#trading-scheduled-updates` via `slack_send_message` (resolve channel ID with `slack_search_channels` first):
   `Cloud news {YYYY-MM-DD} — {N} categories covered, {N} catalysts flagged. Drive: {webViewLink}`

5. Exit summary (one line):
   `Cloud news {YYYY-MM-DD} complete — {N} categories, {N} catalysts, drive_file_id={id}`