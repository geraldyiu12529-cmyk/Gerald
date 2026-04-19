# RM1 Patch — pipeline-recovery SKILL.md (audit-addition drift detection)

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\pipeline-recovery\SKILL.md`

**Why.** On 2026-04-17 the residual-momentum compute silently fell through
two defects and returned MISSING for all 12 single stocks. The surface symptom
was fine at task level (the staging file was written), so `pipeline-recovery`
didn't flag anything — but the *contents* were broken. We now log per-run
state to `/mnt/Trade/audit-data-missing-tracker.md`. This patch makes
pipeline-recovery read that tracker and flag **≥2 consecutive MISSING** rows
per audit-addition variable, so pipeline drift is caught within 48 hours,
not at the 2026-10-14 six-month review.

**Scope.** Variable-content drift detection — not new recovery actions. The
flag surfaces at the `notes` block in scheduled mode and as a WARNING/CRITICAL
escalation into Memory.md when the streak hits 3.

---

## Add a new Step 4f (between 4e and Step 5)

After the "4e. Excel sync integrity" section, insert this new subsection
*before* "Step 5 — Escalate consecutive failures":

```markdown
### 4f. Audit-addition variable drift check (Phase B only)

The task-level health check in Phase A only sees whether a file was written.
It can't see whether the *contents* are usable — a staging file with all
twelve single-stock T-scores reading MISSING is a task "success" but a
variable failure. This check catches that.

Read `/mnt/Trade/audit-data-missing-tracker.md`, pull the last 3 log rows
(or fewer if the file is new), and flag any audit-addition variable with
≥2 consecutive MISSING entries:

```python
from pathlib import Path

tracker = Path('/mnt/Trade/audit-data-missing-tracker.md')
drift_flags = []
if tracker.exists():
    content = tracker.read_text()
    # Pull the markdown-table rows (lines starting with "| 202")
    rows = [ln for ln in content.split('\n') if ln.startswith('| 202')]
    # Parse last 3 rows: [date, residmom, residmom_ok, intercap, basismom, basismom_ok, notes]
    parsed = []
    for ln in rows[-3:]:
        cells = [c.strip() for c in ln.split('|')[1:-1]]
        if len(cells) >= 6:
            parsed.append({
                'date': cells[0],
                'residmom': cells[1],
                'residmom_ok': cells[2],
                'intercap': cells[3],
                'basismom': cells[4],
                'basismom_ok': cells[5],
            })
    # Check each variable for consecutive MISSING
    for var, col in [('residual_momentum', 'residmom'),
                     ('intermediary_capital', 'intercap'),
                     ('basis_momentum', 'basismom')]:
        missing_streak = 0
        for r in reversed(parsed):
            if r[col] == 'MISSING':
                missing_streak += 1
            else:
                break
        if missing_streak >= 2:
            drift_flags.append({
                'variable': var,
                'streak': missing_streak,
                'level': 'CRITICAL' if missing_streak >= 3 else 'WARNING',
            })

if drift_flags:
    for flag in drift_flags:
        notes.append(
            f"{flag['variable']}: {flag['streak']} consecutive MISSING "
            f"({flag['level']})"
        )
        actions.append(f"Flagged {flag['variable']} drift — {flag['streak']}d MISSING")
```

**Escalation rule.** In Step 5, extend the CRITICAL escalation block to also
fire when any `drift_flags` entry has `level='CRITICAL'`. Append a Memory.md
entry like:

```markdown
### System Alert — {today}
AUDIT-ADDITION DRIFT: `{variable}` has been MISSING for {N} consecutive
compute runs. Pipeline task ran (staging file exists), but the variable
could not be produced. Likely causes: data-source shape drift, cache
schema mismatch, fetcher permissions, or the variable's source became
unreliable. Check `audit-data-missing-tracker.md` notes column for the
error tag from each run.
Action required: inspect `/mnt/Trade/audit-data-staging-{today}.md`'s
MISSING block and the staging file's "chain_attempts" subsection.
```

**Why 2-day threshold.** One MISSING day is often transient (source flaked,
Yahoo rate-limited, network blip). Two consecutive is the earliest signal
that a persistent issue has emerged. Three is the level for waking Gerald
up via Memory.md — matches the existing WARNING/CRITICAL threshold for
task-level consecutive failures.

**Why this lives here, not in preflight.** preflight_health_check runs
BEFORE the compute and can't know today's result. The tracker row is only
appended AFTER compute runs. pipeline-recovery at 22:00 is the first time
we have enough data to check the streak.
```

---

## Extend Step 5 escalation block

In "Step 5 — Escalate consecutive failures", after the existing `for each
level='CRITICAL'` block, add:

```python
# Audit-addition variable drift escalation (RM1, 2026-04-17)
for flag in drift_flags:
    if flag['level'] == 'CRITICAL':
        # Write a System Alert to Memory.md (same pattern as task-level CRITICAL)
        memory_path = Path('/mnt/Trade/Memory.md')
        alert = (
            f"\n### System Alert — {ps.today}\n"
            f"AUDIT-ADDITION DRIFT: `{flag['variable']}` has been MISSING "
            f"for {flag['streak']} consecutive compute runs. Pipeline task "
            f"ran (staging file exists), but the variable could not be "
            f"produced. Inspect `/mnt/Trade/audit-data-missing-tracker.md` "
            f"notes column and today's staging file's chain_attempts block.\n"
        )
        if memory_path.exists():
            existing = memory_path.read_text()
            if f"AUDIT-ADDITION DRIFT: `{flag['variable']}`" not in existing:
                with open(memory_path, 'a') as f:
                    f.write(alert)
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\skills\pipeline-recovery\SKILL.md`.
2. Locate "### 4e. Excel sync integrity (Phase B only)" and the following
   "---" separator before "## Step 5 — Escalate consecutive failures".
3. Insert the new "### 4f. Audit-addition variable drift check" block above
   *between* 4e and Step 5 (before the "---").
4. Find the `for each level='CRITICAL'` block inside Step 5 and append the
   drift-flag escalation code after the existing escalation code.
5. Save.

## Verification

**Happy path (today, 2026-04-17 22:00):** The tracker has one row dated
2026-04-17 with all variables LIVE. `drift_flags` should be empty.
`notes` unchanged. Phase A exits healthy.

**Simulate a drift flag (after patch):**

```bash
# From shell with access to /mnt/Trade/
python3 -c "
from pathlib import Path
p = Path('/mnt/Trade/audit-data-missing-tracker.md')
content = p.read_text()
# Append a test MISSING row for a fake prior date
test_rows = (
    '\n| 2026-04-14 | MISSING | 0/12 | LIVE | LIVE | 5/5 | test-drift |\n'
    '| 2026-04-15 | MISSING | 0/12 | LIVE | LIVE | 5/5 | test-drift |'
)
# Prepend before today's row to simulate history
# (then restore after test)
"
```

Run pipeline-recovery in interactive mode:
- `notes` should contain `residual_momentum: 2 consecutive MISSING (WARNING)`
- No Memory.md write (WARNING doesn't escalate)

Change both test rows' `residmom` to MISSING for 3 days in a row:
- `drift_flags[0]['level']` should be `'CRITICAL'`
- Memory.md should gain a `### System Alert — 2026-04-17` block with
  `AUDIT-ADDITION DRIFT: residual_momentum` in it

Remove the test rows after verification.

## Rollback

Remove the inserted 4f block and the drift-flag escalation code from Step 5.
No file-level dependencies — the check is additive and read-only against the
tracker.
