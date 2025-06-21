from typing import TYPE_CHECKING

from .orm import Orm, foreign, index, key, link

if TYPE_CHECKING:
    from .researcher import Researcher


class ProfessionalExperience(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.lattes_id")
    researcher: "Researcher" = link("professional_experience")

    institution: str = index()
    employment_relationship: str | None = None
    start_year: int | None = None
    end_year: int | None = None
