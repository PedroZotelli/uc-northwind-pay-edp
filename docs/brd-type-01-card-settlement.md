# BRD — NorthWind Pay, Type 01 Card Settlement

**Owner:** Helena Dias, Partner Integration · **Drafted:** 2026-08-24 · Converge Pass 0 · Capture
**Altitude:** idea → brief. No requirements, no solution shape, no technology.

> **The six headings the room must be able to restate**, and where each one lives:
> 1. Who asked, and what is out of scope → *Problem* · *Scope*
> 2. What lands → *Problem*
> 3. What "done" means → *Definition of success*
> 4. The lie → *Problem*
> 5. Inbound vs judge → *Constraints*
> 6. What we will not do tonight → *Scope*

---

## Executive summary

We run five live settlement file types through SFTP → Java 21 → PostgreSQL. The same one-cent
trailer mismatch — declared 173.44 against details of 173.45 — has been re-explained twice in
twelve days, because Java is our only reader and no second opinion exists. I want an
independent implementation built beside that line, reading our drop. Type 01 first.

## Problem

### 1. Who asked, and what is out of scope

I asked. We already settle overnight through SFTP → Java 21 → sanitized CSV → PostgreSQL, and I
want a **second, independent implementation built beside that line** — one that reads the drop
we mailed, not our Java, and still reaches the same terminal outcomes (`spec/estate/cover.md`).

I am not asking you to replace Java. Rafael's decision D1 at kick-off: Java is not replaced,
the live line stays the oracle (`spec/estate/meetings/2026-06-02-kick-off.md`). I am not asking
you to fix source totals — Marina's D3: source totals are never rewritten, the lie is evidence.
And Type 06 is not in this drop — D2: five types only; a sixth file is a later pack.

We are not sending a parser, a lakehouse model, or permission to edit the live line (`cover.md`).

**The pain.** The same cent has been explained twice in twelve days: settlement total declared
**173.44** against details adding to **173.45** — on 2026-07-02, and again on 2026-07-14, where
Marina wrote that she is not sending another "corrected" file **(measured — two dated mails,
same cent:** `spec/estate/mail/2026-07-14-the-cent-that-will-not-die.md`,
`spec/type-01-card-settlement/inbound/2026-07-02-settlement-total.md`**)**. The same shape of
lie sits on all five live types — 5 of 5 **(measured** — `brain/notebooklm/08-the-lie.md`**)**.
Because Java is the only reader, a source defect and a plant defect look identical from here.

**Do-nothing answer.** If we build nothing, the line still settles — nothing breaks tonight.
But Marina re-sends the same explanation every few weeks, and the first genuine plant defect
will be indistinguishable from a source defect. Inaction is not catastrophic; it is corrosive.
That is why this is a brief and not a no-go record.

### 2. What lands

Money does not arrive as an API call. A batch lands on SFTP (`README.md`).

Tonight's steel thread is **Type 01, card settlement** — `CRD_SETTLE01`, a `.dat` file in
ISO-8859-1 fixed width with COBOL overpunch (`spec/type-01-card-settlement/README.md`). The
canonical run is batch `B202607230000001`, net **173.45**, reaching `MATCHED` **(measured** —
`evidence/B202607230000001/reconciliation.json`, run tonight**)**.

Type 01 mailed five samples, each with a job:

| Sample | Role | Expected |
|---|---|---|
| `valid-minimal` | happy | accepted · net `173.45` |
| `valid-boundary` | boundary | accepted |
| `negative-overpunch` | type edge | accepted · net `-12.34` |
| `malformed` | grammar | `INVALID_OVERPUNCH` |
| `df-source-001` | source lie | `SOURCE_CONTROL_TOTAL_MISMATCH` · declared `173.44` · computed `173.45` |

The other four live types exist and are mailed — 02 instant payment, 03 payment slip, 04 TED,
05 merchant fees (`cover.md`, `spec/README.md`). They are not tonight's thread, but they are in
the drop. **Type 06 is not here** — not a folder, not an empty folder, not a hint.

The first write of the second plant comes later, and it is not SFTP (`README.md`). That write
is not tonight's business.

### 4. The lie

Every live type ships one source-owned lie, and keeping it is the point of the engagement.

Type 01, sample `df-source-001`, batch `B202607230000004`: the trailer declares **173.44**; the
detail rows add to **173.45**. Detail count agrees at 2 on both sides — only the money
disagrees. Expected finding `SOURCE_CONTROL_TOTAL_MISMATCH`, quarantined at java-validation,
source system role `system_of_record`, `csv_produced: false`,
`postgres_business_mutation: false` **(measured** —
`spec/type-01-card-settlement/expected/df-source-001.finding.yaml`**)**.

