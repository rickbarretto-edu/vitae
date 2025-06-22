"""Researcher's personal information related Schemas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from vitae.infra.database import tables

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

__all__ = ["Expertise", "Nationality", "Researcher"]


@dataclass
class Researcher:
    """Researcher's personal and general data."""

    lattes_id: str
    full_name: str
    quotes_names: str | None
    orcid: str | None
    abstract: str | None

    nationality: Nationality
    expertise: list[Expertise]

    @property
    def as_table(self) -> tables.Researcher:
        """Itself as database table."""
        return tables.Researcher(
            lattes_id=self.lattes_id,
            full_name=self.full_name,
            quotes_names=self.quotes_names,
            orcid=self.orcid,
            abstract=self.abstract,
        )

    @property
    def nationality_table(self) -> tables.Nationality:
        """It's nationality as database table."""
        return self.nationality.as_table(self.lattes_id)

    @property
    def expertise_tables(self) -> Iterator[tables.Expertise]:
        """It's expertise as database tables."""
        return (
            expertise.as_table(self.lattes_id) for expertise in self.expertise
        )


@dataclass
class Nationality:
    """Researcher's Nationality."""

    born_country: str | None
    nationality: str | None

    def as_table(self, researcher_id: str) -> tables.Nationality:
        """Itself as database table."""  # noqa: DOC201
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
        """Itself as database table."""  # noqa: DOC201
        return tables.Expertise(
            researcher_id=researcher_id,
            major=self.major,
            area=self.area,
            sub=self.sub,
            speciality=self.speciality,
        )
