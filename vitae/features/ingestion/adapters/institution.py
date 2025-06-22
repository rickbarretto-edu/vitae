"""Institution Schemas."""

from __future__ import annotations

from dataclasses import dataclass

from vitae.infra.database import schema as db

__all__ = ["Institution"]


@dataclass
class Institution:
    """Institution is a registered entity on Lattes.

    Institution may be found as `INSTITUICAO-EMPRESA` or `INSTITUICAO`.
    Important information about it may be found
    at `INFORMACAO-ADICIONAL-INSTITUICAO`.

    For what I've been investigating, there is no difference between Business
    and non-Business Institution, so let's consider the same.
    """

    lattes_id: str
    name: str | None
    abbr: str | None
    country: str | None
    state: str | None

    @property
    def as_table(self) -> db.Institution:
        return db.Institution(
            lattes_id=self.lattes_id,
            name=self.name,
            country=self.country,
            state=self.state,
            abbr=self.abbr,
        )
