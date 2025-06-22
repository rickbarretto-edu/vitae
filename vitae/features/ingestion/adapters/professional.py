from __future__ import annotations

from dataclasses import dataclass

from vitae.infra.database import schema as db

from .institution import Institution

__all__ = ["Address", "Experience", "Institution"]


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
        """Itself as a Database Schema."""
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
    relationship: str | None
    start: int | None
    end: int | None
    institution: Institution

    @property
    def as_table(self) -> db.Experience:
        """Itself as Database Schema."""
        return db.Experience(
            researcher_id=self.researcher_id,
            institution_id=self.institution.lattes_id,
            relationship=self.relationship,
            start=self.start,
            end=self.end,
        )

    @property
    def institution_as_table(self) -> db.Institution:
        """Its Institution as Database Schema."""
        return self.institution.as_table
