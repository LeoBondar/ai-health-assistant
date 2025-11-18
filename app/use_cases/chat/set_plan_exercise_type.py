from uuid import UUID

from app.api.chats.schemas import SetPlanExerciseTypeCommand, SetPlanExerciseTypeResponse
from app.api.errors.api_error import PlaceNotFoundApiError
from app.repositories.uow import UnitOfWork


class SetPlanExerciseTypeUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: SetPlanExerciseTypeCommand) -> SetPlanExerciseTypeResponse:
        async with self._uow.begin():
            plan = await self._uow.plan_repository.get(plan_id=cmd.plan_id)
            if not plan:
                raise PlaceNotFoundApiError

            plan.set_exercise_type(exercise_type=cmd.exercise_type)

        return SetPlanExerciseTypeResponse()
