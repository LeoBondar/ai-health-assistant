from contextlib import asynccontextmanager
from typing import AsyncGenerator, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import Database, SessionContext
from app.repositories.chat import ChatRepository, IChatRepository
from app.repositories.message import IMessageRepository, MessageRepository


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
