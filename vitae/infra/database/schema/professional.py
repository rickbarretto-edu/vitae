"""Professional experience related Database Tables."""

# ruff: noqa: FA102, D101

from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link, required_key

if TYPE_CHECKING:
    from .researcher import Researcher

__all__ = ["Address", "Business", "Experience"]


class Address(Orm, table=True):
    researcher_id: str = foreign("researcher.lattes_id")
    business_id: str = foreign("business.lattes_id")

    country: str | None
    state: str | None
    city: str | None
    neighborhood: str | None
    cep: str | None
    public_place: str | None

    researcher: "Researcher" = link("address")


class Experience(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.lattes_id")
    business_id: str = foreign("business.lattes_id")

    relationship: str | None
    start: int | None
    end: int | None

    researcher: "Researcher" = link("experience")


class Business(Orm, table=True):
    lattes_id: str = required_key()

    name: str | None
    country: str | None
    state: str | None
    city: str | None
