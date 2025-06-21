from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link, required_key

__all__ = ["Researcher"]

if TYPE_CHECKING:
    from .academic import AcademicBackground
    from .professional import ProfessionalExperience


class Researcher(Orm, table=True):
    lattes_id: str = required_key()

    full_name: str
    quotes_names: str | None
    orcid: str | None
    abstract: str | None

    professional_experience: list["ProfessionalExperience"] = link("researcher")
    academic_background: list["AcademicBackground"] = link("researcher")
    research_area: list["Expertise"] = link("researcher")


class Nationality(Orm, table=True):
    researcher_id: str = foreign("researcher.lattes_id")
    researcher: "Researcher" = link("nationality")

    born_country: str | None
    nationality: str | None


class Expertise(Orm, table=True):
    researcher_id: str = foreign("researcher.lattes_id")
    researcher: "Researcher" = link("research_area")

    major: str | None = key()
    area: str | None = key()
    sub: str | None = key()
    specialty: str | None = key()
