from __future__ import annotations

from dataclasses import dataclass
import enum
from typing import TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from vitae.features.researchers.model.researcher import Researcher
    from vitae.features.researchers.repository.researchers import Researchers


@attrs.frozen
class SortingRule:
    by: SortingGroup
    order: SortingOrder

class SortingGroup(enum.Enum):
    Name = enum.auto()
    Location = enum.auto()
    Institution = enum.auto()


class SortingOrder(enum.Enum):
    Ascendent = enum.auto()
    Descendent = enum.auto()


@dataclass
class SearchResearchers:
    """Researcher's Search use-case.

    Allows the final user to look for Researchers in the database.
    """

    researchers: Researchers

    def query(self, query: str) -> list[Researcher]:
        """Query Researchers automatically by ID or name."""
        if is_lattes_id(query):
            by_id_result = self._by_id(query)
            return [by_id_result] if by_id_result is not None else []

        return self._by_name(query)

    def _by_id(self, id: str) -> Researcher | None:
        return self.researchers.by_id(id)

    def _by_name(self, match: str) -> list[Researcher]:
        return list(self.researchers.by_name(match))


def is_lattes_id(query: str) -> bool:
    return query.isdigit()
