from uuid import UUID

from app.adapters.ai_adapter.adapter_manager import IAIManager
from app.adapters.ai_adapter.schemas import AIAGenPlanCommand, AIAMessageModel
from app.api.chats.schemas import GeneratePlanCommand, GeneratePlanResponse
from app.api.errors.api_error import ChatNotFoundApiError, PlanNotFoundApiError
from app.enums.chats import AIServiceEnum
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class GeneratePlanUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        ai_manager: IAIManager,
    ) -> None:
        self._uow = uow
        self._ai_manager = ai_manager

    async def __call__(self, cmd: GeneratePlanCommand) -> GeneratePlanResponse:
        async with self._uow.begin():
            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            risk_factor = plan.risk_factor.factor if plan.risk_factor else ""
            disease = plan.disease.name if plan.disease else ""
            user_goal = plan.user_goal.name if plan.user_goal else ""
            place = plan.place.name if plan.place else ""
            exercise_info = f"{plan.exercise.name} ({plan.exercise.type})" if plan.exercise else ""

            ai_adapter = self._ai_manager.get_ai_adapter(service=AIServiceEnum.OPENAI)
            
            gen_plan_result = await ai_adapter.gen_plan(
                command=AIAGenPlanCommand(
                    risk_factor=risk_factor,
                    disease=disease,
                    user_goal=user_goal,
                    place=place,
                    exercise=exercise_info,
                )
            )

            plan.description = gen_plan_result.description
            await self._uow.plan_repository.save(plan)

            return GeneratePlanResponse(description=gen_plan_result.description)