from dataclasses import dataclass, field
from typing import Callable, Self

from src.lib.functions import also, then


@dataclass(kw_only=True)
class Buffer[T]:
    """Buffer stores data in batch and then flushes it when reaches it's maximum.

    This class is designed to encapsulate the batching and flushing logic,
    reducing boilerplate code and avoiding primitive obsession.

    Why not use lists and manual flushing?
    --------------------------------------
    Manually managing lists, counters, and flush flags across modules
    leads to scattered state and logic, making the code harder to maintain and reason about.
    This approach increases the risk of bugs, such as forgetting to clear the list,
    mishandling the flush condition, or introducing race conditions in concurrent scenarios.

    The older code used this approach, which is harder to reason about,
    since the logic was distributed between two different modules with different purposes.
    """

    data: list[T] = field(default_factory=list)
    max: int = 64
    _on_flush: Callable[[list[T]], None] = lambda xs: None

    def push(self, value: T) -> Self:
        self.data.append(value)

        if len(self) >= self.max:
            self._on_flush(self.data)
            self.data.clear()

        return self

    def on_flush(self, on_flush: Callable[[list[T]], None]) -> Self:
        self._on_flush = on_flush
        return self

    def also(self, on_flush: Callable[[list[T]], None]) -> Self:
        self._on_flush = also(self._on_flush, on_flush)
        return self

    def then(self, on_flush: Callable[[list[T]], None]) -> Self:
        self._on_flush = then(self._on_flush, on_flush)
        return self

    def __len__(self) -> int:
        return len(self.data)
