from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vitae.features.researchers.model.researcher import Researcher
    from vitae.features.researchers.repository.researchers import Researchers


@dataclass
class SearchResearchers:
    """Researcher's Search use-case.

    Allows the final user to look for Researchers in the database.
    """

    researchers: Researchers

    def query(self, query: str) -> list[Researcher]:
        """Query Researchers automatically by ID or name."""
        if is_lattes_id(query):
            by_id_result = self.by_id(query)
            return [by_id_result] if by_id_result is not None else []

        return self.by_name(query)

    def by_id(self, id: str) -> Researcher | None:
        return self.researchers.by_id(id)

    def by_name(self, match: str) -> list[Researcher]:
        return list(self.researchers.by_name(match))


def is_lattes_id(query: str) -> bool:
    return query.isdigit()
