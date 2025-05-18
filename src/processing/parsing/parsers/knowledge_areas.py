from typing import TypedDict

import eliot

from src.processing.parsing.logging import log_parsing
from src.processing.parsing import xml


__all__ = ["knowledge_areas", "KnowledgmentArea"]


# TODO Ajustar Areas de Conhecimento
class KnowledgmentArea(TypedDict):
    major_area: str | None
    area: str | None
    sub_area: str | None
    specialty: str | None


@log_parsing("Academic Background")
@eliot.log_call(action_type="parsing")
def knowledge_areas(curriculo: xml.Node) -> list[KnowledgmentArea]:
    """Extracts the areas of expertise from a Lattes curriculum XML.

    This function parses the XML structure of a Lattes curriculum to extract
    information about the researcher's areas of expertise, including the
    major area, area, sub-area, and specialty.

    Parameters
    ----------
    curriculo : xml.Node
        The XML element representing the Lattes curriculum.

    Notes
    -----
    If the "AREAS-DE-ATUACAO" tag is not found in the XML, an empty list is returned.
    In case of an exception during parsing, an error is logged, and an empty list is returned.

    Examples
    --------
    >>> from xml.etree.ElementTree import fromstring
    >>> xml_data = '''
    ... <CURRICULO>
    ...     <AREAS-DE-ATUACAO>
    ...         <AREA-DE-ATUACAO NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas"
    ...                         NOME-DA-AREA-DO-CONHECIMENTO="Matemática"
    ...                         NOME-DA-SUB-AREA-DO-CONHECIMENTO="Álgebra"
    ...                         NOME-DA-ESPECIALIDADE="Teoria dos Grupos"/>
    ...     </AREAS-DE-ATUACAO>
    ... </CURRICULO>
    ... '''
    >>> curriculo = fromstring(xml_data)
    >>> knowledgment_area(curriculo)
    [{'major_area': 'Ciências Exatas',
        'area': 'Matemática',
        'sub_area': 'Álgebra',
        'specialty': 'Teoria dos Grupos'}]
    """

    return [
        {
            "major_area": knowledgement["nome grande area do conhecimento"],
            "area": knowledgement["nome da area do conhecimento"],
            "sub_area": knowledgement["nome da sub-area do conhecimento"],
            "specialty": knowledgement["nome da especialidade"],
        }
        for knowledgement in curriculo.all("areas de atuacao")
    ]
