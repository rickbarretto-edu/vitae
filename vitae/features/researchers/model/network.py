from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.model.academic.external import Lattes
from vitae.features.researchers.model.personal import FullName

if TYPE_CHECKING:
    from vitae.infra.database import tables


@attrs.frozen
class ResearcherAsNode:
    _lattes: Lattes
    _name: FullName

    @property
    def lattes_id(self) -> str:
        return self._lattes.id

    @property
    def name(self) -> str:
        full_name = self._name.each
        return "".join(
            [
                full_name[-1],
                *[name[0] for name in full_name[:-1]],
            ],
        )


@attrs.frozen
class AdvisingLink:
    """Linking between two researchers."""

    student: ResearcherAsNode
    advisor: ResearcherAsNode

    @classmethod
    def from_table(cls, advising: tables.Advising) -> Self | None:
        if (student := advising.student) is None:
            return None

        if (advisor := advising.advisor) is None:
            return None

        return cls(
            student=ResearcherAsNode(
                lattes=Lattes.from_id(student.lattes_id),
                name=FullName(student.full_name),
            ),
            advisor=ResearcherAsNode(
                lattes=Lattes.from_id(advisor.lattes_id),
                name=FullName(advisor.full_name),
            ),
        )


@attrs.frozen
class Network:
    """Network of Researchers with a central Researcher.

    On DSA view, this is a graph, where `_of` is the root.
    """

    of: ResearcherAsNode
    links_to: list[Network]
