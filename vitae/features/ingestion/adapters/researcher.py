from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from vitae.infra.database import tables as tables

__all__ = ["Researcher"]


@dataclass
class Researcher:
    """Researcher's personal and general data."""

    lattes_id: str
    full_name: str
    quotes_names: str | None
    orcid: str | None
    abstract: str | None

    nationality: Nationality
    expertise: Iterable[Expertise]

    @property
    def as_table(self) -> tables.Researcher:
        return tables.Researcher(
            lattes_id=self.lattes_id,
            full_name=self.full_name,
            quotes_names=self.quotes_names,
            orcid=self.orcid,
            abstract=self.abstract,
        )

    @property
    def nationality_table(self) -> tables.Nationality:
        return self.nationality.as_table(self.lattes_id)

    @property
    def expertise_tables(self) -> Iterator[tables.Expertise]:
        return (
            expertise.as_table(self.lattes_id) for expertise in self.expertise
        )


@dataclass
class Nationality:
    """Researcher's Nationality."""

    born_country: str | None
    nationality: str | None

    def as_table(self, researcher_id: str) -> tables.Nationality:
        return tables.Nationality(
            researcher_id=researcher_id,
            born_country=self.born_country,
            nationality=self.nationality,
        )


@dataclass
class Expertise:
    """Researcher's Expertise."""

    major: str | None
    area: str | None
    sub: str | None
    speciality: str | None

    def as_table(self, researcher_id: str) -> tables.Expertise:
        return tables.Expertise(
            researcher_id=researcher_id,
            major=self.major,
            area=self.area,
            sub=self.sub,
            speciality=self.speciality,
        )
