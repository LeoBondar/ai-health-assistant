from app.api.chats.schemas import AddPlanDiseaseCommand, AddPlanDiseaseResponse
from app.api.errors.api_error import PlanNotFoundApiError
from app.dto.chat import AddDiseaseDTO
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddPlanDiseaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddPlanDiseaseCommand) -> AddPlanDiseaseResponse:
        async with self._uow.begin():

            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            plan.add_disease(dto=AddDiseaseDTO(name=cmd.name))

            await self._uow.plan_repository.save(plan)

        return AddPlanDiseaseResponse()
