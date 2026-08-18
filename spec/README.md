# Spec — inbound customer drop

This folder is how the **customer arrives**. Until the document factory
exists, we mimic a real engagement drop: Share Folder, not a repo tour.

The picture is KurvPay EDP, distilled. There a type did not arrive as
four YAMLs. It arrived as a vendor PDF, a SQL Server table dump, two
dates of an insert proc, a sample that did not quite match the proc,
and a meeting note that contradicted all three. The work was
**unpack, question, decide, then translate**.

The week works Types `01`–`05`. Those packs are written **in advance**
so day one is a customer drop, not a hunt through `contracts/`. Type
`06` is not in this folder. It arrives on day five as the factory's
unseen kit — the flywheel.

> **No oracle, no build.** A pack that cannot be adjudicated is refused
> before any modern code exists.

## The experience this drop is for

The week is not "open `contracts/` and write a parser." The week is:

1. Receive a messy customer bundle.
2. Unpack it with Converge / Seamwise / Task-Spec / Brief-Spec.
3. Hold the meetings the documents imply.
4. Find what is true, what is stale, and who lied.
5. Only then build the modern vertical and prove it.

Data analysts, software engineers, and platform people are in the same
room. The drop has to give each of them something to do: a layout to
read, a control to recompute, a contradiction to escalate, a privacy
rule to enforce.

Daily agenda is still open. This page is the **inbound**, not the
timetable. The type split is closed: `01`–`05` all week, `06` only
when the factory runs.

## Two layers, like Kurv

Kurv had `notes/` (the engagement) and `specs/{type}/` (each file).
We keep that split.

```text
spec/
├── README.md                 this contract
├── estate/                   one drop for the whole customer
│   ├── cover.md              who they are, what they want, what done means
│   ├── meetings/             kick-off, tech syncs, async handoffs
│   ├── mail/                 threads that "just forward the folder"
│   └── policies/             privacy, rounding, "do not fix the source"
└── type-NN-<slug>/           one inbound pack per file type
    ├── inbound/              what they mailed — messy on purpose
    ├── samples/              raw bytes + checksums
    └── expected/             the oracle (sanitized, recon, refusals)
```

`estate/` is shared. A type pack never repeats the kick-off. It may
contradict it. That contradiction is the work.

Type `05`'s current `01-`…`07-` tree is a **thin compiled example**.
It gets the same inbound shape as `01`–`04` so the week has five
equal drops. Do not leave it as the tidy exception.

## What `estate/` contains

Fictional NorthWind Pay / partner voices. Not Kurv names, not TSYS
layouts, not real PCI.

| Artifact | Job in the room |
|---|---|
| Kick-off note | Scope, stack, who owns SFTP, who owns privacy |
| File-decomposition sync | "Java stays. You rebuild beside it." |
| Async handoff | "Folder is in the share. Walk through next week." |
| One angry / tired thread | A control that has been wrong for months |
| Privacy policy | What must never leave, in customer language |
| Rounding note | `HALF_UP` stated in one place, implied elsewhere |

Every note follows a short template (attendees, decisions, actions,
open questions, implicit signals). That is how Kurv notes were
usable a month later.

## What each type pack contains

Mirror a Kurv `specs/{type}/` drop. Filenames may look like a customer
exported them, not like we designed a repo.

| They mail | Looks like | Why it is there |
|---|---|---|
| Vendor-ish layout | PDF or long markdown, field positions, "see page 14" | Translation starts here |
| Table definitions | `.txt` / `.sql` dump | Analysts and warehouse people land here first |
| Insert / apply proc | One or two dated copies | The legacy "how we post" — not Java, not to be ported |
| Email / Slack export | "Keith said most columns aren't loaded" | Planted gap between proc and table |
| Meeting excerpt | Type-specific walk-through | Open questions with owners |
| Raw samples | Happy, boundary, type edge, malformed, source lie | Real bytes |
| Expected sanitized + recon | For accepted samples | The oracle |
| Expected refusals | Malformed + source lie, stable code | The other half of the oracle |

They never mail the modern parser. If they did, the referee would
score a copy.

The five scenario **roles** stay. Customer names may differ. We map;
we do not drop a role.

## Good stuff and minor issues

The drop must be mostly right. A pack that is only traps teaches
cynicism, not engineering.

**Good (the majority):**

