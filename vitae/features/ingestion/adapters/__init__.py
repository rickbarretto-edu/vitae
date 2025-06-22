"""Adapters are Parsers' Schemas that converts itself to Database Schemas.

The property used for this auto-convertion is `as_table`.
Internal schemas may implement this as a method because this is needed
parent data to complete the Table.
"""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from .academic import Education
from .institution import Institution
from .professional import Address, Experience
from .researcher import Researcher

__all__ = [
    "Address",
    "Education",
    "Experience",
    "Researcher",
]


@dataclass
class Curriculum:
    researcher: Researcher
    address: Address
    education: Iterable[Education]
    experience: Iterable[Experience]

    @property
    def institutions(self) -> Iterator[Institution]:
        yield self.address.institution

        for education in self.education:
            yield education.institution

        for experience in self.experience:
            yield experience.institution
