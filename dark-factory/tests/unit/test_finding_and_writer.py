"""Unit tests for finding assembly, canonical identity, and atomic publication."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from darkfactory import contracts as contract_loader
from darkfactory.attribution.source_system import attribute
from darkfactory.canonical import (
    encode,
    finding_identity,
    identity_bytes,
    serialize,
)
from darkfactory.detection.control_mismatch import detect
from darkfactory.errors import (
    ContinuationUnprovenError,
    EvidenceConflictError,
    IsolationUnprovenError,
)
from darkfactory.findings import model as finding_model
from darkfactory.findings import writer as finding_writer
from darkfactory.observations.postgres import PeerObservation

import factories

DETECTOR_DIGEST = "sha256:" + "e" * 64


def build(**kwargs: object) -> dict[str, object]:
    observations = factories.observation_set(**kwargs)  # type: ignore[arg-type]
    detection = detect(observations)
    return finding_model.build(
        contract_loader.load(),
        observations,
        detection,
        attribute(observations, detection),
        detector_source_sha256=DETECTOR_DIGEST,
    )


class CanonicalIdentityTest(unittest.TestCase):
    def test_identity_ignores_creation_time(self) -> None:
        early = build()
        late = dict(early)
        late["created_at"] = "2099-01-01T00:00:00Z"
        late["finding_id"] = finding_identity(late)
        self.assertEqual(early["finding_id"], late["finding_id"])

    def test_identical_observations_produce_byte_identical_findings(self) -> None:
        first = build()
        second = build()
        self.assertEqual(identity_bytes(first), identity_bytes(second))
        self.assertEqual(first["finding_id"], second["finding_id"])

    def test_identity_changes_when_any_other_member_changes(self) -> None:
        baseline = build()
        drifted = json.loads(encode(baseline).decode())
        drifted["controls"]["compared"][0]["computed"] = "3"
        self.assertNotEqual(
            finding_identity(baseline), finding_identity(drifted)
        )

    def test_canonical_encoding_is_sorted_ascii_and_compact(self) -> None:
        payload = serialize(build())
        self.assertTrue(payload.endswith(b"\n"))
        self.assertNotIn(b", ", payload)
        self.assertNotIn(b": ", payload)
        payload.decode("ascii")  # raises if any non-ASCII byte escaped
        document = json.loads(payload.decode())
        self.assertEqual(list(document), sorted(document))

    def test_creation_time_is_recorded_even_though_it_is_not_identity(self) -> None:
        moment = datetime(2026, 7, 24, 12, 30, 15, tzinfo=timezone.utc)
        observations = factories.observation_set()
        detection = detect(observations)
        finding = finding_model.build(
            contract_loader.load(),
            observations,
            detection,
            attribute(observations, detection),
            detector_source_sha256=DETECTOR_DIGEST,
            created_at=moment,
        )
        self.assertEqual(finding["created_at"], "2026-07-24T12:30:15Z")

    def test_creation_time_is_normalized_to_utc(self) -> None:
        moment = datetime(
            2026, 7, 24, 9, 30, 15, tzinfo=timezone(timedelta(hours=-3))
        )
        observations = factories.observation_set()
        detection = detect(observations)
        finding = finding_model.build(
            contract_loader.load(),
            observations,
            detection,
            attribute(observations, detection),
            detector_source_sha256=DETECTOR_DIGEST,
            created_at=moment,
        )
        self.assertEqual(finding["created_at"], "2026-07-24T12:30:15Z")


class CompletenessTest(unittest.TestCase):
    def test_sanitized_output_blocks_the_finding(self) -> None:
        with self.assertRaises(IsolationUnprovenError):
            build(
                transport_observation=factories.transport(
                    csv_zones=("csv/archive",)
                )
            )

    def test_business_rows_block_the_finding(self) -> None:
        with self.assertRaises(IsolationUnprovenError):
            build(operational_rows=2)

    def test_staging_rows_block_the_finding(self) -> None:
        with self.assertRaises(IsolationUnprovenError):
            build(staging_rows=2)

    def test_a_missing_quarantine_bundle_blocks_the_finding(self) -> None:
        with self.assertRaises(IsolationUnprovenError):
            build(transport_observation=factories.transport(raw_zones=()))

    def test_committed_business_state_blocks_the_finding(self) -> None:
        with self.assertRaises(IsolationUnprovenError):
            build(business_mutation=True)

    def test_a_failed_peer_blocks_the_finding(self) -> None:
        with self.assertRaises(ContinuationUnprovenError):
            build(peer_observations=factories.peers(status="quarantined"))

    def test_an_unreconciled_peer_blocks_the_finding(self) -> None:
        with self.assertRaises(ContinuationUnprovenError):
            build(peer_observations=factories.peers(report="MISMATCHED"))

    def test_a_missing_peer_report_blocks_the_finding(self) -> None:
        with self.assertRaises(ContinuationUnprovenError):
            build(
                peer_observations=(
                    PeerObservation("B202402290000001", "succeeded", "ABSENT"),
                    PeerObservation("B202607230000002", "succeeded", "MATCHED"),
                )
            )


class WriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = contract_loader.load()
        self.observations = factories.observation_set()
        detection = detect(self.observations)
        self.finding = finding_model.build(
            self.contract,
            self.observations,
            detection,
            attribute(self.observations, detection),
            detector_source_sha256=DETECTOR_DIGEST,
        )

    def test_publishes_a_complete_packet_with_private_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            packet = finding_writer.publish(
                self.finding,
                self.observations,
                self.contract,
                evidence_root=Path(temporary),
            )
            self.assertEqual(
                sorted(path.name for path in packet.iterdir()),
                sorted(finding_writer.PACKET_FILES),
            )
            self.assertEqual(packet.stat().st_mode & 0o777, 0o700)
            for path in packet.iterdir():
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_republishing_the_same_finding_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = finding_writer.publish(
                self.finding, self.observations, self.contract, evidence_root=root
            )
            before = (first / "finding.json").read_bytes()
            second = finding_writer.publish(
                self.finding, self.observations, self.contract, evidence_root=root
            )
            self.assertEqual(first, second)
            self.assertEqual((second / "finding.json").read_bytes(), before)

    def test_a_different_finding_for_the_same_batch_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            finding_writer.publish(
                self.finding, self.observations, self.contract, evidence_root=root
            )
            drifted = json.loads(encode(self.finding).decode())
            drifted["controls"]["compared"][0]["computed"] = "9"
            drifted["finding_id"] = finding_identity(drifted)
            with self.assertRaises(EvidenceConflictError):
                finding_writer.publish(
                    drifted, self.observations, self.contract, evidence_root=root
                )

    def test_no_partial_packet_survives_a_failed_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / self.observations.lineage.batch_id).mkdir()
            with self.assertRaises(EvidenceConflictError):
                finding_writer.publish(
                    self.finding,
                    self.observations,
                    self.contract,
                    evidence_root=root,
                )
            self.assertEqual(
                [path.name for path in root.iterdir()],
                [self.observations.lineage.batch_id],
            )

    def test_published_finding_validates_against_the_closed_schema(self) -> None:
        finding_writer.validate_schema(self.finding, self.contract.schema)


if __name__ == "__main__":
    unittest.main()
