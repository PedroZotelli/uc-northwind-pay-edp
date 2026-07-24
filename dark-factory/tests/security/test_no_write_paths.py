"""The Step 2 gate, asserted about the source rather than about a run.

"No adapter has a write path to SFTP, PostgreSQL, legacy evidence, or contracts"
is a statement about code. Parsing the modules holds for code that has never
executed, including code a later slice adds, which an integration test cannot
do.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "darkfactory"
OBSERVATION_ROOT = SOURCE_ROOT / "observations"

# Names that mutate a filesystem, a remote store, or a process environment.
FORBIDDEN_CALLS = frozenset(
    {
        "chmod",
        "chown",
        "link",
        "makedirs",
        "mkdir",
        "mknod",
        "put",
        "putfo",
        "remove",
        "removedirs",
        "rename",
        "renames",
        "replace",
        "rmdir",
        "rmtree",
        "symlink",
        "truncate",
        "unlink",
        "utime",
        "write_bytes",
        "write_text",
    }
)

FORBIDDEN_MODULES = frozenset(
    {
        "config",
        "evidence",
        "lifecycle",
        "loader_common",
        "raw_intake",
        "raw_publisher",
        "recovery_journal",
        "sftp_client",
        "workflow",
        "workflow_registry",
        "worker",
    }
)

WRITE_MODES = ("w", "a", "x", "+")


def _modules(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    )


class ObservationAdaptersAreReadOnlyTest(unittest.TestCase):
    """Every module under ``observations/`` is parsed and checked."""

    def setUp(self) -> None:
        self.modules = _modules(OBSERVATION_ROOT)
        self.assertTrue(self.modules, "no observation modules were found")

    def test_no_write_capable_call_appears(self) -> None:
        for path in self.modules:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = None
                if isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    name = node.func.id
                self.assertNotIn(
                    name,
                    FORBIDDEN_CALLS,
                    f"{path.name} calls the write-capable name {name}",
                )

    def test_no_file_is_opened_for_writing(self) -> None:
        for path in self.modules:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                is_open = (
                    isinstance(node.func, ast.Attribute) and node.func.attr == "open"
                ) or (isinstance(node.func, ast.Name) and node.func.id == "open")
                if not is_open:
                    continue
                modes = [
                    argument.value
                    for argument in node.args[1:]
                    if isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                ]
                modes += [
                    keyword.value.value
                    for keyword in node.keywords
                    if keyword.arg == "mode"
                    and isinstance(keyword.value, ast.Constant)
                    and isinstance(keyword.value.value, str)
                ]
                for mode in modes:
                    for character in WRITE_MODES:
                        self.assertNotIn(
                            character,
                            mode,
                            f"{path.name} opens a path with write mode {mode!r}",
                        )

    def test_no_legacy_runtime_module_is_imported(self) -> None:
        for path in self.modules:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    names = [node.module or ""]
                for name in names:
                    self.assertNotIn(
                        name.split(".")[0],
                        FORBIDDEN_MODULES,
                        f"{path.name} imports the legacy runtime module {name}",
                    )

    def test_the_postgres_adapter_declares_a_read_only_transaction(self) -> None:
        source = (OBSERVATION_ROOT / "postgres.py").read_text(encoding="utf-8")
        self.assertIn("SET TRANSACTION READ ONLY", source)
        self.assertIn("connection.read_only = True", source)

    def test_the_transport_adapter_rejects_unknown_host_keys(self) -> None:
        source = (OBSERVATION_ROOT / "transport.py").read_text(encoding="utf-8")
        self.assertIn("RejectPolicy", source)
        self.assertNotIn("AutoAddPolicy", source)


class DetectorTouchesNoFrozenRootTest(unittest.TestCase):
    """Nothing anywhere in the package may write into a frozen root."""

    FROZEN = ("legacy/", "contracts/types", "gen/", "infra/")

    def test_no_module_references_a_frozen_root_for_writing(self) -> None:
        for path in _modules(SOURCE_ROOT):
            source = path.read_text(encoding="utf-8")
            for root in self.FROZEN:
                if root not in source:
                    continue
                for line in source.splitlines():
                    if root not in line:
                        continue
                    lowered = line.lower()
                    for verb in ("write", "unlink", "rmtree", "rename", "mkdir"):
                        self.assertNotIn(
                            verb,
                            lowered,
                            f"{path.name} appears to write into {root}",
                        )

    def test_only_the_writer_publishes_anything(self) -> None:
        """Publication is confined to one reviewable module."""

        writers = []
        for path in _modules(SOURCE_ROOT):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in {"rename", "mkdir", "fchmod", "chmod"}
                ):
                    writers.append(path.name)
                    break
        self.assertEqual(sorted(set(writers)), ["writer.py"])


if __name__ == "__main__":
    unittest.main()
