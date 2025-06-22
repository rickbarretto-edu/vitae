"""Professional experience related Database Tables."""

# ruff: noqa: FA102, D101

from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link

if TYPE_CHECKING:
    from .researcher import Researcher

__all__ = ["Address", "Experience"]


class Address(Orm, table=True):
    researcher_id: str = foreign("researcher.lattes_id", primary_key=True)
    institution_id: str | None = foreign("institution.lattes_id")

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
    institution_id: str | None = foreign("institution.lattes_id")

    relationship: str | None
    start: int | None
    end: int | None

    researcher: "Researcher" = link("experience")
