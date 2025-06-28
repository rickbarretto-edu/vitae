"""Academic Adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import uuid

from vitae.infra.database import tables

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .institution import Institution

__all__ = ["Education", "StudyField"]


@dataclass
class Education:
    """Researcher's Education.

    For instance: Undergraduee, Master...
    """

    researcher_id: str

    category: str
    course: str | None
    start: int | None
    end: int | None

    institution: Institution
    fields: list[StudyField]

    advisor: str | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid1)

    @property
    def as_table(self) -> tables.Education:
        """Itself as Database Table."""
        return tables.Education(
            id=self.id,
            researcher_id=self.researcher_id,
            institution_id=self.institution.lattes_id,
            category=self.category,
            course=self.course,
            start=self.start,
            end=self.end,
        )

    @property
    def advisor_as_table(self) -> tables.Advisoring | None:
        if not self.advisor:
            return None

        return tables.Advisoring(
            education_id=self.id,
            student_id=self.researcher_id,
            advisor_id=self.advisor,
        )

    @property
    def institution_as_table(self) -> tables.Institution:
        """Its Institution as Database Table."""
        return self.institution.as_table

    @property
    def fields_as_table(self) -> Iterable[tables.StudyField]:
        """Its Study Field as Database Table."""
        return (field.as_table(str(self.id)) for field in self.fields)


@dataclass
class StudyField:
    """Study field of Academic Background."""

    major: str | None
    area: str | None
    sub: str | None
    specialty: str | None

    def as_table(self, education_id: str) -> tables.StudyField:
        """Itself as Database Table."""  # noqa: DOC201
        return tables.StudyField(
            education_id=education_id,
            major=self.major,
            area=self.area,
            sub=self.sub,
            specialty=self.specialty,
        )
