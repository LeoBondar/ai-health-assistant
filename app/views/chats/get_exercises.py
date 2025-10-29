from sqlalchemy import select

from app.api.chats.schemas import GetExercisesResponse, ExerciseData
from app.persistent.db_schemas.chat import exercise_table
from app.repositories.uow import UnitOfWork


class GetExercisesView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> GetExercisesResponse:
        async with self._uow.begin():
            stmt = select(
                exercise_table.c.id,
                exercise_table.c.name,
                exercise_table.c.description,
            ).limit(limit).offset(offset)

            exercises = (await self._uow.session.execute(stmt)).all()

            return GetExercisesResponse(
                exercises=[
                    ExerciseData(id=exercise.id, name=exercise.name, description=exercise.description)
                    for exercise in exercises
                ]
            )