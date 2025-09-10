from app.utils.exceptions import BaseAppException


class DomainException(BaseAppException):
    message: str