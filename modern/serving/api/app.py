"""Read-only FastAPI surface over approved Gold.

Explicit endpoints only. There is no query parameter that reaches SQL, no
passthrough to a restricted zone, and no route that can serve a batch whose
golden-match is unresolved — the service layer refuses that for every caller.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import service  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402

application = FastAPI(
    title="NorthWind Pay modern reconciliation",
    description="Read-only access to approved Gold. No arbitrary SQL.",
    version="1.0.0",
)


def _guard(call: Any, *arguments: Any) -> Any:
    try:
        return call(*arguments)
    except service.ServiceError as error:
        raise HTTPException(status_code=error.status, detail=str(error)) from error


@application.get("/health")
def read_health() -> dict[str, Any]:
    return service.health()


@application.get("/batches/{batch_id}/status")
def read_status(batch_id: str) -> dict[str, Any]:
    return _guard(service.batch_status, batch_id)


@application.get("/batches/{batch_id}/reconciliation")
def read_reconciliation(batch_id: str) -> dict[str, Any]:
    return _guard(service.reconciliation, batch_id)


@application.get("/batches/{batch_id}/golden-match")
def read_golden_match(batch_id: str) -> dict[str, Any]:
    return _guard(service.golden_match, batch_id)
