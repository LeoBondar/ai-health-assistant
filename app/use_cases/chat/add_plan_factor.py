from app.api.chats.schemas import AddPlanFactorCommand, AddPlanFactorResponse
from app.api.errors.api_error import PlanNotFoundApiError, RiskFactorNotFoundApiError
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddPlanFactorUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddPlanFactorCommand) -> AddPlanFactorResponse:
        async with self._uow.begin():

            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            try:
                risk_factor = await self._uow.risk_factor_repository.get(cmd.factor_id)
            except RepositoryNotFoundException:
                raise RiskFactorNotFoundApiError

            plan.add_risk_factor(risk_factor)
            await self._uow.plan_repository.save(plan)

        return AddPlanFactorResponse()
