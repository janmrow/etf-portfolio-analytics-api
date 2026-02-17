from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.infra.json_store import JsonStore
from app.infra.repositories import EtfRepository, PriceRepository


def get_etf_repo() -> EtfRepository:
    settings = get_settings()
    data_path = str(Path(settings.data_dir) / "etfs.json")
    return EtfRepository(store=JsonStore(), data_path=data_path)


def get_price_repo() -> PriceRepository:
    settings = get_settings()
    prices_dir = str(Path(settings.data_dir) / "prices")
    return PriceRepository(store=JsonStore(), prices_dir=prices_dir)
