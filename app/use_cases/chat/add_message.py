from uuid import UUID

from app.adapters.ai_adapter.adapter_manager import IAIManager
from app.adapters.ai_adapter.schemas import AIAGenTextCommand, AIAMessageModel
from app.api.chats.schemas import AddChatMessageResponse
from app.api.errors.api_error import ChatNotFoundApiError
from app.domain.chat import Message
from app.dto.chat import AddMessageDTO
from app.enums.chats import AIServiceEnum, MessageType
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class AddChatMessageUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        ai_manager: IAIManager,
    ) -> None:
        self._uow = uow
        self._ai_manager = ai_manager

    async def __call__(
        self,
        text: str,
        user_id: str,
        chat_id: UUID,
    ) -> AddChatMessageResponse:
        async with self._uow.begin():

            try:
                chat = await self._uow.chat_repository.get(chat_id=chat_id, user_id=user_id)
            except RepositoryNotFoundException:
                raise ChatNotFoundApiError

            chat.add_message(AddMessageDTO(text=text, type=MessageType.USER))

            ai_adapter = self._ai_manager.get_ai_adapter(service=AIServiceEnum.OPENAI)

            gen_message = await ai_adapter.gen_answer(
                command=AIAGenTextCommand(
                    messages=[
                        AIAMessageModel(
                            id=m.id,
                            text=m.text,
                            type=m.type,
                        )
                        for m in chat.messages
                    ],
                    use_context=chat.use_context,
                )
            )
            chat.add_message(AddMessageDTO(text=gen_message.answer, type=MessageType.ASSISTANT))

            await self._uow.chat_repository.save(chat)

        return AddChatMessageResponse(text=gen_message.answer)
