---
name: test-smoke
description: Smoke test of scaffold. Use when Gerald says "{{TRIGGER_PHRASE_1}}", "{{TRIGGER_PHRASE_2}}", or "{{TRIGGER_PHRASE_3}}". Not for {{ANTI_TRIGGER}}.
model: sonnet
---

# Test Smoke

{{ONE_PARAGRAPH_PURPOSE}}

---

## When to use this skill

- {{TRIGGER_CONTEXT_1}}
- {{TRIGGER_CONTEXT_2}}
- {{TRIGGER_CONTEXT_3}}

## When NOT to use this skill

- {{ANTI_TRIGGER_CONTEXT_1}}
- {{ANTI_TRIGGER_CONTEXT_2}}

---

## Inputs

List the files/data this skill reads:

- `/mnt/Trade/...` — {{WHY_NEEDED}}
- `/mnt/.auto-memory/...` — {{WHY_NEEDED}}

## Outputs

List the files this skill produces:

- `/mnt/Trade/...` — {{DESCRIPTION}}

---

## Workflow

Describe the workflow step-by-step. Be specific about decision points and fail-loud conditions.

### Step 1 — {{STEP_NAME}}

{{STEP_DETAIL}}

### Step 2 — {{STEP_NAME}}

{{STEP_DETAIL}}

---

## Evidence discipline

Cite evidence grades (A/B/C) on any variable referenced. Never pad with Grade C. Fail-loud on MISSING Grade A.

## Memory protocol

Update `/mnt/Trade/Memory.md` immediately on state changes relevant to this skill. Also update `/mnt/.auto-memory/` where the change is cross-session-meaningful.
