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
    GetChatsResponse,
    GetPlacesResponse,
    GetRiskFactorsResponse,
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
from app.views.chats.get_chats import GetChatsView
from app.views.chats.get_factors import GetFactorsView
from app.views.chats.get_places import GetPlacesView

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", description="Добавить чат", status_code=201)
@inject
async def add_chat(
    cmd: AddChatCommand,
    chat_add_use_case: AddChatUseCase = Depends(Provide[WebAppContainer.chat_add_use_case]),
) -> ApiResponse[AddChatResponse]:
    result = await chat_add_use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


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
