from app.adapters.ai_adapter.interface import IAIAdapter
from app.adapters.ai_adapter.schemas import (
    AIAGenTextCommand,
    AIAGenAnswerResult
)
from app.infrastructure.http_clients.openai.client import IOpenAIClient


class OpenAIAdapter(IAIAdapter):
    def __init__(self, client: IOpenAIClient) -> None:
        self._client = client

    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        pass