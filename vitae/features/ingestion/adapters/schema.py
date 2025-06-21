"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from typing import TypedDict

__all__ = [
    "AcademicBackground",
    "Expertise",
    "GeneralData",
    "KnowledgeArea",
    "Nationality",
    "ProfessionalExperience",
    "ResearchArea",
]


class GeneralData(TypedDict):
    """Researcher's personal and general data."""

    lattes_id: str
    full_name: str
    quotes_names: str | None
    orcid: str | None
    abstract: str | None


class Nationality(TypedDict):
    """Researcher's Nationality."""

    researcher_id: str
    born_country: str | None
    nationality: str | None


class Expertise(TypedDict):
    """Researcher's Expertise."""

    researcher_id: str
    major: str | None
    area: str | None
    sub: str | None
    speciality: str | None


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
