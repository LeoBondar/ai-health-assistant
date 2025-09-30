from uuid import UUID

from sqlalchemy import select

from app.api.chats.schemas import ChatData, GetChatsResponse
from app.persistent.db_schemas.chat import chat_table
from app.repositories.uow import UnitOfWork


class GetChatsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int, user_id: str) -> GetChatsResponse:
        async with self._uow.begin():
            stmt = (
                select(
                    chat_table.c.id,
                    chat_table.c.name,
                    chat_table.c.user_id,
                    chat_table.c.use_context,
                    chat_table.c.plan_id,
                )
                .where(
                    chat_table.c.user_id == user_id,
                )
                .limit(limit)
                .offset(offset)
            )

            chats = (await self._uow.session.execute(stmt)).all()

            return GetChatsResponse(
                chats=[
                    ChatData(
                        id=chat.id,
                        name=chat.name,
                        use_context=chat.use_context,
                        plan_id=chat.plan_id,
                    )
                    for chat in chats
                ]
            )
