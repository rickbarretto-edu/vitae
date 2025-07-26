"""Institution related domain objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.lib import optional

if TYPE_CHECKING:
    from vitae.infra.database import tables


@attrs.frozen
class LinkedInstitution:
    """Researcher's Linked Institution.

    A Researcher may be associated with certain Institution.
    """

    _name: str

    @property
    def name(self) -> str:
        """Formatted Institution's name."""
        return self._name.title()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_table(cls, address: tables.Address) -> Self | None:
        """Linked Institution from given Address.

        Returns
        -------
        Itself if Address has an institution.

        """
        institution_name: str | None = optional(
            address.institution,
            lambda x: x.name,
        )
        return optional(institution_name, cls)
