from enum import IntEnum

from app.utils.exceptions import BaseAppException


class ErrorCode(IntEnum):
    SUCCESS = 0
    ACCESS_DENIED = 1000
    VALIDATION_ERROR = 2000
    INTERNAL_SERVER_ERROR = 5000


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