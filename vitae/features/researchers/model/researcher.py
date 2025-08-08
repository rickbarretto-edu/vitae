"""Researcher's model related module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from .academic import ExternalLinks
from .cv import Curriculum
from .personal import Person
from .professional import ProfessionalLink

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = ["Researcher"]


@attrs.frozen
class Researcher:
    """A Lattes Researcher representation.

    Attributes
    ----------
    this
        Researcher's personal data.

    curriculum
        Researcher's curriculum, which includes academic
        and professional experiences.

    links
        Researcher's links to external websites,
        such as Lattes and Orcid.

    professional
        Researcher current professional status.

    """

    this: Person
    curriculum: Curriculum
    links: ExternalLinks
    professional: ProfessionalLink

    @classmethod
    def from_table(cls, table: tables.Researcher) -> Self:
        """Build itself from a Researcher row.

        Returns
        -------
        Itself.

        """
        return cls(
            this=Person.from_table(table),
            links=ExternalLinks.from_table(table),
            professional=ProfessionalLink.from_table(table),
            curriculum=Curriculum.from_table(table),
        )


@attrs.frozen
class Network:
    """Network of Researchers with a central Researcher.

    On DSA view, this is a graph, where `_of` is the root.
    """

    of: Researcher
    links_to: list[Network]

