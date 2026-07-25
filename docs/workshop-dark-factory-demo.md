# Dark Factory — live demo script (Acts 3A/3B)

Operator cheat-sheet. Every command here was executed against this checkout and
the output shown is what it actually printed. Keep this on the second screen.

## Read this first: the scripted AHA has changed

`workshop-run-of-show-v1.md` Act 3B scripts the reveal as *"it's the legacy — a
silent defect summing wrong cents for years… the factory indicted the oracle."*

**That is not what this system found.** The golden-match closed with **zero**
`CONFIRMED_LEGACY_DEFECT`. The legacy baseline is correct on all five types.
What exists is five **source-system** defects — the upstream declared a total
that its own detail rows contradict:

| Batch | Type | Source declared | Independently computed |
|---|---|---|---|
| `B202607230000004` | `01` | `173.44` | `173.45` |
| `B202607230000105` | `02` | `173.44` | `173.45` |
| `B202607230000205` | `03` | `198.49` | `198.50` |
| `B202607230000305` | `04` | `999.99` | `1000.00` |
| `B202607230000405` | `05` | `0.99` (fee) | `1.00` |

Delivering the old line would claim a defect the evidence does not support, in
front of an audience who may later read the repo. Use the true reveal below —
it is stronger, because the audience can watch the machine *refuse to conclude*
when you take its evidence away.

**The new AHA, said aloud:**

> "Three independent implementations — Java, SQL, and Python — each computed
> `173.45`. The source declared `173.44`. **Nobody corrected it.** Every system
> preserved the lie exactly as written, refused the batch, and kept the other
> batches running. The one cent never reached the database. And the factory can
> prove *who* lied, without ever showing you a card number."

---

## Pre-flight (before doors open)

```bash
cd <worktree>
make clean CONFIRM=clean-runtime     # guarantees a fresh runtime
make deploy                          # ~30s
make test-e2e TYPE=all               # ~3 min; produces the observations
make df-accept TYPE=all              # ~30s; produces the findings
```

Export the fixture keys for any modern command (they are in `.env`):

```bash
export NWP_TOKENIZATION_KEY=northwind-pay-edp-fixture-key-v1 \
       NWP_DOCUMENT_TOKEN_KEY=northwind-pay-edp-fixture-document-key-v1 \
       NWP_TED_ACCOUNT_TOKEN_KEY=northwind-pay-edp-fixture-ted-account-key-v1 \
       NWP_PAYMENT_REFERENCE_KEY=northwind-pay-edp-fixture-payment-reference-key-v1 \
       NWP_PARTY_TOKEN_KEY=northwind-pay-edp-fixture-party-key-v1 \
       NWP_ACCOUNT_TOKEN_KEY=northwind-pay-edp-fixture-account-key-v1
```

Terminal: 16pt minimum, dark background, window ~100 columns. Nothing below
needs more width.

---

## The seven beats (~18 min of the 45)

Demo batch: **`B202607230000004`**, Type `01`. One cent. Two detail rows.

### Beat 1 — The lie, in the source's own words (1 min)

```bash
python3 -c "
import json; m=json.load(open('.runtime/e2e-evidence/B202607230000004/source-manifest.json'))
print('source declares:', json.dumps(m['source_controls']))"
```

```
source declares: {"currency": "BRL", "detail_count": 2, "net_amount": "173.44"}
```

> "The upstream says this batch nets 173 reais and 44 cents. Hold that number."

### Beat 2 — Three independent implementations, one answer (3 min)

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

> "Java, SQL, and Python. Three implementations that share no code. All three
> computed 173.45. All three kept the source's 173.44 exactly as written —
> nobody rounded it away, nobody 'helpfully' corrected it."

### Beat 3 — Containment (2 min)

```bash
docker exec northwind-pay-legacy-postgres-1 psql -U northwind_admin -d northwind_legacy -t -A -c \
"select 'staging rows='||(select count(*) from staging.card_settlement where batch_id='B202607230000004')||
 ' | business rows='||(select count(*) from legacy.card_settlement where batch_id='B202607230000004')||
 ' | status='||(select status from control.batches where batch_id='B202607230000004')"
```

```
staging rows=0 | business rows=0 | status=quarantined
```

> "Zero rows. Not rolled back — never written. The cent never entered the
> database."

### Beat 4 — The blast radius is one batch (2 min)

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

> "One batch stopped. The two that ran after it succeeded and reconciled. A bad
> file does not take the night down."

### Beat 5 — Run the detector live (3 min)

```bash
PYTHONPATH=dark-factory/src legacy/runner/.venv/bin/python -m darkfactory.cli \
  --type 01 --legacy-evidence-root .runtime/e2e-evidence --no-publish \
  | python3 -m json.tool
```

Point at four things only — do not read the JSON aloud:

