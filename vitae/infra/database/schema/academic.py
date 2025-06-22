from typing import TYPE_CHECKING

from .orm import Orm, foreign, key, link, required_key

if TYPE_CHECKING:
    from .researcher import Researcher

__all__ = ["Education", "Institution", "StudyField"]


class Education(Orm, table=True):
    id: str = required_key()
    researcher_id: str = foreign("researcher.lattes_id")
    institution_id: str = foreign("institution.lattes_id")

    category: str
    course: str | None
    start: int | None
    end: int | None

    researcher: "Researcher" = link("education")
    fields: list["StudyField"] = link("education")


class StudyField(Orm, table=True):
    id: int | None = key()
    education_id: str = foreign("education.id")

    major: str | None
    area: str | None
    sub: str | None
    specialty: str | None

    education: "Education" = link("fields")


class Institution(Orm, table=True):
    lattes_id: str = required_key()

    name: str | None
    country: str | None
    state: str | None
    city: str | None
