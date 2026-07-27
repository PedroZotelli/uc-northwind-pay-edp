"""The single bounded Dark Factory entrypoint.

Read-only by construction: it observes a live legacy runtime, compares declared
against independently computed controls, attributes ownership from evidence, and
writes one privacy-safe finding under its own evidence root. It never moves a
file, repairs data, requests an approval, or makes an external call.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import contracts as contract_loader
from attribution.source_system import attribute
from canonical import serialize
from detector_config import REPOSITORY_ROOT, DetectorConfiguration, detector_source_digest
from detection.control_mismatch import detect
from errors import AttributionInconclusiveError, DarkFactoryError
from findings import model as finding_model
from findings import writer as finding_writer
from observations.collect import collect

DEFAULT_EVIDENCE_ROOT = REPOSITORY_ROOT / "evidence" / "factory"


def run(
    type_number: str,
    *,
    legacy_evidence_root: Path,
    evidence_root: Path,
    withhold: frozenset[str] = frozenset(),
    publish: bool = True,
) -> dict[str, object]:
    """Detect, attribute, and optionally publish one finding."""

    contract = contract_loader.load()
    scenario = contract.for_type(type_number)
    configuration = DetectorConfiguration.load()

    observations = collect(
        scenario,
        configuration=configuration,
        evidence_root=legacy_evidence_root,
        withhold=withhold,
    )
    detection = detect(observations)
    attribution = attribute(observations, detection)
    if not attribution.conclusive:
        raise AttributionInconclusiveError(
            "the observations do not support exactly one attribution"
        )

    finding = finding_model.build(
        contract,
        observations,
        detection,
        attribution,
        detector_source_sha256=detector_source_digest(),
    )
    finding_writer.enforce(finding, contract=contract, scenario=scenario)
    if publish:
        finding_writer.publish(
            finding,
            observations,
            contract,
            evidence_root=evidence_root,
        )
    return finding


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="factory",
        description=(
            "Read-only detection and attribution of source-system control "
            "mismatches from immutable legacy observations."
        ),
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=("01", "02", "03", "04", "05"),
        help="Registered type number to observe.",
    )
    parser.add_argument(
        "--legacy-evidence-root",
        type=Path,
        required=True,
        help="Root holding the legacy evidence packet for the batch.",
    )
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=DEFAULT_EVIDENCE_ROOT,
        help="Dark Factory evidence root (default: evidence/factory).",
    )
    parser.add_argument(
        "--withhold",
        action="append",
        default=[],
        metavar="CHANNEL",
        help=(
            "Withhold one observation channel. Used by the acceptance gate to "
            "prove the attribution depends on it."
        ),
    )
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Detect and validate without writing an evidence packet.",
    )
    arguments = parser.parse_args(argv)

    try:
        finding = run(
            arguments.type,
            legacy_evidence_root=arguments.legacy_evidence_root,
            evidence_root=arguments.evidence_root,
            withhold=frozenset(arguments.withhold),
            publish=not arguments.no_publish,
        )
    except DarkFactoryError as error:
        print(str(error), file=sys.stderr)
        return error.exit_status
    sys.stdout.buffer.write(serialize(finding))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
