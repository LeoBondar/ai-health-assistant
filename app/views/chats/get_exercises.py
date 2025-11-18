from uuid import UUID

from sqlalchemy import select

from app.api.chats.schemas import ExerciseData, GetExercisesResponse
from app.persistent.db_schemas.chat import exercise_table
from app.repositories.uow import UnitOfWork


class GetExercisesView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int, place_id: UUID | None = None) -> GetExercisesResponse:
        async with self._uow.begin():
            stmt = (
                select(
                    exercise_table.c.id,
                    exercise_table.c.name,
                    exercise_table.c.description,
                )
                .limit(limit)
                .offset(offset)
            )

            if place_id is not None:
                stmt = stmt.where(exercise_table.c.place_id == place_id)

            exercises = (await self._uow.session.execute(stmt)).all()

            return GetExercisesResponse(
                exercises=[
                    ExerciseData(id=exercise.id, name=exercise.name, description=exercise.description)
                    for exercise in exercises
                ]
            )
