from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.chats import MessageType


class AIAMessageModel(BaseModel):
    id: UUID | None = None
    text: str
    type: MessageType
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AIAGenTextCommand(BaseModel):
    messages: list[AIAMessageModel]
    use_context: bool


class AIAGenAnswerResult(BaseModel):
    answer: str
    completion_tokens: int = 0
    prompt_tokens: int = 0
