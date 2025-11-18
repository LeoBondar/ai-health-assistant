from dataclasses import dataclass
from uuid import UUID

from app.enums.chats import MessageType


@dataclass
class CreateChatDTO:
    user_id: str
    name: str
    use_context: bool


@dataclass
class AddMessageDTO:
    text: str
    type: MessageType


@dataclass
class CreateMessageDTO:
    text: str
    type: MessageType


@dataclass
class CreatePlanDTO:
    chat_id: UUID


@dataclass
class CreateFactorDTO:
    factor: str


@dataclass
class CreateDiseaseDTO:
    name: str


@dataclass
class CreateUserGoalDTO:
    name: str


@dataclass
class CreatePlaceDTO:
    name: str


@dataclass
class CreateExerciseDTO:
    name: str
    type: str
    place_id: UUID


@dataclass
class AddFactorDTO:
    factor: str


@dataclass
class AddDiseaseDTO:
    name: str


@dataclass
class AddUserGoalDTO:
    name: str


@dataclass
class AddPlaceDTO:
    name: str


@dataclass
class AddExerciseDTO:
    name: str
    type: str
