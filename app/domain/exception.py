from app.utils.exceptions import BaseAppException


class DomainException(BaseAppException):
    message: str


class ExercisePlaceMismatchException(DomainException):
    message = "Exercise place does not match the plan place."
