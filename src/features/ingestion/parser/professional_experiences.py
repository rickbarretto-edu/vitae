from __future__ import annotations

from typing import Iterator  # noqa: UP035

from src.features.ingestion.parser.schema import ProfessionalExperience

from . import _xml as xml

__all__ = ["professional_experiences"]


def link_kind(link: xml.Node) -> str | None:
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


def professional_experiences(
    researcher_id: str,
    data: xml.Node,
) -> Iterator[ProfessionalExperience]:
    """Extract professional experience from the Lattes curriculum.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about professional experiences.

    Yields
    ------
    Researcher's Professional Experience.

    XML Schema
    ----------

        atuacoes-profissionais: [
            atuacao-profissional: {
                codigo-instituicao: string
                > nome-instituicao: string
                sequencia-atividade: integer
                sequencia-importancia: integer
                vinculos: [
                    sequencia-historico: integer
                    > tipo-de-vinculo: string
                    carga-horaria-semanal: integer
                    flag-dedicacao-exclusiva: boolean
                    mes-inicio: integer
                    > ano-inicio: integer
                    mes-fim: integer
                    > ano-fim: integer
                    outras-informacoes: string
                    flag-vinculo-empregaticio: boolean
                    > outro-vinculo-informado: string
                    outro-enquadramento-funcional-informado: string
                    outro-enquadramento-funcional-informado-ingles: string
                    outras-informacoes-ingles: string
                ]
                ...
            }
        ]

    Notes
    -----
    Choosen schema data are marked with ``>``.

    """
    if not (experiences := data.first("atuacoes profissionais")).exists:
        return

    for experience in experiences.all("atuacao profissional"):
        links: list[xml.Node] = experience.all("vinculos")

        institution = experience["nome instituicao"]
        if institution is None:
            institution = "Unknown Institution"

        for link in links:
            yield ProfessionalExperience(
                researcher_id=researcher_id,
                institution=institution,
                employment_relationship=link_kind(link),
                start_year=xml.as_int(link["ano inicio"]),
                end_year=xml.as_int(link["ano fim"]),
            )
