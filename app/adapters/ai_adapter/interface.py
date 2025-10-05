from typing import Protocol

from app.adapters.ai_adapter.schemas import AIAGenAnswerResult, AIAGenTextCommand, AIAGenPlanCommand, AIAGenPlanResponse


class IAIAdapter(Protocol):
    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        pass

    async def gen_plan(self, command: AIAGenPlanCommand) -> AIAGenPlanResponse:
        pass