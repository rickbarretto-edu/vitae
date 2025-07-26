from __future__ import annotations

from typing import TYPE_CHECKING, Final, Self

import attrs

from vitae.features.researchers.model.academic.expertises import Expertises
from vitae.features.researchers.model.academic.titles import AcademicTitles

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = [
    "Abstract",
    "Curriculum",
]


@attrs.frozen
class Abstract:
    """Curriculum's Abstract."""

    _text: str
    _brief_limit: Final[int] = 50

    @property
    def full(self) -> str:
        """Full abstract."""
        return self._text

    @property
    def brief(self) -> str:
        """Brief abstract."""
        limit = self._brief_limit

        words = self._text.split()
        brief_text = " ".join(words[:limit])

        if len(words) > limit:
            return f"{brief_text}..."

        return brief_text


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
            expertises=Expertises(researcher.expertise),
        )
