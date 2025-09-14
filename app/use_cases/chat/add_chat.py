from app.api.chats.schemas import AddChatCommand, AddChatResponse
from app.domain.chat import Chat
from app.dto.chat import CreateChatDTO
from app.repositories.uow import UnitOfWork


class AddChatUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: AddChatCommand) -> AddChatResponse:
        async with self._uow.begin():
            chat = Chat.create(
                dto=CreateChatDTO(
                    user_id=cmd.user_id,
                    name=cmd.name if cmd.name else "Новый чат",
                    use_context=cmd.use_context,
                )
            )

            await self._uow.chat_repository.save(chat)

        return AddChatResponse(id=chat.id)
