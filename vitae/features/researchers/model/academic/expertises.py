"""Expertise related models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

if TYPE_CHECKING:
    from collections.abc import Iterable

    from vitae.infra.database import tables


@attrs.frozen
class Expertises:
    """Researcher's expertises.

    Observation
    -----------
    Expertise doesn't have `speciality` field such as StudyField does.
    This is a rule imposed by Lattes own layout.
    """

    _each: list[StudyField]

    @property
    def specialities(self) -> Iterable[str]:
        """List of Researcher's specialities."""
        return (x.specialization for x in self._each)

    @classmethod
    def from_tables(cls, expertises: list[tables.Expertise]) -> Self:
        return cls(
            [StudyField(e.major, e.area, e.sub, None) for e in expertises],
        )


@attrs.frozen
class StudyField:
    """Classification of a Study Field."""

    _broad_field: str | None
    _area: str | None
    _sub_area: str | None
    _focus: str | None

    @property
    def taxonomy(self) -> Iterable[str]:
        """Taxonomy of a Study Field in order, from the broadest."""
        each = [self._broad_field, self._area, self._sub_area, self._focus]
        normalized = [level.title() for level in each if level is not None]
        return (item for item in normalized)

    @property
    def specialization(self) -> str:
        """The most specific domain in the study field classification."""
        return list(self.taxonomy)[-1]
