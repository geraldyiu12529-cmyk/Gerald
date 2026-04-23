---
name: SKILL.md description character limit
description: Anthropic's hard cap on the SKILL.md frontmatter `description` field and what it should contain
type: reference
originSessionId: 46b9a5ef-3b13-46fc-8fc6-eaf69fef5db2
---
Anthropic's Agent Skills spec caps the `description` frontmatter field at **1024 characters**. The `name` field is capped at 64 chars (lowercase/numbers/hyphens only, no reserved words "anthropic" or "claude"). Descriptions must be non-empty and cannot contain XML tags.

**Source:** <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices> (see "YAML Frontmatter" and "Technical notes" sections).

**Why it matters operationally:**
- Descriptions for *every* installed skill are preloaded into the system prompt on every session — this is the budget for skill activation discovery. Longer descriptions from other skills compete for context with conversation history and the current request.
- The Cowork UI truncates visible descriptions at ~500 chars with an ellipsis, but Claude sees the full field for matching. UI truncation is cosmetic, not a functional limit.
- Anthropic's own published example descriptions run 150–250 chars; skills with richer disambiguation/scheduled-task references may justifiably run 600–850.

**What the description must contain (per Anthropic best practices):**
- WHAT the skill does (brief, specific)
- WHEN Claude should use it (trigger phrases, contexts)
- Third-person voice ("Produces X" not "I can produce X")
- Specific key terms and trigger phrases for discoverability
- No XML tags (hard requirement)

**Gerald's workspace targets (set 2026-04-17):**
- Keep all custom skill descriptions ≤85% of limit (≤870 chars) to leave headroom for future trigger additions.
- Skills with many literal trigger phrases (e.g. trade-update at 26 phrases) may land higher — verify each phrase is still matched verbatim after any rewrite.
- Tightening pass applied 2026-04-17: see `/mnt/Trade/skill-description-tightening-2026-04-17.md`.
