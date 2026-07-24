"""Dagster assets for the modern pipeline.

Orchestration owns sensing, dependencies, retries, partitions, checks, and
lineage. It owns no parsing and no business logic: every asset calls the same
function ``modern/pipeline.py`` calls, which is what makes direct and
orchestrated execution provably equivalent rather than merely similar.
"""

# Dagster resolves the `context` annotation at decoration time, so this module
# deliberately does not use `from __future__ import annotations`.
import sys
from pathlib import Path
from typing import Any, Dict

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "modern"))

import pipeline  # noqa: E402

from dagster import (  # noqa: E402
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
    result = pipeline.build_models()
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


@asset_check(asset=golden_match_report, description="No unexplained difference may reach Gold.")
def no_unexplained_differences(golden_match_report: Dict[str, Any]) -> AssetCheckResult:
    unexplained = int(golden_match_report["unexplained_differences"])
    return AssetCheckResult(
        passed=unexplained == 0,
        metadata={"unexplained_differences": MetadataValue.int(unexplained)},
    )


@asset_check(
    asset=golden_match_report,
    description="Every canonical batch produced a complete evidence packet.",
)
def evidence_complete(golden_match_report: Dict[str, Any]) -> AssetCheckResult:
    packets = golden_match_report["evidence_packets"]
    present = [
        name
        for name in packets
        if (pipeline.EVIDENCE_ROOT / name / "final-status.json").is_file()
    ]
    return AssetCheckResult(
        passed=len(present) == len(packets) and bool(packets),
        metadata={"packets": MetadataValue.int(len(present))},
    )


@asset_check(
    asset=landing_parquet,
    description="A rejected batch must publish no Parquet at all.",
)
def rejected_batches_publish_nothing(
    landing_parquet: Dict[str, Any],
) -> AssetCheckResult:
    offenders = [
        name
        for name, value in landing_parquet.items()
        if value["status"] != "succeeded" and value.get("parquet_sha256") is not None
    ]
    return AssetCheckResult(
        passed=not offenders,
        metadata={"offending_scenarios": MetadataValue.text(", ".join(offenders))},
    )


defs = Definitions(
    assets=[landing_parquet, lakehouse_registration, dbt_models, golden_match_report],
    asset_checks=[
        no_unexplained_differences,
        evidence_complete,
        rejected_batches_publish_nothing,
    ],
)
