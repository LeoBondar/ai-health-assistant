from app.api.chats.schemas import AddPlanExerciseCommand, AddPlanExerciseResponse
from app.api.errors.api_error import ExerciseNotFoundApiError, ExercisePlaceMismatchApiError, PlanNotFoundApiError
from app.domain.exception import ExercisePlaceMismatchException
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddPlanExerciseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddPlanExerciseCommand) -> AddPlanExerciseResponse:
        async with self._uow.begin():

            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            try:
                exercise = await self._uow.exercise_repository.get(cmd.exercise_id)
            except RepositoryNotFoundException:
                raise ExerciseNotFoundApiError

            try:
                plan.add_exercise(exercise)
            except ExercisePlaceMismatchException as e:
                raise ExercisePlaceMismatchApiError from e

            await self._uow.plan_repository.save(plan)

        return AddPlanExerciseResponse()
