"""Researcher's professional experience related models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.lib import optional

from .address import Address
from .institution import LinkedInstitution

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = ["Address", "LinkedInstitution", "ProfessionalLink"]


@attrs.frozen
class ProfessionalLink:
    """Researcher's Professional Link.

    A Researcher may work at some Institution
    in some Address.
    """

    address: Address | None
    institution: LinkedInstitution | None

    @classmethod
    def from_table(cls, address: tables.Address) -> Self:
        return cls(
            address=optional(address, Address.from_table),
            institution=optional(address, LinkedInstitution.from_table),
        )
