from dataclasses import dataclass

from app.enums.chats import MessageType


@dataclass
class CreateChatDTO:
    user_id: str
    name: str
    use_context: bool


@dataclass
class AddMessageDTO:
    text: str
    type: MessageType


@dataclass
class CreateMessageDTO:
    text: str
    type: MessageType
