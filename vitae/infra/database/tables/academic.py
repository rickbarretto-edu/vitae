"""Academic related Database Tables."""

# ruff: noqa: FA102, D101

from typing import TYPE_CHECKING, Optional

from .orm import Orm, foreign, key, link, required_key

if TYPE_CHECKING:
    from .researcher import Researcher

__all__ = ["Education", "StudyField"]


class Education(Orm, table=True):
    id: str = required_key()
    researcher_id: str = foreign("researcher.lattes_id")
    institution_id: str | None = foreign("institution.lattes_id")

    category: str
    course: str | None
    start: int | None
    end: int | None

    researcher: "Researcher" = link("education")
    fields: list["StudyField"] = link("education")
    advisoring: Optional["Advising"] = link("education")


class StudyField(Orm, table=True):
    id: int | None = key()
    education_id: str = foreign("education.id")

    major: str | None
    area: str | None
    sub: str | None
    specialty: str | None

    education: "Education" = link("fields")


class Advising(Orm, table=True):
    education_id: str = foreign("education.id", primary_key=True)
    student_id: str = foreign("researcher.lattes_id")
    advisor_id: str  # = foreign("researcher.lattes_id")

    education: "Education" = link("advisoring")
    student: "Researcher" = link("student_of", viewonly=True)
    advisor: "Researcher" = link("advisor_of", viewonly=True)
