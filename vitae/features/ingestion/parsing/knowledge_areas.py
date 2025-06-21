from vitae.features.ingestion.adapters.schema import KnowledgeArea

from . import _xml as xml

__all__ = ["knowledge_areas"]


def knowledge_areas(curriculo: xml.Node) -> list[KnowledgeArea]:
    """Extract the areas of expertise from a Lattes curriculum XML.

    This function parses the XML structure of a Lattes curriculum to extract
    information about the researcher's areas of expertise, including the
    major area, area, sub-area, and specialty.

    Returns
    -------
    Researcher's Knowledge Areas.

    """
    return [
        KnowledgeArea(
            major_area=knowledgement["nome grande area do conhecimento"],
            area=knowledgement["nome da area do conhecimento"],
            sub_area=knowledgement["nome da sub-area do conhecimento"],
            specialty=knowledgement["nome da especialidade"],
        )
        for knowledgement in curriculo.all("areas de atuacao")
    ]
