# Legacy PostgreSQL

This folder owns the sanitized-file loading boundary, governed business
procedures, operational legacy tables, and reconciliation reporting.

## Loader map

| File | Responsibility |
|---|---|
| `loader_common.py` | Shared batch controls, terminal finalization, rejection recording, and CSV quarantine helpers |
| `type01_diagnostics.py` | Type 01 privacy-safe, read-only control recomputation |
| `type01_loader.py` | Type 01 card-settlement validation, `COPY`, procedures, and reconciliation |
| `type02_loader.py` | Type 02 instant-payment-event loading |
| `type03_loader.py` | Type 03 payment-slip-settlement loading |
| `type04_loader.py` | Type 04 TED-transfer-settlement loading |
| `type05_loader.py` | Type 05 merchant-fee-assessment loading |

The common module does not own a business layout. Each numbered loader owns
the parsing and PostgreSQL behavior for exactly one file type.

## Batch path

```text
/csv/outgoing/<batch>
  -> /csv/processing/<batch>
  -> validate sanitized manifest, checksum, lineage, and CSV
  -> COPY into the type staging table
  -> execute governed legacy procedure
  -> refresh reporting reconciliation
  -> commit only when the controls match
  -> /csv/archive/<batch>
```

An invalid sanitized batch is isolated under `/csv/quarantine/<batch>`.
Unrelated batches remain eligible for processing.

## Database structure

- `migrations/` contains immutable, checksummed schema evolution.
- `procedures/` contains the governed PL/pgSQL entrypoints.
- `init/` creates the least-privilege application role for a fresh database.
- `migrate.py` applies migrations and rejects checksum drift.

Use `make migrate` to apply schema changes and `make test-postgres` to exercise
the real `COPY`, procedure, permission, rollback, and reconciliation boundary.
