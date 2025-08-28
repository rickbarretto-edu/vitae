from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Protocol

from vitae.features.researchers.repository.filters.cached import FiltersInCache

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = [
    "Filters",
    "FiltersInCache"
]


class Filters(Protocol):
    @cached_property
    def countries(self) -> Sequence[str]: ...
    @cached_property
    def states(self) -> Sequence[str]: ...
    @cached_property
    def titles(self) -> Sequence[str]: ...
    @cached_property
    def expertises(self) -> Sequence[str]: ...
