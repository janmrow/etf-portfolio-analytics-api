from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainNotFoundError(Exception):
    resource: str
    key: str
    message: str

    def __str__(self) -> str:
        return self.message
