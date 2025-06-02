"""Ingestion's Log utils."""

from pathlib import Path
from typing import TypedDict

__all__ = ["log_into"]

LOG_DIVIDER = "-" * 80


def log_into[T: TypedDict | dict](data: T, log: Path) -> T:
    """Log ``data`` into ``log``.

    Returns
    -------
    The ``data`` itself

    """
    with log.open("+a", encoding="utf-8") as file:
        for key, val in data.items():
            print(f"{key}: {val}", file=file)

        print(LOG_DIVIDER, file=file, flush=True)

    return data
