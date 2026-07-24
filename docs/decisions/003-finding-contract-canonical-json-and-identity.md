# 003 — Closed finding contract, canonical JSON, and finding identity

- Date: 2026-07-24
- Phase: 1, Step 1
- Status: accepted

## Context

Step 1 of the build sequence requires a frozen finding contract before any
detection code: a closed schema, one exact Type `01` expected finding, a
definition of canonical JSON and finding identity, a privacy allowlist, and
stable error codes. The gate is that independent contract tests reject drift,
extra fields, and restricted values.

The brief lists the fields a finding must carry. Two properties are in tension:
a finding must be *byte-stable* for identical inputs (Step 3's gate), and it
must carry a creation time supplied by the runtime (which is never identical).

## Decision

### Shape

One closed JSON Schema (draft 2020-12) at
`dark-factory/contracts/finding.schema.json`. Every object sets
`additionalProperties: false` and lists `required` exhaustively — including the
nested objects, so drift cannot hide one level down. Enumerations are closed:
`finding_code`, `scenario`, `type_number`, `attribution.owner`,
`attribution.confidence`, `terminal.status`, `terminal.stage`, `approval.state`,
and `remediation.state` all enumerate their legal values rather than accepting
free text. Money is `string` with pattern `^-?\d+\.\d{2}$`, never `number`,
because a JSON float cannot represent an exact cent and the whole finding exists
to talk about a one-cent difference.

Top-level members:

| Member | Role |
|---|---|
| `schema_version`, `finding_version` | Contract and instance versioning |
| `finding_code`, `finding_id`, `scenario` | Stable identity |
| `batch` | Exact batch and type identity, contract and layout version |
| `controls` | Declared, computed, and the differences between them |
| `terminal` | Legacy terminal status, code, and stage |
| `isolation` | Sanitized-output and business-mutation observations |
| `continuation` | Peer batch outcomes |
| `attribution` | Owner, basis, and confidence |
| `method` | Detector name, version, and comparison method |
| `references` | Raw, manifest, contract, observation, and detector hashes |
| `observations` | One entry per consumed channel, with independence class |
| `approval`, `remediation` | Both pinned to `not_requested` by the schema |
| `created_at` | Runtime-supplied RFC 3339 UTC timestamp |

`approval.state` and `remediation.state` are `const: "not_requested"`. A finding
that proposes an action is a different artifact requiring its own approval gate;
making the value constant means the schema itself refuses to express one.

### Canonical JSON

`json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))`
encoded UTF-8, with a single trailing newline on the file. Sorted keys make the
byte sequence independent of construction order; `ensure_ascii=True` removes any
dependence on the reader's encoding and makes the restricted-value scan operate
on a known alphabet.

### Identity

`finding_id` is `sha256` over the canonical encoding of the finding with
`finding_id` and `created_at` removed. The digest is stored hex-encoded and
prefixed `sha256:`.

Excluding `created_at` is what makes Step 3's gate meaningful: two runs against
the same immutable observations produce the same `finding_id` and the same
canonical bytes everywhere except the timestamp line. Excluding `finding_id`
itself is required to avoid a self-referential hash. The brief's phrasing —
"creation time supplied by the runtime, not used in deterministic identity" — is
satisfied literally.

Byte-stability is therefore asserted at two levels: `finding_id` equality, and
equality of the full canonical bytes after `created_at` is elided. The published
finding file keeps `created_at`, so an evidence packet still records when it was
produced.

### Expected fixture

`dark-factory/contracts/expected/df-source-001-finding.json` holds the exact
expected Type `01` finding, minus the two runtime-variable members. It is a
Dark Factory contract artifact, not a copy of a legacy one: the legacy oracle
`contracts/types/01-card-settlement/main/expected-df-source-001-finding.yaml`
stays frozen and is read as an independent input, never regenerated.

### Error codes

Stable, enumerated, and versioned in `dark-factory/contracts/error-codes.yaml`.
Detector failures are named (`DF-E-OBSERVATION-MISSING`,
`DF-E-CROSS-BATCH-OBSERVATION`, `DF-E-ATTRIBUTION-INCONCLUSIVE`,
`DF-E-PRIVACY-VIOLATION`, …) so that a refusal is itself a stable, testable
outcome rather than a stack trace.

## Alternatives considered

- **Include `created_at` in identity.** Rejected: byte-stability would become
  untestable, which is the one property Step 3 gates on.
- **Identity over a hand-picked subset of fields.** Rejected: a subset means a
  field can change without changing identity, so drift stops being detectable.
  Hashing everything-but-two is strictly stronger and simpler to explain.
- **Money as JSON `number`.** Rejected outright; `173.44` is not representable
  and the entire finding is about the last cent.
- **Open schema with a documented convention.** Rejected: the brief requires
  the schema to reject unknown fields, and an open schema makes a leak
  additive rather than fatal.
- **Reusing the legacy YAML oracle as the Dark Factory expected fixture.**
  Rejected: it would collapse source of correctness (legacy contract) into the
  observer's own expectation, and the two must be independently comparable.

## Consequences

- Any new finding member is a contract change with a schema-version bump and a
  new expected fixture; it cannot be added silently.
- The contract test suite can assert three separate things — schema validity,
  exact expected-value equality, and canonical-byte stability — because identity
  and encoding are defined independently of the detector code.
- A finding is inert by construction. Nothing downstream can read an approval or
  remediation intent out of it, because the schema admits only one value.
