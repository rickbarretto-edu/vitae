from __future__ import annotations

from typing import TYPE_CHECKING

from vitae.features.ingestion.adapters import Experience

from . import _xml as xml
from .institution import institution

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["experience"]


def relationship(link: xml.Node) -> str | None:
    """Determine the type of professional link.

    If the researcher has a 'LIVRE' (free) link
    and another link type is provided, the other link type will be used.

    Returns
    -------
    The type of professional link as a string, or None if not available.

    """
    link_kind: str | None = link["tipo de vinculo"]
    other_link_kind: str | None = link["outro vinculo informado"]

    if link_kind == "LIVRE" and other_link_kind:
        return other_link_kind

    return link_kind


def experience(
    researcher_id: str,
    data: xml.Node,
) -> Iterator[Experience]:
    """Extract professional experience from the Lattes curriculum.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about professional experiences.

    Yields
    ------
    Researcher's Professional Experience.

    """
    if not (experiences := data.first("atuacoes profissionais")).exists:
        return

    for experience in experiences.all("atuacao profissional"):
        links: list[xml.Node] = experience.all("vinculos")

        for link in links:
            yield Experience(
                researcher_id=researcher_id,
                relationship=relationship(link),
                institution=institution(
                    experience,
                    data.first("informacoes adicionais instituicoes"),
                ),
                start=xml.as_int(link["ano inicio"]),
                end=xml.as_int(link["ano fim"]),
            )
