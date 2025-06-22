from __future__ import annotations

from dataclasses import dataclass

from vitae.infra.database import schema as db

__all__ = ["Institution"]


@dataclass
class Institution:
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
