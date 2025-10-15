from uuid import UUID

from app.repositories.uow import UnitOfWork
from app.repositories.exception import RepositoryNotFoundException
from app.api.errors.api_error import ChatNotFoundApiError
from app.api.chats.schemas import DeleteChatResponse

class DeleteChatUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, chat_id: UUID) -> DeleteChatResponse:
        async with self._uow.begin():
            try:
                await self._uow.chat_repository.get(chat_id)
            except RepositoryNotFoundException:
                raise ChatNotFoundApiError
            
            await self._uow.chat_repository.delete(chat_id)
        
        return DeleteChatResponse()
