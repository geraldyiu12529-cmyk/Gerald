# News-Events SKILL.md — Approved Patch (2026-04-17)

**Status:** Gerald signed off 2026-04-17. Could not auto-apply — `/mnt/.claude/skills/` is mounted **read-only** in this session (plugin-managed directory). Apply via the plugin-edit path (skill-creator, direct edit outside Cowork, or plugin update).

**Target file:** `/mnt/.claude/skills/news-events/SKILL.md`

**Companion doc:** `literature-review-2026-04-17-news-events.md` §10 contains the evidence trail. This file is the ready-to-paste deliverable.

---

## Edit 1 — Insert Step 1.5 (after current Step 1, before current Step 2)

Insert immediately after the line `If the README is missing, stop and surface the gap.`:

```markdown
## Step 1.5 — Non-overlap check

Before searching, confirm what you will NOT capture because the market-brief owns it:

- Current variable levels (VIX, DXY, rates, prices) — brief §2 owns these
- Regime label and S/T/C/R scores — brief §1, §3
- 2-week rolling catalyst list — brief §5 (news §3 carries ONLY the 48h cut)
- Level milestones ("record high") mentioned without event-character — brief §2 carries the level; news surfaces the event-character only

For data releases, news captures the **surprise delta** (actual vs expected vs prior) only; the brief captures the resulting level the next day. Never restate a variable level in the news file.

See `news-events/README.md` §Scope — News vs Market Brief for the authoritative handoff matrix.
```

---

## Edit 2 — Update Step 2 header/opening (trade-sanctions split note)

Current §Step 2 header currently reads:
> Search by **category**, not by named conflict. Conflicts end, new ones begin.

Replace the Generic category searches list with the same list minus `trade war tariffs today` (which now lives in the trade/sanctions stream captured via §Step 4.5 / §Step 6 flows). Updated bullet list:

```markdown
**Generic category searches (always run):**
- `sanctions today`
- `military conflict today`
- `diplomatic crisis today`
- `territorial dispute today`
- `election crisis today`
- `regime change coup today`
- `naval incident today`
- `blockade embargo today`
```

(Tariff/trade-war searches migrate into the new central-bank/policy-communications section below; they are regulatory-action events, not geopolitical conflicts.)

---

## Edit 3 — Insert Step 4.5 — Central Bank & Policy Communications (new)

Insert after current Step 4 (Economic calendar — next 48h) and before current Step 5 (Corporate & tech):

```markdown
## Step 4.5 — Central bank & policy communications

Search:
- `{central bank} statement today` (Fed, ECB, BoJ, BoE, PBoC, RBA — as scheduled)
- `Fed Chair speech today`
- `Treasury Secretary statement today`
- `USTR statement today`
- `Congressional hearing on economy today`
- `executive order trade tariff today`

Apply the **4-criterion political-communication filter** (see README §Political-Communication Filter) before surfacing any political statement. Statements failing any one criterion are logged with `⟨noise-probable⟩` tag and do not drive regime repricing.

For FOMC decisions specifically, extract:
- Policy rate (actual vs prior)
- Dot-plot delta (median SEP shift)
- 2Y and 10Y yield reaction in the announcement window
- Fed-funds-futures surprise in bps (Kuttner 2001 identification)

For other principal statements (Treasury/USTR/WH), capture the specific asset/sector named and any implementation dates.
```

---

## Edit 4 — Insert Step 6.5 — Credit & Sovereign Events (new)

Insert after current Step 6 (Crypto & regulatory) and before current Step 7 (Flash / surprise events):

```markdown
## Step 6.5 — Credit & sovereign events

Search:
- `Moody's rating action today`
- `S&P Global rating action today`
- `Fitch rating action today`
- `sovereign credit downgrade today`
- `corporate default today`
- `bank stress regulatory action today`
- `CDS spread widening today`

For each action, capture: issuer, old rating, new rating, outlook change, and any primary-market impact visible. Note pre-announcement drift if detectable (BIS WP 207 — spreads typically widen 30–60 days ahead of actual downgrade).
```

---

## Edit 5 — Replace Step 8 output format with 9-section v2 structure

Replace the current Step 8 template block with:

```markdown
## Step 8 — Write the output file

Path: `/mnt/Trade/news-events/news-{YYYY-MM-DD}.md`

Use this format:

\`\`\`
# News & Events — YYYY-MM-DD (vN)

**Local:** HH:MM UTC+8 (HH:MM ET, US pre-open) — scheduled daily news capture[, vN refresh].

---

## 1. Geopolitics & Political Risk
[Items with source citations — exclude trade/tariffs, those belong in §6]

## 2. Macro Data Releases Today (YYYY-MM-DD)
[Actual vs expected vs prior ONLY — NOT levels. Brief owns the level next day.]

## 3. Economic Calendar — Next 48h
[48h cut ONLY; 2-week list lives in brief §5]
[Table: Date/Time ET | Event | Impact | Notes]

## 4. Corporate & Tech (Universe Only)
[EPS/rev/guide/margin + price reaction, universe tickers only]

## 5. Crypto & Regulatory
[ETF flows, SEC/CFTC/FinCEN enforcement, on-chain, CLARITY/GENIUS progress]

## 6. Central Bank & Policy Communications
[FOMC, ECB, BoJ, BoE, Fed speeches, Treasury/USTR — apply 4-criterion filter]

## 7. Credit & Sovereign Events
[Rating actions, CDS widening, defaults, bank stress]

## 8. Flash / Surprise Events
[Omit if none]

## 9. Regime Implications
[≤3 lines max: which items above actually shift regime readings in Memory.md, and which are noise. Handoff surface to brief.]
\`\`\`
```

---

## Edit 6 — Update Rules section

Append to the current Rules list:

```markdown
- Apply the **Tier 1/2/3 source hierarchy** per README §Source Hierarchy — prefer the highest tier that carries the fact. Do not cite Tier 3 when Tier 1/2 carries the same story (recycled-wire noise).
- Apply the **10-rule noise filter** per README §Noise Filters before surfacing any item.
- For political communications, apply the **4-criterion filter** per README §Political-Communication Filter. Items failing any criterion are tagged `⟨noise-probable⟩` and do not drive regime repricing.
- **Never restate a variable level** — the brief owns the level. News owns the surprise, the event-character, and the reaction.
- §2 is actual-vs-expected ONLY, not levels. §3 is the 48h cut ONLY, not the 2-week list.
- §9 Regime Implications remains mandatory (≤3 lines) — the handoff surface to the brief.
```

---

## Verification checklist after applying

- [ ] Step 1.5 inserted between current Step 1 and Step 2
- [ ] Step 2's category list no longer includes `trade war tariffs today`
- [ ] Step 4.5 inserted between Step 4 and Step 5
- [ ] Step 6.5 inserted between Step 6 and Step 7
- [ ] Step 8 template renumbered to 9 sections
- [ ] Rules section extended with 6 new rules
- [ ] Skill description frontmatter left unchanged (skill still triggers on the same phrases)
- [ ] Next scheduled `daily-news-events-810pm-v2` run produces the 9-section file under the new discipline

---

*Approved by Gerald 2026-04-17. Written to workspace because `/mnt/.claude/skills/` is read-only in Cowork sessions (plugin-managed). README.md edits were applied directly in-session.*
