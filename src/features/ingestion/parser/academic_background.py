from typing import Iterator

import eliot

from src.features.ingestion.schema import AcademicBackground

from . import _xml as xml

__all__ = ["academic_background"]


@eliot.log_call(action_type="parsing")
def academic_background(
    researcher_id: str,
    data: xml.Node,
) -> Iterator[AcademicBackground]:
    """Extract academic background information from a Lattes curriculum XML.

    Academic Backgound is a section of general data.
    This contains all the Researcher's academic data such as courses
    and graduations.

    Yields
    ------
    Researcher's Academic backgrounds.

    XML Schema
    ----------
        formacao-academica-titulacao: [
            
        ]

    """
    for background in (
        xml.find(data.element, "formacao academica titulacao") or []
    ):
        yield AcademicBackground(
            researcher_id=researcher_id,
            type=background.tag,
            institution=xml.attribute(background, "nome instituicao"),
            course=xml.attribute(background, "nome curso"),
            start_year=xml.as_int(xml.attribute(background, "ano de inicio")),
            end_year=xml.as_int(xml.attribute(background, "ano de conclusao")),
        )
