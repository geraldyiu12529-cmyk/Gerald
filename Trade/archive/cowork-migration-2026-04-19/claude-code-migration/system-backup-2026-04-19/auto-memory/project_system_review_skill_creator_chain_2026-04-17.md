---
name: System review → skill-creator chain (2026-04-17)
description: Scheduled task system-review-semi-annual updated 2026-04-17 to chain skill-creator for patch generation after verdicts; avoids ro-mount blocker and SKILL.md token bloat
type: project
originSessionId: f7a529e3-9b81-41a4-93a1-c5b246abfc5a
---
System-review-semi-annual scheduled task was updated on 2026-04-17 to chain the skill-creator skill after the main system-review run. Prior behavior: produced KEEP/MODIFY/MERGE/REMOVE verdicts and stopped. New behavior: for every MODIFY verdict against an existing skill or scheduled task, invoke skill-creator to write ONE patch file per target at `/mnt/Trade/patches/system-review-YYYY-MM-DD-{target-name}-patch.md`. Patches queue for Gerald to apply Windows-side — no direct SKILL.md edits.

**Why:** Gerald asked whether skill-creator could be embedded into higher-level skills (pipeline-recovery, literature-review, system-review) to add editing/fix capability. Analysis narrowed the fit to system-review only (already operates at architecture level). Two implementation paths considered: (a) patch each SKILL.md to embed the skill-creator invocation — blocked by ro mount and wastes tokens on every on-demand load; (b) chain at scheduled-task prompt level — no ro-mount issue, tokens loaded only when task fires. Picked (b).

**How to apply:**
- Next scheduled run: 2026-05-03 (first Sunday of May).
- On-demand runs of system-review do NOT get this chaining — if Gerald manually invokes "run system review" via the skill directly, he can invoke skill-creator separately. Gap accepted as minor given semi-annual cadence.
- If the ro mount becomes writable from sandbox, promote this chain from task-prompt-only into the system-review SKILL.md itself so both paths get it, and upgrade from "write patch" to "edit with diff + require Gerald approval" — never auto-apply.
- Guardrails in the task prompt: skill-creator must NOT edit SKILL.md files directly, must NOT touch the system-review skill itself, must record failures explicitly rather than silently dropping.

**Related memory:**
- `project_system_review_2026-04-17.md` — inaugural audit, 6 patches queued.
- `project_system_review_execution_2026-04-17.md` — patch-queue workflow precedent.
- `reference_skill_description_limit.md` — another patch sitting behind the ro-mount block.
