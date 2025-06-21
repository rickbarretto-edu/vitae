from typing import TYPE_CHECKING

from .orm import Orm, foreign, index, key, link, required_key

__all__ = ["Researcher"]

if TYPE_CHECKING:
    from .academic import AcademicBackground
    from .professional import ProfessionalExperience


class Researcher(Orm, table=True):
    id: str = required_key()

    name: str = index()
    city: str | None = None
    state: str | None = None
    country: str | None = None
    quotes_names: str | None = None
    orcid: str | None = None
    abstract: str | None = None
    professional_institution: str | None = None
    institution_state: str | None = None
    institution_city: str | None = None

    professional_experience: list["ProfessionalExperience"] = link("researcher")
    academic_background: list["AcademicBackground"] = link("researcher")
    research_area: list["ResearchArea"] = link("researcher")


class ResearchArea(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.id")
    researcher: "Researcher" = link("research_area")

    major_knowledge_area: str | None = None
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
