from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.domain.errors import DomainNotFoundError
from app.infra.json_store import JsonStore
from app.infra.repositories import EtfRepository

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


def get_etf_repo() -> EtfRepository:
    settings = get_settings()
    data_path = str(Path(settings.data_dir) / "etfs.json")
    return EtfRepository(store=JsonStore(), data_path=data_path)


@router.get("/etfs")
def list_etfs() -> dict[str, object]:
    repo = get_etf_repo()
    items = [asdict(e) for e in repo.list_etfs()]
    return {"items": items, "count": len(items)}


@router.get("/etfs/{symbol}")
def get_etf(symbol: str, request: Request) -> JSONResponse:
    repo = get_etf_repo()
    try:
        etf = repo.get_etf(symbol)
        return JSONResponse(status_code=200, content=asdict(etf))
    except DomainNotFoundError as exc:
        return _problem_not_found(request, title="ETF not found", detail=str(exc))
