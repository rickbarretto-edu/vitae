from typing import Any, NoReturn

from loguru import logger

__all__ = ["panic", "Panic"]

class Panic(RuntimeError):
    pass


def panic(message: str, *args: Any) -> NoReturn:
    """
    Log an error message and raise a Panic to halt execution.

    Parameters
    ----------
    message : str
        The error message to log and raise.
    logger: Logger | None
        The used logger if there is any.

    Raises
    ------
    Panic
        Always raised with the provided message.
    """
    logger.opt(depth=1).critical(f"PANIC: {message}", *args)
    raise Panic(message)
