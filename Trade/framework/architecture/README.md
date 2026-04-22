# Architecture — Versioned History

This folder is the authoritative system-architecture record for T.system. It is **the heart of the operation**.

## Rules (binding)

1. **Files here are immutable once dated.** Never edit a versioned file in place.
2. **New changes = new file.** Name: `architecture-v{N}-{YYYY-MM-DD}.md`, N monotonically increasing.
3. **Every new version must declare:**
   - `**Prior version:**` — filename of the immediately previous version
   - `**Changes from v{N-1}:**` — bulleted diff (additions / modifications / removals, each with section reference)
4. **Latest = highest N.** Consumers read the file with the highest version number.
5. **Append-only folder.** Do not delete prior versions; they are the audit trail.

## Current

- **v6** — [architecture-v6-2026-04-22.md](architecture-v6-2026-04-22.md) — skill renamed methodology-sync → architecture-health throughout.
- **v5** — [architecture-v5-2026-04-22.md](architecture-v5-2026-04-22.md) — HypoLedger added as 11th Excel sheet; §5 daily-trade-rec + signal-review wiring updated; PerformanceStats now 14 dimensions.
- **v4** — [architecture-v4-2026-04-22.md](architecture-v4-2026-04-22.md) — skills path consolidated to `~/.claude/skills/`; `Trade/.claude/` deleted; cowork removed.
- **v3** — see file for prior changes.
- **v2** — [architecture-v2-2026-04-21.md](architecture-v2-2026-04-21.md) — adds §10 Current Variable Registry (Top-33 with grades) + §11 Grade Distribution & Review Cohorts.
- **v1** — [architecture-v1-2026-04-21.md](architecture-v1-2026-04-21.md) — initial versioned cut; consolidates prior `architecture.md`, `pipeline-dependency-graph.mermaid`, `routine-output-map.md`.

## Dashboard

- **[architecture-health.html](architecture-health.html)** — Live health dashboard: source status, pipeline, skills registry, structural risks, variable grades, execution timeline, Excel sheets, architecture versions. Open in browser for a visual overview.

## Cutting a new version

1. Copy the latest version to `architecture-v{N+1}-{today}.md`.
2. Update header: bump `**Version:**`, set `**Dated:**`, set `**Prior version:**` to the file you copied from.
3. Insert `**Changes from v{N}:**` block below the prior-version line.
4. Edit the body.
5. Add an entry to the "Current" section of this README (keep prior entries).
6. Commit.
