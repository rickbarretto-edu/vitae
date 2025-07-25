from __future__ import annotations

import attrs

from vitae.infra.database import tables

from ._shared import optional
from .address import Address
from .cv import Curriculum
from .external import Lattes, Orcid
from .personal import Person


@attrs.frozen
class ExternalLink:
    lattes: Lattes
    orcid: Orcid | None

    @classmethod
    def from_table(cls, researcher: tables.Researcher):
        return cls(
            lattes=Lattes.from_id(researcher.lattes_id),
            orcid=optional(researcher.orcid, Orcid.from_url),
        )


@attrs.frozen
class Researcher:
    this: Person
    curriculum: Curriculum
    links: ExternalLink
    address: Address | None

    @classmethod
    def from_table(cls, table: tables.Researcher):
        return cls(
            this=Person.from_table(table),
            links=ExternalLink.from_table(table),
            address=optional(table.address, Address.from_table),
            curriculum=Curriculum.from_table(table),
        )
