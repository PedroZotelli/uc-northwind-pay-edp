# 004 — Privacy allowlist and restricted-value scan

- Date: 2026-07-24
- Phase: 1, Step 1
- Status: accepted

## Context

The finding must carry "no PAN, CPF, CNPJ, account, name, prohibited
description, raw row, or unrestricted exception text", and the schema "must have
a restricted-value scan". A leak of a restricted value into a produced artifact
is a hard-stop condition for the whole run.

A pattern-only scan is the obvious approach and it is not sufficient here. Batch
identities look like `B202607230000004` — a sixteen-digit run — and would trip
any naive PAN detector, while a genuine leak of a name or a description matches
no numeric pattern at all.

## Decision

Three independent layers, all of which must pass before a finding is written.

### Layer 1 — closed schema (structural)

The schema (DR-003) admits no unknown members, and every free-form member is
either enumerated or constrained by pattern. There is no `message`, `detail`, or
`exception` member anywhere in the finding, so unrestricted exception text has
nowhere to land by construction. This is the layer that makes the other two
tractable: the scanner only ever sees values whose shape is already bounded.

### Layer 2 — field allowlist (positive)

`dark-factory/contracts/privacy-allowlist.yaml` enumerates every leaf path a
finding may contain, together with the value class permitted there
(`batch-id`, `sha256`, `money`, `count`, `enum`, `identifier`, `timestamp`,
`contract-path`, `type-number`). The scanner walks the finding and refuses any
leaf whose path is absent from the allowlist or whose value does not match its
declared class. This is a positive allowlist, not a denylist: a value is safe
because it was approved, not because it failed to look dangerous.

The Type `01` "approved safe transaction reference" that legacy may retain in
its own evidence is deliberately **not** allowlisted for findings. The detector
has no need for it, so it does not carry it.

### Layer 2b — identity binding

Layer 2a proves a value has an approved *shape*. Layer 2b proves the
identity-bearing values are the *expected* ones: `scenario`, `batch.batch_id`,
`batch.contract_code`, `batch.type_number`, and `terminal.code` must equal the
values in the frozen scenario contract, and every peer must be one the contract
names. This closes the last route by which an unapproved string could ride along
inside a correctly shaped member.

### Layer 3 — restricted-corpus scan (negative)

The scanner extracts the restricted identifiers that actually exist in the
frozen raw fixture for the batch under analysis — PAN, CPF, and CNPJ digit runs
— and asserts none of them appears in the finding's placeable values. Where
layer 2 asks "is this value approved?", layer 3 asks "did anything from the
restricted source reach the output?" — including routes nobody anticipated.

Three scoping rules keep the layer from reporting violations that carry no
restricted content, each of which was found by running it:

- **Repeated-digit runs are excluded from the corpus.** Fixed-width layouts
  zero-pad their numeric fields, so `00000000000` is padding, not an identifier;
  keeping it flagged every finding containing a hash of zeros.
- **Digit windows inside contract-bound identities are exempt.** A batch
  identity is fifteen digits and appears in the fixture's own header and
  trailer, so it yields windows that are structural. The exemption is derived
  from the frozen scenario contract, not from a hand-maintained list of allowed
  numbers.
- **Digest-classed members are not scanned.** A digest's value is determined by
  the bytes it references rather than chosen by the detector, so an identifier
  cannot be *placed* in one — while a 64-character hex string coincidentally
  containing an eleven-digit run is common enough to matter.

**Names and free-text descriptions are deliberately not corpus-matched.** The
Type `05` raw header uses the same business vocabulary as the control names
themselves — `gross`, `amount`, `assessed` — so an alphabetic corpus match
reports a violation for `gross_amount`, a value carrying no restricted content.
Those classes are closed off structurally instead: every string member of a
finding is an enumerated value, a pattern-bound identity checked against frozen
contract truth, or a control name derived from a JSON *key* of the legacy
processor result. A name can never become a key, so it has no route in.

Layer 3 reads the frozen fixture read-only and holds the extracted tokens in
memory only. They are never written anywhere, never logged, and never included
in a failure message; a violation reports the finding path and the value class,
never the value.

Because layers 1 and 2 leave no member that can plausibly carry an identifier,
layer 3 functions as a canary: the security suite injects a sixteen-digit PAN
into `batch.contract_code`, whose `[A-Z0-9_]{1,16}` pattern admits it, and
asserts layer 3 catches it alone. That keeps the layer meaningful if a future
contract change opens a hole.

### Failure behavior

Any violation raises `DF-E-PRIVACY-VIOLATION`, the finding is not written, and
the CLI exits non-zero. There is no sanitize-and-continue path: a detector that
can quietly redact is a detector whose output cannot be trusted to be complete.

## Alternatives considered

- **Regex denylist only.** Rejected: false-positives on batch identities and
  false-negatives on names make it both noisy and weak.
- **Allowlist only, without the corpus scan.** Rejected: it proves that approved
  fields hold approved shapes, not that nothing leaked through an approved field
  — a name is a plausible `identifier`-shaped string.
- **Corpus scan only.** Rejected: it cannot see a leak from a batch whose
  fixture the scan did not load, and it says nothing about fields that are
  merely inappropriate rather than restricted.
- **Alphabetic corpus matching for names and descriptions.** Implemented, then
  removed: it reports a violation for `gross_amount` on Type `05` because the
  raw header and the control vocabulary are the same words. Exempting the
  collisions by hand would have meant a list that could also mask a real leak —
  a merchant genuinely named "Gross" would become invisible. The structural
  argument above is the honest replacement.
- **Also matching against a digits-only projection of the whole document.**
  Rejected: it glues unrelated numbers across field boundaries, manufacturing
  matches no real leak would produce, and a "leak" that exists only after every
  delimiter is stripped is not a leak of a readable value.
- **Redact on violation and continue.** Rejected: see above.

## Consequences

- Adding a member to the finding requires an allowlist entry as well as a schema
  change; forgetting one fails closed rather than open.
- The security suite can adversarially inject each restricted class into a
  synthetic finding and assert that each of the three layers independently
  refuses it, which is what makes "privacy-clean" a proven property rather than
  an assertion.
- The scan costs one read of an already-frozen fixture per finding, which is
  negligible and keeps the check bound to real data rather than to a
  hand-maintained list of "bad strings".
