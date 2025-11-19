from enum import IntEnum

from app.utils.exceptions import BaseAppException


class ErrorCode(IntEnum):
    SUCCESS = 0
    ACCESS_DENIED = 1000
    VALIDATION_ERROR = 2000
    INTERNAL_SERVER_ERROR = 5000
    MESSAGE_NOT_FOUND = 3000
    PLAN_NOT_FOUND = 3001
    PLACE_NOT_FOUND = 3002
    RISK_FACTOR_NOT_FOUND = 3003
    EXERCISE_NOT_FOUND = 3004
    USER_GOAL_NOT_FOUND = 3005
    PLAN_DESCRIPTION_EMPTY = 3006


class ApiError(BaseAppException):
    status_code: int
    message: str | None
    error_code: ErrorCode

    def __init__(
        self,
        status_code: int | None = None,
        error_code: ErrorCode | None = None,
        message: str | None = None,
    ):
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code
        if message:
            self.message = message


class BusinessApiError(ApiError):
    pass


class ChatNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.MESSAGE_NOT_FOUND
    message = "Chat not found"


class PlanNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.MESSAGE_NOT_FOUND
    message = "Plan not found"


class PlaceNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.MESSAGE_NOT_FOUND
    message = "Place not found"


class RiskFactorNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.RISK_FACTOR_NOT_FOUND
    message = "Risk factor not found"


class ExerciseNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.EXERCISE_NOT_FOUND
    message = "Exercise not found"


class UserGoalNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.USER_GOAL_NOT_FOUND
    message = "User goal not found"


class PlanDescriptionEmptyApiError(ApiError):
    status_code = 400
    error_code = ErrorCode.PLAN_DESCRIPTION_EMPTY
    message = "Plan description is empty. Generate plan first before updating"


class ExercisePlaceMismatchApiError(ApiError):
    status_code = 400
    error_code = ErrorCode.EXERCISE_NOT_FOUND
    message = "Exercise place does not match the plan place."
