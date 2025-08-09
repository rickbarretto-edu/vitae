from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from vitae.features.researchers.model.researcher import Researcher


@attrs.frozen
class Network:
    """Network of Researchers with a central Researcher.

    On DSA view, this is a graph, where `_of` is the root.
    """

    of: Researcher
    links_to: list[Network]
