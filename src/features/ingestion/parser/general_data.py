import eliot

from src.features.ingestion.schema import GeneralData

from . import _xml as xml
from ._log import log_parsing

__all__ = ["general_data"]


@eliot.log_call(action_type="parsing")
def general_data(id: str, data: xml.Node) -> GeneralData:
    """Extract general data from the Lattes curriculum XML.

    This function navigates through the provided XML structure to extract
    general information about a researcher, such as their name, birthplace,
    ORCID ID, and professional institution details.

    Returns
    -------
    Researcher's general data.

    """
    resume = data.first("resumo CV")
    professional_address = data.first("endereco").first("endereco profissional")

    return GeneralData(
        id=id,
        name=data["nome completo"],
        city=data["cidade nascimento"],
        state=data["UF nascimento"],
        country=data["pais de nascimento"],
        quotes_names=data["nome em citacoes bibliograficas"],
        orcid=data["ORCID ID"],
        abstract=resume["texto resumo CV RH"],
        professional_institution=professional_address["nome instituicao"],
        institution_state=professional_address["UF"],
        institution_city=professional_address["cidade"],
    )
