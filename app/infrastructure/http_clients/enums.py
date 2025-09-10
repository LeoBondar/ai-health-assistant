from enum import Enum


class HTTPClientRequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
