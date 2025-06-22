"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TypedDict

from src.infra.database import schema as db

__all__ = [
    "AcademicBackground",
    "Expertise",
    "Nationality",
    "ProfessionalExperience",
    "Researcher",
]


# =~=~=~=~=~=~ Researcher ~=~=~=~=~=~=


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
    def as_table(self) -> db.Researcher:
        return db.Researcher(
            lattes_id=self.lattes_id,
            full_name=self.full_name,
            quotes_names=self.quotes_names,
            orcid=self.orcid,
            abstract=self.abstract,
        )

    @property
    def nationality_table(self) -> db.Nationality:
        return self.nationality.as_table(self.lattes_id)

    @property
    def expertise_tables(self) -> Iterator[db.Expertise]:
        return (
            expertise.as_table(self.lattes_id) for expertise in self.expertise
        )


@dataclass
class Nationality:
    """Researcher's Nationality."""

    born_country: str | None
    nationality: str | None

    def as_table(self, researcher_id: str) -> db.Nationality:
        db.Nationality(
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

    def as_table(self, researcher_id: str) -> db.Expertise:
        return db.Expertise(
            researcher_id=researcher_id,
            major=self.major,
            area=self.area,
            sub=self.sub,
            speciality=self.speciality,
        )


class AcademicBackground(TypedDict):
    """Researcher's Academic Background.

    For instance: Undergraduee, Master...
    """

    # Metadata
    researcher_id: str

    type: str
    institution: str
    course: str | None
    start_year: int | None
    end_year: int | None


class ProfessionalExperience(TypedDict):
    """Researcher's Professional Experience."""

    # Metadata
    researcher_id: str

    institution: str
    employment_relationship: str | None
    start_year: int | None
    end_year: int | None
