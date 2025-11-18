from dependency_injector import containers, providers

from app.adapters.ai_adapter.adapter_manager import AIManager, IAIManager
from app.adapters.ai_adapter.openai.adapter import IAIAdapter, OpenAIAdapter
from app.infrastructure.db import Database, SessionContext
from app.infrastructure.http_clients.openai.client import IOpenAIClient, OpenAIClient
from app.repositories.uow import IUnitOfWork, UnitOfWork
from app.settings import Settings
from app.use_cases.chat.add_chat import AddChatUseCase
from app.use_cases.chat.add_message import AddChatMessageUseCase
from app.use_cases.chat.add_plan_disease import AddPlanDiseaseUseCase
from app.use_cases.chat.add_plan_exercise import AddPlanExerciseUseCase
from app.use_cases.chat.add_plan_factor import AddPlanFactorUseCase
from app.use_cases.chat.add_plan_goal import AddPlanGoalUseCase
from app.use_cases.chat.add_plan_place import AddPlanPlaceUseCase
from app.use_cases.chat.delete_chat import DeleteChatUseCase
from app.use_cases.chat.generate_plan import GeneratePlanUseCase
from app.use_cases.chat.set_plan_exercise_type import SetPlanExerciseTypeUseCase
from app.use_cases.chat.update_plan import UpdatePlanUseCase
from app.views.chats.get_chats import GetChatsView
from app.views.chats.get_exercises import GetExercisesView
from app.views.chats.get_factors import GetFactorsView
from app.views.chats.get_places import GetPlacesView
from app.views.chats.get_plan_info import GetPlanInfoView
from app.views.chats.get_user_goals import GetUserGoalsView


class WebAppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api", __name__])
    settings = providers.Singleton(Settings)
    database: providers.Singleton[Database] = providers.Singleton(Database, settings=settings.provided.database)
    session_context = providers.Factory(SessionContext)

    unit_of_work: providers.ContextLocalSingleton[IUnitOfWork] = providers.ContextLocalSingleton(
        UnitOfWork, session_context=session_context, database=database
    )

    # HTTP Clients
    openai_client: providers.Singleton[IOpenAIClient] = providers.Singleton(
        OpenAIClient,
        settings=settings.provided.openai,
        proxy_url=settings.provided.openai.proxy,
    )

    # Adapters
    openai_adapter: providers.Singleton[IAIAdapter] = providers.Singleton(OpenAIAdapter, client=openai_client)

    ai_manager: providers.Singleton[IAIManager] = providers.Singleton(
        AIManager,
        openai_adapter=openai_adapter,
    )

    # UseCase
    chat_add_use_case = providers.Factory(AddChatUseCase, uow=unit_of_work)
    chat_add_message_use_case = providers.Factory(AddChatMessageUseCase, uow=unit_of_work, ai_manager=ai_manager)
    chat_add_plan_factor_use_case = providers.Factory(AddPlanFactorUseCase, uow=unit_of_work)
    chat_add_plan_place_use_case = providers.Factory(AddPlanPlaceUseCase, uow=unit_of_work)
    chat_add_plan_exercise_use_case = providers.Factory(AddPlanExerciseUseCase, uow=unit_of_work)
    chat_add_plan_goal_use_case = providers.Factory(AddPlanGoalUseCase, uow=unit_of_work)
    chat_add_plan_disease_use_case = providers.Factory(AddPlanDiseaseUseCase, uow=unit_of_work)
    chat_generate_plan_use_case = providers.Factory(GeneratePlanUseCase, uow=unit_of_work, ai_manager=ai_manager)
    chat_update_plan_use_case = providers.Factory(UpdatePlanUseCase, uow=unit_of_work, ai_manager=ai_manager)
    chat_delete_chat_use_case = providers.Factory(DeleteChatUseCase, uow=unit_of_work)
    chat_set_plan_exercise_type_use_case = providers.Factory(SetPlanExerciseTypeUseCase, uow=unit_of_work)

    # Views
    chat_get_chats_view = providers.Factory(GetChatsView, uow=unit_of_work)
    chat_get_exercises_view = providers.Factory(GetExercisesView, uow=unit_of_work)
    chat_get_factors_view = providers.Factory(GetFactorsView, uow=unit_of_work)
    chat_get_places_view = providers.Factory(GetPlacesView, uow=unit_of_work)
    chat_get_plan_info_view = providers.Factory(GetPlanInfoView, uow=unit_of_work)
    chat_get_user_goals_view = providers.Factory(GetUserGoalsView, uow=unit_of_work)
