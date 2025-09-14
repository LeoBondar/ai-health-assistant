from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.dto.chat import AddMessageDTO, CreateChatDTO, CreateMessageDTO
from app.enums.chats import MessageType
from app.utils.datetime import get_now_w_tz


@dataclass
class Message:
    id: UUID
    text: str
    type: MessageType
    created_at: datetime = field(default_factory=get_now_w_tz)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateMessageDTO) -> "Message":
        return cls(
            id=uuid4(),
            text=dto.text,
            type=dto.type,
        )


@dataclass
class Chat:
    id: UUID
    user_id: str
    name: str
    use_context: bool = True

    @classmethod
    def create(cls, dto: CreateChatDTO) -> "Chat":
        return cls(id=uuid4(), user_id=dto.user_id, name=dto.name, use_context=dto.use_context)

    def add_message(self, dto: AddMessageDTO) -> None:
        self.messages.append(Message.create(CreateMessageDTO(text=dto.text, type=dto.type)))
