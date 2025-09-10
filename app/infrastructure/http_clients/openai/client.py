from abc import abstractmethod
from asyncio import Protocol
from typing import Any

import httpx
from openai.types.chat import ChatCompletion

from app.infrastructure.http_clients.base import BaseHttpClient
from app.infrastructure.http_clients.enums import HTTPClientRequestMethod
from app.infrastructure.http_clients.openai.schemas import (
    OACGenTextCommand,
)
from app.settings import settings


class IOpenAIClient(Protocol):
    @abstractmethod
    async def gen_text(self, command: OACGenTextCommand) -> ChatCompletion:
        raise NotImplementedError

class OpenAIClient(BaseHttpClient, IOpenAIClient):
    async def gen_text(self, command: OACGenTextCommand) -> ChatCompletion:
        pass

    async def _make_request(
        self,
        url: str,
        method: HTTPClientRequestMethod,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> httpx.Response:
        if headers:
            headers |= {"Authorization": f"Bearer {settings.openai.api_key}"}
        else:
            headers = {"Authorization": f"Bearer {settings.openai.api_key}"}
        return await self._request(
            url=url,
            method=method,
            json=json,
            headers=headers,
            params=params,
            data=data,
            files=files,
        )
