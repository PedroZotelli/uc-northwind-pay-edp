# NorthWind Pay DataGen

`gen/` is the standalone Python simulator for the upstream legacy source
system. It generates contract-controlled raw artifacts. It does not publish to
SFTP, call Java, produce sanitized CSV, or connect to PostgreSQL.

## Current scope

DataGen implements all five independent legacy layouts and five deterministic
scenarios per type:

| Type | Layout | Accepted scenarios | Malformed scenario | Source-control defect |
|---|---|---|---|---|
| `01` | Card Settlement Detail | `valid-minimal`, `valid-boundary`, `negative-overpunch` | `INVALID_OVERPUNCH` | `DF-SOURCE-001` → `SOURCE_CONTROL_TOTAL_MISMATCH` |
| `02` | Instant Payment Events | `valid-minimal`, `valid-boundary`, `escaped-content` | `INVALID_FIELD_COUNT` | `DF-SOURCE-002` → `SOURCE_CONTROL_NET_MISMATCH` |
| `03` | Payment Slip Settlement | `valid-minimal`, `valid-boundary`, `multi-lot` | `SEGMENT_PAIR_MISMATCH` | `DF-SOURCE-003` → `SOURCE_CONTROL_NET_MISMATCH` |
| `04` | TED Transfer Settlement | `valid-minimal`, `valid-boundary`, `all-returned-zero-net` | `INVALID_TRANSPORT` | `DF-SOURCE-004` → `SOURCE_CONTROL_NET_MISMATCH` |
| `05` | Merchant Fee Assessment | `valid-minimal`, `valid-boundary`, `rounding-half-up` | `INVALID_CSV_QUOTING` | `DF-SOURCE-005` → `SOURCE_CONTROL_ASSESSED_FEE_MISMATCH` |

SFTP, Java, and PostgreSQL intentionally remain outside `gen/`; the
repository-level runner connects those independent components.

## Run

Requirements:

- Python 3.12 or newer.
- PyYAML 6.x.

For an isolated development environment:

```bash
python3 -m venv gen/.venv
source gen/.venv/bin/activate
python -m pip install -e 'gen[dev]'
```

From the repository root:

```bash
python3 gen/src/cli.py \
  --type 01 \
  --scenario valid-minimal
```

Set `--type` to `01`, `02`, `03`, `04`, or `05`, and replace
`valid-minimal` with any scenario supported by that type. Scenario names are
case-sensitive.

After editable installation, `datagen` provides the same CLI. Run it inside the
repository, set `NWP_EDP_ROOT`, or pass both `--contracts-root` and `--output`.

The optional `--output` argument selects another output root. The default is
`gen/output/`.

`valid-minimal` is a fixed canonical recipe, so it intentionally has no seed.
A seed will be introduced only when a future scenario genuinely varies its
synthetic values.

## Output

```text
gen/output/B202607230000001/
├── NW_CARD_SETTLEMENT_20260723_B202607230000001.dat
├── NW_CARD_SETTLEMENT_20260723_B202607230000001.dat.sha256
├── source-manifest.json
└── generation-receipt.json
```

Each scenario has a distinct batch ID, so all 25 implemented scenarios may
coexist under the same output root. Re-running a scenario against that root
fails safely rather than overwriting its immutable batch.

Raw `.dat`, `.txt`, `.rem`, and `.csv` files contain restricted synthetic
source values. The other artifacts contain only safe metadata, controls,
filenames, and hashes.

The output directory is written privately in a temporary sibling directory and
atomically renamed into place. An existing batch directory is never
overwritten.

## Artifact ownership

DataGen creates:

- Raw source file.
- GNU-compatible SHA-256 sidecar.
- Deterministic source manifest.
- Deterministic local generation receipt.

The repository publisher verifies and transports the raw file, checksum, and
source manifest unchanged. It publishes the source manifest last as the SFTP
readiness marker. The generation receipt remains local evidence and is not sent
to SFTP.

The source manifest describes what the simulated source declares. It does not
disclose local scenario or fault labels. The local receipt records both
computed and declared controls, so both Dark Factory scenarios preserve their
BRL 173.45 versus BRL 173.44 contradiction without telling downstream systems
that a test fault was injected.

## Test

From the repository root:

```bash
PYTHONPATH=gen/src \
  python3 -m unittest discover \
    --start-directory gen/tests \
    --pattern 'test_*.py' \
    --verbose
```

The contract tests compare hashes, lengths, and the first differing byte offset
without printing raw records or restricted identifiers.

The shared source interfaces are also checked with strict typing:

```bash
PYTHONPATH=gen/src mypy --python-version 3.12 --strict gen/src
```
