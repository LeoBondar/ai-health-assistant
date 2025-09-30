from uuid import UUID

from pydantic import Field

from app.enums.chats import MessageType
from app.utils.model import ApiCamelModel


class AddChatCommand(ApiCamelModel):
    name: str | None = Field(None, description="Название чата", min_length=2, max_length=30)
    user_id: str = Field(description="Идентификатор пользователя")
    use_context: bool = Field(True, description="Использовать контекст чата")


class AddChatResponse(ApiCamelModel):
    id: UUID = Field(description="Идентификатор чата")


class ChatData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор чата")
    name: str = Field(description="Название чата")
    plan_id: UUID = Field(description="Идентификатор плана")
    use_context: bool = Field(description="Использовать контекст чата")


class GetChatsResponse(ApiCamelModel):
    chats: list[ChatData] = Field(description="Чаты")


class RiskFactorData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор фактора риска")
    name: str = Field(description="Название фактора риска")


class GetRiskFactorsResponse(ApiCamelModel):
    factors: list[RiskFactorData] = Field(description="Факторы риска")


class AddChatMessageResponse(ApiCamelModel):
    text: str = Field(description="Текст сообщения")


class RiskFactorData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор фактора риска")
    factor: str = Field(description="Название фактора риска")


class DiseaseData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор заболевания")
    name: str = Field(description="Название заболевания")


class UserGoalData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор цели пользователя")
    name: str = Field(description="Название цели пользователя")


class PlaceData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор места")
    name: str = Field(description="Название места")


class GetPlacesResponse(ApiCamelModel):
    places: list[PlaceData] = Field(description="Места")


class ExerciseData(ApiCamelModel):
    id: UUID = Field(description="Идентификатор упражнения")
    name: str = Field(description="Название упражнения")
    type: str = Field(description="Тип упражнения")


class GetPlanInfoResponse(ApiCamelModel):
    id: UUID = Field(description="Идентификатор плана")
    description: str | None = Field(None, description="Описание плана")
    risk_factor: RiskFactorData | None = Field(None, description="Фактор риска")
    disease: DiseaseData | None = Field(None, description="Заболевание")
    user_goal: UserGoalData | None = Field(None, description="Цель пользователя")
    place: PlaceData | None = Field(None, description="Место")
    exercise: ExerciseData | None = Field(None, description="Упражнение")


class AddPlanPlaceCommand(ApiCamelModel):
    plan_id: UUID = Field(description="Идентификатор плана")
    place_id: UUID = Field(description="Идентификатор места")


class AddPlanPlaceResponse(ApiCamelModel):
    ...


class AddPlanFactorCommand(ApiCamelModel):
    plan_id: UUID = Field(description="Идентификатор плана")
    factor_id: UUID = Field(description="Идентификатор фактора риска")


class AddPlanFactorResponse(ApiCamelModel):
    ...


class AddPlanExerciseCommand(ApiCamelModel):
    plan_id: UUID = Field(description="Идентификатор плана")
    exercise_id: UUID = Field(description="Идентификатор упражнения")


class AddPlanExerciseResponse(ApiCamelModel):
    ...


class AddPlanGoalCommand(ApiCamelModel):
    plan_id: UUID = Field(description="Идентификатор плана")
    goal_id: UUID = Field(description="Идентификатор цели пользователя")


class AddPlanGoalResponse(ApiCamelModel):
    ...


class AddPlanDiseaseCommand(ApiCamelModel):
    plan_id: UUID = Field(description="Идентификатор плана")
    name: str = Field(description="Название заболевания", min_length=2, max_length=100)


class AddPlanDiseaseResponse(ApiCamelModel):
    ...