The same shape runs through the drop **(measured** — `brain/notebooklm/08-the-lie.md`**)**:

| Type | Sample | Declares | Rows add to | Finding |
|---|---|---|---|---|
| `01` card | `df-source-001` | 173.44 | 173.45 | `SOURCE_CONTROL_TOTAL_MISMATCH` |
| `02` PIX | `df-source-002` | 173.44 | 173.45 | `SOURCE_CONTROL_NET_MISMATCH` |
| `03` slips | `df-source-003` | 198.49 | 198.50 | `SOURCE_CONTROL_NET_MISMATCH` |
| `04` TED | `df-source-004` | 999.99 | 1000.00 | `SOURCE_CONTROL_NET_MISMATCH` |
| `05` fees | `df-source-005` | 0.99 | 1.00 | assessed-fee lie |

**Keep the declaration. Compute the truth. Refuse the batch.** In Marina's words: if your new
plant quietly writes 173.45 into the trailer, we will have nothing to show the source — keep
their number, refuse the batch, that is the whole point
(`spec/estate/mail/2026-07-14-the-cent-that-will-not-die.md`).

A source system can be our system of record and still emit a defective batch. Naming that
mismatch is the deliverable. Silently correcting it destroys the only evidence we have.
**Do not "fix" 173.44.**

## Goals & KPIs

| # | KPI, in my terms | Current | Desired |
|---|---|---|---|
| K1 | Source lies kept and refused, never repaired | 0 of 5 types have an independent second reader | 5 of 5 classified as source defects, 0 repairs |
| K2 | Accepted batches matching the oracle, zero tolerance | Java's word only | Every accepted sample matches sanitized rows + reconciliation |
| K3 | Restricted values surviving sanitize | unverified outside Java | 0, in any CSV, Parquet, log, evidence packet, ticket, or warehouse table |
| K4 | Times Marina re-explains the same cent | twice in twelve days (measured) | 0 — the refusal cites itself |

## Scope

**In:** Types `01`–`05`, all five mailed with inbound, samples, and expected outputs. Type `01`
is tonight's steel thread.

**In:** An independent reader of the same raw bytes, reaching accepted / refused / kept-lie.

**Out:** Type `06` — not in this drop. It arrives later as its own pack with its own expected
outputs.

**Out:** Replacing, editing, or calling the live Java line; changing our SFTP roles; editing
`legacy/`, `contracts/`, `gen/`, or `infra/`.

**Out — 6. What we will not do tonight.** Tonight is Pass 0 Capture and Pass 1 Intent, human-led,
no product code:

- **No stack.** No DuckDB, no dbt, no lakehouse, no warehouse, no library.
- **No ADRs** — Pass 2 Structure is tomorrow.
- **No seams, no swimlanes, no legs** — Pass 3 Decompose is tomorrow.
- **No Consensus** — Pass 4 is the barrier, and an unsigned tech-spec is not a licence to code.
- **No `modern/`** — it must not exist today; its first write comes after Consensus is signed.
- **No repair of 173.44** — not tonight, not ever.
- **No Type `06`.**

**Undecided:** the reporting noun — "settlement total" versus "net" (see Open questions, Q3).
**Undecided:** whether the dead columns on Rafael's table dumps carry forward (Q2).

## Definition of success

### 3. What "done" means

In three months I point at a batch and say: the second plant read the same bytes and reached
the same verdict, without anyone opening Java. Done has exactly **three** shapes, and all
three are successes:

1. **Accepted.** Sanitized rows and reconciliation match the oracle, privacy holds, tolerances
   are zero (`cover.md`).
2. **Refused.** A stable code, no CSV, no business rows, and peers continue (`cover.md`).
   Quarantine is batch-scoped — Marina's D3 at the decomposition sync — so one bad batch never
   stops the line (`spec/estate/meetings/2026-06-09-file-decomposition.md`).
3. **A kept source lie.** Classified as a source defect, never repaired (`cover.md`).

A refusal is not a failure. `df-source-001` quarantining with no CSV and no business mutation,
while unrelated batches continue, is a correct night.

## Stakeholders

| Name | Role | Stake |
|---|---|---|
| **Helena Dias** | Partner Integration, requesting side | **Decider** — owns this brief and breaks ties |
| Marina Alves | Settlement Ops, NorthWind Pay | Feels the pain; owns the kept-lie rule (D3) and the reporting noun |
| Rafael Costa | Legacy Platform, NorthWind Pay | Owns the frozen line (D1); does not want the team reading Java to go faster |
| Priya Shah | Privacy, NorthWind Pay | Owns the privacy boundary (D4) — privacy finished before any CSV |

