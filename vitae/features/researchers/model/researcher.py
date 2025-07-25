from __future__ import annotations

import attrs

from vitae.infra.database import tables

from ._shared import optional
from .address import Address
from .cv import Curriculum
from .external import Lattes, Orcid


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
    links: ExternalLink
    address: Address
    curriculum: Curriculum

    @classmethod
    def from_table(cls, table: tables.Researcher):
        return cls(
            links=ExternalLink.from_table(table),
            address=Address.from_table(table.address),
            curriculum=Curriculum.from_table(table),
        )
