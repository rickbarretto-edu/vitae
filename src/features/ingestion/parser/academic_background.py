import eliot

from src.features.ingestion.schema import AcademicBackground
from . import _xml as xml
from ._log import log_parsing

__all__ = ["academic_background"]


@eliot.log_call(action_type="parsing")
def academic_background(id: str, data: xml.Node) -> list[AcademicBackground]:
    """Extract academic background information from a Lattes curriculum XML.

    This function navigates through the XML tags of a Lattes curriculum
    to extract information about the academic background of a researcher.

    Returns
    -------
    Researcher's Academic backgrounds.

    """
    return [
        AcademicBackground(
            researcher_id=id,
            type=bg.tag,
            institution=xml.attribute(bg, "nome instituicao"),
            course=xml.attribute(bg, "nome curso"),
            start_year=xml.as_int(xml.attribute(bg, "ano de inicio")),
            end_year=xml.as_int(xml.attribute(bg, "ano de conclusao")),
        )
        for bg in xml.find(data.element, "formacao academica titulacao") or []
    ]