## Risks

The pre-mortem — it is six months from now, this shipped, and it failed. What killed it:

- **The new plant quietly wrote the computed total** and we lost the evidence. Marina's exact
  fear, stated in writing. *Accepted as the primary risk; it is the reason this brief exists.*
- **Somebody read Java to go faster** and we got a copy scored against itself instead of an
  independent reader. Rafael's implicit signal at kick-off. *Accepted.*
- **A stack was chosen before anyone agreed what the problem was**, and the argument became
  about tools. *Accepted — mitigated by holding Pass 1 free of technology.*
- **A restricted value reached a Parquet file** and stalled the type. *Accepted; the privacy
  policy fails closed and there is no exception for a demo.*
- **A vocabulary disagreement was settled by editing the contract** instead of escalating it.
  *Converted to Q3.*

## Constraints

Business constraints only.

- **Sixteen-week parallel modernization** of the five live files (kick-off, 2026-06-02).
- **Java stays the privacy boundary on the current line.** Not negotiable (D1, D4).
- **NorthWind keeps SFTP and PCI-adjacent bytes inside its own roles** (kick-off).
- **Privacy is finished before any CSV.** PAN, CPF, CNPJ, account numbers and holder names may
  exist in the raw file and must not exist after sanitize in any CSV, Parquet, log, evidence
  packet, ticket, or warehouse table, unless a type policy names an approved transform. Fail
  closed if a tokenization key is missing. A leak stalls the type
  (`spec/estate/policies/privacy.md`).
- **Exact decimal — no float money** (Rafael, D2, decomposition sync).

### 5. Inbound vs judge

`spec/` and `contracts/` are two different folders and they do not rank the same.

| | `spec/` — inbound | `contracts/` — judge |
|---|---|---|
| What it is | How the request arrived: mail, meetings, layouts, procs, policies | The source of correctness, signed |
| Contradictions | Allowed, and deliberate | Never |
| Authority | None over the contract | Outranks the code |

**Inbound prose does not outrank `contracts/`.** My cover letter is mail. A meeting note is
mail. When a meeting used the wrong noun, we do not edit the contract to match it
(`spec/README.md`). When two components disagree, `contracts/` decides which one is wrong; when
an implementation and a contract disagree, the implementation is the bug
(`contracts/README.md`).

Our own drop contains a live example: Marina wants "settlement total" on the recon report
because that is what the ops dashboard has said for six years, and does not care what the
layout PDF calls bytes 16–30. That is a vocabulary question to escalate — not a licence to
rename anything in `contracts/`.

## Open questions

- question: "Who owns Type 05 rounding language — the ops email or the fee schedule?"
  owner: Marina Alves
  blocks: any Type 05 work; raised P1 at kick-off 2026-06-02

- question: "Do the unused columns on Rafael's table dumps belong in the served model? He said most of those were for a report that died."
  owner: Rafael Costa
  blocks: nothing tonight; blocks the served layer whenever it is designed

- question: "Is the reporting noun 'settlement total' or 'net'? Ops has said one for six years; the layout says another."
  owner: Marina Alves
  blocks: nothing tonight; must be settled before any reporting surface is named

- question: "Which single person signs this brief canonical, and when?"
  owner: Helena Dias
  blocks: Pass 1 consuming this brief as canonical

## Source

- `spec/estate/cover.md` — the drop's cover letter, 2026-06-24
- `spec/estate/meetings/2026-06-02-kick-off.md` — decisions D1–D4, open question Q1
- `spec/estate/meetings/2026-06-09-file-decomposition.md` — Java stays, rebuild beside it
- `spec/estate/policies/privacy.md` — restricted data, 2026-06-16
- `spec/estate/mail/2026-07-14-the-cent-that-will-not-die.md` — Marina on the trailer
- `spec/type-01-card-settlement/` — README, inbound notes, samples, `expected/`
- `spec/README.md` — the five live types; Type 06 not in the drop
- `brain/notebooklm/08-the-lie.md` and packs `00`–`08` — the Second Brain, compiled from the drop
- `evidence/B202607230000001/reconciliation.json` — tonight's MATCHED run

Facts came from the Second Brain packs and `spec/`. Not from `contracts/`, not from reading Java.

## Sign-off

- **Owner/decider:** Helena Dias, Partner Integration — verdict: _pending_
- **Date:** —

A green draft token is structure, never owner authorization. This brief is a draft until the
owner writes canonical, and Pass 1 must not consume an unsigned brief. Drafted by the agent;
gated by `cvg`; the owner signs.
