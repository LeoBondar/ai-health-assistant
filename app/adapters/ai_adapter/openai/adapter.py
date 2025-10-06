from app.adapters.ai_adapter.base import BaseAIAdapter
from app.adapters.ai_adapter.interface import IAIAdapter
from app.adapters.ai_adapter.schemas import AIAGenAnswerResult, AIAGenTextCommand, AIAGenPlanResponse, AIAGenPlanCommand
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
                        Если я не располагаю знаниями я прогнозирую и импровизирую, но не допускаю ответов о незнании.
                        Ты должен объяснять людям и помогать им с их рисками сердечного приступа,
                        снизу пример формы по которой ты должен общаться.
                        
                        1.	Помочь поставить цель, предложив варианты
                        a.	У тебя есть следующие факторы риска… Хочешь составим план и начнем работать над каким-то из них?
                        b.	Отлично, ты бы хотел увеличить физическую активность. Это отличный способ не только улучшить самочувствие и настроение, а также завести новые знакомства, испытать новые ощущения, найти новое увлечение. 
                        c.	Давай определим какой вариант тебе может подойти
                        i.	Занятия в зале
                        1.	Кардиотренировки – это …, лучше всего подходя для… Примеры…
                        2.	Силовые тренировки – это…, ….
                        3.	Упражнения для улучшения гибкости, расслабления мышц - …
                        ii.	Что можно делать дома
                        1.	Занятия на тренажере
                        2.	Комплекс кардио упражнений
                        iii.	Если у меня есть ограничения из-за травмы/заболевания
                        1.	Какое состояние?
                        2.	Тебе может подойти…
                        iv.	Что можно делать для увеличения физической активности если у меня нет времени (посмотреть, что предложит гпт)
                        1.	Можно подниматься по лестнице несколько этажей вместо лифта
                        2.	Выйти на одну остановку раньше из автобуса и пройти быстрым шагом…
                        3.	Прогулка хотя бы 30 мин, желательно со спусками и подъёмами
                        v.	Составить план персональных тренировок в зале/дома
                        d.	Ты выбрал …. Хочешь помогу найти зал для …, выбрать (тренажер, снаряжение gear)  для занятия …., составить план тренировки дома (тип, утром/вечером, сколько по времени, раз в неделю)
                        e.	Как сделать так, чтобы регулярные занятия были выполнимыми, и приносили радость и удовлетворение.
                        i.	Объясняем, что нужно выработать привычку, добавить приятные ништяки (примеры), облегчить первый шаг и постараться сделать его неизбежным, составить план и подготовить что-то, что поддержит в момент, когда необходимо преодолеть нежелание – купить абонемент, попросить поддержку со стороны, хорошо представить положительные результаты (пример Шварценеггера, который детально и ярко визуализировал свои победы)
                        ii.	Выберем, что конкретно нас поддержит в выполнении плана, выберем первый шаг
                        1.	Купить абонемент
                        2.	Записаться на групповые занятия/ занятия с тренером
                        3.	Сходить на тренировку с другом/коллегой
                        4.	Подготовим любимый музыкальный трек
                        5.	Попросим друга/партнера/… напомнить
                        6.	…
                        iii.	Установим напоминания?
                        1.	Выбрать частоту
                        2.	Поддерживающие напоминания
                        a.	Коррекция плана
                        i.	Спросить через несколько дней – Тебе удалось … (нужно где-то подтвердить выбор первого шага для активности – записаться в клуб или составить план индивидуальных занятий и установить дату первого или попробовать что-то из минимальных активностей в течение дня)
                        ii.	Если, ответ да, то поддержать и спросить, как это было?
                        iii.	Если нет, то спросить чего не хватило, что не получилось. Предложить установить дату новой попытки или выбрать что-то другое
                        """,
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


    async def gen_plan(self, command: AIAGenPlanCommand) -> AIAGenPlanResponse:
        messages = [
            {
                "role": "system",
                "content": f"""My knowledge is current as of September 2025.
                        I take on the role of a specialist based on the request.
                        I respond in the language I am addressed in.
                        If I lack knowledge, I predict and improvise, but I do not allow responses about not knowing.
                        I receive the following information about a person as input:
                        1) Risk factor: {command.risk_factor}
                        2) Disease: {command.disease}
                        3) Goal: {command.user_goal}
                        4) Place: {command.place}
                        5) Exercise: {command.exercise}
                        
                        Based on this, I must create a future work plan. I should specify when, how much, and with what intensity a person should work to achieve their goals.
                        All information is output in Telegram format (so use appropriate markup)
                        """,
            }
        ]
        response = await self._client.gen_text(command=OACGenTextCommand(messages=messages))

        return AIAGenPlanResponse(
            description=response.choices[0].message.content,
        )