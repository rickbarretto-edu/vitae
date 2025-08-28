"""Researcher's model related module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import attrs

from vitae.features.researchers.lib import optional
from vitae.features.researchers.model.academic.external import Lattes, Orcid

from .academic import ExternalLinks
from .cv import Curriculum
from .personal import FullName, Nationality, Person
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
        nationality: tables.Nationality | None = None,
        education: list[tables.Education] | None = None,
        expertise: list[tables.Expertise] | None = None,
    ) -> Self:
        """Build itself from a Researcher row.

        Returns
        -------
        Itself.

        """
        return cls(
            this=Person(
                name=FullName(researcher.full_name),
                nationality=Nationality.from_table(some_or(nationality, lambda: researcher.nationality))
            ),
            links=ExternalLinks(
                lattes=Lattes.from_id(researcher.lattes_id),
                orcid=optional(researcher.orcid, Orcid.from_url),
            ),
            professional=ProfessionalLink.from_table(
                some_or(addresss, lambda: researcher.address)
            ),
            curriculum=Curriculum.from_table(
                researcher,
                some_or(education, lambda: researcher.education),
                some_or(expertise, lambda: researcher.expertise),
            ),
        )
