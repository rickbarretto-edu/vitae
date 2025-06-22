from __future__ import annotations

from dataclasses import dataclass

from vitae.infra.database import schema as db


@dataclass
class Experience:
    """Researcher's professional experience."""

    researcher_id: str
    relationship: str
    start: str
    end: str
    business: Business

    @property
    def as_table(self) -> db.Experience:
        return db.Experience(
            researcher_id=self.researcher_id,
            business_id=self.business.lattes_id,
            relationship=self.relationship,
            start=self.start,
            end=self.end,
        )

    @property
    def business_as_table(self) -> db.Business:
        return self.business.as_table


@dataclass
class Business:
    """Business Institution."""

    lattes_id: str
    name: str | None
    country: str | None
    state: str | None
    city: str | None

    @property
    def as_table(self) -> db.Business:
        return db.Business(
            lattes_id=self.lattes_id,
            name=self.name,
            country=self.country,
            state=self.state,
            city=self.city,
        )
