# Spec — inbound customer packs

This folder is how a **customer request arrives**. Until the document
factory exists, we mimic that drop: a bundle of files, not a repo tour,
not a copy of `legacy/`.

The factory's job on a pack is project understanding, then translation,
then proof. It does not invent the truth. If the pack cannot be
adjudicated, the factory refuses **before** doing any work.

> **No oracle, no build.**

Approve this page. After that, compile one pack per type the week will
touch. Do not compile from this README being written — compile from it
being accepted.

## What a pack is

A pack is everything the customer would hand a partner to modernize one
file type. Style may vary. Numbered folders like Type `05`'s `01-`…`07-`
are one compiled example, not the required shape.

Every pack must answer the same questions, whatever the filenames:

| The customer must send | Why the factory needs it |
|---|---|
| **Cover** — who they are, what the file does, what "done" means | Intake. Without a request there is nothing to accept. |
| **How to read the bytes** — encoding, grammar, money, dates, rejection codes | Parser. The factory must not guess a layout. |
| **What may leave** — restricted fields and the approved transform | Privacy gate. A leak stalls the type. |
| **What sanitized output looks like** — columns, types, grain | The interface to reproduce. |
| **How it must add up** — controls, tolerances (zero), success criteria | Gold and golden-match. |
| **Raw samples** — at least happy, boundary, malformed, and one source lie | Real bytes. Checksums belong with them. |
| **Expected sanitized rows** for every accepted sample | The oracle for success. |
| **Expected refusals** for malformed and the source lie | The oracle for quarantine. Status, stable code, no rows. |

Optional, and useful when they already have a working path:

| They may also send | Why |
|---|---|
| One observed run from their current system | So the factory can compare without calling their plant |
| A source manifesto / control totals as they declare them | System of record, even when it is wrong |

They never send the translation. If they sent a finished parser, the
referee would be comparing a copy with its original.

## What we produce from a pack

That is the factory, not the customer:

| We hand back | Meaning |
|---|---|
| Project understanding | What this type is, what it exercises, what must never happen |
| The modern vertical | model → parser → schema → writer → handler, then lakehouse |
| Evidence | golden-match resolved, unexplained count zero, privacy-safe packet |
| Classification of the source lie | `CONFIRMED_SOURCE_DEFECT` — declaration preserved, batch refused |

Folder `07-deliverable-shape/` in the Type `05` example is **our**
target shape, not something the customer mailed.

## Five scenarios, always

The base already uses this vocabulary. A compiled pack should too, even
if the customer used other names — we map, we do not drop a role.

| Role | What it proves |
|---|---|
| Happy path | The smallest complete accepted batch |
| Boundary | Extreme but legal values |
| Type-specific edge | The reason this layout exists (overpunch, escapes, lots, returns, `HALF_UP`, …) |
| Malformed | Transport or grammar. Must be refused. |
| Source lie | Declared control contradicts the rows. Compute the truth, keep the declaration, refuse. |

The source-lie file is the one that matters. Repairing the customer's
number destroys the evidence that something upstream is broken.

## This folder vs `contracts/`

| | `spec/` | `contracts/types/` |
|---|---|---|
| Role | How the request **arrives** | Source of correctness once **installed** |
| Audience | Factory intake | DataGen, Java, oracles, later modern |
| Editable after sign-off | No — a new pack version arrives | No — versioned, never patched to pass a gate |

A compiled pack may duplicate YAML and fixtures that also live under
`contracts/`. That is deliberate. The factory reads the pack as if the
customer sent it. It does not browse `legacy/` for the answer.

## On this tree today

| Pack | Status |
|---|---|
| [`type-05-merchant-fee-assessment/`](type-05-merchant-fee-assessment/INVENTORY.md) | Compiled example. Five scenarios, expected outs, one legacy execution, deliverable shape. |
| Types `01`–`04` | **Not compiled.** Truth already lives in `contracts/types/`. Packs wait on approval of this page. |
| Types `06+` | Not reserved. A later kit arrives the same way: a pack, not an empty folder. |

Type `05` is already on the legacy line (`make run TYPE=05`). The pack
is the inbound envelope for the **modern** vertical, not a second
legacy implementation.

## Gate before compile

A pack is ready to compile only when:

1. Every accepted sample has expected sanitized rows **and** expected
   reconciliation.
2. Malformed and the source lie have expected refusals with a stable
   code.
3. Privacy transforms are stated, not implied.
4. Tolerances are zero.
5. Nothing in the pack requires editing `legacy/`, `gen/`, or
   `infra/` to become true.

Fail any one of those and the factory must not start.

## After you approve this page

Compile one pack per type the week will work, from the signed
contracts and the live fixtures — same contents as the table above,
style free. Type `05` stays as the first compiled example. Types
`01`–`04` get the same kind of envelope so the room receives a
customer drop, not a pointer into `contracts/`.
