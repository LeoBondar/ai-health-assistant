from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Chat
from app.repositories.exception import RepositoryNotFoundException


class IChatRepository(Protocol):
    async def get(self, chat_id: UUID, with_lock: bool = True, user_id: UUID | None = None) -> Chat:
        pass

    async def save(self, chat: Chat) -> None:
        pass

    async def delete(self, chat: Chat) -> None:
        pass


class ChatRepository(IChatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, chat_id: UUID, with_lock: bool = True, user_id: UUID | None = None) -> Chat:
        stmt = select(Chat).filter_by(id=chat_id)
        if user_id:
            stmt = stmt.filter_by(user_id=user_id)
        if with_lock:
            stmt = stmt.with_for_update()
        chat = (await self.session.execute(stmt)).scalar()
        if not chat:
            raise RepositoryNotFoundException
        return chat

    async def save(self, chat: Chat) -> None:
        self.session.add(chat)

    async def delete(self, chat: Chat) -> None:
        await self.session.delete(chat)
