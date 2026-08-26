# Tech-Spec — NorthWind Pay, Type 01 Card Settlement

**Answers:** `docs/brd-type-01-card-settlement.md` (Pass 0 Capture, unsigned draft)
**Owner:** Helena Dias, Partner Integration · **Drafted:** 2026-08-24 · Converge Pass 1 · Intent
**Altitude:** intent. Falsifiable requirements only — no architecture, no components, no technology.

---

## 1. The brief, restated — problem restated

NorthWind Pay settles overnight card files through a line that already works: a batch lands on
SFTP, Java 21 parses, validates and sanitizes it, and the results are applied and reconciled in
the legacy relational store. Helena asked for a **second, independent implementation built
beside that line** — one that reads the same raw bytes from the drop she mailed, never calls or
copies the existing Java, and still reaches the same terminal verdict on every batch.

The reason is evidence, not throughput. Today one reader exists, so when a number disagrees
nobody can tell a **source** defect from a **plant** defect. The drop carries a deliberate case
of exactly that: a batch whose trailer declares **173.44** while its detail rows add to
**173.45**. Marina has explained that same cent twice in twelve days. A second reader that
independently reaches "the source is wrong, and here is the number it declared" ends that
conversation permanently.

**In scope:** Types `01` through `05`, all five mailed with inbound notes, samples and expected
outputs; Type `01` is the steel thread. Reading the same raw bytes and producing one of three
terminal verdicts per batch.

**Out of scope, explicitly:** Type `06` — it is not in this drop and is not opened here.
Replacing, editing, calling, or reading the existing Java line to derive an answer. Editing
`legacy/`, `contracts/`, `gen/`, or `infra/`. Any architecture, component boundary, storage
format, or tool decision — those belong to later passes, not to this one.

---

## 2. Requirements

Priority: **must** = the outcome fails without it. **should** = expected, negotiable at plan
altitude. **wont** = explicitly excluded at this altitude (`W-n`).

### Correctness of the accepted path

- **R-1 (must)** — For every accepted sample, the independently computed net amount must equal
  the expected net amount with an absolute difference of exactly `0.00`, and the record count
  must match exactly. Tolerance is `0` and stays `0`. Reference: `valid-minimal` = `173.45`
  over 2 records; `negative-overpunch` = `-12.34`.
- **R-2 (must)** — Money must be carried as exact decimal end to end. Binary floating point is
  excluded; a value that cannot round-trip to the same 2 decimal places fails the requirement.
- **R-3 (must)** — All 5 mailed Type `01` samples must reach their declared expected outcome:
  3 accepted, 1 grammar refusal, 1 source refusal. Fewer than 5 of 5 is a failed type.

### The lie, and the refusal

- **R-4 (must)** — Exactly `0` declared control values may be rewritten. When a batch's declared
  control total disagrees with the total computed from its own detail rows, the implementation
  **must keep the declared value unchanged** and must
  not write the computed value into any field that represents the source's declaration. For
  `df-source-001`: declared stays `173.44`; computed is reported as `173.45`; the difference of
  `0.01` is reported, never closed.
- **R-5 (must)** — That batch must be **refused**, not accepted with a correction. Expected
  finding `SOURCE_CONTROL_TOTAL_MISMATCH`, attributed to the source system in its role as
  system of record. Exactly 0 sanitized output rows and 0 business-state mutations may result
  from a refused batch.
- **R-6 (must)** — A refusal must carry a stable code drawn from the approved vocabulary. The
  code for a given defect must not vary between 2 runs of the same input.
- **R-7 (must)** — Refusal must be **batch-scoped**: when 1 batch is refused, every unrelated
  batch in the same cycle must continue to completion. A refusal that halts more than the
  1 offending batch fails this requirement.
- **R-8 (must)** — A grammar defect and a source defect must be distinguishable in the output.
  `malformed` yields `INVALID_OVERPUNCH`; `df-source-001` yields
  `SOURCE_CONTROL_TOTAL_MISMATCH`. Collapsing these 2 into 1 code fails the requirement.
- **R-9 (should)** — The same keep-the-declaration rule should hold unchanged for the other
  4 live types, whose lies are 173.44/173.45, 198.49/198.50, 999.99/1000.00, and 0.99/1.00.

