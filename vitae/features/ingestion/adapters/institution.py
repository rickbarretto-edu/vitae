"""Institution Schemas."""

from __future__ import annotations

import dataclasses as dt
import uuid

from vitae.infra.database import tables

__all__ = ["Institution"]


@dt.dataclass
class Institution:
    """Institution is a registered entity on Lattes.

    Institution may be found as `INSTITUICAO-EMPRESA` or `INSTITUICAO`.
    Important information about it may be found
    at `INFORMACAO-ADICIONAL-INSTITUICAO`.

    For what I've been investigating, there is no difference between Business
    and non-Business Institution, so let's consider the same.
    """

    lattes_id: str | None
    name: str | None
    abbr: str | None
    country: str | None
    state: str | None

    @property
    def as_table(self) -> tables.Institution:
        """Itself as a Databse Schema."""
        return tables.Institution(
            lattes_id=self.lattes_id,
            name=self.name,
            country=self.country,
            state=self.state,
            abbr=self.abbr,
        )
