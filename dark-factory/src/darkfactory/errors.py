"""Stable Dark Factory error codes.

Every refusal path carries a code from ``dark-factory/contracts/error-codes.yaml``
so that a red gate names a reason instead of surfacing a stack trace. Messages
never contain observed values; they name paths, channels, and control names.
"""

from __future__ import annotations


class DarkFactoryError(Exception):
    """Base class for every bounded Dark Factory refusal."""

    code = "DF-E-UNKNOWN"
    exit_status = 1

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


class ObservationMissingError(DarkFactoryError):
    code = "DF-E-OBSERVATION-MISSING"
    exit_status = 3


class CrossBatchObservationError(DarkFactoryError):
    code = "DF-E-CROSS-BATCH-OBSERVATION"
    exit_status = 3


class AmbiguousObservationError(DarkFactoryError):
    code = "DF-E-AMBIGUOUS-OBSERVATION"
    exit_status = 3


class LineageConflictError(DarkFactoryError):
    code = "DF-E-LINEAGE-CONFLICT"
    exit_status = 3


class ContradictoryObservationError(DarkFactoryError):
    code = "DF-E-CONTRADICTORY-OBSERVATION"
    exit_status = 3


class NoMismatchError(DarkFactoryError):
    code = "DF-E-NO-MISMATCH"
    exit_status = 4


class AttributionInconclusiveError(DarkFactoryError):
    code = "DF-E-ATTRIBUTION-INCONCLUSIVE"
    exit_status = 5


class IsolationUnprovenError(DarkFactoryError):
    code = "DF-E-ISOLATION-UNPROVEN"
    exit_status = 5


class ContinuationUnprovenError(DarkFactoryError):
    code = "DF-E-CONTINUATION-UNPROVEN"
    exit_status = 5


class PrivacyViolationError(DarkFactoryError):
    code = "DF-E-PRIVACY-VIOLATION"
    exit_status = 6


class SchemaViolationError(DarkFactoryError):
    code = "DF-E-SCHEMA-VIOLATION"
    exit_status = 6


class EvidenceConflictError(DarkFactoryError):
    code = "DF-E-EVIDENCE-CONFLICT"
    exit_status = 7


class RuntimeUnavailableError(DarkFactoryError):
    code = "DF-E-RUNTIME-UNAVAILABLE"
    exit_status = 8
