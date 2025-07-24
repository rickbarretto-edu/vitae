import attrs

from .address import Address
from .cv import Curriculum
from .external import Lattes, Orcid


@attrs.frozen
class ExternalLink:
    lattes: Lattes
    orcid: Orcid

@attrs.frozen
class Researcher:
    links: ExternalLink
    address: Address
    curriculum: Curriculum
