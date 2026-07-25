# The run-of-show

Nine cards. Paste them in order. Each card holds the exact prompt, what it does,
what will be on screen, and what to say over it.

**Audience:** engineers who have never seen this repository. Most come from Cline
or a similar agentic IDE and already know what auto-approve feels like — and most
have turned it back off.

**The question the hour answers:**

> *What would have to be true about a codebase before you would let an agent run
> in it unsupervised, all night, on a system that moves money?*

---

## The cards

| # | Min | Card | What lands |
|---|---|---|---|
| — | 0–4 | *(no prompt — just the question)* | Why an agent demo starts with a payment file |
| **01** | 4–14 | [`01-tour.md`](01-tour.md) | **The agent explains your repo for you.** Proves it is self-documenting |
| **02** | 14–24 | [`02-legacy-run.md`](02-legacy-run.md) | A real batch crosses SFTP → Java → PostgreSQL. Evidence, not logs |
| **03** | 24–34 | [`03-who-lied.md`](03-who-lied.md) | One cent. Three implementations. **Refusal when evidence is withheld** |
| **04** | 34–40 | [`04-modern-today.md`](04-modern-today.md) | Four verticals. **The room spots the gap before you say it** |
| **05** | 40–44 | [`05-new-arrival.md`](05-new-arrival.md) | The spec arrives. *Is it adjudicatable?* — no oracle, no build |
| **06** | 44–46 | [`06-fab-translate.md`](06-fab-translate.md) | ★ **THE INVOCATION.** One line. Then you step back |
| — | 46–58 | *(you talk)* | The ladder, the loop, the six empty gates |
| **07** | *as needed* | [`07-nudge.md`](07-nudge.md) | Only if it drifts |
| **08** | 58–62 | [`08-verdict.md`](08-verdict.md) | The referee speaks, not the agent. The pull request |
| **09** | 62–65 | [`09-the-cents.md`](09-the-cents.md) | ★ **The close.** The machine found the cent and refused to fix it |

Cards 01–05 are conversation. Card 06 is the moment. Cards 08–09 are the payoff.

---

## Pre-flight — 15 minutes before doors

```bash
cd <worktree>
make clean CONFIRM=clean-runtime     # fresh runtime; batch IDs are immutable
make deploy                          # ~40s
make test-e2e TYPE=all               # ~3 min — produces the legacy observations
make df-accept TYPE=all              # ~30s — produces the findings
make modern-run TYPE=01              # ~60s — produces modern evidence for card 03

# REQUIRED. modern/landing/ survives `make clean`, and the Type 05 Parquet from
# before the deletion is still there. Leave it and the factory's first publish
# dies with "a different Parquet publication already exists for this batch".
# (written this way on purpose: in zsh an unmatched glob aborts the whole
#  command, so a bare `rm -rf .../.NW_*` would silently remove nothing)
for b in B202607230000401 B202607230000404 B200002290000402; do
  rm -rf "modern/landing/$b"
done
find modern/landing -maxdepth 1 -name '.NW_MERCHANT_FEES*' -exec rm -rf {} +
```

**Rehearsed 2026-07-25.** The factory built the modern Type 05 from this pack in
one pass: golden-match resolved, zero unexplained differences, and
`DF-SOURCE-005` classified `CONFIRMED_SOURCE_DEFECT` — computed `1.00` against
declared `0.99`. The build is on branch `rehearsal/type-05-modern` if you need
to cut to it.

Then **open a second shell and leave it clean.** Run the demo there so your setup
is not in scrollback.

Check these two things or the ending changes:

| Check | If it fails |
|---|---|
| `/fab` appears in a fresh Claude Code session | Card 06 has a plain-text fallback that works without the skill |
| `git push --dry-run origin HEAD` reports `[new branch]` | See below |

**The push path was broken and is now fixed.** The remote was `git@github.com:…`
over SSH, and this machine has no working key — `Permission denied (publickey)`.
`gh` is authenticated over **HTTPS** and its credential helper is already wired
for `https://github.com`, so the remote was switched:

```bash
git remote set-url origin https://github.com/luanmorenommaciel/uc-northwind-pay-edp.git
```

Verified 2026-07-25 with a dry-run push of both the demo branch and a
`factory/…` branch: both report `[new branch]`. Without this, card 08 ends at
commits and evidence rather than a pull request.

To go back to SSH: `git remote set-url origin git@github.com:luanmorenommaciel/uc-northwind-pay-edp.git`

Terminal: 16 pt minimum, dark background, ~100 columns. Nothing here needs more.

---

## Two things to say early, and mean

**On autonomy — say the number.**

> "Almost every autonomous-coding demo you have seen is **L3**: unattended, with
> guardrails. Nobody independent grades the result. The interesting rung is
> **L4 — adjudicated**, where an oracle you are forbidden to touch decides
> whether the work is right. That is the whole reason this repository builds the
> same system twice."

| | Level | Meaning |
|---|---|---|
| L1 | Suggest | It drafts. You apply |
| L2 | Assist | It patches. You approve each one |
| L3 | Unattended | It runs with guardrails. You review after |
| **L4** | **Adjudicated** | **An independent oracle decides if it is right** |
| **L5** | **Self-delivering** | Work order in, pull request out. Evidence for you to approve |

**On the risk — promise the failure, not the miracle.**

> "I do not know whether it gets this right first time. I hope it does not,
> honestly — because then you will see the part that matters."

A clean run proves the agent is capable. A caught defect plus a self-correction
proves the **system** is trustworthy. With HALF_UP rounding in play you have a
real chance of the better version.

---

## What not to claim

- **Not** "it deploys." There is no deployment target and `plans/modern.md`
  forbids claiming production- or CI-readiness from local proof. It runs until
  **every gate closes and the referee signs off.** Deployment is a decision a
  human makes with that evidence in hand.
- **Not** "the factory found a legacy defect." Zero. All five are source-system
  defects.
- **Not** "it translated the Java." Nothing is ported. It builds from the
  contract, and reading the old implementation is forbidden.
- **Not** "auto-allow is safe." The claim is narrower and truer: *auto-allow is
  exactly as safe as your gates are falsifiable.*

---

## If it stalls

| Symptom | Move |
|---|---|
| Docker unhealthy | `make deploy` — idempotent |
| Batch IDs collide | `make clean CONFIRM=clean-runtime && make deploy` (~4 min) |
| Detector says `DF-E-OBSERVATION-MISSING` | The e2e portfolio has not run on this runtime |
| Everything quarantines with `PRIVACY_VIOLATION` | `.env` not loaded — `set -a; . ./.env; set +a` |
| The build circles for more than ~4 minutes | Card 07. If that does not move it, say so plainly and cut to card 09 using the committed evidence |
| `a different Parquet publication already exists` | The pre-flight `rm -rf modern/landing/...` was skipped |
| dlt fails on `computed_detail_count` | A failed publish orphaned `modern/landing/.NW_*`. Remove it and re-run |

Errors on screen are fine and on-brand for this material. **A silent stall is
not.** An honest *"it is struggling, here is what it has done so far"* costs you
nothing.
