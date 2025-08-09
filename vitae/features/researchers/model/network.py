from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from vitae.features.researchers.model.academic.external import Lattes
from vitae.features.researchers.model.personal import FullName

if TYPE_CHECKING:
    from vitae.features.researchers.model.researcher import Researcher


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

    @property
    def lattes_id(self) -> str:
        return self._itself.links.lattes.id


@attrs.frozen
class AdvisingLink:
    """Linking between two researchers."""

    student: ResearcherAsNode
    advisor: ResearcherAsNode


@attrs.frozen
class Network:
    """Network of Researchers with a central Researcher.

    On DSA view, this is a graph, where `_of` is the root.
    """

    of: ResearcherAsNode
    links_to: list[Network]
