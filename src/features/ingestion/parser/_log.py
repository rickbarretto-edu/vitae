from functools import wraps
import pprint

from loguru import logger

from src.lib.result import Result, catch

from ._xml import ParsingError

__all__ = ["log_parsing"]


def log_parsing(topic: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Parsing {}'s data...", topic)

            result: Result[list | dict, ParsingError] = catch(
                lambda: func(*args, **kwargs),
            )

            if result:
                logger.debug("{}'s data successfully extracted.", topic)
                logger.trace("Parsed data:\n{}", pprint.pformat(result.value))
                return result.value
            logger.error(
                "Error when extracting {}'s data...: {}",
                topic,
                str(result.error),
            )
            return_type = func.__annotations__.get("return")
            return [] if isinstance(return_type, list) else {}

        return wrapper

    return decorator
