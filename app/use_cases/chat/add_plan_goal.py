from app.api.chats.schemas import AddPlanGoalCommand, AddPlanGoalResponse
from app.api.errors.api_error import PlanNotFoundApiError, UserGoalNotFoundApiError
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddPlanGoalUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddPlanGoalCommand) -> AddPlanGoalResponse:
        async with self._uow.begin():

            try:
                plan = await self._uow.plan_repository.get(cmd.plan_id)
            except RepositoryNotFoundException:
                raise PlanNotFoundApiError

            try:
                user_goal = await self._uow.user_goal_repository.get(cmd.goal_id)
            except RepositoryNotFoundException:
                raise UserGoalNotFoundApiError

            plan.add_user_goal(user_goal)
            await self._uow.plan_repository.save(plan)

        return AddPlanGoalResponse()
