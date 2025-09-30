from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import UserGoal
from app.repositories.exception import RepositoryNotFoundException


class IUserGoalRepository(Protocol):
    async def get(self, user_goal_id: UUID, with_lock: bool = False) -> UserGoal:
        pass

    async def get_all_user_goals(self, chat_id: UUID, with_lock: bool = True) -> Sequence[UserGoal]:
        pass

    async def save(self, user_goal: UserGoal) -> None:
        pass


class UserGoalRepository(IUserGoalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, user_goal_id: UUID, with_lock: bool = True) -> UserGoal:
        stmt = select(UserGoal).filter_by(id=user_goal_id)
        if with_lock:
            stmt = stmt.with_for_update()
        user_goal = (await self.session.execute(stmt)).scalar()
        if not user_goal:
            raise RepositoryNotFoundException
        return user_goal

    async def get_all_user_goals(self, chat_id: UUID, with_lock: bool = True) -> Sequence[UserGoal]:
        stmt = select(UserGoal).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        user_goals = (await self.session.execute(stmt)).scalars().all()
        return user_goals

    async def save(self, user_goal: UserGoal) -> None:
        self.session.add(user_goal)
