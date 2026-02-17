from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.domain.errors import DomainNotFoundError
from app.infra.repositories import PricePoint, PriceRepository
from app.infra.wiring import get_price_repo

router = APIRouter(prefix="/v1", tags=["prices"])

MAX_RANGE_DAYS = 3650


def _problem_not_found(request: Request, title: str, detail: str) -> JSONResponse:
    payload = {
        "type": "not_found",
        "title": title,
        "status": 404,
        "detail": detail,
        "instance": str(request.url.path),
    }
    return JSONResponse(status_code=404, content=payload)


def _serialize_points(points: list[PricePoint]) -> list[dict[str, Any]]:
    return [{"date": p.date.isoformat(), "close": p.close} for p in points]


@router.get("/prices/{symbol}")
def get_prices(
    symbol: str,
    request: Request,
    repo: PriceRepository = Depends(get_price_repo),
    from_: date | None = Query(default=None, alias="from"),
    to: date | None = Query(default=None),
) -> JSONResponse:
    if from_ and to and from_ > to:
        return JSONResponse(status_code=422, content={"detail": "from must be <= to"})

    # Fetch all points first (simple); later we can optimize if needed.
    try:
        points = repo.get_prices(symbol)
    except DomainNotFoundError as exc:
        return _problem_not_found(request, title="Prices not found", detail=str(exc))

    if not points:
        return _problem_not_found(
            request, title="Prices not found", detail=f"No price data for symbol: {symbol.upper()}"
        )

    min_date = points[0].date
    max_date = points[-1].date

    effective_from = from_ or min_date
    effective_to = to or max_date

    if (effective_to - effective_from).days > MAX_RANGE_DAYS:
        return JSONResponse(
            status_code=422, content={"detail": f"date range too large (max {MAX_RANGE_DAYS} days)"}
        )

    filtered = [p for p in points if effective_from <= p.date <= effective_to]

    payload = {
        "symbol": symbol.upper(),
        "currency": "USD",
        "from": effective_from.isoformat(),
        "to": effective_to.isoformat(),
        "count": len(filtered),
        "items": _serialize_points(filtered),
    }
    return JSONResponse(status_code=200, content=payload)
