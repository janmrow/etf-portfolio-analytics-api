from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.domain.errors import DomainNotFoundError
from app.infra.json_store import JsonStore


@dataclass(frozen=True)
class Etf:
    symbol: str
    name: str
    currency: str
    inception_date: str


class EtfRepository:
    def __init__(self, store: JsonStore, data_path: str) -> None:
        self._store = store
        self._data_path = data_path

    def list_etfs(self) -> list[Etf]:
        items = self._store.load_list(self._data_path)
        return [self._to_etf(item) for item in items]

    def get_etf(self, symbol: str) -> Etf:
        normalized = symbol.upper()
        for etf in self.list_etfs():
            if etf.symbol == normalized:
                return etf

        raise DomainNotFoundError(
            resource="etf",
            key=normalized,
            message=f"Unknown symbol: {normalized}",
        )

    def _to_etf(self, item: dict[str, Any]) -> Etf:
        # Be explicit and forgiving; validation will be added later if needed.
        return Etf(
            symbol=str(item.get("symbol", "")).upper(),
            name=str(item.get("name", "")),
            currency=str(item.get("currency", "")),
            inception_date=str(item.get("inception_date", "")),
        )
