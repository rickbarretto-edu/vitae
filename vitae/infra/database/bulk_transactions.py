"""Batch Transaction schemas.

Since this project deals with a lot of data,
this is good to have a Batch structure to fit all together
and send to database.
"""

# ruff: noqa: D101, D105

import abc
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from sqlmodel import SQLModel

from vitae.infra.database.tables import (
    Address,
    Education,
    Experience,
    Expertise,
    Institution,
    Nationality,
    Researcher,
    StudyField,
)

__all__ = [
    "Academic",
    "Curricula",
    "Institutions",
    "Professional",
    "Researchers",
]


class Transaction(abc.ABC):
    """Database Transaction abstraction.

    This Abstract Class defines the interface and semantic for
    a Database Transaction. As such, internal types are not defines here
    and each subclass is free to implement this on its own way.

    Its internal types may be of any kind,
    but since this is into `database` package, it should, preferably be,
    database's models composition.

    The transaction must define an iteration method `__iter__`
    that iterates over desired types that returns a database model.
    This makes possible for generic database operations
    with multiple models at once.

    Notice that `Transaction`s must define the right order of insertion.

    Examples
    --------
        class Championship(Transaction):
            teams: list[Team]
            referencees: list[Referencee]
            staff: list[Staff]

            def __iter__(self) -> Iterable[SQLModel]:
                yield from self.teams
                yield from self.referencees
                yield from self.staff

        championship = Championship(
            teams=[Team(...), Team(...), Team(...), ...]
            referencees=[Referencee(...), Referencee(...), ...]
            staff=[Staff(...), Staff(...), Staff(...), ...]
        )
        session.add_all(championship)

    """

    @abc.abstractmethod
    def __iter__(self) -> Iterator[SQLModel]:
        pass


@dataclass
class Researchers(Transaction):
    researchers: Iterable[Researcher]
    nationality: Iterable[Nationality]
    expertise: Iterable[Expertise]

    def __iter__(self) -> Iterator[SQLModel]:
        yield from self.researchers
        yield from self.nationality
        yield from self.expertise


@dataclass
class Academic(Transaction):
    education: Iterable[Education]
    fields: Iterable[StudyField]

    def __iter__(self) -> Iterator[SQLModel]:
        yield from self.education
        yield from self.fields


@dataclass
class Professional(Transaction):
    experience: Iterable[Experience]
    address: Iterable[Address]

    def __iter__(self) -> Iterator[SQLModel]:
        yield from self.experience
        yield from self.address


@dataclass
class Curricula(Transaction):
    researchers: Researchers
    academic: Academic
    professional: Professional

    def __iter__(self) -> Iterator[SQLModel]:
        yield from self.researchers
        yield from self.academic
        yield from self.professional


@dataclass
class Institutions(Transaction):
    all: Iterable[Institution]

    def __iter__(self) -> Iterator[Institution]:
        yield from self.all
