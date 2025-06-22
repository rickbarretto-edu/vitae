from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link, required_key

__all__ = ["Researcher"]

if TYPE_CHECKING:
    from .academic import Education
    from .professional import Address, Experience


class Researcher(Orm, table=True):
    lattes_id: str = required_key()

    full_name: str
    quotes_names: str | None
    orcid: str | None
    abstract: str | None

    address: "Address" = link("researcher")
    nationality: "Nationality" = link("researcher")

    expertise: list["Expertise"] = link("researcher")
    experience: list["Experience"] = link("researcher")
    education: list["Education"] = link("researcher")


class Nationality(Orm, table=True):
    researcher_id: str = foreign("researcher.lattes_id", primary_key=True)

    born_country: str | None
    nationality: str | None

    researcher: "Researcher" = link("nationality")


class Expertise(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.lattes_id")

    major: str | None
    area: str | None
    sub: str | None
    specialty: str | None

    researcher: "Researcher" = link("expertise")
