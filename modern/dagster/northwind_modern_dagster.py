"""Dagster assets for the modern pipeline.

Orchestration owns sensing, dependencies, retries, partitions, checks, and
lineage. It owns no parsing and no business logic: every asset calls the same
function ``modern/pipeline.py`` calls, which is what makes direct and
orchestrated execution provably equivalent rather than merely similar.
"""

# Dagster resolves the `context` annotation at decoration time, so this module
# deliberately does not use `from __future__ import annotations`.
import json
import sys
from pathlib import Path
from typing import Any, Dict

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "modern"))

import pipeline  # noqa: E402

from dagster import (  # noqa: E402
    AssetCheckExecutionContext,
    AssetCheckResult,
    AssetExecutionContext,
    Definitions,
    MetadataValue,
    Output,
    RetryPolicy,
    StaticPartitionsDefinition,
    asset,
    asset_check,
)

IMPLEMENTED_TYPES = sorted(pipeline.SCENARIOS)
TYPE_PARTITIONS = StaticPartitionsDefinition(IMPLEMENTED_TYPES)

# Transient boundaries only. A contract, privacy, or golden-match failure is
# deterministic: retrying it burns the same result again and hides the signal.
TRANSIENT_RETRIES = RetryPolicy(max_retries=2, delay=1)


@asset(
    partitions_def=TYPE_PARTITIONS,
    retry_policy=TRANSIENT_RETRIES,
    description="Deterministic sanitized Parquet, one immutable file per batch.",
)
def landing_parquet(context: AssetExecutionContext) -> Output[Dict[str, Any]]:
    type_number = context.partition_key
    pipeline.generate_bundles(type_number)
    outcomes = pipeline.ingest(type_number)
    accepted = [name for name, value in outcomes.items() if value["status"] == "succeeded"]
    rejected = [name for name, value in outcomes.items() if value["status"] != "succeeded"]
    return Output(
        outcomes,
        metadata={
            "accepted": MetadataValue.int(len(accepted)),
            "rejected": MetadataValue.int(len(rejected)),
            "rejected_scenarios": MetadataValue.text(", ".join(sorted(rejected))),
        },
    )


@asset(
    partitions_def=TYPE_PARTITIONS,
    retry_policy=TRANSIENT_RETRIES,
    description="dlt registration of landing Parquet into the DuckDB catalog.",
)
def lakehouse_registration(
    context: AssetExecutionContext,
    landing_parquet: Dict[str, Any],
) -> Output[Dict[str, Any]]:
    result = pipeline.register(context.partition_key)
    return Output(
        result,
        metadata={
            "rows": MetadataValue.int(result["row_count"]),
            "table": MetadataValue.text(result["table"]),
        },
    )


@asset(
    partitions_def=TYPE_PARTITIONS,
    description="dbt Bronze, Silver, and Gold with their quality gates.",
)
def dbt_models(
    context: AssetExecutionContext,
    lakehouse_registration: Dict[str, Any],
) -> Output[Dict[str, Any]]:
    result = pipeline.build_models(context.partition_key)
    return Output(result, metadata={"summary": MetadataValue.text(result["summary"])})


@asset(
    partitions_def=TYPE_PARTITIONS,
    description="Golden-match against contract truth and legacy observation.",
)
def golden_match_report(
    context: AssetExecutionContext,
    landing_parquet: Dict[str, Any],
    lakehouse_registration: Dict[str, Any],
    dbt_models: Dict[str, Any],
) -> Output[Dict[str, Any]]:
    type_number = context.partition_key
    results = pipeline.StageResults(
        outcomes=landing_parquet,
        registration=lakehouse_registration,
        dbt=dbt_models,
        gold=pipeline.read_gold(type_number),
    )
    comparisons = pipeline.compare(type_number, results, skip_legacy=False)
    packets = pipeline.write_evidence(type_number, results, comparisons)
    unexplained = sum(len(item.unexplained) for item in comparisons.values())
    report = {
        "evidence_packets": packets,
        "reports": {
            scenario: comparison.as_dict()
            for scenario, comparison in comparisons.items()
        },
        "unexplained_differences": unexplained,
    }
    return Output(
        report,
        metadata={
            "evidence_packets": MetadataValue.int(len(packets)),
            "unexplained_differences": MetadataValue.int(unexplained),
        },
    )


# The checks read published evidence rather than the in-memory asset value.
# A partitioned asset input arrives as a mapping keyed by partition once more
# than one partition exists, so reading the artifacts is both partition-
# independent and a stronger statement: it asserts what was actually written.


def _packets() -> Dict[str, Dict[str, Any]]:
    root = pipeline.EVIDENCE_ROOT
    if not root.is_dir():
        return {}
    found: Dict[str, Dict[str, Any]] = {}
    for directory in sorted(root.iterdir()):
        final = directory / "final-status.json"
        if final.is_file():
            found[directory.name] = json.loads(final.read_text(encoding="utf-8"))
    return found


@asset_check(
    asset=golden_match_report,
    description="No unexplained difference may reach Gold, in any packet.",
)
def no_unexplained_differences(
    context: AssetCheckExecutionContext,
) -> AssetCheckResult:
    unexplained = 0
    unresolved = []
    for batch_id in _packets():
        path = pipeline.EVIDENCE_ROOT / batch_id / "difference-adjudication.json"
        if not path.is_file():
            unresolved.append(batch_id)
            continue
        adjudication = json.loads(path.read_text(encoding="utf-8"))
        unexplained += len(adjudication.get("unexplained", []))
        if not adjudication.get("resolved"):
            unresolved.append(batch_id)
    return AssetCheckResult(
        passed=unexplained == 0 and not unresolved,
        metadata={
            "unexplained_differences": MetadataValue.int(unexplained),
            "unresolved_batches": MetadataValue.text(", ".join(unresolved)),
        },
    )


@asset_check(
    asset=golden_match_report,
    description="Every packet carries exactly the artifacts its outcome allows.",
)
def evidence_complete(context: AssetCheckExecutionContext) -> AssetCheckResult:
    from northwind_pay.evidence import REJECTED_FILES, SUCCESS_FILES

    incomplete = []
    packets = _packets()
    for batch_id, final in packets.items():
        expected = (
            SUCCESS_FILES if final.get("status") == "succeeded" else REJECTED_FILES
        )
        present = {
            path.name for path in (pipeline.EVIDENCE_ROOT / batch_id).iterdir()
        }
        if present != set(expected):
            incomplete.append(batch_id)
    return AssetCheckResult(
        passed=bool(packets) and not incomplete,
        metadata={
            "packets": MetadataValue.int(len(packets)),
            "incomplete": MetadataValue.text(", ".join(incomplete)),
        },
    )


@asset_check(
    asset=landing_parquet,
    description="A rejected batch must have no landing artifact at all.",
)
def rejected_batches_publish_nothing(
    context: AssetCheckExecutionContext,
) -> AssetCheckResult:
    offenders = [
        batch_id
        for batch_id, final in _packets().items()
        if final.get("status") != "succeeded"
        and (pipeline.LANDING_ROOT / batch_id).exists()
    ]
    return AssetCheckResult(
        passed=not offenders,
        metadata={"offending_batches": MetadataValue.text(", ".join(offenders))},
    )


defs = Definitions(
    assets=[landing_parquet, lakehouse_registration, dbt_models, golden_match_report],
    asset_checks=[
        no_unexplained_differences,
        evidence_complete,
        rejected_batches_publish_nothing,
    ],
)
