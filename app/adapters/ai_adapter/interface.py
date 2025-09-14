from typing import Protocol

from app.adapters.ai_adapter.schemas import AIAGenAnswerResult, AIAGenTextCommand


class IAIAdapter(Protocol):
    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        pass
