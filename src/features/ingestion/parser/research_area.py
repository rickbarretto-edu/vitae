import eliot

from src.features.ingestion.schema import ResearchArea

from . import _xml as xml
from ._log import log_parsing

__all__ = ["research_area"]


@eliot.log_call(action_type="parsing")
def research_area(id: str, data: xml.Node) -> list[ResearchArea]:
    """Extract research areas from the Lattes curriculum XML.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about research areas, including major knowledge
    areas, knowledge areas, sub-knowledge areas, and specialties.

    Returns
    -------
    A collection of Research Areas.

    """
    return [
        ResearchArea(
            researcher_id=id,
            major_knowledge_area=xml.attribute(
                area,
                "nome grande area do conhecimento",
            ),
            knowledge_area=xml.attribute(
                area,
                "nome da area do conhecimento",
            ),
            sub_knowledge_area=xml.attribute(
                area,
                "nome da sub-area do conhecimento",
            ),
            specialty=xml.attribute(area, "nome da especialidade"),
        )
        for area in xml.find(data.element, "areas de atuacao") or []
    ]
