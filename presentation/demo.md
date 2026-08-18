# NorthWind Pay EDP — the 60-minute live session

**Audience:** engineers who have never seen this repository. Most come from
Cline or a similar agentic IDE. They already know what *auto-approve* feels
like — the checkbox that lets an agent run without asking — and most of them
have turned it off again after it did something they did not expect.

**The question this hour answers:**

> *What would have to be true about a codebase before you would let an agent run
> in it unsupervised, all night, on a system that moves money?*

Everything in the next 60 minutes is an answer to that. The payment estate is
the setting; **auto-allow is the subject.**

**Operator note.** Every command here has been executed against this checkout
and the output shown is what it actually printed. Keep this file on a second
screen. Timings assume you talk while things run.

---

## Two tracks — pick one before you prepare

| | **Track A — the estate that exists** | **Track B — the live build** |
|---|---|---|
| Length | 60 min | 90 min, or 60 with Acts 1–2 compressed |
| What runs | Types `01`–`05`, already built | A **sixth type arrives** and the factory builds it on stage |
| Prep | 10 min pre-flight | 10 min pre-flight **+ the Type 06 kit built beforehand** (~2 days) |
| Risk | Low. Everything is committed and verified | High. A live agent run can stall or surprise |
| Use when | First exposure, or any audience under 90 min | Repeat audience, or when the point is *autonomy* rather than *architecture* |

Acts 0–6 below are **Track A** and stand alone. Track B is Act 7, and it
requires the preparation in **Appendix B** — which is the part that is easy to
underestimate.

**If you are doing Track B, read Appendix B first.** The kit must exist and must
be proven working on the legacy side *before* the demo, or the factory has
nothing to be graded against and the whole point collapses.

---

## Pre-flight — 10 minutes before doors open

```bash
cd <worktree>
make clean CONFIRM=clean-runtime     # guarantees a fresh runtime (destructive)
make deploy                          # ~30s   SFTP + PostgreSQL + migrations
make test-e2e TYPE=all               # ~3 min produces the legacy observations
# detector is not on this tree — it is built later
# modern is not on this tree — it is built during the week
```

Then **open a second shell and leave it clean** — you will run the live parts
there so nothing you typed during setup is in scrollback.

Terminal: 16 pt minimum, dark background, ~100 columns. Nothing here needs more
width. Have `README.md` open in an editor on screen two.

**Time budget:**

| Act | Minutes | What lands |
|---|---:|---|
| 0 · The question | 0–4 | Why an agent demo starts with a payment file |
| 1 · Orientation | 4–14 | What this repo *is*, without running anything |
| 2 · Run the legacy | 14–25 | A batch travels SFTP → Java → PostgreSQL, live |
| 3 · The defect | 25–35 | One cent. Three implementations. Containment |
| 4 · The factory | 35–46 | Attribution with evidence — and refusal |
| 5 · Auto-allow | 46–58 | **The payoff.** What made unsupervised running safe |
| 6 · Close | 58–60 | The one sentence to leave with |

---

## Act 0 — The question (4 min)

*Nothing on screen but the question. Do not open the repo yet.*

Say it plainly:

> "Everyone here has used auto-approve. And most of you have turned it off
> again, because at some point the agent did something confident and wrong, and
> the tests still passed.
>
> That is the actual problem. Not that agents make mistakes — people make
> mistakes too. The problem is that **our tests are usually not good enough to
> catch an agent's mistakes**, because they were written to catch a human's,
> and a human doesn't generate 4,000 lines before lunch.
>
> So: what would have to be true before you'd let one run all night on a system
> that moves money? That is what I want to show you. The payment system is just
> the setting."

Then the one-line premise:

> "This repository builds the same payment system **twice**, on purpose, and
> has a third component whose only job is to decide which one is wrong."

---

## Act 1 — Orientation: what am I looking at? (10 min)

*Goal: they can navigate this repo alone afterwards. Run almost nothing.*

### 1.1 · The shape (3 min)

Open `README.md`. Show the diagram and the folder table.

```bash
make help | head -30
```

Point at three folders only — resist listing all thirteen:

