from typing import Any

from openai import BaseModel


class OACGenTextCommand(BaseModel):
    chat_model_name: str
    messages: list[dict[str, Any]]


class OACGenSpeachToTextCommand(BaseModel):
    file: bytes
    chat_model_name: str
