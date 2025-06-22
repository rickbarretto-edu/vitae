"""Batch Transaction schemas.

Since this project deals with a lot of data,
this is good to have a Batch structure to fit all together
and send to database.
"""

# ruff: noqa: D101

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

__all__ = ["Academic", "Curricula", "Professional", "Researchers"]


class Transaction(abc.ABC):
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
    institutions: Iterable[Institution]

    def __iter__(self) -> Iterator[SQLModel]:
        """Iterate each internal Tables."""  # noqa: DOC402
        yield from self.researchers
        yield from self.academic
        yield from self.professional
        yield from self.institutions