| Folder | Say this |
|---|---|
| `legacy/` — 29,732 lines | "The system that works. Java, PL/pgSQL, Python, SFTP. **Frozen.** Nothing may modify it to make a test pass." |
| `modern/` — 6,888 lines | "The same job, rebuilt independently. 23% of the size." |
| `contracts/` — 5,748 lines | "**Neither of them is allowed to define what 'correct' means.** This folder does." |

> "Two implementations that share no code, one referee that outranks both.
> That structure is not academic — it is the only reason a mistake is
> *detectable* rather than merely *absent from the logs*."

### 1.2 · Open one contract (4 min)

```bash
ls contracts/types/01-card-settlement/
ls contracts/types/01-card-settlement/main/
```

```
csv.yaml  layout.yaml  privacy.yaml  reconciliation.yaml  main/  README.md
```

> "Four files, four questions. How do I read the bytes? What do I emit? What
> must never leave? How do I know it added up?"

Then open `main/` and land the important idea:

```bash
head -2 contracts/types/01-card-settlement/main/expected-sanitized.csv
```

> "This is not a test fixture. This is **the approved answer**, reviewed by a
> human, committed to Git. Both implementations are graded against it. Neither
> one is allowed to edit it.
>
> The rule the whole repo rests on: **no oracle, no build.** A spec that does
> not ship its expected output cannot be adjudicated — so the factory refuses
> it before doing any work."

*If someone asks "why five types?"* — each stresses something different: COBOL
overpunch, escaped delimiters, 240-byte paired segments, heterogeneous record
widths, semicolon CSV with decimal commas. A parser that handles one tells you
nothing about the next.

### 1.3 · The privacy boundary is the operating system (3 min)

```bash
sed -n '/| Zone/,/csv\/archive/p' infra/README.md
```

> "Four SFTP roles, eight zones, real Unix groups. The component that talks to
> PostgreSQL **cannot see the raw files at all** — not by policy, by `chown`.
>
> When someone asks 'how do you know the loader can't leak a card number?', the
> answer is not a code review. It's the filesystem."

---

## Act 2 — Run the legacy, live (11 min)

*Goal: they see a real batch move through a real stack. This is the "it's not slides" moment.*

### 2.1 · Deploy (2 min)

```bash
make status
```

> "SFTP and PostgreSQL, both bound to localhost. Docker-pinned by digest — not
> by tag, because a tag can be republished and then your proof means nothing."

### 2.2 · One batch, end to end (5 min)

```bash
make run TYPE=01 SCENARIO=valid-minimal
```

While it runs, narrate the journey:

```
gen/output/          DataGen writes an immutable bundle
   ↓ publisher       authenticates as raw-publisher — can write ONE zone
raw/incoming/        manifest written LAST = the readiness signal
   ↓ intake          claims by rename: posix_rename, atomic
raw/processing/
   ↓ processor       Java 21, in a container
csv/outgoing/        sanitized — no PAN, no clear CPF
   ↓ loader          never sees raw/ at all
staging → legacy → reporting
   ↓ operator        the only role that may archive
raw/archive/
```

> "Manifest-last is the synchronisation primitive. There is no lock and none is
> needed — a consumer treats the manifest's presence as 'this batch is
> complete'."

### 2.3 · What it left behind (4 min)

```bash
ls .runtime/e2e-evidence/B202607230000001/
```

> "Every batch leaves an evidence packet. Not logs — **artifacts**: what was
> published, what Java produced, what PostgreSQL committed, what the oracle
> said. This is what makes an autonomous run reviewable the next morning."

Show that the sanitized output is genuinely sanitized:

```bash
cut -d, -f1,6,7,8,10 \
  contracts/types/01-card-settlement/main/expected-sanitized.csv | column -t -s,
```

```
batch_id          card_token                  card_last4  cpf_masked   amount_brl
B202607230000001  tok_0c5ac34fdde4aa92c6115f09  1111       *******8909  123.45
B202607230000001  tok_ebda34304c95de0d57d08c99  4444       *******2100  50.00
```

> "`tok_0c5ac34f…` and `*******8909`. The card number and the CPF never made it
> past Java. That boundary is checked byte-for-byte against the approved file —
> not with a regex that says 'looks tokenised'."

---

## Act 3 — The defect (10 min)

*Goal: the room understands what "correct" means here, and why it is hard.*

