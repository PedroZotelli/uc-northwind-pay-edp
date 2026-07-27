---
name: fab
description: The Dark Factory floor. Verb-dispatched work on the NorthWind Pay estate — `translate` a docked specification into the modern stack autonomously, `retool` to inspect a docked kit, `status` for where every type stands, `audit` to check a run obeyed its mandate. Use when the user types /fab, or asks to run the factory, translate a spec, or modernize a file type.
---

# fab — the factory floor

Verb-dispatched. The first argument is the verb.

| Verb | Invocation | What it does |
|---|---|---|
| `translate` | `/fab translate spec/<kit>` | **Build the modern vertical for a docked specification. Autonomous, to a pull request.** |
| `retool` | `/fab retool 05` | Show the docked kit, the state of the line, and the work order |
| `status` | `/fab status` | Where every registered type stands, legacy vs modern |
| `audit` | `/fab audit` | Did the last run obey its mandate? Frozen paths, git archaeology |

If no verb is given, print this table and stop.

---

## `translate` — the autonomous build

**Autonomy level 5: self-delivering.** You take a work order and run to a pull
request. You do not ask for approval. You do not stop to confirm. The operator
has handed you the floor and walked away.

### Step 1 — Read the work order, and refuse if you must

Read every file in the docked kit. The work order and inventory are the entry
points; the numbered folders carry the specification, the raw inputs, the
sanitized outputs, the reconciliations, the refusals, one real legacy execution,
and the shape of the deliverable.

**Then apply the rule this repository rests on:**

> **No oracle, no build.** A specification that does not ship its expected
> outputs cannot be adjudicated.

If the kit carries no approved expected outputs, **stop and say so.** Do not
write a line of code. Refusing an unadjudicatable specification is the correct
outcome, not a failure.

### Step 2 — Confirm the ground truth is alive

Before trusting anything you build against it, prove the legacy side runs:

```bash
make run TYPE=<NN> SCENARIO=valid-minimal     # must succeed
make run TYPE=<NN> SCENARIO=DF-SOURCE-<NNN>   # must be refused
```

If the runtime is not deployed, `make deploy` first. If a batch was already
processed on this runtime, batch identities are immutable — say so rather than
working around it.

### Step 3 — Build the modern vertical

Work on a new branch: `factory/type-<NN>-modern`.

```
ingestion → canonical Parquet → dlt → DuckDB → dbt Bronze/Silver/Gold
    → golden-match → evidence
```

The already-modernized types are your pattern. Follow their conventions rather
than inventing new ones — five files per type (`model`, `parser`, `schema`,
`writer`, `handler`), Bronze detail plus Bronze control, Silver, Gold at the
legacy reporting grain, and dbt assertions tagged `type_<NN>`.

**An untagged dbt test silently never runs in a scoped build.** Tag everything.

You will also need to wire the type into: `modern/pipeline.py` (four maps),
`modern/lakehouse/dlt/registration.py`, `modern/serving/service.py`, and the dbt
`schema.yml` and `sources.yml` files. A new type is not only new code.

### Step 4 — Close the gates, then open the pull request

Commit in **small gate-passing increments.** Never leave the tree red between
commits.

Then open a pull request into `main` from your branch. The body must state:

- what you built, and roughly how many lines
- **the referee's verdict, quoted from `evidence/modern/<batch>/golden-match.json`** —
  not your own summary of whether tests passed
- the source-defect batch's classification
- anything you had to work out: a convention you inferred, a gate that proved
  nothing, a place an old type list was hardcoded
- anything you could not do, and why

---

## Build from the specification, never from the old implementation

You may read the legacy code to understand *behaviour*. You may not port it.

Porting reproduces the old implementation's defects and then reports the result
as parity. The entire value of a second implementation is that it did not see
the first one.

**Forbidden:** searching git history for a previous modern implementation of this
type. No `git log`, `git show`, `git diff`, or stash archaeology aimed at
recovering deleted code. Build from the contract.

**If you look anyway, say that you looked.** An honest report of a shortcut is
worth more than a clean result nobody can trust.

---

## Frozen — read freely, never write

```
legacy/     contracts/     gen/     infra/     applied migrations
```

**Never edit an expected value, fixture, or oracle to turn a red gate green.**
Green must come from the referee, not from moving the goalposts.

If a gate cannot pass without changing frozen truth, that is a **hard stop**.
Report it and wait.

---

## Halt immediately and report on

- a restricted value reaching any sanitized output, log, Parquet file, or
  evidence artifact
- any write to a frozen path
- a gate that cannot pass without changing frozen truth
- Docker or the database unavailable

Halting is a first-class outcome. A system that always finishes will eventually
finish wrongly.

---

## The loop

| | |
|---|---|
| **act** | `make modern-run TYPE=<NN>` · `make modern-dbt` · `make modern-check` |
| **observe** | `evidence/modern/<batch>/*.json` — deterministic artifacts, not logs |
| **gate** | golden-match `resolved: true` **and** `unexplained_count: 0` |
| **repeat** | until the gate closes or a halt condition fires |

Read the artifacts, not your own console output. The artifacts are what a human
will review tomorrow.

---

## Done when

Every one of these is true:

```bash
make modern-run TYPE=<NN>    # golden-match resolves, zero unexplained
make modern-dbt              # every model and data test green
make modern-check            # units green, strict mypy clean
make test-e2e TYPE=all       # nothing regressed for the other types
```

**and the money is right.** This is the acceptance criterion that matters:

| | Required |
|---|---|
| The source-defect batch, computed | the true value |
| The source's declaration | **preserved byte-exact, never repaired** |
| golden-match classification | `CONFIRMED_SOURCE_DEFECT` |
| Calculation delta on accepted batches | exactly `0.00` |
| `unexplained_count` | `0` |

⚠️ **Python's default rounding is `ROUND_HALF_EVEN`. Financial contracts here
mandate `HALF_UP`.** `f"{value:.2f}"` and `round()` will both quietly give you
banker's rounding. Use `Decimal.quantize(..., rounding=ROUND_HALF_UP)`. Getting
this wrong is a one-cent error that the referee will catch and that no
structural test will.

---

## Narrate as you go

One line per milestone, in plain language. The operator is explaining this to an
audience while you work and needs to be able to glance at your output and know
where you are. Announce: the kit read, legacy confirmed, each file written, each
gate attempted, each gate passed or failed, the branch, the commits, the PR.

Do not ask questions. Do not wait. Go.

---

## `retool` — inspect a docked kit

```bash
make retool TYPE=<NN>
```

Prints the kit, the state of the line, the loop's surfaces, and the work order.
Read-only. Changes nothing.

## `status` — where every type stands

Report, per registered type: is the specification installed, does the legacy
vertical run, is the modern vertical built, and does golden-match close.

```bash
ls contracts/types/
ls modern/ingestion/src/northwind_pay/types/
ls evidence/modern/ 2>/dev/null
```

## `audit` — did the run obey its mandate

Check and report honestly:

- did anything write to a frozen path? (`git diff --name-only` against
  `legacy/ contracts/ gen/ infra/`)
- was any expected value, fixture, or oracle modified?
- is there evidence of git archaeology for deleted implementations?
- did every commit leave the gates green?

Report what you find, including nothing. **An audit that always passes is worth
nothing** — say what you actually checked and how you checked it.
