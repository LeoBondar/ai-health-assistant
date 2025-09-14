from typing import Any

from app.adapters.ai_adapter.schemas import AIAMessageModel
from app.enums.chats import MessageType


class BaseAIAdapter:
    @staticmethod
    async def _form_context(messages: list[AIAMessageModel]) -> list[dict[str, Any]]:
        context = []
        for msg in messages:
            if msg.type in [
                MessageType.USER,
            ]:
                user_message = {"role": "user", "content": msg.text}
                context.append(user_message)
            elif msg.type in [MessageType.ASSISTANT]:
                context.append(
                    {
                        "role": "assistant",
                        "content": msg.text,
                    }
                )
        return context
