from typing import Protocol

from app.adapters.ai_adapter.schemas import (
    AIAGenTextCommand,
    AIAGenAnswerResult
)


class IAIAdapter(Protocol):
    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        pass