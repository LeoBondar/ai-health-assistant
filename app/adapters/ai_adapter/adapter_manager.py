from typing import Protocol

from app.adapters.ai_adapter.interface import IAIAdapter
from app.enums.chats import AIServiceEnum


class IAIManager(Protocol):
    def get_ai_adapter(self, service: AIServiceEnum) -> IAIAdapter:
        pass


class AIManager(IAIManager):
    def __init__(
        self,
        openai_adapter: IAIAdapter,
    ):
        self._openai_adapter = openai_adapter

    def get_ai_adapter(self, service: AIServiceEnum) -> IAIAdapter:
        match service:
            case AIServiceEnum.OPENAI:
                return self._openai_adapter
