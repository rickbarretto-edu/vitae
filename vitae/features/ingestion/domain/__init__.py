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
    ResearchArea,
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
    _research_areas: Iterator[ResearchArea]

    @cached_property
    def id(self) -> str:
        return self._personal_data["lattes_id"]

    @property
    def personal_data(self) -> db_schema.Researcher:
        return db_schema.Researcher(**self._personal_data)

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

    @property
    def research_areas(self) -> Iterator[db_schema.ResearchArea]:
        return (db_schema.ResearchArea(**area) for area in self._research_areas)
