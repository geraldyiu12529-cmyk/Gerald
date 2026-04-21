---
name: asset-universe-update
description: Update the trading asset universe across all skills, tasks, and framework files in one operation. Accepts the new canonical universe as input and patches every file that declares or uses it.
---

**Workspace anchor (run FIRST):**

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade" || { echo "FAIL: T.system/Trade/ not found. Aborting."; exit 1; }
pwd | grep -qE '/T[.]system/Trade$' || { echo "FAIL: cwd is $(pwd)"; exit 1; }
```

---

## How to invoke

Call this skill with the new universe in natural language, for example:

> "Update universe: remove PYPL, add HOOD and COIN"
> "Remove FX entirely from the universe"
> "Add NVDM to equities"

The skill reads the CANONICAL UNIVERSE block below, applies the requested change, then propagates the updated universe to every downstream file.

---

## CANONICAL UNIVERSE (update this block when universe changes)

```
CRYPTO:     BTC, ETH
EQUITIES:   INTC, TSM, NVDA, TSLA, AAPL, GOOGL, AMZN, META, PYPL, PLTR, MU, WDC, AVGO, BABA, MSFT
ETFS:       QQQ, SPY, EWJ, EWY
COMMODITIES: Brent, WTI, Gold, Silver, Copper, Palladium, Platinum
FX:         (none — not trading FX)
```

**Equity short-list (single-stock scoring skills, slash-separated):**
`NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC/AVGO/BABA/MSFT`

**Python fetch-list (market-brief SKILL.md data pull block):**
`'NVDA', 'TSLA', 'AAPL', 'GOOGL', 'AMZN', 'META', 'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL', 'AVGO', 'BABA', 'MSFT',`

---

## STEP 1 — Parse the requested change

From the invocation input, determine:
- **Add:** tickers to add, and which asset class (crypto / equity / ETF / commodity)
- **Remove:** tickers to remove
- **Class changes:** any asset class being added or removed entirely (e.g., "remove FX")

Apply the change to the CANONICAL UNIVERSE block above to produce the **updated universe**. Confirm the delta with a one-line summary before proceeding:
```
Universe delta: ADD [X, Y] to equities | REMOVE [Z] | FX removed entirely
Updated equities: INTC, TSM, ...
```

Do not proceed if the requested change is ambiguous — ask for clarification on the asset class.

---

## STEP 2 — Build the target file list

Read each of the following files. Identify all locations where the asset universe is declared or used (equity lists, FX lines, scorecard loops, data-pull arrays):

**Framework (canonical — update first):**
1. `framework/Methodology Prompt.md` — §0 Asset Universe, §3 Minimal Dashboard
2. `.claude/CLAUDE.md` — Asset Universe line

**Local skills** (read each from `Trade/.claude/skills/`):
3. `market-brief/SKILL.md` — Python fetch array lines
4. `daily-trade-rec/SKILL.md` — universe references, single-stock slash-list
5. `news-events/SKILL.md` — Universe: line in Step 5
6. `positions-monitor/SKILL.md` — if equity list present
7. `signal-review/SKILL.md` — if equity list present
8. `trade-update/SKILL.md` — if equity list present

**Scheduled tasks** (read each from `~/.claude/scheduled-tasks/`):
9. `cloud-market-brief/SKILL.md` — asset universe header, STEP 2 pull list, single-stock slash-list
10. `cloud-market-brief-6pm/SKILL.md` — same
11. `cloud-trade-rec-7pm/SKILL.md` — if universe present
12. `us-close-snapshot/SKILL.md` — equity earnings universe line
13. `slack-ingest/SKILL.md` — single-stock slash-list, S/T/R methodology sections
14. `preflight-audit-data/SKILL.md` — if equity list present
15. `preflight-meta-additions/SKILL.md` — if equity list present
16. `news-events-daily/SKILL.md` — if equity list present
17. `weekly-regime-signal-review/SKILL.md` — if equity list present

For each file, record: file path, line numbers of universe declarations, current text.

---

## STEP 3 — Apply changes

For every location identified in Step 2, apply these replacement rules derived from the updated universe:

### Rule A — Comma-separated equity list (plain text)
Match: any line containing 3+ equity tickers from the current list with comma separation.
Replace: with the updated equity list, same format.

Pattern examples that must be updated:
- `Equities: INTC, TSM, NVDA, ...`
- `universe (INTC, TSM, NVDA, ...)`
- `Universe: INTC, TSM, ...`

### Rule B — Space-separated equity list (data-pull style)
Match: `INTC TSM NVDA TSLA ...` (space-separated, typically in STEP 2 data pull sections)
Replace: with updated space-separated list.

### Rule C — Python string list
Match: lines like `'INTC', 'TSM', 'MU', 'WDC', 'PLTR', 'PYPL',`
Replace: with updated Python list maintaining quote and comma style.

### Rule D — Slash-separated single-stock list
Match: `NVDA/TSLA/AAPL/GOOGL/AMZN/META/TSM/INTC/MU/PYPL/PLTR/WDC/...`
Replace: with updated slash-separated list (equities only, no ETFs/commodities/crypto).

### Rule E — FX asset class block
If FX is being REMOVED:
- Remove any `FX: EURUSD, USDJPY` or `FX: {tickers}` universe declaration lines
- Remove `- FX: carry, REER/PPP gap` from S-score scoring sections
- Remove `- FX: carry differential, REER/PPP gap` from scoring sections
- Change `Indices/ETFs/commodities/FX/crypto:` → `Indices/ETFs/commodities/crypto:` in T-score sections
- Change `equities, commodities, FX longs` → `equities and commodities` in R-overlay descriptions
- Remove V015 (FX interest-rate differential) and V016 (FX real valuation/PPP) from any variable monitoring lists
- Change `impact on commodities/FX` → `impact on commodities` in table templates

If FX is being ADDED: reverse the above.

### Rule F — Minimal Dashboard in Methodology Prompt.md
If FX is present in new universe: ensure `**FX:** Carry, REER/PPP gap, trend, CFTC positioning, risk reversals` exists in §3 Minimal Dashboard.
If FX absent: remove that line from §3.

### Rule G — Crypto additions/removals
If crypto tickers added/removed: update `Crypto: BTC, ETH` lines accordingly.

---

## STEP 4 — Apply and verify

For each file, make the edits. After each file, re-read the changed lines and confirm:
- No old ticker remains where it shouldn't
- No new ticker is missing
- No formatting broken (commas, quotes, slashes consistent)

Output per file:
```
✓ framework/Methodology Prompt.md — §0 universe updated, §3 dashboard updated
✓ .claude/CLAUDE.md — universe line updated
✓ cloud-market-brief/SKILL.md — header, pull list, slash-list updated
...
✗ signal-review/SKILL.md — no universe declaration found (skip)
```

---

## STEP 5 — Update the CANONICAL UNIVERSE block in this file

After successfully propagating the change, update the CANONICAL UNIVERSE block at the top of this SKILL.md to reflect the new state. This file is the single source of truth for future updates.

Edit `Trade/.claude/skills/asset-universe-update/SKILL.md`:
- Update the CRYPTO / EQUITIES / ETFS / COMMODITIES / FX lines
- Update the Equity short-list (slash-separated)
- Update the Python fetch-list

---

## STEP 6 — Update methodology-sync CHECK H

The methodology-sync skill at `Trade/.claude/skills/methodology-sync/SKILL.md` contains a CHECK H section for universe compliance. After this update, verify CHECK H reflects the new canonical universe. If it doesn't, update it.

---

## STEP 7 — Commit

```bash
cd "$HOME/OneDrive/Desktop/T.system/Trade"
git add -A
git commit -m "feat: update asset universe — {one-line summary of changes}"
```

Output exit line:
```
Asset universe update complete — {delta summary} — {N} files patched — committed.
```

---

## Scope rules (do not touch)

- **Archive folders** (`Trade/archive/`, `cowork/Gerald/cloud-sync/archive/`) — never update; these are frozen snapshots.
- **AppData sessions cache** (`AppData/Roaming/Claude/local-agent-mode-sessions/`) — skip.
- **Comments or examples** referencing old tickers in non-universe contexts (e.g., a worked example in a doc) — skip unless it's a live scorecard template.
- **methodology-audit-6mo-review** and **meta-shadow-review** tasks — no universe references; skip.
