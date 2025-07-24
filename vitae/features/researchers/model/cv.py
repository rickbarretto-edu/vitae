from __future__ import annotations

from functools import cached_property
from typing import Final, Self

import attrs

from vitae.infra.database import tables

from .titles import AcademicTitles


@attrs.frozen
class FullName:
    value: str

    @cached_property
    def each(self) -> list[str]:
        return self.value.split(" ")

    @cached_property
    def first(self) -> str:
        return self.each[0]

    @cached_property
    def surname(self) -> str:
        return self.each[-1]

    @cached_property
    def initials(self) -> str:
        return self.first[0] + self.surname[0]


@attrs.frozen
class Nationality:
    value: str

    @classmethod
    def from_table(cls, table: tables.Nationality) -> Self:
        match table:
            case Nationality(born_country="Brasil", nationality="B"):
                return cls("Brasileiro(a)")
            case Nationality(born_country, nationality="B"):
                return cls(f"{born_country} (Brasileiro)")
            case Nationality(born_country, nationality="E"):
                return cls(f"{born_country} (Estranjeito)")
            case _:
                return cls("")


@attrs.frozen
class Abstract:
    text: str
    brief_limit: Final[int] = 50

    @property
    def brief(self) -> str:
        limit = self.brief_limit

        words = self.text.split()
        brief_text = " ".join(words[:limit])

        if len(words) > limit:
            return f"{brief_text}..."

        return brief_text


@attrs.frozen
class Curriculum:
    name: FullName
    titles: AcademicTitles
    nationality: Nationality
    abstract: Abstract

    @classmethod
    def from_table(cls, researcher: tables.Researcher) -> Self:
        return cls(
            name=FullName(researcher.full_name),
            titles=AcademicTitles.from_tables(researcher.education),
            nationality=Nationality.from_table(researcher.nationality),
            abstract=Abstract(researcher.abstract or ""),
        )
