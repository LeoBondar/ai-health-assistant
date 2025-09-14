from uuid import UUID

from pydantic import Field

from app.enums.chats import MessageType
from app.utils.model import ApiCamelModel


class AddChatCommand(ApiCamelModel):
    name: str | None = Field(None, description="Название чата", min_length=2, max_length=30)
    user_id: str = Field(description="Идентификатор пользователя")
    use_context: bool = Field(True, description="Использовать контекст чата")


class AddChatResponse(ApiCamelModel):
    id: UUID = Field(description="Идентификатор чата")


class ChatData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор чата")
    name: str = Field(description="Название чата")
    use_context: bool = Field(description="Использовать контекст чата")


class GetChatsResponse(ApiCamelModel):
    chats: list[ChatData] = Field(description="Чаты")


class AddChatMessageResponse(ApiCamelModel):
    text: str = Field(description="Текст сообщения")
