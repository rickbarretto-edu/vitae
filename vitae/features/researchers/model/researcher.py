from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from vitae.features.researchers.lib import optional

from .academic import ExternalLinks
from .cv import Curriculum
from .personal import Person
from .professional import Address

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = ["Researcher"]


@attrs.frozen
class Researcher:
    this: Person
    curriculum: Curriculum
    links: ExternalLinks
    address: Address | None

    @classmethod
    def from_table(cls, table: tables.Researcher):
        return cls(
            this=Person.from_table(table),
            links=ExternalLinks.from_table(table),
            address=optional(table.address, Address.from_table),
            curriculum=Curriculum.from_table(table),
        )
