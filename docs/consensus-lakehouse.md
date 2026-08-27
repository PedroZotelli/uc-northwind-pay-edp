# Consensus — Type 01 dlt → Gold (lakehouse addendum)

Pass 4. The barrier for seam 2. Papers live in `docs/`, not `cvg/docs/`.
**Do not overwrite** [`consensus.md`](consensus.md). Ingest → landing
stays canonical. Keep **173.44**. Do not patch the trailer. Do not
copy Gold from Postgres.

**Signed.** This lakehouse plan is the right thing to build. The
machine may take Pass 5 (Type 01 remainder + lakehouse leaves). The
eval is the judge of done. Keep **173.44**.

- Date: 2026-08-26
- Author of ADRs 0007–0011 / seam 2 legs: Grok seat (Night 3 Constructor)
- Signed by: **Luan Moreno, Agentic Lead**
- Verdict: **canonical** (lakehouse steel thread only)
- Steel thread: Type 01 dlt → Gold (ADR 0007–0011, `docs/seams.md` seam 2)
- Ingest sign remains [`consensus.md`](consensus.md) 2026-08-25
- Fictional brief owner (Helena Dias, Partner Integration) remains in
  the BRD; this barrier is signed by the Agentic Lead.

## What `cvg` actually ran

Night prompt says `cvg consensus --sign --json`. That verb is **not**
on `cvg` 0.2.0 (same as Tuesday). Pass 4 on the referee is still
`cvg review --adversary` / `--check` / `--resolve`.

Default `taskspec` on PATH is **3.9.0**. Converge 0.2 requires **3.8.x**.

```text
cvg consensus --sign --json
```

```json
{
  "contract": "ConvergeCLIResult/v1",
  "ok": false,
  "command": "consensus",
  "exit_code": 3,
  "changed": false,
  "error": {
    "code": "ENGINE_UNAVAILABLE",
    "message": "error: incompatible Task-Spec engine '3.9.0' at /Users/luanmorenomaciel/.local/bin/taskspec — Converge 0.2 requires 3.8.x"
  },
  "meta": { "tool": "cvg", "cvg_version": "0.2.0" }
}
```

`CHECK_CONSENSUS` is **not green**. Cross-family dispatch was **not**
run: there is still no `cvg/` workspace / swimlane tree. A dated
signature in this file **counts** (`run/d3/07-consensus.md`).

## Contradiction walked (dlt-as-parser vs register; Gold vs Postgres)

- Mail (2026-06-09): second reader of the same raw bytes, then
  Parquet, then Bronze / Silver / Gold. That sketch is **mail**. It
  does not name dlt and is not a grain.
- Constructor might treat dlt as a second parser, or copy
  `reporting.card_settlement_reconciliation` into DuckDB and call it
  Gold.
- Judge: landing is immutable sanitized Parquet (ADR 0001). dlt
  **registers landing only** (ADR 0007). DuckLake / DuckDB are
  **local** (ADR 0008). Paid observation is
  `reporting.card_settlement_reconciliation`, grain `batch_id` +
  `currency` — staging is not paid, and Postgres is not the modern
  store. Keep **173.44**. Refuse. Zero Parquet. Zero Gold for that
  batch.

**dlt does not re-parse. Gold is not a warehouse copy. Keep 173.44.**

## Objections (default-to-refuted)

Same-family attack on ADRs 0007–0011 + `docs/seams.md` seam 2.
Not a substitute for `cvg review --adversary codex|kimi`.

| ID | Objection | Disposition |
|---|---|---|
| L-1 | Author and reviewer are the same seat. Converge requires a **different family**. | **ACCEPTED** — owner: Luan Moreno. Same as ingest C-1. No `cvg/` swimlane tree. Does not block this sign. |
| L-2 | dlt will re-parse raw / own money / tokenize PAN. | **FIXED** in ADR 0007 and seam 2 Register: dlt registers `modern/landing/` only. |
| L-3 | Gold is a copy of Postgres reporting, or staging is paid. | **FIXED** in ADR 0008–0009: local DuckLake/DuckDB; Gold grain `batch_id`+`currency`; staging is not Gold; Postgres is observation. |
| L-4 | Gold should “fix” trailer 173.44 to 173.45 so MATCHED. | **FIXED** in ADR 0005 / 0010 / 0011. Keep 173.44. Zero Parquet. Zero Gold. `CONFIRMED_SOURCE_DEFECT`. |
| L-5 | dbt will retokenize or re-decode overpunch. | **FIXED** in ADR 0010. Parser already did privacy + Decimal. |
| L-6 | Bronze / Silver / Gold are three new seams (or Types 02–05 sneak in). | **FIXED** in `docs/seams.md`: they are **legs** on seam 2. Types `02`–`05` refused tonight. |
| L-7 | Dagster / FastAPI belong in tonight’s ADRs. | **FIXED** — still parked (ADR 0006 rows 8–9). Seam 2 must not write them. |
| L-8 | This sign should overwrite ingest `consensus.md` to smuggle a lakehouse. | **FIXED** — this file is the addendum. Ingest verdict unchanged. |
| L-9 | Paid / match keys were guessed joins. | **FIXED** in ADR 0009 / 0011: OntoLayer paid grain `batch_id`+`currency`; contract replay `batch_id`+`source_record_number`. |
| L-10 | Seam 1 ingest cut needs a recut now that Gold exists. | **ACCEPTED** — owner: Constructor. Seam 1 Sense/Claim/Emit stand. Constructor does not rewrite landing. |

No objection remains unresolved. None of them is a license to code
until Pass 5 leaves are gated.

## Open questions (do not block the sign; they block the **machine** gate)

1. Pin `taskspec` 3.8.x (`CVG_TASKSPEC_BIN` or PATH). Owner: host.
2. `cvg init` so review / evidence doctor have a workspace. Papers
   still live in `docs/`. Owner: host.
3. Optional: project `docs/seams.md` into `cvg/swimlanes/<seam>/`.
   Owner: Luan Moreno.
4. Exact dlt register-vs-load **API** is an implementation leaf, not
   a grain. Role is closed (register landing only). Owner: Constructor.
5. Dagster, FastAPI, Types `02`–`05`: Day 4. Owner: Helena Dias.

## Sign-off

I sign that this **lakehouse** plan is the right thing to build, and
I hand it to the machine. I do not sign that the code will be
correct — that is the eval. I do **not** recut Tuesday’s ingest sign.

| Field | Value |
|---|---|
| Signed by | **Luan Moreno, Agentic Lead** |
| Date | **2026-08-26** |
| Verdict | **canonical** (dlt → Gold) |
| Ingest sign | **unchanged** — `docs/consensus.md` 2026-08-25 |
| FIXED | L-2, L-3, L-4, L-5, L-6, L-7, L-8, L-9 |
| ACCEPTED | L-1, L-10 (named owners above) |
| Keep | **173.44** |

Pass 5 may write Type 01 remainder + lakehouse leaves in
`docs/tasks/`, `signed_off` false until each leaf’s own gate. No
Gold in `modern/` until those leaves are executed. Do not edit
frozen `legacy/`, `contracts/`, `gen/`, or `infra/`. Do not author
Types `02`–`05`. Do not author Dagster.

## Referee vs this sign

Bootcamp proof (`run/d3/07-consensus.md`): dated signature here
**counts**. The room can point at **this** sign **and** Tuesday’s
ingest sign.

Converge referee `CHECK_CONSENSUS` is still not green. That is
host/tooling, not a refusal of this plan.
