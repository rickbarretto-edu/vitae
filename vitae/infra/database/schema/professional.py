from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link, required_key

if TYPE_CHECKING:
    from .researcher import Researcher

__all__ = ["Business", "Experience"]


class Experience(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.lattes_id")
    business_id: str = foreign("business.lattes_id")

    relationship: str | None = None
    start: int | None = None
    end: int | None = None

    researcher: "Researcher" = link("experience")


class Business(Orm, table=True):
    lattes_id: str = required_key()

    name: str | None
    country: str | None
    state: str | None
    city: str | None
