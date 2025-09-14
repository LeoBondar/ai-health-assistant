from typing import Any

from openai import BaseModel


class OACGenTextCommand(BaseModel):
    messages: list[dict[str, Any]]
