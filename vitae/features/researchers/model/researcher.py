"""Researcher's model related module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import attrs

from .academic import ExternalLinks
from .cv import Curriculum
from .personal import Person
from .professional import ProfessionalLink

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = ["Researcher"]


def some_or[T](x: T | None, default: Callable[[], T]) -> T:
    if x is None:
        return default()
    else:
        return x


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
    def from_table(cls, 
        researcher: tables.Researcher,
        addresss: tables.Address | None = None,
        education: list[tables.Education] | None = None,
        expertise: list[tables.Expertise] | None = None,
    ) -> Self:
        """Build itself from a Researcher row.

        Returns
        -------
        Itself.

        """
        return cls(
            this=Person.from_table(researcher),
            links=ExternalLinks.from_table(researcher),
            professional=ProfessionalLink.from_table(
                some_or(addresss, lambda: researcher.address)
            ),
            curriculum=Curriculum.from_table(
                researcher,
                some_or(education, lambda: researcher.education),
                some_or(expertise, lambda: researcher.expertise),
            ),
        )
