"""Professional Experience's related parsing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from vitae.features.ingestion.adapters import Address, Experience

from . import _xml as xml
from .institution import institution_from_xml

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["address_from_xml", "experience_from_xml"]


def experience_from_xml(
    researcher_id: str,
    document: xml.Node,
) -> Iterator[Experience]:
    """Extract professional experience from the Lattes curriculum.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about professional experiences.

    Yields
    ------
    Researcher's Professional Experience.

    """
    data = document.first("dados gerais")

    if not (experiences := data.first("atuacoes profissionais")).exists:
        return

    for experience in experiences.all("atuacao profissional"):
        links: list[xml.Node] = experience.all("vinculos")

        for link in links:
            yield Experience(
                researcher_id=researcher_id,
                relationship=relationship_from_link(link),
                institution=institution_from_xml(
                    experience["codigo instituicao"],
                    experience["nome instituicao"],
                    document,
                ),
                start=xml.as_int(link["ano inicio"]),
                end=xml.as_int(link["ano fim"]),
            )


def address_from_xml(researcher_id: str, document: xml.Node) -> Address:
    """Extract Researcher's Professional Address from XML.

    Returns
    -------
    Researcher's Address.

    """
    data = document.first("dados gerais")
    addr = data.first("endereco").first("endereco profissional")

    return Address(
        researcher_id=researcher_id,
        country=addr["pais"],
        state=addr["uf"],
        city=addr["cidade"],
        neighborhood=addr["bairro"],
        cep=addr["cep"],
        public_place=addr["logradouro completo"],
        institution=institution_from_xml(
            addr["codigo instituicao empresa"],
            addr["nome instituicao empresa"],
            document,
        ),
    )


def relationship_from_link(link: xml.Node) -> str | None:
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
