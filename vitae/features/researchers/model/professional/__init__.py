from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.lib import optional

from .address import Address
from .institution import LinkedInstitution

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = [
    "Address",
    "LinkedInstitution",
]


@attrs.frozen
class ProfessionalLink:
    address: Address
    institution: LinkedInstitution

    @classmethod
    def from_table(cls, researcher: tables.Researcher) -> Self:

        return cls(
            address=optional(researcher.address, Address.from_table),
            institution=optional(researcher.address, LinkedInstitution.from_table)
        )
