from typing import Protocol

from app.adapters.ai_adapter.schemas import AIAGenAnswerResult, AIAGenTextCommand, AIAGenPlanCommand, AIAGenPlanResponse, AIAUpdatePlanCommand, AIAUpdatePlanResponse


class IAIAdapter(Protocol):
    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        pass

    async def gen_plan(self, command: AIAGenPlanCommand) -> AIAGenPlanResponse:
        pass

    async def update_plan(self, command: AIAUpdatePlanCommand) -> AIAUpdatePlanResponse:
        pass
