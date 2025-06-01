from __future__ import annotations

from functools import wraps
from pathlib import Path
import pprint
from typing import Any, TypedDict

from loguru import logger

from src.lib.result import Result, catch

from ._xml import ParsingError

__all__ = ["log_parsing"]


def log_parsing(topic: str):  # noqa: ANN202
    def decorator(func):  # noqa: ANN202
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN202
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


def log_into[T: TypedDict | dict](data: T, log: Path) -> T:
    with log.open("+a", encoding="utf-8") as file:
        for key, val in data.items():
            print(f"{key}: {val}", file=file)
        print("-" * 80, file=file, flush=True)

    return data
