from app.api.chats.schemas import AddPlanPlaceCommand, AddPlanPlaceResponse
from app.api.errors.api_error import PlaceNotFoundApiError, PlanNotFoundApiError
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddPlanPlaceUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddPlanPlaceCommand) -> AddPlanPlaceResponse:
        async with self._uow.begin():

            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            try:
                place = await self._uow.place_repository.get(cmd.place_id)
            except RepositoryNotFoundException:
                raise PlaceNotFoundApiError

            plan.add_place(place)
            await self._uow.plan_repository.save(plan)

        return AddPlanPlaceResponse()