Demo batch: **`B202607230000004`**, Type `01`. One cent. Two detail rows.

### 3.1 · The lie, in the source's own words (2 min)

```bash
python3 -c "
import json; m=json.load(open('.runtime/e2e-evidence/B202607230000004/source-manifest.json'))
print('source declares:', json.dumps(m['source_controls']))"
```

```
source declares: {"currency": "BRL", "detail_count": 2, "net_amount": "173.44"}
```

> "The upstream says this batch nets 173 reais and 44 cents. Hold that number."

### 3.2 · Three implementations, one answer (3 min)

```bash
python3 -c "
import json
j=json.load(open('.runtime/e2e-evidence/B202607230000004/java-run.json'))
p=json.load(open('.runtime/e2e-evidence/B202607230000004/postgres-diagnostic.json'))
g=json.load(open('evidence/modern/B202607230000004/parser-run.json'))
print(f\"legacy Java parser   declared={j['declared_net_amount']}  computed={j['computed_net_amount']}\")
print(f\"PostgreSQL read-only SQL           computed={p['computed_net_amount']}\")
print(f\"modern Python parser declared={g['controls']['declared_net_amount']}  computed={g['controls']['computed_net_amount']}\")"
```

```
legacy Java parser   declared=173.44  computed=173.45
PostgreSQL read-only SQL           computed=173.45
modern Python parser declared=173.44  computed=173.45
```

> "Java, SQL and Python. Three implementations that share no code. All three
> computed 173.45. All three kept the source's 173.44 **exactly as written** —
> nobody rounded it away, nobody helpfully corrected it.
>
> That restraint is the whole discipline. A system that silently fixes its
> input has destroyed the evidence that something upstream is broken."

### 3.3 · Containment (2 min)

```bash
docker exec northwind-pay-legacy-postgres-1 psql -U northwind_admin -d northwind_legacy -t -A -c \
"select 'staging rows='||(select count(*) from staging.card_settlement where batch_id='B202607230000004')||
 ' | business rows='||(select count(*) from legacy.card_settlement where batch_id='B202607230000004')||
 ' | status='||(select status from control.batches where batch_id='B202607230000004')"
```

```
staging rows=0 | business rows=0 | status=quarantined
```

> "Zero rows. Not rolled back — **never written.** The cent never entered the
> database."

### 3.4 · Blast radius is one batch (3 min)

```bash
docker exec northwind-pay-legacy-postgres-1 psql -U northwind_admin -d northwind_legacy -t -A -F' | ' -c \
"select batch_id, status from control.batches
 where batch_id in ('B202402290000001','B202607230000002','B202607230000004') order by batch_id"
```

```
B202402290000001 | succeeded
B202607230000002 | succeeded
B202607230000004 | quarantined
```

> "One batch stopped. The two around it succeeded and reconciled. **A bad file
> does not take the night down.** If you are going to run unattended, that
> property is not optional."

---

## Act 4 — The factory: attribution with evidence (11 min)

*Goal: the difference between a system that reasons and one that asserts.*

### 4.1 · Run the detector live (3 min)

```bash
PYTHONPATH=factory/src legacy/runner/.venv/bin/python -m cli \
  --type 01 --legacy-evidence-root .runtime/e2e-evidence --no-publish \
  | python3 -m json.tool
```

Point at four things. **Do not read the JSON aloud.**

- `attribution.owner: "source_system_of_record"` — **who**
- `attribution.basis[]` — named rules, each listing the channels that fed it.
  *"This is the explanation. Not a sentence a model wrote — a list a test can
  check."*
- `controls.compared[]` — `detail_count` matches, `net_amount` does not
- `observations[].independence` — each channel labelled
  `independent_computation`, `persisted_record`, `derived_projection`

> "No card number. No document. No raw row. Scroll it — there is nothing here
> you would not paste into a ticket."

### 4.2 · Take its evidence away (5 min) ← **the money shot**

```bash
for ch in legacy-source-manifest legacy-java-processor \
          legacy-postgres-control-plane legacy-postgres-diagnostic; do
  out=$(PYTHONPATH=factory/src legacy/runner/.venv/bin/python -m cli \
        --type 01 --legacy-evidence-root .runtime/e2e-evidence --no-publish \
        --withhold "$ch" 2>&1 >/dev/null)
  printf "  withhold %-32s -> %s\n" "$ch" "${out:-CONCLUSIVE}"
done
```

