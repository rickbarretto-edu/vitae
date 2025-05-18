import eliot

from src.processing.proxies import AcademicBackground
from src.processing.parsing.logging import log_parsing
from src.processing.parsing import xml


__all__ = ["academic_background"]


@log_parsing("Academic Background")
@eliot.log_call(action_type="parsing")
def academic_background(id: str, data: xml.Node) -> list[AcademicBackground]:
    """Extracts academic background information from a Lattes curriculum XML.

    This function navigates through the XML tags of a Lattes curriculum to extract
    information about the academic background of a researcher.

    Parameters
    ----------
    curriculum : xml.etree.ElementTree.Element
        The Lattes curriculum of a researcher in XML format.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary contains information about
        an academic background. Each dictionary includes the following keys:
        - 'type' (str): The type of academic background (e.g., undergraduate, master's, etc.).
        - 'institution' (str or None): The name of the institution.
        - 'course' (str or None): The name of the course.
        - 'start_year' (int or None): The year the course started.
        - 'end_year' (int or None): The year the course ended.

    Notes
    -----
    If no academic background information is found, an empty list is returned.
    Any errors during extraction are logged, and an empty list is returned in case of exceptions.
    """

    return [
        {
            "researcher_id": id,
            "type": bg.tag,
            "institution": xml.attribute(bg, "nome instituicao"),
            "course": xml.attribute(bg, "nome curso"),
            "start_year": xml.as_int(xml.attribute(bg, "ano de inicio")),
            "end_year": xml.as_int(xml.attribute(bg, "ano de conclusao")),
        }
        for bg in xml.find(data.element, "formacao academica titulacao") or []
    ]
