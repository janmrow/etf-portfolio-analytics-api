from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.domain.errors import DomainNotFoundError
from app.infra.repositories import EtfRepository
from app.infra.wiring import get_etf_repo

router = APIRouter(prefix="/v1", tags=["etfs"])


def _problem_not_found(request: Request, title: str, detail: str) -> JSONResponse:
    payload = {
        "type": "not_found",
        "title": title,
        "status": 404,
        "detail": detail,
        "instance": str(request.url.path),
    }
    return JSONResponse(status_code=404, content=payload)


@router.get("/etfs")
def list_etfs(repo: EtfRepository = Depends(get_etf_repo)) -> dict[str, object]:
    items = [asdict(e) for e in repo.list_etfs()]
    return {"items": items, "count": len(items)}


@router.get("/etfs/{symbol}")
def get_etf(
    symbol: str, request: Request, repo: EtfRepository = Depends(get_etf_repo)
) -> JSONResponse:
    try:
        etf = repo.get_etf(symbol)
        return JSONResponse(status_code=200, content=asdict(etf))
    except DomainNotFoundError as exc:
        return _problem_not_found(request, title="ETF not found", detail=str(exc))
