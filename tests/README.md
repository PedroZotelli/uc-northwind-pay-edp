# Verification map

Type 01 was the first implemented vertical slice. Its behavior is now exposed
through the same named test surfaces as the later types instead of being
hidden inside generic prototype tests.

## Type 01 coverage

| Boundary | Named proof |
|---|---|
| Contract bytes and layout | `gen/tests/contract/test_type_01_contract.py` |
| Cross-component contract oracle | `tests/contracts/test_type01_contract.py` |
| Generator encoding | `gen/tests/unit/test_type_01_encoding.py` |
| Generator bundle integration | `gen/tests/integration/test_type_01_generation.py` |
| Generator privacy and security | `gen/tests/security/test_type_01_security_acceptance.py` |
| Java conversion and privacy | `legacy/processor/src/test/java/com/northwindpay/legacy/type01/Type01ProcessorTest.java` |
| Python loader boundary | `tests/unit/test_type01_loader.py` |
| Typed workflow and Java dispatch | `tests/unit/test_type01_workflow.py` |
| Independent correctness oracle | `validation/oracle/tests/test_type01_oracle.py` |
| PostgreSQL transaction rollback | `tests/postgres/test_type01_loader_rollback.py` |
| PostgreSQL procedure and reconciliation | Type 01 case in `tests/postgres/test_postgres_regression.py` |
| Live SFTP, role boundaries, PostgreSQL, and evidence | `tests/end-to-end/run_type01_suite.py` |

The automatic worker, SFTP server, role model, migration engine, and common
batch-control code are intentionally shared across file types. Their tests
therefore keep shared names under `tests/security/` and `tests/unit/`. Type 01
exercises that shared infrastructure live in its end-to-end suite, including
least-privilege role checks, manifest-last readiness, duplicate refusal,
archive/quarantine routing, restart seams, database procedures,
reconciliation, and evidence privacy.

DataGen uses `type_01` in Python module names to match its existing
`generators/type_01_*` convention. The legacy runtime uses `type01` to match
Java packages and the established loader/workflow convention. Both spellings
identify file type number `01`; this is a layer-specific naming convention,
not two implementations.

Run the complete Type 01 proof on a freshly deployed disposable runtime with:

```sh
make test-type01
```

The target does not erase runtime state. Canonical batch IDs are immutable, so
clean or isolate the runtime before repeating the live suite.
