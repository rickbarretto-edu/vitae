"""Domain model for Ingestion feature."""

from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property

from vitae.core import Entity
from vitae.features.ingestion.adapters.schema import (
    AcademicBackground,
    Expertise,
    GeneralData,
    Nationality,
    ProfessionalExperience,
)
from vitae.infra.database import schema as db_schema

__all__ = ["Curriculum"]


@dataclass
class Curriculum(Entity[str]):
    """Mother class to convert XML Schemas to Database schemas."""

    _personal_data: GeneralData
    _nationality: Nationality
    _expertise: Iterator[Expertise]
    _academic_background: Iterator[AcademicBackground]
    _professional_experiences: Iterator[ProfessionalExperience]

    @cached_property
    def id(self) -> str:
        return self._personal_data["lattes_id"]

    @property
    def personal_data(self) -> db_schema.Researcher:
        return db_schema.Researcher(**self._personal_data)

    @property
    def nationality(self) -> db_schema.Nationality:
        return db_schema.Nationality(**self._nationality)

    @property
    def expertise(self) -> Iterator[db_schema.Expertise]:
        return (db_schema.Expertise(**exp) for exp in self._expertise)

    @property
    def academic_background(self) -> Iterator[db_schema.AcademicBackground]:
        return (
            db_schema.AcademicBackground(**background)
            for background in self._academic_background
        )

    @property
    def professional_experiences(
        self,
    ) -> Iterator[db_schema.ProfessionalExperience]:
        return (
            db_schema.ProfessionalExperience(**experience)
            for experience in self._professional_experiences
        )
