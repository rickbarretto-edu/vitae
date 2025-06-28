"""Academic related parsing."""

from collections.abc import Iterator
import uuid

from vitae.features.ingestion.adapters import Education
from vitae.features.ingestion.adapters.academic import StudyField

from . import _xml as xml
from .institution import institution_from_xml

__all__ = ["education_from_xml"]


def education_from_xml(
    researcher_id: str,
    document: xml.Node,
) -> Iterator[Education]:
    """Extract education information from a Lattes curriculum XML.

    Yields
    ------
    Researcher's Education Background.

    """
    data = document.first("dados gerais")
    education_summary = data.first("formacao academica titulacao").element

    if education_summary is not None:
        for edu in education_summary:
            education = xml.Node(edu)
            if edu.tag != "FORMACAO-ACADEMICA-TITULACAO":
                yield Education(
                    id=uuid.uuid1(),
                    researcher_id=researcher_id,
                    category=edu.tag,
                    course=education["nome curso"],
                    start=xml.as_int(education["ano de inicio"]),
                    end=xml.as_int(education["ano de conclusao"]),
                    institution=institution_from_xml(
                        education["codigo instituicao"],
                        education["nome instituicao"],
                        document,
                    ),
                    advisor=education["numero id orientador"],
                    fields=list(fields_from_education(education)),
                )


def fields_from_education(education: xml.Node) -> Iterator[StudyField]:
    areas = education.first("areas do conhecimento").element
    if areas is not None:
        for a in areas:
            area = xml.Node(a)
            yield StudyField(
                major=area["nome grande area do conhecimento"],
                area=area["nome da area do conhecimento"],
                sub=area["nome da sub area do conhecimento"],
                specialty=area["nome da especialidade"],
            )
