"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from typing import TypedDict

from src.core import Entity
from src.infra.database import schema as db_schema

__all__ = [
    "AcademicBackground",
    "GeneralData",
    "KnowledgeArea",
    "ProfessionalExperience",
    "ResearchArea",
]


@dataclass
class Curriculum(Entity[str]):
    """Mother class to convert XML Schemas to Database schemas."""

    _personal_data: GeneralData
    _academic_background: Iterator[AcademicBackground]
    _professional_experiences: Iterator[ProfessionalExperience]
    _research_areas: Iterator[ResearchArea]

    @cached_property
    def id(self) -> str:
        return self._personal_data["id"]

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


class GeneralData(TypedDict):
    """Researcher's personal and general data.

    Note:
    ----
    ``id`` is provided by the Lattes curriculum.

    """

    # Metadata
    id: str

    # Researcher's personal data
    name: str
    city: str | None
    state: str | None
    country: str | None

    # Researcher's CV data
    quotes_names: str | None
    orcid: str | None
    abstract: str | None

    # Researcher's Instituition
    professional_institution: str | None
    institution_state: str | None
    institution_city: str | None


class AcademicBackground(TypedDict):
    """Researcher's Academic Background.

    For instance: Undergraduee, Master...
    """

    # Metadata
    researcher_id: str

    type: str
    institution: str
    course: str | None
    start_year: int | None
    end_year: int | None


class ProfessionalExperience(TypedDict):
    """Researcher's Professional Experience."""

    # Metadata
    researcher_id: str

    institution: str
    employment_relationship: str | None
    start_year: int | None
    end_year: int | None


class ResearchArea(TypedDict):
    """Researcher's Area of Researching."""

    # Metadata
    researcher_id: str

    major_knowledge_area: str | None
    knowledge_area: str | None
    sub_knowledge_area: str | None
    specialty: str | None


# TODO Ajustar Areas de Conhecimento
class KnowledgeArea(TypedDict):
    """Academic Background's Knowledge Area."""

    major_area: str | None
    area: str | None
    sub_area: str | None
    specialty: str | None
