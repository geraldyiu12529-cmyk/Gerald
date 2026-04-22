---
name: pipeline-recovery-daily
description: Daily pipeline recovery check — Phase A triage, Phase B recovery if needed
---

**Workspace anchor (run FIRST, before any other work):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd), expected /T.system/Trade"; exit 1; }
```

Canonical workspace: `T.system/Trade/`. All relative paths resolve here. Do NOT write to `cowork/Gerald/...` — that is a separate Cowork platform workspace.

---

Run the pipeline-recovery skill to check today's pipeline health and recover from any upstream failures.

Ensure today's date folder exists before invoking the skill: `mkdir -p {YYYY-MM-DD}` (Phase B output artifacts go under the date folder).

/pipeline-recovery

The skill runs in two phases:
- Phase A: fast triage (<3K tokens). Reads .pipeline-status.json, checks file sizes against MIN_SIZES (globs `{YYYY-MM-DD}/market-brief-*.md`, `{YYYY-MM-DD}/news-*.md`, `{YYYY-MM-DD}/trade-rec-*.md` with root fallback for legacy runs), runs structural sniff on brief and trade-rec. If all healthy, print "Pipeline healthy. No recovery needed." and EXIT — do NOT write any files.
- Phase B: recovery (only if Phase A finds failures). Attempts cache-brief from Tier 3 data if market-brief failed (writes `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md`). Writes news skeleton `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` if news-events failed. Flags .recovery-pending if trade-rec aborted and brief was just recovered. Escalates to Memory.md §7 if consecutive_failures >= 5 for any task.

After the skill exits, pack §H into the consolidated daily file ONLY if Phase B ran (healthy Phase A writes nothing — consistent with the existing rule):
- Phase A+B (recovered):
  `python scripts/pack_daily.py --section H --content "Phase A+B — {one-line summary of files touched}" --status recovered`
- Phase A+B (unrecoverable):
  `python scripts/pack_daily.py --section H --content "Phase A+B — escalated to Memory.md §7 ({reason})" --status unrecoverable`
- Phase A-only (healthy): skip the pack step.

Commit + push ONLY if Phase B created or modified files. If Phase A was clean, no commit needed. (The §H pack is part of Phase B, so it is covered by the existing commit rule.)

Exit summary (one line):
`Pipeline recovery {YYYY-MM-DD} — phase={A-only|A+B}, status={healthy|recovered|unrecoverable}`