from functools import wraps
import asyncio
from loguru import logger


def retry_async(
    max_attempts: int = 3,
    delay: float = 1,
    exceptions: tuple[Exception] = (Exception,),
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"All {max_attempts} attempts failed")
                        raise e

                    logger.warning(f"Attempt {attempt}/{max_attempts} failed: {str(e)}")

                    await asyncio.sleep(delay * attempt)  # Экспоненциальная задержка
            raise RuntimeError("Should never reach this line")

        return wrapper

    return decorator
