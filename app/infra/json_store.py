from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DataStoreError(Exception):
    message: str
    path: str | None = None

    def __str__(self) -> str:
        if self.path:
            return f"{self.message} (path={self.path})"
        return self.message


class JsonStore:
    """
    Small JSON loader used by repositories.

    Design goals:
    - Be explicit and easy to test.
    - Produce clear, predictable errors.
    - Keep data shape validation close to the I/O boundary.
    """

    def load_list(self, path: str | Path) -> list[dict[str, Any]]:
        file_path = Path(path)

        if not file_path.exists():
            raise DataStoreError("JSON file not found", path=str(file_path))

        try:
            raw = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise DataStoreError(f"Cannot read JSON file: {exc}", path=str(file_path)) from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise DataStoreError(f"Invalid JSON: {exc}", path=str(file_path)) from exc

        if not isinstance(data, list):
            raise DataStoreError("Expected a JSON array (list)", path=str(file_path))

        items: list[dict[str, Any]] = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise DataStoreError(
                    f"Expected each array item to be an object (dict), "
                    f"got {type(item).__name__} at index {idx}",
                    path=str(file_path),
                )
            items.append(item)

        return items
