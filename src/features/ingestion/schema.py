"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from typing import TypedDict

__all__ = ["AcademicBackground"]


class GeneralData(TypedDict):
    id: str
    name: str | None
    city: str | None
    state: str | None
    country: str | None
    quotes_names: str | None
    orcid: str | None
    abstract: str | None
    professional_institution: str | None
    institution_state: str | None
    institution_city: str | None


class AcademicBackground(TypedDict):
    researcher_id: str
    type: str
    institution: str | None
    course: str | None
    start_year: int | None
    end_year: int | None


class ProfessionalExperience(TypedDict):
    researcher_id: str
    institution: str | None
    employment_relationship: str | None
    start_year: int | None
    end_year: int | None


class ResearchArea(TypedDict):
    researcher_id: str
    major_knowledge_area: str | None
    knowledge_area: str | None
    sub_knowledge_area: str | None
    specialty: str | None


# TODO Ajustar Areas de Conhecimento
class KnowledgeArea(TypedDict):
    major_area: str | None
    area: str | None
    sub_area: str | None
    specialty: str | None
