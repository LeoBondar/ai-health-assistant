from sqlalchemy import select

from app.api.chats.schemas import GetUserGoalsResponse, UserGoalData
from app.persistent.db_schemas.chat import user_goal_table
from app.repositories.uow import UnitOfWork


class GetUserGoalsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> GetUserGoalsResponse:
        async with self._uow.begin():
            stmt = select(
                user_goal_table.c.id,
                user_goal_table.c.name
            ).limit(limit).offset(offset)

            goals = (await self._uow.session.execute(stmt)).all()

            return GetUserGoalsResponse(
                goals=[
                    UserGoalData(id=goal.id, name=goal.name)
                    for goal in goals
                ]
            )