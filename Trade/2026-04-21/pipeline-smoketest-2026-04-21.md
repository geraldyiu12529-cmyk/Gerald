# Pipeline Smoke Test — 2026-04-21 (UTC+8)

> **Revision note:** initial report had two false-positive FAILs due to smoketest bugs (cwd drift and no mock-detection). Corrected below. Real finding is a workspace-canonicalization issue, not a pipeline break.

## Workspace anchor
All OK. pwd = `Trade/`; all 5 anchor files/dirs present. `pipeline/.pipeline-status.json` mtime 2026-04-20 20:48.

## Skills (11 expected)
All 11 SKILL.md files on disk load with valid frontmatter. `test_write` listed in the skill spec but not present — low-priority spec/reality drift; either restore or remove from expected list. `pipeline-smoketest` itself is new (installed 2026-04-21).

## Scheduled tasks (20 expected + 1 orphan)
All 20 expected tasks registered and enabled (two `*-2026-*` one-times are disabled-as-intended). Cadences mostly OK. Notes:
- `weekly-regime-signal-review`: no `lastRunAt` recorded — next run Sun 04-26; verify after it fires.
- `cwd-smoke-test` (one-time, disabled, last ran 04-21 02:57): orphan leftover, safe to delete.

## Pipeline chain — date checked: 2026-04-20 (canonical `Trade/` tree)

| # | Producer → File | Status | Notes |
|---|---|---|---|
| 1 | preflight-audit-data → `audit-data-staging-2026-04-20.md` | ✓ | |
| 2 | preflight-meta-additions → `meta-additions-staging-2026-04-20.md` | ✓ | |
| 3a | news-events-daily → `news-2026-04-20.md` | ⚠ MOCK | file header: `**[MOCK — TEST RUN 2026-04-20]**`. mtime 13:26, not 20:10 as claimed. |
| 3b | news-events-daily → `.catalysts-cache/catalysts-cache-2026-04-20.json` | ✗ MISSING | news file claims "cache written ✅" but Step 10 never executed in this tree — the ✅ is model-fabricated text, not a real write confirmation. |
| 4 | daily-market-brief-8pm → `market-brief-2026-04-20.md` | ✓ | content quality not audited |
| 5 | cloud-market-brief-6pm → `cloud-market-brief-2026-04-20.md` | ✓ | |
| 6 | cloud-news-events-630pm → `cloud-news-2026-04-20.md` | ✓ | |
| 7 | cloud-trade-rec-7pm → `cloud-trade-rec-2026-04-20.md` | ✓ | |
| 8a | trade-rec-daily → `trade-rec-2026-04-20.md` | ✓ | |
| 8b | trade-rec-daily → `report-2026-04-20-trade-rec.html` | ✓ | (earlier report said ✗ — **smoketest bug**, shell cwd had drifted to `T.system/` parent; file exists at 5.3KB) |
| 9 | pipeline-recovery-daily → status.json update | ✓ | no recovery log (silent-OK) |
| 10 | positions-monitor → `positions-monitor-2026-04-20.md` | ✓ | |
| 11 | us-close-snapshot → `us-close-snapshot-2026-04-20.md` | ✓ | |
| 12 | slack-ingest → `slack-digest-2026-04-20.md` | ✓ | |

## Workspace split — the real finding

There are **two parallel Trade trees**, both receiving active writes:

| Tree | Evidence |
|---|---|
| `Trade/` (repo root, canonical per skill spec) | Contains mock/test artifacts for 04-20 (e.g. news-2026-04-20 has `[MOCK — TEST RUN]` header). No real catalyst cache written since 04-17. |
| `cowork/Gerald/Trade/` (separate nested git repo) | Contains REAL production artifacts: news-2026-04-20.md at 20:07 with real content, catalyst cache at 20:07, independent commit history. Latest commit: `3b29df4 routine: trade-rec 2026-04-20 (manual recovery) + 2026-04-21 (abort)`. |

Git history shows the intent:
- `b3d69be tidy: separate Claude Code and Cowork workspaces`
- `191c08b revert: restore Trade/ at repo root, keep cowork/ separation`

So canonical `Trade/` was restored at repo root, but **scheduled tasks are still firing production writes into `cowork/Gerald/Trade/`**. The `Trade/` tree has test/mock content from the restore and has not received a real pipeline run.

User confirmed trade-rec-daily is running now with zero aborts — that run is happening in `cowork/Gerald/Trade/`, not in `Trade/`.

## Excel + Memory.md (canonical tree)
10 sheets present. AuditAdditionLog max date 2026-04-17 (2 weekdays stale vs expected 04-20) — consistent with the workspace split: no real preflight has written into this tree since the restore. framework/Memory.md has §2/§5/§6 headers ✓.

## Path consistency
All clean (only self-reference in smoketest skill).

## Summary

- Pass: ~22
- Warn: 2 (weekly-review never-run lastRunAt; `test_write` skill spec/reality drift)
- Fail: 0 real pipeline failures
- Blocker: **1 workspace-canonicalization decision needed** — which tree is production going forward?

## Action items

### Decision needed (user)
**Pick the production target — `Trade/` or `cowork/Gerald/Trade/`.** Then either:
- **(A) Keep `Trade/` canonical**: repoint every scheduled task's cwd from `cowork/Gerald/Trade/` to `Trade/`; cold-start the pipeline there; retire cowork/Gerald/Trade or archive it. Accept that today's real 04-20 outputs live in cowork and need a one-time sync.
- **(B) Keep `cowork/Gerald/Trade/` canonical**: update the smoketest (and any other skills) that assert `pwd ends with /Trade`; point future sessions there; delete or relocate the mock artifacts in repo-root `Trade/`.

### Low-priority cleanup (independent of decision)
- Delete disabled orphan scheduled task `cwd-smoke-test`.
- Resolve `test_write` — restore the skill or remove it from the expected-11 list.
- (Smoketest skill itself patched in this session — see below.)

## Smoketest skill bugs fixed in this pass
1. Added `pwd` anchor hard-fail (Step 1 now exits on cwd drift instead of continuing with broken globs).
2. Added Step 4 enhancement: detect `[MOCK` / `[TEST` header prefixes in dated outputs and flag them.
3. Added Step 4 enhancement: cross-check news-events cache-write claim against actual file presence.
4. Step 4 file checks now use explicit `Trade/{date}/...` paths.

Smoketest 2026-04-21 complete — pass=22, warn=2, fail=0, blocker=1. Report: 2026-04-21/pipeline-smoketest-2026-04-21.md
