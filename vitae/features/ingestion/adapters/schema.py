"""Schema objects to be extracted from the XML files."""

from __future__ import annotations

from typing import TypedDict

__all__ = [
    "AcademicBackground",
    "ProfessionalExperience",
]


class ProfessionalExperience(TypedDict):
    """Researcher's Professional Experience."""

    # Metadata
    researcher_id: str

    institution: str
    employment_relationship: str | None
    start_year: int | None
    end_year: int | None
