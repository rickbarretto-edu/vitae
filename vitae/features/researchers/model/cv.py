"""Researcher's Curriculum models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.model.academic import (
    Abstract,
    AcademicTitles,
    Expertises,
)

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = [
    "Curriculum",
]


@attrs.frozen
class Curriculum:
    """Researcher's Lattes curriculum."""

    titles: AcademicTitles
    abstract: Abstract
    expertises: Expertises

    @classmethod
    def from_table(cls, researcher: tables.Researcher) -> Self:
        """Build itself from a database's row.

        Returns
        -------
        A new Curriculum class.

        """
        return cls(
            titles=AcademicTitles.from_tables(researcher.education),
            abstract=Abstract(researcher.abstract or ""),
            expertises=Expertises.from_tables(researcher.expertise),
        )
