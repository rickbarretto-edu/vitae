"""Researcher's related parsing."""

from collections.abc import Iterator

from vitae.features.ingestion.adapters import (
    Expertise,
    Nationality,
    Researcher,
)

from . import _xml as xml

__all__ = ["researcher_from_xml"]


def researcher_from_xml(researcher_id: str, data: xml.Node) -> Researcher:
    """Extract general data from the Lattes curriculum XML.

    This function navigates through the provided XML structure to extract
    general information about a researcher, such as their name, birthplace,
    ORCID ID, and professional institution details.

    Returns
    -------
    Researcher's general data.

    """
    resume = data.first("resumo CV")

    return Researcher(
        lattes_id=researcher_id,
        full_name=data["nome completo"] or "Invalid Name",
        quotes_names=data["nome em citacoes bibliograficas"],
        orcid=data["ORCID ID"],
        abstract=resume["texto resumo CV RH"],
        nationality=nationality_from_xml(data),
        expertise=list(expertise_from_xml(data)),
    )


def nationality_from_xml(data: xml.Node) -> Nationality:
    return Nationality(
        born_country=data["pais-de-nascimento"],
        nationality=data["nacionalidade"],
    )


def expertise_from_xml(data: xml.Node) -> Iterator[Expertise]:
    areas = data.first("areas-de-atuacao").all("area-de-atuacao")

    return (
        Expertise(
            major=area["nome-grande-area-do-conhecimento"],
            area=area["nome-da-area-do-conhecimento"],
            sub=area["nome-da-sub-area-do-conhecimento"],
            speciality=area["nome-da-especialidade"],
        )
        for area in areas
    )
