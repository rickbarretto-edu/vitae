"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from typing import TypedDict

__all__ = [
    "AcademicBackground",
    "ProfessionalExperience",
]


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
