from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Message
from app.repositories.exception import RepositoryNotFoundException


class IMessageRepository(Protocol):
    async def get(self, message_id: UUID, with_lock: bool = False) -> Message:
        pass

    async def get_all_messages(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Message]:
        pass

    async def save(self, message: Message) -> None:
        pass


class MessageRepository(IMessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, message_id: UUID, with_lock: bool = True) -> Message:
        stmt = select(Message).filter_by(id=message_id)
        if with_lock:
            stmt = stmt.with_for_update()
        message = (await self.session.execute(stmt)).scalar()
        if not message:
            raise RepositoryNotFoundException
        return message

    async def get_all_messages(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Message]:
        stmt = select(Message).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        messages = (await self.session.execute(stmt)).scalars().all()
        return messages

    async def save(self, message: Message) -> None:
        self.session.add(message)
