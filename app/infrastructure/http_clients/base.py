from typing import Any

import httpx
from httpx import HTTPStatusError
from loguru import logger

from app.infrastructure.http_clients.enums import HTTPClientRequestMethod
from app.infrastructure.http_clients.exceptions import HTTPClientStatusException
from app.settings import HttpClientSettings


class BaseHttpClient:
    def __init__(
        self,
        settings: HttpClientSettings,
        proxy_url: str | None = None,
    ):
        self.client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.timeout,
            verify=settings.verify_ssl,
            proxy=proxy_url,
        )

    async def _request(
        self,
        url: str,
        method: HTTPClientRequestMethod,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> httpx.Response:
        response = await self.client.request(
            method=method,
            url=url,
            json=json,
            headers=headers,
            params=params,
            data=data,
            files=files,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise HTTPClientStatusException(status_code=response.status_code, body=response.json()) from e
        return response