### Independence

- **R-10 (must)** — The implementation must derive its answer from the raw bytes and the signed
  contract alone. It must not call, import, decompile, or transcribe the existing Java line,
  and must not re-use the existing stored routines to produce its answer. At most `0` of its
  outputs may depend on the legacy line executing.
- **R-11 (must)** — Where the 2 implementations disagree, both results must be preserved and
  reported, with at most `0` of them silently overwritten by the other.

### Privacy

- **R-12 (must)** — Restricted identifiers must appear **0 times in the clear** downstream.
  Card numbers, national identifiers, account numbers and holder names may exist in the raw
  file, and no more than `0` of them may appear unprotected in
  any downstream output, log, evidence record, or reporting surface, unless the type policy
  names an approved transform.
- **R-13 (must)** — Privacy must fail closed: if a required transform key is unavailable, the
  batch must halt with 0 outputs written rather than proceed unprotected. A single leak stalls
  the type; there is no demo exception.

### Explicit non-requirements at this altitude

- **W-1 (wont)** — No storage format, engine, framework, library, or product is chosen here.
  0 technologies are named in this spec by design; that decision belongs to a later pass.
- **W-2 (wont)** — No component boundaries, no seams, no swimlanes, no interfaces. 0 of them
  are cut at intent altitude.
- **W-3 (wont)** — No architecture decision records. 0 are written here.
- **W-4 (wont)** — Type `06` is not specified, not sampled, and not designed for. It appears
  0 times as a requirement.

## Success metrics (current → target, traced to BRD KPIs)

| # | Metric | Current | Target | Traces to |
|---|---|---|---|---|
| M-1 | Live types with an independent second reader | 0 of 5 | 5 of 5 | K1 |
| M-2 | Source lies kept and refused, never repaired | 0 kept independently | 5 of 5 kept, 0 repairs | K1 |
| M-3 | Accepted samples matching expected output, zero tolerance | Java's word only | 100% match, delta `0.00` | K2 |
| M-4 | Restricted values surviving sanitize | unverified outside Java | 0 occurrences | K3 |
| M-5 | Times the same cent must be re-explained by hand | 2 in 12 days | 0 — the refusal cites itself | K4 |

## Data named (problem level)

The records this work acts on, named at problem level and not as a schema:

- **The raw settlement file** — a fixed-width, single-byte-encoded file carrying a header, detail
  records, and a trailer, with signed amounts encoded in the final byte of the amount field.
- **The declared controls** — the source's own record count and net amount, carried in the
  trailer. These are the source's claim about itself and are the subject of R-4.
- **The detail records** — the individual settlement rows whose independently computed sum is
  compared against the declared control.
- **The source manifest and checksum** — what the sender says it sent, and the hash that proves
  the bytes did not change in transit.
- **The expected outputs** — per-sample sanitized rows, reconciliation, and refusal findings
  that constitute the oracle for this type.
- **Restricted identifiers** — present in the raw records, governed by R-12 and R-13.

---

## 3. Truth roles on this tree

Four roles, and no requirement may blur them.

| Role | Who holds it here | Consequence |
|---|---|---|
| **System of record** | The source, for its raw file and declared controls; the committed legacy tables, for applied state | A source can be the system of record **and** emit a defective batch — R-4 exists because of this |
| **Source of observation** | Immutable inbound bytes, hashes, manifests, and the per-run evidence packet | Shows what happened; never decides what should have happened |
| **Source of correctness** | The independently reviewed expected outputs and governed business rules | Decides what should happen; no implementation may redefine its own expected answer |
| **Executable contract** | The versioned schemas, canonical fixtures, and tests | Encodes the currently approved expectation; changes by version, never by edit |

Applied to the folders on this tree:

- **Inbound — `spec/`.** How the request arrived: mail, meeting notes, layout documents, dated
  routines, policies. Contradictions here are allowed and deliberate. **Inbound prose does not
  outrank the judge.** The cover letter is mail. A meeting note is mail.
- **Judge — `contracts/`.** The source of correctness, signed. It outranks the code: where an
  implementation and the contract disagree, the implementation is the bug. A meeting using the
  wrong noun is not a reason to edit it.
