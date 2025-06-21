from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link

if TYPE_CHECKING:
    from .researcher import Researcher


class AcademicBackground(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.id")
    researcher: "Researcher" = link("academic_background")

    type: str
    institution: str
    course: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    knowledge_area: list["KnowledgeArea"] = link("academic_background")


class KnowledgeArea(Orm, table=True):
    id: int | None = key()
    academic_background_id: int = foreign("academic_background.id")
    academic_background: "AcademicBackground" = link("knowledge_area")

    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
