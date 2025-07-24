from __future__ import annotations

from typing import Callable

def optional[E, T](
    entry: E | None,
    expression: Callable[[E], T],
) -> T | None:
    if entry is None:
        return None
    try:
        return expression(entry)
    except:  # noqa: E722
        return None