- Layout that actually matches the happy-path sample
- Privacy rule that is load-bearing and consistent
- Reconciliation that the live legacy run already satisfies
- A source-lie file whose declared total is wrong by one cent

**Minor issues (planted, findable, not sabotage):**

| Class | Example | What the room should do |
|---|---|---|
| Stale revision | Proc dated earlier than the table dump | Ask which one is current |
| Unused columns | Table has fields the proc never writes | Do not invent Gold from dead columns |
| Name drift | Meeting says "net fee"; layout says "assessed fee" | One ADR, then one vocabulary |
| Implied rounding | Email says "normal rounding"; Type `05` needs `HALF_UP` | Prove it on the sample, do not guess |
| Two truths | Cover letter vs trailer control | Keep the declaration; compute independently |
| Missing expected | One "nice to have" sample with no oracle | Factory must refuse that sample, not invent it |

Do **not** put an `issues.md` in the student pack. That is an answer
key. The instructor key, if we need one, lives under `plans/` after
the drop is compiled.

## How the week uses the methods

The drop is the input to the method stack. It is not a substitute
for it.

| Method | What it does with the drop |
|---|---|
| **Brief-Spec** | Each day has a type: unpack is exploration, a contradiction is review, a parser is implementation |
| **Converge** | Pass 0–1 compile the messy folder into a BRD / tech-spec. Pass 2 writes ADRs for money, privacy, which doc wins. Pass 4 attacks the planted issues **before** code |
| **Seamwise** | Seams from the drop: raw → sanitize → stage → apply → report. Ownership must be one per handoff |
| **Task-Spec** | Only after Consensus. Each leaf has evals against `expected/`. No eval, no task |
| **Dark Factory seed** | [`plans/dark-factory.md`](../plans/dark-factory.md) — later, the same drop is what the unattended line consumes |

The room should spend real time in "meetings" that the notes set up:
walk the unused columns, pick a vocabulary, refuse a sample that has
no oracle. That is the ultimate experience — not slides about it.

## This folder vs `contracts/`

| | `spec/` | `contracts/types/` |
|---|---|---|
| Role | How the request **arrives** (messy) | Source of correctness once **installed** (clean) |
| Audience | The week, the factory | DataGen, Java, oracles |
| Planted issues | Yes, in inbound prose and dated dumps | **Never.** Contracts stay executable truth |

The factory reads the pack as if the customer sent it. After
understanding, the signed contract in `contracts/` is still what
Java and the oracles obey. We do not "fix" `contracts/` because a
meeting used the wrong noun.

## On this tree today

| Piece | Status |
|---|---|
| This page | The drop contract. Week = Types `01`–`05`. Day five = Type `06`. |
| [`estate/`](estate/README.md) | Compiled. Cover, five meetings, two mails, two policies. |
| [`type-01-…`](type-01-card-settlement/README.md) | Compiled. inbound / samples / expected |
| [`type-02-…`](type-02-instant-payment-events/README.md) | Compiled |
| [`type-03-…`](type-03-payment-slip-settlement/README.md) | Compiled |
| [`type-04-…`](type-04-ted-transfer-settlement/README.md) | Compiled |
| [`type-05-…`](type-05-merchant-fee-assessment/README.md) | Compiled. Same shape as the others. |
| Type `06` | **Not here.** Sealed until day five. No empty folder. |

Instructor key (not for the room): [`../plans/spec-instructor-key.md`](../plans/spec-instructor-key.md).

## Gate before a pack is written

A type pack is ready only when:

1. Accepted samples have expected sanitized rows **and** recon.
2. Malformed and the source lie have expected refusals and a stable code.
3. Privacy is stated in customer language **and** matches `contracts/`
   once installed.
4. Tolerances are zero in the oracle half.
5. Every planted issue is discoverable from the drop itself.
6. Nothing requires editing `legacy/`, `gen/`, or `infra/` to become true.

Fail any one and we do not write that type.

## What is written in advance

1. `estate/` — cover, five notes, two mails, two policies.
2. Types `01`–`05` — inbound / samples / expected. Five equal drops.
3. Instructor key under [`plans/spec-instructor-key.md`](../plans/spec-instructor-key.md).
4. Type `06` — **not written.** Sealed until day five.

The room starts on a drop, not on a pointer. The factory learns on a
type it has not already unpacked.
