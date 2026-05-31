from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import requests

LOGGER = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = f"{base_url.rstrip('/')}/"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "qa-automation-portfolio/1.0",
            }
        )

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        LOGGER.info("Sending %s request to %s", method.upper(), url)
        if params:
            LOGGER.debug("Query parameters: %s", params)
        if json:
            LOGGER.debug("Request body: %s", json)

        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )

        LOGGER.info("Received status code %s from %s", response.status_code, url)
        LOGGER.debug("Response body: %s", response.text)
        return response
