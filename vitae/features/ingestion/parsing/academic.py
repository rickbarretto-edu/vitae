from collections.abc import Iterator
import uuid

from vitae.features.ingestion.adapters import Education
from vitae.features.ingestion.adapters.academic import Institution

from . import _xml as xml

__all__ = ["education_from_xml"]


def education_from_xml(
    researcher_id: str,
    data: xml.Node,
) -> Iterator[Education]:
    """Extract education information from a Lattes curriculum XML.

    Yields
    ------
    Researcher's Education Background.

    """
    education_summary = data.first("formacao academica titulacao").element

    if education_summary is not None:
        for edu in education_summary.iter():
            education = xml.Node(edu)

            yield Education(
                id=uuid.uuid1(),
                researcher_id=researcher_id,
                category=edu.tag,
                course=education["nome curso"],
                start=xml.as_int(education["ano de inicio"]),
                end=xml.as_int(education["ano de conclusao"]),
                institution=institution(
                    education,
                    data.first("informacoes adicionais instituicoes"),
                ),
                fields=[],
            )


def institution(education: xml.Node, extra_data: xml.Node) -> Institution:
    lattes_id: str = education["codigo instituicao"] or ""
    found: xml.Node = xml.Node(None)

    for inst in extra_data.all("informacao adicional instituicao"):
        if inst["codigo instituicao"] == lattes_id:
            found = inst
            break

    return Institution(
        lattes_id=lattes_id,
        name=education["nome instituicao"],
        country=found["nome pais instituicao"],
        state=found["sigla uf instituicao"],
        abbr=found["sigla instituicao"],
    )
