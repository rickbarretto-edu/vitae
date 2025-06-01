import eliot

from src.features.ingestion.schema import ProfessionalExperience

from . import _xml as xml
from ._log import log_parsing

__all__ = ["professional_experiences"]


@eliot.log_call(action_type="parsing")
def professional_experiences(
    id: str,
    data: xml.Node,
) -> list[ProfessionalExperience]:
    """Extract professional experience from the Lattes curriculum.

    This function navigates through the XML structure of a Lattes curriculum
    to extract information about professional experiences.

    Returns
    -------
    Researcher's Professional experiences.

    """
    if (experiences := data.first("atuacoes profissionais")).exists is None:
        return []

    professional_experience: list[ProfessionalExperience] = []
    for experience in experiences.all("atuacao profissional"):
        institution = experience["nome instituicao"]
        links = experience.all("vinculos")

        for link in links:
            if (link_type := link["tipo de vinculo"]) == "LIVRE":
                link_type = link["outro vinculo informado"]

            professional_experience.append(
                ProfessionalExperience(
                    researcher_id=id,
                    institution=institution,
                    employment_relationship=link_type,
                    start_year=xml.as_int(link["ano inicio"]),
                    end_year=xml.as_int(link["ano fim"]),
                ),
            )

    return professional_experience
