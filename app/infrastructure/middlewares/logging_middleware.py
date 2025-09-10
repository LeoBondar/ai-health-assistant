import datetime
import time
from types import TracebackType
from uuid import uuid4

import loguru
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class Measure:
    def __init__(self) -> None:
        self._start: float | None = None

    def __enter__(self) -> "Measure":
        self._start = time.monotonic()
        return self

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def get_elapsed(self) -> datetime.timedelta:
        if self._start is None:
            raise RuntimeError("Time measure not started")
        return datetime.timedelta(seconds=time.monotonic() - self._start)

    def get_elapsed_seconds(self) -> float:
        return self.get_elapsed().total_seconds()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Обогащает контекст loguru и логгирует запросы
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        context = {
            "method": request.method,
            "path": request.url.path,
            "query": request.url.query,
            "content_type": request.headers.get("Content-Type"),
            "user_agent": request.headers.get("User-Agent"),
        }

        if request_id := request.headers.get("X-Request-Id"):
            context["X-Request-Id"] = request_id
        else:
            context["X-Request-Id"] = str(uuid4())

        with loguru.logger.contextualize(**context):
            logger = loguru.logger
            logger.info("Request received")

            with Measure() as measurer:
                try:
                    response = await call_next(request)

                except BaseException:
                    logger.opt(exception=True).exception(
                        "Exception raised while processing request",
                        elapsed_sec=measurer.get_elapsed_seconds(),
                    )
                    raise
            response.headers["X-Request-Id"] = context["X-Request-Id"]  # type: ignore
            response.headers["X-Request-Time"] = str(measurer.get_elapsed_seconds())
            logger.info(
                "Request successfully processed",
                elapsed_sec=measurer.get_elapsed_seconds(),
                response_status_code=response.status_code,
            )
            return response


def init_logging_middleware(app: FastAPI) -> None:
    app.add_middleware(LoggingMiddleware)
