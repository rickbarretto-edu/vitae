from typing import TypedDict

import eliot

from src.processing.parsing.logging import log_parsing
from src.processing.parsing import xml


__all__ = ["research_area"]


@log_parsing("Research Area")
@eliot.log_call(action_type="parsing")
def research_area(id: str, data: xml.Node):
    """Extract research areas from the Lattes curriculum XML.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about research areas, including major knowledge
    areas, knowledge areas, sub-knowledge areas, and specialties.

    Parameters
    ----------
    curriculum : xml.etree.ElementTree.Element
        The Lattes curriculum XML element.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary contains information
        about a research area with the following keys:
        - 'major_knowledge_area' (str or None): The name of the major knowledge area.
        - 'knowledge_area' (str or None): The name of the knowledge area.
        - 'sub_knowledge_area' (str or None): The name of the sub-knowledge area.
        - 'specialty' (str or None): The name of the specialty.

    Notes
    -----
    If no research areas are found, an empty list is returned. In case of an
    error during extraction, the function logs the error and returns an empty list.

    Examples
    --------
    >>> curriculum = ET.parse("lattes.xml").getroot()
    >>> parser = LattesParser()
    >>> research_areas = parser.research_area(curriculum)
    >>> print(research_areas)
    [{'major_knowledge_area': 'Engineering', 'knowledge_area': 'Civil Engineering',
        'sub_knowledge_area': 'Structural Engineering', 'specialty': 'Concrete Structures'}, ...]
    """

    return [
        {
            "researcher_id": id,
            "major_knowledge_area": xml.attribute(
                area, "nome grande area do conhecimento"
            ),
            "knowledge_area": xml.attribute(
                area, "nome da area do conhecimento"
            ),
            "sub_knowledge_area": xml.attribute(
                area, "nome da sub-area do conhecimento"
            ),
            "specialty": xml.attribute(area, "nome da especialidade"),
        }
        for area in xml.find(data.element, "areas de atuacao") or []
    ]
