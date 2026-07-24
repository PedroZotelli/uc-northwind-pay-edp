# 006 — Evidence-based attribution and the conclusiveness rule

- Date: 2026-07-24
- Phase: 1, Step 4
- Status: accepted

## Context

Step 4 requires attributing the discrepancy to the source system of record
"because the raw declaration is wrong while independent observations agree",
keeping detection, attribution, and explanation as separate fields, and failing
closed when observations do not support one attribution. Its gate: "removing any
required independent observation prevents a conclusive attribution."

That gate only bites if the required observations are genuinely independent. An
inventory of what the legacy baseline actually publishes for a quarantined
`DF-SOURCE-*` batch shows they are not equally independent:

| Channel | Type `01` | Types `02`–`05` |
|---|---|---|
| `java-run.json` | Independent parse of the raw bytes | Independent parse of the raw bytes |
| `postgres-diagnostic.json` | Independent SQL aggregation (`mode: read_only`) | Projection of the Java result (`mode: source-parser-observation`) |
| `control.rejects` (live) | Persisted by the loader component | Persisted by the loader component |
| `control.batches.source_controls` (live) | Persisted source declaration | Persisted source declaration |
| SFTP quarantine bundle | Transport-level terminal observation | Transport-level terminal observation |
| `expected-diff.json` | Contract oracle comparison | Contract oracle comparison |

Claiming five independent computations when Types `02`–`05` have one would be
the kind of overclaim the plans exist to prevent.

## Decision

### Every observation carries its own independence class

`independent_computation` (a component that computed the control from a source
it parsed itself), `persisted_record` (a distinct component that durably
recorded the control), `derived_projection` (a restatement of another
component's result), `transport_observation`, and `contract_comparison`. The
class is a member of the finding, so a reader never has to guess how much a
given corroboration is worth. `postgres-diagnostic.json` is classified from its
own `mode` member, so Type `01` earns `independent_computation` and Types
`02`–`05` earn `derived_projection` — from the data, not from a table I wrote.

### Conclusiveness rule

`attribution.confidence` is `conclusive` only when all three hold:

- **A1 — the declaration is source-owned and internally consistent.** The
  declared controls in the source manifest equal the declared controls the
  processor decoded from the raw file's own trailer, and equal the declaration
  persisted in `control.batches.source_controls`. Two of those are independent
  source-owned artifacts bound by hash, so agreement rules out transport damage
  or a manifest-only error and places the defect in what the source system
  computed.
- **A2 — every component that computed the controls agrees**, and at least one
  of them is an `independent_computation` rather than a restatement, so a chain
  of projections can never look like corroboration. Required channels:
  `java-processor`, `postgres-diagnostic`, `postgres-control-plane`.
- **A3 — at least one control differs** between the declared and computed sets.

Each rule requires its **complete** channel set, not "at least two of them".
The first implementation used the weaker form and it made the Step 4 gate
vacuous: with three declarations and three computed reports available, an
"at least two" rule survives the loss of any single channel, so withholding one
still produced a conclusive attribution and the probe proved nothing. Demanding
the whole set turns the available redundancy into strength instead of slack,
and it is the reading that matches the brief's "fail closed when observations do
not support one attribution".

Otherwise `attribution.confidence` is `inconclusive`, `attribution.owner` is
`undetermined`, and the CLI refuses with `DF-E-ATTRIBUTION-INCONCLUSIVE`.

Completeness is a separate predicate. A finding is complete only if attribution
is conclusive **and** the terminal classification, isolation, and peer
continuation are all observed (Step 5). Attribution answers "who owns it";
completeness answers "is this finding safe to publish".

### Detection, attribution, and explanation stay separate

`controls` holds what differs and nothing about blame. `attribution` holds owner,
basis, and confidence. `method` holds how the comparison was made. There is no
prose "explanation" member: the basis list — each entry naming the rule, the
contributing channels, and whether it was satisfied — *is* the explanation, and
it is machine-checkable. A sentence would be a model judgment, and model
judgment is not correctness evidence.

### The gate is executed, not argued

`darkfactory.attribution` exposes a withhold set. The end-to-end suite runs the
attribution once per required channel with that channel withheld and asserts
each run yields `inconclusive`. That turns "removing any required independent
observation prevents a conclusive attribution" into five executed probes for
Type `01` rather than a claim in a document.

## Alternatives considered

- **"At least two corroborating channels" instead of the complete set.**
  Rejected after implementation showed it makes the Step 4 gate unfalsifiable,
  as described above.
- **Require two `independent_computation` channels for every type.** Rejected:
  Types `02`–`05` cannot satisfy it without the detector parsing raw bytes
  itself, which would make the observer a second implementation and put it
  outside its read-only mandate.
- **Let the detector recompute the control identity** (net from credit minus
  debit, and so on) as a second independent channel. Rejected: those formulas
  are not stated in the frozen contracts, so authoring them would create a new
  source of correctness owned by the observer — exactly the role-merging the
  plans forbid. The declaration-consistency check in A1 gets a real independent
  cross-check out of two source-owned artifacts without inventing a rule.
- **A numeric confidence score.** Rejected: it invites tuning a threshold until
  a gate passes. Two named states with an explicit rule cannot be tuned quietly.
- **Attributing to a named upstream component.** Rejected: the observations
  identify the system of record as the owner and support nothing finer. The
  finding says exactly what the evidence supports.

## Consequences

- Types `02`–`05` reach `conclusive` on a strictly weaker corroboration set than
  Type `01`, and the finding says so in `observations[].independence`. A reader
  can see the difference without reading this record.
- If legacy ever gains a genuinely independent recomputation for Types `02`–`05`,
  the rule needs no change; the classifier will pick it up from `mode`.
- Fail-closed means a torn-down or partially observed runtime yields no finding
  at all, which is the intended behavior.
