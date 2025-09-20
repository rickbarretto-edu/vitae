from __future__ import annotations

import enum
from typing import TYPE_CHECKING

import attrs

from vitae.features.researchers.schemes.filters import ChoosenFilters

if TYPE_CHECKING:
    from vitae.features.researchers.model.researcher import Researcher
    from vitae.features.researchers.repository.researchers import Researchers


class SortingOrder(enum.StrEnum):
    Ascendent = "asc"
    Descendent = "desc"


@attrs.frozen
class SearchResearchers:
    """Researcher's Search use-case.

    Allows the final user to look for Researchers in the database.
    """

    researchers: Researchers

    def query(
        self,
        query: str,
        *,
        order_by: SortingOrder | None = None,
        filter_by: ChoosenFilters | None = None,
        page: int | None = 1,
    ) -> list[Researcher]:
        if is_lattes_id(query):
            result = self.researchers.by_id(query)
            return [result] if result else []

        return self.researchers.by_name(
            query,
            researchers=50,
            order_by=order_by.value if order_by else None,
            filter_by=filter_by,
            page=page,
        )


def is_lattes_id(query: str) -> bool:
    return query.isdigit()
