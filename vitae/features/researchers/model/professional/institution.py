from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

if TYPE_CHECKING:
    from vitae.infra.database import tables


@attrs.frozen
class LinkedInstitution:
    _name: str

    @property
    def name(self) -> str:
        return self._name.title()
    
    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_table(cls, address: tables.Address) -> Self:
        return cls(address.institution.name)
