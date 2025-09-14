from enum import Enum


class AIServiceEnum(str, Enum):
    OPENAI = "openai"


class MessageType(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
