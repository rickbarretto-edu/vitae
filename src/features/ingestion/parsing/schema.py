"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from typing import TypedDict

__all__ = [
    "AcademicBackground",
    "GeneralData",
    "KnowledgeArea",
    "ProfessionalExperience",
    "ResearchArea",
]


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
