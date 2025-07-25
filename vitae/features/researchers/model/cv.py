from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Final, Self

import attrs

from .titles import AcademicTitles

if TYPE_CHECKING:
    from vitae.infra.database import tables


@attrs.frozen
class FullName:
    _value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value

    @cached_property
    def value(self) -> str:
        """The name itself."""
        return self._value.title()

    @cached_property
    def each(self) -> list[str]:
        """Each Researcher's name individually."""
        return self.value.split(" ")

    @cached_property
    def first(self) -> str:
        """Researcher's first name."""
        return self.each[0]

    @cached_property
    def surname(self) -> str:
        """Researcher's last surname."""
        return self.each[-1]

    @cached_property
    def initials(self) -> str:
        """Researcher's name initials."""
        return self.first[0] + self.surname[0]


@attrs.frozen
class Nationality:
    """Researcher's Nationality."""

    value: str

    @classmethod
    def from_table(cls, table: tables.Nationality) -> Self:
        """Build itself from database's row.

        Returns
        -------
        A new Nationality domain class.

        """
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
    """Curriculum's Abstract."""

    text: str
    brief_limit: Final[int] = 50

    @property
    def brief(self) -> str:
        """Formated Abstract's brief, given `brief_limit`."""
        limit = self.brief_limit

        words = self.text.split()
        brief_text = " ".join(words[:limit])

        if len(words) > limit:
            return f"{brief_text}..."

        return brief_text


@attrs.frozen
class Curriculum:
    """Researcher's Lattes curriculum."""

    name: FullName
    titles: AcademicTitles
    nationality: Nationality
    abstract: Abstract

    @classmethod
    def from_table(cls, researcher: tables.Researcher) -> Self:
        """Build itself from a database's row.

        Returns
        -------
        A new Curriculum class.

        """
        return cls(
            name=FullName(researcher.full_name),
            titles=AcademicTitles.from_tables(researcher.education),
            nationality=Nationality.from_table(researcher.nationality),
            abstract=Abstract(researcher.abstract or ""),
        )
