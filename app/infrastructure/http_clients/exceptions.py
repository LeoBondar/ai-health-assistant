from typing import Any

from app.utils.exceptions import BaseAppException


class HTTPClientException(BaseAppException):
    pass


class HTTPClientTransportException(HTTPClientException):
    pass


class HTTPClientStatusException(HTTPClientException):
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self.body = body
