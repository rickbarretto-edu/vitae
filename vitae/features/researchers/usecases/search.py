from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from vitae.infra.database.tables.researcher import Researcher


class Researcher(Protocol):
    """Placeholder for Researcher entity."""


class Researchers(Protocol):
    """Placeholder for Researcher repository."""

    def by_id(self, id: str) -> Iterable[Researcher]: ...

    def by_name(self, name: str) -> Iterable[Researcher]: ...


@dataclass
class SearchResearchers:
    researchers: Researchers

    def query(self, query: str) -> Iterable[Researcher]:
        return self.by_id(query) if is_lattes_id(query) else self.by_name(query)

    def by_id(self, id: str) -> Iterable[Researcher]:
        return self.researchers.by_id(id)

    def by_name(self, match: str) -> Iterable[Researcher]:
        return self.researchers.by_name(match)


def is_lattes_id(query: str) -> bool:
    return query.isdigit()