- `attribution.owner: "source_system_of_record"` — **who**
- `attribution.basis[]` — three named rules, each listing the channels that fed
  it. *"This is the explanation. Not a sentence a model wrote — a list a test
  can check."*
- `controls.compared[]` — `detail_count` matches, `net_amount` does not
- `observations[].independence` — each channel labelled
  `independent_computation`, `persisted_record`, `derived_projection`

> "No card number. No document. No raw row. Scroll it — there is nothing in
> here you would not put in a ticket."

### Beat 6 — Take its evidence away (4 min) ← **the money shot**

```bash
for ch in legacy-source-manifest legacy-java-processor \
          legacy-postgres-control-plane legacy-postgres-diagnostic; do
  out=$(PYTHONPATH=dark-factory/src legacy/runner/.venv/bin/python -m darkfactory.cli \
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

> "Remove any single piece of evidence and it refuses to conclude. It does not
> lower a confidence score — it declines. **That is the difference between a
> system that reasons from evidence and one that produces opinions.**"

Worth telling them: the first version of this rule passed *every* withhold probe,
because it asked for "at least two" corroborations out of three available. The
gate was green and proved nothing. The run caught it and tightened it. *"A green
gate that cannot fail is worse than a red one."*

### Beat 7 — Determinism (2 min)

```bash
for i in 1 2; do
  PYTHONPATH=dark-factory/src legacy/runner/.venv/bin/python -m darkfactory.cli \
    --type 01 --legacy-evidence-root .runtime/e2e-evidence --no-publish \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['finding_id'])"
done
```

```
sha256:2ba123ee0dfd24d31dc12db93e300c0ce949fc7cd113ddabf7ff0e3bd0807710
sha256:2ba123ee0dfd24d31dc12db93e300c0ce949fc7cd113ddabf7ff0e3bd0807710
```

> "Same identity. That hash is byte-identical on four different runtimes built
> from scratch on different days. The finding is a fact, not a generation."

---

## Closing the loop — all five types (3 min)

```bash
make df-accept TYPE=all 2>&1 | grep "acceptance passed"
for b in $(ls evidence/modern); do
  python3 -c "
import json
d=json.load(open('evidence/modern/$b/golden-match.json'))
for x in d['differences']:
    print(f\"  {d['batch_id']}  {x['classification']:24} {x['field']}  computed={x['modern']}  declared={x['reference']}\")"
done
```

Five lines. Five types. Five source defects. **Zero unexplained differences.**

> "Five file formats — COBOL overpunch, escaped pipes, 240-byte paired segments,
> heterogeneous widths, semicolon CSV with decimal commas. Two independent
> implementations. Every difference between them is classified, and all five are
> the same finding: the source lied by one cent. Nothing unexplained is left."

---

## If you have 5 more minutes: the honest engineering beat

This lands hard with senior engineers and is entirely true:

Four gates in this build passed while proving nothing, and the run caught each:

1. The withhold probe was unfalsifiable (Beat 6).
2. `make check` served the Java suite from a **build cache** — 78 tests
   "passed" without executing on the committed bytes.
3. Golden-match reported **legacy parity while never contacting legacy** — a
   missing driver plus a bare `except` degraded it to contract-only comparison.
4. The Type 04 account token hashed the account number alone where the contract
   says `ispb:branch:account`. Tokens were well-formed, deterministic, stable —
   every structural test passed. Only byte-for-byte comparison against the
   approved output caught it. That bug would have made the same account at two
   different banks share a token.

> "Every one of those was green. Green is not the goal — **green for the right
> reason** is. That is what eval engineering buys you."

---

## Failure protocol

| If | Then |
|---|---|
| Docker is unhealthy | `make deploy` again; it is idempotent |
| Runtime is dirty / batch IDs collide | `make clean CONFIRM=clean-runtime && make deploy && make test-e2e TYPE=all` (~4 min) |
| Detector says `DF-E-OBSERVATION-MISSING` | The e2e portfolio has not run on this runtime — run it |
| Modern command fails on a key | The `export` block above was not sourced in that shell |
| Everything stalls | `evidence/dark-factory/` and `evidence/modern/` are already on disk from the pre-flight — read the packets instead of regenerating |

Errors on screen are fine and on-brand for this material. A stall is not — fall
back to reading the committed evidence packets.

---

## What not to claim

- **Not** "the factory found a legacy defect." It did not; there are zero.
- **Not** "the agent wrote all this unsupervised with no corrections." The run
  was autonomous, but it found and fixed four vacuous gates along the way —
  which is the more interesting story anyway.
- **Not** "production-ready" or "CI-ready." `plans/modern.md` explicitly forbids
  claiming either from local proof, and no CI exists.
- **Not** "modern replaces legacy." Legacy is the frozen oracle; modern is an
  independent second implementation whose whole purpose is to disagree
  detectably.
