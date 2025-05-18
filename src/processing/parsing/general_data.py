from datetime import datetime

import eliot

from src.processing.parsing.logging import log_parsing
from src.processing.parsing import xml


@log_parsing("General Data")
@eliot.log_call(action_type="parsing")
def general_data(data: xml.Node):
    """Extract general data from the Lattes curriculum XML.

    This function navigates through the provided XML structure to extract
    general information about a researcher, such as their name, birthplace,
    ORCID ID, and professional institution details.

    Parameters
    ----------
    curriculum : xml.etree.ElementTree.Element
        The Lattes curriculum XML element representing a researcher's data.

    Returns
    -------
    dict
        A dictionary containing the following keys:
        - 'name' (str or None): Full name of the researcher.
        - 'city' (str or None): Birth city of the researcher.
        - 'state' (str or None): Birth state of the researcher.
        - 'country' (str or None): Birth country of the researcher.
        - 'quotes_names' (str or None): Names used in bibliographic citations.
        - 'orcid' (str or None): ORCID ID of the researcher.
        - 'abstract' (str or None): Abstract text from the researcher's CV.
        - 'professional_institution' (str or None): Name of the professional institution.
        - 'institution_state' (str or None): State of the professional institution.
        - 'institution_city' (str or None): City of the professional institution.

    Raises
    ------
    Exception
        If an error occurs during the extraction process, it is logged, and an
        empty dictionary is returned.
    """

    resume = data.first("resumo CV")
    professional_address = data.first("endereco").first("endereco profissional")

    return {
        "name": data["nome completo"],
        "city": data["cidade nascimento"],
        "state": data["UF nascimento"],
        "country": data["pais de nascimento"],
        "quotes_names": data["nome em citacoes bibliograficas"],
        "orcid": data["ORCID ID"],
        "abstract": resume["texto resumo CV RH"],
        "professional_institution": professional_address["nome instituicao"],
        "institution_state": professional_address["UF"],
        "institution_city": professional_address["cidade"],
    }
