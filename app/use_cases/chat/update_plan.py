from app.adapters.ai_adapter.adapter_manager import IAIManager
from app.adapters.ai_adapter.schemas import AIAUpdatePlanCommand
from app.api.chats.schemas import UpdatePlanCommand, UpdatePlanResponse
from app.api.errors.api_error import PlanDescriptionEmptyApiError, PlanNotFoundApiError
from app.enums.chats import AIServiceEnum
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class UpdatePlanUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        ai_manager: IAIManager,
    ) -> None:
        self._uow = uow
        self._ai_manager = ai_manager

    async def __call__(self, cmd: UpdatePlanCommand) -> UpdatePlanResponse:

        async with self._uow.begin():
            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            if not plan.description or plan.description.strip() == "":
                raise PlanDescriptionEmptyApiError

            ai_adapter = self._ai_manager.get_ai_adapter(service=AIServiceEnum.OPENAI)

            update_plan_result = await ai_adapter.update_plan(
                command=AIAUpdatePlanCommand(
                    plan=plan.description,
                    comment=cmd.comment,
                )
            )

            plan.description = update_plan_result.description
            await self._uow.plan_repository.save(plan)

            return UpdatePlanResponse(description=update_plan_result.description)
