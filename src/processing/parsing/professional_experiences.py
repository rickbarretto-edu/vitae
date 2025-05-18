from typing import TypedDict

import eliot

from src.processing.parsing.logging import log_parsing
from src.processing.parsing import xml


__all__ = ["professional_experiences"]


@log_parsing("Professional Experience")
@eliot.log_call(action_type="parsing")
def professional_experiences(id: str, data: xml.Node):
    """Extract professional experience from the Lattes curriculum.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about professional experiences.

    Parameters
    ----------
    id : str
        The unique identifier of the researcher.
    data : xml.Node
        The Lattes curriculum XML element representing a researcher's data.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary contains information
        about a professional experience. Each dictionary has the following keys:
        - 'institution' (str or None): Name of the institution.
        - 'employment_relationship' (str or None): Type of employment relationship.
        - 'start_year' (int or None): Start year of the professional experience.
        - 'end_year' (int or None): End year of the professional experience.

    Notes
    -----
    If no professional experiences are found, an empty list is returned.
    In case of an error during extraction, the function logs the error and
    returns an empty list.
    """

    if (experiences := data.first("atuacoes profissionais")).exists is None:
        return []

    professional_experience = []
    for experience in experiences.all("atuacao profissional"):
        institution = experience["nome instituicao"]
        links = experience.all("vinculos")

        for link in links:
            if (link_type := link["tipo de vinculo"]) == "LIVRE":
                link_type = link["outro vinculo informado"]

            professional_experience.append(
                {
                    "researcher_id": id,
                    "institution": institution,
                    "employment_relationship": link_type,
                    "start_year": xml.as_int(link["ano inicio"]),
                    "end_year": xml.as_int(link["ano fim"]),
                }
            )

    return professional_experience
