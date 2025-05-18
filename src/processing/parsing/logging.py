from functools import wraps
from xml.etree import ElementTree as ET

from loguru import logger

from src.lib.result import Result, catch

__all__ = ["log_parsing"]

def log_parsing(topic: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Parsing {}'s data...", topic)

            result: Result[list | dict, ET.ParseError] = catch(
                lambda: func(*args, **kwargs)
            )

            if result:
                logger.debug("{}'s data successfully extracted.", topic)
                return result.value
            else:
                logger.error(
                    "Error when extracting {}'s data...: {}",
                    topic,
                    str(result.error),
                )
                return_type = func.__annotations__.get("return")
                return [] if isinstance(return_type, list) else {}

        return wrapper

    return decorator
