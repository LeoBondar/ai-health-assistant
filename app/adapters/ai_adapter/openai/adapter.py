from app.adapters.ai_adapter.base import BaseAIAdapter
from app.adapters.ai_adapter.interface import IAIAdapter
from app.adapters.ai_adapter.schemas import AIAGenAnswerResult, AIAGenTextCommand
from app.infrastructure.http_clients.openai.client import IOpenAIClient
from app.infrastructure.http_clients.openai.schemas import OACGenTextCommand


class OpenAIAdapter(IAIAdapter, BaseAIAdapter):
    def __init__(self, client: IOpenAIClient) -> None:
        self._client = client

    async def gen_answer(self, command: AIAGenTextCommand) -> AIAGenAnswerResult:
        messages = [
            {
                "role": "system",
                "content": """Мои знания актуальны на сентябрь 2025 года.
                        Я принимаю роль специалиста исходя из запроса.
                        Отвечаю на том языке, на котором ко мне обратились.
                        Если я не располагаю знаниями я прогнозирую и импровизирую, но не допускаю ответов о незнании.""",
            }
        ]
        if command.use_context:
            messages.extend(await self._form_context(messages=command.messages))
        else:
            messages.append({"role": "user", "content": command.messages[-1].text})
        response = await self._client.gen_text(command=OACGenTextCommand(messages=messages))

        return AIAGenAnswerResult(
            answer=response.choices[0].message.content,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )
