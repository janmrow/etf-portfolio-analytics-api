from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_dir: str


def get_settings() -> Settings:
    # Keep it simple: env var with a safe default.
    data_dir = os.getenv("DATA_DIR", "data")
    return Settings(data_dir=data_dir)
