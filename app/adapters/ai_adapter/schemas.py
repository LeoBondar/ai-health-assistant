from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.dto.message import MessageType


class BaseGenCommand(BaseModel):
    chat_model_name: str


class AIAMessageModel(BaseModel):
    id: UUID | None = None
    text: str
    type: MessageType
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AIAGenTextCommand(BaseGenCommand):
    messages: list[AIAMessageModel]
    preset: str | None = None
    use_context: bool


class AIAGenAnswerResult(BaseModel):
    answer: str
    completion_tokens: int = 0
    prompt_tokens: int = 0


class AIAGetSpeachToTextCommand(BaseGenCommand):
    file: bytes


class AIAGetSpeachToTextResult(BaseModel):
    text: str
