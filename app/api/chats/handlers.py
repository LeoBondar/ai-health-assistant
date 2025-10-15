from uuid import UUID
from app.use_cases.chat.delete_chat import DeleteChatUseCase
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Form, Path, Query

from app.api.chats.schemas import (
    AddChatCommand,
    AddChatMessageResponse,
    AddChatResponse,
    AddPlanDiseaseCommand,
    AddPlanDiseaseResponse,
    AddPlanExerciseCommand,
    AddPlanExerciseResponse,
    AddPlanFactorCommand,
    AddPlanFactorResponse,
    AddPlanGoalCommand,
    AddPlanGoalResponse,
    AddPlanPlaceCommand,
    AddPlanPlaceResponse,
    GeneratePlanCommand,
    GeneratePlanResponse,
    GetChatsResponse,
    GetExercisesResponse,
    GetPlacesResponse,
    GetPlanInfoResponse,
    GetRiskFactorsResponse,
    GetUserGoalsResponse,
    UpdatePlanCommand,
    UpdatePlanResponse,
    DeleteChatResponse
)
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.use_cases.chat.add_chat import AddChatUseCase
from app.use_cases.chat.add_message import AddChatMessageUseCase
from app.use_cases.chat.add_plan_disease import AddPlanDiseaseUseCase
from app.use_cases.chat.add_plan_exercise import AddPlanExerciseUseCase
from app.use_cases.chat.add_plan_factor import AddPlanFactorUseCase
from app.use_cases.chat.add_plan_goal import AddPlanGoalUseCase
from app.use_cases.chat.add_plan_place import AddPlanPlaceUseCase
from app.use_cases.chat.generate_plan import GeneratePlanUseCase
from app.use_cases.chat.update_plan import UpdatePlanUseCase
from app.views.chats.get_chats import GetChatsView
from app.views.chats.get_exercises import GetExercisesView
from app.views.chats.get_factors import GetFactorsView
from app.views.chats.get_places import GetPlacesView
from app.views.chats.get_plan_info import GetPlanInfoView
from app.views.chats.get_user_goals import GetUserGoalsView

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", description="Добавить чат", status_code=201)
@inject
async def add_chat(
    cmd: AddChatCommand,
    chat_add_use_case: AddChatUseCase = Depends(Provide[WebAppContainer.chat_add_use_case]),
) -> ApiResponse[AddChatResponse]:
    result = await chat_add_use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.delete("/{chatId}", description="Удалить чат", status_code=204)
@inject
async def delete_chat(
    chat_id: UUID = Path(description="Идентификатор чата", alias="chatId"),
    use_case: DeleteChatUseCase = Depends(Provide[WebAppContainer.chat_delete_chat_use_case]),
) -> ApiResponse[DeleteChatResponse]:
    await use_case(chat_id=chat_id)


@router.get("/", description="Получить чаты")
@inject
async def get_chats(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    user_id: str = Query(description="Идентификатор пользователя", alias="userId", validation_alias="userId"),
    view: GetChatsView = Depends(Provide[WebAppContainer.chat_get_chats_view]),
) -> ApiResponse[GetChatsResponse]:
    result = await view(limit=limit, offset=offset, user_id=user_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/{chatId}/message", description="Добавить сообщение в чат", status_code=201)
@inject
async def add_chat_message(
    text: str = Body(description="Текст сообщения", alias="text"),
    chat_id: UUID = Path(description="Идентификатор чата", alias="chatId"),
    user_id: str = Body(description="Идентификатор пользователя", alias="userId"),
    use_case: AddChatMessageUseCase = Depends(Provide[WebAppContainer.chat_add_message_use_case]),
) -> ApiResponse[AddChatMessageResponse]:
    result = await use_case(text=text, user_id=user_id, chat_id=chat_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/riskFactors", description="Получить факторы риска")
@inject
async def get_risk_factors(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    view: GetFactorsView = Depends(Provide[WebAppContainer.chat_get_factors_view]),
) -> ApiResponse[GetRiskFactorsResponse]:
    result = await view(limit=limit, offset=offset)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/places", description="Получить места")
@inject
async def get_places(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    view: GetPlacesView = Depends(Provide[WebAppContainer.chat_get_places_view]),
) -> ApiResponse[GetPlacesResponse]:
    result = await view(limit=limit, offset=offset)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/exercises", description="Получить упражнения")
@inject
async def get_exercises(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    view: GetExercisesView = Depends(Provide[WebAppContainer.chat_get_exercises_view]),
) -> ApiResponse[GetExercisesResponse]:
    result = await view(limit=limit, offset=offset)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/goals", description="Получить цели пользователя")
@inject
async def get_user_goals(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    view: GetUserGoalsView = Depends(Provide[WebAppContainer.chat_get_user_goals_view]),
) -> ApiResponse[GetUserGoalsResponse]:
    result = await view(limit=limit, offset=offset)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/riskFactor", description="Добавить фактор риска к плану", status_code=201)
@inject
async def add_plan_factor(
    cmd: AddPlanFactorCommand,
    use_case: AddPlanFactorUseCase = Depends(Provide[WebAppContainer.chat_add_plan_factor_use_case]),
) -> ApiResponse[AddPlanFactorResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/place", description="Добавить место к плану", status_code=201)
@inject
async def add_plan_place(
    cmd: AddPlanPlaceCommand,
    use_case: AddPlanPlaceUseCase = Depends(Provide[WebAppContainer.chat_add_plan_place_use_case]),
) -> ApiResponse[AddPlanPlaceResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/exercise", description="Добавить упражнение к плану", status_code=201)
@inject
async def add_plan_exercise(
    cmd: AddPlanExerciseCommand,
    use_case: AddPlanExerciseUseCase = Depends(Provide[WebAppContainer.chat_add_plan_exercise_use_case]),
) -> ApiResponse[AddPlanExerciseResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/goal", description="Добавить цель пользователя к плану", status_code=201)
@inject
async def add_plan_goal(
    cmd: AddPlanGoalCommand,
    use_case: AddPlanGoalUseCase = Depends(Provide[WebAppContainer.chat_add_plan_goal_use_case]),
) -> ApiResponse[AddPlanGoalResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/disease", description="Добавить заболевание к плану", status_code=201)
@inject
async def add_plan_disease(
    cmd: AddPlanDiseaseCommand,
    use_case: AddPlanDiseaseUseCase = Depends(Provide[WebAppContainer.chat_add_plan_disease_use_case]),
) -> ApiResponse[AddPlanDiseaseResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/plans/{planId}", description="Получить информацию о плане")
@inject
async def get_plan_info(
    plan_id: UUID = Path(description="Идентификатор плана", alias="planId"),
    view: GetPlanInfoView = Depends(Provide[WebAppContainer.chat_get_plan_info_view]),
) -> ApiResponse[GetPlanInfoResponse]:
    result = await view(plan_id=plan_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/plans/{planId}/generate", description="Сгенерировать описание плана", status_code=201)
@inject
async def generate_plan(
    plan_id: UUID = Path(description="Идентификатор плана", alias="planId"),
    use_case: GeneratePlanUseCase = Depends(Provide[WebAppContainer.chat_generate_plan_use_case]),
) -> ApiResponse[GeneratePlanResponse]:
    result = await use_case(cmd=GeneratePlanCommand(plan_id=plan_id))
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.put("/plans", description="Обновить описание плана", status_code=200)
@inject
async def update_plan(
    cmd: UpdatePlanCommand,
    use_case: UpdatePlanUseCase = Depends(Provide[WebAppContainer.chat_update_plan_use_case]),
) -> ApiResponse[UpdatePlanResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")
