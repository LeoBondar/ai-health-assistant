from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Exercise
from app.repositories.exception import RepositoryNotFoundException


class IExerciseRepository(Protocol):
    async def get(self, exercise_id: UUID, with_lock: bool = False) -> Exercise:
        pass

    async def get_all_exercises(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Exercise]:
        pass

    async def save(self, exercise: Exercise) -> None:
        pass


class ExerciseRepository(IExerciseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, exercise_id: UUID, with_lock: bool = True) -> Exercise:
        stmt = select(Exercise).filter_by(id=exercise_id)
        if with_lock:
            stmt = stmt.with_for_update()
        exercise = (await self.session.execute(stmt)).scalar()
        if not exercise:
            raise RepositoryNotFoundException
        return exercise

    async def get_all_exercises(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Exercise]:
        stmt = select(Exercise).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        exercises = (await self.session.execute(stmt)).scalars().all()
        return exercises

    async def save(self, exercise: Exercise) -> None:
        self.session.add(exercise)
