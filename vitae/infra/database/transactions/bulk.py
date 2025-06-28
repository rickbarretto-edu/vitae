"""Batch Transaction schemas.

Since this project deals with a lot of data,
this is good to have a Batch structure to fit all together
and send to database.
"""

# ruff: noqa: D101, D105

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field

from sqlmodel import SQLModel

from vitae.infra.database.tables import (
    Address,
    Advisoring,
    Education,
    Experience,
    Expertise,
    Institution,
    Nationality,
    Researcher,
    StudyField,
)

from .base import Transaction

__all__ = [
    "Academic",
    "Curricula",
    "Institutions",
    "Professional",
    "Researchers",
]


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
    advisoring: Iterable[Advisoring] = field(default_factory=list)

    def __iter__(self) -> Iterator[SQLModel]:
        yield from self.education
        yield from self.fields
        yield from self.advisoring


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
