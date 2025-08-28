from functools import cached_property
from typing import Self

import attrs

from vitae.infra.database import tables

__all__ = [
    "FullName",
    "Nationality",
    "Person",
]


@attrs.frozen
class FullName:
    """Researcher's full name."""

    _value: str

    def __str__(self) -> str:
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

    _value: str

    def __str__(self) -> str:
        return self._value

    @classmethod
    def from_table(cls, table: tables.Nationality) -> Self:
        """Build itself from database's row.

        Returns
        -------
        A new Nationality domain class.

        """
        match table:
            case tables.Nationality(born_country="Brasil", nationality="B"):
                return cls("Brasileiro(a)")
            case tables.Nationality(born_country=born_country, nationality="B"):
                return cls(f"{born_country} (Brasileiro)")
            case tables.Nationality(born_country=born_country, nationality="E"):
                return cls(f"{born_country} (Estrangeiro)")
            case _:
                return cls("")


@attrs.frozen
class Person:
    """Researcher's personal information."""

    name: FullName
    nationality: Nationality

