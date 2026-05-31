from __future__ import annotations

import logging
from typing import Any

from faker import Faker

from src.api_automation.client import APIClient
from src.api_automation.config import load_settings
from src.api_automation.logging_config import configure_logging

LOGGER = logging.getLogger(__name__)


def before_all(context: Any) -> None:
    settings = load_settings()
    configure_logging(settings.log_level)

    context.settings = settings
    context.api = APIClient(settings.base_url, settings.request_timeout)
    context.faker = Faker()

    LOGGER.info("Test run configured for base URL: %s", settings.base_url)


def before_scenario(context: Any, scenario: Any) -> None:
    context.endpoint = None
    context.query_params = {}
    context.request_payload = None
    context.response = None
    LOGGER.info("Starting scenario: %s", scenario.name)
