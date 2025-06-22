from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from vitae.infra.database import schema as db

if TYPE_CHECKING:
    from collections.abc import Iterable
    import uuid

    from .institution import Institution

__all__ = ["Education"]


@dataclass
class Education:
    """Researcher's Education.

    For instance: Undergraduee, Master...
    """

    id: uuid.UUID
    researcher_id: str

    category: str
    course: str | None
    start: int | None
    end: int | None

    institution: Institution
    fields: Iterable[StudyField]

    @property
    def as_table(self) -> db.Education:
        return db.Education(
            id=self.id,
            researcher_id=self.researcher_id,
            category=self.category,
            course=self.course,
            start=self.start,
            end=self.end,
            instituion_id=self.institution.lattes_id,
        )

    @property
    def institution_as_table(self) -> db.Institution:
        return self.institution.as_table

    @property
    def fields_as_table(self) -> Iterable[db.StudyField]:
        return (field.as_table(str(self.id)) for field in self.fields)


@dataclass
class StudyField:
    major: str | None
    area: str | None
    sub: str | None
    specialty: str | None

    def as_table(self, education_id: str) -> db.StudyField:
        return db.StudyField(
            education_id=education_id,
            major=self.major,
            area=self.area,
            sub=self.sub,
            specialty=self.specialty,
        )
