# 009 — Cross-type expansion invariants

- Date: 2026-07-24
- Phase: 3, Milestone M5
- Status: accepted

## Context

DR-008 settled the modern architecture against Type `01`. Expanding to Types
`02`–`05` surfaced four decisions that only appear once a second type exists,
each found by a gate failing rather than by design review.

## Decisions

### 1. Rejection codes come from the contract, never from the implementation

Each type's `layout.yaml` declares `canonical_rejection_codes`. Modern emits
those exact codes.

The first Type `05` implementation invented `INVALID_QUOTING` where the contract
declares `INVALID_CSV_QUOTING`, and golden-match classified the mismatch as
`APPROVED_BEHAVIOR_CHANGE` — a defensible-looking verdict that was wrong. An
independent implementation owes the contract's stable vocabulary; independence
is about not sharing *code*, not about not sharing *names*. Accepting the
classification would have let a one-line fix be recorded as an approved
divergence, and every future reader would have inherited that.

### 2. dbt models are tagged per type and built per type

Every model and singular test carries a `type_NN` tag and `dbt build` runs with
`--select tag:type_NN`. Without it, adding Type `05` broke Type `01`'s gate,
because a single-type run tried to build models over landing tables that
legitimately did not exist yet. Scoping makes expansion safe in both directions:
a new type cannot break an existing one, and an existing one cannot mask a new
one's failure.

### 3. Comparison logic discovers structure rather than naming it

Two comparisons were written against Type `01`'s vocabulary and silently did the
wrong thing on another type:

- the source-defect comparison looked for `declared_net_amount`/
  `computed_net_amount`, so Type `05`'s `assessed_fee` disagreement produced no
  difference at all — the batch was correctly rejected, but the finding that
  explains *why* was missing;
- the record comparison assumed a `source_record_number` column, which Type `03`
  does not have; it keys by `source_record_number_a`, the A segment of its pair.

Both now derive their keys from the data or the approved artifact. A hard-coded
name that happens to be right for four types out of five fails silently on the
fifth, which is the worst available failure mode.

### 4. Each token scope keeps its own key and canonical input

Five tokenizations exist across the estate — card PAN, instant-payment document,
payment-slip reference, party, and bank account, plus the TED account — and each
has its own environment key and its own canonical input. The TED account's is
`ispb:branch:account`, not the account number alone.

The first implementation hashed the account number by itself. The tokens were
well-formed, deterministic, and stable, so every structural test passed; only
the byte-for-byte comparison against the approved sanitized CSV caught it. That
bug would have made the same account number at two different institutions share
a token — a privacy defect invisible until someone joins on it.

## Alternatives considered

- **Letting modern own its rejection-code vocabulary and classifying every
  mismatch as `APPROVED_BEHAVIOR_CHANGE`.** Rejected: it makes the
  classification meaningless and hides fixable defects.
- **Building all dbt models on every run.** Rejected: it couples the types
  together exactly where they should be independent.
- **A per-type registry mapping control names and record keys.** Rejected where
  the value is derivable: a registry is another place to forget an entry. It is
  used only where derivation is impossible — the control plane's generic column
  names, which `scenarios.yaml` binds explicitly.
- **One shared tokenization key.** Rejected: the privacy contracts require
  separated secrets, and shared keys would let tokens correlate across scopes
  that are meant to be independent.

## Consequences

- Adding a sixth type means a parser, a schema, a writer, a handler, tagged dbt
  models, scenario bindings, and tests — with no change to the comparison or
  orchestration layers.
- The byte-for-byte comparison against each contract's approved sanitized CSV is
  the highest-value test in the modern suite. It is the only check that caught
  the token-composition defect, and it caught it immediately.