```
  withhold legacy-source-manifest           -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-java-processor            -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-postgres-control-plane    -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-postgres-diagnostic       -> DF-E-ATTRIBUTION-INCONCLUSIVE
```

> "Remove any single piece of evidence and it **refuses to conclude.** It does
> not lower a confidence score. It declines.
>
> That is the difference between a system that reasons from evidence and one
> that produces opinions — and it is the property you actually need before you
> let something run unattended."

**Then the confession, immediately** — it is the strongest thing in the hour:

> "The first version of this probe passed with *any* channel removed, because
> the rule asked for 'at least two corroborations out of three'. The gate was
> green and proved nothing. The autonomous run caught it and tightened it."

### 4.3 · Determinism (3 min)

```bash
for i in 1 2; do
  PYTHONPATH=factory/src legacy/runner/.venv/bin/python -m cli \
    --type 01 --legacy-evidence-root .runtime/e2e-evidence --no-publish \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['finding_id'])"
done
```

```
sha256:2ba123ee0dfd24d31dc12db93e300c0ce949fc7cd113ddabf7ff0e3bd0807710
sha256:2ba123ee0dfd24d31dc12db93e300c0ce949fc7cd113ddabf7ff0e3bd0807710
```

> "Same identity, byte for byte, on four different runtimes built from scratch
> on different days. **The finding is a fact, not a generation.** You can diff
> it, store it, and page on it."

---

## Act 5 — Auto-allow: what actually made this safe (12 min)

*This is the act your audience came for. Everything before it was setup.*

### 5.1 · Name the thing they already know (2 min)

> "In Cline you tick auto-approve and the agent stops asking. What you have
> actually done is **transfer the review burden onto your gates.** Every check
> that would have caught a mistake is now the only thing standing between the
> agent and your repository.
>
> So the question is not 'do I trust the model.' It is: **are my gates good
> enough to be the last line?** Here is what I learned by finding out."

**Then give them the ladder.** This is ours, not borrowed — and the rung that
matters is L4, which almost nobody can claim:

| | Level | Meaning |
|---|---|---|
| L1 | **Suggest** | It drafts. You apply |
| L2 | **Assist** | It patches. You approve each one |
| L3 | **Unattended** | It runs with guardrails. You review after |
| **L4** | **Adjudicated** | **An independent oracle decides whether it is right** — not the agent, not you |
| **L5** | **Self-delivering** | Work order in, pull request out. Evidence for a human to approve |

> "Almost every autonomous-coding demo you have seen is **L3.** Unattended, yes —
> but nothing independent grades the result. The interesting rung is **L4**, and
> you cannot reach it without an oracle you are forbidden to touch. **That is the
> whole reason this repository builds the same system twice.**"

