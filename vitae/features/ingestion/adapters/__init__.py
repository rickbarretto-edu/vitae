"""Adapters are Parsers' Schemas that converts itself to Database Schemas.

The property used for this auto-convertion is `as_table`.
Internal schemas may implement this as a method because this is needed
parent data to complete the Table.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from .academic import Education, StudyField
from .institution import Institution
from .professional import Address, Experience
from .researcher import Expertise, Nationality, Researcher

__all__ = [
    "Address",
    "Education",
    "Experience",
    "Expertise",
    "Institution",
    "Nationality",
    "Researcher",
    "StudyField",
]


@dataclass
class Curriculum:
    researcher: Researcher
    address: Address | None
    education: list[Education]
    experience: list[Experience]

    @cached_property
    def id(self) -> str:
        return self.researcher.lattes_id

    @property
    def all_institutions(self) -> list[Institution]:
        from_address = [self.address.institution] if self.address else []
        from_institutions = [edu.institution for edu in self.education]
        from_experiences = [xp.institution for xp in self.experience]

        return from_address + from_institutions + from_experiences
