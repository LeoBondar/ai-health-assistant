from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.dto.chat import (
    AddDiseaseDTO,
    AddExerciseDTO,
    AddFactorDTO,
    AddMessageDTO,
    AddPlaceDTO,
    AddUserGoalDTO,
    CreateChatDTO,
    CreateDiseaseDTO,
    CreateExerciseDTO,
    CreateFactorDTO,
    CreateMessageDTO,
    CreatePlaceDTO,
    CreatePlanDTO,
    CreateUserGoalDTO,
)
from app.enums.chats import MessageType
from app.utils.datetime import get_now_w_tz


@dataclass
class Message:
    id: UUID
    text: str
    type: MessageType
    created_at: datetime = field(default_factory=get_now_w_tz)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateMessageDTO) -> "Message":
        return cls(
            id=uuid4(),
            text=dto.text,
            type=dto.type,
        )


@dataclass
class RiskFactor:
    id: UUID
    factor: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateFactorDTO) -> "RiskFactor":
        return cls(id=uuid4(), factor=dto.factor)


@dataclass
class Disease:
    id: UUID
    name: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateDiseaseDTO) -> "Disease":
        return cls(id=uuid4(), name=dto.name)


@dataclass
class UserGoal:
    id: UUID
    name: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateUserGoalDTO) -> "UserGoal":
        return cls(id=uuid4(), name=dto.name)


@dataclass
class Place:
    id: UUID
    name: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreatePlaceDTO) -> "Place":
        return cls(id=uuid4(), name=dto.name)


@dataclass
class Exercise:
    id: UUID
    name: str
    type: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreateExerciseDTO) -> "Exercise":
        return cls(id=uuid4(), name=dto.name, type=dto.type)


@dataclass
class Plan:
    id: UUID
    chat_id: UUID
    risk_factor: RiskFactor | None = None
    disease: Disease | None = None
    user_goal: UserGoal | None = None
    place: Place | None = None
    exercise: Exercise | None = None
    description: str | None = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, dto: CreatePlanDTO) -> "Plan":
        return cls(id=uuid4(), chat_id=dto.chat_id)

    def add_risk_factor(self, risk_factor: RiskFactor) -> None:
        self.risk_factor = risk_factor

    def add_disease(self, dto: AddDiseaseDTO) -> None:
        self.disease = Disease.create(dto=CreateDiseaseDTO(name=dto.name))

    def add_user_goal(self, goal: UserGoal) -> None:
        self.user_goal = goal

    def add_place(self, place: Place) -> None:
        self.place = place

    def add_exercise(self, exercise: Exercise) -> None:
        self.exercise = exercise


@dataclass
class Chat:
    id: UUID
    user_id: str
    name: str
    plan: "Plan"
    use_context: bool = True
    plan_id: UUID | None = None
    messages: list[Message] = field(default_factory=list)

    @classmethod
    def create(cls, dto: CreateChatDTO) -> "Chat":
        plan = Plan.create(
            dto=CreatePlanDTO(
                chat_id=uuid4(),
            )
        )
        return cls(id=uuid4(), user_id=dto.user_id, name=dto.name, use_context=dto.use_context, plan=plan)

    def add_message(self, dto: AddMessageDTO) -> None:
        self.messages.append(Message.create(CreateMessageDTO(text=dto.text, type=dto.type)))