*Credit where due:* the L1–L3 shape comes from
[Loop Engineering](https://github.com/cobusgreyling/loop-engineering), whose scale
stops at L3 — unattended with guardrails. L4 and L5 are this repository's
addition, and they are the two that required an oracle.

### 5.2 · The mandate (2 min)

Read the hard rules out loud from
[`plans/dark-factory.md`](../plans/dark-factory.md) §9 — they are short and
they are the design:

- `legacy/`, `contracts/`, `gen/`, `infra/`, and applied migrations are
  **frozen oracles** — never modified to make a gate pass
- **never** edit an expected value, fixture, or oracle to force green
- a **fresh isolated runtime** for every authoritative acceptance
- commit in **small gate-passing increments**
- **halt** on: privacy leak, legacy mutation, a gate that cannot pass without
  changing frozen truth, or Docker unavailable

> "Notice what those rules have in common. They all exist to stop the agent
> from doing the one thing agents are best at: **making the red thing green.**"

### 5.3 · Six gates that could not fail (6 min) ← **the heart of it**

> "Six checks in this repository were green and proved nothing. Four were found
> by the autonomous run itself. Two were found last night, reading code."

| # | The gate | Why it was empty |
|---|---|---|
| 1 | Withhold probe | "At least two of three" — passed with any channel removed |
| 2 | `make check` Java suite | Served **from Docker build cache** — 78 tests "passed" without executing on the committed bytes |
| 3 | Golden-match legacy parity | Reported parity **while never contacting legacy** — a missing driver plus a bare `except` |
| 4 | Type 04 account token | Hashed the account alone where the contract says `ispb:branch:account`. Well-formed, deterministic, stable — every structural test passed. Only byte-for-byte comparison caught it |
| 5 | dbt release gate | Existed for **Type 01 only**, and the pipeline scopes dbt per type — types 02–05 ran no release gate at all |
| 6 | Rejected-batch parity | Built its "legacy observation" **out of the contract**, so two checks compared the contract with itself |

Land #4 hard — it is the one senior engineers feel in their stomach:

> "That token bug would have given the same account at two different banks the
> same token. Every structural test passed. It was only caught by comparing
> bytes to a human-approved file."

Then the rule:

> "**A gate that cannot fail is worse than no gate**, because it spends your
> attention and gives nothing back. Auto-allow does not fail because models are
> dumb. It fails because we have a lot of green that means nothing, and until
> an agent runs for eight hours straight, nobody notices."

### 5.4 · So what do you actually do? (2 min)

Four transferable practices — this is the takeaway slide:

1. **Freeze your oracles.** Declare files the agent may never edit, and put it
   in writing. Most agent failures are *the expected value quietly changing*.
2. **Mutation-test your gates.** Before you trust a check, break the code on
   purpose and watch it go red. Every gate added here was proven falsifiable
   first.
3. **Make evidence an artifact, not a log line.** Deterministic, reviewable,
   diffable. Logs tell you what a run said; artifacts let you check.
4. **Let it refuse.** Design the system so "I cannot conclude" is a first-class
   outcome. A system that always answers will always answer wrongly eventually.

---

## Act 6 — Close (2 min)

```bash
make df-accept TYPE=all 2>&1 | grep "acceptance passed"
```

> "Five file formats. Two independent implementations. Every difference between
> them classified, and all five turn out to be the same finding: the source
> declared a total its own rows contradict.
>
> **Zero unexplained differences. Zero legacy defects.** The old system was
> right the whole time — its inputs were not.
>
> If you take one thing from the hour: auto-allow is a bet on your gates. Go
> and try to break one of yours this week. If you can't make it go red, it was
> never protecting you."

---

## Act 7 — Track B: a sixth type arrives (30 min)

*Only if Appendix B is done. This is the act where the factory builds something.*

### 7.1 · The kit arrives (4 min)

Show the folder as if it were an email attachment that landed this morning:

```bash
ls contracts/types/06-*/ contracts/types/06-*/main/
git log --oneline -1 -- contracts/types/06-*
```

> "A partner bank sends a new file format. In most estates this is a
> three-month project. Here is what actually arrived."

Then say the sentence the whole act rests on:

> "Notice what is in this kit. A contract. A generator. A Java processor. A
> PostgreSQL loader. An independent oracle. **The legacy side is already built —
> it came with the request.** That is not us being lazy. That is the *only* way
> the factory can be graded: it has to reach an answer that something
> independent already knows."

Show the size:

```bash
git ls-files 'contracts/types/06-*' 'legacy/**/type06*' 'legacy/**/*type06*' \
  'gen/src/generators/type_06*' 'validation/oracle/type06*' | xargs wc -l | tail -1
```

> "About 5,500 lines of ground truth arrived. **The factory's job is the other
> thousand** — and to prove that thousand is right."

### 7.2 · Prove the ground truth runs (4 min)

```bash
make run TYPE=06 SCENARIO=valid-minimal
make run TYPE=06 SCENARIO=DF-SOURCE-006
```

> "Legacy accepts the good batch and quarantines the defective one. The kit
> works. **Now there is something to be wrong against.**"

This is also the moment to be explicit about what does *not* exist:

```bash
ls modern/ingestion/src/northwind_pay/types/
```

```
type01_card_settlement  type02_instant_payment_events  type03_payment_slip_settlement
type04_ted_transfer_settlement  type05_merchant_fee_assessment
```

> "No `type06`. Nothing. The modern side of this type does not exist, and I am
> not going to write it."

### 7.3 · Hand it to the factory (3 min)

> **The prompt cards live in [`prompts/`](../prompts/README.md).** Card 06 is the
> invocation; the rest walk the whole hour. Keep `prompts/README.md` on the second
> screen.

The factory invocation is **not in this tree yet**. Do not look for a
`/fab` skill or a `.claude/` harness. On the factory day the work order
is a docked kit under `spec/`; the verb that consumes it comes back then.

State the goal out loud:

> "Push Type 06 to the modern platform end to end. The contract is the
> specification. `legacy/`, `contracts/`, and `gen/` are frozen — you may read
> them and you may not touch them. Close golden-match against the approved
> expected outputs and against the live legacy observation. Halt on a privacy
> leak, on legacy mutation, or on any gate you cannot pass without changing
> frozen truth."

Then **turn on auto-allow** and say so:

> "This is the checkbox. From here it does not ask me anything. Everything I
> showed you in Act 5 is now the only thing between it and this repository."

### 7.4 · Narrate the run (12 min)

Do not watch silently. Call out each milestone as it lands, and use the waiting
time for the commentary:

| When you see | Say |
|---|---|
| It reads `contracts/types/06-*/layout.yaml` | "It is reading the spec, not the Java. If it read the Java it would inherit its bugs and call it parity." |
| It writes `modern/ingestion/.../type06_*/parser.py` | "Five files per type, same rhythm as the other five. It is following a convention it inferred from the repository, not one I gave it." |
| It writes dbt models | "Bronze, Silver, Gold — and the type tag. An untagged test silently never runs in a scoped build. That is the kind of detail that decides whether this works." |
| It runs `make modern-run TYPE=06` and something fails | **This is the best moment in the demo.** "Watch. It is not asking me. It reads the error, forms a hypothesis, and tries again." |
| It hits the hardcoded `SUPPORTED_TYPES := 01 02 03 04 05` | "There it is — the Makefile allowlist. A new type is not just new code, it is every place the old number list was written down." |
| golden-match closes | "Now the referee speaks. Not the agent." |

If it stalls or goes in circles for more than ~4 minutes, **say so and cut to
7.5 using the pre-built branch** (Appendix B keeps one). An honest "it's
struggling, here's the run I did last night" costs you nothing. A silent
ten-minute stall costs you the room.

### 7.5 · The verdict (5 min)

```bash
make modern-run TYPE=06
make modern-dbt
```

```bash
python3 -c "
import json
d=json.load(open('evidence/modern/<type06-df-source-batch>/golden-match.json'))
print('resolved:', d['resolved'], '| unexplained:', d['unexplained_count'])
for x in d['differences']:
    print(' ', x['classification'], x['field'], 'computed=', x['modern'], 'declared=', x['reference'])"
```

> "`CONFIRMED_SOURCE_DEFECT`. Zero unexplained. **The agent did not tell me it
> worked — the referee did**, by comparing what the agent built against an
> oracle the agent was forbidden to touch.
>
> That distinction is the entire talk. An agent saying 'tests pass' is a claim.
> An independent oracle saying 'byte-identical to the approved answer' is
> evidence."

### 7.6 · The flywheel (2 min)

```bash
git log --oneline -3
git diff --stat HEAD~1
```

> "One commit, gates green. And whatever it learned on the way — a convention it
> had to infer, a gate that was empty, a place the old number list was written
> down — gets written down so the seventh type is cheaper than the sixth."

---

## Failure protocol

| If | Then |
|---|---|
| Docker unhealthy | `make deploy` again — idempotent |
| Runtime dirty / batch IDs collide | `make clean CONFIRM=clean-runtime && make deploy && make test-e2e TYPE=all` (~4 min) |
| Detector says `DF-E-OBSERVATION-MISSING` | The e2e portfolio has not run on this runtime — run it |
| Modern command quarantines everything with `PRIVACY_VIOLATION` | `.env` was not loaded. `pipeline.py` loads it now; if you invoke Python directly, `set -a; . ./.env; set +a` |
| Everything stalls | `evidence/factory/` and `evidence/modern/` are on disk from pre-flight — **read the packets instead of regenerating** |

Errors on screen are fine and on-brand for this material. A stall is not — fall
back to reading committed evidence.

---

## What not to claim

- **Not** "the factory found a legacy defect." Zero. All five are source-system
  defects.
- **Not** "the agent wrote all this unsupervised with no corrections." It was
  autonomous, and it found and fixed four empty gates on the way — which is the
  better story.
- **Not** "production-ready" or "CI-ready." `plans/modern.md` forbids claiming
  either from local proof, and no CI exists.
- **Not** "modern replaces legacy." Legacy is the frozen oracle; modern is an
  independent second implementation whose entire purpose is to disagree
  detectably.
- **Not** "auto-allow is safe." The claim is narrower and truer: *auto-allow is
  exactly as safe as your gates are falsifiable.*

---

## Appendix B — building the Type 06 kit (Track B prep)

**The rule that governs everything below:** you build the **legacy** side and
the **contract**. You do **not** build the modern side, the dbt models, or the
modern tests. Those are the demo. If you build them, you have nothing to show.

### The one decision that shapes the demo

Pick a layout that stresses something the existing five do not — otherwise the
factory is doing a copy-paste and the audience can tell.

| Already covered | Type | Good Type 06 candidates |
|---|---|---|
| Fixed-width, COBOL overpunch | `01` | **Multi-currency** — a second currency column, so reconciliation groups by `(batch_id, currency)` for real instead of always `BRL` |
| Escaped delimiters | `02` | **Nested/repeating group** — a header with N child rows declared in the header itself |
| Paired 240-byte segments | `03` | **Fixed-point with 4 decimals** — forces a scale the money helper has never emitted |
| Heterogeneous widths | `04` | **EBCDIC or Latin-1 encoding** — a genuinely different byte world |
| Semicolon CSV, decimal commas | `05` | **Positional file with a checksum digit per record** |

My recommendation: **multi-currency fixed-width.** It is visibly different, it
exercises the `(batch_id, currency)` grain that currently only ever sees one
value, and it will very likely expose a real assumption in the modern
reconciliation — which is a *better* demo than a clean run.

### Build order — each step must pass before the next

```
Day 1 morning    1. Registry entry + the four YAMLs + README
Day 1 afternoon  2. main/ fixtures: 5 inputs + every approved output   ← the oracle
Day 1 late       3. DataGen generator
Day 2 morning    4. Migration 011 + PostgreSQL loader
Day 2 midday     5. Java processor + its tests
Day 2 afternoon  6. Independent oracle + workflow adapter + Makefile allowlists
Day 2 evening    7. Full legacy acceptance, clean runtime
```

**Step 2 is the one to spend real time on.** Those files are the ground truth
the factory will be graded against. If they are wrong, the demo either fails for
the wrong reason or — much worse — passes for the wrong reason.

### The file manifest

| # | Path | Model on | ~Lines |
|---|---|---|---:|
| 1 | `contracts/types/registry.yaml` — new entry | the `05` entry | 15 |
| 2 | `contracts/types/06-<slug>/{layout,csv,privacy,reconciliation}.yaml` + `README.md` | Type `01` (fixed-width) | 400 |
| 3 | `contracts/types/06-<slug>/main/` — 5 inputs + approved CSVs + reconciliation YAMLs + 2 rejection YAMLs | Type `01`'s `main/` | 130 |
| 4 | `gen/src/generators/type_06_<slug>.py` + registry dispatch in `generation.py` | `type_05_*.py` (517) | 520 |
| 5 | `legacy/postgres/migrations/011_type06_<slug>.sql` | `007_type05_*.sql` (475) | 480 |
| 6 | `legacy/postgres/type06_loader.py` | `type05_loader.py` (965) | 960 |
| 7 | `legacy/processor/src/main/java/.../type06/` | `type05/` (1,126) | 1,100 |
| 8 | `legacy/processor/src/test/java/.../type06/` | `type05/` (997) | 1,000 |
| 9 | `validation/oracle/type06_oracle.py` + `tests/test_type06_oracle.py` | `type05_oracle.py` (487) | 620 |
| 10 | `Type06WorkflowAdapter` in `legacy/runner/workflow_registry.py` + `WORKFLOWS` entry | `Type05WorkflowAdapter` (350) | 370 |
| 11 | `tests/contracts/test_type06_contract.py`, `tests/unit/test_type06_{loader,workflow}.py`, `tests/postgres/test_type06_loader_rollback.py` | their `05` twins | 1,700 |
| 12 | `tests/end-to-end/run_type06_suite.py` — **7 lines**, delegates to the shared harness, plus a `TypeAcceptanceSpec` entry | `run_type05_suite.py` | 130 |

**Total ≈ 7,400 lines** including tests. The kit *shown on stage* is ~5,500; the
rest is the legacy-side test suite that makes it trustworthy.

### The five scenarios — non-negotiable

Every type carries the same five, and the factory's acceptance depends on them:

| Scenario | Must |
|---|---|
| `valid-minimal` | Succeed. The smallest complete batch |
| `valid-boundary` | Succeed. Maximum amounts, leap-year date |
| `malformed` | Be **refused** with a `canonical_rejection_code` |
| `DF-SOURCE-006` | Declare a total its own rows contradict — **refused and attributed** |
| *(type-specific)* | Your chosen edge case, e.g. `mixed-currency` |

`DF-SOURCE-006` is the most important fixture you will write. It is what makes
Act 7.5 land.

### The ten methods the adapter must satisfy

This is the acceptance checklist for the kit — satisfy these and the existing
worker, engine, and recovery journal need **zero changes**:

`prepare` · `commit` · `recover` · `prepared_observation` · `load_observation` ·
`compare_sanitized` · `compare_post_db` · `compare_rejection` ·
`rejection_diagnostic` · `diagnostic_controls`

Plus six overridable evidence hooks. Ten mandatory, six optional.

### Things that will bite you

- **`SUPPORTED_TYPES := 01 02 03 04 05`** in the `Makefile`, plus hardcoded
  `case "$(TYPE)" in 01|02|03|04|05|all)` in `run`, `run-file`, `test-e2e`, and
  `modern-run`. A new type is not just new code.
- **Migration `011` is append-only.** Once applied, its checksum is in
  `control.schema_migrations`; you cannot edit it, only add `012`.
- **`gen/output/` survives `make clean`** and DataGen refuses to overwrite. After
  changing a Type 06 fixture, `rm -rf gen/output/<batch>` by hand or you will
  silently regenerate nothing.
- **Batch ID ranges** — pick a fresh block (e.g. `B2026072300005xx`) so Type 06
  never collides with `01`–`05`.
- **Do not add `type_06` dbt tags or models.** That is the factory's work.

### Gate before you demo

```bash
make clean CONFIRM=clean-runtime && make deploy
make check                       # includes the Java build, no cache
make test-e2e TYPE=06            # 3 succeeded, 2 quarantined
make test-e2e TYPE=all           # 06 must not have broken 01-05
make df-accept TYPE=all
```

**Then commit the kit on a branch and tag it.** Keep a second branch with the
*completed* modern side — the one you built yourself as a rehearsal — so Act 7.4
has somewhere to cut to if the live run stalls.

> The kit is ready when `make test-e2e TYPE=06` passes on a clean runtime **and**
> `modern/ingestion/src/northwind_pay/types/` still has exactly five folders.

---

## Appendix — questions you will get

**"Why build the same system twice? Nobody does that."**
> You already do — it's called the rewrite, and it usually ships without a
> referee. The second implementation here is not extra work; it's the only way
> a difference becomes *detectable* instead of *arguable*.

**"Couldn't the agent just read the Java and copy it?"**
> That is explicitly forbidden, and it is the point. Copying the old
> implementation reproduces its defects and then calls it parity. Modern reads
> the *contract*.

**"How long did the autonomous run take?"**
> One overnight session, Phases 0→4. But the interesting number isn't the
> duration — it's the four empty gates it found in work that was already green.

**"What stops it from editing a test to pass?"**
> Frozen-oracle rules in writing, plus the fact that expected values live in
> `contracts/` and are compared byte-for-byte. And honestly: nothing stops it
> absolutely. That's why the rule is written down and why the diff gets read.

**"Is 23% smaller really the win?"**
> No. The win is that the 23% is *adjudicated*. A smaller rewrite you can't
> grade is worse than the legacy you already trust.
