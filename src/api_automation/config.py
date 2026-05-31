from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    base_url: str
    request_timeout: float
    log_level: str


def load_settings() -> Settings:
    load_dotenv()

    base_url = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
    timeout_raw = os.getenv("REQUEST_TIMEOUT", "10")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    try:
        request_timeout = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("REQUEST_TIMEOUT must be a number") from exc

    if request_timeout <= 0:
        raise ValueError("REQUEST_TIMEOUT must be greater than zero")

    return Settings(
        base_url=base_url,
        request_timeout=request_timeout,
        log_level=log_level,
    )
