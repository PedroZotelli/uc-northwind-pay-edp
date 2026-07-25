# Inventory — Type 05 kit

## Delivered and installed by the platform team

The legacy side of this type is **already running.** Prove it before you build
anything:

```bash
make run TYPE=05 SCENARIO=valid-minimal     # accepted
make run TYPE=05 SCENARIO=DF-SOURCE-005     # refused
```

| | Where | Lines |
|---|---|---:|
| **Contract + oracle** — the four YAMLs and `main/` | `contracts/types/05-merchant-fee-assessment/` | 534 |
| Schema — migrations `007`–`010` | `legacy/postgres/migrations/` | 834 |
| PostgreSQL loader | `legacy/postgres/type05_loader.py` | 965 |
| Java privacy boundary | `legacy/processor/.../type05/` | 1,126 |
| Java regression suite | `legacy/processor/src/test/.../type05/` | 997 |
| Source generator | `gen/src/generators/type_05_*.py` | 517 |
| Independent oracle | `validation/oracle/type05_oracle.py` | 487 |
| Workflow adapter | `Type05WorkflowAdapter` | 350 |

**~5,800 lines of ground truth.** The `main/` folder is the part that matters:
five scenario inputs and, for every one, the approved output. That is what will
grade your work, and you may not touch it.

## In this folder, awaiting installation

| Delivered | Install to |
|---|---|
| `tests/test_type05_contract.py` | `tests/contracts/` |
| `tests/test_type05_loader.py` | `tests/unit/` |
| `tests/test_type05_workflow.py` | `tests/unit/` |
| `tests/test_type05_loader_rollback.py` | `tests/postgres/` |

The kit ships its own proof suite. Put each file where the estate's test
discovery will find it.

## Missing — this is the job

| | Status |
|---|---|
| `modern/ingestion/src/northwind_pay/types/type05_*/` — model, parser, schema, writer, handler | ❌ **not built** |
| `modern/dbt/models/bronze/` — detail + control | ❌ **not built** |
| `modern/dbt/models/silver/` | ❌ **not built** |
| `modern/dbt/models/gold/` — reconciliation at the legacy grain | ❌ **not built** |
| `modern/dbt/tests/assert_type05_*` — release gate, conservation, privacy, HALF_UP | ❌ **not built** |
| `tests/modern/test_modern_type05.py` | ❌ **not built** |
| `"05"` in `pipeline.py` (4 maps), `registration.py`, `service.py` | ❌ **not wired** |
| `05` entries in `modern/dbt/models/*/schema.yml`, `sources.yml` | ❌ **not wired** |

Prove it:

```bash
ls modern/ingestion/src/northwind_pay/types/
→ type01_card_settlement  type02_instant_payment_events
  type03_payment_slip_settlement  type04_ted_transfer_settlement
```

Four. Not five.

## The arithmetic

**~5,800 lines arrived. About 1,000 is missing.**

That thousand is the work. The other 5,800 is what will grade it.
