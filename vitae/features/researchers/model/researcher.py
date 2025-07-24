
import attrs

from .address import Address
from .external import Lattes, Orcid


@attrs.frozen
class ExternalLink:
    lattes: Lattes
    orcid: Orcid

@attrs.frozen
class Researcher:
    links: ExternalLink
    address: Address
