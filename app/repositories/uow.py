from contextlib import asynccontextmanager
from typing import AsyncGenerator, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import Database, SessionContext
from app.repositories.chat import ChatRepository, IChatRepository
from app.repositories.disease import DiseaseRepository, IDiseaseRepository
from app.repositories.exercise import ExerciseRepository, IExerciseRepository
from app.repositories.factor import IRiskFactorRepository, RiskFactorRepository
from app.repositories.message import IMessageRepository, MessageRepository
from app.repositories.place import IPlaceRepository, PlaceRepository
from app.repositories.plan import IPlanRepository, PlanRepository
from app.repositories.user_goal import IUserGoalRepository, UserGoalRepository


class IUnitOfWork(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, database: Database, session_context: SessionContext) -> None:
        self._database = database
        self._session_context = session_context

    @property
    def session(self) -> AsyncSession:
        assert self._session_context.session is not None  # nosec
        return self._session_context.session

    @asynccontextmanager
    async def begin(self) -> AsyncGenerator[AsyncSession, None]:
        session = None

        if not self._session_context.session:
            session = self._database.session_factory()
            self._session_context.session = session

        if self.session.in_transaction():
            yield self.session
        else:
            try:
                async with self.session.begin():
                    yield self.session
            finally:
                if session:
                    await session.close()
                self._session_context.close_session()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def chat_repository(self) -> IChatRepository:
        return ChatRepository(self.session)

    @property
    def message_repository(self) -> IMessageRepository:
        return MessageRepository(self.session)

    @property
    def place_repository(self) -> IPlaceRepository:
        return PlaceRepository(self.session)

    @property
    def disease_repository(self) -> IDiseaseRepository:
        return DiseaseRepository(self.session)

    @property
    def exercise_repository(self) -> IExerciseRepository:
        return ExerciseRepository(self.session)

    @property
    def plan_repository(self) -> IPlanRepository:
        return PlanRepository(self.session)

    @property
    def user_goal_repository(self) -> IUserGoalRepository:
        return UserGoalRepository(self.session)

    @property
    def risk_factor_repository(self) -> IRiskFactorRepository:
        return RiskFactorRepository(self.session)