- **Frozen plant — `legacy/`, `gen/`, `infra/`** (and `contracts/` itself). Not editable to make
  any gate pass. If a gate cannot pass without changing something in there, that is a hard stop
  to classify and escalate, not a task.
- **Observation — `evidence/`.** The per-run packet. It records what happened; it never
  adjudicates, and it is not committed truth.

The live vocabulary disagreement in the drop belongs here: Ops has said "settlement total" for
six years, while the mailed layout describes the same bytes differently. That is a question to
escalate to its owner, recorded below — **not** a licence to rename anything in the judge.

---

## 4. What the second plant must not do

These are the boundaries the brief bought, restated as constraints on the work — every one of
them out of scope for the implementation, permanently or for now.

1. **It must not repair the source.** `173.44` stays `173.44`. Computing `173.45` and reporting
   the `0.01` difference is the deliverable; closing that difference destroys the only evidence
   Marina has. This does not expire at any later pass.
2. **It must not write to SFTP, and its first write comes later.** The existing line's first
   write is a sanitized file on SFTP. **The second plant's first write is its own, it is not
   SFTP, and it does not happen tonight** — it happens only after the owner signs the hardened
   plans at the Consensus barrier. Writing to the existing line's destination is a failed day.
3. **It must not read Java for the answer.** Not to go faster, not to break a tie. It reads the
   bytes and the contract. A second reader that consults the first is not a second reader.
4. **It must not re-use the legacy routines** to invent an answer it could not derive itself.
5. **It must not edit the frozen plant** — `legacy/`, `contracts/`, `gen/`, `infra/` — to turn
   any gate green.
6. **It must not let a restricted value through**, and must fail closed rather than proceed
   without a required transform.
7. **It must not exist yet.** No implementation directory is created at this altitude; the
   first write is after Consensus.
8. **It must not open Type `06`.** Not in scope, not in this drop, not designed for here.
9. **It must not pick its own tools in this document.** The stack is decided later, on evidence,
   by the pass that owns that decision.

---

## 5. Open questions

Carried from the brief, each owned and dated. None blocks this spec; each blocks the work it
names.

### Open assumptions & gap register

- id: GAP-001
  question: "Is the reporting noun 'settlement total' or 'net'? Ops has said one for six years; the mailed layout says another."
  type: definition
  severity: minor
  owner: Marina Alves
  raised: 2026-07-02
  blocks: naming any reporting surface for this type
  resolution: "Deferred to the owner. This spec deliberately avoids fixing the noun; R-4 and R-5 are stated in terms of declared versus computed values, which hold under either name."

- id: GAP-002
  question: "Who owns Type 05 rounding language — the ops email or the fee schedule?"
  type: scope
  severity: minor
  owner: Marina Alves
  raised: 2026-06-02
  blocks: any Type 05 work; raised P1 at kick-off
  resolution: "Out of scope for Type 01. Must be answered by its owner before Type 05 requirements are written; it does not affect R-1 through R-13."

- id: GAP-003
  question: "Do the unused columns on the mailed table dumps carry forward? The sender said most were for a report that died."
  type: data
  severity: minor
  owner: Rafael Costa
  raised: 2026-06-09
  blocks: any served model, whenever one is designed
  resolution: "Deferred. No requirement here depends on those columns; the question returns when a serving surface is specified."

- id: GAP-004
  question: "Who signs this spec canonical, and when?"
  type: scope
  severity: minor
  owner: Helena Dias
  raised: 2026-08-24
  blocks: Pass 2 consuming this spec
  resolution: "Named: Helena Dias is the decider of record per the brief's stakeholder table. The verdict below stays pending until she signs; no later pass may proceed on the draft."

**Assumption carried, not verified here:** that the expected outputs mailed with the drop are
themselves correct. This spec treats them as the oracle. If an expected output is ever shown to
be wrong, that is a contract-versioning event owned by the contract, not a licence for any
implementation to adjust its own answer.

---

## Sign-off

- **Owner/decider:** Helena Dias, Partner Integration — verdict: _pending_
- **Date:** —

A draft validates structure and authorizes nothing. This spec is not canonical, and **Pass 2
must not consume it** — an unsigned tech-spec is not a licence to code. Structure, decomposition
and consensus are later passes; the barrier is still ahead. Drafted by the agent, gated by the
referee, signed by the owner.
