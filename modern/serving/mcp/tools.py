"""Narrow MCP tools over the same read-only service functions.

Three tools, each mapping to exactly one service call. Deliberately no
"run_query" tool: an MCP surface that can express arbitrary SQL cannot promise
that only approved Gold is reachable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import service  # noqa: E402

TOOLS: Mapping[str, dict[str, Any]] = {
    "batch_status": {
        "description": "Terminal status of one batch and whether golden-match resolved.",
        "parameters": {"batch_id": "Canonical batch identity, B followed by 15 digits."},
        "call": service.batch_status,
    },
    "batch_reconciliation": {
        "description": "Approved Gold reconciliation for one batch.",
        "parameters": {"batch_id": "Canonical batch identity, B followed by 15 digits."},
        "call": service.reconciliation,
    },
    "explain_difference": {
        "description": "Structured golden-match differences and their adjudication.",
        "parameters": {"batch_id": "Canonical batch identity, B followed by 15 digits."},
        "call": service.golden_match,
    },
}


def describe() -> list[dict[str, Any]]:
    """Return the tool catalogue without exposing any callable."""

    return [
        {
            "description": definition["description"],
            "name": name,
            "parameters": definition["parameters"],
        }
        for name, definition in sorted(TOOLS.items())
    ]


def invoke(name: str, batch_id: str) -> str:
    """Invoke one narrow tool and return its JSON result."""

    definition = TOOLS.get(name)
    if definition is None:
        raise service.ServiceError(404, "no such tool")
    call: Callable[[str], Any] = definition["call"]
    return json.dumps(call(batch_id), indent=2, sort_keys=True, default=str)
