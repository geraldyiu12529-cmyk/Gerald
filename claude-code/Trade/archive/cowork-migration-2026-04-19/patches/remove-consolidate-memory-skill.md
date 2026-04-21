# Patch — Remove `consolidate-memory` skill (2026-04-17)

**Why:** Gerald: "there is no consolidate-memory skill. remove." Skill is defunct and should not be referenced anywhere in the live scaffold.

**Why sandbox-blocked:** `/mnt/.claude/skills/` is a read-only mount from the Cowork sandbox, so deletion and edits to SKILL.md files must happen Windows-side.

---

## Actions

### 1. Delete the skill folder

```
rmdir /s /q "C:\Users\Lokis\Documents\Claude\.claude\skills\consolidate-memory"
```

(Adjust path if the Claude skills root is elsewhere on Windows — it was mounted to the sandbox at `/mnt/.claude/skills/consolidate-memory/`.)

### 2. Patch `system-review/SKILL.md`

File: `.claude/skills/system-review/SKILL.md`

**Edit A — line 37 (bucket 6: Infrastructure).** Drop `consolidate-memory` from the parenthetical.

BEFORE:
```
6. **Infrastructure** — pipeline glue, recovery, archival, memory housekeeping (workspace-tidy, pipeline-recovery, consolidate-memory, us-close-snapshot)
```

AFTER:
```
6. **Infrastructure** — pipeline glue, recovery, archival, memory housekeeping (workspace-tidy, pipeline-recovery, us-close-snapshot)
```

**Edit B — line 186 (scope boundary list).** Delete the entire bullet; memory consolidation, if it happens at all, is now subsumed into `workspace-tidy-sunday-9pm` Phase 2.

BEFORE:
```
- Consolidate memory — `consolidate-memory` owns that
```

AFTER:
```
(remove line entirely)
```

---

## Verification after applying

From the sandbox, after Windows-side changes land:

```
ls /mnt/.claude/skills/ | grep -i consolidate       # should return nothing
grep -rn "consolidate-memory" /mnt/.claude/skills/  # should return nothing
```

## Already done (sandbox-side)

- `CLAUDE.md` — skills list no longer lists `consolidate-memory` (on-demand line now contains only `trade-update`).
- `/mnt/.auto-memory/` — grep confirmed no residual references.
