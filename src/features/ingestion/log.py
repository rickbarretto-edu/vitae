from pathlib import Path
from typing import TypedDict


__all__ = ["log_into"]


def log_into[T: TypedDict | dict](data: T, log: Path) -> T:
    with log.open("+a", encoding="utf-8") as file:
        for key, val in data.items():
            print(f"{key}: {val}", file=file)
        print("-" * 80, file=file, flush=True)

    return data
