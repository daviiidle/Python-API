from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(level_name: str) -> None:
    Path("reports").mkdir(exist_ok=True)

    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("reports/api-tests.log", mode="w", encoding="utf-8"),
        ],
        force=True,
    )
