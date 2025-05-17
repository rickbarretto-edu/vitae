from logging import Logger
from typing import Any, NoReturn


__all__ = ["panic"]


def panic(message: str, *args: Any, logger: Logger | None = None) -> NoReturn:
    """
    Log an error message and raise a RuntimeError to halt execution.

    Parameters
    ----------
    message : str
        The error message to log and raise.
    logger: Logger | None
        The used logger if there is any.

    Raises
    ------
    RuntimeError
        Always raised with the provided message.
    """
    if logger:
        logger.error("PANIC: %s", message, *args)

    raise RuntimeError(message)
