from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_dir: str


def get_settings() -> Settings:
    return Settings(data_dir=os.getenv("DATA_DIR", "data"))
