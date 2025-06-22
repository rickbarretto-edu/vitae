from __future__ import annotations

from dataclasses import dataclass

from vitae.infra.database import schema as db

__all__ = ["Address", "Business", "Experience"]


@dataclass
class Address:
    """Researcher's professional address."""

    researcher_id: str
    business_id: str

    country: str | None
    state: str | None
    city: str | None
    neighborhood: str | None
    cep: str | None
    public_place: str | None

    @property
    def as_table(self) -> db.Address:
        return db.Address(
            researcher_id=self.researcher_id,
            business_id=self.business_id,
            country=self.country,
            state=self.state,
            city=self.city,
            neighborhood=self.neighborhood,
            cep=self.cep,
            public_place=self.public_place,
        )


@dataclass
class Experience:
    """Researcher's professional experience."""

    researcher_id: str
    relationship: str
    start: str | None
    end: str | None
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
