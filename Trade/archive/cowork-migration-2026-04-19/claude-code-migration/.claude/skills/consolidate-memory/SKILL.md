---
name: consolidate-memory
description: "Reflective pass over memory files — merge duplicates, fix stale facts, prune index."
model: haiku
allowed-tools: Read Write Edit Grep Glob
---

# Memory Consolidation

## Phase 1 — Take stock
List memory directory, read index (MEMORY.md), skim each topic file. Note overlaps, stale entries, thin files.

## Phase 2 — Consolidate
- Separate durable (preferences, style, relationships) from dated (specific deadlines, one-off tasks)
- Merge overlapping files, keep richer path
- Convert relative dates to absolute
- Drop what's easy to re-derive from files/tools

## Phase 3 — Tidy index
Keep MEMORY.md under 200 lines / 25KB. One line per entry, <150 chars: `- [Title](file.md) — hook`.
